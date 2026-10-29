---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/event-deltas
fetched_at: 2026-10-29T02:15:48.406163Z
sha256: 6763afd54978202d7f7f9177368ccadd746cc511b1a6122d3155282eaf9cdc61
---

---
title: Pratinjau respons dengan delta event
url: https://platform.claude.com/docs/id/managed-agents/event-deltas
description: Tampilkan teks respons agen sebagai pratinjau langsung saat model masih menghasilkannya.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Sessions are stateful resources; transcripts persist until you delete them. Applies to all Managed Agents sub-features, including Self-hosted sandboxes.
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
    Claude Models on Google Cloud (Anthropic managed): beta
---

Secara default, teks respons agen mencapai [aliran event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) sebagai event `agent.message` yang di-buffer. Masing-masing dipancarkan hanya setelah permintaan model yang menghasilkannya selesai. “Event delta” (delta event) memungkinkan Anda menampilkan teks tersebut secara bertahap, sebagai pratinjau langsung, saat model masih menghasilkannya.

Pratinjau adalah alat bantu tampilan berbasis upaya terbaik, dan `agent.message` yang di-buffer selalu menjadi catatan otoritatif. Klien yang mengabaikan pratinjau tetap menerima aliran yang lengkap dan benar.

## Mengaktifkan pratinjau

Pratinjau bersifat opt-in untuk setiap koneksi aliran. Tambahkan parameter kueri `event_deltas[]` ke aliran yang Anda baca, dan ulangi sekali untuk setiap jenis event yang ingin Anda pratinjau. Nilai yang diterima adalah `agent.message` dan `agent.thinking`. Nilai lain apa pun akan mengembalikan error 400, demikian pula permintaan dengan lebih dari 100 nilai.

Kedua endpoint aliran menerima parameter tersebut:

* **Aliran tingkat sesi:** `GET /v1/sessions/{session_id}/events/stream`
* **Aliran thread sesi:** `GET /v1/sessions/{session_id}/threads/{thread_id}/stream`

