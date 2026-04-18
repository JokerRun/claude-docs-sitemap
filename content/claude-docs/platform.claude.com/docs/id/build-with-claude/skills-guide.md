---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/skills-guide
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 3ee284fb5fd1145dae97c24d36c1e84df50c893356644a4cde75f0135ebd79bf
---

# Menggunakan Agent Skills dengan API

Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.

---

Agent Skills memperluas kemampuan Claude melalui folder terorganisir yang berisi instruksi, skrip, dan sumber daya. Panduan ini menunjukkan cara menggunakan Skills yang sudah dibuat sebelumnya dan Skills khusus dengan Claude API.

<Note>
Untuk referensi API lengkap termasuk skema permintaan/respons dan semua parameter, lihat:
- [Skill Management API Reference](/docs/id/api/skills/list-skills) - Operasi CRUD untuk Skills
- [Skill Versions API Reference](/docs/id/api/skills/list-skill-versions) - Manajemen versi
</Note>

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Tautan Cepat

<CardGroup cols={2}>
  <Card
    title="Mulai dengan Agent Skills"
    icon="rocket"
    href="/docs/id/agents-and-tools/agent-skills/quickstart"
  >
    Buat Skill pertama Anda
  </Card>
  <Card
    title="Buat Skills Khusus"
    icon="hammer"
    href="/docs/id/agents-and-tools/agent-skills/best-practices"
  >
    Praktik terbaik untuk membuat Skills
  </Card>
</CardGroup>

## Ikhtisar

<Note>
Untuk penjelasan mendalam tentang arsitektur dan aplikasi dunia nyata dari Agent Skills, baca posting blog teknik: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

Skills terintegrasi dengan Messages API melalui alat eksekusi kode. Baik menggunakan Skills yang sudah dibuat sebelumnya yang dikelola oleh Anthropic atau Skills khusus yang telah Anda unggah, bentuk integrasi identik: keduanya memerlukan eksekusi kode dan menggunakan struktur `container` yang sama.

### Menggunakan Skills

Skills terintegrasi secara identik dalam Messages API terlepas dari sumbernya. Anda menentukan Skills dalam parameter `container` dengan `skill_id`, `type`, dan `version` opsional, dan mereka dieksekusi di lingkungan eksekusi kode.

**Anda dapat menggunakan Skills dari dua sumber:**

| Aspek | Anthropic Skills | Custom Skills |
|--------|------------------|---------------|
| **Nilai Type** | `anthropic` | `custom` |
| **Skill IDs** | Nama pendek: `pptx`, `xlsx`, `docx`, `pdf` | Dihasilkan: `skill_01AbCdEfGhIjKlMnOpQrStUv` |
| **Format Versi** | Berbasis tanggal: `20251013` atau `latest` | Epoch timestamp: `1759178010641129` atau `latest` |
| **Manajemen** | Dibuat sebelumnya dan dikelola oleh Anthropic | Unggah dan kelola melalui [Skills API](/docs/id/api/skills/create-skill) |
| **Ketersediaan** | Tersedia untuk semua pengguna | Pribadi untuk workspace Anda |

Kedua sumber skill dikembalikan oleh [endpoint List Skills](/docs/id/api/skills/list-skills) (gunakan parameter `source` untuk memfilter). Bentuk integrasi dan lingkungan eksekusi identik. Satu-satunya perbedaan adalah dari mana Skills berasal dan bagaimana mereka dikelola.

### Prasyarat

Untuk menggunakan Skills, Anda memerlukan:

1. **Kunci API Claude** dari [Console](/settings/keys)
2. **Header beta:**
   - `code-execution-2025-08-25` - Mengaktifkan eksekusi kode (diperlukan untuk Skills)
   - `skills-2025-10-02` - Mengaktifkan Skills API
   - `files-api-2025-04-14` - Untuk mengunggah/mengunduh file ke/dari container
3. **Alat eksekusi kode** diaktifkan dalam permintaan Anda

---

## Menggunakan Skills dalam Messages

### Parameter Container

Skills ditentukan menggunakan parameter `container` dalam Messages API. Anda dapat menyertakan hingga 8 Skills per permintaan.

Strukturnya identik untuk Skills Anthropic dan custom. Tentukan `type` dan `skill_id` yang diperlukan, dan secara opsional sertakan `version` untuk mengikat ke versi tertentu:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-7",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {
          "type": "anthropic",
          "skill_id": "pptx",
          "version": "latest"
        }
      ]
    },
    "messages": [{
      "role": "user",
      "content": "Create a presentation about renewable energy"
    }],
    "tools": [{
      "type": "code_execution_20250825",
      "name": "code_execution"
    }]
  }'
```

```bash CLI
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: pptx
      version: latest
messages:
  - role: user
    content: Create a presentation about renewable energy
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
    },
    messages=[
        {"role": "user", "content": "Create a presentation about renewable energy"}
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "anthropic",
        skill_id: "pptx",
        version: "latest"
      }
    ]
  },
  messages: [
    {
      role: "user",
      content: "Create a presentation about renewable energy"
    }
  ],
  tools: [
    {
      type: "code_execution_20250825",
      name: "code_execution"
    }
  ]
});
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Betas = new[] { "code-execution-2025-08-25", "skills-2025-10-02" },
            Container = new BetaContainerParams
            {
                Skills = new[]
                {
                    new BetaAnthropicSkillParams
                    {
                        Type = "anthropic",
                        SkillId = "pptx",
                        Version = "latest"
                    }
                }
            },
            Messages = new[]
            {
                new BetaMessageParam
                {
                    Role = Role.User,
                    Content = "Create a presentation about renewable energy"
                }
            },
            Tools = new[]
            {
                new BetaCodeExecutionToolParams
                {
                    Type = "code_execution_20250825",
                    Name = "code_execution"
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
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas: []anthropic.AnthropicBeta{
			"code-execution-2025-08-25",
			anthropic.AnthropicBetaSkills2025_10_02,
		},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeAnthropic,
						SkillID: "pptx",
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a presentation about renewable energy")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..4,8..10,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaContainerParams;
import com.anthropic.models.beta.messages.BetaSkillParams;
import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .container(BetaContainerParams.builder()
                .addSkill(BetaSkillParams.builder()
                    .type(BetaSkillParams.Type.ANTHROPIC)
                    .skillId("pptx")
                    .version("latest")
                    .build())
                .build())
            .addUserMessage("Create a presentation about renewable energy")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
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
        ['role' => 'user', 'content' => 'Create a presentation about renewable energy']
    ],
    model: 'claude-opus-4-7',
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: [
        'skills' => [
            [
                'type' => 'anthropic',
                'skill_id' => 'pptx',
                'version' => 'latest'
            ]
        ]
    ],
    tools: [
        ['type' => 'code_execution_20250825', 'name' => 'code_execution']
    ]
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "anthropic",
        skill_id: "pptx",
        version: "latest"
      }
    ]
  },
  messages: [
    { role: "user", content: "Create a presentation about renewable energy" }
  ],
  tools: [
    { type: "code_execution_20250825", name: "code_execution" }
  ]
)
puts message
```
</CodeGroup>

### Mengunduh File yang Dihasilkan

Ketika Skills membuat dokumen (Excel, PowerPoint, PDF, Word), mereka mengembalikan atribut `file_id` dalam respons. Anda harus menggunakan Files API untuk mengunduh file-file ini.

**Cara kerjanya:**
1. Skills membuat file selama eksekusi kode
2. Respons mencakup `file_id` untuk setiap file yang dibuat
3. Gunakan Files API untuk mengunduh konten file sebenarnya
4. Simpan secara lokal atau proses sesuai kebutuhan

**Contoh: Membuat dan mengunduh file Excel**

<Tabs>
<Tab title="Shell">

```bash Shell hidelines={1}
cd "$(mktemp -d)"
# Step 1: Use a Skill to create a file
RESPONSE=$(curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-7",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
      ]
    },
    "messages": [{
      "role": "user",
      "content": "Create an Excel file with a simple budget spreadsheet"
    }],
    "tools": [{
      "type": "code_execution_20250825",
      "name": "code_execution"
    }]
  }')

# Step 2: Extract file_id from response (using jq)
FILE_ID=$(echo "$RESPONSE" | jq -r '.content[] | select(.type=="bash_code_execution_tool_result") | .content | select(.type=="bash_code_execution_result") | .content[] | select(.file_id) | .file_id')

# Step 3: Get filename from metadata
FILENAME=$(curl "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" | jq -r '.filename')

# Step 4: Download the file using Files API
curl "https://api.anthropic.com/v1/files/$FILE_ID/content" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  --output "$FILENAME"

echo "Downloaded: $FILENAME"
```

</Tab>
<Tab title="CLI">

```bash CLI hidelines={1}
cd "$(mktemp -d)"
# Step 1: Use the xlsx Skill to create a file
# Step 2: Extract file_id from the response via --transform (GJSON path)
FILE_ID=$(ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
  --transform 'content.#.content.content.#.file_id|@flatten|0' \
  --format yaml <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: xlsx
      version: latest
messages:
  - role: user
    content: Create an Excel file with a simple budget spreadsheet
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
)

# Step 3: Get the filename from file metadata
FILENAME=$(ant beta:files retrieve-metadata \
  --file-id "$FILE_ID" \
  --transform filename --format yaml)

# Step 4: Download the file using Files API
ant beta:files download \
  --file-id "$FILE_ID" \
  --output "$FILENAME" > /dev/null

printf 'Downloaded: %s\n' "$FILENAME"
```

</Tab>
<Tab title="Python">

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Step 1: Use a Skill to create a file
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
    },
    messages=[
        {
            "role": "user",
            "content": "Create an Excel file with a simple budget spreadsheet",
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)


# Step 2: Extract file IDs from the response
def extract_file_ids(response):
    file_ids = []
    for item in response.content:
        if item.type == "bash_code_execution_tool_result":
            content_item = item.content
            if content_item.type == "bash_code_execution_result":
                for file in content_item.content:
                    if hasattr(file, "file_id"):
                        file_ids.append(file.file_id)
    return file_ids


# Step 3: Download the file using Files API
for file_id in extract_file_ids(response):
    file_metadata = client.beta.files.retrieve_metadata(
        file_id=file_id, betas=["files-api-2025-04-14"]
    )
    file_content = client.beta.files.download(
        file_id=file_id, betas=["files-api-2025-04-14"]
    )

    # Step 4: Save to disk
    file_content.write_to_file(file_metadata.filename)
    print(f"Downloaded: {file_metadata.filename}")
```

</Tab>
<Tab title="TypeScript">

```typescript TypeScript hidelines={1..3}
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs/promises";

const client = new Anthropic();

// Step 1: Use a Skill to create a file
const response = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
  },
  messages: [
    {
      role: "user",
      content: "Create an Excel file with a simple budget spreadsheet"
    }
  ],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});

// Step 2: Extract file IDs from the response
function extractFileIds(response: any): string[] {
  const fileIds: string[] = [];
  for (const item of response.content) {
    if (item.type === "bash_code_execution_tool_result") {
      const contentItem = item.content;
      if (contentItem.type === "bash_code_execution_result") {
        for (const file of contentItem.content) {
          if ("file_id" in file) {
            fileIds.push(file.file_id);
          }
        }
      }
    }
  }
  return fileIds;
}

// Step 3: Download the file using Files API
for (const fileId of extractFileIds(response)) {
  const fileMetadata = await client.beta.files.retrieveMetadata(fileId, {
    betas: ["files-api-2025-04-14"]
  });
  const fileContent = await client.beta.files.download(fileId, {
    betas: ["files-api-2025-04-14"]
  });

  // Step 4: Save to disk
  await fs.writeFile(fileMetadata.filename, Buffer.from(await fileContent.arrayBuffer()));
  console.log(`Downloaded: ${fileMetadata.filename}`);
}
```

</Tab>
<Tab title="C#">

