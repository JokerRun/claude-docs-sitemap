---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/multi-agent
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: cde5882abe93f2760af3764491770f3b7404a523ce874a15de6ce4957bf5b69f
---

# Sesi multiagen

Koordinasikan beberapa agen dalam satu sesi.

---

Orkestrasi multiagen memungkinkan satu agen berkoordinasi dengan agen lain untuk menyelesaikan pekerjaan yang kompleks. Agen dapat bertindak secara paralel dengan konteks terisolasi masing-masing, yang membantu meningkatkan kualitas output dan juga dapat mempercepat waktu penyelesaian.

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Cara kerjanya \{#how-it-works}

Semua agen berbagi sandbox, filesystem, dan [kredensial vault](/docs/id/managed-agents/vaults) yang sama, tetapi setiap agen berjalan di **session thread** (utas sesi) miliknya sendiri, yaitu aliran event dengan konteks terisolasi yang memiliki riwayat percakapan sendiri. Koordinator melaporkan aktivitas di **primary thread** (utas utama), yang sama dengan [aliran event](/docs/id/managed-agents/events-and-streaming) tingkat sesi; thread tambahan dibuat saat runtime ketika koordinator mendelegasikan pekerjaan.

Thread bersifat persisten: koordinator dapat mengirim tindak lanjut ke agen yang telah dipanggil sebelumnya, dan agen tersebut tetap menyimpan semua hal dari giliran sebelumnya.

Setiap agen menggunakan konfigurasinya sendiri (model, prompt sistem, alat, server MCP, dan skill) sebagaimana didefinisikan saat agen tersebut dibuat. Alat, server MCP, dan konteks tidak dibagikan antar agen.

### Apa yang sebaiknya didelegasikan \{#what-to-delegate}

Koordinasi multiagen paling cocok untuk tugas kompleks yang memerlukan pekerjaan di berbagai permukaan, atau ketika beberapa tugas dengan cakupan yang jelas berkontribusi pada satu tujuan keseluruhan.

Pola yang bekerja dengan baik:

- **Paralelisasi:** Sebarkan subtugas independen secara bersamaan (mencari di beberapa sumber, menganalisis file terpisah) dan biarkan koordinator menyintesis hasilnya.
- **Spesialisasi:** Arahkan ke agen dengan prompt sistem dan alat yang berfokus pada domain tertentu, seperti agen keamanan atau agen dokumentasi, alih-alih membebani satu agen dengan semua kemampuan.
- **Eskalasi:** Konsultasikan dengan agen atau model yang lebih mumpuni untuk sebagian subtugas yang kompleks.

## Mengonfigurasi koordinator \{#configure-the-coordinator}

Saat [mendefinisikan agen Anda](/docs/id/managed-agents/agent-setup), atur `multiagent` untuk mendeklarasikan daftar agen yang dapat didelegasikan oleh koordinator:

<CodeGroup defaultLanguage="CLI">
  
````bash
coordinator=$(curl -fsS https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "name": "Engineering Lead",
  "model": "claude-opus-4-8",
  "system": "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
  "tools": [
    {
      "type": "agent_toolset_20260401"
    }
  ],
  "multiagent": {
    "type": "coordinator",
    "agents": [
      {"type": "agent", "id": "$REVIEWER_AGENT_ID"},
      {"type": "agent", "id": "$TEST_WRITER_AGENT_ID"}
    ]
  }
}
EOF
)
````

  
````bash
ant beta:agents create <<YAML
name: Engineering Lead
model: claude-opus-4-8
system: You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.
tools:
  - type: agent_toolset_20260401
multiagent:
  type: coordinator
  agents:
    - type: agent
      id: $REVIEWER_AGENT_ID
    - type: agent
      id: $TEST_WRITER_AGENT_ID
