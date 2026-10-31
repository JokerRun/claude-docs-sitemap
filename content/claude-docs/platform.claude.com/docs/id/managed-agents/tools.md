---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/tools
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: c4b0036bccf8efdfe4953bd20d9e77e2acd10a97f8b167aa2243d51ca115ef46
---

---
title: Alat
url: https://platform.claude.com/docs/id/managed-agents/tools
description: Konfigurasikan alat yang tersedia untuk agen Anda.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. Berlaku untuk semua subfitur Managed Agents, termasuk Sandbox yang di-host sendiri.
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
---

Claude Managed Agents menyediakan serangkaian alat bawaan yang dapat digunakan Claude secara otonom di dalam sebuah [sesi](https://platform.claude.com/docs/id/managed-agents/sessions). Anda mengontrol alat mana yang tersedia dengan menentukannya dalam konfigurasi agen.

Claude Managed Agents juga mendukung alat kustom yang ditentukan pengguna. Aplikasi Anda menjalankan alat-alat ini secara terpisah dan mengembalikan hasilnya kepada Claude, yang menggunakannya untuk melanjutkan tugas. Untuk memberikan alat dari server MCP kepada agen, gunakan [konektor MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) sebagai gantinya.

## Alat yang tersedia

Toolset agen mencakup alat-alat berikut. Semuanya diaktifkan secara default saat Anda menyertakan toolset dalam konfigurasi agen.

| Alat       | Nama         | Deskripsi                                                       |
| ---------- | ------------ | --------------------------------------------------------------- |
| Bash       | `bash`       | Menjalankan perintah bash dalam sesi shell                      |
| Read       | `read`       | Membaca file dari filesystem sandbox                            |
| Write      | `write`      | Menulis file ke filesystem sandbox                              |
| Edit       | `edit`       | Melakukan penggantian string dalam sebuah file                  |
| Glob       | `glob`       | Melakukan pencocokan pola file yang cepat menggunakan pola glob |
| Grep       | `grep`       | Mencari teks menggunakan pola regex                             |
| Web fetch  | `web_fetch`  | Mengambil konten dari sebuah URL                                |
| Web search | `web_search` | Mencari informasi di web                                        |

Ketika output alat melebihi 100.000 karakter (sekitar 25.000 token), output tersebut secara otomatis ditulis ke sebuah file di [sandbox](https://platform.claude.com/docs/id/managed-agents/environments). Model menerima pratinjau terpotong beserta path file dan dapat membaca konten lengkapnya dari sana.

## Mengonfigurasi toolset

Aktifkan toolset lengkap dengan `agent_toolset_20260401` saat membuat agen. Gunakan array `configs` (csharp, go: `Configs`) untuk menonaktifkan alat tertentu atau menimpa pengaturannya. Setiap entri diidentifikasi oleh `name` (csharp, go: `Name`)-nya, yang mengambil nilai dari kolom Nama di [Alat yang tersedia](https://platform.claude.com/docs/id/managed-agents/tools#available-tools). Sebuah entri juga menerima field `type` (csharp, go: `Type`) opsional dengan nilai yang sama.

Setiap entri konfigurasi juga dapat menetapkan `permission_policy` (java, php: `permissionPolicy`; csharp, go: `PermissionPolicy`). Kebijakan ini mengontrol apakah panggilan alat berjalan tanpa konfirmasi, memerlukan konfirmasi, atau dievaluasi secara individual oleh server. Lihat [Kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) untuk jenis kebijakan yang tersedia.

Contoh berikut mengaktifkan toolset dan menonaktifkan `web_fetch`:

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
      "tools": [
        {
          "type": "agent_toolset_20260401",
          "configs": [
            {"name": "web_fetch", "enabled": false}
          ]
        }
      ]
    }'
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply agent.md
    ```

    <File filename="agent.md">
      ```markdown
      ---
      name: Coding Assistant
      model: claude-opus-5-5
      tools:
        - type: agent_toolset_20260401
          configs:
            - name: web_fetch
              enabled: false
      ---
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  agent = client.beta.agents.create(
      name="Coding Assistant",
      model="claude-opus-5-5",
      tools=[
          {
              "type": "agent_toolset_20260401",
              "configs": [
                  {"name": "web_fetch", "enabled": False},
              ],
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Coding Assistant",
    model: "claude-opus-5-5",
    tools: [
      {
        type: "agent_toolset_20260401",
        configs: [{ name: "web_fetch", enabled: false }]
      }
    ]
  });
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Agents;

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = BetaManagedAgentsModel.ClaudeOpus5_5,
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Configs =
              [
                  new BetaManagedAgentsWebFetchToolConfigParams { Enabled = false },
              ],
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
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Configs: []anthropic.BetaManagedAgentsAgentToolConfigParamsUnion{{
  				OfWebFetch: &anthropic.BetaManagedAgentsWebFetchToolConfigParams{
  					Enabled: anthropic.Bool(false),
  				},
  			}},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;

  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("Coding Assistant")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_5_5)
      .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
          .addConfig(BetaManagedAgentsWebFetchToolConfigParams.builder()
              .enabled(false)
              .build())
          .build())
      .build());
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsWebFetchToolConfigParams;

  $agent = $client->beta->agents->create(
      name: 'Coding Assistant',
      model: 'claude-opus-5-5',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              configs: [
                  BetaManagedAgentsWebFetchToolConfigParams::with(enabled: false),
              ],
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Coding Assistant",
    model: "claude-opus-5-5",
    tools: [
      {
        type: :agent_toolset_20260401,
        configs: [
          {name: :web_fetch, enabled: false}
        ]
      }
    ]
  )
  ```
</CodeGroup>

### Menonaktifkan alat tertentu

Untuk menonaktifkan alat, tetapkan `enabled: false` dalam entri `configs`-nya:

```json
{
  "type": "agent_toolset_20260401",
  "configs": [
    { "name": "web_fetch", "enabled": false },
    { "name": "web_search", "enabled": false }
  ]
}
```

### Mengaktifkan hanya alat tertentu

Objek `default_config` menetapkan baseline untuk setiap alat dalam set, dan entri `configs` per alat menimpanya. Untuk memulai dengan semuanya nonaktif dan hanya mengaktifkan yang Anda butuhkan, tetapkan `default_config.enabled` ke `false`:

```json
{
  "type": "agent_toolset_20260401",
  "default_config": { "enabled": false },
  "configs": [
    { "name": "bash", "enabled": true },
    { "name": "read", "enabled": true },
    { "name": "write", "enabled": true }
  ]
}
```

### Membatasi web search dan web fetch

Entri `web_search` dan `web_fetch` juga menerima daftar domain, batas konten yang diambil, dan lokasi pencarian. Lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions).

### Jenis entri konfigurasi di SDK

SDK memberikan tipe pada setiap entri `configs` (csharp, go: `Configs`) berdasarkan alat. Tipe tersebut adalah union dengan satu anggota untuk setiap alat bawaan, yang dibedakan oleh `type` (csharp, go: `Type`).

Di Go, Java, C#, dan PHP, Anda membuat entri dari nilai bertipe, bukan dari dictionary atau hash biasa. Di SDK tersebut, tipe elemen dari `configs` (csharp, go: `Configs`) adalah union itu sendiri, jadi buat setiap entri dari tipe anggota per alatnya.

Anda dapat menghilangkan `type` (csharp, go: `Type`) saat membuat entri, karena server menyimpulkannya dari `name` (csharp, go: `Name`). Respons selalu menyertakannya. Pemberian tipe ini tidak mengubah JSON hasil serialisasi sebuah entri. Permintaan yang entrinya hanya menetapkan `name`, `enabled`, dan `permission_policy` valid dengan atau tanpa `type`.

## Alat kustom

Alat kustom serupa dengan [alat klien yang didefinisikan pengguna](https://platform.claude.com/docs/id/agents-and-tools/tool-use/how-tool-use-works#user-defined-tools-client-executed) di Messages API. Anda menentukan operasi apa yang tersedia dan apa yang dikembalikannya, dan Claude menentukan kapan dan bagaimana memanggilnya.

Claude tidak menjalankan alat kustom sendiri. Claude mengeluarkan permintaan terstruktur, kode Anda menjalankan operasinya, dan Anda mengembalikan hasilnya ke sesi.

Contoh berikut membuat agen dengan toolset bawaan dan satu alat kustom, `get_weather`:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Weather Agent",
      "model": "claude-opus-5-5",
      "tools": [
        {
          "type": "agent_toolset_20260401"
        },
        {
          "type": "custom",
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
          }
        }
      ]
    }'
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply agent.md
    ```

    <File filename="agent.md">
      ```markdown
      ---
      name: Weather Agent
      model: claude-opus-5-5
      tools:
        - type: agent_toolset_20260401
        - type: custom
          name: get_weather
          description: Get current weather for a location
          input_schema:
            type: object
            properties:
              location:
                type: string
                description: City name
            required:
              - location
      ---
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  agent = client.beta.agents.create(
      name="Weather Agent",
      model="claude-opus-5-5",
      tools=[
          {
              "type": "agent_toolset_20260401",
          },
          {
              "type": "custom",
              "name": "get_weather",
              "description": "Get current weather for a location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {"type": "string", "description": "City name"},
                  },
                  "required": ["location"],
              },
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Weather Agent",
    model: "claude-opus-5-5",
    tools: [
      { type: "agent_toolset_20260401" },
      {
        type: "custom",
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: { location: { type: "string", description: "City name" } },
          required: ["location"]
        }
      }
    ]
  });
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic.Models.Beta.Agents;

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Weather Agent",
      Model = BetaManagedAgentsModel.ClaudeOpus5_5,
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params(),
          new BetaManagedAgentsCustomToolParams
          {
              Name = "get_weather",
              Description = "Get current weather for a location",
              InputSchema = new()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(
                          new { type = "string", description = "City name" }
                      ),
                  },
                  Required = ["location"],
              },
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Weather Agent",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5_5,
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{},
  	}, {
  		OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
  			Name:        "get_weather",
  			Description: "Get current weather for a location",
  			InputSchema: anthropic.BetaManagedAgentsCustomToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "City name",
  					},
  				},
  				Required: []string{"location"},
  			},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;
  import java.util.Map;

  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("Weather Agent")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_5_5)
      .addTool(BetaManagedAgentsAgentToolset20260401Params.builder().build())
      .addTool(BetaManagedAgentsCustomToolParams.builder()
          .name("get_weather")
          .description("Get current weather for a location")
          .inputSchema(BetaManagedAgentsCustomToolInputSchema.builder()
              .properties(BetaManagedAgentsCustomToolInputSchema.Properties.builder()
                  .putAdditionalProperty("location", JsonValue.from(Map.of(
                      "type", "string",
                      "description", "City name")))
                  .build())
              .addRequired("location")
              .build())
          .build())
      .build());
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolInputSchema;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolParams;

  $agent = $client->beta->agents->create(
      name: 'Weather Agent',
      model: 'claude-opus-5-5',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(),
          BetaManagedAgentsCustomToolParams::with(
              name: 'get_weather',
              description: 'Get current weather for a location',
              inputSchema: BetaManagedAgentsCustomToolInputSchema::with(
                  properties: ['location' => ['type' => 'string', 'description' => 'City name']],
                  required: ['location'],
              ),
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Weather Agent",
    model: "claude-opus-5-5",
    tools: [
      {type: :agent_toolset_20260401},
      {
        type: :custom,
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: :object,
          properties: {location: {type: "string", description: "City name"}},
          required: ["location"]
        }
      }
    ]
  )
  ```
