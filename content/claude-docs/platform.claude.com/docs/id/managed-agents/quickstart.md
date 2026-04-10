---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/quickstart
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 22022737bf88534826966be8242b2aebb28f8ac994d6842e3bc3b6c23fda75b8
---

# Mulai dengan Claude Managed Agents

Buat agen otonom pertama Anda.

---

Panduan ini memandu Anda membuat agen, menyiapkan lingkungan, memulai sesi, dan melakukan streaming respons agen.

## Konsep inti

| Concept | Description |
|---------|-------------|
| **Agent** | The model, system prompt, tools, MCP servers, and skills |
| **Environment** | A configured container template (packages, network access) |
| **Session** | A running agent instance within an environment, performing a specific task and generating outputs |
| **Events** | Messages exchanged between your application and the agent (user turns, tool results, status updates) |

## Prasyarat

- Akun [Console](/) Anthropic
- [Kunci API](/settings/keys)

## Instal CLI

<Tabs>
<Tab title="Homebrew (macOS)">

```bash
brew install anthropics/tap/ant
```

Di macOS, hapus karantina binary:

```bash
xattr -d com.apple.quarantine "$(brew --prefix)/bin/ant"
```

</Tab>
<Tab title="curl (Linux/WSL)">

Untuk lingkungan Linux, unduh binary rilis secara langsung.

```bash
VERSION=1.0.0
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m | sed -e 's/x86_64/amd64/' -e 's/aarch64/arm64/')
curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_${OS}_${ARCH}.tar.gz" \
  | sudo tar -xz -C /usr/local/bin ant
```