YAML
````

  
````python
coordinator = client.beta.agents.create(
    name="Engineering Lead",
    model="claude-opus-4-8",
    system="You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    tools=[
        {"type": "agent_toolset_20260401"},
    ],
    multiagent={
        "type": "coordinator",
        "agents": [
            {"type": "agent", "id": reviewer_agent.id},
            {"type": "agent", "id": test_writer_agent.id},
        ],
    },
)
````

  
````typescript
const coordinator = await client.beta.agents.create({
  name: "Engineering Lead",
  model: "claude-opus-4-8",
  system:
    "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
  tools: [{ type: "agent_toolset_20260401" }],
  multiagent: {
    type: "coordinator",
    agents: [
      { type: "agent", id: reviewerAgent.id },
      { type: "agent", id: testWriterAgent.id },
    ],
  },
});
````

  
````csharp
var coordinator = await client.Beta.Agents.Create(new()
{
    Name = "Engineering Lead",
    Model = BetaManagedAgentsModel.ClaudeOpus4_8,
    System = "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    Tools =
    [
        new BetaManagedAgentsAgentToolset20260401Params
        {
            Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
        },
    ],
    Multiagent = new BetaManagedAgentsMultiagentParams
    {
        Type = BetaManagedAgentsMultiagentParamsType.Coordinator,
        Agents = [reviewerAgent.ID, testWriterAgent.ID],
    },
});
````

  
````go
coordinator, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name:   "Engineering Lead",
	Model:  anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus4_8},
	System: anthropic.String("You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent."),
	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
		},
	}},
	Multiagent: anthropic.BetaManagedAgentsMultiagentParams{
		Type: anthropic.BetaManagedAgentsMultiagentParamsTypeCoordinator,
		Agents: []anthropic.BetaManagedAgentsMultiagentRosterEntryParamsUnion{
			{OfString: anthropic.String(reviewerAgent.ID)},
			{OfString: anthropic.String(testWriterAgent.ID)},
		},
	},
})
if err != nil {
	panic(err)
}
````

  
````java
var coordinator = client.beta().agents().create(
    AgentCreateParams.builder()
        .name("Engineering Lead")
        .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
        .system("You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.")
        .addTool(
            BetaManagedAgentsAgentToolset20260401Params.builder()
                .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                .build()
        )
        .multiagent(BetaManagedAgentsMultiagentParams.builder()
            .type(BetaManagedAgentsMultiagentParams.Type.COORDINATOR)
            .addAgent(BetaManagedAgentsAgentParams.builder()
                .type(BetaManagedAgentsAgentParams.Type.AGENT)
                .id(reviewerAgent.id())
                .build())
            .addAgent(BetaManagedAgentsAgentParams.builder()
                .type(BetaManagedAgentsAgentParams.Type.AGENT)
                .id(testWriterAgent.id())
                .build())
            .build())
        .build()
);
````

  
````php
$coordinator = $client->beta->agents->create(
    name: 'Engineering Lead',
    model: 'claude-opus-4-8',
    system: 'You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.',
    tools: [
        ['type' => 'agent_toolset_20260401'],
    ],
    multiagent: [
        'type' => 'coordinator',
        'agents' => [
            ['type' => 'agent', 'id' => $reviewerAgent->id],
            ['type' => 'agent', 'id' => $testWriterAgent->id],
        ],
    ],
);
````

  
````ruby
coordinator = client.beta.agents.create(
  name: "Engineering Lead",
  model: "claude-opus-4-8",
  system: "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
  tools: [
    {type: "agent_toolset_20260401"}
  ],
  multiagent: {
    type: "coordinator",
    agents: [
      {type: "agent", id: reviewer_agent.id},
      {type: "agent", id: test_writer_agent.id}
    ]
  }
)
````

</CodeGroup>

`multiagent.agents` dapat menerima salah satu dari berikut ini:
* `{"type": "agent", "id": agent.id}` mereferensikan `agent` yang telah dibuat sebelumnya berdasarkan ID. Jika `version` tidak ditentukan, referensi dipatok ke versi terbaru agen tersebut pada saat koordinator dibuat.
* `{"type": "agent", "id": agent.id, "version": agent.version}` mematok versi agen tertentu.
* `{"type": "self"}` memungkinkan koordinator membuat salinan dirinya sendiri.

Konfigurasi koordinator, termasuk daftar `multiagent.agents`-nya, di-snapshot saat koordinator dibuat atau diperbarui. Agen yang direferensikan tetap dipatok ke versi yang di-resolve pada saat itu dan tidak secara otomatis mengambil pembaruan selanjutnya pada definisinya. Untuk mendelegasikan ke versi yang lebih baru dari agen yang direferensikan, [perbarui koordinator](/docs/id/managed-agents/agent-setup#update-an-agent) agar daftarnya mereferensikan versi tersebut.

Koordinator hanya dapat mendelegasikan ke satu tingkat agen; kedalaman > 1 diabaikan. Maksimal 20 agen unik dapat dicantumkan di `multiagent.agents`, tetapi koordinator dapat memanggil beberapa salinan dari setiap agen.

## Membuat sesi \{#create-the-session}

Buat sesi yang mereferensikan koordinator. Koordinator mendelegasikan ke agen dalam daftarnya sesuai kebutuhan.

<CodeGroup>
  
````bash
session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "agent": "$COORDINATOR_ID",
  "environment_id": "$ENVIRONMENT_ID"
}
EOF
)
SESSION_ID=$(jq -r '.id' <<< "$session")
````

  
````bash
ant beta:sessions create \
  --agent "$COORDINATOR_ID" \
  --environment-id "$ENVIRONMENT_ID"
````

  
````python
session = client.beta.sessions.create(
    agent=coordinator.id,
    environment_id=environment.id,
)
````

  
````typescript
const session = await client.beta.sessions.create({
  agent: coordinator.id,
  environment_id: environment.id,
});
````

  
````csharp
var session = await client.Beta.Sessions.Create(new()
{
    Agent = coordinator.ID,
    EnvironmentID = environment.ID,
});
````

  
````go
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfString: anthropic.String(coordinator.ID),
	},
	EnvironmentID: environment.ID,
})
if err != nil {
	panic(err)
}
````

  
````java
var session = client.beta().sessions().create(SessionCreateParams.builder()
    .agent(coordinator.id())
    .environmentId(environment.id())
    .build());
````

  
````php
$session = $client->beta->sessions->create(
    agent: $coordinator->id,
    environmentID: $environment->id,
);
````

  
````ruby
session = client.beta.sessions.create(
  agent: coordinator.id,
  environment_id: environment.id
)
````

</CodeGroup>

## Menghubungkan agen ke server MCP \{#connect-agents-to-mcp-servers}

Server MCP memiliki cakupan per agen (setiap definisi agen mendeklarasikan server dan alatnya sendiri), sedangkan kredensial vault memiliki cakupan per sesi (`vault_ids` yang diteruskan saat pembuatan sesi berlaku untuk setiap thread). Dua implikasi untuk integrasi Anda:
- Untuk mengautentikasi server MCP, sertakan kredensial vault untuk setiap server MCP yang digunakan di seluruh agen.
- Untuk membatasi akses agen, deklarasikan hanya server yang dibutuhkan dalam definisi agen tersebut.

