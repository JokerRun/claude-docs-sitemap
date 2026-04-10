---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/onboarding
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: bd4cf4dc8ee88dff4b286885fa45820735fbbb63252e8207c9f72cf3c81aef9e
---

# Prototipe di Console

Buat dan uji agen secara visual di Console tanpa menulis panggilan API.

---

[Console](https://platform.claude.com/workspaces/default/agent-quickstart/) menyediakan antarmuka visual untuk membuat dan mengonfigurasi agen. Ini menghasilkan sumber daya `/v1/agents` dan `/v1/sessions` yang sama seperti API tetapi memungkinkan Anda untuk mengulangi konfigurasi secara interaktif sebelum menulis kode.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK mengatur header beta secara otomatis.
</Note>

## Cara membangun agen

[Antarmuka visual](https://platform.claude.com/workspaces/default/agent-quickstart/) memandu Anda melalui setiap bidang dari definisi agen:

- **Model dan system prompt:** Pilih model dan tulis system prompt di editor lebar penuh.
- **Server MCP:** Tambahkan server MCP jarak jauh berdasarkan URL dan autentikasi agen Anda untuk mengambil tindakan atas nama Anda.
- **Tools:** Perluas kemampuan agen Anda menggunakan toolset agen pra-bangun dan tools MCP.
- **Skills:** Lampirkan skills Anthropic atau kustom dari perpustakaan organisasi Anda.

Saat Anda mengonfigurasi, Console menampilkan permintaan API yang setara sehingga Anda dapat menyalinnya ke dalam kode Anda setelah Anda puas.

## Menguji agen

Console mencakup runner sesi inline. Setelah mengonfigurasi agen Anda, Anda dapat memulai sesi pengujian secara langsung, mengirim pesan, dan menonton aliran acara tanpa meninggalkan halaman. Ini adalah cara tercepat untuk memeriksa bahwa system prompt dan pemilihan tool Anda menghasilkan perilaku yang Anda harapkan.

## Dari prototipe ke kode

Setelah agen Anda bekerja seperti yang diharapkan:

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
    "agent": "agent_01XXXXXXXXXXXXXXXXXXXXXX",
    "environment_id": "env_01XXXXXXXXXXXXXXXXXXXXXX",
    "title": "My first session"
  }')
```

```bash CLI
ant beta:sessions create \
  --agent agent_01XXXXXXXXXXXXXXXXXXXXXX \
  --environment env_01XXXXXXXXXXXXXXXXXXXXXX \
  --title "My first session"
```

```python Python
session = client.beta.sessions.create(
    agent="agent_01XXXXXXXXXXXXXXXXXXXXXX",
    environment_id="env_01XXXXXXXXXXXXXXXXXXXXXX",
    title="My first session",
)
```

```typescript TypeScript
const session = await client.beta.sessions.create({
  agent: "agent_01XXXXXXXXXXXXXXXXXXXXXX",
  environment_id: "env_01XXXXXXXXXXXXXXXXXXXXXX",
  title: "My first session"
});
```

```csharp C#
var session = await client.Beta.Sessions.Create(new()
{
    Agent = "agent_01XXXXXXXXXXXXXXXXXXXXXX",
    EnvironmentID = "env_01XXXXXXXXXXXXXXXXXXXXXX",
    Title = "My first session",
});
```

```go Go
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfBetaManagedAgentsAgents: &anthropic.BetaManagedAgentsAgentParams{
			Type:    anthropic.BetaManagedAgentsAgentParamsTypeAgent,
			ID:      "agent_01XXXXXXXXXXXXXXXXXXXXXX",
			Version: anthropic.Int(1),
		},
	},
	EnvironmentID: "env_01XXXXXXXXXXXXXXXXXXXXXX",
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
        .agent("agent_01XXXXXXXXXXXXXXXXXXXXXX")
        .environmentId("env_01XXXXXXXXXXXXXXXXXXXXXX")
        .title("My first session")
        .build()
);
```

```php PHP
$session = $client->beta->sessions->create(
    agent: 'agent_01XXXXXXXXXXXXXXXXXXXXXX',
    environmentID: 'env_01XXXXXXXXXXXXXXXXXXXXXX',
    title: 'My first session',
);
```

```ruby Ruby
session = client.beta.sessions.create(
  agent: "agent_01XXXXXXXXXXXXXXXXXXXXXX",
  environment_id: "env_01XXXXXXXXXXXXXXXXXXXXXX",
  title: "My first session"
)
```
</CodeGroup>