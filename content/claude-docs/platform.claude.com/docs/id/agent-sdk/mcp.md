---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/mcp
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 77b50bc356b5ab88e01aff573aa7367974d48d2213529a5ccf1a404a4eeb3574
---

# Terhubung ke alat eksternal dengan MCP

Konfigurasi server MCP untuk memperluas agen Anda dengan alat eksternal. Mencakup jenis transport, pencarian alat untuk set alat besar, autentikasi, dan penanganan kesalahan.

---

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) adalah standar terbuka untuk menghubungkan agen AI ke alat dan sumber data eksternal. Dengan MCP, agen Anda dapat menanyakan database, mengintegrasikan dengan API seperti Slack dan GitHub, dan terhubung ke layanan lain tanpa menulis implementasi alat khusus.

Server MCP dapat berjalan sebagai proses lokal, terhubung melalui HTTP, atau dieksekusi langsung dalam aplikasi SDK Anda.

## Quickstart

Contoh ini terhubung ke server MCP [dokumentasi Claude Code](https://code.claude.com/docs) menggunakan [transport HTTP](#httpsse-servers) dan menggunakan [`allowedTools`](#allow-mcp-tools) dengan wildcard untuk mengizinkan semua alat dari server.

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Use the docs MCP server to explain what hooks are in Claude Code",
  options: {
    mcpServers: {
      "claude-code-docs": {
        type: "http",
        url: "https://code.claude.com/docs/mcp"
      }
    },
    allowedTools: ["mcp__claude-code-docs__*"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "claude-code-docs": {
                "type": "http",
                "url": "https://code.claude.com/docs/mcp"
            }
        },
        allowed_tools=["mcp__claude-code-docs__*"]
    )

    async for message in query(prompt="Use the docs MCP server to explain what hooks are in Claude Code", options=options):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)

asyncio.run(main())
```

</CodeGroup>

Agen terhubung ke server dokumentasi, mencari informasi tentang hooks, dan mengembalikan hasilnya.

## Tambahkan server MCP

Anda dapat mengonfigurasi server MCP dalam kode saat memanggil `query()`, atau dalam file `.mcp.json` yang dimuat SDK secara otomatis.

### Dalam kode

Teruskan server MCP langsung dalam opsi `mcpServers`:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "List files in my project",
  options: {
    mcpServers: {
      "filesystem": {
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
      }
    },
    allowedTools: ["mcp__filesystem__*"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
            }
        },
        allowed_tools=["mcp__filesystem__*"]
    )

    async for message in query(prompt="List files in my project", options=options):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)

asyncio.run(main())
```

</CodeGroup>

### Dari file konfigurasi