<CodeGroup>
  
````bash
research_agent_id=$(curl --fail-with-body -sS "$BASE/v1/agents" "${H[@]}" --data @- <<'EOF' | jq -er '.id'
{
  "name": "researcher",
  "model": "claude-haiku-4-5",
  "mcp_servers": [{"type": "url", "name": "github", "url": "https://api.githubcopilot.com/mcp/"}],
  "tools": [{"type": "mcp_toolset", "mcp_server_name": "github"}]
}
EOF
)

coordinator_id=$(curl --fail-with-body -sS "$BASE/v1/agents" "${H[@]}" --data @- <<EOF | jq -er '.id'
{
  "name": "coordinator",
  "model": "claude-opus-4-8",
  "tools": [{"type": "agent_toolset_20260401"}],
  "multiagent": {
    "type": "coordinator",
    "agents": [{"type": "agent", "id": "$research_agent_id"}]
  }
}
EOF
)

session_id=$(curl --fail-with-body -sS "$BASE/v1/sessions" "${H[@]}" --data @- <<EOF | jq -er '.id'
{
  "agent": "$coordinator_id",
  "environment_id": "$environment_id",
  "vault_ids": ["$vault_id"]
}
EOF
)
echo "$session_id"
````

  
````bash
research_agent_id=$(ant beta:agents create --transform id --raw-output <<YAML
name: researcher
model: claude-haiku-4-5
mcp_servers:
  - type: url
    name: github
    url: https://api.githubcopilot.com/mcp/
tools:
  - type: mcp_toolset
    mcp_server_name: github
YAML
)

coordinator_id=$(ant beta:agents create --transform id --raw-output <<YAML
name: coordinator
model: claude-opus-4-8
tools:
  - type: agent_toolset_20260401
multiagent:
  type: coordinator
  agents:
    - type: agent
      id: $research_agent_id
YAML
)

session_id=$(ant beta:sessions create \
  --agent "$coordinator_id" \
  --environment-id "$environment_id" \
  --vault-id "$vault_id" \
  --transform id --raw-output)
echo "$session_id"
````

  
````python
research_agent = client.beta.agents.create(
    name="researcher",
    model="claude-haiku-4-5",
    mcp_servers=[
        {"type": "url", "name": "github", "url": "https://api.githubcopilot.com/mcp/"},
    ],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "github"}],
)

coordinator = client.beta.agents.create(
    name="coordinator",
    model="claude-opus-4-8",
    tools=[{"type": "agent_toolset_20260401"}],
    multiagent={
        "type": "coordinator",
        "agents": [{"type": "agent", "id": research_agent.id}],
    },
)

session = client.beta.sessions.create(
    agent=coordinator.id,
    environment_id=environment.id,
    vault_ids=[vault.id],
)
print(session.id)
````

  
````typescript
const researchAgent = await client.beta.agents.create({
  name: "researcher",
  model: "claude-haiku-4-5",
  mcp_servers: [
    { type: "url", name: "github", url: "https://api.githubcopilot.com/mcp/" },
  ],
  tools: [{ type: "mcp_toolset", mcp_server_name: "github" }],
});

const coordinator = await client.beta.agents.create({
  name: "coordinator",
  model: "claude-opus-4-8",
  tools: [{ type: "agent_toolset_20260401" }],
  multiagent: {
    type: "coordinator",
    agents: [{ type: "agent", id: researchAgent.id }],
  },
});

const session = await client.beta.sessions.create({
  agent: coordinator.id,
  environment_id: environment.id,
  vault_ids: [vault.id],
});
console.log(session.id);
````

  
````csharp
var researchAgent = await client.Beta.Agents.Create(new()
{
    Name = "researcher",
    Model = BetaManagedAgentsModel.ClaudeHaiku4_5,
    McpServers =
    [
        new()
        {
            Type = BetaManagedAgentsUrlMcpServerParamsType.Url,
            Name = "github",
            Url = "https://api.githubcopilot.com/mcp/",
        },
    ],
    Tools =
    [
        new BetaManagedAgentsMcpToolsetParams
        {
            Type = BetaManagedAgentsMcpToolsetParamsType.McpToolset,
            McpServerName = "github",
        },
    ],
});

var coordinator = await client.Beta.Agents.Create(new()
{
    Name = "coordinator",
    Model = BetaManagedAgentsModel.ClaudeOpus4_8,
    Tools =
    [
        new BetaManagedAgentsAgentToolset20260401Params
        {
            Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
        },
    ],
    Multiagent = new()
    {
        Type = BetaManagedAgentsMultiagentParamsType.Coordinator,
        Agents =
        [
            new BetaManagedAgentsAgentParams
            {
                Type = Anthropic.Models.Beta.Sessions.Type.Agent,
                ID = researchAgent.ID,
            },
        ],
    },
});

var session = await client.Beta.Sessions.Create(new()
{
    Agent = coordinator.ID,
    EnvironmentID = environment.ID,
    VaultIds = [vault.ID],
});
Console.WriteLine(session.ID);
````

  
````go
researcher, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name:  "researcher",
	Model: anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeHaiku4_5},
	MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{{
		Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
		Name: "github",
		URL:  "https://api.githubcopilot.com/mcp/",
	}},
	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
		OfMCPToolset: &anthropic.BetaManagedAgentsMCPToolsetParams{
			Type:          anthropic.BetaManagedAgentsMCPToolsetParamsTypeMCPToolset,
			MCPServerName: "github",
		},
	}},
})
if err != nil {
	panic(err)
}

