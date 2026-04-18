---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/permission-policies
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: fb68f22a1cdfb9d9fb86f17343217e6e7ce6c5980b15f05778f7ea331299d879
---

# Kebijakan izin

Kontrol kapan alat agen dan MCP dijalankan.

---

Kebijakan izin mengontrol apakah alat yang dijalankan server (kumpulan alat agen pra-bangun dan kumpulan alat MCP) berjalan secara otomatis atau menunggu persetujuan Anda. Alat khusus dijalankan oleh aplikasi Anda dan dikendalikan oleh Anda, jadi tidak diatur oleh kebijakan izin.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

## Jenis kebijakan izin

| Kebijakan | Perilaku |
| --- | --- |
| `always_allow` | Alat dijalankan secara otomatis tanpa konfirmasi. |
| `always_ask` | Sesi mengeluarkan acara `session.status_idle` dan menunggu acara `user.tool_confirmation` sebelum dijalankan. |

## Tetapkan kebijakan untuk kumpulan alat

### Izin kumpulan alat agen
Saat membuat agen, Anda dapat secara opsional menerapkan kebijakan ke setiap alat dalam `agent_toolset_20260401` menggunakan `default_config.permission_policy`:

<CodeGroup defaultLanguage="CLI">
```bash curl
agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{
    "name": "Coding Assistant",
    "model": "claude-opus-4-7",
    "tools": [
      {
        "type": "agent_toolset_20260401",
        "default_config": {
          "permission_policy": {"type": "always_ask"}
        }
      }
    ]
  }')
```

```bash CLI
ant beta:agents create <<'YAML'
name: Coding Assistant
model: claude-opus-4-7
tools:
  - type: agent_toolset_20260401
    default_config:
      permission_policy:
        type: always_ask
YAML
```

```python Python
agent = client.beta.agents.create(
    name="Coding Assistant",
    model="claude-opus-4-7",
    tools=[
        {
            "type": "agent_toolset_20260401",
            "default_config": {
                "permission_policy": {"type": "always_ask"},
            },
        },
    ],
)
```

```typescript TypeScript
const agent = await client.beta.agents.create({
  name: "Coding Assistant",
  model: "claude-opus-4-7",
  tools: [
    {
      type: "agent_toolset_20260401",
      default_config: {
        permission_policy: { type: "always_ask" }
      }
    }
  ]
});
```

```csharp C#
var agent = await client.Beta.Agents.Create(new()
{
    Name = "Coding Assistant",
    Model = new("claude-opus-4-7"),
    Tools =
    [
        new BetaManagedAgentsAgentToolset20260401Params
        {
            Type = "agent_toolset_20260401",
            DefaultConfig = new()
            {
                PermissionPolicy = new BetaManagedAgentsAlwaysAskPolicy { Type = "always_ask" },
            },
        },
    ],
});
```

```go Go
agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name: "Coding Assistant",
	Model: anthropic.BetaManagedAgentsModelConfigParams{
		ID:   "claude-opus-4-7",
		Type: anthropic.BetaManagedAgentsModelConfigParamsTypeModelConfig,
	},
	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
			DefaultConfig: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParams{
				PermissionPolicy: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParamsPermissionPolicyUnion{
					OfAlwaysAsk: &anthropic.BetaManagedAgentsAlwaysAskPolicyParam{
						Type: anthropic.BetaManagedAgentsAlwaysAskPolicyTypeAlwaysAsk,
					},
				},
			},
		},
	}},
})
if err != nil {
	panic(err)
}
```

```java Java
var agent = client.beta().agents().create(
    AgentCreateParams.builder()
        .name("Coding Assistant")
        .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_7)
        .addTool(
            BetaManagedAgentsAgentToolset20260401Params.builder()
                .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                .defaultConfig(
                    BetaManagedAgentsAgentToolsetDefaultConfigParams.builder()
                        .permissionPolicy(
                            BetaManagedAgentsAlwaysAskPolicy.builder()
                                .type(BetaManagedAgentsAlwaysAskPolicy.Type.ALWAYS_ASK)
                                .build()
                        )
                        .build()
                )
                .build()
        )
        .build()
);
```