```csharp C# nocheck
using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Collections.Generic;
using Anthropic;
using Anthropic.Models.Beta.Messages;
using Anthropic.Models.Beta.Files;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        // Step 1: Use a Skill to create a file
        var parameters = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Betas = new[] { "code-execution-2025-08-25", "skills-2025-10-02" },
            Container = new BetaContainer
            {
                Skills = new[]
                {
                    new BetaSkill
                    {
                        Type = "anthropic",
                        SkillId = "xlsx",
                        Version = "latest"
                    }
                }
            },
            Messages = new[]
            {
                new BetaMessage
                {
                    Role = Role.User,
                    Content = "Create an Excel file with a simple budget spreadsheet"
                }
            },
            Tools = new[]
            {
                new BetaTool
                {
                    Type = "code_execution_20250825",
                    Name = "code_execution"
                }
            }
        };

        var response = await client.Beta.Messages.Create(parameters);

        // Step 2: Extract file IDs from the response
        var fileIds = ExtractFileIds(response);

        // Step 3: Download the file using Files API
        foreach (var fileId in fileIds)
        {
            var fileMetadata = await client.Beta.Files.RetrieveMetadata(fileId,
                new FileRetrieveMetadataParams
                {
                    Betas = new[] { "files-api-2025-04-14" }
                });

            var fileContent = await client.Beta.Files.Download(fileId,
                new FileDownloadParams
                {
                    Betas = new[] { "files-api-2025-04-14" }
                });

            // Step 4: Save to disk
            await File.WriteAllBytesAsync(fileMetadata.Filename, fileContent);
            Console.WriteLine($"Downloaded: {fileMetadata.Filename}");
        }
    }

    static List<string> ExtractFileIds(BetaMessage response)
    {
        var fileIds = new List<string>();
        foreach (var item in response.Content)
        {
            if (item is BetaBashCodeExecutionToolResult toolResult)
            {
                if (toolResult.Content is BetaBashCodeExecutionResult result)
                {
                    foreach (var content in result.Content)
                    {
                        if (content is BetaBashCodeExecutionResultFile file)
                        {
                            fileIds.Add(file.FileId);
                        }
                    }
                }
            }
        }
        return fileIds;
    }
}
```

</Tab>
<Tab title="Go">

```go Go hidelines={1..15,72..73}
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	// Step 1: Use a Skill to create a file
	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeAnthropic,
						SkillID: "xlsx",
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create an Excel file with a simple budget spreadsheet")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	// Step 2: Extract file IDs from the response
	fileIDs := extractFileIDs(response)

	// Step 3: Download the file using Files API
	for _, fileID := range fileIDs {
		fileMetadata, err := client.Beta.Files.GetMetadata(context.TODO(), fileID, anthropic.BetaFileGetMetadataParams{
			Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
		})
		if err != nil {
			log.Fatal(err)
		}

		fileContent, err := client.Beta.Files.Download(context.TODO(), fileID, anthropic.BetaFileDownloadParams{
			Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
		})
		if err != nil {
			log.Fatal(err)
		}

		// Step 4: Save to disk
		out, err := os.Create(fileMetadata.Filename)
		if err != nil {
			log.Fatal(err)
		}
		io.Copy(out, fileContent.Body)
		out.Close()
		fileContent.Body.Close()
		fmt.Printf("Downloaded: %s\n", fileMetadata.Filename)
	}
}

func extractFileIDs(response *anthropic.BetaMessage) []string {
	var fileIDs []string
	for _, item := range response.Content {
		switch v := item.AsAny().(type) {
		case anthropic.BetaBashCodeExecutionToolResultBlock:
			for _, output := range v.Content.Content {
				if output.FileID != "" {
					fileIDs = append(fileIDs, output.FileID)
				}
			}
		}
	}
	return fileIDs
}
```

</Tab>
<Tab title="Java">

```java Java nocheck hidelines={1..4,8,10..17,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaContainerParams;
import com.anthropic.models.beta.messages.BetaSkillParams;
import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
import com.anthropic.models.beta.messages.BetaContentBlock;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.core.http.HttpResponse;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

public class SkillsFileDownload {
    public static void main(String[] args) throws Exception {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Step 1: Use a Skill to create a file
        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .container(BetaContainerParams.builder()
                .addSkill(BetaSkillParams.builder()
                    .type(BetaSkillParams.Type.ANTHROPIC)
                    .skillId("xlsx")
                    .version("latest")
                    .build())
                .build())
            .addUserMessage("Create an Excel file with a simple budget spreadsheet")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
            .build();

        BetaMessage response = client.beta().messages().create(params);

        // Step 2: Extract file IDs from the response
        List<String> fileIds = new ArrayList<>();
        for (BetaContentBlock block : response.content()) {
            if (block.isCodeExecutionToolResult()) {
                var toolResult = block.asCodeExecutionToolResult();
                for (var content : toolResult.content()) {
                    content.file().ifPresent(file -> fileIds.add(file.fileId()));
                }
            }
        }

        // Step 3: Download the file using Files API
        for (String fileId : fileIds) {
            FileMetadata fileMetadata = client.beta().files().retrieveMetadata(fileId);
            HttpResponse fileContent = client.beta().files().download(fileId);

            // Step 4: Save to disk
            try (InputStream is = fileContent.body();
                 FileOutputStream fos = new FileOutputStream(fileMetadata.filename())) {
                is.transferTo(fos);
            }
            System.out.println("Downloaded: " + fileMetadata.filename());
        }
    }
}
```

</Tab>
<Tab title="PHP">

<Note>
SDK PHP tidak menyertakan metode pengunduhan file. Gunakan `retrieveMetadata()` untuk informasi file, kemudian unduh konten file melalui REST API.
</Note>

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

// Step 1: Use a Skill to create a file
$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Create an Excel file with a simple budget spreadsheet']
    ],
    model: 'claude-opus-4-7',
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: [
        'skills' => [
            ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
        ]
    ],
    tools: [
        ['type' => 'code_execution_20250825', 'name' => 'code_execution']
    ]
);

// Step 2: Extract file IDs from the response
function extractFileIds($response) {
    $fileIds = [];
    foreach ($response->content as $item) {
        if ($item->type === 'bash_code_execution_tool_result') {
            $contentItem = $item->content;
            if ($contentItem->type === 'bash_code_execution_result') {
                foreach ($contentItem->content as $file) {
                    if (isset($file->fileID)) {
                        $fileIds[] = $file->fileID;
                    }
                }
            }
        }
    }
    return $fileIds;
}

// Step 3: Get metadata and download via REST API
$apiKey = getenv("ANTHROPIC_API_KEY");
foreach (extractFileIds($response) as $fileId) {
    $fileMetadata = $client->beta->files->retrieveMetadata(
        fileID: $fileId,
        betas: ['files-api-2025-04-14']
    );

    // Download file content via REST API
    $context = stream_context_create([
        'http' => [
            'header' => implode("\r\n", [
                "x-api-key: $apiKey",
                "anthropic-version: 2023-06-01",
                "anthropic-beta: files-api-2025-04-14",
            ]),
        ],
    ]);
    $fileContent = file_get_contents(
        "https://api.anthropic.com/v1/files/$fileId/content",
        false,
        $context
    );

    // Step 4: Save to disk
    file_put_contents($fileMetadata->filename, $fileContent);
    echo "Downloaded: {$fileMetadata->filename}\n";
}
```

</Tab>
<Tab title="Ruby">

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Step 1: Use a Skill to create a file
response = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
  },
  messages: [
    {
      role: "user",
      content: "Create an Excel file with a simple budget spreadsheet"
    }
  ],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
)

# Step 2: Extract file IDs from the response
def extract_file_ids(response)
  file_ids = []
  response.content.each do |item|
    if item.type == :bash_code_execution_tool_result
      content_item = item.content
      if content_item.type == :bash_code_execution_result
        content_item.content.each do |file|
          file_ids << file.file_id if file.respond_to?(:file_id)
        end
      end
    end
  end
  file_ids
end

# Step 3: Download the file using Files API
extract_file_ids(response).each do |file_id|
  file_metadata = client.beta.files.retrieve_metadata(
    file_id,
    betas: ["files-api-2025-04-14"]
  )

  file_content = client.beta.files.download(
    file_id,
    betas: ["files-api-2025-04-14"]
  )

  # Step 4: Save to disk
  File.binwrite(file_metadata.filename, file_content.read)
  puts "Downloaded: #{file_metadata.filename}"
end
```

</Tab>
</Tabs>

**Operasi Files API tambahan:**

<CodeGroup>
```bash Shell
# Get file metadata
curl "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"

# List all files
curl "https://api.anthropic.com/v1/files" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"

# Delete a file
curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

```bash CLI
# Get file metadata
ant beta:files retrieve-metadata --file-id "$FILE_ID" \
  --transform '{filename,size_bytes}' --format yaml \
  | { read -r _ name; read -r _ size
      printf 'Filename: %s, Size: %s bytes\n' "$name" "$size"; }

# List all files
ant beta:files list \
  --transform '{filename,created_at}' --format yaml \
  | while read -r _ name && read -r _ date; do
      printf '%s - %s\n' "$name" "${date//\"/}"
    done

# Delete a file
ant beta:files delete --file-id "$FILE_ID" >/dev/null
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
file_id = "file_abc123"
# Get file metadata
file_info = client.beta.files.retrieve_metadata(
    file_id=file_id, betas=["files-api-2025-04-14"]
)
print(f"Filename: {file_info.filename}, Size: {file_info.size_bytes} bytes")

# List all files
files = client.beta.files.list(betas=["files-api-2025-04-14"])
for file in files.data:
    print(f"{file.filename} - {file.created_at}")

# Delete a file
client.beta.files.delete(file_id=file_id, betas=["files-api-2025-04-14"])
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const fileId = "file_011CNha8iCJcU1wXNR6q4V8w";

// Get file metadata
const fileInfo = await client.beta.files.retrieveMetadata(fileId, {
  betas: ["files-api-2025-04-14"]
});
console.log(`Filename: ${fileInfo.filename}, Size: ${fileInfo.size_bytes} bytes`);

// List all files
const files = await client.beta.files.list({
  betas: ["files-api-2025-04-14"]
});
for (const file of files.data) {
  console.log(`${file.filename} - ${file.created_at}`);
}

// Delete a file
await client.beta.files.delete(fileId, {
  betas: ["files-api-2025-04-14"]
});
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Files;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();
        string fileId = "file_abc123";

        // Get file metadata
        var fileInfo = await client.Beta.Files.RetrieveMetadata(fileId, new() { Betas = ["files-api-2025-04-14"] });
        Console.WriteLine($"Filename: {fileInfo.Filename}, Size: {fileInfo.SizeBytes} bytes");

        // List all files
        var files = await client.Beta.Files.List(new() { Betas = ["files-api-2025-04-14"] });
        foreach (var file in files.Data)
        {
            Console.WriteLine($"{file.Filename} - {file.CreatedAt}");
        }

        // Delete a file
        await client.Beta.Files.Delete(fileId, new() { Betas = ["files-api-2025-04-14"] });
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
	fileID := "file_abc123"

	// Get file metadata
	fileInfo, err := client.Beta.Files.GetMetadata(context.TODO(), fileID, anthropic.BetaFileGetMetadataParams{
		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Filename: %s, Size: %d bytes\n", fileInfo.Filename, fileInfo.SizeBytes)

	// List all files
	files := client.Beta.Files.ListAutoPaging(context.TODO(), anthropic.BetaFileListParams{
		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
	})
	for files.Next() {
		file := files.Current()
		fmt.Printf("%s - %s\n", file.Filename, file.CreatedAt)
	}

	// Delete a file
	_, err = client.Beta.Files.Delete(context.TODO(), fileID, anthropic.BetaFileDeleteParams{
		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
	})
	if err != nil {
		log.Fatal(err)
	}
}
```

```java Java nocheck hidelines={1..2,5..7,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileListPage;

public class FileManagement {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();
        String fileId = "file_abc123";

        // Get file metadata
        FileMetadata fileInfo = client.beta().files().retrieveMetadata(fileId);
        System.out.println("Filename: " + fileInfo.filename() + ", Size: " + fileInfo.sizeBytes() + " bytes");

        // List all files
        FileListPage files = client.beta().files().list();
        for (var file : files.data()) {
            System.out.println(file.filename() + " - " + file.createdAt());
        }

        // Delete a file
        client.beta().files().delete(fileId);
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));
$fileId = "file_abc123";

// Get file metadata
$fileInfo = $client->beta->files->retrieveMetadata(
    fileID: $fileId,
    betas: ['files-api-2025-04-14']
);
echo "Filename: {$fileInfo->filename}, Size: {$fileInfo->sizeBytes} bytes\n";

// List all files
$files = $client->beta->files->list(
    betas: ['files-api-2025-04-14']
);
foreach ($files->data as $file) {
    echo "{$file->filename} - {$file->createdAt}\n";
}

// Delete a file
$client->beta->files->delete(
    fileID: $fileId,
    betas: ['files-api-2025-04-14']
);
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new
file_id = "file_abc123"

# Get file metadata
file_info = client.beta.files.retrieve_metadata(
  file_id,
  betas: ["files-api-2025-04-14"]
)
puts "Filename: #{file_info.filename}, Size: #{file_info.size_bytes} bytes"

# List all files
files = client.beta.files.list(betas: ["files-api-2025-04-14"])
files.data.each do |file|
  puts "#{file.filename} - #{file.created_at}"
end

# Delete a file
client.beta.files.delete(
  file_id,
  betas: ["files-api-2025-04-14"]
)
```
</CodeGroup>

<Note>
Untuk detail lengkap tentang Files API, lihat [dokumentasi Files API](/docs/id/api/files-content).
</Note>

### Percakapan Multi-Putaran

Gunakan kembali kontainer yang sama di seluruh beberapa pesan dengan menentukan ID kontainer:

<CodeGroup>
```bash CLI
# Permintaan pertama membuat kontainer
CONTAINER_ID=$(ant beta:messages create \
  --beta code-execution-2025-08-25 --beta skills-2025-10-02 \
  --transform container.id --format yaml <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - {type: anthropic, skill_id: xlsx, version: latest}
messages:
  - role: user
    content: Analyze this sales data
tools:
  - {type: code_execution_20250825, name: code_execution}
YAML
)

# Lanjutkan percakapan dengan kontainer yang sama
ant beta:messages create \
  --beta code-execution-2025-08-25 --beta skills-2025-10-02 <<YAML
model: claude-opus-4-7
max_tokens: 4096
container:
  id: $CONTAINER_ID  # Gunakan kembali kontainer
  skills:
    - {type: anthropic, skill_id: xlsx, version: latest}
messages:
  - role: user
    content: Analyze this sales data
  - role: assistant
    content: []  # blok konten dari respons pertama
  - role: user
    content: What was the total revenue?
tools:
  - {type: code_execution_20250825, name: code_execution}
YAML
```

```python Python
# Permintaan pertama membuat kontainer
response1 = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
    },
    messages=[{"role": "user", "content": "Analyze this sales data"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

# Lanjutkan percakapan dengan kontainer yang sama
messages = [
    {"role": "user", "content": "Analyze this sales data"},
    {"role": "assistant", "content": response1.content},
    {"role": "user", "content": "What was the total revenue?"},
]

response2 = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "id": response1.container.id,  # Gunakan kembali kontainer
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}],
    },
    messages=messages,
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript
// Permintaan pertama membuat kontainer
const response1 = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
  },
  messages: [{ role: "user", content: "Analyze this sales data" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});

