---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/skills
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 00850f2fb29d90ab315b86d17cec768a78c1b6b50613f3ada0bf7461960bcd61
---

# Skills

Lampirkan keahlian berbasis sistem file yang dapat digunakan kembali ke agen Anda untuk alur kerja spesifik domain.

---

"Skills" (keterampilan) adalah sumber daya berbasis sistem file yang dapat digunakan kembali dan memberikan keahlian spesifik domain kepada agen Anda: alur kerja, konteks, dan praktik terbaik yang mengubah agen serbaguna menjadi spesialis. Tidak seperti prompt (instruksi tingkat percakapan untuk tugas sekali pakai), skills dimuat sesuai kebutuhan, dan hanya memengaruhi jendela konteks saat diperlukan.

Anda dapat melampirkan dua jenis skill. Keduanya bekerja dengan cara yang sama: agen Anda memanggilnya secara otomatis ketika relevan dengan tugas.

- **Skill bawaan Anthropic:** Tugas dokumen umum seperti penanganan PowerPoint, Excel, Word, dan PDF.
- **Skill kustom:** Skill yang Anda buat dan unggah ke workspace Anda.

Untuk mempelajari cara membuat skill kustom, lihat [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) dan [Praktik terbaik pembuatan skill](/docs/id/agents-and-tools/agent-skills/best-practices). Halaman ini mengasumsikan Anda sudah memiliki skill yang tersedia di workspace Anda atau menggunakan skill bawaan Anthropic.

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Melampirkan skill ke agen \{#attach-skills-to-an-agent}

Lampirkan skill saat membuat agen. Setiap sesi mendukung hingga 20 skill secara total, dihitung di seluruh agen dalam sesi tersebut (lihat [Sesi multiagen](/docs/id/managed-agents/multi-agent)).

Setiap entri dalam array `skills` menggunakan field berikut:

| Field | Deskripsi |
| --- | --- |
| `type` | Bernilai `anthropic` untuk skill bawaan atau `custom` untuk skill yang dibuat di workspace. |
| `skill_id` | Pengidentifikasi skill. Untuk skill Anthropic, gunakan nama pendek (misalnya, `xlsx`). Untuk skill kustom, gunakan ID `skill_*` yang dikembalikan saat pembuatan. |
| `version` | Hanya untuk skill kustom. Tetapkan ke versi tertentu atau gunakan `latest`. |

<CodeGroup defaultLanguage="CLI">
```bash curl
agent=$(curl -sS https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  --json @- <<'EOF'
{
  "name": "Financial Analyst",
  "model": "claude-opus-4-8",
  "system": "You are a financial analysis agent.",
  "skills": [
    {"type": "anthropic", "skill_id": "xlsx"},
    {"type": "custom", "skill_id": "skill_abc123", "version": "latest"}
  ]
}
EOF
)
```

```bash CLI nocheck
ant beta:agents create <<'YAML'
name: Financial Analyst
model: claude-opus-4-8
system: You are a financial analysis agent.
skills:
  - type: anthropic
    skill_id: xlsx
  - type: custom
    skill_id: skill_abc123
    version: latest
YAML
```

```python Python
agent = client.beta.agents.create(
    name="Financial Analyst",
    model="claude-opus-4-8",
    system="You are a financial analysis agent.",
    skills=[
        {
            "type": "anthropic",
            "skill_id": "xlsx",
        },
        {
            "type": "custom",
            "skill_id": "skill_abc123",
            "version": "latest",
        },
    ],
)
```

```typescript TypeScript
const agent = await client.beta.agents.create({
  name: "Financial Analyst",
  model: "claude-opus-4-8",
  system: "You are a financial analysis agent.",
  skills: [
    {
      type: "anthropic",
      skill_id: "xlsx"
    },
    {
      type: "custom",
      skill_id: "skill_abc123",
      version: "latest"
    }
  ]
});
```

```csharp C#
var agent = await client.Beta.Agents.Create(new()
{
    Name = "Financial Analyst",
    Model = BetaManagedAgentsModel.ClaudeOpus4_8,
    System = "You are a financial analysis agent.",
    Skills =
    [
        new BetaManagedAgentsAnthropicSkillParams { Type = BetaManagedAgentsAnthropicSkillParamsType.Anthropic, SkillID = "xlsx" },
        new BetaManagedAgentsCustomSkillParams { Type = BetaManagedAgentsCustomSkillParamsType.Custom, SkillID = "skill_abc123", Version = "latest" },
    ],
});
```

```go Go nocheck
agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name: "Financial Analyst",
	Model: anthropic.BetaManagedAgentsModelConfigParams{
		ID: "claude-opus-4-8",
	},
	System: anthropic.String("You are a financial analysis agent."),
	Skills: []anthropic.BetaManagedAgentsSkillParamsUnion{
		{OfAnthropic: &anthropic.BetaManagedAgentsAnthropicSkillParams{
			SkillID: "xlsx",
			Type:    anthropic.BetaManagedAgentsAnthropicSkillParamsTypeAnthropic,
		}},
		{OfCustom: &anthropic.BetaManagedAgentsCustomSkillParams{
			SkillID: "skill_abc123",
			Type:    anthropic.BetaManagedAgentsCustomSkillParamsTypeCustom,
			Version: anthropic.String("latest"),
		}},
	},
})
if err != nil {
	panic(err)
}
_ = agent
```

```java Java
var agent = client.beta().agents().create(
    AgentCreateParams.builder()
        .name("Financial Analyst")
        .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
        .system("You are a financial analysis agent.")
        .addSkill(
            BetaManagedAgentsAnthropicSkillParams.builder()
                .type(BetaManagedAgentsAnthropicSkillParams.Type.ANTHROPIC)
                .skillId("xlsx")
                .build()
        )
        .addSkill(
            BetaManagedAgentsCustomSkillParams.builder()
                .type(BetaManagedAgentsCustomSkillParams.Type.CUSTOM)
                .skillId("skill_abc123")
                .version("latest")
                .build()
        )
        .build()
);
```

```php PHP
$agent = $client->beta->agents->create(
    name: 'Financial Analyst',
    model: 'claude-opus-4-8',
    system: 'You are a financial analysis agent.',
    skills: [
        ['type' => 'anthropic', 'skill_id' => 'xlsx'],
        ['type' => 'custom', 'skill_id' => 'skill_abc123', 'version' => 'latest'],
    ],
);
```

```ruby Ruby
agent = client.beta.agents.create(
  name: "Financial Analyst",
  model: "claude-opus-4-8",
  system_: "You are a financial analysis agent.",
  skills: [
    {type: "anthropic", skill_id: "xlsx"},
    {type: "custom", skill_id: "skill_abc123", version: "latest"}
  ]
)
```
</CodeGroup>