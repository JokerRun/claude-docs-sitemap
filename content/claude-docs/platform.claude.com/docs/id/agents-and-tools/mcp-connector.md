---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-connector
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 4430d2c9c89b3e620ea60523a2edc4f6598275329579a52975476df09973deb2
---

---
title: Konektor MCP
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-connector
description: Hubungkan ke server MCP jarak jauh langsung dari Messages API tanpa klien MCP, dan buat allowlist, denylist, atau konfigurasikan alat satu per satu.
---

## Compatibility
- Status: Beta
- [Beta header](https://platform.claude.com/docs/en/api/beta-headers): `mcp-client-2025-11-20`
- [ZDR](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention): not eligible
- Platforms: Claude API (beta), Claude Platform on AWS (beta), Microsoft Foundry (beta); not available on Amazon Bedrock, Google Cloud

Fitur konektor "Model Context Protocol", atau MCP, milik Claude memungkinkan Anda terhubung ke server MCP jarak jauh langsung dari Messages API tanpa klien MCP terpisah.

<Note>
  Versi sebelumnya dari fitur ini (`mcp-client-2025-04-04`) sudah tidak digunakan lagi (deprecated). Lihat [Versi deprecated: mcp-client-2025-04-04](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#deprecated-version-mcp-client-2025-04-04).
</Note>

## Fitur utama

* **Integrasi API langsung:** Terhubung ke server MCP tanpa mengimplementasikan klien MCP
* **Dukungan pemanggilan alat:** Akses alat MCP melalui Messages API
* **Konfigurasi alat yang fleksibel:** Aktifkan semua alat, buat allowlist untuk alat tertentu, atau denylist untuk alat yang tidak diinginkan
* **Konfigurasi per alat:** Konfigurasikan alat satu per satu dengan pengaturan kustom
* **Autentikasi OAuth:** Dukungan untuk token OAuth Bearer untuk server yang memerlukan autentikasi
* **Beberapa server:** Terhubung ke beberapa server MCP dalam satu permintaan

## Kapan Claude menggunakan alat MCP

Setelah server MCP terhubung, Claude memanggil alat-alatnya ketika permintaan pengguna sesuai dengan kemampuan yang dideskripsikan oleh suatu alat, baik secara eksplisit ("cari bug yang masih terbuka di Jira") maupun implisit ("apa yang menghambat rilis?" dengan server Jira terpasang).

Claude **tidak** memanggil alat MCP untuk pertanyaan pengetahuan umum tentang layanan yang terhubung. Pertanyaan "bagaimana cara kerja database Notion?" dengan server Notion terpasang akan dijawab secara langsung; pertanyaan "apa isi database Projects saya?" akan memicu alat tersebut.

Anda dapat mengarahkan seberapa mudah Claude memanggil alat MCP melalui "system prompt" (prompt sistem) Anda. Lihat [Kapan Claude menggunakan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview#when-claude-uses-tools) untuk panduan umum dan contoh frasa.

## Keterbatasan

* Dari rangkaian fitur [spesifikasi MCP](https://modelcontextprotocol.io/introduction#explore-mcp), saat ini hanya [pemanggilan alat](https://modelcontextprotocol.io/docs/concepts/tools) yang didukung.
* Server harus diekspos secara publik melalui HTTP (mendukung transport Streamable HTTP dan SSE). Server STDIO lokal tidak dapat dihubungkan secara langsung.

## Menggunakan konektor MCP di Messages API

Konektor MCP menggunakan dua komponen:

1. **Definisi server MCP** (array `mcp_servers`): Mendefinisikan detail koneksi server (URL, autentikasi)
2. **Toolset MCP** (array `tools`): Mengonfigurasi alat mana yang diaktifkan dan bagaimana mengonfigurasinya

### Contoh dasar

Contoh ini mengaktifkan semua alat dari server MCP dengan konfigurasi default:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: mcp-client-2025-11-20" \
    -d '{
      "model": "claude-opus-5",
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

  ```bash CLI
  ant beta:messages create --beta mcp-client-2025-11-20 <<'YAML'
  model: claude-opus-5
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

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5",
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

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-5",
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

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
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
      Betas = [AnthropicBeta.McpClient2025_11_20]
  };

  var message = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
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
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaMcpToolset;
  // ...
  import com.anthropic.models.beta.messages.BetaRequestMcpServerUrlDefinition;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
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
          .addBeta(AnthropicBeta.MCP_CLIENT_2025_11_20)
          .build();

      BetaMessage response = client.beta().messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 1000,
      messages: [
          ['role' => 'user', 'content' => 'What tools do you have available?']
      ],
      model: 'claude-opus-5',
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

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-5",
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

### Deskripsi field

| Properti              | Tipe   | Wajib | Deskripsi                                                                                                                                                                                                                                                                                                            |
| --------------------- | ------ | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                | string | Ya    | Saat ini hanya "url" yang didukung.                                                                                                                                                                                                                                                                                  |
| `url`                 | string | Ya    | URL server MCP. Harus diawali dengan https\://.                                                                                                                                                                                                                                                                      |
| `name`                | string | Ya    | Pengenal unik untuk server MCP ini. Harus direferensikan oleh tepat satu MCPToolset dalam array `tools`.                                                                                                                                                                                                             |
| `authorization_token` | string | Tidak | Token otorisasi OAuth jika diperlukan oleh server MCP. Lihat [Autentikasi](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#authentication) untuk cara mendapatkannya, atau [spesifikasi MCP](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) untuk detail protokol. |

## Konfigurasi toolset MCP

MCPToolset berada dalam array `tools` dan mengonfigurasi alat mana dari server MCP yang diaktifkan serta bagaimana alat tersebut harus dikonfigurasi.

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

### Deskripsi field

| Properti          | Tipe   | Wajib | Deskripsi                                                                                                                                                 |
| ----------------- | ------ | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`            | string | Ya    | Harus "mcp\_toolset".                                                                                                                                     |
| `mcp_server_name` | string | Ya    | Harus cocok dengan nama server yang didefinisikan dalam array `mcp_servers`.                                                                              |
| `default_config`  | object | Tidak | Konfigurasi default yang diterapkan ke semua alat dalam set ini. Konfigurasi alat individual dalam `configs` menimpa default ini.                         |
| `configs`         | object | Tidak | Penimpaan konfigurasi per alat. Key adalah nama alat, value adalah objek konfigurasi.                                                                     |
| `cache_control`   | object | Tidak | Konfigurasi breakpoint cache ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) untuk toolset ini. |

### Opsi konfigurasi alat

Setiap alat (baik dikonfigurasi dalam `default_config` maupun dalam `configs`) mendukung field berikut:

| Properti        | Tipe    | Default | Deskripsi                                                                                                                                                                               |
| --------------- | ------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`       | boolean | `true`  | Apakah alat ini diaktifkan.                                                                                                                                                             |
| `defer_loading` | boolean | `false` | Jika true, deskripsi alat tidak dikirim ke model pada awalnya. Digunakan bersama [alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool). |

Untuk direktori lengkap alat yang disediakan Anthropic dan properti opsional seperti `defer_loading`, lihat [Referensi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference). Untuk mencari di antara kumpulan alat yang besar, lihat [alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool).

### Penggabungan konfigurasi

Nilai konfigurasi digabungkan dengan urutan prioritas berikut (tertinggi ke terendah):

1. Pengaturan khusus alat dalam `configs`
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

* `search_events`: `enabled: false` (dari configs), `defer_loading: true` (dari default\_config)
* Semua alat lainnya: `enabled: true` (default sistem), `defer_loading: true` (dari default\_config)

## Pola konfigurasi umum

### Aktifkan semua alat dengan konfigurasi default

Pola paling sederhana: aktifkan semua alat dari sebuah server:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp"
}
```

### Allowlist: aktifkan hanya alat tertentu

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

### Denylist: nonaktifkan alat tertentu

Aktifkan semua alat secara default, lalu nonaktifkan alat yang tidak diinginkan secara eksplisit. Membuat denylist untuk alat tulis atau alat yang bersifat destruktif disarankan saat membangun asisten read-only, atau ketika Anda menginginkan langkah konfirmasi manusia sebelum perubahan state:

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

### Campuran: allowlist dengan konfigurasi per alat

Gabungkan allowlist dengan konfigurasi kustom untuk setiap alat:

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

* `search_events` diaktifkan dengan `defer_loading: false`
* `list_events` diaktifkan dengan `defer_loading: true` (diwarisi dari default\_config)
* Semua alat lainnya dinonaktifkan

## Aturan validasi

API menerapkan aturan validasi berikut:

* **Server harus ada:** `mcp_server_name` dalam MCPToolset harus cocok dengan server yang didefinisikan dalam array `mcp_servers`
* **Server harus digunakan:** Setiap server MCP yang didefinisikan dalam `mcp_servers` harus direferensikan oleh tepat satu MCPToolset
* **Toolset unik per server:** Setiap server MCP hanya dapat direferensikan oleh satu MCPToolset
* **Nama alat tidak dikenal:** Jika nama alat dalam `configs` tidak ada di server MCP, peringatan backend akan dicatat tetapi tidak ada error yang dikembalikan (server MCP mungkin memiliki ketersediaan alat yang dinamis)

## Tipe konten respons

Ketika Claude menggunakan alat MCP, respons menyertakan dua tipe blok konten baru:

### Blok MCP tool use

```json
{
  "type": "mcp_tool_use",
  "id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "name": "echo",
  "server_name": "example-mcp",
  "input": { "param1": "value1", "param2": "value2" }
}
```

### Blok MCP tool result

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

## Beberapa server MCP

Anda dapat terhubung ke beberapa server MCP dengan menyertakan beberapa definisi server dalam `mcp_servers` dan MCPToolset yang sesuai untuk masing-masing dalam array `tools`:

```json
{
  "model": "claude-opus-5",
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

Dengan banyak alat yang tersedia, Claude memilih berdasarkan nama dan deskripsi alat. Deskripsi alat yang jelas dan spesifik meningkatkan akurasi pemilihan. Untuk kumpulan alat yang besar (puluhan alat di beberapa server), pertimbangkan untuk mengaktifkan [`defer_loading`](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#tool-configuration-options) bersama [alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool) sehingga hanya alat yang relevan yang ditampilkan per kueri.

## Autentikasi

Untuk server MCP yang memerlukan autentikasi OAuth, Anda perlu mendapatkan access token. Konektor MCP beta mendukung pengiriman parameter `authorization_token` dalam definisi server MCP. Konsumen API diharapkan menangani alur OAuth dan mendapatkan access token sebelum melakukan panggilan API, serta memperbarui token sesuai kebutuhan.

### Mendapatkan access token untuk pengujian

MCP inspector dapat memandu Anda melalui proses mendapatkan access token untuk tujuan pengujian.

1. Jalankan inspector dengan perintah berikut. Anda memerlukan Node.js terinstal di mesin Anda.

   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. Di sidebar sebelah kiri, untuk **Transport type**, pilih **SSE** atau **Streamable HTTP**.

3. Masukkan URL server MCP.

4. Di area kanan, klik **Open Auth Settings** setelah **Need to configure authentication?**.

5. Klik **Quick OAuth Flow** dan lakukan otorisasi di layar OAuth.

6. Ikuti langkah-langkah di bagian **OAuth Flow Progress** pada inspector dan klik **Continue** hingga Anda mencapai **Authentication complete**.

7. Salin nilai `access_token`.

8. Tempelkan ke field `authorization_token` dalam konfigurasi server MCP Anda.

### Menggunakan access token

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

Untuk penjelasan detail tentang alur OAuth, lihat [bagian Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) dalam spesifikasi MCP.

## Helper MCP sisi klien

Jika Anda mengelola koneksi klien MCP Anda sendiri (misalnya, dengan server stdio lokal, prompt MCP, atau resource MCP), SDK menyediakan fungsi helper yang mengonversi antara tipe MCP dan tipe Claude API. Ini menghilangkan kode konversi manual saat menggunakan MCP SDK untuk bahasa Anda (misalnya, [TypeScript MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk)) bersama Anthropic SDK.

<Note>
  Gunakan [parameter API `mcp_servers`](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#using-the-mcp-connector-in-the-messages-api) ketika Anda memiliki server jarak jauh yang dapat diakses melalui URL dan hanya memerlukan dukungan alat. Gunakan helper sisi klien ketika Anda memerlukan server lokal, prompt, resource, atau kontrol lebih atas koneksi dengan SDK dasar.
</Note>

### Instalasi

Instal Anthropic SDK dan MCP SDK:

<Tabs>
  <Tab title="Python">
    Helper MCP disertakan dalam extra `mcp`, yang memerlukan Python 3.10 atau lebih baru:

    ```bash
    pip install "anthropic[mcp]"
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/sdk @modelcontextprotocol/sdk
    ```
  </Tab>

  <Tab title="C#">
    Helper berada dalam paket terpisah `Anthropic.Mcp`; klien MCP itu sendiri berasal dari [paket ModelContextProtocol](https://www.nuget.org/packages/ModelContextProtocol) resmi:

    ```bash
    dotnet add package Anthropic.Mcp
    dotnet add package ModelContextProtocol
    ```
  </Tab>

  <Tab title="Go">
    Helper berada dalam subpaket `mcp` dari Go SDK, yang dibangun di atas [MCP Go SDK](https://github.com/modelcontextprotocol/go-sdk):

    ```bash
    go get github.com/anthropics/anthropic-sdk-go/mcp
    ```
  </Tab>

  <Tab title="Java">
    Helper berada dalam artifact terpisah `anthropic-java-mcp`, yang memerlukan Java 17 atau lebih baru (SDK inti mendukung Java 8):

    <Tabs>
      <Tab title="Gradle">
        ```kotlin
        implementation("com.anthropic:anthropic-java-mcp:2.58.0")
        ```
      </Tab>

      <Tab title="Maven">
        ```xml
        <dependency>
            <groupId>com.anthropic</groupId>
            <artifactId>anthropic-java-mcp</artifactId>
            <version>2.58.0</version>
        </dependency>
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="PHP">
    Helper menggunakan [MCP PHP SDK](https://packagist.org/packages/mcp/sdk) resmi:

    ```bash
    composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7" "mcp/sdk"
    ```
  </Tab>

  <Tab title="Ruby">
    Helper menggunakan [gem `mcp`](https://rubygems.org/gems/mcp) resmi:

    ```bash
    bundle add anthropic mcp
    ```
  </Tab>
</Tabs>

### Helper yang tersedia

Impor helper untuk bahasa Anda:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.mcp import (
      async_mcp_tool,
      mcp_message,
      mcp_resource_to_content,
      mcp_resource_to_file,
  )
  ```

  ```typescript TypeScript
  import {
    mcpTools,
    mcpMessages,
    mcpResourceToContent,
    mcpResourceToFile
  } from "@anthropic-ai/sdk/helpers/beta/mcp";
  ```

  ```csharp C#
  using Anthropic.Helpers.Beta;
  using Anthropic.Helpers.Beta.Mcp;
  ```

  ```go Go
  import (
  	"github.com/anthropics/anthropic-sdk-go/mcp"
  )

  ```

  ```java Java
  import com.anthropic.helpers.McpBetaTool;
  import com.anthropic.mcp.BetaMcp;
  ```

  ```php PHP
  use Anthropic\Lib\Tools\BetaMcp;
  ```

  ```ruby Ruby
  require "anthropic"

  # Helper tersedia pada modul Anthropic::Mcp
  ```
</CodeGroup>

Nama helper dan signature persisnya mengikuti konvensi masing-masing bahasa; tabel ini menunjukkan bentuk TypeScript:

| Helper                           | Deskripsi                                                                                               |
| -------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `mcpTools(tools, mcpClient)`     | Mengonversi alat MCP menjadi alat Claude API untuk digunakan dengan `client.beta.messages.toolRunner()` |
| `mcpMessages(messages)`          | Mengonversi pesan prompt MCP ke format pesan Claude API                                                 |
| `mcpResourceToContent(resource)` | Mengonversi resource MCP menjadi blok konten Claude API                                                 |
| `mcpResourceToFile(resource)`    | Mengonversi resource MCP menjadi objek file untuk diunggah                                              |

### Menggunakan alat MCP

Konversi alat MCP untuk digunakan dengan [tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner) SDK, yang menangani eksekusi alat secara otomatis:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.mcp import async_mcp_tool
  from mcp import ClientSession
  from mcp.client.stdio import StdioServerParameters, stdio_client

  client = AsyncAnthropic()


  async def main() -> None:
      # Menghubungkan ke server MCP
      server_params = StdioServerParameters(command="mcp-server")
      async with stdio_client(server_params) as (read, write):
          async with ClientSession(read, write) as mcp_client:
              await mcp_client.initialize()

              # Mendaftar alat dan mengonversinya untuk Claude API
              tools_result = await mcp_client.list_tools()
              runner = client.beta.messages.tool_runner(
                  model="claude-opus-5",
                  max_tokens=1024,
                  messages=[
                      {"role": "user", "content": "What tools do you have available?"},
                  ],
                  tools=[async_mcp_tool(tool, mcp_client) for tool in tools_result.tools],
              )

              final_message = await runner.until_done()
              print(final_message)


  asyncio.run(main())
  ```

  ```typescript TypeScript
  import {
    mcpTools,
    type MCPCallToolResultLike,
    type MCPClientLike
  } from "@anthropic-ai/sdk/helpers/beta/mcp";
  import { Client } from "@modelcontextprotocol/sdk/client/index.js";
  import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

  const anthropic = new Anthropic();

  // Hubungkan ke server MCP
  const transport = new StdioClientTransport({ command: "mcp-server", args: [] });
  const mcpClient = new Client({ name: "my-client", version: "1.0.0" });
  await mcpClient.connect(transport);

  // Buat daftar alat dan konversikan untuk Claude API
  const { tools } = await mcpClient.listTools();

  // Tipe kembalian callTool dari MCP SDK masih menyertakan bentuk hasil lama yang
  // tidak diterima mcpTools; persempit tipenya. Hapus ini setelah MCPClientLike diperluas.
  const mcpClientForTools: MCPClientLike = {
    callTool: (params) => mcpClient.callTool(params) as Promise<MCPCallToolResultLike>
  };

  const finalMessage = await anthropic.beta.messages.toolRunner({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "What tools do you have available?" }],
    tools: mcpTools(tools, mcpClientForTools)
  });

  console.log(finalMessage);
  ```

  ```csharp C#
  using Anthropic.Helpers.Beta;
  using Anthropic.Helpers.Beta.Mcp;
  using Anthropic.Models.Beta.Messages;
  using ModelContextProtocol.Client;
  using Messages = Anthropic.Models.Messages;

  var anthropic = new AnthropicClient();

  // Hubungkan ke server MCP
  await using var mcpClient = await McpClient.CreateAsync(
      new StdioClientTransport(new StdioClientTransportOptions { Command = "mcp-server" })
  );

  // Daftar alat dan konversikan untuk Claude API
  var tools = await BetaMcp.ListToolsAsync(mcpClient);
  var runner = anthropic.Beta.Messages.ToolRunner(
      new MessageCreateParams
      {
          Model = Messages::Model.ClaudeOpus5,
          MaxTokens = 1024,
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = "What tools do you have available?",
              },
          ],
      },
      tools
  );

  var finalMessage = await runner.RunUntilDoneAsync();
  Console.WriteLine(finalMessage);
  ```

  ```go Go
  import (
  // ...

  // ...
  	"github.com/anthropics/anthropic-sdk-go/mcp"
  	mcpsdk "github.com/modelcontextprotocol/go-sdk/mcp"
  )

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	// Hubungkan ke server MCP
  	mcpClient := mcpsdk.NewClient(&mcpsdk.Implementation{Name: "my-client", Version: "1.0.0"}, nil)
  	session, err := mcpClient.Connect(ctx, &mcpsdk.CommandTransport{Command: exec.Command("mcp-server")}, nil)
  	if err != nil {
  		log.Fatal(err)
  	}
  	defer session.Close()

  	// Daftar alat dan konversikan untuk Claude API
  	toolsResult, err := session.ListTools(ctx, nil)
  	if err != nil {
  		log.Fatal(err)
  	}
  	betaTools, err := mcp.NewBetaTools(toolsResult.Tools, session)
  	if err != nil {
  		log.Fatal(err)
  	}

  	runner := client.Beta.Messages.NewToolRunner(betaTools, anthropic.BetaToolRunnerParams{
  		BetaMessageNewParams: anthropic.BetaMessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5,
  			MaxTokens: 1024,
  			Messages: []anthropic.BetaMessageParam{
  				anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What tools do you have available?")),
  			},
  		},
  	})

  	finalMessage, err := runner.RunToCompletion(ctx)
  	if err != nil {
  		log.Fatal(err)
  	}
  	fmt.Println(finalMessage.RawJSON())
  }

  ```

  ```java Java
  import com.anthropic.helpers.BetaToolRunner;
  import com.anthropic.helpers.McpBetaTool;
  import com.anthropic.mcp.BetaMcp;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import io.modelcontextprotocol.client.McpClient;
  import io.modelcontextprotocol.client.McpSyncClient;
  import io.modelcontextprotocol.client.transport.ServerParameters;
  import io.modelcontextprotocol.client.transport.StdioClientTransport;
  import io.modelcontextprotocol.json.McpJsonDefaults;
  import io.modelcontextprotocol.spec.McpSchema;
  // ...

  void main() throws Exception {
      AnthropicClient anthropic = AnthropicOkHttpClient.fromEnv();

      // Hubungkan ke server MCP
      StdioClientTransport transport = new StdioClientTransport(
              ServerParameters.builder("mcp-server").build(), McpJsonDefaults.getMapper());

      try (McpSyncClient mcpClient = McpClient.sync(transport)
              .clientInfo(new McpSchema.Implementation("my-client", "1.0.0"))
              .build()) {

          mcpClient.initialize();

          // Dapatkan daftar alat dan konversikan untuk Claude API
          List<McpBetaTool> betaTools = BetaMcp.mcpTools(mcpClient.listTools().tools(), mcpClient);

          MessageCreateParams params = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
                  .maxTokens(1024L)
                  .addUserMessage("What tools do you have available?")
                  .addTools(betaTools)
                  .build();

          // Runner menghasilkan satu pesan per giliran asisten; yang terakhir adalah respons final
          BetaToolRunner runner = anthropic.beta().messages().toolRunner(params);
          BetaMessage finalMessage = null;
          for (BetaMessage message : runner) {
              finalMessage = message;
          }
          IO.println(finalMessage);
      }
  }
  ```

  ```php PHP
  use Anthropic\Lib\Tools\BetaMcp;
  use Mcp\Client;
  use Mcp\Client\Transport\HttpTransport;

  $anthropic = new Anthropic();

  // Hubungkan ke server MCP. Klien MCP PHP terhubung melalui HTTP; arahkan ini
  // ke endpoint server Anda.
  $mcp = Client::builder()->build();
  $mcp->connect(new HttpTransport('http://localhost:8000/mcp'));

  // Daftar alat dan konversikan untuk Claude API
  $runner = $anthropic->beta->messages->toolRunner(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'What tools do you have available?']],
      model: 'claude-opus-5',
      tools: BetaMcp::tools($mcp->listTools()->tools, $mcp),
  );

  echo $runner->runUntilDone(), "\n";
  ```

  ```ruby Ruby
  require "mcp"

  anthropic = Anthropic::Client.new

  # Menghubungkan ke server MCP
  transport = MCP::Client::Stdio.new(command: "mcp-server")
  mcp_client = MCP::Client.new(transport: transport)
  mcp_client.connect

  # Mendaftar alat dan mengonversinya untuk Claude API
  runner = anthropic.beta.messages.tool_runner(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "What tools do you have available?" }],
    tools: Anthropic::Mcp.tools(mcp_client.tools, mcp_client)
  )

  final_message = runner.run_until_finished.last
  puts final_message
  ```
</CodeGroup>

### Menggunakan prompt MCP

Konversi pesan prompt MCP ke format pesan Claude API:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.mcp import mcp_message

  prompt = await mcp_client.get_prompt(name="my-prompt")
  response = await client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[mcp_message(message) for message in prompt.messages],
  )

  print(response)
  ```

  ```typescript TypeScript
  import { mcpMessages } from "@anthropic-ai/sdk/helpers/beta/mcp";

  const { messages } = await mcpClient.getPrompt({ name: "my-prompt" });
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: mcpMessages(messages)
  });

  console.log(response);
  ```

  ```csharp C#
  var prompt = await mcpClient.GetPromptAsync("my-prompt");
  var response = await anthropic.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Messages::Model.ClaudeOpus5,
          MaxTokens = 1024,
          Messages = BetaMcp.Messages(prompt.Messages),
      }
  );

  Console.WriteLine(response);
  ```

  ```go Go
  prompt, err := session.GetPrompt(ctx, &mcpsdk.GetPromptParams{Name: "my-prompt"})
  if err != nil {
  	log.Fatal(err)
  }

  messages := make([]anthropic.BetaMessageParam, 0, len(prompt.Messages))
  for _, promptMessage := range prompt.Messages {
  	message, err := mcp.ToMessage(promptMessage)
  	if err != nil {
  		log.Fatal(err)
  	}
  	messages = append(messages, message)
  }

  response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages:  messages,
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  McpSchema.GetPromptResult prompt = mcpClient.getPrompt(
          new McpSchema.GetPromptRequest("my-prompt", Map.of()));

  BetaMessage response = anthropic.beta().messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .messages(BetaMcp.mcpMessages(prompt.messages()))
          .build());

  IO.println(response);
  ```

  ```php PHP
  $prompt = $mcp->getPrompt('my-prompt');

  $response = $anthropic->beta->messages->create(
      maxTokens: 1024,
      messages: array_map(BetaMcp::message(...), $prompt->messages),
      model: 'claude-opus-5',
  );

  echo $response, "\n";
  ```

  ```ruby Ruby
  prompt = mcp_client.get_prompt(name: "my-prompt")

  response = anthropic.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: prompt["messages"].map { |message| Anthropic::Mcp.message(message) }
  )

  puts response
  ```
</CodeGroup>

### Menggunakan resource MCP

Konversi resource MCP menjadi blok konten untuk disertakan dalam pesan, atau menjadi objek file untuk diunggah:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.mcp import (
      mcp_resource_to_content,
      mcp_resource_to_file,
  )

  # Sebagai blok konten dalam pesan
  resource = await mcp_client.read_resource(uri="file:///path/to/doc.txt")
  response = await client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  mcp_resource_to_content(resource),
                  {"type": "text", "text": "Summarize this document"},
              ],
          }
      ],
  )
  print(response)

  # Sebagai unggahan file
  file_resource = await mcp_client.read_resource(
      uri="file:///path/to/data.json",
  )
  uploaded = await client.files.upload(
      file=mcp_resource_to_file(file_resource),
  )
  print(uploaded.id)
  ```

  ```typescript TypeScript
  import { mcpResourceToContent, mcpResourceToFile } from "@anthropic-ai/sdk/helpers/beta/mcp";

  // Sebagai blok konten dalam pesan
  const resource = await mcpClient.readResource({ uri: "file:///path/to/doc.txt" });
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-5",
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
  console.log(response);

  // Sebagai unggahan file
  const fileResource = await mcpClient.readResource({ uri: "file:///path/to/data.json" });
  const uploaded = await anthropic.files.upload({ file: mcpResourceToFile(fileResource) });
  console.log(uploaded.id);
  ```

  ```csharp C#
  // Sebagai blok konten dalam pesan
  var resource = await mcpClient.ReadResourceAsync("file:///path/to/doc.txt");
  var response = await anthropic.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Messages::Model.ClaudeOpus5,
          MaxTokens = 1024,
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = new BetaMessageParamContent(
                      [
                          BetaMcp.ResourceToContent(resource),
                          new BetaTextBlockParam { Text = "Summarize this document" },
                      ]
                  ),
              },
          ],
      }
  );

  Console.WriteLine(response);

  // Sebagai unggahan file
  var fileResource = await mcpClient.ReadResourceAsync("file:///path/to/data.json");
  var (filename, data, mediaType) = BetaMcp.ResourceToFile(fileResource);

  // Bangun bagian file secara eksplisit agar nama file dan tipe MIME resource
  // terbawa hingga ke unggahan.
  var file = new BinaryContent { Stream = new MemoryStream(data), FileName = filename };
  if (mediaType is not null)
  {
      file.ContentType = new(mediaType);
  }

  var uploaded = await anthropic.Files.Upload(new FileUploadParams { File = file });
  Console.WriteLine(uploaded.ID);
  ```

  ```go Go
  // Sebagai blok konten dalam pesan
  resource, err := session.ReadResource(ctx, &mcpsdk.ReadResourceParams{URI: "file:///path/to/doc.txt"})
  if err != nil {
  	log.Fatal(err)
  }
  block, err := mcp.ResourceToBlock(resource)
  if err != nil {
  	log.Fatal(err)
  }

  response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(
  			// ResourceToBlock mengembalikan union konten tool-result; konten
  			// pesan adalah tipe union terpisah, jadi bungkus ulang varian bersama
  			// (mcp.ToMessage melakukan hal yang sama secara internal).
  			anthropic.BetaContentBlockParamUnion{
  				OfText:     block.OfText,
  				OfImage:    block.OfImage,
  				OfDocument: block.OfDocument,
  			},
  			anthropic.NewBetaTextBlock("Summarize this document"),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())

  // Sebagai unggahan file
  fileResult, err := session.ReadResource(ctx, &mcpsdk.ReadResourceParams{URI: "file:///path/to/data.json"})
  if err != nil {
  	log.Fatal(err)
  }
  fileReader, err := mcp.ResourceToFile(fileResult)
  if err != nil {
  	log.Fatal(err)
  }
  uploaded, err := client.Files.Upload(ctx, anthropic.FileUploadParams{File: fileReader})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(uploaded.ID)
  ```

  ```java Java
  // Sebagai blok konten dalam sebuah pesan
  McpSchema.ReadResourceResult resource = mcpClient.readResource(
          new McpSchema.ReadResourceRequest("file:///path/to/doc.txt"));

  List<BetaContentBlockParam> content =
          new ArrayList<>(BetaMcp.mcpResourceContents(resource));
  content.add(BetaContentBlockParam.ofText(
          BetaTextBlockParam.builder().text("Summarize this document").build()));

  BetaMessage response = anthropic.beta().messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .addUserMessageOfBetaContentBlockParams(content)
          .build());

  IO.println(response);

  // Sebagai unggahan file
  McpSchema.ReadResourceResult fileResource = mcpClient.readResource(
          new McpSchema.ReadResourceRequest("file:///path/to/data.json"));

  McpResourceFile resourceFile = BetaMcp.mcpResourceFiles(fileResource).getFirst();

  // Bangun bagian file secara eksplisit agar nama file dan tipe MIME resource
  // terbawa hingga ke unggahan.
  MultipartField.Builder<InputStream> fileField = MultipartField.<InputStream>builder()
          .value(new ByteArrayInputStream(resourceFile.content()))
          .filename(resourceFile.filename());
  if (resourceFile.mimeType() != null) {
      fileField.contentType(resourceFile.mimeType());
  }

  var uploaded = anthropic.files().upload(FileUploadParams.builder()
          .file(fileField.build())
          .build());

  IO.println(uploaded.id());
  ```

  ```php PHP
  // Sebagai blok konten dalam pesan
  $resource = $mcp->readResource('file:///path/to/doc.txt');

  $response = $anthropic->beta->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  BetaMcp::resourceToContent($resource),
                  ['type' => 'text', 'text' => 'Summarize this document'],
              ],
          ],
      ],
      model: 'claude-opus-5',
  );

  echo $response, "\n";

  // Sebagai unggahan file
  $fileResource = $mcp->readResource('file:///path/to/data.json');
  $file = $anthropic->files->upload(file: BetaMcp::resourceToFile($fileResource));
  echo $file->id, "\n";
  ```

  ```ruby Ruby
  # Sebagai blok konten dalam pesan
  resource = mcp_client.read_resource(uri: "file:///path/to/doc.txt")

  response = anthropic.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          *Anthropic::Mcp.resource_to_contents(resource),
          { type: "text", text: "Summarize this document" }
        ]
      }
    ]
  )

  puts response

  # Sebagai unggahan file
  file_resource = mcp_client.read_resource(uri: "file:///path/to/data.json")
  file = Anthropic::Mcp.resource_to_files(file_resource).first
  uploaded_file = anthropic.files.upload(file: file)
  puts uploaded_file.id
  ```
