---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/sessions
fetched_at: 2026-07-23T03:08:39.550142Z
sha256: 2d39aec44d0c1622549bc76fae0d4b2572dfd17f87d7ba770f68886c53a9ca7b
---

# Memulai sesi

Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.

---

Sesi adalah instans agen di dalam sebuah environment. Setiap sesi mereferensikan sebuah [agen](/docs/id/managed-agents/agent-setup) dan sebuah [environment](/docs/id/managed-agents/environments) (keduanya dibuat secara terpisah), dan mempertahankan riwayat percakapan di sepanjang beberapa interaksi. Sesi mengikuti siklus hidup dua langkah: pertama [buat sesi](#creating-a-session) untuk menyediakan sandbox-nya, lalu [kirim user event](#starting-the-session) untuk memulai pekerjaan.

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Membuat sesi

Sebuah sesi memerlukan ID `agent` dan ID `environment`. Agen adalah sumber daya yang memiliki versi; meneruskan ID `agent` sebagai string akan memulai sesi dengan versi agen terbaru.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
  )
  SESSION_ID=$(jq -r '.id' <<< "$session")
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID"
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id
  )
  ```
</CodeGroup>

Untuk menyematkan sesi ke versi agen tertentu, teruskan sebuah objek. Ini memungkinkan Anda mengontrol dengan tepat versi mana yang berjalan dan melakukan rollout bertahap untuk versi baru secara independen.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  pinned_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": {"type": "agent", "id": "$AGENT_ID", "version": 1},
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
  )
  PINNED_SESSION_ID=$(jq -r '.id' <<< "$pinned_session")
  ```

  ```bash CLI
  ant beta:sessions create <<YAML
  agent:
    type: agent
    id: $AGENT_ID
    version: 1
  environment_id: $ENVIRONMENT_ID
  YAML
  ```

  ```python Python
  pinned_session = client.beta.sessions.create(
      agent={"type": "agent", "id": agent.id, "version": 1},
      environment_id=environment.id,
  )
  ```

  ```typescript TypeScript
  const pinnedSession = await client.beta.sessions.create({
    agent: { type: "agent", id: agent.id, version: 1 },
    environment_id: environment.id
  });
  ```

  ```csharp C#
  var pinnedSession = await client.Beta.Sessions.Create(new()
  {
      Agent = new BetaManagedAgentsAgentParams
      {
          Type = BetaManagedAgentsAgentParamsType.Agent,
          ID = agent.ID,
          Version = 1,
      },
      EnvironmentID = environment.ID,
  });
  ```

  ```go Go
  pinnedSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfBetaManagedAgentsAgents: &anthropic.BetaManagedAgentsAgentParams{
  			Type:    anthropic.BetaManagedAgentsAgentParamsTypeAgent,
  			ID:      agent.ID,
  			Version: anthropic.Int(1),
  		},
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var pinnedSession = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(BetaManagedAgentsAgentParams.builder()
          .type(BetaManagedAgentsAgentParams.Type.AGENT)
          .id(agent.id())
          .version(1)
          .build())
      .environmentId(environment.id())
      .build());
  ```

  ```php PHP
  $pinnedSession = $client->beta->sessions->create(
      agent: ['type' => 'agent', 'id' => $agent->id, 'version' => 1],
      environmentID: $environment->id,
  );
  ```

  ```ruby Ruby
  pinned_session = client.beta.sessions.create(
    agent: {type: :agent, id: agent.id, version: 1},
    environment_id: environment.id
  )
  ```
</CodeGroup>

### Menimpa konfigurasi agen untuk sebuah sesi

Anda dapat meneruskan `agent` dalam tiga bentuk: string ID agen, objek versi tersemat (`type: "agent"`), atau objek overrides. Bentuk overrides mengubah sebagian konfigurasi agen untuk satu sesi saja. Gunakan ini untuk mencoba model yang berbeda atau memberikan alat tambahan dalam satu sesi tanpa membuat versi baru agen. Untuk bentuk overrides, atur `type` ke `agent_with_overrides` dan teruskan `id` agen serta secara opsional `version` (hilangkan `version` untuk menggunakan versi terbaru agen). Kemudian sertakan salah satu dari `model`, `system`, `tools`, `mcp_servers`, atau `skills` dengan nilai yang harus digunakan oleh sesi.

