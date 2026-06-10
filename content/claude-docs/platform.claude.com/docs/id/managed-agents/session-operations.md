---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/session-operations
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 065e506cd96cfbb02646f402b3d8f65ed2f188f2612337e652bb42f06f8ca91d
---

# Operasi sesi

Mengambil, membuat daftar, memperbarui, mengarsipkan, dan menghapus sesi Claude Managed Agents.

---

Setelah sesi dibuat, gunakan operasi ini untuk membaca, memperbarui, mengarsipkan, atau menghapusnya. Lihat [Memulai sesi](/docs/id/managed-agents/sessions) untuk membuat sesi dan mengirimkan pekerjaan kepadanya.

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Status sesi \{#session-statuses}

Sesi berjalan melalui status-status berikut. Lihat [Memulai sesi](/docs/id/managed-agents/sessions) untuk siklus hidup sesi.

| Status | Deskripsi |
|--------|-------------|
| `idle` | Agen sedang menunggu input, termasuk pesan pengguna atau konfirmasi alat. Sesi dimulai dalam status `idle`. |
| `running` | Agen sedang aktif mengeksekusi. |
| `rescheduling` | Terjadi kesalahan sementara, mencoba ulang secara otomatis. |
| `terminated` | Sesi telah berakhir karena kesalahan yang tidak dapat dipulihkan. |

## Memperbarui konfigurasi agen \{#updating-the-agent-configuration}

Anda dapat memperbarui `agent.tools` dan `agent.mcp_servers` milik sesi, termasuk kebijakan izin, di tengah sesi tanpa membuat versi agen baru. Pembaruan bersifat lokal untuk sesi dan tidak disebarkan kembali ke agen yang mendasarinya.

Semantik pembaruan adalah penggantian penuh: array yang diberikan menjadi nilai baru. Untuk mempertahankan entri yang sudah ada, lakukan `GET` pada sesi, modifikasi array-nya, lalu kirim kembali dengan `POST`.

Sesi harus dalam status `idle` untuk memperbarui agen. [Interupsi](/docs/id/managed-agents/events-and-streaming#integrating-events) sesi jika Anda perlu memperbarui agen saat sesi sedang berjalan.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "agent": {
    "tools": [
      {"type": "agent_toolset_20260401"},
      {"type": "mcp_toolset", "mcp_server_name": "linear"}
    ],
    "mcp_servers": [
      {"type": "url", "name": "linear", "url": "https://mcp.linear.app/sse"}
    ]
  }
}
EOF
````

  
````bash
ant beta:sessions update --session-id "$SESSION_ID" <<'YAML'
agent:
  tools:
    - type: agent_toolset_20260401
    - type: mcp_toolset
      mcp_server_name: linear
  mcp_servers:
    - type: url
      name: linear
      url: https://mcp.linear.app/sse
