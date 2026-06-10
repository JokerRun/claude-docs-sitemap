---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/events-and-streaming
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: b7c0d6a4b709587d4bf4df1a8a55d0dd86133fe35c1dfb90e3d460ab54aa85b9
---

# Aliran event sesi

Kirim event, stream respons, dan interupsi atau alihkan sesi Anda di tengah eksekusi.

---

Komunikasi dengan Claude Managed Agents berbasis event. Anda mengirim event pengguna ke agen, dan menerima kembali event agen dan event sesi untuk melacak status.

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Jenis event \{#event-types}

Event mengalir dalam dua arah.
- **Event pengguna** dan **event sistem** adalah yang Anda kirim ke agen: event `user.*` memulai sesi dan mengarahkannya saat berjalan; `system.message` memperbarui prompt sistem agen di antara giliran.
- **Event sesi**, **event span**, dan **event agen** dikirim kepada Anda untuk observabilitas terhadap status sesi dan progres agen Anda.

String jenis event mengikuti konvensi penamaan `{domain}.{action}`. Lihat [Jenis event](/docs/id/managed-agents/reference#event-types) di referensi untuk katalog lengkapnya.

Setiap event menyertakan timestamp `processed_at` yang menunjukkan kapan event tersebut dicatat di sisi server. Jika `processed_at` bernilai null, artinya event telah diantrekan oleh harness dan ditangani setelah event sebelumnya selesai diproses.

## Mengintegrasikan event \{#integrating-events}

<Tabs>
  <Tab title="Mengirim event">

Kirim event `user.message` untuk memulai atau melanjutkan pekerjaan agen:

<CodeGroup>
  
````bash
curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<'EOF'
{
  "events": [
    {
      "type": "user.message",
      "content": [
        {"type": "text", "text": "Analyze the performance of the sort function in utils.py"}
      ]
    }
  ]
}
EOF
````

  
````bash
ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
events:
  - type: user.message
    content:
      - type: text
        text: Analyze the performance of the sort function in utils.py
YAML
````

  
````python
client.beta.sessions.events.send(
    session.id,
    events=[
        {
            "type": "user.message",
            "content": [
                {
                    "type": "text",
                    "text": "Analyze the performance of the sort function in utils.py",
                },
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
      content: [
        {
          type: "text",
          text: "Analyze the performance of the sort function in utils.py",
        },
      ],
    },
  ],
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
                    Text = "Analyze the performance of the sort function in utils.py",
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
					Text: "Analyze the performance of the sort function in utils.py",
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
            .addTextContent("Analyze the performance of the sort function in utils.py")
            .build())
        .build());
````

  
````php
$client->beta->sessions->events->send(
    $session->id,
    events: [
        [
            'type' => 'user.message',
            'content' => [
                [
                    'type' => 'text',
                    'text' => 'Analyze the performance of the sort function in utils.py',
                ],
            ],
        ],
    ],
);
````

  
````ruby
client.beta.sessions.events.send_(
  session.id,
  events: [
    {
      type: "user.message",
      content: [
        {
          type: "text",
          text: "Analyze the performance of the sort function in utils.py"
        }
      ]
    }
  ]
)
````

</CodeGroup>

Kirim event `user.interrupt` untuk menghentikan agen di tengah eksekusi, lalu lanjutkan dengan event `user.message` untuk mengalihkannya:

<CodeGroup>
  
````bash
# Agent is currently analyzing a file...
# Interrupt with a new direction:
curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<'EOF'
{
  "events": [
    {"type": "user.interrupt"},
    {
      "type": "user.message",
      "content": [
        {"type": "text", "text": "Instead, focus on fixing the bug in line 42."}
      ]
    }
  ]
}
EOF
````

  
````bash
# Agent is currently analyzing a file...
# Interrupt with a new direction:
ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
events:
  - type: user.interrupt
  - type: user.message
    content:
      - type: text
        text: Instead, focus on fixing the bug in line 42.
YAML
````

  
````python
# Agent is currently analyzing a file...
# Interrupt with a new direction:
client.beta.sessions.events.send(
    session.id,
    events=[
        {"type": "user.interrupt"},
        {
            "type": "user.message",
            "content": [
                {
                    "type": "text",
                    "text": "Instead, focus on fixing the bug in line 42.",
                },
            ],
        },
    ],
)
````

  
````typescript
// Agent is currently analyzing a file...
// Interrupt with a new direction:
await client.beta.sessions.events.send(session.id, {
  events: [
    { type: "user.interrupt" },
    {
      type: "user.message",
      content: [
        {
          type: "text",
          text: "Instead, focus on fixing the bug in line 42.",
        },
      ],
    },
  ],
});
````

  
````csharp
// Agent is currently analyzing a file...
// Interrupt with a new direction:
await client.Beta.Sessions.Events.Send(session.ID, new()
{
    Events =
    [
        new BetaManagedAgentsUserInterruptEventParams
        {
            Type = BetaManagedAgentsUserInterruptEventParamsType.UserInterrupt,
        },
        new BetaManagedAgentsUserMessageEventParams
        {
            Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
            Content =
            [
                new BetaManagedAgentsTextBlock
                {
                    Type = BetaManagedAgentsTextBlockType.Text,
                    Text = "Instead, focus on fixing the bug in line 42.",
                },
            ],
        },
    ],
});
````

  
````go
// Agent is currently analyzing a file...
// Interrupt with a new direction:
if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.BetaManagedAgentsEventParamsUnion{
		{
			OfUserInterrupt: &anthropic.BetaManagedAgentsUserInterruptEventParams{
				Type: anthropic.BetaManagedAgentsUserInterruptEventParamsTypeUserInterrupt,
			},
		},
		{
			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
						Type: anthropic.BetaManagedAgentsTextBlockTypeText,
						Text: "Instead, focus on fixing the bug in line 42.",
					},
				}},
			},
		},
	},
}); err != nil {
	panic(err)
}
````

  
````java
// Agent is currently analyzing a file...
// Interrupt with a new direction:
client.beta().sessions().events().send(
    session.id(),
    EventSendParams.builder()
        .addEvent(BetaManagedAgentsUserInterruptEventParams.builder()
            .type(BetaManagedAgentsUserInterruptEventParams.Type.USER_INTERRUPT)
            .build())
        .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
            .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
            .addTextContent("Instead, focus on fixing the bug in line 42.")
            .build())
        .build());