// Lanjutkan percakapan dengan kontainer yang sama
const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
  { role: "user", content: "Analyze this sales data" },
  {
    role: "assistant",
    content: response1.content as Anthropic.Beta.Messages.BetaContentBlockParam[]
  },
  { role: "user", content: "What was the total revenue?" }
];

const response2 = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    id: response1.container!.id, // Gunakan kembali kontainer
    skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
  },
  messages,
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Messages;

public class Program
{
    public static async Task Main()
    {
        var client = new AnthropicClient();

        var parameters1 = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Betas = new[] { "code-execution-2025-08-25", "skills-2025-10-02" },
            Container = new BetaContainerParams
            {
                Skills = new[]
                {
                    new BetaSkillParam
                    {
                        Type = "anthropic",
                        SkillId = "xlsx",
                        Version = "latest"
                    }
                }
            },
            Messages = new[]
            {
                new BetaMessageParam
                {
                    Role = Role.User,
                    Content = "Analyze this sales data"
                }
            },
            Tools = new[]
            {
                new BetaToolParam
                {
                    Type = "code_execution_20250825",
                    Name = "code_execution"
                }
            }
        };

        var response1 = await client.Beta.Messages.Create(parameters1);

        var parameters2 = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Betas = new[] { "code-execution-2025-08-25", "skills-2025-10-02" },
            Container = new BetaContainerParams
            {
                Id = response1.Container.Id,
                Skills = new[]
                {
                    new BetaSkillParam
                    {
                        Type = "anthropic",
                        SkillId = "xlsx",
                        Version = "latest"
                    }
                }
            },
            Messages = new[]
            {
                new BetaMessageParam { Role = Role.User, Content = "Analyze this sales data" },
                new BetaMessageParam { Role = Role.Assistant, Content = response1.Content },
                new BetaMessageParam { Role = Role.User, Content = "What was the total revenue?" }
            },
            Tools = new[]
            {
                new BetaToolParam
                {
                    Type = "code_execution_20250825",
                    Name = "code_execution"
                }
            }
        };

        var response2 = await client.Beta.Messages.Create(parameters2);
        Console.WriteLine(response2);
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

	response1, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeAnthropic,
						SkillID: "xlsx",
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Analyze this sales data")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	response2, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfString: anthropic.String(response1.Container.ID),
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Analyze this sales data")),
			response1.ToParam(),
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What was the total revenue?")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(response2)
}
```

```java Java hidelines={1..4,8..10,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaContainerParams;
import com.anthropic.models.beta.messages.BetaSkillParams;
import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;

public class ContainerReuse {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params1 = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .container(BetaContainerParams.builder()
                .addSkill(BetaSkillParams.builder()
                    .type(BetaSkillParams.Type.ANTHROPIC)
                    .skillId("xlsx")
                    .version("latest")
                    .build())
                .build())
            .addUserMessage("Analyze this sales data")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
            .build();

        BetaMessage response1 = client.beta().messages().create(params1);

        MessageCreateParams params2 = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .container(BetaContainerParams.builder()
                .id(response1.container().get().id())
                .addSkill(BetaSkillParams.builder()
                    .type(BetaSkillParams.Type.ANTHROPIC)
                    .skillId("xlsx")
                    .version("latest")
                    .build())
                .build())
            .addUserMessage("Analyze this sales data")
            .addMessage(response1)
            .addUserMessage("What was the total revenue?")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
            .build();

        BetaMessage response2 = client.beta().messages().create(params2);
        System.out.println(response2);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response1 = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Analyze this sales data']
    ],
    model: 'claude-opus-4-7',
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: [
        'skills' => [
            ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
        ]
    ],
    tools: [
        ['type' => 'code_execution_20250825', 'name' => 'code_execution']
    ]
);

$messages = [
    ['role' => 'user', 'content' => 'Analyze this sales data'],
    ['role' => 'assistant', 'content' => $response1->content],
    ['role' => 'user', 'content' => 'What was the total revenue?']
];

$response2 = $client->beta->messages->create(
    maxTokens: 4096,
    messages: $messages,
    model: 'claude-opus-4-7',
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: [
        'id' => $response1->container->id,
        'skills' => [
            ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
        ]
    ],
    tools: [
        ['type' => 'code_execution_20250825', 'name' => 'code_execution']
    ]
);

echo $response2;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response1 = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
  },
  messages: [
    { role: "user", content: "Analyze this sales data" }
  ],
  tools: [
    { type: "code_execution_20250825", name: "code_execution" }
  ]
)

messages = [
  { role: "user", content: "Analyze this sales data" },
  { role: "assistant", content: response1.content },
  { role: "user", content: "What was the total revenue?" }
]

response2 = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    id: response1.container.id,
    skills: [
      { type: "anthropic", skill_id: "xlsx", version: "latest" }
    ]
  },
  messages: messages,
  tools: [
    { type: "code_execution_20250825", name: "code_execution" }
  ]
)

puts response2
```
</CodeGroup>

### Operasi Berjalan Lama

Keterampilan dapat melakukan operasi yang memerlukan beberapa putaran. Tangani alasan penghentian `pause_turn`:

<CodeGroup>

```bash Shell nocheck
# Permintaan awal
RESPONSE=$(curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-7",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "latest"
        }
      ]
    },
    "messages": [{
      "role": "user",
      "content": "Process this large dataset"
    }],
    "tools": [{
      "type": "code_execution_20250825",
      "name": "code_execution"
    }]
  }')

# Periksa stop_reason dan tangani pause_turn dalam loop
STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason')
CONTAINER_ID=$(echo "$RESPONSE" | jq -r '.container.id')

while [ "$STOP_REASON" = "pause_turn" ]; do
  # Lanjutkan dengan kontainer yang sama
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-4-7\",
      \"max_tokens\": 4096,
      \"container\": {
        \"id\": \"$CONTAINER_ID\",
        \"skills\": [{
          \"type\": \"custom\",
          \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
          \"version\": \"latest\"
        }]
      },
      \"messages\": [/* include conversation history */],
      \"tools\": [{
        \"type\": \"code_execution_20250825\",
        \"name\": \"code_execution\"
      }]
    }")

  STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason')
done
```

```bash CLI nocheck
RESP=$(mktemp)

# Permintaan awal: tangkap respons JSON lengkap ke file temp
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
 > "$RESP" <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: custom
      skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
      version: latest
messages:
  - role: user
    content: Process this large dataset
tools:
  - type: code_execution_20250825
    name: code_execution
YAML

# Tangani pause_turn untuk operasi panjang (hingga 10 iterasi)
for _ in {1..10}; do
  [[ $(jq -r '.stop_reason' "$RESP") == pause_turn ]] || break

  CONTAINER_ID=$(jq -r '.container.id' "$RESP")

  # Lanjutkan dalam kontainer yang sama, menambahkan array konten respons sebelumnya
  # ke pesan sebagai putaran asisten.
  ant beta:messages create \
    --beta code-execution-2025-08-25 \
    --beta skills-2025-10-02 \
 > "$RESP" <<YAML
model: claude-opus-4-7
max_tokens: 4096
container:
  id: $CONTAINER_ID
  skills:
    - type: custom
      skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
      version: latest
messages:
  # ... riwayat percakapan dengan konten asisten sebelumnya ditambahkan
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
done
```

```python Python nocheck
messages = [{"role": "user", "content": "Process this large dataset"}]
max_retries = 10

response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                "version": "latest",
            }
        ]
    },
    messages=messages,
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

# Tangani pause_turn untuk operasi panjang
for i in range(max_retries):
    if response.stop_reason != "pause_turn":
        break

    messages.append({"role": "assistant", "content": response.content})
    response = client.beta.messages.create(
        model="claude-opus-4-7",
        max_tokens=4096,
        betas=["code-execution-2025-08-25", "skills-2025-10-02"],
        container={
            "id": response.container.id,
            "skills": [
                {
                    "type": "custom",
                    "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                    "version": "latest",
                }
            ],
        },
        messages=messages,
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    )
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
  { role: "user", content: "Process this large dataset" }
];
const maxRetries = 10;

let response = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [{ type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }]
  },
  messages,
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});

// Tangani pause_turn untuk operasi panjang
for (let i = 0; i < maxRetries; i++) {
  if (response.stop_reason !== "pause_turn") {
    break;
  }

  messages.push({
    role: "assistant" as const,
    content: response.content as Anthropic.Beta.Messages.BetaContentBlockParam[]
  });
  response = await client.beta.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      id: response.container!.id,
      skills: [
        { type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }
      ]
    },
    messages,
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
}
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Beta.Messages;

AnthropicClient client = new();

var messages = new List<BetaMessageParam>
{
    new() { Role = Role.User, Content = "Process this large dataset" }
};
int maxRetries = 10;

var response = await client.Beta.Messages.Create(new MessageCreateParams
{
    Model = "claude-opus-4-7",
    MaxTokens = 4096,
    Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
    Container = new BetaContainerParams
    {
        Skills = [
            new BetaSkillParam
            {
                Type = "custom",
                SkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                Version = "latest"
            }
        ]
    },
    Messages = messages,
    Tools = [new BetaToolParam { Type = "code_execution_20250825", Name = "code_execution" }]
});