</CodeGroup>

Nama alat kustom tidak boleh diawali dengan `mcp__` atau `ant__`, atau sama dengan nama alat agen bawaan. Permintaan yang melanggar aturan ini mengembalikan error 400. Agen yang sudah memiliki alat kustom dengan nama yang diawali `ant__` hanya menerima pembaruan jika pembaruan tersebut mengirim `tools` (csharp, go: `Tools`) tanpa nama tersebut, jadi ganti nama atau hapus alat tersebut pada pembaruan Anda berikutnya. Sesi baru ditolak dengan error 400 jika alat semacam itu ada pada agennya (setelah [penimpaan](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session) apa pun), pada agen dalam daftar `predefined_agents` (java, php: `predefinedAgents`; csharp, go: `PredefinedAgents`) dari `subagents` (csharp, go: `Subagents`), atau pada agen dalam daftar `predefined_agents` (java, php: `predefinedAgents`; csharp, go: `PredefinedAgents`) dari `workflows` (csharp, go: `Workflows`). Sesi yang sudah ada tidak terpengaruh.

Agen memanggil alat kustomnya selama sesi. Untuk menerima panggilan dan mengembalikan hasil, lihat [Menjawab panggilan alat yang menjeda sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls).

Untuk sesi yang berjalan di sandbox self-hosted, environment worker dapat [melayani alat kustom dari sandbox](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools). Ini dapat mencakup alat yang membungkus server MCP di dalam jaringan Anda.