Anda dapat menemukan semua rilis di [halaman rilis GitHub](https://github.com/anthropics/anthropic-cli/releases).

</Tab>
<Tab title="Go">

Anda juga dapat menginstal CLI dari sumber menggunakan `go install`. Memerlukan Go 1.22 atau lebih baru.

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
    implementation("com.anthropic:anthropic-java:2.20.0")
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

Tetapkan kunci API Anda sebagai variabel lingkungan:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Buat sesi pertama Anda

<Note>
Semua permintaan API Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

<Steps>
  <Step title="Buat agen">
    Buat agen yang mendefinisikan model, system prompt, dan alat yang tersedia.

    
    <CodeGroup defaultLanguage="CLI">
    
````bash
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
  "model": "claude-sonnet-4-6",
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
````

    
````bash
ant beta:agents create \
  --name "Coding Assistant" \
  --model '{id: claude-sonnet-4-6}' \
  --system "You are a helpful coding assistant. Write clean, well-documented code." \
  --tool '{type: agent_toolset_20260401}'
````

    
````python
from anthropic import Anthropic

client = Anthropic()

agent = client.beta.agents.create(
    name="Coding Assistant",
    model="claude-sonnet-4-6",
    system="You are a helpful coding assistant. Write clean, well-documented code.",
    tools=[
        {"type": "agent_toolset_20260401"},
    ],
)

print(f"Agent ID: {agent.id}, version: {agent.version}")
````

    
````typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const agent = await client.beta.agents.create({
  name: "Coding Assistant",
  model: "claude-sonnet-4-6",
  system: "You are a helpful coding assistant. Write clean, well-documented code.",
  tools: [
    { type: "agent_toolset_20260401" },
  ],
});

console.log(`Agent ID: ${agent.id}, version: ${agent.version}`);
````

    
````csharp
using Anthropic;
using Anthropic.Models.Beta.Agents;
using Anthropic.Models.Beta.Environments;
using Anthropic.Models.Beta.Sessions;
using Anthropic.Models.Beta.Sessions.Events;

var client = new AnthropicClient();

var agent = await client.Beta.Agents.Create(new()
{
    Name = "Coding Assistant",
    Model = BetaManagedAgentsModel.ClaudeSonnet4_6,
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
````

    
````go
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
			ID:   anthropic.BetaManagedAgentsModelClaudeSonnet4_6,
			Type: anthropic.BetaManagedAgentsModelConfigParamsTypeModelConfig,
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
````

    
````java
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.agents.AgentCreateParams;
import com.anthropic.models.beta.agents.BetaManagedAgentsAgentToolset20260401Params;
import com.anthropic.models.beta.agents.BetaManagedAgentsModel;
import com.anthropic.models.beta.environments.BetaCloudConfigParams;
import com.anthropic.models.beta.environments.EnvironmentCreateParams;
import com.anthropic.models.beta.environments.UnrestrictedNetwork;
import com.anthropic.models.beta.sessions.SessionCreateParams;
import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserMessageEventParams;
import com.anthropic.models.beta.sessions.events.EventSendParams;
import com.anthropic.models.beta.sessions.events.StreamEvents;

void main() {
    var client = AnthropicOkHttpClient.fromEnv();

    var agent = client.beta().agents().create(AgentCreateParams.builder()
        .name("Coding Assistant")
        .model(BetaManagedAgentsModel.CLAUDE_SONNET_4_6)
        .system("You are a helpful coding assistant. Write clean, well-documented code.")
        .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
            .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
            .build())
        .build());

    IO.println("Agent ID: " + agent.id() + ", version: " + agent.version());
````

    
````php
use Anthropic\Client;

$client = new Client();

$agent = $client->beta->agents->create(
    name: 'Coding Assistant',
    model: 'claude-sonnet-4-6',
    system: 'You are a helpful coding assistant. Write clean, well-documented code.',
    tools: [
        ['type' => 'agent_toolset_20260401'],
    ],
);

echo "Agent ID: {$agent->id}, version: {$agent->version}\n";
````

    
````ruby
require "anthropic"

client = Anthropic::Client.new

agent = client.beta.agents.create(
  name: "Coding Assistant",
  model: "claude-sonnet-4-6",
  system_: "You are a helpful coding assistant. Write clean, well-documented code.",
  tools: [{type: "agent_toolset_20260401"}]
)

puts "Agent ID: #{agent.id}, version: #{agent.version}"
````

    </CodeGroup>

    Tipe alat `agent_toolset_20260401` mengaktifkan kumpulan lengkap alat agen bawaan (bash, operasi file, pencarian web, dan lainnya). Lihat [Alat](/docs/id/managed-agents/tools) untuk daftar lengkap dan opsi konfigurasi per alat.

    Simpan `agent.id` yang dikembalikan. Anda akan merujuknya di setiap sesi yang Anda buat.

  </Step>

  <Step title="Buat lingkungan">
    Lingkungan mendefinisikan kontainer tempat agen Anda berjalan.

    <CodeGroup defaultLanguage="CLI">
    
````bash
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
````

    
````bash
ant beta:environments create \
  --name "quickstart-env" \
  --config '{type: cloud, networking: {type: unrestricted}}'
````

    
````python
environment = client.beta.environments.create(
    name="quickstart-env",
    config={
        "type": "cloud",
        "networking": {"type": "unrestricted"},
    },
)

print(f"Environment ID: {environment.id}")
````

    
````typescript
const environment = await client.beta.environments.create({
  name: "quickstart-env",
  config: {
    type: "cloud",
    networking: { type: "unrestricted" },
  },
});

console.log(`Environment ID: ${environment.id}`);
````

    
````csharp
var environment = await client.Beta.Environments.Create(new()
{
    Name = "quickstart-env",
    Config = new() { Networking = new UnrestrictedNetwork() },
});

Console.WriteLine($"Environment ID: {environment.ID}");
````

    
````go
environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
	Name: "quickstart-env",
	Config: anthropic.BetaCloudConfigParams{
		Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
			OfUnrestricted: &anthropic.UnrestrictedNetworkParam{},
		},
	},
})
if err != nil {
	panic(err)
}

fmt.Printf("Environment ID: %s\n", environment.ID)
````

    
````java
var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
    .name("quickstart-env")
    .config(BetaCloudConfigParams.builder()
        .networking(UnrestrictedNetwork.builder().build())
        .build())
    .build());

IO.println("Environment ID: " + environment.id());
````

    
````php
$environment = $client->beta->environments->create(
    name: 'quickstart-env',
    config: ['type' => 'cloud', 'networking' => ['type' => 'unrestricted']],
);

echo "Environment ID: {$environment->id}\n";
````

    
````ruby
environment = client.beta.environments.create(
  name: "quickstart-env",
  config: {type: "cloud", networking: {type: "unrestricted"}}
)

puts "Environment ID: #{environment.id}"
````

    </CodeGroup>

    Simpan `environment.id` yang dikembalikan. Anda akan merujuknya di setiap sesi yang Anda buat.
  </Step>

  <Step title="Mulai sesi">
    Buat sesi yang merujuk agen dan lingkungan Anda.

    <CodeGroup>
    
````bash
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
````

    
````python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Quickstart session",
)

print(f"Session ID: {session.id}")
````

    
````typescript
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  title: "Quickstart session",
});

