---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/migration
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 71c8c8ddd08be9ceb234787f53b5d160dba50a0d56e06ca7a883a22697a902cc
---

# Migrasi

Pindahkan agen yang sudah ada yang dibangun di atas Messages API atau Claude Agent SDK ke Claude Managed Agents.

---

Claude Managed Agents menggantikan loop agen yang Anda tulis sendiri dengan infrastruktur terkelola. Halaman ini membahas apa saja yang berubah ketika Anda bermigrasi dari loop kustom yang dibangun di atas [Messages API](/docs/id/build-with-claude/working-with-messages) atau dari [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview).

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Dari loop agen Messages API

Jika Anda membangun agen dengan memanggil `messages.create` dalam loop `while`, mengeksekusi pemanggilan alat sendiri, dan menambahkan hasilnya ke riwayat percakapan, sebagian besar kode tersebut tidak lagi diperlukan.

### Apa yang tidak lagi Anda kelola

| Sebelum                                                                                                             | Sesudah                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Anda memelihara array riwayat percakapan dan mengirimkannya kembali pada setiap giliran.                            | Sesi menyimpan riwayat di sisi server. Kirim event, terima event.                                                              |
| Anda mengiterasi blok konten `tool_use`, menjalankan setiap alat, dan mengulang kembali dengan pesan `tool_result`. | Alat bawaan berjalan di dalam sandbox secara otomatis. Anda hanya menangani alat kustom melalui event `agent.custom_tool_use`. |
| Anda menyediakan sandbox sendiri untuk menjalankan kode yang dihasilkan agen.                                       | Sandbox sesi menangani eksekusi kode, operasi file, dan bash.                                                                  |
| Anda memutuskan kapan loop selesai.                                                                                 | Sesi mengeluarkan `session.status_idle` ketika agen tidak memiliki hal lain untuk dilakukan.                                   |

### Perbandingan kode

**Sebelum** (loop Messages API, disederhanakan):

