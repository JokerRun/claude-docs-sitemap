---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/event-deltas
fetched_at: 2026-10-09T02:29:51.005508Z
sha256: d11fbfc2d14f26f78f4df00715f89e592c45277ea5a0ec401375dd3592309652
---

---
title: Pratinjau respons dengan event delta
url: https://platform.claude.com/docs/id/managed-agents/event-deltas
description: Tampilkan teks respons agen sebagai pratinjau langsung saat model masih menghasilkannya.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Secara default, teks respons agen mencapai [aliran event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) sebagai event `agent.message` yang di-buffer. Masing-masing dipancarkan hanya setelah permintaan model yang menghasilkannya selesai. Event delta memungkinkan Anda menampilkan teks tersebut secara bertahap, sebagai pratinjau langsung, saat model masih menghasilkannya.

Pratinjau adalah alat bantu tampilan berbasis "best-effort" (upaya terbaik), dan `agent.message` yang di-buffer selalu menjadi catatan otoritatif. Klien yang mengabaikan pratinjau tetap menerima aliran yang lengkap dan benar.

## Mengaktifkan pratinjau

Pratinjau bersifat opt-in per koneksi aliran. Tambahkan parameter kueri `event_deltas[]` ke aliran yang Anda baca, dan ulangi sekali untuk setiap jenis event yang ingin Anda pratinjau. Nilai yang diterima adalah `agent.message` dan `agent.thinking`. Nilai lain apa pun mengembalikan error 400, begitu pula permintaan dengan lebih dari 100 nilai.

Kedua endpoint aliran menerima parameter ini:

* **Aliran tingkat sesi:** `GET /v1/sessions/{session_id}/events/stream`
* **Aliran thread sesi:** `GET /v1/sessions/{session_id}/threads/{thread_id}/stream`