```php PHP

$agent = $client->beta->agents->create(
    name: 'Coding Assistant',
    model: 'claude-opus-4-7',
    tools: [
        BetaManagedAgentsAgentToolset20260401Params::with(
            type: 'agent_toolset_20260401',
            defaultConfig: BetaManagedAgentsAgentToolsetDefaultConfigParams::with(
                permissionPolicy: BetaManagedAgentsAlwaysAskPolicy::with(type: 'always_ask'),
            ),
        ),
    ],
);
```

```ruby Ruby
agent = client.beta.agents.create(
  name: "Coding Assistant",
  model: "claude-opus-4-7",
  tools: [
    {
      type: "agent_toolset_20260401",
      default_config: {
        permission_policy: {type: "always_ask"}
      }
    }
  ]
)
```
</CodeGroup>

`default_config` adalah pengaturan opsional. Jika Anda menghilangkannya, kumpulan alat agen akan diaktifkan dengan kebijakan izin default, `always_allow`.

### Izin kumpulan alat MCP

Kumpulan alat MCP secara default menggunakan `always_ask`. Ini memastikan bahwa alat baru yang ditambahkan ke server MCP tidak dijalankan dalam aplikasi Anda tanpa persetujuan. Untuk menyetujui otomatis alat dari server MCP yang terpercaya, atur `permission_policy` pada entri `mcp_toolset`.

`mcp_server_name` harus cocok dengan `name` yang direferensikan dalam array `mcp_servers`.

Contoh ini menghubungkan server MCP GitHub dan memungkinkan alatnya berjalan tanpa konfirmasi:

<CodeGroup defaultLanguage="CLI">
```bash curl
agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{
    "name": "Dev Assistant",
    "model": "claude-opus-4-7",
    "mcp_servers": [
      {"type": "url", "name": "github", "url": "https://mcp.example.com/github"}
    ],
    "tools": [
      {"type": "agent_toolset_20260401"},
      {
        "type": "mcp_toolset",
        "mcp_server_name": "github",
        "default_config": {
          "permission_policy": {"type": "always_allow"}
        }
      }
    ]
  }')
```

```bash CLI
ant beta:agents create <<'YAML'
name: Dev Assistant
model: claude-opus-4-7
mcp_servers:
  - type: url
    name: github
    url: https://mcp.example.com/github
tools:
  - type: agent_toolset_20260401
  - type: mcp_toolset
    mcp_server_name: github
    default_config:
      permission_policy:
        type: always_allow
YAML
```

```python Python
agent = client.beta.agents.create(
    name="Dev Assistant",
    model="claude-opus-4-7",
    mcp_servers=[
        {"type": "url", "name": "github", "url": "https://mcp.example.com/github"},
    ],
    tools=[
        {"type": "agent_toolset_20260401"},
        {
            "type": "mcp_toolset",
            "mcp_server_name": "github",
            "default_config": {
                "permission_policy": {"type": "always_allow"},
            },
        },
    ],
)
```

```typescript TypeScript
const agent = await client.beta.agents.create({
  name: "Dev Assistant",
  model: "claude-opus-4-7",
  mcp_servers: [{ type: "url", name: "github", url: "https://mcp.example.com/github" }],
  tools: [
    { type: "agent_toolset_20260401" },
    {
      type: "mcp_toolset",
      mcp_server_name: "github",
      default_config: {
        permission_policy: { type: "always_allow" }
      }
    }
  ]
});
```

```csharp C#
var agent = await client.Beta.Agents.Create(new()
{
    Name = "Dev Assistant",
    Model = new("claude-opus-4-7"),
    McpServers =
    [
        new() { Type = "url", Name = "github", Url = "https://mcp.example.com/github" },
    ],
    Tools =
    [
        new BetaManagedAgentsAgentToolset20260401Params
        {
            Type = "agent_toolset_20260401",
        },
        new BetaManagedAgentsMcpToolsetParams
        {
            Type = "mcp_toolset",
            McpServerName = "github",
            DefaultConfig = new()
            {
                PermissionPolicy = new BetaManagedAgentsAlwaysAllowPolicy { Type = "always_allow" },
            },
        },
    ],
});
```