### Praktik terbaik untuk definisi alat kustom

* **Berikan deskripsi yang sangat mendetail.** Ini sejauh ini merupakan faktor terpenting dalam kinerja alat. Semakin banyak konteks yang dapat Anda berikan kepada Claude tentang alat Anda, semakin baik Claude dalam menentukan kapan dan bagaimana menggunakannya. Usahakan tiga hingga empat kalimat untuk setiap deskripsi alat, lebih banyak jika alatnya kompleks. Deskripsi Anda harus mencakup:

  * Apa yang dilakukan alat tersebut
  * Kapan menggunakannya, dan kapan tidak
  * Apa arti setiap parameter dan bagaimana pengaruhnya terhadap perilaku alat
  * Peringatan atau batasan penting apa pun

* **Gabungkan operasi terkait ke dalam lebih sedikit alat.** Kelompokkan tindakan seperti `create_pr`, `review_pr`, dan `merge_pr` ke dalam satu alat dengan parameter `action`. Alat yang lebih sedikit namun lebih mumpuni mengurangi ambiguitas pemilihan dan membuat kumpulan alat Anda lebih mudah dinavigasi oleh Claude.

* **Gunakan namespace yang bermakna dalam nama alat.** Ketika alat Anda mencakup beberapa layanan atau sumber daya, awali nama dengan sumber dayanya (misalnya, `db_query` atau `storage_read`). Ini membuat pemilihan alat tidak ambigu seiring bertambahnya pustaka Anda.

