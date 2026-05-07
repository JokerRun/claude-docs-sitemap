---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/events-and-streaming
fetched_at: 2026-05-07T03:15:02.178755Z
sha256: c9845d3519c9ba23fca9f0c8c2c8f0d1e401d5df9da757b13870bb931f6915bc
---

# Aliran peristiwa sesi

Kirim peristiwa, streaming respons, dan hentikan atau alihkan sesi Anda di tengah eksekusi.

---

Komunikasi dengan Claude Managed Agents berbasis peristiwa. Anda mengirim peristiwa pengguna ke agen, dan menerima peristiwa agen dan sesi kembali untuk melacak status.

<Note>
Semua permintaan API Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK secara otomatis menetapkan header beta.
</Note>

## Jenis peristiwa

Peristiwa mengalir dalam dua arah.
- **Peristiwa pengguna** adalah apa yang Anda kirim ke agen untuk memulai sesi dan mengarahkannya saat berkembang.
- **Peristiwa sesi**, **peristiwa span**, dan **peristiwa agen** dikirim kepada Anda untuk observabilitas ke dalam status sesi dan kemajuan agen Anda.

String jenis peristiwa mengikuti konvensi penamaan `{domain}.{action}`.

<Tabs>
  <Tab title="Peristiwa pengguna">

| Jenis | Deskripsi |
| --- | --- |
| `user.message` | Pesan pengguna dengan konten teks. |
| `user.interrupt` | Hentikan agen di tengah eksekusi. |
| `user.custom_tool_result` | Respons terhadap panggilan alat kustom dari agen. |
| `user.tool_confirmation` | Setujui atau tolak panggilan alat agen atau MCP ketika kebijakan izin memerlukan konfirmasi. |
| `user.define_outcome` | Tentukan [hasil](/docs/id/managed-agents/define-outcomes) untuk agen bekerja menuju.  |

  </Tab>
  <Tab title="Peristiwa agen">

| Jenis | Deskripsi |
| --- | --- |
| `agent.message` | Respons agen yang berisi blok konten teks. |
| `agent.thinking` | Konten pemikiran agen, dipancarkan terpisah dari pesan. |
| `agent.tool_use` | Agen menjalankan alat agen pra-bangun (bash, operasi file, dan sebagainya). |
| `agent.tool_result` | Hasil eksekusi alat agen pra-bangun. |
| `agent.mcp_tool_use` | Agen menjalankan alat server MCP. |
| `agent.mcp_tool_result` | Hasil eksekusi alat MCP. |
| `agent.custom_tool_use` | Agen menjalankan salah satu alat kustom Anda. Respons dengan peristiwa `user.custom_tool_result`. |
| `agent.thread_context_compacted` | Riwayat percakapan dikompres agar sesuai dengan jendela konteks. |
| `agent.thread_message_sent` | Agen mengirim pesan ke [multiagent](/docs/id/managed-agents/multi-agent) thread lain. |
| `agent.thread_message_received` | Agen menerima pesan dari [multiagent](/docs/id/managed-agents/multi-agent) thread lain. |

  </Tab>
  <Tab title="Peristiwa sesi">

| Jenis | Deskripsi |
| --- | --- |
| `session.status_running` | Agen sedang memproses secara aktif. |
| `session.status_idle` | Agen menyelesaikan tugas saat ini dan menunggu masukan. Mencakup `stop_reason` yang menunjukkan mengapa agen berhenti. |
| `session.status_rescheduled` | Kesalahan transien terjadi dan sesi sedang mencoba ulang secara otomatis. |
| `session.status_terminated` | Sesi berakhir karena kesalahan yang tidak dapat dipulihkan. |
| `session.error` | Kesalahan terjadi selama pemrosesan. Mencakup objek `error` yang diketik dengan `retry_status`. |
| `session.outcome_evaluated` | Evaluasi [hasil](/docs/id/managed-agents/define-outcomes) telah mencapai status terminal.  |
| `session.thread_created` | Koordinator menelurkan [multiagent](/docs/id/managed-agents/multi-agent) thread baru. |
| `session.thread_idle` | [multiagent](/docs/id/managed-agents/multi-agent) thread menyelesaikan pekerjaan saat ini. |

  </Tab>
  <Tab title="Peristiwa span">