Setiap field yang dapat ditimpa mengikuti tiga aturan yang sama:

* **Hilangkan field:** Sesi mewarisi nilai dari versi agen yang direferensikannya.

* **Atur field ke `null`, atau ke array kosong untuk field berbentuk daftar:** Sesi berjalan dengan field tersebut dikosongkan. Aturan ini berlaku sepenuhnya untuk `system`, `mcp_servers`, dan `skills`. Ada dua pengecualian:

  * `model` tidak pernah dapat dikosongkan. Sesi selalu membutuhkan model, sehingga `model: null` mengembalikan error 400 `agent_model_required`.
  * Mengosongkan `tools` mengembalikan error 400 ketika `skills` efektif sesi tidak kosong, karena skills memerlukan alat `read`. Jika tidak, `tools: null` dan `tools: []` akan mengosongkan field tersebut.

* **Atur field ke sebuah nilai:** Nilai tersebut menggantikan nilai agen sepenuhnya. Overrides tidak pernah digabungkan dengan konfigurasi agen, sehingga override `tools` harus mencantumkan setiap alat yang harus dimiliki sesi.

Overrides hanya berlaku untuk sesi yang Anda buat. Overrides tidak memodifikasi sumber daya agen atau membuat versi agen baru, sehingga sesi lain yang mereferensikan agen yang sama tidak terpengaruh.

Dalam respons, objek `agent` mencerminkan konfigurasi yang digunakan sesi setelah overrides diterapkan. `id` dan `version`-nya tetap mengidentifikasi agen dan versi tempat overrides diterapkan. Ini memungkinkan Anda melacak sesi kembali ke agen dasarnya.

