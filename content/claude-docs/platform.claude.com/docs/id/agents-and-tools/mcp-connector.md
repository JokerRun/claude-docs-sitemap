---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-connector
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: 327e62769bfce804c94cd031ff0df8463920cbaab6799a5e58645fd24fdcec1f
---

# Konektor MCP

---

Fitur konektor "Model Context Protocol", atau MCP, dari Claude memungkinkan Anda terhubung ke server MCP jarak jauh langsung dari Messages API tanpa memerlukan klien MCP terpisah.

<Note>
  **Versi saat ini:** Fitur ini memerlukan header beta: `"anthropic-beta": "mcp-client-2025-11-20"`

  Versi sebelumnya (`mcp-client-2025-04-04`) sudah tidak digunakan lagi (deprecated). Lihat [Versi yang tidak digunakan lagi: mcp-client-2025-04-04](#versi-yang-tidak-digunakan-lagi-mcp-client-2025-04-04).
</Note>

<Note>
Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Fitur utama \{#key-features}

- **Integrasi API langsung**: Terhubung ke server MCP tanpa mengimplementasikan klien MCP
- **Dukungan pemanggilan alat**: Akses alat MCP melalui Messages API
- **Konfigurasi alat yang fleksibel**: Aktifkan semua alat, izinkan alat tertentu (allowlist), atau tolak alat yang tidak diinginkan (denylist)
- **Konfigurasi per alat**: Konfigurasikan masing-masing alat dengan pengaturan khusus
- **Autentikasi OAuth**: Dukungan untuk token OAuth Bearer untuk server yang memerlukan autentikasi
- **Beberapa server**: Terhubung ke beberapa server MCP dalam satu permintaan

## Kapan Claude menggunakan alat MCP \{#when-claude-uses-mcp-tools}

Setelah server MCP terhubung, Claude memanggil alatnya ketika permintaan pengguna sesuai dengan kemampuan yang dijelaskan oleh suatu alat, baik secara eksplisit ("cari bug yang masih terbuka di Jira") maupun secara implisit ("apa yang menghambat rilis?" dengan server Jira yang terhubung).

Claude **tidak** memanggil alat MCP untuk pertanyaan pengetahuan umum tentang layanan yang terhubung. Bertanya "bagaimana cara kerja database Notion?" dengan server Notion yang terhubung akan dijawab secara langsung; bertanya "apa isi database Projects saya?" akan memicu alat tersebut.

Anda dapat mengarahkan seberapa mudah Claude memanggil alat MCP melalui prompt sistem Anda. Lihat [Kapan Claude menggunakan alat](/docs/id/agents-and-tools/tool-use/overview#when-claude-uses-tools) untuk panduan umum dan contoh frasa.

## Batasan \{#limitations}

- Dari rangkaian fitur dalam [spesifikasi MCP](https://modelcontextprotocol.io/introduction#explore-mcp), saat ini hanya [pemanggilan alat](https://modelcontextprotocol.io/docs/concepts/tools) yang didukung.
- Server harus diekspos secara publik melalui HTTP (mendukung transport Streamable HTTP dan SSE). Server STDIO lokal tidak dapat dihubungkan secara langsung.
- Konektor MCP tersedia di Claude API, [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Saat ini belum tersedia di Amazon Bedrock atau Vertex AI.

## Menggunakan konektor MCP di Messages API \{#using-the-mcp-connector-in-the-messages-api}

Konektor MCP menggunakan dua komponen:

1. **Definisi Server MCP** (array `mcp_servers`): Mendefinisikan detail koneksi server (URL, autentikasi)
2. **MCP Toolset** (array `tools`): Mengonfigurasi alat mana yang diaktifkan dan bagaimana mengonfigurasinya

### Contoh dasar \{#basic-example}

Contoh ini mengaktifkan semua alat dari server MCP dengan konfigurasi default:

<CodeGroup>

```bash cURL nocheck
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: mcp-client-2025-11-20" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": "What tools do you have available?"}],
    "mcp_servers": [
      {
        "type": "url",
        "url": "https://example-server.modelcontextprotocol.io/sse",
        "name": "example-mcp",
        "authorization_token": "YOUR_TOKEN"
      }
    ],
    "tools": [
      {
        "type": "mcp_toolset",
        "mcp_server_name": "example-mcp"
      }
    ]
  }'
```

```bash CLI nocheck
ant beta:messages create --beta mcp-client-2025-11-20 <<'YAML'
model: claude-opus-4-8
max_tokens: 1000
messages:
  - role: user
    content: What tools do you have available?
mcp_servers:
  - type: url
    url: https://example-server.modelcontextprotocol.io/sse
    name: example-mcp
    authorization_token: YOUR_TOKEN
tools:
  - type: mcp_toolset
    mcp_server_name: example-mcp
YAML
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-8",
    max_tokens=1000,
    messages=[{"role": "user", "content": "What tools do you have available?"}],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://example-server.modelcontextprotocol.io/sse",
            "name": "example-mcp",
            "authorization_token": "YOUR_TOKEN",
        }
    ],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "example-mcp"}],
    betas=["mcp-client-2025-11-20"],
)

print(response)
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1000,
  messages: [
    {
      role: "user",
      content: "What tools do you have available?"
    }
  ],
  mcp_servers: [
    {
      type: "url",
      url: "https://example-server.modelcontextprotocol.io/sse",
      name: "example-mcp",
      authorization_token: "YOUR_TOKEN"
    }
  ],
  tools: [
    {
      type: "mcp_toolset",
      mcp_server_name: "example-mcp"
    }
  ],
  betas: ["mcp-client-2025-11-20"]
});

console.log(response);
```

```csharp C# nocheck hidelines={1..6}
using Anthropic;
using Anthropic.Models.Beta.Messages;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1000,
    Messages = new List<BetaMessageParam>
    {
        new() { Role = Role.User, Content = "What tools do you have available?" }
    },
    McpServers = new List<BetaRequestMcpServerUrlDefinition>
    {
        new()
        {
            Url = "https://example-server.modelcontextprotocol.io/sse",
            Name = "example-mcp",
            AuthorizationToken = "YOUR_TOKEN"
        }
    },
    Tools = new List<BetaToolUnion>
    {
        new BetaMcpToolset("example-mcp")
    },
    Betas = new List<string> { "mcp-client-2025-11-20" }
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

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1000,
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What tools do you have available?")),
		},
		MCPServers: []anthropic.BetaRequestMCPServerURLDefinitionParam{
			{
				URL:                "https://example-server.modelcontextprotocol.io/sse",
				Name:               "example-mcp",
				AuthorizationToken: anthropic.String("YOUR_TOKEN"),
			},
		},
		Tools: []anthropic.BetaToolUnionParam{
			{OfMCPToolset: &anthropic.BetaMCPToolsetParam{
				MCPServerName: "example-mcp",
			}},
		},
		Betas: []anthropic.AnthropicBeta{
			anthropic.AnthropicBetaMCPClient2025_11_20,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..2,4,6..7}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.BetaMcpToolset;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaRequestMcpServerUrlDefinition;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1000L)
        .addUserMessage("What tools do you have available?")
        .addMcpServer(BetaRequestMcpServerUrlDefinition.builder()
            .url("https://example-server.modelcontextprotocol.io/sse")
            .name("example-mcp")
            .authorizationToken("YOUR_TOKEN")
            .build())
        .addTool(BetaMcpToolset.builder()
            .mcpServerName("example-mcp")
            .build())
        .addBeta("mcp-client-2025-11-20")
        .build();

    BetaMessage response = client.beta().messages().create(params);
    IO.println(response);
}
```

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->beta->messages->create(
    maxTokens: 1000,
    messages: [
        ['role' => 'user', 'content' => 'What tools do you have available?']
    ],
    model: 'claude-opus-4-8',
    mcpServers: [
        [
            'type' => 'url',
            'url' => 'https://example-server.modelcontextprotocol.io/sse',
            'name' => 'example-mcp',
            'authorization_token' => 'YOUR_TOKEN',
        ],
    ],
    tools: [
        [
            'type' => 'mcp_toolset',
            'mcp_server_name' => 'example-mcp',
        ],
    ],
    betas: ['mcp-client-2025-11-20'],
);

echo $message;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1000,
  messages: [
    { role: "user", content: "What tools do you have available?" }
  ],
  mcp_servers: [
    {
      type: "url",
      url: "https://example-server.modelcontextprotocol.io/sse",
      name: "example-mcp",
      authorization_token: "YOUR_TOKEN"
    }
  ],
  tools: [
    {
      type: "mcp_toolset",
      mcp_server_name: "example-mcp"
    }
  ],
  betas: ["mcp-client-2025-11-20"]
)

puts response
```
</CodeGroup>

## Konfigurasi server MCP \{#mcp-server-configuration}

Setiap server MCP dalam array `mcp_servers` mendefinisikan detail koneksi:

```json
{
  "type": "url",
  "url": "https://example-server.modelcontextprotocol.io/sse",
  "name": "example-mcp",
  "authorization_token": "YOUR_TOKEN"
}
```

### Deskripsi field \{#field-descriptions}

| Properti | Tipe | Wajib | Deskripsi |
|----------|------|----------|-------------|
| `type` | string | Ya | Saat ini hanya "url" yang didukung. |
| `url` | string | Ya | URL server MCP. Harus dimulai dengan https://. |
| `name` | string | Ya | Pengidentifikasi unik untuk server MCP ini. Harus direferensikan oleh tepat satu MCPToolset dalam array `tools`. |
| `authorization_token` | string | Tidak | Token otorisasi OAuth jika diperlukan oleh server MCP. Lihat [spesifikasi MCP](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization). |

## Konfigurasi MCP toolset \{#mcp-toolset-configuration}

MCPToolset berada dalam array `tools` dan mengonfigurasi alat mana dari server MCP yang diaktifkan serta bagaimana alat tersebut harus dikonfigurasi.

### Struktur dasar \{#basic-structure}

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "example-mcp",
  "default_config": {
    "enabled": true,
    "defer_loading": false
  },
  "configs": {
    "specific_tool_name": {
      "enabled": true,
      "defer_loading": true
    }
  }
}
```

### Deskripsi field \{#field-descriptions-2}

| Properti | Tipe | Wajib | Deskripsi |
|----------|------|----------|-------------|
| `type` | string | Ya | Harus berupa "mcp_toolset". |
| `mcp_server_name` | string | Ya | Harus cocok dengan nama server yang didefinisikan dalam array `mcp_servers`. |
| `default_config` | object | Tidak | Konfigurasi default yang diterapkan ke semua alat dalam set ini. Konfigurasi alat individual dalam `configs` akan menimpa default ini. |
| `configs` | object | Tidak | Penimpaan konfigurasi per alat. Kunci adalah nama alat, nilai adalah objek konfigurasi. |
| `cache_control` | object | Tidak | Konfigurasi breakpoint cache [caching prompt](/docs/id/build-with-claude/prompt-caching) untuk toolset ini. |

### Opsi konfigurasi alat \{#tool-configuration-options}

Setiap alat (baik dikonfigurasi dalam `default_config` maupun dalam `configs`) mendukung field berikut:

| Properti | Tipe | Default | Deskripsi |
|----------|------|---------|-------------|
| `enabled` | boolean | `true` | Apakah alat ini diaktifkan. |
| `defer_loading` | boolean | `false` | Jika true, deskripsi alat tidak dikirim ke model pada awalnya. Digunakan dengan [Tool search tool](/docs/id/agents-and-tools/tool-use/tool-search-tool). |

Untuk direktori lengkap alat yang disediakan Anthropic dan properti opsional seperti `defer_loading`, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference). Untuk pencarian di seluruh kumpulan alat yang besar, lihat [Tool search tool](/docs/id/agents-and-tools/tool-use/tool-search-tool).

### Penggabungan konfigurasi \{#configuration-merging}

Nilai konfigurasi digabungkan dengan urutan prioritas berikut (tertinggi ke terendah):

1. Pengaturan spesifik alat dalam `configs`
2. `default_config` tingkat set
3. Default sistem

Contoh:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp",
  "default_config": {
    "defer_loading": true
  },
  "configs": {
    "search_events": {
      "enabled": false
    }
  }
}
```

Menghasilkan:
- `search_events`: `enabled: false` (dari configs), `defer_loading: true` (dari default_config)
- Semua alat lainnya: `enabled: true` (default sistem), `defer_loading: true` (dari default_config)

## Pola konfigurasi umum \{#common-configuration-patterns}

### Aktifkan semua alat dengan konfigurasi default \{#enable-all-tools-with-default-configuration}

Pola paling sederhana - aktifkan semua alat dari sebuah server:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp"
}
```

### Allowlist: aktifkan hanya alat tertentu \{#allowlist-enable-only-specific-tools}

Atur `enabled: false` sebagai default, lalu aktifkan alat tertentu secara eksplisit:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp",
  "default_config": {
    "enabled": false
  },
  "configs": {
    "search_events": {
      "enabled": true
    },
    "create_event": {
      "enabled": true
    }
  }
}
```

### Denylist: nonaktifkan alat tertentu \{#denylist-disable-specific-tools}

Aktifkan semua alat secara default, lalu nonaktifkan alat yang tidak diinginkan secara eksplisit. Menolak alat tulis atau alat destruktif direkomendasikan saat membangun asisten read-only, atau saat Anda menginginkan langkah konfirmasi manusia sebelum perubahan state:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp",
  "configs": {
    "delete_all_events": {
      "enabled": false
    },
    "share_calendar_publicly": {
      "enabled": false
    }
  }
}
```

### Campuran: allowlist dengan konfigurasi per alat \{#mixed-allowlist-with-per-tool-configuration}

Gabungkan allowlist dengan konfigurasi khusus untuk setiap alat:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp",
  "default_config": {
    "enabled": false,
    "defer_loading": true
  },
  "configs": {
    "search_events": {
      "enabled": true,
      "defer_loading": false
    },
    "list_events": {
      "enabled": true
    }
  }
}
```

Dalam contoh ini:
- `search_events` diaktifkan dengan `defer_loading: false`
- `list_events` diaktifkan dengan `defer_loading: true` (diwarisi dari default_config)
- Semua alat lainnya dinonaktifkan

## Aturan validasi \{#validation-rules}

API menerapkan aturan validasi berikut:

- **Server harus ada**: `mcp_server_name` dalam MCPToolset harus cocok dengan server yang didefinisikan dalam array `mcp_servers`
- **Server harus digunakan**: Setiap server MCP yang didefinisikan dalam `mcp_servers` harus direferensikan oleh tepat satu MCPToolset
- **Toolset unik per server**: Setiap server MCP hanya dapat direferensikan oleh satu MCPToolset
- **Nama alat yang tidak dikenal**: Jika nama alat dalam `configs` tidak ada di server MCP, peringatan backend akan dicatat tetapi tidak ada error yang dikembalikan (server MCP mungkin memiliki ketersediaan alat yang dinamis)

## Tipe konten respons \{#response-content-types}

Ketika Claude menggunakan alat MCP, respons menyertakan dua tipe blok konten baru:

### Blok MCP tool use \{#mcp-tool-use-block}

```json
{
  "type": "mcp_tool_use",
  "id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "name": "echo",
  "server_name": "example-mcp",
  "input": { "param1": "value1", "param2": "value2" }
}
```

### Blok MCP tool result \{#mcp-tool-result-block}

```json
{
  "type": "mcp_tool_result",
  "tool_use_id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "is_error": false,
  "content": [
    {
      "type": "text",
      "text": "Hello"
    }
  ]
}
```

## Beberapa server MCP \{#multiple-mcp-servers}

Anda dapat terhubung ke beberapa server MCP dengan menyertakan beberapa definisi server dalam `mcp_servers` dan MCPToolset yang sesuai untuk masing-masing dalam array `tools`:

```json
{
  "model": "claude-opus-4-8",
  "max_tokens": 1000,
  "messages": [
    {
      "role": "user",
      "content": "Use tools from both mcp-server-1 and mcp-server-2 to complete this task"
    }
  ],
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://mcp.example1.com/sse",
      "name": "mcp-server-1",
      "authorization_token": "TOKEN1"
    },
    {
      "type": "url",
      "url": "https://mcp.example2.com/sse",
      "name": "mcp-server-2",
      "authorization_token": "TOKEN2"
    }
  ],
  "tools": [
    {
      "type": "mcp_toolset",
      "mcp_server_name": "mcp-server-1"
    },
    {
      "type": "mcp_toolset",
      "mcp_server_name": "mcp-server-2",
      "default_config": {
        "defer_loading": true
      }
    }
  ]
}
```

Dengan banyak alat yang tersedia, Claude memilih berdasarkan nama dan deskripsi alat. Deskripsi alat yang jelas dan spesifik meningkatkan akurasi pemilihan. Untuk kumpulan alat yang besar (puluhan alat di beberapa server), pertimbangkan untuk mengaktifkan [`defer_loading`](#opsi-konfigurasi-alat) dengan [Tool search tool](/docs/id/agents-and-tools/tool-use/tool-search-tool) sehingga hanya alat yang relevan yang ditampilkan per kueri.

## Autentikasi \{#authentication}

Untuk server MCP yang memerlukan autentikasi OAuth, Anda perlu mendapatkan access token. Beta konektor MCP mendukung pengiriman parameter `authorization_token` dalam definisi server MCP.
Konsumen API diharapkan menangani alur OAuth dan mendapatkan access token sebelum melakukan panggilan API, serta me-refresh token sesuai kebutuhan.

### Mendapatkan access token untuk pengujian \{#obtaining-an-access-token-for-testing}

MCP inspector dapat memandu Anda melalui proses mendapatkan access token untuk tujuan pengujian.

1. Jalankan inspector dengan perintah berikut. Anda memerlukan Node.js yang terinstal di mesin Anda.

   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. Di sidebar sebelah kiri, untuk "Transport type", pilih "SSE" atau "Streamable HTTP".
3. Masukkan URL server MCP.
4. Di area sebelah kanan, klik tombol "Open Auth Settings" setelah "Need to configure authentication?".
5. Klik "Quick OAuth Flow" dan otorisasi pada layar OAuth.
6. Ikuti langkah-langkah di bagian "OAuth Flow Progress" pada inspector dan klik "Continue" hingga Anda mencapai "Authentication complete".
7. Salin nilai `access_token`.
8. Tempelkan ke field `authorization_token` dalam konfigurasi server MCP Anda.

### Menggunakan access token \{#using-the-access-token}

Setelah Anda mendapatkan access token menggunakan salah satu alur OAuth sebelumnya, Anda dapat menggunakannya dalam konfigurasi server MCP Anda:

```json
{
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://example-server.modelcontextprotocol.io/sse",
      "name": "authenticated-server",
      "authorization_token": "YOUR_ACCESS_TOKEN_HERE"
    }
  ]
}
```

Untuk penjelasan terperinci tentang alur OAuth, lihat [bagian Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) dalam spesifikasi MCP.

## Helper MCP sisi klien \{#client-side-mcp-helpers}

Jika Anda mengelola koneksi klien MCP Anda sendiri (misalnya, dengan server stdio lokal, prompt MCP, atau resource MCP), SDK menyediakan fungsi helper yang mengonversi antara tipe MCP dan tipe Claude API. Ini menghilangkan kode konversi manual saat menggunakan SDK MCP (seperti [TypeScript MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk)) bersama dengan Anthropic SDK.

<Note>
  Helper ini tersedia di SDK Python, TypeScript, Java, Go, Ruby, dan PHP. Helper ini belum tersedia di SDK C#. Contoh di bagian ini menggunakan TypeScript; di bahasa lain, impor helper yang setara dari:

  - **Python:** `anthropic.lib.tools.mcp` (instal dengan `pip install anthropic[mcp]`)
  - **Java:** `com.anthropic.mcp.BetaMcp` dalam modul `anthropic-java-mcp`
  - **Go:** `github.com/anthropics/anthropic-sdk-go/mcp`
  - **Ruby:** `Anthropic::Mcp` (memerlukan gem `mcp`)
  - **PHP:** `Anthropic\Lib\Tools\BetaMcp`
</Note>
<Note>
  Gunakan [parameter API `mcp_servers`](#menggunakan-konektor-mcp-di-messages-api) ketika Anda memiliki server jarak jauh yang dapat diakses melalui URL dan hanya memerlukan dukungan alat. Gunakan helper sisi klien ketika Anda memerlukan server lokal, prompt, resource, atau kontrol lebih besar atas koneksi dengan SDK dasar.
</Note>

### Instalasi \{#installation}

Instal Anthropic SDK dan MCP SDK:

```bash
npm install @anthropic-ai/sdk @modelcontextprotocol/sdk
```

### Helper yang tersedia \{#available-helpers}

Impor helper dari namespace beta:

```typescript nocheck
import {
  mcpTools,
  mcpMessages,
  mcpResourceToContent,
  mcpResourceToFile
} from "@anthropic-ai/sdk/helpers/beta/mcp";
```

| Helper | Deskripsi |
|--------|-------------|
| `mcpTools(tools, mcpClient)` | Mengonversi alat MCP menjadi alat Claude API untuk digunakan dengan `client.beta.messages.toolRunner()` |
| `mcpMessages(messages)` | Mengonversi pesan prompt MCP ke format pesan Claude API |
| `mcpResourceToContent(resource)` | Mengonversi resource MCP menjadi blok konten Claude API |
| `mcpResourceToFile(resource)` | Mengonversi resource MCP menjadi objek file untuk diunggah |

### Menggunakan alat MCP \{#use-mcp-tools}

Konversi alat MCP untuk digunakan dengan [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner) SDK, yang menangani eksekusi alat secara otomatis:

```typescript nocheck hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import { mcpTools } from "@anthropic-ai/sdk/helpers/beta/mcp";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const anthropic = new Anthropic();