YAML
````

  
````python
client.beta.sessions.update(
    session.id,
    agent={
        "tools": [
            {"type": "agent_toolset_20260401"},
            {"type": "mcp_toolset", "mcp_server_name": "linear"},
        ],
        "mcp_servers": [
            {"type": "url", "name": "linear", "url": "https://mcp.linear.app/sse"}
        ],
    },
)
````

  
````typescript
await client.beta.sessions.update(session.id, {
  agent: {
    tools: [
      { type: "agent_toolset_20260401" },
      { type: "mcp_toolset", mcp_server_name: "linear" }
    ],
    mcp_servers: [{ type: "url", name: "linear", url: "https://mcp.linear.app/sse" }]
  }
});
````

  
````csharp
await client.Beta.Sessions.Update(session.ID, new()
{
    Agent = new()
    {
        Tools =
        [
            new BetaManagedAgentsAgentToolset20260401Params
            {
                Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
            },
            new BetaManagedAgentsMcpToolsetParams
            {
                Type = BetaManagedAgentsMcpToolsetParamsType.McpToolset,
                McpServerName = "linear",
            },
        ],
        McpServers =
        [
            new()
            {
                Type = BetaManagedAgentsUrlMcpServerParamsType.Url,
                Name = "linear",
                Url = "https://mcp.linear.app/sse",
            },
        ],
    },
});
````

  
````go
_, err = client.Beta.Sessions.Update(ctx, session.ID, anthropic.BetaSessionUpdateParams{
	Agent: anthropic.BetaManagedAgentsSessionAgentUpdateParam{
		Tools: []anthropic.BetaManagedAgentsSessionAgentUpdateToolUnionParam{
			{
				OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
					Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
				},
			},
			{
				OfMCPToolset: &anthropic.BetaManagedAgentsMCPToolsetParams{
					Type:          anthropic.BetaManagedAgentsMCPToolsetParamsTypeMCPToolset,
					MCPServerName: "linear",
				},
			},
		},
		MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{
			{
				Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
				Name: "linear",
				URL:  "https://mcp.linear.app/sse",
			},
		},
	},
})
if err != nil {
	panic(err)
}
````

  
````java
client.beta().sessions().update(
    session.id(),
    SessionUpdateParams.builder()
        .agent(BetaManagedAgentsSessionAgentUpdate.builder()
            .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
                .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                .build())
            .addTool(BetaManagedAgentsMcpToolsetParams.builder()
                .type(BetaManagedAgentsMcpToolsetParams.Type.MCP_TOOLSET)
                .mcpServerName("linear")
                .build())
            .addMcpServer(BetaManagedAgentsUrlMcpServerParams.builder()
                .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
                .name("linear")
                .url("https://mcp.linear.app/sse")
                .build())
            .build())
        .build()
);
````

  
````php
$client->beta->sessions->update(
    $session->id,
    agent: BetaManagedAgentsSessionAgentUpdate::with(
        tools: [
            BetaManagedAgentsAgentToolset20260401Params::with(type: 'agent_toolset_20260401'),
            BetaManagedAgentsMCPToolsetParams::with(mcpServerName: 'linear', type: 'mcp_toolset'),
        ],
        mcpServers: [
            BetaManagedAgentsURLMCPServerParams::with(
                name: 'linear',
                type: 'url',
                url: 'https://mcp.linear.app/sse',
            ),
        ],
    ),
);
````

  
````ruby
client.beta.sessions.update(
  session.id,
  agent: {
    tools: [
      {type: :agent_toolset_20260401},
      {type: :mcp_toolset, mcp_server_name: "linear"}
    ],
    mcp_servers: [
      {type: :url, name: "linear", url: "https://mcp.linear.app/sse"}
    ]
  }
)
````

</CodeGroup>

## Mengambil sesi \{#retrieving-a-session}

<CodeGroup defaultLanguage="CLI">
  