Peristiwa span adalah penanda observabilitas yang membungkus aktivitas untuk waktu dan pelacakan penggunaan.

| Jenis | Deskripsi |
| --- | --- |
| `span.model_request_start` | Panggilan inferensi model telah dimulai. |
| `span.model_request_end` | Panggilan inferensi model telah selesai. Mencakup `model_usage` dengan jumlah token. |
| `span.outcome_evaluation_start` | Evaluasi [hasil](/docs/id/managed-agents/define-outcomes) telah dimulai.  |
| `span.outcome_evaluation_ongoing` | Detak jantung selama evaluasi [hasil](/docs/id/managed-agents/define-outcomes) yang sedang berlangsung.  |
| `span.outcome_evaluation_end` | Evaluasi [hasil](/docs/id/managed-agents/define-outcomes) telah selesai.  |

  </Tab>
</Tabs>

Setiap peristiwa mencakup stempel waktu `processed_at` yang menunjukkan kapan peristiwa dicatat di sisi server. Jika `processed_at` adalah null, itu berarti peristiwa telah antri oleh harness dan akan ditangani setelah peristiwa sebelumnya selesai diproses.

## Mengintegrasikan peristiwa

<Tabs>
  <Tab title="Mengirim peristiwa">

Kirim peristiwa `user.message` untuk memulai atau melanjutkan pekerjaan agen:

<CodeGroup>
```bash curl
curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
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
```

```python Python
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
```

```typescript TypeScript
await client.beta.sessions.events.send(session.id, {
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
});
```

```csharp C#
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
```

```go Go
if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.SendEventsParamsUnion{{
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
```

```java Java
client.beta().sessions().events().send(
    session.id(),
    EventSendParams.builder()
        .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
            .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
            .addTextContent("Analyze the performance of the sort function in utils.py")
            .build())
        .build());
```

```php PHP
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
```

```ruby Ruby
client.beta.sessions.events.send_(
  session.id,
  events: [
    {
      type: "user.message",
      content: [
        {type: "text", text: "Analyze the performance of the sort function in utils.py"}
      ]
    }
  ]
)
```
</CodeGroup>

Kirim peristiwa `user.interrupt` untuk menghentikan agen di tengah eksekusi, kemudian ikuti dengan peristiwa `user.message` untuk mengalihkannya:

<CodeGroup>
```bash curl
# Agent is currently analyzing a file...
# Interrupt with a new direction:
curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
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
```

```python Python
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
```

```typescript TypeScript
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
          text: "Instead, focus on fixing the bug in line 42."
        }
      ]
    }
  ]
});
```

```csharp C#
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
```

```go Go
// Agent is currently analyzing a file...
// Interrupt with a new direction:
if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.SendEventsParamsUnion{
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
```

```java Java
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
```

```php PHP
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
```

```ruby Ruby
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
```
</CodeGroup>

Agen akan mengakui gangguan dan beralih ke tugas baru.

  </Tab>
  <Tab title="Streaming respons">

Streaming peristiwa dari sesi untuk menerima pembaruan real-time saat agen bekerja. Hanya peristiwa yang dipancarkan setelah aliran dibuka yang disampaikan, jadi buka aliran sebelum mengirim peristiwa untuk menghindari kondisi balapan.

<CodeGroup>
  
````bash
# Open the stream first, then send the user message
exec {stream}< <(
  curl -sS -N --fail-with-body \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -H "Accept: text/event-stream"
)

curl -sS --fail-with-body \
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

while IFS= read -r -u "$stream" line; do
  [[ $line == data:* ]] || continue
  json=${line#data: }
  case $(jq -r '.type' <<<"$json") in
    agent.message)
      jq -j '.content[] | select(.type == "text") | .text' <<<"$json"
      ;;
    session.status_idle)
      break
      ;;
    session.error)
      printf '\n[Error: %s]\n' "$(jq -r '.error.message // "unknown"' <<<"$json")"
      break
      ;;
  esac
done
exec {stream}<&-
````

  
````bash
# Open the stream first, then send the user message
exec {stream}< <(ant beta:sessions:events stream \
  --session-id "$SESSION_ID" \
  --transform '{type,text:content.#(type=="text").text,err:error.message}' \
  --format yaml)

ant beta:sessions:events send \
  --session-id "$SESSION_ID" \
 > /dev/null <<'YAML'
