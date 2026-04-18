---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/sessions
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 167cd8da777db8cadb9e49be0ab32f6608533c5207dcee8365fb3a50bac3a0a7
---

# Mulai sesi

Buat sesi untuk menjalankan agen Anda dan mulai menjalankan tugas.

---

Sesi adalah instans agen yang berjalan dalam lingkungan. Setiap sesi mereferensikan [agen](/docs/id/managed-agents/agent-setup) dan [lingkungan](/docs/id/managed-agents/environments) (keduanya dibuat secara terpisah), dan mempertahankan riwayat percakapan di seluruh interaksi ganda.

<Note>
Semua permintaan API Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

## Membuat sesi

Sesi memerlukan ID `agent` dan ID `environment`. Agen adalah sumber daya yang memiliki versi; melewatkan ID `agent` sebagai string memulai sesi dengan versi agen terbaru.

<CodeGroup>
  
  ```bash curl
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

Untuk mengikat sesi ke versi agen tertentu, lewatkan objek. Ini memungkinkan Anda mengontrol dengan tepat versi mana yang berjalan dan melakukan peluncuran versi baru secara independen.

<CodeGroup>
  
  ```bash curl
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
          Type = "agent",
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
    agent: {type: "agent", id: agent.id, version: 1},
    environment_id: environment.id
  )
  ```
</CodeGroup>

<Tip>
Agen mendefinisikan bagaimana Claude berperilaku dalam sesi, termasuk model, prompt sistem, alat, dan server MCP. Lihat [Pengaturan Agen](/docs/id/managed-agents/agent-setup) untuk detail.
</Tip>

## Autentikasi MCP melalui vault

Jika agen Anda menggunakan alat MCP yang memerlukan autentikasi, lewatkan `vault_ids` saat pembuatan sesi untuk mereferensikan vault yang berisi kredensial OAuth yang disimpan. Anthropic mengelola penyegaran token atas nama Anda. Lihat [Autentikasi dengan vault](/docs/id/managed-agents/vaults) untuk cara membuat vault dan mendaftarkan kredensial.

<CodeGroup>
  
  ```bash curl
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