coordinator, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name:  "coordinator",
	Model: anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus4_8},
	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
		},
	}},
	Multiagent: anthropic.BetaManagedAgentsMultiagentParams{
		Type: anthropic.BetaManagedAgentsMultiagentParamsTypeCoordinator,
		Agents: []anthropic.BetaManagedAgentsMultiagentRosterEntryParamsUnion{{
			OfBetaManagedAgentsAgents: &anthropic.BetaManagedAgentsAgentParams{
				Type: anthropic.BetaManagedAgentsAgentParamsTypeAgent,
				ID:   researcher.ID,
			},
		}},
	},
})
if err != nil {
	panic(err)
}

session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfString: anthropic.String(coordinator.ID),
	},
	EnvironmentID: environment.ID,
	VaultIDs:      []string{vault.ID},
})
if err != nil {
	panic(err)
}
fmt.Println(session.ID)
````

  
````java
var researcher = client.beta().agents().create(
    AgentCreateParams.builder()
        .name("researcher")
        .model(BetaManagedAgentsModel.CLAUDE_HAIKU_4_5)
        .addMcpServer(BetaManagedAgentsUrlMcpServerParams.builder()
            .name("github")
            .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
            .url("https://api.githubcopilot.com/mcp/")
            .build())
        .addTool(BetaManagedAgentsMcpToolsetParams.builder()
            .type(BetaManagedAgentsMcpToolsetParams.Type.MCP_TOOLSET)
            .mcpServerName("github")
            .build())
        .build()
);

var coordinator = client.beta().agents().create(
    AgentCreateParams.builder()
        .name("coordinator")
        .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
        .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
            .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
            .build())
        .multiagent(BetaManagedAgentsMultiagentParams.builder()
            .type(BetaManagedAgentsMultiagentParams.Type.COORDINATOR)
            .addAgent(BetaManagedAgentsAgentParams.builder()
                .type(BetaManagedAgentsAgentParams.Type.AGENT)
                .id(researcher.id())
                .build())
            .build())
        .build()
);

var session = client.beta().sessions().create(SessionCreateParams.builder()
    .agent(coordinator.id())
    .environmentId(environment.id())
    .vaultIds(List.of(vault.id()))
    .build());
IO.println(session.id());
````

  
````php
$researchAgent = $client->beta->agents->create(
    name: 'researcher',
    model: 'claude-haiku-4-5',
    mcpServers: [
        ['type' => 'url', 'name' => 'github', 'url' => 'https://api.githubcopilot.com/mcp/'],
    ],
    tools: [
        ['type' => 'mcp_toolset', 'mcp_server_name' => 'github'],
    ],
);

$coordinator = $client->beta->agents->create(
    name: 'coordinator',
    model: 'claude-opus-4-8',
    tools: [
        ['type' => 'agent_toolset_20260401'],
    ],
    multiagent: [
        'type' => 'coordinator',
        'agents' => [
            ['type' => 'agent', 'id' => $researchAgent->id],
        ],
    ],
);

$session = $client->beta->sessions->create(
    agent: $coordinator->id,
    environmentID: $environment->id,
    vaultIDs: [$vault->id],
);
echo "{$session->id}\n";
````

  
````ruby
research_agent = client.beta.agents.create(
  name: "researcher",
  model: "claude-haiku-4-5",
  mcp_servers: [
    {type: "url", name: "github", url: "https://api.githubcopilot.com/mcp/"}
  ],
  tools: [
    {type: "mcp_toolset", mcp_server_name: "github"}
  ]
)

coordinator = client.beta.agents.create(
  name: "coordinator",
  model: "claude-opus-4-8",
  tools: [
    {type: "agent_toolset_20260401"}
  ],
  multiagent: {
    type: "coordinator",
    agents: [
      {type: "agent", id: research_agent.id}
    ]
  }
)

session = client.beta.sessions.create(
  agent: coordinator.id,
  environment_id: environment.id,
  vault_ids: [vault.id]
)
puts session.id
````

</CodeGroup>

Dalam contoh ini, hanya researcher yang mendeklarasikan server MCP GitHub, sehingga koordinator tidak memiliki akses. `vault_ids` sesi menyediakan kredensial GitHub ke thread milik researcher.

<Tip>
Jika panggilan MCP agen gagal diautentikasi setelah Anda mendeklarasikan server, pastikan `mcp_server_url` kredensial cocok persis dengan `mcp_servers[].url` agen, termasuk skema dan garis miring di akhir.
</Tip>

## Thread \{#threads}

**Aliran event tingkat sesi** (`/v1/sessions/:id/events/stream`) dianggap sebagai **primary thread** (utas utama), yang berisi tampilan ringkas dari semua aktivitas di seluruh thread. Anda tidak melihat aktivitas lengkap dari subagen, tetapi Anda melihat awal dan akhir pekerjaan mereka, serta event yang memblokir seperti permintaan izin alat.

**Session thread** (utas sesi) adalah tempat Anda menelusuri aktivitas agen tertentu secara mendalam.

`status` sesi adalah agregasi dari semua aktivitas agen; jika setidaknya satu thread berstatus `running`, maka status sesi keseluruhan juga `running`.

