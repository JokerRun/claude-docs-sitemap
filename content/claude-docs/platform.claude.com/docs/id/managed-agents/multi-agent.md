---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/multi-agent
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 07963699518af0112a4a46a4394befdb363b66f6dbcaae199728782ac4027fa7
---

# Sesi multiagen

Koordinasikan beberapa agen dalam satu sesi.

---

<Tip>
Multiagen adalah fitur Research Preview. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Tip>

Orkestrasi multi-agen memungkinkan satu agen berkoordinasi dengan agen lain untuk menyelesaikan pekerjaan yang kompleks. Agen dapat bekerja secara paralel dengan konteks terisolasi masing-masing, yang membantu meningkatkan kualitas output dan mempercepat waktu penyelesaian.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. Header beta tambahan diperlukan untuk fitur research preview. SDK menetapkan header beta ini secara otomatis.
</Note>

## Cara kerjanya

Semua agen berbagi container dan filesystem yang sama, tetapi setiap agen berjalan dalam **thread** sesinya sendiri, yaitu aliran event yang terisolasi konteksnya dengan riwayat percakapan tersendiri. Koordinator melaporkan aktivitas di **thread utama** (yang sama dengan aliran event tingkat sesi); thread tambahan dibuat saat runtime ketika koordinator memutuskan untuk mendelegasikan.

Thread bersifat persisten: koordinator dapat mengirim tindak lanjut ke agen yang dipanggilnya sebelumnya, dan agen tersebut menyimpan semua informasi dari giliran sebelumnya.

Setiap agen menggunakan konfigurasinya sendiri (model, system prompt, tools, server MCP, dan skill) sebagaimana didefinisikan saat agen tersebut dibuat. Tools dan konteks tidak dibagikan.

### Apa yang perlu didelegasikan

Sesi multiagen bekerja paling baik ketika ada beberapa tugas yang terdefinisi dengan baik dan terspesialisasi dalam tujuan keseluruhan:

- **Tinjauan kode:** Agen peninjau dengan system prompt yang terfokus dan tools hanya-baca.
- **Pembuatan pengujian:** Agen pengujian yang menulis dan menjalankan pengujian tanpa menyentuh kode produksi.
- **Riset:** Agen pencarian dengan tools web yang merangkum temuan kembali ke koordinator.

## Deklarasikan agen yang dapat dipanggil

Saat [mendefinisikan agen Anda](/docs/id/managed-agents/agent-setup), cantumkan ID tambahan dari agen yang diizinkan untuk dipanggil:

<CodeGroup defaultLanguage="CLI">
```bash curl
orchestrator=$(curl -fsS https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "name": "Engineering Lead",
  "model": "claude-sonnet-4-6",
  "system": "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
  "tools": [
    {
      "type": "agent_toolset_20260401"
    }
  ],
  "callable_agents": [
    {"type": "agent", "id": "$REVIEWER_AGENT_ID", "version": $REVIEWER_AGENT_VERSION},
    {"type": "agent", "id": "$TEST_WRITER_AGENT_ID", "version": $TEST_WRITER_AGENT_VERSION}
  ]
}
EOF
)
```

```bash CLI
ant beta:agents create <<YAML
name: Engineering Lead
model: claude-sonnet-4-6
system: You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.
tools:
  - type: agent_toolset_20260401
callable_agents:
  - type: agent
    id: $REVIEWER_AGENT_ID
    version: $REVIEWER_AGENT_VERSION
  - type: agent
    id: $TEST_WRITER_AGENT_ID
    version: $TEST_WRITER_AGENT_VERSION
YAML
```

```python Python
orchestrator = client.beta.agents.create(
    name="Engineering Lead",
    model="claude-sonnet-4-6",
    system="You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    tools=[
        {"type": "agent_toolset_20260401"},
    ],
    callable_agents=[
        {"type": "agent", "id": reviewer_agent.id, "version": reviewer_agent.version},
        {
            "type": "agent",
            "id": test_writer_agent.id,
            "version": test_writer_agent.version,
        },
    ],
)
```

```typescript TypeScript
const orchestrator = await client.beta.agents.create({
  name: "Engineering Lead",
  model: "claude-sonnet-4-6",
  system:
    "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
  tools: [{ type: "agent_toolset_20260401" }],
  callable_agents: [
    { type: "agent", id: reviewerAgent.id, version: reviewerAgent.version },
    { type: "agent", id: testWriterAgent.id, version: testWriterAgent.version }
  ]
});
```