<CodeGroup>
  ```python Python
  messages = [{"role": "user", "content": task}]
  while True:
      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          messages=messages,
          tools=tools,
      )
      messages.append({"role": "assistant", "content": response.content})
      if response.stop_reason == "end_turn":
          break
      for block in response.content:
          if block.type == "tool_use":
              result = execute_tool(block.name, block.input)
              messages.append(
                  {
                      "role": "user",
                      "content": [
                          {
                              "type": "tool_result",
                              "tool_use_id": block.id,
                              "content": result,
                          }
                      ],
                  }
              )
  ```

  ```typescript TypeScript
  const messages: Anthropic.MessageParam[] = [{ role: "user", content: task }];
  while (true) {
    const response = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages,
      tools
    });
    messages.push({ role: "assistant", content: response.content });
    if (response.stop_reason === "end_turn") {
      break;
    }
    for (const block of response.content) {
      if (block.type === "tool_use") {
        const result = executeTool(block.name, block.input);
        messages.push({
          role: "user",
          content: [
            {
              type: "tool_result",
              tool_use_id: block.id,
              content: result
            }
          ]
        });
      }
    }
  }
  ```

  ```csharp C#
  List<MessageParam> messages = [new() { Role = Role.User, Content = task }];
  while (true)
  {
      var response = await client.Messages.Create(new()
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages = messages,
          Tools = tools,
      });
      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = new([.. response.Content.Select(block => new ContentBlockParam(block.Json))]),
      });
      if (response.StopReason == StopReason.EndTurn)
      {
          break;
      }
      foreach (var block in response.Content)
      {
          if (block.Value is ToolUseBlock toolUse)
          {
              var result = ExecuteTool(toolUse.Name, toolUse.Input);
              messages.Add(new()
              {
                  Role = Role.User,
                  Content = new([new ToolResultBlockParam { ToolUseID = toolUse.ID, Content = result }]),
              });
          }
      }
  }
  ```

  ```go Go
  messages := []anthropic.MessageParam{
  	anthropic.NewUserMessage(anthropic.NewTextBlock(task)),
  }
  for {
  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Messages:  messages,
  		Tools:     tools,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	messages = append(messages, response.ToParam())
  	if response.StopReason == anthropic.StopReasonEndTurn {
  		break
  	}
  	for _, block := range response.Content {
  		if toolUse, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
  			result := executeTool(toolUse.Name, toolUse.Input)
  			messages = append(messages, anthropic.NewUserMessage(
  				anthropic.NewToolResultBlock(toolUse.ID, result, false),
  			))
  		}
  	}
  }
  ```

  ```java Java
  var messages = new ArrayList<MessageParam>();
  messages.add(MessageParam.builder()
      .role(MessageParam.Role.USER)
      .content(task)
      .build());
  while (true) {
      var response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .messages(messages)
          .tools(tools)
          .build());
      messages.add(response.toParam());
      if (StopReason.END_TURN.equals(response.stopReason().orElse(null))) {
          break;
      }
      for (var block : response.content()) {
          block.toolUse().ifPresent(toolUse -> {
              var result = executeTool(toolUse.name(), toolUse._input());
              messages.add(MessageParam.builder()
                  .role(MessageParam.Role.USER)
                  .contentOfBlockParams(List.of(
                      ContentBlockParam.ofToolResult(ToolResultBlockParam.builder()
                          .toolUseId(toolUse.id())
                          .content(result)
                          .build())))
                  .build());
          });
      }
  }
  ```

  ```php PHP
  $messages = [['role' => 'user', 'content' => $task]];
  while (true) {
      $response = $client->messages->create(
          model: 'claude-opus-4-8',
          maxTokens: 1024,
          messages: $messages,
          tools: $tools,
      );
      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      if ($response->stopReason === 'end_turn') {
          break;
      }
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              $result = executeTool($block->name, $block->input);
              $messages[] = [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'tool_result',
                          'tool_use_id' => $block->id,
                          'content' => $result,
                      ],
                  ],
              ];
          }
      }
  }
  ```

  ```ruby Ruby
  messages = [{ role: "user", content: task }]
  loop do
    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: messages,
      tools: tools
    )
    messages << { role: "assistant", content: response.content }
    break if response.stop_reason == :end_turn
    response.content.each do |block|
      next unless block.type == :tool_use
      result = execute_tool(block.name, block.input)
      messages << {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: block.id,
            content: result
          }
        ]
      }
    end
  end
  ```
</CodeGroup>

**Sesudah** (Claude Managed Agents):