<Note>
Maksimal 25 thread bersamaan didukung. Koordinator dapat memanggil beberapa salinan dari satu agen dalam daftar, sehingga membuat beberapa thread yang terkait dengan satu `agent`.
</Note>

<Tabs>
  <Tab title="Mencantumkan thread">
Cantumkan semua thread yang terkait dengan sesi sebagai berikut:
<CodeGroup>
  
````bash
curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  | jq -r '.data[] | "[\(.agent.name)] \(.status)"'
````

  
````bash
ant beta:sessions:threads list --session-id "$SESSION_ID"
````

  
````python
for thread in client.beta.sessions.threads.list(session.id):
    print(f"[{thread.agent.name}] {thread.status}")
````

  
````typescript
for await (const thread of client.beta.sessions.threads.list(session.id)) {
  console.log(`[${thread.agent.name}] ${thread.status}`);
}
````

  
````csharp
await foreach (var thread in (await client.Beta.Sessions.Threads.List(session.ID)).Paginate())
{
    Console.WriteLine($"[{thread.Agent.Name}] {thread.Status}");
}
````

  
````go
threads := client.Beta.Sessions.Threads.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionThreadListParams{})
for threads.Next() {
	thread := threads.Current()
	fmt.Printf("[%s] %s\n", thread.Agent.Name, thread.Status)
}
if err := threads.Err(); err != nil {
	panic(err)
}
````

  
````java
for (var thread : client.beta().sessions().threads().list(session.id()).autoPager()) {
    IO.println("[" + thread.agent().name() + "] " + thread.status());
}
````

  
````php
foreach ($client->beta->sessions->threads->list($session->id)->pagingEachItem() as $thread) {
    echo "[{$thread->agent->name}] {$thread->status}\n";
}
````

  
````ruby
client.beta.sessions.threads.list(session.id).auto_paging_each do |thread|
  puts "[#{thread.agent.name}] #{thread.status}"
end
````

</CodeGroup>

Daftar lengkap mencakup primary thread. `parent_thread_id` bernilai null untuk primary thread.
  </Tab>

  <Tab title="Menginterupsi session thread">
Kirim `user.interrupt` dengan `session_thread_id` untuk menghentikan thread tertentu. Menghilangkan `session_thread_id` akan menargetkan primary thread.

<CodeGroup>
  
````bash
curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d "{\"events\": [{\"type\": \"user.interrupt\", \"session_thread_id\": \"$THREAD_ID\"}]}"
````

  
````bash
ant beta:sessions:events send \
  --session-id "$SESSION_ID" \
  --event "{type: user.interrupt, session_thread_id: $THREAD_ID}"
````

  
````python
client.beta.sessions.events.send(
    session.id,
    events=[{"type": "user.interrupt", "session_thread_id": thread.id}],
)
````

  
````typescript
await client.beta.sessions.events.send(session.id, {
  events: [{ type: "user.interrupt", session_thread_id: thread.id }],
});
````

  
````csharp
await client.Beta.Sessions.Events.Send(session.ID, new()
{
    Events =
    [
        new BetaManagedAgentsUserInterruptEventParams
        {
            Type = BetaManagedAgentsUserInterruptEventParamsType.UserInterrupt,
            SessionThreadID = thread.ID,
        },
    ],
});
````

  
````go
if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
		OfUserInterrupt: &anthropic.BetaManagedAgentsUserInterruptEventParams{
			Type:            anthropic.BetaManagedAgentsUserInterruptEventParamsTypeUserInterrupt,
			SessionThreadID: anthropic.String(thread.ID),
		},
	}},
}); err != nil {
	panic(err)
}
````

  
````java
client.beta().sessions().events().send(
    session.id(),
    EventSendParams.builder()
        .addEvent(BetaManagedAgentsUserInterruptEventParams.builder()
            .type(BetaManagedAgentsUserInterruptEventParams.Type.USER_INTERRUPT)
            .sessionThreadId(thread.id())
            .build())
        .build());
````

  
````php
$client->beta->sessions->events->send(
    $session->id,
    events: [
        ['type' => 'user.interrupt', 'session_thread_id' => $thread->id],
    ],
);
````

  
````ruby
client.beta.sessions.events.send_(
  session.id,
  events: [{type: "user.interrupt", session_thread_id: thread.id}]
)
````

</CodeGroup>

Terhadap thread anak yang diblokir pada `requires_action`, interupsi menandai setiap panggilan alat yang tertunda sebagai ditolak dan langsung mengirim ulang `session.thread_status_idle` dengan `stop_reason: end_turn`; model tidak di-sample. Terhadap thread yang sudah berstatus `idle`, interupsi tidak melakukan apa-apa (no-op).
  </Tab>

  <Tab title="Mengarsipkan session thread">
Secara opsional, arsipkan session thread ketika pekerjaannya telah selesai. Ini membebaskan satu thread dari batas 25 thread.

<CodeGroup>
  
````bash
curl -fsS -X POST "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/archive" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:sessions:threads archive \
  --session-id "$SESSION_ID" \
  --thread-id "$THREAD_ID"
