---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/sessions
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 9cda4c2e3ee4730ea7403dfab9c8ede09b882bd578d4c3f2f9def1eaa3d3f9a4
---

# Memulai sesi

Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.

---

Sesi adalah instans agen di dalam sebuah lingkungan. Setiap sesi mereferensikan sebuah [agen](/docs/id/managed-agents/agent-setup) dan sebuah [lingkungan](/docs/id/managed-agents/environments) (keduanya dibuat secara terpisah), serta mempertahankan riwayat percakapan di sepanjang beberapa interaksi. Sesi mengikuti siklus hidup dua langkah: pertama [buat sesi](#creating-a-session) untuk menyediakan sandbox-nya, lalu [kirim user event](#starting-the-session) untuk memulai pekerjaan.

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Membuat sesi \{#creating-a-session}

Sebuah sesi memerlukan ID `agent` dan ID `environment`. Agen adalah sumber daya yang memiliki versi; meneruskan ID `agent` sebagai string akan memulai sesi dengan versi agen terbaru.

<CodeGroup defaultLanguage="CLI">
  
````bash
session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "agent": "$AGENT_ID",
  "environment_id": "$ENVIRONMENT_ID"
}
EOF
)
SESSION_ID=$(jq -r '.id' <<< "$session")
````

  
````bash
ant beta:sessions create \
  --agent "$AGENT_ID" \
  --environment-id "$ENVIRONMENT_ID"
````

  
````python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
)
````

  
````typescript
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id
});
````

  
````csharp
var session = await client.Beta.Sessions.Create(new()
{
    Agent = agent.ID,
    EnvironmentID = environment.ID,
});
````

  
````go
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfString: anthropic.String(agent.ID),
	},
	EnvironmentID: environment.ID,
})
if err != nil {
	panic(err)
}
````

  
````java
var session = client.beta().sessions().create(SessionCreateParams.builder()
    .agent(agent.id())
    .environmentId(environment.id())
    .build());
````

  
````php
$session = $client->beta->sessions->create(
    agent: $agent->id,
    environmentID: $environment->id,
);
````

  
````ruby
session = client.beta.sessions.create(
  agent: agent.id,
  environment_id: environment.id
)
````

</CodeGroup>

Untuk menyematkan sesi ke versi agen tertentu, teruskan sebuah objek. Ini memungkinkan Anda mengontrol secara tepat versi mana yang dijalankan dan mengatur peluncuran versi baru secara independen.

<CodeGroup defaultLanguage="CLI">
  
````bash
pinned_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "agent": {"type": "agent", "id": "$AGENT_ID", "version": 1},
  "environment_id": "$ENVIRONMENT_ID"
}
EOF
)
PINNED_SESSION_ID=$(jq -r '.id' <<< "$pinned_session")
````

  
````bash
ant beta:sessions create <<YAML
agent:
  type: agent
  id: $AGENT_ID
  version: 1
environment_id: $ENVIRONMENT_ID
YAML
````

  
````python
pinned_session = client.beta.sessions.create(
    agent={"type": "agent", "id": agent.id, "version": 1},
    environment_id=environment.id,
)
````

  
````typescript
const pinnedSession = await client.beta.sessions.create({
  agent: { type: "agent", id: agent.id, version: 1 },
  environment_id: environment.id
});
````

  
````csharp
var pinnedSession = await client.Beta.Sessions.Create(new()
{
    Agent = new BetaManagedAgentsAgentParams
    {
        Type = Anthropic.Models.Beta.Sessions.Type.Agent,
        ID = agent.ID,
        Version = 1,
    },
    EnvironmentID = environment.ID,
});
````

  
````go
pinnedSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfBetaManagedAgentsAgents: &anthropic.BetaManagedAgentsAgentParams{
			Type:    anthropic.BetaManagedAgentsAgentParamsTypeAgent,
			ID:      agent.ID,
			Version: anthropic.Int(1),
		},
	},
	EnvironmentID: environment.ID,
})
if err != nil {
	panic(err)
}
````

  
````java
var pinnedSession = client.beta().sessions().create(SessionCreateParams.builder()
    .agent(BetaManagedAgentsAgentParams.builder()
        .type(BetaManagedAgentsAgentParams.Type.AGENT)
        .id(agent.id())
        .version(1)
        .build())
    .environmentId(environment.id())
    .build());
````

  
````php
$pinnedSession = $client->beta->sessions->create(
    agent: ['type' => 'agent', 'id' => $agent->id, 'version' => 1],
    environmentID: $environment->id,
);
````

  
````ruby
pinned_session = client.beta.sessions.create(
  agent: {type: :agent, id: agent.id, version: 1},
  environment_id: environment.id
)
````

</CodeGroup>

<Tip>
Agen mendefinisikan bagaimana Claude berperilaku di dalam sesi, termasuk model, prompt sistem, alat, dan server MCP. Lihat [Mendefinisikan agen Anda](/docs/id/managed-agents/agent-setup) untuk detailnya.
</Tip>