````

  
````php
// Agent is currently analyzing a file...
// Interrupt with a new direction:
$client->beta->sessions->events->send(
    $session->id,
    events: [
        ['type' => 'user.interrupt'],
        [
            'type' => 'user.message',
            'content' => [
                [
                    'type' => 'text',
                    'text' => 'Instead, focus on fixing the bug in line 42.',
                ],
            ],
        ],
    ],
);
````

  
````ruby
# Agent is currently analyzing a file...
# Interrupt with a new direction:
client.beta.sessions.events.send_(
  session.id,
  events: [
    {type: "user.interrupt"},
    {
      type: "user.message",
      content: [
        {type: "text", text: "Instead, focus on fixing the bug in line 42."}
      ]
    }
  ]
)
````

</CodeGroup>

Agen mengakui interupsi tersebut dan beralih ke tugas baru.

  </Tab>
  <Tab title="Streaming event">

Lakukan streaming event dari sesi untuk menerima pembaruan real-time saat agen bekerja. Hanya event yang dipancarkan setelah stream dibuka yang akan dikirimkan, jadi buka stream sebelum mengirim event untuk menghindari "race condition" (kondisi balapan).

<CodeGroup>
  
````bash
# Open the stream first, then send the user message
exec {stream}< <(
  curl --fail-with-body -sS -N \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -H "accept: text/event-stream"
)

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- >/dev/null <<'EOF'
{
  "events": [
    {
      "type": "user.message",
      "content": [{"type": "text", "text": "Summarize the repo README"}]
    }
  ]
}
EOF

while IFS= read -r -u "$stream" event_line; do
  [[ $event_line == data:* ]] || continue
  event_json=${event_line#data: }
  case $(jq -r '.type' <<<"$event_json") in
    agent.message)
      jq -j '.content[] | select(.type == "text") | .text' <<<"$event_json"
      ;;
    session.status_idle)
      break
      ;;
    session.error)
      printf '\n[Error: %s]\n' "$(jq -r '.error.message // "unknown"' <<<"$event_json")"
      break
      ;;
  esac
done
exec {stream}<&-
````

  
````bash
# This workflow does not translate well to a one-off shell command.
# Use one of the SDK examples in this code group instead.
````

  
````python
# Open the stream first, then send the user message
with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[
            {
                "type": "user.message",
                "content": [{"type": "text", "text": "Summarize the repo README"}],
            },
        ],
    )

    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(block.text, end="")
            case "session.status_idle":
                break
            case "session.error":
                error_message = event.error.message if event.error else "unknown"
                print(f"\n[Error: {error_message}]")
                break
````

  
````typescript
// Open the stream first, then send the user message
const stream = await client.beta.sessions.events.stream(session.id);
await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.message",
      content: [{ type: "text", text: "Summarize the repo README" }]
    }
  ]
});

for await (const event of stream) {
  if (event.type === "agent.message") {
    for (const block of event.content) {
      if (block.type === "text") {
        process.stdout.write(block.text);
      }
    }
  } else if (event.type === "session.status_idle") {
    break;
  } else if (event.type === "session.error") {
    console.log(`\n[Error: ${event.error?.message ?? "unknown"}]`);
    break;
  }
}
````

  
````csharp
// Open the stream first, then send the user message
using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(session.ID);
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
                    Text = "Summarize the repo README",
                },
            ],
        },
    ],
});

await foreach (var streamEvent in stream.Enumerate())
{
    if (streamEvent.Value is BetaManagedAgentsAgentMessageEvent message)
    {
        foreach (var block in message.Content)
        {
            Console.Write(block.Text);
        }
    }
    else if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent)
    {
        break;
    }
    else if (streamEvent.Value is BetaManagedAgentsSessionErrorEvent error)
    {
        Console.WriteLine($"\n[Error: {error.Error?.Message ?? "unknown"}]");
        break;
    }
}
````

  
````go
	// Open the stream first, then send the user message
	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
	defer stream.Close()

	if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
						Type: anthropic.BetaManagedAgentsTextBlockTypeText,
						Text: "Summarize the repo README",
					},
				}},
			},
		}},
	}); err != nil {
		panic(err)
	}

events:
	for stream.Next() {
		switch event := stream.Current().AsAny().(type) {
		case anthropic.BetaManagedAgentsAgentMessageEvent:
			// concrete-typed list: BetaManagedAgentsTextBlock
			for _, block := range event.Content {
				fmt.Print(block.Text)
			}
		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
			break events
		case anthropic.BetaManagedAgentsSessionErrorEvent:
			fmt.Printf("\n[Error: %s]\n", cmp.Or(event.Error.Message, "unknown"))
			break events
		}
	}
	if err := stream.Err(); err != nil {
		panic(err)
	}
````

  
````java
// Open the stream first, then send the user message
try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
    client.beta().sessions().events().send(
        session.id(),
        EventSendParams.builder()
            .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                .addTextContent("Summarize the repo README")
                .build())
            .build()
    );

    Iterable<BetaManagedAgentsStreamSessionEvents> events = stream.stream()::iterator;
    for (var event : events) {
        if (event.isAgentMessage()) {
            event.asAgentMessage().content().forEach(block -> IO.print(block.text()));
        } else if (event.isSessionStatusIdle()) {
            break;
        } else if (event.isSessionError()) {
            // The `message` field spans all error variants; read it from the raw JSON.
            var errorMessage =
                event.asSessionError().error()._json().orElse(null) instanceof JsonObject json
                    ? json.values().get("message").asStringOrThrow()
                    : "unknown";
            IO.println("\n[Error: " + errorMessage + "]");
            break;
        }
    }
}
````

  
````php
// Open the stream first, then send the user message
$stream = $client->beta->sessions->events->streamStream($session->id);
$client->beta->sessions->events->send(
    $session->id,
    events: [
        [
            'type' => 'user.message',
            'content' => [['type' => 'text', 'text' => 'Summarize the repo README']],
        ],
    ],
);