</CodeGroup>

### Penanganan error

Fungsi konversi melempar `UnsupportedMCPValueError` jika suatu nilai MCP tidak didukung oleh Claude API (di Go, helper mengembalikan `UnsupportedValueError`; di Java dan C#, helper melempar `AnthropicInvalidDataException`). Ini dapat terjadi pada tipe konten, tipe MIME, atau tautan resource yang tidak didukung (selesaikan tautan resource dengan klien MCP Anda sebelum mengonversi).

## Permintaan batch

Anda dapat menyertakan `mcp_servers` dalam permintaan [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing). Pemanggilan alat MCP melalui Batches API dikenai harga yang sama dengan pemanggilan dalam permintaan Messages API biasa.

## Retensi data

Konektor MCP tidak tercakup dalam pengaturan ZDR. Data yang dipertukarkan dengan server MCP, termasuk definisi alat dan hasil eksekusi, disimpan sesuai dengan kebijakan retensi data standar Anthropic.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

## Panduan migrasi

Jika Anda menggunakan header beta `mcp-client-2025-04-04` yang sudah deprecated, ikuti panduan ini untuk bermigrasi ke versi baru.

### Perubahan utama

1. **Header beta baru:** Ubah dari `mcp-client-2025-04-04` menjadi `mcp-client-2025-11-20`
2. **Konfigurasi alat dipindahkan:** Konfigurasi alat kini berada dalam array `tools` sebagai objek MCPToolset, bukan dalam definisi server MCP
3. **Konfigurasi lebih fleksibel:** Pola baru mendukung allowlist, denylist, dan konfigurasi per alat

### Langkah migrasi

**Sebelum (deprecated):**

```json
{
  "model": "claude-opus-5",
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
  "model": "claude-opus-5",
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

| Pola lama                                          | Pola baru                                                                                      |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Tanpa `tool_configuration` (semua alat diaktifkan) | MCPToolset tanpa `default_config` atau `configs`                                               |
| `tool_configuration.enabled: false`                | MCPToolset dengan `default_config.enabled: false`                                              |
| `tool_configuration.allowed_tools: [...]`          | MCPToolset dengan `default_config.enabled: false` dan alat tertentu diaktifkan dalam `configs` |

## Versi deprecated: mcp-client-2025-04-04

<Note type="warning">
  Versi ini sudah deprecated. Migrasikan ke `mcp-client-2025-11-20` menggunakan [panduan migrasi](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#migration-guide) sebelumnya.
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

### Deskripsi field deprecated

| Properti                           | Tipe    | Deskripsi                                                                |
| ---------------------------------- | ------- | ------------------------------------------------------------------------ |
| `tool_configuration`               | object  | **Deprecated:** Gunakan MCPToolset dalam array `tools` sebagai gantinya  |
| `tool_configuration.enabled`       | boolean | **Deprecated:** Gunakan `default_config.enabled` dalam MCPToolset        |
| `tool_configuration.allowed_tools` | array   | **Deprecated:** Gunakan pola allowlist dengan `configs` dalam MCPToolset |
