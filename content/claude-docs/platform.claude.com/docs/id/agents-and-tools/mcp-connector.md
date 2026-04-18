---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-connector
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 212d1ec591d8ea0ae2941f9d4b91196fa120dbf1efa875fa60fb2fab30a24683
---

# Konektor MCP

Hubungkan ke server MCP jarak jauh langsung dari Messages API tanpa klien MCP terpisah

---

Fitur konektor Model Context Protocol (MCP) Claude memungkinkan Anda untuk terhubung ke server MCP jarak jauh langsung dari Messages API tanpa klien MCP terpisah.

<Note>
  **Versi saat ini**: Fitur ini memerlukan header beta: `"anthropic-beta": "mcp-client-2025-11-20"`

  Versi sebelumnya (`mcp-client-2025-04-04`) sudah tidak digunakan lagi. Lihat [dokumentasi versi yang tidak digunakan lagi](#deprecated-version-mcp-client-2025-04-04) di bawah.
</Note>

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Fitur utama

- **Integrasi API langsung**: Terhubung ke server MCP tanpa mengimplementasikan klien MCP
- **Dukungan pemanggilan alat**: Akses alat MCP melalui Messages API
- **Konfigurasi alat yang fleksibel**: Aktifkan semua alat, daftar putih alat tertentu, atau daftar hitam alat yang tidak diinginkan
- **Konfigurasi per-alat**: Konfigurasikan alat individual dengan pengaturan khusus
- **Autentikasi OAuth**: Dukungan untuk token Bearer OAuth untuk server yang diautentikasi
- **Server ganda**: Terhubung ke beberapa server MCP dalam satu permintaan

## Batasan

- Dari kumpulan fitur [spesifikasi MCP](https://modelcontextprotocol.io/introduction#explore-mcp), hanya [pemanggilan alat](https://modelcontextprotocol.io/docs/concepts/tools) yang saat ini didukung.
- Server harus terbuka untuk publik melalui HTTP (mendukung transportasi HTTP Streamable dan SSE). Server STDIO lokal tidak dapat terhubung secara langsung.
- Konektor MCP saat ini tidak didukung di Amazon Bedrock dan Google Vertex.

## Menggunakan konektor MCP di Messages API

Konektor MCP menggunakan dua komponen:

1. **Definisi Server MCP** (array `mcp_servers`): Mendefinisikan detail koneksi server (URL, autentikasi)
2. **Perangkat Alat MCP** (array `tools`): Mengonfigurasi alat mana yang akan diaktifkan dan cara mengonfigurasinya

### Contoh dasar

Contoh ini mengaktifkan semua alat dari server MCP dengan konfigurasi default:

<CodeGroup>

```bash Shell nocheck
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: mcp-client-2025-11-20" \
  -d '{
    "model": "claude-opus-4-7",
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
model: claude-opus-4-7
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
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
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
    Model = Model.ClaudeOpus4_7,
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
		Model:     anthropic.ModelClaudeOpus4_7,
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

```java Java nocheck hidelines={1..2,4,6..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.BetaMcpToolset;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaRequestMcpServerUrlDefinition;
import com.anthropic.models.beta.messages.MessageCreateParams;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-opus-4-7")
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
        System.out.println(response);
    }
}
```

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->beta->messages->create(
    maxTokens: 1000,
    messages: [
        ['role' => 'user', 'content' => 'What tools do you have available?']
    ],
    model: 'claude-opus-4-7',
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
  model: "claude-opus-4-7",
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

## Konfigurasi server MCP

Setiap server MCP dalam array `mcp_servers` mendefinisikan detail koneksi:

```json
{
  "type": "url",
  "url": "https://example-server.modelcontextprotocol.io/sse",
  "name": "example-mcp",
  "authorization_token": "YOUR_TOKEN"
}
```

### Deskripsi bidang

| Properti | Tipe | Diperlukan | Deskripsi |
|----------|------|----------|-------------|
| `type` | string | Ya | Saat ini hanya "url" yang didukung |
| `url` | string | Ya | URL server MCP. Harus dimulai dengan https:// |
| `name` | string | Ya | Pengidentifikasi unik untuk server MCP ini. Harus dirujuk oleh tepat satu MCPToolset dalam array `tools`. |
| `authorization_token` | string | Tidak | Token otorisasi OAuth jika diperlukan oleh server MCP. Lihat [spesifikasi MCP](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization). |

## Konfigurasi perangkat alat MCP

MCPToolset berada dalam array `tools` dan mengonfigurasi alat mana dari server MCP yang diaktifkan dan cara mengonfigurasinya.

### Struktur dasar

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

### Deskripsi bidang

| Properti | Tipe | Diperlukan | Deskripsi |
|----------|------|----------|-------------|
| `type` | string | Ya | Harus "mcp_toolset" |
| `mcp_server_name` | string | Ya | Harus cocok dengan nama server yang didefinisikan dalam array `mcp_servers` |
| `default_config` | object | Tidak | Konfigurasi default yang diterapkan ke semua alat dalam set ini. Konfigurasi alat individual dalam `configs` akan mengganti default ini. |
| `configs` | object | Tidak | Penggantian konfigurasi per-alat. Kunci adalah nama alat, nilai adalah objek konfigurasi. |
| `cache_control` | object | Tidak | Konfigurasi titik henti cache untuk perangkat alat ini |

### Opsi konfigurasi alat

Setiap alat (baik dikonfigurasi dalam `default_config` atau dalam `configs`) mendukung bidang berikut:

| Properti | Tipe | Default | Deskripsi |
|----------|------|---------|-------------|
| `enabled` | boolean | `true` | Apakah alat ini diaktifkan |
| `defer_loading` | boolean | `false` | Jika true, deskripsi alat tidak dikirim ke model awalnya. Digunakan dengan [Tool Search Tool](/docs/id/agents-and-tools/tool-use/tool-search-tool). |

Untuk direktori lengkap alat yang disediakan Anthropic dan properti opsional seperti `defer_loading`, lihat [referensi Alat](/docs/id/agents-and-tools/tool-use/tool-reference). Untuk pencarian di seluruh set alat besar, lihat [alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool).

### Penggabungan konfigurasi

Nilai konfigurasi digabungkan dengan urutan prioritas ini (tertinggi ke terendah):

1. Pengaturan khusus alat dalam `configs`
2. Set-level `default_config`
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

## Pola konfigurasi umum

### Aktifkan semua alat dengan konfigurasi default

Pola paling sederhana - aktifkan semua alat dari server:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp"
}
```

### Daftar putih - Aktifkan hanya alat tertentu

Atur `enabled: false` sebagai default, kemudian secara eksplisit aktifkan alat tertentu:

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

### Daftar hitam - Nonaktifkan alat tertentu

Aktifkan semua alat secara default, kemudian secara eksplisit nonaktifkan alat yang tidak diinginkan:

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

### Campuran - Daftar putih dengan konfigurasi per-alat

Gabungkan daftar putih dengan konfigurasi khusus untuk setiap alat:

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
- `list_events` diaktifkan dengan `defer_loading: true` (diwariskan dari default_config)
- Semua alat lainnya dinonaktifkan

## Aturan validasi

API memberlakukan aturan validasi ini:

- **Server harus ada**: `mcp_server_name` dalam MCPToolset harus cocok dengan server yang didefinisikan dalam array `mcp_servers`
- **Server harus digunakan**: Setiap server MCP yang didefinisikan dalam `mcp_servers` harus dirujuk oleh tepat satu MCPToolset
- **Perangkat alat unik per server**: Setiap server MCP hanya dapat dirujuk oleh satu MCPToolset
- **Nama alat yang tidak dikenal**: Jika nama alat dalam `configs` tidak ada di server MCP, peringatan backend dicatat tetapi tidak ada kesalahan yang dikembalikan (server MCP mungkin memiliki ketersediaan alat yang dinamis)

## Jenis konten respons

Ketika Claude menggunakan alat MCP, respons akan mencakup dua jenis blok konten baru:

### Blok Penggunaan Alat MCP

```json
{
  "type": "mcp_tool_use",
  "id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "name": "echo",
  "server_name": "example-mcp",
  "input": { "param1": "value1", "param2": "value2" }
}
```

### Blok Hasil Alat MCP

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

## Server MCP ganda

Anda dapat terhubung ke beberapa server MCP dengan menyertakan beberapa definisi server dalam `mcp_servers` dan MCPToolset yang sesuai untuk masing-masing dalam array `tools`:

```json
{
  "model": "claude-opus-4-7",
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

## Autentikasi

Untuk server MCP yang memerlukan autentikasi OAuth, Anda perlu mendapatkan token akses. Beta konektor MCP mendukung melewatkan parameter `authorization_token` dalam definisi server MCP.
Konsumen API diharapkan menangani alur OAuth dan mendapatkan token akses sebelum melakukan panggilan API, serta menyegarkan token sesuai kebutuhan.

### Mendapatkan token akses untuk pengujian

Inspektur MCP dapat memandu Anda melalui proses mendapatkan token akses untuk tujuan pengujian.

1. Jalankan inspektur dengan perintah berikut. Anda perlu Node.js terinstal di mesin Anda.

   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. Di bilah sisi di sebelah kiri, untuk "Jenis transportasi", pilih "SSE" atau "Streamable HTTP".
3. Masukkan URL server MCP.
4. Di area kanan, klik tombol "Buka Pengaturan Autentikasi" setelah "Perlu mengonfigurasi autentikasi?".
5. Klik "Alur OAuth Cepat" dan otorisasi di layar OAuth.
6. Ikuti langkah-langkah di bagian "Kemajuan Alur OAuth" dari inspektur dan klik "Lanjutkan" hingga Anda mencapai "Autentikasi selesai".
7. Salin nilai `access_token`.
8. Tempel ke bidang `authorization_token` dalam konfigurasi server MCP Anda.

### Menggunakan token akses

Setelah Anda mendapatkan token akses menggunakan salah satu alur OAuth di atas, Anda dapat menggunakannya dalam konfigurasi server MCP Anda:

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

Untuk penjelasan terperinci tentang alur OAuth, lihat [bagian Otorisasi](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) dalam spesifikasi MCP.

## Pembantu MCP sisi klien (TypeScript)

Jika Anda mengelola koneksi klien MCP Anda sendiri (misalnya, dengan server stdio lokal, prompt MCP, atau sumber daya MCP), SDK TypeScript menyediakan fungsi pembantu yang mengonversi antara jenis MCP dan jenis Claude API. Ini menghilangkan kode konversi manual saat menggunakan [SDK MCP](https://github.com/modelcontextprotocol/typescript-sdk) bersama SDK Anthropic.

<Note>
  Pembantu ini saat ini hanya tersedia di SDK TypeScript.
</Note>
<Note>
  Gunakan [parameter API `mcp_servers`](#using-the-mcp-connector-in-the-messages-api) ketika Anda memiliki server jarak jauh yang dapat diakses melalui URL dan hanya memerlukan dukungan alat. Gunakan pembantu sisi klien ketika Anda memerlukan server lokal, prompt, sumber daya, atau kontrol lebih besar atas koneksi dengan SDK dasar.
</Note>

### Instalasi

Instal SDK Anthropic dan SDK MCP:

```bash
npm install @anthropic-ai/sdk @modelcontextprotocol/sdk
```

### Pembantu yang tersedia

Impor pembantu dari namespace beta:

```typescript nocheck
import {
  mcpTools,
  mcpMessages,
  mcpResourceToContent,
  mcpResourceToFile
} from "@anthropic-ai/sdk/helpers/beta/mcp";
```

| Pembantu | Deskripsi |
|--------|-------------|
| `mcpTools(tools, mcpClient)` | Mengonversi alat MCP ke alat Claude API untuk digunakan dengan `client.beta.messages.toolRunner()` |
| `mcpMessages(messages)` | Mengonversi pesan prompt MCP ke format pesan Claude API |
| `mcpResourceToContent(resource)` | Mengonversi sumber daya MCP ke blok konten Claude API |
| `mcpResourceToFile(resource)` | Mengonversi sumber daya MCP ke objek file untuk unggahan |

### Gunakan alat MCP

Konversi alat MCP untuk digunakan dengan [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner) SDK, yang menangani eksekusi alat secara otomatis:

```typescript nocheck hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import { mcpTools } from "@anthropic-ai/sdk/helpers/beta/mcp";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const anthropic = new Anthropic();

// Connect to an MCP server
const transport = new StdioClientTransport({ command: "mcp-server", args: [] });
const mcpClient = new Client({ name: "my-client", version: "1.0.0" });
await mcpClient.connect(transport);

// List tools and convert them for the Claude API
const { tools } = await mcpClient.listTools();
const runner = await anthropic.beta.messages.toolRunner({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "What tools do you have available?" }],
  tools: mcpTools(tools, mcpClient)
});
```

### Gunakan prompt MCP

Konversi pesan prompt MCP ke format pesan Claude API:

```typescript nocheck
import { mcpMessages } from "@anthropic-ai/sdk/helpers/beta/mcp";

