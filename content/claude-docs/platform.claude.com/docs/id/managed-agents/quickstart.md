---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/quickstart
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 92296e07652c493b1c46996b38becb473581dd7ad69b6d75e1af43a5441d56fd
---

---
title: Memulai dengan Claude Managed Agents
url: https://platform.claude.com/docs/id/managed-agents/quickstart
description: Buat agen otonom pertama Anda.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. Berlaku untuk semua subfitur Managed Agents, termasuk Sandbox yang di-host sendiri.
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

Panduan ini memandu Anda dalam membuat agen, menyiapkan lingkungan, memulai sesi, dan melakukan “streaming” (streaming) respons agen.

Biarkan Claude Code menyiapkan agen Anda untuk Anda

```text
/claude-api managed-agents-onboard
```

## Konsep inti

| Konsep          | Deskripsi                                                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Agent**       | Model, prompt sistem, alat, server MCP, dan skill                                                                                                 |
| **Environment** | Konfigurasi untuk tempat sesi berjalan: sandbox cloud yang dikelola Anthropic, atau sandbox yang di-hosting sendiri di infrastruktur Anda sendiri |
| **Session**     | Instans agen yang sedang berjalan di dalam sebuah environment, melakukan tugas tertentu dan menghasilkan output                                   |
| **Events**      | Pesan yang dipertukarkan antara aplikasi Anda dan agen (giliran pengguna, hasil alat, pembaruan status)                                           |

## Prasyarat