for (int i = 0; i < maxRetries; i++)
{
    if (response.StopReason != "pause_turn")
    {
        break;
    }

    messages.Add(new BetaMessageParam { Role = Role.Assistant, Content = response.Content });

    response = await client.Beta.Messages.Create(new MessageCreateParams
    {
        Model = "claude-opus-4-7",
        MaxTokens = 4096,
        Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
        Container = new BetaContainerParams
        {
            Id = response.Container.Id,
            Skills = [
                new BetaSkillParam
                {
                    Type = "custom",
                    SkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                    Version = "latest"
                }
            ]
        },
        Messages = messages,
        Tools = [new BetaToolParam { Type = "code_execution_20250825", Name = "code_execution" }]
    });
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

	messages := []anthropic.BetaMessageParam{
		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Process this large dataset")),
	}
	maxRetries := 10

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeCustom,
						SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: messages,
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	for i := 0; i < maxRetries; i++ {
		if response.StopReason != "pause_turn" {
			break
		}

		messages = append(messages, response.ToParam())

		response, err = client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
			Model:     "claude-opus-4-7",
			MaxTokens: 4096,
			Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
			Container: anthropic.BetaMessageNewParamsContainerUnion{
				OfString: anthropic.String(response.Container.ID),
			},
			Messages: messages,
			Tools: []anthropic.BetaToolUnionParam{
				{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
			},
		})
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..5,9..10,12..14,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaMessageParam;
import com.anthropic.models.beta.messages.BetaContainerParams;
import com.anthropic.models.beta.messages.BetaSkillParams;
import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
import java.util.ArrayList;
import java.util.List;
import com.anthropic.models.beta.messages.BetaStopReason;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        List<BetaMessageParam> messages = new ArrayList<>();
        messages.add(
            BetaMessageParam.builder()
                .role(BetaMessageParam.Role.USER)
                .content("Process this large dataset")
                .build()
        );
        int maxRetries = 10;

        BetaMessage response = client.beta().messages().create(
            MessageCreateParams.builder()
                .model("claude-opus-4-7")
                .maxTokens(4096L)
                .addBeta("code-execution-2025-08-25")
                .addBeta("skills-2025-10-02")
                .container(BetaContainerParams.builder()
                    .addSkill(BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.CUSTOM)
                        .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                        .version("latest")
                        .build())
                    .build())
                .messages(messages)
                .addTool(BetaCodeExecutionTool20250825.builder().build())
                .build());

        for (int i = 0; i < maxRetries; i++) {
            if (!response.stopReason().isPresent()
                    || !response.stopReason().get().equals(BetaStopReason.PAUSE_TURN)) {
                break;
            }

            messages.add(response.toParam());

            response = client.beta().messages().create(
                MessageCreateParams.builder()
                    .model("claude-opus-4-7")
                    .maxTokens(4096L)
                    .addBeta("code-execution-2025-08-25")
                    .addBeta("skills-2025-10-02")
                    .container(BetaContainerParams.builder()
                        .id(response.container().get().id())
                        .addSkill(BetaSkillParams.builder()
                            .type(BetaSkillParams.Type.CUSTOM)
                            .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                            .version("latest")
                            .build())
                        .build())
                    .messages(messages)
                    .addTool(BetaCodeExecutionTool20250825.builder().build())
                    .build());
        }
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$messages = [
    ['role' => 'user', 'content' => 'Process this large dataset']
];
$maxRetries = 10;

$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: $messages,
    model: 'claude-opus-4-7',
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: [
        'skills' => [
            [
                'type' => 'custom',
                'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                'version' => 'latest'
            ]
        ]
    ],
    tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
);

for ($i = 0; $i < $maxRetries; $i++) {
    if ($response->stopReason !== 'pause_turn') {
        break;
    }

    $messages[] = ['role' => 'assistant', 'content' => $response->content];

    $response = $client->beta->messages->create(
        maxTokens: 4096,
        messages: $messages,
        model: 'claude-opus-4-7',
        betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
        container: [
            'id' => $response->container->id,
            'skills' => [
                [
                    'type' => 'custom',
                    'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                    'version' => 'latest'
                ]
            ]
        ],
        tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
    );
}
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

messages = [
  { role: "user", content: "Process this large dataset" }
]
max_retries = 10

response = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "latest"
      }
    ]
  },
  messages: messages,
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
)

max_retries.times do
  break if response.stop_reason != :pause_turn

  messages << { role: "assistant", content: response.content }

  response = client.beta.messages.create(
    model: "claude-opus-4-7",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      id: response.container.id,
      skills: [
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: messages,
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
end
```
</CodeGroup>

<Note>
Respons mungkin menyertakan alasan penghentian `pause_turn`, yang menunjukkan bahwa API menjeda operasi Keterampilan yang berjalan lama. Anda dapat memberikan respons kembali apa adanya dalam permintaan berikutnya untuk membiarkan Claude melanjutkan gilirannya, atau memodifikasi konten jika Anda ingin mengganggu percakapan dan memberikan panduan tambahan.
</Note>

### Menggunakan Beberapa Skills

Gabungkan beberapa Skills dalam satu permintaan untuk menangani alur kerja yang kompleks:

<CodeGroup>

```bash Shell nocheck
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-7",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {
          "type": "anthropic",
          "skill_id": "xlsx",
          "version": "latest"
        },
        {
          "type": "anthropic",
          "skill_id": "pptx",
          "version": "latest"
        },
        {
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "latest"
        }
      ]
    },
    "messages": [{
      "role": "user",
      "content": "Analyze sales data and create a presentation"
    }],
    "tools": [{
      "type": "code_execution_20250825",
      "name": "code_execution"
    }]
  }'
```

```bash CLI nocheck
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: xlsx
      version: latest
    - type: anthropic
      skill_id: pptx
      version: latest
    - type: custom
      skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
      version: latest
messages:
  - role: user
    content: Analyze sales data and create a presentation
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
```

```python Python nocheck
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
            {"type": "anthropic", "skill_id": "pptx", "version": "latest"},
            {
                "type": "custom",
                "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                "version": "latest",
            },
        ]
    },
    messages=[
        {"role": "user", "content": "Analyze sales data and create a presentation"}
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript nocheck
const response = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "anthropic",
        skill_id: "xlsx",
        version: "latest"
      },
      {
        type: "anthropic",
        skill_id: "pptx",
        version: "latest"
      },
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "latest"
      }
    ]
  },
  messages: [
    {
      role: "user",
      content: "Analyze sales data and create a presentation"
    }
  ],
  tools: [
    {
      type: "code_execution_20250825",
      name: "code_execution"
    }
  ]
});
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Betas = new[] { "code-execution-2025-08-25", "skills-2025-10-02" },
            Container = new BetaContainerParams
            {
                Skills = new object[]
                {
                    new
                    {
                        type = "anthropic",
                        skill_id = "xlsx",
                        version = "latest"
                    },
                    new
                    {
                        type = "anthropic",
                        skill_id = "pptx",
                        version = "latest"
                    },
                    new
                    {
                        type = "custom",
                        skill_id = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                        version = "latest"
                    }
                }
            },
            Messages = new[]
            {
                new BetaMessageParam
                {
                    Role = Role.User,
                    Content = "Analyze sales data and create a presentation"
                }
            ],
            Tools = new object[]
            {
                new
                {
                    type = "code_execution_20250825",
                    name = "code_execution"
                }
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
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas: []anthropic.AnthropicBeta{
			"code-execution-2025-08-25",
			anthropic.AnthropicBetaSkills2025_10_02,
		},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeAnthropic,
						SkillID: "xlsx",
						Version: anthropic.String("latest"),
					},
					{
						Type:    anthropic.BetaSkillParamsTypeAnthropic,
						SkillID: "pptx",
						Version: anthropic.String("latest"),
					},
					{
						Type:    anthropic.BetaSkillParamsTypeCustom,
						SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Analyze sales data and create a presentation")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..4,8..11,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaContainerParams;
import com.anthropic.models.beta.messages.BetaSkillParams;
import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
import java.util.List;

public class SkillsExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .container(BetaContainerParams.builder()
                .skills(List.of(
                    BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.ANTHROPIC)
                        .skillId("xlsx")
                        .version("latest")
                        .build(),
                    BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.ANTHROPIC)
                        .skillId("pptx")
                        .version("latest")
                        .build(),
                    BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.CUSTOM)
                        .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                        .version("latest")
                        .build()
                ))
                .build())
            .addUserMessage("Analyze sales data and create a presentation")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
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
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Analyze sales data and create a presentation']
    ],
    model: 'claude-opus-4-7',
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: [
        'skills' => [
            [
                'type' => 'anthropic',
                'skill_id' => 'xlsx',
                'version' => 'latest'
            ],
            [
                'type' => 'anthropic',
                'skill_id' => 'pptx',
                'version' => 'latest'
            ],
            [
                'type' => 'custom',
                'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                'version' => 'latest'
            ]
        ]
    ],
    tools: [
        ['type' => 'code_execution_20250825', 'name' => 'code_execution']
    ]
);

echo $message;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "anthropic",
        skill_id: "xlsx",
        version: "latest"
      },
      {
        type: "anthropic",
        skill_id: "pptx",
        version: "latest"
      },
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "latest"
      }
    ]
  },
  messages: [
    { role: "user", content: "Analyze sales data and create a presentation" }
  ],
  tools: [
    { type: "code_execution_20250825", name: "code_execution" }
  ]
)
puts message
```
</CodeGroup>

---

## Mengelola Skills Kustom

### Membuat Skill

Unggah Skill kustom Anda untuk membuatnya tersedia di ruang kerja Anda. Anda dapat mengunggah menggunakan jalur direktori atau objek file individual.

<CodeGroup defaultLanguage="CLI">

```bash Shell nocheck
curl -X POST "https://api.anthropic.com/v1/skills" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02" \
  -F "display_title=Financial Analysis" \
  -F "files[]=@financial_skill/SKILL.md;filename=financial_skill/SKILL.md" \
  -F "files[]=@financial_skill/analyze.py;filename=financial_skill/analyze.py"
```

```bash CLI nocheck
# Option 1: Upload individual files (one --file flag per file)
ant beta:skills create \
  --display-title "Financial Analysis" \
  --file financial_skill/SKILL.md \
  --file financial_skill/analyze.py \
  --beta skills-2025-10-02

# Option 2: Upload a zip archive
ant beta:skills create \
  --display-title "Financial Analysis" \
  --file financial_analysis_skill.zip \
  --beta skills-2025-10-02
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Option 1: Using files_from_dir helper (Python only, recommended)
from anthropic.lib import files_from_dir

skill = client.beta.skills.create(
    display_title="Financial Analysis",
    files=files_from_dir("/path/to/financial_analysis_skill"),
    betas=["skills-2025-10-02"],
)

# Option 2: Using a zip file
skill = client.beta.skills.create(
    display_title="Financial Analysis",
    files=[("skill.zip", open("financial_analysis_skill.zip", "rb"))],
    betas=["skills-2025-10-02"],
)

# Option 3: Using file tuples (filename, file_content, mime_type)
skill = client.beta.skills.create(
    display_title="Financial Analysis",
    files=[
        (
            "financial_skill/SKILL.md",
            open("financial_skill/SKILL.md", "rb"),
            "text/markdown",
        ),
        (
            "financial_skill/analyze.py",
            open("financial_skill/analyze.py", "rb"),
            "text/x-python",
        ),
    ],
    betas=["skills-2025-10-02"],
)

print(f"Created skill: {skill.id}")
print(f"Latest version: {skill.latest_version}")
```

```typescript TypeScript nocheck
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

const client = new Anthropic();

// Option 1: Using a zip file
const skillFromZip = await client.beta.skills.create({
  display_title: "Financial Analysis",
  files: [await toFile(fs.createReadStream("financial_analysis_skill.zip"), "skill.zip")],
  betas: ["skills-2025-10-02"]
});

// Option 2: Using individual file objects
const skill = await client.beta.skills.create({
  display_title: "Financial Analysis",
  files: [
    await toFile(fs.createReadStream("financial_skill/SKILL.md"), "financial_skill/SKILL.md", {
      type: "text/markdown"
    }),
    await toFile(
      fs.createReadStream("financial_skill/analyze.py"),
      "financial_skill/analyze.py",
      { type: "text/x-python" }
    )
  ],
  betas: ["skills-2025-10-02"]
});

