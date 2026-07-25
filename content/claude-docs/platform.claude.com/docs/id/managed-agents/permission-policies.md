---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/permission-policies
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: d1503569ea8fa067deb9ba245886d50454d6246e4855ef81ff109311ed434cf6
---

# Kebijakan izin

Kontrol kapan alat agen dan MCP dieksekusi.

---

Kebijakan izin mengontrol apakah alat yang dieksekusi server (toolset agen bawaan dan toolset MCP) berjalan secara otomatis atau menunggu persetujuan Anda. Alat kustom dieksekusi oleh aplikasi Anda dan dikontrol oleh Anda, sehingga tidak diatur oleh kebijakan izin.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Jenis kebijakan izin

| Kebijakan      | Perilaku                                                                                                                                                         |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `always_allow` | Alat dieksekusi secara otomatis tanpa konfirmasi.                                                                                                                |
| `always_ask`   | Sesi dijeda dan menunggu persetujuan Anda sebelum mengeksekusi. Lihat [Merespons permintaan konfirmasi](#respond-to-confirmation-requests) untuk alur event-nya. |

Setiap jenis toolset memiliki default-nya sendiri: toolset agen secara default menggunakan `always_allow`, dan toolset MCP secara default menggunakan `always_ask`.

Kebijakan izin mengontrol kapan alat yang diaktifkan berjalan. Untuk menghapus alat dari agen sepenuhnya, nonaktifkan alat tersebut. Lihat [Menonaktifkan alat tertentu](/docs/id/managed-agents/tools#disabling-specific-tools).

## Menetapkan kebijakan untuk toolset

Anda menetapkan kebijakan izin dalam konfigurasi `tools` agen saat Anda membuat agen, dan Anda dapat mengubahnya nanti dengan [memperbarui agen](/docs/id/managed-agents/agent-setup#update-an-agent). Sesi yang sedang berjalan mempertahankan konfigurasi toolset yang digunakan saat sesi dibuat. Pembaruan berlaku untuk sesi yang dibuat setelahnya.

### Izin toolset agen

Saat membuat agen, Anda dapat menerapkan kebijakan ke setiap alat dalam `agent_toolset_20260401` menggunakan `default_config.permission_policy`:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Coding Assistant",
      "model": "claude-opus-5",
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
  model: claude-opus-5
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
      model="claude-opus-5",
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
    model: "claude-opus-5",
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
  using Anthropic.Models.Beta.Agents;

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = new("claude-opus-5"),
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
  		ID: "claude-opus-5",
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
  _ = agent
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;

  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Coding Assistant")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
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
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolsetDefaultConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsAlwaysAskPolicy;

  $agent = $client->beta->agents->create(
      name: 'Coding Assistant',
      model: 'claude-opus-5',
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
    model: "claude-opus-5",
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

`default_config` bersifat opsional. Jika Anda menghilangkannya, toolset agen diaktifkan dengan kebijakan izin default, yaitu `always_allow`.

### Izin toolset MCP

Toolset MCP secara default menggunakan `always_ask`. Ini memastikan bahwa alat baru yang ditambahkan ke server MCP tidak dieksekusi di aplikasi Anda tanpa persetujuan. Untuk menyetujui alat secara otomatis dari server MCP yang tepercaya, tetapkan `default_config.permission_policy` pada entri `mcp_toolset`.

`mcp_server_name` harus cocok dengan `name` dari sebuah server dalam array `mcp_servers`.

Contoh ini menghubungkan server MCP GitHub dan mengizinkan alat-alatnya berjalan tanpa konfirmasi:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Dev Assistant",
      "model": "claude-opus-5",
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
  model: claude-opus-5
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
      model="claude-opus-5",
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
    model: "claude-opus-5",
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
  using Anthropic.Models.Beta.Agents;

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Dev Assistant",
      Model = new("claude-opus-5"),
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
  		ID: "claude-opus-5",
  	},
  	MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{{
  		Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
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
  _ = agent
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;

  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Dev Assistant")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
          .addMcpServer(
              BetaManagedAgentsUrlMcpServerParams.builder()
                  .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
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
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsAlwaysAllowPolicy;
  use Anthropic\Beta\Agents\BetaManagedAgentsMCPToolsetDefaultConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsMCPToolsetParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsURLMCPServerParams;

  $agent = $client->beta->agents->create(
      name: 'Dev Assistant',
      model: 'claude-opus-5',
      mcpServers: [
          BetaManagedAgentsURLMCPServerParams::with(
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
    model: "claude-opus-5",
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

## Menimpa kebijakan alat individual

Gunakan array `configs` untuk menimpa default pada alat individual. Nilai `name` untuk toolset agen tercantum di [Alat yang tersedia](/docs/id/managed-agents/tools#available-tools). Contoh ini mengizinkan seluruh toolset agen secara default tetapi memerlukan konfirmasi sebelum perintah bash apa pun berjalan:

<CodeGroup defaultLanguage="CLI">
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
  ant beta:agents create <<'YAML'
  name: Coding Assistant
  model: claude-opus-5
  tools:
    - type: agent_toolset_20260401
      default_config:
        permission_policy:
          type: always_allow
      configs:
        - name: bash
          permission_policy:
            type: always_ask
  YAML
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
  using Anthropic.Models.Beta.Agents;
  using Tool = Anthropic.Models.Beta.Agents.Tool;

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
  _ = tools
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;
  import java.util.List;

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
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolsetDefaultConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsAlwaysAllowPolicy;
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

Teruskan konfigurasi `tools` ini dalam permintaan pembuatan agen (tab CLI menunjukkan perintah lengkapnya). Toolset MCP mendukung penimpaan per-alat yang sama, dengan `name` diatur ke nama alat yang dilaporkan oleh server MCP. Lihat [Mengonfigurasi alat MCP mana yang tersedia](/docs/id/managed-agents/mcp-connector#configure-which-mcp-tools-are-available).

## Merespons permintaan konfirmasi

Ketika agen memanggil alat dengan kebijakan `always_ask`:

1. Sesi memancarkan event `agent.tool_use` atau `agent.mcp_tool_use`.
2. Sesi dijeda dengan event `session.status_idle` yang `stop_reason.type`-nya adalah `requires_action`. ID event yang memblokir ada di array `stop_reason.event_ids`. Sesi menunggu tanpa batas waktu untuk sebuah respons.
3. Kirim event `user.tool_confirmation` untuk setiap event yang memblokir, dengan meneruskan ID event dalam parameter `tool_use_id`. Atur `result` ke `"allow"` atau `"deny"`. Gunakan `deny_message` untuk menjelaskan penolakan. Anda dapat mengirim beberapa konfirmasi dalam satu permintaan `events`.
4. Setelah semua event yang memblokir diselesaikan, sesi bertransisi kembali ke `running`. Alat yang diizinkan dieksekusi. Alat yang ditolak tidak berjalan, dan agen menerima tool result yang menyatakan bahwa panggilan tersebut ditolak, termasuk `deny_message` Anda.

Dalam contoh berikut, ID event tool-use berasal dari array `stop_reason.event_ids` pada event `session.status_idle`. Pelajari lebih lanjut tentang menerima event di panduan [Aliran event sesi](/docs/id/managed-agents/events-and-streaming#integrating-events), atau [berlangganan webhook](/docs/id/managed-agents/webhooks) untuk mendapatkan notifikasi ketika sesi dijeda untuk menunggu input.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  # Izinkan alat untuk dieksekusi
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
  # Izinkan alat untuk dieksekusi
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
  # Izinkan alat untuk dieksekusi
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
  // Izinkan alat untuk dieksekusi
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
  // Izinkan alat untuk dieksekusi
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
  // Izinkan alat untuk dieksekusi
  _, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
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
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
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
  // Izinkan alat untuk dieksekusi
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

  // Izinkan alat untuk dieksekusi
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
  # Izinkan alat untuk dieksekusi
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

## Alat kustom

Kebijakan izin tidak berlaku untuk alat kustom. Ketika agen memanggil alat kustom, aplikasi Anda menerima event `agent.custom_tool_use` dan bertanggung jawab untuk memutuskan apakah akan mengeksekusinya sebelum mengirim kembali `user.custom_tool_result`. Lihat [Aliran event sesi](/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) untuk alur lengkapnya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Skills" icon="books" href="/docs/id/managed-agents/skills">
    Lampirkan keahlian berbasis filesystem yang dapat digunakan kembali ke agen Anda untuk alur kerja spesifik domain.
  </Card>

  <Card title="Aliran event sesi" icon="lightning" href="/docs/id/managed-agents/events-and-streaming">
    Kirim event, streaming respons, dan interupsi atau alihkan sesi Anda di tengah eksekusi.
  </Card>
</CardGroup>