foreach ($stream as $event) {
    match ($event->type) {
        'agent.message' => array_walk(
            $event->content,
            static fn ($block) => $block->type === 'text' ? print($block->text) : null,
        ),
        'session.error' => printf("\n[Error: %s]", $event->error?->message ?? 'unknown'),
        default => null,
    };
    if ($event->type === 'session.status_idle' || $event->type === 'session.error') {
        break;
    }
}
$stream->close();
````

  
````ruby
# Open the stream first, then send the user message
stream = client.beta.sessions.events.stream_events(session.id)

client.beta.sessions.events.send_(
  session.id,
  events: [{
    type: "user.message",
    content: [{type: "text", text: "Summarize the repo README"}]
  }]
)

stream.each do |event|
  case event.type
  in :"agent.message"
    event.content.each { print it.text }
  in :"session.status_idle"
    break
  in :"session.error"
    puts "\n[Error: #{event.error&.message || "unknown"}]"
    break
  else
    # ignore other event types
  end
end
````

</CodeGroup>

Untuk menyambung kembali ke sesi yang sudah ada tanpa melewatkan event:

1. Buka stream baru.
2. Ambil daftar riwayat event lengkap untuk menginisialisasi kumpulan ID event yang sudah dilihat.
3. Ikuti stream langsung, lewati event apa pun yang sudah dikembalikan oleh daftar riwayat.

<CodeGroup>
  
````bash
exec {stream}< <(
  curl --fail-with-body -sS -N \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -H "accept: text/event-stream"
)

# Stream is open and buffering. List history before tailing live.
declare -A seen_event_ids
while IFS= read -r event_id; do
  seen_event_ids[$event_id]=1
done < <(
  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" | jq -r '.data[].id'
)

# Tail live events, skipping anything already seen
while IFS= read -r -u "$stream" event_line; do
  [[ $event_line == data:* ]] || continue
  event_json=${event_line#data: }
  event_id=$(jq -r '.id' <<<"$event_json")
  [[ -n ${seen_event_ids[$event_id]+seen} ]] && continue
  seen_event_ids[$event_id]=1
  case $(jq -r '.type' <<<"$event_json") in
    agent.message)
      jq -j '.content[] | select(.type == "text") | .text' <<<"$event_json"
      ;;
    session.status_idle)
      break
      ;;
  esac
done
exec {stream}<&-
````

  
````bash
# This workflow does not translate well to a one-off shell command.
# Use one of the SDK examples in this code group instead.
````

  
````python
with client.beta.sessions.events.stream(session.id) as stream:
    # Stream is open and buffering. List history before tailing live.
    history = client.beta.sessions.events.list(session.id)
    seen_event_ids = {past_event.id for past_event in history}

    # Tail live events, skipping anything already seen
    for event in stream:
        if event.id in seen_event_ids:
            continue
        seen_event_ids.add(event.id)
        match event.type:
            case "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(block.text, end="")
            case "session.status_idle":
                break
````

  
````typescript
const seenEventIds = new Set<string>();
const stream = await client.beta.sessions.events.stream(session.id);

// Stream is open and buffering. List history before tailing live.
for await (const event of client.beta.sessions.events.list(session.id)) {
  seenEventIds.add(event.id);
}

// Tail live events, skipping anything already seen
for await (const event of stream) {
  if (seenEventIds.has(event.id)) continue;
  seenEventIds.add(event.id);
  if (event.type === "agent.message") {
    for (const block of event.content) {
      if (block.type === "text") {
        process.stdout.write(block.text);
      }
    }
  } else if (event.type === "session.status_idle") {
    break;
  }
}
````

  
````csharp
using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(session.ID);

// Stream is open and buffering. List history before tailing live.
HashSet<string> seenEventIds = [];
var history = await client.Beta.Sessions.Events.List(session.ID);
await foreach (var pastEvent in history.Paginate())
{
    seenEventIds.Add(pastEvent.ID);
}

// Tail live events, skipping anything already seen
await foreach (var streamEvent in stream.Enumerate())
{
    if (!seenEventIds.Add(streamEvent.ID))
    {
        continue;
    }
    if (streamEvent.Value is BetaManagedAgentsAgentMessageEvent message)
    {
        foreach (var block in message.Content)
        {
            Console.Write(block.Text);
        }
    }
    else if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent)
    {
        break;
    }
}
````

  
````go
	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
	defer stream.Close()

	// Stream is open and buffering. List history before tailing live.
	seenEventIDs := map[string]struct{}{}
	history := client.Beta.Sessions.Events.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionEventListParams{})
	for history.Next() {
		seenEventIDs[history.Current().ID] = struct{}{}
	}
	if err := history.Err(); err != nil {
		panic(err)
	}

	// Tail live events, skipping anything already seen
tail:
	for stream.Next() {
		event := stream.Current()
		if _, seen := seenEventIDs[event.ID]; seen {
			continue
		}
		seenEventIDs[event.ID] = struct{}{}
		switch event := event.AsAny().(type) {
		case anthropic.BetaManagedAgentsAgentMessageEvent:
			// concrete-typed list: BetaManagedAgentsTextBlock
			for _, block := range event.Content {
				fmt.Print(block.Text)
			}
		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
			break tail
		}
	}
	if err := stream.Err(); err != nil {
		panic(err)
	}
````

  
````java
try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
    // Stream is open and buffering. List history before tailing live.
    // Every event variant carries `id`; read it from the raw JSON to dedup across variants.
    var seenEventIds = new HashSet<String>();
    for (var pastEvent : client.beta().sessions().events().list(session.id()).autoPager()) {
        if (pastEvent._json().orElseThrow() instanceof JsonObject json) {
            seenEventIds.add(json.values().get("id").asStringOrThrow());
        }
    }

    // Tail live events; Set.add returns false for already-seen IDs, skipping the replay.
    stream.stream()
        .filter(event -> event._json().orElseThrow() instanceof JsonObject json
            && seenEventIds.add(json.values().get("id").asStringOrThrow()))
        .takeWhile(event -> !event.isSessionStatusIdle())
        .filter(BetaManagedAgentsStreamSessionEvents::isAgentMessage)
        .forEach(event -> event.asAgentMessage().content().forEach(block -> IO.print(block.text())));
}
````

  
````php
$stream = $client->beta->sessions->events->streamStream($session->id);

