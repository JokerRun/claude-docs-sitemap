---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/tools
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 76f760a95cd48a871a9a25fe7533ba3b5991ff46525e6d74b8045b61281cf23a
---

# Tools

Konfigurasikan tools yang tersedia untuk agen Anda.

---

Claude Managed Agents menyediakan sekumpulan tools bawaan yang dapat digunakan Claude secara otonom dalam sebuah sesi. Anda mengontrol tools mana yang tersedia dengan menentukannya dalam konfigurasi agen.

Tools kustom yang didefinisikan pengguna juga didukung. Aplikasi Anda mengeksekusi tools ini secara terpisah dan mengirimkan hasil tools kembali ke Claude; Claude dapat menggunakan hasilnya untuk melanjutkan tugas yang sedang dikerjakan.

<Note>
Semua permintaan API Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

## Tools yang tersedia

Toolset agen mencakup tools berikut. Semua diaktifkan secara default ketika Anda menyertakan toolset dalam konfigurasi agen Anda.

| Tool | Nama | Deskripsi |
|---|---|---|
| Bash | `bash` | Menjalankan perintah bash dalam sesi shell |
| Read | `read` | Membaca file dari filesystem lokal |
| Write | `write` | Menulis file ke filesystem lokal |
| Edit | `edit` | Melakukan penggantian string dalam sebuah file |
| Glob | `glob` | Pencocokan pola file cepat menggunakan pola glob |
| Grep | `grep` | Pencarian teks menggunakan pola regex |
| Web fetch | `web_fetch` | Mengambil konten dari URL |
| Web search | `web_search` | Mencari informasi di web |

## Mengonfigurasi toolset

Aktifkan toolset lengkap dengan `agent_toolset_20260401` saat membuat agen. Gunakan array `configs` untuk menonaktifkan tools tertentu atau mengganti pengaturannya.

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
  "model": "claude-sonnet-4-6",
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
model: claude-sonnet-4-6
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
    model="claude-sonnet-4-6",
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
  model: "claude-sonnet-4-6",
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
    Model = new("claude-sonnet-4-6"),
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
		ID:   "claude-sonnet-4-6",
		Type: anthropic.BetaManagedAgentsModelConfigParamsTypeModelConfig,
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
```

```java Java
var agent = client.beta().agents().create(AgentCreateParams.builder()
    .name("Coding Assistant")
    .model(BetaManagedAgentsModel.CLAUDE_SONNET_4_6)
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
    model: 'claude-sonnet-4-6',
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
  model: "claude-sonnet-4-6",
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

### Menonaktifkan tools tertentu

Untuk menonaktifkan sebuah tool, atur `enabled: false` dalam entri konfigurasinya:

```json
{
  "type": "agent_toolset_20260401",
  "configs": [
    { "name": "web_fetch", "enabled": false },
    { "name": "web_search", "enabled": false }
  ]
}
```

### Mengaktifkan hanya tools tertentu

Untuk memulai dengan semua dinonaktifkan dan hanya mengaktifkan yang Anda butuhkan, atur `default_config.enabled` ke `false`:

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

## Tools kustom

Selain tools bawaan, Anda dapat mendefinisikan tools kustom. Tools kustom analog dengan [tools klien yang didefinisikan pengguna](/docs/id/agents-and-tools/tool-use/how-tool-use-works#user-defined-tools-client-executed) dalam Messages API.

Tools kustom memungkinkan Anda memperluas kemampuan Claude untuk melakukan berbagai tugas yang lebih luas. Setiap tool mendefinisikan sebuah kontrak: Anda menentukan operasi apa yang tersedia dan apa yang dikembalikannya; Claude memutuskan kapan dan bagaimana memanggilnya. Model tidak pernah mengeksekusi apa pun sendiri. Model mengeluarkan permintaan terstruktur, kode Anda menjalankan operasi, dan hasilnya mengalir kembali ke dalam percakapan.

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
  "model": "claude-sonnet-4-6",
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
model: claude-sonnet-4-6
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
    model="claude-sonnet-4-6",
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
  model: "claude-sonnet-4-6",
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
    Model = new("claude-sonnet-4-6"),
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
		ID:   "claude-sonnet-4-6",
		Type: anthropic.BetaManagedAgentsModelConfigParamsTypeModelConfig,
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
```

```java Java
var agent = client.beta().agents().create(AgentCreateParams.builder()
    .name("Weather Agent")
    .model(BetaManagedAgentsModel.CLAUDE_SONNET_4_6)
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
    model: 'claude-sonnet-4-6',
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
  model: "claude-sonnet-4-6",
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

Setelah Anda mendefinisikan tool di tingkat agen, agen akan memanggil tools tersebut selama berlangsungnya sesi. Lihat [Aliran event sesi](/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) untuk alur lengkapnya.

### Praktik terbaik untuk definisi tools kustom

- **Berikan deskripsi yang sangat detail.** Ini adalah faktor terpenting dalam performa tool. Deskripsi Anda harus menjelaskan apa yang dilakukan tool, kapan harus digunakan (dan kapan tidak), apa arti setiap parameter dan bagaimana pengaruhnya terhadap perilaku tool, serta peringatan atau batasan penting apa pun. Semakin banyak konteks yang dapat Anda berikan kepada Claude tentang tools Anda, semakin baik Claude dalam memutuskan kapan dan bagaimana menggunakannya. Targetkan setidaknya 3-4 kalimat per deskripsi tool, lebih banyak jika toolnya kompleks.
- **Gabungkan operasi terkait ke dalam lebih sedikit tools.** Daripada membuat tool terpisah untuk setiap tindakan (`create_pr`, `review_pr`, `merge_pr`), kelompokkan menjadi satu tool dengan parameter `action`. Lebih sedikit tools yang lebih mampu mengurangi ambiguitas pemilihan dan membuat permukaan tool Anda lebih mudah dinavigasi oleh Claude.
- **Gunakan penamaan namespace yang bermakna dalam nama tools.** Ketika tools Anda mencakup beberapa layanan atau sumber daya, awali nama dengan sumber daya (misalnya, `db_query`, `storage_read`). Ini membuat pemilihan tool tidak ambigu seiring berkembangnya library Anda.
- **Rancang respons tool untuk mengembalikan hanya informasi yang bernilai tinggi.** Kembalikan pengidentifikasi semantik yang stabil (misalnya, slug atau UUID) daripada referensi internal yang tidak transparan, dan sertakan hanya field yang dibutuhkan Claude untuk mempertimbangkan langkah selanjutnya. Respons yang membengkak membuang konteks dan mempersulit Claude untuk mengekstrak hal yang penting.