console.log(`Created skill: ${skill.id}`);
console.log(`Latest version: ${skill.latest_version}`);
```

```csharp C# nocheck
using System;
using System.IO;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Skills;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        // Option 1: Using a zip file
        var parameters = new SkillCreateParams
        {
            DisplayTitle = "Financial Analysis",
            Files = [
                new FileStream("financial_analysis_skill.zip", FileMode.Open, FileAccess.Read)
            ],
            Betas = ["skills-2025-10-02"]
        };

        var skill = await client.Beta.Skills.Create(parameters);

        // Option 2: Using individual files
        var parameters2 = new SkillCreateParams
        {
            DisplayTitle = "Financial Analysis",
            Files = [
                new FileStream("financial_skill/SKILL.md", FileMode.Open, FileAccess.Read),
                new FileStream("financial_skill/analyze.py", FileMode.Open, FileAccess.Read)
            ],
            Betas = ["skills-2025-10-02"]
        };

        var skill2 = await client.Beta.Skills.Create(parameters2);

        Console.WriteLine($"Created skill: {skill.Id}");
        Console.WriteLine($"Latest version: {skill.LatestVersion}");
    }
}
```

```go Go nocheck hidelines={1..15,-1}
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	// Option 1: Using a zip file
	zipFile, err := os.Open("financial_analysis_skill.zip")
	if err != nil {
		log.Fatal(err)
	}
	defer zipFile.Close()

	skill, err := client.Beta.Skills.New(context.TODO(), anthropic.BetaSkillNewParams{
		DisplayTitle: anthropic.String("Financial Analysis"),
		Files:        []io.Reader{zipFile},
		Betas:        []anthropic.AnthropicBeta{anthropic.AnthropicBetaSkills2025_10_02},
	})
	if err != nil {
		log.Fatal(err)
	}

	// Option 2: Using individual files
	skillMd, err := os.Open("financial_skill/SKILL.md")
	if err != nil {
		log.Fatal(err)
	}
	defer skillMd.Close()

	analyzePy, err := os.Open("financial_skill/analyze.py")
	if err != nil {
		log.Fatal(err)
	}
	defer analyzePy.Close()

	skill2, err := client.Beta.Skills.New(context.TODO(), anthropic.BetaSkillNewParams{
		DisplayTitle: anthropic.String("Financial Analysis"),
		Files:        []io.Reader{skillMd, analyzePy},
		Betas:        []anthropic.AnthropicBeta{anthropic.AnthropicBetaSkills2025_10_02},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Created skill: %s\n", skill.ID)
	fmt.Printf("Latest version: %s\n", skill.LatestVersion)
	fmt.Printf("Created skill 2: %s\n", skill2.ID)
}
```

```java Java nocheck hidelines={1..2,5..10,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.SkillCreateParams;
import com.anthropic.models.beta.skills.SkillCreateResponse;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Path;

public class SkillCreate {
    public static void main(String[] args) throws IOException {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Option 1: Using a zip file
        SkillCreateParams params = SkillCreateParams.builder()
            .displayTitle("Financial Analysis")
            .addFile(new FileInputStream("financial_analysis_skill.zip"))
            .addBeta("skills-2025-10-02")
            .build();

        SkillCreateResponse skill = client.beta().skills().create(params);

        // Option 2: Using individual files
        SkillCreateParams params2 = SkillCreateParams.builder()
            .displayTitle("Financial Analysis")
            .addFile(Path.of("financial_skill/SKILL.md"))
            .addFile(Path.of("financial_skill/analyze.py"))
            .addBeta("skills-2025-10-02")
            .build();

        SkillCreateResponse skill2 = client.beta().skills().create(params2);

        System.out.println("Created skill: " + skill.id());
        System.out.println("Latest version: " + skill.latestVersion());
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

// Option 1: Using a zip file
$skill = $client->beta->skills->create(
    displayTitle: 'Financial Analysis',
    files: [
        fopen('financial_analysis_skill.zip', 'r')
    ],
    betas: ['skills-2025-10-02']
);

// Option 2: Using individual files
$skill = $client->beta->skills->create(
    displayTitle: 'Financial Analysis',
    files: [
        fopen('financial_skill/SKILL.md', 'r'),
        fopen('financial_skill/analyze.py', 'r')
    ],
    betas: ['skills-2025-10-02']
);

echo "Created skill: {$skill->id}\n";
echo "Latest version: {$skill->latestVersion}\n";
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Option 1: Using a zip file
skill = client.beta.skills.create(
  display_title: "Financial Analysis",
  files: [
    File.open("financial_analysis_skill.zip", "rb")
  ],
  betas: ["skills-2025-10-02"]
)

# Option 2: Using individual files
skill = client.beta.skills.create(
  display_title: "Financial Analysis",
  files: [
    File.open("financial_skill/SKILL.md", "rb"),
    File.open("financial_skill/analyze.py", "rb")
  ],
  betas: ["skills-2025-10-02"]
)

puts "Created skill: #{skill.id}"
puts "Latest version: #{skill.latest_version}"
```
</CodeGroup>

**Persyaratan:**
- Harus menyertakan file SKILL.md di tingkat atas
- Semua file harus menentukan direktori root umum dalam jalur mereka
- Ukuran unggahan total harus di bawah 30&nbsp;MB
- Persyaratan frontmatter YAML:
  - `name`: Maksimal 64 karakter, hanya huruf kecil/angka/tanda hubung, tanpa tag XML, tanpa kata-kata yang dicadangkan ("anthropic", "claude")
  - `description`: Maksimal 1024 karakter, tidak kosong, tanpa tag XML

Untuk skema permintaan/respons lengkap, lihat [referensi API Buat Skill](/docs/id/api/skills/create-skill).

### Mendaftar Skills

Ambil semua Skills yang tersedia untuk ruang kerja Anda, termasuk Skills pra-bangun Anthropic dan Skills kustom Anda. Gunakan parameter `source` untuk memfilter berdasarkan jenis skill:

<CodeGroup defaultLanguage="CLI">
```bash Shell
# List all Skills
curl "https://api.anthropic.com/v1/skills" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02"

# List only custom Skills
curl "https://api.anthropic.com/v1/skills?source=custom" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02"
```

```bash CLI
# List all Skills
ant beta:skills list

# List only custom Skills
ant beta:skills list --source custom
```

```python Python
# List all Skills
skills = client.beta.skills.list(betas=["skills-2025-10-02"])

for skill in skills.data:
    print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

# List only custom Skills
custom_skills = client.beta.skills.list(source="custom", betas=["skills-2025-10-02"])
```

```typescript TypeScript
// List all Skills
const skills = await client.beta.skills.list({
  betas: ["skills-2025-10-02"]
});

for (const skill of skills.data) {
  console.log(`${skill.id}: ${skill.display_title} (source: ${skill.source})`);
}

// List only custom Skills
const customSkills = await client.beta.skills.list({
  source: "custom",
  betas: ["skills-2025-10-02"]
});
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Skills;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        // List all Skills
        var skills = await client.Beta.Skills.List(new SkillListParams
        {
            Betas = new[] { "skills-2025-10-02" }
        });

        foreach (var skill in skills.Data)
        {
            Console.WriteLine($"{skill.Id}: {skill.DisplayTitle} (source: {skill.Source})");
        }

        // List only custom Skills
        var customSkills = await client.Beta.Skills.List(new SkillListParams
        {
            Source = "custom",
            Betas = new[] { "skills-2025-10-02" }
        });
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

	// List all Skills
	skills := client.Beta.Skills.ListAutoPaging(context.TODO(), anthropic.BetaSkillListParams{
		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaSkills2025_10_02},
	})

	for skills.Next() {
		skill := skills.Current()
		fmt.Printf("%s: %s (source: %s)\n", skill.ID, skill.DisplayTitle, skill.Source)
	}
	if skills.Err() != nil {
		log.Fatal(skills.Err())
	}

	// List only custom Skills
	customSkills := client.Beta.Skills.ListAutoPaging(context.TODO(), anthropic.BetaSkillListParams{
		Source: anthropic.String("custom"),
		Betas:  []anthropic.AnthropicBeta{anthropic.AnthropicBetaSkills2025_10_02},
	})

	for customSkills.Next() {
		skill := customSkills.Current()
		fmt.Printf("%s: %s (source: %s)\n", skill.ID, skill.DisplayTitle, skill.Source)
	}
}
```

```java Java hidelines={1..2,6..8,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.SkillListParams;
import com.anthropic.models.beta.skills.SkillListPage;
import com.anthropic.models.beta.skills.SkillListResponse;

public class ListSkills {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // List all Skills
        SkillListParams params = SkillListParams.builder()
            .addBeta("skills-2025-10-02")
            .build();

        SkillListPage skills = client.beta().skills().list(params);

        for (SkillListResponse skill : skills.data()) {
            System.out.println(skill.id() + ": " + skill.displayTitle() + " (source: " + skill.source() + ")");
        }

        // List only custom Skills
        SkillListParams customParams = SkillListParams.builder()
            .source("custom")
            .addBeta("skills-2025-10-02")
            .build();

        SkillListPage customSkills = client.beta().skills().list(customParams);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

// List all Skills
$skills = $client->beta->skills->list(
    betas: ['skills-2025-10-02']
);

foreach ($skills->data as $skill) {
    echo "{$skill->id}: {$skill->displayTitle} (source: {$skill->source})\n";
}

// List only custom Skills
$customSkills = $client->beta->skills->list(
    source: 'custom',
    betas: ['skills-2025-10-02']
);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# List all Skills
skills = client.beta.skills.list(betas: ["skills-2025-10-02"])

skills.data.each do |skill|
  puts "#{skill.id}: #{skill.display_title} (source: #{skill.source})"
end

# List only custom Skills
custom_skills = client.beta.skills.list(
  source: "custom",
  betas: ["skills-2025-10-02"]
)
```
</CodeGroup>

Lihat [referensi API Daftar Skills](/docs/id/api/skills/list-skills) untuk opsi paginasi dan pemfilteran.

### Mengambil Skill

Dapatkan detail tentang Skill tertentu:

<CodeGroup defaultLanguage="CLI">

```bash Shell nocheck
curl "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02"
```

```bash CLI nocheck
ant beta:skills retrieve \
  --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv
```

```python Python nocheck
skill = client.beta.skills.retrieve(
    skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv", betas=["skills-2025-10-02"]
)

print(f"Skill: {skill.display_title}")
print(f"Latest version: {skill.latest_version}")
print(f"Created: {skill.created_at}")
```

```typescript TypeScript nocheck
const skill = await client.beta.skills.retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv", {
  betas: ["skills-2025-10-02"]
});

console.log(`Skill: ${skill.display_title}`);
console.log(`Latest version: ${skill.latest_version}`);
console.log(`Created: ${skill.created_at}`);
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Skills;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var skill = await client.Beta.Skills.Retrieve(
            "skill_01AbCdEfGhIjKlMnOpQrStUv",
            new() { Betas = ["skills-2025-10-02"] }
        );

        Console.WriteLine($"Skill: {skill.DisplayTitle}");
        Console.WriteLine($"Latest version: {skill.LatestVersion}");
        Console.WriteLine($"Created: {skill.CreatedAt}");
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

	skill, err := client.Beta.Skills.Get(
		context.TODO(),
		"skill_01AbCdEfGhIjKlMnOpQrStUv",
		anthropic.BetaSkillGetParams{
			Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaSkills2025_10_02},
		},
	)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Skill: %s\n", skill.DisplayTitle)
	fmt.Printf("Latest version: %s\n", skill.LatestVersion)
	fmt.Printf("Created: %s\n", skill.CreatedAt)
}
```

```java Java nocheck hidelines={1..2,5..7,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.SkillRetrieveParams;
import com.anthropic.models.beta.skills.SkillRetrieveResponse;

public class RetrieveSkill {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        SkillRetrieveResponse skill = client.beta().skills().retrieve(
            "skill_01AbCdEfGhIjKlMnOpQrStUv",
            SkillRetrieveParams.builder()
                .addBeta("skills-2025-10-02")
                .build()
        );

        System.out.println("Skill: " + skill.displayTitle());
        System.out.println("Latest version: " + skill.latestVersion());
        System.out.println("Created: " + skill.createdAt());
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$skill = $client->beta->skills->retrieve(
    skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
    betas: ["skills-2025-10-02"]
);

echo "Skill: " . $skill->displayTitle . "\n";
echo "Latest version: " . $skill->latestVersion . "\n";
echo "Created: " . $skill->createdAt . "\n";
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

skill = client.beta.skills.retrieve(
  "skill_01AbCdEfGhIjKlMnOpQrStUv",
  betas: ["skills-2025-10-02"]
)

puts "Skill: #{skill.display_title}"
puts "Latest version: #{skill.latest_version}"
puts "Created: #{skill.created_at}"
```
</CodeGroup>

### Menghapus Skill

Untuk menghapus Skill, Anda harus terlebih dahulu menghapus semua versinya:

<CodeGroup defaultLanguage="CLI">

```bash Shell nocheck
# Delete all versions first, then delete the Skill
curl -X DELETE "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02"
```

```bash CLI nocheck
# Step 1: Delete all versions
ant beta:skills:versions list \
  --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
  --transform version --format yaml \
  | tr -d '"' \
  | while read -r VERSION; do
      ant beta:skills:versions delete \
        --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
        --version "$VERSION" >/dev/null
    done

# Step 2: Delete the Skill
ant beta:skills delete \
  --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv >/dev/null
```

```python Python nocheck
# Step 1: Delete all versions
versions = client.beta.skills.versions.list(
    skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv", betas=["skills-2025-10-02"]
)

for version in versions.data:
    client.beta.skills.versions.delete(
        skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
        version=version.version,
        betas=["skills-2025-10-02"],
    )

# Step 2: Delete the Skill
client.beta.skills.delete(
    skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv", betas=["skills-2025-10-02"]
)
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// Step 1: Delete all versions
const versions = await client.beta.skills.versions.list("skill_01AbCdEfGhIjKlMnOpQrStUv", {
  betas: ["skills-2025-10-02"]
});

for (const version of versions.data) {
  await client.beta.skills.versions.delete("skill_01AbCdEfGhIjKlMnOpQrStUv", version.version, {
    betas: ["skills-2025-10-02"]
  });
}

// Step 2: Delete the Skill
await client.beta.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv", {
  betas: ["skills-2025-10-02"]
});
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        // Step 1: Delete all versions
        var versions = await client.Beta.Skills.Versions.List(
            "skill_01AbCdEfGhIjKlMnOpQrStUv",
            new() { Betas = ["skills-2025-10-02"] }
        );

        foreach (var version in versions.Data)
        {
            await client.Beta.Skills.Versions.Delete(
                "skill_01AbCdEfGhIjKlMnOpQrStUv",
                version.Version,
                new() { Betas = ["skills-2025-10-02"] }
            );
        }

        // Step 2: Delete the Skill
        await client.Beta.Skills.Delete(
            "skill_01AbCdEfGhIjKlMnOpQrStUv",
            new() { Betas = ["skills-2025-10-02"] }
        );
    }
}
```

```go Go nocheck hidelines={1..12,-1}
package main

