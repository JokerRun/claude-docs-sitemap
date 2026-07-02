---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/sessions
fetched_at: 2026-07-02T03:13:49.360020Z
sha256: 0de64b650a6ffaa310dad3afbca6c52a626e34ca95105756893ab29c2cac6c56
---

# Memulai sesi

Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.

---

Sesi adalah instans agen di dalam sebuah lingkungan. Setiap sesi mereferensikan sebuah [agen](/docs/id/managed-agents/agent-setup) dan sebuah [lingkungan](/docs/id/managed-agents/environments) (keduanya dibuat secara terpisah), dan mempertahankan riwayat percakapan di sepanjang beberapa interaksi. Sesi mengikuti siklus hidup dua langkah: pertama [buat sesi](#creating-a-session) untuk menyediakan sandbox-nya, lalu [kirim user event](#starting-the-session) untuk memulai pekerjaan.

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

Untuk menyematkan sesi ke versi agen tertentu, teruskan sebuah objek. Ini memungkinkan Anda mengontrol secara tepat versi mana yang dijalankan dan mengatur peluncuran versi baru secara independen.

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
          Type = Anthropic.Models.Beta.Sessions.Type.Agent,
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

Anda dapat meneruskan `agent` dalam tiga bentuk: string ID agen, objek versi tersemat (`type: "agent"`), atau objek overrides. Bentuk overrides mengubah sebagian konfigurasi agen untuk satu sesi saja. Gunakan ini untuk mencoba model yang berbeda atau memberikan alat tambahan dalam satu sesi tanpa membuat versi baru pada agen. Untuk bentuk overrides, atur `type` ke `agent_with_overrides` dan teruskan `id` agen serta secara opsional `version` (hilangkan `version` untuk menggunakan versi terbaru agen). Kemudian sertakan salah satu dari `model`, `system`, `tools`, `mcp_servers`, atau `skills` dengan nilai yang harus digunakan sesi.

Setiap field yang dapat ditimpa mengikuti tiga aturan yang sama:

* **Hilangkan field:** Sesi mewarisi nilai dari versi agen yang direferensikannya.

* **Atur field ke `null`, atau ke array kosong untuk field berupa daftar:** Sesi berjalan dengan field tersebut dikosongkan. Aturan ini berlaku sepenuhnya untuk `system`, `mcp_servers`, dan `skills`. Ada dua pengecualian:

  * `model` tidak pernah dapat dikosongkan. Sebuah sesi selalu membutuhkan model, sehingga `model: null` mengembalikan error 400 `agent_model_required`.
  * Mengosongkan `tools` mengembalikan error 400 ketika `skills` efektif pada sesi tidak kosong, karena skills memerlukan alat `read`. Jika tidak, `tools: null` dan `tools: []` akan mengosongkan field tersebut.

* **Atur field ke sebuah nilai:** Nilai tersebut menggantikan nilai agen secara penuh. Overrides tidak pernah digabungkan dengan konfigurasi agen, sehingga override `tools` harus mencantumkan setiap alat yang harus dimiliki sesi.

Overrides hanya berlaku untuk sesi yang Anda buat. Overrides tidak memodifikasi sumber daya agen atau membuat versi agen baru, sehingga sesi lain yang mereferensikan agen yang sama tidak terpengaruh.

Dalam respons, objek `agent` mencerminkan konfigurasi yang dijalankan sesi setelah overrides diterapkan. `id` dan `version`-nya tetap mengidentifikasi agen dan versi tempat overrides diterapkan. Ini memungkinkan Anda melacak sesi kembali ke agen dasarnya.

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
  # `agent` pada respons adalah snapshot yang telah di-resolve: setiap override mengganti field
  # itu hanya untuk sesi ini, dan resource agent mempertahankan id serta versinya.
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
</CodeGroup>

<Tip>
  Agen mendefinisikan bagaimana Claude berperilaku di dalam sesi, termasuk model, prompt sistem, alat, dan server MCP. Lihat [Mendefinisikan agen Anda](/docs/id/managed-agents/agent-setup) untuk detailnya.
</Tip>

## Autentikasi MCP melalui vault

Jika agen Anda menggunakan alat MCP yang memerlukan autentikasi, teruskan `vault_ids` saat pembuatan sesi untuk mereferensikan vault yang berisi kredensial OAuth yang tersimpan. Anthropic mengelola penyegaran token atas nama Anda. Lihat [Autentikasi dengan vault](/docs/id/managed-agents/vaults) untuk cara membuat vault dan mendaftarkan kredensial.

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

Membuat sesi akan menyediakan sandbox lingkungan tetapi tidak memulai pekerjaan apa pun. Untuk mendelegasikan tugas, kirim event ke sesi menggunakan [user event](/docs/id/managed-agents/reference#event-types). Sesi bertindak sebagai "state machine" (mesin status) yang melacak kemajuan sementara event menggerakkan eksekusi sebenarnya.

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

Lihat [Status sesi](/docs/id/managed-agents/session-operations#session-statuses) untuk status-status yang dilalui sebuah sesi, dan [Operasi sesi](/docs/id/managed-agents/session-operations) untuk mengambil, mencantumkan, memperbarui, mengarsipkan, dan menghapus sesi.

Untuk membuat sesi secara otomatis pada jadwal berulang, lihat [Deployment terjadwal](/docs/id/managed-agents/scheduled-deployments).