events:
  - type: user.message
    content:
      - type: text
        text: Summarize the repo README
YAML

type=
while IFS= read -r -u "$stream" line; do
  case "$line" in
    type:\ session.status_idle) break ;;
    type:\ session.error)
      IFS= read -r -u "$stream" next || next=
      case "$next" in err:\ *) msg=${next#err: } ;; *) msg=unknown ;; esac
      printf '\n[Error: %s]\n' "$msg"; break ;;
    type:\ *) type=${line#type: } ;;
    text:*)
      [[ $type == agent.message ]] || continue
      val=${line#text: }
      case "$val" in '|-'|'|') ;; *) printf '%s' "$val" ;; esac ;;
    \ \ *)
      if [[ $type == agent.message ]]; then printf '%s\n' "${line#  }"; fi ;;
  esac
done
exec {stream}<&-
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
                msg = event.error.message if event.error else "unknown"
                print(f"\n[Error: {msg}]")
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
		Events: []anthropic.SendEventsParamsUnion{{
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

    for (var event : (Iterable<StreamEvents>) stream.stream()::iterator) {
        if (event.isAgentMessage()) {
            event.asAgentMessage().content().forEach(block -> IO.print(block.text()));
        } else if (event.isSessionStatusIdle()) {
            break;
        } else if (event.isSessionError()) {
            var msg = event.asSessionError().error()
                .flatMap(err -> err._json())
                .map(json -> {
                    Optional<Map<String, JsonValue>> obj = json.asObject();
                    return obj.orElseThrow().get("message").asStringOrThrow();
                })
                .orElse("unknown");
            IO.println("\n[Error: " + msg + "]");
            break;
        }
    }
}
````

  
````php
// Open the stream first, then send the user message
$stream = $client->beta->sessions->events->streamStream(
    $session->id,
    requestOptions: ['transporter' => $streamingClient],
);
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
            static fn($block) => $block->type === 'text' ? print($block->text) : null,
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

Untuk terhubung kembali ke sesi yang ada tanpa melewatkan peristiwa, buka aliran baru dan kemudian daftar riwayat lengkap untuk menabur set ID peristiwa yang terlihat. Ikuti aliran langsung sambil melewati peristiwa apa pun yang sudah dikembalikan oleh daftar riwayat.

<CodeGroup>
  
````bash
exec {stream}< <(
  curl -sS -N --fail-with-body \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -H "Accept: text/event-stream"
)

# Stream is open and buffering. List history before tailing live.
declare -A seen_event_ids
while IFS= read -r id; do
  seen_event_ids[$id]=1
done < <(
  curl -sS --fail-with-body \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" | jq -r '.data[].id'
)

# Tail live events, skipping anything already seen
while IFS= read -r -u "$stream" line; do
  [[ $line == data:* ]] || continue
  json=${line#data: }
  id=$(jq -r '.id' <<<"$json")
  [[ -n ${seen_event_ids[$id]+seen} ]] && continue
  seen_event_ids[$id]=1
  case $(jq -r '.type' <<<"$json") in
    agent.message)
      jq -j '.content[] | select(.type == "text") | .text' <<<"$json"
      ;;
    session.status_idle)
      break
      ;;
  esac
done
exec {stream}<&-
````

  
````bash
exec {stream}< <(ant beta:sessions:events stream \
  --session-id "$SESSION_ID" \
  --transform '{id,type,text:content.#(type=="text").text}' \
  --format yaml)
stream_pid=$!

# Stream is open and buffering. List history before tailing live.
declare -A seen_event_ids
while IFS= read -r id; do
  seen_event_ids[$id]=1
done < <(ant beta:sessions:events list \
  --session-id "$SESSION_ID" \
  --transform id --format yaml)

# Tail live events, skipping anything already seen
id= type= skip=
while IFS= read -r -u "$stream" line; do
  case "$line" in
    id:\ *)
      id=${line#id: }
      if [[ -n ${seen_event_ids[$id]+seen} ]]; then skip=1; continue; fi
      skip=; seen_event_ids[$id]=1 ;;
    type:\ *)
      [[ -n $skip ]] && continue
      type=${line#type: }
      [[ $type == session.status_idle ]] && break ;;
    text:*)
      [[ -z $skip && $type == agent.message ]] || continue
      val=${line#text: }
      case "$val" in '|-'|'|') ;; *) printf '%s' "$val" ;; esac ;;
    \ \ *)
      [[ -z $skip && $type == agent.message ]] && printf '%s\n' "${line#  }" ;;
  esac