````

  
````python
archived = client.beta.sessions.threads.archive(thread.id, session_id=session.id)
print(archived.status, archived.archived_at)
````

  
````typescript
const archived = await client.beta.sessions.threads.archive(thread.id, {
  session_id: session.id,
});
console.log(archived.status, archived.archived_at);
````

  
````csharp
var archived = await client.Beta.Sessions.Threads.Archive(thread.ID, new() { SessionID = session.ID });
Console.WriteLine($"{archived.Status} {archived.ArchivedAt}");
````

  
````go
archived, err := client.Beta.Sessions.Threads.Archive(ctx, thread.ID, anthropic.BetaSessionThreadArchiveParams{
	SessionID: session.ID,
})
if err != nil {
	panic(err)
}
fmt.Println(archived.Status, archived.ArchivedAt)
````

  
````java
var archived = client.beta().sessions().threads().archive(
    thread.id(),
    ThreadArchiveParams.builder()
        .sessionId(session.id())
        .build());
IO.println(archived.status() + " " + archived.archivedAt());
````

  
````php
$archived = $client->beta->sessions->threads->archive($thread->id, sessionID: $session->id);
echo "{$archived->status} {$archived->archivedAt->format(DATE_ATOM)}\n";
````

  
````ruby
archived = client.beta.sessions.threads.archive(thread.id, session_id: session.id)
puts "#{archived.status} #{archived.archived_at}"
````

</CodeGroup>

Pengarsipan hanya berhasil jika thread berstatus `idle`. Jika thread sedang berjalan atau diblokir pada `requires_action`, interupsi terlebih dahulu:

<CodeGroup>
  
````bash
# Interupsi thread tersebut, lalu arsipkan
curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d "{\"events\": [{\"type\": \"user.interrupt\", \"session_thread_id\": \"$THREAD_ID\"}]}"

curl -fsS -X POST "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/archive" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:sessions:events send \
  --session-id "$SESSION_ID" \
  --event "{type: user.interrupt, session_thread_id: $THREAD_ID}"

ant beta:sessions:threads archive \
  --session-id "$SESSION_ID" \
  --thread-id "$THREAD_ID"
````

  
````python
client.beta.sessions.events.send(
    session.id,
    events=[{"type": "user.interrupt", "session_thread_id": thread.id}],
)
archived = client.beta.sessions.threads.archive(thread.id, session_id=session.id)
print(archived.status, archived.archived_at)
````

  
````typescript
await client.beta.sessions.events.send(session.id, {
  events: [{ type: "user.interrupt", session_thread_id: thread.id }],
});
const archived = await client.beta.sessions.threads.archive(thread.id, {
  session_id: session.id,
});
console.log(archived.status, archived.archived_at);
````

  
````csharp
await client.Beta.Sessions.Events.Send(session.ID, new()
{
    Events =
    [
        new BetaManagedAgentsUserInterruptEventParams
        {
            Type = BetaManagedAgentsUserInterruptEventParamsType.UserInterrupt,
            SessionThreadID = thread.ID,
        },
    ],
});
archived = await client.Beta.Sessions.Threads.Archive(thread.ID, new() { SessionID = session.ID });
Console.WriteLine($"{archived.Status} {archived.ArchivedAt}");
````

  
````go
if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
		OfUserInterrupt: &anthropic.BetaManagedAgentsUserInterruptEventParams{
			Type:            anthropic.BetaManagedAgentsUserInterruptEventParamsTypeUserInterrupt,
			SessionThreadID: anthropic.String(thread.ID),
		},
	}},
}); err != nil {
	panic(err)
}

archived, err := client.Beta.Sessions.Threads.Archive(ctx, thread.ID, anthropic.BetaSessionThreadArchiveParams{
	SessionID: session.ID,
})
if err != nil {
	panic(err)
}
fmt.Println(archived.Status, archived.ArchivedAt)
````

  
````java
client.beta().sessions().events().send(
    session.id(),
    EventSendParams.builder()
        .addEvent(BetaManagedAgentsUserInterruptEventParams.builder()
            .type(BetaManagedAgentsUserInterruptEventParams.Type.USER_INTERRUPT)
            .sessionThreadId(thread.id())
            .build())
        .build());

archived = client.beta().sessions().threads().archive(
    thread.id(),
    ThreadArchiveParams.builder()
        .sessionId(session.id())
        .build());
IO.println(archived.status() + " " + archived.archivedAt());
````

  
````php
$client->beta->sessions->events->send(
    $session->id,
    events: [['type' => 'user.interrupt', 'session_thread_id' => $thread->id]],
);
$archived = $client->beta->sessions->threads->archive($thread->id, sessionID: $session->id);
echo "{$archived->status} {$archived->archivedAt->format(DATE_ATOM)}\n";
````

  
````ruby
client.beta.sessions.events.send_(
  session.id,
  events: [{type: "user.interrupt", session_thread_id: thread.id}]
)
archived = client.beta.sessions.threads.archive(thread.id, session_id: session.id)
puts "#{archived.status} #{archived.archived_at}"
````

</CodeGroup>
  </Tab>
</Tabs>

### Event primary thread \{#primary-thread-events}

Event berikut menampilkan aktivitas multiagen pada primary thread di `/v1/sessions/:id/events/stream`.

