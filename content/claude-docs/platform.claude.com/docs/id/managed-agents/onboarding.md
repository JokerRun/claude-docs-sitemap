---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/onboarding
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 5a2c0283cf04f010dae58062ff383289fb8a668701503c0be3de18c443e67c59
---

---
title: Membangun di Console
url: https://platform.claude.com/docs/id/managed-agents/onboarding
description: Buat, uji, dan iterasi agen secara visual di Console, lalu jalankan dari kode Anda dengan API.
---

[Console](https://platform.claude.com/workspaces/default/agent-quickstart/) menyediakan antarmuka visual untuk membuat dan mengonfigurasi agen. Console memungkinkan Anda melakukan iterasi konfigurasi secara interaktif sebelum menulis kode.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK menetapkan header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Cara membangun agen

[Antarmuka visual](https://platform.claude.com/workspaces/default/agent-quickstart/) memandu Anda melalui setiap bidang dalam definisi agen:

* **Model dan prompt sistem:** Pilih model dan tulis "system prompt" (prompt sistem) di editor lebar penuh.
* **Server MCP:** Tambahkan server MCP jarak jauh melalui URL dan autentikasi agen Anda agar dapat mengambil tindakan atas nama Anda.
* **Alat:** Perluas kemampuan agen Anda menggunakan toolset agen bawaan dan alat MCP.
* **Skills:** Lampirkan skill Anthropic atau skill kustom dari pustaka organisasi Anda.

Saat Anda mengonfigurasi, Console menampilkan permintaan API yang setara sehingga Anda dapat menyalinnya ke kode Anda setelah Anda puas.

## Menguji agen

Console menyertakan session runner inline. Setelah mengonfigurasi agen Anda, Anda dapat memulai sesi pengujian secara langsung, mengirim pesan, dan memantau aliran event tanpa meninggalkan halaman. Ini adalah cara tercepat untuk memeriksa bahwa prompt sistem dan pilihan alat Anda menghasilkan perilaku yang Anda harapkan.

## Dari Console ke codebase Anda

Setelah agen Anda berfungsi sesuai harapan:

1. Salin ID agen dan [ID environment](https://platform.claude.com/docs/id/managed-agents/environments) dari Console.
2. Referensikan keduanya dalam kode Anda saat [membuat sesi](https://platform.claude.com/docs/id/managed-agents/sessions):

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
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
