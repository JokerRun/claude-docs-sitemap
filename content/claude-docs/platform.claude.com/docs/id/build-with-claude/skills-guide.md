---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/skills-guide
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 44aa5c551617b4121f1b7911397b0ab3ef9d2d69b9fad55f4fefb5be424d5a28
---

# Menggunakan Agent Skills dengan API

Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.

---

Agent Skills memperluas kemampuan Claude melalui folder terorganisir yang berisi instruksi, skrip, dan sumber daya. Panduan ini menunjukkan cara menggunakan Skill bawaan maupun Skill kustom dengan Claude API.

<Note>
Untuk referensi API lengkap termasuk skema request/response dan semua parameter, lihat:
- [Referensi API Manajemen Skill](/docs/id/api/skills/list-skills) - Operasi CRUD untuk Skill
- [Referensi API Versi Skill](/docs/id/api/skills/list-skill-versions) - Manajemen versi
</Note>

<Note>
Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Tautan cepat \{#quick-links}

<CardGroup cols={2}>
  <Card
    title="Memulai dengan Agent Skills"
    icon="rocket"
    href="/docs/id/agents-and-tools/agent-skills/quickstart"
  >
    Buat Skill pertama Anda
  </Card>
  <Card
    title="Membuat Skill kustom"
    icon="hammer"
    href="/docs/id/agents-and-tools/agent-skills/best-practices"
  >
    Praktik terbaik untuk menulis Skill
  </Card>
</CardGroup>

## Ikhtisar \{#overview}

<Note>
Untuk pembahasan mendalam tentang arsitektur dan penerapan Agent Skills di dunia nyata, baca postingan blog engineering: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

Skill terintegrasi dengan Messages API melalui [code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool). Baik menggunakan Skill bawaan yang dikelola oleh Anthropic maupun Skill kustom yang telah Anda unggah, bentuk integrasinya identik: keduanya memerlukan eksekusi kode dan menggunakan struktur `container` yang sama.

### Menggunakan Skill \{#using-skills}

Skill terintegrasi secara identik di Messages API terlepas dari sumbernya. Anda menentukan Skill dalam parameter `container` dengan `skill_id`, `type`, dan `version` opsional, dan Skill tersebut dieksekusi di lingkungan eksekusi kode.

**Anda dapat menggunakan Skill dari dua sumber:**

| Aspek | Skill Anthropic | Skill Kustom |
|--------|------------------|---------------|
| **Nilai type** | `anthropic` | `custom` |
| **Skill ID** | Nama pendek: `pptx`, `xlsx`, `docx`, `pdf` | Dihasilkan otomatis: `skill_01AbCdEfGhIjKlMnOpQrStUv` |
| **Format versi** | Berbasis tanggal: `20251013` atau `latest` | Epoch timestamp: `1759178010641129` atau `latest` |
| **Pengelolaan** | Dibuat dan dikelola oleh Anthropic | Unggah dan kelola melalui [Skills API](/docs/id/api/skills/create-skill) |
| **Ketersediaan** | Tersedia untuk semua pengguna | Privat untuk workspace Anda |

Kedua sumber Skill dikembalikan oleh [endpoint List Skills](/docs/id/api/skills/list-skills) (gunakan parameter `source` untuk memfilter). Bentuk integrasi dan lingkungan eksekusinya identik. Satu-satunya perbedaan adalah dari mana Skill berasal dan bagaimana Skill tersebut dikelola.

### Prasyarat \{#prerequisites}

Untuk menggunakan Skill, Anda memerlukan:

1. **Kunci API Claude** dari [Console](/settings/keys)
2. **Header beta:**
   - `code-execution-2025-08-25` - Mengaktifkan eksekusi kode (diperlukan untuk Skill)
   - `skills-2025-10-02` - Mengaktifkan Skills API
   - `files-api-2025-04-14` - Untuk mengunggah/mengunduh file ke/dari container
3. **[Code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool)** diaktifkan dalam permintaan Anda

---

## Menggunakan Skill dalam Messages \{#using-skills-in-messages}

### Parameter container \{#container-parameter}

Skill ditentukan menggunakan parameter `container` di Messages API. Anda dapat menyertakan hingga 8 Skill per permintaan.

Strukturnya identik untuk Skill Anthropic maupun Skill kustom. Tentukan `type` dan `skill_id` yang diperlukan, dan secara opsional sertakan `version` untuk mengunci ke versi tertentu:

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
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
model: claude-opus-4-8
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
    model="claude-opus-4-8",
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
  model: "claude-opus-4-8",
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
            Model = Model.ClaudeOpus4_8,
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
		Model:     "claude-opus-4-8",
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
            .model("claude-opus-4-8")
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

$client = new Client();

$message = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Create a presentation about renewable energy']
    ],
    model: 'claude-opus-4-8',
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
  model: "claude-opus-4-8",
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

### Mengunduh file yang dihasilkan \{#downloading-generated-files}

Ketika Skill membuat dokumen (Excel, PowerPoint, PDF, Word), Skill mengembalikan atribut `file_id` dalam respons. Anda harus menggunakan Files API untuk mengunduh file-file ini.

**Cara kerjanya:**
1. Skill membuat file selama eksekusi kode
2. Respons menyertakan `file_id` untuk setiap file yang dibuat
3. Gunakan Files API untuk mengunduh konten file yang sebenarnya
4. Simpan secara lokal atau proses sesuai kebutuhan

**Contoh: Membuat dan mengunduh file Excel**

<CodeGroup>

```bash cURL hidelines={1}
cd "$(mktemp -d)"
# Langkah 1: Gunakan Skill untuk membuat file
RESPONSE=$(curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
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

# Langkah 2: Ekstrak file_id dari respons (menggunakan jq)
FILE_ID=$(echo "$RESPONSE" | jq -r '.content[] | select(.type=="bash_code_execution_tool_result") | .content | select(.type=="bash_code_execution_result") | .content[] | select(.file_id) | .file_id')

# Langkah 3: Dapatkan nama file dari metadata
FILENAME=$(curl "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" | jq -r '.filename')

# Langkah 4: Unduh file menggunakan Files API
curl "https://api.anthropic.com/v1/files/$FILE_ID/content" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  --output "$FILENAME"

echo "Downloaded: $FILENAME"
```