// Stream is open and buffering. List history before tailing live.
$seenEventIds = [];
foreach ($client->beta->sessions->events->list($session->id)->pagingEachItem() as $event) {
    $seenEventIds[$event->id] = true;
}

// Tail live events, skipping anything already seen
foreach ($stream as $event) {
    if (isset($seenEventIds[$event->id])) {
        continue;
    }
    $seenEventIds[$event->id] = true;
    match ($event->type) {
        'agent.message' => array_walk(
            $event->content,
            static fn ($block) => $block->type === 'text' ? print($block->text) : null,
        ),
        default => null,
    };
    if ($event->type === 'session.status_idle') {
        break;
    }
}
$stream->close();
````

  
````ruby
stream = client.beta.sessions.events.stream_events(session.id)

# Stream is open and buffering. List history before tailing live.
seen_event_ids = Set.new
client.beta.sessions.events.list(session.id).auto_paging_each { seen_event_ids << it.id }

# Tail live events, skipping anything already seen — Set#add? returns nil for duplicates
stream.each do |event|
  next unless seen_event_ids.add?(event.id)
  case event.type
  in :"agent.message"
    event.content.each { print it.text }
  in :"session.status_idle"
    break
  else
    # ignore other event types
  end
end
````

</CodeGroup>

  </Tab>
  <Tab title="Mengambil daftar event sebelumnya">

Ambil riwayat event lengkap untuk sebuah sesi:

<CodeGroup>
  
````bash
curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
````

  
````bash
ant beta:sessions:events list --session-id "$SESSION_ID" \
  --format jsonl --transform '{type,processed_at}'
````

  
````python
events = client.beta.sessions.events.list(session.id)
for event in events.data:
    print(f"[{event.type}] {event.processed_at}")
````

  
````typescript
const events = await client.beta.sessions.events.list(session.id);
for (const event of events.data) {
  console.log(`[${event.type}] ${event.processed_at}`);
}
````

  
````csharp
var events = await client.Beta.Sessions.Events.List(session.ID);
foreach (var sessionEvent in events.Items)
{
    Console.WriteLine($"[{sessionEvent.Json.GetProperty("type").GetString()}] {sessionEvent.ProcessedAt}");
}
````

  
````go
events, err := client.Beta.Sessions.Events.List(ctx, session.ID, anthropic.BetaSessionEventListParams{})
if err != nil {
	panic(err)
}
for _, event := range events.Data {
	fmt.Printf("[%s] %s\n", event.Type, event.ProcessedAt)
}
````

  
````java
var events = client.beta().sessions().events().list(session.id());
for (var event : events.data()) {
    var eventJson = event._json().orElseThrow().convert(JsonNode.class);
    var processedAt = eventJson.path("processed_at");
    IO.println("[" + eventJson.get("type").asText() + "] "
        + (processedAt.isTextual() ? processedAt.asText() : "null"));
}
````

  
````php
$events = $client->beta->sessions->events->list($session->id);
foreach ($events->data as $event) {
    $processedAt = ($event->processedAt ?? null)?->format(DATE_RFC3339) ?? 'null';
    echo "[{$event->type}] {$processedAt}\n";
}
````

  
````ruby
events = client.beta.sessions.events.list(session.id)
events.data.each { puts "[#{it.type}] #{it.processed_at}" }
````

</CodeGroup>

Berikan filter `types` untuk hanya mengembalikan jenis event tertentu:

<CodeGroup>
  
````bash
curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true&types[]=agent.tool_use&types[]=agent.tool_result" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
````

  
````bash
ant beta:sessions:events list --session-id "$SESSION_ID" \
  --type agent.tool_use --type agent.tool_result \
  --format jsonl --transform '{type,processed_at}'
````

  
````python
events = client.beta.sessions.events.list(
    session.id,
    types=["agent.tool_use", "agent.tool_result"],
)
for event in events.data:
    print(f"[{event.type}] {event.processed_at}")
````

  
````typescript
const events = await client.beta.sessions.events.list(session.id, {
  types: ["agent.tool_use", "agent.tool_result"],
});
for (const event of events.data) {
  console.log(`[${event.type}] ${event.processed_at}`);
}
````

  
````csharp
var events = await client.Beta.Sessions.Events.List(session.ID, new()
{
    Types = ["agent.tool_use", "agent.tool_result"],
});
foreach (var sessionEvent in events.Items)
{
    Console.WriteLine($"[{sessionEvent.Json.GetProperty("type").GetString()}] {sessionEvent.ProcessedAt}");
}
````

  
````go
events, err := client.Beta.Sessions.Events.List(ctx, session.ID, anthropic.BetaSessionEventListParams{
	Types: []string{"agent.tool_use", "agent.tool_result"},
})
if err != nil {
	panic(err)
}
for _, event := range events.Data {
	fmt.Printf("[%s] %s\n", event.Type, event.ProcessedAt)
}
````

  
````java
var events = client.beta().sessions().events().list(
    session.id(),
    EventListParams.builder()
        .addType("agent.tool_use")
        .addType("agent.tool_result")
        .build());
for (var event : events.data()) {
    event.agentToolUse().ifPresent(toolUse ->
        IO.println("[" + toolUse.type() + "] " + toolUse.processedAt()));
    event.agentToolResult().ifPresent(toolResult ->
        IO.println("[" + toolResult.type() + "] " + toolResult.processedAt()));
}
````

  
````php
$events = $client->beta->sessions->events->list(
    $session->id,
    types: ['agent.tool_use', 'agent.tool_result'],
);
foreach ($events->data as $event) {
    $processedAt = ($event->processedAt ?? null)?->format(DATE_RFC3339) ?? 'null';
    echo "[{$event->type}] {$processedAt}\n";
}
````

  
````ruby
events = client.beta.sessions.events.list(
  session.id,
  types: ["agent.tool_use", "agent.tool_result"]
)
events.data.each { puts "[#{it.type}] #{it.processed_at}" }
````

</CodeGroup>

  </Tab>
</Tabs>

## Skenario tambahan \{#additional-scenarios}

### Menangani panggilan alat kustom \{#handling-custom-tool-calls}

