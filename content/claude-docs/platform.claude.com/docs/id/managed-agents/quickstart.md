---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/quickstart
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: 32e7f6acb87c6cb4c670b5f0eca95d6c65b1a6ee5ed83f86c8a8c45bc2d4f58a
---

# Memulai dengan Claude Managed Agents

Buat agen otonom pertama Anda.

---

Panduan ini memandu Anda membuat agen, menyiapkan environment, memulai sesi, dan melakukan streaming respons agen.

<Tip>
  **Lebih suka panduan interaktif?** Jalankan `/claude-api managed-agents-onboard` di versi terbaru [Claude Code](https://claude.com/product/claude-code) untuk penyiapan terpandu dan tanya jawab interaktif.
</Tip>

## Konsep inti

| Konsep          | Deskripsi                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Agent**       | Model, prompt sistem, alat, server MCP, dan skill                                                                                          |
| **Environment** | Konfigurasi untuk tempat sesi dijalankan: sandbox cloud yang dikelola Anthropic, atau sandbox yang di-host sendiri pada infrastruktur Anda |
| **Session**     | Instance agent yang sedang berjalan dalam sebuah environment, menjalankan tugas tertentu dan menghasilkan output                           |
| **Events**      | Pesan yang dipertukarkan antara aplikasi Anda dan agent (giliran pengguna, hasil alat, pembaruan status)                                   |

## Prasyarat

* Akun [Console](https://platform.claude.com) Anthropic
* Sebuah [kunci API](/settings/keys)

## Instal CLI

<Tabs>
  <Tab title="Homebrew (macOS)">
    ```bash
    brew install anthropics/tap/ant
    ```
  </Tab>

  <Tab title="curl (Linux/WSL)">
    Untuk lingkungan Linux, unduh binary rilis secara langsung.

    ```bash
    VERSION=1.15.0
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    case $(uname -m) in
      x86_64) ARCH=amd64 ;;
      aarch64) ARCH=arm64 ;;
    esac
    curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_${OS}_${ARCH}.tar.gz" \
      | sudo tar -xz -C /usr/local/bin ant
    ```

    Anda dapat menemukan semua rilis di [halaman rilis GitHub](https://github.com/anthropics/anthropic-cli/releases).
  </Tab>

  <Tab title="Go">
    Anda juga dapat menginstal CLI dari sumber menggunakan `go install`. Memerlukan Go 1.25 atau yang lebih baru.

    ```bash
    go install github.com/anthropics/anthropic-cli/cmd/ant@latest
    ```

    Binary ditempatkan di `$(go env GOPATH)/bin`. Tambahkan ke `PATH` Anda jika belum ada:

    ```bash
    export PATH="$PATH:$(go env GOPATH)/bin"
    ```
  </Tab>
</Tabs>

Periksa instalasi:

```bash
ant --version
```

## Instal SDK

<Tabs>
  <Tab title="Python">
    ```bash
    pip install anthropic
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/sdk
    ```
  </Tab>

  <Tab title="Java">
    ```groovy Gradle
    implementation("com.anthropic:anthropic-java:2.47.1")
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    go get github.com/anthropics/anthropic-sdk-go
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic
    ```
  </Tab>

  <Tab title="Ruby">
    ```bash
    bundle add anthropic
    ```
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require anthropic-ai/sdk
    ```
  </Tab>
</Tabs>

Atur kunci API Anda sebagai variabel lingkungan:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Buat sesi pertama Anda

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

<Steps>
  <Step title="Buat agen">
    Buat agen yang mendefinisikan model, prompt sistem, dan alat yang tersedia.

    <CodeGroup defaultLanguage="CLI">
      ```bash curl
      set -euo pipefail

      agent=$(
        curl -sS --fail-with-body https://api.anthropic.com/v1/agents \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -H "anthropic-beta: managed-agents-2026-04-01" \
          -H "content-type: application/json" \
          -d @- <<'EOF'
      {
        "name": "Coding Assistant",
        "model": "claude-opus-4-8",
        "system": "You are a helpful coding assistant. Write clean, well-documented code.",
        "tools": [
          {"type": "agent_toolset_20260401"}
        ]
      }
      EOF
      )

      AGENT_ID=$(jq -er '.id' <<<"$agent")
      AGENT_VERSION=$(jq -er '.version' <<<"$agent")

      echo "Agent ID: $AGENT_ID, version: $AGENT_VERSION"
      ```

      ```bash CLI
      ant beta:agents create \
        --name "Coding Assistant" \
        --model '{id: claude-opus-4-8}' \
        --system "You are a helpful coding assistant. Write clean, well-documented code." \
        --tool '{type: agent_toolset_20260401}'
      ```

      ```python Python
      from anthropic import Anthropic

      client = Anthropic()

      agent = client.beta.agents.create(
          name="Coding Assistant",
          model="claude-opus-4-8",
          system="You are a helpful coding assistant. Write clean, well-documented code.",
          tools=[
              {"type": "agent_toolset_20260401"},
          ],
      )

      print(f"Agent ID: {agent.id}, version: {agent.version}")
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";

      const client = new Anthropic();

      const agent = await client.beta.agents.create({
        name: "Coding Assistant",
        model: "claude-opus-4-8",
        system: "You are a helpful coding assistant. Write clean, well-documented code.",
        tools: [
          { type: "agent_toolset_20260401" },
        ],
      });

      console.log(`Agent ID: ${agent.id}, version: ${agent.version}`);
      ```

      ```csharp C#
      using Anthropic;
      using Anthropic.Models.Beta.Agents;
      using Anthropic.Models.Beta.Environments;
      using Anthropic.Models.Beta.Sessions;
      using Anthropic.Models.Beta.Sessions.Events;

      var client = new AnthropicClient();

      var agent = await client.Beta.Agents.Create(new()
      {
          Name = "Coding Assistant",
          Model = BetaManagedAgentsModel.ClaudeOpus4_8,
          System = "You are a helpful coding assistant. Write clean, well-documented code.",
          Tools =
          [
              new BetaManagedAgentsAgentToolset20260401Params
              {
                  Type = "agent_toolset_20260401",
              },
          ],
      });

      Console.WriteLine($"Agent ID: {agent.ID}, version: {agent.Version}");
      ```

      ```go Go
      package main

      import (
      	"context"
      	"fmt"

      	"github.com/anthropics/anthropic-sdk-go"
      )

      func main() {
      	client := anthropic.NewClient()
      	ctx := context.Background()

      	agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
      		Name: "Coding Assistant",
      		Model: anthropic.BetaManagedAgentsModelConfigParams{
      			ID: anthropic.BetaManagedAgentsModelClaudeOpus4_8,
      		},
      		System: anthropic.String("You are a helpful coding assistant. Write clean, well-documented code."),
      		Tools: []anthropic.BetaAgentNewParamsToolUnion{{
      			OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
      				Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
      			},
      		}},
      	})
      	if err != nil {
      		panic(err)
      	}

      	fmt.Printf("Agent ID: %s, version: %d\n", agent.ID, agent.Version)
      ```

      ```java Java
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.models.beta.agents.AgentCreateParams;
      import com.anthropic.models.beta.agents.BetaManagedAgentsAgentToolset20260401Params;
      import com.anthropic.models.beta.agents.BetaManagedAgentsModel;
      import com.anthropic.models.beta.environments.BetaCloudConfigParams;
      import com.anthropic.models.beta.environments.BetaUnrestrictedNetwork;
      import com.anthropic.models.beta.environments.EnvironmentCreateParams;
      import com.anthropic.models.beta.sessions.SessionCreateParams;
      import com.anthropic.models.beta.sessions.events.BetaManagedAgentsStreamSessionEvents;
      import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserMessageEventParams;
      import com.anthropic.models.beta.sessions.events.EventSendParams;

      void main() {
          var client = AnthropicOkHttpClient.fromEnv();

          var agent = client.beta().agents().create(AgentCreateParams.builder()
              .name("Coding Assistant")
              .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
              .system("You are a helpful coding assistant. Write clean, well-documented code.")
              .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .build())
              .build());

          IO.println("Agent ID: " + agent.id() + ", version: " + agent.version());
      ```

      ```php PHP
      use Anthropic\Client;

      $client = new Client();

      $agent = $client->beta->agents->create(
          name: 'Coding Assistant',
          model: 'claude-opus-4-8',
          system: 'You are a helpful coding assistant. Write clean, well-documented code.',
          tools: [
              ['type' => 'agent_toolset_20260401'],
          ],
      );

      echo "Agent ID: {$agent->id}, version: {$agent->version}\n";
      ```

      ```ruby Ruby
      require "anthropic"

      client = Anthropic::Client.new

      agent = client.beta.agents.create(
        name: "Coding Assistant",
        model: "claude-opus-4-8",
        system_: "You are a helpful coding assistant. Write clean, well-documented code.",
        tools: [{type: "agent_toolset_20260401"}]
      )

      puts "Agent ID: #{agent.id}, version: #{agent.version}"
      ```
    </CodeGroup>

    Tipe alat `agent_toolset_20260401` mengaktifkan rangkaian lengkap alat agen bawaan (bash, operasi file, pencarian web, dan lainnya). Lihat [Alat](/docs/id/managed-agents/tools) untuk daftar lengkap dan opsi konfigurasi per alat.

    Simpan `agent.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.
  </Step>

  <Step title="Buat environment">
    Environment mendefinisikan sandbox tempat agen Anda berjalan.

    <CodeGroup defaultLanguage="CLI">
      ```bash curl
      environment=$(
        curl -sS --fail-with-body https://api.anthropic.com/v1/environments \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -H "anthropic-beta: managed-agents-2026-04-01" \
          -H "content-type: application/json" \
          -d @- <<'EOF'
      {
        "name": "quickstart-env",
        "config": {
          "type": "cloud",
          "networking": {"type": "unrestricted"}
        }
      }
      EOF
      )

      ENVIRONMENT_ID=$(jq -er '.id' <<<"$environment")

      echo "Environment ID: $ENVIRONMENT_ID"
      ```

      ```bash CLI
      ant beta:environments create \
        --name "quickstart-env" \
        --config '{type: cloud, networking: {type: unrestricted}}'
      ```

      ```python Python
      environment = client.beta.environments.create(
          name="quickstart-env",
          config={
              "type": "cloud",
              "networking": {"type": "unrestricted"},
          },
      )

      print(f"Environment ID: {environment.id}")
      ```

      ```typescript TypeScript
      const environment = await client.beta.environments.create({
        name: "quickstart-env",
        config: {
          type: "cloud",
          networking: { type: "unrestricted" },
        },
      });

      console.log(`Environment ID: ${environment.id}`);
      ```

      ```csharp C#
      var environment = await client.Beta.Environments.Create(new()
      {
          Name = "quickstart-env",
          Config = new BetaCloudConfigParams { Networking = new BetaUnrestrictedNetwork() },
      });

      Console.WriteLine($"Environment ID: {environment.ID}");
      ```

      ```go Go
      environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
      	Name: "quickstart-env",
      	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
      		OfCloud: &anthropic.BetaCloudConfigParams{
      			Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
      				OfUnrestricted: &anthropic.BetaUnrestrictedNetworkParam{},
      			},
      		},
      	},
      })
      if err != nil {
      	panic(err)
      }

      fmt.Printf("Environment ID: %s\n", environment.ID)
      ```

      ```java Java
      var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
          .name("quickstart-env")
          .config(BetaCloudConfigParams.builder()
              .networking(BetaUnrestrictedNetwork.builder().build())
              .build())
          .build());

      IO.println("Environment ID: " + environment.id());
      ```

      ```php PHP
      $environment = $client->beta->environments->create(
          name: 'quickstart-env',
          config: ['type' => 'cloud', 'networking' => ['type' => 'unrestricted']],
      );

      echo "Environment ID: {$environment->id}\n";
      ```

      ```ruby Ruby
      environment = client.beta.environments.create(
        name: "quickstart-env",
        config: {type: "cloud", networking: {type: "unrestricted"}}
      )

      puts "Environment ID: #{environment.id}"
      ```
    </CodeGroup>

    Simpan `environment.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.

    <Tip>
      Untuk menjalankan sandbox di infrastruktur Anda sendiri alih-alih sandbox cloud, lihat 

      [Sandbox yang dihosting sendiri](/docs/id/managed-agents/self-hosted-sandboxes)

      .
    </Tip>
  </Step>

  <Step title="Mulai sesi">
    Buat sesi yang mereferensikan agen dan environment Anda.

    <CodeGroup>
      ```bash curl
      session=$(
        curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -H "anthropic-beta: managed-agents-2026-04-01" \
          -H "content-type: application/json" \
          -d @- <<EOF
      {
        "agent": "$AGENT_ID",
        "environment_id": "$ENVIRONMENT_ID",
        "title": "Quickstart session"
      }
      EOF
      )

      SESSION_ID=$(jq -er '.id' <<<"$session")

      echo "Session ID: $SESSION_ID"
      ```

      ```python Python
      session = client.beta.sessions.create(
          agent=agent.id,
          environment_id=environment.id,
          title="Quickstart session",
      )

      print(f"Session ID: {session.id}")
      ```

      ```typescript TypeScript
      const session = await client.beta.sessions.create({
        agent: agent.id,
        environment_id: environment.id,
        title: "Quickstart session",
      });

      console.log(`Session ID: ${session.id}`);
      ```

      ```csharp C#
      var session = await client.Beta.Sessions.Create(new()
      {
          Agent = agent.ID,
          EnvironmentID = environment.ID,
          Title = "Quickstart session",
      });

      Console.WriteLine($"Session ID: {session.ID}");
      ```

      ```go Go
      session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
      	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
      	EnvironmentID: environment.ID,
      	Title:         anthropic.String("Quickstart session"),
      })
      if err != nil {
      	panic(err)
      }

      fmt.Printf("Session ID: %s\n", session.ID)
      ```

      ```java Java
      var session = client.beta().sessions().create(SessionCreateParams.builder()
          .agent(agent.id())
          .environmentId(environment.id())
          .title("Quickstart session")
          .build());

      IO.println("Session ID: " + session.id());
      ```

      ```php PHP
      $session = $client->beta->sessions->create(
          agent: $agent->id,
          environmentID: $environment->id,
          title: 'Quickstart session',
      );

      echo "Session ID: {$session->id}\n";
      ```

      ```ruby Ruby
      session = client.beta.sessions.create(
        agent: agent.id,
        environment_id: environment.id,
        title: "Quickstart session"
      )

      puts "Session ID: #{session.id}"
      ```
    </CodeGroup>
  </Step>

  <Step title="Kirim pesan dan streaming responsnya">
    Buka stream, kirim event pengguna, lalu proses event saat event tersebut tiba:

    <CodeGroup>
      ```bash curl
      # Kirim pesan pengguna terlebih dahulu; API menyangga event hingga stream terhubung
      curl -sS --fail-with-body \
        "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d @- >/dev/null <<'EOF'
      {
        "events": [
          {
            "type": "user.message",
            "content": [
              {
                "type": "text",
                "text": "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt"
              }
            ]
          }
        ]
      }
      EOF

      # Buka stream SSE dan proses event saat diterima
      while IFS= read -r line; do
        [[ $line == data:* ]] || continue
        json=${line#data: }
        case $(jq -r '.type' <<<"$json") in
          agent.message)
            jq -j '.content[] | select(.type == "text") | .text' <<<"$json"
            ;;
          agent.tool_use)
            printf '\n[Using tool: %s]\n' "$(jq -r '.name' <<<"$json")"
            ;;
          session.status_idle)
            printf '\n\nAgent finished.\n'
            break
            ;;
        esac
      done < <(
        curl -sS -N --fail-with-body \
          "https://api.anthropic.com/v1/sessions/$SESSION_ID/stream" \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -H "anthropic-beta: managed-agents-2026-04-01" \
          -H "Accept: text/event-stream"
      )
      ```

      ```python Python
      with client.beta.sessions.events.stream(session.id) as stream:
          # Kirim pesan pengguna setelah stream terbuka
          client.beta.sessions.events.send(
              session.id,
              events=[
                  {
                      "type": "user.message",
                      "content": [
                          {
                              "type": "text",
                              "text": "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt",
                          },
                      ],
                  },
              ],
          )

          # Proses event streaming
          for event in stream:
              match event.type:
                  case "agent.message":
                      for block in event.content:
                          print(block.text, end="")
                  case "agent.tool_use":
                      print(f"\n[Using tool: {event.name}]")
                  case "session.status_idle":
                      print("\n\nAgent finished.")
                      break
      ```

      ```typescript TypeScript
      const stream = await client.beta.sessions.events.stream(session.id);

      // Kirim pesan pengguna setelah stream terbuka
      await client.beta.sessions.events.send(session.id, {
        events: [
          {
            type: "user.message",
            content: [
              {
                type: "text",
                text: "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt",
              },
            ],
          },
        ],
      });

      // Proses event streaming
      for await (const event of stream) {
        if (event.type === "agent.message") {
          for (const block of event.content) {
            process.stdout.write(block.text);
          }
        } else if (event.type === "agent.tool_use") {
          console.log(`\n[Using tool: ${event.name}]`);
        } else if (event.type === "session.status_idle") {
          console.log("\n\nAgent finished.");
          break;
        }
      }
      ```

      ```csharp C#
      var stream = client.Beta.Sessions.Events.StreamStreaming(session.ID);

      // Kirim pesan pengguna setelah stream terbuka
      await client.Beta.Sessions.Events.Send(session.ID, new()
      {
          Events =
          [
              new BetaManagedAgentsUserMessageEventParams
              {
                  Type = "user.message",
                  Content =
                  [
                      new BetaManagedAgentsTextBlock
                      {
                          Type = "text",
                          Text = "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt",
                      },
                  ],
              },
          ],
      });

      // Proses event streaming
      await foreach (var ev in stream)
      {
          if (ev.Value is BetaManagedAgentsAgentMessageEvent message)
          {
              foreach (var block in message.Content)
              {
                  Console.Write(block.Text);
              }
          }
          else if (ev.Value is BetaManagedAgentsAgentToolUseEvent toolUse)
          {
              Console.WriteLine($"\n[Using tool: {toolUse.Name}]");
          }
          else if (ev.Value is BetaManagedAgentsSessionStatusIdleEvent)
          {
              Console.WriteLine("\n\nAgent finished.");
              break;
          }
      }
      ```

      ```go Go
      	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
      	defer stream.Close()

      	// Kirim pesan pengguna setelah stream terbuka
      	_, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
      		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
      			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
      				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
      				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
      					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
      						Type: anthropic.BetaManagedAgentsTextBlockTypeText,
      						Text: "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt",
      					},
      				}},
      			},
      		}},
      	})
      	if err != nil {
      		panic(err)
      	}

      	// Proses event streaming
      loop:
      	for stream.Next() {
      		switch event := stream.Current().AsAny().(type) {
      		case anthropic.BetaManagedAgentsAgentMessageEvent:
      			for _, block := range event.Content {
      				fmt.Print(block.Text)
      			}
      		case anthropic.BetaManagedAgentsAgentToolUseEvent:
      			fmt.Printf("\n[Using tool: %s]\n", event.Name)
      		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
      			fmt.Print("\n\nAgent finished.\n")
      			break loop
      		}
      	}
      	if err := stream.Err(); err != nil {
      		panic(err)
      	}
      ```

      ```java Java
      try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
          // Kirim pesan pengguna setelah stream terbuka
          client.beta().sessions().events().send(session.id(), EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                  .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                  .addTextContent("Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt")
                  .build())
              .build());

          // Proses event streaming
          for (var event : (Iterable<BetaManagedAgentsStreamSessionEvents>) stream.stream()::iterator) {
              if (event.isAgentMessage()) {
                  event.asAgentMessage().content().forEach(block -> IO.print(block.text()));
              } else if (event.isAgentToolUse()) {
                  IO.println("\n[Using tool: " + event.asAgentToolUse().name() + "]");
              } else if (event.isSessionStatusIdle()) {
                  IO.println("\n\nAgent finished.");
                  break;
              }
          }
      }
      ```

      ```php PHP
      $stream = $client->beta->sessions->events->streamStream($session->id);

      // Kirim pesan pengguna setelah stream terbuka
      $client->beta->sessions->events->send(
          $session->id,
          events: [
              [
                  'type' => 'user.message',
                  'content' => [
                      ['type' => 'text', 'text' => 'Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt'],
                  ],
              ],
          ],
      );

      // Proses event streaming
      foreach ($stream as $event) {
          match ($event->type) {
              'agent.message' => print(implode('', array_map(fn($block) => $block->text, $event->content))),
              'agent.tool_use' => print("\n[Using tool: {$event->name}]\n"),
              'session.status_idle' => print("\n\nAgent finished.\n"),
              default => null,
          };
          if ($event->type === 'session.status_idle') {
              break;
          }
      }
      ```

      ```ruby Ruby
      stream = client.beta.sessions.events.stream_events(session.id)

      # Kirim pesan pengguna setelah stream terbuka
      client.beta.sessions.events.send_(
        session.id,
        events: [{
          type: "user.message",
          content: [{type: "text", text: "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt"}]
        }]
      )

      # Proses event streaming
      stream.each do |event|
        case event.type
        in :"agent.message"
          event.content.each { print it.text }
        in :"agent.tool_use"
          puts "\n[Using tool: #{event.name}]"
        in :"session.status_idle"
          puts "\n\nAgent finished."
          break
        else
          # abaikan tipe event lainnya
        end
      end
      ```
    </CodeGroup>

    Agen menulis skrip Python, mengeksekusinya di dalam sandbox, dan memverifikasi bahwa file output telah dibuat. Output Anda akan terlihat mirip seperti ini:

    ```text wrap
    I'll create a Python script that generates the first 20 Fibonacci numbers and saves them to a file.
    [Using tool: write]
    [Using tool: bash]
    The script ran successfully. Let me verify the output file.
    [Using tool: bash]
    fibonacci.txt contains the first 20 Fibonacci numbers (0 through 4181).

    Agent finished.
    ```
  </Step>
</Steps>

## Apa yang terjadi

Ketika Anda mengirim event pengguna, Claude Managed Agents:

1. **Menyediakan sandbox:** Konfigurasi environment Anda menentukan bagaimana sandbox dibangun.
2. **Menjalankan loop agen:** Claude menentukan alat mana yang akan digunakan berdasarkan pesan Anda.
3. **Mengeksekusi alat:** Penulisan file, perintah bash, dan pemanggilan alat lainnya berjalan di dalam sandbox.
4. **Streaming event:** Anda menerima pembaruan real-time saat agen bekerja.
5. **Menjadi idle:** Agen mengeluarkan event `session.status_idle` ketika tidak ada lagi yang perlu dilakukan.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Definisikan agen Anda" icon="brain" href="/docs/id/managed-agents/agent-setup">
    Buat konfigurasi agen yang dapat digunakan kembali dan berversi
  </Card>

  <Card title="Konfigurasikan environment" icon="settings" href="/docs/id/managed-agents/environments">
    Sesuaikan pengaturan jaringan dan sandbox
  </Card>

  <Card title="Alat agen" icon="tool" href="/docs/id/managed-agents/tools">
    Aktifkan alat tertentu untuk agen Anda
  </Card>

  <Card title="Stream event sesi" icon="lightning" href="/docs/id/managed-agents/events-and-streaming">
    Tangani event dan arahkan agen di tengah eksekusi
  </Card>

  <Card title="Deployment terjadwal" icon="arrows-clockwise" href="/docs/id/managed-agents/scheduled-deployments">
    Jalankan agen Anda dengan jadwal cron berulang
  </Card>
</CardGroup>