import (
	"context"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	// Step 1: Delete all versions
	versions := client.Beta.Skills.Versions.ListAutoPaging(
		context.TODO(),
		"skill_01AbCdEfGhIjKlMnOpQrStUv",
		anthropic.BetaSkillVersionListParams{
			Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaSkills2025_10_02},
		},
	)

	for versions.Next() {
		version := versions.Current()
		_, err := client.Beta.Skills.Versions.Delete(
			context.TODO(),
			version.Version,
			anthropic.BetaSkillVersionDeleteParams{
				SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
				Betas:   []anthropic.AnthropicBeta{anthropic.AnthropicBetaSkills2025_10_02},
			},
		)
		if err != nil {
			log.Fatal(err)
		}
	}

	// Step 2: Delete the Skill
	_, err := client.Beta.Skills.Delete(
		context.TODO(),
		"skill_01AbCdEfGhIjKlMnOpQrStUv",
		anthropic.BetaSkillDeleteParams{
			Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaSkills2025_10_02},
		},
	)
	if err != nil {
		log.Fatal(err)
	}
}
```

```java Java nocheck hidelines={1..2,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.SkillDeleteParams;
import com.anthropic.models.beta.skills.versions.VersionListParams;
import com.anthropic.models.beta.skills.versions.VersionListPage;
import com.anthropic.models.beta.skills.versions.VersionDeleteParams;

public class DeleteSkill {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Step 1: Delete all versions
        VersionListPage versions = client.beta().skills().versions().list(
            "skill_01AbCdEfGhIjKlMnOpQrStUv",
            VersionListParams.builder()
                .addBeta("skills-2025-10-02")
                .build()
        );

        for (var version : versions.data()) {
            client.beta().skills().versions().delete(
                version.version(),
                VersionDeleteParams.builder()
                    .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                    .addBeta("skills-2025-10-02")
                    .build()
            );
        }

        // Step 2: Delete the Skill
        client.beta().skills().delete(
            "skill_01AbCdEfGhIjKlMnOpQrStUv",
            SkillDeleteParams.builder()
                .addBeta("skills-2025-10-02")
                .build()
        );
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

// Step 1: Delete all versions
$versions = $client->beta->skills->versions->list(
    skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
    betas: ["skills-2025-10-02"]
);

foreach ($versions->data as $version) {
    $client->beta->skills->versions->delete(
        skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: $version->version,
        betas: ["skills-2025-10-02"]
    );
}

// Step 2: Delete the Skill
$client->beta->skills->delete(
    skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
    betas: ["skills-2025-10-02"]
);
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Step 1: Delete all versions
versions = client.beta.skills.versions.list(
  "skill_01AbCdEfGhIjKlMnOpQrStUv",
  betas: ["skills-2025-10-02"]
)

versions.data.each do |version|
  client.beta.skills.versions.delete(
    version.version,
    skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
    betas: ["skills-2025-10-02"]
  )
end

# Step 2: Delete the Skill
client.beta.skills.delete(
  "skill_01AbCdEfGhIjKlMnOpQrStUv",
  betas: ["skills-2025-10-02"]
)
```
</CodeGroup>

Mencoba menghapus Skill dengan versi yang ada mengembalikan kesalahan 400.

### Versioning

Skills mendukung versioning untuk mengelola pembaruan dengan aman:

**Anthropic-Managed Skills:**
- Versi menggunakan format tanggal: `20251013`
- Versi baru dirilis saat pembaruan dilakukan
- Tentukan versi yang tepat untuk stabilitas

**Custom Skills:**
- Timestamp epoch yang dihasilkan secara otomatis: `1759178010641129`
- Gunakan `"latest"` untuk selalu mendapatkan versi terbaru
- Buat versi baru saat memperbarui file Skill

<CodeGroup defaultLanguage="CLI">

```bash Shell nocheck
# Create a new version
NEW_VERSION=$(curl -X POST "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02" \
  -F "files[]=@updated_skill/SKILL.md;filename=updated_skill/SKILL.md")

VERSION_NUMBER=$(echo "$NEW_VERSION" | jq -r '.version')

# Use specific version
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d "{
    \"model\": \"claude-opus-4-7\",
    \"max_tokens\": 4096,
    \"container\": {
      \"skills\": [{
        \"type\": \"custom\",
        \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
        \"version\": \"$VERSION_NUMBER\"
      }]
    },
    \"messages\": [{\"role\": \"user\", \"content\": \"Use updated Skill\"}],
    \"tools\": [{\"type\": \"code_execution_20250825\", \"name\": \"code_execution\"}]
  }"

# Use latest version
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-7",
    "max_tokens": 4096,
    "container": {
      "skills": [{
        "type": "custom",
        "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
        "version": "latest"
      }]
    },
    "messages": [{"role": "user", "content": "Use latest Skill version"}],
    "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
  }'
```

```bash CLI nocheck
# Create a new version
VERSION_NUMBER=$(ant beta:skills:versions create \
  --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
  --file updated_skill/SKILL.md \
  --transform version --format yaml)

# Use specific version
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<YAML
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: custom
      skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
      version: $VERSION_NUMBER
messages:
  - role: user
    content: Use updated Skill
tools:
  - type: code_execution_20250825
    name: code_execution
YAML

# Use latest version
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: custom
      skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
      version: latest
messages:
  - role: user
    content: Use latest Skill version
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
```

```python Python nocheck
# Create a new version
from anthropic.lib import files_from_dir

new_version = client.beta.skills.versions.create(
    skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
    files=files_from_dir("/path/to/updated_skill"),
    betas=["skills-2025-10-02"],
)

# Use specific version
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                "version": new_version.version,
            }
        ]
    },
    messages=[{"role": "user", "content": "Use updated Skill"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

# Use latest version
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                "version": "latest",
            }
        ]
    },
    messages=[{"role": "user", "content": "Use latest Skill version"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript nocheck hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import fs from "fs";

const client = new Anthropic();

// Create a new version using a zip file
const newVersion = await client.beta.skills.versions.create("skill_01AbCdEfGhIjKlMnOpQrStUv", {
  files: [fs.createReadStream("updated_skill.zip")],
  betas: ["skills-2025-10-02"]
});

// Use specific version
const specificVersionResponse = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: newVersion.version
      }
    ]
  },
  messages: [{ role: "user", content: "Use updated Skill" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});

// Use latest version
const latestVersionResponse = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "latest"
      }
    ]
  },
  messages: [{ role: "user", content: "Use latest Skill version" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});
```

```csharp C# nocheck
using System;
using System.IO;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Messages;
using Anthropic.Models.Beta.Skills;

class Program
{
    static async Task Main()
    {
        var client = new AnthropicClient
        {
            ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
        };

        // Create a new version
        var versionParams = new SkillVersionCreateParams
        {
            Files = [File.OpenRead("/path/to/updated_skill/SKILL.md")],
            Betas = ["skills-2025-10-02"]
        };

        var newVersion = await client.Beta.Skills.Versions.Create(
            "skill_01AbCdEfGhIjKlMnOpQrStUv",
            versionParams
        );

        // Use specific version
        var specificVersionParams = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
            Container = new()
            {
                Skills =
                [
                    new()
                    {
                        Type = "custom",
                        SkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                        Version = newVersion.Version
                    }
                ]
            },
            Messages = [new() { Role = Role.User, Content = "Use updated Skill" }],
            Tools =
            [
                new() { Type = "code_execution_20250825", Name = "code_execution" }
            ]
        };

        var response = await client.Beta.Messages.Create(specificVersionParams);
        Console.WriteLine(response);

        // Use latest version
        var latestVersionParams = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
            Container = new()
            {
                Skills =
                [
                    new()
                    {
                        Type = "custom",
                        SkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                        Version = "latest"
                    }
                ]
            },
            Messages = [new() { Role = Role.User, Content = "Use latest Skill version" }],
            Tools =
            [
                new() { Type = "code_execution_20250825", Name = "code_execution" }
            ]
        };

        var latestResponse = await client.Beta.Messages.Create(latestVersionParams);
        Console.WriteLine(latestResponse);
    }
}
```

```go Go nocheck hidelines={1..13,87..88}
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	// Create a new version
	skillFile := mustOpen("/path/to/updated_skill/SKILL.md")
	defer skillFile.Close()

	newVersion, err := client.Beta.Skills.Versions.New(
		context.TODO(),
		"skill_01AbCdEfGhIjKlMnOpQrStUv",
		anthropic.BetaSkillVersionNewParams{
			Files: []io.Reader{skillFile},
			Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaSkills2025_10_02},
		},
	)
	if err != nil {
		log.Fatal(err)
	}

	// Use specific version
	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeCustom,
						SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
						Version: anthropic.String(newVersion.Version),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Use updated Skill")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)

	// Use latest version
	latestResponse, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeCustom,
						SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Use latest Skill version")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(latestResponse)
}

func mustOpen(path string) *os.File {
	f, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	return f
}
```

```java Java nocheck hidelines={1..4,10..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaContainerParams;
import com.anthropic.models.beta.messages.BetaSkillParams;
import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
import com.anthropic.models.beta.skills.versions.VersionCreateParams;
import com.anthropic.models.beta.skills.versions.VersionCreateResponse;
import java.nio.file.Path;

public class SkillVersioning {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Create a new version
        VersionCreateParams versionParams = VersionCreateParams.builder()
            .addFile(Path.of("/path/to/updated_skill/SKILL.md"))
            .addBeta("skills-2025-10-02")
            .build();

        VersionCreateResponse newVersion = client.beta().skills().versions()
            .create("skill_01AbCdEfGhIjKlMnOpQrStUv", versionParams);

        // Use specific version
        MessageCreateParams specificVersionParams = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .container(BetaContainerParams.builder()
                .addSkill(BetaSkillParams.builder()
                    .type(BetaSkillParams.Type.CUSTOM)
                    .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                    .version(newVersion.version())
                    .build())
                .build())
            .addUserMessage("Use updated Skill")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
            .build();

        BetaMessage response = client.beta().messages().create(specificVersionParams);
        System.out.println(response);

        // Use latest version
        MessageCreateParams latestVersionParams = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .container(BetaContainerParams.builder()
                .addSkill(BetaSkillParams.builder()
                    .type(BetaSkillParams.Type.CUSTOM)
                    .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                    .version("latest")
                    .build())
                .build())
            .addUserMessage("Use latest Skill version")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
            .build();

        BetaMessage latestResponse = client.beta().messages().create(latestVersionParams);
        System.out.println(latestResponse);
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

// Create a new version
$newVersion = $client->beta->skills->versions->create(
    skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
    files: [fopen("/path/to/updated_skill/SKILL.md", "r")],
    betas: ["skills-2025-10-02"]
);

// Use specific version
$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [['role' => 'user', 'content' => 'Use updated Skill']],
    model: 'claude-opus-4-7',
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: [
        'skills' => [[
            'type' => 'custom',
            'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
            'version' => $newVersion->version
        ]]
    ],
    tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
);
echo $response;

// Use latest version
$latestResponse = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [['role' => 'user', 'content' => 'Use latest Skill version']],
    model: 'claude-opus-4-7',
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: [
        'skills' => [[
            'type' => 'custom',
            'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
            'version' => 'latest'
        ]]
    ],
    tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
);
echo $latestResponse;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Create a new version
new_version = client.beta.skills.versions.create(
  "skill_01AbCdEfGhIjKlMnOpQrStUv",
  files: [File.open("/path/to/updated_skill/SKILL.md")],
  betas: ["skills-2025-10-02"]
)