Ketika agen memanggil [alat kustom](/docs/id/managed-agents/tools#custom-tools):

1. Sesi memancarkan event `agent.custom_tool_use` yang berisi nama alat dan inputnya.
2. Sesi dijeda dengan event `session.status_idle` yang berisi `stop_reason: requires_action`. ID event yang memblokir ada di array `stop_reason.event_ids`.
3. Jalankan alat tersebut di sistem Anda dan kirim event `user.custom_tool_result` untuk masing-masing, dengan meneruskan ID event di parameter `custom_tool_use_id` beserta konten hasilnya.
4. Setelah semua event yang memblokir diselesaikan, sesi bertransisi kembali ke `running`.

<CodeGroup>
  
````bash
exec {stream_fd}< <(curl --fail-with-body -sS -N \
  "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -H "accept: text/event-stream")

while IFS= read -r -u "$stream_fd" line; do
  [[ $line == data:* ]] || continue
  event_json="${line#data: }"
  stop_reason=$(jq -r 'select(.type == "session.status_idle") | .stop_reason.type // empty' <<<"$event_json")
  case "$stop_reason" in
    requires_action)
      while IFS= read -r event_id; do
        # Execute the tool and send the result back
        result=$(call_tool "$event_id")
        jq -n --arg id "$event_id" --arg result "$result" \
          '{events: [{type: "user.custom_tool_result", custom_tool_use_id: $id, content: [{type: "text", text: $result}]}]}' |
          curl --fail-with-body -sS \
            "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            -H "anthropic-beta: managed-agents-2026-04-01" \
            -H "content-type: application/json" \
            -d @-
      done < <(jq -r '.stop_reason.event_ids[]' <<<"$event_json")
      ;;
    end_turn)
      break
      ;;
  esac
done
exec {stream_fd}<&-
````

  
````bash
# This workflow does not translate well to a one-off shell command.
# Use one of the SDK examples in this code group instead.
````

  
````python
with client.beta.sessions.events.stream(session.id) as stream:
    for event in stream:
        if event.type == "session.status_idle" and (stop_reason := event.stop_reason):
            match stop_reason.type:
                case "requires_action":
                    for event_id in stop_reason.event_ids:
                        # Look up the custom tool use event and execute it
                        tool_event = events_by_id[event_id]
                        result = call_tool(tool_event.name, tool_event.input)

                        # Send the result back
                        client.beta.sessions.events.send(
                            session.id,
                            events=[
                                {
                                    "type": "user.custom_tool_result",
                                    "custom_tool_use_id": event_id,
                                    "content": [{"type": "text", "text": result}],
                                },
                            ],
                        )
                case "end_turn":
                    break
````

  
````typescript
const stream = await client.beta.sessions.events.stream(session.id);

for await (const event of stream) {
  if (event.type !== "session.status_idle") continue;
  if (event.stop_reason.type === "end_turn") break;
  if (event.stop_reason.type !== "requires_action") continue;

  for (const eventId of event.stop_reason.event_ids) {
    // Look up the custom tool use event and execute it
    const toolEvent = eventsById.get(eventId);
    if (!toolEvent) continue;
    const result = await callTool(toolEvent.name, toolEvent.input);

    // Send the result back
    await client.beta.sessions.events.send(session.id, {
      events: [
        {
          type: "user.custom_tool_result",
          custom_tool_use_id: eventId,
          content: [{ type: "text", text: result }],
        },
      ],
    });
  }
}
````

  
````csharp
await foreach (var streamEvent in client.Beta.Sessions.Events.StreamStreaming(session.ID))
{
    if (streamEvent.Value is not BetaManagedAgentsSessionStatusIdleEvent idle) continue;

    if (idle.StopReason?.Value is BetaManagedAgentsSessionRequiresAction requiresAction)
    {
        foreach (var eventId in requiresAction.EventIds)
        {
            // Look up the custom tool use event and execute it
            var toolEvent = eventsById[eventId];
            var result = await CallTool(toolEvent.Name, toolEvent.Input);

            // Send the result back
            await client.Beta.Sessions.Events.Send(session.ID, new()
            {
                Events =
                [
                    new BetaManagedAgentsUserCustomToolResultEventParams
                    {
                        Type = BetaManagedAgentsUserCustomToolResultEventParamsType.UserCustomToolResult,
                        CustomToolUseID = eventId,
                        Content =
                        [
                            new BetaManagedAgentsTextBlock
                            {
                                Type = BetaManagedAgentsTextBlockType.Text,
                                Text = result,
                            },
                        ],
                    },
                ],
            });
        }
    }
    else if (idle.StopReason?.Value is BetaManagedAgentsSessionEndTurn)
    {
        break;
    }
}
````

  
````go
	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
	defer stream.Close()

loop:
	for stream.Next() {
		event, ok := stream.Current().AsAny().(anthropic.BetaManagedAgentsSessionStatusIdleEvent)
		if !ok {
			continue
		}
		switch stopReason := event.StopReason.AsAny().(type) {
		case anthropic.BetaManagedAgentsSessionRequiresAction:
			for _, eventID := range stopReason.EventIDs {
				// Look up the custom tool use event and execute it
				toolEvent := eventsByID[eventID]
				result := callTool(toolEvent.Name, toolEvent.Input)
				// Send the result back
				if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
					Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
						OfUserCustomToolResult: &anthropic.BetaManagedAgentsUserCustomToolResultEventParams{
							Type:            anthropic.BetaManagedAgentsUserCustomToolResultEventParamsTypeUserCustomToolResult,
							CustomToolUseID: eventID,
							Content: []anthropic.BetaManagedAgentsUserCustomToolResultEventParamsContentUnion{{
								OfText: &anthropic.BetaManagedAgentsTextBlockParam{
									Type: anthropic.BetaManagedAgentsTextBlockTypeText,
									Text: result,
								},
							}},
						},
					}},
				}); err != nil {
					panic(err)
				}
			}
		case anthropic.BetaManagedAgentsSessionEndTurn:
			break loop
		}
	}
	if err := stream.Err(); err != nil {
		panic(err)
	}