Buat file `.mcp.json` di root proyek Anda. SDK memuat ini secara otomatis:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
    }
  }
}
```

## Izinkan alat MCP

Alat MCP memerlukan izin eksplisit sebelum Claude dapat menggunakannya. Tanpa izin, Claude akan melihat bahwa alat tersedia tetapi tidak akan dapat memanggilnya.

### Konvensi penamaan alat

Alat MCP mengikuti pola penamaan `mcp__<server-name>__<tool-name>`. Misalnya, server GitHub bernama `"github"` dengan alat `list_issues` menjadi `mcp__github__list_issues`.

### Berikan akses dengan allowedTools

Gunakan `allowedTools` untuk menentukan alat MCP mana yang dapat digunakan Claude:

```typescript
options: {
  mcpServers: { /* your servers */ },
  allowedTools: [
    "mcp__github__*",              // All tools from the github server
    "mcp__db__query",              // Only the query tool from db server
    "mcp__slack__send_message"     // Only send_message from slack server
  ]
}
```

Wildcard (`*`) memungkinkan Anda mengizinkan semua alat dari server tanpa mencantumkan masing-masing secara individual.

### Alternatif: Ubah mode izin

Alih-alih mencantumkan alat yang diizinkan, Anda dapat mengubah mode izin untuk memberikan akses yang lebih luas:

- `permissionMode: "acceptEdits"`: Secara otomatis menyetujui penggunaan alat (masih meminta operasi destruktif)
- `permissionMode: "bypassPermissions"`: Melewati semua prompt keamanan, termasuk operasi destruktif seperti penghapusan file atau menjalankan perintah shell. Gunakan dengan hati-hati, terutama dalam produksi. Mode ini menyebar ke subagen yang dihasilkan oleh alat Task.

```typescript
options: {
  mcpServers: { /* your servers */ },
  permissionMode: "acceptEdits"  // No need for allowedTools
}
```

Lihat [Permissions](/docs/id/agent-sdk/permissions) untuk detail lebih lanjut tentang mode izin.

### Temukan alat yang tersedia

Untuk melihat alat apa yang disediakan server MCP, periksa dokumentasi server atau terhubung ke server dan periksa pesan init `system`:

```typescript
for await (const message of query({ prompt: "...", options })) {
  if (message.type === "system" && message.subtype === "init") {
    console.log("Available MCP tools:", message.mcp_servers);
  }
}
```

## Jenis transport

Server MCP berkomunikasi dengan agen Anda menggunakan protokol transport yang berbeda. Periksa dokumentasi server untuk melihat transport mana yang didukungnya:

- Jika dokumen memberi Anda **perintah untuk dijalankan** (seperti `npx @modelcontextprotocol/server-github`), gunakan stdio
- Jika dokumen memberi Anda **URL**, gunakan HTTP atau SSE
- Jika Anda membangun alat Anda sendiri dalam kode, gunakan server MCP SDK

### Server stdio

Proses lokal yang berkomunikasi melalui stdin/stdout. Gunakan ini untuk server MCP yang Anda jalankan di mesin yang sama:

<Tabs>
  <Tab title="Dalam kode">
    <CodeGroup>

    ```typescript TypeScript
    options: {
      mcpServers: {
        "github": {
          command: "npx",
          args: ["-y", "@modelcontextprotocol/server-github"],
          env: {
            GITHUB_TOKEN: process.env.GITHUB_TOKEN
          }
        }
      },
      allowedTools: ["mcp__github__list_issues", "mcp__github__search_issues"]
    }
    ```

    ```python Python
    options = ClaudeAgentOptions(
        mcp_servers={
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]
                }
            }
        },
        allowed_tools=["mcp__github__list_issues", "mcp__github__search_issues"]
    )
    ```

    </CodeGroup>
  </Tab>
  <Tab title=".mcp.json">
    ```json
    {
      "mcpServers": {
        "github": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-github"],
          "env": {
            "GITHUB_TOKEN": "${GITHUB_TOKEN}"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

### Server HTTP/SSE

Gunakan HTTP atau SSE untuk server MCP yang dihosting cloud dan API jarak jauh:

<Tabs>
  <Tab title="Dalam kode">
    <CodeGroup>

    ```typescript TypeScript
    options: {
      mcpServers: {
        "remote-api": {
          type: "sse",
          url: "https://api.example.com/mcp/sse",
          headers: {
            Authorization: `Bearer ${process.env.API_TOKEN}`
          }
        }
      },
      allowedTools: ["mcp__remote-api__*"]
    }
    ```

    ```python Python
    options = ClaudeAgentOptions(
        mcp_servers={
            "remote-api": {
                "type": "sse",
                "url": "https://api.example.com/mcp/sse",
                "headers": {
                    "Authorization": f"Bearer {os.environ['API_TOKEN']}"
                }
            }
        },
        allowed_tools=["mcp__remote-api__*"]
    )
    ```

    </CodeGroup>
  </Tab>
  <Tab title=".mcp.json">
    ```json
    {
      "mcpServers": {
        "remote-api": {
          "type": "sse",
          "url": "https://api.example.com/mcp/sse",
          "headers": {
            "Authorization": "Bearer ${API_TOKEN}"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

Untuk HTTP (non-streaming), gunakan `"type": "http"` sebagai gantinya.

### Server MCP SDK

Tentukan alat khusus langsung dalam kode aplikasi Anda alih-alih menjalankan proses server terpisah. Lihat [panduan alat khusus](/docs/id/agent-sdk/custom-tools) untuk detail implementasi.

## Pencarian alat MCP

Ketika Anda memiliki banyak alat MCP yang dikonfigurasi, definisi alat dapat mengonsumsi bagian signifikan dari jendela konteks Anda. Pencarian alat MCP menyelesaikan ini dengan memuat alat secara dinamis sesuai permintaan alih-alih memuat semuanya sebelumnya.

### Cara kerjanya

Pencarian alat berjalan dalam mode otomatis secara default. Ini diaktifkan ketika deskripsi alat MCP Anda akan mengonsumsi lebih dari 10% dari jendela konteks. Ketika dipicu:

1. Alat MCP ditandai dengan `defer_loading: true` daripada dimuat ke konteks sebelumnya
2. Claude menggunakan alat pencarian untuk menemukan alat MCP yang relevan saat diperlukan
3. Hanya alat yang benar-benar dibutuhkan Claude yang dimuat ke dalam konteks

Pencarian alat memerlukan model yang mendukung blok `tool_reference`: Sonnet 4 dan yang lebih baru, atau Opus 4 dan yang lebih baru. Model Haiku tidak mendukung pencarian alat.

### Konfigurasi pencarian alat

Kontrol perilaku pencarian alat dengan variabel lingkungan `ENABLE_TOOL_SEARCH`:

| Nilai | Perilaku |
|:------|:---------|
| `auto` | Diaktifkan ketika alat MCP melebihi 10% konteks (default) |
| `auto:5` | Diaktifkan pada ambang 5% (sesuaikan persentasenya) |
| `true` | Selalu diaktifkan |
| `false` | Dinonaktifkan, semua alat MCP dimuat sebelumnya |

Atur nilai dalam opsi `env`:

<CodeGroup>

```typescript TypeScript
const options = {
  mcpServers: { /* your MCP servers */ },
  env: {
    ENABLE_TOOL_SEARCH: "auto:5"  // Enable at 5% threshold
  }
};
```

```python Python
options = ClaudeAgentOptions(
    mcp_servers={ ... },  # your MCP servers
    env={
        "ENABLE_TOOL_SEARCH": "auto:5"  # Enable at 5% threshold
    }
)
```

</CodeGroup>

## Autentikasi

Sebagian besar server MCP memerlukan autentikasi untuk mengakses layanan eksternal. Teruskan kredensial melalui variabel lingkungan dalam konfigurasi server.

### Teruskan kredensial melalui variabel lingkungan

Gunakan bidang `env` untuk meneruskan kunci API, token, dan kredensial lainnya ke server MCP:

<Tabs>
  <Tab title="Dalam kode">
    <CodeGroup>

    ```typescript TypeScript
    options: {
      mcpServers: {
        "github": {
          command: "npx",
          args: ["-y", "@modelcontextprotocol/server-github"],
          env: {
            GITHUB_TOKEN: process.env.GITHUB_TOKEN
          }
        }
      },
      allowedTools: ["mcp__github__list_issues"]
    }
    ```

    ```python Python
    options = ClaudeAgentOptions(
        mcp_servers={
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]
                }
            }
        },
        allowed_tools=["mcp__github__list_issues"]
    )
    ```

    </CodeGroup>
  </Tab>
  <Tab title=".mcp.json">
    ```json
    {
      "mcpServers": {
        "github": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-github"],
          "env": {
            "GITHUB_TOKEN": "${GITHUB_TOKEN}"
          }
        }
      }
    }
    ```

    Sintaks `${GITHUB_TOKEN}` memperluas variabel lingkungan saat runtime.
  </Tab>
</Tabs>

Lihat [Daftar masalah dari repositori](#list-issues-from-a-repository) untuk contoh kerja lengkap dengan logging debug.

### Header HTTP untuk server jarak jauh

Untuk server HTTP dan SSE, teruskan header autentikasi langsung dalam konfigurasi server:

<Tabs>
  <Tab title="Dalam kode">
    <CodeGroup>

    ```typescript TypeScript
    options: {
      mcpServers: {
        "secure-api": {
          type: "http",
          url: "https://api.example.com/mcp",
          headers: {
            Authorization: `Bearer ${process.env.API_TOKEN}`
          }
        }
      },
      allowedTools: ["mcp__secure-api__*"]
    }
    ```

    ```python Python
    options = ClaudeAgentOptions(
        mcp_servers={
            "secure-api": {
                "type": "http",
                "url": "https://api.example.com/mcp",
                "headers": {
                    "Authorization": f"Bearer {os.environ['API_TOKEN']}"
                }
            }
        },
        allowed_tools=["mcp__secure-api__*"]
    )
    ```

    </CodeGroup>
  </Tab>
  <Tab title=".mcp.json">
    ```json
    {
      "mcpServers": {
        "secure-api": {
          "type": "http",
          "url": "https://api.example.com/mcp",
          "headers": {
            "Authorization": "Bearer ${API_TOKEN}"
          }
        }
      }
    }
    ```

    Sintaks `${API_TOKEN}` memperluas variabel lingkungan saat runtime.
  </Tab>
</Tabs>

### Autentikasi OAuth2

[Spesifikasi MCP mendukung OAuth 2.1](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization) untuk otorisasi. SDK tidak menangani alur OAuth secara otomatis, tetapi Anda dapat meneruskan token akses melalui header setelah menyelesaikan alur OAuth dalam aplikasi Anda:

<CodeGroup>

```typescript TypeScript
// After completing OAuth flow in your app
const accessToken = await getAccessTokenFromOAuthFlow();

