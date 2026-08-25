---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/mcp-connector
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 02b38fd4ca2c6601d0504a414a6e4d8624a5461e0a8c99e65760468fdd913c84
---

---
title: Konektor MCP
url: https://platform.claude.com/docs/id/managed-agents/mcp-connector
description: Hubungkan server MCP ke agen Anda untuk mengakses alat dan sumber data eksternal.
---

Claude Managed Agents mendukung penghubungan server [Model Context Protocol (MCP)](https://modelcontextprotocol.io) ke agen Anda. Ini memberi agen akses ke alat, sumber data, dan layanan eksternal melalui protokol yang terstandar.

Konfigurasi MCP dibagi menjadi dua langkah:

1. **Pembuatan agen** mendeklarasikan server MCP mana yang dihubungkan ke agen, berdasarkan nama dan URL.
2. **Pembuatan sesi** menyediakan autentikasi untuk server tersebut dengan mereferensikan vault yang telah didaftarkan sebelumnya (lihat [Autentikasi dengan vault](https://platform.claude.com/docs/id/managed-agents/vaults)).

Pemisahan ini menjaga rahasia agar tidak masuk ke dalam definisi agen yang dapat digunakan ulang, sekaligus memungkinkan setiap sesi melakukan autentikasi dengan kredensialnya sendiri.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Mendeklarasikan server MCP pada agen

Tentukan server MCP dalam array `mcp_servers` saat membuat agen. Setiap server memerlukan `type`, `name` yang unik, dan `url`. Tidak ada token autentikasi yang diberikan pada tahap ini.

Setiap server yang dideklarasikan juga memerlukan entri `mcp_toolset` yang sesuai dalam array `tools`. `mcp_server_name` pada toolset harus cocok dengan `name` server.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent_response=$(curl -sS --fail-with-body https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "GitHub Assistant",
    "model": "claude-opus-5",
    "mcp_servers": [
      {
        "type": "url",
        "name": "github",
        "url": "https://api.githubcopilot.com/mcp/"
      }
    ],
    "tools": [
      {"type": "agent_toolset_20260401"},
      {"type": "mcp_toolset", "mcp_server_name": "github"}
    ]
  }
  EOF
  )
  agent_id=$(jq -r '.id' <<<"$agent_response")
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    AGENT_ID=$(ant beta:agents create --transform id --raw-output < github-assistant.agent.yaml)
    ```

    <File filename="github-assistant.agent.yaml">
      ```yaml
      name: GitHub Assistant
      model:
        id: claude-opus-5
      mcp_servers:
        - type: url
          name: github
          url: https://api.githubcopilot.com/mcp/
      tools:
        - type: agent_toolset_20260401
        - type: mcp_toolset
          mcp_server_name: github
      ```
    </File>
  </MultiFileExample>

  ```python Python
  agent = client.beta.agents.create(
      name="GitHub Assistant",
      model="claude-opus-5",
      mcp_servers=[
          {
              "type": "url",
              "name": "github",
              "url": "https://api.githubcopilot.com/mcp/",
          },
      ],
      tools=[
          {"type": "agent_toolset_20260401"},
          {"type": "mcp_toolset", "mcp_server_name": "github"},
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "GitHub Assistant",
    model: "claude-opus-5",
    mcp_servers: [
      {
        type: "url",
        name: "github",
        url: "https://api.githubcopilot.com/mcp/",
      },
    ],
    tools: [
      { type: "agent_toolset_20260401" },
      { type: "mcp_toolset", mcp_server_name: "github" },
    ],
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "GitHub Assistant",
      Model = BetaManagedAgentsModel.ClaudeOpus5,
      McpServers =
      [
          new() { Type = "url", Name = "github", Url = "https://api.githubcopilot.com/mcp/" },
      ],
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
          new BetaManagedAgentsMcpToolsetParams { Type = "mcp_toolset", McpServerName = "github" },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "GitHub Assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5,
  	},
  	MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{{
  		Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
  		Name: "github",
  		URL:  "https://api.githubcopilot.com/mcp/",
  	}},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{
  		{
  			OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  				Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			},
  		},
  		{
  			OfMCPToolset: &anthropic.BetaManagedAgentsMCPToolsetParams{
  				Type:          anthropic.BetaManagedAgentsMCPToolsetParamsTypeMCPToolset,
  				MCPServerName: "github",
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("GitHub Assistant")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
          .addMcpServer(
              BetaManagedAgentsUrlMcpServerParams.builder()
                  .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
                  .name("github")
                  .url("https://api.githubcopilot.com/mcp/")
                  .build()
          )
          .addTool(
              BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .build()
          )
          .addTool(
              BetaManagedAgentsMcpToolsetParams.builder()
                  .type(BetaManagedAgentsMcpToolsetParams.Type.MCP_TOOLSET)
                  .mcpServerName("github")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'GitHub Assistant',
      model: 'claude-opus-5',
      mcpServers: [
          BetaManagedAgentsURLMCPServerParams::with(
              type: 'url',
              name: 'github',
              url: 'https://api.githubcopilot.com/mcp/',
          ),
      ],
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
          ),
          BetaManagedAgentsMCPToolsetParams::with(
              type: 'mcp_toolset',
              mcpServerName: 'github',
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "GitHub Assistant",
    model: "claude-opus-5",
    mcp_servers: [
      {
        type: "url",
        name: "github",
        url: "https://api.githubcopilot.com/mcp/"
      }
    ],
    tools: [
      {type: "agent_toolset_20260401"},
      {type: "mcp_toolset", mcp_server_name: "github"}
    ]
  )
  ```
</CodeGroup>

<Tip>
  Toolset MCP secara default menggunakan kebijakan izin `always_ask`, yang memerlukan persetujuan pengguna sebelum setiap pemanggilan alat. Lihat [kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) untuk mengonfigurasi perilaku ini.
</Tip>

### Referensi field `mcp_servers`

Setiap entri dalam array `mcp_servers` mendefinisikan satu koneksi.

| Field  | Deskripsi                                                                                                                                                                                                                                                      |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type` | Wajib. Harus bernilai `"url"`.                                                                                                                                                                                                                                 |
| `name` | Wajib. Nama unik untuk server ini di dalam agen (1–255 karakter). Digunakan sebagai `mcp_server_name` dalam array `tools` dan ditampilkan pada event alat MCP di [aliran event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming). |
| `url`  | Wajib. Endpoint server MCP jarak jauh (hingga 2.048 karakter). Lihat [Jenis server MCP yang didukung](https://platform.claude.com/docs/id/managed-agents/reference#supported-mcp-server-types) untuk persyaratan transport.                                    |

Batasan:

* Sebuah agen dapat mendeklarasikan hingga 20 server MCP. Nama server harus unik di dalam array.
* Setiap entri `mcp_servers` harus direferensikan oleh sebuah `mcp_toolset` dalam array `tools`, dan setiap `mcp_toolset` harus mereferensikan server yang telah dideklarasikan. API menolak definisi agen dengan server yang tidak direferensikan atau toolset yang menggantung.

## Mengonfigurasi alat MCP mana yang tersedia

Entri `mcp_toolset` mendukung objek `default_config` dan array `configs`, yang diterapkan pada alat yang diekspos oleh server MCP. Setiap entri `configs` hanya menerima `name`, `enabled`, dan `permission_policy`. Berbeda dengan entri dalam toolset agen bawaan, entri alat MCP tidak menerima field `type`, dan [pengaturan web](https://platform.claude.com/docs/id/managed-agents/tools#restrict-web-search-and-web-fetch-domains) yang tersedia pada `web_search` dan `web_fetch` tidak berlaku untuk alat MCP. `name` dalam setiap entri `configs` adalah nama alat polos sebagaimana dilaporkan oleh server.

Secara default, semua alat yang diekspos oleh server MCP diaktifkan. Untuk mengaktifkan hanya alat tertentu, atur `default_config.enabled` ke `false` dan aktifkan secara eksplisit alat yang Anda inginkan:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "github",
  "default_config": { "enabled": false },
  "configs": [
    { "name": "get_issue", "enabled": true },
    { "name": "list_issues", "enabled": true },
    { "name": "add_issue_comment", "enabled": true }
  ]
}
```

Pola ini berguna ketika sebuah server mengekspos banyak alat tetapi agen hanya membutuhkan beberapa, atau ketika Anda ingin alat yang ditambahkan oleh operator server tetap nonaktif sampai Anda meninjaunya.

Untuk menonaktifkan alat tertentu sambil tetap mengaktifkan sisanya, hilangkan `default_config` dan atur `enabled: false` pada entri individual:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "github",
  "configs": [{ "name": "delete_repository", "enabled": false }]
}
```

Lihat [mengonfigurasi toolset](https://platform.claude.com/docs/id/managed-agents/tools#configuring-the-toolset) untuk pola umum `default_config` / `configs`, dan [izin toolset MCP](https://platform.claude.com/docs/id/managed-agents/permission-policies#mcp-toolset-permissions) untuk mengatur `permission_policy` pada alat MCP dan menangani permintaan konfirmasi.

### Penanganan output alat MCP

Ketika output alat MCP melebihi 100.000 karakter (sekitar 25.000 token), output tersebut secara otomatis ditulis ke sebuah file di sandbox. Model menerima pratinjau terpotong beserta path file dan dapat membaca konten lengkapnya dari sana.

## Menyediakan autentikasi saat pembuatan sesi

Saat memulai sesi, teruskan `vault_ids` untuk menyediakan kredensial bagi server MCP Anda. Vault adalah kumpulan kredensial yang Anda daftarkan sekali dan referensikan berdasarkan ID. Lihat [Autentikasi dengan vault](https://platform.claude.com/docs/id/managed-agents/vaults) untuk cara membuat vault dan mengelola kredensial.

<CodeGroup>
  ```bash cURL
  session_response=$(curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id",
    "vault_ids": ["$vault_id"]
  }
  EOF
  )
  session_id=$(jq -r '.id' <<<"$session_response")
  ```

  ```bash CLI
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --vault-id "$VAULT_ID" \
    --transform id --raw-output)
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      vault_ids=[vault.id],
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id],
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      VaultIds = [vault.ID],
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
  	EnvironmentID: environment.ID,
  	VaultIDs:      []string{vault.ID},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(
      SessionCreateParams.builder()
          .agent(agent.id())
          .environmentId(environment.id())
          .addVaultId(vault.id())
          .build()
  );
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      vaultIDs: [$vault->id],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id]
  )
  ```
</CodeGroup>

Kredensial dicocokkan berdasarkan URL, sehingga vault harus berisi kredensial yang `mcp_server_url`-nya merujuk ke server yang sama dengan `url` yang dideklarasikan dalam `mcp_servers`. Kedua URL dinormalisasi sebelum pencocokan (skema dan host diubah ke huruf kecil, port default dan garis miring di akhir dihapus), sehingga perbedaan huruf besar/kecil pada host, port default, atau garis miring di akhir tidak menghalangi kecocokan; sedangkan path, subdomain, atau port non-default yang berbeda akan menghalanginya. Jika tidak ada yang cocok, koneksi dicoba tanpa autentikasi. Lihat [Menambahkan kredensial](https://platform.claude.com/docs/id/managed-agents/vaults#add-a-credential) untuk jenis kredensial `static_bearer` dan `mcp_oauth`.

### Menangani kegagalan koneksi dan autentikasi

Pembuatan sesi tidak memvalidasi konektivitas atau kredensial MCP. Jika server MCP tidak dapat dijangkau atau menolak kredensial yang diberikan, sesi tetap dimulai dan interaksi tetap dimungkinkan. Sebuah event [`session.error`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) dipancarkan dengan `mcp_server_name` dari server yang terdampak dan sebuah `retry_status`:

| Jenis error                       | Arti                                                                                                                                                                                                        |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mcp_connection_failed_error`     | Server MCP tidak dapat dijangkau (error jaringan, timeout, atau kegagalan HTTP non-autentikasi).                                                                                                            |
| `mcp_authentication_failed_error` | Autentikasi dengan server MCP gagal: server menolak kredensial dari vault yang dilampirkan, memerlukan autentikasi ketika tidak ada kredensial yang cocok dikonfigurasi, atau penyegaran token OAuth gagal. |

Anda dapat memutuskan apakah akan memblokir interaksi lebih lanjut pada error ini, memicu rotasi kredensial, atau membiarkan sesi berlanjut tanpa alat dari server yang terdampak. Koneksi dicoba ulang pada transisi `session.status_idle` ke `session.status_running` berikutnya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Kebijakan izin" icon="check" href="https://platform.claude.com/docs/id/managed-agents/permission-policies">
    Kendalikan kapan alat agen dan MCP dijalankan.
  </Card>

  <Card title="Aliran event sesi" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/events-and-streaming">
    Kirim event, lakukan streaming respons, dan interupsi atau alihkan sesi Anda di tengah eksekusi.
  </Card>

  <Card title="Jenis server MCP yang didukung" icon="book" href="https://platform.claude.com/docs/id/managed-agents/reference#supported-mcp-server-types">
    Persyaratan transport untuk server MCP jarak jauh.
  </Card>
</CardGroup>