````

  
````java
try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
    stream.stream()
        .filter(BetaManagedAgentsStreamSessionEvents::isSessionStatusIdle)
        .map(idleEvent -> idleEvent.asSessionStatusIdle().stopReason())
        .takeWhile(stopReason -> !stopReason.isEndTurn())
        .filter(stopReason -> stopReason.isRequiresAction())
        .flatMap(stopReason -> stopReason.asRequiresAction().eventIds().stream())
        .forEach(eventId -> {
            // Look up the custom tool use event and execute it
            var toolEvent = eventsById.get(eventId);
            var result = callTool(toolEvent.name(), toolEvent.input());

            // Send the result back
            client.beta().sessions().events().send(
                session.id(),
                EventSendParams.builder()
                    .addEvent(BetaManagedAgentsUserCustomToolResultEventParams.builder()
                        .type(BetaManagedAgentsUserCustomToolResultEventParams.Type.USER_CUSTOM_TOOL_RESULT)
                        .customToolUseId(eventId)
                        .addTextContent(result)
                        .build())
                    .build());
        });
}
````

  
````php
$stream = $client->beta->sessions->events->streamStream($session->id);

foreach ($stream as $event) {
    if ($event->type === 'session.status_idle' && $event->stopReason) {
        if ($event->stopReason->type === 'requires_action') {
            foreach ($event->stopReason->eventIDs as $eventId) {
                // Look up the custom tool use event and execute it
                $toolEvent = $eventsById[$eventId];
                $result = callTool($toolEvent->name, $toolEvent->input);

                // Send the result back
                $client->beta->sessions->events->send(
                    $session->id,
                    events: [
                        [
                            'type' => 'user.custom_tool_result',
                            'custom_tool_use_id' => $eventId,
                            'content' => [['type' => 'text', 'text' => $result]],
                        ],
                    ],
                );
            }
        } elseif ($event->stopReason->type === 'end_turn') {
            break;
        }
    }
}
````

  
````ruby
client.beta.sessions.events.stream_events(session.id).each do |event|
  case event
  in {type: :"session.status_idle", stop_reason: {type: :requires_action, event_ids:}}
    event_ids.each do |event_id|
      # Look up the custom tool use event and execute it
      tool_event = events_by_id[event_id]
      result = call_tool.call(tool_event.name, tool_event.input)
      # Send the result back
      client.beta.sessions.events.send_(
        session.id,
        events: [
          {
            type: "user.custom_tool_result",
            custom_tool_use_id: event_id,
            content: [{type: "text", text: result}]
          }
        ]
      )
    end
  in {type: :"session.status_idle", stop_reason: {type: :end_turn}}
    break
  else
  end
end
````

</CodeGroup>

### Konfirmasi alat \{#tool-confirmation}

Ketika [kebijakan izin](/docs/id/managed-agents/permission-policies) memerlukan konfirmasi sebelum alat dieksekusi:

1. Sesi memancarkan event `agent.tool_use` atau `agent.mcp_tool_use`.
2. Sesi dijeda dengan event `session.status_idle` yang berisi `stop_reason: requires_action`. ID event yang memblokir ada di array `stop_reason.event_ids`.
3. Kirim event `user.tool_confirmation` untuk masing-masing, dengan meneruskan ID event di parameter `tool_use_id`. Atur `result` ke `"allow"` atau `"deny"`. Gunakan `deny_message` untuk menjelaskan penolakan.
4. Setelah semua event yang memblokir diselesaikan, sesi bertransisi kembali ke `running`.

<CodeGroup>
  
````bash
exec {stream_fd}< <(curl --fail-with-body -sS -N \
  "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -H "accept: text/event-stream")

while IFS= read -r -u "$stream_fd" line; do
  [[ $line == data:* ]] || continue
  event_json="${line#data: }"
  stop_reason=$(jq -r 'select(.type == "session.status_idle") | .stop_reason.type // empty' <<<"$event_json")
  case "$stop_reason" in
    requires_action)
      while IFS= read -r event_id; do
        # Approve the pending tool call
        jq -n --arg id "$event_id" \
          '{events: [{type: "user.tool_confirmation", tool_use_id: $id, result: "allow"}]}' |
          curl --fail-with-body -sS \
            "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            -H "anthropic-beta: managed-agents-2026-04-01" \
            -H "content-type: application/json" \
            -d @-
      done < <(jq -r '.stop_reason.event_ids[]' <<<"$event_json")
      ;;
    end_turn)
      break
      ;;
  esac
done
exec {stream_fd}<&-
````

  
````bash
# This workflow does not translate well to a one-off shell command.
# Use one of the SDK examples in this code group instead.
````

  
````python
with client.beta.sessions.events.stream(session.id) as stream:
    for event in stream:
        if event.type == "session.status_idle" and (stop_reason := event.stop_reason):
            match stop_reason.type:
                case "requires_action":
                    for event_id in stop_reason.event_ids:
                        # Approve the pending tool call
                        client.beta.sessions.events.send(
                            session.id,
                            events=[
                                {
                                    "type": "user.tool_confirmation",
                                    "tool_use_id": event_id,
                                    "result": "allow",
                                },
                            ],
                        )
                case "end_turn":
                    break
````

  
````typescript
const stream = await client.beta.sessions.events.stream(session.id);

for await (const event of stream) {
  if (event.type !== "session.status_idle") continue;
  if (event.stop_reason.type === "end_turn") break;
  if (event.stop_reason.type !== "requires_action") continue;

  for (const eventId of event.stop_reason.event_ids) {
    // Approve the pending tool call
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
}
````

  
````csharp
await foreach (var streamEvent in client.Beta.Sessions.Events.StreamStreaming(session.ID))
{
    if (streamEvent.Value is not BetaManagedAgentsSessionStatusIdleEvent idle) continue;

    if (idle.StopReason?.Value is BetaManagedAgentsSessionRequiresAction requiresAction)
    {
        foreach (var eventId in requiresAction.EventIds)
        {
            // Approve the pending tool call
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
    }
    else if (idle.StopReason?.Value is BetaManagedAgentsSessionEndTurn)
    {
        break;
    }
}
````

  
````go
	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
	defer stream.Close()

loop:
	for stream.Next() {
		event, ok := stream.Current().AsAny().(anthropic.BetaManagedAgentsSessionStatusIdleEvent)
		if !ok {
			continue
		}
		switch stopReason := event.StopReason.AsAny().(type) {
		case anthropic.BetaManagedAgentsSessionRequiresAction:
			for _, eventID := range stopReason.EventIDs {
				// Approve the pending tool call
				if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
					Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
						OfUserToolConfirmation: &anthropic.BetaManagedAgentsUserToolConfirmationEventParams{
							Type:      anthropic.BetaManagedAgentsUserToolConfirmationEventParamsTypeUserToolConfirmation,
							ToolUseID: eventID,
							Result:    anthropic.BetaManagedAgentsUserToolConfirmationEventParamsResultAllow,
						},
					}},
				}); err != nil {
					panic(err)
				}
			}
		case anthropic.BetaManagedAgentsSessionEndTurn:
			break loop
		}
	}
	if err := stream.Err(); err != nil {
		panic(err)
	}