```go Go
agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name: "Dev Assistant",
	Model: anthropic.BetaManagedAgentsModelConfigParams{
		ID:   "claude-opus-4-7",
		Type: anthropic.BetaManagedAgentsModelConfigParamsTypeModelConfig,
	},
	MCPServers: []anthropic.BetaManagedAgentsUrlmcpServerParams{{
		Type: anthropic.BetaManagedAgentsUrlmcpServerParamsTypeURL,
		Name: "github",
		URL:  "https://mcp.example.com/github",
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
				DefaultConfig: anthropic.BetaManagedAgentsMCPToolsetDefaultConfigParams{
					PermissionPolicy: anthropic.BetaManagedAgentsMCPToolsetDefaultConfigParamsPermissionPolicyUnion{
						OfAlwaysAllow: &anthropic.BetaManagedAgentsAlwaysAllowPolicyParam{
							Type: anthropic.BetaManagedAgentsAlwaysAllowPolicyTypeAlwaysAllow,
						},
					},
				},
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
        .name("Dev Assistant")
        .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_7)
        .addMcpServer(
            BetaManagedAgentsUrlmcpServerParams.builder()
                .type(BetaManagedAgentsUrlmcpServerParams.Type.URL)
                .name("github")
                .url("https://mcp.example.com/github")
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
                .defaultConfig(
                    BetaManagedAgentsMcpToolsetDefaultConfigParams.builder()
                        .permissionPolicy(
                            BetaManagedAgentsAlwaysAllowPolicy.builder()
                                .type(BetaManagedAgentsAlwaysAllowPolicy.Type.ALWAYS_ALLOW)
                                .build()
                        )
                        .build()
                )
                .build()
        )
        .build()
);
```

```php PHP
use Anthropic\Beta\Agents\BetaManagedAgentsMCPToolsetDefaultConfigParams;
use Anthropic\Beta\Agents\BetaManagedAgentsMCPToolsetParams;
use Anthropic\Beta\Agents\BetaManagedAgentsUrlmcpServerParams;

$agent = $client->beta->agents->create(
    name: 'Dev Assistant',
    model: 'claude-opus-4-7',
    mcpServers: [
        BetaManagedAgentsUrlmcpServerParams::with(
            type: 'url',
            name: 'github',
            url: 'https://mcp.example.com/github',
        ),
    ],
    tools: [
        BetaManagedAgentsAgentToolset20260401Params::with(
            type: 'agent_toolset_20260401',
        ),
        BetaManagedAgentsMCPToolsetParams::with(
            type: 'mcp_toolset',
            mcpServerName: 'github',
            defaultConfig: BetaManagedAgentsMCPToolsetDefaultConfigParams::with(
                permissionPolicy: BetaManagedAgentsAlwaysAllowPolicy::with(type: 'always_allow'),
            ),
        ),
    ],
);
```

```ruby Ruby
agent = client.beta.agents.create(
  name: "Dev Assistant",
  model: "claude-opus-4-7",
  mcp_servers: [
    {type: "url", name: "github", url: "https://mcp.example.com/github"}
  ],
  tools: [
    {type: "agent_toolset_20260401"},
    {
      type: "mcp_toolset",
      mcp_server_name: "github",
      default_config: {
        permission_policy: {type: "always_allow"}
      }
    }
  ]
)
```
</CodeGroup>

## Ganti kebijakan alat individual

Gunakan array `configs` untuk mengganti default untuk alat individual. Contoh ini memungkinkan kumpulan alat agen lengkap secara default tetapi memerlukan konfirmasi sebelum perintah bash apa pun dijalankan:

<CodeGroup>
```bash curl
tools='[
  {
    "type": "agent_toolset_20260401",
    "default_config": {
      "permission_policy": {"type": "always_allow"}
    },
    "configs": [
      {
        "name": "bash",
        "permission_policy": {"type": "always_ask"}
      }
    ]
  }
]'
```

