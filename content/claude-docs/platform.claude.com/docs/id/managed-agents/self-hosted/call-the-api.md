---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 31f94d77e4098391ab0034e96582d590158c54fef5e4e1557d06a4b4a5f03994
---

---
title: Memanggil API pada server yang di-host sendiri
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api
description: Arahkan SDK resmi, cURL, atau CLI ant ke server Claude Managed Agents yang di-host sendiri milik Anda, mulai sesi, dan baca balasan agen. Lalu hubungkan worker Anda sendiri, jika Anda membutuhkannya.
---

<Note>
  Untuk meminta akses ke Claude Managed Agents yang di-host sendiri, hubungi tim akun Anthropic Anda.
</Note>

Server Claude Managed Agents yang di-host sendiri memiliki API yang sama dengan layanan [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) yang di-hosting oleh Anthropic. Kode Anda memanggilnya dengan SDK resmi, cURL, atau CLI `ant`. Ada dua hal yang berubah: “base URL” (URL dasar) adalah alamat server Anda, dan kunci API adalah [kunci API server](https://platform.claude.com/docs/id/managed-agents/self-hosted#the-three-credentials) Anda, bukan kunci API Claude.

Untuk membuat agen dan menjalankan sesi di browser, lihat [Gunakan konsol di server Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/console).

## Prasyarat

* **Server yang berjalan:** Mulai satu server dengan [Memulai dengan Claude Managed Agents yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/quickstart) atau [Menerapkan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes).
* **Akses ke server:** Jika orang lain yang menjalankan server, tanyakan kepada mereka alamat server dan cara melakukan autentikasi. Jika mereka menggunakan single sign-on, lihat [Mengizinkan developer login dari terminal](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#let-developers-log-in-from-a-terminal).
* **CLI `ant`:** Instal versi terbaru, seperti yang ditunjukkan di [quickstart CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart#installation).

## Mengarahkan klien Anda ke server Anda

SDK dan CLI `ant` membaca alamat server dari `ANTHROPIC_BASE_URL` dan kunci API dari `ANTHROPIC_API_KEY`. Atur kedua variabel tersebut di terminal yang Anda gunakan khusus untuk server ini.

Untuk [stack quickstart](https://platform.claude.com/docs/id/managed-agents/self-hosted/quickstart), jalankan perintah berikut dari direktori yang berisi file `.env` Anda:

```bash
export ANTHROPIC_BASE_URL=http://127.0.0.1:8400
export ANTHROPIC_API_KEY=$(grep '^CMA_SERVER__API_KEY=' .env | cut -d= -f2)
```

Di Kubernetes, atur kedua variabel tersebut seperti yang ditunjukkan di [Menjalankan sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#run-a-session), dan biarkan port-forward-nya tetap berjalan.

Di terminal tersebut, setiap perintah `ant`, seperti `ant beta:agents list`, menjangkau server Anda. Jangan jalankan Claude Code atau `docker compose` di terminal tersebut, karena keduanya membaca variabel yang sama.

## Memulai sesi

Sebuah sesi memerlukan ID agen dan ID lingkungan:

* **Agen:** Buat satu seperti yang ditunjukkan di [Membuat agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#create-an-agent), dengan klien Anda diarahkan ke server Anda. Jika Anda mengirim permintaan HTTP mentah, ganti `https://api.anthropic.com` di URL dengan `$ANTHROPIC_BASE_URL`.
* **Lingkungan:** Stack quickstart membuat satu environment bernama `compose-sandbox`, dan Helm chart membuat satu environment bernama `default`. `ant beta:environments list` mencetak nama dan ID setiap environment. Untuk worker Anda sendiri, ID tersebut adalah ID yang dicetak oleh CLI admin di [Menjalankan worker Anda sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api#point-a-worker-at-your-server).

Masukkan kedua ID Anda ke shell Anda, sebagai pengganti ID contoh berikut:

```bash
export AGENT_ID=agent_011CYm1BLqPXpQRk5khsSXrs
export ENVIRONMENT_ID=env_01595EKxaaTTGwwY3kyXdtbs
```

Contoh berikut membuat sesi dan mengirim pesan pertamanya dalam permintaan yang sama:

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body "$ANTHROPIC_BASE_URL/v1/sessions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "agent": "'"$AGENT_ID"'",
      "environment_id": "'"$ENVIRONMENT_ID"'",
      "initial_events": [
        {
          "type": "user.message",
          "content": [{"type": "text", "text": "List the files in the working directory."}]
        }
      ]
    }'
  ```

  ```bash CLI
  ant beta:sessions create --agent "$AGENT_ID" --environment-id "$ENVIRONMENT_ID" \
    --initial-event '{type: user.message, content: [{type: text, text: "List the files in the working directory."}]}'
  ```

  ```python Python
  import os

  from anthropic import Anthropic

  client = Anthropic()

  session = client.beta.sessions.create(
      agent=os.environ["AGENT_ID"],
      environment_id=os.environ["ENVIRONMENT_ID"],
      initial_events=[
          {
              "type": "user.message",
              "content": [
                  {"type": "text", "text": "List the files in the working directory."}
              ],
          },
      ],
  )
  print(session.id)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const session = await client.beta.sessions.create({
    agent: process.env["AGENT_ID"]!,
    environment_id: process.env["ENVIRONMENT_ID"]!,
    initial_events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "List the files in the working directory." }]
      }
    ]
  });
  console.log(session.id);
  ```

  ```csharp C#
  using System;
  using Anthropic;
  using Anthropic.Models.Beta.Agents;
  using Anthropic.Models.Beta.Sessions;
  using Anthropic.Models.Beta.Sessions.Events;

  AnthropicClient client = new();

  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = Environment.GetEnvironmentVariable("AGENT_ID")!,
      EnvironmentID = Environment.GetEnvironmentVariable("ENVIRONMENT_ID")!,
      InitialEvents =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Content =
              [
                  new BetaManagedAgentsTextBlock
                  {
                      Text = "List the files in the working directory.",
                  },
              ],
          },
      ],
  });
  Console.WriteLine(session.ID);
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go/v2"
  )

  func main() {
  	client := anthropic.NewClient()

  	session, err := client.Beta.Sessions.New(context.Background(), anthropic.BetaSessionNewParams{
  		Agent: anthropic.BetaSessionNewParamsAgentUnion{
  			OfString: anthropic.String(os.Getenv("AGENT_ID")),
  		},
  		EnvironmentID: os.Getenv("ENVIRONMENT_ID"),
  		InitialEvents: []anthropic.BetaSessionNewParamsInitialEventUnion{{
  			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  						Text: "List the files in the working directory.",
  					},
  				}},
  			},
  		}},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(session.ID)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.beta.sessions.SessionCreateParams;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserMessageEventParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var session = client.beta().sessions().create(SessionCreateParams.builder()
          .agent(System.getenv("AGENT_ID"))
          .environmentId(System.getenv("ENVIRONMENT_ID"))
          .addInitialEvent(BetaManagedAgentsUserMessageEventParams.builder()
              .addTextContent("List the files in the working directory.")
              .build())
          .build());
      IO.println(session.id());
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Client;

  $client = new Client();

  $session = $client->beta->sessions->create(
      agent: (string) getenv('AGENT_ID'),
      environmentID: (string) getenv('ENVIRONMENT_ID'),
      initialEvents: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => 'List the files in the working directory.']],
          ],
      ],
  );
  echo $session->id, "\n";
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  session = client.beta.sessions.create(
    agent: ENV.fetch("AGENT_ID"),
    environment_id: ENV.fetch("ENVIRONMENT_ID"),
    initial_events: [
      {
        type: :"user.message",
        content: [{type: :text, text: "List the files in the working directory."}]
      }
    ]
  )
  puts session.id
  ```
</CodeGroup>

Respons berisi ID sesi, yang diawali dengan `sesn_`. Agen langsung mulai bekerja. Alat bawaannya, seperti `bash`, berjalan pada worker yang melayani environment tersebut.

Untuk memantau sesi, buka [konsol di server Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/console) di browser, pilih **Sessions**, lalu pilih sesi tersebut. Sesi yang Anda mulai dengan kunci API server, seperti di halaman ini, hanya terlihat oleh administrator.

Untuk mengikuti sesi di terminal Anda, teruskan ID-nya ke [`ant beta:sessions connect`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/sessions-connect):

```bash
ant beta:sessions connect sesn_011CZkZAtmR3yMPDzynEDxu7
```

Untuk hal lain yang dapat dilakukan sesi, seperti menyematkan versi agen, lihat [Memulai sesi](https://platform.claude.com/docs/id/managed-agents/sessions).

## Mengirim pesan dan membaca balasan

Masukkan ID sesi Anda ke shell Anda, sebagai pengganti ID contoh berikut:

```bash
export SESSION_ID=sesn_011CZkZAtmR3yMPDzynEDxu7
```

Tunggu hingga sesi dalam keadaan idle sebelum Anda menjalankan contoh berikutnya. Contoh tersebut berhenti membaca ketika sebuah giliran berakhir. Jika giliran sebelumnya masih berjalan, akhir giliran tersebut dapat menghentikan contoh sebelum balasan untuk pesan Anda tiba. Konsol dan `ant beta:sessions connect` sama-sama menampilkan status sesi.

Contoh berikut mengirim pesan dan mencetak balasan agen. Contoh ini membuka aliran event sesi terlebih dahulu, karena aliran hanya mengirimkan event yang muncul setelah aliran dibuka:

<CodeGroup exclude="shell">
  <CodeGroupItem language="cURL">
    Alur kerja ini membutuhkan lebih banyak logika daripada satu perintah shell. Gunakan [Anthropic SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk menjalankannya.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Alur kerja ini membutuhkan lebih banyak logika daripada satu perintah shell. Untuk mengirim pesan dan membaca balasan di terminal Anda, gunakan [`ant beta:sessions connect`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/sessions-connect).
  </CodeGroupItem>

  ```python Python
  import os

  from anthropic import Anthropic

  client = Anthropic()
  session_id = os.environ["SESSION_ID"]

  with client.beta.sessions.events.stream(session_id) as stream:
      client.beta.sessions.events.send(
          session_id,
          events=[
              {
                  "type": "user.message",
                  "content": [
                      {"type": "text", "text": "Summarize what you did in one sentence."}
                  ],
              },
          ],
      )

      for event in stream:
          match event.type:
              case "agent.message":
                  for block in event.content:
                      if block.type == "text":
                          print(block.text, end="")
              case "session.error":
                  error_message = event.error.message if event.error else "unknown"
                  print(f"\n[Error: {error_message}]")
              case "session.status_idle":
                  if event.stop_reason.type != "requires_action":
                      break
              case "session.status_terminated":
                  break
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();
  const sessionId = process.env["SESSION_ID"]!;

  const stream = await client.beta.sessions.events.stream(sessionId);
  await client.beta.sessions.events.send(sessionId, {
    events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "Summarize what you did in one sentence." }]
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
      case "session.error":
        console.log(`\n[Error: ${event.error?.message ?? "unknown"}]`);
        break;
      case "session.status_idle":
        if (event.stop_reason.type !== "requires_action") {
          break events;
        }
        break;
      case "session.status_terminated":
        break events;
    }
  }
  ```

  ```csharp C#
  using System;
  using Anthropic;
  using Anthropic.Models.Beta.Sessions.Events;

  AnthropicClient client = new();
  var sessionId = Environment.GetEnvironmentVariable("SESSION_ID")!;

  using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(sessionId);
  await client.Beta.Sessions.Events.Send(sessionId, new()
  {
      Events =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Content = [new BetaManagedAgentsTextBlock { Text = "Summarize what you did in one sentence." }],
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
      else if (streamEvent.Value is BetaManagedAgentsSessionErrorEvent error)
      {
          Console.WriteLine($"\n[Error: {error.Error?.Message ?? "unknown"}]");
      }
      else if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent idle
          && idle.StopReason?.Value is not BetaManagedAgentsSessionRequiresAction)
      {
          break;
      }
      else if (streamEvent.Value is BetaManagedAgentsSessionStatusTerminatedEvent)
      {
          break;
      }
  }
  ```

  ```go Go
  package main

  import (
  	"cmp"
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go/v2"
  )

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()
  	sessionID := os.Getenv("SESSION_ID")

  	stream := client.Beta.Sessions.Events.StreamEvents(ctx, sessionID, anthropic.BetaSessionEventStreamParams{})
  	defer stream.Close()

  	if _, err := client.Beta.Sessions.Events.Send(ctx, sessionID, anthropic.BetaSessionEventSendParams{
  		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  						Text: "Summarize what you did in one sentence.",
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
  				if block.Type == "text" {
  					fmt.Print(block.Text)
  				}
  			}
  		case anthropic.BetaManagedAgentsSessionErrorEvent:
  			fmt.Printf("\n[Error: %s]\n", cmp.Or(event.Error.Message, "unknown"))
  		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
  			if _, paused := event.StopReason.AsAny().(anthropic.BetaManagedAgentsSessionRequiresAction); !paused {
  				break events
  			}
  		case anthropic.BetaManagedAgentsSessionStatusTerminatedEvent:
  			break events
  		}
  	}
  	if err := stream.Err(); err != nil {
  		panic(err)
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonObject;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserMessageEventParams;
  import com.anthropic.models.beta.sessions.events.EventSendParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();
      var sessionId = System.getenv("SESSION_ID");

      try (var stream = client.beta().sessions().events().streamStreaming(sessionId)) {
          client.beta().sessions().events().send(
              sessionId,
              EventSendParams.builder()
                  .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                      .addTextContent("Summarize what you did in one sentence.")
                      .build())
                  .build()
          );

          events:
          for (var event : stream) {
              switch (event.type().value()) {
                  case AGENT_MESSAGE -> {
                      for (var block : event.asAgentMessage().content()) {
                          block.text().ifPresent(textBlock -> IO.print(textBlock.text()));
                      }
                  }
                  case SESSION_ERROR -> {
                      var errorMessage =
                          event.asSessionError().error()._json().orElse(null) instanceof JsonObject json
                              ? json.values().get("message").asStringOrThrow()
                              : "unknown";
                      IO.println("\n[Error: " + errorMessage + "]");
                  }
                  case SESSION_STATUS_IDLE -> {
                      if (!event.asSessionStatusIdle().stopReason().isRequiresAction()) {
                          break events;
                      }
                  }
                  case SESSION_STATUS_TERMINATED -> {
                      break events;
                  }
                  default -> {}
              }
          }
      }
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Beta\Sessions\Events\ManagedAgentsAgentMessageEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsSessionErrorEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsSessionRequiresAction;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsSessionStatusIdleEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsSessionStatusTerminatedEvent;
  use Anthropic\Beta\Sessions\Events\ManagedAgentsTextBlock;
  use Anthropic\Client;

  $client = new Client();
  $sessionId = (string) getenv('SESSION_ID');

  $stream = $client->beta->sessions->events->streamStream($sessionId);
  $client->beta->sessions->events->send(
      $sessionId,
      events: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => 'Summarize what you did in one sentence.']],
          ],
      ],
  );

  foreach ($stream as $event) {
      switch (true) {
          case $event instanceof ManagedAgentsAgentMessageEvent:
              foreach ($event->content as $block) {
                  if ($block instanceof ManagedAgentsTextBlock) {
                      echo $block->text;
                  }
              }
              break;
          case $event instanceof ManagedAgentsSessionErrorEvent:
              printf("\n[Error: %s]\n", $event->error->message);
              break;
          case $event instanceof ManagedAgentsSessionStatusIdleEvent:
              if (!($event->stopReason instanceof ManagedAgentsSessionRequiresAction)) {
                  break 2; // Break foreach loop
              }
              break;
          case $event instanceof ManagedAgentsSessionStatusTerminatedEvent:
              break 2; // Break foreach loop
      }
  }
  $stream->close();
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new
  session_id = ENV.fetch("SESSION_ID")

  stream = client.beta.sessions.events.stream_events(session_id)

  client.beta.sessions.events.send_(
    session_id,
    events: [{
      type: "user.message",
      content: [{type: "text", text: "Summarize what you did in one sentence."}]
    }]
  )

  stream.each do |event|
    case event
    when Anthropic::Beta::Sessions::BetaManagedAgentsAgentMessageEvent
      event.content.each do |block|
        print block.text if block.is_a?(Anthropic::Beta::Sessions::BetaManagedAgentsTextBlock)
      end
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionErrorEvent
      puts "\n[Error: #{event.error&.message || "unknown"}]"
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusIdleEvent
      break unless event.stop_reason.is_a?(Anthropic::Beta::Sessions::BetaManagedAgentsSessionRequiresAction)
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusTerminatedEvent
      break
    else
      # abaikan jenis event lainnya
    end
  end
  ```
</CodeGroup>

Selain mencetak teks `agent.message`, loop menangani tiga event:

* **`session.status_idle`:** Loop berakhir, kecuali `stop_reason.type` milik event tersebut adalah `requires_action`.
* **`session.status_terminated`:** Loop berakhir.
* **`session.error`:** Loop mencetak pesan error tersebut dan terus membaca, karena server dapat mencoba ulang panggilan model yang gagal dan menyelesaikan giliran tersebut.

`requires_action` berarti sesi dijeda untuk panggilan alat. Apa yang mengakhiri jeda tersebut bergantung pada panggilannya:

* **Panggilan alat kustom, atau permintaan untuk mengonfirmasi panggilan alat:** Hanya kode Anda yang dapat menjawabnya. Jika agen Anda menggunakan salah satunya, lihat [Menjawab panggilan alat yang menjeda sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#answer-tool-calls-that-pause-the-session).
* **Panggilan ke alat yang dijalankan oleh worker, seperti `bash`:** Panggilan ini biasanya tidak menjeda sesi. Jika tidak ada worker yang mengambil panggilan tersebut selama sekitar 3 menit, sesi dijeda hingga sebuah worker mengembalikan hasilnya. Dalam kasus tersebut, kode Anda tidak perlu menjawab apa pun. Biarkan aliran tetap terbuka, dan giliran akan berlanjut ketika worker menjalankan panggilan tersebut.

Untuk event lain yang dikirim sesi, dan cara menyambung ulang tanpa melewatkan satu pun, lihat [Aliran event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming).

## Memindahkan data masuk dan keluar dari sesi

Data masuk ke sesi dan keluar darinya melalui direktori kerja worker.

Pada stack quickstart, container setiap sesi dimulai dengan direktori `/workspace` yang kosong, kecuali clone dari repositori sesi tersebut. Secara default, sekitar satu menit setelah sebuah giliran berakhir, container berhenti, dan Docker menghapusnya bersama direktori tersebut. Apa pun yang harus disimpan oleh sesi harus dikeluarkan melalui pemanggilan alat, seperti unggahan atau `git push`, sebelum itu terjadi.

Container juga berhenti sekitar satu jam setelah dimulai, bahkan di tengah sebuah giliran. Tidak ada pengaturan yang mengubah hal tersebut. Giliran berlanjut di container baru, biasanya setelah satu atau dua menit, dan klien Anda tidak menerima event apa pun untuk peralihan tersebut. Peralihan ini memiliki dua konsekuensi:

* **Perintah:** Semua yang berjalan di container lama berhenti. Container baru menjalankan ulang panggilan alat yang terputus dari awal, tetapi tidak ada yang memulai ulang perintah yang dibiarkan agen berjalan di latar belakang.
* **File:** Direktori `/workspace` milik container baru kembali kosong, kecuali clone baru dari repositori sesi tersebut.

Dalam giliran yang panjang, minta agen mengunggah atau melakukan push atas pekerjaannya secara bertahap, dan hindari perintah yang menimbulkan masalah jika dijalankan dua kali.

Di Kubernetes, sebuah sesi mempertahankan satu pod paling lama sekitar satu jam, dan giliran berlanjut dengan cara yang sama. Ada dua hal yang berbeda: pod baru menemukan file sesi di `/workspace`, dan pod tersebut dimulai sekitar 6 menit setelah pod lama berhenti.

Untuk worker yang Anda mulai sendiri, letakkan file input di direktori kerja sebelum Anda mengirim pesan yang membutuhkannya. Baca file output darinya setelahnya.

Jika Anda sendiri yang memulai container untuk setiap sesi, mount direktori yang berisi file input sesi sebagai direktori kerja container. Kumpulkan file output darinya setelah container berhenti. Lihat [Menyiapkan file untuk sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#stage-files-for-a-session).

## Menemukan contoh lainnya di panduan layanan yang di-hosting

Panduan layanan yang di-hosting menjelaskan [konsep inti](https://platform.claude.com/docs/id/managed-agents/overview#core-concepts) API dan memiliki contoh untuk setiap fitur. Contoh SDK dan CLI pada panduan-panduan tersebut memanggil server Anda saat Anda menjalankannya di terminal tempat `ANTHROPIC_BASE_URL` dan `ANTHROPIC_API_KEY` diatur. Contoh cURL pada panduan-panduan tersebut menyebutkan `https://api.anthropic.com`, jadi ganti alamat tersebut dengan `$ANTHROPIC_BASE_URL` sebelum Anda menjalankannya.