* Sebuah [akun Claude Console](https://platform.claude.com/)
* Sebuah [kunci API](https://platform.claude.com/settings/keys) dari Console

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
    VERSION=2.4.0
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
    Anda juga dapat menginstal CLI dari source menggunakan `go install`. Memerlukan Go 1.25 atau yang lebih baru.

    ```bash
    go install github.com/anthropics/anthropic-cli/v2/cmd/ant@latest
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
    implementation("com.anthropic:anthropic-java:3.3.0")
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    go get github.com/anthropics/anthropic-sdk-go/v2
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
    composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7"
    ```
  </Tab>
</Tabs>

Tetapkan kunci API Anda sebagai variabel lingkungan:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Buat sesi pertama Anda

<Steps>
  <Step title="Buat agen">
    Buat agen yang menentukan model, “system prompt” (prompt sistem), dan alat yang tersedia.

    <CodeGroup defaultLanguage="CLI">
      <CodeGroupItem>
        ```bash cURL
        curl -sS --fail-with-body https://api.anthropic.com/v1/agents \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -H "anthropic-beta: managed-agents-2026-04-01" \
          -H "content-type: application/json" \
          -d '{
            "name": "Coding Assistant",
            "model": "claude-opus-5-5",
            "system": "You are a helpful coding assistant. Write clean, well-documented code.",
            "tools": [
              {"type": "agent_toolset_20260401"}
            ]
          }'
        ```

        Simpan `agent.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.
      </CodeGroupItem>

      <CodeGroupItem>
        ```bash CLI
        ant apply coding-assistant.md
        ```

        <File filename="coding-assistant.md">
          ```markdown
          ---
          name: Coding Assistant
          model: claude-opus-5-5
          tools:
            - type: agent_toolset_20260401
          ---

          You are a helpful coding assistant. Write clean, well-documented code.
          ```
        </File>

        [`ant apply`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply) mencetak ID agen dan mencatatnya di `claude-lock.json`. Anda akan mereferensikannya di setiap sesi yang Anda buat.
      </CodeGroupItem>

      <CodeGroupItem>
        ```python Python
        from anthropic import Anthropic

        client = Anthropic()

        agent = client.beta.agents.create(
            name="Coding Assistant",
            model="claude-opus-5-5",
            system="You are a helpful coding assistant. Write clean, well-documented code.",
            tools=[
                {"type": "agent_toolset_20260401"},
            ],
        )

        print(f"Agent ID: {agent.id}, version: {agent.version}")
        ```

        Simpan `agent.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.
      </CodeGroupItem>

      <CodeGroupItem>
        ```typescript TypeScript
        import Anthropic from "@anthropic-ai/sdk";

        const client = new Anthropic();

        const agent = await client.beta.agents.create({
          name: "Coding Assistant",
          model: "claude-opus-5-5",
          system: "You are a helpful coding assistant. Write clean, well-documented code.",
          tools: [{ type: "agent_toolset_20260401" }]
        });

        console.log(`Agent ID: ${agent.id}, version: ${agent.version}`);
        ```

        Simpan `agent.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.
      </CodeGroupItem>

      <CodeGroupItem>
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
            Model = BetaManagedAgentsModel.ClaudeOpus5_5,
            System = "You are a helpful coding assistant. Write clean, well-documented code.",
            Tools = [new BetaManagedAgentsAgentToolset20260401Params()],
        });

        Console.WriteLine($"Agent ID: {agent.ID}, version: {agent.Version}");
        ```

        Simpan `agent.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.
      </CodeGroupItem>

      <CodeGroupItem>
        ```go Go
        package main

        import (
        	"context"
        	"fmt"

        	"github.com/anthropics/anthropic-sdk-go/v2"
        )

        func main() {
        	client := anthropic.NewClient()
        	ctx := context.Background()

        	agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
        		Name: "Coding Assistant",
        		Model: anthropic.BetaManagedAgentsModelConfigParams{
        			ID: anthropic.BetaManagedAgentsModelClaudeOpus5_5,
        		},
        		System: anthropic.String("You are a helpful coding assistant. Write clean, well-documented code."),
        		Tools: []anthropic.BetaAgentNewParamsToolUnion{{
        			OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{},
        		}},
        	})
        	if err != nil {
        		panic(err)
        	}

        	fmt.Printf("Agent ID: %s, version: %d\n", agent.ID, agent.Version)
        ```

        Simpan `agent.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.
      </CodeGroupItem>

      <CodeGroupItem>
        ```java Java
        import com.anthropic.client.okhttp.AnthropicOkHttpClient;
        import com.anthropic.models.beta.agents.AgentCreateParams;
        import com.anthropic.models.beta.agents.BetaManagedAgentsAgentToolset20260401Params;
        import com.anthropic.models.beta.agents.BetaManagedAgentsModel;
        import com.anthropic.models.beta.environments.BetaCloudConfigParams;
        import com.anthropic.models.beta.environments.BetaLimitedNetworkParams;
        import com.anthropic.models.beta.environments.EnvironmentCreateParams;
        import com.anthropic.models.beta.sessions.SessionCreateParams;
        import com.anthropic.models.beta.sessions.events.BetaManagedAgentsStreamSessionEvents;
        import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserMessageEventParams;
        import com.anthropic.models.beta.sessions.events.EventSendParams;

        void main() {
            var client = AnthropicOkHttpClient.fromEnv();

            var agent = client.beta().agents().create(AgentCreateParams.builder()
                .name("Coding Assistant")
                .model(BetaManagedAgentsModel.CLAUDE_OPUS_5_5)
                .system("You are a helpful coding assistant. Write clean, well-documented code.")
                .addTool(BetaManagedAgentsAgentToolset20260401Params.builder().build())
                .build());

            IO.println("Agent ID: " + agent.id() + ", version: " + agent.version());
        ```

        Simpan `agent.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.
      </CodeGroupItem>

      <CodeGroupItem>
        ```php PHP
        use Anthropic\Beta\Agents\BetaManagedAgentsModel;
        use Anthropic\Client;

        $client = new Client();

        $agent = $client->beta->agents->create(
            name: 'Coding Assistant',
            model: BetaManagedAgentsModel::CLAUDE_OPUS_5_5,
            system: 'You are a helpful coding assistant. Write clean, well-documented code.',
            tools: [
                ['type' => 'agent_toolset_20260401'],
            ],
        );

        echo "Agent ID: {$agent->id}, version: {$agent->version}\n";
        ```

        Simpan `agent.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.
      </CodeGroupItem>

      <CodeGroupItem>
        ```ruby Ruby
        require "anthropic"

        client = Anthropic::Client.new

        agent = client.beta.agents.create(
          name: "Coding Assistant",
          model: Anthropic::Beta::BetaManagedAgentsModel::CLAUDE_OPUS_5_5,
          system_: "You are a helpful coding assistant. Write clean, well-documented code.",
          tools: [{type: "agent_toolset_20260401"}]
        )

        puts "Agent ID: #{agent.id}, version: #{agent.version}"
        ```

        Simpan `agent.id` yang dikembalikan. Anda akan mereferensikannya di setiap sesi yang Anda buat.
      </CodeGroupItem>
    </CodeGroup>

    Tipe alat `agent_toolset_20260401` mengaktifkan set lengkap alat agen bawaan (bash, operasi file, pencarian web, dan lainnya). Lihat [Alat](https://platform.claude.com/docs/id/managed-agents/tools) untuk daftar lengkap dan opsi konfigurasi per alat.
  </Step>

  <Step title="Buat lingkungan">
    Lingkungan menentukan sandbox tempat agen Anda berjalan. Lingkungan ini menggunakan [jaringan](https://platform.claude.com/docs/id/managed-agents/environments#networking) `limited` dengan manajer paket diizinkan, sehingga kode yang berjalan di sandbox dapat menjangkau [registri paket dan host kode](https://platform.claude.com/docs/id/managed-agents/environments#package-manager-hosts) publik. Pencarian web dan pengambilan web berjalan di luar sandbox, dan quickstart ini tidak memerlukannya. Dengan jaringan `limited`, [daftar `allowed_hosts` (java, php: `allowedHosts`; csharp, go: `AllowedHosts`)](https://platform.claude.com/docs/id/managed-agents/environments#networking) juga berlaku untuk keduanya. Keduanya tidak mengembalikan halaman atau hasil pencarian di lingkungan ini, karena lingkungan ini tidak mencantumkan host apa pun. Untuk agen Anda sendiri, cantumkan host yang dibutuhkannya di `allowed_hosts` (java, php: `allowedHosts`; csharp, go: `AllowedHosts`).

    <CodeGroup defaultLanguage="CLI">
      <CodeGroupItem>
        ```bash cURL
        curl -sS --fail-with-body https://api.anthropic.com/v1/environments \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -H "anthropic-beta: managed-agents-2026-04-01" \
          -H "content-type: application/json" \
          -d '{
            "name": "quickstart-env",
            "config": {
              "type": "cloud",
              "networking": {"type": "limited", "allow_package_managers": true}
            }
          }'
        ```

        Simpan juga `environment.id` yang dikembalikan.
      </CodeGroupItem>

      <CodeGroupItem>
        ```bash CLI
        ant apply environment.yaml
        ```

        <File filename="environment.yaml">
          ```yaml
          # yaml-language-server: $schema=https://platform.claude.com/schemas/ant/beta/environment.json
          name: quickstart-env
          config:
            type: cloud
            networking:
              type: limited
              allow_package_managers: true
          ```
        </File>

        [`ant apply`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply) juga mencatat ID lingkungan di `claude-lock.json`. Untuk membuat agen dan lingkungan dengan satu perintah, berikan kedua file: `ant apply coding-assistant.md environment.yaml`.
      </CodeGroupItem>

      <CodeGroupItem>
        ```python Python
        environment = client.beta.environments.create(
            name="quickstart-env",
            config={
                "type": "cloud",
                "networking": {"type": "limited", "allow_package_managers": True},
            },
        )

        print(f"Environment ID: {environment.id}")
        ```

        Simpan juga `environment.id` yang dikembalikan.
      </CodeGroupItem>

      <CodeGroupItem>
        ```typescript TypeScript
        const environment = await client.beta.environments.create({
          name: "quickstart-env",
          config: {
            type: "cloud",
            networking: { type: "limited", allow_package_managers: true }
          }
        });

        console.log(`Environment ID: ${environment.id}`);
        ```

        Simpan juga `environment.id` yang dikembalikan.
      </CodeGroupItem>

      <CodeGroupItem>
        ```csharp C#
        var environment = await client.Beta.Environments.Create(new()
        {
            Name = "quickstart-env",
            Config = new BetaCloudConfigParams
            {
                Networking = new BetaLimitedNetworkParams { AllowPackageManagers = true },
            },
        });

        Console.WriteLine($"Environment ID: {environment.ID}");
        ```

        Simpan juga `environment.id` yang dikembalikan.
      </CodeGroupItem>

      <CodeGroupItem>
        ```go Go
        environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
        	Name: "quickstart-env",
        	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
        		OfCloud: &anthropic.BetaCloudConfigParams{
        			Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
        				OfLimited: &anthropic.BetaLimitedNetworkParams{
        					AllowPackageManagers: anthropic.Bool(true),
        				},
        			},
        		},
        	},
        })
        if err != nil {
        	panic(err)
        }

        fmt.Printf("Environment ID: %s\n", environment.ID)
        ```

        Simpan juga `environment.id` yang dikembalikan.
      </CodeGroupItem>

      <CodeGroupItem>
        ```java Java
        var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
            .name("quickstart-env")
            .config(BetaCloudConfigParams.builder()
                .networking(BetaLimitedNetworkParams.builder()
                    .allowPackageManagers(true)
                    .build())
                .build())
            .build());

        IO.println("Environment ID: " + environment.id());
        ```

        Simpan juga `environment.id` yang dikembalikan.
      </CodeGroupItem>

      <CodeGroupItem>
        ```php PHP
        $environment = $client->beta->environments->create(
            name: 'quickstart-env',
            config: [
                'type' => 'cloud',
                'networking' => ['type' => 'limited', 'allow_package_managers' => true],
            ],
        );

        echo "Environment ID: {$environment->id}\n";
        ```

        Simpan juga `environment.id` yang dikembalikan.
      </CodeGroupItem>

      <CodeGroupItem>
        ```ruby Ruby
        environment = client.beta.environments.create(
          name: "quickstart-env",
          config: {type: "cloud", networking: {type: "limited", allow_package_managers: true}}
        )

        puts "Environment ID: #{environment.id}"
        ```

        Simpan juga `environment.id` yang dikembalikan.
      </CodeGroupItem>
    </CodeGroup>

    <Tip>
      Quickstart ini menggunakan lingkungan cloud. Untuk memutuskan apakah akan menjalankan alat di infrastruktur Anda sendiri dengan 

      [sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes)

       sebagai gantinya, lihat 

      [Memilih lingkungan agen](https://platform.claude.com/docs/id/managed-agents/choosing-an-environment)

      .
    </Tip>
  </Step>

  <Step title="Mulai sesi">
    Buat sesi yang mereferensikan agen dan lingkungan Anda.

    <CodeGroup>
      ```bash cURL
      curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d '{
          "agent": "'"$AGENT_ID"'",
          "environment_id": "'"$ENVIRONMENT_ID"'",
          "title": "Quickstart session"
        }'
      ```

      ```bash CLI
      ant beta:sessions create \
        --agent "$AGENT_ID" \
        --environment-id "$ENVIRONMENT_ID" \
        --title "Quickstart session"
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
        title: "Quickstart session"
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

  <Step title="Kirim pesan dan lakukan streaming respons">
    Buka stream, kirim event pengguna, lalu proses event saat tiba:

    <CodeGroup exclude="shell">
      <CodeGroupItem language="cURL">
        Alur kerja ini membutuhkan lebih banyak logika daripada satu perintah shell. Gunakan [Claude SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk menjalankannya.
      </CodeGroupItem>

      <CodeGroupItem language="CLI">
        Alur kerja ini membutuhkan lebih banyak logika daripada satu perintah shell. Gunakan [Claude SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk menjalankannya.
      </CodeGroupItem>

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
                          if block.type == "text":
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
                text: "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt"
              }
            ]
          }
        ]
      });

      // Proses event streaming
      loop: for await (const event of stream) {
        switch (event.type) {
          case "agent.message":
            for (const block of event.content) {
              if (block.type === "text") {
                process.stdout.write(block.text);
              }
            }
            break;
          case "agent.tool_use":
            console.log(`\n[Using tool: ${event.name}]`);
            break;
          case "session.status_idle":
            console.log("\n\nAgent finished.");
            break loop;
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
                  Content =
                  [
                      new BetaManagedAgentsTextBlock
                      {
                          Text = "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt",
                      },
                  ],
              },
          ],
      });

      // Proses event streaming
      await foreach (var streamEvent in stream)
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
          else if (streamEvent.Value is BetaManagedAgentsAgentToolUseEvent toolUse)
          {
              Console.WriteLine($"\n[Using tool: {toolUse.Name}]");
          }
          else if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent)
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
      				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
      					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
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
      				if block.Type == "text" {
      					fmt.Print(block.Text)
      				}
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
                  .addTextContent("Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt")
                  .build())
              .build());

          // Proses event streaming
          loop:
          for (var event : (Iterable<BetaManagedAgentsStreamSessionEvents>) stream.stream()::iterator) {
              switch (event.type().value()) {
                  case AGENT_MESSAGE -> event.asAgentMessage().content().forEach(block -> block.text().ifPresent(textBlock -> IO.print(textBlock.text())));
                  case AGENT_TOOL_USE -> IO.println("\n[Using tool: " + event.asAgentToolUse().name() + "]");
                  case SESSION_STATUS_IDLE -> {
                      IO.println("\n\nAgent finished.");
                      break loop;
                  }
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
          match (true) {
              $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsAgentMessageEvent => array_walk(
                  $event->content,
                  static fn ($block) => $block instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsTextBlock ? print($block->text) : null,
              ),
              $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsAgentToolUseEvent => print("\n[Using tool: {$event->name}]\n"),
              $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionStatusIdleEvent => print("\n\nAgent finished.\n"),
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
        case event
        when Anthropic::Beta::Sessions::BetaManagedAgentsAgentMessageEvent
          event.content.each { print it.text if it.is_a?(Anthropic::Beta::Sessions::BetaManagedAgentsTextBlock) }
        when Anthropic::Beta::Sessions::BetaManagedAgentsAgentToolUseEvent
          puts "\n[Using tool: #{event.name}]"
        when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusIdleEvent
          puts "\n\nAgent finished."
          break
        else
          # abaikan tipe event lainnya
        end
      end
      ```
    </CodeGroup>

    Agen menulis skrip Python, menjalankannya di sandbox, dan memverifikasi bahwa file output telah dibuat. Output Anda akan terlihat mirip dengan ini:

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

Saat Anda mengirim event pengguna, Claude Managed Agents:

1. **Menyediakan sandbox:** Konfigurasi lingkungan Anda menentukan cara sandbox dibangun.
2. **Menjalankan loop agen:** Claude menentukan alat mana yang akan digunakan berdasarkan pesan Anda.
3. **Menjalankan alat:** Penulisan file, perintah bash, dan panggilan alat lainnya berjalan di dalam sandbox.
4. **Melakukan streaming event:** Anda menerima pembaruan real-time saat agen bekerja.
5. **Menjadi idle:** Agen memancarkan event `session.status_idle` ketika tidak ada lagi yang perlu dilakukan.

## Bangun aplikasi lengkap

Masing-masing quickstart ini memadukan Claude Managed Agents dengan framework chat populer untuk membuat aplikasi lengkap yang dapat dijalankan. Di masing-masing, framework merender antarmuka chat sementara sesi terkelola menjalankan loop agen di sisi server: sesi menyimpan transkrip, menjalankan alat di sandbox, dan melakukan streaming event yang dirender oleh front end.

<CardGroup cols={3}>
  <Card title="Chat SDK" icon="github-logo" href="https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/chat-sdk">
    Seorang analis riset dalam chat browser yang dibangun dengan Chat SDK dari Vercel. Setiap percakapan adalah satu sesi persisten yang melakukan streaming balasannya sementara feed langsung menampilkan panggilan alat. Mengganti adaptor Chat SDK akan memindahkan handler yang sama ke Slack, Teams, Discord, atau WhatsApp.
  </Card>

  <Card title="assistant-ui" icon="github-logo" href="https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/assistant-ui">
    Seorang analis spreadsheet dalam chat yang dibangun dari primitif assistant-ui. Sesi menjadi daftar thread, satu reducer mengubah log event sesi menjadi pesan dan kartu alat, dan setiap perintah bash merender gerbang Allow/Deny inline sebelum dijalankan.
  </Card>

  <Card title="CopilotKit (AG-UI)" icon="github-logo" href="https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/copilot-kit-ag-ui">
    Asisten keuangan pribadi dalam chat CopilotKit. Adaptor AG-UI untuk Claude Managed Agents memetakan setiap thread chat ke sesi terkelola dan melakukan streaming balasan token demi token, dan alat kustom merender grafik interaktif secara inline dalam percakapan.
  </Card>
</CardGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Definisikan agen Anda" icon="brain" href="https://platform.claude.com/docs/id/managed-agents/agent-setup">
    Buat konfigurasi agen yang dapat digunakan kembali dan berversi
  </Card>

  <Card title="Konfigurasikan lingkungan" icon="settings" href="https://platform.claude.com/docs/id/managed-agents/environments">
    Sesuaikan pengaturan jaringan dan sandbox
  </Card>

  <Card title="Alat agen" icon="tool" href="https://platform.claude.com/docs/id/managed-agents/tools">
    Aktifkan alat tertentu untuk agen Anda
  </Card>

  <Card title="Stream event sesi" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/events-and-streaming">
    Tangani event dan arahkan agen saat berjalan
  </Card>

  <Card title="Deployment terjadwal" icon="arrows-clockwise" href="https://platform.claude.com/docs/id/managed-agents/scheduled-deployments">
    Jalankan agen Anda pada jadwal cron berulang
  </Card>

  <Card title="Quickstart wiki pengetahuan" icon="github-logo" href="https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/knowledge-wiki">
    Saring korpus dokumen sekali menjadi wiki pengetahuan, lalu jawab pertanyaan berulang darinya dengan sebagian kecil biaya
  </Card>
</CardGroup>