<CodeGroup>
  ```bash cURL
  agent=$(
    curl --fail-with-body -sS "https://api.anthropic.com/v1/agents?beta=true" \
      -H "x-api-key: ${ANTHROPIC_API_KEY}" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
      --json '{
        "name": "Task Runner",
        "model": "claude-opus-4-8",
        "tools": [{"type": "agent_toolset_20260401"}]
      }'
  )
  agent_id=$(jq -r '.id' <<< "${agent}")

  session_id=$(
    curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions?beta=true" \
      -H "x-api-key: ${ANTHROPIC_API_KEY}" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
      --json "$(jq -n --argjson a "${agent}" --arg env "${environment_id}" \
        '{agent: {type: "agent", id: $a.id, version: $a.version}, environment_id: $env}')" \
    | jq -r '.id'
  )

  # Buka stream SSE di latar belakang, lalu kirim pesan pengguna.
  stream_log=$(mktemp)
  curl --fail-with-body -sS -N \
    "https://api.anthropic.com/v1/sessions/${session_id}/events/stream?beta=true" \
    -H "x-api-key: ${ANTHROPIC_API_KEY}" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    > "${stream_log}" &
  stream_pid=$!

  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/sessions/${session_id}/events?beta=true" \
    -H "x-api-key: ${ANTHROPIC_API_KEY}" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    --json "$(jq -n --arg text "${task}" \
      '{events: [{type: "user.message", content: [{type: "text", text: $text}]}]}')" \
    > /dev/null

  # Tunggu hingga sesi menjadi idle. grep keluar pada kecocokan pertama, dan
  # membaca via process substitution berarti shell tidak menunggu
  # tail (pipeline `tail -f | grep -m1` di foreground akan menggantung: tail
  # baru mati pada penulisan berikutnya, yang tak pernah datang setelah stream idle).
  grep -m1 '"session.status_idle"' <(tail -f -n +1 "${stream_log}") > /dev/null

  kill "${stream_pid}" 2>/dev/null || true
  ```

  ```bash CLI
  { read -r _ agent_id; read -r _ agent_version; } < <(ant beta:agents create \
    --name "Task Runner" \
    --model claude-opus-4-8 \
    --tool '{type: agent_toolset_20260401}' \
    --transform '{id,version}' --format yaml)

  session_id=$(ant beta:sessions create \
    --agent "{type: agent, id: $agent_id, version: $agent_version}" \
    --environment-id "$environment_id" \
    --transform id --raw-output)

  # Buka stream terlebih dahulu, lalu kirim pesan pengguna
  exec {stream}< <(ant beta:sessions:events stream \
    --session-id "$session_id" \
    --transform type --raw-output)

  ant beta:sessions:events send \
    --session-id "$session_id" \
    --event "{type: user.message, content: [{type: text, text: \"$task\"}]}" \
  > /dev/null

  # Tunggu hingga sesi menjadi idle (grep keluar pada kecocokan pertama)
  grep -m1 -x 'session.status_idle' <&"$stream" > /dev/null
  exec {stream}<&-
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Task Runner",
      model="claude-opus-4-8",
      tools=[{"type": "agent_toolset_20260401"}],
  )

  session = client.beta.sessions.create(
      agent={"type": "agent", "id": agent.id, "version": agent.version},
      environment_id=environment.id,
  )

  with client.beta.sessions.events.stream(session.id) as stream:
      client.beta.sessions.events.send(
          session.id,
          events=[{"type": "user.message", "content": [{"type": "text", "text": task}]}],
      )
      for event in stream:
          if event.type == "session.status_idle":
              break
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Task Runner",
    model: "claude-opus-4-8",
    tools: [{ type: "agent_toolset_20260401" }]
  });

  const session = await client.beta.sessions.create({
    agent: { type: "agent", id: agent.id, version: agent.version },
    environment_id: environment.id
  });

  const stream = await client.beta.sessions.events.stream(session.id);

  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.message",
        content: [{ type: "text", text: task }]
      }
    ]
  });

  for await (const event of stream) {
    if (event.type === "session.status_idle") {
      break;
    }
  }
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Task Runner",
      Model = BetaManagedAgentsModel.ClaudeOpus4_8,
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
      ],
  });

  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = new BetaManagedAgentsAgentParams
      {
          Type = "agent",
          ID = agent.ID,
          Version = agent.Version,
      },
      EnvironmentID = environment.ID,
  });

  var stream = client.Beta.Sessions.Events.StreamStreaming(session.ID);

  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Type = "user.message",
              Content = [new BetaManagedAgentsTextBlock { Type = "text", Text = task }],
          },
      ],
  });

  await foreach (var streamEvent in stream)
  {
      if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent)
      {
          break;
      }
  }
  ```

  ```go Go
  	agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  		Name: "Task Runner",
  		Model: anthropic.BetaManagedAgentsModelConfigParams{
  			ID: anthropic.BetaManagedAgentsModelClaudeOpus4_8,
  		},
  		Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  			OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  				Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			},
  		}},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  		Agent: anthropic.BetaSessionNewParamsAgentUnion{
  			OfBetaManagedAgentsAgents: &anthropic.BetaManagedAgentsAgentParams{
  				Type:    anthropic.BetaManagedAgentsAgentParamsTypeAgent,
  				ID:      agent.ID,
  				Version: anthropic.Int(agent.Version),
  			},
  		},
  		EnvironmentID: environment.ID,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
  	defer stream.Close()

  	_, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
  				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  						Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  						Text: task,
  					},
  				}},
  			},
  		}},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for stream.Next() {
  		event := stream.Current()
  		if event.Type == "session.status_idle" {
  			break
  		}
  	}
  	if err := stream.Err(); err != nil {
  		log.Fatal(err)
  	}
  ```

  ```java Java
      var agent = client.beta().agents().create(
          AgentCreateParams.builder()
              .name("Task Runner")
              .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
              .addTool(
                  BetaManagedAgentsAgentToolset20260401Params.builder()
                      .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                      .build()
              )
              .build()
      );

      var session = client.beta().sessions().create(
          SessionCreateParams.builder()
              .agent(
                  BetaManagedAgentsAgentParams.builder()
                      .type(BetaManagedAgentsAgentParams.Type.AGENT)
                      .id(agent.id())
                      .version(agent.version())
                      .build()
              )
              .environmentId(environment.id())
              .build()
      );

      try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
          client.beta().sessions().events().send(
              session.id(),
              EventSendParams.builder()
                  .addEvent(
                      BetaManagedAgentsUserMessageEventParams.builder()
                          .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                          .addTextContent(task)
                          .build()
                  )
                  .build()
          );
          stream.stream()
              .takeWhile(event -> !event.isSessionStatusIdle())
              .forEach(_ -> {});
      }
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Task Runner',
      model: 'claude-opus-4-8',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
          ),
      ],
  );

  $session = $client->beta->sessions->create(
      agent: BetaManagedAgentsAgentParams::with(
          type: 'agent',
          id: $agent->id,
          version: $agent->version,
      ),
      environmentID: $environment->id,
  );

  $stream = $client->beta->sessions->events->streamStream($session->id);

  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => $task]],
          ],
      ],
  );

  foreach ($stream as $event) {
      if ($event->type === 'session.status_idle') {
          break;
      }
  }
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Task Runner",
    model: "claude-opus-4-8",
    tools: [{type: "agent_toolset_20260401"}]
  )

  session = client.beta.sessions.create(
    agent: {type: "agent", id: agent.id, version: agent.version},
    environment_id: environment.id
  )

  stream = client.beta.sessions.events.stream_events(session.id)
  client.beta.sessions.events.send_(
    session.id,
    events: [{type: "user.message", content: [{type: "text", text: task}]}]
  )
  stream.each do
    break if it.type == :"session.status_idle"
  end
  ```
