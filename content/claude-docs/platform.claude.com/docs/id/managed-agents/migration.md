---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/migration
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 6e53b6948e94fb3b2573ab6f8db68d355eb41ecd73b238708e2cb1c0420a220d
---

---
title: Migrasi
url: https://platform.claude.com/docs/id/managed-agents/migration
description: Pindahkan agen yang sudah ada yang dibangun di atas Messages API atau Claude Agent SDK ke Claude Managed Agents.
---

Claude Managed Agents menggantikan loop agen yang Anda tulis sendiri dengan infrastruktur terkelola. Halaman ini membahas apa yang berubah ketika Anda bermigrasi dari loop kustom yang dibangun di atas [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) atau dari [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview).

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK menetapkan header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Dari loop agen Messages API

Jika Anda membangun agen dengan memanggil `messages.create` dalam loop `while`, menjalankan pemanggilan alat sendiri, dan menambahkan hasilnya ke riwayat percakapan, sebagian besar kode tersebut akan hilang.

### Apa yang tidak perlu Anda kelola lagi

| Sebelum                                                                                                           | Sesudah                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Anda memelihara array riwayat percakapan dan mengirimkannya kembali pada setiap giliran.                          | Sesi menyimpan riwayat di sisi server. Kirim event, terima event.                                                              |
| Anda mengiterasi blok konten `tool_use`, menjalankan setiap alat, dan kembali ke loop dengan pesan `tool_result`. | Alat bawaan berjalan di dalam sandbox secara otomatis. Anda hanya menangani alat kustom melalui event `agent.custom_tool_use`. |
| Anda menyediakan sandbox sendiri untuk menjalankan kode yang dihasilkan agen.                                     | Sandbox sesi menangani eksekusi kode, operasi file, dan bash.                                                                  |
| Anda memutuskan kapan loop selesai.                                                                               | Sesi memancarkan `session.status_idle` ketika agen tidak memiliki hal lain untuk dilakukan.                                    |

### Perbandingan kode

**Sebelum** (loop Messages API, disederhanakan):