```bash CLI
tools=$(cat <<'YAML'
- type: agent_toolset_20260401
  default_config:
    permission_policy:
      type: always_allow
  configs:
    - name: bash
      permission_policy:
        type: always_ask
YAML
)
```

```python Python
tools = [
    {
        "type": "agent_toolset_20260401",
        "default_config": {
            "permission_policy": {"type": "always_allow"},
        },
        "configs": [
            {
                "name": "bash",
                "permission_policy": {"type": "always_ask"},
            },
        ],
    },
]
```

```typescript TypeScript
const tools = [
  {
    type: "agent_toolset_20260401",
    default_config: {
      permission_policy: { type: "always_allow" }
    },
    configs: [
      {
        name: "bash",
        permission_policy: { type: "always_ask" }
      }
    ]
  }
] satisfies Anthropic.Beta.AgentCreateParams["tools"];
```

```csharp C#
Tool[] tools =
[
    new BetaManagedAgentsAgentToolset20260401Params
    {
        Type = "agent_toolset_20260401",
        DefaultConfig = new()
        {
            PermissionPolicy = new BetaManagedAgentsAlwaysAllowPolicy { Type = "always_allow" },
        },
        Configs =
        [
            new()
            {
                Name = "bash",
                PermissionPolicy = new BetaManagedAgentsAlwaysAskPolicy { Type = "always_ask" },
            },
        ],
    },
];
```

```go Go
tools := []anthropic.BetaAgentNewParamsToolUnion{{
	OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
		Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
		DefaultConfig: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParams{
			PermissionPolicy: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParamsPermissionPolicyUnion{
				OfAlwaysAllow: &anthropic.BetaManagedAgentsAlwaysAllowPolicyParam{
					Type: anthropic.BetaManagedAgentsAlwaysAllowPolicyTypeAlwaysAllow,
				},
			},
		},
		Configs: []anthropic.BetaManagedAgentsAgentToolConfigParams{{
			Name: anthropic.BetaManagedAgentsAgentToolConfigParamsNameBash,
			PermissionPolicy: anthropic.BetaManagedAgentsAgentToolConfigParamsPermissionPolicyUnion{
				OfAlwaysAsk: &anthropic.BetaManagedAgentsAlwaysAskPolicyParam{
					Type: anthropic.BetaManagedAgentsAlwaysAskPolicyTypeAlwaysAsk,
				},
			},
		}},
	},
}}
```

```java Java
var tools = List.of(
    AgentCreateParams.Tool.ofAgentToolset20260401(
        BetaManagedAgentsAgentToolset20260401Params.builder()
            .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
            .defaultConfig(
                BetaManagedAgentsAgentToolsetDefaultConfigParams.builder()
                    .permissionPolicy(
                        BetaManagedAgentsAlwaysAllowPolicy.builder()
                            .type(BetaManagedAgentsAlwaysAllowPolicy.Type.ALWAYS_ALLOW)
                            .build()
                    )
                    .build()
            )
            .addConfig(
                BetaManagedAgentsAgentToolConfigParams.builder()
                    .name(BetaManagedAgentsAgentToolConfigParams.Name.BASH)
                    .permissionPolicy(
                        BetaManagedAgentsAlwaysAskPolicy.builder()
                            .type(BetaManagedAgentsAlwaysAskPolicy.Type.ALWAYS_ASK)
                            .build()
                    )
                    .build()
            )
            .build()
    )
);
```

```php PHP
use Anthropic\Beta\Agents\BetaManagedAgentsAlwaysAskPolicy;

$tools = [
    BetaManagedAgentsAgentToolset20260401Params::with(
        type: 'agent_toolset_20260401',
        defaultConfig: BetaManagedAgentsAgentToolsetDefaultConfigParams::with(
            permissionPolicy: BetaManagedAgentsAlwaysAllowPolicy::with(type: 'always_allow'),
        ),
        configs: [
            BetaManagedAgentsAgentToolConfigParams::with(
                name: 'bash',
                permissionPolicy: BetaManagedAgentsAlwaysAskPolicy::with(type: 'always_ask'),
            ),
        ],
    ),
];
```

