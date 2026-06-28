---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/onboarding
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 5cb47bacfc624dd9dd1bd79b9412f4af5ae216395d93a434ab234ff938e40d1d
---

# Membuat prototipe di Console

Buat dan uji agen secara visual di Console tanpa menulis panggilan API.

---

[Console](https://platform.claude.com/workspaces/default/agent-quickstart/) menyediakan antarmuka visual untuk membuat dan mengonfigurasi agen. Antarmuka ini memungkinkan Anda melakukan iterasi pada konfigurasi secara interaktif sebelum menulis kode.

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Cara membangun agen

[Antarmuka visual](https://platform.claude.com/workspaces/default/agent-quickstart/) memandu Anda melalui setiap bidang dari definisi agen:

* **Model dan prompt sistem:** Pilih model dan tulis prompt sistem dalam editor lebar penuh.
* **Server MCP:** Tambahkan server MCP jarak jauh melalui URL dan autentikasi agen Anda untuk mengambil tindakan atas nama Anda.
* **Alat:** Perluas kemampuan agen Anda menggunakan kumpulan alat agen yang telah dibuat sebelumnya dan alat MCP.
* **Skill:** Lampirkan skill Anthropic atau skill kustom dari pustaka organisasi Anda.

Saat Anda mengonfigurasi, Console menampilkan permintaan API yang setara sehingga Anda dapat menyalinnya ke dalam kode Anda setelah Anda puas.

## Menguji agen

Console menyertakan "session runner" (pelaksana sesi) inline. Setelah mengonfigurasi agen Anda, Anda dapat langsung memulai sesi pengujian, mengirim pesan, dan mengamati aliran event tanpa meninggalkan halaman. Ini adalah cara tercepat untuk memeriksa bahwa prompt sistem dan pemilihan alat Anda menghasilkan perilaku yang Anda harapkan.

## Dari prototipe ke kode

Setelah agen Anda berfungsi sesuai harapan:

1. Salin ID agen dan [ID environment](/docs/id/managed-agents/environments) dari Console.
2. Referensikan keduanya dalam kode Anda saat [membuat sesi](/docs/id/managed-agents/sessions):

<CodeGroup defaultLanguage="CLI">
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
  		OfString: anthropic.String("agent_01J8XkN5uT3vHpLqRfWdY2"),
  	},
  	EnvironmentID: "env_01K2mPsT7hNwR4jXuLvCqD8",
  	Title:         anthropic.String("My first session"),
  })
  if err != nil {
  	panic(err)
  }
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
