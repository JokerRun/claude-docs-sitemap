---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/tools
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 1edd0ea70df6c7d306603ec79398c8a97e36035186c6dcba841d45b1de918778
---

# Alat

Konfigurasi alat yang tersedia untuk agen Anda.

---

Claude Managed Agents menyediakan serangkaian alat bawaan yang dapat digunakan Claude secara otonom dalam sesi. Anda mengontrol alat mana yang tersedia dengan menentukan alat tersebut dalam konfigurasi agen.

Alat khusus yang ditentukan pengguna juga didukung. Aplikasi Anda menjalankan alat ini secara terpisah dan mengirimkan hasil alat kembali ke Claude; Claude dapat menggunakan hasil untuk melanjutkan tugas yang sedang berlangsung.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

## Alat yang tersedia

Set alat agen mencakup alat berikut. Semua diaktifkan secara default ketika Anda menyertakan set alat dalam konfigurasi agen Anda.

| Alat | Nama | Deskripsi |
|---|---|---|
| Bash | `bash` | Jalankan perintah bash dalam sesi shell |
| Baca | `read` | Baca file dari sistem file lokal |
| Tulis | `write` | Tulis file ke sistem file lokal |
| Edit | `edit` | Lakukan penggantian string dalam file |
| Glob | `glob` | Pencocokan pola file cepat menggunakan pola glob |
| Grep | `grep` | Pencarian teks menggunakan pola regex |
| Pengambilan web | `web_fetch` | Ambil konten dari URL |
| Pencarian web | `web_search` | Cari web untuk informasi |

## Mengonfigurasi set alat

Aktifkan set alat lengkap dengan `agent_toolset_20260401` saat membuat agen. Gunakan array `configs` untuk menonaktifkan alat tertentu atau mengganti pengaturan mereka.

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
  "model": "claude-opus-4-7",
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
model: claude-opus-4-7
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
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
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
    Model = new("claude-opus-4-7"),
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
		ID:   "claude-opus-4-7",
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
    .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_7)
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
    model: 'claude-opus-4-7',
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
  model: "claude-opus-4-7",
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

Untuk menonaktifkan alat, atur `enabled: false` dalam entri konfigurasinya:

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

Untuk memulai dengan semuanya dimatikan dan mengaktifkan hanya apa yang Anda butuhkan, atur `default_config.enabled` ke `false`:

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

## Alat khusus

Selain alat bawaan, Anda dapat menentukan alat khusus. Alat khusus analog dengan [alat yang ditentukan pengguna yang dijalankan klien](/docs/id/agents-and-tools/tool-use/how-tool-use-works#user-defined-tools-client-executed) dalam Messages API.

Alat khusus memungkinkan Anda memperluas kemampuan Claude untuk melakukan berbagai tugas. Setiap alat mendefinisikan kontrak: Anda menentukan operasi apa yang tersedia dan apa yang mereka kembalikan; Claude memutuskan kapan dan bagaimana memanggilnya. Model tidak pernah menjalankan apa pun sendiri. Ini mengeluarkan permintaan terstruktur, kode Anda menjalankan operasi, dan hasilnya mengalir kembali ke percakapan.

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
  "model": "claude-opus-4-7",
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
model: claude-opus-4-7
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
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
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
    Model = new("claude-opus-4-7"),
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
		ID:   "claude-opus-4-7",
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
    .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_7)
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
    model: 'claude-opus-4-7',
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
  model: "claude-opus-4-7",
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

Setelah Anda menentukan alat di tingkat agen, agen akan memanggil alat selama sesi. Lihat [Aliran acara sesi](/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) untuk alur lengkapnya.

### Praktik terbaik untuk definisi alat khusus

- **Berikan deskripsi yang sangat detail.** Ini adalah faktor paling penting dalam kinerja alat. Deskripsi Anda harus menjelaskan apa yang dilakukan alat, kapan alat harus digunakan (dan kapan tidak), apa arti setiap parameter dan bagaimana hal itu mempengaruhi perilaku alat, dan peringatan atau batasan penting apa pun. Semakin banyak konteks yang dapat Anda berikan Claude tentang alat Anda, semakin baik dalam memutuskan kapan dan bagaimana menggunakannya. Targetkan setidaknya 3-4 kalimat per deskripsi alat, lebih banyak jika alat tersebut kompleks.
- **Konsolidasikan operasi terkait ke dalam lebih sedikit alat.** Daripada membuat alat terpisah untuk setiap tindakan (`create_pr`, `review_pr`, `merge_pr`), kelompokkan mereka ke dalam satu alat dengan parameter `action`. Lebih sedikit alat yang lebih mampu mengurangi ambiguitas pemilihan dan membuat permukaan alat Anda lebih mudah dinavigasi oleh Claude.
- **Gunakan penamaan namespace yang bermakna dalam nama alat.** Ketika alat Anda mencakup beberapa layanan atau sumber daya, awali nama dengan sumber daya (misalnya, `db_query`, `storage_read`). Ini membuat pemilihan alat tidak ambigu saat perpustakaan Anda berkembang.
- **Desain respons alat untuk mengembalikan hanya informasi sinyal tinggi.** Kembalikan pengidentifikasi semantik yang stabil (misalnya, slug atau UUID) daripada referensi internal yang buram, dan sertakan hanya bidang yang Claude butuhkan untuk bernalar tentang langkah berikutnya. Respons yang membengkak membuang konteks dan membuat lebih sulit bagi Claude untuk mengekstrak apa yang penting.