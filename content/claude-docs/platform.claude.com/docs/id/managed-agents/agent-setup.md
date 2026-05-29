---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/agent-setup
fetched_at: 2026-05-29T03:17:00.216417Z
sha256: 21a89da7a71e4d65884530619292c4f98fb083458747ac83c0925d38e2c0ad86
---

# Tentukan agen Anda

Buat konfigurasi agen yang dapat digunakan kembali dan memiliki versi.

---

Agen adalah konfigurasi yang dapat digunakan kembali dan memiliki versi yang mendefinisikan persona dan kemampuan. Agen menggabungkan model, system prompt, tools, server MCP, dan skills yang membentuk cara Claude berperilaku selama sesi.

Buat agen sekali sebagai sumber daya yang dapat digunakan kembali dan referensikan berdasarkan ID setiap kali Anda [memulai sesi](/docs/id/managed-agents/sessions). Agen memiliki versi dan lebih mudah dikelola di banyak sesi.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK mengatur header beta secara otomatis.
</Note>

## Bidang konfigurasi agen

| Bidang | Deskripsi |
| --- | --- |
| `name` | Diperlukan. Nama yang dapat dibaca manusia untuk agen. |
| `model` | Diperlukan. Claude [model](/docs/id/about-claude/models/overview) yang menggerakkan agen. Semua model Claude 4.5 dan yang lebih baru didukung. |
| `system` | [System prompt](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role) yang mendefinisikan perilaku dan persona agen. System prompt berbeda dari [pesan pengguna](/docs/id/managed-agents/events-and-streaming#user-events), yang harus mendeskripsikan pekerjaan yang akan dilakukan. |
| `tools` | Tools yang tersedia untuk agen. Menggabungkan [pre-built agent tools](/docs/id/managed-agents/tools), [MCP tools](/docs/id/managed-agents/mcp-connector), dan [custom tools](/docs/id/managed-agents/tools#custom-tools). |
| `mcp_servers` | Server MCP yang menyediakan kemampuan pihak ketiga yang terstandar. |
| `skills` | [Skills](/docs/id/managed-agents/skills) yang menyediakan konteks khusus domain dengan pengungkapan progresif. |
| `callable_agents` | Agen lain yang dapat dipanggil agen ini untuk [orkestrasi multi-agen](/docs/id/managed-agents/multi-agent). Ini adalah fitur pratinjau penelitian; [minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.|
| `description` | Deskripsi tentang apa yang dilakukan agen. |
| `metadata` | Pasangan kunci-nilai arbitrer untuk pelacakan Anda sendiri. |

## Buat agen

Contoh berikut mendefinisikan agen pengkodean yang menggunakan Claude Opus 4.7 dengan akses ke toolset agen pre-built. Toolset memungkinkan agen menulis kode, membaca file, mencari web, dan banyak lagi. Lihat [referensi agent tools](/docs/id/managed-agents/tools) untuk daftar lengkap tools yang didukung.

<CodeGroup defaultLanguage="CLI">
  
````bash
agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{
    "name": "Coding Assistant",
    "model": "claude-opus-4-8",
    "system": "You are a helpful coding agent.",
    "tools": [{"type": "agent_toolset_20260401"}]
  }')

AGENT_ID=$(jq -r '.id' <<< "$agent")
AGENT_VERSION=$(jq -r '.version' <<< "$agent")
````

  
````bash
ant beta:agents create \
  --name "Coding Assistant" \
  --model '{id: claude-opus-4-8}' \
  --system "You are a helpful coding agent." \
  --tool '{type: agent_toolset_20260401}'
````

  
````python
agent = client.beta.agents.create(
    name="Coding Assistant",
    model="claude-opus-4-8",
    system="You are a helpful coding agent.",
    tools=[
        {"type": "agent_toolset_20260401"},
    ],
)
````

  
````typescript
const agent = await client.beta.agents.create({
  name: "Coding Assistant",
  model: "claude-opus-4-8",
  system: "You are a helpful coding agent.",
  tools: [{ type: "agent_toolset_20260401" }],
});
````

  
````csharp
var agent = await client.Beta.Agents.Create(new()
{
    Name = "Coding Assistant",
    Model = new("claude-opus-4-8"),
    System = "You are a helpful coding agent.",
    Tools =
    [
        new BetaManagedAgentsAgentToolset20260401Params
        {
            Type = "agent_toolset_20260401",
        },
    ],
});
````

  
````go
agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name: "Coding Assistant",
	Model: anthropic.BetaManagedAgentsModelConfigParams{
		ID: "claude-opus-4-8",
	},
	System: anthropic.String("You are a helpful coding agent."),
	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
		},
	}},
})
if err != nil {
	panic(err)
}
````

  
````java
var agent = client.beta().agents().create(
    AgentCreateParams.builder()
        .name("Coding Assistant")
        .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
        .system("You are a helpful coding agent.")
        .addTool(
            BetaManagedAgentsAgentToolset20260401Params.builder()
                .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                .build()
        )
        .build()
);
````

  
````php
$agent = $client->beta->agents->create(
    name: 'Coding Assistant',
    model: 'claude-opus-4-8',
    system: 'You are a helpful coding agent.',
    tools: [
        BetaManagedAgentsAgentToolset20260401Params::with(
            type: 'agent_toolset_20260401',
        ),
    ],
);
````

  
````ruby
agent = client.beta.agents.create(
  name: "Coding Assistant",
  model: "claude-opus-4-8",
  system_: "You are a helpful coding agent.",
  tools: [{type: "agent_toolset_20260401"}]
)
````