```csharp C#
var orchestrator = await client.Beta.Agents.Create(new()
{
    Name = "Engineering Lead",
    Model = BetaManagedAgentsModel.ClaudeSonnet4_6,
    System = "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    Tools =
    [
        new BetaManagedAgentsAgentToolset20260401Params
        {
            Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
        },
    ],
    CallableAgents =
    [
        new BetaManagedAgentsCallableAgentParams
        {
            Type = BetaManagedAgentsCallableAgentParamsType.Agent,
            ID = reviewerAgent.ID,
            Version = reviewerAgent.Version,
        },
        new BetaManagedAgentsCallableAgentParams
        {
            Type = BetaManagedAgentsCallableAgentParamsType.Agent,
            ID = testWriterAgent.ID,
            Version = testWriterAgent.Version,
        },
    ],
});
```

```go Go
orchestrator, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name:   "Engineering Lead",
	Model:  anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeSonnet4_6},
	System: anthropic.String("You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent."),
	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
		},
	}},
	CallableAgents: []anthropic.BetaManagedAgentsCallableAgentParams{
		{Type: "agent", ID: reviewerAgent.ID, Version: reviewerAgent.Version},
		{Type: "agent", ID: testWriterAgent.ID, Version: testWriterAgent.Version},
	},
})
if err != nil {
	panic(err)
}
```

```java Java
var orchestrator = client.beta().agents().create(
    AgentCreateParams.builder()
        .name("Engineering Lead")
        .model(BetaManagedAgentsModel.CLAUDE_SONNET_4_6)
        .system("You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.")
        .addTool(
            BetaManagedAgentsAgentToolset20260401Params.builder()
                .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                .build()
        )
        .addCallableAgent(
            BetaManagedAgentsAgentParams.builder()
                .type(BetaManagedAgentsAgentParams.Type.AGENT)
                .id(reviewerAgent.id())
                .version(reviewerAgent.version())
                .build()
        )
        .addCallableAgent(
            BetaManagedAgentsAgentParams.builder()
                .type(BetaManagedAgentsAgentParams.Type.AGENT)
                .id(testWriterAgent.id())
                .version(testWriterAgent.version())
                .build()
        )
        .build()
);
```

```php PHP
$orchestrator = $client->beta->agents->create(
    name: 'Engineering Lead',
    model: 'claude-sonnet-4-6',
    system: 'You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.',
    tools: [
        ['type' => 'agent_toolset_20260401'],
    ],
    callableAgents: [
        ['type' => 'agent', 'id' => $reviewerAgent->id, 'version' => $reviewerAgent->version],
        ['type' => 'agent', 'id' => $testWriterAgent->id, 'version' => $testWriterAgent->version],
    ],
);
```

```ruby Ruby
orchestrator = client.beta.agents.create(
  name: "Engineering Lead",
  model: "claude-sonnet-4-6",
  system: "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
  tools: [
    {type: "agent_toolset_20260401"}
  ],
  callable_agents: [
    {type: "agent", id: reviewer_agent.id, version: reviewer_agent.version},
    {type: "agent", id: test_writer_agent.id, version: test_writer_agent.version}
  ]
)
```
</CodeGroup>

Setiap entri dalam `callable_agents` harus berupa ID dari agen yang sudah ada. Hanya satu tingkat delegasi yang didukung: koordinator dapat memanggil agen lain, tetapi agen-agen tersebut tidak dapat memanggil agen milik mereka sendiri.

Kemudian buat sesi yang merujuk ke orkestrator:

<CodeGroup>
```bash curl
session=$(curl -fsS https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{"agent": "'$ORCHESTRATOR_ID'", "environment_id": "'$ENVIRONMENT_ID'"}')
```

```bash CLI
ant beta:sessions create \
  --agent "$ORCHESTRATOR_ID" \
  --environment "$ENVIRONMENT_ID"
```

```python Python
session = client.beta.sessions.create(
    agent=orchestrator.id,
    environment_id=environment.id,
)
```

```typescript TypeScript
const session = await client.beta.sessions.create({
  agent: orchestrator.id,
  environment_id: environment.id
});
```
</CodeGroup>

Agen yang dapat dipanggil diselesaikan dari konfigurasi orkestrator. Anda tidak perlu merujuknya saat pembuatan sesi.

## Thread sesi

