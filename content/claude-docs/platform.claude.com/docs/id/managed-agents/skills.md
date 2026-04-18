---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/skills
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: a21c5f31d2b014f43fd50631322bba4252f2183466c42e18a9b46d1df64d76d6
---

# Keterampilan

Lampirkan keahlian berbasis sistem file yang dapat digunakan kembali ke agen Anda untuk alur kerja khusus domain.

---

Keterampilan adalah sumber daya berbasis sistem file yang dapat digunakan kembali dan memberikan agen Anda keahlian khusus domain: alur kerja, konteks, dan praktik terbaik yang mengubah agen tujuan umum menjadi spesialis. Tidak seperti prompt (instruksi tingkat percakapan untuk tugas sekali jadi), keterampilan dimuat sesuai permintaan, hanya berdampak pada jendela konteks saat diperlukan.

Dua jenis keterampilan didukung. Keduanya bekerja dengan cara yang sama: agen Anda menginvokasinya secara otomatis ketika relevan dengan tugas.

- **Keterampilan Anthropic pra-bangun:** Tugas dokumen umum seperti penanganan PowerPoint, Excel, Word, dan PDF.
- **Keterampilan khusus:** Keterampilan yang Anda buat dan unggah ke organisasi Anda.

Untuk mempelajari cara membuat keterampilan khusus, lihat [gambaran umum Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) dan [praktik terbaik](/docs/id/agents-and-tools/agent-skills/best-practices). Halaman ini mengasumsikan Anda sudah memiliki keterampilan yang tersedia di organisasi Anda atau menggunakan keterampilan pra-bangun Anthropic.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

## Aktifkan keterampilan pada sesi

Lampirkan keterampilan saat membuat agen. Maksimum 20 keterampilan per sesi didukung - ini mencakup keterampilan di semua agen untuk sesi, jika Anda bekerja dengan [beberapa agen](/docs/id/managed-agents/multi-agent).

<CodeGroup>
```bash curl
agent=$(curl -sS https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  --json @- <<'EOF'
{
  "name": "Financial Analyst",
  "model": "claude-opus-4-7",
  "system": "You are a financial analysis agent.",
  "skills": [
    {"type": "anthropic", "skill_id": "xlsx"},
    {"type": "custom", "skill_id": "skill_abc123", "version": "latest"}
  ]
}
EOF
)
```

```bash CLI
ant beta:agents create <<'YAML'
name: Financial Analyst
model: claude-opus-4-7
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
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
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
    Model = BetaManagedAgentsModel.ClaudeOpus4_7,
    System = "You are a financial analysis agent.",
    Skills =
    [
        new BetaManagedAgentsAnthropicSkillParams { Type = "anthropic", SkillID = "xlsx" },
        new BetaManagedAgentsCustomSkillParams { Type = "custom", SkillID = "skill_abc123", Version = "latest" },
    ],
});
```

```go Go
agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
	Name: "Financial Analyst",
	Model: anthropic.BetaManagedAgentsModelConfigParams{
		ID:   "claude-opus-4-7",
		Type: anthropic.BetaManagedAgentsModelConfigParamsTypeModelConfig,
	},
	System: anthropic.String("You are a financial analysis agent."),
	Skills: []anthropic.ManagedAgentsSkillParamUnion{
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
```

```java Java
var agent = client.beta().agents().create(
    AgentCreateParams.builder()
        .name("Financial Analyst")
        .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_7)
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
    model: 'claude-opus-4-7',
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
  model: "claude-opus-4-7",
  system_: "You are a financial analysis agent.",
  skills: [
    {type: "anthropic", skill_id: "xlsx"},
    {type: "custom", skill_id: "skill_abc123", version: "latest"}
  ]
)
```
</CodeGroup>

## Jenis keterampilan

| Bidang | Deskripsi |
| --- | --- |
| `type` | Baik `anthropic` untuk keterampilan pra-bangun atau `custom` untuk keterampilan yang dibuat organisasi. |
| `skill_id` | Pengenal keterampilan. Untuk keterampilan Anthropic, gunakan nama pendek (misalnya, `xlsx`). Untuk keterampilan khusus, gunakan ID `skill_*` yang dikembalikan saat pembuatan. |
| `version` | Keterampilan khusus saja. Sematkan ke versi tertentu atau gunakan `latest`. |