```bash CLI nocheck hidelines={1}
cd "$(mktemp -d)"
# Langkah 1: Gunakan Skill xlsx untuk membuat file
# Langkah 2: Ekstrak file_id dari respons dengan --transform (path GJSON)
FILE_ID=$(ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
  --transform 'content.#.content.content.#.file_id|@flatten|0' \
  --raw-output <<'YAML'
model: claude-opus-4-8
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

# Langkah 3: Dapatkan nama file dari metadata file
FILENAME=$(ant beta:files retrieve-metadata \
  --file-id "$FILE_ID" \
  --transform filename --raw-output)

# Langkah 4: Unduh file menggunakan Files API
ant beta:files download \
  --file-id "$FILE_ID" \
  --output "$FILENAME" > /dev/null

printf 'Downloaded: %s\n' "$FILENAME"
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Langkah 1: Gunakan Skill untuk membuat file
response = client.beta.messages.create(
    model="claude-opus-4-8",
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


# Langkah 2: Ekstrak ID file dari respons
def extract_file_ids(response):
    file_ids = []
    for item in response.content:
        if item.type == "bash_code_execution_tool_result":
            content_item = item.content
            if content_item.type == "bash_code_execution_result":
                # list dengan tipe konkret: List[BashCodeExecutionOutputBlock]
                for file in content_item.content:
                    file_ids.append(file.file_id)
    return file_ids


# Langkah 3: Unduh file menggunakan Files API
for file_id in extract_file_ids(response):
    file_metadata = client.beta.files.retrieve_metadata(file_id=file_id)
    file_content = client.beta.files.download(file_id=file_id)

    # Langkah 4: Simpan ke disk
    file_content.write_to_file(file_metadata.filename)
    print(f"Downloaded: {file_metadata.filename}")
```