</CodeGroup>

### Apa yang masih Anda kendalikan

* **Prompt sistem dan model:** Field yang sama, sekarang berada pada definisi agen.
* **Alat kustom:** Masih dideklarasikan dengan JSON Schema. Eksekusi berpindah dari penanganan inline ke merespons event `agent.custom_tool_use`. Lihat [Stream event sesi](/docs/id/managed-agents/events-and-streaming).
* **Konteks:** Anda masih dapat menyuntikkan konteks melalui prompt sistem, [resource file](/docs/id/managed-agents/files), atau [skill](/docs/id/managed-agents/skills).

## Dari Claude Agent SDK

Jika Anda membangun dengan [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), Anda sudah bekerja dengan agen, alat, dan sesi sebagai konsep. Perbedaannya adalah di mana mereka berjalan: SDK dieksekusi dalam proses yang Anda operasikan, sedangkan Managed Agents berjalan di infrastruktur Anthropic. Sebagian besar migrasi adalah memetakan objek konfigurasi SDK ke padanannya di sisi API.

### Apa yang berubah

| Agent SDK                                                                 | Managed Agents                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ClaudeAgentOptions(...)` dibuat per eksekusi                             | `client.beta.agents.create(...)` sekali; Agen disimpan dan diberi versi di sisi server. Lihat [Penyiapan agen](/docs/id/managed-agents/agent-setup).                                                                                       |
| `async with ClaudeSDKClient(...)` atau `query(...)`                       | `client.beta.sessions.create(...)` lalu kirim dan terima [event](/docs/id/managed-agents/events-and-streaming).                                                                                                                            |
| Fungsi dengan dekorator `@tool` yang di-dispatch secara otomatis oleh SDK | Deklarasikan sebagai `{"type": "custom", ...}` pada Agen; klien Anda menangani event `agent.custom_tool_use` dan membalas dengan `user.custom_tool_result`. Lihat [Alat](/docs/id/managed-agents/tools).                                   |
| Alat bawaan berjalan dalam proses Anda terhadap filesystem Anda           | `{"type": "agent_toolset_20260401"}` menjalankan alat yang sama di dalam sandbox sesi terhadap `/workspace`.                                                                                                                               |
| `cwd`, `add_dirs` menunjuk ke path lokal                                  | Unggah atau mount [file](/docs/id/managed-agents/files) sebagai resource sesi.                                                                                                                                                             |
| `system_prompt` dan hierarki `CLAUDE.md`                                  | Satu string `system` pada Agen. Setiap pembaruan menghasilkan versi baru di sisi server; pin sesi ke versi tertentu untuk mempromosikan atau melakukan rollback tanpa deploy. Lihat [Penyiapan agen](/docs/id/managed-agents/agent-setup). |
| `mcp_servers` dikonfigurasi dan diautentikasi di satu tempat              | Deklarasikan server pada Agen; sediakan kredensial melalui [Vault](/docs/id/managed-agents/vaults) pada Sesi.                                                                                                                              |
| `permission_mode`, `can_use_tool`                                         | [`permission_policy`](/docs/id/managed-agents/permission-policies) per alat; kirim event `user.tool_confirmation` untuk alat `always_ask`.                                                                                                 |

### Perbandingan kode

**Sebelum** (Agent SDK):

```python
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    create_sdk_mcp_server,
    tool,
)