```ruby Ruby
tools = [
  {
    type: "agent_toolset_20260401",
    default_config: {
      permission_policy: {type: "always_allow"}
    },
    configs: [
      {
        name: "bash",
        permission_policy: {type: "always_ask"}
      }
    ]
  }
]
```
</CodeGroup>

## Merespons permintaan konfirmasi

Ketika agen memanggil alat dengan kebijakan `always_ask`:

1. Sesi mengeluarkan acara `agent.tool_use` atau `agent.mcp_tool_use`.
2. Sesi dijeda dengan acara `session.status_idle` yang berisi `stop_reason: requires_action`. ID acara pemblokiran ada dalam array `stop_reason.requires_action.event_ids`.
3. Kirim acara `user.tool_confirmation` untuk masing-masing, meneruskan ID acara dalam parameter `tool_use_id`. Atur `result` ke `"allow"` atau `"deny"`. Gunakan `deny_message` untuk menjelaskan penolakan.
4. Setelah semua acara pemblokiran diselesaikan, sesi beralih kembali ke `running`.

Pelajari lebih lanjut tentang penanganan acara dalam panduan [aliran acara sesi](/docs/id/managed-agents/events-and-streaming).

<CodeGroup>
```bash curl
# Izinkan alat untuk dijalankan
curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{
    "events": [
      {
        "type": "user.tool_confirmation",
        "tool_use_id": "'$AGENT_TOOL_USE_EVENT_ID'",
        "result": "allow"
      }
    ]
  }'

# Atau tolak dengan penjelasan
curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{
    "events": [
      {
        "type": "user.tool_confirmation",
        "tool_use_id": "'$MCP_TOOL_USE_EVENT_ID'",
        "result": "deny",
        "deny_message": "Don'\''t create issues in the production project. Use the staging project."
      }
    ]
  }'
```

```bash CLI
# Izinkan alat untuk dijalankan
ant beta:sessions:events send \
  --session-id "$SESSION_ID" \
  --event "{type: user.tool_confirmation, tool_use_id: $AGENT_TOOL_USE_EVENT_ID, result: allow}"

# Atau tolak dengan penjelasan
ant beta:sessions:events send \
  --session-id "$SESSION_ID" \
  --event "{type: user.tool_confirmation, tool_use_id: $MCP_TOOL_USE_EVENT_ID, result: deny,
    deny_message: Don't create issues in the production project. Use the staging project.}"
```

```python Python
# Izinkan alat untuk dijalankan
client.beta.sessions.events.send(
    session.id,
    events=[
        {
            "type": "user.tool_confirmation",
            "tool_use_id": agent_tool_use_event.id,
            "result": "allow",
        },
    ],
)

# Atau tolak dengan penjelasan
client.beta.sessions.events.send(
    session.id,
    events=[
        {
            "type": "user.tool_confirmation",
            "tool_use_id": mcp_tool_use_event.id,
            "result": "deny",
            "deny_message": "Don't create issues in the production project. Use the staging project.",
        },
    ],
)
```

```typescript TypeScript
// Izinkan alat untuk dijalankan
await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.tool_confirmation",
      tool_use_id: agent_tool_use_event.id,
      result: "allow"
    }
  ]
});

// Atau tolak dengan penjelasan
await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.tool_confirmation",
      tool_use_id: mcp_tool_use_event.id,
      result: "deny",
      deny_message: "Don't create issues in the production project. Use the staging project."
    }
  ]
});
```

```csharp C#
// Izinkan alat untuk dijalankan
await client.Beta.Sessions.Events.Send(session.ID, new()
{
    Events =
    [
        new BetaManagedAgentsUserToolConfirmationEventParams
        {
            Type = "user.tool_confirmation",
            ToolUseID = agentToolUseEvent.ID,
            Result = "allow",
        },
    ],
});

// Atau tolak dengan penjelasan
await client.Beta.Sessions.Events.Send(session.ID, new()
{
    Events =
    [
        new BetaManagedAgentsUserToolConfirmationEventParams
        {
            Type = "user.tool_confirmation",
            ToolUseID = mcpToolUseEvent.ID,
            Result = "deny",
            DenyMessage = "Don't create issues in the production project. Use the staging project.",
        },
    ],
});
```