**Aliran event tingkat sesi** (`/v1/sessions/:id/stream`) dianggap sebagai **thread utama**, yang berisi tampilan ringkas dari semua aktivitas di semua thread. Anda tidak akan melihat jejak individual agen yang dipanggil, tetapi Anda akan melihat awal dan akhir pekerjaan mereka. **Thread sesi** adalah tempat Anda menelusuri lebih dalam penalaran dan pemanggilan tool agen tertentu.

Status sesi juga merupakan agregasi dari semua aktivitas agen; jika setidaknya satu thread berstatus `running`, maka status sesi keseluruhan juga akan menjadi `running`.

Daftarkan semua thread dalam sesi sebagai berikut:
<CodeGroup>
```bash curl
curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  | jq -r '.data[] | "[\(.agent_name)] \(.status)"'
```

```bash CLI
ant beta:sessions:threads list --session-id "$SESSION_ID"
```

```python Python
for thread in client.beta.sessions.threads.list(session.id):
    print(f"[{thread.agent_name}] {thread.status}")
```

```typescript TypeScript
for await (const thread of client.beta.sessions.threads.list(session.id)) {
  console.log(`[${thread.agent_name}] ${thread.status}`);
}
```

```csharp C#
await foreach (var thread in (await client.Beta.Sessions.Threads.List(session.ID)).Paginate())
{
    Console.WriteLine($"[{thread.AgentName}] {thread.Status}");
}
```

```go Go
threads := client.Beta.Sessions.Threads.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionThreadListParams{})
for threads.Next() {
	thread := threads.Current()
	fmt.Printf("[%s] %s\n", thread.AgentName, thread.Status)
}
if err := threads.Err(); err != nil {
	panic(err)
}
```

```java Java
for (var thread : client.beta().sessions().threads().list(session.id()).autoPager()) {
    IO.println("[" + thread.agentName() + "] " + thread.status());
}
```

```php PHP
foreach ($client->beta->sessions->threads->list($session->id)->pagingEachItem() as $thread) {
    echo "[{$thread->agentName}] {$thread->status}\n";
}
```

```ruby Ruby
client.beta.sessions.threads.list(session.id).auto_paging_each do |thread|
  puts "[#{thread.agent_name}] #{thread.status}"
end
```
</CodeGroup>

Stream event dari thread tertentu:

<CodeGroup>
```bash curl
curl -fsSN "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/stream" \
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
      session.thread_idle)
        break
        ;;
    esac
  done
```

```bash CLI
ant beta:sessions:threads stream \
  --session-id "$SESSION_ID" \
  --thread-id "$THREAD_ID"
```

```python Python
with client.beta.sessions.threads.stream(
    thread.id,
    session_id=session.id,
) as stream:
    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(block.text, end="")
            case "session.thread_idle":
                break
```

```typescript TypeScript
const stream = await client.beta.sessions.threads.stream(thread.id, {
  session_id: session.id
});

for await (const event of stream) {
  if (event.type === "agent.message") {
    for (const block of event.content) {
      if (block.type === "text") {
        process.stdout.write(block.text);
      }
    }
  } else if (event.type === "session.thread_idle") {
    break;
  }
}
```

```csharp C#
await foreach (var evt in client.Beta.Sessions.Threads.Stream(thread.ID, new() { SessionID = session.ID }))
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
    else if (evt.Value is BetaManagedAgentsSessionThreadIdleEvent)
    {
        break;
    }
}
```

```go Go
stream := client.Beta.Sessions.Threads.StreamEvents(ctx, thread.ID, anthropic.BetaSessionThreadStreamParams{
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
	case "session.thread_idle":
		break loop
	}
}
if err := stream.Err(); err != nil {
	panic(err)
}
```

```java Java
try (var streamResponse = client.beta().sessions().threads().streamStreaming(
    thread.id(),
    ThreadStreamParams.builder().sessionId(session.id()).build()
)) {
    for (var event : (Iterable<StreamEvents>) streamResponse.stream()::iterator) {
        if (event.isAgentMessage()) {
            for (var block : event.asAgentMessage().content()) {
                IO.print(block.text());
            }
        } else if (event.isSessionThreadIdle()) {
            break;
        }
    }
}
```

```php PHP
$stream = $client->beta->sessions->threads->stream(
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
    } elseif ($event->type === 'session.thread_idle') {
        break;
    }
}
```