<CodeGroup>
  ```python Python
  messages = [{"role": "user", "content": task}]
  while True:
      response = client.messages.create(
          model="claude-opus-5",
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
      model: "claude-opus-5",
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
          Model = Model.ClaudeOpus5,
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
  		Model:     anthropic.ModelClaudeOpus5,
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
          .model(Model.CLAUDE_OPUS_5)
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
          model: 'claude-opus-5',
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
      model: "claude-opus-5",
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
        "model": "claude-opus-5",
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
  # membaca melalui process substitution berarti shell tidak menunggu
  # tail (pipeline `tail -f | grep -m1` di latar depan akan macet: tail
  # hanya mati pada penulisan berikutnya, yang tak pernah terjadi setelah stream idle).
  grep -m1 '"session.status_idle"' <(tail -f -n +1 "${stream_log}") > /dev/null

  kill "${stream_pid}" 2>/dev/null || true
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    { read -r _ agent_id; read -r _ agent_version; } < <(ant beta:agents create \
      --transform '{id,version}' --format yaml < task-runner.agent.yaml)

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

    <File filename="task-runner.agent.yaml">
      ```yaml
      name: Task Runner
      model: claude-opus-5
      tools:
        - type: agent_toolset_20260401
      ```
    </File>
  </MultiFileExample>

  ```python Python
  agent = client.beta.agents.create(
      name="Task Runner",
      model="claude-opus-5",
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
    model: "claude-opus-5",
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
      Model = BetaManagedAgentsModel.ClaudeOpus5,
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
  			ID: anthropic.BetaManagedAgentsModelClaudeOpus5,
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
              .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
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
      model: 'claude-opus-5',
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
    model: "claude-opus-5",
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

* **Prompt sistem dan model:** Field yang sama, kini berada pada definisi agen.
* **Alat kustom:** Masih dideklarasikan dengan JSON Schema. Eksekusi berpindah dari penanganan inline menjadi merespons event `agent.custom_tool_use`. Lihat [Aliran event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming).
* **Pengaturan web search dan web fetch:** Field `allowed_domains`, `blocked_domains`, `max_content_tokens`, dan `user_location` yang sama, kini diatur sekali pada entri `web_search` dan `web_fetch` dalam array `configs` milik toolset agen, bukan pada setiap permintaan. Field `max_uses`, `citations`, dan `cache_control` tidak tersedia. Lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools#restrict-web-search-and-web-fetch-domains).
* **Konteks:** Anda masih dapat menyuntikkan konteks melalui prompt sistem, [sumber daya file](https://platform.claude.com/docs/id/managed-agents/files), atau [skills](https://platform.claude.com/docs/id/managed-agents/skills).

## Dari Claude Agent SDK

Jika Anda membangun dengan [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), Anda sudah bekerja dengan agen, alat, dan sesi sebagai konsep. Perbedaannya adalah di mana semuanya berjalan: SDK berjalan dalam proses yang Anda operasikan, sedangkan Managed Agents berjalan di infrastruktur Anthropic. Sebagian besar migrasi adalah memetakan objek konfigurasi SDK ke padanannya di sisi API.

### Apa yang berubah

| Agent SDK                                                            | Managed Agents                                                                                                                                                                                                                                                                                 |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ClaudeAgentOptions(...)` dibuat per eksekusi                        | `client.beta.agents.create(...)` sekali; Agent disimpan dan diberi versi di sisi server. Lihat [Penyiapan agen](https://platform.claude.com/docs/id/managed-agents/agent-setup).                                                                                                               |
| `async with ClaudeSDKClient(...)` atau `query(...)`                  | `client.beta.sessions.create(...)` lalu kirim dan terima [event](https://platform.claude.com/docs/id/managed-agents/events-and-streaming).                                                                                                                                                     |
| Fungsi berdekorator `@tool` yang didispatch secara otomatis oleh SDK | Deklarasikan sebagai `{"type": "custom", ...}` pada Agent; klien Anda menangani event `agent.custom_tool_use` dan membalas dengan `user.custom_tool_result`. Lihat [Alat](https://platform.claude.com/docs/id/managed-agents/tools).                                                           |
| Alat bawaan berjalan dalam proses Anda terhadap sistem file Anda     | `{"type": "agent_toolset_20260401"}` menjalankan alat yang sama di dalam sandbox sesi terhadap `/workspace`.                                                                                                                                                                                   |
| `cwd`, `add_dirs` menunjuk ke path lokal                             | Unggah atau mount [file](https://platform.claude.com/docs/id/managed-agents/files) sebagai sumber daya sesi.                                                                                                                                                                                   |
| `system_prompt` dan hierarki `CLAUDE.md`                             | Satu string `system` pada Agent. Setiap pembaruan yang mengubah agen menghasilkan versi baru di sisi server; sematkan sesi ke versi tertentu untuk mempromosikan atau melakukan rollback tanpa deploy. Lihat [Penyiapan agen](https://platform.claude.com/docs/id/managed-agents/agent-setup). |
| `mcp_servers` dikonfigurasi dan diautentikasi di satu tempat         | Deklarasikan server pada Agent; sediakan kredensial melalui [Vault](https://platform.claude.com/docs/id/managed-agents/vaults) pada Session.                                                                                                                                                   |
| `permission_mode`, `can_use_tool`                                    | [`permission_policy`](https://platform.claude.com/docs/id/managed-agents/permission-policies) per alat; kirim event `user.tool_confirmation` untuk alat `always_ask`.                                                                                                                          |

### Perbandingan kode

**Sebelum** (Agent SDK):

<CodeGroup exclude="shell, csharp, go, java, php, ruby">
  ```python Python
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
      model="claude-opus-5",
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

  ```typescript TypeScript
  import { createSdkMcpServer, query, tool } from "@anthropic-ai/claude-agent-sdk";
  import { z } from "zod";

  const getWeather = tool(
    "get_weather",
    "Get the current weather for a city.",
    { city: z.string() },
    async (args) => ({
      content: [{ type: "text", text: `${args.city}: 18°C, clear` }]
    })
  );

  for await (const message of query({
    prompt: "What's the weather in Tokyo?",
    options: {
      model: "claude-opus-5",
      systemPrompt: "You are a concise weather assistant.",
      mcpServers: {
        weather: createSdkMcpServer({ name: "weather", version: "1.0", tools: [getWeather] })
      }
    }
  })) {
    console.log(message);
  }
  ```
</CodeGroup>

**Sesudah** (Managed Agents):

<CodeGroup exclude="shell">
  ```python Python
  from anthropic import Anthropic

  client = Anthropic()

  agent = client.beta.agents.create(
      name="weather-agent",
      model="claude-opus-5",
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
      for event in stream:
          if event.type == "agent.message":
              print(
                  "".join(block.text for block in event.content if block.type == "text")
              )
          elif event.type == "agent.custom_tool_use":
              result = get_weather(**event.input)
              client.beta.sessions.events.send(
                  session.id,
                  events=[
                      {
                          "type": "user.custom_tool_result",
                          "custom_tool_use_id": event.id,
                          "content": [{"type": "text", "text": result}],
                      }
                  ],
              )
          elif (
              event.type == "session.status_idle"
              and event.stop_reason
              and event.stop_reason.type == "end_turn"
          ):
              break
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const agent = await client.beta.agents.create({
    name: "weather-agent",
    model: "claude-opus-5",
    system: "You are a concise weather assistant.",
    tools: [
      {
        type: "custom",
        name: "get_weather",
        description: "Get the current weather for a city.",
        input_schema: {
          type: "object",
          properties: { city: { type: "string" } },
          required: ["city"]
        }
      }
    ]
  });
  const environment = await client.beta.environments.create({
    name: "weather-env",
    config: { type: "cloud", networking: { type: "unrestricted" } }
  });

  const session = await client.beta.sessions.create({
    agent: { type: "agent", id: agent.id, version: agent.version },
    environment_id: environment.id
  });

  function getWeather({ city }: Record<string, unknown>): string {
    return `${city}: 18°C, clear`;
  }

  const stream = await client.beta.sessions.events.stream(session.id);

  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "What's the weather in Tokyo?" }]
      }
    ]
  });

  for await (const event of stream) {
    if (event.type === "agent.message") {
      for (const block of event.content) {
        if (block.type === "text") {
          console.log(block.text);
        }
      }
    } else if (event.type === "agent.custom_tool_use") {
      const result = getWeather(event.input);
      await client.beta.sessions.events.send(session.id, {
        events: [
          {
            type: "user.custom_tool_result",
            custom_tool_use_id: event.id,
            content: [{ type: "text", text: result }]
          }
        ]
      });
    } else if (event.type === "session.status_idle" && event.stop_reason?.type === "end_turn") {
      break;
    }
  }
  ```

  ```csharp C#
  using System.Text.Json;

  using Anthropic.Models.Beta.Agents;
  using Anthropic.Models.Beta.Environments;
  using Anthropic.Models.Beta.Sessions;
  using Anthropic.Models.Beta.Sessions.Events;

  AnthropicClient client = new();

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "weather-agent",
      Model = BetaManagedAgentsModel.ClaudeOpus5,
      System = "You are a concise weather assistant.",
      Tools =
      [
          new BetaManagedAgentsCustomToolParams
          {
              Type = "custom",
              Name = "get_weather",
              Description = "Get the current weather for a city.",
              InputSchema = new()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["city"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  },
                  Required = ["city"],
              },
          },
      ],
  });
  var environment = await client.Beta.Environments.Create(new()
  {
      Name = "weather-env",
      Config = new BetaCloudConfigParams
      {
          Networking = new BetaUnrestrictedNetwork(),
      },
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

  static string GetWeather(string city) => $"{city}: 18°C, clear";

  using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(session.ID);

  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Type = "user.message",
              Content = [new BetaManagedAgentsTextBlock { Type = "text", Text = "What's the weather in Tokyo?" }],
          },
      ],
  });

  await foreach (var streamEvent in stream.Enumerate())
  {
      if (streamEvent.Value is BetaManagedAgentsAgentMessageEvent message)
      {
          Console.WriteLine(string.Concat(message.Content.Select(block => block.Text)));
      }
      else if (streamEvent.Value is BetaManagedAgentsAgentCustomToolUseEvent toolUse)
      {
          var result = GetWeather(toolUse.Input["city"].GetString()!);
          await client.Beta.Sessions.Events.Send(session.ID, new()
          {
              Events =
              [
                  new BetaManagedAgentsUserCustomToolResultEventParams
                  {
                      Type = "user.custom_tool_result",
                      CustomToolUseID = toolUse.ID,
                      Content =
                      [
                          new BetaManagedAgentsTextBlock
                          {
                              Type = "text",
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
  client := anthropic.NewClient()
  ctx := context.Background()

  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "weather-agent",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5,
  	},
  	System: anthropic.String("You are a concise weather assistant."),
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
  			Type:        anthropic.BetaManagedAgentsCustomToolParamsTypeCustom,
  			Name:        "get_weather",
  			Description: "Get the current weather for a city.",
  			InputSchema: anthropic.BetaManagedAgentsCustomToolInputSchemaParam{
  				Properties: map[string]any{
  					"city": map[string]any{"type": "string"},
  				},
  				Required: []string{"city"},
  			},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
  	Name: "weather-env",
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
  	panic(err)
  }

  getWeather := func(city string) string {
  	return fmt.Sprintf("%s: 18°C, clear", city)
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
  					Text: "What's the weather in Tokyo?",
  				},
  			}},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }

  loop:
  for stream.Next() {
  	event := stream.Current()
  	switch event.Type {
  	case "agent.message":
  		for _, block := range event.AsAgentMessage().Content {
  			if block.Type == "text" {
  				fmt.Println(block.Text)
  			}
  		}
  	case "agent.custom_tool_use":
  		toolUse := event.AsAgentCustomToolUse()
  		result := getWeather(toolUse.Input["city"].(string))
  		if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  			Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  				OfUserCustomToolResult: &anthropic.BetaManagedAgentsUserCustomToolResultEventParams{
  					Type:            anthropic.BetaManagedAgentsUserCustomToolResultEventParamsTypeUserCustomToolResult,
  					CustomToolUseID: toolUse.ID,
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
  	case "session.status_idle":
  		idle := event.AsSessionStatusIdle()
  		if _, ok := idle.StopReason.AsAny().(anthropic.BetaManagedAgentsSessionEndTurn); ok {
  			break loop
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  import java.util.Map;
  import java.util.function.Function;

  import com.anthropic.models.beta.agents.AgentCreateParams;
  import com.anthropic.models.beta.agents.BetaManagedAgentsCustomToolInputSchema;
  import com.anthropic.models.beta.agents.BetaManagedAgentsCustomToolParams;
  import com.anthropic.models.beta.agents.BetaManagedAgentsModel;
  import com.anthropic.models.beta.environments.BetaCloudConfigParams;
  import com.anthropic.models.beta.environments.BetaUnrestrictedNetwork;
  import com.anthropic.models.beta.environments.EnvironmentCreateParams;
  import com.anthropic.models.beta.sessions.BetaManagedAgentsAgentParams;
  import com.anthropic.models.beta.sessions.SessionCreateParams;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsStreamSessionEvents;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserCustomToolResultEventParams;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserMessageEventParams;
  import com.anthropic.models.beta.sessions.events.EventSendParams;

  var client = AnthropicOkHttpClient.fromEnv();

  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("weather-agent")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
      .system("You are a concise weather assistant.")
      .addTool(BetaManagedAgentsCustomToolParams.builder()
          .type(BetaManagedAgentsCustomToolParams.Type.CUSTOM)
          .name("get_weather")
          .description("Get the current weather for a city.")
          .inputSchema(BetaManagedAgentsCustomToolInputSchema.builder()
              .properties(BetaManagedAgentsCustomToolInputSchema.Properties.builder()
                  .putAdditionalProperty("city", JsonValue.from(Map.of("type", "string")))
                  .build())
              .addRequired("city")
              .build())
          .build())
      .build());
  var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
      .name("weather-env")
      .config(BetaCloudConfigParams.builder()
          .networking(BetaUnrestrictedNetwork.builder().build())
          .build())
      .build());

  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(BetaManagedAgentsAgentParams.builder()
          .type(BetaManagedAgentsAgentParams.Type.AGENT)
          .id(agent.id())
          .version(agent.version())
          .build())
      .environmentId(environment.id())
      .build());

  Function<String, String> getWeather = city -> city + ": 18°C, clear";

  try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                  .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                  .addTextContent("What's the weather in Tokyo?")
                  .build())
              .build());

      for (var event : (Iterable<BetaManagedAgentsStreamSessionEvents>) stream.stream()::iterator) {
          if (event.isAgentMessage()) {
              for (var block : event.asAgentMessage().content()) {
                  block.text().ifPresent(textBlock -> IO.println(textBlock.text()));
              }
          } else if (event.isAgentCustomToolUse()) {
              var toolUse = event.asAgentCustomToolUse();
              var city = toolUse.input()._additionalProperties().get("city").asStringOrThrow();
              var result = getWeather.apply(city);
              client.beta().sessions().events().send(
                  session.id(),
                  EventSendParams.builder()
                      .addEvent(BetaManagedAgentsUserCustomToolResultEventParams.builder()
                          .type(BetaManagedAgentsUserCustomToolResultEventParams.Type.USER_CUSTOM_TOOL_RESULT)
                          .customToolUseId(toolUse.id())
                          .addTextContent(result)
                          .build())
                      .build());
          } else if (event.isSessionStatusIdle()
              && event.asSessionStatusIdle().stopReason().isEndTurn()) {
              break;
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolInputSchema;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolParams;
  use Anthropic\Beta\Sessions\BetaManagedAgentsAgentParams;

  $client = new Client();

  $agent = $client->beta->agents->create(
      name: 'weather-agent',
      model: 'claude-opus-5',
      system: 'You are a concise weather assistant.',
      tools: [
          BetaManagedAgentsCustomToolParams::with(
              type: 'custom',
              name: 'get_weather',
              description: 'Get the current weather for a city.',
              inputSchema: BetaManagedAgentsCustomToolInputSchema::with(
                  properties: ['city' => ['type' => 'string']],
                  required: ['city'],
              ),
          ),
      ],
  );
  $environment = $client->beta->environments->create(
      name: 'weather-env',
      config: ['type' => 'cloud', 'networking' => ['type' => 'unrestricted']],
  );

  $session = $client->beta->sessions->create(
      agent: BetaManagedAgentsAgentParams::with(
          type: 'agent',
          id: $agent->id,
          version: $agent->version,
      ),
      environmentID: $environment->id,
  );

  function getWeather(string $city): string
  {
      return "{$city}: 18°C, clear";
  }

  $stream = $client->beta->sessions->events->streamStream($session->id);

  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => "What's the weather in Tokyo?"]],
          ],
      ],
  );

  foreach ($stream as $event) {
      if ($event->type === 'agent.message') {
          foreach ($event->content as $block) {
              if ($block->type === 'text') {
                  echo $block->text . "\n";
              }
          }
      } elseif ($event->type === 'agent.custom_tool_use') {
          $result = getWeather($event->input['city']);
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
      } elseif ($event->type === 'session.status_idle' && $event->stopReason?->type === 'end_turn') {
          break;
      }
  }
  $stream->close();
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  agent = client.beta.agents.create(
    name: "weather-agent",
    model: "claude-opus-5",
    system_: "You are a concise weather assistant.",
    tools: [
      {
        type: "custom",
        name: "get_weather",
        description: "Get the current weather for a city.",
        input_schema: {
          type: "object",
          properties: {city: {type: "string"}},
          required: ["city"]
        }
      }
    ]
  )
  environment = client.beta.environments.create(
    name: "weather-env",
    config: {type: "cloud", networking: {type: "unrestricted"}}
  )

  session = client.beta.sessions.create(
    agent: {type: "agent", id: agent.id, version: agent.version},
    environment_id: environment.id
  )

  def get_weather(city)
    "#{city}: 18°C, clear"
  end

  stream = client.beta.sessions.events.stream_events(session.id)
  client.beta.sessions.events.send_(
    session.id,
    events: [{type: "user.message", content: [{type: "text", text: "What's the weather in Tokyo?"}]}]
  )

  stream.each do |event|
    case event.type
    when :"agent.message"
      event.content.each do |block|
        puts block.text if block.type == :text
      end
    when :"agent.custom_tool_use"
      result = get_weather(event.input[:city])
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
    when :"session.status_idle"
      break if event.stop_reason&.type == :end_turn
    end
  end
  ```
</CodeGroup>

Agent dan Environment dibuat sekali dan digunakan kembali di berbagai sesi. Fungsi alat masih berjalan dalam proses Anda; perbedaannya adalah Anda membaca event `agent.custom_tool_use` dan mengirim hasilnya secara eksplisit, bukan SDK yang mendispatchnya untuk Anda.

### Fitur yang berpindah ke klien Anda

Konsekuensi dari Anthropic menjalankan loop agen adalah beberapa hal yang sebelumnya ditangani SDK secara otomatis kini menjadi tanggung jawab klien Anda.

| Fitur SDK                         | Pendekatan Managed Agents                                                                                                                                                |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Mode plan                         | Jalankan sesi khusus perencanaan terlebih dahulu, lalu sesi kedua untuk menjalankan rencana tersebut.                                                                    |
| Gaya output, slash command        | Terapkan di klien Anda sebelum mengirim `user.message` atau setelah menerima `agent.message`.                                                                            |
| Hook `PreToolUse` / `PostToolUse` | Klien Anda sudah melihat setiap event `agent.custom_tool_use` sebelum merespons; letakkan logikanya di sana. Untuk alat bawaan, gunakan `permission_policy: always_ask`. |
| `max_turns`                       | Hitung giliran di sisi klien.                                                                                                                                            |

## Daftar periksa migrasi

1. [Buat environment](https://platform.claude.com/docs/id/managed-agents/environments) dengan jaringan dan runtime yang dibutuhkan agen Anda.
2. Pindahkan prompt sistem dan pilihan alat Anda ke [definisi agen](https://platform.claude.com/docs/id/managed-agents/agent-setup).
3. Ganti loop Anda dengan [`sessions.create`](https://platform.claude.com/docs/id/managed-agents/sessions) dan [`sessions.events.stream`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming).
4. Untuk file lokal apa pun yang dibaca agen, unggah melalui [Files API](https://platform.claude.com/docs/id/managed-agents/files) dan mount sebagai `resources`.
5. Untuk handler alat kustom apa pun, pindahkan eksekusi ke dalam loop event Anda sebagai respons terhadap event `agent.custom_tool_use`.
6. Verifikasi dengan sesi uji sebelum mengarahkan lalu lintas produksi ke alur baru.

## Migrasi antar versi model

Ketika model Claude baru dirilis, migrasi integrasi Claude Managed Agents biasanya hanya berupa perubahan satu field: perbarui `model` pada [definisi agen](https://platform.claude.com/docs/id/managed-agents/agent-setup) Anda dan perubahan tersebut berlaku pada sesi berikutnya yang Anda buat.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -sS --fail-with-body "https://api.anthropic.com/v1/agents/$AGENT_ID?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    --json "$(jq -n --argjson version "$AGENT_VERSION" '{version: $version, model: "claude-opus-5"}')"
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:agents update --agent-id "$AGENT_ID" < agent.yaml
    ```

    <File filename="agent.yaml">
      ```yaml
      name: Task Runner
      model: claude-opus-5
      system: You are a task automation agent. Complete the task you are given end to end.
      tools:
        - type: agent_toolset_20260401
      ```
    </File>
  </MultiFileExample>

  ```python Python
  client.beta.agents.update(
      agent.id,
      version=agent.version,
      model="claude-opus-5",
  )
  ```

  ```typescript TypeScript
  await client.beta.agents.update(agent.id, {
    version: agent.version,
    model: "claude-opus-5"
  });
  ```

  ```csharp C#
  await client.Beta.Agents.Update(agent.ID, new()
  {
      Version = agent.Version,
      Model = BetaManagedAgentsModel.ClaudeOpus5,
  });
  ```

  ```go Go
  _, err = client.Beta.Agents.Update(ctx, agent.ID, anthropic.BetaAgentUpdateParams{
  	Version: agent.Version,
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5,
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
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
          .build()
  );
  ```

  ```php PHP
  $client->beta->agents->update(
      $agent->id,
      version: $agent->version,
      model: 'claude-opus-5',
  );
  ```

  ```ruby Ruby
  client.beta.agents.update(
    agent.id,
    version: agent.version,
    model: "claude-opus-5"
  )
  ```
</CodeGroup>

Sebagian besar perubahan perilaku tingkat model yang didokumentasikan dalam [panduan migrasi Messages API](https://platform.claude.com/docs/id/about-claude/models/migration-guide) tidak memerlukan tindakan dari pihak Anda:

* **Perubahan parameter permintaan** (default `max_tokens`, konfigurasi `thinking`) ditangani oleh runtime Claude Managed Agents. Field ini tidak diekspos pada definisi agen.
* **Prefilling pesan asisten** tidak ada dalam model sesi berbasis event, sehingga penghapusannya pada model yang lebih baru tidak berdampak apa pun.
* **Escaping JSON argumen alat** diurai oleh runtime sebelum Anda menerima event `agent.custom_tool_use`. Anda melihat data terstruktur, bukan string mentah.

Deskripsi perilaku dalam panduan Messages API (apa yang dilakukan model secara berbeda) tetap berlaku. Langkah-langkah migrasinya (cara mengubah kode permintaan Anda) tidak berlaku.