// Hubungkan ke server MCP
const transport = new StdioClientTransport({ command: "mcp-server", args: [] });
const mcpClient = new Client({ name: "my-client", version: "1.0.0" });
await mcpClient.connect(transport);

// Daftar alat dan konversikan untuk API Claude
const { tools } = await mcpClient.listTools();
const finalMessage = await anthropic.beta.messages.toolRunner({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "What tools do you have available?" }],
  tools: mcpTools(tools, mcpClient)
});

console.log(finalMessage);
```

### Menggunakan prompt MCP \{#use-mcp-prompts}

Konversi pesan prompt MCP ke format pesan Claude API:

```typescript nocheck
import { mcpMessages } from "@anthropic-ai/sdk/helpers/beta/mcp";

const { messages } = await mcpClient.getPrompt({ name: "my-prompt" });
const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: mcpMessages(messages)
});

console.log(response);
```

### Menggunakan resource MCP \{#use-mcp-resources}

Konversi resource MCP menjadi blok konten untuk disertakan dalam pesan, atau menjadi objek file untuk diunggah:

```typescript nocheck
import { mcpResourceToContent, mcpResourceToFile } from "@anthropic-ai/sdk/helpers/beta/mcp";

// Sebagai blok konten dalam pesan
const resource = await mcpClient.readResource({ uri: "file:///path/to/doc.txt" });
await anthropic.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        mcpResourceToContent(resource),
        { type: "text", text: "Summarize this document" }
      ]
    }
  ]
});