# Use specific version
response = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [{
      type: "custom",
      skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
      version: new_version.version
    }]
  },
  messages: [{ role: "user", content: "Use updated Skill" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
)
puts response

# Use latest version
latest_response = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [{
      type: "custom",
      skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
      version: "latest"
    }]
  },
  messages: [{ role: "user", content: "Use latest Skill version" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
)
puts latest_response
```
</CodeGroup>

Lihat [referensi API Create Skill Version](/docs/id/api/skills/create-skill-version) untuk detail lengkap.

---

## Bagaimana Skill Dimuat

Ketika Anda menentukan Skills dalam container:

1. **Penemuan Metadata:** Claude melihat metadata untuk setiap Skill (nama, deskripsi) dalam system prompt
2. **Pemuatan File:** File Skill disalin ke dalam container di `/skills/{directory}/`
3. **Penggunaan Otomatis:** Claude secara otomatis memuat dan menggunakan Skills ketika relevan dengan permintaan Anda
4. **Komposisi:** Beberapa Skills bersama-sama untuk alur kerja yang kompleks

Arsitektur pengungkapan progresif memastikan penggunaan konteks yang efisien: Claude hanya memuat instruksi Skill lengkap ketika diperlukan.

---

## Use Cases

### Organizational Skills

**Brand & Communications**
- Terapkan pemformatan khusus perusahaan (warna, font, tata letak) ke dokumen
- Hasilkan komunikasi mengikuti template organisasi
- Pastikan pedoman merek yang konsisten di semua output

**Project Management**
- Struktur catatan dengan format khusus perusahaan (OKRs, decision logs)
- Hasilkan tugas mengikuti konvensi tim
- Buat ringkasan rapat dan pembaruan status yang terstandar

**Business Operations**
- Buat laporan, proposal, dan analisis standar perusahaan
- Jalankan prosedur analitik khusus perusahaan
- Hasilkan model keuangan mengikuti template organisasi

### Personal Skills

**Content Creation**
- Template dokumen khusus
- Pemformatan dan styling khusus
- Pembuatan konten khusus domain

**Data Analysis**
- Pipeline pemrosesan data khusus
- Template visualisasi khusus
- Metode analitik khusus industri

**Development & Automation**
- Template pembuatan kode
- Framework pengujian
- Alur kerja deployment

### Contoh: Pemodelan Keuangan

Gabungkan Excel dan Skill analisis DCF khusus:

<CodeGroup>

```bash Shell nocheck
# Buat Skill analisis DCF khusus
DCF_SKILL=$(curl -X POST "https://api.anthropic.com/v1/skills" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02" \
  -F "display_title=DCF Analysis" \
  -F "files[]=@dcf_skill/SKILL.md;filename=dcf_skill/SKILL.md")

DCF_SKILL_ID=$(echo "$DCF_SKILL" | jq -r '.id')

# Gunakan dengan Excel untuk membuat model keuangan
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d "{
    \"model\": \"claude-opus-4-7\",
    \"max_tokens\": 4096,
    \"container\": {
      \"skills\": [
        {
          \"type\": \"anthropic\",
          \"skill_id\": \"xlsx\",
          \"version\": \"latest\"
        },
        {
          \"type\": \"custom\",
          \"skill_id\": \"$DCF_SKILL_ID\",
          \"version\": \"latest\"
        }
      ]
    },
    \"messages\": [{
      \"role\": \"user\",
      \"content\": \"Build a DCF valuation model for a SaaS company with the attached financials\"
    }],
    \"tools\": [{
      \"type\": \"code_execution_20250825\",
      \"name\": \"code_execution\"
    }]
  }"
```

```bash CLI nocheck
# Buat Skill analisis DCF khusus
DCF_SKILL_ID=$(ant beta:skills create \
  --display-title "DCF Analysis" \
  --file dcf_skill/SKILL.md \
  --transform id --format yaml)

# Gunakan dengan Excel untuk membuat model keuangan
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<YAML
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: xlsx
      version: latest
    - type: custom
      skill_id: $DCF_SKILL_ID
      version: latest
messages:
  - role: user
    content: Build a DCF valuation model for a SaaS company with the attached financials
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
```

```python Python nocheck
# Buat Skill analisis DCF khusus
from anthropic.lib import files_from_dir

dcf_skill = client.beta.skills.create(
    display_title="DCF Analysis",
    files=files_from_dir("/path/to/dcf_skill"),
    betas=["skills-2025-10-02"],
)

# Gunakan dengan Excel untuk membuat model keuangan
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
            {"type": "custom", "skill_id": dcf_skill.id, "version": "latest"},
        ]
    },
    messages=[
        {
            "role": "user",
            "content": "Build a DCF valuation model for a SaaS company with the attached financials",
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript nocheck
// Buat Skill analisis DCF khusus
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

const client = new Anthropic();

const dcfSkill = await client.beta.skills.create({
  display_title: "DCF Analysis",
  files: [await toFile(fs.createReadStream("dcf_skill.zip"), "skill.zip")],
  betas: ["skills-2025-10-02"]
});

// Gunakan dengan Excel untuk membuat model keuangan
const response = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      { type: "anthropic", skill_id: "xlsx", version: "latest" },
      { type: "custom", skill_id: dcfSkill.id, version: "latest" }
    ]
  },
  messages: [
    {
      role: "user",
      content: "Build a DCF valuation model for a SaaS company with the attached financials"
    }
  ],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});
```

```csharp C# nocheck hidelines={1..7}
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Messages;

var client = new AnthropicClient();

// Buat Skill analisis DCF khusus
var dcfSkill = await client.Beta.Skills.Create(new SkillCreateParams
{
    DisplayTitle = "DCF Analysis",
    Files = new[] { new SkillFileParam { Path = "dcf_skill/SKILL.md", Content = skillContent } },
    Betas = new[] { "skills-2025-10-02" },
});

// Gunakan dengan Excel untuk membuat model keuangan
var parameters = new MessageCreateParams
{
    Model = "claude-opus-4-7",
    MaxTokens = 4096,
    Betas = new[] { "code-execution-2025-08-25", "skills-2025-10-02" },
    Container = new BetaContainerParams
    {
        Skills = new[]
        {
            new BetaSkillParam
            {
                Type = "anthropic",
                SkillId = "xlsx",
                Version = "latest"
            },
            new BetaSkillParam
            {
                Type = "custom",
                SkillId = dcfSkill.Id,
                Version = "latest"
            }
        }
    },
    Messages = new[]
    {
        new BetaMessageParam
        {
            Role = Role.User,
            Content = "Build a DCF valuation model for a SaaS company with the attached financials"
        }
    },
    Tools = new[]
    {
        new BetaToolParam
        {
            Type = "code_execution_20250825",
            Name = "code_execution"
        }
    }
};

var message = await client.Beta.Messages.Create(parameters);
Console.WriteLine(message);
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

	// Buat Skill analisis DCF khusus (ID diperoleh dari Skills API)
	dcfSkillID := "skill_01AbCdEfGhIjKlMnOpQrStUv"

	// Gunakan dengan Excel untuk membuat model keuangan
	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas: []anthropic.AnthropicBeta{
			"code-execution-2025-08-25",
			anthropic.AnthropicBetaSkills2025_10_02,
		},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeAnthropic,
						SkillID: "xlsx",
						Version: anthropic.String("latest"),
					},
					{
						Type:    anthropic.BetaSkillParamsTypeCustom,
						SkillID: dcfSkillID,
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Build a DCF valuation model for a SaaS company with the attached financials")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..4,8..11,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaContainerParams;
import com.anthropic.models.beta.messages.BetaSkillParams;
import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
import java.util.List;

public class CustomSkillExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Buat Skill analisis DCF khusus (melalui Skills API)
        String dcfSkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv"; // Dari respons create Skills API

        // Gunakan dengan Skill Excel untuk membuat model keuangan
        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .container(BetaContainerParams.builder()
                .skills(List.of(
                    BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.ANTHROPIC)
                        .skillId("xlsx")
                        .version("latest")
                        .build(),
                    BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.CUSTOM)
                        .skillId(dcfSkillId)
                        .version("latest")
                        .build()
                ))
                .build())
            .addUserMessage("Build a DCF valuation model for a SaaS company with the attached financials")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
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

// Buat Skill analisis DCF khusus
$dcfSkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv"; // Dari respons API

// Gunakan dengan Excel untuk membuat model keuangan
$message = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Build a DCF valuation model for a SaaS company with the attached financials']
    ],
    model: 'claude-opus-4-7',
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: [
        'skills' => [
            ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest'],
            ['type' => 'custom', 'skill_id' => $dcfSkillId, 'version' => 'latest']
        ]
    ],
    tools: [
        ['type' => 'code_execution_20250825', 'name' => 'code_execution']
    ]
);
echo $message->content[0]->text;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Buat Skill analisis DCF khusus
dcf_skill = client.beta.skills.create(
  display_title: "DCF Analysis",
  files: [
    File.open("dcf_skill/SKILL.md", "rb")
  ],
  betas: ["skills-2025-10-02"]
)

# Gunakan dengan Excel untuk membuat model keuangan
response = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      { type: "anthropic", skill_id: "xlsx", version: "latest" },
      { type: "custom", skill_id: dcf_skill.id, version: "latest" }
    ]
  },
  messages: [
    { role: "user", content: "Build a DCF valuation model for a SaaS company with the attached financials" }
  ],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
)
```
</CodeGroup>

---

## Batas dan Kendala

### Batas Permintaan
- **Skill maksimal per permintaan:** 8
- **Ukuran unggah Skill maksimal:** 30&nbsp;MB (semua file digabungkan)
- **Persyaratan frontmatter YAML:**
  - `name`: Maksimal 64 karakter, hanya huruf kecil/angka/tanda hubung, tanpa tag XML, tanpa kata-kata yang dicadangkan
  - `description`: Maksimal 1024 karakter, tidak kosong, tanpa tag XML

### Kendala Lingkungan
Skill berjalan dalam kontainer eksekusi kode dengan batasan berikut:
- **Tidak ada akses jaringan** - Tidak dapat melakukan panggilan API eksternal
- **Tidak ada instalasi paket runtime** - Hanya paket yang sudah diinstal sebelumnya yang tersedia
- **Lingkungan terisolasi** - Setiap permintaan mendapatkan kontainer segar

Lihat [dokumentasi alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk paket yang tersedia.

---

## Praktik Terbaik

### Kapan Menggunakan Beberapa Skill

Gabungkan Skill ketika tugas melibatkan beberapa jenis dokumen atau domain:

**Kasus penggunaan yang baik:**
- Analisis data (Excel) + pembuatan presentasi (PowerPoint)
- Pembuatan laporan (Word) + ekspor ke PDF
- Logika domain khusus + pembuatan dokumen

**Hindari:**
- Menyertakan Skill yang tidak digunakan (mempengaruhi kinerja)

### Strategi Manajemen Versi

**Untuk produksi:**

```python nocheck
# Sematkan ke versi spesifik untuk stabilitas
container = {
    "skills": [
        {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "1759178010641129",  # Versi spesifik
        }
    ]
}
```

**Untuk pengembangan:**

```python nocheck
# Gunakan latest untuk pengembangan aktif
container = {
    "skills": [
        {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest",  # Selalu dapatkan yang terbaru
        }
    ]
}
```

### Pertimbangan Prompt Caching

Saat menggunakan prompt caching, perhatikan bahwa mengubah daftar Skill dalam kontainer Anda memecahkan cache:

<CodeGroup>
```bash Shell
# Permintaan pertama membuat cache
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,prompt-caching-2024-07-31" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-7",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
      ]
    },
    "messages": [{"role": "user", "content": "Analyze sales data"}],
    "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
  }'

# Menambah/menghapus Skill memecahkan cache
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,prompt-caching-2024-07-31" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-7",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
        {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
      ]
    },
    "messages": [{"role": "user", "content": "Create a presentation"}],
    "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
  }'
```

```bash CLI
# Permintaan pertama membuat cache
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
  --beta prompt-caching-2024-07-31 <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: xlsx
      version: latest
messages:
  - role: user
    content: Analyze sales data
tools:
  - type: code_execution_20250825
    name: code_execution
YAML

# Menambah/menghapus Skill memecahkan cache
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
  --beta prompt-caching-2024-07-31 <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: xlsx
      version: latest
    - type: anthropic
      skill_id: pptx
      version: latest