````

  
````java
try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
    stream.stream()
        .filter(BetaManagedAgentsStreamSessionEvents::isSessionStatusIdle)
        .map(idleEvent -> idleEvent.asSessionStatusIdle().stopReason())
        .takeWhile(stopReason -> !stopReason.isEndTurn())
        .filter(stopReason -> stopReason.isRequiresAction())
        .flatMap(stopReason -> stopReason.asRequiresAction().eventIds().stream())
        // Approve each pending tool call
        .forEach(toolUseId -> client.beta().sessions().events().send(
            session.id(),
            EventSendParams.builder()
                .addEvent(BetaManagedAgentsUserToolConfirmationEventParams.builder()
                    .type(BetaManagedAgentsUserToolConfirmationEventParams.Type.USER_TOOL_CONFIRMATION)
                    .toolUseId(toolUseId)
                    .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.ALLOW)
                    .build())
                .build()));
}
````

  
````php
$stream = $client->beta->sessions->events->streamStream($session->id);

foreach ($stream as $event) {
    if ($event->type === 'session.status_idle' && $event->stopReason) {
        if ($event->stopReason->type === 'requires_action') {
            foreach ($event->stopReason->eventIDs as $eventId) {
                // Approve the pending tool call
                $client->beta->sessions->events->send(
                    $session->id,
                    events: [
                        [
                            'type' => 'user.tool_confirmation',
                            'tool_use_id' => $eventId,
                            'result' => 'allow',
                        ],
                    ],
                );
            }
        } elseif ($event->stopReason->type === 'end_turn') {
            break;
        }
    }
}
````

  
````ruby
client.beta.sessions.events.stream_events(session.id).each do |event|
  case event
  in {type: :"session.status_idle", stop_reason: {type: :requires_action, event_ids:}}
    event_ids.each do |event_id|
      # Approve the pending tool call
      client.beta.sessions.events.send_(
        session.id,
        events: [
          {type: "user.tool_confirmation", tool_use_id: event_id, result: "allow"}
        ]
      )
    end
  in {type: :"session.status_idle", stop_reason: {type: :end_turn}}
    break
  else
  end
end
````

</CodeGroup>

### Melanjutkan sesi yang idle \{#resuming-an-idle-session}

Sesi tetap ada di antara interaksi. Riwayat percakapan dipertahankan kecuali sesi dihapus secara eksplisit. Ketika sesi menjadi idle, sandbox-nya di-checkpoint, mempertahankan seluruh status sandbox, termasuk filesystem, paket yang terinstal, dan file apa pun yang dibuat agen. Ini memungkinkan Anda melanjutkan dengan bersih setelah periode tidak aktif.

<Note>
Meskipun riwayat sesi dipertahankan hingga dihapus, checkpoint hanya dipertahankan selama 30 hari setelah aktivitas terakhir sesi. Jika alur kerja Anda memerlukan status sandbox lengkap (file, alat yang terinstal, dan sebagainya) untuk bertahan lebih dari 30 hari, kirim event `user.message` secara berkala untuk mengatur ulang timer inaktivitas sebelum checkpoint kedaluwarsa.
</Note>

Untuk melanjutkan sesi, kirim event `user.message` ke sesi tersebut seperti biasa:

<CodeGroup defaultLanguage="CLI">
  
````bash
# In production, pass the stored ID of the session you want to resume.
curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<'EOF'
{
  "events": [
    {
      "type": "user.message",
      "content": [
        {"type": "text", "text": "Now run the tests against the changes you made earlier."}
      ]
    }
  ]
}
EOF
````

  
````bash
# In production, pass the stored ID of the session you want to resume.
ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
events:
  - type: user.message
    content:
      - type: text
        text: Now run the tests against the changes you made earlier.
YAML
````

  
````python
# Resume a previously created session by sending it a new user.message event.
# In production, pass the stored ID of the session you want to resume.
client.beta.sessions.events.send(
    session.id,
    events=[
        {
            "type": "user.message",
            "content": [
                {
                    "type": "text",
                    "text": "Now run the tests against the changes you made earlier.",
                },
            ],
        },
    ],
)
````

  
````typescript
// Resume a previously created session by sending it a new user event.
// In production, pass the stored ID of the session you want to resume.
await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.message",
      content: [
        {
          type: "text",
          text: "Now run the tests against the changes you made earlier.",
        },
      ],
    },
  ],
});
````

  
````csharp
// Resume a previously created session by ID. In production, pass the
// session ID you stored when the session was created.
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
                    Text = "Now run the tests against the changes you made earlier.",
                },
            ],
        },
    ],
});
````

  
````go
// Resume a previously created session by sending it a new user.message
// event. In production, pass the stored ID of the session to resume.
if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
		OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
			Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
			Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
				OfText: &anthropic.BetaManagedAgentsTextBlockParam{
					Type: anthropic.BetaManagedAgentsTextBlockTypeText,
					Text: "Now run the tests against the changes you made earlier.",
				},
			}},
		},
	}},
}); err != nil {
	panic(err)
}
````

  
````java
// Resume a previously created session by ID. In production, pass the
// session ID you stored when the session was created.
client.beta().sessions().events().send(
    session.id(),
    EventSendParams.builder()
        .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
            .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
            .addTextContent("Now run the tests against the changes you made earlier.")
            .build())
        .build());