Membuat sesi menyediakan lingkungan dan agen tetapi tidak memulai pekerjaan apa pun. Untuk mendelegasikan tugas, kirim peristiwa ke sesi menggunakan [peristiwa pengguna](/docs/id/managed-agents/events-and-streaming#user-events). Sesi bertindak sebagai mesin keadaan yang melacak kemajuan sementara peristiwa mendorong eksekusi sebenarnya.

<CodeGroup>
  
  ```bash curl
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
    --session-id "$SESSION_ID" \
 <<'YAML'
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
  		Events: []anthropic.SendEventsParamsUnion{{
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
        type: "user.message",
        content: [{type: "text", text: "List the files in the working directory."}]
      }
    ]
  )
  ```
</CodeGroup>

Lihat [Peristiwa dan streaming](/docs/id/managed-agents/events-and-streaming) untuk cara melakukan streaming respons agen dan menangani konfirmasi alat.

## Status sesi

Sesi berkembang melalui status ini:

| Status | Deskripsi |
|--------|-------------|
| `idle` | Agen menunggu input, termasuk pesan pengguna atau konfirmasi alat. Sesi dimulai dalam `idle`. |
| `running` | Agen sedang aktif mengeksekusi |
| `rescheduling` | Kesalahan transien terjadi, mencoba ulang secara otomatis |
| `terminated` | Sesi telah berakhir karena kesalahan yang tidak dapat dipulihkan |

## Operasi sesi lainnya

### Mengambil sesi

<CodeGroup>
  
  ```bash curl
  retrieved=$(curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")
  echo "Status: $(jq -r '.status' <<< "$retrieved")"
  ```
  
  ```bash CLI
  ant beta:sessions retrieve --session-id "$SESSION_ID"
  ```
  ```python Python
  retrieved = client.beta.sessions.retrieve(session.id)
  print(f"Status: {retrieved.status}")
  ```
  ```typescript TypeScript
  const retrieved = await client.beta.sessions.retrieve(session.id);
  console.log(`Status: ${retrieved.status}`);
  ```
  ```csharp C#
  var retrieved = await client.Beta.Sessions.Retrieve(session.ID);
  Console.WriteLine($"Status: {retrieved.Status.Raw()}");
  ```
  ```go Go
  	retrieved, err := client.Beta.Sessions.Get(ctx, session.ID, anthropic.BetaSessionGetParams{})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("Status: %s\n", retrieved.Status)
  ```
  ```java Java
      var retrieved = client.beta().sessions().retrieve(session.id());
      IO.println("Status: " + retrieved.status());
  ```
  ```php PHP
  $retrieved = $client->beta->sessions->retrieve($session->id);
  echo "Status: {$retrieved->status}\n";
  ```
  ```ruby Ruby
  retrieved = client.beta.sessions.retrieve(session.id)
  puts "Status: #{retrieved.status}"
  ```
</CodeGroup>

### Daftar sesi

<CodeGroup>
  ```bash curl
  curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    | jq -r '.data[] | "\(.id): \(.status)"'
  ```
  ```bash CLI
  ant beta:sessions list
  ```
  ```python Python
  for session in client.beta.sessions.list():
      print(f"{session.id}: {session.status}")
  ```
  ```typescript TypeScript
  for await (const session of client.beta.sessions.list()) {
    console.log(`${session.id}: ${session.status}`);
  }
  ```
  ```csharp C#
  var sessions = await client.Beta.Sessions.List();
  await foreach (var listedSession in sessions.Paginate())
  {
      Console.WriteLine($"{listedSession.ID}: {listedSession.Status.Raw()}");
  }
  ```
  ```go Go
  	page := client.Beta.Sessions.ListAutoPaging(ctx, anthropic.BetaSessionListParams{})
  	for page.Next() {
  		session := page.Current()
  		fmt.Printf("%s: %s\n", session.ID, session.Status)
  	}
  	if err := page.Err(); err != nil {
  		panic(err)
  	}
  ```
  ```java Java
      for (var listed : client.beta().sessions().list().autoPager()) {
          IO.println(listed.id() + ": " + listed.status());
      }
  ```
  ```php PHP
  foreach ($client->beta->sessions->list()->pagingEachItem() as $session) {
      echo "{$session->id}: {$session->status}\n";
  }
  ```
  ```ruby Ruby
  client.beta.sessions.list.auto_paging_each do |session|
    puts "#{session.id}: #{session.status}"
  end
  ```
</CodeGroup>

### Mengarsipkan sesi

Arsipkan sesi untuk mencegah peristiwa baru dikirim sambil mempertahankan riwayatnya:

<CodeGroup>
  
  ```bash curl
  curl -fsSL -X POST "https://api.anthropic.com/v1/sessions/$SESSION_ID/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```
  
  ```bash CLI
  ant beta:sessions archive \
    --session-id "$SESSION_ID"
  ```
  ```python Python
  client.beta.sessions.archive(session.id)
  ```
  ```typescript TypeScript
  await client.beta.sessions.archive(session.id);
  ```
  ```csharp C#
  await client.Beta.Sessions.Archive(session.ID);
  ```
  ```go Go
  	_, err = client.Beta.Sessions.Archive(ctx, session.ID, anthropic.BetaSessionArchiveParams{})
  	if err != nil {
  		panic(err)
  	}
  ```
  ```java Java
      client.beta().sessions().archive(session.id());
  ```
  ```php PHP
  $client->beta->sessions->archive($session->id);
  ```
  ```ruby Ruby
  client.beta.sessions.archive(session.id)
  ```
</CodeGroup>

### Menghapus sesi

Hapus sesi untuk menghapus secara permanen catatan, peristiwa, dan kontainer terkaitnya. Sesi `running` tidak dapat dihapus; kirim [peristiwa interrupt](/docs/id/managed-agents/events-and-streaming#user-events) jika Anda perlu menghapusnya segera.

File, penyimpanan memori, lingkungan, dan agen adalah sumber daya independen dan tidak terpengaruh oleh penghapusan sesi.

<CodeGroup>
  
  ```bash curl
  curl -fsSL -X DELETE "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```
  
  ```bash CLI
  ant beta:sessions delete \
    --session-id "$SESSION_ID"
  ```
  ```python Python
  client.beta.sessions.delete(session.id)
  ```
  ```typescript TypeScript
  await client.beta.sessions.delete(session.id);
  ```
  ```csharp C#
  await client.Beta.Sessions.Delete(session.ID);
  ```
  ```go Go
  	_, err = client.Beta.Sessions.Delete(ctx, session.ID, anthropic.BetaSessionDeleteParams{})
  	if err != nil {
  		panic(err)
  	}
  ```
  ```java Java
      client.beta().sessions().delete(session.id());
  ```
  ```php PHP
  $client->beta->sessions->delete($session->id);
  ```
  ```ruby Ruby
  client.beta.sessions.delete(session.id)
  ```
</CodeGroup>