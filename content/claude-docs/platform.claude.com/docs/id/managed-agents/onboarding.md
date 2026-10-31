---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/onboarding
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 143600c6d81867aff18678f0dacf9c1bd4b8a3aecbd004571c8657c473574d5f
---

---
title: Membangun di Console
url: https://platform.claude.com/docs/id/managed-agents/onboarding
description: Buat, uji, dan iterasi agen secara visual di Claude Console, lalu jalankan dari kode Anda dengan API.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. Berlaku untuk semua subfitur Managed Agents, termasuk Sandbox yang di-host sendiri.
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
---

[Claude Console](https://platform.claude.com/workspaces/default/agent-quickstart/) menyediakan antarmuka visual untuk membuat dan mengonfigurasi agen. Antarmuka ini memungkinkan Anda melakukan iterasi konfigurasi secara interaktif sebelum menulis kode.

## Cara membangun agen

[Antarmuka visual](https://platform.claude.com/workspaces/default/agent-quickstart/) di Claude Console memandu Anda melalui setiap kolom definisi agen:

* **Model dan prompt sistem:** Pilih model dan tulis “system prompt” (prompt sistem) di editor lebar penuh.
* **Server MCP:** Tambahkan server MCP jarak jauh melalui URL dan autentikasi agen Anda agar dapat mengambil tindakan atas nama Anda.
* **Alat:** Perluas kemampuan agen Anda menggunakan toolset agen bawaan dan alat MCP.
* **Skills:** Lampirkan skill Anthropic atau skill kustom dari pustaka organisasi Anda.

Saat Anda mengonfigurasi, Console menampilkan permintaan API yang setara sehingga Anda dapat menyalinnya ke kode Anda setelah Anda puas.

## Menguji agen

Console menyertakan session runner inline. Setelah mengonfigurasi agen Anda, Anda dapat memulai sesi pengujian secara langsung, mengirim pesan, dan memantau aliran event tanpa meninggalkan halaman. Ini adalah cara tercepat untuk memeriksa bahwa prompt sistem dan pilihan alat Anda menghasilkan perilaku yang Anda harapkan.

## Dari Console ke basis kode Anda

Setelah agen Anda berfungsi sesuai harapan:

1. Salin ID agen dan [ID environment](https://platform.claude.com/docs/id/managed-agents/environments) dari Console.
2. Referensikan keduanya dalam kode Anda saat [membuat sesi](https://platform.claude.com/docs/id/managed-agents/sessions):

<CodeGroup>
  ```bash cURL
  curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "agent": "agent_01J8XkN5uT3vHpLqRfWdY2",
      "environment_id": "env_01K2mPsT7hNwR4jXuLvCqD8",
      "title": "My first session"
    }'
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

## Ketersediaan

Pembuat agen Console dalam versi beta di semua model.

### Dukungan API

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tersedia

| Status | Platform cloud                                                                                                     |
| ------ | ------------------------------------------------------------------------------------------------------------------ |
| Beta   | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

### Header beta yang diperlukan

[Ikhtisar header beta](https://platform.claude.com/docs/id/api/beta-headers)

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

* `managed-agents-2026-04-01`

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                          | HIPAA                                                                               |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Status | Tidak layak                                                                                                                                                               | Tidak layak                                                                         |
| Detail | Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. Berlaku untuk semua subfitur Managed Agents, termasuk Sandbox yang di-host sendiri. | Berlaku untuk semua subfitur Managed Agents, termasuk Sandbox yang di-host sendiri. |

Endpoint yang berlaku:

* `/v1/agents`
* `/v1/sessions`
* `/v1/environments`
