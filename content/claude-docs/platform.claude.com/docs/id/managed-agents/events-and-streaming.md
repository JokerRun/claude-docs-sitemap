---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/events-and-streaming
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: a48cac48fce2a18f60078d16a71ac21985690a87110fe5e31ccd7c723cdae079
---

# Stream event sesi

Kirim event, streaming respons, dan interupsi atau alihkan sesi Anda di tengah eksekusi.

---

Komunikasi dengan Claude Managed Agents berbasis event. Anda mengirim event pengguna ke agen, dan menerima kembali event agen dan event sesi untuk melacak status.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Jenis event

Event mengalir dalam dua arah.

* **Event pengguna** dan **event sistem** adalah yang Anda kirim ke agen: event `user.*` memulai sesi dan mengarahkannya seiring berjalannya sesi; `system.message` menambahkan konteks tingkat sistem yang berlaku untuk giliran yang menyertainya dan semua giliran berikutnya.
* **Event sesi**, **event span**, dan **event agen** dikirim kepada Anda untuk observabilitas terhadap status sesi dan kemajuan agen Anda. Koneksi stream yang memilih ikut serta juga menerima [event delta](#event-deltas).

String jenis event sesi, span, agen, pengguna, dan sistem mengikuti konvensi penamaan `{domain}.{action}`. Event pratinjau delta khusus stream (`event_start`, `event_delta`) adalah pengecualian. Lihat [Jenis event](/docs/id/managed-agents/reference#event-types) di referensi untuk katalog lengkapnya.

Setiap event yang dipersistenkan menyertakan timestamp `processed_at` yang diatur saat event selesai diproses. Pada event yang Anda kirim, `processed_at` bernilai null selama event masih mengantre di belakang event-event sebelumnya. Pengecualiannya adalah `user.define_outcome`, `user.custom_tool_result`, dan `user.tool_result`, yang diproses saat diterima dan dikembalikan dengan `processed_at` yang sudah terisi.

## Mengintegrasikan event

<Tabs>
  <Tab title="Mengirim event">
    Kirim event `user.message` untuk memulai atau melanjutkan pekerjaan agen:

    <CodeGroup>
      ```bash curl
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

    Kirim event `user.interrupt` untuk menghentikan agen di tengah eksekusi, lalu lanjutkan dengan event `user.message` untuk mengalihkannya:

    <CodeGroup>
      ```bash curl
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

    Agen mengakui interupsi tersebut dan beralih ke tugas baru. Giliran yang diinterupsi berakhir dengan event `session.status_idle` yang `stop_reason`-nya adalah `end_turn`, nilai yang sama dengan giliran yang selesai dengan sendirinya; tidak ada stop reason khusus untuk interupsi.
  </Tab>

  <Tab title="Streaming event">
    Streaming event dari sesi untuk menerima pembaruan real-time saat agen bekerja. Hanya event yang dipancarkan setelah stream dibuka yang akan dikirimkan, jadi buka stream sebelum mengirim event untuk menghindari race condition.

    <CodeGroup>
      ```bash curl
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
      # Gunakan salah satu contoh SDK di grup kode ini sebagai gantinya.
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
          for (var event : events) {
              if (event.isAgentMessage()) {
                  event.asAgentMessage().content().forEach(block -> IO.print(block.text()));
              } else if (event.isSessionStatusIdle()) {
                  break;
              } else if (event.isSessionError()) {
                  // Field `message` ada di semua varian error; baca dari JSON mentah.
                  var errorMessage =
                      event.asSessionError().error()._json().orElse(null) instanceof JsonObject json
                          ? json.values().get("message").asStringOrThrow()
                          : "unknown";
                  IO.println("\n[Error: " + errorMessage + "]");
                  break;
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
        case event.type
        in :"agent.message"
          event.content.each { print it.text }
        in :"session.status_idle"
          break
        in :"session.error"
          puts "\n[Error: #{event.error&.message || "unknown"}]"
          break
        else
          # abaikan tipe event lainnya
        end
      end
      ```
    </CodeGroup>

    Untuk menyambung kembali ke sesi yang sudah ada tanpa melewatkan event:

    1. Buka stream baru.
    2. Daftarkan riwayat event lengkap untuk mengisi kumpulan ID event yang sudah terlihat.
    3. Ikuti stream langsung, lewati event apa pun yang sudah dikembalikan oleh daftar riwayat.

    <CodeGroup>
      ```bash curl
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
      # Gunakan salah satu contoh SDK di grup kode ini sebagai gantinya.
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
      for await (const event of stream) {
        // Event pratinjau (event_start/event_delta) tidak membawa id tingkat atas
        if (event.type === "event_start" || event.type === "event_delta") continue;
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
      ```

      ```csharp C#
      using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(session.ID);

      // Stream terbuka dan melakukan buffering. Daftar riwayat sebelum mengikuti event langsung.
      HashSet<string> seenEventIds = [];
      var history = await client.Beta.Sessions.Events.List(session.ID);
      await foreach (var pastEvent in history.Paginate())
      {
          seenEventIds.Add(pastEvent.ID);
      }

      // Ikuti event langsung, lewati yang sudah terlihat
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
      ```

      ```go Go
      	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
      	defer stream.Close()

      	// Stream terbuka dan melakukan buffering. Daftarkan riwayat sebelum men-tail secara langsung.
      	seenEventIDs := map[string]struct{}{}
      	history := client.Beta.Sessions.Events.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionEventListParams{})
      	for history.Next() {
      		seenEventIDs[history.Current().ID] = struct{}{}
      	}
      	if err := history.Err(); err != nil {
      		panic(err)
      	}

      	// Tail event langsung, lewati yang sudah terlihat
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
          // Stream terbuka dan melakukan buffering. Daftarkan riwayat sebelum mengikuti event langsung.
          // Setiap varian event membawa `id`; baca dari JSON mentah untuk deduplikasi antar varian.
          var seenEventIds = new HashSet<String>();
          for (var pastEvent : client.beta().sessions().events().list(session.id()).autoPager()) {
              if (pastEvent._json().orElseThrow() instanceof JsonObject json) {
                  seenEventIds.add(json.values().get("id").asStringOrThrow());
              }
          }

          // Ikuti event langsung; Set.add mengembalikan false untuk ID yang sudah terlihat, melewati replay.
          stream.stream()
              .filter(event -> event._json().orElseThrow() instanceof JsonObject json
                  && seenEventIds.add(json.values().get("id").asStringOrThrow()))
              .takeWhile(event -> !event.isSessionStatusIdle())
              .filter(BetaManagedAgentsStreamSessionEvents::isAgentMessage)
              .forEach(event -> event.asAgentMessage().content().forEach(block -> IO.print(block.text())));
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
      ```

      ```ruby Ruby
      stream = client.beta.sessions.events.stream_events(session.id)

      # Stream terbuka dan melakukan buffering. Tampilkan riwayat sebelum mengikuti event langsung.
      seen_event_ids = Set.new
      client.beta.sessions.events.list(session.id).auto_paging_each { seen_event_ids << it.id }

      # Ikuti event langsung, lewati yang sudah terlihat — Set#add? mengembalikan nil untuk duplikat
      stream.each do |event|
        next unless seen_event_ids.add?(event.id)
        case event.type
        in :"agent.message"
          event.content.each { print it.text }
        in :"session.status_idle"
          break
        else
          # abaikan tipe event lainnya
        end
      end
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Mendaftar event sebelumnya">
    Ambil riwayat event lengkap untuk sebuah sesi:

    <CodeGroup>
      ```bash curl
      curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
      ```

      ```bash CLI
      ant beta:sessions:events list --session-id "$SESSION_ID" \
        --format jsonl --transform '{type,processed_at}'
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

    Berikan filter `types` untuk mengembalikan hanya jenis event tertentu:

    <CodeGroup>
      ```bash curl
      curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true&types[]=agent.tool_use&types[]=agent.tool_result" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
      ```

      ```bash CLI
      ant beta:sessions:events list --session-id "$SESSION_ID" \
        --type agent.tool_use --type agent.tool_result \
        --format jsonl --transform '{type,processed_at}'
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
      	Types: []string{"agent.tool_use", "agent.tool_result"},
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
              .addType("agent.tool_use")
              .addType("agent.tool_result")
              .build());
      for (var event : events.data()) {
          event.agentToolUse().ifPresent(toolUse ->
              IO.println("[" + toolUse.type() + "] " + toolUse.processedAt()));
          event.agentToolResult().ifPresent(toolResult ->
              IO.println("[" + toolResult.type() + "] " + toolResult.processedAt()));
      }
      ```

      ```php PHP
      // Pemfilteran event berdasarkan tipe saat ini belum tersedia di SDK PHP.
      ```

      ```ruby Ruby
      events = client.beta.sessions.events.list(
        session.id,
        types: ["agent.tool_use", "agent.tool_result"]
      )
      events.data.each { puts "[#{it.type}] #{it.processed_at}" }
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## Event delta

Secara default, teks respons agen mencapai stream sebagai event `agent.message` yang di-buffer, masing-masing dipancarkan hanya setelah permintaan model yang menghasilkannya selesai. Event delta memungkinkan Anda merender teks tersebut secara inkremental, sebagai pratinjau langsung, sementara model masih menghasilkannya. Pratinjau bukanlah respons: pratinjau adalah alat bantu tampilan yang bersifat best-effort, dan `agent.message` yang di-buffer selalu menjadi catatan otoritatif. Klien yang mengabaikan pratinjau tetap menerima stream yang lengkap dan benar.

### Memilih ikut serta untuk pratinjau

Pratinjau bersifat opt-in per koneksi stream. Tambahkan parameter query `event_deltas[]` ke stream yang Anda baca, ulangi sekali untuk setiap jenis event yang ingin Anda pratinjau. Karena `[]` adalah pola glob shell, beri tanda kutip pada URL setiap kali Anda membangun permintaan di shell; contoh-contoh melakukan percent-encoding pada tanda kurung sebagai `%5B%5D`, yang juga berfungsi. Kedua endpoint stream menerima parameter ini: stream tingkat sesi di `GET /v1/sessions/{session_id}/events/stream`, dan stream milik setiap [thread sesi](/docs/id/managed-agents/multiagent-orchestration) di `GET /v1/sessions/{session_id}/threads/{thread_id}/stream`. Nilai yang diterima adalah `agent.message` dan `agent.thinking`; nilai lain apa pun mengembalikan error 400, begitu juga permintaan dengan lebih dari 100 nilai. Pratinjau subagen muncul di [stream thread milik subagen itu sendiri](#preview-session-thread-events).

Saat event yang dipratinjau dimulai, stream memancarkan `event_start` yang membawa jenis dan `id` event yang akan datang:

```json
{
  "type": "event_start",
  "event": {
    "type": "agent.message",
    "id": "sevt_01abc..."
  }
}
```

Untuk `agent.message`, awal tersebut diikuti oleh event `event_delta` yang membawa teks inkremental. Setiap delta menyebutkan event yang diperluasnya di `event_id` dan blok konten yang diperluasnya di `delta.index`:

```json
{
  "type": "event_delta",
  "event_id": "sevt_01abc...",
  "delta": {
    "type": "content_delta",
    "index": 0,
    "content": {
      "type": "text",
      "text": "Here is the summary"
    }
  }
}
```

Saat event `agent.thinking` dipratinjau, hanya `event_start` yang dipancarkan. Tidak ada event `event_delta` yang mengikuti, dan event `agent.thinking` yang di-buffer yang mengakhiri pratinjau tidak membawa konten pemikiran; ini adalah sinyal kemajuan, bukan pembawa konten.

Tidak seperti event yang dipersistenkan, `event_start` dan `event_delta` tidak memiliki `id` atau `processed_at` sendiri. Satu-satunya pengidentifikasi yang mereka bawa adalah `id` dari event yang mereka pratinjau.

<Note>
  Event delta menggunakan format wire yang berbeda dari [Streaming messages](/docs/id/build-with-claude/streaming), dan perbedaan ini disengaja. `agent.message` yang dipratinjau mendapatkan satu `event_start` yang hanya diikuti oleh event `event_delta`. Tidak ada event start atau stop per blok konten dan tidak ada event stop untuk event yang dipratinjau itu sendiri. Jenis delta-nya adalah `content_delta`, bukan `content_block_delta`. Kode akumulator yang ditulis untuk Messages API tidak dapat dipindahkan begitu saja tanpa perubahan.
</Note>

### Akumulasi dan rekonsiliasi

Setiap SDK yang mendukung event delta menyertakan helper akumulator yang mengunci pratinjau berdasarkan `id` event dan menangani pembukuan `index` untuk Anda (event delta saat ini belum tersedia di SDK PHP; lihat tab PHP berikutnya). Pola manual juga berfungsi di setiap bahasa saat Anda memerlukan pembukuan khusus: terapkan pada jenis event yang dihasilkan.

Dalam pola manual, perlakukan pratinjau sebagai buffer sementara dan event yang di-buffer sebagai catatan. Kunci buffer berdasarkan `(event_id, index)`. Rekonsiliasi per permintaan model: sebuah giliran dibuka dengan satu event `session.status_running`, lalu pada giliran yang selesai secara normal setiap permintaan model menghasilkan, secara berurutan, `span.model_request_start`, `event_start`, event-event `event_delta`, `agent.message` yang di-buffer, dan akhirnya [`span.model_request_end`](/docs/id/managed-agents/reference#event-types) (di tab Span events). Di wire, ini adalah bagian yang dipratinjau dari urutan tersebut, diselingi dengan event-event ter-buffer lainnya dari koneksi:

```text wrap
event_start     {"event": {"type": "agent.message", "id": "sevt_01abc..."}}
event_delta     {"event_id": "sevt_01abc...", "delta": {"type": "content_delta", "index": 0, "content": {"type": "text", "text": "..."}}}
...
agent.message   {"id": "sevt_01abc...", "content": [...]}
```

Baris `event_delta` berulang sekali per fragmen teks. Proses setiap event saat tiba:

1. Pada `event_start`, catat `id` yang diumumkan. Pengidentifikasi selalu selaras: `event_start.event.id`, setiap `event_delta.event_id`, dan `id` dari `agent.message` yang di-buffer adalah nilai yang sama.
2. Pada setiap `event_delta`, tambahkan `delta.content.text` ke entri di `(event_id, delta.index)` dan render teks yang sedang berjalan. Delta pertama untuk sebuah `index` membuat entri tersebut.
3. Saat `agent.message` yang di-buffer tiba, cocokkan berdasarkan `id`, buang pratinjau yang terakumulasi, dan render konten pesan sebagai gantinya.
4. Pada `span.model_request_end`, tutup pratinjau apa pun yang belum direkonsiliasi oleh event ter-buffer-nya. Tidak ada lagi delta yang akan datang untuknya. Jika giliran mengalami error atau diinterupsi, event yang di-buffer mungkin tidak pernah tiba; `span.model_request_end` tetap tiba.

Jaminan yang diandalkan oleh pola ini:

* Menggabungkan delta-delta sebuah pratinjau dalam urutan kedatangan, dikunci berdasarkan `(event_id, index)`, menghasilkan prefiks dari `content[index].text` di event yang di-buffer (prefiks, tidak selalu seluruh teks, karena delta dapat dibuang saat beban tinggi).
* Sebuah koneksi memancarkan paling banyak satu `event_start` per `event_id`, dan event yang di-buffer adalah hal terakhir yang dikirimkan koneksi tersebut untuk `id` itu.

<CodeGroup>
  ```bash curl
  # Aktifkan pratinjau agent.message melalui event_deltas, lalu akumulasikan secara manual.
  exec {stream}< <(
    curl --fail-with-body -sS -N \
      "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true&event_deltas%5B%5D=agent.message" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
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
        "content": [{"type": "text", "text": "In one short sentence, describe what an event delta is."}]
      }
    ]
  }
  EOF

  # Akumulasikan delta dengan kunci (id pesan, indeks konten); agent.message
  # final membawa teks lengkap, sehingga menggantikan semua pratinjau untuk id tersebut.
  declare -A preview
  while IFS= read -r -u "$stream" event_line; do
    [[ $event_line == data:* ]] || continue
    event_json=${event_line#data: }
    case $(jq -r '.type' <<<"$event_json") in
      event_start)
        preview_id=$(jq -r '.event.id' <<<"$event_json")
        printf '[event_start id=%s]\n' "$preview_id"
        ;;
      event_delta)
        preview_key=$(jq -r '.event_id + ":" + (.delta.index | tostring)' <<<"$event_json")
        preview[$preview_key]+=$(jq -r '.delta.content.text' <<<"$event_json")
        printf '[event_delta] %s\n' "${preview[$preview_key]}"
        ;;
      agent.message)
        msg_id=$(jq -r '.id' <<<"$event_json")
        for preview_key in "${!preview[@]}"; do
          [[ $preview_key == "$msg_id":* ]] && unset "preview[$preview_key]"
        done
        printf '[agent.message id=%s] ' "$msg_id"
        jq -j '.content[] | select(.type == "text") | .text' <<<"$event_json"
        printf '\n'
        ;;
      span.model_request_end)
        for preview_key in "${!preview[@]}"; do
          printf '[closing unreconciled preview for %s]\n' "${preview_key%%:*}"
        done
        preview=()
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
  # Gunakan salah satu contoh SDK di grup kode ini sebagai gantinya.
  ```

  ```python Python
  # Snapshot pratinjau, dengan kunci id event. accumulate_managed_agents_event melipat setiap
  # event_start / event_delta menjadi snapshot agent.message; agent.message
  # yang di-buffer akan menggantikannya.
  previews: dict[str, BetaManagedAgentsAgentMessageEvent] = {}

  # Aktifkan pratinjau agent.message pada koneksi ini
  with client.beta.sessions.events.stream(
      session.id, event_deltas=["agent.message"]
  ) as stream:
      client.beta.sessions.events.send(
          session.id,
          events=[
              {
                  "type": "user.message",
                  "content": [{"type": "text", "text": "Describe the repo in one sentence."}],
              },
          ],
      )

      for event in stream:
          match event.type:
              case "event_start":
                  snapshot = accumulate_managed_agents_event(None, event)
                  if snapshot is not None:
                      previews[event.event.id] = snapshot
                  print(f"event_start             {event.event.type} {event.event.id}")
              case "event_delta":
                  preview = accumulate_managed_agents_event(previews.get(event.event_id), event)
                  if preview is not None:
                      previews[event.event_id] = preview
                      text = "".join(block.text for block in preview.content)
                      print(f"event_delta             preview: {text!r}")
              case "agent.message":
                  # Event yang di-buffer adalah catatan resminya: ia menggantikan dan menutup pratinjau
                  preview = accumulate_managed_agents_event(previews.pop(event.id, None), event)
                  text = "".join(block.text for block in preview.content)
                  print(f"agent.message           {event.id} {text!r}")
              case "span.model_request_end":
                  # Tidak ada delta lagi yang akan datang. Tutup setiap pratinjau yang
                  # event buffer-nya tidak pernah tiba.
                  for event_id in previews:
                      print(f"span.model_request_end  closing preview for {event_id}")
                  previews.clear()
              case "session.status_idle":
                  break
  ```

  ```typescript TypeScript
  // Snapshot pratinjau, dikunci berdasarkan id event. `accumulateManagedAgentsEvent`
  // menggabungkan pratinjau event_start / event_delta menjadi snapshot agent.message.
  const previews = new Map<string, BetaManagedAgentsAgentMessageEvent>();

  // Aktifkan pratinjau agent.message hanya untuk koneksi ini
  const stream = await client.beta.sessions.events.stream(session.id, {
    event_deltas: ["agent.message"],
  });
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "Summarize the repo README" }]
      }
    ]
  });

  for await (const event of stream) {
    if (event.type === "event_start") {
      // 1. Catat id yang diumumkan dan buka snapshot. Delta dan
      //    event yang di-buffer membawa id yang sama.
      const preview = accumulateManagedAgentsEvent(undefined, event);
      if (preview) previews.set(event.event.id, preview);
      console.log(`event_start             ${event.event.type} ${event.event.id}`);
    } else if (event.type === "event_delta") {
      // 2. Gabungkan fragmen ke dalam snapshot dan render
      const preview = accumulateManagedAgentsEvent(previews.get(event.event_id), event);
      if (preview) {
        previews.set(event.event_id, preview);
        const text = preview.content.map((block) => block.text).join("");
        console.log(`event_delta             preview: ${JSON.stringify(text)}`);
      }
    } else if (event.type === "agent.message") {
      // 3. Event yang di-buffer adalah rekamannya: menggantikan dan menutup pratinjau
      const message = accumulateManagedAgentsEvent(previews.get(event.id), event);
      previews.delete(event.id);
      const text = message.content.map((block) => block.text).join("");
      console.log(`agent.message           ${event.id} ${JSON.stringify(text)}`);
    } else if (event.type === "span.model_request_end") {
      // 4. Tidak ada delta lagi yang akan datang. Tutup pratinjau yang belum pernah direkonsiliasi.
      for (const eventId of previews.keys()) {
        console.log(`span.model_request_end  closing preview for ${eventId}`);
      }
      previews.clear();
    } else if (event.type === "session.status_idle") {
      break;
    }
  }
  stream.controller.abort();
  ```

  ```csharp C#
  // Aktifkan delta event: event agent.message dipratinjau saat dihasilkan.
  using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(
      session.ID,
      new() { EventDeltas = [BetaManagedAgentsDeltaType.AgentMessage] }
  );
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
                      Text = "Write a haiku about event streams.",
                  },
              ],
          },
      ],
  });

  // Akumulasikan fragmen pratinjau per (id event, indeks konten). Event agent.message
  // yang di-buffer berikutnya membawa konten lengkap, sehingga menggantikan
  // pratinjau yang terakumulasi alih-alih menambahkannya.
  Dictionary<string, SortedDictionary<long, string>> previews = [];

  await foreach (var streamEvent in stream.Enumerate())
  {
      if (streamEvent.TryPickStartEvent(out var start))
      {
          // Pratinjau dibuka untuk event dengan id ini. Stream ini hanya mengaktifkan
          // delta agent.message; TryPick* mengembalikan false alih-alih melempar error,
          // sehingga tipe pratinjau lain (termasuk yang ditambahkan kemudian) dilewati.
          if (start.Event.TryPickAgentMessage(out var preview))
          {
              Console.WriteLine($"event_start             {preview.Type.Raw()} {preview.ID}");
          }
      }
      else if (streamEvent.TryPickDeltaEvent(out var delta))
      {
          // Sisipkan pada indeks baru, tambahkan pada indeks yang sudah ada
          if (!previews.TryGetValue(delta.EventID, out var fragments))
          {
              previews[delta.EventID] = fragments = [];
          }
          var index = delta.Delta.Index ?? 0;
          fragments[index] = fragments.GetValueOrDefault(index, "") + delta.Delta.Content.Text;
          Console.WriteLine($"event_delta             preview: {fragments[index]}");
      }
      else if (streamEvent.TryPickAgentMessageEvent(out var message))
      {
          // Delta bersifat best-effort: buang pratinjau dan gunakan event yang di-buffer
          previews.Remove(message.ID);
          Console.WriteLine($"agent.message           {message.ID} {string.Concat(message.Content.Select(block => block.Text))}");
      }
      else if (streamEvent.TryPickSpanModelRequestEndEvent(out _))
      {
          // Tidak ada delta lagi yang datang; tutup pratinjau apa pun yang belum direkonsiliasi.
          foreach (var eventId in previews.Keys)
          {
              Console.WriteLine($"span.model_request_end  closing preview for {eventId}");
          }
          previews.Clear();
      }
      else if (streamEvent.TryPickSessionStatusIdleEvent(out _))
      {
          break;
      }
  }
  ```

  ```go Go
  	// Aktifkan pratinjau inkremental untuk event agent.message
  	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{
  		EventDeltas: []anthropic.BetaManagedAgentsDeltaType{
  			anthropic.BetaManagedAgentsDeltaTypeAgentMessage,
  		},
  	})

  	if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
  				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  						Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  						Text: "Write a haiku about the ocean.",
  					},
  				}},
  			},
  		}},
  	}); err != nil {
  		panic(err)
  	}

  	// Akumulator menggabungkan fragmen event_start / event_delta menjadi
  	// snapshot agent.message per event-id. Nilai zero-nya siap dipakai.
  	var previews anthropic.BetaManagedAgentsEventAccumulator

  deltas:
  	for stream.Next() {
  		event := stream.Current()
  		previews.Accumulate(event)

  		switch event := event.AsAny().(type) {
  		case anthropic.BetaManagedAgentsStartEvent:
  			fmt.Printf("event_start             %s %s\n", event.Event.Type, event.Event.ID)
  		case anthropic.BetaManagedAgentsDeltaEvent:
  			fmt.Printf("event_delta             preview: %q\n", previews.AgentMessageText(event.EventID))
  		case anthropic.BetaManagedAgentsAgentMessageEvent:
  			// Event yang di-buffer membawa konten lengkap: akumulator
  			// menggantikan pratinjau dengannya
  			fmt.Printf("agent.message           %s %q\n", event.ID, previews.AgentMessageText(event.ID))
  		case anthropic.BetaManagedAgentsSpanModelRequestEndEvent:
  			// Tidak ada delta lagi untuk permintaan ini. Akumulator
  			// membuang snapshot-nya di sini, menutup pratinjau apa pun yang tidak pernah
  			// direkonsiliasi oleh agent.message yang di-buffer.
  			fmt.Println("span.model_request_end  no more deltas for this request")
  		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
  			break deltas
  		}
  	}
  	if err := stream.Err(); err != nil {
  		panic(err)
  	}
  	stream.Close()
  ```

  ```java Java
  // Teks pratinjau, dikunci oleh ID event lalu indeks konten. agent.message yang di-buffer menggantikannya.
  Map<String, Map<Long, StringBuilder>> previews = new HashMap<>();

  // Aktifkan pratinjau agent.message pada koneksi ini
  try (var stream = client.beta().sessions().events().streamStreaming(
          session.id(),
          EventStreamParams.builder()
              .addEventDelta(BetaManagedAgentsDeltaType.AGENT_MESSAGE)
              .build()
  )) {
      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                  .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                  .addTextContent("Describe the repo in one sentence.")
                  .build())
              .build()
      );

      Iterable<BetaManagedAgentsStreamSessionEvents> events = stream.stream()::iterator;
      for (var event : events) {
          if (event.isEventStart() && event.asEventStart().event().isAgentMessage()) {
              var preview = event.asEventStart().event().asAgentMessage();
              IO.println("event_start             " + preview.type().asString() + " " + preview.id());
          } else if (event.isEventDelta()) {
              var eventDelta = event.asEventDelta();
              var fragment = eventDelta.delta();
              var buffer = previews
                  .computeIfAbsent(eventDelta.eventId(), _ -> new HashMap<>())
                  .computeIfAbsent(fragment.index().orElse(0L), _ -> new StringBuilder());
              buffer.append(fragment.content().text());
              IO.println("event_delta             preview: " + buffer);
          } else if (event.isAgentMessage()) {
              // Event yang di-buffer adalah catatan resminya: buang pratinjaunya, render kontennya
              var message = event.asAgentMessage();
              previews.remove(message.id());
              var text = message.content().stream()
                  .map(block -> block.text())
                  .collect(Collectors.joining());
              IO.println("agent.message           " + message.id() + " " + text);
          } else if (event.isSpanModelRequestEnd()) {
              // Tidak ada delta lagi yang akan datang. Tutup pratinjau yang event buffer-nya tidak pernah tiba.
              previews.keySet().forEach(eventId ->
                  IO.println("span.model_request_end  closing preview for " + eventId));
              previews.clear();
          } else if (event.isSessionStatusIdle()) {
              break;
          }
      }
  }
  ```

  ```php PHP
  // Delta event saat ini belum tersedia di SDK PHP.
  ```

  ```ruby Ruby
  # Aktifkan delta event: pratinjau agent.message di-stream sebagai fragmen inkremental.
  stream = client.beta.sessions.events.stream_events(
    session.id,
    event_deltas: [Anthropic::Beta::BetaManagedAgentsDeltaType::AGENT_MESSAGE]
  )

  client.beta.sessions.events.send_(
    session.id,
    events: [{
      type: "user.message",
      content: [{type: "text", text: "Give a one-sentence project tagline."}]
    }]
  )

  # Akumulasikan fragmen pratinjau berdasarkan (event_id, index) ke dalam buffer yang
  # secara eksplisit mutable (`+""`) agar `<<` bisa menambahkan di tempat. agent.message ter-buffer dengan
  # id yang sama bersifat otoritatif dan menggantikan apa pun yang dibangun oleh delta.
  buffers = Hash.new do |by_event, event_id|
    by_event[event_id] = Hash.new { |fragments, index| fragments[index] = +"" }
  end

  stream.each do |event|
    case event.type
    in :event_start
      puts "event_start             #{event.event.type} #{event.event.id}"
    in :event_delta
      delta = event.delta
      fragment = delta.content.text
      buffers[event.event_id][delta.index || 0] << fragment
      puts "event_delta             preview: #{buffers[event.event_id][delta.index || 0].inspect}"
    in :"agent.message"
      # Ganti: buang pratinjau yang terakumulasi dan render event lengkapnya.
      buffers.delete(event.id)
      puts "agent.message           #{event.id} #{event.content.map(&:text).join.inspect}"
    in :"span.model_request_end"
      # Tidak ada delta lagi yang akan datang. Tutup pratinjau yang belum pernah direkonsiliasi.
      buffers.each_key { |event_id| puts "span.model_request_end  closing preview for #{event_id}" }
      buffers.clear
    in :"session.status_idle"
      break
    else
      # abaikan tipe event lainnya
    end
  end
  ```
</CodeGroup>

### Pratinjau event thread sesi

Dalam sesi [multiagen](/docs/id/managed-agents/multiagent-orchestration), setiap thread sesi memiliki stream event-nya sendiri di `GET /v1/sessions/{session_id}/threads/{thread_id}/stream`, dan menerima parameter `event_deltas[]` yang sama dengan nilai yang sama. Pratinjau dibatasi per thread secara desain: sebuah koneksi hanya mempratinjau thread yang sedang dibacanya. Pratinjau thread anak dikirimkan pada stream milik anak tersebut dan tidak pernah disalin-silang ke stream tingkat sesi, yang pratinjaunya tetap terbatas pada thread utama. Untuk melihat teks subagen saat model menghasilkannya, buka stream thread subagen tersebut.

Path stream thread mudah keliru: path-nya adalah `/threads/{thread_id}/stream`, bukan `/events/stream` (yang hanya ada di tingkat sesi), dan tidak ada endpoint `/threads/{thread_id}/events/stream`.

Event pratinjau itu sendiri tidak berubah. `event_start` dan `event_delta` memiliki bentuk yang sama pada stream thread seperti pada stream tingkat sesi, dan pola [akumulasi dan rekonsiliasi](#accumulate-and-reconcile) berlaku sebagaimana tertulis. Satu-satunya penyesuaian adalah pembukuan: jalankan satu instans akumulator per koneksi stream.

<CodeGroup defaultLanguage="curl">
  ```bash curl
  # Tampilkan daftar thread sesi dan pilih satu anak: thread anak memiliki
  # parent_thread_id yang tidak null, dan parent_thread_id thread utama bernilai null.
  THREAD_ID=$(
    curl --fail-with-body -sS \
      "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads?beta=true" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" |
      jq -er 'first(.data[] | select(.parent_thread_id != null)).id'
  )

  # Stream thread anak menerima parameter event_deltas[] yang sama dengan
  # stream sesi. Lakukan percent-encode pada tanda kurung (%5B%5D) dan beri tanda kutip pada URL.
  exec {stream}< <(
    curl --fail-with-body -sS -N \
      "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/stream?beta=true&event_deltas%5B%5D=agent.message" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
      -H "accept: text/event-stream"
  )

  while IFS= read -r -u "$stream" event_line; do
    [[ $event_line == data:* ]] || continue
    event_json=${event_line#data: }
    case $(jq -r '.type' <<<"$event_json") in
      event_delta)
        jq -j '.delta.content.text' <<<"$event_json"
        ;;
      agent.message)
        # Event yang di-buffer adalah catatan otoritatif; render kontennya.
        printf '\n'
        jq -j '.content[] | select(.type == "text") | .text' <<<"$event_json"
        printf '\n'
        ;;
      session.thread_status_idle)
        break
        ;;
    esac
  done
  exec {stream}<&-
  ```

  ```bash CLI
  # Daftarkan thread sesi dan pilih satu anak: thread anak membawa parent_thread_id
  # non-null, dan parent_thread_id thread utama bernilai null
  # (kueri #(parent_thread_id!=~null) pada --transform mencocokkan nilai non-null).
  THREAD_ID=$(ant beta:sessions:threads list \
    --session-id "$SESSION_ID" \
    --format raw --transform 'data.#(parent_thread_id!=~null).id' --raw-output)

  # Stream thread anak menerima parameter event_deltas yang sama dengan stream
  # sesi, satu flag --event-delta per tipe event yang akan dipratinjau. @tostr
  # mengenkode ulang setiap field teks sebagai string JSON, sehingga setiap nilai tetap
  # pada satu baris YAML dan fromjson milik jq memulihkan teks aslinya.
  transform='{type,frag:delta.content.text|@tostr,text:content.#(type=="text").text|@tostr}'
  exec {stream}< <(ant beta:sessions:threads:events stream \
    --session-id "$SESSION_ID" \
    --thread-id "$THREAD_ID" \
    --event-delta agent.message \
    --transform "$transform" \
    --format yaml)

  type=
  while IFS= read -r -u "$stream" line; do
    case "$line" in
      type:\ session.thread_status_idle) break ;;
      type:\ *) type=${line#type: } ;;
      frag:*)
        [[ $type == event_delta ]] || continue
        jq -j fromjson <<<"${line#frag: }" ;;
      text:*)
        [[ $type == agent.message ]] || continue
        # Event yang di-buffer adalah catatan otoritatif; render kontennya.
        printf '\n'
        jq -r fromjson <<<"${line#text: }" ;;
    esac
  done
  exec {stream}<&-
  ```

  ```python Python
  # Daftar thread milik sesi dan pilih satu anak: thread anak membawa parent_thread_id
  # non-null, sedangkan parent_thread_id thread utama bernilai null.
  child_thread = next(
      thread
      for thread in client.beta.sessions.threads.list(session.id)
      if thread.parent_thread_id is not None
  )

  # Stream thread anak menerima parameter event_deltas yang sama dengan
  # stream sesi.
  with client.beta.sessions.threads.events.stream(
      child_thread.id,
      session_id=session.id,
      event_deltas=["agent.message"],
  ) as stream:
      for event in stream:
          match event.type:
              case "event_delta":
                  print(event.delta.content.text, end="")
              case "agent.message":
                  # Event yang di-buffer adalah catatan otoritatif; render kontennya
                  print()
                  for block in event.content:
                      if block.type == "text":
                          print(block.text, end="")
                  print()
              case "session.thread_status_idle":
                  break
  ```

  ```typescript TypeScript
  // Tampilkan daftar thread sesi dan pilih anak: thread anak membawa parent_thread_id
  // non-null, dan parent_thread_id thread utama bernilai null.
  let childThreadId: string | undefined;
  for await (const thread of client.beta.sessions.threads.list(session.id)) {
    if (thread.parent_thread_id !== null) {
      childThreadId = thread.id;
      break;
    }
  }
  if (!childThreadId) throw new Error("No child thread found");

  // Stream thread anak menerima parameter event_deltas yang sama dengan
  // stream sesi.
  const stream = await client.beta.sessions.threads.events.stream(childThreadId, {
    session_id: session.id,
    event_deltas: ["agent.message"],
  });

  for await (const event of stream) {
    if (event.type === "event_delta") {
      process.stdout.write(event.delta.content.text);
    } else if (event.type === "agent.message") {
      // Event yang di-buffer adalah rekaman otoritatif; render kontennya.
      process.stdout.write("\n");
      const text = event.content.map((block) => block.text).join("");
      console.log(text);
    } else if (event.type === "session.thread_status_idle") {
      break;
    }
  }
  stream.controller.abort();
  ```

  ```csharp C#
  // Daftar thread sesi dan pilih satu anak: thread anak membawa parent_thread_id
  // non-null, dan parent_thread_id thread utama bernilai null.
  var threads = await client.Beta.Sessions.Threads.List(session.ID);
  var childThread = threads.Items.First(thread => thread.ParentThreadID is not null);

  // Stream thread anak menerima parameter event_deltas yang sama dengan
  // stream sesi.
  using var stream = await client.Beta.Sessions.Threads.Events.WithRawResponse.StreamStreaming(
      childThread.ID,
      new() { SessionID = session.ID, EventDeltas = [BetaManagedAgentsDeltaType.AgentMessage] }
  );

  await foreach (var streamEvent in stream.Enumerate())
  {
      if (streamEvent.TryPickDeltaEvent(out var delta))
      {
          Console.Write(delta.Delta.Content.Text);
      }
      else if (streamEvent.TryPickAgentMessageEvent(out var message))
      {
          // Event yang di-buffer adalah catatan otoritatif; render kontennya.
          Console.WriteLine();
          Console.WriteLine(string.Concat(message.Content.Select(block => block.Text)));
      }
      else if (streamEvent.TryPickSessionThreadStatusIdleEvent(out _))
      {
          break;
      }
  }
  ```

  ```go Go
  	// Daftarkan thread sesi dan pilih satu anak: thread anak memiliki parent_thread_id
  	// non-null, dan parent_thread_id thread utama bernilai null.
  	var childThreadID string
  	threads := client.Beta.Sessions.Threads.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionThreadListParams{})
  	for threads.Next() {
  		if thread := threads.Current(); thread.ParentThreadID != "" {
  			childThreadID = thread.ID
  			break
  		}
  	}
  	if err := threads.Err(); err != nil {
  		panic(err)
  	}

  	// Stream thread anak menerima parameter event_deltas yang sama dengan
  	// stream sesi; jalankan satu loop baca per koneksi stream.
  	stream := client.Beta.Sessions.Threads.Events.StreamEvents(ctx, childThreadID, anthropic.BetaSessionThreadEventStreamParams{
  		SessionID: session.ID,
  		EventDeltas: []anthropic.BetaManagedAgentsDeltaType{
  			anthropic.BetaManagedAgentsDeltaTypeAgentMessage,
  		},
  	})

  threadDeltas:
  	for stream.Next() {
  		switch event := stream.Current().AsAny().(type) {
  		case anthropic.BetaManagedAgentsDeltaEvent:
  			fmt.Print(event.Delta.Content.Text)
  		case anthropic.BetaManagedAgentsAgentMessageEvent:
  			// Event yang di-buffer adalah catatan otoritatif; render kontennya.
  			fmt.Println()
  			// daftar bertipe konkret: BetaManagedAgentsTextBlock
  			for _, block := range event.Content {
  				fmt.Print(block.Text)
  			}
  			fmt.Println()
  		case anthropic.BetaManagedAgentsSessionThreadStatusIdleEvent:
  			break threadDeltas
  		}
  	}
  	if err := stream.Err(); err != nil {
  		panic(err)
  	}
  	stream.Close()
  ```

  ```java Java
  // Daftarkan thread milik sesi dan pilih satu anak: thread anak membawa
  // parent_thread_id non-null, dan parent_thread_id thread utama bernilai null.
  var childThread = client.beta().sessions().threads().list(session.id()).autoPager().stream()
      .filter(thread -> thread.parentThreadId().isPresent())
      .findFirst()
      .orElseThrow();

  // Stream thread anak menerima parameter event_deltas yang sama dengan stream
  // sesi. Kelas params-nya punya nama sederhana yang sama dengan milik level sesi, jadi kualifikasikan.
  try (var stream = client.beta().sessions().threads().events().streamStreaming(
          childThread.id(),
          com.anthropic.models.beta.sessions.threads.events.EventStreamParams.builder()
              .sessionId(session.id())
              .addEventDelta(BetaManagedAgentsDeltaType.AGENT_MESSAGE)
              .build()
  )) {
      Iterable<BetaManagedAgentsStreamSessionThreadEvents> events = stream.stream()::iterator;
      for (var event : events) {
          if (event.isEventDelta()) {
              IO.print(event.asEventDelta().delta().content().text());
          } else if (event.isAgentMessage()) {
              // Event yang di-buffer adalah catatan otoritatif; render kontennya.
              IO.println();
              event.asAgentMessage().content().forEach(block -> IO.print(block.text()));
              IO.println();
          } else if (event.isSessionThreadStatusIdle()) {
              break;
          }
      }
  }
  ```

  ```php PHP
  // Pratinjau event thread sesi saat ini belum tersedia di SDK PHP.
  ```

  ```ruby Ruby
  # Daftarkan thread milik sesi dan pilih satu anak: thread anak memiliki
  # parent_thread_id non-null, dan parent_thread_id thread utama bernilai null.
  child_thread = client.beta.sessions.threads.list(session.id).to_enum.find { it.parent_thread_id }

  # Stream thread anak menerima parameter event_deltas yang sama dengan
  # stream sesi.
  stream = client.beta.sessions.threads.events.stream_events(
    child_thread.id,
    session_id: session.id,
    event_deltas: [Anthropic::Beta::BetaManagedAgentsDeltaType::AGENT_MESSAGE]
  )

  stream.each do |event|
    case event.type
    in :event_delta
      print event.delta.content.text
    in :"agent.message"
      # Event yang ter-buffer adalah catatan otoritatif; render kontennya.
      puts
      event.content.each { print it.text }
      puts
    in :"session.thread_status_idle"
      break
    else
      # abaikan tipe event lainnya
    end
  end
  ```
</CodeGroup>

Loop pembacaan keluar pada [`session.thread_status_idle`](/docs/id/managed-agents/reference#event-types), event yang dipancarkan saat giliran thread sesi selesai dan thread menjadi idle.

### Keterbatasan

Pratinjau disetel untuk responsivitas. Bangun dengan mempertimbangkan batasan-batasan berikut:

* **Best effort:** Saat beban tinggi, server dapat membuang delta untuk sebuah event. Saat itu terjadi, Anda menerima prefiks teks yang berkesinambungan dan kemudian tidak ada delta lebih lanjut untuk event tersebut. `agent.message` yang di-buffer tetap tiba secara lengkap. Jangan pernah memperlakukan pratinjau yang terakumulasi sebagai final.
* **Tidak ada replay saat menyambung kembali:** Delta hanya dikirimkan ke koneksi yang memilih ikut serta, selama koneksi tersebut terbuka. Ini berlaku untuk stream tingkat sesi dan untuk setiap stream thread sesi, dan koneksi yang dibuka setelah permintaan model dimulai tidak menerima delta untuk event yang sedang berjalan tersebut. Jika stream terputus, ikuti [prosedur penyambungan kembali](#integrating-events) di tab Streaming event: buka kembali stream dan daftarkan riwayat event. Riwayat tersebut mencakup event ter-buffer apa pun yang dipancarkan saat Anda terputus, termasuk `agent.message` yang ditunggu oleh pratinjau Anda. Tidak ada cara untuk meminta ulang delta yang terlewat.
* **Satu thread, teks saja:** Pratinjau mencakup teks asisten pada thread yang sedang dibaca oleh koneksi. Penggunaan alat, hasil alat, hasil MCP, dan aktivitas pada [thread sesi](/docs/id/managed-agents/multiagent-orchestration) lain mana pun tidak pernah dipratinjau pada koneksi tersebut.
* **`agent.thinking` hanya start:** Pratinjau `agent.thinking` hanya memancarkan `event_start` sebagai sinyal bahwa blok pemikiran telah dimulai; tidak ada event `event_delta` yang mengikutinya.
* **Tidak pernah dipersistenkan:** `event_start` dan `event_delta` hanya ada di stream langsung. Keduanya tidak muncul di riwayat event sesi (`GET /v1/sessions/{session_id}/events`) atau di riwayat event thread sesi mana pun.

### Pemecahan masalah pratinjau

Jika stream tidak berperilaku seperti yang Anda harapkan:

| Yang Anda lihat                                                              | Artinya                                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stream dengan event ter-buffer tetapi tanpa `event_start` atau `event_delta` | Koneksi yang Anda baca tidak memilih ikut serta (`event_deltas[]` berlaku per koneksi, bukan per sesi), atau giliran tersebut tidak pernah menyentuh thread yang Anda streaming. Pratinjau dibatasi per thread, jadi daftarkan thread-thread sesi (`GET /v1/sessions/{session_id}/threads`) untuk menemukan mana yang berjalan. |
| 404 pada URL stream                                                          | Path atau ID salah, atau permintaan sama sekali tidak membawa header beta managed-agents. Endpoint thread dibatasi oleh beta, jadi tanpa header tersebut endpoint-nya tidak ada.                                                                                                                                                |
| 400 yang menyebutkan `event_deltas`                                          | Hanya `agent.message` dan `agent.thinking` yang diterima.                                                                                                                                                                                                                                                                       |

## Skenario tambahan

### Menangani panggilan alat kustom

Saat agen memanggil [alat kustom](/docs/id/managed-agents/tools#custom-tools):

1. Sesi memancarkan event `agent.custom_tool_use` yang berisi nama alat dan input.
2. Sesi berhenti sementara dengan event `session.status_idle` yang berisi `stop_reason: requires_action`. ID event yang memblokir ada di array `stop_reason.event_ids`.
3. Eksekusi alat di sistem Anda dan kirim event `user.custom_tool_result` untuk masing-masing, dengan meneruskan ID event di parameter `custom_tool_use_id` bersama dengan konten hasilnya.
4. Setelah semua event yang memblokir terselesaikan, sesi bertransisi kembali ke `running`.

<CodeGroup>
  ```bash curl
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
          # Jalankan alat dan kirim hasilnya kembali
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
                          # Cari event custom tool use dan jalankan
                          tool_event = events_by_id[event_id]
                          result = call_tool(tool_event.name, tool_event.input)

                          # Kirim hasilnya kembali
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
    if (event.type !== "session.status_idle") continue;
    if (event.stop_reason.type === "end_turn") break;
    if (event.stop_reason.type !== "requires_action") continue;

    for (const eventId of event.stop_reason.event_ids) {
      // Cari event custom tool use dan jalankan
      const toolEvent = eventsById.get(eventId);
      if (!toolEvent) continue;
      const result = await callTool(toolEvent.name, toolEvent.input);

      // Kirim hasilnya kembali
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
  ```

  ```csharp C#
  await foreach (var streamEvent in client.Beta.Sessions.Events.StreamStreaming(session.ID))
  {
      if (streamEvent.Value is not BetaManagedAgentsSessionStatusIdleEvent idle) continue;

      if (idle.StopReason?.Value is BetaManagedAgentsSessionRequiresAction requiresAction)
      {
          foreach (var eventId in requiresAction.EventIds)
          {
              // Cari event custom tool use dan jalankan
              var toolEvent = eventsById[eventId];
              var result = await CallTool(toolEvent.Name, toolEvent.Input);

              // Kirim hasilnya kembali
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
  				// Cari event custom tool use dan jalankan
  				toolEvent := eventsByID[eventID]
  				result := callTool(toolEvent.Name, toolEvent.Input)
  				// Kirim hasilnya kembali
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
  ```

  ```java Java
  try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
      stream.stream()
          .filter(BetaManagedAgentsStreamSessionEvents::isSessionStatusIdle)
          .map(idleEvent -> idleEvent.asSessionStatusIdle().stopReason())
          .takeWhile(stopReason -> !stopReason.isEndTurn())
          .filter(stopReason -> stopReason.isRequiresAction())
          .flatMap(stopReason -> stopReason.asRequiresAction().eventIds().stream())
          .forEach(eventId -> {
              // Cari event custom tool use dan jalankan
              var toolEvent = eventsById.get(eventId);
              var result = callTool(toolEvent.name(), toolEvent.input());

              // Kirim hasilnya kembali
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
  ```

  ```php PHP
  $stream = $client->beta->sessions->events->streamStream($session->id);

  foreach ($stream as $event) {
      if ($event->type === 'session.status_idle' && $event->stopReason) {
          if ($event->stopReason->type === 'requires_action') {
              foreach ($event->stopReason->eventIDs as $eventId) {
                  // Cari event penggunaan alat kustom lalu eksekusi
                  $toolEvent = $eventsById[$eventId];
                  $result = callTool($toolEvent->name, $toolEvent->input);

                  // Kirim kembali hasilnya
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
        # Cari event custom tool use dan jalankan
        tool_event = events_by_id[event_id]
        result = call_tool.call(tool_event.name, tool_event.input)
        # Kirim hasilnya kembali
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

Saat [kebijakan izin](/docs/id/managed-agents/permission-policies) memerlukan konfirmasi sebelum alat dieksekusi:

1. Sesi memancarkan event `agent.tool_use` atau `agent.mcp_tool_use`.
2. Sesi berhenti sementara dengan event `session.status_idle` yang berisi `stop_reason: requires_action`. ID event yang memblokir ada di array `stop_reason.event_ids`.
3. Kirim event `user.tool_confirmation` untuk masing-masing, dengan meneruskan ID event di parameter `tool_use_id`. Atur `result` ke `"allow"` atau `"deny"`. Gunakan `deny_message` untuk menjelaskan penolakan.
4. Setelah semua event yang memblokir terselesaikan, sesi bertransisi kembali ke `running`.

<CodeGroup>
  ```bash curl
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
      if ($event->type === 'session.status_idle' && $event->stopReason) {
          if ($event->stopReason->type === 'requires_action') {
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
        # Setujui pemanggilan alat yang tertunda
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

### Melanjutkan sesi yang idle

Sesi tetap ada di antara interaksi. Riwayat percakapan dipertahankan kecuali sesi dihapus secara eksplisit. Saat sesi menjadi idle, sandbox-nya di-checkpoint, mempertahankan seluruh status sandbox, termasuk filesystem, paket yang terpasang, dan file apa pun yang dibuat agen. Ini memungkinkan Anda melanjutkan dengan bersih dari ketidakaktifan.

<Note>
  Meskipun riwayat sesi dipersistenkan hingga dihapus, status sandbox hanya dipertahankan selama 30 hari setelah sandbox dibuat. Aktivitas tidak memperpanjang jendela ini: setelah 30 hari status sandbox (file, alat yang terpasang, dan sebagainya) tidak dapat dipulihkan, dan sesi yang dilanjutkan dimulai dari sandbox yang baru. Jika alur kerja Anda bergantung pada isi sandbox, minta agen menulis artefak penting ke [output](/docs/id/managed-agents/define-outcomes#retrieving-deliverables) sebelum jendela tersebut berakhir.
</Note>

Untuk melanjutkan sesi, kirim event `user.message` ke sesi tersebut seperti biasa:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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

### Mengirim pesan sistem

<Note>
  `system.message` saat ini didukung oleh Claude Opus 4.8, Claude Sonnet 5, Claude Fable 5, dan Claude Mythos 5. Jika model utama agen tidak mendukung injeksi sistem di tengah percakapan, event tersebut ditolak dengan error validasi `model_does_not_support_mid_conversation_system`; model subagen tidak diperiksa, karena `system.message` hanya masuk ke thread utama.
</Note>

Kirim event `system.message` untuk memberi agen konteks tingkat sistem yang memiliki hak istimewa yang berlaku untuk giliran yang menyertainya dan semua giliran berikutnya. Tidak seperti field `system` pada definisi agen (yang mengatur prompt sistem tingkat atas), konten `system.message` ditambahkan ke konteks sistem sesi sebagai giliran `role: "system"` alih-alih menggantikan prompt tersebut. Gunakan ini saat agen memerlukan panduan tingkat sistem yang diperbarui di tengah sesi: persona yang berbeda, batasan yang direvisi, atau konteks yang diambil saat runtime yang harus membentuk perilaku model ke depannya.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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

Saat sesi idle dengan `stop_reason: requires_action`, `system.message` hanya diterima jika mengikuti event hasil alat dalam permintaan yang sama; jika dikirim sendiri atau bersama `user.message`, event tersebut ditolak hingga event alat yang tertunda terselesaikan. `content` menerima 1–1000 item teks.

### Melacak penggunaan

Objek sesi menyertakan field `usage` dengan statistik token kumulatif. Ambil sesi setelah menjadi idle untuk membaca total terbaru, dan gunakan untuk melacak biaya, menegakkan anggaran, atau memantau konsumsi.

```json
{
  "id": "sesn_01...",
  "status": "idle",
  "usage": {
    "input_tokens": 5000,
    "output_tokens": 3200,
    "cache_read_input_tokens": 20000,
    "cache_creation": {
      "ephemeral_5m_input_tokens": 2000,
      "ephemeral_1h_input_tokens": 0
    }
  }
}
```

`input_tokens` melaporkan token input yang tidak di-cache dan `output_tokens` melaporkan total token output di semua panggilan model dalam sesi. Field `cache_read_input_tokens` melaporkan token yang dibaca dari cache prompt, dan objek `cache_creation` merinci token pembuatan cache berdasarkan masa hidup cache (`ephemeral_5m_input_tokens` dan `ephemeral_1h_input_tokens`). Entri cache menggunakan TTL 5 menit secara default, jadi giliran yang berurutan dalam jendela tersebut mendapat manfaat dari pembacaan cache, yang mengurangi biaya per token.

## Observabilitas Console

Console menyediakan tampilan timeline visual dari sesi agen Anda. Navigasikan ke bagian Claude Managed Agents di Console untuk melihat:

* **Daftar sesi:** Semua sesi dengan status, waktu pembuatan, dan agennya
* **Tampilan tracing:** Tampilan kronologis event (konten, timestamp, penggunaan token) dalam sebuah sesi. Tampilan tracing hanya dapat diakses oleh Developer dan Admin.
* **Eksekusi alat:** Detail setiap panggilan alat dan hasilnya

## Tips debugging

* **Periksa event sesi:** Error sesi disampaikan melalui event `session.error`
* **Tinjau hasil alat:** Kegagalan eksekusi alat sering menjelaskan perilaku agen yang tidak terduga
* **Lacak penggunaan token:** Pantau konsumsi token untuk mengoptimalkan prompt dan mengurangi biaya
* **Gunakan prompt sistem:** Tambahkan instruksi logging ke prompt sistem agar agen menjelaskan penalarannya
* **Pecahkan masalah pratinjau:** Jika stream yang memilih ikut serta untuk event delta tidak berperilaku seperti yang Anda harapkan, lihat [Pemecahan masalah pratinjau](#troubleshoot-previews)