Untuk beberapa fitur, server Anda memerlukan pengaturan terlebih dahulu, atau sebuah contoh perlu diubah:

| Tugas                                                 | Panduan layanan yang di-hosting                                                                                                                                            | Di server Anda                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mengatur model, prompt sistem, dan versi agen         | [Definisikan agen Anda](https://platform.claude.com/docs/id/managed-agents/agent-setup)                                                                                    | Beberapa field [bergantung pada penyedia inferensi Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences#differences-that-depend-on-your-inference-provider).                                                                                                                                                             |
| Memilih alat bawaan, atau menambahkan alat kustom     | [Alat](https://platform.claude.com/docs/id/managed-agents/tools)                                                                                                           | Untuk menggunakan alat web, aktifkan alat tersebut terlebih dahulu, seperti yang dijelaskan di [Alat web memerlukan pengaturan server](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences#web-tools-need-a-server-setting). Alat mana yang tersedia bergantung pada penyedia inferensi Anda.                                 |
| Menghubungkan server MCP dan menyimpan token-nya      | [Konektor MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) dan [Autentikasi dengan vault](https://platform.claude.com/docs/id/managed-agents/vaults) | Tambahkan host server MCP ke [allowlist untuk server MCP](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences#mcp-servers-need-an-allowlist-entry). Simpan token sebagai kredensial `static_bearer`.                                                                                                                          |
| Memberikan skill kepada agen                          | [Skill](https://platform.claude.com/docs/id/managed-agents/skills)                                                                                                         | Unggah setiap skill sebagai file-file terpisah, karena server Anda menolak arsip zip. [Skill bawaan](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences#features-that-arent-available) dalam contoh panduan tersebut tidak tersedia.                                                                                         |
| Menyimpan memori antarsesi                            | [Menggunakan memori agen](https://platform.claude.com/docs/id/managed-agents/memory)                                                                                       | Jika Anda menjalankan worker sendiri, berikan direktori `/mnt/memory` yang dapat ditulisi kepada worker tersebut, seperti di [Penyimpanan memori di sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory).                                                                                  |
| Menyerahkan pekerjaan ke agen lain                    | [Orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration)                                                                        | Ganti blok `multiagent_20261001` dalam contoh panduan tersebut dengan [blok `coordinator`](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences#features-that-behave-differently).                                                                                                                                             |
| Bekerja di repositori Git                             | [Mengakses GitHub](https://platform.claude.com/docs/id/managed-agents/github)                                                                                              | Daftarkan host Git di pengaturan server Anda, seperti yang dijelaskan di [Repositori Git memerlukan entri allowlist](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences#git-repositories-need-an-allowlist-entry). Contoh agen dalam panduan tersebut juga memerlukan `api.githubcopilot.com` di allowlist untuk server MCP. |
| Meminta grader memeriksa pekerjaan berdasarkan rubrik | [Mendefinisikan hasil](https://platform.claude.com/docs/id/managed-agents/define-outcomes)                                                                                 | Kirim rubrik sebagai teks. Files API tidak tersedia, jadi [kumpulkan file output](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api#move-data-in-and-out-of-a-session) dari direktori kerja.                                                                                                                               |
| Mengikuti sesi dan menjawab panggilan alatnya         | [Aliran event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming)                                                                               | Contoh pertama dalam panduan tersebut menutup aliran pada jeda apa pun, jadi mulailah dari loop di [Mengirim pesan dan membaca balasan](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api#send-a-message-and-read-the-reply) sebagai gantinya.                                                                             |

[Perbedaan dari layanan yang di-hosting](https://platform.claude.com/docs/id/managed-agents/self-hosted/differences) berisi daftar lengkapnya. Periksa daftar tersebut sebelum Anda memindahkan aplikasi yang sudah ada.

## Menjalankan worker Anda sendiri

[Stack quickstart](https://platform.claude.com/docs/id/managed-agents/self-hosted/quickstart) membuat environment dan menjalankan worker-nya. Begitu pula Helm chart di [Menerapkan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes). Jika worker tersebut sudah cukup untuk kebutuhan Anda, lewati bagian ini.

Anda menjalankan worker seperti yang Anda lakukan untuk [sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes): perintah `ant beta:worker` dan worker SDK yang sama, dengan cara-cara yang ditunjukkan di [Menerapkan worker self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers). Pengecualiannya adalah worker yang dipicu oleh webhook, karena server Anda tidak mengirimkan webhook apa pun.

### Membuat environment dan kuncinya

Buat environment dan kunci environment dengan CLI admin, bukan di Claude Console. CLI tersebut, `cma-server-admin`, berada di bagian teratas arsip rilis, jadi jalankan perintah dari sana. Untuk `-base-url`, teruskan alamat yang digunakan worker Anda untuk menjangkau server:

* **Worker di mesin yang menjalankan stack quickstart:** `http://127.0.0.1:8400`
* **Worker di mesin lain:** alamat `https` dari [proxy TLS yang Anda tempatkan di depan server](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#put-tls-in-front-of-the-server)

CLI admin memanggil server di alamat yang sama, jadi jalankan CLI tersebut di mesin yang dapat menjangkau alamat tersebut.

```bash
echo "$ANTHROPIC_API_KEY" | ./cma-server-admin bootstrap \
  -base-url http://127.0.0.1:8400 -name my-env -key-file -
```

Perintah ini mencetak pengaturan worker, perintah yang memulai worker, serta ID dan masa berlaku kunci:

```text wrap
export ANTHROPIC_BASE_URL='http://127.0.0.1:8400'
export ANTHROPIC_ENVIRONMENT_ID='env_...'
export ANTHROPIC_ENVIRONMENT_KEY='sk-ant-oat01-...'
# then: histchars= HISTFILE=/dev/null ant beta:worker poll --workdir /workspace
# key id: 'etok_...'  expires: '...'
```

Perintah tersebut hanya menampilkan kunci sekali, jadi simpan kunci, ID-nya, dan masa berlakunya di secret manager Anda. Kunci berhenti berfungsi setelah 365 hari. Sebelum itu, ikuti [Mengganti kunci environment untuk worker Anda sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#replace-an-environment-key-for-your-own-workers).

Jauhkan kunci API server dari mesin yang menjalankan worker. Jalankan worker di container atau VM yang tidak menyimpan apa pun yang perlu Anda lindungi. Untuk tugas keamanan Anda lainnya, lihat [Tanggung jawab keamanan Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted#your-security-responsibilities).

### Menjalankan eksperimen lokal

Jalankan ketiga baris `export` di shell tempat Anda memulai worker. Lalu mulai worker dengan perintah berikut, bukan perintah yang dicetak. Perintah pertama membuat direktori kerja worker, karena worker tidak membuatnya:

```bash
mkdir -p "$HOME/cma-workspace" "$HOME/.config/cma"
cat > "$HOME/.config/cma/worker.inputrc" <<'EOF'
$include /etc/inputrc
set disable-completion on
EOF
histchars= HISTFILE=/dev/null INPUTRC="$HOME/.config/cma/worker.inputrc" \
  ant beta:worker poll --workdir "$HOME/cma-workspace"
```

`histchars`, `INPUTRC`, dan `HISTFILE` menyiapkan shell di balik alat `bash` milik worker, sehingga shell menjalankan setiap perintah persis seperti yang ditulis oleh agen:

* **`histchars=`:** Shell tidak memperlakukan `!` sebagai referensi ke riwayat perintahnya.
* **`INPUTRC`:** File ini menonaktifkan pelengkapan otomatis, yang jika tidak dinonaktifkan akan menelan setiap karakter tab dalam perintah. Jauhkan file ini dari direktori kerja, tempat alat file milik agen dapat menulis ulang file tersebut.
* **`HISTFILE=/dev/null`:** Shell tidak membaca maupun menulis file riwayat.

Jangan gunakan worker ini untuk hal lain. Worker ini menyimpan kunci environment dan menjalankan alat setiap sesi dalam satu proses. Worker ini juga tidak meng-clone repositori milik sebuah sesi. Sesi berjalan tanpa repositori tersebut, dan klien Anda tidak menerima error.

### Menjalankan worker di produksi

Untuk keperluan apa pun selain eksperimen lokal, mulai satu container untuk setiap sesi dan jalankan `ant beta:worker run` di dalamnya, seperti yang ditunjukkan di [Menjalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#run-one-sandbox-per-session). Berikan image-nya apa yang tercantum di [Membangun image sandbox Anda sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api#build-your-own-sandbox-image), dan ubah tiga hal dalam penyiapan tersebut:

* **Kunci environment:** Jangan teruskan `ANTHROPIC_ENVIRONMENT_KEY` ke dalam container sebuah sesi. Server menerima kunci tersebut untuk setiap sesi di environment, sedangkan container hanya memerlukan akses ke satu sesi.
* **Secret milik work item:** Teruskan secret ini sebagai pengganti kunci tersebut, karena server menerimanya hanya untuk satu sesi itu. [Meneruskan secret item pekerjaan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#forward-the-work-items-secret) menunjukkan tempat kode Anda menerimanya. Di tempat bagian tersebut mengatur `ANTHROPIC_WORK_SECRET`, letakkan secret tersebut dalam file yang hanya dapat dibaca oleh pengguna container. Misalnya, salurkan secret tersebut ke input standar container, dan minta container menulis file tersebut sebelum memulai worker. Lalu atur `ANTHROPIC_WORK_SECRET_FILE` ke path file tersebut.
* **Alamat server:** Atur `ANTHROPIC_BASE_URL` ke alamat yang dapat dijangkau container. `http://127.0.0.1:8400` bukan salah satunya.

Untuk worker SDK, dua hal lagi berlaku:

* **Versi:** Bangun worker pada versi terbaru SDK, seperti yang dijelaskan di [SDK, CLI, dan library](https://platform.claude.com/docs/id/cli-sdks-libraries/overview). Worker pada versi tersebut menunggu persetujuan sebelum menjalankan panggilan alat yang memerlukannya, dan tidak pernah menjalankan panggilan yang ditolak oleh kebijakan. Worker yang dibangun pada versi lama menjalankan setiap panggilan alat segera setelah panggilan tersebut tiba.
* **Contoh:** Contoh di [Menjalankan worker SDK di dalam sandbox](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#run-the-sdk-worker-inside-the-sandbox) membaca kunci environment, sehingga contoh tersebut tidak berfungsi di sini apa adanya.

### Membangun image sandbox Anda sendiri

Image milik Anda sendiri memerlukan paket dan pengaturan berikut:

* **Paket:** Git 2.38 atau yang lebih baru, `curl`, `jq`, dan ripgrep, yang digunakan oleh alat `grep` milik worker untuk melakukan pencarian.

* **Pengaturan shell:** `histchars`, `HISTFILE`, dan `INPUTRC`, seperti pada eksperimen lokal, serta `TERMINFO`. Letakkan baris-baris berikut di Dockerfile, sebelum baris `USER` mana pun:

  ```dockerfile
  ENV histchars=
  RUN printf '\nset disable-completion on\n' >> /etc/inputrc
  ENV INPUTRC=/etc/inputrc TERMINFO=/etc/terminfo HISTFILE=/dev/null
  RUN test -r /etc/terminfo/d/dumb
  ```

  `TERMINFO` harus menyebutkan direktori yang berisi `d/dumb`, deskripsi terminal yang dibaca oleh `bash` milik worker. Di Alpine dengan `bash` terinstal, direktori tersebut adalah `/etc/terminfo`, seperti yang ditunjukkan. Pada base lain, seperti Debian atau Ubuntu, direktori tersebut adalah `/lib/terminfo` atau `/usr/share/terminfo`, mana pun yang berisi `d/dumb`. Tuliskan direktori tersebut di pengaturan `TERMINFO` dan di baris `RUN test`, yang menghentikan build jika file tersebut tidak ada.

Image tersebut juga memerlukan dua skrip dari arsip, yang berjalan sebelum worker dimulai:

1. Salin `image-build/with-repositories.sh` ke `/usr/local/bin/cma-with-repositories`. Skrip ini meng-clone repositori milik satu sesi.
2. Salin `image-build/with-egress.sh` ke `/usr/local/bin/cma-with-egress`. Skrip ini mengarahkan alat sesi ke [egress gateway](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#environment-variable-credentials), jika server Anda menjalankannya.
3. Jadikan kedua file tersebut dapat dieksekusi.
4. Letakkan keduanya di depan perintah worker, seperti pada `cma-with-egress cma-with-repositories ant beta:worker run ...`. Lewati langkah ini jika image Anda menjalankan `kubernetes/sandbox/worker.sh` dari arsip, karena skrip tersebut memulai worker dengan cara ini.

Worker yang dimulai tanpa `cma-with-repositories` menjalankan sesi tanpa repositori. Klien Anda tidak menerima error.

### Memindahkan worker dari layanan yang di-hosting

Jika Anda sudah menjalankan worker untuk layanan yang di-hosting oleh Anthropic, worker yang sama dapat melayani server Anda sebagai gantinya. Lakukan tiga hal:

* Berikan ketiga nilai `export` yang dicetak oleh CLI admin kepada proses yang melakukan polling untuk pekerjaan.
* Mulai proses tersebut dengan `histchars`, `HISTFILE`, dan `INPUTRC` yang diatur, seperti pada eksperimen lokal.
* Lakukan perubahan yang dijelaskan di [Menjalankan worker di produksi](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api#run-workers-in-production), dan periksa image setiap sesi berdasarkan [Membangun image sandbox Anda sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api#build-your-own-sandbox-image).

## Langkah selanjutnya

* [Mengizinkan developer login dari terminal](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#let-developers-log-in-from-a-terminal): Siapkan single sign-on, sehingga developer dapat menggunakan CLI `ant` dengan identitas mereka sendiri, di terminal tanpa `ANTHROPIC_API_KEY`.
* [Identitas dan kredensial agen](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity): Izinkan sistem luar memercayai agen Anda, dan simpan kredensial vault di pengelola rahasia Anda.
* [Penyedia inferensi](https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider): Kirim panggilan model ke penyedia cloud atau gateway model Anda sendiri.