Pratinjau subagen muncul di [aliran thread milik subagen tersebut](https://platform.claude.com/docs/id/managed-agents/event-deltas#preview-session-thread-events).

`[]` adalah pola glob shell, jadi beri tanda kutip pada URL setiap kali Anda membangun permintaan di shell. Contoh-contoh ini melakukan percent-encoding pada tanda kurung siku sebagai `%5B%5D`, yang juga berfungsi.

### Event pratinjau

Ketika event yang dipratinjau dimulai, aliran memancarkan `event_start` yang membawa jenis dan `id` event yang akan datang:

```json
{
  "type": "event_start",
  "event": {
    "type": "agent.message",
    "id": "sevt_01abc..."
  }
}
```

Untuk `agent.message`, start tersebut diikuti oleh event `event_delta` yang membawa teks bertahap. Setiap delta menyebutkan event yang diperluasnya di `event_id` dan blok konten yang diperluasnya di `delta.index`:

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

Untuk `agent.thinking`, hanya `event_start` yang dipancarkan, sebagai sinyal bahwa blok thinking telah dimulai. Tidak ada event `event_delta` yang menyusul. Event `agent.thinking` yang di-buffer yang mengakhiri pratinjau adalah sinyal kemajuan dan tidak membawa konten thinking.

Tidak seperti event yang dipersistenkan, `event_start` dan `event_delta` tidak memiliki `id` atau `processed_at` sendiri. Satu-satunya pengenal yang mereka bawa adalah `id` dari event yang mereka pratinjau. String jenisnya juga merupakan pengecualian dari konvensi penamaan `{domain}.{action}` pada event yang dipersistenkan.

<Note>
  Event delta menggunakan format wire yang berbeda dari [Streaming pesan](https://platform.claude.com/docs/id/build-with-claude/streaming), dan perbedaan ini disengaja. `agent.message` yang dipratinjau mendapatkan satu `event_start` yang hanya diikuti oleh event `event_delta`. Tidak ada event start atau stop per blok konten dan tidak ada event stop untuk event yang dipratinjau itu sendiri. Jenis deltanya adalah `content_delta`, bukan `content_block_delta`. Kode akumulator yang ditulis untuk Messages API tidak dapat dipakai begitu saja tanpa perubahan.
</Note>

## Mengakumulasi dan merekonsiliasi

Setiap SDK yang mendukung event delta menyertakan [helper akumulator](https://platform.claude.com/docs/id/managed-agents/event-deltas#sdk-accumulator-helpers) yang menangani pencatatan `index` untuk Anda. Pola manual di bagian ini berfungsi di setiap bahasa ketika Anda memerlukan pencatatan kustom. Terapkan pola ini pada jenis event yang dihasilkan.

Dalam pola manual, simpan teks pratinjau dalam map sementara dengan kunci `(event_id, index)`, dan perlakukan event yang di-buffer sebagai catatan. Rekonsiliasikan keduanya per permintaan model.

Sebuah giliran dibuka dengan satu event `session.status_running`. Pada giliran yang selesai secara normal, setiap permintaan model kemudian menghasilkan event-event berikut, secara berurutan:

1. `span.model_request_start`
2. `event_start`
3. Event-event `event_delta`
4. `agent.message` yang di-buffer
5. [`span.model_request_end`](https://platform.claude.com/docs/id/managed-agents/reference#event-types) (di tab Event span)

Di wire, ini adalah bagian yang dipratinjau dari urutan tersebut, diselingi dengan event ter-buffer lain milik koneksi:

```text wrap
event_start     {"event": {"type": "agent.message", "id": "sevt_01abc..."}}
event_delta     {"event_id": "sevt_01abc...", "delta": {"type": "content_delta", "index": 0, "content": {"type": "text", "text": "..."}}}
...
agent.message   {"id": "sevt_01abc...", "content": [...]}
```

Baris `event_delta` berulang sekali per fragmen teks. Proses setiap event saat tiba:

1. Pada `event_start`, catat `id` yang diumumkan. Pengenal-pengenalnya selalu selaras: `event_start.event.id`, setiap `event_delta.event_id`, dan `id` dari `agent.message` yang di-buffer adalah nilai yang sama.
2. Pada setiap `event_delta`, tambahkan `delta.content.text` ke entri di `(event_id, delta.index)` dan tampilkan teks yang telah terakumulasi sejauh ini. Delta pertama untuk sebuah `index` membuat entri tersebut.
3. Ketika `agent.message` yang di-buffer tiba, cocokkan berdasarkan `id`, buang pratinjau yang terakumulasi, dan tampilkan konten pesan sebagai gantinya.
4. Pada `span.model_request_end`, tutup pratinjau apa pun yang belum direkonsiliasi oleh event ter-buffer-nya. Tidak ada lagi delta yang akan datang untuknya. Jika giliran mengalami error atau diinterupsi, event yang di-buffer mungkin tidak pernah tiba, tetapi `span.model_request_end` tetap tiba.

Pola ini bergantung pada dua jaminan:

* Menggabungkan delta-delta pratinjau sesuai urutan kedatangan, dengan kunci `(event_id, index)`, menghasilkan prefiks dari `content[index].text` di event yang di-buffer. Ini belum tentu keseluruhan teks, karena delta mungkin [dibuang saat beban tinggi](https://platform.claude.com/docs/id/managed-agents/event-deltas#limitations).
* Sebuah koneksi memancarkan paling banyak satu `event_start` per `event_id`, dan event yang di-buffer adalah hal terakhir yang dikirimkan koneksi tersebut untuk `id` itu.

### Helper akumulator SDK

Helper setiap SDK menangani pencatatan `index`. Helper Go, Java, Ruby, dan C# juga menyimpan pratinjau yang sedang diakumulasi dengan kunci `id` event. Dengan helper Python, TypeScript, dan PHP, kelola map tersebut sendiri dan gabungkan setiap delta ke dalam entri untuk `id`-nya.

Contoh-contoh berikut mengaktifkan pratinjau `agent.message` dan merekonsiliasinya dengan event yang di-buffer:

<CodeGroup>
  ```bash cURL
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
  # Gunakan salah satu contoh SDK dalam grup kode ini sebagai gantinya.
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

  deltas: for await (const event of stream) {
    switch (event.type) {
      case "event_start": {
        // 1. Catat id yang diumumkan dan buka snapshot. Delta dan
        //    event yang di-buffer membawa id yang sama.
        const preview = accumulateManagedAgentsEvent(undefined, event);
        if (preview) previews.set(event.event.id, preview);
        console.log(`event_start             ${event.event.type} ${event.event.id}`);
        break;
      }
      case "event_delta": {
        // 2. Gabungkan fragmen ke dalam snapshot lalu render
        const preview = accumulateManagedAgentsEvent(previews.get(event.event_id), event);
        if (preview) {
          previews.set(event.event_id, preview);
          const text = preview.content
            .map((block) => (block.type === "text" ? block.text : ""))
            .join("");
          console.log(`event_delta             preview: ${JSON.stringify(text)}`);
        }
        break;
      }
      case "agent.message": {
        // 3. Event yang di-buffer adalah catatannya: ia menggantikan dan menutup pratinjau
        const message = accumulateManagedAgentsEvent(previews.get(event.id), event);
        previews.delete(event.id);
        const text = message.content
          .map((block) => (block.type === "text" ? block.text : ""))
          .join("");
        console.log(`agent.message           ${event.id} ${JSON.stringify(text)}`);
        break;
      }
      case "span.model_request_end":
        // 4. Tidak ada delta lagi yang akan datang. Tutup pratinjau yang belum pernah direkonsiliasi.
        for (const eventId of previews.keys()) {
          console.log(`span.model_request_end  closing preview for ${eventId}`);
        }
        previews.clear();
        break;
      case "session.status_idle":
        break deltas;
    }
  }
  stream.controller.abort();
  ```

  ```csharp C#
  // Aktifkan delta event: event agent.message dipratinjau saat diproduksi.
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

  // Akumulasikan fragmen pratinjau per (id event, indeks konten). Event
  // agent.message ter-buffer yang menyusul membawa konten lengkap, jadi ia
  // menggantikan pratinjau yang terakumulasi, bukan menambahkannya.
  Dictionary<string, SortedDictionary<long, string>> previews = [];

  await foreach (var streamEvent in stream.Enumerate())
  {
      if (streamEvent.TryPickStartEvent(out var start))
      {
          // Pratinjau dibuka untuk event dengan id ini. Stream ini hanya mengaktifkan
          // delta agent.message; TryPick* mengembalikan false alih-alih throw,
          // jadi tipe pratinjau lain (termasuk yang ditambahkan nanti) dilewati.
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
          // Delta bersifat best-effort: buang pratinjau dan gunakan event ter-buffer
          previews.Remove(message.ID);
          var text = string.Concat(message.Content.Select(block =>
              block.TryPickBetaManagedAgentsTextBlock(out var textBlock) ? textBlock.Text : ""));
          Console.WriteLine($"agent.message           {message.ID} {text}");
      }
      else if (streamEvent.TryPickSpanModelRequestEndEvent(out _))
      {
          // Tidak ada delta lagi; tutup pratinjau yang belum pernah direkonsiliasi.
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
  	// snapshot agent.message per-event-id. Nilai nol (zero value) siap digunakan.
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
  			// mengganti pratinjau dengannya
  			fmt.Printf("agent.message           %s %q\n", event.ID, previews.AgentMessageText(event.ID))
  		case anthropic.BetaManagedAgentsSpanModelRequestEndEvent:
  			// Tidak ada delta lagi untuk permintaan ini. Akumulator
  			// membuang snapshot-nya di sini, menutup pratinjau yang tidak pernah
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
      deltas:
      for (var event : events) {
          switch (event.type().value()) {
              case EVENT_START -> {
                  if (event.asEventStart().event().isAgentMessage()) {
                      var preview = event.asEventStart().event().asAgentMessage();
                      IO.println("event_start             " + preview.type().asString() + " " + preview.id());
                  }
              }
              case EVENT_DELTA -> {
                  var eventDelta = event.asEventDelta();
                  var fragment = eventDelta.delta();
                  var buffer = previews
                      .computeIfAbsent(eventDelta.eventId(), _ -> new HashMap<>())
                      .computeIfAbsent(fragment.index().orElse(0L), _ -> new StringBuilder());
                  buffer.append(fragment.content().text());
                  IO.println("event_delta             preview: " + buffer);
              }
              case AGENT_MESSAGE -> {
                  // Event yang di-buffer adalah catatannya: buang pratinjaunya, render kontennya
                  var message = event.asAgentMessage();
                  previews.remove(message.id());
                  var text = message.content().stream()
                      .flatMap(block -> block.text().stream())
                      .map(textBlock -> textBlock.text())
                      .collect(Collectors.joining());
                  IO.println("agent.message           " + message.id() + " " + text);
              }
              case SPAN_MODEL_REQUEST_END -> {
                  // Tidak ada delta lagi yang akan datang. Tutup pratinjau yang event buffer-nya tidak pernah tiba.
                  previews.keySet().forEach(eventId ->
                      IO.println("span.model_request_end  closing preview for " + eventId));
                  previews.clear();
              }
              case SESSION_STATUS_IDLE -> {
                  break deltas;
              }
          }
      }
  }
  ```

  ```php PHP
  // Di PHP, atur eventDeltas pada EventStreamParams dan akumulasikan dengan Anthropic\Lib\Sessions\EventAccumulator.
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
    case event
    when Anthropic::Beta::BetaManagedAgentsStartEvent
      puts "event_start             #{event.event.type} #{event.event.id}"
    when Anthropic::Beta::BetaManagedAgentsDeltaEvent
      delta = event.delta
      fragment = delta.content.text
      buffers[event.event_id][delta.index || 0] << fragment
      puts "event_delta             preview: #{buffers[event.event_id][delta.index || 0].inspect}"
    when Anthropic::Beta::Sessions::BetaManagedAgentsAgentMessageEvent
      # Ganti: buang pratinjau yang terakumulasi dan render event lengkapnya.
      buffers.delete(event.id)
      puts "agent.message           #{event.id} #{event.content.map(&:text).join.inspect}"
    when Anthropic::Beta::Sessions::BetaManagedAgentsSpanModelRequestEndEvent
      # Tidak ada delta lagi yang akan datang. Tutup pratinjau yang belum pernah direkonsiliasi.
      buffers.each_key { |event_id| puts "span.model_request_end  closing preview for #{event_id}" }
      buffers.clear
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusIdleEvent
      break
    else
      # abaikan tipe event lainnya
    end
  end
  ```
</CodeGroup>

## Pratinjau event thread sesi

Dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), setiap thread sesi memiliki aliran event sendiri. Aliran ini menerima parameter `event_deltas[]` yang sama dengan nilai yang sama.

Sebuah koneksi hanya mempratinjau thread yang sedang dibacanya. Aliran tingkat sesi mempratinjau thread utama, dan pratinjau thread anak tidak pernah diposting silang ke sana. Untuk melihat teks subagen saat model menghasilkannya, buka aliran thread subagen tersebut.

Path aliran thread diakhiri dengan `/threads/{thread_id}/stream`. `/events/stream` hanya ada di tingkat sesi, jadi tidak ada endpoint `/threads/{thread_id}/events/stream`.

`event_start` dan `event_delta` memiliki bentuk yang sama di aliran thread seperti di aliran tingkat sesi, dan pola [mengakumulasi dan merekonsiliasi](https://platform.claude.com/docs/id/managed-agents/event-deltas#accumulate-and-reconcile) berlaku sebagaimana tertulis. Jalankan satu instans akumulator per koneksi aliran.

<CodeGroup>
  ```bash cURL
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
  # Daftarkan thread sesi dan pilih satu anak: thread anak membawa
  # parent_thread_id non-null, dan parent_thread_id thread utama bernilai null
  # (kueri #(parent_thread_id!=~null) milik --transform cocok dengan nilai non-null).
  THREAD_ID=$(ant beta:sessions:threads list \
    --session-id "$SESSION_ID" \
    --format raw --transform 'data.#(parent_thread_id!=~null).id' --raw-output)

  # Stream thread anak menerima parameter event_deltas yang sama dengan
  # stream sesi, satu flag --event-delta per jenis event untuk dipratinjau. @tostr
  # mengodekan ulang tiap field teks sebagai string JSON, sehingga setiap nilai tetap di satu
  # baris YAML dan fromjson milik jq memulihkan teks aslinya.
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

  threadDeltas: for await (const event of stream) {
    switch (event.type) {
      case "event_delta":
        process.stdout.write(event.delta.content.text);
        break;
      case "agent.message": {
        // Event yang di-buffer adalah catatan otoritatif; render kontennya.
        process.stdout.write("\n");
        const text = event.content
          .map((block) => (block.type === "text" ? block.text : ""))
          .join("");
        console.log(text);
        break;
      }
      case "session.thread_status_idle":
        break threadDeltas;
    }
  }
  stream.controller.abort();
  ```

  ```csharp C#
  // Daftar thread sesi dan pilih satu anak: thread anak memiliki
  // parent_thread_id non-null, dan parent_thread_id thread utama adalah null.
  var threads = await client.Beta.Sessions.Threads.List(session.ID);
  var childThread = threads.Items.First(thread => thread.ParentThreadID is not null);

  // Stream thread anak menerima parameter event_deltas yang sama seperti
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
          // Event ter-buffer adalah catatan otoritatif; render kontennya.
          Console.WriteLine();
          var text = string.Concat(message.Content.Select(block =>
              block.TryPickBetaManagedAgentsTextBlock(out var textBlock) ? textBlock.Text : ""));
          Console.WriteLine(text);
      }
      else if (streamEvent.TryPickSessionThreadStatusIdleEvent(out _))
      {
          break;
      }
  }
  ```

  ```go Go
  	// Daftar thread sesi dan pilih satu anak: thread anak memiliki
  	// parent_thread_id non-null, dan parent_thread_id thread utama adalah null.
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

  	// Stream thread anak menerima parameter event_deltas yang sama seperti
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
  // Daftar thread sesi dan pilih satu child: child thread membawa parent_thread_id
  // yang non-null, dan parent_thread_id thread utama bernilai null.
  var childThread = client.beta().sessions().threads().list(session.id()).autoPager().stream()
      .filter(thread -> thread.parentThreadId().isPresent())
      .findFirst()
      .orElseThrow();

  // Stream child thread menerima parameter event_deltas yang sama dengan stream sesi.
  // Kelas params-nya berbagi nama sederhana dengan yang level sesi, jadi kualifikasikan.
  try (var stream = client.beta().sessions().threads().events().streamStreaming(
          childThread.id(),
          com.anthropic.models.beta.sessions.threads.events.EventStreamParams.builder()
              .sessionId(session.id())
              .addEventDelta(BetaManagedAgentsDeltaType.AGENT_MESSAGE)
              .build()
  )) {
      Iterable<BetaManagedAgentsStreamSessionThreadEvents> events = stream.stream()::iterator;
      threadDeltas:
      for (var event : events) {
          switch (event.type().value()) {
              case EVENT_DELTA -> IO.print(event.asEventDelta().delta().content().text());
              case AGENT_MESSAGE -> {
                  // Event yang di-buffer adalah catatan otoritatif; render kontennya.
                  IO.println();
                  event.asAgentMessage().content().forEach(block -> block.text().ifPresent(textBlock -> IO.print(textBlock.text())));
                  IO.println();
              }
              case SESSION_THREAD_STATUS_IDLE -> {
                  break threadDeltas;
              }
          }
      }
  }
  ```

  ```php PHP
  // Di PHP, atur eventDeltas pada EventStreamParams thread dan akumulasikan dengan Anthropic\Lib\Sessions\EventAccumulator.
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
    case event
    when Anthropic::Beta::BetaManagedAgentsDeltaEvent
      print event.delta.content.text
    when Anthropic::Beta::Sessions::BetaManagedAgentsAgentMessageEvent
      # Event yang ter-buffer adalah catatan otoritatif; render kontennya.
      puts
      event.content.each { print it.text }
      puts
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionThreadStatusIdleEvent
      break
    else
      # abaikan tipe event lainnya
    end
  end
  ```
</CodeGroup>

Loop pembacaan keluar pada [`session.thread_status_idle`](https://platform.claude.com/docs/id/managed-agents/reference#event-types), event yang dipancarkan ketika giliran thread sesi selesai dan thread menjadi idle.

## Keterbatasan

* **Best effort:** Saat beban tinggi, server mungkin membuang delta untuk sebuah event. Ketika itu terjadi, Anda menerima prefiks teks yang berkesinambungan lalu tidak ada delta lebih lanjut untuk event tersebut. `agent.message` yang di-buffer tetap tiba secara lengkap. Jangan pernah memperlakukan pratinjau yang terakumulasi sebagai final.
* **Tidak ada replay saat menyambung ulang:** Delta hanya dikirimkan ke koneksi yang mengaktifkannya, selama koneksi tersebut terbuka. Ini berlaku sama untuk aliran tingkat sesi maupun setiap aliran thread sesi. Koneksi yang dibuka setelah permintaan model dimulai tidak menerima delta untuk event yang sedang berlangsung tersebut. Tidak ada cara untuk meminta ulang delta yang terlewat.
* **Satu thread, hanya teks:** Pratinjau mencakup teks asisten di [thread yang sedang dibaca koneksi](https://platform.claude.com/docs/id/managed-agents/event-deltas#preview-session-thread-events). Penggunaan alat, hasil alat, dan hasil MCP tidak pernah dipratinjau.
* **Tidak pernah dipersistenkan:** `event_start` dan `event_delta` hanya ada di aliran langsung. Keduanya tidak muncul di riwayat event sesi (`GET /v1/sessions/{session_id}/events`) atau di riwayat event thread sesi mana pun.

## Memecahkan masalah pratinjau

| Yang Anda lihat                                                                  | Artinya                                                                                                                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Aliran dengan event yang di-buffer tetapi tanpa `event_start` atau `event_delta` | Koneksi yang Anda baca tidak mengaktifkan pratinjau, atau giliran tidak pernah menyentuh thread yang Anda streaming. `event_deltas[]` berlaku per koneksi, bukan per sesi. Untuk mengetahui thread mana yang berjalan, daftarkan thread-thread sesi (`GET /v1/sessions/{session_id}/threads`).                                                                                 |
| Aliran yang terputus selama pratinjau                                            | Delta tidak diputar ulang. Ikuti [prosedur penyambungan ulang](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#reconnect-without-missing-events): buka kembali aliran dan daftarkan riwayat event. Riwayat tersebut mencakup event ter-buffer apa pun yang dipancarkan saat Anda terputus, termasuk `agent.message` yang ditunggu oleh pratinjau Anda. |
| Error 404 pada URL aliran                                                        | Path atau ID salah, atau permintaan sama sekali tidak membawa header beta managed-agents. Endpoint thread dibatasi beta, jadi tanpa header tersebut endpoint itu tidak ada.                                                                                                                                                                                                    |
| Error 400 yang menyebutkan `event_deltas`                                        | Hanya `agent.message` dan `agent.thinking` yang diterima.                                                                                                                                                                                                                                                                                                                      |

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Aliran event sesi" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/events-and-streaming">
    Kirim event, streaming respons, dan interupsi atau arahkan ulang sesi Anda di tengah eksekusi.
  </Card>

  <Card title="Orkestrasi multiagen" icon="stack" href="https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration">
    Koordinasikan beberapa agen dalam satu sesi.
  </Card>
</CardGroup>
