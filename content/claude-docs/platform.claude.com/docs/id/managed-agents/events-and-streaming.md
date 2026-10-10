---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/events-and-streaming
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: 453602715894397d4faccdfcfb6b83d510fe69ff0074c23b003cf821ebef7962
---

---
title: Aliran event sesi
url: https://platform.claude.com/docs/id/managed-agents/events-and-streaming
description: Kirim event, lakukan streaming respons, dan interupsi atau arahkan ulang sesi Anda di tengah eksekusi.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Komunikasi dengan Claude Managed Agents berbasis event. Anda membuka aliran (stream) untuk mengikuti sesi, mengirim event untuk mengarahkannya, dan menjawabnya ketika sesi berhenti sejenak untuk menunggu input.

## Jenis event

Event mengalir dalam dua arah: Anda mengirim event ke agen, dan sesi mengirim event kembali kepada Anda.

* **Event yang Anda kirim:** Event `user.*` memulai sesi dan mengarahkannya seiring berjalannya sesi. Event [`system.message`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#send-system-messages) menambahkan konteks tingkat sistem.
* **Event yang Anda terima:** Event sesi, event span, dan event agen melaporkan status sesi dan kemajuan agen.

String jenis event ini mengikuti konvensi penamaan `{domain}.{action}`. Lihat [Tipe event](https://platform.claude.com/docs/id/managed-agents/reference#event-types) di referensi untuk katalog lengkapnya.

[Jenis event webhook](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types) terpisah, dan beberapa namanya berbeda dari nama di aliran. Misalnya, webhook menggunakan `session.status_idled` alih-alih `session.status_idle`.

## Streaming event

Lakukan streaming event dari sesi untuk menerima pembaruan real-time saat agen bekerja. Sebuah aliran hanya mengirimkan event yang dipancarkan setelah aliran dibuka, jadi buka aliran sebelum Anda mengirim event untuk menghindari "race condition" (kondisi balapan).

<CodeGroup>
  ```bash cURL
  # Buka stream terlebih dahulu, lalu kirim pesan pengguna
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
  ```

  ```bash CLI
  # Alur kerja ini tidak cocok dijadikan perintah shell sekali jalan.
  # Gunakan salah satu contoh SDK dalam grup kode ini sebagai gantinya.
  ```

  ```python Python
  # Buka stream terlebih dahulu, lalu kirim pesan pengguna
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
  ```

  ```typescript TypeScript
  // Buka stream terlebih dahulu, lalu kirim pesan pengguna
  const stream = await client.beta.sessions.events.stream(session.id);
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "Summarize the repo README" }]
      }
    ]
  });

  events: for await (const event of stream) {
    switch (event.type) {
      case "agent.message":
        for (const block of event.content) {
          if (block.type === "text") {
            process.stdout.write(block.text);
          }
        }
        break;
      case "session.status_idle":
        break events;
      case "session.error":
        console.log(`\n[Error: ${event.error?.message ?? "unknown"}]`);
        break events;
    }
  }
  ```

  ```csharp C#
  // Buka stream terlebih dahulu, lalu kirim pesan pengguna
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
              if (block.Value is BetaManagedAgentsTextBlock textBlock)
              {
                  Console.Write(textBlock.Text);
              }
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
  ```

  ```go Go
  	// Buka stream terlebih dahulu, lalu kirim pesan pengguna
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
  			// daftar bertipe konkret: BetaManagedAgentsTextBlock
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
  ```

  ```java Java
  // Buka stream terlebih dahulu, lalu kirim pesan pengguna
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
      events:
      for (var event : events) {
          switch (event.type().value()) {
              case AGENT_MESSAGE -> event.asAgentMessage().content().forEach(block -> block.text().ifPresent(textBlock -> IO.print(textBlock.text())));
              case SESSION_STATUS_IDLE -> {
                  break events;
              }
              case SESSION_ERROR -> {
                  // Field `message` ada di semua varian error; baca dari JSON mentah.
                  var errorMessage =
                      event.asSessionError().error()._json().orElse(null) instanceof JsonObject json
                          ? json.values().get("message").asStringOrThrow()
                          : "unknown";
                  IO.println("\n[Error: " + errorMessage + "]");
                  break events;
              }
          }
      }
  }
  ```

  ```php PHP
  // Buka stream terlebih dahulu, lalu kirim pesan pengguna
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
      match (true) {
          $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsAgentMessageEvent => array_walk(
              $event->content,
              static fn ($block) => $block instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsTextBlock ? print($block->text) : null,
          ),
          $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionErrorEvent => printf("\n[Error: %s]", $event->error?->message ?? 'unknown'),
          default => null,
      };
      if ($event->type === 'session.status_idle' || $event->type === 'session.error') {
          break;
      }
  }
  $stream->close();
  ```

  ```ruby Ruby
  # Buka stream terlebih dahulu, lalu kirim pesan pengguna
  stream = client.beta.sessions.events.stream_events(session.id)

  client.beta.sessions.events.send_(
    session.id,
    events: [{
      type: "user.message",
      content: [{type: "text", text: "Summarize the repo README"}]
    }]
  )

  stream.each do |event|
    case event
    when Anthropic::Beta::Sessions::BetaManagedAgentsAgentMessageEvent
      event.content.each { print it.text }
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusIdleEvent
      break
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionErrorEvent
      puts "\n[Error: #{event.error&.message || "unknown"}]"
      break
    else
      # abaikan tipe event lainnya
    end
  end
  ```
</CodeGroup>

Sesi melaporkan error melalui event `session.error`. Lihat [Tipe event](https://platform.claude.com/docs/id/managed-agents/reference#event-types) untuk field-nya.

Teks respons agen tiba sebagai event `agent.message` yang di-buffer, masing-masing dipancarkan hanya setelah permintaan model yang menghasilkannya selesai. Untuk merender teks saat model masih menghasilkannya, lihat [Pratinjau respons dengan event delta](https://platform.claude.com/docs/id/managed-agents/event-deltas).

### Menyambung kembali tanpa melewatkan event

Untuk menyambung kembali ke sesi yang sudah ada tanpa melewatkan event, gabungkan aliran baru dengan riwayat event:

1. Buka aliran baru.
2. [Daftarkan riwayat event lengkap](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#list-past-events) untuk mengisi kumpulan ID event yang sudah terlihat.
3. Ikuti aliran langsung, lewati event apa pun yang sudah dikembalikan oleh daftar riwayat.

<CodeGroup>
  ```bash cURL
  exec {stream}< <(
    curl --fail-with-body -sS -N \
      "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
      -H "content-type: application/json" \
      -H "accept: text/event-stream"
  )

  # Stream terbuka dan melakukan buffering. Tampilkan riwayat sebelum mengikuti event langsung.
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

  # Ikuti event langsung, lewati yang sudah pernah dilihat
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
  ```

  ```bash CLI
  # Alur kerja ini tidak cocok dijadikan perintah shell sekali jalan.
  # Gunakan salah satu contoh SDK dalam grup kode ini sebagai gantinya.
  ```

  ```python Python
  with client.beta.sessions.events.stream(session.id) as stream:
      # Stream terbuka dan sedang buffering. Tampilkan riwayat sebelum mengikuti event langsung.
      history = client.beta.sessions.events.list(session.id)
      seen_event_ids = {past_event.id for past_event in history}

      # Ikuti event langsung, lewati yang sudah pernah terlihat
      for event in stream:
          if event.type == "event_start" or event.type == "event_delta":
              # Pratinjau delta tidak diaktifkan pada koneksi ini.
              continue
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
  ```

  ```typescript TypeScript
  const seenEventIds = new Set<string>();
  const stream = await client.beta.sessions.events.stream(session.id);

  // Stream terbuka dan melakukan buffering. Tampilkan riwayat sebelum mengikuti event langsung.
  for await (const event of client.beta.sessions.events.list(session.id)) {
    seenEventIds.add(event.id);
  }

  // Ikuti event langsung, lewati yang sudah terlihat
  tail: for await (const event of stream) {
    // Event pratinjau (event_start/event_delta) tidak membawa id tingkat atas
    if (event.type === "event_start" || event.type === "event_delta") continue;
    if (seenEventIds.has(event.id)) continue;
    seenEventIds.add(event.id);
    switch (event.type) {
      case "agent.message":
        for (const block of event.content) {
          if (block.type === "text") {
            process.stdout.write(block.text);
          }
        }
        break;
      case "session.status_idle":
        break tail;
    }
  }
  ```

  ```csharp C#
  using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(session.ID);

  // Stream terbuka dan sedang buffering. Tampilkan riwayat sebelum tailing live.
  HashSet<string> seenEventIds = [];
  var history = await client.Beta.Sessions.Events.List(session.ID);
  await foreach (var pastEvent in history.Paginate())
  {
      seenEventIds.Add(pastEvent.ID);
  }

  // Tail event live, lewati yang sudah pernah dilihat
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
              if (block.Value is BetaManagedAgentsTextBlock textBlock)
              {
                  Console.Write(textBlock.Text);
              }
          }
      }
      else if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent)
      {
          break;
      }
  }
  ```

  ```go Go
  	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
  	defer stream.Close()

  	// Stream terbuka dan sedang buffering. Tampilkan riwayat sebelum tailing live.
  	seenEventIDs := map[string]struct{}{}
  	history := client.Beta.Sessions.Events.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionEventListParams{})
  	for history.Next() {
  		seenEventIDs[history.Current().ID] = struct{}{}
  	}
  	if err := history.Err(); err != nil {
  		panic(err)
  	}

  	// Tail event live, lewati yang sudah pernah dilihat
  tail:
  	for stream.Next() {
  		event := stream.Current()
  		if _, seen := seenEventIDs[event.ID]; seen {
  			continue
  		}
  		seenEventIDs[event.ID] = struct{}{}
  		switch event := event.AsAny().(type) {
  		case anthropic.BetaManagedAgentsAgentMessageEvent:
  			// daftar bertipe konkret: BetaManagedAgentsTextBlock
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
  ```

  ```java Java
  try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
      // Stream terbuka dan sedang buffering. Tampilkan riwayat sebelum tailing live.
      // Setiap varian event membawa `id`; baca dari JSON mentah untuk dedup lintas varian.
      var seenEventIds = new HashSet<String>();
      for (var pastEvent : client.beta().sessions().events().list(session.id()).autoPager()) {
          if (pastEvent._json().orElseThrow() instanceof JsonObject json) {
              seenEventIds.add(json.values().get("id").asStringOrThrow());
          }
      }

      // Tail event live; Set.add mengembalikan false untuk ID yang sudah dilihat, melewati replay.
      stream.stream()
          .filter(event -> event._json().orElseThrow() instanceof JsonObject json
              && seenEventIds.add(json.values().get("id").asStringOrThrow()))
          .takeWhile(event -> !event.isSessionStatusIdle())
          .filter(BetaManagedAgentsStreamSessionEvents::isAgentMessage)
          .forEach(event -> event.asAgentMessage().content()
              .forEach(block -> block.text().ifPresent(textBlock -> IO.print(textBlock.text()))));
  }
  ```

  ```php PHP
  $stream = $client->beta->sessions->events->streamStream($session->id);

  // Stream terbuka dan sedang buffering. Tampilkan riwayat sebelum mengikuti event langsung.
  $seenEventIds = [];
  foreach ($client->beta->sessions->events->list($session->id)->pagingEachItem() as $event) {
      $seenEventIds[$event->id] = true;
  }

  // Ikuti event langsung, lewati apa pun yang sudah terlihat
  foreach ($stream as $event) {
      if (isset($seenEventIds[$event->id])) {
          continue;
      }
      $seenEventIds[$event->id] = true;
      match (true) {
          $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsAgentMessageEvent => array_walk(
              $event->content,
              static fn ($block) => $block instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsTextBlock ? print($block->text) : null,
          ),
          default => null,
      };
      if ($event->type === 'session.status_idle') {
          break;
      }
  }
  $stream->close();
  ```

  ```ruby Ruby
  stream = client.beta.sessions.events.stream_events(session.id)

  # Stream terbuka dan melakukan buffering. Tampilkan riwayat sebelum mengikuti event langsung.
  seen_event_ids = Set.new
  client.beta.sessions.events.list(session.id).auto_paging_each { seen_event_ids << it.id }

  # Ikuti event langsung, lewati yang sudah terlihat — Set#add? mengembalikan nil untuk duplikat
  stream.each do |event|
    next unless seen_event_ids.add?(event.id)
    case event
    when Anthropic::Beta::Sessions::BetaManagedAgentsAgentMessageEvent
      event.content.each { print it.text }
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusIdleEvent
      break
    else
      # abaikan tipe event lainnya
    end
  end
  ```
</CodeGroup>

## Mengirim event

Kirim event `user.message` untuk memulai atau melanjutkan pekerjaan agen:

<CodeGroup>
  ```bash cURL
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
  ```

  ```bash CLI
  ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
  events:
    - type: user.message
      content:
        - type: text
          text: Analyze the performance of the sort function in utils.py
  YAML
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
            text: "Analyze the performance of the sort function in utils.py",
          },
        ],
      },
    ],
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
          {
            type: "text",
            text: "Analyze the performance of the sort function in utils.py"
          }
        ]
      }
    ]
  )
  ```
</CodeGroup>

Setiap event dalam riwayat sesi menyertakan timestamp `processed_at`, yang ditetapkan ketika event selesai diproses. Pada event yang Anda kirim, `processed_at` bernilai null selama event masih mengantre di belakang event sebelumnya. Pengecualiannya adalah `user.define_outcome`, `user.custom_tool_result`, dan `user.tool_result`, yang diproses saat diterima dan dikembalikan dengan `processed_at` yang sudah terisi.

## Merespons ketika sesi menjadi idle

Event `session.status_idle` berarti agen telah berhenti dan sedang menunggu input. `stop_reason.type`-nya menjelaskan alasannya:

| `stop_reason.type` | Mengapa sesi berhenti                                                                                                                                     | Apa yang harus dilakukan                                                                                                                                               |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `end_turn`         | Agen menyelesaikan gilirannya, atau [Anda menginterupsinya](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#interrupt-the-agent). | [Kirim `user.message`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#resume-an-idle-session) ketika Anda memiliki pekerjaan lain untuk agen. |
| `requires_action`  | Satu atau lebih panggilan alat memerlukan jawaban dari Anda, seperti panggilan alat kustom atau permintaan konfirmasi.                                    | [Jawab setiap panggilan alat yang memblokir](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#answer-tool-calls-that-pause-the-session).        |
| `budget_reached`   | Biaya daftar yang dilacak sesi telah mencapai [anggarannya](https://platform.claude.com/docs/id/managed-agents/budgets).                                  | [Ubah atau hapus anggaran](https://platform.claude.com/docs/id/managed-agents/budgets#resume-a-session-at-its-budget).                                                 |

Tidak ada event yang Anda kirim yang dapat melanjutkan sesi yang dijeda pada anggarannya. Pekerjaan yang dijeda oleh anggaran akan dilanjutkan secara otomatis ketika Anda mengubah anggaran ke nilai di atas biaya daftar yang telah terpakai, atau menghapusnya. Ketika pekerjaan dilanjutkan, sesi memancarkan event `workflow_run.status_running` untuk setiap [eksekusi workflow yang dijeda oleh anggaran](https://platform.claude.com/docs/id/managed-agents/workflow-runs#budgets-and-limits). Eksekusi yang dijeda oleh interupsi tetap dijeda; lihat [Melanjutkan sesi yang mencapai anggarannya](https://platform.claude.com/docs/id/managed-agents/budgets#resume-a-session-at-its-budget). Lihat [Ketika sesi mencapai anggarannya](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget) untuk event yang menandai jeda dan event yang masih diterima oleh sesi.

## Menjawab panggilan alat yang menjeda sesi

Sesi dijeda ketika agen memanggil [alat kustom](https://platform.claude.com/docs/id/managed-agents/tools#custom-tools), dan ketika panggilan alat memerlukan konfirmasi Anda berdasarkan [kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies). Kedua jeda mengikuti urutan yang sama:

1. Sesi memancarkan panggilan alat sebagai event `agent.custom_tool_use`, `agent.tool_use`, atau `agent.mcp_tool_use`.
2. Sesi dijeda dengan event `session.status_idle` yang `stop_reason.type`-nya adalah `requires_action`. ID event yang memblokir ada di array `stop_reason.event_ids`.
3. Untuk setiap ID event yang memblokir, kirim event [`user.custom_tool_result`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#return-a-custom-tool-result) atau [`user.tool_confirmation`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#confirm-a-tool-call). Hasil alat kustom tidak perlu menunggu langkah 2.
4. Setelah semua event yang memblokir diselesaikan, sesi kembali ke status `running`.

Dalam sesi multiagen, event yang memblokir dari subagen juga diposting ke thread utama. Lihat [Izin alat dan alat kustom](https://platform.claude.com/docs/id/managed-agents/session-threads#tool-permissions-and-custom-tools).

### Mengembalikan hasil alat kustom

Event `agent.custom_tool_use` berisi nama alat dan input. Jalankan alat tersebut di sistem Anda. Kemudian kirim event `user.custom_tool_result`, dengan meneruskan ID event di parameter `custom_tool_use_id` beserta konten hasilnya.

Anda dapat mengirim hasil segera setelah event `agent.custom_tool_use` tiba, tanpa menunggu `session.status_idle`. Sesi tetap memancarkan `session.status_idle` dengan alasan berhenti `requires_action` untuk panggilan tersebut, dan klien Anda dapat mengabaikannya. Hasil kedua untuk panggilan yang sama akan diterima dan tidak berpengaruh apa pun.

Ketika Anda [menyambung kembali](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#reconnect-without-missing-events) ke sesi yang dijeda, `stop_reason.event_ids` pada event `session.status_idle` terbaru mencantumkan panggilan yang perlu dijawab.

Contoh berikut menjawab setiap panggilan saat panggilan tersebut tiba:

<CodeGroup>
  ```bash cURL
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
    case $(jq -r '.type' <<<"$event_json") in
      agent.custom_tool_use)
        # Jalankan alat dan kirim hasilnya kembali
        result=$(call_tool "$(jq -r '.name' <<<"$event_json")" "$(jq -c '.input' <<<"$event_json")")
        jq --arg result "$result" \
          '{events: [{type: "user.custom_tool_result", custom_tool_use_id: .id, content: [{type: "text", text: $result}]}]}' <<<"$event_json" |
          curl --fail-with-body -sS \
            "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            -H "anthropic-beta: managed-agents-2026-04-01" \
            -H "content-type: application/json" \
            -d @-
        ;;
      session.status_idle)
        if [[ $(jq -r '.stop_reason.type' <<<"$event_json") == end_turn ]]; then
          break
        fi
        ;;
    esac
  done
  exec {stream_fd}<&-
  ```

  ```bash CLI
  # Alur kerja ini tidak cocok diterjemahkan ke perintah shell sekali jalan.
  # Gunakan salah satu contoh SDK dalam grup kode ini sebagai gantinya.
  ```

  ```python Python
  with client.beta.sessions.events.stream(session.id) as stream:
      for event in stream:
          match event.type:
              case "agent.custom_tool_use":
                  # Jalankan alat
                  result = call_tool(event.name, event.input)

                  # Kirim hasilnya kembali
                  client.beta.sessions.events.send(
                      session.id,
                      events=[
                          {
                              "type": "user.custom_tool_result",
                              "custom_tool_use_id": event.id,
                              "content": [{"type": "text", "text": result}],
                          },
                      ],
                  )
              case "session.status_idle":
                  if event.stop_reason and event.stop_reason.type == "end_turn":
                      break
  ```

  ```typescript TypeScript
  const stream = await client.beta.sessions.events.stream(session.id);

  loop: for await (const event of stream) {
    switch (event.type) {
      case "agent.custom_tool_use": {
        // Jalankan alat
        const result = await callTool(event.name, event.input);

        // Kirim hasilnya kembali
        await client.beta.sessions.events.send(session.id, {
          events: [
            {
              type: "user.custom_tool_result",
              custom_tool_use_id: event.id,
              content: [{ type: "text", text: result }],
            },
          ],
        });
        break;
      }
      case "session.status_idle":
        if (event.stop_reason.type === "end_turn") break loop;
        break;
    }
  }
  ```

  ```csharp C#
  await foreach (var streamEvent in client.Beta.Sessions.Events.StreamStreaming(session.ID))
  {
      if (streamEvent.Value is BetaManagedAgentsAgentCustomToolUseEvent toolUse)
      {
          // Jalankan alat
          var result = await CallTool(toolUse.Name, toolUse.Input);

          // Kirim hasilnya kembali
          await client.Beta.Sessions.Events.Send(session.ID, new()
          {
              Events =
              [
                  new BetaManagedAgentsUserCustomToolResultEventParams
                  {
                      Type = BetaManagedAgentsUserCustomToolResultEventParamsType.UserCustomToolResult,
                      CustomToolUseID = toolUse.ID,
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
      else if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent idle
          && idle.StopReason?.Value is BetaManagedAgentsSessionEndTurn)
      {
          break;
      }
  }
  ```

  ```go Go
  	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
  	defer stream.Close()

  loop:
  	for stream.Next() {
  		switch event := stream.Current().AsAny().(type) {
  		case anthropic.BetaManagedAgentsAgentCustomToolUseEvent:
  			// Jalankan alat
  			result := callTool(event.Name, event.Input)
  			// Kirim hasilnya kembali
  			if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  				Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  					OfUserCustomToolResult: &anthropic.BetaManagedAgentsUserCustomToolResultEventParams{
  						Type:            anthropic.BetaManagedAgentsUserCustomToolResultEventParamsTypeUserCustomToolResult,
  						CustomToolUseID: event.ID,
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
  		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
  			if _, ok := event.StopReason.AsAny().(anthropic.BetaManagedAgentsSessionEndTurn); ok {
  				break loop
  			}
  		}
  	}
  	if err := stream.Err(); err != nil {
  		panic(err)
  	}
  ```

  ```java Java
  try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
      loop:
      for (var event : (Iterable<BetaManagedAgentsStreamSessionEvents>) stream.stream()::iterator) {
          switch (event.type().value()) {
              case AGENT_CUSTOM_TOOL_USE -> {
                  // Jalankan alat
                  var toolUse = event.asAgentCustomToolUse();
                  var result = callTool(toolUse.name(), toolUse.input());

                  // Kirim hasilnya kembali
                  client.beta().sessions().events().send(
                      session.id(),
                      EventSendParams.builder()
                          .addEvent(BetaManagedAgentsUserCustomToolResultEventParams.builder()
                              .type(BetaManagedAgentsUserCustomToolResultEventParams.Type.USER_CUSTOM_TOOL_RESULT)
                              .customToolUseId(toolUse.id())
                              .addTextContent(result)
                              .build())
                          .build());
              }
              case SESSION_STATUS_IDLE -> {
                  if (event.asSessionStatusIdle().stopReason().isEndTurn()) {
                      break loop;
                  }
              }
          }
      }
  }
  ```

  ```php PHP
  $stream = $client->beta->sessions->events->streamStream($session->id);

  foreach ($stream as $event) {
      switch (true) {
          case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsAgentCustomToolUseEvent:
              // Jalankan alat
              $result = callTool($event->name, $event->input);

              // Kirim hasilnya kembali
              $client->beta->sessions->events->send(
                  $session->id,
                  events: [
                      [
                          'type' => 'user.custom_tool_result',
                          'custom_tool_use_id' => $event->id,
                          'content' => [['type' => 'text', 'text' => $result]],
                      ],
                  ],
              );
              break;
          case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionStatusIdleEvent:
              if ($event->stopReason instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionEndTurn) {
                  break 2;
              }
              break;
      }
  }
  ```

  ```ruby Ruby
  client.beta.sessions.events.stream_events(session.id).each do |event|
    case event
    when Anthropic::Beta::Sessions::BetaManagedAgentsAgentCustomToolUseEvent
      # Jalankan alat
      result = call_tool.call(event.name, event.input)
      # Kirim hasilnya kembali
      client.beta.sessions.events.send_(
        session.id,
        events: [
          {
            type: "user.custom_tool_result",
            custom_tool_use_id: event.id,
            content: [{type: "text", text: result}]
          }
        ]
      )
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusIdleEvent
      break if event.stop_reason.is_a?(Anthropic::Beta::Sessions::BetaManagedAgentsSessionEndTurn)
    end
  end
  ```
</CodeGroup>

Jika agen memiliki [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs) yang terbuka, panggilan alat kustom dapat tiba saat sesi tetap `running`. Event idle `requires_action` hanya tiba ketika tidak ada satu pun [thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads) yang sedang bekerja. Jangan menunggunya: jawab setiap panggilan ketika event `agent.custom_tool_use`-nya tiba. Contoh di [Mengikuti eksekusi](https://platform.claude.com/docs/id/managed-agents/workflow-runs#follow-a-run) menunjukkan caranya.

### Mengonfirmasi panggilan alat

Kirim event `user.tool_confirmation`, dengan meneruskan ID event di parameter `tool_use_id`. Atur `result` ke `"allow"` atau `"deny"`. Lihat [Merespons permintaan konfirmasi](https://platform.claude.com/docs/id/managed-agents/permission-policies#respond-to-confirmation-requests) untuk mengetahui panggilan mana yang menunggu konfirmasi dan cara menjelaskan penolakan.

Contoh berikut menyetujui setiap panggilan yang tertunda:

<CodeGroup>
  ```bash cURL
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
          # Setujui panggilan alat yang tertunda
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
  ```

  ```bash CLI
  # Alur kerja ini tidak cocok diterjemahkan ke perintah shell sekali jalan.
  # Gunakan salah satu contoh SDK dalam grup kode ini sebagai gantinya.
  ```

  ```python Python
  with client.beta.sessions.events.stream(session.id) as stream:
      for event in stream:
          if event.type == "session.status_idle" and (stop_reason := event.stop_reason):
              match stop_reason.type:
                  case "requires_action":
                      for event_id in stop_reason.event_ids:
                          # Setujui panggilan alat yang tertunda
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
    if (event.type !== "session.status_idle") continue;
    if (event.stop_reason.type === "end_turn") break;
    if (event.stop_reason.type !== "requires_action") continue;

    for (const eventId of event.stop_reason.event_ids) {
      // Setujui panggilan alat yang tertunda
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
  ```

  ```csharp C#
  await foreach (var streamEvent in client.Beta.Sessions.Events.StreamStreaming(session.ID))
  {
      if (streamEvent.Value is not BetaManagedAgentsSessionStatusIdleEvent idle) continue;

      if (idle.StopReason?.Value is BetaManagedAgentsSessionRequiresAction requiresAction)
      {
          foreach (var eventId in requiresAction.EventIds)
          {
              // Setujui panggilan alat yang tertunda
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
  				// Setujui panggilan alat yang tertunda
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
  ```

  ```java Java
  try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
      stream.stream()
          .filter(BetaManagedAgentsStreamSessionEvents::isSessionStatusIdle)
          .map(idleEvent -> idleEvent.asSessionStatusIdle().stopReason())
          .takeWhile(stopReason -> !stopReason.isEndTurn())
          .filter(stopReason -> stopReason.isRequiresAction())
          .flatMap(stopReason -> stopReason.asRequiresAction().eventIds().stream())
          // Setujui setiap panggilan alat yang tertunda
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
  ```

  ```php PHP
  $stream = $client->beta->sessions->events->streamStream($session->id);

  foreach ($stream as $event) {
      if ($event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionStatusIdleEvent && $event->stopReason) {
          switch (true) {
              case $event->stopReason instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionRequiresAction:
                  foreach ($event->stopReason->eventIDs as $eventId) {
                      // Setujui panggilan alat yang tertunda
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
                  break;
              case $event->stopReason instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionEndTurn:
                  break 2;
          }
      }
  }
  ```

  ```ruby Ruby
  client.beta.sessions.events.stream_events(session.id).each do |event|
    case event
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusIdleEvent
      stop_reason = event.stop_reason
      case stop_reason
      when Anthropic::Beta::Sessions::BetaManagedAgentsSessionRequiresAction
        stop_reason.event_ids.each do |event_id|
          # Setujui panggilan alat yang tertunda
          client.beta.sessions.events.send_(
            session.id,
            events: [
              {type: "user.tool_confirmation", tool_use_id: event_id, result: "allow"}
            ]
          )
        end
      when Anthropic::Beta::Sessions::BetaManagedAgentsSessionEndTurn
        break
      end
    end
  end
  ```
</CodeGroup>

Contoh sebelumnya menyetujui setiap panggilan setelah sesi menjadi idle. Jika agen memiliki [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs) yang terbuka, panggilan alat dapat menunggu konfirmasi Anda saat sesi tetap `running`. Jangan menunggu event idle: ketika event `agent.tool_use` atau `agent.mcp_tool_use` tiba dengan [`evaluated_permission`](https://platform.claude.com/docs/id/managed-agents/permission-policies#see-how-each-call-was-evaluated) bernilai `ask`, jawablah. Contoh di [Mengikuti eksekusi](https://platform.claude.com/docs/id/managed-agents/workflow-runs#follow-a-run) menjawab panggilan alat kustom dengan cara ini, dan pengantarnya menjelaskan cara menambahkan konfirmasi.

## Melanjutkan sesi yang idle

Sesi tetap tersimpan di antara interaksi. Untuk melanjutkan sesi, kirim event `user.message` ke sesi tersebut seperti biasa:

<CodeGroup>
  ```bash cURL
  # Di produksi, berikan ID tersimpan dari sesi yang ingin Anda lanjutkan.
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
  ```

  ```bash CLI
  # Di produksi, berikan ID tersimpan dari sesi yang ingin Anda lanjutkan.
  ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
  events:
    - type: user.message
      content:
        - type: text
          text: Now run the tests against the changes you made earlier.
  YAML
  ```

  ```python Python
  # Lanjutkan sesi yang dibuat sebelumnya dengan mengirimkan event user.message baru.
  # Di produksi, berikan ID tersimpan dari sesi yang ingin Anda lanjutkan.
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
  ```

  ```typescript TypeScript
  // Lanjutkan sesi yang dibuat sebelumnya dengan mengirimkan event pengguna baru.
  // Di produksi, berikan ID tersimpan dari sesi yang ingin Anda lanjutkan.
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
  ```

  ```csharp C#
  // Lanjutkan sesi yang dibuat sebelumnya berdasarkan ID. Di produksi, berikan
  // ID sesi yang Anda simpan saat sesi dibuat.
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
  ```

  ```go Go
  // Lanjutkan sesi yang dibuat sebelumnya dengan mengirimkan event user.message
  // baru. Di produksi, berikan ID tersimpan dari sesi yang akan dilanjutkan.
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
  ```

  ```java Java
  // Lanjutkan sesi yang dibuat sebelumnya berdasarkan ID. Di produksi, teruskan
  // ID sesi yang Anda simpan saat sesi dibuat.
  client.beta().sessions().events().send(
      session.id(),
      EventSendParams.builder()
          .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
              .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
              .addTextContent("Now run the tests against the changes you made earlier.")
              .build())
          .build());
  ```

  ```php PHP
  // Lanjutkan sesi yang dibuat sebelumnya dengan mengirimkan event user.message baru.
  // Di produksi, berikan ID sesi yang Anda simpan saat sesi dibuat.
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
  ```

  ```ruby Ruby
  # Melanjutkan sesi cukup dengan mengirim event berikutnya ke sesi tersebut. Di produksi,
  # teruskan ID sesi yang Anda simpan saat sesi dibuat.
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
  ```
</CodeGroup>

Riwayat percakapan dipertahankan kecuali sesi dihapus secara eksplisit. Ketika sesi menjadi idle, sandbox-nya di-checkpoint. Checkpoint mempertahankan status sandbox secara penuh, termasuk sistem file, paket yang terinstal, dan file apa pun yang dibuat agen.

<Note>
  Status sandbox hanya dipertahankan selama 30 hari setelah sandbox dibuat, dan aktivitas tidak memperpanjang jangka waktu ini. Setelah 30 hari, status sandbox (file, alat yang terinstal, dan sebagainya) tidak dapat dipulihkan, dan sesi yang dilanjutkan dimulai dari sandbox baru. Jika alur kerja Anda bergantung pada isi sandbox, minta agen untuk menulis artefak penting ke [output](https://platform.claude.com/docs/id/managed-agents/define-outcomes#retrieving-deliverables) sebelum jangka waktu tersebut berakhir.
</Note>

## Menginterupsi agen

Kirim event `user.interrupt` untuk menghentikan agen di tengah eksekusi, lalu lanjutkan dengan event `user.message` untuk mengarahkannya ulang:

<CodeGroup>
  ```bash cURL
  # Agen sedang menganalisis sebuah file...
  # Interupsi dengan arahan baru:
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
  ```

  ```bash CLI
  # Agen sedang menganalisis sebuah file...
  # Interupsi dengan arahan baru:
  ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
  events:
    - type: user.interrupt
    - type: user.message
      content:
        - type: text
          text: Instead, focus on fixing the bug in line 42.
  YAML
  ```

  ```python Python
  # Agen sedang menganalisis sebuah file...
  # Interupsi dengan arahan baru:
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
  // Agen sedang menganalisis sebuah file...
  // Interupsi dengan arahan baru:
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
  ```

  ```csharp C#
  // Agen sedang menganalisis sebuah file...
  // Interupsi dengan arahan baru:
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
  // Agen sedang menganalisis sebuah file...
  // Interupsi dengan arahan baru:
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
  ```

  ```java Java
  // Agen sedang menganalisis sebuah file...
  // Interupsi dengan arahan baru:
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
  // Agen sedang menganalisis sebuah file...
  // Interupsi dengan arahan baru:
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
  # Agen sedang menganalisis sebuah file...
  # Interupsi dengan arahan baru:
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

Panggilan tersebut kembali segera setelah event dimasukkan ke antrean. Interupsi kemudian berlaku dalam urutan berikut:

1. Agen menerapkan interupsi. Sampai saat itu, `processed_at` dari interupsi tetap null dan sesi tetap `running`. Respons model yang sedang berlangsung langsung berhenti, tetapi interupsi dapat memerlukan waktu lebih lama untuk diterapkan saat panggilan alat sedang berjalan.
2. Event `user.interrupt` muncul di aliran, dan giliran yang diinterupsi berakhir dengan event `session.status_idle`.
3. Agen memulai giliran berikutnya dengan `user.message` yang Anda kirim setelah interupsi.

`stop_reason.type` dari event idle adalah `end_turn`, nilai yang sama dengan giliran yang selesai dengan sendirinya. Jika ada eksekusi workflow yang terbuka, interupsi tidak mengakhiri satu pun di antaranya. Eksekusi yang sedang berjalan dapat membuat sesi tetap `running`, sehingga event `session.status_idle` pada langkah 2 mungkin tidak tiba. Lihat [Menginterupsi sesi dengan eksekusi yang terbuka](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open).

## Mendaftar event sebelumnya

Ambil riwayat event lengkap untuk sebuah sesi:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json"
  ```

  ```bash CLI
  ant beta:sessions:events list --session-id "$SESSION_ID" --format jsonl
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
  foreach (var sessionEvent in events.Items)
  {
      Console.WriteLine($"[{sessionEvent.Json.GetProperty("type").GetString()}] {sessionEvent.ProcessedAt}");
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
      var eventJson = event._json().orElseThrow().convert(JsonNode.class);
      var processedAt = eventJson.path("processed_at");
      IO.println("[" + eventJson.get("type").asText() + "] "
          + (processedAt.isTextual() ? processedAt.asText() : "null"));
  }
  ```

  ```php PHP
  $events = $client->beta->sessions->events->list($session->id);
  foreach ($events->data as $event) {
      $processedAt = ($event->processedAt ?? null)?->format(DATE_RFC3339) ?? 'null';
      echo "[{$event->type}] {$processedAt}\n";
  }
  ```

  ```ruby Ruby
  events = client.beta.sessions.events.list(session.id)
  events.data.each { puts "[#{it.type}] #{it.processed_at}" }
  ```
</CodeGroup>

Teruskan filter `types` untuk mengembalikan hanya jenis event tertentu:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true&types[]=agent.tool_use&types[]=agent.tool_result" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:sessions:events list --session-id "$SESSION_ID" \
    --type agent.tool_use --type agent.tool_result \
    --format jsonl
  ```

  ```python Python
  events = client.beta.sessions.events.list(
      session.id,
      types=["agent.tool_use", "agent.tool_result"],
  )
  for event in events.data:
      print(f"[{event.type}] {event.processed_at}")
  ```

  ```typescript TypeScript
  const events = await client.beta.sessions.events.list(session.id, {
    types: ["agent.tool_use", "agent.tool_result"],
  });
  for (const event of events.data) {
    console.log(`[${event.type}] ${event.processed_at}`);
  }
  ```

  ```csharp C#
  var events = await client.Beta.Sessions.Events.List(session.ID, new()
  {
      Types = ["agent.tool_use", "agent.tool_result"],
  });
  foreach (var sessionEvent in events.Items)
  {
      Console.WriteLine($"[{sessionEvent.Json.GetProperty("type").GetString()}] {sessionEvent.ProcessedAt}");
  }
  ```

  ```go Go
  events, err := client.Beta.Sessions.Events.List(ctx, session.ID, anthropic.BetaSessionEventListParams{
  	Types: []anthropic.BetaManagedAgentsSessionEventType{
  		anthropic.BetaManagedAgentsSessionEventTypeAgentToolUse,
  		anthropic.BetaManagedAgentsSessionEventTypeAgentToolResult,
  	},
  })
  if err != nil {
  	panic(err)
  }
  for _, event := range events.Data {
  	fmt.Printf("[%s] %s\n", event.Type, event.ProcessedAt)
  }
  ```

  ```java Java
  var events = client.beta().sessions().events().list(
      session.id(),
      EventListParams.builder()
          .addType(BetaManagedAgentsSessionEventType.AGENT_TOOL_USE)
          .addType(BetaManagedAgentsSessionEventType.AGENT_TOOL_RESULT)
          .build());
  for (var event : events.data()) {
      event.agentToolUse().ifPresent(toolUse ->
          IO.println("[" + toolUse.type() + "] " + toolUse.processedAt()));
      event.agentToolResult().ifPresent(toolResult ->
          IO.println("[" + toolResult.type() + "] " + toolResult.processedAt()));
  }
  ```

  ```php PHP
  // Di PHP, teruskan tipe yang Anda inginkan pada EventListParams; lihat Anthropic PHP SDK.
  ```

  ```ruby Ruby
  events = client.beta.sessions.events.list(
    session.id,
    types: ["agent.tool_use", "agent.tool_result"]
  )
  events.data.each { puts "[#{it.type}] #{it.processed_at}" }
  ```
</CodeGroup>

## Mengirim pesan sistem

Pada [model yang didukung](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#supported-models), kirim event `system.message` untuk memberikan konteks tingkat sistem yang diistimewakan kepada agen. Konteks tersebut berlaku untuk giliran yang menyertainya dan semua giliran berikutnya. Gunakan ini ketika agen memerlukan panduan tingkat sistem yang diperbarui di tengah sesi, misalnya persona yang berbeda, batasan yang direvisi, atau konteks yang diambil saat runtime.

`content` dari event menerima 1–1000 item teks. Konten tersebut ditambahkan ke konteks sistem sesi sebagai giliran `role: "system"`. Konten ini tidak menggantikan "system prompt" (prompt sistem) tingkat atas, yang ditetapkan oleh field `system` pada definisi agen.

<CodeGroup>
  ```bash cURL
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
  ```

  ```bash CLI
  ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
  events:
    - type: system.message
      content:
        - type: text
          text: "The user's current timezone is America/New_York."
  YAML
  ```

  ```python Python
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
  ```

  ```typescript TypeScript
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
  ```

  ```csharp C#
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
  ```

  ```go Go
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
  ```

  ```java Java
  client.beta().sessions().events().send(
      session.id(),
      EventSendParams.builder()
          .addEvent(BetaManagedAgentsSystemMessageEventParams.builder()
              .type(BetaManagedAgentsSystemMessageEventParams.Type.SYSTEM_MESSAGE)
              .addTextContent("The user's current timezone is America/New_York.")
              .build())
          .build());
  ```

  ```php PHP
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
  ```

  ```ruby Ruby
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
  ```
</CodeGroup>

### Model yang didukung

`system.message` didukung oleh model-model berikut:

* Claude Fable 5.1
* Claude Mythos 5.1
* Claude Fable 5
* Claude Mythos 5
* Claude Opus 5.5
* Claude Opus 5
* Claude Opus 4.8
* Claude Sonnet 5.5
* Claude Haiku 5.5

Jika model utama agen tidak mendukung injeksi sistem di tengah percakapan, event ditolak dengan error validasi `model_does_not_support_mid_conversation_system`. Model subagen tidak diperiksa, karena `system.message` hanya masuk ke thread utama.

### Pesan sistem saat panggilan alat tertunda

Saat sesi idle dengan alasan berhenti `requires_action`, `system.message` harus mengikuti event hasil alat dalam permintaan yang sama. Jika dikirim sendiri atau bersama `user.message`, pesan tersebut ditolak hingga event alat yang tertunda diselesaikan.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Pratinjau respons dengan event delta" icon="text" href="https://platform.claude.com/docs/id/managed-agents/event-deltas">
    Render teks respons agen saat model masih menghasilkannya.
  </Card>

  <Card title="Memeriksa sesi dan melacak penggunaan" icon="magnifying-glass" href="https://platform.claude.com/docs/id/managed-agents/session-observability">
    Periksa sesi di Claude Console dan baca penggunaan token serta biaya daftarnya.
  </Card>

  <Card title="Berlangganan webhook" icon="link" href="https://platform.claude.com/docs/id/managed-agents/webhooks">
    Dapatkan notifikasi ketika event penting terjadi tanpa polling.
  </Card>

  <Card title="Tipe event" icon="book" href="https://platform.claude.com/docs/id/managed-agents/reference#event-types">
    Cari setiap jenis event yang dapat dikirim atau diterima sesi.
  </Card>
</CardGroup>