done
exec {stream}<&-
````

  
````python
with client.beta.sessions.events.stream(session.id) as stream:
    # Stream is open and buffering. List history before tailing live.
    seen_event_ids = {event.id for event in client.beta.sessions.events.list(session.id)}

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
    // _json() exposes the raw event so we can read the cross-variant `id` field.
    var seenEventIds = new HashSet<String>();
    for (var past : client.beta().sessions().events().list(session.id()).autoPager()) {
        Optional<Map<String, JsonValue>> obj = past._json().orElseThrow().asObject();
        seenEventIds.add(obj.orElseThrow().get("id").asStringOrThrow());
    }

    // Tail live events, skipping anything already seen
    for (var event : (Iterable<StreamEvents>) stream.stream()::iterator) {
        Optional<Map<String, JsonValue>> obj = event._json().orElseThrow().asObject();
        if (!seenEventIds.add(obj.orElseThrow().get("id").asStringOrThrow())) continue;
        if (event.isAgentMessage()) {
            event.asAgentMessage().content().forEach(block -> IO.print(block.text()));
        } else if (event.isSessionStatusIdle()) {
            break;
        }
    }
}
````

  
````php
$stream = $client->beta->sessions->events->streamStream(
    $session->id,
    requestOptions: ['transporter' => $streamingClient],
);

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
            static fn($block) => $block->type === 'text' ? print($block->text) : null,
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

# Tail live events, skipping anything already seen
stream.each do |event|
  next if seen_event_ids.include?(event.id)
  seen_event_ids << event.id
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
  <Tab title="Mendaftar peristiwa masa lalu">

Ambil riwayat peristiwa lengkap untuk sesi:

<CodeGroup>
```bash curl
curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
```

```python Python
events = client.beta.sessions.events.list(session.id)
for event in events.data:
    print(f"[{event.type}] {event.processed_at}")
```

```typescript TypeScript
const events = await client.beta.sessions.events.list(session.id);
for (const event of events.data) {
  console.log(`[${event.type}] ${event.processed_at}`);
}
```

```csharp C#
var events = await client.Beta.Sessions.Events.List(session.ID);
foreach (var evt in events.Items)
{
    Console.WriteLine($"[{evt.Json.GetProperty("type").GetString()}] {evt.ProcessedAt}");
}
```

```go Go
events, err := client.Beta.Sessions.Events.List(ctx, session.ID, anthropic.BetaSessionEventListParams{})
if err != nil {
	panic(err)
}
for _, event := range events.Data {
	fmt.Printf("[%s] %s\n", event.Type, event.ProcessedAt)
}
```

```java Java
var events = client.beta().sessions().events().list(session.id());
for (var event : events.data()) {
    var json = (Map<String, JsonValue>) event._json().orElseThrow().asObject().orElseThrow();
    var type = json.get("type").asStringOrThrow();
    var processedAt = json.containsKey("processed_at")
        ? json.get("processed_at").asStringOrThrow()
        : "pending";
    IO.println("[" + type + "] " + processedAt);
}
```

```php PHP
$events = $client->beta->sessions->events->list($session->id);
foreach ($events->data as $event) {
    $processedAt = ($event->processedAt ?? null)?->format(DATE_RFC3339) ?? 'pending';
    echo "[{$event->type}] {$processedAt}\n";
}
```

```ruby Ruby
events = client.beta.sessions.events.list(session.id)
events.data.each { puts "[#{it.type}] #{it.processed_at}" }
```
</CodeGroup>

  </Tab>
</Tabs>

## Skenario tambahan

### Menangani panggilan alat kustom

