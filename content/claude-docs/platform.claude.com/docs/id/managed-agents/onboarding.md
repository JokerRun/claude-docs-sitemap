---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/onboarding
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 18d653f5688ca9cd77388f0946b9a4fc4d20392f2a7461c790b45e3a018065f6
---

# Prototipe di Console

Buat dan uji agen secara visual di Console tanpa menulis panggilan API.

---

[Console](https://platform.claude.com/workspaces/default/agent-quickstart/) menyediakan antarmuka visual untuk membuat dan mengonfigurasi agen. Ini menghasilkan sumber daya `/v1/agents` dan `/v1/sessions` yang sama seperti API tetapi memungkinkan Anda untuk mengulangi konfigurasi secara interaktif sebelum menulis kode.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

## Cara membangun agen

[Antarmuka visual](https://platform.claude.com/workspaces/default/agent-quickstart/) memandu Anda melalui setiap bidang dari definisi agen:

- **Model dan system prompt:** Pilih model dan tulis system prompt di editor lebar penuh.
- **Server MCP:** Tambahkan server MCP jarak jauh berdasarkan URL dan autentikasi agen Anda untuk mengambil tindakan atas nama Anda.
- **Tools:** Perluas kemampuan agen Anda menggunakan toolset agen pra-bangun dan alat MCP.
- **Skills:** Lampirkan skill Anthropic atau kustom dari perpustakaan organisasi Anda.

Saat Anda mengonfigurasi, Console menampilkan permintaan API yang setara sehingga Anda dapat menyalinnya ke dalam kode Anda setelah puas.

## Menguji agen

Console mencakup runner sesi inline. Setelah mengonfigurasi agen Anda, Anda dapat memulai sesi uji secara langsung, mengirim pesan, dan menonton aliran acara tanpa meninggalkan halaman. Ini adalah cara tercepat untuk memeriksa bahwa system prompt dan pemilihan tool Anda menghasilkan perilaku yang Anda harapkan.

## Dari prototipe ke kode

Setelah agen Anda berfungsi seperti yang diharapkan:

1. Salin ID agen dari output Console.
2. Referensikan dalam kode Anda saat [membuat sesi](/docs/id/managed-agents/sessions):

<CodeGroup>

```bash curl
session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{
    "agent": "agent_01J8XkN5uT3vHpLqRfWdY2",
    "environment_id": "env_01K2mPsT7hNwR4jXuLvCqD8",
    "title": "My first session"
  }')
```

```bash CLI
ant beta:sessions create \
  --agent agent_01J8XkN5uT3vHpLqRfWdY2 \
  --environment-id env_01K2mPsT7hNwR4jXuLvCqD8 \
  --title "My first session"
```

```python Python
session = client.beta.sessions.create(
    agent="agent_01J8XkN5uT3vHpLqRfWdY2",
    environment_id="env_01K2mPsT7hNwR4jXuLvCqD8",
    title="My first session",
)
```

```typescript TypeScript
const session = await client.beta.sessions.create({
  agent: "agent_01J8XkN5uT3vHpLqRfWdY2",
  environment_id: "env_01K2mPsT7hNwR4jXuLvCqD8",
  title: "My first session"
});
```

```csharp C#
var session = await client.Beta.Sessions.Create(new()
{
    Agent = "agent_01J8XkN5uT3vHpLqRfWdY2",
    EnvironmentID = "env_01K2mPsT7hNwR4jXuLvCqD8",
    Title = "My first session",
});
```

```go Go
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfBetaManagedAgentsAgents: &anthropic.BetaManagedAgentsAgentParams{
			Type:    anthropic.BetaManagedAgentsAgentParamsTypeAgent,
			ID:      "agent_01J8XkN5uT3vHpLqRfWdY2",
			Version: anthropic.Int(1),
		},
	},
	EnvironmentID: "env_01K2mPsT7hNwR4jXuLvCqD8",
	Title:         anthropic.String("My first session"),
})
if err != nil {
	panic(err)
}
_ = session
```

```java Java
var session = client.beta().sessions().create(
    SessionCreateParams.builder()
        .agent("agent_01J8XkN5uT3vHpLqRfWdY2")
        .environmentId("env_01K2mPsT7hNwR4jXuLvCqD8")
        .title("My first session")
        .build()
);
```

```php PHP
$session = $client->beta->sessions->create(
    agent: 'agent_01J8XkN5uT3vHpLqRfWdY2',
    environmentID: 'env_01K2mPsT7hNwR4jXuLvCqD8',
    title: 'My first session',
);
```

```ruby Ruby
session = client.beta.sessions.create(
  agent: "agent_01J8XkN5uT3vHpLqRfWdY2",
  environment_id: "env_01K2mPsT7hNwR4jXuLvCqD8",
  title: "My first session"
)
```
</CodeGroup>