```ruby Ruby
client.beta.sessions.threads.stream(thread.id, session_id: session.id).each do |event|
  case event.type
  when :"agent.message"
    event.content.each do |block|
      print block.text if block.type == :text
    end
  when :"session.thread_idle"
    break
  end
end
```
</CodeGroup>

Daftarkan event masa lalu untuk sebuah thread:

<CodeGroup>
```bash curl
curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/events" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
```

```bash CLI
ant beta:sessions:threads:events list \
  --session-id "$SESSION_ID" \
  --thread-id "$THREAD_ID"
```

```python Python
for event in client.beta.sessions.threads.events.list(
    thread.id,
    session_id=session.id,
):
    print(f"[{event.type}] {event.processed_at}")
```

```typescript TypeScript
for await (const event of client.beta.sessions.threads.events.list(thread.id, {
  session_id: session.id
})) {
  console.log(`[${event.type}] ${event.processed_at}`);
}
```

```csharp C#
var page = await client.Beta.Sessions.Threads.Events.List(thread.ID, new() { SessionID = session.ID });
await foreach (var evt in page.Paginate())
{
    Console.WriteLine($"[{evt.Type}] {evt.ProcessedAt}");
}
```

```go Go
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
```

```java Java
for (var event : client.beta().sessions().threads().events().list(
        thread.id(),
        EventListParams.builder().sessionId(session.id()).build()
    ).autoPager()) {
    IO.println("[" + event.type() + "] " + event.processedAt());
}
```

```php PHP
foreach (
    $client->beta->sessions->threads->events->list(
        $thread->id,
        sessionID: $session->id,
    )->pagingEachItem() as $event
) {
    echo "[{$event->type}] {$event->processedAt->format(DATE_RFC3339)}\n";
}
```

```ruby Ruby
client.beta.sessions.threads.events.list(
  thread.id,
  session_id: session.id
).auto_paging_each do |event|
  puts "[#{event.type}] #{event.processed_at}"
end
```
</CodeGroup>

## Tipe event multiagen

Event-event ini menampilkan aktivitas multiagen pada aliran sesi tingkat atas.

| Tipe | Deskripsi |
| --- | --- |
| `session.thread_created` | Koordinator membuat thread baru. Menyertakan `session_thread_id` dan `model`. |
| `session.thread_idle` | Thread agen menyelesaikan pekerjaan saat ini. |
| `agent.thread_message_sent` | Agen mengirim pesan ke thread lain. Menyertakan `to_thread_id` dan `content`. |
| `agent.thread_message_received` | Agen menerima pesan dari thread lain. Menyertakan `from_thread_id` dan `content`. |

## Izin tool dan tool kustom dalam thread