Ketika agen menjalankan [alat kustom](/docs/id/managed-agents/tools#custom-tools):

1. Sesi memancarkan peristiwa `agent.custom_tool_use` yang berisi nama alat dan masukan.
2. Sesi dijeda dengan peristiwa `session.status_idle` yang berisi `stop_reason: requires_action`. ID peristiwa pemblokiran ada di array `stop_reason.requires_action.event_ids`.
3. Jalankan alat di sistem Anda dan kirim peristiwa `user.custom_tool_result` untuk masing-masing, meneruskan ID peristiwa dalam parameter `custom_tool_use_id` bersama dengan konten hasil.
4. Setelah semua peristiwa pemblokiran diselesaikan, sesi beralih kembali ke `running`.

<CodeGroup>
```bash curl
exec {fd}< <(curl -sS -N --fail-with-body \
  "https://api.anthropic.com/v1/sessions/$SESSION_ID/stream?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -H "Accept: text/event-stream")

while IFS= read -r -u "$fd" line; do
  [[ $line == data:* ]] || continue
  data="${line#data: }"
  [[ $(jq -r '.type' <<<"$data") == "session.status_idle" ]] || continue
  case $(jq -r '.stop_reason.type // empty' <<<"$data") in
    requires_action)
      while IFS= read -r event_id; do
        # Look up the custom tool use event and execute it
        result=$(call_tool "$event_id")
        # Send the result back
        jq -n --arg id "$event_id" --arg result "$result" \
          '{events: [{type: "user.custom_tool_result", custom_tool_use_id: $id, content: [{type: "text", text: $result}]}]}' |
          curl -sS --fail-with-body \
            "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            -H "anthropic-beta: managed-agents-2026-04-01" \
            -H "content-type: application/json" \
            -d @-
      done < <(jq -r '.stop_reason.event_ids[]' <<<"$data")
      ;;
    end_turn)
      break
      ;;
  esac
done
exec {fd}<&-
```

```python Python
with client.beta.sessions.events.stream(session.id) as stream:
    for event in stream:
        if event.type == "session.status_idle" and (stop := event.stop_reason):
            match stop.type:
                case "requires_action":
                    for event_id in stop.event_ids:
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
```

```typescript TypeScript
const stream = await client.beta.sessions.events.stream(session.id);

for await (const event of stream) {
  if (event.type === "session.status_idle") {
    if (event.stop_reason?.type === "requires_action") {
      for (const eventId of event.stop_reason.event_ids) {
        // Look up the custom tool use event and execute it
        const toolEvent = eventsById[eventId];
        const result = await callTool(toolEvent.name, toolEvent.input);

        // Send the result back
        await client.beta.sessions.events.send(session.id, {
          events: [
            {
              type: "user.custom_tool_result",
              custom_tool_use_id: eventId,
              content: [{ type: "text", text: result }]
            }
          ]
        });
      }
    } else if (event.stop_reason?.type === "end_turn") {
      break;
    }
  }
}
```

```csharp C#
await foreach (var streamEvent in client.Beta.Sessions.Events.StreamStreaming(session.ID))
{
    if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent idle)
    {
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
}
```

```go Go
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
				Events: []anthropic.SendEventsParamsUnion{{
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
```

```java Java
try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
    for (var event : (Iterable<StreamEvents>) stream.stream()::iterator) {
        if (!event.isSessionStatusIdle()) continue;
        var stopReason = event.asSessionStatusIdle().stopReason().orElseThrow();
        if (stopReason.isRequiresAction()) {
            for (var eventId : stopReason.asRequiresAction().eventIds()) {
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
            }
        } else if (stopReason.isEndTurn()) {
            break;
        }
    }
}
```

```php PHP
$stream = $client->beta->sessions->events->streamStream(
    $session->id,
    requestOptions: ['transporter' => $streamingClient],
);

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
```

```ruby Ruby
client.beta.sessions.events.stream_events(session.id).each do |event|
  case event
  in {type: :"session.status_idle", stop_reason: {type: :requires_action, event_ids:}}
    event_ids.each do |event_id|
      # Look up the custom tool use event and execute it
      tool_event = events_by_id[event_id]
      result = call_tool(tool_event.name, tool_event.input)
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
```
</CodeGroup>

### Konfirmasi alat

Ketika [kebijakan izin](/docs/id/managed-agents/permission-policies) memerlukan konfirmasi sebelum alat dijalankan:

1. Sesi mengeluarkan acara `agent.tool_use` atau `agent.mcp_tool_use`.
2. Sesi berhenti dengan acara `session.status_idle` yang berisi `stop_reason: requires_action`. ID acara pemblokir berada dalam array `stop_reason.requires_action.event_ids`.
3. Kirim acara `user.tool_confirmation` untuk masing-masing, meneruskan ID acara dalam parameter `tool_use_id`. Atur `result` ke `"allow"` atau `"deny"`. Gunakan `deny_message` untuk menjelaskan penolakan.
4. Setelah semua acara pemblokir diselesaikan, sesi kembali ke `running`.

<CodeGroup>
```bash curl
exec {fd}< <(curl -sS -N --fail-with-body \
  "https://api.anthropic.com/v1/sessions/$SESSION_ID/stream?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -H "Accept: text/event-stream")

while IFS= read -r -u "$fd" line; do
  [[ $line == data:* ]] || continue
  data="${line#data: }"
  [[ $(jq -r '.type' <<<"$data") == "session.status_idle" ]] || continue
  case $(jq -r '.stop_reason.type // empty' <<<"$data") in
    requires_action)
      while IFS= read -r event_id; do
        # Approve the pending tool call
        jq -n --arg id "$event_id" \
          '{events: [{type: "user.tool_confirmation", tool_use_id: $id, result: "allow"}]}' |
          curl -sS --fail-with-body \
            "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            -H "anthropic-beta: managed-agents-2026-04-01" \
            -H "content-type: application/json" \
            -d @-
      done < <(jq -r '.stop_reason.event_ids[]' <<<"$data")
      ;;
    end_turn)
      break
      ;;
  esac
done
exec {fd}<&-
```

```python Python
with client.beta.sessions.events.stream(session.id) as stream:
    for event in stream:
        if event.type == "session.status_idle" and (stop := event.stop_reason):
            match stop.type:
                case "requires_action":
                    for event_id in stop.event_ids:
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
```

```typescript TypeScript
const stream = await client.beta.sessions.events.stream(session.id);

for await (const event of stream) {
  if (event.type === "session.status_idle") {
    if (event.stop_reason?.type === "requires_action") {
      for (const eventId of event.stop_reason.event_ids) {
        // Approve the pending tool call
        await client.beta.sessions.events.send(session.id, {
          events: [
            {
              type: "user.tool_confirmation",
              tool_use_id: eventId,
              result: "allow"
            }
          ]
        });
      }
    } else if (event.stop_reason?.type === "end_turn") {
      break;
    }
  }
}
```

```csharp C#
await foreach (var streamEvent in client.Beta.Sessions.Events.StreamStreaming(session.ID))
{
    if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent idle)
    {
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
}
```

```go Go
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
				Events: []anthropic.SendEventsParamsUnion{{
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
```

```java Java
try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
    for (var event : (Iterable<StreamEvents>) stream.stream()::iterator) {
        if (!event.isSessionStatusIdle()) continue;
        var stopReason = event.asSessionStatusIdle().stopReason().orElseThrow();
        if (stopReason.isRequiresAction()) {
            for (var eventId : stopReason.asRequiresAction().eventIds()) {
                // Approve the pending tool call
                client.beta().sessions().events().send(
                    session.id(),
                    EventSendParams.builder()
                        .addEvent(BetaManagedAgentsUserToolConfirmationEventParams.builder()
                            .type(BetaManagedAgentsUserToolConfirmationEventParams.Type.USER_TOOL_CONFIRMATION)
                            .toolUseId(eventId)
                            .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.ALLOW)
                            .build())
                        .build());
            }
        } else if (stopReason.isEndTurn()) {
            break;
        }
    }
}
```

```php PHP
$stream = $client->beta->sessions->events->streamStream(
    $session->id,
    requestOptions: ['transporter' => $streamingClient],
);

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
```

```ruby Ruby
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
```
</CodeGroup>

### Melacak penggunaan

Objek sesi mencakup bidang `usage` dengan statistik token kumulatif. Ambil sesi setelah menjadi idle untuk membaca total terbaru, dan gunakan untuk melacak biaya, memberlakukan anggaran, atau memantau konsumsi.

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

`input_tokens` melaporkan token input yang tidak di-cache dan `output_tokens` melaporkan total token output di semua panggilan model dalam sesi. Bidang `cache_creation_input_tokens` dan `cache_read_input_tokens` mencerminkan aktivitas prompt caching. Entri cache menggunakan TTL 5 menit, jadi giliran berturut-turut dalam jendela itu mendapat manfaat dari pembacaan cache, yang mengurangi biaya per-token.