</CodeGroup>

<Tip>
Untuk menggunakan Claude Opus 4.6 dengan [fast mode](/docs/id/build-with-claude/fast-mode), teruskan `model` sebagai objek: `{"id": "claude-opus-4-6", "speed": "fast"}`.
</Tip>

Respons mengulangi konfigurasi Anda dan menambahkan bidang `id`, `version`, `created_at`, `updated_at`, dan `archived_at`. `version` dimulai dari 1 dan bertambah setiap kali Anda memperbarui agen.

```json
{
  "id": "agent_01HqR2k7vXbZ9mNpL3wYcT8f",
  "type": "agent",
  "name": "Coding Assistant",
  "model": {
    "id": "claude-opus-4-7",
    "speed": "standard"
  },
  "system": "You are a helpful coding agent.",
  "description": null,
  "tools": [
    {
      "type": "agent_toolset_20260401",
      "default_config": {
        "permission_policy": { "type": "always_allow" }
      }
    }
  ],
  "skills": [],
  "mcp_servers": [],
  "metadata": {},
  "version": 1,
  "created_at": "2026-04-03T18:24:10.412Z",
  "updated_at": "2026-04-03T18:24:10.412Z",
  "archived_at": null
}
```

## Perbarui agen

Memperbarui agen menghasilkan versi baru. Teruskan `version` saat ini untuk memastikan Anda memperbarui dari status yang diketahui.

<CodeGroup defaultLanguage="CLI">
  
````bash
updated_agent=$(curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "version": $AGENT_VERSION,
  "system": "You are a helpful coding agent. Always write tests."
}
EOF
)

echo "New version: $(jq -r '.version' <<< "$updated_agent")"
````

  
````bash
ant beta:agents update \
  --agent-id "$AGENT_ID" \
  --version "$AGENT_VERSION" \
  --system "You are a helpful coding agent. Always write tests."
````

  
````python
updated_agent = client.beta.agents.update(
    agent.id,
    version=agent.version,
    system="You are a helpful coding agent. Always write tests.",
)

print(f"New version: {updated_agent.version}")
````

  
````typescript
const updatedAgent = await client.beta.agents.update(agent.id, {
  version: agent.version,
  system: "You are a helpful coding agent. Always write tests.",
});

console.log(`New version: ${updatedAgent.version}`);
````

  
````csharp
var updatedAgent = await client.Beta.Agents.Update(agent.ID, new()
{
    Version = agent.Version,
    System = "You are a helpful coding agent. Always write tests.",
});

Console.WriteLine($"New version: {updatedAgent.Version}");
````

  
````go
updatedAgent, err := client.Beta.Agents.Update(ctx, agent.ID, anthropic.BetaAgentUpdateParams{
	Version: agent.Version,
	System:  anthropic.String("You are a helpful coding agent. Always write tests."),
})
if err != nil {
	panic(err)
}

fmt.Printf("New version: %d\n", updatedAgent.Version)
````

  
````java
var updatedAgent = client.beta().agents().update(
    agent.id(),
    AgentUpdateParams.builder()
        .version(agent.version())
        .system("You are a helpful coding agent. Always write tests.")
        .build()
);

IO.println("New version: " + updatedAgent.version());
````

  
````php
$updatedAgent = $client->beta->agents->update(
    $agent->id,
    version: $agent->version,
    system: 'You are a helpful coding agent. Always write tests.',
);

echo "New version: {$updatedAgent->version}\n";
````

  
````ruby
updated_agent = client.beta.agents.update(
  agent.id,
  version: agent.version,
  system_: "You are a helpful coding agent. Always write tests."
)

puts "New version: #{updated_agent.version}"
````

</CodeGroup>

### Semantik pembaruan

- **Bidang yang dihilangkan dipertahankan.** Anda hanya perlu menyertakan bidang yang ingin Anda ubah.

- **Bidang skalar** (`model`, `system`, `name`, dll.) diganti dengan nilai baru. `system` dan `description` dapat dihapus dengan melewatkan `null`. `model` dan `name` wajib dan tidak dapat dihapus.

- **Bidang array** (`tools`, `mcp_servers`, `skills`, `callable_agents`) sepenuhnya diganti oleh array baru. Untuk menghapus bidang array sepenuhnya, teruskan `null` atau array kosong.