## Autentikasi MCP melalui vault \{#mcp-authentication-through-vaults}

Jika agen Anda menggunakan alat MCP yang memerlukan autentikasi, teruskan `vault_ids` saat pembuatan sesi untuk mereferensikan vault yang berisi kredensial OAuth yang tersimpan. Anthropic mengelola penyegaran token atas nama Anda. Lihat [Autentikasi dengan vault](/docs/id/managed-agents/vaults) untuk cara membuat vault dan mendaftarkan kredensial.

<CodeGroup defaultLanguage="CLI">
  
````bash
vault_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "agent": "$AGENT_ID",
  "environment_id": "$ENVIRONMENT_ID",
  "vault_ids": ["$VAULT_ID"]
}
EOF
)
VAULT_SESSION_ID=$(jq -r '.id' <<< "$vault_session")
````

  
````bash
ant beta:sessions create <<YAML
agent: $AGENT_ID
environment_id: $ENVIRONMENT_ID
vault_ids:
  - $VAULT_ID
YAML
````

  
````python
vault_session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    vault_ids=[vault.id],
)
````

  
````typescript
const vaultSession = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  vault_ids: [vault.id]
});
````

  
````csharp
var vaultSession = await client.Beta.Sessions.Create(new()
{
    Agent = agent.ID,
    EnvironmentID = environment.ID,
    VaultIds = [vault.ID],
});
````

  
````go
vaultSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfString: anthropic.String(agent.ID),
	},
	EnvironmentID: environment.ID,
	VaultIDs:      []string{vault.ID},
})
if err != nil {
	panic(err)
}
````

  
````java
var vaultSession = client.beta().sessions().create(SessionCreateParams.builder()
    .agent(agent.id())
    .environmentId(environment.id())
    .addVaultId(vault.id())
    .build());
````

  
````php
$vaultSession = $client->beta->sessions->create(
    agent: $agent->id,
    environmentID: $environment->id,
    vaultIDs: [$vault->id],
);
````

  
````ruby
vault_session = client.beta.sessions.create(
  agent: agent.id,
  environment_id: environment.id,
  vault_ids: [vault.id]
)
````

</CodeGroup>

## Memulai sesi \{#starting-the-session}

Membuat sesi akan menyediakan sandbox lingkungan tetapi tidak memulai pekerjaan apa pun. Untuk mendelegasikan tugas, kirim event ke sesi menggunakan [user event](/docs/id/managed-agents/reference#event-types). Sesi bertindak sebagai "state machine" (mesin status) yang melacak progres sementara event menggerakkan eksekusi sebenarnya.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<'EOF'
{
  "events": [
    {
      "type": "user.message",
      "content": [{"type": "text", "text": "List the files in the working directory."}]
    }
  ]
}
EOF
````

  
````bash
ant beta:sessions:events send \
  --session-id "$SESSION_ID" <<'YAML'
events:
  - type: user.message
    content:
      - type: text
        text: List the files in the working directory.
YAML
````

  
````python
client.beta.sessions.events.send(
    session.id,
    events=[
        {
            "type": "user.message",
            "content": [
                {"type": "text", "text": "List the files in the working directory."}
            ],
        },
    ],
)
````

  
````typescript
await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.message",
      content: [{ type: "text", text: "List the files in the working directory." }]
    }
  ]
});
````

  
````csharp
await client.Beta.Sessions.Events.Send(session.ID, new()
{
    Events =
    [
        new BetaManagedAgentsUserMessageEventParams
        {
            Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
            Content =
            [
                new BetaManagedAgentsTextBlock
                {
                    Type = BetaManagedAgentsTextBlockType.Text,
                    Text = "List the files in the working directory.",
                },
            ],
        },
    ],
});
````

  
````go
if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
		OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
			Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
			Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
				OfText: &anthropic.BetaManagedAgentsTextBlockParam{
					Type: anthropic.BetaManagedAgentsTextBlockTypeText,
					Text: "List the files in the working directory.",
				},
			}},
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
        .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
            .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
            .addTextContent("List the files in the working directory.")
            .build())
        .build());
````

  
````php
$client->beta->sessions->events->send(
    $session->id,
    events: [
        [
            'type' => 'user.message',
            'content' => [['type' => 'text', 'text' => 'List the files in the working directory.']],
        ],
    ],
);
````

  
````ruby
client.beta.sessions.events.send_(
  session.id,
  events: [
    {
      type: :"user.message",
      content: [{type: :text, text: "List the files in the working directory."}]
    }
  ]
)
````

</CodeGroup>

Lihat [Aliran event sesi](/docs/id/managed-agents/events-and-streaming) untuk cara melakukan streaming respons agen dan menangani konfirmasi alat.

Lihat [Status sesi](/docs/id/managed-agents/session-operations#session-statuses) untuk status-status yang dilalui sebuah sesi, dan [Operasi sesi](/docs/id/managed-agents/session-operations) untuk mengambil, membuat daftar, memperbarui, mengarsipkan, dan menghapus sesi.