console.log(`Session ID: ${session.id}`);
````

    
````csharp
var session = await client.Beta.Sessions.Create(new()
{
    Agent = agent.ID,
    EnvironmentID = environment.ID,
    Title = "Quickstart session",
});

Console.WriteLine($"Session ID: {session.ID}");
````

    
````go
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
	EnvironmentID: environment.ID,
	Title:         anthropic.String("Quickstart session"),
})
if err != nil {
	panic(err)
}

fmt.Printf("Session ID: %s\n", session.ID)
````

    
````java
var session = client.beta().sessions().create(SessionCreateParams.builder()
    .agent(agent.id())
    .environmentId(environment.id())
    .title("Quickstart session")
    .build());

IO.println("Session ID: " + session.id());
````

    
````php
$session = $client->beta->sessions->create(
    agent: $agent->id,
    environmentID: $environment->id,
    title: 'Quickstart session',
);

echo "Session ID: {$session->id}\n";
````

    
````ruby
session = client.beta.sessions.create(
  agent: agent.id,
  environment_id: environment.id,
  title: "Quickstart session"
)

puts "Session ID: #{session.id}"
````

    </CodeGroup>
  </Step>

  <Step title="Kirim pesan dan streaming respons">
    Buka stream, kirim event pengguna, lalu proses event saat tiba:

    <CodeGroup>
    
````bash
# Send the user message first; the API buffers events until the stream attaches
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

# Open the SSE stream and process events as they arrive
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
````

    
````python
with client.beta.sessions.events.stream(session.id) as stream:
    # Send the user message after the stream opens
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

    # Process streaming events
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
````

    
````typescript
const stream = await client.beta.sessions.events.stream(session.id);

// Send the user message after the stream opens
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

// Process streaming events
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
````

    
````csharp
var stream = client.Beta.Sessions.Events.StreamStreaming(session.ID);

// Send the user message after the stream opens
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

// Process streaming events
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
````

    
````go
	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
	defer stream.Close()

	// Send the user message after the stream opens
	_, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
		Events: []anthropic.SendEventsParamsUnion{{
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

	// Process streaming events
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
````

    
````java
try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
    // Send the user message after the stream opens
    client.beta().sessions().events().send(session.id(), EventSendParams.builder()
        .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
            .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
            .addTextContent("Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt")
            .build())
        .build());

    // Process streaming events
    for (var event : (Iterable<StreamEvents>) stream.stream()::iterator) {
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
````

    
````php
$stream = $client->beta->sessions->events->streamStream($session->id);

// Send the user message after the stream opens
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

// Process streaming events
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
````

    
````ruby
stream = client.beta.sessions.events.stream_events(session.id)

# Send the user message after the stream opens
client.beta.sessions.events.send_(
  session.id,
  events: [{
    type: "user.message",
    content: [{type: "text", text: "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt"}]
  }]
)

# Process streaming events
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
    # ignore other event types
  end
end
````

    </CodeGroup>

    Agen akan menulis skrip Python, mengeksekusinya di dalam kontainer, dan memverifikasi bahwa file output telah dibuat. Output Anda akan terlihat seperti ini:

    ```text
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

## Yang terjadi

Saat Anda mengirim event pengguna, Claude Managed Agents:

1. **Menyediakan kontainer:** Konfigurasi lingkungan Anda menentukan cara pembuatannya.
2. **Menjalankan loop agen:** Claude memutuskan alat mana yang akan digunakan berdasarkan pesan Anda
3. **Mengeksekusi alat:** Penulisan file, perintah bash, dan panggilan alat lainnya berjalan di dalam kontainer
4. **Melakukan streaming event:** Anda menerima pembaruan real-time saat agen bekerja
5. **Menjadi idle:** Agen memancarkan event `session.status_idle` ketika tidak ada lagi yang perlu dilakukan

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Definisikan agen Anda" icon="brain" href="/docs/id/managed-agents/agent-setup">
    Buat konfigurasi agen yang dapat digunakan kembali dan berversi
  </Card>
  <Card title="Konfigurasi lingkungan" icon="settings" href="/docs/id/managed-agents/environments">
    Sesuaikan pengaturan jaringan dan kontainer
  </Card>
  <Card title="Alat agen" icon="tool" href="/docs/id/managed-agents/tools">
    Aktifkan alat tertentu untuk agen Anda
  </Card>
  <Card title="Event dan streaming" icon="lightning" href="/docs/id/managed-agents/events-and-streaming">
    Tangani event dan arahkan agen di tengah eksekusi
  </Card>
</CardGroup>