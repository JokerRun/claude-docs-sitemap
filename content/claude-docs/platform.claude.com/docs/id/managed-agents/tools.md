---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/tools
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: f3a364e403c57a0517130c364d39c3751f72070ac51f43c39cb18ed2c0b19d5c
---

# Alat

Konfigurasikan alat yang tersedia untuk agen Anda.

---

Claude Managed Agents menyediakan serangkaian alat bawaan yang dapat digunakan Claude secara otonom dalam sebuah sesi. Anda mengontrol alat mana yang tersedia dengan menentukannya dalam konfigurasi agen.

Alat kustom yang didefinisikan pengguna juga didukung. Aplikasi Anda mengeksekusi alat-alat ini secara terpisah dan mengirimkan hasil alat kembali ke Claude; Claude dapat menggunakan hasil tersebut untuk melanjutkan tugas yang sedang dikerjakan.

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Alat yang tersedia

Toolset agen mencakup alat-alat berikut. Semuanya diaktifkan secara default ketika Anda menyertakan toolset dalam konfigurasi agen Anda.

| Alat       | Nama         | Deskripsi                                             |
| ---------- | ------------ | ----------------------------------------------------- |
| Bash       | `bash`       | Menjalankan perintah bash dalam sesi shell            |
| Read       | `read`       | Membaca file dari filesystem lokal                    |
| Write      | `write`      | Menulis file ke filesystem lokal                      |
| Edit       | `edit`       | Melakukan penggantian string dalam file               |
| Glob       | `glob`       | Pencocokan pola file yang cepat menggunakan pola glob |
| Grep       | `grep`       | Pencarian teks menggunakan pola regex                 |
| Web fetch  | `web_fetch`  | Mengambil konten dari URL                             |
| Web search | `web_search` | Mencari informasi di web                              |

Ketika output alat melebihi 100.000 token, output tersebut secara otomatis ditulis ke file di dalam sandbox. Model menerima pratinjau yang terpotong beserta path file dan dapat membaca konten lengkapnya dari sana.

## Mengonfigurasi toolset