```typescript TypeScript hidelines={1..3}
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs/promises";

const client = new Anthropic();

// Langkah 1: Gunakan Skill untuk membuat file
const response = await client.beta.messages.create({
  model: "claude-opus-4-8",
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

// Langkah 2: Ekstrak ID file dari respons
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

// Langkah 3: Unduh file menggunakan Files API
for (const fileId of extractFileIds(response)) {
  const fileMetadata = await client.beta.files.retrieveMetadata(fileId);
  const fileContent = await client.beta.files.download(fileId);

  // Langkah 4: Simpan ke disk
  await fs.writeFile(fileMetadata.filename, Buffer.from(await fileContent.arrayBuffer()));
  console.log(`Downloaded: ${fileMetadata.filename}`);
}
```

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

        // Langkah 1: Gunakan Skill untuk membuat file
        var parameters = new MessageCreateParams
        {
            Model = "claude-opus-4-8",
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

        // Langkah 2: Ekstrak ID file dari respons
        var fileIds = ExtractFileIds(response);

        // Langkah 3: Unduh file menggunakan Files API
        foreach (var fileId in fileIds)
        {
            var fileMetadata = await client.Beta.Files.RetrieveMetadata(fileId);

            var fileContent = await client.Beta.Files.Download(fileId);

            // Langkah 4: Simpan ke disk
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

```go Go hidelines={1..15,68..69}
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

	// Langkah 1: Gunakan Skill untuk membuat file
	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-8",
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

	// Langkah 2: Ekstrak ID file dari respons
	fileIDs := extractFileIDs(response)

	// Langkah 3: Unduh file menggunakan Files API
	for _, fileID := range fileIDs {
		fileMetadata, err := client.Beta.Files.GetMetadata(context.TODO(), fileID, anthropic.BetaFileGetMetadataParams{})
		if err != nil {
			log.Fatal(err)
		}

		fileContent, err := client.Beta.Files.Download(context.TODO(), fileID, anthropic.BetaFileDownloadParams{})
		if err != nil {
			log.Fatal(err)
		}

		// Langkah 4: Simpan ke disk
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

        // Langkah 1: Gunakan Skill untuk membuat file
        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-opus-4-8")
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

        // Langkah 2: Ekstrak ID file dari respons
        List<String> fileIds = new ArrayList<>();
        for (BetaContentBlock block : response.content()) {
            if (block.isCodeExecutionToolResult()) {
                var toolResult = block.asCodeExecutionToolResult();
                for (var content : toolResult.content()) {
                    content.file().ifPresent(file -> fileIds.add(file.fileId()));
                }
            }
        }

        // Langkah 3: Unduh file menggunakan Files API
        for (String fileId : fileIds) {
            FileMetadata fileMetadata = client.beta().files().retrieveMetadata(fileId);
            HttpResponse fileContent = client.beta().files().download(fileId);

            // Langkah 4: Simpan ke disk
            try (InputStream is = fileContent.body();
                 FileOutputStream fos = new FileOutputStream(fileMetadata.filename())) {
                is.transferTo(fos);
            }
            System.out.println("Downloaded: " + fileMetadata.filename());
        }
    }
}
```

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

// Langkah 1: Gunakan Skill untuk membuat file
$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Create an Excel file with a simple budget spreadsheet']
    ],
    model: 'claude-opus-4-8',
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

// Langkah 2: Ekstrak ID file dari respons
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

// Langkah 3: Unduh file menggunakan Files API
foreach (extractFileIds($response) as $fileId) {
    $fileMetadata = $client->beta->files->retrieveMetadata($fileId);
    $fileContent  = $client->beta->files->download($fileId);

    // Langkah 4: Simpan ke disk
    file_put_contents($fileMetadata->filename, $fileContent);
    echo "Downloaded: {$fileMetadata->filename}\n";
}
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Langkah 1: Gunakan Skill untuk membuat file
response = client.beta.messages.create(
  model: "claude-opus-4-8",
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

# Langkah 2: Ekstrak ID file dari respons
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

# Langkah 3: Unduh file menggunakan Files API
extract_file_ids(response).each do |file_id|
  file_metadata = client.beta.files.retrieve_metadata(file_id)

  file_content = client.beta.files.download(file_id)

  # Langkah 4: Simpan ke disk
  File.binwrite(file_metadata.filename, file_content.read)
  puts "Downloaded: #{file_metadata.filename}"
end
```

</CodeGroup>

**Operasi Files API tambahan:**

<CodeGroup>
```bash cURL
# Dapatkan metadata file
curl "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"

# Daftar semua file
curl "https://api.anthropic.com/v1/files" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"

# Hapus file
curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

```bash CLI nocheck
# Dapatkan metadata file
ant beta:files retrieve-metadata --file-id "$FILE_ID" \
  --transform '{filename,size_bytes}' --format yaml \
  | { read -r _ name; read -r _ size
      printf 'Filename: %s, Size: %s bytes\n' "$name" "$size"; }

# Daftar semua file
ant beta:files list \
  --transform '{filename,created_at}' --format yaml \
  | while read -r _ name && read -r _ date; do
      printf '%s - %s\n' "$name" "${date//\"/}"
    done

# Hapus file
ant beta:files delete --file-id "$FILE_ID" >/dev/null
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
file_id = "file_abc123"
# Dapatkan metadata file
file_info = client.beta.files.retrieve_metadata(file_id=file_id)
print(f"Filename: {file_info.filename}, Size: {file_info.size_bytes} bytes")

# Daftar semua file
files = client.beta.files.list()
for file in files.data:
    print(f"{file.filename} - {file.created_at}")

# Hapus file
client.beta.files.delete(file_id=file_id)
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const fileId = "file_011CNha8iCJcU1wXNR6q4V8w";

// Dapatkan metadata file
const fileInfo = await client.beta.files.retrieveMetadata(fileId);
console.log(`Filename: ${fileInfo.filename}, Size: ${fileInfo.size_bytes} bytes`);

// Daftar semua file
const files = await client.beta.files.list();
for (const file of files.data) {
  console.log(`${file.filename} - ${file.created_at}`);
}

// Hapus file
await client.beta.files.delete(fileId);
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

        // Dapatkan metadata file
        var fileInfo = await client.Beta.Files.RetrieveMetadata(fileId);
        Console.WriteLine($"Filename: {fileInfo.Filename}, Size: {fileInfo.SizeBytes} bytes");

        // Daftar semua file
        var files = await client.Beta.Files.List();
        foreach (var file in files.Data)
        {
            Console.WriteLine($"{file.Filename} - {file.CreatedAt}");
        }

        // Hapus file
        await client.Beta.Files.Delete(fileId);
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

	// Dapatkan metadata file
	fileInfo, err := client.Beta.Files.GetMetadata(context.TODO(), fileID, anthropic.BetaFileGetMetadataParams{})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Filename: %s, Size: %d bytes\n", fileInfo.Filename, fileInfo.SizeBytes)

	// Daftar semua file
	files := client.Beta.Files.ListAutoPaging(context.TODO(), anthropic.BetaFileListParams{})
	for files.Next() {
		file := files.Current()
		fmt.Printf("%s - %s\n", file.Filename, file.CreatedAt)
	}

	// Hapus file
	_, err = client.Beta.Files.Delete(context.TODO(), fileID, anthropic.BetaFileDeleteParams{})
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

        // Dapatkan metadata file
        FileMetadata fileInfo = client.beta().files().retrieveMetadata(fileId);
        System.out.println("Filename: " + fileInfo.filename() + ", Size: " + fileInfo.sizeBytes() + " bytes");

        // Daftar semua file
        FileListPage files = client.beta().files().list();
        for (var file : files.data()) {
            System.out.println(file.filename() + " - " + file.createdAt());
        }

        // Hapus file
        client.beta().files().delete(fileId);
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client();
$fileId = "file_abc123";

// Dapatkan metadata file
$fileInfo = $client->beta->files->retrieveMetadata($fileId);
echo "Filename: {$fileInfo->filename}, Size: {$fileInfo->sizeBytes} bytes\n";

// Daftar semua file
$files = $client->beta->files->list();
foreach ($files->data as $file) {
    echo "{$file->filename} - {$file->createdAt}\n";
}

// Hapus file
$client->beta->files->delete($fileId);
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new
file_id = "file_abc123"

# Dapatkan metadata file
file_info = client.beta.files.retrieve_metadata(file_id)
puts "Filename: #{file_info.filename}, Size: #{file_info.size_bytes} bytes"

# Daftar semua file
files = client.beta.files.list
files.data.each do |file|
  puts "#{file.filename} - #{file.created_at}"
end

# Hapus file
client.beta.files.delete(file_id)
```
</CodeGroup>

<Note>
Untuk detail lengkap tentang Files API, lihat [dokumentasi Files API](/docs/id/api/files-content).
</Note>

### Percakapan multi-turn \{#multi-turn-conversations}

Gunakan kembali container yang sama di beberapa pesan dengan menentukan ID container:

<CodeGroup>
```bash CLI
# Permintaan pertama membuat kontainer
CONTAINER_ID=$(ant beta:messages create \
  --beta code-execution-2025-08-25 --beta skills-2025-10-02 \
  --transform container.id --raw-output <<'YAML'
model: claude-opus-4-8
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
model: claude-opus-4-8
max_tokens: 4096
container:
  id: $CONTAINER_ID  # Reuse container
  skills:
    - {type: anthropic, skill_id: xlsx, version: latest}
messages:
  - role: user
    content: Analyze this sales data
  - role: assistant
    content: []  # content blocks from the first response
  - role: user
    content: What was the total revenue?
tools:
  - {type: code_execution_20250825, name: code_execution}
YAML
```

```python Python
# Permintaan pertama membuat kontainer
response1 = client.beta.messages.create(
    model="claude-opus-4-8",
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
    model="claude-opus-4-8",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "id": response1.container.id,  # Reuse container
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}],
    },
    messages=messages,
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript
// Permintaan pertama membuat kontainer
const response1 = await client.beta.messages.create({
  model: "claude-opus-4-8",
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
  model: "claude-opus-4-8",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    id: response1.container!.id, // Reuse container
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
            Model = "claude-opus-4-8",
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
            Model = "claude-opus-4-8",
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
		Model:     "claude-opus-4-8",
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
		Model:     "claude-opus-4-8",
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
            .model("claude-opus-4-8")
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
            .model("claude-opus-4-8")
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

$client = new Client();

$response1 = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Analyze this sales data']
    ],
    model: 'claude-opus-4-8',
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
    model: 'claude-opus-4-8',
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
  model: "claude-opus-4-8",
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
  model: "claude-opus-4-8",
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

### Operasi yang berjalan lama \{#long-running-operations}

Skill mungkin melakukan operasi yang memerlukan beberapa turn. Tangani stop reason `pause_turn`:

<CodeGroup>

```bash cURL nocheck
# Permintaan awal
RESPONSE=$(curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
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
      \"model\": \"claude-opus-4-8\",
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

# Permintaan awal: tangkap respons JSON lengkap ke file sementara
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
 > "$RESP" <<'YAML'
model: claude-opus-4-8
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

  # Lanjutkan di kontainer yang sama, tambahkan array content dari
  # respons sebelumnya ke messages sebagai giliran asisten.
  ant beta:messages create \
    --beta code-execution-2025-08-25 \
    --beta skills-2025-10-02 \
 > "$RESP" <<YAML
model: claude-opus-4-8
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
    model="claude-opus-4-8",
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

# Tangani pause_turn untuk operasi yang lama
for i in range(max_retries):
    if response.stop_reason != "pause_turn":
        break

    messages.append({"role": "assistant", "content": response.content})
    response = client.beta.messages.create(
        model="claude-opus-4-8",
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
  model: "claude-opus-4-8",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [{ type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }]
  },
  messages,
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});

// Tangani pause_turn untuk operasi yang lama
for (let i = 0; i < maxRetries; i++) {
  if (response.stop_reason !== "pause_turn") {
    break;
  }

  messages.push({
    role: "assistant" as const,
    content: response.content as Anthropic.Beta.Messages.BetaContentBlockParam[]
  });
  response = await client.beta.messages.create({
    model: "claude-opus-4-8",
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
    Model = "claude-opus-4-8",
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
        Model = "claude-opus-4-8",
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
		Model:     "claude-opus-4-8",
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
			Model:     "claude-opus-4-8",
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
                .model("claude-opus-4-8")
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
                    .model("claude-opus-4-8")
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

$client = new Client();

$messages = [
    ['role' => 'user', 'content' => 'Process this large dataset']
];
$maxRetries = 10;

$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: $messages,
    model: 'claude-opus-4-8',
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
        model: 'claude-opus-4-8',
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
  model: "claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
Respons mungkin menyertakan stop reason `pause_turn`, yang menunjukkan bahwa API menjeda operasi Skill yang berjalan lama. Anda dapat memberikan respons tersebut kembali apa adanya dalam permintaan berikutnya agar Claude dapat melanjutkan turn-nya, atau memodifikasi konten jika Anda ingin menginterupsi percakapan dan memberikan panduan tambahan.
</Note>

### Menggunakan Beberapa Skill \{#using-multiple-skills}

Gabungkan beberapa Skill dalam satu permintaan untuk menangani alur kerja yang kompleks:

<CodeGroup>

```bash cURL nocheck
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
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
model: claude-opus-4-8
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
    model="claude-opus-4-8",
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
  model: "claude-opus-4-8",
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
            Model = "claude-opus-4-8",
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
            },
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
		Model:     "claude-opus-4-8",
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
            .model("claude-opus-4-8")
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

$client = new Client();

$message = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Analyze sales data and create a presentation']
    ],
    model: 'claude-opus-4-8',
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
  model: "claude-opus-4-8",
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

## Mengelola Skill Kustom \{#managing-custom-skills}

### Membuat Skill \{#creating-a-skill}

Bundle Skill adalah direktori yang berisi file `SKILL.md` di tingkat teratas dengan frontmatter YAML `name` dan `description`, ditambah skrip atau sumber daya pendukung apa pun. Lihat [Memulai dengan Agent Skills di API](/docs/id/agents-and-tools/agent-skills/quickstart) untuk membuatnya, dan daftar **Persyaratan** setelah contoh-contoh berikut untuk batasan lengkapnya.

Unggah Skill kustom Anda agar tersedia di workspace Anda. Anda dapat mengunggah arsip zip atau objek file individual; SDK Python juga menyediakan helper `files_from_dir` yang menerima path direktori.

<CodeGroup defaultLanguage="CLI">

```bash cURL nocheck
curl -X POST "https://api.anthropic.com/v1/skills" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02" \
  -F "display_title=Financial Analysis" \
  -F "files[]=@financial_skill/SKILL.md;filename=financial_skill/SKILL.md" \
  -F "files[]=@financial_skill/analyze.py;filename=financial_skill/analyze.py"
```

```bash CLI nocheck
# Opsi 1: Unggah file individual (satu flag --file per file)
ant beta:skills create \
  --display-title "Financial Analysis" \
  --file financial_skill/SKILL.md \
  --file financial_skill/analyze.py \
  --beta skills-2025-10-02

# Opsi 2: Unggah arsip zip
ant beta:skills create \
  --display-title "Financial Analysis" \
  --file financial_analysis_skill.zip \
  --beta skills-2025-10-02
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Opsi 1: Menggunakan helper files_from_dir (hanya Python, direkomendasikan)
from anthropic.lib import files_from_dir

skill = client.beta.skills.create(
    display_title="Financial Analysis",
    files=files_from_dir("/path/to/financial_analysis_skill"),
)

# Opsi 2: Menggunakan file zip
skill = client.beta.skills.create(
    display_title="Financial Analysis",
    files=[("skill.zip", open("financial_analysis_skill.zip", "rb"))],
)

# Opsi 3: Menggunakan tuple file (filename, file_content, mime_type)
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
)

print(f"Created skill: {skill.id}")
print(f"Latest version: {skill.latest_version}")
```

```typescript TypeScript nocheck
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

const client = new Anthropic();

// Opsi 1: Menggunakan file zip
const skillFromZip = await client.beta.skills.create({
  display_title: "Financial Analysis",
  files: [await toFile(fs.createReadStream("financial_analysis_skill.zip"), "skill.zip")]
});

// Opsi 2: Menggunakan objek file individual
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
  ]
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

        // Opsi 1: Menggunakan file zip
        var parameters = new SkillCreateParams
        {
            DisplayTitle = "Financial Analysis",
            Files = [
                new FileStream("financial_analysis_skill.zip", FileMode.Open, FileAccess.Read)
            ],
        };

        var skill = await client.Beta.Skills.Create(parameters);

        // Opsi 2: Menggunakan file individual
        var parameters2 = new SkillCreateParams
        {
            DisplayTitle = "Financial Analysis",
            Files = [
                new FileStream("financial_skill/SKILL.md", FileMode.Open, FileAccess.Read),
                new FileStream("financial_skill/analyze.py", FileMode.Open, FileAccess.Read)
            ],
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

	// Opsi 1: Menggunakan file zip
	zipFile, err := os.Open("financial_analysis_skill.zip")
	if err != nil {
		log.Fatal(err)
	}
	defer zipFile.Close()

	skill, err := client.Beta.Skills.New(context.TODO(), anthropic.BetaSkillNewParams{
		DisplayTitle: anthropic.String("Financial Analysis"),
		Files:        []io.Reader{zipFile},
	})
	if err != nil {
		log.Fatal(err)
	}

	// Opsi 2: Menggunakan file individual
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

        // Opsi 1: Menggunakan file zip
        SkillCreateParams params = SkillCreateParams.builder()
            .displayTitle("Financial Analysis")
            .addFile(new FileInputStream("financial_analysis_skill.zip"))
            .build();

        SkillCreateResponse skill = client.beta().skills().create(params);

        // Opsi 2: Menggunakan file individual
        SkillCreateParams params2 = SkillCreateParams.builder()
            .displayTitle("Financial Analysis")
            .addFile(Path.of("financial_skill/SKILL.md"))
            .addFile(Path.of("financial_skill/analyze.py"))
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

$client = new Client();

// Opsi 1: Menggunakan file zip
$skill = $client->beta->skills->create(
    displayTitle: 'Financial Analysis',
    files: [
        fopen('financial_analysis_skill.zip', 'r')
    ],
);

// Opsi 2: Menggunakan file individual
$skill = $client->beta->skills->create(
    displayTitle: 'Financial Analysis',
    files: [
        fopen('financial_skill/SKILL.md', 'r'),
        fopen('financial_skill/analyze.py', 'r')
    ],
);

echo "Created skill: {$skill->id}\n";
echo "Latest version: {$skill->latestVersion}\n";
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Opsi 1: Menggunakan file zip
skill = client.beta.skills.create(
  display_title: "Financial Analysis",
  files: [
    File.open("financial_analysis_skill.zip", "rb")
  ]
)

# Opsi 2: Menggunakan file individual
skill = client.beta.skills.create(
  display_title: "Financial Analysis",
  files: [
    File.open("financial_skill/SKILL.md", "rb"),
    File.open("financial_skill/analyze.py", "rb")
  ]
)

puts "Created skill: #{skill.id}"
puts "Latest version: #{skill.latest_version}"
```
</CodeGroup>

**Persyaratan:**
- Harus menyertakan file SKILL.md di tingkat teratas
- Semua file harus menentukan direktori root yang sama dalam path-nya
- Total ukuran unggahan harus di bawah 30&nbsp;MB
- Persyaratan frontmatter YAML:
  - `name`: Maksimum 64 karakter, hanya huruf kecil/angka/tanda hubung, tanpa tag XML, tanpa kata yang dicadangkan ("anthropic", "claude")
  - `description`: Maksimum 1024 karakter, tidak boleh kosong, tanpa tag XML

Untuk skema request/response lengkap, lihat [referensi API Create Skill](/docs/id/api/skills/create-skill).

### Menampilkan daftar Skill \{#listing-skills}

Ambil semua Skill yang tersedia untuk workspace Anda, termasuk Skill bawaan Anthropic dan Skill kustom Anda. Gunakan parameter `source` untuk memfilter berdasarkan jenis Skill:

<CodeGroup defaultLanguage="CLI">
```bash cURL
# Daftar semua Skill
curl "https://api.anthropic.com/v1/skills" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02"

# Daftar hanya Skill kustom
curl "https://api.anthropic.com/v1/skills?source=custom" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02"
```

```bash CLI
# Daftar semua Skill
ant beta:skills list

# Daftar hanya Skill kustom
ant beta:skills list --source custom
```

```python Python
# Daftar semua Skill
skills = client.beta.skills.list()

for skill in skills.data:
    print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

# Daftar hanya Skill kustom
custom_skills = client.beta.skills.list(source="custom")
```

```typescript TypeScript
// Daftar semua Skill
const skills = await client.beta.skills.list();

for (const skill of skills.data) {
  console.log(`${skill.id}: ${skill.display_title} (source: ${skill.source})`);
}

// Daftar hanya Skill kustom
const customSkills = await client.beta.skills.list({
  source: "custom"
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

        // Daftar semua Skill
        var skills = await client.Beta.Skills.List();

        foreach (var skill in skills.Data)
        {
            Console.WriteLine($"{skill.Id}: {skill.DisplayTitle} (source: {skill.Source})");
        }

        // Daftar hanya Skill kustom
        var customSkills = await client.Beta.Skills.List(new SkillListParams
        {
            Source = "custom",
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

	// Daftar semua Skill
	skills := client.Beta.Skills.ListAutoPaging(context.TODO(), anthropic.BetaSkillListParams{})

	for skills.Next() {
		skill := skills.Current()
		fmt.Printf("%s: %s (source: %s)\n", skill.ID, skill.DisplayTitle, skill.Source)
	}
	if skills.Err() != nil {
		log.Fatal(skills.Err())
	}

	// Daftar hanya Skill kustom
	customSkills := client.Beta.Skills.ListAutoPaging(context.TODO(), anthropic.BetaSkillListParams{
		Source: anthropic.String("custom"),
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

        // Daftar semua Skill
        SkillListPage skills = client.beta().skills().list();

        for (SkillListResponse skill : skills.data()) {
            System.out.println(skill.id() + ": " + skill.displayTitle() + " (source: " + skill.source() + ")");
        }

        // Daftar hanya Skill kustom
        SkillListParams customParams = SkillListParams.builder()
            .source("custom")
            .build();

        SkillListPage customSkills = client.beta().skills().list(customParams);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

// Daftar semua Skill
$skills = $client->beta->skills->list();

foreach ($skills->data as $skill) {
    echo "{$skill->id}: {$skill->displayTitle} (source: {$skill->source})\n";
}

// Daftar hanya Skill kustom
$customSkills = $client->beta->skills->list(
    source: 'custom',
);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Daftar semua Skill
skills = client.beta.skills.list

skills.data.each do |skill|
  puts "#{skill.id}: #{skill.display_title} (source: #{skill.source})"
end

# Daftar hanya Skill kustom
custom_skills = client.beta.skills.list(
  source: "custom"
)
```
</CodeGroup>

Lihat [referensi API List Skills](/docs/id/api/skills/list-skills) untuk opsi paginasi dan pemfilteran.

### Mengambil Skill \{#retrieving-a-skill}

Dapatkan detail tentang Skill tertentu:

<CodeGroup defaultLanguage="CLI">

```bash cURL nocheck
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
skill = client.beta.skills.retrieve(skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv")

print(f"Skill: {skill.display_title}")
print(f"Latest version: {skill.latest_version}")
print(f"Created: {skill.created_at}")
```

```typescript TypeScript nocheck
const skill = await client.beta.skills.retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv");

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

        var skill = await client.Beta.Skills.Retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv");

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
		anthropic.BetaSkillGetParams{},
	)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Skill: %s\n", skill.DisplayTitle)
	fmt.Printf("Latest version: %s\n", skill.LatestVersion)
	fmt.Printf("Created: %s\n", skill.CreatedAt)
}
```

```java Java nocheck hidelines={1..2,4..6,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.SkillRetrieveResponse;

public class RetrieveSkill {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        SkillRetrieveResponse skill = client.beta().skills().retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv");

        System.out.println("Skill: " + skill.displayTitle());
        System.out.println("Latest version: " + skill.latestVersion());
        System.out.println("Created: " + skill.createdAt());
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client();

$skill = $client->beta->skills->retrieve(
    skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
);

echo "Skill: " . $skill->displayTitle . "\n";
echo "Latest version: " . $skill->latestVersion . "\n";
echo "Created: " . $skill->createdAt . "\n";
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

skill = client.beta.skills.retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv")

puts "Skill: #{skill.display_title}"
puts "Latest version: #{skill.latest_version}"
puts "Created: #{skill.created_at}"
```
</CodeGroup>

### Menghapus Skill \{#deleting-a-skill}

Untuk menghapus Skill, Anda harus terlebih dahulu menghapus semua versinya:

<CodeGroup defaultLanguage="CLI">

```bash cURL nocheck
# Hapus semua versi terlebih dahulu, lalu hapus Skill
curl -X DELETE "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02"
```

```bash CLI nocheck
# Langkah 1: Hapus semua versi
ant beta:skills:versions list \
  --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
  --transform version --raw-output \
  | while read -r VERSION; do
      ant beta:skills:versions delete \
        --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
        --version "$VERSION" >/dev/null
    done

# Langkah 2: Hapus Skill
ant beta:skills delete \
  --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv >/dev/null
```

```python Python nocheck
# Langkah 1: Hapus semua versi
versions = client.beta.skills.versions.list(skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv")

for version in versions.data:
    client.beta.skills.versions.delete(
        skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
        version=version.version,
    )

# Langkah 2: Hapus Skill
client.beta.skills.delete(skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv")
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// Langkah 1: Hapus semua versi
const versions = await client.beta.skills.versions.list("skill_01AbCdEfGhIjKlMnOpQrStUv");

for (const version of versions.data) {
  await client.beta.skills.versions.delete("skill_01AbCdEfGhIjKlMnOpQrStUv", version.version);
}

// Langkah 2: Hapus Skill
await client.beta.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
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

        // Langkah 1: Hapus semua versi
        var versions = await client.Beta.Skills.Versions.List("skill_01AbCdEfGhIjKlMnOpQrStUv");

        foreach (var version in versions.Data)
        {
            await client.Beta.Skills.Versions.Delete(
                "skill_01AbCdEfGhIjKlMnOpQrStUv",
                version.Version
            );
        }

        // Langkah 2: Hapus Skill
        await client.Beta.Skills.Delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
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

	// Langkah 1: Hapus semua versi
	versions := client.Beta.Skills.Versions.ListAutoPaging(
		context.TODO(),
		"skill_01AbCdEfGhIjKlMnOpQrStUv",
		anthropic.BetaSkillVersionListParams{},
	)

	for versions.Next() {
		version := versions.Current()
		_, err := client.Beta.Skills.Versions.Delete(
			context.TODO(),
			version.Version,
			anthropic.BetaSkillVersionDeleteParams{
				SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
			},
		)
		if err != nil {
			log.Fatal(err)
		}
	}

	// Langkah 2: Hapus Skill
	_, err := client.Beta.Skills.Delete(
		context.TODO(),
		"skill_01AbCdEfGhIjKlMnOpQrStUv",
		anthropic.BetaSkillDeleteParams{},
	)
	if err != nil {
		log.Fatal(err)
	}
}
```

```java Java nocheck hidelines={1..2,5..7,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.versions.VersionListPage;
import com.anthropic.models.beta.skills.versions.VersionDeleteParams;

public class DeleteSkill {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Langkah 1: Hapus semua versi
        VersionListPage versions = client.beta().skills().versions().list("skill_01AbCdEfGhIjKlMnOpQrStUv");

        for (var version : versions.data()) {
            client.beta().skills().versions().delete(
                version.version(),
                VersionDeleteParams.builder()
                    .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                    .build()
            );
        }

        // Langkah 2: Hapus Skill
        client.beta().skills().delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client();

// Langkah 1: Hapus semua versi
$versions = $client->beta->skills->versions->list(
    skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
);

foreach ($versions->data as $version) {
    $client->beta->skills->versions->delete(
        skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: $version->version,
    );
}

// Langkah 2: Hapus Skill
$client->beta->skills->delete(
    skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
);
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Langkah 1: Hapus semua versi
versions = client.beta.skills.versions.list("skill_01AbCdEfGhIjKlMnOpQrStUv")

versions.data.each do |version|
  client.beta.skills.versions.delete(
    version.version,
    skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv"
  )
end

# Langkah 2: Hapus Skill
client.beta.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv")
```
</CodeGroup>

Mencoba menghapus Skill yang masih memiliki versi akan mengembalikan error 400.

### Versioning \{#versioning}

Skill mendukung versioning untuk mengelola pembaruan dengan aman:

**Skill Anthropic:**
- Versi menggunakan format tanggal: `20251013`
- Versi baru dirilis saat pembaruan dibuat
- Tentukan versi yang tepat untuk stabilitas

**Skill Kustom:**
- Epoch timestamp yang dihasilkan otomatis: `1759178010641129`
- Gunakan `"latest"` untuk selalu mendapatkan versi terbaru
- Buat versi baru saat memperbarui file Skill

<CodeGroup defaultLanguage="CLI">

```bash cURL nocheck
# Buat versi baru
NEW_VERSION=$(curl -X POST "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02" \
  -F "files[]=@updated_skill/SKILL.md;filename=updated_skill/SKILL.md")

VERSION_NUMBER=$(echo "$NEW_VERSION" | jq -r '.version')

# Gunakan versi tertentu
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d "{
    \"model\": \"claude-opus-4-8\",
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

# Gunakan versi terbaru
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
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
# Buat versi baru
VERSION_NUMBER=$(ant beta:skills:versions create \
  --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
  --file updated_skill/SKILL.md \
  --transform version --raw-output)

# Gunakan versi tertentu
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<YAML
model: claude-opus-4-8
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

# Gunakan versi terbaru
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<'YAML'
model: claude-opus-4-8
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
# Buat versi baru
from anthropic.lib import files_from_dir

new_version = client.beta.skills.versions.create(
    skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
    files=files_from_dir("/path/to/updated_skill"),
)

# Gunakan versi tertentu
response = client.beta.messages.create(
    model="claude-opus-4-8",
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

# Gunakan versi terbaru
response = client.beta.messages.create(
    model="claude-opus-4-8",
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

// Buat versi baru menggunakan file zip
const newVersion = await client.beta.skills.versions.create("skill_01AbCdEfGhIjKlMnOpQrStUv", {
  files: [fs.createReadStream("updated_skill.zip")]
});

// Gunakan versi tertentu
const specificVersionResponse = await client.beta.messages.create({
  model: "claude-opus-4-8",
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

// Gunakan versi terbaru
const latestVersionResponse = await client.beta.messages.create({
  model: "claude-opus-4-8",
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

        // Buat versi baru
        var versionParams = new SkillVersionCreateParams
        {
            Files = [File.OpenRead("/path/to/updated_skill/SKILL.md")],
        };

        var newVersion = await client.Beta.Skills.Versions.Create(
            "skill_01AbCdEfGhIjKlMnOpQrStUv",
            versionParams
        );

        // Gunakan versi tertentu
        var specificVersionParams = new MessageCreateParams
        {
            Model = "claude-opus-4-8",
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

        // Gunakan versi terbaru
        var latestVersionParams = new MessageCreateParams
        {
            Model = "claude-opus-4-8",
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

	// Buat versi baru
	skillFile := mustOpen("/path/to/updated_skill/SKILL.md")
	defer skillFile.Close()

	newVersion, err := client.Beta.Skills.Versions.New(
		context.TODO(),
		"skill_01AbCdEfGhIjKlMnOpQrStUv",
		anthropic.BetaSkillVersionNewParams{
			Files: []io.Reader{skillFile},
		},
	)
	if err != nil {
		log.Fatal(err)
	}

	// Gunakan versi tertentu
	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-8",
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

	// Gunakan versi terbaru
	latestResponse, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-8",
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

        // Buat versi baru
        VersionCreateParams versionParams = VersionCreateParams.builder()
            .addFile(Path.of("/path/to/updated_skill/SKILL.md"))
            .build();

        VersionCreateResponse newVersion = client.beta().skills().versions()
            .create("skill_01AbCdEfGhIjKlMnOpQrStUv", versionParams);

        // Gunakan versi tertentu
        MessageCreateParams specificVersionParams = MessageCreateParams.builder()
            .model("claude-opus-4-8")
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

        // Gunakan versi terbaru
        MessageCreateParams latestVersionParams = MessageCreateParams.builder()
            .model("claude-opus-4-8")
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

$client = new Client();

// Buat versi baru
$newVersion = $client->beta->skills->versions->create(
    skillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
    files: [fopen("/path/to/updated_skill/SKILL.md", "r")],
);

// Gunakan versi tertentu
$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [['role' => 'user', 'content' => 'Use updated Skill']],
    model: 'claude-opus-4-8',
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

// Gunakan versi terbaru
$latestResponse = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [['role' => 'user', 'content' => 'Use latest Skill version']],
    model: 'claude-opus-4-8',
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

# Buat versi baru
new_version = client.beta.skills.versions.create(
  "skill_01AbCdEfGhIjKlMnOpQrStUv",
  files: [File.open("/path/to/updated_skill/SKILL.md")]
)

# Gunakan versi tertentu
response = client.beta.messages.create(
  model: "claude-opus-4-8",
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

# Gunakan versi terbaru
latest_response = client.beta.messages.create(
  model: "claude-opus-4-8",
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

## Cara Skill dimuat \{#how-skills-are-loaded}

Ketika Anda menentukan Skill dalam container:

1. **Penemuan Metadata:** Claude melihat metadata untuk setiap Skill (name, description) dalam prompt sistem
2. **Pemuatan File:** File Skill disalin ke dalam container di `/skills/{directory}/`
3. **Penggunaan Otomatis:** Claude secara otomatis memuat dan menggunakan Skill ketika relevan dengan permintaan Anda
4. **Komposisi:** Beberapa Skill dapat dikomposisikan bersama untuk alur kerja yang kompleks

Arsitektur "progressive disclosure" (pengungkapan progresif) memastikan penggunaan konteks yang efisien: Claude hanya memuat instruksi Skill lengkap saat diperlukan.

---

## Kasus penggunaan \{#use-cases}

### Skill Organisasi \{#organizational-skills}

**Merek & Komunikasi**
- Menerapkan format spesifik perusahaan (warna, font, tata letak) ke dokumen
- Menghasilkan komunikasi yang mengikuti template organisasi
- Memastikan pedoman merek yang konsisten di semua output

**Manajemen Proyek**
- Menyusun catatan dengan format spesifik perusahaan (OKR, log keputusan)
- Menghasilkan tugas yang mengikuti konvensi tim
- Membuat rekap rapat dan pembaruan status yang terstandar

**Operasi Bisnis**
- Membuat laporan, proposal, dan analisis standar perusahaan
- Menjalankan prosedur analitis spesifik perusahaan
- Menghasilkan model keuangan yang mengikuti template organisasi

### Skill Personal \{#personal-skills}

**Pembuatan Konten**
- Template dokumen kustom
- Format dan gaya khusus
- Pembuatan konten spesifik domain

**Analisis Data**
- Pipeline pemrosesan data kustom
- Template visualisasi khusus
- Metode analitis spesifik industri

**Pengembangan & Otomatisasi**
- Template pembuatan kode
- Framework pengujian
- Alur kerja deployment

### Contoh: pemodelan keuangan \{#example-financial-modeling}

Gabungkan Skill Excel dan Skill analisis DCF kustom:

<CodeGroup>

```bash cURL nocheck
# Buat Skill analisis DCF kustom
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
    \"model\": \"claude-opus-4-8\",
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
# Buat Skill analisis DCF kustom
DCF_SKILL_ID=$(ant beta:skills create \
  --display-title "DCF Analysis" \
  --file dcf_skill/SKILL.md \
  --transform id --raw-output)

# Gunakan dengan Excel untuk membuat model keuangan
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<YAML
model: claude-opus-4-8
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
# Buat Skill analisis DCF kustom
from anthropic.lib import files_from_dir

dcf_skill = client.beta.skills.create(
    display_title="DCF Analysis",
    files=files_from_dir("/path/to/dcf_skill"),
)

# Gunakan dengan Excel untuk membuat model keuangan
response = client.beta.messages.create(
    model="claude-opus-4-8",
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
print(response)
```

```typescript TypeScript nocheck
// Buat Skill analisis DCF kustom
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

const client = new Anthropic();

const dcfSkill = await client.beta.skills.create({
  display_title: "DCF Analysis",
  files: [await toFile(fs.createReadStream("dcf_skill.zip"), "skill.zip")]
});

// Gunakan dengan Excel untuk membuat model keuangan
const response = await client.beta.messages.create({
  model: "claude-opus-4-8",
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
console.log(response);
```

```csharp C# nocheck hidelines={1..7}
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Messages;

var client = new AnthropicClient();

// Buat Skill analisis DCF kustom
var dcfSkill = await client.Beta.Skills.Create(new SkillCreateParams
{
    DisplayTitle = "DCF Analysis",
    Files = new[]
    {
        new SkillFileParam
        {
            Path = "dcf_skill/SKILL.md",
            Content = System.IO.File.ReadAllText("dcf_skill/SKILL.md")
        }
    },
});

// Gunakan dengan Excel untuk membuat model keuangan
var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
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

	// Skill analisis DCF kustom (ID diperoleh dari respons create Skills API)
	dcfSkillID := "skill_01AbCdEfGhIjKlMnOpQrStUv"

	// Gunakan dengan Excel untuk membuat model keuangan
	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-8",
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

        // Skill analisis DCF kustom (ID diperoleh dari respons create Skills API)
        String dcfSkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv";

        // Gunakan dengan Excel Skill untuk membuat model keuangan
        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-opus-4-8")
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

$client = new Client();

// Skill analisis DCF kustom (ID diperoleh dari respons create Skills API)
$dcfSkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv";

// Gunakan dengan Excel untuk membuat model keuangan
$message = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Build a DCF valuation model for a SaaS company with the attached financials']
    ],
    model: 'claude-opus-4-8',
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
echo $message;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Buat Skill analisis DCF kustom
dcf_skill = client.beta.skills.create(
  display_title: "DCF Analysis",
  files: [
    File.open("dcf_skill/SKILL.md", "rb")
  ]
)

# Gunakan dengan Excel untuk membuat model keuangan
response = client.beta.messages.create(
  model: "claude-opus-4-8",
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
puts response
```
</CodeGroup>

---

## Batasan dan kendala \{#limits-and-constraints}

### Batasan permintaan \{#request-limits}
- **Maksimum Skill per permintaan:** 8
- **Ukuran maksimum unggahan Skill:** 30&nbsp;MB (semua file digabungkan)
- **Persyaratan frontmatter YAML:**
  - `name`: Maksimum 64 karakter, hanya huruf kecil/angka/tanda hubung, tanpa tag XML, tanpa kata yang dicadangkan ("anthropic", "claude")
  - `description`: Maksimum 1024 karakter, tidak boleh kosong, tanpa tag XML

### Kendala lingkungan \{#environment-constraints}
Skill berjalan di container eksekusi kode dengan batasan berikut:
- **Tanpa akses jaringan:** Tidak dapat melakukan panggilan API eksternal
- **Tanpa instalasi paket saat runtime:** Hanya paket yang sudah terinstal yang tersedia
- **Lingkungan terisolasi:** Container terisolasi; container baru dibuat kecuali Anda menentukan ID container yang sudah ada

Lihat [Code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk paket yang tersedia.

---

## Praktik terbaik \{#best-practices}

### Kapan menggunakan beberapa Skill \{#when-to-use-multiple-skills}

Gabungkan Skill ketika tugas melibatkan beberapa jenis dokumen atau domain:

**Kasus penggunaan yang baik:**
- Analisis data (Excel) + pembuatan presentasi (PowerPoint)
- Pembuatan laporan (Word) + ekspor ke PDF
- Logika domain kustom + pembuatan dokumen

**Hindari:**
- Menyertakan Skill yang tidak digunakan (memengaruhi performa)

### Strategi manajemen versi \{#version-management-strategy}

**Untuk produksi:**

```python nocheck
# Sematkan ke versi tertentu untuk stabilitas
container = {
    "skills": [
        {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "1759178010641129",  # Specific version
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
            "version": "latest",  # Always get newest
        }
    ]
}
```

### Pertimbangan caching prompt \{#prompt-caching-considerations}

Saat menggunakan caching prompt, perhatikan bahwa mengubah daftar Skill di container Anda akan membatalkan cache:

<CodeGroup>
```bash cURL
# Permintaan pertama membuat cache
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,prompt-caching-2024-07-31" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
      ]
    },
    "messages": [{"role": "user", "content": "Analyze sales data"}],
    "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
  }'

# Menambah/menghapus Skill merusak cache
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,prompt-caching-2024-07-31" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
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
model: claude-opus-4-8
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

# Menambah/menghapus Skill merusak cache
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
  --beta prompt-caching-2024-07-31 <<'YAML'
model: claude-opus-4-8
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
    model="claude-opus-4-8",
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

# Menambah/menghapus Skill merusak cache
response2 = client.beta.messages.create(
    model="claude-opus-4-8",
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
  model: "claude-opus-4-8",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02", "prompt-caching-2024-07-31"],
  container: {
    skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
  },
  messages: [{ role: "user", content: "Analyze sales data" }],
  tools: [{ type: "code_execution_20250825", name: "code_execution" }]
});

// Menambah/menghapus Skill merusak cache
const response2 = await client.beta.messages.create({
  model: "claude-opus-4-8",
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

```csharp C# nocheck hidelines={1..7}
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta.Messages;

var client = new AnthropicClient();

// Permintaan pertama membuat cache
var parameters1 = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
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

// Menambah/menghapus Skill merusak cache
var parameters2 = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
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
		Model:     "claude-opus-4-8",
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

	// Menambah/menghapus Skill merusak cache
	response2, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-8",
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
            .model("claude-opus-4-8")
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

        // Menambah/menghapus Skill merusak cache
        MessageCreateParams params2 = MessageCreateParams.builder()
            .model("claude-opus-4-8")
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

$client = new Client();

// Permintaan pertama membuat cache
$response1 = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Analyze sales data']
    ],
    model: 'claude-opus-4-8',
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

// Menambah/menghapus Skill merusak cache
$response2 = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Create a presentation']
    ],
    model: 'claude-opus-4-8',
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
  model: "claude-opus-4-8",
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

# Menambah/menghapus Skill merusak cache
response2 = client.beta.messages.create(
  model: "claude-opus-4-8",
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

Untuk performa caching terbaik, jaga agar daftar Skill Anda tetap konsisten di seluruh permintaan.

### Penanganan error \{#error-handling}

Tangani error terkait Skill dengan baik:

<CodeGroup>

```bash CLI nocheck
if ! RESULT=$(ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
  --transform-error error.message --format-error yaml 2>&1 <<'YAML'
model: claude-opus-4-8
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
      # Tangani error khusus skill
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
        model="claude-opus-4-8",
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
        # Tangani error spesifik skill
    else:
        raise
```

```typescript TypeScript nocheck
try {
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
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
  console.log(response);
} catch (error) {
  if (error instanceof Anthropic.BadRequestError && error.message.includes("skill")) {
    console.error(`Skill error: ${error.message}`);
    // Tangani error khusus skill
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
                Model = "claude-opus-4-8",
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

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-8",
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
		return
	}
	fmt.Println(response)
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
                .model("claude-opus-4-8")
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

$client = new Client();

try {
    $message = $client->beta->messages->create(
        maxTokens: 4096,
        messages: [
            ['role' => 'user', 'content' => 'Process data']
        ],
        model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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

## Retensi data \{#data-retention}

Agent Skills tidak tercakup dalam pengaturan ZDR. Definisi Skill dan data eksekusi disimpan sesuai dengan kebijakan retensi data standar Anthropic.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya \{#next-steps}

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
    Praktik terbaik untuk menulis Skill yang efektif
  </Card>
  <Card
    title="Code Execution Tool"
    icon="terminal"
    href="/docs/id/agents-and-tools/tool-use/code-execution-tool"
  >
    Pelajari tentang lingkungan eksekusi kode
  </Card>
</CardGroup>