````bash
retrieved=$(curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01")
echo "Status: $(jq -r '.status' <<< "$retrieved")"
````

  
````bash
ant beta:sessions retrieve --session-id "$SESSION_ID"
````

  
````python
retrieved = client.beta.sessions.retrieve(session.id)
print(f"Status: {retrieved.status}")
````

  
````typescript
const retrieved = await client.beta.sessions.retrieve(session.id);
console.log(`Status: ${retrieved.status}`);
````

  
````csharp
var retrieved = await client.Beta.Sessions.Retrieve(session.ID);
Console.WriteLine($"Status: {retrieved.Status.Raw()}");
````

  
````go
retrieved, err := client.Beta.Sessions.Get(ctx, session.ID, anthropic.BetaSessionGetParams{})
if err != nil {
	panic(err)
}
fmt.Printf("Status: %s\n", retrieved.Status)
````

  
````java
var retrieved = client.beta().sessions().retrieve(session.id());
IO.println("Status: " + retrieved.status());
````

  
````php
$retrieved = $client->beta->sessions->retrieve($session->id);
echo "Status: {$retrieved->status}\n";
````

  
````ruby
retrieved = client.beta.sessions.retrieve(session.id)
puts "Status: #{retrieved.status}"
````

</CodeGroup>

## Membuat daftar sesi \{#listing-sessions}

<CodeGroup defaultLanguage="CLI">
  
````bash
curl -fsSL "https://api.anthropic.com/v1/sessions?agent_id=$AGENT_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  | jq -r '.data[] | "\(.id): \(.status)"'
````

  
````bash
ant beta:sessions list --agent-id "$AGENT_ID"
````

  
````python
for listed_session in client.beta.sessions.list(agent_id=agent.id):
    print(f"{listed_session.id}: {listed_session.status}")
````

  
````typescript
for await (const listedSession of client.beta.sessions.list({ agent_id: agent.id })) {
  console.log(`${listedSession.id}: ${listedSession.status}`);
}
````

  
````csharp
var sessions = await client.Beta.Sessions.List(new SessionListParams { AgentID = agent.ID });
await foreach (var listedSession in sessions.Paginate())
{
    Console.WriteLine($"{listedSession.ID}: {listedSession.Status.Raw()}");
}
````

  
````go
page := client.Beta.Sessions.ListAutoPaging(ctx, anthropic.BetaSessionListParams{
	AgentID: anthropic.String(agent.ID),
})
for page.Next() {
	listedSession := page.Current()
	fmt.Printf("%s: %s\n", listedSession.ID, listedSession.Status)
}
if err := page.Err(); err != nil {
	panic(err)
}
````

  
````java
var params = SessionListParams.builder().agentId(agent.id()).build();
for (var listed : client.beta().sessions().list(params).autoPager()) {
    IO.println(listed.id() + ": " + listed.status());
}
````

  
````php
foreach ($client->beta->sessions->list(agentID: $agent->id)->pagingEachItem() as $listedSession) {
    echo "{$listedSession->id}: {$listedSession->status}\n";
}
````

  
````ruby
client.beta.sessions.list(agent_id: agent.id).auto_paging_each do |listed_session|
  puts "#{listed_session.id}: #{listed_session.status}"
end
````

</CodeGroup>

## Mengarsipkan sesi \{#archiving-a-session}

Arsipkan sesi untuk mencegah event baru dikirim sambil tetap mempertahankan riwayatnya. Sesi dengan status `running` tidak dapat diarsipkan; kirim [event interupsi](/docs/id/managed-agents/events-and-streaming#integrating-events) jika Anda perlu segera mengarsipkannya.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl -fsSL -X POST "https://api.anthropic.com/v1/sessions/$SESSION_ID/archive" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:sessions archive \
  --session-id "$SESSION_ID"
````

  
````python
client.beta.sessions.archive(session.id)
````

  
````typescript
await client.beta.sessions.archive(session.id);
````

  
````csharp
await client.Beta.Sessions.Archive(session.ID);
````

  
````go
_, err = client.Beta.Sessions.Archive(ctx, session.ID, anthropic.BetaSessionArchiveParams{})
if err != nil {
	panic(err)
}
````

  
````java
client.beta().sessions().archive(session.id());
````

  
````php
$client->beta->sessions->archive($session->id);
````

  
````ruby
client.beta.sessions.archive(session.id)
````

</CodeGroup>

## Menghapus sesi \{#deleting-a-session}

Hapus sesi untuk menghapus secara permanen catatannya, event-nya, dan sandbox yang terkait. Sesi dengan status `running` tidak dapat dihapus; kirim [event interupsi](/docs/id/managed-agents/events-and-streaming#integrating-events) jika Anda perlu segera menghapusnya.

File, memory store, vault, skill, environment, dan agen adalah sumber daya independen dan tidak terpengaruh oleh penghapusan sesi.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl -fsSL -X DELETE "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:sessions delete \
  --session-id "$SESSION_ID"
````

  
````python
client.beta.sessions.delete(session.id)
````

  
````typescript
await client.beta.sessions.delete(session.id);
````

  
````csharp
await client.Beta.Sessions.Delete(session.ID);
````

  
````go
_, err = client.Beta.Sessions.Delete(ctx, session.ID, anthropic.BetaSessionDeleteParams{})
if err != nil {
	panic(err)
}
````

  
````java
client.beta().sessions().delete(session.id());
````

  
````php
$client->beta->sessions->delete($session->id);
````

  
````ruby
client.beta.sessions.delete(session.id)
````

</CodeGroup>