// Sebagai unggahan file
const fileResource = await mcpClient.readResource({ uri: "file:///path/to/data.json" });
await anthropic.beta.files.upload({ file: mcpResourceToFile(fileResource) });
```

### Penanganan error \{#error-handling}

Fungsi konversi akan melempar `UnsupportedMCPValueError` jika nilai MCP tidak didukung oleh Claude API. Ini dapat terjadi dengan tipe konten yang tidak didukung, tipe MIME, atau tautan resource non-HTTP.

## Permintaan batch \{#batch-requests}

Anda dapat menyertakan `mcp_servers` dalam permintaan [Message Batches API](/docs/id/build-with-claude/batch-processing). Pemanggilan alat MCP melalui Batches API dikenakan harga yang sama dengan permintaan Messages API reguler.

## Retensi data \{#data-retention}

Konektor MCP tidak tercakup dalam pengaturan ZDR. Data yang dipertukarkan dengan server MCP, termasuk definisi alat dan hasil eksekusi, disimpan sesuai dengan kebijakan retensi data standar Anthropic.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Panduan migrasi \{#migration-guide}

Jika Anda menggunakan header beta `mcp-client-2025-04-04` yang sudah tidak digunakan lagi, ikuti panduan ini untuk bermigrasi ke versi baru.

### Perubahan utama \{#key-changes}

1. **Header beta baru**: Ubah dari `mcp-client-2025-04-04` ke `mcp-client-2025-11-20`
2. **Konfigurasi alat dipindahkan**: Konfigurasi alat sekarang berada dalam array `tools` sebagai objek MCPToolset, bukan dalam definisi server MCP
3. **Konfigurasi lebih fleksibel**: Pola baru mendukung allowlist, denylist, dan konfigurasi per alat

### Langkah-langkah migrasi \{#migration-steps}

**Sebelum (tidak digunakan lagi):**

```json
{
  "model": "claude-opus-4-8",
  "max_tokens": 1000,
  "messages": [
    // ...
  ],
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://mcp.example.com/sse",
      "name": "example-mcp",
      "authorization_token": "YOUR_TOKEN",
      "tool_configuration": {
        "enabled": true,
        "allowed_tools": ["tool1", "tool2"]
      }
    }
  ]
}
```

**Sesudah (saat ini):**

```json
{
  "model": "claude-opus-4-8",
  "max_tokens": 1000,
  "messages": [
    // ...
  ],
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://mcp.example.com/sse",
      "name": "example-mcp",
      "authorization_token": "YOUR_TOKEN"
    }
  ],
  "tools": [
    {
      "type": "mcp_toolset",
      "mcp_server_name": "example-mcp",
      "default_config": {
        "enabled": false
      },
      "configs": {
        "tool1": {
          "enabled": true
        },
        "tool2": {
          "enabled": true
        }
      }
    }
  ]
}
```

### Pola migrasi umum \{#common-migration-patterns}

| Pola lama | Pola baru |
|-------------|-------------|
| Tanpa `tool_configuration` (semua alat diaktifkan) | MCPToolset tanpa `default_config` atau `configs` |
| `tool_configuration.enabled: false` | MCPToolset dengan `default_config.enabled: false` |
| `tool_configuration.allowed_tools: [...]` | MCPToolset dengan `default_config.enabled: false` dan alat tertentu diaktifkan dalam `configs` |

## Versi yang tidak digunakan lagi: mcp-client-2025-04-04 \{#deprecated-version-mcp-client-2025-04-04}

<Note type="warning">
  Versi ini sudah tidak digunakan lagi. Migrasikan ke `mcp-client-2025-11-20` menggunakan [panduan migrasi](#panduan-migrasi) sebelumnya.
</Note>

Versi sebelumnya dari konektor MCP menyertakan konfigurasi alat langsung dalam definisi server MCP:

```json
{
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://example-server.modelcontextprotocol.io/sse",
      "name": "example-mcp",
      "authorization_token": "YOUR_TOKEN",
      "tool_configuration": {
        "enabled": true,
        "allowed_tools": ["example_tool_1", "example_tool_2"]
      }
    }
  ]
}
```

### Deskripsi field yang tidak digunakan lagi \{#deprecated-field-descriptions}

| Properti | Tipe | Deskripsi |
|----------|------|-------------|
| `tool_configuration` | object | **Tidak digunakan lagi**: Gunakan MCPToolset dalam array `tools` sebagai gantinya |
| `tool_configuration.enabled` | boolean | **Tidak digunakan lagi**: Gunakan `default_config.enabled` dalam MCPToolset |
| `tool_configuration.allowed_tools` | array | **Tidak digunakan lagi**: Gunakan pola allowlist dengan `configs` dalam MCPToolset |