Aktifkan toolset lengkap dengan `agent_toolset_20260401` saat membuat agen. Gunakan array `configs` untuk menonaktifkan alat tertentu atau mengganti pengaturannya.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "Coding Assistant",
    "model": "claude-opus-4-8",
    "tools": [
      {
        "type": "agent_toolset_20260401",
        "configs": [
          {"name": "web_fetch", "enabled": false}
        ]
      }
    ]
  }
  EOF
  )
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Coding Assistant
  model: claude-opus-4-8
  tools:
    - type: agent_toolset_20260401
      configs:
        - name: web_fetch
          enabled: false
  YAML
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Coding Assistant",
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
    tools: [
      {
        type: "agent_toolset_20260401",
        configs: [{ name: "web_fetch", enabled: false }]
      }
    ]
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = new("claude-opus-4-8"),
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
              Configs =
              [
                  new() { Name = "web_fetch", Enabled = false },
              ],
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
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			Configs: []anthropic.BetaManagedAgentsAgentToolConfigParams{{
  				Name:    anthropic.BetaManagedAgentsAgentToolConfigParamsNameWebFetch,
  				Enabled: anthropic.Bool(false),
  			}},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  _ = agent
  ```

  ```java Java
  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("Coding Assistant")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
      .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
          .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
          .addConfig(BetaManagedAgentsAgentToolConfigParams.builder()
              .name(BetaManagedAgentsAgentToolConfigParams.Name.WEB_FETCH)
              .enabled(false)
              .build())
          .build())
      .build());
  ```

  ```php PHP

  $agent = $client->beta->agents->create(
      name: 'Coding Assistant',
      model: 'claude-opus-4-8',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
              configs: [
                  BetaManagedAgentsAgentToolConfigParams::with(name: 'web_fetch', enabled: false),
              ],
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Coding Assistant",
    model: "claude-opus-4-8",
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

Untuk menonaktifkan sebuah alat, atur `enabled: false` dalam entri konfigurasinya:

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

Untuk memulai dengan semua alat dinonaktifkan dan hanya mengaktifkan yang Anda butuhkan, atur `default_config.enabled` ke `false`:

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

## Alat kustom

Selain alat bawaan, Anda dapat mendefinisikan alat kustom. Alat kustom serupa dengan [alat klien yang didefinisikan pengguna](/docs/id/agents-and-tools/tool-use/how-tool-use-works#user-defined-tools-client-executed) di Messages API.

Alat kustom memungkinkan Anda memperluas kemampuan Claude untuk melakukan berbagai tugas yang lebih luas. Setiap alat mendefinisikan sebuah kontrak: Anda menentukan operasi apa yang tersedia dan apa yang dikembalikannya; Claude menentukan kapan dan bagaimana memanggilnya. Model tidak pernah mengeksekusi apa pun sendiri. Model mengeluarkan permintaan terstruktur, kode Anda menjalankan operasinya, dan hasilnya mengalir kembali ke dalam percakapan.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "Weather Agent",
    "model": "claude-opus-4-8",
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
  }
  EOF
  )
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Weather Agent
  model: claude-opus-4-8
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
  YAML
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Weather Agent",
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Weather Agent",
      Model = new("claude-opus-4-8"),
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
          new BetaManagedAgentsCustomToolParams
          {
              Type = "custom",
              Name = "get_weather",
              Description = "Get current weather for a location",
              InputSchema = new()
              {
                  Type = "object",
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
  		ID: "claude-opus-4-8",
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}, {
  		OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
  			Type:        anthropic.BetaManagedAgentsCustomToolParamsTypeCustom,
  			Name:        "get_weather",
  			Description: "Get current weather for a location",
  			InputSchema: anthropic.BetaManagedAgentsCustomToolInputSchemaParam{
  				Type: anthropic.BetaManagedAgentsCustomToolInputSchemaTypeObject,
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
  _ = agent
  ```

  ```java Java
  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("Weather Agent")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
      .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
          .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
          .build())
      .addTool(BetaManagedAgentsCustomToolParams.builder()
          .type(BetaManagedAgentsCustomToolParams.Type.CUSTOM)
          .name("get_weather")
          .description("Get current weather for a location")
          .inputSchema(BetaManagedAgentsCustomToolInputSchema.builder()
              .type(BetaManagedAgentsCustomToolInputSchema.Type.OBJECT)
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
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolInputSchema;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolParams;

  $agent = $client->beta->agents->create(
      name: 'Weather Agent',
      model: 'claude-opus-4-8',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
          ),
          BetaManagedAgentsCustomToolParams::with(
              type: 'custom',
              name: 'get_weather',
              description: 'Get current weather for a location',
              inputSchema: BetaManagedAgentsCustomToolInputSchema::with(
                  type: 'object',
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
    model: "claude-opus-4-8",
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

Setelah Anda mendefinisikan alat di tingkat agen, agen akan memanggil alat tersebut selama berlangsungnya sesi. Lihat [Aliran event sesi](/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) untuk alur lengkapnya.

### Praktik terbaik untuk definisi alat kustom

* **Berikan deskripsi yang sangat detail.** Ini adalah faktor terpenting dalam performa alat. Deskripsi Anda harus menjelaskan apa yang dilakukan alat tersebut, kapan alat tersebut harus digunakan (dan kapan tidak), apa arti setiap parameter dan bagaimana pengaruhnya terhadap perilaku alat, serta peringatan atau batasan penting apa pun. Semakin banyak konteks yang dapat Anda berikan kepada Claude tentang alat Anda, semakin baik Claude dalam menentukan kapan dan bagaimana menggunakannya. Usahakan setidaknya 3-4 kalimat per deskripsi alat, lebih banyak jika alatnya kompleks.
* **Konsolidasikan operasi terkait ke dalam lebih sedikit alat.** Daripada membuat alat terpisah untuk setiap tindakan (`create_pr`, `review_pr`, `merge_pr`), kelompokkan ke dalam satu alat dengan parameter `action`. Alat yang lebih sedikit namun lebih mumpuni mengurangi ambiguitas pemilihan dan membuat kumpulan alat Anda lebih mudah dinavigasi oleh Claude.
* **Gunakan namespacing yang bermakna dalam nama alat.** Ketika alat Anda mencakup beberapa layanan atau sumber daya, beri prefiks pada nama dengan sumber dayanya (misalnya, `db_query` atau `storage_read`). Ini membuat pemilihan alat tidak ambigu seiring bertambahnya pustaka alat Anda.
* **Rancang respons alat agar hanya mengembalikan informasi bernilai tinggi.** Kembalikan pengidentifikasi yang semantik dan stabil (misalnya, slug atau UUID) daripada referensi internal yang tidak jelas, dan sertakan hanya field yang dibutuhkan Claude untuk menalar langkah berikutnya. Respons yang membengkak membuang-buang konteks dan mempersulit Claude untuk mengekstrak hal yang penting.