Contoh berikut memulai sesi yang menimpa model dan mengosongkan prompt sistem:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  override_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": {
      "type": "agent_with_overrides",
      "id": "$AGENT_ID",
      "model": {"id": "claude-sonnet-5"},
      "system": null
    },
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
  )
  jq '.agent | {id, version, model, system}' <<< "$override_session"
  OVERRIDE_SESSION_ID=$(jq -r '.id' <<< "$override_session")
  ```

  ```bash CLI
  # The response's `agent` is the resolved snapshot: each override replaces that
  # field for this session only, and the agent resource keeps its id and version.
  ant beta:sessions create \
    --transform 'agent.{id,version,model,system}' \
    --format json <<YAML
  agent:
    type: agent_with_overrides
    id: $AGENT_ID
    model:
      id: claude-sonnet-5
    system: null
  environment_id: $ENVIRONMENT_ID
  YAML
  ```

  ```python Python
  override_session = client.beta.sessions.create(
      agent={
          "type": "agent_with_overrides",
          "id": agent.id,
          "model": {"id": "claude-sonnet-5"},
          "system": None,  # clear the agent's system prompt for this session
      },
      environment_id=environment.id,
  )
  # The response's agent is the resolved snapshot with the overrides applied.
  print(f"Model: {override_session.agent.model.id}")
  print(f"System: {override_session.agent.system}")
  ```

  ```typescript TypeScript
  const overrideSession = await client.beta.sessions.create({
    agent: {
      type: "agent_with_overrides",
      id: agent.id,
      model: { id: "claude-sonnet-5" },
      system: null // clear the agent's system prompt for this session
    },
    environment_id: environment.id
  });
  // The response's agent is the resolved snapshot with the overrides applied.
  console.log(`Model: ${overrideSession.agent.model.id}`);
  console.log(`System: ${overrideSession.agent.system}`);
  ```

  ```csharp C#
  var overrideSession = await client.Beta.Sessions.Create(new()
  {
      Agent = new BetaManagedAgentsAgentWithOverridesParams
      {
          Type = BetaManagedAgentsAgentWithOverridesParamsType.AgentWithOverrides,
          ID = agent.ID,
          Model = new BetaManagedAgentsModelConfigParams
          {
              ID = BetaManagedAgentsModel.ClaudeSonnet5,
          },
          System = null, // clear the agent's system prompt for this session
      },
      EnvironmentID = environment.ID,
  });
  // The response's agent is the resolved snapshot with the overrides applied.
  Console.WriteLine($"Model: {overrideSession.Agent.Model.ID.Raw()}");
  Console.WriteLine($"System: {overrideSession.Agent.System ?? "null"}");
  ```

  ```go Go
  overrideSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfBetaManagedAgentsAgentWithOverridess: &anthropic.BetaManagedAgentsAgentWithOverridesParams{
  			Type: anthropic.BetaManagedAgentsAgentWithOverridesParamsTypeAgentWithOverrides,
  			ID:   agent.ID,
  			Model: anthropic.BetaManagedAgentsModelConfigParams{
  				ID: anthropic.BetaManagedAgentsModelClaudeSonnet5,
  			},
  			// Clear the agent's system prompt for this session.
  			System: param.Null[string](),
  		},
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  // The response's agent is the resolved snapshot with the overrides applied.
  fmt.Printf("Model: %s\n", overrideSession.Agent.Model.ID)
  fmt.Printf("System: %q\n", overrideSession.Agent.System)
  ```

  ```java Java
  var overrideSession = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(BetaManagedAgentsAgentWithOverridesParams.builder()
          .type(BetaManagedAgentsAgentWithOverridesParams.Type.AGENT_WITH_OVERRIDES)
          .id(agent.id())
          .model(BetaManagedAgentsModelConfigParams.builder()
              .id(BetaManagedAgentsModel.CLAUDE_SONNET_5)
              .build())
          .system((String) null) // clear the agent's system prompt for this session
          .build())
      .environmentId(environment.id())
      .build());
  // The response's agent is the resolved snapshot with the overrides applied.
  IO.println("Model: " + overrideSession.agent().model().id());
  IO.println("System: " + overrideSession.agent().system().orElse("null"));
  ```

  ```php PHP
  $overrides = BetaManagedAgentsAgentWithOverridesParams::with(
      id: $agent->id,
      type: 'agent_with_overrides',
      model: ['id' => 'claude-sonnet-5'],
  );
  // Clear the system prompt for this session. Array access is load-bearing here:
  // create() strips nulls from raw arrays and ::with() treats null args as omitted.
  $overrides['system'] = null;

  $overrideSession = $client->beta->sessions->create(
      agent: $overrides,
      environmentID: $environment->id,
  );
  // The response's agent is the resolved snapshot with the overrides applied.
  echo "Model: {$overrideSession->agent->model->id}\n";
  echo 'System: ' . ($overrideSession->agent->system ?? 'null') . "\n";
  ```

  ```ruby Ruby
  # The system prompt override is `system_` (trailing underscore) because plain
  # `system` is Ruby's Kernel#system. Setting it to nil clears the prompt.
  override_session = client.beta.sessions.create(
    agent: Anthropic::Beta::BetaManagedAgentsAgentWithOverridesParams.new(
      type: :agent_with_overrides,
      id: agent.id,
      model: {id: "claude-sonnet-5"},
      system_: nil
    ),
    environment_id: environment.id
  )
  # The response's agent is the resolved snapshot with the overrides applied.
  puts "Model: #{override_session.agent.model.id}"
  puts "System: #{override_session.agent.system_.inspect}"
  ```
</CodeGroup>

<Tip>
  Agen mendefinisikan bagaimana Claude berperilaku di dalam sesi, termasuk model, prompt sistem, alat, dan server MCP. Lihat [Definisikan agen Anda](/docs/id/managed-agents/agent-setup) untuk detailnya.
</Tip>

## Autentikasi MCP melalui vault

Jika agen Anda menggunakan alat MCP yang memerlukan autentikasi, teruskan `vault_ids` saat pembuatan sesi untuk mereferensikan vault yang berisi kredensial OAuth yang tersimpan. Anthropic mengelola pembaruan token atas nama Anda. Lihat [Autentikasi dengan vault](/docs/id/managed-agents/vaults) untuk cara membuat vault dan mendaftarkan kredensial.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  vault_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID",
    "vault_ids": ["$VAULT_ID"]
  }
  EOF
  )
  VAULT_SESSION_ID=$(jq -r '.id' <<< "$vault_session")
  ```

  ```bash CLI
  ant beta:sessions create <<YAML
  agent: $AGENT_ID
  environment_id: $ENVIRONMENT_ID
  vault_ids:
    - $VAULT_ID
  YAML
  ```

  ```python Python
  vault_session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      vault_ids=[vault.id],
  )
  ```

  ```typescript TypeScript
  const vaultSession = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id]
  });
  ```

  ```csharp C#
  var vaultSession = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      VaultIds = [vault.ID],
  });
  ```

  ```go Go
  vaultSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	VaultIDs:      []string{vault.ID},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var vaultSession = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .addVaultId(vault.id())
      .build());
  ```

  ```php PHP
  $vaultSession = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      vaultIDs: [$vault->id],
  );
  ```

  ```ruby Ruby
  vault_session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id]
  )
  ```