````

  
````php
// Resume a previously created session by sending it a new user.message event.
// In production, pass the session ID you stored when the session was created.
$client->beta->sessions->events->send(
    $session->id,
    events: [
        [
            'type' => 'user.message',
            'content' => [
                [
                    'type' => 'text',
                    'text' => 'Now run the tests against the changes you made earlier.',
                ],
            ],
        ],
    ],
);
````

  
````ruby
# Resuming a session is just sending the next event to it. In production,
# pass the session ID you stored when the session was created.
client.beta.sessions.events.send_(
  session.id,
  events: [
    {
      type: "user.message",
      content: [
        {type: "text", text: "Now run the tests against the changes you made earlier."}
      ]
    }
  ]
)
````

</CodeGroup>

### Mengirim pesan sistem \{#sending-system-messages}

<Note>
`system.message` saat ini hanya didukung oleh Claude Opus 4.8. Jika ada model yang dikonfigurasi pada agen yang tidak mendukung injeksi sistem di tengah percakapan, event tersebut ditolak dengan error validasi `model_does_not_support_mid_conversation_system`.
</Note>

Kirim event `system.message` untuk memperbarui prompt sistem agen di antara giliran. Tidak seperti field `system` pada definisi agen (yang ditetapkan saat pembuatan sesi), `system.message` memungkinkan Anda mengubah prompt sistem saat sesi berjalan. Gunakan ini ketika agen memerlukan panduan tingkat sistem yang diperbarui di tengah sesi: persona yang berbeda, batasan yang direvisi, atau konteks yang diambil saat runtime yang seharusnya membentuk perilaku model ke depannya.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<'EOF'
{
  "events": [
    {
      "type": "system.message",
      "content": [
        {"type": "text", "text": "The user's current timezone is America/New_York."}
      ]
    }
  ]
}
EOF
````

  
````bash
ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
events:
  - type: system.message
    content:
      - type: text
        text: "The user's current timezone is America/New_York."
YAML
````

  
````python
client.beta.sessions.events.send(
    session.id,
    events=[
        {
            "type": "system.message",
            "content": [
                {
                    "type": "text",
                    "text": "The user's current timezone is America/New_York.",
                },
            ],
        },
    ],
)
````

  
````typescript
await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "system.message",
      content: [
        {
          type: "text",
          text: "The user's current timezone is America/New_York.",
        },
      ],
    },
  ],
});
````

  
````csharp
await client.Beta.Sessions.Events.Send(session.ID, new()
{
    Events =
    [
        new BetaManagedAgentsSystemMessageEventParams
        {
            Type = BetaManagedAgentsSystemMessageEventParamsType.SystemMessage,
            Content =
            [
                new BetaManagedAgentsSystemContentBlock
                {
                    Type = BetaManagedAgentsSystemContentBlockType.Text,
                    Text = "The user's current timezone is America/New_York.",
                },
            ],
        },
    ],
});
````

  
````go
if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
		OfSystemMessage: &anthropic.BetaManagedAgentsSystemMessageEventParams{
			Type: anthropic.BetaManagedAgentsSystemMessageEventParamsTypeSystemMessage,
			Content: []anthropic.BetaManagedAgentsSystemContentBlockParam{{
				Type: anthropic.BetaManagedAgentsSystemContentBlockTypeText,
				Text: "The user's current timezone is America/New_York.",
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
        .addEvent(BetaManagedAgentsSystemMessageEventParams.builder()
            .type(BetaManagedAgentsSystemMessageEventParams.Type.SYSTEM_MESSAGE)
            .addTextContent("The user's current timezone is America/New_York.")
            .build())
        .build());
````

  
````php
$client->beta->sessions->events->send(
    $session->id,
    events: [
        [
            'type' => 'system.message',
            'content' => [
                [
                    'type' => 'text',
                    'text' => "The user's current timezone is America/New_York.",
                ],
            ],
        ],
    ],
);
````

  
````ruby
client.beta.sessions.events.send_(
  session.id,
  events: [
    {
      type: "system.message",
      content: [
        {type: "text", text: "The user's current timezone is America/New_York."}
      ]
    }
  ]
)
````

</CodeGroup>

`system.message` tidak dapat dikirim saat sesi idle dengan `stop_reason: requires_action`. `content` menerima 1–1000 item teks.

### Melacak penggunaan \{#tracking-usage}

Objek sesi menyertakan field `usage` dengan statistik token kumulatif. Ambil sesi setelah menjadi idle untuk membaca total terbaru, dan gunakan untuk melacak biaya, menerapkan anggaran, atau memantau konsumsi.

```json
{
  "id": "sesn_01...",
  "status": "idle",
  "usage": {
    "input_tokens": 5000,
    "output_tokens": 3200,
    "cache_creation_input_tokens": 2000,
    "cache_read_input_tokens": 20000
  }
}
```

`input_tokens` melaporkan token input yang tidak di-cache dan `output_tokens` melaporkan total token output di seluruh panggilan model dalam sesi. Field `cache_creation_input_tokens` dan `cache_read_input_tokens` mencerminkan aktivitas caching prompt. Entri cache menggunakan TTL 5 menit, sehingga giliran berturut-turut dalam jendela waktu tersebut mendapat manfaat dari pembacaan cache, yang mengurangi biaya per token.

## Observabilitas Console \{#console-observability}

Console menyediakan tampilan timeline visual dari sesi agen Anda. Navigasikan ke bagian Claude Managed Agents di Console untuk melihat:

- **Daftar sesi:** Semua sesi dengan status, waktu pembuatan, dan modelnya
- **Tampilan tracing:** Tampilan kronologis event (konten, timestamp, penggunaan token) dalam sebuah sesi. Tampilan tracing hanya dapat diakses oleh Developer dan Admin.
- **Eksekusi alat:** Detail setiap panggilan alat dan hasilnya

## Tips debugging \{#debugging-tips}

- **Periksa event sesi:** Error sesi disampaikan melalui event `session.error`
- **Tinjau hasil alat:** Kegagalan eksekusi alat sering kali menjelaskan perilaku agen yang tidak terduga
- **Lacak penggunaan token:** Pantau konsumsi token untuk mengoptimalkan prompt dan mengurangi biaya
- **Gunakan prompt sistem:** Tambahkan instruksi logging ke prompt sistem agar agen menjelaskan penalarannya