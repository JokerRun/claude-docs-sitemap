---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/session-threads
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: 1ad97d767239be74cf989b6f382b191a73c4ab8412f324dc043167c2823e3bdc
---

---
title: Thread sesi
url: https://platform.claude.com/docs/id/managed-agents/session-threads
description: Cantumkan, interupsi, dan arsipkan thread dari sesi multiagen, baca event-nya, dan tangani izin alat di seluruh thread tersebut.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Dalam [sesi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), setiap agen bekerja di **session thread** (thread sesi) miliknya sendiri. Halaman ini membahas cara mencantumkan, menginterupsi, dan mengarsipkan thread, event yang dikirimkannya, serta cara kerja izin alat di seluruh thread tersebut. Sebuah [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs) juga membuat thread sesi.

## Thread utama dan thread sesi

**Aliran event tingkat sesi** (`/v1/sessions/{session_id}/events/stream`) dianggap sebagai **primary thread** (thread utama), yang berisi tampilan ringkas dari semua aktivitas di seluruh thread. Anda tidak melihat aktivitas lengkap dari [subagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#delegate-to-subagents), tetapi Anda melihat awal dan akhir pekerjaan mereka, serta event yang memblokir seperti permintaan izin alat.

**Thread sesi** adalah tempat Anda menelusuri aktivitas agen tertentu secara mendalam.

`status` sesi merupakan agregasi dari semua aktivitas agen; jika setidaknya satu thread berstatus `running`, maka status sesi secara keseluruhan juga `running`. Sebuah [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs) yang sedang berjalan juga dapat membuat sesi tetap `running`, bahkan ketika tidak ada thread-nya yang sedang bekerja. Ketika tidak ada thread yang bekerja dan sebuah thread menunggu klien Anda, sesi berstatus `idle`; lihat [Mengetahui kapan pekerjaan selesai](https://platform.claude.com/docs/id/managed-agents/workflow-runs#know-when-the-work-is-done).

Sebuah [anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets) adalah satu batas bersama untuk semua thread dalam sebuah sesi. Saat batas tercapai, thread berhenti sementara secara independen, dan biaya setiap thread dihitung berdasarkan model yang melayani thread itu sendiri.

<Note>
  Sebuah sesi dapat memiliki paling banyak 25 thread anak pada satu waktu. Thread yang idle tetap dihitung hingga Anda mengarsipkannya, dan thread utama tidak dihitung. Agen thread utama dapat memanggil beberapa salinan dari satu subagen, sehingga membuat beberapa thread yang terkait dengan satu `agent`. Thread konsultasi [advisor](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor) dikecualikan dari batas ini. Demikian pula thread dari sebuah [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs).
</Note>

## Mencantumkan thread

Cantumkan semua thread yang terkait dengan sebuah sesi sebagai berikut:

<CodeGroup>
  ```bash cURL
  curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:sessions:threads list --session-id "$SESSION_ID"
  ```

  ```python Python
  for thread in client.beta.sessions.threads.list(session.id):
      agent = thread.agent
      label = agent.type if agent.type == "advisor" else agent.name
      print(f"[{label}] {thread.status}")
  ```

  ```typescript TypeScript
  for await (const thread of client.beta.sessions.threads.list(session.id)) {
    const label = thread.agent.type === "advisor" ? thread.agent.type : thread.agent.name;
    console.log(`[${label}] ${thread.status}`);
  }
  ```

  ```csharp C#
  await foreach (var thread in (await client.Beta.Sessions.Threads.List(session.ID)).Paginate())
  {
      var label = thread.Agent.TryPickBetaManagedAgentsSessionThread(out var agent)
          ? agent.Name
          : thread.Agent.Json.GetProperty("type").GetString();
      Console.WriteLine($"[{label}] {thread.Status.Raw()}");
  }
  ```

  ```go Go
  threads := client.Beta.Sessions.Threads.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionThreadListParams{})
  for threads.Next() {
  	thread := threads.Current()
  	label := cmp.Or(thread.Agent.Name, thread.Agent.Type)
  	fmt.Printf("[%s] %s\n", label, thread.Status)
  }
  if err := threads.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  for (var thread : client.beta().sessions().threads().list(session.id()).autoPager()) {
      var agent = thread.agent();
      var label = agent.isAgent() ? agent.asAgent().name() : agent.type().asString();
      IO.println("[" + label + "] " + thread.status());
  }
  ```

  ```php PHP
  foreach ($client->beta->sessions->threads->list($session->id)->pagingEachItem() as $thread) {
      $label = $thread->agent instanceof \Anthropic\Beta\Agents\BetaManagedAgentsAdvisor
          ? $thread->agent->type
          : $thread->agent->name;
      echo "[{$label}] {$thread->status}\n";
  }
  ```

  ```ruby Ruby
  client.beta.sessions.threads.list(session.id).auto_paging_each do |thread|
    agent = thread.agent
    label = agent.type == :advisor ? agent.type : agent.name
    puts "[#{label}] #{thread.status}"
  end
  ```
</CodeGroup>

Daftar lengkap mencakup thread utama. `parent_thread_id` bernilai `null` untuk thread utama. Setiap thread lainnya adalah thread anak. `workflow_run_id` bernilai `null` kecuali pada [thread milik sebuah eksekusi](https://platform.claude.com/docs/id/managed-agents/workflow-runs#a-runs-threads).

Untuk mencantumkan hanya thread yang memiliki status tertentu, tambahkan `statuses[]` ke permintaan, dan ulangi untuk memberikan lebih dari satu status, seperti pada `?statuses[]=running&statuses[]=idle`. Hilangkan parameter ini untuk mengembalikan thread dengan semua status.

## Menginterupsi thread sesi

Kirim `user.interrupt` dengan `session_thread_id` untuk menghentikan thread tertentu. Menghilangkan `session_thread_id` akan menginterupsi setiap thread yang tidak diarsipkan dalam sesi, termasuk thread utama. Dalam sesi dengan alur kerja dinamis, interupsi tidak mengakhiri eksekusi apa pun, dan interupsi yang menyebut thread milik sebuah eksekusi tidak menghentikan apa pun. Interupsi menutup panggilan alat yang tertunda pada thread anak lainnya, tetapi jangan mengandalkannya untuk menutup panggilan alat milik thread eksekusi. Lihat [Menginterupsi sesi dengan eksekusi yang terbuka](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open).

<CodeGroup>
  ```bash cURL
  curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d "{\"events\": [{\"type\": \"user.interrupt\", \"session_thread_id\": \"$THREAD_ID\"}]}"
  ```

  ```bash CLI
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" \
    --event "{type: user.interrupt, session_thread_id: $THREAD_ID}"
  ```

  ```python Python
  client.beta.sessions.events.send(
      session.id,
      events=[{"type": "user.interrupt", "session_thread_id": thread.id}],
  )
  ```

  ```typescript TypeScript
  await client.beta.sessions.events.send(session.id, {
    events: [{ type: "user.interrupt", session_thread_id: thread.id }],
  });
  ```

  ```csharp C#
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
  ```

  ```go Go
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
  ```

  ```java Java
  client.beta().sessions().events().send(
      session.id(),
      EventSendParams.builder()
          .addEvent(BetaManagedAgentsUserInterruptEventParams.builder()
              .type(BetaManagedAgentsUserInterruptEventParams.Type.USER_INTERRUPT)
              .sessionThreadId(thread.id())
              .build())
          .build());
  ```

  ```php PHP
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          ['type' => 'user.interrupt', 'session_thread_id' => $thread->id],
      ],
  );
  ```

  ```ruby Ruby
  client.beta.sessions.events.send_(
    session.id,
    events: [{type: "user.interrupt", session_thread_id: thread.id}]
  )
  ```
</CodeGroup>

Terhadap thread subagen yang terblokir pada `requires_action`, interupsi menutup setiap panggilan alat yang tertunda dengan hasil alat berupa error ("Tool execution was interrupted before completion. Please retry.") dan langsung memancarkan ulang `session.thread_status_idle` dengan `stop_reason: end_turn`; model tidak di-sampling. Terhadap thread anak yang idle dengan `end_turn` atau `budget_reached`, interupsi tidak berpengaruh apa pun. Interupsi yang menyebut thread yang telah dihentikan mengembalikan error 400. Thread anak yang diinterupsi tidak mengirimkan kepada agen thread utama laporan yang biasanya dikirimkannya saat sebuah giliran berakhir. Selama agen tersebut menunggu thread anak, agen tidak memulai giliran lain hingga ada hal lain yang mencapainya, seperti `user.message` atau laporan dari thread lain.

## Mengarsipkan thread sesi

Secara opsional, arsipkan thread sesi ketika thread tersebut telah menyelesaikan pekerjaannya. Mengarsipkan thread membebaskan tempatnya di bawah batas 25 thread anak. Server mengarsipkan sendiri thread milik sebuah [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs). Anda tidak perlu mengarsipkannya, dan Anda tidak dapat melakukannya selama eksekusi masih terbuka.

<CodeGroup>
  ```bash cURL
  curl -fsS -X POST "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:sessions:threads archive \
    --session-id "$SESSION_ID" \
    --thread-id "$THREAD_ID"
  ```

  ```python Python
  archived = client.beta.sessions.threads.archive(thread.id, session_id=session.id)
  print(archived.status, archived.archived_at)
  ```

  ```typescript TypeScript
  const archived = await client.beta.sessions.threads.archive(thread.id, {
    session_id: session.id,
  });
  console.log(archived.status, archived.archived_at);
  ```

  ```csharp C#
  var archived = await client.Beta.Sessions.Threads.Archive(thread.ID, new() { SessionID = session.ID });
  Console.WriteLine($"{archived.Status} {archived.ArchivedAt}");
  ```

  ```go Go
  archived, err := client.Beta.Sessions.Threads.Archive(ctx, thread.ID, anthropic.BetaSessionThreadArchiveParams{
  	SessionID: session.ID,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(archived.Status, archived.ArchivedAt)
  ```

  ```java Java
  var archived = client.beta().sessions().threads().archive(
      thread.id(),
      ThreadArchiveParams.builder()
          .sessionId(session.id())
          .build());
  IO.println(archived.status() + " " + archived.archivedAt().orElseThrow());
  ```

  ```php PHP
  $archived = $client->beta->sessions->threads->archive($thread->id, sessionID: $session->id);
  echo "{$archived->status} {$archived->archivedAt->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  archived = client.beta.sessions.threads.archive(thread.id, session_id: session.id)
  puts "#{archived.status} #{archived.archived_at}"
  ```
</CodeGroup>

Pengarsipan hanya berhasil jika thread berstatus `idle`. Thread yang tertahan pada `requires_action` dihitung sebagai idle dan dapat langsung diarsipkan; hanya thread yang sedang berjalan yang harus diinterupsi terlebih dahulu:

<CodeGroup>
  ```bash cURL
  # Interupsi thread, lalu arsipkan
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
  ```

  ```bash CLI
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" \
    --event "{type: user.interrupt, session_thread_id: $THREAD_ID}"

  ant beta:sessions:threads archive \
    --session-id "$SESSION_ID" \
    --thread-id "$THREAD_ID"
  ```

  ```python Python
  client.beta.sessions.events.send(
      session.id,
      events=[{"type": "user.interrupt", "session_thread_id": thread.id}],
  )
  archived = client.beta.sessions.threads.archive(thread.id, session_id=session.id)
  print(archived.status, archived.archived_at)
  ```

  ```typescript TypeScript
  await client.beta.sessions.events.send(session.id, {
    events: [{ type: "user.interrupt", session_thread_id: thread.id }],
  });
  const archived = await client.beta.sessions.threads.archive(thread.id, {
    session_id: session.id,
  });
  console.log(archived.status, archived.archived_at);
  ```

  ```csharp C#
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
  ```

  ```go Go
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
  ```

  ```java Java
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
  IO.println(archived.status() + " " + archived.archivedAt().orElseThrow());
  ```

  ```php PHP
  $client->beta->sessions->events->send(
      $session->id,
      events: [['type' => 'user.interrupt', 'session_thread_id' => $thread->id]],
  );
  $archived = $client->beta->sessions->threads->archive($thread->id, sessionID: $session->id);
  echo "{$archived->status} {$archived->archivedAt->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client.beta.sessions.events.send_(
    session.id,
    events: [{type: "user.interrupt", session_thread_id: thread.id}]
  )
  archived = client.beta.sessions.threads.archive(thread.id, session_id: session.id)
  puts "#{archived.status} #{archived.archived_at}"
  ```
</CodeGroup>

## Event thread utama

Event-event ini menampilkan aktivitas multiagen pada thread utama di `/v1/sessions/{session_id}/events/stream`. Event arah pesan dinamai relatif terhadap thread yang aliran event-nya memuat event tersebut: `agent.thread_message_received` berarti sebuah pesan tiba di thread ini dari thread lain, dan `agent.thread_message_sent` berarti thread ini mengirimkan pesan. Tugas yang didelegasikan oleh agen thread utama, misalnya, tiba di aliran milik thread anak sebagai event `agent.thread_message_received`.

| Tipe                               | Deskripsi                                                                                                                                                                                                  |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `session.thread_created`           | Sebuah thread telah dibuat. Mencakup `session_thread_id` dan `agent_name`.                                                                                                                                 |
| `session.thread_status_running`    | Sebuah thread memulai aktivitas.                                                                                                                                                                           |
| `session.thread_status_idle`       | Agen yang terkait dengan thread sedang menunggu input. Mencakup `stop_reason` yang menunjukkan mengapa agen berhenti.                                                                                      |
| `session.thread_status_terminated` | Sebuah thread dihentikan dan tidak menerima input lebih lanjut, misalnya karena diarsipkan atau mengalami error yang tidak dapat dipulihkan. Thread advisor juga dihentikan ketika konsultasinya berakhir. |
| `agent.thread_message_received`    | Pada thread utama, sebuah subagen mengirimkan laporan atau pertanyaan kepada agen thread utama. Mencakup `from_session_thread_id`, `from_agent_name`, dan `content`.                                       |
| `agent.thread_message_sent`        | Pada thread utama, agen thread utama mengirimkan tugas atau pesan tindak lanjut kepada sebuah subagen. Mencakup `to_session_thread_id`, `to_agent_name`, dan `content`.                                    |

Konsultasi advisor memancarkan event thread yang sama ini dengan nama cadangan `anthropic.advisor` (sebagai `agent_name` pada event siklus hidup thread dan `from_agent_name` pada penyampaian saran); lihat [Berikan advisor pada sesi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor) untuk urutannya.

Thread milik sebuah [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs) ditampilkan pada aliran utama sebagai berikut:

* **Event siklus hidup:** Setiap thread eksekusi mengirimkan `session.thread_created`, dengan `workflow_run_id` milik eksekusi tersebut, serta event `session.thread_status_running`, `session.thread_status_idle`, dan `session.thread_status_terminated` miliknya.
* **Event pesan:** Prompt thread eksekusi, yaitu event `agent.thread_message_received`, tetap berada di alirannya sendiri.
* **Event eksekusi:** Event `workflow_run.*` juga tiba di aliran ini; lihat [Event eksekusi](https://platform.claude.com/docs/id/managed-agents/workflow-runs#run-events).
* **Panggilan alat yang menunggu Anda:** Panggilan alat thread eksekusi yang memerlukan klien Anda diposting silang ke aliran ini, sama seperti untuk thread anak mana pun. Lihat [Izin alat dan alat kustom](https://platform.claude.com/docs/id/managed-agents/session-threads#tool-permissions-and-custom-tools).

## Event thread sesi

Event penting diteruskan ke thread utama. Namun, Anda mungkin tetap ingin menyelidiki penalaran dan panggilan alat dari agen tertentu. Untuk melakukannya, lakukan streaming atau cantumkan event dari thread sesi yang terkait.

Setiap thread sesi memiliki aliran event sendiri di `/v1/sessions/{session_id}/threads/{thread_id}/stream`, dan aliran ini menerima parameter `event_deltas[]` yang sama dengan aliran tingkat sesi, sehingga Anda dapat melihat pratinjau teks subagen saat model menghasilkannya. Sebuah koneksi hanya menampilkan pratinjau thread yang sedang dibacanya: pratinjau thread anak tidak pernah muncul di aliran tingkat sesi, jadi untuk memantau subagen secara langsung, buka aliran thread miliknya sendiri. Lihat [Pratinjau event thread sesi](https://platform.claude.com/docs/id/managed-agents/event-deltas#preview-session-thread-events) untuk cara mengaktifkan, mengakumulasi, dan merekonsiliasi pratinjau.

Dalam sebuah eksekusi workflow, server menjalankan workflow: sebuah program yang ditulis oleh agen thread utama. Pada setiap thread milik eksekusi, `agent.thread_message_received` pertama adalah prompt yang ditulis oleh workflow. `from_session_thread_id`-nya adalah ID thread utama, dan event tersebut tidak memiliki `from_agent_name`. API tidak menjamin teks prompt tersebut, jadi jangan mem-parsing-nya. Event `session.thread_status_terminated` milik thread, pada aliran thread utama, memberi tahu Anda bahwa thread telah selesai. Tidak ada event yang mencatat hasil yang dikembalikannya ke workflow.

Aliran thread tidak memutar ulang event sebelumnya. Tepat setelah `session.thread_created`, daftar event thread milik eksekusi dapat kosong, karena server menulis event pertama thread setelahnya. Jadi, buka aliran thread terlebih dahulu, lalu cantumkan event thread tersebut, dan lewati setiap event yang di-streaming yang `id`-nya telah dikembalikan oleh daftar.

<Tabs>
  <Tab title="Streaming event thread sesi">
    <CodeGroup>
      ```bash cURL
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
      ```

      ```bash CLI
      ant beta:sessions:threads:events stream \
        --session-id "$SESSION_ID" \
        --thread-id "$THREAD_ID"
      ```

      ```python Python
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
      ```

      ```typescript TypeScript
      const stream = await client.beta.sessions.threads.events.stream(thread.id, {
        session_id: session.id,
      });

      loop: for await (const event of stream) {
        switch (event.type) {
          case "agent.message":
            for (const block of event.content) {
              if (block.type === "text") {
                process.stdout.write(block.text);
              }
            }
            break;
          case "session.thread_status_idle":
            break loop;
        }
      }
      ```

      ```csharp C#
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
      ```

      ```go Go
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
      ```

      ```java Java
      try (var streamResponse = client.beta().sessions().threads().events().streamStreaming(
          thread.id(),
          EventStreamParams.builder().sessionId(session.id()).build()
      )) {
          loop:
          for (var event : (Iterable<BetaManagedAgentsStreamSessionThreadEvents>) streamResponse.stream()::iterator) {
              switch (event.type().value()) {
                  case AGENT_MESSAGE -> {
                      for (var block : event.asAgentMessage().content()) {
                          block.text().ifPresent(textBlock -> IO.print(textBlock.text()));
                      }
                  }
                  case SESSION_THREAD_STATUS_IDLE -> {
                      break loop;
                  }
              }
          }
      }
      ```

      ```php PHP
      $stream = $client->beta->sessions->threads->events->streamStream(
          $thread->id,
          sessionID: $session->id,
      );

      foreach ($stream as $event) {
          switch (true) {
              case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsAgentMessageEvent:
                  foreach ($event->content as $block) {
                      if ($block instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsTextBlock) {
                          echo $block->text;
                      }
                  }
                  break;
              case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionThreadStatusIdleEvent:
                  break 2;
          }
      }
      ```

      ```ruby Ruby
      client.beta.sessions.threads.events.stream_events(thread.id, session_id: session.id).each do |event|
        case event
        when Anthropic::Beta::Sessions::BetaManagedAgentsAgentMessageEvent
          event.content.each do |block|
            print block.text if block.is_a?(Anthropic::Beta::Sessions::BetaManagedAgentsTextBlock)
          end
        when Anthropic::Beta::Sessions::BetaManagedAgentsSessionThreadStatusIdleEvent
          break
        end
      end
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Mencantumkan event thread sesi">
    Cantumkan semua event thread sesi sebelumnya untuk mengambil riwayat lengkap.

    <CodeGroup>
      ```bash cURL
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
        session_id: session.id,
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
          var type = event._json().orElseThrow() instanceof JsonObject json
              ? json.values().get("type").asStringOrThrow()
              : "unknown";
          var processedAt = event.processedAt().map(OffsetDateTime::toString).orElse("pending");
          IO.println("[" + type + "] " + processedAt);
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
  </Tab>
</Tabs>

## Izin alat dan alat kustom

Jika sebuah subagen memerlukan sesuatu dari klien Anda, seperti [izin](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#tool-confirmation) untuk menjalankan panggilan alat atau [hasil dari alat kustom](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls), event tersebut diposting silang ke **thread utama** dengan `session_thread_id` yang mengidentifikasi thread sesi asalnya. Sebuah panggilan alat memerlukan izin Anda di bawah `always_ask`, atau di bawah [`auto`](https://platform.claude.com/docs/id/managed-agents/permission-policies#let-the-server-evaluate-each-call-with-auto) ketika server tidak mencapai keputusan.

```json
{
  "type": "session.thread_status_idle",
  "id": "sevt_01ABC...",
  "session_thread_id": "sthr_01DEF...",
  "agent_name": "code-reviewer",
  "stop_reason": {
    "type": "requires_action",
    "event_ids": ["sevt_01XYZ..."]
  }
}
```

Kirim `user.tool_confirmation` (dengan `tool_use_id`) atau `user.custom_tool_result` (dengan `custom_tool_use_id`); server secara otomatis merutekan respons ke thread yang benar. Respons dapat muncul di thread utama dan di thread subagen dengan nilai `id` yang berbeda. Untuk mencocokkan kedua salinan tersebut, bandingkan `type` dan `tool_use_id` (atau `custom_tool_use_id`), bukan `id`.

Sesi menjadi `idle` hanya ketika tidak ada thread yang berstatus `running`, sehingga `session.status_idle` dapat tiba lama setelah panggilan subagen. Anda tidak perlu menunggunya: kirim `user.custom_tool_result` segera setelah event `agent.custom_tool_use` yang diposting silang tiba.

Di bawah `auto`, event `user.message` Anda dapat membuat server mengizinkan panggilan yang seharusnya ditolaknya. Tidak ada apa pun di thread subagen yang dihitung sebagai maksud Anda. Klien Anda tidak memposting pesan apa pun di sana, dan pesan yang dikirimkan agen thread utama kepada subagen tidak dihitung. Ketika server menolak panggilan di bawah `auto`, tidak ada yang diposting silang: event dan hasil alat berupa error hanya muncul di [aliran thread](https://platform.claude.com/docs/id/managed-agents/session-threads#session-thread-events) milik subagen itu sendiri, dan subagen tetap berjalan.

Contoh berikut ditempatkan di dalam loop event dari [handler konfirmasi alat](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#tool-confirmation). Untuk setiap ID dalam `stop_reason.event_ids`, contoh ini mengirimkan `user.tool_confirmation` yang mengizinkan panggilan tersebut. Pola yang sama berlaku untuk `user.custom_tool_result`.

<CodeGroup>
  ```bash cURL
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
  ```

  ```bash CLI
  # Workflow ini tidak cocok diterjemahkan menjadi perintah shell sekali jalan.
  # Sebagai gantinya, gunakan salah satu contoh SDK di grup kode ini.
  ```

  ```python Python
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
  ```

  ```typescript TypeScript
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
  ```

  ```csharp C#
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
  ```

  ```go Go
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
  ```

  ```java Java
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
  ```

  ```php PHP
  foreach ($event->stopReason->eventIDs as $eventId) {
      $client->beta->sessions->events->send($session->id, events: [[
          'type' => 'user.tool_confirmation',
          'tool_use_id' => $eventId,
          'result' => 'allow',
      ]]);
  }
  ```

  ```ruby Ruby
  event_ids.each do |event_id|
    client.beta.sessions.events.send_(session.id, events: [{
      type: "user.tool_confirmation",
      tool_use_id: event_id,
      result: "allow"
    }])
  end
  ```
</CodeGroup>

Pola sebelumnya menjawab panggilan yang dicantumkan oleh event idle. Pada aliran utama, event `session.thread_status_idle` milik subagen dapat tiba sebelum event `agent.tool_use` atau `agent.mcp_tool_use` yang dicantumkan oleh `stop_reason.event_ids`-nya. `user.tool_confirmation` untuk panggilan yang event-nya belum tiba dapat mengembalikan 400. Untuk menghindarinya, jawab setiap panggilan yang [`evaluated_permission`](https://platform.claude.com/docs/id/managed-agents/permission-policies#see-how-each-call-was-evaluated)-nya bernilai `ask` ketika event miliknya sendiri tiba di aliran utama.