Ketika thread `callable_agent` membutuhkan sesuatu dari klien Anda ([izin](/docs/id/managed-agents/events-and-streaming#tool-confirmation) untuk menjalankan tool `always_ask`, atau [hasil dari tool kustom](/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls)) permintaan tersebut muncul di **aliran sesi** dengan field `session_thread_id`. Sertakan `session_thread_id` yang sama saat Anda memposting respons agar platform mengarahkannya kembali ke thread yang menunggu.

- **`session_thread_id` ada:** event berasal dari thread subagen. Sertakan kembali dalam balasan Anda.
- **`session_thread_id` tidak ada:** event berasal dari thread utama. Balas tanpa field tersebut.
- Cocokkan `tool_use_id` untuk memasangkan permintaan dengan respons.

Contoh di bawah ini memperluas [penangan konfirmasi tool](/docs/id/managed-agents/events-and-streaming#tool-confirmation) untuk merutekan balasan. Pola yang sama berlaku untuk `user.custom_tool_result`.

<CodeGroup>
```bash curl
while IFS= read -r event_id; do
  pending=$(jq -r --arg id "$event_id" '.[$id]' <<<"$events_by_id")
  thread_id=$(jq -r '.session_thread_id // empty' <<<"$pending")
  jq -n --arg id "$event_id" --arg thread "$thread_id" '
    {events: [
      {type: "user.tool_confirmation", tool_use_id: $id, result: "allow"}
      + (if $thread != "" then {session_thread_id: $thread} else {} end)
    ]}' |
    curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
      -H "content-type: application/json" \
      -d @-
done < <(jq -r '.stop_reason.event_ids[]' <<<"$data")
```

```bash CLI
while IFS= read -r event_id; do
  pending=$(jq -r --arg id "$event_id" '.[$id]' <<<"$events_by_id")
  thread_id=$(jq -r '.session_thread_id // empty' <<<"$pending")
  event="type: user.tool_confirmation, tool_use_id: $event_id, result: allow"
  # Echo session_thread_id when the request came from a subagent thread
  if [[ -n $thread_id ]]; then
    event+=", session_thread_id: $thread_id"
  fi
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" \
    --event "{$event}" \
 </dev/null
done < <(jq -r '.stop_reason.event_ids[]' <<<"$data")
```

```python Python
for event_id in stop.event_ids:
    pending = events_by_id[event_id]
    confirmation = {
        "type": "user.tool_confirmation",
        "tool_use_id": event_id,
        "result": "allow",
    }
    # Echo session_thread_id when the request came from a subagent thread
    if pending.session_thread_id is not None:
        confirmation["session_thread_id"] = pending.session_thread_id
    client.beta.sessions.events.send(session.id, events=[confirmation])
```

```typescript TypeScript
for (const eventId of event.stop_reason.event_ids) {
  const pending = eventsById[eventId];
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.tool_confirmation",
        tool_use_id: eventId,
        result: "allow",
        // Echo session_thread_id when the request came from a subagent thread
        ...(pending.session_thread_id != null && {
          session_thread_id: pending.session_thread_id
        })
      }
    ]
  });
}
```

```csharp C#
foreach (var eventId in requiresAction.EventIds)
{
    var pending = eventsById[eventId];
    await client.Beta.Sessions.Events.Send(session.ID, new()
    {
        Events =
        [
            new BetaManagedAgentsUserToolConfirmationEventParams
            {
                Type = BetaManagedAgentsUserToolConfirmationEventParamsType.UserToolConfirmation,
                ToolUseID = eventId,
                Result = BetaManagedAgentsUserToolConfirmationEventParamsResult.Allow,
                // Echo session_thread_id when the request came from a subagent thread
                SessionThreadID = pending.SessionThreadID,
            },
        ],
    });
}
```

```go Go
for _, eventID := range stopReason.EventIDs {
	pending := eventsByID[eventID]
	params := anthropic.BetaManagedAgentsUserToolConfirmationEventParams{
		Type:      anthropic.BetaManagedAgentsUserToolConfirmationEventParamsTypeUserToolConfirmation,
		ToolUseID: eventID,
		Result:    anthropic.BetaManagedAgentsUserToolConfirmationEventParamsResultAllow,
	}
	// Echo session_thread_id when the request came from a subagent thread
	if pending.SessionThreadID != "" {
		params.SessionThreadID = anthropic.String(pending.SessionThreadID)
	}
	if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
		Events: []anthropic.SendEventsParamsUnion{{OfUserToolConfirmation: &params}},
	}); err != nil {
		panic(err)
	}
}
```

```java Java
for (var eventId : stopReason.asRequiresAction().eventIds()) {
    var pending = eventsById.get(eventId);
    var confirmation = BetaManagedAgentsUserToolConfirmationEventParams.builder()
        .toolUseId(eventId)
        .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.ALLOW);
    // Echo session_thread_id when the request came from a subagent thread
    pending.sessionThreadId().ifPresent(confirmation::sessionThreadId);
    client.beta().sessions().events().send(
        session.id(),
        EventSendParams.builder().addEvent(confirmation.build()).build()
    );
}
```

```php PHP
foreach ($event->stopReason->eventIDs as $eventId) {
    $pending = $eventsById[$eventId];
    $confirmation = [
        'type' => 'user.tool_confirmation',
        'tool_use_id' => $eventId,
        'result' => 'allow',
    ];
    // Echo session_thread_id when the request came from a subagent thread
    if ($pending->sessionThreadID !== null) {
        $confirmation['session_thread_id'] = $pending->sessionThreadID;
    }
    $client->beta->sessions->events->send($session->id, events: [$confirmation]);
}
```

```ruby Ruby
event_ids.each do |event_id|
  pending = events_by_id[event_id]
  confirmation = {
    type: "user.tool_confirmation",
    tool_use_id: event_id,
    result: "allow"
  }
  # Echo session_thread_id when the request came from a subagent thread
  confirmation[:session_thread_id] = pending.session_thread_id if pending.session_thread_id
  client.beta.sessions.events.send_(session.id, events: [confirmation])
end
```
</CodeGroup>