* **Rancang respons alat agar hanya mengembalikan informasi bernilai tinggi.** Kembalikan pengidentifikasi yang semantik dan stabil (misalnya, slug atau UUID) alih-alih referensi internal yang tidak transparan. Sertakan hanya field yang dibutuhkan Claude untuk menentukan langkah berikutnya. Respons yang membengkak membuang konteks dan mempersulit Claude untuk mengekstrak hal yang penting.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Membatasi domain web search dan web fetch" icon="shield" href="https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions">
    Kontrol situs mana yang dapat dijangkau alat web, batasi konten yang diambil, dan lokalkan hasil pencarian.
  </Card>

  <Card title="Konektor MCP" icon="link" href="https://platform.claude.com/docs/id/managed-agents/mcp-connector">
    Hubungkan server MCP ke agen Anda untuk mengakses alat dan sumber data eksternal.
  </Card>

  <Card title="Kebijakan izin" icon="lock" href="https://platform.claude.com/docs/id/managed-agents/permission-policies">
    Kontrol kapan alat agen dan alat MCP berjalan.
  </Card>

  <Card title="Aliran event sesi" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/events-and-streaming">
    Kirim event, lakukan streaming respons, dan interupsi atau arahkan ulang sesi Anda saat sedang berjalan.
  </Card>
</CardGroup>

## Ketersediaan

Toolset agen dalam versi beta di semua model.

### Dukungan API

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tersedia

| Status | Platform cloud                                                                                                     |
| ------ | ------------------------------------------------------------------------------------------------------------------ |
| Beta   | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

### Header beta yang diperlukan

[Ikhtisar header beta](https://platform.claude.com/docs/id/api/beta-headers)

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

* `managed-agents-2026-04-01`

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                          | HIPAA                                                                               |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Status | Tidak layak                                                                                                                                                               | Tidak layak                                                                         |
| Detail | Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. Berlaku untuk semua subfitur Managed Agents, termasuk Sandbox yang di-host sendiri. | Berlaku untuk semua subfitur Managed Agents, termasuk Sandbox yang di-host sendiri. |

Endpoint yang berlaku:

* `/v1/agents`
* `/v1/sessions`
* `/v1/environments`