- **Metadata** digabungkan di tingkat kunci. Kunci yang Anda berikan ditambahkan atau diperbarui. Kunci yang Anda hilangkan dipertahankan. Untuk menghapus kunci tertentu, atur nilainya ke string kosong.

- **Deteksi no-op.** Jika pembaruan tidak menghasilkan perubahan relatif terhadap versi saat ini, versi baru tidak dibuat dan versi yang ada dikembalikan.

## Siklus hidup agen

| Operasi | Perilaku |
| --- | --- |
| **Perbarui** | Menghasilkan versi agen baru. |
| **Daftar versi** | Ambil riwayat versi lengkap untuk melacak perubahan seiring waktu. |
| **Arsipkan** | Agen menjadi read-only. Sesi baru tidak dapat mereferensikannya, tetapi sesi yang ada terus berjalan. |

### Daftar versi

Ambil riwayat versi lengkap untuk melacak bagaimana agen telah berubah seiring waktu.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID/versions" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  | jq -r '.data[] | "Version \(.version): \(.updated_at)"'
````

  
````bash
ant beta:agents:versions list --agent-id "$AGENT_ID"
````

  
````python
for version in client.beta.agents.versions.list(agent.id):
    print(f"Version {version.version}: {version.updated_at.isoformat()}")
````

  
````typescript
for await (const version of client.beta.agents.versions.list(agent.id)) {
  console.log(`Version ${version.version}: ${version.updated_at}`);
}
````

  
````csharp
var versions = await client.Beta.Agents.Versions.List(agent.ID);
await foreach (var version in versions.Paginate())
{
    Console.WriteLine($"Version {version.Version}: {version.UpdatedAt:O}");
}
````

  
````go
iter := client.Beta.Agents.Versions.ListAutoPaging(ctx, agent.ID, anthropic.BetaAgentVersionListParams{})
for iter.Next() {
	version := iter.Current()
	fmt.Printf("Version %d: %s\n", version.Version, version.UpdatedAt.Format(time.RFC3339))
}
if err := iter.Err(); err != nil {
	panic(err)
}
````

  
````java
for (var version : client.beta().agents().versions().list(agent.id()).autoPager()) {
    IO.println("Version " + version.version() + ": " + version.updatedAt());
}
````

  
````php
foreach ($client->beta->agents->versions->list($agent->id)->pagingEachItem() as $version) {
    echo "Version {$version->version}: {$version->updatedAt->format(DateTimeInterface::ATOM)}\n";
}
````

  
````ruby
client.beta.agents.versions.list(agent.id).auto_paging_each do
  puts "Version #{it.version}: #{it.updated_at.iso8601}"
end
````

</CodeGroup>

### Arsipkan agen

Pengarsipan membuat agen read-only. Sesi yang ada terus berjalan, tetapi sesi baru tidak dapat mereferensikan agen. Respons mengatur `archived_at` ke stempel waktu arsip.

<CodeGroup defaultLanguage="CLI">
  
````bash
archived=$(curl -fsSL -X POST "https://api.anthropic.com/v1/agents/$AGENT_ID/archive" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01")

echo "Archived at: $(jq -r '.archived_at' <<< "$archived")"
````

  
````bash
ant beta:agents archive --agent-id "$AGENT_ID"
````

  
````python
archived = client.beta.agents.archive(agent.id)

print(f"Archived at: {archived.archived_at.isoformat()}")
````

  
````typescript
const archived = await client.beta.agents.archive(agent.id);
console.log(`Archived at: ${archived.archived_at}`);
````

  
````csharp
var archived = await client.Beta.Agents.Archive(agent.ID);
Console.WriteLine($"Archived at: {archived.ArchivedAt:O}");
````

  
````go
archived, err := client.Beta.Agents.Archive(ctx, agent.ID, anthropic.BetaAgentArchiveParams{})
if err != nil {
	panic(err)
}
fmt.Printf("Archived at: %s\n", archived.ArchivedAt.Format(time.RFC3339))
````

  
````java
var archived = client.beta().agents().archive(agent.id());
IO.println("Archived at: " + archived.archivedAt().orElseThrow());
````

  
````php
$archived = $client->beta->agents->archive($agent->id);

echo "Archived at: {$archived->archivedAt->format(DateTimeInterface::ATOM)}\n";
````

  
````ruby
archived = client.beta.agents.archive(agent.id)
puts "Archived at: #{archived.archived_at.iso8601}"
````

</CodeGroup>

## Langkah berikutnya

- [Konfigurasi tools](/docs/id/managed-agents/tools) untuk menyesuaikan kemampuan mana yang dapat digunakan agen.
- [Lampirkan skills](/docs/id/managed-agents/skills) untuk keahlian khusus domain.
- [Mulai sesi](/docs/id/managed-agents/sessions) yang mereferensikan agen Anda.