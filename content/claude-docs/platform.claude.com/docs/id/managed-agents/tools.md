---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/tools
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: 518791c52829f0547f646192faa3f28b75e6ccda370b0b0fcce31bb20d5e73ba
---

# Alat

Konfigurasikan alat yang tersedia untuk agen Anda.

---

Claude Managed Agents menyediakan serangkaian alat bawaan yang dapat digunakan Claude secara otonom dalam sebuah [sesi](/docs/id/managed-agents/sessions). Anda mengontrol alat mana yang tersedia dengan menentukannya dalam konfigurasi agen.

Claude Managed Agents juga mendukung alat kustom yang didefinisikan pengguna. Aplikasi Anda mengeksekusi alat-alat ini secara terpisah dan mengembalikan hasilnya ke Claude, yang kemudian menggunakannya untuk melanjutkan tugas. Untuk memberikan agen alat dari server MCP, gunakan [konektor MCP](/docs/id/managed-agents/mcp-connector) sebagai gantinya.

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Alat yang tersedia

Toolset agen mencakup alat-alat berikut. Semuanya diaktifkan secara default ketika Anda menyertakan toolset dalam konfigurasi agen Anda. Gunakan nilai di kolom Nama untuk mereferensikan alat dalam array `configs`.

| Alat       | Nama         | Deskripsi                                        |
| ---------- | ------------ | ------------------------------------------------ |
| Bash       | `bash`       | Mengeksekusi perintah bash dalam sesi shell      |
| Read       | `read`       | Membaca file dari filesystem sandbox             |
| Write      | `write`      | Menulis file ke filesystem sandbox               |
| Edit       | `edit`       | Melakukan penggantian string dalam file          |
| Glob       | `glob`       | Pencocokan pola file cepat menggunakan pola glob |
| Grep       | `grep`       | Pencarian teks menggunakan pola regex            |
| Web fetch  | `web_fetch`  | Mengambil konten dari URL                        |
| Web search | `web_search` | Mencari informasi di web                         |

Ketika output alat melebihi 100.000 token, output tersebut secara otomatis ditulis ke file dalam [sandbox](/docs/id/managed-agents/environments). Model menerima pratinjau yang dipotong beserta path file dan dapat membaca konten lengkapnya dari sana.

## Mengonfigurasi toolset

Aktifkan toolset lengkap dengan `agent_toolset_20260401` saat membuat agen. Gunakan array `configs` untuk menonaktifkan alat tertentu atau mengganti pengaturannya. Setiap entri config juga dapat menetapkan `permission_policy` yang mengontrol apakah panggilan alat disetujui secara otomatis atau memerlukan konfirmasi. Lihat [Kebijakan izin](/docs/id/managed-agents/permission-policies) untuk jenis kebijakan yang tersedia.

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
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;

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

Untuk menonaktifkan alat, tetapkan `enabled: false` dalam entri config-nya di objek toolset pada array `tools` agen Anda:

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

Objek `default_config` menetapkan baseline untuk setiap alat dalam set, dan entri `configs` per-alat akan menggantinya. Untuk memulai dengan semuanya nonaktif dan hanya mengaktifkan yang Anda butuhkan, tetapkan `default_config.enabled` ke `false`:

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

Selain alat bawaan, Anda dapat mendefinisikan alat kustom. Alat kustom analog dengan [alat klien yang didefinisikan pengguna](/docs/id/agents-and-tools/tool-use/how-tool-use-works#user-defined-tools-client-executed) di Messages API.

Setiap alat kustom mendefinisikan sebuah kontrak: Anda menentukan operasi apa yang tersedia dan apa yang dikembalikannya, dan Claude menentukan kapan dan bagaimana memanggilnya. Model tidak pernah mengeksekusi apa pun sendiri. Model mengeluarkan permintaan terstruktur, kode Anda menjalankan operasi tersebut, dan hasilnya mengalir kembali ke dalam percakapan. Lihat [Aliran event sesi](/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) untuk cara menerima panggilan alat kustom dan mengembalikan hasil selama sesi.

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

Setelah Anda mendefinisikan alat kustom pada agen, agen akan memanggilnya selama sesi.

### Praktik terbaik untuk definisi alat kustom

* **Berikan deskripsi yang sangat detail.** Ini adalah faktor terpenting dalam performa alat. Deskripsi Anda harus menjelaskan apa yang dilakukan alat dan kapan menggunakannya (dan kapan tidak). Jelaskan apa arti setiap parameter dan bagaimana pengaruhnya terhadap perilaku alat. Sebutkan peringatan atau batasan penting apa pun. Semakin banyak konteks yang dapat Anda berikan kepada Claude tentang alat Anda, semakin baik Claude dalam menentukan kapan dan bagaimana menggunakannya. Targetkan tiga hingga empat kalimat untuk setiap deskripsi alat, lebih banyak jika alatnya kompleks.
* **Konsolidasikan operasi terkait ke dalam lebih sedikit alat.** Daripada membuat alat terpisah untuk setiap tindakan (`create_pr`, `review_pr`, `merge_pr`), kelompokkan ke dalam satu alat dengan parameter `action`. Alat yang lebih sedikit namun lebih mumpuni mengurangi ambiguitas pemilihan dan membuat kumpulan alat Anda lebih mudah dinavigasi oleh Claude.
* **Gunakan namespacing yang bermakna dalam nama alat.** Ketika alat Anda mencakup beberapa layanan atau sumber daya, beri prefiks nama dengan sumber daya tersebut (misalnya, `db_query` atau `storage_read`). Ini membuat pemilihan alat tidak ambigu seiring bertambahnya pustaka Anda.
* **Rancang respons alat agar hanya mengembalikan informasi bernilai tinggi.** Kembalikan pengidentifikasi yang semantik dan stabil (misalnya, slug atau UUID) daripada referensi internal yang tidak jelas, dan sertakan hanya field yang dibutuhkan Claude untuk menentukan langkah berikutnya. Respons yang membengkak memboroskan konteks dan mempersulit Claude untuk mengekstrak apa yang penting.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Konektor MCP" icon="link" href="/docs/id/managed-agents/mcp-connector">
    Hubungkan server MCP ke agen Anda untuk akses ke alat eksternal dan sumber data.
  </Card>

  <Card title="Kebijakan izin" icon="lock" href="/docs/id/managed-agents/permission-policies">
    Kontrol kapan alat agen dan MCP dieksekusi.
  </Card>

  <Card title="Aliran event sesi" icon="lightning" href="/docs/id/managed-agents/events-and-streaming">
    Kirim event, stream respons, dan interupsi atau arahkan ulang sesi Anda di tengah eksekusi.
  </Card>
</CardGroup>