@tool("get_weather", "Get the current weather for a city.", {"city": str})
async def get_weather(args: dict) -> dict:
    return {"content": [{"type": "text", "text": f"{args['city']}: 18°C, clear"}]}


options = ClaudeAgentOptions(
    model="claude-opus-4-8",
    system_prompt="You are a concise weather assistant.",
    mcp_servers={
        "weather": create_sdk_mcp_server("weather", "1.0", tools=[get_weather])
    },
)

async with ClaudeSDKClient(options=options) as agent:
    await agent.query("What's the weather in Tokyo?")
    async for msg in agent.receive_response():
        print(msg)
```

**Sesudah** (Managed Agents):

```python
from anthropic import Anthropic

client = Anthropic()

agent = client.beta.agents.create(
    name="weather-agent",
    model="claude-opus-4-8",
    system="You are a concise weather assistant.",
    tools=[
        {
            "type": "custom",
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "input_schema": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        }
    ],
)
environment = client.beta.environments.create(
    name="weather-env",
    config={"type": "cloud", "networking": {"type": "unrestricted"}},
)

session = client.beta.sessions.create(
    agent={"type": "agent", "id": agent.id, "version": agent.version},
    environment_id=environment.id,
)


def get_weather(city: str) -> str:
    return f"{city}: 18°C, clear"


with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[
            {
                "type": "user.message",
                "content": [{"type": "text", "text": "What's the weather in Tokyo?"}],
            }
        ],
    )
    for ev in stream:
        if ev.type == "agent.message":
            print("".join(block.text for block in ev.content if block.type == "text"))
        elif ev.type == "agent.custom_tool_use":
            result = get_weather(**ev.input)
            client.beta.sessions.events.send(
                session.id,
                events=[
                    {
                        "type": "user.custom_tool_result",
                        "custom_tool_use_id": ev.id,
                        "content": [{"type": "text", "text": result}],
                    }
                ],
            )
        elif (
            ev.type == "session.status_idle"
            and ev.stop_reason
            and ev.stop_reason.type == "end_turn"
        ):
            break
