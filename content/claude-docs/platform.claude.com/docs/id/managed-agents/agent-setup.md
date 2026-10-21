---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/agent-setup
fetched_at: 2026-10-21T02:21:05.363362Z
sha256: c8bfd8cdb1522195c166867fe770627c95357b9c7d8937a2af774de17678f477
---

---
title: Definisikan agen Anda
url: https://platform.claude.com/docs/id/managed-agents/agent-setup
description: Buat konfigurasi agen yang dapat digunakan ulang dan memiliki versi.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Agen adalah konfigurasi yang dapat digunakan ulang dan memiliki versi yang mendefinisikan persona dan kemampuan. Agen menggabungkan model, prompt sistem, alat, server MCP, dan skill yang membentuk perilaku Claude selama sesi.

Buat agen sekali sebagai sumber daya yang dapat digunakan ulang dan rujuk agen tersebut berdasarkan ID setiap kali Anda [memulai sesi](https://platform.claude.com/docs/id/managed-agents/sessions). Agen memiliki versi dan lebih mudah dikelola di banyak sesi.

## Bidang konfigurasi agen

| Bidang                                                                          | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name` (csharp, go: `Name`)                                                     | Wajib. Nama agen yang mudah dibaca manusia.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `model` (csharp, go: `Model`)                                                   | Wajib. [Model](https://platform.claude.com/docs/id/models/overview) Claude yang menjalankan agen. Menerima string ID model atau objek, misalnya `{"id": "claude-opus-5-5"}`. Model Claude 4.5 dan yang lebih baru didukung. Bentuk objek juga menerima bidang `speed`, `effort`, dan `inference_geo`; lihat tips di bawah [Buat agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#create-an-agent), [Tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort#effort-levels), dan [Sematkan geo inferensi](https://platform.claude.com/docs/id/managed-agents/agent-setup#pin-the-inference-geo). |
| `system` (csharp, go: `System`; ruby: `system_`)                                | "System prompt" (prompt sistem) yang [mendefinisikan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role) perilaku dan persona agen. Prompt sistem berbeda dari [pesan pengguna](https://platform.claude.com/docs/id/managed-agents/reference#event-types), yang seharusnya menjelaskan pekerjaan yang harus dilakukan.                                                                                                                                                                                                                                         |
| `tools` (csharp, go: `Tools`)                                                   | Alat yang tersedia untuk agen. Menggabungkan [alat agen bawaan](https://platform.claude.com/docs/id/managed-agents/tools), [alat MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector), dan [alat kustom](https://platform.claude.com/docs/id/managed-agents/tools#custom-tools).                                                                                                                                                                                                                                                                                                                                       |
| `mcp_servers` (java, php: `mcpServers`; csharp: `McpServers`; go: `MCPServers`) | [Server MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) yang menyediakan kemampuan pihak ketiga yang terstandar.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `skills` (csharp, go: `Skills`)                                                 | [Skill](https://platform.claude.com/docs/id/managed-agents/skills) yang menyediakan konteks khusus domain dengan pengungkapan progresif.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `multiagent` (csharp, go: `Multiagent`)                                         | Memungkinkan agen menyerahkan pekerjaan ke agen lain, sebagai subagen atau dalam [alur kerja dinamis](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#dynamic-workflows), dan secara opsional berkonsultasi dengan model [penasihat](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor). Dengan tipe `multiagent_20261001`, alur kerja dinamis aktif kecuali Anda menonaktifkannya. Lihat [Orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration).                                                         |
| `description` (csharp, go: `Description`)                                       | Deskripsi tentang apa yang dilakukan agen.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `metadata` (csharp, go: `Metadata`)                                             | Pasangan kunci-nilai bebas untuk pelacakan Anda sendiri.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

Anda juga dapat menimpa `model` (csharp, go: `Model`), `system` (csharp, go: `System`; ruby: `system_`), `tools` (csharp, go: `Tools`), `mcp_servers` (java, php: `mcpServers`; csharp: `McpServers`; go: `MCPServers`), dan `skills` (csharp, go: `Skills`) untuk satu sesi tanpa mengubah agen. Penimpaan `model` (csharp, go: `Model`) menggantikan objek `model` (csharp, go: `Model`) milik agen secara penuh, sehingga `effort` (csharp, go: `Effort`) milik agen sendiri tidak terbawa. Untuk menjalankan sesi pada tingkat effort tertentu, atur `effort` (csharp, go: `Effort`) di dalam objek `model` (csharp, go: `Model`) penimpaan tersebut. Lihat [Menimpa konfigurasi agen untuk sesi](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session).

## Buat agen

Contoh berikut mendefinisikan agen coding yang menggunakan model Claude Opus terbaru dengan akses ke toolset agen bawaan. Toolset ini memungkinkan agen menulis kode, membaca file, mencari di web, dan lainnya. Lihat [referensi alat agen](https://platform.claude.com/docs/id/managed-agents/tools) untuk daftar lengkap alat yang didukung.

Contoh-contoh ini menggunakan curl, CLI `ant`, atau salah satu SDK. Jika Anda belum menyiapkannya, [quickstart](https://platform.claude.com/docs/id/managed-agents/quickstart#install-the-cli) membahas instalasi dan penyiapan klien.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Coding Assistant",
      "model": "claude-opus-5-5",
      "system": "You are a helpful coding agent.",
      "tools": [{"type": "agent_toolset_20260401"}]
    }'
  ```

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

      You are a helpful coding agent.
      ```
    </File>

    [`ant apply`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply) membuat agen dari `coding-assistant.md`, mencetak ID-nya, dan mencatatnya di `claude-lock.json`. Commit `claude-lock.json` agar `ant apply` berikutnya memperbarui agen ini alih-alih membuat agen kedua.
  </CodeGroupItem>

  ```python Python
  agent = client.beta.agents.create(
      name="Coding Assistant",
      model="claude-opus-5-5",
      system="You are a helpful coding agent.",
      tools=[
          {"type": "agent_toolset_20260401"},
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Coding Assistant",
    model: "claude-opus-5-5",
    system: "You are a helpful coding agent.",
    tools: [{ type: "agent_toolset_20260401" }]
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = BetaManagedAgentsModel.ClaudeOpus5_5,
      System = "You are a helpful coding agent.",
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Coding Assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5_5,
  	},
  	System: anthropic.String("You are a helpful coding agent."),
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Coding Assistant")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5_5)
          .system("You are a helpful coding agent.")
          .addTool(
              BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Coding Assistant',
      model: 'claude-opus-5-5',
      system: 'You are a helpful coding agent.',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Coding Assistant",
    model: "claude-opus-5-5",
    system_: "You are a helpful coding agent.",
    tools: [{type: "agent_toolset_20260401"}]
  )
  ```
</CodeGroup>

Respons menggemakan konfigurasi Anda dan menambahkan bidang `id`, `type`, `version`, `created_at`, `updated_at`, dan `archived_at`, serta mengisi bidang `model` yang Anda hilangkan, seperti `effort`, dengan nilai default-nya. `version` dimulai dari 1 dan bertambah setiap kali pembaruan mengubah agen.

```json
{
  "id": "agent_01HqR2k7vXbZ9mNpL3wYcT8f",
  "type": "agent",
  "name": "Coding Assistant",
  "model": {
    "id": "claude-opus-5-5",
    "effort": { "type": "medium" },
    "speed": "standard"
  },
  "system": "You are a helpful coding agent.",
  "description": null,
  "tools": [
    {
      "type": "agent_toolset_20260401",
      "default_config": {
        "permission_policy": { "type": "always_allow" }
      }
    }
  ],
  "skills": [],
  "mcp_servers": [],
  "multiagent": null,
  "metadata": {},
  "version": 1,
  "created_at": "2026-04-03T18:24:10.412Z",
  "updated_at": "2026-04-03T18:24:10.412Z",
  "archived_at": null
}
```

`default_config` pada toolset menunjukkan [kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) default-nya, `always_allow`, yang berlaku kecuali Anda mengonfigurasinya.

<Tip>
  Untuk menggunakan Claude Opus 5.5, Claude Opus 5, atau Claude Opus 4.8 dengan [mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode), berikan `model` sebagai objek, misalnya: `{"id": "claude-opus-5-5", "speed": "fast"}`. Lihat [model yang didukung](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models) di halaman mode cepat.
</Tip>

<Tip>
  Untuk mengatur tingkat effort model, berikan `model` sebagai objek, misalnya: `{"id": "claude-opus-5-5", "effort": "high"}`. Bidang `effort` menerima string tingkat (`low`, `medium`, `high`, `xhigh`, atau `max`) atau objek seperti `{"type": "high"}`. Lihat [Tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort#effort-levels) untuk mengetahui fungsi setiap tingkat.
</Tip>

### Sematkan geo inferensi

Seperti `speed` (csharp, go: `Speed`) dan `effort` (csharp, go: `Effort`), `inference_geo` (java, php: `inferenceGeo`; csharp, go: `InferenceGeo`) diatur melalui bentuk objek dari `model` (csharp, go: `Model`): berikan `model` (csharp, go: `Model`) sebagai objek dan atur `inference_geo` (java, php: `inferenceGeo`; csharp, go: `InferenceGeo`) bersama `id` (csharp, go: `ID`). Bidang ini menerima `"us"` atau `"global"`. Jika tidak diatur, setiap permintaan model mengikuti geo inferensi default workspace pada saat permintaan dilayani. Lihat [Residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency) untuk kontrol geo tingkat workspace dan harga.

Contoh berikut menyematkan agen ke inferensi AS. Respons membawa nilai `inference_geo` (java, php: `inferenceGeo`; csharp, go: `InferenceGeo`) di dalam objek `model` (csharp, go: `Model`) milik agen:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Geo-pinned assistant",
      "model": {"id": "claude-opus-5-5", "inference_geo": "us"},
      "system": "You are a helpful assistant."
    }'
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply geo-pinned-assistant.md
    ```

    <File filename="geo-pinned-assistant.md">
      ```markdown
      ---
      name: Geo-pinned assistant
      model:
        id: claude-opus-5-5
        inference_geo: us
      ---

      You are a helpful assistant.
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  agent = client.beta.agents.create(
      name="Geo-pinned assistant",
      model={
          "id": "claude-opus-5-5",
          "inference_geo": "us",
      },
      system="You are a helpful assistant.",
  )

  print(f"Inference geo: {agent.model.inference_geo}")
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Geo-pinned assistant",
    model: { id: "claude-opus-5-5", inference_geo: "us" },
    system: "You are a helpful assistant."
  });

  console.log(`Inference geo: ${agent.model.inference_geo}`);
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Geo-pinned assistant",
      Model = new BetaManagedAgentsModelConfigParams
      {
          ID = BetaManagedAgentsModel.ClaudeOpus5_5,
          InferenceGeo = "us",
      },
      System = "You are a helpful assistant.",
  });

  Console.WriteLine($"Inference geo: {agent.Model.InferenceGeo}");
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Geo-pinned assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID:           anthropic.BetaManagedAgentsModelClaudeOpus5_5,
  		InferenceGeo: anthropic.String("us"),
  	},
  	System: anthropic.String("You are a helpful assistant."),
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("Inference geo: %s\n", agent.Model.InferenceGeo)
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Geo-pinned assistant")
          .model(
              BetaManagedAgentsModelConfigParams.builder()
                  .id(BetaManagedAgentsModel.CLAUDE_OPUS_5_5)
                  .inferenceGeo("us")
                  .build()
          )
          .system("You are a helpful assistant.")
          .build()
  );

  IO.println("Inference geo: " + agent.model().inferenceGeo().orElseThrow());
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Geo-pinned assistant',
      model: BetaManagedAgentsModelConfigParams::with(
          id: 'claude-opus-5-5',
          inferenceGeo: 'us',
      ),
      system: 'You are a helpful assistant.',
  );

  echo "Inference geo: {$agent->model->inferenceGeo}\n";
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Geo-pinned assistant",
    model: {id: "claude-opus-5-5", inference_geo: "us"},
    system_: "You are a helpful assistant."
  )

  puts "Inference geo: #{agent.model.inference_geo}"
  ```
</CodeGroup>

Penyematan `inference_geo` (java, php: `inferenceGeo`; csharp, go: `InferenceGeo`) divalidasi terhadap [`allowed_inference_geos`](https://platform.claude.com/docs/id/manage-claude/data-residency#workspace-level-restrictions) milik workspace saat agen disimpan, saat sesi dibuat darinya, dan pada setiap giliran yang dilayani sesi. Jika daftar izin workspace dipersempit sehingga suatu penyematan tidak lagi diizinkan, sesi baru tidak dapat dibuat dari agen tersebut dan sesi yang sedang berjalan menolak giliran berikutnya; penyematan tidak pernah dikecualikan, karena workspace mengandalkannya untuk kepatuhan dan residensi data.

Mengatur `inference_geo` (java, php: `inferenceGeo`; csharp, go: `InferenceGeo`) pada model yang tidak mendukung penyematan inferensi geografis akan mengembalikan error 400; lihat [Ketersediaan model](https://platform.claude.com/docs/id/manage-claude/data-residency#model-availability) untuk model yang mendukungnya. Dalam konfigurasi `multiagent` (csharp, go: `Multiagent`), penyematan agen dan penyematan setiap agen yang tercantum dalam daftar `predefined_agents` (java, php: `predefinedAgents`; csharp, go: `PredefinedAgents`) dari `subagents` (csharp, go: `Subagents`) atau `workflows` (csharp, go: `Workflows`) harus semuanya diatur ke nilai yang sama atau semuanya tidak diatur; lihat [Orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration). Untuk mengubah atau menghapus penyematan nanti, perbarui objek `model` (csharp, go: `Model`) milik agen; memberikan `model` (csharp, go: `Model`) tanpa `inference_geo` (java, php: `inferenceGeo`; csharp, go: `InferenceGeo`) akan menghapusnya, seperti dijelaskan di bawah [Semantik pembaruan](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-semantics).

## Perbarui agen

Memperbarui agen menghasilkan versi baru ketika konfigurasi berubah. Bidang `version` (csharp, go: `Version`) bersifat opsional: berikan untuk konkurensi optimistis (ketidakcocokan mengembalikan 409), atau hilangkan untuk menerapkan pembaruan tanpa syarat (penulisan terakhir yang menang). Pembaruan pada agen yang diarsipkan akan ditolak.

Dengan CLI, edit file agen dan jalankan `ant apply` lagi; apply memberikan `version` untuk Anda.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "version": '"$AGENT_VERSION"',
      "system": "You are a helpful coding agent. Always write tests."
    }'
  ```

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

      You are a helpful coding agent. Always write tests.
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  updated_agent = client.beta.agents.update(
      agent.id,
      version=agent.version,
      system="You are a helpful coding agent. Always write tests.",
  )

  print(f"New version: {updated_agent.version}")
  ```

  ```typescript TypeScript
  const updatedAgent = await client.beta.agents.update(agent.id, {
    version: agent.version,
    system: "You are a helpful coding agent. Always write tests."
  });

  console.log(`New version: ${updatedAgent.version}`);
  ```

  ```csharp C#
  var updatedAgent = await client.Beta.Agents.Update(agent.ID, new()
  {
      Version = agent.Version,
      System = "You are a helpful coding agent. Always write tests.",
  });

  Console.WriteLine($"New version: {updatedAgent.Version}");
  ```

  ```go Go
  updatedAgent, err := client.Beta.Agents.Update(ctx, agent.ID, anthropic.BetaAgentUpdateParams{
  	Version: anthropic.Int(agent.Version),
  	System:  anthropic.String("You are a helpful coding agent. Always write tests."),
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("New version: %d\n", updatedAgent.Version)
  ```

  ```java Java
  var updatedAgent = client.beta().agents().update(
      agent.id(),
      AgentUpdateParams.builder()
          .version(agent.version())
          .system("You are a helpful coding agent. Always write tests.")
          .build()
  );

  IO.println("New version: " + updatedAgent.version());
  ```

  ```php PHP
  $updatedAgent = $client->beta->agents->update(
      $agent->id,
      version: $agent->version,
      system: 'You are a helpful coding agent. Always write tests.',
  );

  echo "New version: {$updatedAgent->version}\n";
  ```

  ```ruby Ruby
  updated_agent = client.beta.agents.update(
    agent.id,
    version: agent.version,
    system_: "You are a helpful coding agent. Always write tests."
  )

  puts "New version: #{updated_agent.version}"
  ```
</CodeGroup>

Contoh sebelumnya memberikan `version` dari respons pembuatan, sehingga pembaruan hanya diterapkan jika tidak ada hal lain yang mengubah agen sejak Anda membacanya. Untuk menerapkan pembaruan tanpa syarat, hilangkan `version` dari permintaan:

<CodeGroup>
  ```bash cURL
  curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "description": "Writes and reviews code."
    }'
  ```

  ```bash CLI
  ant beta:agents update \
    --agent-id "$AGENT_ID" \
    --description "Writes and reviews code."
  ```

  ```python Python
  unconditional_agent = client.beta.agents.update(
      agent.id,
      description="Writes and reviews code.",
  )

  print(f"New version: {unconditional_agent.version}")
  ```

  ```typescript TypeScript
  const unconditionalAgent = await client.beta.agents.update(agent.id, {
    description: "Writes and reviews code."
  });

  console.log(`New version: ${unconditionalAgent.version}`);
  ```

  ```csharp C#
  var unconditionalAgent = await client.Beta.Agents.Update(agent.ID, new()
  {
      Description = "Writes and reviews code.",
  });

  Console.WriteLine($"New version: {unconditionalAgent.Version}");
  ```

  ```go Go
  unconditionalAgent, err := client.Beta.Agents.Update(ctx, agent.ID, anthropic.BetaAgentUpdateParams{
  	Description: anthropic.String("Writes and reviews code."),
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("New version: %d\n", unconditionalAgent.Version)
  ```

  ```java Java
  var unconditionalAgent = client.beta().agents().update(
      agent.id(),
      AgentUpdateParams.builder()
          .description("Writes and reviews code.")
          .build()
  );

  IO.println("New version: " + unconditionalAgent.version());
  ```

  ```php PHP
  $unconditionalAgent = $client->beta->agents->update(
      $agent->id,
      description: 'Writes and reviews code.',
  );

  echo "New version: {$unconditionalAgent->version}\n";
  ```

  ```ruby Ruby
  unconditional_agent = client.beta.agents.update(
    agent.id,
    description: "Writes and reviews code."
  )

  puts "New version: #{unconditional_agent.version}"
  ```
</CodeGroup>

### Semantik pembaruan

* **`version` (csharp, go: `Version`)** bersifat opsional dan harus minimal 1 jika diberikan. Jika diberikan, permintaan mengembalikan 409 jika tidak cocok dengan versi agen saat ini, bahkan ketika bidang yang Anda kirim sudah cocok dengan nilai yang tersimpan; baca ulang agen dan coba lagi. Jika dihilangkan, pembaruan diterapkan tanpa syarat dan pembaruan terbaru secara diam-diam menggantikan pembaruan bersamaan lainnya, tanpa error bagi pemanggil mana pun. Memberikan `version` (csharp, go: `Version`) adalah default yang direkomendasikan untuk pemanggil interaktif, dan menghilangkannya cocok untuk loop apply deklaratif, seperti job CI yang menyinkronkan definisi agen yang di-check-in, di mana loop tersebut memiliki agen.

* **Bidang yang dihilangkan dipertahankan.** Anda hanya perlu menyertakan bidang yang ingin Anda ubah.

* **Bidang skalar** (`model` (csharp, go: `Model`), `system` (csharp, go: `System`; ruby: `system_`), `name` (csharp, go: `Name`), `description` (csharp, go: `Description`)) diganti dengan nilai baru. `system` (csharp, go: `System`; ruby: `system_`) dan `description` (csharp, go: `Description`) dapat dihapus dengan memberikan `null` (python: `None`; ruby: `nil`; java: `Optional.empty()`; go: `param.Null[string]()`; php: `requestOptions: ['extraBodyParams' => ['system' => null, 'description' => null]]`). `model` (csharp, go: `Model`) dan `name` (csharp, go: `Name`) bersifat wajib dan tidak dapat dihapus. Di dalam objek `model` (csharp, go: `Model`) yang Anda berikan, `effort` (csharp, go: `Effort`) adalah satu-satunya pengecualian: jika `id` (csharp, go: `ID`) model tidak berubah, menghilangkan `effort` (csharp, go: `Effort`) membuat tingkat effort yang tersimpan tidak berubah. Jika Anda mengubah `id` (csharp, go: `ID`) model, `effort` (csharp, go: `Effort`) yang dihilangkan akan direset ke default model baru. Bidang `model` (csharp, go: `Model`) lainnya diganti bersama objeknya: memberikan `model` (csharp, go: `Model`) tanpa `inference_geo` (java, php: `inferenceGeo`; csharp, go: `InferenceGeo`) akan menghapus penyematan geo inferensi agen.

* **Bidang array** (`tools` (csharp, go: `Tools`), `mcp_servers` (java, php: `mcpServers`; csharp: `McpServers`; go: `MCPServers`), `skills` (csharp, go: `Skills`)) sepenuhnya diganti oleh array baru. Untuk menghapus bidang array sepenuhnya, berikan `null` (python: `None`; ruby: `nil`; java: `Optional.empty()`; go: `param.NullSlice[[]anthropic.BetaAgentUpdateParamsToolUnion]()`; php: `requestOptions: ['extraBodyParams' => ['mcp_servers' => null]]`) atau array kosong.

* **`multiagent` (csharp, go: `Multiagent`)** digabungkan ke dalam blok yang tersimpan tingkat demi tingkat ketika pembaruan mempertahankan tipe `multiagent_20261001`. Pengaturan yang Anda hilangkan mempertahankan nilai tersimpannya, dan daftar `predefined_agents` (java, php: `predefinedAgents`; csharp, go: `PredefinedAgents`) yang Anda kirim menggantikan daftar yang tersimpan. Pembaruan lain apa pun yang mengirim `multiagent` (csharp, go: `Multiagent`) menggantikan blok yang tersimpan secara keseluruhan, dan pengaturan yang dihilangkannya mengambil nilai default. Berikan `"multiagent": null` (python: `multiagent=None`; typescript: `multiagent: null`; ruby: `multiagent: nil`; go: `Multiagent: param.NullStruct[anthropic.BetaManagedAgentsMultiagentParamsUnion]()`; java: `.multiagent(Optional.empty())`; csharp: `Multiagent = null`; php: `requestOptions: ['extraBodyParams' => ['multiagent' => null]]`) untuk menghapus seluruh blok. Di dalam blok, `null` mereset pengaturan ke default-nya, sehingga mengatur `workflows` (csharp, go: `Workflows`) ke `null` akan mengaktifkan alur kerja dinamis. Lihat [Aktifkan alur kerja dinamis](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#turn-on-dynamic-workflows).

* **Metadata** digabungkan pada tingkat kunci. Kunci yang Anda berikan ditambahkan atau diperbarui. Kunci yang Anda hilangkan dipertahankan. Untuk menghapus kunci tertentu, atur nilainya ke `null`.

* **Deteksi no-op.** Jika pembaruan tidak menghasilkan perubahan relatif terhadap versi saat ini, tidak ada versi baru yang dibuat dan versi yang ada dikembalikan.

* **Daftar `predefined_agents` (java, php: `predefinedAgents`; csharp, go: `PredefinedAgents`) milik agen lain tidak diperbarui.** Agen yang mencantumkan agen ini dalam daftar `predefined_agents` (java, php: `predefinedAgents`; csharp, go: `PredefinedAgents`) dari `subagents` (csharp, go: `Subagents`) atau `workflows` (csharp, go: `Workflows`) mempertahankan versi yang disematkan saat agen tersebut dibuat atau saat pembaruan terakhir mengirim daftar itu, bahkan jika referensinya menghilangkan `version` (csharp, go: `Version`). Untuk mendelegasikan ke versi baru, [perbarui agen yang mencantumkannya](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#list-the-subagents) sehingga daftar tersebut merujuk ke versi baru.

Pembaruan berikut menghapus deskripsi, menghapus kunci `team` dari `metadata` (csharp, go: `Metadata`), dan mengatur `workflows` (csharp, go: `Workflows`) ke `null`, yang mengaktifkan alur kerja dinamis:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "description": null,
      "metadata": {"team": null},
      "multiagent": {"type": "multiagent_20261001", "workflows": null}
    }'
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply code-reviewer.md
    ```

    <File filename="code-reviewer.md">
      ```markdown
      ---
      name: Code Reviewer
      model: claude-opus-5-5
      tools:
        - type: agent_toolset_20260401
      metadata:
        owner: docs
      multiagent:
        type: multiagent_20261001
        workflows: null
      ---

      You are a helpful coding agent.
      ```
    </File>

    File tersebut tidak lagi memiliki `description` atau kunci `team`, sehingga `ant apply` mengirim `null` untuk keduanya. Menghapus pengaturan di dalam `multiagent` mempertahankan nilai tersimpannya, sehingga file tersebut mengatur `workflows` ke `null`.
  </CodeGroupItem>

  ```python Python
  cleared_agent = client.beta.agents.update(
      agent.id,
      description=None,
      metadata={"team": None},
      multiagent={"type": "multiagent_20261001", "workflows": None},
  )

  print(f"Description: {cleared_agent.description}")
  ```

  ```typescript TypeScript
  const clearedAgent = await client.beta.agents.update(agent.id, {
    description: null,
    metadata: { team: null },
    multiagent: { type: "multiagent_20261001", workflows: null }
  });

  console.log(`Description: ${clearedAgent.description}`);
  ```

  ```csharp C#
  var clearedAgent = await client.Beta.Agents.Update(agent.ID, new()
  {
      Description = null,
      Metadata = new Dictionary<string, string?> { ["team"] = null },
      Multiagent = new BetaManagedAgentsMultiagent20261001Params { Workflows = null },
  });

  Console.WriteLine($"Description: {clearedAgent.Description}");
  ```

  ```go Go
  // Metadata adalah map[string]string, jadi kirim null untuk team sebagai opsi request.
  clearedAgent, err := client.Beta.Agents.Update(ctx, agent.ID, anthropic.BetaAgentUpdateParams{
  	Description: param.Null[string](),
  	Multiagent: anthropic.BetaManagedAgentsMultiagentParamsUnion{
  		OfMultiagent20261001: &anthropic.BetaManagedAgentsMultiagent20261001Params{
  			Workflows: param.NullStruct[anthropic.BetaManagedAgentsMultiagentWorkflowsParamsUnion](),
  		},
  	},
  }, option.WithJSONSet("metadata.team", nil))
  if err != nil {
  	panic(err)
  }

  fmt.Printf("Description: %q\n", clearedAgent.Description)
  ```

  ```java Java
  var clearedAgent = client.beta().agents().update(
      agent.id(),
      AgentUpdateParams.builder()
          .description(Optional.empty())
          .metadata(
              AgentUpdateParams.Metadata.builder()
                  .putAdditionalProperty("team", JsonValue.from(null))
                  .build()
          )
          .multiagent(
              BetaManagedAgentsMultiagent20261001Params.builder()
                  .workflows(Optional.empty())
                  .build()
          )
          .build()
  );

  IO.println("Description: " + clearedAgent.description().orElse(null));
  ```

  ```php PHP
  // update() membuang argumen null, jadi teruskan nilai null di extraBodyParams.
  $clearedAgent = $client->beta->agents->update(
      $agent->id,
      requestOptions: [
          'extraBodyParams' => [
              'description' => null,
              'metadata' => ['team' => null],
              'multiagent' => ['type' => 'multiagent_20261001', 'workflows' => null],
          ],
      ],
  );

  echo 'Description: ' . json_encode($clearedAgent->description) . "\n";
  ```

  ```ruby Ruby
  cleared_agent = client.beta.agents.update(
    agent.id,
    description: nil,
    metadata: {team: nil},
    multiagent: {type: :multiagent_20261001, workflows: nil}
  )

  puts "Description: #{cleared_agent.description.inspect}"
  ```
</CodeGroup>

## Siklus hidup agen

| Operasi           | Perilaku                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------- |
| **Update**        | Menghasilkan versi agen baru ketika konfigurasi berubah.                                                |
| **List versions** | Mengembalikan riwayat versi lengkap sehingga Anda dapat melacak perubahan dari waktu ke waktu.          |
| **Archive**       | Membuat agen menjadi hanya-baca. Sesi baru tidak dapat merujuknya, tetapi sesi yang ada tetap berjalan. |

### Daftar versi

Ambil riwayat versi lengkap untuk melacak bagaimana agen berubah dari waktu ke waktu. Hasil dipaginasi, dan contoh SDK mengambil setiap halaman secara otomatis.

<CodeGroup>
  ```bash cURL
  curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:agents:versions list --agent-id "$AGENT_ID"
  ```

  ```python Python
  for version in client.beta.agents.versions.list(agent.id):
      print(f"Version {version.version}: {version.updated_at.isoformat()}")
  ```

  ```typescript TypeScript
  for await (const version of client.beta.agents.versions.list(agent.id)) {
    console.log(`Version ${version.version}: ${version.updated_at}`);
  }
  ```

  ```csharp C#
  var versions = await client.Beta.Agents.Versions.List(agent.ID);
  await foreach (var version in versions.Paginate())
  {
      Console.WriteLine($"Version {version.Version}: {version.UpdatedAt:O}");
  }
  ```

  ```go Go
  iter := client.Beta.Agents.Versions.ListAutoPaging(ctx, agent.ID, anthropic.BetaAgentVersionListParams{})
  for iter.Next() {
  	version := iter.Current()
  	fmt.Printf("Version %d: %s\n", version.Version, version.UpdatedAt.Format(time.RFC3339))
  }
  if err := iter.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  for (var version : client.beta().agents().versions().list(agent.id()).autoPager()) {
      IO.println("Version " + version.version() + ": " + version.updatedAt());
  }
  ```

  ```php PHP
  foreach ($client->beta->agents->versions->list($agent->id)->pagingEachItem() as $version) {
      echo "Version {$version->version}: {$version->updatedAt->format(\DateTimeInterface::ATOM)}\n";
  }
  ```

  ```ruby Ruby
  client.beta.agents.versions.list(agent.id).auto_paging_each do |agent_version|
    puts "Version #{agent_version.version}: #{agent_version.updated_at.iso8601}"
  end
  ```
</CodeGroup>

### Arsipkan agen

Pengarsipan membuat agen menjadi hanya-baca dan tidak dapat dibatalkan. Sesi yang ada tetap berjalan, tetapi sesi baru tidak dapat merujuk agen tersebut. Respons mengatur `archived_at` (java, php: `archivedAt`; csharp, go: `ArchivedAt`) ke timestamp pengarsipan.

<CodeGroup>
  ```bash cURL
  curl -fsSL -X POST "https://api.anthropic.com/v1/agents/$AGENT_ID/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:agents archive --agent-id "$AGENT_ID"
  ```

  ```python Python
  archived = client.beta.agents.archive(agent.id)

  print(f"Archived at: {archived.archived_at.isoformat()}")
  ```

  ```typescript TypeScript
  const archived = await client.beta.agents.archive(agent.id);
  console.log(`Archived at: ${archived.archived_at}`);
  ```

  ```csharp C#
  var archived = await client.Beta.Agents.Archive(agent.ID);
  Console.WriteLine($"Archived at: {archived.ArchivedAt:O}");
  ```

  ```go Go
  archived, err := client.Beta.Agents.Archive(ctx, agent.ID, anthropic.BetaAgentArchiveParams{})
  if err != nil {
  	panic(err)
  }
  fmt.Printf("Archived at: %s\n", archived.ArchivedAt.Format(time.RFC3339))
  ```

  ```java Java
  var archived = client.beta().agents().archive(agent.id());
  IO.println("Archived at: " + archived.archivedAt().orElseThrow());
  ```

  ```php PHP
  $archived = $client->beta->agents->archive($agent->id);

  echo "Archived at: {$archived->archivedAt->format(\DateTimeInterface::ATOM)}\n";
  ```

  ```ruby Ruby
  archived = client.beta.agents.archive(agent.id)
  puts "Archived at: #{archived.archived_at.iso8601}"
  ```
</CodeGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Alat" icon="tool" href="https://platform.claude.com/docs/id/managed-agents/tools">
    Konfigurasikan alat yang tersedia untuk agen Anda.
  </Card>

  <Card title="Skill" icon="graduation-cap" href="https://platform.claude.com/docs/id/managed-agents/skills">
    Lampirkan keahlian berbasis sistem file yang dapat digunakan ulang ke agen Anda untuk alur kerja khusus domain.
  </Card>

  <Card title="Mulai sesi" icon="play" href="https://platform.claude.com/docs/id/managed-agents/sessions">
    Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.
  </Card>

  <Card title="Referensi" icon="book" href="https://platform.claude.com/docs/id/managed-agents/reference">
    Tipe event, flag CLI worker self-hosted, tipe server MCP yang didukung, batas laju, dan pedoman branding untuk Claude Managed Agents.
  </Card>
</CardGroup>