messages:
  - role: user
    content: Create a presentation
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
```

```python Python
# Permintaan pertama membuat cache
response1 = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=[
        "code-execution-2025-08-25",
        "skills-2025-10-02",
        "prompt-caching-2024-07-31",
    ],
    container={
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
    },
    messages=[{"role": "user", "content": "Analyze sales data"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

# Menambah/menghapus Skill memecahkan cache
response2 = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    betas=[
        "code-execution-2025-08-25",
        "skills-2025-10-02",
        "prompt-caching-2024-07-31",
    ],
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
            {
                "type": "anthropic",
                "skill_id": "pptx",
                "version": "latest",
            },  # Cache miss
        ]
    },
    messages=[{"role": "user", "content": "Create a presentation"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript
// Permintaan pertama membuat cache
const response1 = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02", "prompt-caching-2024-07-31"],
  container: {
    skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
  },
  messages: [{ role: "user", content: "Analyze sales data" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});

// Menambah/menghapus Skill memecahkan cache
const response2 = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02", "prompt-caching-2024-07-31"],
  container: {
    skills: [
      { type: "anthropic", skill_id: "xlsx", version: "latest" },
      { type: "anthropic", skill_id: "pptx", version: "latest" } // Cache miss
    ]
  },
  messages: [{ role: "user", content: "Create a presentation" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        // Permintaan pertama membuat cache
        var parameters1 = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Betas = new[] { "code-execution-2025-08-25", "skills-2025-10-02", "prompt-caching-2024-07-31" },
            Container = new BetaContainer
            {
                Skills = new[]
                {
                    new BetaSkill { Type = "anthropic", SkillId = "xlsx", Version = "latest" }
                }
            },
            Messages = new[] { new BetaMessageParam { Role = Role.User, Content = "Analyze sales data" } },
            Tools = new[] { new BetaTool { Type = "code_execution_20250825", Name = "code_execution" } }
        };
        var response1 = await client.Beta.Messages.Create(parameters1);
        Console.WriteLine(response1);

        // Menambah/menghapus Skill memecahkan cache
        var parameters2 = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Betas = new[] { "code-execution-2025-08-25", "skills-2025-10-02", "prompt-caching-2024-07-31" },
            Container = new BetaContainer
            {
                Skills = new[]
                {
                    new BetaSkill { Type = "anthropic", SkillId = "xlsx", Version = "latest" },
                    new BetaSkill { Type = "anthropic", SkillId = "pptx", Version = "latest" }
                }
            },
            Messages = new[] { new BetaMessageParam { Role = Role.User, Content = "Create a presentation" } },
            Tools = new[] { new BetaTool { Type = "code_execution_20250825", Name = "code_execution" } }
        };
        var response2 = await client.Beta.Messages.Create(parameters2);
        Console.WriteLine(response2);
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

	// Permintaan pertama membuat cache
	response1, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas: []anthropic.AnthropicBeta{
			"code-execution-2025-08-25",
			anthropic.AnthropicBetaSkills2025_10_02,
			anthropic.AnthropicBetaPromptCaching2024_07_31,
		},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeAnthropic,
						SkillID: "xlsx",
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Analyze sales data")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response1)

	// Menambah/menghapus Skill memecahkan cache
	response2, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas: []anthropic.AnthropicBeta{
			"code-execution-2025-08-25",
			anthropic.AnthropicBetaSkills2025_10_02,
			anthropic.AnthropicBetaPromptCaching2024_07_31,
		},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeAnthropic,
						SkillID: "xlsx",
						Version: anthropic.String("latest"),
					},
					{
						Type:    anthropic.BetaSkillParamsTypeAnthropic,
						SkillID: "pptx",
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a presentation")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response2)
}
```

```java Java hidelines={1..4,8..11,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaContainerParams;
import com.anthropic.models.beta.messages.BetaSkillParams;
import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
import java.util.List;

public class SkillsCaching {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Permintaan pertama membuat cache
        MessageCreateParams params1 = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .addBeta("prompt-caching-2024-07-31")
            .container(BetaContainerParams.builder()
                .skills(List.of(
                    BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.ANTHROPIC)
                        .skillId("xlsx")
                        .version("latest")
                        .build()
                ))
                .build())
            .addUserMessage("Analyze sales data")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
            .build();

        BetaMessage response1 = client.beta().messages().create(params1);
        System.out.println(response1);

        // Menambah/menghapus Skill memecahkan cache
        MessageCreateParams params2 = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(4096L)
            .addBeta("code-execution-2025-08-25")
            .addBeta("skills-2025-10-02")
            .addBeta("prompt-caching-2024-07-31")
            .container(BetaContainerParams.builder()
                .skills(List.of(
                    BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.ANTHROPIC)
                        .skillId("xlsx")
                        .version("latest")
                        .build(),
                    BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.ANTHROPIC)
                        .skillId("pptx")
                        .version("latest")
                        .build()
                ))
                .build())
            .addUserMessage("Create a presentation")
            .addTool(BetaCodeExecutionTool20250825.builder().build())
            .build();

        BetaMessage response2 = client.beta().messages().create(params2);
        System.out.println(response2);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

// Permintaan pertama membuat cache
$response1 = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Analyze sales data']
    ],
    model: 'claude-opus-4-7',
    betas: [
        'code-execution-2025-08-25',
        'skills-2025-10-02',
        'prompt-caching-2024-07-31'
    ],
    container: [
        'skills' => [
            ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
        ]
    ],
    tools: [
        ['type' => 'code_execution_20250825', 'name' => 'code_execution']
    ]
);
echo $response1;

// Menambah/menghapus Skill memecahkan cache
$response2 = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Create a presentation']
    ],
    model: 'claude-opus-4-7',
    betas: [
        'code-execution-2025-08-25',
        'skills-2025-10-02',
        'prompt-caching-2024-07-31'
    ],
    container: [
        'skills' => [
            ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest'],
            ['type' => 'anthropic', 'skill_id' => 'pptx', 'version' => 'latest']
        ]
    ],
    tools: [
        ['type' => 'code_execution_20250825', 'name' => 'code_execution']
    ]
);
echo $response2;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Permintaan pertama membuat cache
response1 = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: [
    "code-execution-2025-08-25",
    "skills-2025-10-02",
    "prompt-caching-2024-07-31"
  ],
  container: {
    skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
  },
  messages: [{ role: "user", content: "Analyze sales data" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
)
puts response1

# Menambah/menghapus Skill memecahkan cache
response2 = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  betas: [
    "code-execution-2025-08-25",
    "skills-2025-10-02",
    "prompt-caching-2024-07-31"
  ],
  container: {
    skills: [
      { type: "anthropic", skill_id: "xlsx", version: "latest" },
      { type: "anthropic", skill_id: "pptx", version: "latest" }
    ]
  },
  messages: [{ role: "user", content: "Create a presentation" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
)
puts response2
```
</CodeGroup>

Untuk kinerja caching terbaik, jaga daftar Skill Anda tetap konsisten di seluruh permintaan.

### Penanganan Kesalahan

Tangani kesalahan terkait Skill dengan baik:

<CodeGroup>

```bash CLI nocheck
if ! RESULT=$(ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
  --transform-error error.message --format-error yaml 2>&1 <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
container:
  skills:
    - type: custom
      skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
      version: latest
messages:
  - role: user
    content: Process data
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
); then
  case "$RESULT" in
    *skill*)
      printf 'Skill error: %s\n' "$RESULT"
      # Handle skill-specific errors
      ;;
    *)
      printf '%s\n' "$RESULT" >&2
      exit 1
      ;;
  esac
fi
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

try:
    response = client.beta.messages.create(
        model="claude-opus-4-7",
        max_tokens=4096,
        betas=["code-execution-2025-08-25", "skills-2025-10-02"],
        container={
            "skills": [
                {
                    "type": "custom",
                    "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                    "version": "latest",
                }
            ]
        },
        messages=[{"role": "user", "content": "Process data"}],
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    )
except anthropic.BadRequestError as e:
    if "skill" in str(e):
        print(f"Skill error: {e}")
        # Handle skill-specific errors
    else:
        raise
```

```typescript TypeScript nocheck
try {
  const response = await client.beta.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        { type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }
      ]
    },
    messages: [{ role: "user", content: "Process data" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
} catch (error) {
  if (error instanceof Anthropic.BadRequestError && error.message.includes("skill")) {
    console.error(`Skill error: ${error.message}`);
    // Handle skill-specific errors
  } else {
    throw error;
  }
}
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
        var client = new AnthropicClient();

        try
        {
            var parameters = new MessageCreateParams
            {
                Model = "claude-opus-4-7",
                MaxTokens = 4096,
                Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
                Container = new BetaContainerParams
                {
                    Skills = [
                        new BetaSkillParam
                        {
                            Type = "custom",
                            SkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                            Version = "latest"
                        }
                    ]
                },
                Messages = [new() { Role = Role.User, Content = "Process data" }],
                Tools = [new BetaToolParam { Type = "code_execution_20250825", Name = "code_execution" }]
            };

            var message = await client.Beta.Messages.Create(parameters);
            Console.WriteLine(message);
        }
        catch (Exception e) when (e.Message.Contains("skill"))
        {
            Console.WriteLine($"Skill error: {e.Message}");
        }
    }
}
```

```go Go nocheck hidelines={1..14,-1}
package main

import (
	"context"
	"fmt"
	"log"
	"strings"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	_, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 4096,
		Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
		Container: anthropic.BetaMessageNewParamsContainerUnion{
			OfContainers: &anthropic.BetaContainerParams{
				Skills: []anthropic.BetaSkillParams{
					{
						Type:    anthropic.BetaSkillParamsTypeCustom,
						SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
						Version: anthropic.String("latest"),
					},
				},
			},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Process data")),
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
		},
	})

	if err != nil {
		if strings.Contains(err.Error(), "skill") {
			fmt.Printf("Skill error: %v\n", err)
		} else {
			log.Fatal(err)
		}
	}
}
```

```java Java nocheck hidelines={1..4,8..10,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaContainerParams;
import com.anthropic.models.beta.messages.BetaSkillParams;
import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;

public class SkillErrorHandling {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        try {
            MessageCreateParams params = MessageCreateParams.builder()
                .model("claude-opus-4-7")
                .maxTokens(4096L)
                .addBeta("code-execution-2025-08-25")
                .addBeta("skills-2025-10-02")
                .container(BetaContainerParams.builder()
                    .addSkill(BetaSkillParams.builder()
                        .type(BetaSkillParams.Type.CUSTOM)
                        .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                        .version("latest")
                        .build())
                    .build())
                .addUserMessage("Process data")
                .addTool(BetaCodeExecutionTool20250825.builder().build())
                .build();

            BetaMessage response = client.beta().messages().create(params);
            System.out.println(response);
        } catch (Exception e) {
            if (e.getMessage().contains("skill")) {
                System.err.println("Skill error: " + e.getMessage());
            } else {
                throw e;
            }
        }
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

try {
    $message = $client->beta->messages->create(
        maxTokens: 4096,
        messages: [
            ['role' => 'user', 'content' => 'Process data']
        ],
        model: 'claude-opus-4-7',
        betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
        container: [
            'skills' => [
                [
                    'type' => 'custom',
                    'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                    'version' => 'latest'
                ]
            ]
        ],
        tools: [
            ['type' => 'code_execution_20250825', 'name' => 'code_execution']
        ]
    );
    echo $message->content[0]->text;
} catch (Exception $e) {
    if (str_contains($e->getMessage(), 'skill')) {
        echo "Skill error: " . $e->getMessage();
    } else {
        throw $e;
    }
}
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

begin
  response = client.beta.messages.create(
    model: "claude-opus-4-7",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: [{ role: "user", content: "Process data" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
rescue Anthropic::Errors::BadRequestError => e
  if e.message.include?("skill")
    puts "Skill error: #{e.message}"
  else
    raise
  end
end
```
</CodeGroup>

---

## Retensi Data

Agent Skills tidak tercakup oleh pengaturan ZDR. Definisi Skill dan data eksekusi disimpan sesuai dengan kebijakan retensi data standar Anthropic.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/build-with-claude/api-and-data-retention).

## Langkah Selanjutnya

<CardGroup cols={2}>
  <Card
    title="Referensi API"
    icon="book"
    href="/docs/id/api/skills/create-skill"
  >
    Referensi API lengkap dengan semua endpoint
  </Card>
  <Card
    title="Panduan Penulisan"
    icon="edit"
    href="/docs/id/agents-and-tools/agent-skills/best-practices"
  >
    Praktik terbaik untuk menulis Skills yang efektif
  </Card>
  <Card
    title="Alat Eksekusi Kode"
    icon="terminal"
    href="/docs/id/agents-and-tools/tool-use/code-execution-tool"
  >
    Pelajari tentang lingkungan eksekusi kode
  </Card>
</CardGroup>