---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/sessions
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: e8dc2618e6d6d1fdf568690506fafbd49d81788c254e0aaabef339e8cadb58f2
---

# Memulai sesi

Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.

---

Sesi adalah instans agen di dalam sebuah environment. Setiap sesi mereferensikan sebuah [agen](/docs/id/managed-agents/agent-setup) dan sebuah [environment](/docs/id/managed-agents/environments) (keduanya dibuat secara terpisah), dan mempertahankan riwayat percakapan di sepanjang beberapa interaksi. Sesi mengikuti siklus hidup dua langkah: pertama [buat sesi](#creating-a-session), lalu [kirim event pengguna](#starting-the-session) untuk memulai pekerjaan. Anda juga dapat menggabungkan kedua langkah tersebut menjadi satu panggilan dengan [`initial_events`](#seed-the-session-with-initial-events).

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Membuat sesi

Sebuah sesi memerlukan ID `agent` dan ID `environment`. Agen adalah sumber daya berversi; memasukkan ID `agent` sebagai string akan memulai sesi dengan versi agen terbaru.

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

Untuk menyematkan sesi ke versi agen tertentu, masukkan sebuah objek. Ini memungkinkan Anda mengontrol secara tepat versi mana yang berjalan dan melakukan rollout bertahap versi baru secara independen.

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

### Mengisi sesi dengan initial events

Anda dapat membuat sesi dan memulai pekerjaannya dalam satu panggilan. `initial_events` adalah array opsional berisi [event](/docs/id/managed-agents/reference#event-types) awal yang dikirim ke sesi saat pembuatan, diproses secara berurutan. Array ini mendukung event `user.message` dan [`user.define_outcome`](/docs/id/managed-agents/define-outcomes), dan menerima maksimum 50 event. Daftar yang tidak kosong akan memulai loop agen dalam panggilan yang sama: sesi dibuat langsung dalam status `running`, tanpa permintaan lebih lanjut.

Contoh berikut membuat sesi dengan satu `user.message` di dalam `initial_events`:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  seeded_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID",
    "initial_events": [
      {
        "type": "user.message",
        "content": [{"type": "text", "text": "List the files in the working directory."}]
      }
    ]
  }
  EOF
  )
  SEEDED_SESSION_ID=$(jq -r '.id' <<< "$seeded_session")

  # initial_events tidak ikut dikembalikan pada respons create; tampilkan daftar
  # event sesi untuk melihat pesan yang di-seed.
  seeded_events=$(curl -fsSL \
    "https://api.anthropic.com/v1/sessions/$SEEDED_SESSION_ID/events" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")
  echo "Seeded event: $(jq -r \
    '.data[] | select(.type == "user.message") | .content[0].text' <<< "$seeded_events")"
  ```

  ```bash CLI
  SEEDED_SESSION_ID=$(ant beta:sessions create \
    --transform id --raw-output <<YAML
  agent: $AGENT_ID
  environment_id: $ENVIRONMENT_ID
  initial_events:
    - type: user.message
      content:
        - type: text
          text: List the files in the working directory.
  YAML
  )

  # initial_events tidak ikut dikembalikan pada respons create; tampilkan daftar
  # event sesi untuk melihat pesan yang di-seed.
  echo "Seeded event: $(ant beta:sessions:events list \
    --session-id "$SEEDED_SESSION_ID" \
    --format raw \
    --transform 'data.#(type=="user.message").content.0.text' --raw-output)"
  ```

  ```python Python
  seeded_session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      initial_events=[
          {
              "type": "user.message",
              "content": [
                  {"type": "text", "text": "List the files in the working directory."}
              ],
          },
      ],
  )
  # initial_events tidak digemakan pada respons create; baca kembali
  # dari daftar event milik sesi.
  for event in client.beta.sessions.events.list(seeded_session.id):
      if event.type == "user.message":
          for block in event.content:
              if block.type == "text":
                  print(f"Seeded event: {block.text}")
  ```

  ```typescript TypeScript
  const seededSession = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    initial_events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "List the files in the working directory." }]
      }
    ]
  });

  // initial_events tidak digemakan pada respons create; daftarkan event
  // sesi untuk membaca kembali pesan yang di-seed.
  for await (const event of client.beta.sessions.events.list(seededSession.id)) {
    if (event.type === "user.message") {
      for (const block of event.content) {
        if (block.type === "text") {
          console.log(`Seeded event: ${block.text}`);
        }
      }
    }
  }
  ```

  ```csharp C#
  var seededSession = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      InitialEvents =
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
  // initial_events tidak digemakan pada respons create; baca kembali
  // dari daftar event sesi.
  var seededEvents = await client.Beta.Sessions.Events.List(seededSession.ID);
  await foreach (var sessionEvent in seededEvents.Paginate())
  {
      if (sessionEvent.TryPickUserMessage(out var userMessage))
      {
          foreach (var contentBlock in userMessage.Content)
          {
              if (contentBlock.TryPickBetaManagedAgentsTextBlock(out var textBlock))
              {
                  Console.WriteLine($"Seeded event: {textBlock.Text}");
              }
          }
      }
  }
  ```

  ```go Go
  seededSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	InitialEvents: []anthropic.BetaSessionNewParamsInitialEventUnion{{
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
  })
  if err != nil {
  	panic(err)
  }
  // initial_events tidak digaungkan pada respons create, jadi daftarkan
  // event sesi untuk membaca kembali user.message yang di-seed.
  seededEvents, err := client.Beta.Sessions.Events.List(ctx, seededSession.ID, anthropic.BetaSessionEventListParams{})
  if err != nil {
  	panic(err)
  }
  for _, event := range seededEvents.Data {
  	if event.Type != "user.message" {
  		continue
  	}
  	for _, contentBlock := range event.AsUserMessage().Content {
  		if contentBlock.Type == "text" {
  			fmt.Printf("Seeded event: %s\n", contentBlock.AsText().Text)
  		}
  	}
  }
  ```

  ```java Java
  var seededSession = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .addInitialEvent(BetaManagedAgentsUserMessageEventParams.builder()
          .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
          .addTextContent("List the files in the working directory.")
          .build())
      .build());
  // initial_events tidak digemakan pada respons create; daftarkan
  // event sesi untuk membaca kembali user.message yang di-seed.
  for (var event : client.beta().sessions().events().list(seededSession.id()).autoPager()) {
      if (event.isUserMessage()) {
          for (var contentBlock : event.asUserMessage().content()) {
              if (contentBlock.isText()) {
                  IO.println("Seeded event: " + contentBlock.asText().text());
              }
          }
      }
  }
  ```

  ```php PHP
  $seededSession = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      initialEvents: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => 'List the files in the working directory.']],
          ],
      ],
  );

  // initial_events tidak digemakan pada respons create; baca kembali
  // dari daftar event sesi.
  $seededEvents = $client->beta->sessions->events->list($seededSession->id);
  foreach ($seededEvents->getItems() as $event) {
      if ($event->type === 'user.message') {
          echo "Seeded event: {$event->content[0]->text}\n";
      }
  }
  ```

  ```ruby Ruby
  seeded_session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    initial_events: [
      {
        type: :"user.message",
        content: [{type: :text, text: "List the files in the working directory."}]
      }
    ]
  )

  # initial_events tidak digemakan pada respons create; baca kembali dari
  # daftar event milik sesi.
  client.beta.sessions.events.list(seeded_session.id).auto_paging_each do |event|
    next unless event.type == :"user.message"
    event.content.each do |block|
      puts "Seeded event: #{block.text}" if block.type == :text
    end
  end
  ```
</CodeGroup>

Tidak ada tipe event lain yang diterima. Event yang merespons giliran agen (`user.tool_confirmation`, `user.tool_result`, dan `user.custom_tool_result`) tidak diterima karena belum ada giliran agen, dan `user.interrupt` tidak diterima karena tidak ada giliran yang perlu dihentikan. Berbeda dengan `initial_events` pada scheduled deployment, `initial_events` milik sesi tidak menerima `system.message`.

Setiap event di dalam `initial_events` divalidasi dan disimpan sebelum respons pembuatan dikembalikan, sesuai urutan daftar, dengan ID yang ditetapkan oleh server, persis seolah-olah Anda mengirimkannya ke endpoint [kirim event](/docs/id/managed-agents/events-and-streaming) segera setelah pembuatan. Aturan konten per event juga sama dengan endpoint tersebut. Daftar kosong setara dengan menghilangkan field tersebut. Validasi bersifat semua-atau-tidak-sama-sekali: jika ada satu event yang gagal validasi, seluruh permintaan ditolak dan tidak ada sesi yang dibuat.

Permintaan pembuatan ditolak dalam kasus-kasus berikut:

| Kondisi                                                                                                                              | Status |
| ------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| Lebih dari satu event `user.define_outcome`                                                                                          | 400    |
| Event `user.define_outcome` tanpa `rubric`                                                                                           | 400    |
| Lebih dari 100 [blok konten `document`](/docs/id/build-with-claude/files#document-blocks) yang bersumber dari file di seluruh daftar | 400    |
| Body permintaan lebih dari 32 MB                                                                                                     | 413    |

Event `user.define_outcome` di dalam `initial_events` diterima dengan kondisi yang sama seperti mengirimkannya ke sesi yang sudah ada; lihat [Mendefinisikan outcome](/docs/id/managed-agents/define-outcomes).

### Menimpa konfigurasi agen untuk sebuah sesi

Anda dapat memasukkan `agent` dalam tiga bentuk: string ID agen, objek versi tersemat (`type: "agent"`), atau objek override. Bentuk override mengubah sebagian konfigurasi agen untuk satu sesi saja. Gunakan ini untuk mencoba model yang berbeda atau memberikan alat tambahan dalam satu sesi tanpa membuat versi baru agen. Untuk bentuk override, atur `type` ke `agent_with_overrides` dan masukkan `id` agen serta secara opsional `version` (hilangkan `version` untuk menggunakan versi terbaru agen). Kemudian sertakan salah satu dari `model`, `system`, `tools`, `mcp_servers`, atau `skills` dengan nilai yang harus digunakan sesi.

Setiap field yang dapat ditimpa mengikuti tiga aturan yang sama:

* **Hilangkan field:** Sesi mewarisi nilai dari versi agen yang direferensikannya.

* **Atur field ke `null`, atau ke array kosong untuk field berbentuk daftar:** Sesi berjalan dengan field tersebut dikosongkan. Aturan ini berlaku sepenuhnya untuk `system` dan `skills`. Ada tiga pengecualian:

  * `model` tidak pernah dapat dikosongkan. Sesi selalu memerlukan model, sehingga `model: null` mengembalikan error 400 `agent_model_required`.
  * Mengosongkan `tools` mengembalikan error 400 ketika `skills` efektif milik sesi tidak kosong, karena skills memerlukan alat `read`. Jika tidak, `tools: null` dan `tools: []` akan mengosongkan field tersebut.
  * Mengosongkan `mcp_servers` mengembalikan error 400 ketika `tools` efektif milik sesi masih berisi `mcp_toolset` yang mereferensikan salah satu server milik agen. Timpa `tools` dalam permintaan yang sama untuk menghapus entri `mcp_toolset` tersebut, lalu kosongkan `mcp_servers`.

* **Atur field ke sebuah nilai:** Nilai tersebut menggantikan nilai agen sepenuhnya. Override tidak pernah digabungkan dengan konfigurasi agen, sehingga override `tools` harus mencantumkan setiap alat yang harus dimiliki sesi. Ada satu pengecualian:
  * Level `effort` di dalam override `model` per sesi tidak diterapkan. Atur `effort` pada [agen](/docs/id/managed-agents/agent-setup#agent-configuration-fields) sebagai gantinya.

Override hanya berlaku untuk sesi yang Anda buat. Override tidak memodifikasi sumber daya agen atau membuat versi agen baru, sehingga sesi lain yang mereferensikan agen yang sama tidak terpengaruh.

Dalam respons, objek `agent` mencerminkan konfigurasi yang digunakan sesi setelah override diterapkan. `id` dan `version`-nya tetap mengidentifikasi agen dan versi tempat override diterapkan. Ini memungkinkan Anda melacak sesi kembali ke agen dasarnya.

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
  # `agent` pada respons adalah snapshot hasil resolusi: setiap override mengganti
  # field tersebut hanya untuk sesi ini, dan resource agen tetap menyimpan id dan versinya.
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
  # Agen pada respons adalah snapshot terselesaikan dengan override yang diterapkan.
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
  // Agen pada respons adalah snapshot terselesaikan dengan override yang diterapkan.
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
  // Agen pada respons adalah snapshot yang sudah diresolusi dengan override diterapkan.
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
  			// Kosongkan prompt sistem agen untuk sesi ini.
  			System: param.Null[string](),
  		},
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  // Agen pada respons adalah snapshot yang telah diselesaikan dengan override diterapkan.
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
  // Agen pada respons adalah snapshot terselesaikan dengan override diterapkan.
  IO.println("Model: " + overrideSession.agent().model().id());
  IO.println("System: " + overrideSession.agent().system().orElse("null"));
  ```

  ```php PHP
  $overrides = BetaManagedAgentsAgentWithOverridesParams::with(
      id: $agent->id,
      type: 'agent_with_overrides',
      model: ['id' => 'claude-sonnet-5'],
  );
  // Kosongkan prompt sistem untuk sesi ini. Akses array penting di sini:
  // create() membuang null dari array mentah dan ::with() memperlakukan argumen null sebagai dihilangkan.
  $overrides['system'] = null;

  $overrideSession = $client->beta->sessions->create(
      agent: $overrides,
      environmentID: $environment->id,
  );
  // Agen pada respons adalah snapshot terselesaikan dengan override yang diterapkan.
  echo "Model: {$overrideSession->agent->model->id}\n";
  echo 'System: ' . ($overrideSession->agent->system ?? 'null') . "\n";
  ```

  ```ruby Ruby
  # Override prompt sistem adalah `system_` (garis bawah di akhir) karena
  # `system` biasa adalah Kernel#system milik Ruby. Menyetelnya ke nil menghapus prompt.
  override_session = client.beta.sessions.create(
    agent: Anthropic::Beta::BetaManagedAgentsAgentWithOverridesParams.new(
      type: :agent_with_overrides,
      id: agent.id,
      model: {id: "claude-sonnet-5"},
      system_: nil
    ),
    environment_id: environment.id
  )
  # Agen pada respons adalah snapshot terselesaikan dengan override yang diterapkan.
  puts "Model: #{override_session.agent.model.id}"
  puts "System: #{override_session.agent.system_.inspect}"
  ```