const { messages } = await mcpClient.getPrompt({ name: "my-prompt" });
const response = await anthropic.beta.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: mcpMessages(messages)
});
```

### Gunakan sumber daya MCP

Konversi sumber daya MCP ke blok konten untuk disertakan dalam pesan, atau ke objek file untuk unggahan:

```typescript nocheck
import { mcpResourceToContent, mcpResourceToFile } from "@anthropic-ai/sdk/helpers/beta/mcp";

// As a content block in a message
const resource = await mcpClient.readResource({ uri: "file:///path/to/doc.txt" });
await anthropic.beta.messages.create({
  model: "claude-sonnet-4-6",
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

// As a file upload
const fileResource = await mcpClient.readResource({ uri: "file:///path/to/data.json" });
await anthropic.beta.files.upload({ file: mcpResourceToFile(fileResource) });
```

### Penanganan kesalahan

Fungsi konversi melempar `UnsupportedMCPValueError` jika nilai MCP tidak didukung oleh Claude API. Ini dapat terjadi dengan jenis konten yang tidak didukung, jenis MIME, atau tautan sumber daya non-HTTP.

## Retensi data

Konektor MCP tidak tercakup oleh pengaturan ZDR. Data yang ditukar dengan server MCP, termasuk definisi alat dan hasil eksekusi, disimpan sesuai dengan kebijakan retensi data standar Anthropic.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/build-with-claude/api-and-data-retention).

## Panduan migrasi

Jika Anda menggunakan header beta yang tidak digunakan lagi `mcp-client-2025-04-04`, ikuti panduan ini untuk bermigrasi ke versi baru.

### Perubahan utama

1. **Header beta baru**: Ubah dari `mcp-client-2025-04-04` ke `mcp-client-2025-11-20`
2. **Konfigurasi alat dipindahkan**: Konfigurasi alat sekarang berada dalam array `tools` sebagai objek MCPToolset, bukan dalam definisi server MCP
3. **Konfigurasi yang lebih fleksibel**: Pola baru mendukung daftar putih, daftar hitam, dan konfigurasi per-alat

### Langkah-langkah migrasi

**Sebelumnya (tidak digunakan lagi):**

```json
{
  "model": "claude-opus-4-7",
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

**Sesudahnya (saat ini):**

```json
{
  "model": "claude-opus-4-7",
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

### Pola migrasi umum

| Pola lama | Pola baru |
|-------------|-------------|
| Tidak ada `tool_configuration` (semua alat diaktifkan) | MCPToolset tanpa `default_config` atau `configs` |
| `tool_configuration.enabled: false` | MCPToolset dengan `default_config.enabled: false` |
| `tool_configuration.allowed_tools: [...]` | MCPToolset dengan `default_config.enabled: false` dan alat tertentu diaktifkan dalam `configs` |

## Versi yang tidak digunakan lagi: mcp-client-2025-04-04

<Note type="warning">
  Versi ini tidak digunakan lagi. Bermigrasi ke `mcp-client-2025-11-20` menggunakan [panduan migrasi](#migration-guide) di atas.
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

### Deskripsi bidang yang tidak digunakan lagi

| Properti | Tipe | Deskripsi |
|----------|------|-------------|
| `tool_configuration` | object | **Tidak digunakan lagi**: Gunakan MCPToolset dalam array `tools` sebagai gantinya |
| `tool_configuration.enabled` | boolean | **Tidak digunakan lagi**: Gunakan `default_config.enabled` dalam MCPToolset |
| `tool_configuration.allowed_tools` | array | **Tidak digunakan lagi**: Gunakan pola daftar putih dengan `configs` dalam MCPToolset |