| Tipe | Deskripsi |
| --- | --- |
| `session.thread_created` | Sebuah thread telah dibuat. Menyertakan `session_thread_id` dan `agent_name`. |
| `session.thread_status_running` | Sebuah thread memulai aktivitas. |
| `session.thread_status_idle` | Agen yang terkait dengan thread sedang menunggu input. Menyertakan `stop_reason` yang menunjukkan mengapa agen berhenti.  |
| `session.thread_status_terminated` | Sebuah thread diarsipkan atau mengalami error terminal. |
| `agent.thread_message_received` | Sebuah agen mengirimkan hasilnya ke koordinator. Menyertakan `from_session_thread_id`, `from_agent_name`, dan `content`. |
| `agent.thread_message_sent` | Koordinator mengirim tindak lanjut ke agen lain. Menyertakan `to_session_thread_id`, `to_agent_name`, dan `content`. |

### Event session thread \{#session-thread-events}
Event penting diproksikan ke primary thread. Namun, Anda mungkin tetap ingin menyelidiki penalaran dan panggilan alat dari agen tertentu. Untuk melakukannya, lakukan streaming atau cantumkan event dari session thread yang terkait.

<Tabs>
  <Tab title="Streaming event session thread">
<CodeGroup>
  
````bash
curl -fsSN "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/stream?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" |
  while IFS= read -r line; do
    [[ $line == data:* ]] || continue
    json=${line#data: }
    case $(jq -r '.type' <<<"$json") in
      agent.message)
        printf '%s' "$(jq -j '.content[] | select(.type == "text") | .text' <<<"$json")"
        ;;
      session.thread_status_idle)
        break
        ;;
    esac
  done
````

  
````bash
ant beta:sessions:threads:events stream \
  --session-id "$SESSION_ID" \
  --thread-id "$THREAD_ID"
````

  
````python
with client.beta.sessions.threads.events.stream(
    thread.id,
    session_id=session.id,
) as stream:
    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(block.text, end="")
            case "session.thread_status_idle":
                break
````

  
````typescript
const stream = await client.beta.sessions.threads.events.stream(thread.id, {
  session_id: session.id,
});

for await (const event of stream) {
  if (event.type === "agent.message") {
    for (const block of event.content) {
      if (block.type === "text") {
        process.stdout.write(block.text);
      }
    }
  } else if (event.type === "session.thread_status_idle") {
    break;
  }
}
````

  
````csharp
await foreach (var evt in client.Beta.Sessions.Threads.Events.StreamStreaming(thread.ID, new() { SessionID = session.ID }))
{
    if (evt.Value is BetaManagedAgentsAgentMessageEvent message)
    {
        foreach (var block in message.Content)
        {
            if (block.Type == "text")
            {
                Console.Write(block.Text);
            }
        }
    }
    else if (evt.Value is BetaManagedAgentsSessionThreadStatusIdleEvent)
    {
        break;
    }
}
````

  
````go
	stream := client.Beta.Sessions.Threads.Events.StreamEvents(ctx, thread.ID, anthropic.BetaSessionThreadEventStreamParams{
		SessionID: session.ID,
	})
	defer stream.Close()

loop:
	for stream.Next() {
		event := stream.Current()
		switch event.Type {
		case "agent.message":
			for _, block := range event.AsAgentMessage().Content {
				if block.Type == "text" {
					fmt.Print(block.Text)
				}
			}
		case "session.thread_status_idle":
			break loop
		}
	}
	if err := stream.Err(); err != nil {
		panic(err)
	}
````

  
````java
try (var streamResponse = client.beta().sessions().threads().events().streamStreaming(
    thread.id(),
    EventStreamParams.builder().sessionId(session.id()).build()
)) {
    for (var event : (Iterable<BetaManagedAgentsStreamSessionThreadEvents>) streamResponse.stream()::iterator) {
        if (event.isAgentMessage()) {
            for (var block : event.asAgentMessage().content()) {
                IO.print(block.text());
            }
        } else if (event.isSessionThreadStatusIdle()) {
            break;
        }
    }
}
````

  
````php
$stream = $client->beta->sessions->threads->events->streamStream(
    $thread->id,
    sessionID: $session->id,
);

foreach ($stream as $event) {
    if ($event->type === 'agent.message') {
        foreach ($event->content as $block) {
            if ($block->type === 'text') {
                echo $block->text;
            }
        }
    } elseif ($event->type === 'session.thread_status_idle') {
        break;
    }
}
````

  
````ruby
client.beta.sessions.threads.events.stream_events(thread.id, session_id: session.id).each do |event|
  case event.type
  when :"agent.message"
    event.content.each do |block|
      print block.text if block.type == :text
    end
  when :"session.thread_status_idle"
    break
  end
end
````

</CodeGroup>
  </Tab>

  <Tab title="Mencantumkan event session thread">
Cantumkan semua event session thread sebelumnya untuk mengambil riwayat lengkap.

<CodeGroup>
  
````bash
curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/events" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
````

  
````bash
ant beta:sessions:threads:events list \
  --session-id "$SESSION_ID" \
  --thread-id "$THREAD_ID"
````

  
````python
for event in client.beta.sessions.threads.events.list(
    thread.id,
    session_id=session.id,
):
    print(f"[{event.type}] {event.processed_at}")
