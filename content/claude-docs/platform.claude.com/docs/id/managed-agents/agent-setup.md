---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/agent-setup
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: f7ea17e03ab58de432c0ddf781a3c857962f75520724ae30023bdd88b9d6a596
---

---
title: Definisikan agen Anda
url: https://platform.claude.com/docs/id/managed-agents/agent-setup
description: Buat konfigurasi agen yang dapat digunakan kembali dan memiliki versi.
---

Agen adalah konfigurasi yang dapat digunakan kembali dan memiliki versi yang mendefinisikan persona dan kemampuan. Agen menggabungkan model, "system prompt" (prompt sistem), alat, server MCP, dan skill yang membentuk bagaimana Claude berperilaku selama sesi.

Buat agen sekali sebagai sumber daya yang dapat digunakan kembali dan referensikan berdasarkan ID setiap kali Anda [memulai sesi](https://platform.claude.com/docs/id/managed-agents/sessions). Agen memiliki versi dan lebih mudah dikelola di banyak sesi.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK menetapkan header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Field konfigurasi agen

| Field         | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | Wajib. Nama agen yang mudah dibaca manusia.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `model`       | Wajib. [Model](https://platform.claude.com/docs/id/models/overview) Claude yang menjalankan agen. Menerima string ID model atau objek, misalnya `{"id": "claude-opus-5"}`. Model Claude 4.5 dan yang lebih baru didukung. Bentuk objek juga menerima field `speed`, `effort`, dan `inference_geo`; lihat tips di bawah [Membuat agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#create-an-agent), [Tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort#effort-levels), dan [Menyematkan inference geo](https://platform.claude.com/docs/id/managed-agents/agent-setup#pin-the-inference-geo). |
| `system`      | [Prompt sistem](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role) yang mendefinisikan perilaku dan persona agen. Prompt sistem berbeda dari [pesan pengguna](https://platform.claude.com/docs/id/managed-agents/reference#event-types), yang seharusnya mendeskripsikan pekerjaan yang akan dilakukan.                                                                                                                                                                                                                                                           |
| `tools`       | Alat yang tersedia untuk agen. Menggabungkan [alat agen bawaan](https://platform.claude.com/docs/id/managed-agents/tools), [alat MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector), dan [alat kustom](https://platform.claude.com/docs/id/managed-agents/tools#custom-tools).                                                                                                                                                                                                                                                                                                                                          |
| `mcp_servers` | [Server MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) yang menyediakan kemampuan pihak ketiga yang terstandar.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `skills`      | [Skill](https://platform.claude.com/docs/id/managed-agents/skills) yang menyediakan konteks khusus domain dengan pengungkapan progresif.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `multiagent`  | Deklarasi koordinator yang mencantumkan agen-agen yang dapat didelegasikan oleh agen ini. Lihat [Orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration).                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `description` | Deskripsi tentang apa yang dilakukan agen.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `metadata`    | Pasangan key-value arbitrer untuk pelacakan Anda sendiri.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

Anda juga dapat menimpa `model`, `system`, `tools`, `mcp_servers`, dan `skills` untuk satu sesi tanpa mengubah agen. Tingkat `effort` yang ditetapkan di dalam penimpaan `model` per sesi tidak diterapkan, dan karena penimpaan tersebut menggantikan objek `model` agen secara penuh, sesi yang dibuat dengan penimpaan `model` berjalan pada tingkat effort default model; untuk berjalan pada tingkat effort tertentu, tetapkan `effort` pada agen dan jangan menimpa `model` untuk sesi tersebut. Lihat [Menimpa konfigurasi agen untuk sesi](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session).

## Membuat agen

Contoh berikut mendefinisikan agen coding yang menggunakan Claude Opus 5 dengan akses ke toolset agen bawaan. Toolset ini memungkinkan agen menulis kode, membaca file, mencari di web, dan lainnya. Lihat [referensi alat agen](https://platform.claude.com/docs/id/managed-agents/tools) untuk daftar lengkap alat yang didukung.

Contoh-contoh ini menggunakan curl, CLI `ant`, atau salah satu SDK. Jika Anda belum menyiapkannya, [quickstart](https://platform.claude.com/docs/id/managed-agents/quickstart#install-the-cli) mencakup instalasi dan penyiapan klien.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Coding Assistant",
      "model": "claude-opus-5",
      "system": "You are a helpful coding agent.",
      "tools": [{"type": "agent_toolset_20260401"}]
    }')

  AGENT_ID=$(jq -r '.id' <<< "$agent")
  AGENT_VERSION=$(jq -r '.version' <<< "$agent")
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    agent=$(ant beta:agents create --format json < coding-assistant.agent.yaml)

    AGENT_ID=$(jq -r '.id' <<< "$agent")
    ```

    <File filename="coding-assistant.agent.yaml">
      ```yaml
      name: Coding Assistant
      model:
        id: claude-opus-5
      system: You are a helpful coding agent.
      tools:
        - type: agent_toolset_20260401
      ```
    </File>
  </MultiFileExample>

  ```python Python
  agent = client.beta.agents.create(
      name="Coding Assistant",
      model="claude-opus-5",
      system="You are a helpful coding agent.",
      tools=[
          {"type": "agent_toolset_20260401"},
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Coding Assistant",
    model: "claude-opus-5",
    system: "You are a helpful coding agent.",
    tools: [{ type: "agent_toolset_20260401" }],
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = BetaManagedAgentsModel.ClaudeOpus5,
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
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5,
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
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
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
      model: 'claude-opus-5',
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
    model: "claude-opus-5",
    system_: "You are a helpful coding agent.",
    tools: [{type: "agent_toolset_20260401"}]
  )
  ```
</CodeGroup>

Respons menggemakan konfigurasi Anda dan menambahkan field `id`, `type`, `version`, `created_at`, `updated_at`, dan `archived_at`, serta mengisi field `model` yang Anda hilangkan, seperti `effort`, dengan nilai defaultnya. `version` dimulai dari 1 dan bertambah setiap kali pembaruan mengubah agen.

```json
{
  "id": "agent_01HqR2k7vXbZ9mNpL3wYcT8f",
  "type": "agent",
  "name": "Coding Assistant",
  "model": {
    "id": "claude-opus-5",
    "effort": { "type": "high" },
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

`default_config` pada toolset menunjukkan [kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) defaultnya, `always_allow`, yang berlaku kecuali Anda mengonfigurasinya.

<Tip>
  Untuk menggunakan Claude Opus 5 atau Claude Opus 4.8 dengan [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode), teruskan `model` sebagai objek, misalnya: `{"id": "claude-opus-5", "speed": "fast"}`. Lihat [model yang didukung](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models) di halaman fast mode.
</Tip>

<Tip>
  Untuk menetapkan tingkat effort model, teruskan `model` sebagai objek, misalnya: `{"id": "claude-opus-5", "effort": "high"}`. Field `effort` menerima string tingkat (`low`, `medium`, `high`, `xhigh`, atau `max`) atau objek seperti `{"type": "high"}`. Lihat [Tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort#effort-levels) untuk mengetahui apa yang dilakukan setiap tingkat.
</Tip>

### Menyematkan inference geo

Seperti `speed` dan `effort`, `inference_geo` ditetapkan melalui bentuk objek dari `model`: teruskan `model` sebagai objek dan tetapkan `inference_geo` bersama `id`. Field ini menerima `"us"` atau `"global"`. Ketika tidak ditetapkan, setiap permintaan model mengikuti inference geo default workspace pada saat permintaan dilayani. Lihat [Residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency) untuk kontrol geo tingkat workspace dan harga.

Contoh berikut menyematkan agen ke inferensi US dan mencetak nilai `inference_geo` yang digemakan dalam objek `model` pada respons:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Geo-pinned assistant",
      "model": {"id": "claude-opus-5", "inference_geo": "us"},
      "system": "You are a helpful assistant."
    }')

  echo "Inference geo: $(jq -r '.model.inference_geo' <<< "$agent")"
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    agent=$(ant beta:agents create --format json < geo-pinned.agent.yaml)

    echo "Inference geo: $(jq -r '.model.inference_geo' <<< "$agent")"
    ```

    <File filename="geo-pinned.agent.yaml">
      ```yaml
      name: Geo-pinned assistant
      model:
        id: claude-opus-5
        inference_geo: us
      system: You are a helpful assistant.
      ```
    </File>
  </MultiFileExample>

  ```python Python
  agent = client.beta.agents.create(
      name="Geo-pinned assistant",
      model={
          "id": "claude-opus-5",
          "inference_geo": "us",
      },
      system="You are a helpful assistant.",
  )

  print(f"Inference geo: {agent.model.inference_geo}")
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Geo-pinned assistant",
    model: { id: "claude-opus-5", inference_geo: "us" },
    system: "You are a helpful assistant.",
  });

  console.log(`Inference geo: ${agent.model.inference_geo}`);
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Geo-pinned assistant",
      Model = new BetaManagedAgentsModelConfigParams
      {
          ID = BetaManagedAgentsModel.ClaudeOpus5,
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
  		ID:           anthropic.BetaManagedAgentsModelClaudeOpus5,
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
                  .id(BetaManagedAgentsModel.CLAUDE_OPUS_5)
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
          id: 'claude-opus-5',
          inferenceGeo: 'us',
      ),
      system: 'You are a helpful assistant.',
  );

  echo "Inference geo: {$agent->model->inferenceGeo}\n";
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Geo-pinned assistant",
    model: {id: "claude-opus-5", inference_geo: "us"},
    system_: "You are a helpful assistant."
  )

  puts "Inference geo: #{agent.model.inference_geo}"
  ```
</CodeGroup>

Penyematan `inference_geo` divalidasi terhadap [`allowed_inference_geos`](https://platform.claude.com/docs/id/manage-claude/data-residency#workspace-level-restrictions) milik workspace ketika agen disimpan, ketika sesi dibuat darinya, dan pada setiap giliran yang dilayani sesi. Jika allowlist workspace menyempit sehingga penyematan tidak lagi diizinkan, sesi baru tidak dapat dibuat dari agen tersebut dan sesi yang sedang berjalan menolak giliran selanjutnya; penyematan tidak pernah dikecualikan, karena workspace mengandalkannya untuk kepatuhan dan residensi data.

Menetapkan `inference_geo` pada model yang tidak mendukung penyematan inferensi geografis mengembalikan error 400; lihat [Ketersediaan model](https://platform.claude.com/docs/id/manage-claude/data-residency#model-availability) untuk model yang mendukungnya. Dalam konfigurasi `multiagent`, penyematan koordinator dan setiap anggota roster harus semuanya ditetapkan ke nilai yang sama atau semuanya tidak ditetapkan; lihat [Orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration). Untuk mengubah atau menghapus penyematan nanti, perbarui objek `model` agen; menyediakan `model` tanpa `inference_geo` akan menghapusnya, seperti dijelaskan di bawah [Semantik pembaruan](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-semantics).

## Memperbarui agen

Memperbarui agen menghasilkan versi baru ketika konfigurasi berubah. Field `version` bersifat opsional: sediakan untuk optimistic concurrency (ketidakcocokan mengembalikan 409), atau hilangkan untuk menerapkan pembaruan tanpa syarat (penulisan terakhir menang). Pembaruan pada agen yang diarsipkan ditolak.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  updated_agent=$(curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "version": $AGENT_VERSION,
    "system": "You are a helpful coding agent. Always write tests."
  }
  EOF
  )

  echo "New version: $(jq -r '.version' <<< "$updated_agent")"
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:agents update --agent-id "$AGENT_ID" < coding-assistant.agent.yaml
    ```

    <File filename="coding-assistant.agent.yaml">
      ```yaml
      name: Coding Assistant
      model:
        id: claude-opus-5
      system: You are a helpful coding agent. Always write tests.
      tools:
        - type: agent_toolset_20260401
      ```
    </File>
  </MultiFileExample>

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
    system: "You are a helpful coding agent. Always write tests.",
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

Contoh sebelumnya menyediakan `version` dari respons pembuatan, sehingga pembaruan hanya diterapkan jika tidak ada hal lain yang mengubah agen sejak Anda membacanya. Untuk menerapkan pembaruan tanpa syarat, hilangkan `version` dari permintaan:

<CodeGroup defaultLanguage="cURL">
  ```bash cURL
  updated_agent=$(curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "description": "Writes and reviews code."
    }')

  echo "New version: $(jq -r '.version' <<< "$updated_agent")"
  ```
</CodeGroup>

### Semantik pembaruan

* **`version`** bersifat opsional dan harus minimal 1 ketika disediakan. Ketika disediakan, permintaan mengembalikan 409 jika tidak cocok dengan versi agen saat ini, bahkan ketika field yang Anda kirim sudah cocok dengan nilai yang tersimpan; baca ulang agen dan coba lagi. Ketika dihilangkan, pembaruan diterapkan tanpa syarat dan pembaruan terbaru secara diam-diam menggantikan pembaruan bersamaan lainnya, tanpa error bagi kedua pemanggil. Menyediakan `version` adalah default yang direkomendasikan untuk pemanggil interaktif, dan menghilangkannya cocok untuk loop apply deklaratif, seperti job CI yang menyinkronkan definisi agen yang di-check-in, di mana loop tersebut memiliki agen.

* **Field yang dihilangkan dipertahankan.** Anda hanya perlu menyertakan field yang ingin Anda ubah.

* **Field skalar** (`model`, `system`, `name`, `description`) diganti dengan nilai baru. `system` dan `description` dapat dihapus dengan meneruskan `null`. `model` dan `name` bersifat wajib dan tidak dapat dihapus. Di dalam objek `model` yang Anda sediakan, `effort` adalah satu-satunya pengecualian: jika `id` model tidak berubah, menghilangkan `effort` membiarkan tingkat effort yang tersimpan tidak berubah. Jika Anda mengubah `id` model, `effort` yang dihilangkan direset ke default model baru. Field `model` lainnya diganti bersama objeknya: menyediakan `model` tanpa `inference_geo` menghapus penyematan inference geo agen.

* **Field array** (`tools`, `mcp_servers`, `skills`) diganti sepenuhnya oleh array baru. Untuk menghapus field array seluruhnya, teruskan `null` atau array kosong.

* **`multiagent`** diganti secara keseluruhan, termasuk roster `agents`-nya. Teruskan `null` untuk menghapusnya.

* **Metadata** digabungkan pada tingkat key. Key yang Anda sediakan ditambahkan atau diperbarui. Key yang Anda hilangkan dipertahankan. Untuk menghapus key tertentu, tetapkan nilainya ke `null`.

* **Deteksi no-op.** Jika pembaruan tidak menghasilkan perubahan relatif terhadap versi saat ini, tidak ada versi baru yang dibuat dan versi yang ada dikembalikan.

* **Roster koordinator tidak diperbarui.** Koordinator yang mereferensikan agen ini dalam roster `multiagent.agents` mereka tetap menggunakan versi yang disematkan ketika koordinator dibuat atau terakhir diperbarui, bahkan jika referensi tersebut menghilangkan `version`. Untuk mendelegasikan ke versi baru, [perbarui koordinator](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#configure-the-coordinator) agar rosternya mereferensikannya.

## Siklus hidup agen

| Operasi          | Perilaku                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |
| **Perbarui**     | Menghasilkan versi agen baru ketika konfigurasi berubah.                                                      |
| **Daftar versi** | Mengembalikan riwayat versi lengkap sehingga Anda dapat melacak perubahan dari waktu ke waktu.                |
| **Arsipkan**     | Membuat agen menjadi read-only. Sesi baru tidak dapat mereferensikannya, tetapi sesi yang ada terus berjalan. |

### Daftar versi

Ambil riwayat versi lengkap untuk melacak bagaimana agen telah berubah dari waktu ke waktu. Hasil dipaginasi, dan contoh SDK mengambil setiap halaman secara otomatis.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    | jq -r '.data[] | "Version \(.version): \(.updated_at)"'
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
      echo "Version {$version->version}: {$version->updatedAt->format(DateTimeInterface::ATOM)}\n";
  }
  ```

  ```ruby Ruby
  client.beta.agents.versions.list(agent.id).auto_paging_each do |agent_version|
    puts "Version #{agent_version.version}: #{agent_version.updated_at.iso8601}"
  end
  ```
</CodeGroup>

### Mengarsipkan agen

Pengarsipan membuat agen menjadi read-only dan tidak dapat dibatalkan. Sesi yang ada terus berjalan, tetapi sesi baru tidak dapat mereferensikan agen tersebut. Respons menetapkan `archived_at` ke timestamp pengarsipan.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  archived=$(curl -fsSL -X POST "https://api.anthropic.com/v1/agents/$AGENT_ID/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")

  echo "Archived at: $(jq -r '.archived_at' <<< "$archived")"
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

  echo "Archived at: {$archived->archivedAt->format(DateTimeInterface::ATOM)}\n";
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
    Lampirkan keahlian berbasis filesystem yang dapat digunakan kembali ke agen Anda untuk alur kerja khusus domain.
  </Card>

  <Card title="Memulai sesi" icon="play" href="https://platform.claude.com/docs/id/managed-agents/sessions">
    Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.
  </Card>

  <Card title="Referensi" icon="book" href="https://platform.claude.com/docs/id/managed-agents/reference">
    Tipe event, flag CLI worker self-hosted, tipe server MCP yang didukung, batas laju, dan pedoman branding untuk Claude Managed Agents.
  </Card>
</CardGroup>