</CodeGroup>

<Tip>
  Agen mendefinisikan bagaimana Claude berperilaku di dalam sesi, termasuk model, prompt sistem, alat, dan server MCP. Lihat [Definisikan agen Anda](/docs/id/managed-agents/agent-setup) untuk detailnya.
</Tip>

## Autentikasi MCP melalui vault

Jika agen Anda menggunakan alat MCP yang memerlukan autentikasi, masukkan `vault_ids` saat pembuatan sesi untuk mereferensikan vault yang berisi kredensial OAuth yang tersimpan. Anthropic mengelola pembaruan token atas nama Anda. Lihat [Autentikasi dengan vault](/docs/id/managed-agents/vaults) untuk cara membuat vault dan mendaftarkan kredensial.

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

Membuat sesi tanpa `initial_events` akan mendaftarkan sesi tetapi tidak memulai pekerjaan apa pun; sandbox milik environment disediakan ketika sesi pertama kali membutuhkannya. Untuk mendelegasikan tugas, kirim event ke sesi menggunakan [event pengguna](/docs/id/managed-agents/reference#event-types). Untuk menyediakan event pertama dalam permintaan pembuatan sebagai gantinya, lihat [Mengisi sesi dengan initial events](#seed-the-session-with-initial-events). Sesi bertindak sebagai state machine yang melacak kemajuan sementara event menggerakkan eksekusi yang sebenarnya.

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

Lihat [Stream event sesi](/docs/id/managed-agents/events-and-streaming) untuk cara melakukan streaming respons agen dan menangani konfirmasi alat.

Lihat [Status sesi](/docs/id/managed-agents/session-operations#session-statuses) untuk status-status yang dilalui sebuah sesi.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Operasi sesi" icon="settings" href="/docs/id/managed-agents/session-operations">
    Ambil, daftarkan, perbarui, arsipkan, dan hapus sesi Claude Managed Agents.
  </Card>

  <Card title="Stream event sesi" icon="lightning" href="/docs/id/managed-agents/events-and-streaming">
    Kirim event, lakukan streaming respons, dan interupsi atau alihkan sesi Anda di tengah eksekusi.
  </Card>

  <Card title="Scheduled deployments" icon="arrows-clockwise" href="/docs/id/managed-agents/scheduled-deployments">
    Buat dan kelola deployment dengan Claude API: jalankan agen pada jadwal cron berulang dan periksa riwayat eksekusinya.
  </Card>
</CardGroup>