```

Agen dan Environment dibuat sekali dan digunakan kembali di seluruh sesi. Fungsi alat masih berjalan dalam proses Anda; perbedaannya adalah Anda membaca event `agent.custom_tool_use` dan mengirim hasilnya secara eksplisit alih-alih SDK yang men-dispatch-nya untuk Anda.

### Fitur yang berpindah ke klien Anda

Konsekuensi dari Anthropic yang menjalankan loop agen adalah beberapa hal yang sebelumnya ditangani SDK secara otomatis kini menjadi tanggung jawab klien Anda.

| Fitur SDK                         | Pendekatan Managed Agents                                                                                                                                                |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Plan mode                         | Jalankan sesi khusus perencanaan terlebih dahulu, lalu sesi kedua untuk menjalankan rencana tersebut.                                                                    |
| Output styles, slash commands     | Terapkan di klien Anda sebelum mengirim `user.message` atau setelah menerima `agent.message`.                                                                            |
| Hook `PreToolUse` / `PostToolUse` | Klien Anda sudah melihat setiap event `agent.custom_tool_use` sebelum merespons; letakkan logikanya di sana. Untuk alat bawaan, gunakan `permission_policy: always_ask`. |
| `max_turns`                       | Hitung giliran di sisi klien.                                                                                                                                            |

## Daftar periksa migrasi

1. [Buat environment](/docs/id/managed-agents/environments) dengan jaringan dan runtime yang dibutuhkan agen Anda.
2. Pindahkan prompt sistem dan pemilihan alat Anda ke [definisi agen](/docs/id/managed-agents/agent-setup).
3. Ganti loop Anda dengan [`sessions.create`](/docs/id/managed-agents/sessions) dan [`sessions.events.stream`](/docs/id/managed-agents/events-and-streaming).
4. Untuk file lokal apa pun yang dibaca agen, unggah melalui [Files API](/docs/id/managed-agents/files) dan mount sebagai `resources`.
5. Untuk handler alat kustom apa pun, pindahkan eksekusi ke dalam event loop Anda sebagai respons terhadap event `agent.custom_tool_use`.
6. Verifikasi dengan sesi uji sebelum mengarahkan trafik produksi ke alur baru.

## Migrasi antar versi model

Ketika model Claude baru dirilis, memigrasikan integrasi Claude Managed Agents biasanya hanya perubahan satu field: perbarui `model` pada [definisi agen](/docs/id/managed-agents/agent-setup) Anda dan perubahan tersebut berlaku pada sesi berikutnya yang Anda buat.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -sS --fail-with-body "https://api.anthropic.com/v1/agents/$AGENT_ID?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    --json "$(jq -n --argjson version "$AGENT_VERSION" '{version: $version, model: "claude-opus-4-8"}')"
  ```

  ```bash CLI
  ant beta:agents update \
    --agent-id "$AGENT_ID" \
    --version "$AGENT_VERSION" \
    --model claude-opus-4-8
  ```

  ```python Python
  client.beta.agents.update(
      agent.id,
      version=agent.version,
      model="claude-opus-4-8",
  )
  ```

  ```typescript TypeScript
  await client.beta.agents.update(agent.id, {
    version: agent.version,
    model: "claude-opus-4-8"
  });
  ```

  ```csharp C#
  await client.Beta.Agents.Update(agent.ID, new()
  {
      Version = agent.Version,
      Model = BetaManagedAgentsModel.ClaudeOpus4_8,
  });
  ```

  ```go Go
  _, err = client.Beta.Agents.Update(ctx, agent.ID, anthropic.BetaAgentUpdateParams{
  	Version: agent.Version,
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus4_8,
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().agents().update(
      agent.id(),
      AgentUpdateParams.builder()
          .version(agent.version())
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
          .build()
  );
  ```

  ```php PHP
  $client->beta->agents->update(
      $agent->id,
      version: $agent->version,
      model: 'claude-opus-4-8',
  );
  ```

  ```ruby Ruby
  client.beta.agents.update(
    agent.id,
    version: agent.version,
    model: "claude-opus-4-8"
  )
  ```
</CodeGroup>

Sebagian besar perubahan perilaku tingkat model yang didokumentasikan dalam [panduan migrasi Messages API](/docs/id/about-claude/models/migration-guide) tidak memerlukan tindakan dari sisi Anda:

* **Perubahan parameter permintaan** (default `max_tokens`, konfigurasi `thinking`) ditangani oleh runtime Claude Managed Agents. Field ini tidak diekspos pada definisi agen.
* **Prefilling pesan asisten** tidak ada dalam model sesi berbasis event, sehingga penghapusannya pada model yang lebih baru tidak berdampak apa-apa.
* **Escaping JSON argumen alat** di-parse oleh runtime sebelum Anda menerima event `agent.custom_tool_use`. Anda melihat data terstruktur, bukan string mentah.

Deskripsi perilaku dalam panduan Messages API (apa yang dilakukan model secara berbeda) masih berlaku. Langkah-langkah migrasi (cara mengubah kode permintaan Anda) tidak berlaku.