Pratinjau subagen muncul di [aliran thread milik subagen itu sendiri](https://platform.claude.com/docs/id/managed-agents/event-deltas#preview-session-thread-events).

`[]` adalah pola glob shell, jadi beri tanda kutip pada URL setiap kali Anda membangun permintaan di shell. Contoh-contoh ini melakukan percent-encode pada tanda kurung siku sebagai `%5B%5D`, yang juga berfungsi.

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

Untuk `agent.thinking`, hanya `event_start` yang dipancarkan, sebagai sinyal bahwa blok thinking telah dimulai. Tidak ada event `event_delta` yang menyusul. Event `agent.thinking` yang di-buffer yang mengakhiri pratinjau adalah sinyal kemajuan dan tidak membawa konten thinking.

Tidak seperti event yang dipersistenkan, `event_start` dan `event_delta` tidak memiliki `id` atau `processed_at` sendiri. Satu-satunya pengidentifikasi yang mereka bawa adalah `id` dari event yang mereka pratinjau. String jenisnya juga merupakan pengecualian dari konvensi penamaan `{domain}.{action}` pada event yang dipersistenkan.

<Note>
  Delta event menggunakan format wire yang berbeda dari [Streaming pesan](https://platform.claude.com/docs/id/build-with-claude/streaming), dan perbedaan ini disengaja. `agent.message` yang dipratinjau mendapatkan satu `event_start` yang hanya diikuti oleh event `event_delta`. Tidak ada event start atau stop per blok konten dan tidak ada event stop untuk event yang dipratinjau itu sendiri. Jenis delta-nya adalah `content_delta`, bukan `content_block_delta`. Kode akumulator yang ditulis untuk Messages API tidak dapat digunakan tanpa perubahan.
</Note>

## Mengakumulasi dan merekonsiliasi

Setiap SDK yang mendukung event delta menyertakan [helper akumulator](https://platform.claude.com/docs/id/managed-agents/event-deltas#sdk-accumulator-helpers) yang menangani pembukuan `index` (csharp, go: `Index`) untuk Anda. Pola manual di bagian ini berfungsi di setiap bahasa ketika Anda memerlukan pembukuan kustom. Terapkan pada jenis event yang dihasilkan.

Dalam pola manual, simpan teks pratinjau dalam map sementara dengan kunci `(event_id, index)`, dan perlakukan event yang di-buffer sebagai catatan. Rekonsiliasi keduanya untuk setiap permintaan model.

Sebuah giliran dibuka dengan satu event `session.status_running`. Pada giliran yang selesai secara normal, setiap permintaan model kemudian menghasilkan event-event berikut, secara berurutan:

1. `span.model_request_start`
2. `event_start`
3. Event-event `event_delta`
4. `agent.message` yang di-buffer
5. [`span.model_request_end`](https://platform.claude.com/docs/id/managed-agents/reference#event-types) (di tab **Span events**)

Di wire, ini adalah bagian yang dipratinjau dari urutan tersebut, diselingi dengan event buffer lain dari koneksi:

```text wrap
event_start     {"event": {"type": "agent.message", "id": "sevt_01abc..."}}
event_delta     {"event_id": "sevt_01abc...", "delta": {"type": "content_delta", "index": 0, "content": {"type": "text", "text": "..."}}}
...
agent.message   {"id": "sevt_01abc...", "content": [...]}
```

Baris `event_delta` berulang sekali untuk setiap fragmen teks. Proses setiap event saat tiba:

1. Pada `event_start`, catat `id` yang diumumkan. Pengidentifikasi selalu selaras: `event_start.event.id`, setiap `event_delta.event_id`, dan `id` dari `agent.message` yang di-buffer memiliki nilai yang sama.
2. Pada setiap `event_delta`, tambahkan `delta.content.text` ke entri di `(event_id, delta.index)` dan tampilkan teks berjalan. Delta pertama untuk sebuah `index` membuat entri tersebut.
3. Ketika `agent.message` yang di-buffer tiba, cocokkan berdasarkan `id`, buang pratinjau yang terakumulasi, dan tampilkan konten pesan sebagai gantinya.
4. Pada `span.model_request_end`, tutup pratinjau apa pun yang belum direkonsiliasi oleh event buffer-nya. Tidak ada lagi delta yang akan datang untuknya. Jika giliran mengalami error atau diinterupsi, event yang di-buffer mungkin tidak pernah tiba, tetapi `span.model_request_end` tetap tiba.

Pola ini bergantung pada dua jaminan:

* Menggabungkan delta pratinjau dalam urutan kedatangan, dengan kunci `(event_id, index)`, menghasilkan prefiks dari `content[index].text` dalam event yang di-buffer. Ini belum tentu keseluruhan teks, karena delta mungkin [dibuang saat beban tinggi](https://platform.claude.com/docs/id/managed-agents/event-deltas#limitations).
* Sebuah koneksi memancarkan paling banyak satu `event_start` untuk setiap `event_id`, dan event yang di-buffer adalah hal terakhir yang dikirimkan koneksi tersebut untuk `id` itu.

### Helper akumulator SDK

Helper setiap SDK menangani pencatatan `index` (csharp, go: `Index`). Helper Go, Java, Ruby, dan C# juga memberi kunci pada pratinjau yang terakumulasi berdasarkan `id` (csharp, go: `ID`) event. Dengan helper Python, TypeScript, dan PHP, simpan map tersebut sendiri dan gabungkan setiap delta ke dalam entri untuk `id` (csharp, go: `ID`)-nya.

Contoh-contoh berikut mengaktifkan pratinjau `agent.message` dan merekonsiliasinya dengan event yang di-buffer:

<CodeGroup exclude="shell:cURL, shell:CLI">
  <CodeGroupItem language="cURL">
    Alur kerja ini memerlukan logika lebih dari sekadar satu perintah shell. Gunakan [Claude SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk menjalankannya.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Alur kerja ini memerlukan logika lebih dari sekadar satu perintah shell. Gunakan [Claude SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk menjalankannya.
  </CodeGroupItem>

  ```python Python
  # Snapshot pratinjau, dengan kunci ID event. accumulate_managed_agents_event melipat setiap
  # event_start / event_delta ke dalam snapshot agent.message; agent.message yang
  # di-buffer menggantikannya.
  previews: dict[str, BetaManagedAgentsAgentMessageEvent] = {}

  # Ikut serta (opt in) pratinjau agent.message pada koneksi ini
  with client.beta.sessions.events.stream(
      session.id, event_deltas=["agent.message"]
  ) as stream:
      client.beta.sessions.events.send(
          session.id,
          events=[
              {
                  "type": "user.message",
                  "content": [
                      {"type": "text", "text": "Describe the repo in one sentence."}
                  ],
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
                  preview = accumulate_managed_agents_event(
                      previews.get(event.event_id), event
                  )
                  if preview is not None:
                      previews[event.event_id] = preview
                      text = "".join(block.text for block in preview.content)
                      print(f"event_delta             preview: {text!r}")
              case "agent.message":
                  # Event yang di-buffer adalah catatannya: ia menggantikan dan menutup pratinjau
                  preview = accumulate_managed_agents_event(
                      previews.pop(event.id, None), event
                  )
                  text = "".join(block.text for block in preview.content)
                  print(f"agent.message           {event.id} {text!r}")
              case "span.model_request_end":
                  # Tidak ada delta lagi yang akan datang. Tutup pratinjau mana pun yang
                  # event buffer-nya tidak pernah tiba.
                  for event_id in previews:
                      print(f"span.model_request_end  closing preview for {event_id}")
                  previews.clear()
              case "session.status_idle":
                  break
  ```

  ```typescript TypeScript
  // Snapshot pratinjau, dikunci berdasarkan ID event. `accumulateManagedAgentsEvent`
  // menggabungkan pratinjau event_start / event_delta ke dalam snapshot agent.message.
  const previews = new Map<string, BetaManagedAgentsAgentMessageEvent>();

  // Aktifkan pratinjau agent.message hanya untuk koneksi ini
  const stream = await client.beta.sessions.events.stream(session.id, {
    event_deltas: ["agent.message"]
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
        // 1. Catat ID yang diumumkan dan buka snapshot. Delta dan
        //    event yang di-buffer membawa ID yang sama.
        const preview = accumulateManagedAgentsEvent(undefined, event);
        if (preview) {
          previews.set(event.event.id, preview);
        }
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
        // 4. Tidak ada delta lagi. Tutup pratinjau yang belum pernah direkonsiliasi.
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
  // Aktifkan delta event: event agent.message dipratinjau saat sedang dihasilkan.
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
              Content =
              [
                  new BetaManagedAgentsTextBlock { Text = "Write a haiku about event streams." },
              ],
          },
      ],
  });

  // Kumpulkan fragmen pratinjau untuk tiap (ID event, indeks konten). agent.message
  // yang di-buffer berikutnya membawa konten lengkap, sehingga menggantikan
  // pratinjau yang terkumpul alih-alih ditambahkan ke dalamnya.
  Dictionary<string, SortedDictionary<long, string>> previews = [];

  await foreach (var streamEvent in stream.Enumerate())
  {
      if (streamEvent.TryPickStartEvent(out var start))
      {
          // Pratinjau dibuka untuk event dengan ID ini. Stream ini hanya mengaktifkan
          // delta agent.message; TryPick* mengembalikan false alih-alih melempar error,
          // sehingga jenis pratinjau lain (termasuk yang ditambahkan nanti) dilewati.
          if (start.Event.TryPickAgentMessage(out var preview))
          {
              Console.WriteLine($"event_start             {preview.Type.GetString()} {preview.ID}");
          }
      }
      else if (streamEvent.TryPickDeltaEvent(out var delta))
      {
          // Sisipkan di indeks baru, tambahkan di indeks yang sudah ada
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
  				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  						Text: "Write a haiku about the ocean.",
  					},
  				}},
  			},
  		}},
  	}); err != nil {
  		panic(err)
  	}

  	// Akumulator menggabungkan fragmen event_start / event_delta menjadi
  	// snapshot agent.message, satu untuk setiap ID event. Nilai nol-nya siap digunakan.
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
  			// Event yang di-buffer membawa konten lengkap: accumulator
  			// mengganti pratinjau dengannya
  			fmt.Printf("agent.message           %s %q\n", event.ID, previews.AgentMessageText(event.ID))
  		case anthropic.BetaManagedAgentsSpanModelRequestEndEvent:
  			// Tidak ada delta lagi untuk request ini. Accumulator
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
                      IO.println("event_start             " + preview._type() + " " + preview.id());
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
                  // Tidak ada delta lagi. Tutup pratinjau yang event buffer-nya tidak pernah tiba.
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
  use Anthropic\Beta\Sessions\BetaManagedAgentsDeltaEvent;
  use Anthropic\Beta\Sessions\BetaManagedAgentsDeltaType;
  use Anthropic\Beta\Sessions\BetaManagedAgentsStartEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsAgentMessageEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsSessionStatusIdleEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsSpanModelRequestEndEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsTextBlock;
  use Anthropic\Lib\Sessions\EventAccumulator;

  // Snapshot pratinjau, dengan kunci ID event. EventAccumulator::accumulate() menambahkan setiap
  // event_start / event_delta ke snapshot agent.message; agent.message yang
  // di-buffer menggantikannya.
  $previews = [];

  // Teks dari snapshot atau event agent.message
  $textOf = fn (ManagedAgentsAgentMessageEvent $message): string => implode(
      '',
      array_map(
          fn ($block) => $block->text,
          array_filter(
              $message->content,
              fn ($block) => $block instanceof ManagedAgentsTextBlock,
          ),
      ),
  );

  // Aktifkan pratinjau agent.message pada koneksi ini
  $stream = $client->beta->sessions->events->streamStream(
      $session->id,
      eventDeltas: [BetaManagedAgentsDeltaType::AGENT_MESSAGE],
  );

  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => 'Describe the repo in one sentence.']],
          ],
      ],
  );

  foreach ($stream as $event) {
      switch (true) {
          case $event instanceof BetaManagedAgentsStartEvent:
              $snapshot = EventAccumulator::accumulate(null, $event);
              if ($snapshot !== null) {
                  $previews[$event->event->id] = $snapshot;
              }
              printf("event_start             %s %s\n", $event->event->type, $event->event->id);
              break;
          case $event instanceof BetaManagedAgentsDeltaEvent:
              // Lewati delta terlambat untuk pratinjau yang sudah diganti atau ditutup
              if (!isset($previews[$event->eventID])) {
                  break; // Break switch statement
              }
              $previews[$event->eventID] = EventAccumulator::accumulate($previews[$event->eventID], $event);
              printf("event_delta             preview: %s\n", json_encode($textOf($previews[$event->eventID])));
              break;
          case $event instanceof ManagedAgentsAgentMessageEvent:
              // Event yang di-buffer adalah catatan resminya: event ini mengganti dan menutup pratinjau
              unset($previews[$event->id]);
              printf("agent.message           %s %s\n", $event->id, json_encode($textOf($event)));
              break;
          case $event instanceof ManagedAgentsSpanModelRequestEndEvent:
              // Tidak ada delta lagi yang akan datang. Tutup pratinjau mana pun yang
              // event buffer-nya tidak pernah tiba.
              foreach (array_keys($previews) as $eventID) {
                  printf("span.model_request_end  closing preview for %s\n", $eventID);
              }
              $previews = [];
              break;
          case $event instanceof ManagedAgentsSessionStatusIdleEvent:
              break 2; // Break foreach loop
      }
  }
  $stream->close();
  ```

  ```ruby Ruby
  # Aktifkan event delta: pratinjau agent.message di-stream sebagai fragmen inkremental.
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

  # Kumpulkan fragmen pratinjau berdasarkan (event_id, index) ke buffer yang eksplisit mutable
  # (`+""`) agar `<<` dapat menambahkan di tempat. agent.message yang di-buffer dengan
  # ID yang sama bersifat otoritatif dan menggantikan apa pun yang dibangun oleh delta.
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
      # Ganti: buang pratinjau yang terkumpul dan render event lengkapnya.
      buffers.delete(event.id)
      puts "agent.message           #{event.id} #{event.content.map(&:text).join.inspect}"
    when Anthropic::Beta::Sessions::BetaManagedAgentsSpanModelRequestEndEvent
      # Tidak ada delta lagi. Tutup pratinjau yang belum pernah direkonsiliasi.
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

Dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), setiap thread sesi memiliki aliran event sendiri. Aliran tersebut menerima parameter `event_deltas[]` yang sama dengan nilai yang sama.

Sebuah koneksi hanya mempratinjau thread yang sedang dibacanya. Aliran tingkat sesi mempratinjau thread utama, dan pratinjau thread anak tidak pernah diposting silang ke sana. Untuk melihat teks subagen saat model menghasilkannya, buka aliran thread subagen tersebut.

Path aliran thread diakhiri dengan `/threads/{thread_id}/stream`. `/events/stream` hanya ada di tingkat sesi, jadi tidak ada endpoint `/threads/{thread_id}/events/stream`.

`event_start` dan `event_delta` memiliki bentuk yang sama pada aliran thread seperti pada aliran tingkat sesi, dan pola [mengakumulasi dan merekonsiliasi](https://platform.claude.com/docs/id/managed-agents/event-deltas#accumulate-and-reconcile) berlaku sebagaimana tertulis. Jalankan satu instans akumulator untuk setiap koneksi aliran.

<CodeGroup>
  ```bash cURL
  # Stream thread menerima parameter event_deltas[] yang sama dengan stream sesi.
  # Lakukan percent-encode pada tanda kurung (%5B%5D) dan beri tanda kutip pada URL.
  curl --fail-with-body -sS -N \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/stream?beta=true&event_deltas%5B%5D=agent.message" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "accept: text/event-stream"
  ```

  ```bash CLI
  # Stream thread menerima parameter event_deltas yang sama dengan stream sesi,
  # satu flag --event-delta untuk setiap tipe event yang dipratinjau.
  ant beta:sessions:threads:events stream \
    --session-id "$SESSION_ID" \
    --thread-id "$THREAD_ID" \
    --event-delta agent.message
  ```

  ```python Python
  # Daftarkan thread sesi dan pilih child: child thread punya parent_thread_id
  # non-null, dan parent_thread_id thread utama bernilai null.
  child_thread = next(
      thread
      for thread in client.beta.sessions.threads.list(session.id)
      if thread.parent_thread_id is not None
  )

  # Stream child thread menerima parameter event_deltas yang sama dengan
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
                  # Event yang di-buffer adalah catatan otoritatif; render kontennya.
                  print()
                  for block in event.content:
                      if block.type == "text":
                          print(block.text, end="")
                  print()
              case "session.thread_status_idle":
                  break
  ```

  ```typescript TypeScript
  // Daftarkan thread sesi dan pilih child: child thread memiliki parent_thread_id
  // yang tidak null, dan parent_thread_id thread utama bernilai null.
  let childThreadId: string | undefined;
  for await (const thread of client.beta.sessions.threads.list(session.id)) {
    if (thread.parent_thread_id !== null) {
      childThreadId = thread.id;
      break;
    }
  }
  if (!childThreadId) {
    throw new Error("No child thread found");
  }

  // Stream child thread menerima parameter event_deltas yang sama dengan
  // stream sesi.
  const stream = await client.beta.sessions.threads.events.stream(childThreadId, {
    session_id: session.id,
    event_deltas: ["agent.message"]
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
  // Daftar thread sesi dan pilih child: child thread punya parent_thread_id
  // non-null, dan parent_thread_id thread utama bernilai null.
  var threads = await client.Beta.Sessions.Threads.List(session.ID);
  var childThread = threads.Items.First(thread => thread.ParentThreadID is not null);

  // Stream child thread menerima parameter event_deltas yang sama dengan
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
  	// Tampilkan thread sesi dan pilih child: child thread punya parent_thread_id
  	// non-null, sedangkan parent_thread_id thread utama bernilai null.
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

  	// Stream child thread menerima parameter event_deltas yang sama dengan
  	// stream sesi; jalankan satu loop baca untuk setiap koneksi stream.
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
  			// list bertipe konkret: BetaManagedAgentsTextBlock
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
  // Tampilkan thread sesi dan pilih child: child thread punya parent_thread_id
  // non-null, sedangkan parent_thread_id thread utama bernilai null.
  var childThread = client.beta().sessions().threads().list(session.id()).autoPager().stream()
      .filter(thread -> thread.parentThreadId().isPresent())
      .findFirst()
      .orElseThrow();

  // Stream child thread menerima parameter event_deltas yang sama dengan stream
  // sesi. Kelas params-nya bernama sama dengan milik level sesi, jadi gunakan nama lengkap.
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
  use Anthropic\Beta\Sessions\BetaManagedAgentsDeltaEvent;
  use Anthropic\Beta\Sessions\BetaManagedAgentsDeltaType;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsAgentMessageEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsSessionThreadStatusIdleEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsTextBlock;

  // Tampilkan daftar thread sesi dan pilih child: thread child memiliki
  // parentThreadID yang tidak null, dan parentThreadID thread utama bernilai null.
  $childThread = null;
  foreach ($client->beta->sessions->threads->list($session->id)->pagingEachItem() as $thread) {
      if ($thread->parentThreadID !== null) {
          $childThread = $thread;
          break;
      }
  }

  // Stream thread child menerima parameter eventDeltas yang sama dengan
  // stream sesi.
  $stream = $client->beta->sessions->threads->events->streamStream(
      $childThread->id,
      sessionID: $session->id,
      eventDeltas: [BetaManagedAgentsDeltaType::AGENT_MESSAGE],
  );

  foreach ($stream as $event) {
      switch (true) {
          case $event instanceof BetaManagedAgentsDeltaEvent:
              echo $event->delta->content->text;
              break;
          case $event instanceof ManagedAgentsAgentMessageEvent:
              // Event yang di-buffer adalah catatan otoritatif; render kontennya.
              echo "\n";
              foreach ($event->content as $block) {
                  if ($block instanceof ManagedAgentsTextBlock) {
                      echo $block->text;
                  }
              }
              echo "\n";
              break;
          case $event instanceof ManagedAgentsSessionThreadStatusIdleEvent:
              break 2; // Break foreach loop
      }
  }
  $stream->close();
  ```

  ```ruby Ruby
  # Tampilkan thread sesi dan pilih child: child thread punya parent_thread_id
  # non-null, sedangkan parent_thread_id thread utama bernilai null.
  child_thread = client.beta.sessions.threads.list(session.id).to_enum.find { it.parent_thread_id }

  # Stream child thread menerima parameter event_deltas yang sama dengan
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
      # Event yang di-buffer adalah catatan otoritatif; render kontennya.
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

* **Upaya terbaik:** Saat beban tinggi, server mungkin membuang delta untuk sebuah event. Ketika itu terjadi, Anda menerima prefiks teks yang berkesinambungan lalu tidak ada delta lebih lanjut untuk event tersebut. `agent.message` yang di-buffer tetap tiba secara lengkap. Jangan pernah memperlakukan pratinjau yang terakumulasi sebagai final.
* **Tidak ada pemutaran ulang saat menyambung kembali:** Delta hanya dikirimkan ke koneksi yang mengaktifkannya, selama koneksi tersebut terbuka. Ini berlaku sama untuk aliran tingkat sesi dan setiap aliran thread sesi. Koneksi yang dibuka setelah permintaan model dimulai tidak menerima delta untuk event yang sedang berlangsung tersebut. Tidak ada cara untuk meminta ulang delta yang terlewat.
* **Satu thread, hanya teks:** Pratinjau mencakup teks asisten pada [thread yang sedang dibaca koneksi](https://platform.claude.com/docs/id/managed-agents/event-deltas#preview-session-thread-events). Penggunaan alat, hasil alat, dan hasil MCP tidak pernah dipratinjau.
* **Tidak pernah dipersistenkan:** `event_start` dan `event_delta` hanya ada di aliran langsung. Keduanya tidak muncul dalam riwayat event sesi (`GET /v1/sessions/{session_id}/events`) atau dalam riwayat event thread sesi mana pun.

## Memecahkan masalah pratinjau

| Yang Anda lihat                                                                  | Artinya                                                                                                                                                                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Aliran dengan event yang di-buffer tetapi tanpa `event_start` atau `event_delta` | Koneksi yang Anda baca tidak mengaktifkannya, atau giliran tidak pernah menyentuh thread yang Anda streaming. `event_deltas[]` berlaku per koneksi, bukan per sesi. Untuk mengetahui thread mana yang berjalan, daftarkan thread sesi (`GET /v1/sessions/{session_id}/threads`).                                                                                           |
| Aliran yang terputus selama pratinjau                                            | Delta tidak diputar ulang. Ikuti [prosedur menyambung kembali](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#reconnect-without-missing-events): buka kembali aliran dan daftarkan riwayat event. Riwayat tersebut mencakup event buffer apa pun yang dipancarkan saat Anda terputus, termasuk `agent.message` yang ditunggu oleh pratinjau Anda. |
| Error 404 pada URL aliran                                                        | Path atau ID salah, atau permintaan sama sekali tidak membawa header beta managed-agents. Endpoint thread dibatasi beta, jadi tanpa header tersebut endpoint itu tidak ada.                                                                                                                                                                                                |
| Error 400 yang menyebutkan `event_deltas`                                        | Hanya `agent.message` dan `agent.thinking` yang diterima.                                                                                                                                                                                                                                                                                                                  |

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Aliran event sesi" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/events-and-streaming">
    Kirim event, streaming respons, dan interupsi atau arahkan ulang sesi Anda saat sedang berjalan.
  </Card>

  <Card title="Orkestrasi multiagen" icon="stack" href="https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration">
    Koordinasikan beberapa agen dalam satu sesi.
  </Card>
</CardGroup>

## Availability

Event deltas are in beta on every model.

### API support

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Availability: Available

| Status | Cloud platforms         | Models                                                            |
| ------ | ----------------------- | ----------------------------------------------------------------- |
| Beta   | All supported platforms | [All models](https://platform.claude.com/docs/id/models/overview) |

### Required beta headers

[Beta headers overview](https://platform.claude.com/docs/id/api/beta-headers)

Beta headers allow you to access experimental features and new model capabilities before they become part of the standard API.

* `managed-agents-2026-04-01`

### Data handling

[Data handling overview](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item    | Zero data retention                                                                                                                                      | HIPAA                                                                        |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Status  | Not eligible                                                                                                                                             | Not eligible                                                                 |
| Details | Sessions are stateful resources; transcripts persist until you delete them. Applies to all Managed Agents sub-features, including Self-hosted sandboxes. | Applies to all Managed Agents sub-features, including Self-hosted sandboxes. |

Applicable endpoints:

* `/v1/agents`
* `/v1/sessions`
* `/v1/environments`