</CodeGroup>

## Memulai sesi

Membuat sesi akan menyediakan sandbox environment tetapi tidak memulai pekerjaan apa pun. Untuk mendelegasikan tugas, kirim event ke sesi menggunakan [user event](/docs/id/managed-agents/reference#event-types). Sesi bertindak sebagai state machine yang melacak kemajuan sementara event menggerakkan eksekusi yang sebenarnya.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "events": [
      {
        "type": "user.message",
        "content": [{"type": "text", "text": "List the files in the working directory."}]
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" <<'YAML'
  events:
    - type: user.message
      content:
        - type: text
          text: List the files in the working directory.
  YAML
  ```

  ```python Python
  client.beta.sessions.events.send(
      session.id,
      events=[
          {
              "type": "user.message",
              "content": [
                  {"type": "text", "text": "List the files in the working directory."}
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
        content: [{ type: "text", text: "List the files in the working directory." }]
      }
    ]
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
                      Text = "List the files in the working directory.",
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
  					Text: "List the files in the working directory.",
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
              .addTextContent("List the files in the working directory.")
              .build())
          .build());
  ```

  ```php PHP
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => 'List the files in the working directory.']],
          ],
      ],
  );
  ```

  ```ruby Ruby
  client.beta.sessions.events.send_(
    session.id,
    events: [
      {
        type: :"user.message",
        content: [{type: :text, text: "List the files in the working directory."}]
      }
    ]
  )
  ```
</CodeGroup>

Lihat [Aliran event sesi](/docs/id/managed-agents/events-and-streaming) untuk cara melakukan streaming respons agen dan menangani konfirmasi alat.

Lihat [Status sesi](/docs/id/managed-agents/session-operations#session-statuses) untuk status-status yang dilalui sebuah sesi.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Operasi sesi" icon="settings" href="/docs/id/managed-agents/session-operations">
    Ambil, daftar, perbarui, arsipkan, dan hapus sesi Claude Managed Agents.
  </Card>

  <Card title="Aliran event sesi" icon="lightning" href="/docs/id/managed-agents/events-and-streaming">
    Kirim event, lakukan streaming respons, dan interupsi atau alihkan sesi Anda di tengah eksekusi.
  </Card>

  <Card title="Deployment terjadwal" icon="arrows-clockwise" href="/docs/id/managed-agents/scheduled-deployments">
    Buat dan kelola deployment dengan Claude API: jalankan agen pada jadwal cron berulang dan periksa riwayat eksekusinya.
  </Card>
</CardGroup>