```go Go
// Izinkan alat untuk dijalankan
_, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.SendEventsParamsUnion{{
		OfUserToolConfirmation: &anthropic.BetaManagedAgentsUserToolConfirmationEventParams{
			Type:      anthropic.BetaManagedAgentsUserToolConfirmationEventParamsTypeUserToolConfirmation,
			ToolUseID: agentToolUseEvent.ID,
			Result:    anthropic.BetaManagedAgentsUserToolConfirmationEventParamsResultAllow,
		},
	}},
})
if err != nil {
	panic(err)
}

// Atau tolak dengan penjelasan
_, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.SendEventsParamsUnion{{
		OfUserToolConfirmation: &anthropic.BetaManagedAgentsUserToolConfirmationEventParams{
			Type:        anthropic.BetaManagedAgentsUserToolConfirmationEventParamsTypeUserToolConfirmation,
			ToolUseID:   mcpToolUseEvent.ID,
			Result:      anthropic.BetaManagedAgentsUserToolConfirmationEventParamsResultDeny,
			DenyMessage: anthropic.String("Don't create issues in the production project. Use the staging project."),
		},
	}},
})
if err != nil {
	panic(err)
}
```

```java Java
// Izinkan alat untuk dijalankan
client.beta().sessions().events().send(
    session.id(),
    EventSendParams.builder()
        .addEvent(
            BetaManagedAgentsUserToolConfirmationEventParams.builder()
                .type(BetaManagedAgentsUserToolConfirmationEventParams.Type.USER_TOOL_CONFIRMATION)
                .toolUseId(agentToolUseEvent.id())
                .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.ALLOW)
                .build()
        )
        .build()
);

// Atau tolak dengan penjelasan
client.beta().sessions().events().send(
    session.id(),
    EventSendParams.builder()
        .addEvent(
            BetaManagedAgentsUserToolConfirmationEventParams.builder()
                .type(BetaManagedAgentsUserToolConfirmationEventParams.Type.USER_TOOL_CONFIRMATION)
                .toolUseId(mcpToolUseEvent.id())
                .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.DENY)
                .denyMessage("Don't create issues in the production project. Use the staging project.")
                .build()
        )
        .build()
);
```

```php PHP
use Anthropic\Beta\Sessions\Events\ManagedAgentsUserToolConfirmationEventParams;

// Izinkan alat untuk dijalankan
$client->beta->sessions->events->send(
    $session->id,
    events: [
        ManagedAgentsUserToolConfirmationEventParams::with(
            type: 'user.tool_confirmation',
            toolUseID: $agentToolUseEvent->id,
            result: 'allow',
        ),
    ],
);

// Atau tolak dengan penjelasan
$client->beta->sessions->events->send(
    $session->id,
    events: [
        ManagedAgentsUserToolConfirmationEventParams::with(
            type: 'user.tool_confirmation',
            toolUseID: $mcpToolUseEvent->id,
            result: 'deny',
            denyMessage: "Don't create issues in the production project. Use the staging project.",
        ),
    ],
);
```

```ruby Ruby
# Izinkan alat untuk dijalankan
client.beta.sessions.events.send_(
  session.id,
  events: [
    {
      type: "user.tool_confirmation",
      tool_use_id: agent_tool_use_event.id,
      result: "allow"
    }
  ]
)

# Atau tolak dengan penjelasan
client.beta.sessions.events.send_(
  session.id,
  events: [
    {
      type: "user.tool_confirmation",
      tool_use_id: mcp_tool_use_event.id,
      result: "deny",
      deny_message: "Don't create issues in the production project. Use the staging project."
    }
  ]
)
```
</CodeGroup>

## Alat khusus

Kebijakan izin tidak berlaku untuk alat khusus. Ketika agen memanggil alat khusus, aplikasi Anda menerima acara `agent.custom_tool_use` dan bertanggung jawab untuk memutuskan apakah akan menjalankannya sebelum mengirim kembali `user.custom_tool_result`. Lihat [Aliran acara sesi](/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) untuk alur lengkapnya.