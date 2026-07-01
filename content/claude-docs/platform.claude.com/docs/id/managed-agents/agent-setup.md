---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/agent-setup
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: f9b4ce5fa237c3ad07f8b2ceaf55b1981a8c4290bf0d2de3c3dbd1248a4f1945
---

# Definisikan agen Anda

Buat konfigurasi agen yang dapat digunakan kembali dan memiliki versi.

---

Agen adalah konfigurasi yang dapat digunakan kembali dan memiliki versi yang mendefinisikan persona dan kapabilitas. Agen menggabungkan model, prompt sistem, alat, server MCP, dan skill yang membentuk bagaimana Claude berperilaku selama sesi.

Buat agen sekali sebagai sumber daya yang dapat digunakan kembali dan referensikan berdasarkan ID setiap kali Anda [memulai sesi](/docs/id/managed-agents/sessions). Agen memiliki versi dan lebih mudah dikelola di banyak sesi.

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Field konfigurasi agen

| Field         | Deskripsi                                                                                                                                                                                                                                                                                                                    |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | Wajib. Nama yang mudah dibaca manusia untuk agen.                                                                                                                                                                                                                                                                            |
| `model`       | Wajib. [Model](/docs/id/about-claude/models/overview) Claude yang menjalankan agen. Menerima string ID model atau objek, misalnya `{"id": "claude-opus-4-8"}`. Semua model keluarga Claude 4.5 dan yang lebih baru didukung.                                                                                                 |
| `system`      | [Prompt sistem](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role) yang mendefinisikan perilaku dan persona agen. Prompt sistem berbeda dari [pesan pengguna](/docs/id/managed-agents/reference#event-types), yang seharusnya mendeskripsikan pekerjaan yang harus dilakukan. |
| `tools`       | Alat yang tersedia untuk agen. Menggabungkan [alat agen bawaan](/docs/id/managed-agents/tools), [alat MCP](/docs/id/managed-agents/mcp-connector), dan [alat kustom](/docs/id/managed-agents/tools#custom-tools).                                                                                                            |
| `mcp_servers` | [Server MCP](/docs/id/managed-agents/mcp-connector) yang menyediakan kapabilitas pihak ketiga yang terstandarisasi.                                                                                                                                                                                                          |
| `skills`      | [Skill](/docs/id/managed-agents/skills) yang menyediakan konteks spesifik domain dengan pengungkapan progresif.                                                                                                                                                                                                              |
| `multiagent`  | Deklarasi koordinator yang mencantumkan agen-agen yang dapat didelegasikan oleh agen ini. Lihat [Sesi multiagen](/docs/id/managed-agents/multi-agent).                                                                                                                                                                       |
| `description` | Deskripsi tentang apa yang dilakukan agen.                                                                                                                                                                                                                                                                                   |
| `metadata`    | Pasangan key-value arbitrer untuk pelacakan Anda sendiri.                                                                                                                                                                                                                                                                    |

## Membuat agen

Contoh berikut mendefinisikan agen coding yang menggunakan Claude Opus 4.8 dengan akses ke toolset agen bawaan. Toolset ini memungkinkan agen menulis kode, membaca file, mencari di web, dan lainnya. Lihat [referensi alat agen](/docs/id/managed-agents/tools) untuk daftar lengkap alat yang didukung.

Contoh-contoh ini menggunakan curl, CLI `ant`, atau salah satu SDK. Jika Anda belum menyiapkannya, [quickstart](/docs/id/managed-agents/quickstart#install-the-cli) mencakup instalasi dan penyiapan klien.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Coding Assistant",
      "model": "claude-opus-4-8",
      "system": "You are a helpful coding agent.",
      "tools": [{"type": "agent_toolset_20260401"}]
    }')

  AGENT_ID=$(jq -r '.id' <<< "$agent")
  AGENT_VERSION=$(jq -r '.version' <<< "$agent")
  ```

  ```bash CLI
  agent=$(ant beta:agents create \
    --name "Coding Assistant" \
    --model '{id: claude-opus-4-8}' \
    --system "You are a helpful coding agent." \
    --tool '{type: agent_toolset_20260401}' \
    --format json)

  AGENT_ID=$(jq -r '.id' <<< "$agent")
  AGENT_VERSION=$(jq -r '.version' <<< "$agent")
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Coding Assistant",
      model="claude-opus-4-8",
      system="You are a helpful coding agent.",
      tools=[
          {"type": "agent_toolset_20260401"},
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Coding Assistant",
    model: "claude-opus-4-8",
    system: "You are a helpful coding agent.",
    tools: [{ type: "agent_toolset_20260401" }],
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = new("claude-opus-4-8"),
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
  		ID: "claude-opus-4-8",
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
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
    system_: "You are a helpful coding agent.",
    tools: [{type: "agent_toolset_20260401"}]
  )
  ```
</CodeGroup>

<Tip>
  Untuk menggunakan Claude Opus 4.8 atau Claude Opus 4.7 dengan [fast mode](/docs/id/build-with-claude/fast-mode), berikan `model` sebagai objek, misalnya: `{"id": "claude-opus-4-8", "speed": "fast"}`. Fast mode untuk Claude Opus 4.7 sudah tidak digunakan lagi (deprecated); lihat [Fast mode](/docs/id/build-with-claude/fast-mode#supported-models) untuk tanggal penghapusan dan perilakunya.
</Tip>

Respons akan mengembalikan konfigurasi Anda dan menambahkan field `id`, `type`, `version`, `created_at`, `updated_at`, dan `archived_at`. `version` dimulai dari 1 dan bertambah setiap kali pembaruan mengubah agen.

```json
{
  "id": "agent_01HqR2k7vXbZ9mNpL3wYcT8f",
  "type": "agent",
  "name": "Coding Assistant",
  "model": {
    "id": "claude-opus-4-8",
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
  "metadata": {},
  "version": 1,
  "created_at": "2026-04-03T18:24:10.412Z",
  "updated_at": "2026-04-03T18:24:10.412Z",
  "archived_at": null
}
```

`default_config` pada toolset menunjukkan [kebijakan izin](/docs/id/managed-agents/permission-policies) default-nya, `always_allow`, yang berlaku kecuali Anda mengonfigurasinya.

## Memperbarui agen

Memperbarui agen menghasilkan versi baru ketika konfigurasi berubah. Field `version` wajib diisi dan harus cocok dengan versi agen saat ini, sehingga Anda selalu memperbarui dari keadaan yang diketahui. Ketidakcocokan versi mengembalikan 409, dan pembaruan pada agen yang diarsipkan akan ditolak.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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

  ```bash CLI
  ant beta:agents update \
    --agent-id "$AGENT_ID" \
    --version "$AGENT_VERSION" \
    --system "You are a helpful coding agent. Always write tests."
  ```

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
  	Version: agent.Version,
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

### Semantik pembaruan

* **Field yang dihilangkan akan dipertahankan.** Anda hanya perlu menyertakan field yang ingin Anda ubah.

* **Field skalar** (`model`, `system`, `name`, `description`) diganti dengan nilai baru. `system` dan `description` dapat dikosongkan dengan memberikan `null`. `model` dan `name` bersifat wajib dan tidak dapat dikosongkan.

* **Field array** (`tools`, `mcp_servers`, `skills`) sepenuhnya diganti oleh array baru. Untuk mengosongkan field array sepenuhnya, berikan `null` atau array kosong.

* **`multiagent`** diganti secara keseluruhan, termasuk daftar `agents`-nya. Berikan `null` untuk mengosongkannya.

* **Metadata** digabungkan pada level key. Key yang Anda berikan akan ditambahkan atau diperbarui. Key yang Anda hilangkan akan dipertahankan. Untuk menghapus key tertentu, atur nilainya ke `null`.

* **Deteksi no-op.** Jika pembaruan tidak menghasilkan perubahan relatif terhadap versi saat ini, tidak ada versi baru yang dibuat dan versi yang ada akan dikembalikan.

* **Daftar koordinator tidak diperbarui.** Koordinator yang mereferensikan agen ini dalam daftar `multiagent.agents` mereka tetap menggunakan versi yang disematkan saat koordinator dibuat atau terakhir diperbarui, bahkan jika referensi tersebut menghilangkan `version`. Untuk mendelegasikan ke versi baru, [perbarui koordinator](/docs/id/managed-agents/multi-agent#configure-the-coordinator) sehingga daftarnya mereferensikan versi tersebut.

## Siklus hidup agen

| Operasi           | Perilaku                                                                                                  |
| ----------------- | --------------------------------------------------------------------------------------------------------- |
| **Update**        | Menghasilkan versi agen baru ketika konfigurasi berubah.                                                  |
| **List versions** | Mengembalikan riwayat versi lengkap sehingga Anda dapat melacak perubahan dari waktu ke waktu.            |
| **Archive**       | Menjadikan agen hanya-baca. Sesi baru tidak dapat mereferensikannya, tetapi sesi yang ada tetap berjalan. |

### Mencantumkan versi

Ambil riwayat versi lengkap untuk melacak bagaimana agen telah berubah dari waktu ke waktu. Hasil dipaginasi, dan contoh SDK mengambil setiap halaman secara otomatis.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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

Pengarsipan menjadikan agen hanya-baca dan tidak dapat dibatalkan. Sesi yang ada tetap berjalan, tetapi sesi baru tidak dapat mereferensikan agen tersebut. Respons mengatur `archived_at` ke timestamp pengarsipan.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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
  <Card title="Alat" icon="tool" href="/docs/id/managed-agents/tools">
    Konfigurasikan alat yang tersedia untuk agen Anda.
  </Card>

  <Card title="Skill" icon="graduation-cap" href="/docs/id/managed-agents/skills">
    Lampirkan keahlian berbasis filesystem yang dapat digunakan kembali ke agen Anda untuk alur kerja spesifik domain.
  </Card>

  <Card title="Memulai sesi" icon="play" href="/docs/id/managed-agents/sessions">
    Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.
  </Card>

  <Card title="Referensi" icon="book" href="/docs/id/managed-agents/reference">
    Tipe event, flag CLI worker self-hosted, tipe server MCP yang didukung, batas laju, dan panduan branding untuk Claude Managed Agents.
  </Card>
</CardGroup>