const options = {
  mcpServers: {
    "oauth-api": {
      type: "http",
      url: "https://api.example.com/mcp",
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    }
  },
  allowedTools: ["mcp__oauth-api__*"]
};
```

```python Python
# After completing OAuth flow in your app
access_token = await get_access_token_from_oauth_flow()

options = ClaudeAgentOptions(
    mcp_servers={
        "oauth-api": {
            "type": "http",
            "url": "https://api.example.com/mcp",
            "headers": {
                "Authorization": f"Bearer {access_token}"
            }
        }
    },
    allowed_tools=["mcp__oauth-api__*"]
)
```

</CodeGroup>

## Contoh

### Daftar masalah dari repositori

Contoh ini terhubung ke [server MCP GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/github) untuk mencantumkan masalah terbaru. Contoh ini mencakup logging debug untuk memverifikasi koneksi MCP dan panggilan alat.

Sebelum menjalankan, buat [token akses pribadi GitHub](https://github.com/settings/tokens) dengan cakupan `repo` dan atur sebagai variabel lingkungan:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "List the 3 most recent issues in anthropics/claude-code",
  options: {
    mcpServers: {
      "github": {
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-github"],
        env: {
          GITHUB_TOKEN: process.env.GITHUB_TOKEN
        }
      }
    },
    allowedTools: ["mcp__github__list_issues"]
  }
})) {
  // Verify MCP server connected successfully
  if (message.type === "system" && message.subtype === "init") {
    console.log("MCP servers:", message.mcp_servers);
  }

  // Log when Claude calls an MCP tool
  if (message.type === "assistant") {
    for (const block of message.content) {
      if (block.type === "tool_use" && block.name.startsWith("mcp__")) {
        console.log("MCP tool called:", block.name);
      }
    }
  }

  // Print the final result
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python
import asyncio
import os
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage, AssistantMessage

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]
                }
            }
        },
        allowed_tools=["mcp__github__list_issues"]
    )

    async for message in query(prompt="List the 3 most recent issues in anthropics/claude-code", options=options):
        # Verify MCP server connected successfully
        if isinstance(message, SystemMessage) and message.subtype == "init":
            print("MCP servers:", message.data.get("mcp_servers"))

        # Log when Claude calls an MCP tool
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "name") and block.name.startswith("mcp__"):
                    print("MCP tool called:", block.name)

        # Print the final result
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)

asyncio.run(main())
```

