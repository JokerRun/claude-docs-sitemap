---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/mcp-connector
fetched_at: 2026-05-29T03:17:00.216417Z
sha256: ec2cfd2f0f22fdb833be31b88f500f8d84b9e26f982014bc2ab753a90b0bea0f
---

# Konektor MCP

Hubungkan server MCP ke agen Anda untuk mengakses alat eksternal dan sumber data.

---

Claude Managed Agents mendukung koneksi server [Model Context Protocol (MCP)](https://modelcontextprotocol.io) ke agen Anda. Ini memberikan agen akses ke alat eksternal, sumber data, dan layanan melalui protokol standar.

Konfigurasi MCP dibagi menjadi dua langkah:

1. **Pembuatan agen** mendeklarasikan server MCP mana yang terhubung dengan agen, berdasarkan nama dan URL.
2. **Pembuatan sesi** menyediakan autentikasi untuk server tersebut dengan mereferensikan [vault](/docs/id/managed-agents/vaults) yang telah terdaftar sebelumnya.

Pemisahan ini menjaga rahasia tetap keluar dari definisi agen yang dapat digunakan kembali sambil memungkinkan setiap sesi untuk melakukan autentikasi dengan kredensial miliknya sendiri.

<Note>
Semua permintaan API Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

## Deklarasikan server MCP pada agen

Tentukan server MCP dalam array `mcp_servers` saat membuat agen. Setiap server memerlukan `type`, `name` yang unik, dan `url`. Tidak ada token autentikasi yang disediakan pada tahap ini.

`name` yang Anda tetapkan dalam array server MCP digunakan untuk mereferensikan entri `mcp_toolset` dalam array alat.

<CodeGroup defaultLanguage="CLI">
  
````bash
agent_response=$(curl -sS --fail-with-body https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<'EOF'
{
  "name": "GitHub Assistant",
  "model": "claude-opus-4-8",
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
````

  
````bash
AGENT_ID=$(ant beta:agents create \
  --name "GitHub Assistant" \
  --model claude-opus-4-8 \
  --mcp-server '{type: url, name: github, url: "https://api.githubcopilot.com/mcp/"}' \
  --tool '{type: agent_toolset_20260401}' \
  --tool '{type: mcp_toolset, mcp_server_name: github}' \
  --transform id --raw-output)
````

  
````python
agent = client.beta.agents.create(
    name="GitHub Assistant",
    model="claude-opus-4-8",
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
````

  
````typescript
const agent = await client.beta.agents.create({
  name: "GitHub Assistant",
  model: "claude-opus-4-8",
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
````

  
````csharp
var agent = await client.Beta.Agents.Create(new()
{
    Name = "GitHub Assistant",
    Model = BetaManagedAgentsModel.ClaudeOpus4_8,
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
````

  
````go
agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name: "GitHub Assistant",
	Model: anthropic.BetaManagedAgentsModelConfigParams{
		ID: anthropic.BetaManagedAgentsModelClaudeOpus4_8,
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
````

  
````java
var agent = client.beta().agents().create(
    AgentCreateParams.builder()
        .name("GitHub Assistant")
        .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
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
````

  
````php
$agent = $client->beta->agents->create(
    name: 'GitHub Assistant',
    model: 'claude-opus-4-8',
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
````

  
````ruby
agent = client.beta.agents.create(
  name: "GitHub Assistant",
  model: "claude-opus-4-8",
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
````

</CodeGroup>

<Tip>
Toolset MCP secara default menggunakan kebijakan izin `always_ask`, yang memerlukan persetujuan pengguna sebelum setiap pemanggilan alat. Lihat [kebijakan izin](/docs/id/managed-agents/permission-policies) untuk mengonfigurasi perilaku ini.
</Tip>

## Sediakan autentikasi saat pembuatan sesi

Saat memulai sesi, teruskan `vault_ids` untuk menyediakan kredensial untuk server MCP Anda. Vault adalah koleksi kredensial yang Anda daftarkan sekali dan referensikan berdasarkan ID. Lihat [Autentikasi dengan vault](/docs/id/managed-agents/vaults) untuk cara membuat vault dan mengelola kredensial.

<CodeGroup>
  
````bash
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
````

  
````bash
SESSION_ID=$(ant beta:sessions create \
  --agent "$AGENT_ID" \
  --environment-id "$ENVIRONMENT_ID" \
  --vault-id "$VAULT_ID" \
  --transform id --raw-output)
````

  
````python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    vault_ids=[vault.id],
)
````

  
````typescript
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  vault_ids: [vault.id],
});
````

  
````csharp
var session = await client.Beta.Sessions.Create(new()
{
    Agent = agent.ID,
    EnvironmentID = environment.ID,
    VaultIds = [vault.ID],
});
````

  
````go
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
	EnvironmentID: environment.ID,
	VaultIDs:      []string{vault.ID},
})
if err != nil {
	panic(err)
}
````

  
````java
var session = client.beta().sessions().create(
    SessionCreateParams.builder()
        .agent(agent.id())
        .environmentId(environment.id())
        .addVaultId(vault.id())
        .build()
);
````

  
````php
$session = $client->beta->sessions->create(
    agent: $agent->id,
    environmentID: $environment->id,
    vaultIDs: [$vault->id],
);
````

  
````ruby
session = client.beta.sessions.create(
  agent: agent.id,
  environment_id: environment.id,
  vault_ids: [vault.id]
)
````

</CodeGroup>

Jika kredensial otorisasi yang disediakan dalam vault tidak valid, pembuatan sesi akan berhasil dan interaksi masih dimungkinkan. Acara `session.error` dipancarkan yang menjelaskan kegagalan autentikasi MCP. Anda dapat memutuskan apakah akan memblokir interaksi lebih lanjut pada kesalahan ini, memicu pembaruan kredensial, atau membiarkan sesi berlanjut tanpa MCP. Percobaan ulang autentikasi akan terjadi pada transisi `session.status_idle` ke `session.status_running` berikutnya. Lihat [Aliran acara sesi](/docs/id/managed-agents/events-and-streaming) untuk detail tentang mengonsumsi `session.error` dan acara lainnya.

## Jenis server MCP yang didukung

Claude Managed Agents terhubung ke [server MCP jarak jauh](/docs/id/agents-and-tools/remote-mcp-servers) yang mengekspos titik akhir HTTP. Server harus mendukung transportasi HTTP yang dapat dialirkan dari protokol MCP.

Untuk informasi lebih lanjut tentang MCP dan membangun server MCP, lihat [dokumentasi MCP](https://modelcontextprotocol.io).