````

  
````typescript
for await (const event of client.beta.sessions.threads.events.list(thread.id, {
  session_id: session.id,
})) {
  console.log(`[${event.type}] ${event.processed_at}`);
}
````

  
````csharp
var page = await client.Beta.Sessions.Threads.Events.List(thread.ID, new() { SessionID = session.ID });
await foreach (var evt in page.Paginate())
{
    Console.WriteLine($"[{evt.Type}] {evt.ProcessedAt}");
}
````

  
````go
pager := client.Beta.Sessions.Threads.Events.ListAutoPaging(ctx, thread.ID, anthropic.BetaSessionThreadEventListParams{
	SessionID: session.ID,
})
for pager.Next() {
	event := pager.Current()
	fmt.Printf("[%s] %s\n", event.Type, event.ProcessedAt)
}
if err := pager.Err(); err != nil {
	panic(err)
}
````

  
````java
for (var event : client.beta().sessions().threads().events().list(
        thread.id(),
        EventListParams.builder().sessionId(session.id()).build()
    ).autoPager()) {
    var json = event._json().orElseThrow().asObject().orElseThrow();
    var type = json.get("type").asStringOrThrow();
    var processedAt = json.containsKey("processed_at")
        ? json.get("processed_at").asStringOrThrow()
        : "pending";
    IO.println("[" + type + "] " + processedAt);
}
````

  
````php
foreach (
    $client->beta->sessions->threads->events->list(
        $thread->id,
        sessionID: $session->id,
    )->pagingEachItem() as $event
) {
    echo "[{$event->type}] {$event->processedAt->format(DATE_RFC3339)}\n";
}
````

  
````ruby
client.beta.sessions.threads.events.list(
  thread.id,
  session_id: session.id
).auto_paging_each do |event|
  puts "[#{event.type}] #{event.processed_at}"
end
````

</CodeGroup>
  </Tab>
</Tabs>

### Izin alat dan alat kustom \{#tool-permissions-and-custom-tools}

Jika subagen membutuhkan sesuatu dari klien Anda, seperti [izin](/docs/id/managed-agents/events-and-streaming#tool-confirmation) untuk menjalankan alat `always_ask`, atau [hasil dari alat kustom](/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls), event tersebut di-cross-post ke **primary thread** dengan `session_thread_id` yang mengidentifikasi session thread asal.

```json
{
  "type": "session.thread_status_idle",
  "id": "sevt_01ABC...",
  "session_thread_id": "sth_01DEF...",
  "agent_name": "code-reviewer",
  "stop_reason": {
    "type": "requires_action",
    "event_ids": ["toolu_01XYZ..."]
  }
}
```

Kirim `user.tool_confirmation` (dengan `tool_use_id`) atau `user.custom_tool_result` (dengan `custom_tool_use_id`); server akan merutekan respons ke thread yang benar secara otomatis.

Contoh berikut memperluas [handler konfirmasi alat](/docs/id/managed-agents/events-and-streaming#tool-confirmation) untuk merutekan balasan. Pola yang sama berlaku untuk `user.custom_tool_result`.

<CodeGroup>
  
````bash
while IFS= read -r event_id; do
  jq -n --arg id "$event_id" \
    '{events: [{type: "user.tool_confirmation", tool_use_id: $id, result: "allow"}]}' |
    curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
      -H "content-type: application/json" \
      -d @-
done < <(jq -r '.stop_reason.event_ids[]' <<<"$data")
````

  
````bash
# Alur kerja ini tidak cocok diterjemahkan menjadi perintah shell sekali jalan.
# Gunakan salah satu contoh SDK dalam grup kode ini sebagai gantinya.
````

  
````python
for event_id in stop.event_ids:
    client.beta.sessions.events.send(
        session.id,
        events=[
            {
                "type": "user.tool_confirmation",
                "tool_use_id": event_id,
                "result": "allow",
            }
        ],
    )
````

  
````typescript
for (const eventId of stop.event_ids) {
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.tool_confirmation",
        tool_use_id: eventId,
        result: "allow",
      },
    ],
  });
}
````

  
````csharp
foreach (var eventId in requiresAction.EventIds)
{
    await client.Beta.Sessions.Events.Send(session.ID, new()
    {
        Events =
        [
            new BetaManagedAgentsUserToolConfirmationEventParams
            {
                Type = BetaManagedAgentsUserToolConfirmationEventParamsType.UserToolConfirmation,
                ToolUseID = eventId,
                Result = BetaManagedAgentsUserToolConfirmationEventParamsResult.Allow,
            },
        ],
    });
}
````

  
````go
for _, eventID := range stopReason.EventIDs {
	params := anthropic.BetaManagedAgentsUserToolConfirmationEventParams{
		Type:      anthropic.BetaManagedAgentsUserToolConfirmationEventParamsTypeUserToolConfirmation,
		ToolUseID: eventID,
		Result:    anthropic.BetaManagedAgentsUserToolConfirmationEventParamsResultAllow,
	}
	if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{OfUserToolConfirmation: &params}},
	}); err != nil {
		panic(err)
	}
}
````

  
````java
for (var eventId : pendingToolUseIds) {
    client.beta().sessions().events().send(
        session.id(),
        EventSendParams.builder()
            .addEvent(BetaManagedAgentsUserToolConfirmationEventParams.builder()
                .toolUseId(eventId)
                .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.ALLOW)
                .build())
            .build()
    );
}
````

  
````php
foreach ($event->stopReason->eventIDs as $eventId) {
    $client->beta->sessions->events->send($session->id, events: [[
        'type' => 'user.tool_confirmation',
        'tool_use_id' => $eventId,
        'result' => 'allow',
    ]]);
}
````

  
````ruby
event_ids.each do |event_id|
  client.beta.sessions.events.send_(session.id, events: [{
    type: "user.tool_confirmation",
    tool_use_id: event_id,
    result: "allow"
  }])
end
````

</CodeGroup>