</CodeGroup>

### Tanyakan database

Contoh ini menggunakan [server MCP Postgres](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) untuk menanyakan database. String koneksi diteruskan sebagai argumen ke server. Agen secara otomatis menemukan skema database, menulis kueri SQL, dan mengembalikan hasilnya:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Connection string from environment variable
const connectionString = process.env.DATABASE_URL;

for await (const message of query({
  // Natural language query - Claude writes the SQL
  prompt: "How many users signed up last week? Break it down by day.",
  options: {
    mcpServers: {
      "postgres": {
        command: "npx",
        // Pass connection string as argument to the server
        args: ["-y", "@modelcontextprotocol/server-postgres", connectionString]
      }
    },
    // Allow only read queries, not writes
    allowedTools: ["mcp__postgres__query"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python
import asyncio
import os
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    # Connection string from environment variable
    connection_string = os.environ["DATABASE_URL"]

    options = ClaudeAgentOptions(
        mcp_servers={
            "postgres": {
                "command": "npx",
                # Pass connection string as argument to the server
                "args": ["-y", "@modelcontextprotocol/server-postgres", connection_string]
            }
        },
        # Allow only read queries, not writes
        allowed_tools=["mcp__postgres__query"]
    )

    # Natural language query - Claude writes the SQL
    async for message in query(
        prompt="How many users signed up last week? Break it down by day.",
        options=options
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)

asyncio.run(main())
```

</CodeGroup>

## Penanganan kesalahan

Server MCP dapat gagal terhubung karena berbagai alasan: proses server mungkin tidak terinstal, kredensial mungkin tidak valid, atau server jarak jauh mungkin tidak dapat dijangkau.

SDK mengirimkan pesan `system` dengan subtype `init` di awal setiap kueri. Pesan ini mencakup status koneksi untuk setiap server MCP. Periksa bidang `status` untuk mendeteksi kegagalan koneksi sebelum agen mulai bekerja:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Process data",
  options: {
    mcpServers: {
      "data-processor": dataServer
    }
  }
})) {
  if (message.type === "system" && message.subtype === "init") {
    const failedServers = message.mcp_servers.filter(
      s => s.status !== "connected"
    );

    if (failedServers.length > 0) {
      console.warn("Failed to connect:", failedServers);
    }
  }

  if (message.type === "result" && message.subtype === "error_during_execution") {
    console.error("Execution failed");
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage, ResultMessage

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "data-processor": data_server
        }
    )

    async for message in query(prompt="Process data", options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            failed_servers = [
                s for s in message.data.get("mcp_servers", [])
                if s.get("status") != "connected"
            ]

            if failed_servers:
                print(f"Failed to connect: {failed_servers}")

        if isinstance(message, ResultMessage) and message.subtype == "error_during_execution":
            print("Execution failed")

asyncio.run(main())
```

</CodeGroup>

## Pemecahan masalah

### Server menunjukkan status "failed"

Periksa pesan `init` untuk melihat server mana yang gagal terhubung:

```typescript
if (message.type === "system" && message.subtype === "init") {
  for (const server of message.mcp_servers) {
    if (server.status === "failed") {
      console.error(`Server ${server.name} failed to connect`);
    }
  }
}
```

Penyebab umum:

- **Variabel lingkungan yang hilang**: Pastikan token dan kredensial yang diperlukan diatur. Untuk server stdio, periksa bidang `env` cocok dengan apa yang diharapkan server.
- **Server tidak terinstal**: Untuk perintah `npx`, verifikasi paket ada dan Node.js ada di PATH Anda.
- **String koneksi tidak valid**: Untuk server database, verifikasi format string koneksi dan bahwa database dapat diakses.
- **Masalah jaringan**: Untuk server HTTP/SSE jarak jauh, periksa URL dapat dijangkau dan firewall apa pun memungkinkan koneksi.

### Alat tidak dipanggil

Jika Claude melihat alat tetapi tidak menggunakannya, periksa bahwa Anda telah memberikan izin dengan `allowedTools` atau dengan [mengubah mode izin](#alternative-change-the-permission-mode):

```typescript
options: {
  mcpServers: { /* your servers */ },
  allowedTools: ["mcp__servername__*"]  // Required for Claude to use the tools
}
```

### Batas waktu koneksi

SDK MCP memiliki batas waktu default 60 detik untuk koneksi server. Jika server Anda membutuhkan waktu lebih lama untuk memulai, koneksi akan gagal. Untuk server yang memerlukan waktu startup lebih lama, pertimbangkan:

- Menggunakan server yang lebih ringan jika tersedia
- Pra-pemanasan server sebelum memulai agen Anda
- Memeriksa log server untuk penyebab inisialisasi lambat

## Sumber daya terkait

- **[Panduan alat khusus](/docs/id/agent-sdk/custom-tools)**: Bangun server MCP Anda sendiri yang berjalan dalam proses dengan aplikasi SDK Anda
- **[Permissions](/docs/id/agent-sdk/permissions)**: Kontrol alat MCP mana yang dapat digunakan agen Anda dengan `allowedTools` dan `disallowedTools`
- **[Referensi SDK TypeScript](/docs/id/agent-sdk/typescript)**: Referensi API lengkap termasuk opsi konfigurasi MCP
- **[Referensi SDK Python](/docs/id/agent-sdk/python)**: Referensi API lengkap termasuk opsi konfigurasi MCP
- **[Direktori server MCP](https://github.com/modelcontextprotocol/servers)**: Jelajahi server MCP yang tersedia untuk database, API, dan lainnya