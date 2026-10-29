---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/session-operations
fetched_at: 2026-10-29T02:15:48.406163Z
sha256: 68bf786ac52cac68dda1dcddfbc1902e042a3190784fa27cc4abf62496e273bf
---

---
title: Operasi sesi
url: https://platform.claude.com/docs/id/managed-agents/session-operations
description: Mengambil, mendaftar, memperbarui, mengarsipkan, dan menghapus sesi Claude Managed Agents.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Sessions are stateful resources; transcripts persist until you delete them. Applies to all Managed Agents sub-features, including Self-hosted sandboxes.
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
    Claude Models on Google Cloud (Anthropic managed): beta
---

Setelah sebuah sesi ada, gunakan operasi-operasi ini untuk membaca, memperbarui, mengarsipkan, atau menghapusnya. Lihat [Memulai sesi](https://platform.claude.com/docs/id/managed-agents/sessions) untuk membuat sesi dan mengirimkan pekerjaan kepadanya.

## Status sesi

Sesi berkembang melalui status-status berikut. Lihat [Memulai sesi](https://platform.claude.com/docs/id/managed-agents/sessions) untuk siklus hidup sesi.

| Status         | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `idle`         | Agen sedang menunggu input, termasuk pesan pengguna atau konfirmasi alat. Sesi yang dibuat tanpa `initial_events` (java, php: `initialEvents`; csharp, go: `InitialEvents`) dimulai dalam status `idle`. Sesi dapat berstatus `idle` saat sebuah [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs#while-a-run-is-open) masih terbuka, sehingga `idle` saja tidak berarti pekerjaan telah selesai. Lihat [Mengetahui kapan pekerjaan selesai](https://platform.claude.com/docs/id/managed-agents/workflow-runs#know-when-the-work-is-done). |
| `running`      | Agen sedang aktif mengeksekusi.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `rescheduling` | Terjadi kesalahan sementara, mencoba ulang secara otomatis.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `terminated`   | Sesi telah berakhir, baik karena kesalahan yang tidak dapat dipulihkan atau karena telah diarsipkan. Sesi yang menyelesaikan pekerjaannya beralih ke `idle`, bukan `terminated`.                                                                                                                                                                                                                                                                                                                                                                                               |

## Memperbarui konfigurasi agen

Anda dapat memperbarui `agent.tools` (csharp, go: `Agent.Tools`) dan `agent.mcp_servers` (java, php: `agent.mcpServers`; csharp: `Agent.McpServers`; go: `Agent.MCPServers`) sebuah sesi, termasuk kebijakan izin dan pengaturan web per alat seperti [filter domain](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#change-the-lists-mid-session), di tengah sesi tanpa membuat versi agen baru. Pembaruan bersifat lokal untuk sesi dan tidak berlaku untuk agen yang mendasarinya. `allowed_domains` (java, php: `allowedDomains`; csharp, go: `AllowedDomains`) dan `blocked_domains` (java, php: `blockedDomains`; csharp, go: `BlockedDomains`) yang diperbarui berlaku untuk sisa sesi.

Hanya `tools` (csharp, go: `Tools`) dan `mcp_servers` (java, php: `mcpServers`; csharp: `McpServers`; go: `MCPServers`) milik agen yang dapat berubah setelah sesi dibuat. Untuk menjalankan sesi dengan nilai `model` (csharp, go: `Model`), `system` (csharp, go: `System`; ruby: `system_`), atau `skills` (csharp, go: `Skills`) yang berbeda dari milik agen, gunakan [override konfigurasi agen](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session) saat Anda membuat sesi. Konfigurasi model agen, termasuk pin [`inference_geo`](https://platform.claude.com/docs/id/manage-claude/data-residency)-nya, juga tidak dapat berubah di tengah sesi: tetapkan pin saat Anda menyimpan agen, atau tetapkan atau hapus pin untuk satu sesi dengan override `model` (csharp, go: `Model`) saat Anda membuatnya. Field `system` (csharp, go: `System`; ruby: `system_`) yang dikonfigurasi pada agen bersifat tetap selama masa hidup sesi. Pada model yang mendukungnya, Anda tetap dapat menambahkan panduan tingkat sistem di tengah sesi dengan mengirimkan [event `system.message`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#send-system-messages).

Semantik pembaruan `tools` (csharp, go: `Tools`) atau `mcp_servers` (java, php: `mcpServers`; csharp: `McpServers`; go: `MCPServers`) adalah penggantian penuh: array yang diberikan menjadi nilai baru. Untuk mempertahankan entri yang ada, lakukan `GET` pada sesi, ubah array-nya, lalu `POST` kembali.

Sesi harus berstatus `idle` untuk memperbarui agen. Untuk memperbarui agen saat sesi sedang berjalan, kirimkan [event `user.interrupt`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#interrupt-the-agent) secara tersendiri dan tunggu hingga sesi menjadi `idle`. Jika sebuah [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs#while-a-run-is-open) terbuka, baik sedang berjalan maupun dijeda, pembaruan akan mengembalikan kesalahan 400, bahkan ketika sesi berstatus `idle`. Interupsi tidak mengakhiri eksekusi, sehingga pembaruan tetap gagal setelah Anda menginterupsi sesi. Kirimkan `user.message` yang [meminta agen untuk menghentikan eksekusinya](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open), atau tunggu hingga setiap eksekusi berakhir.

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "agent": {
        "tools": [
          {"type": "agent_toolset_20260401"},
          {"type": "mcp_toolset", "mcp_server_name": "linear"}
        ],
        "mcp_servers": [
          {"type": "url", "name": "linear", "url": "https://mcp.linear.app/sse"}
        ]
      }
    }'
  ```

  ```bash CLI
  ant beta:sessions update --session-id "$SESSION_ID" <<'YAML'
  agent:
    tools:
      - type: agent_toolset_20260401
      - type: mcp_toolset
        mcp_server_name: linear
    mcp_servers:
      - type: url
        name: linear
        url: https://mcp.linear.app/sse
  YAML
  ```

  ```python Python
  client.beta.sessions.update(
      session.id,
      agent={
          "tools": [
              {"type": "agent_toolset_20260401"},
              {"type": "mcp_toolset", "mcp_server_name": "linear"},
          ],
          "mcp_servers": [
              {"type": "url", "name": "linear", "url": "https://mcp.linear.app/sse"}
          ],
      },
  )
  ```

  ```typescript TypeScript
  await client.beta.sessions.update(session.id, {
    agent: {
      tools: [
        { type: "agent_toolset_20260401" },
        { type: "mcp_toolset", mcp_server_name: "linear" }
      ],
      mcp_servers: [{ type: "url", name: "linear", url: "https://mcp.linear.app/sse" }]
    }
  });
  ```

  ```csharp C#
  await client.Beta.Sessions.Update(session.ID, new()
  {
      Agent = new()
      {
          Tools =
          [
              new BetaManagedAgentsAgentToolset20260401Params(),
              new BetaManagedAgentsMcpToolsetParams { McpServerName = "linear" },
          ],
          McpServers =
          [
              new()
              {
                  Name = "linear",
                  Url = "https://mcp.linear.app/sse",
              },
          ],
      },
  });
  ```

  ```go Go
  _, err = client.Beta.Sessions.Update(ctx, session.ID, anthropic.BetaSessionUpdateParams{
  	Agent: anthropic.BetaManagedAgentsSessionAgentUpdateParam{
  		Tools: []anthropic.BetaManagedAgentsSessionAgentUpdateToolUnionParam{
  			{
  				OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{},
  			},
  			{
  				OfMCPToolset: &anthropic.BetaManagedAgentsMCPToolsetParams{
  					MCPServerName: "linear",
  				},
  			},
  		},
  		MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{
  			{
  				Name: "linear",
  				URL:  "https://mcp.linear.app/sse",
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().sessions().update(
      session.id(),
      SessionUpdateParams.builder()
          .agent(BetaManagedAgentsSessionAgentUpdate.builder()
              .addTool(BetaManagedAgentsAgentToolset20260401Params.builder().build())
              .addTool(BetaManagedAgentsMcpToolsetParams.builder()
                  .mcpServerName("linear")
                  .build())
              .addMcpServer(BetaManagedAgentsUrlMcpServerParams.builder()
                  .name("linear")
                  .url("https://mcp.linear.app/sse")
                  .build())
              .build())
          .build()
  );
  ```

  ```php PHP
  $client->beta->sessions->update(
      $session->id,
      agent: BetaManagedAgentsSessionAgentUpdate::with(
          tools: [
              BetaManagedAgentsAgentToolset20260401Params::with(),
              BetaManagedAgentsMCPToolsetParams::with(mcpServerName: 'linear'),
          ],
          mcpServers: [
              BetaManagedAgentsURLMCPServerParams::with(
                  name: 'linear',
                  url: 'https://mcp.linear.app/sse',
              ),
          ],
      ),
  );
  ```

  ```ruby Ruby
  client.beta.sessions.update(
    session.id,
    agent: {
      tools: [
        {type: :agent_toolset_20260401},
        {type: :mcp_toolset, mcp_server_name: "linear"}
      ],
      mcp_servers: [
        {type: :url, name: "linear", url: "https://mcp.linear.app/sse"}
      ]
    }
  )
  ```
</CodeGroup>

## Memperbarui anggaran sesi

Sesi yang [dibuat dengan anggaran](https://platform.claude.com/docs/id/managed-agents/sessions#set-a-session-budget) menerima dua jenis pembaruan anggaran: mengganti batas dengan `max_list_cost` (java, php: `maxListCost`; csharp, go: `MaxListCost`) baru, dan menghapusnya dengan meneruskan `"budget": null` (python: `budget=None`; typescript: `budget: null`; ruby: `budget: nil`; go: `Budget: param.NullStruct[anthropic.BetaManagedAgentsBudgetLimitParam]()`; java: `.budget(Optional.empty())`; csharp: `Budget = null`; php: `requestOptions: ['extraBodyParams' => ['budget' => null]]`; cli: `--budget null`). Keduanya secara otomatis melanjutkan pekerjaan yang dijeda ketika sesi mencapai batasnya. Batas pengganti dapat lebih tinggi atau lebih rendah dari batas saat ini, tetapi harus benar-benar lebih besar dari biaya daftar (list cost) yang telah digunakan sesi. Penghapusan bersifat satu arah: `budget` (csharp, go: `Budget`) yang tidak null hanya diterima pada sesi yang saat ini memilikinya. Oleh karena itu, Anda tidak dapat menambahkan kembali anggaran yang telah dihapus atau menambahkannya ke sesi yang dibuat tanpa anggaran. Lihat [Anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets#resume-a-session-at-its-budget) untuk contoh permintaan, perilaku kesalahan, dan apa saja yang dihitung terhadap biaya daftar.

## Mengambil sesi

<CodeGroup>
  ```bash cURL
  curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:sessions retrieve --session-id "$SESSION_ID"
  ```

  ```python Python
  retrieved = client.beta.sessions.retrieve(session.id)
  print(f"Status: {retrieved.status}")
  ```

  ```typescript TypeScript
  const retrieved = await client.beta.sessions.retrieve(session.id);
  console.log(`Status: ${retrieved.status}`);
  ```

  ```csharp C#
  var retrieved = await client.Beta.Sessions.Retrieve(session.ID);
  Console.WriteLine($"Status: {retrieved.Status.Raw()}");
  ```

  ```go Go
  retrieved, err := client.Beta.Sessions.Get(ctx, session.ID, anthropic.BetaSessionGetParams{})
  if err != nil {
  	panic(err)
  }
  fmt.Printf("Status: %s\n", retrieved.Status)
  ```

  ```java Java
  var retrieved = client.beta().sessions().retrieve(session.id());
  IO.println("Status: " + retrieved.status());
  ```

  ```php PHP
  $retrieved = $client->beta->sessions->retrieve($session->id);
  echo "Status: {$retrieved->status}\n";
  ```

  ```ruby Ruby
  retrieved = client.beta.sessions.retrieve(session.id)
  puts "Status: #{retrieved.status}"
  ```
</CodeGroup>

## Mendaftar sesi

Hasil dari `GET /v1/sessions` dipaginasi. Gunakan parameter query `limit` untuk mengontrol ukuran halaman. Setiap respons menyertakan kursor `next_page`; teruskan sebagai parameter `page` pada permintaan berikutnya untuk mengambil halaman selanjutnya. `next_page` bernilai `null` ketika tidak ada hasil lagi.

Untuk kembali satu halaman, teruskan `prev_page` sebagai parameter `page`. `prev_page` bernilai `null` ketika Anda berada di halaman pertama.

Kursor `page` bersifat opaque dan mengodekan `order` dari permintaan yang menghasilkannya. Parameter query `order` menetapkan arah pengurutan hasil, `asc` atau `desc` berdasarkan waktu pembuatan; nilai default-nya adalah `desc` (terbaru lebih dulu). Menggunakan kembali kursor dengan `order` yang berbeda akan mengembalikan kesalahan 400, begitu pula mengubah filter `created_at` sehingga mengecualikan posisi kursor. Parameter query lainnya, termasuk filter-filter yang tersisa dan `limit`, dapat berubah di antara permintaan yang dipaginasi. Untuk field paginasi yang digunakan bersama di seluruh endpoint daftar, lihat [Paginasi](https://platform.claude.com/docs/id/api/overview#pagination).

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body \
    "https://api.anthropic.com/v1/sessions?agent_id=$AGENT_ID&limit=1" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  # Teruskan next_page kembali sebagai parameter query page untuk mengambil halaman berikutnya,
  # atau prev_page untuk kembali.
  ```

  ```bash CLI
  # --format raw mengembalikan satu amplop halaman dengan kursor prev_page dan
  # next_page-nya; output default melakukan paginasi otomatis dan hanya mengeluarkan sesi.
  ant beta:sessions list --agent-id "$AGENT_ID" --limit 1 --format raw
  # Teruskan next_page kembali sebagai --page untuk mengambil halaman berikutnya, atau prev_page untuk kembali.
  ```

  ```python Python
  # Setel `limit` rendah agar hasil mencakup lebih dari satu halaman.
  first_page = client.beta.sessions.list(limit=1, agent_id=agent.id)
  # `prev_page` bernilai None di halaman pertama; `next_page` bernilai None di halaman terakhir.
  print(f"prev_page: {first_page.prev_page}")
  print(f"next_page: {first_page.next_page}")

  # Teruskan kembali `next_page` sebagai `page` untuk mengambil halaman berikutnya.
  second_page = client.beta.sessions.list(
      limit=1, agent_id=agent.id, page=first_page.next_page
  )
  for listed_session in second_page.data:
      print(f"{listed_session.id}: {listed_session.status}")

  # Teruskan kembali `prev_page` sebagai `page` untuk kembali ke halaman sebelumnya.
  previous_page = client.beta.sessions.list(
      limit=1, agent_id=agent.id, page=second_page.prev_page
  )
  for listed_session in previous_page.data:
      print(f"{listed_session.id}: {listed_session.status}")
  # Untuk iterasi maju saja, objek halaman juga dapat diiterasi secara langsung.
  ```

  ```typescript TypeScript
  const firstPage = await client.beta.sessions.list({ limit: 1, agent_id: agent.id });
  // prev_page bernilai null pada halaman pertama; next_page terisi saat masih ada sesi lain.
  console.log(`prev_page: ${firstPage.prev_page}`);
  console.log(`next_page: ${firstPage.next_page}`);

  // Teruskan next_page sebagai kursor `page` untuk mengambil halaman kedua.
  const secondPage = await client.beta.sessions.list({
    limit: 1,
    agent_id: agent.id,
    page: firstPage.next_page
  });
  for (const listedSession of secondPage.data) {
    console.log(`Page 2 has ${listedSession.id}: ${listedSession.status}`);
  }

  // Teruskan kursor prev_page dari halaman kedua untuk kembali ke halaman pertama.
  const previousPage = await client.beta.sessions.list({
    limit: 1,
    agent_id: agent.id,
    page: secondPage.prev_page
  });
  for (const listedSession of previousPage.data) {
    console.log(`Back on page 1: ${listedSession.id} is ${listedSession.status}`);
  }
  // Untuk iterasi maju saja, objek page juga dapat diiterasi langsung.
  ```

  ```csharp C#
  // SessionListPage yang dikembalikan `List` mengekspos item-itemnya tetapi tidak
  // kursor paginasinya. Untuk membaca `prev_page` / `next_page`, deserialisasi respons
  // mentahnya ke SessionListPageResponse sebagai gantinya.
  using var page1Response = await client.Beta.Sessions.WithRawResponse.List(
      new SessionListParams { Limit = 1, AgentID = agent.ID }
  );
  var page1 = await page1Response.Deserialize<SessionListPageResponse>();
  Console.WriteLine($"prev_page: {page1.PrevPage ?? "null"}");
  Console.WriteLine($"next_page: {page1.NextPage ?? "null"}");

  // Maju: berikan `next_page` dari halaman 1 sebagai kursor `page`.
  using var page2Response = await client.Beta.Sessions.WithRawResponse.List(
      new SessionListParams { Limit = 1, AgentID = agent.ID, Page = page1.NextPage }
  );
  var page2 = await page2Response.Deserialize<SessionListPageResponse>();
  foreach (var listedSession in page2.Data ?? [])
  {
      Console.WriteLine($"Page 2: {listedSession.ID}: {listedSession.Status.Raw()}");
  }

  // Mundur: berikan `prev_page` dari halaman 2 sebagai kursor `page` yang sama.
  using var previousPageResponse = await client.Beta.Sessions.WithRawResponse.List(
      new SessionListParams { Limit = 1, AgentID = agent.ID, Page = page2.PrevPage }
  );
  var previousPage = await previousPageResponse.Deserialize<SessionListPageResponse>();
  foreach (var listedSession in previousPage.Data ?? [])
  {
      Console.WriteLine($"Back to page 1: {listedSession.ID}: {listedSession.Status.Raw()}");
  }
  // Untuk iterasi maju saja, (await client.Beta.Sessions.List(...)).Paginate() mengembalikan IAsyncEnumerable yang otomatis mengikuti next_page.
  ```

  ```go Go
  // Halaman 1: prev_page kosong karena tidak ada yang mendahului halaman pertama.
  firstPage, err := client.Beta.Sessions.List(ctx, anthropic.BetaSessionListParams{
  	AgentID: anthropic.String(agent.ID),
  	Limit:   anthropic.Int(1),
  })
  if err != nil {
  	panic(err)
  }
  fmt.Printf("Page 1 prev_page: %q\n", firstPage.PrevPage)
  fmt.Printf("Page 1 next_page: %q\n", firstPage.NextPage)

  // Maju: berikan next_page sebagai kursor Page untuk mengambil halaman 2.
  secondPage, err := client.Beta.Sessions.List(ctx, anthropic.BetaSessionListParams{
  	AgentID: anthropic.String(agent.ID),
  	Limit:   anthropic.Int(1),
  	Page:    anthropic.String(firstPage.NextPage),
  })
  if err != nil {
  	panic(err)
  }
  for _, listedSession := range secondPage.Data {
  	fmt.Printf("Page 2: %s: %s\n", listedSession.ID, listedSession.Status)
  }

  // Kembali: prev_page halaman 2 adalah kursor untuk halaman sebelumnya.
  previousPage, err := client.Beta.Sessions.List(ctx, anthropic.BetaSessionListParams{
  	AgentID: anthropic.String(agent.ID),
  	Limit:   anthropic.Int(1),
  	Page:    anthropic.String(secondPage.PrevPage),
  })
  if err != nil {
  	panic(err)
  }
  for _, listedSession := range previousPage.Data {
  	fmt.Printf("Back to page 1: %s: %s\n", listedSession.ID, listedSession.Status)
  }
  // Untuk iterasi maju saja, gunakan ListAutoPaging agar next_page diikuti otomatis.
  ```

  ```java Java
  var params = SessionListParams.builder()
      .agentId(agent.id())
      .limit(1)
      .build();
  var firstPage = client.beta().sessions().list(params);
  for (var listedSession : firstPage.data()) {
      IO.println(listedSession.id() + ": " + listedSession.status());
  }
  // prev_page adalah Optional kosong pada halaman pertama; next_page menunjuk ke halaman 2.
  IO.println("prev_page: " + firstPage.response().prevPage());
  IO.println("next_page: " + firstPage.response().nextPage());

  // Maju dengan meneruskan next_page sebagai kursor halaman.
  var nextCursor = firstPage.response().nextPage().orElseThrow();
  var secondPage = client.beta().sessions().list(params.toBuilder()
      .page(nextCursor)
      .build());

  // Kembali dengan meneruskan prev_page sebagai kursor halaman yang sama.
  var prevCursor = secondPage.response().prevPage().orElseThrow();
  var previousPage = client.beta().sessions().list(params.toBuilder()
      .page(prevCursor)
      .build());
  // Kembali ke halaman pertama, jadi prev_page kosong lagi.
  IO.println("prev_page: " + previousPage.response().prevPage());
  // Untuk iterasi maju saja, page.autoPager() mengembalikan Iterable yang otomatis mengikuti next_page.
  ```

  ```php PHP
  // Halaman 1: prevPage bernilai null karena tidak ada yang mendahului halaman pertama.
  $firstPage = $client->beta->sessions->list(agentID: $agent->id, limit: 1);
  echo 'Page 1 prev_page: ' . ($firstPage->prevPage ?? 'null') . "\n";
  echo 'Page 1 next_page: ' . ($firstPage->nextPage ?? 'null') . "\n";

  // Maju: kirim kembali nextPage sebagai kursor `page` untuk mengambil halaman 2.
  $secondPage = $client->beta->sessions->list(
      agentID: $agent->id,
      limit: 1,
      page: $firstPage->nextPage,
  );
  foreach ($secondPage->getItems() as $listedSession) {
      echo "Page 2: {$listedSession->id}: {$listedSession->status}\n";
  }

  // Mundur: prevPage halaman 2 adalah kursor untuk halaman sebelumnya.
  $previousPage = $client->beta->sessions->list(
      agentID: $agent->id,
      limit: 1,
      page: $secondPage->prevPage,
  );
  foreach ($previousPage->getItems() as $listedSession) {
      echo "Back to page 1: {$listedSession->id}: {$listedSession->status}\n";
  }
  // Untuk iterasi maju saja, $page->pagingEachItem() menghasilkan setiap sesi di semua halaman.
  ```

  ```ruby Ruby
  first_page = client.beta.sessions.list(agent_id: agent.id, limit: 1)
  first_page.data.each do |listed_session|
    puts "#{listed_session.id}: #{listed_session.status}"
  end

  # `prev_page` bernilai nil pada halaman pertama. Kursor halaman berikutnya diekspos sebagai
  # `next_page_` (garis bawah di akhir) karena `next_page` biasa adalah metode helper
  # yang mengambil objek halaman berikutnya untuk Anda.
  puts "prev_page: #{first_page.prev_page.inspect}"
  puts "next_page: #{first_page.next_page_.inspect}"

  # Kirimkan salah satu kursor kembali sebagai `page` untuk menelusuri daftar di kedua arah.
  second_page = client.beta.sessions.list(
    agent_id: agent.id,
    limit: 1,
    page: first_page.next_page_
  )
  back_to_first = client.beta.sessions.list(
    agent_id: agent.id,
    limit: 1,
    page: second_page.prev_page
  )
  back_to_first.data.each do |listed_session|
    puts "#{listed_session.id}: #{listed_session.status}"
  end
  # Untuk iterasi maju saja, page.auto_paging_each otomatis mengikuti next_page.
  ```
</CodeGroup>

## Mengarsipkan sesi

Arsipkan sesi untuk mencegah event baru dikirim sambil tetap mempertahankan riwayatnya. Sesi yang berstatus `running` tidak dapat diarsipkan; untuk mengarsipkannya, kirimkan [event `user.interrupt`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#interrupt-the-agent) secara tersendiri dan tunggu hingga sesi menjadi `idle`. Jika sebuah [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs#while-a-run-is-open) terbuka, pengarsipan mungkin mengembalikan kesalahan 400, bahkan ketika sesi berstatus `idle`, atau mungkin berhasil dan mengakhiri eksekusi tersebut. Sebelum Anda mengarsipkan, kirimkan `user.message` yang [meminta agen untuk menghentikan eksekusinya](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open), atau tunggu hingga setiap eksekusi berakhir. Kemudian arsipkan sesi setelah berstatus `idle`.

<CodeGroup>
  ```bash cURL
  curl -fsSL -X POST "https://api.anthropic.com/v1/sessions/$SESSION_ID/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:sessions archive --session-id "$SESSION_ID"
  ```

  ```python Python
  client.beta.sessions.archive(session.id)
  ```

  ```typescript TypeScript
  await client.beta.sessions.archive(session.id);
  ```

  ```csharp C#
  await client.Beta.Sessions.Archive(session.ID);
  ```

  ```go Go
  _, err = client.Beta.Sessions.Archive(ctx, session.ID, anthropic.BetaSessionArchiveParams{})
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().sessions().archive(session.id());
  ```

  ```php PHP
  $client->beta->sessions->archive($session->id);
  ```

  ```ruby Ruby
  client.beta.sessions.archive(session.id)
  ```
</CodeGroup>

## Menghapus sesi

Menghapus sesi bersifat permanen. Tindakan ini menghapus catatan sesi, event, dan sandbox terkait. Sesi yang berstatus `running` tidak dapat dihapus; untuk menghapusnya, kirimkan [event `user.interrupt`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#interrupt-the-agent) secara tersendiri dan tunggu hingga sesi menjadi `idle`. Jika sebuah [workflow run](https://platform.claude.com/docs/id/managed-agents/workflow-runs#while-a-run-is-open) terbuka, penghapusan mungkin mengembalikan kesalahan 400, bahkan ketika sesi berstatus `idle`, atau mungkin berhasil. Setelah penghapusan berhasil, tidak ada event `workflow_run` yang melaporkan berakhirnya run sesi tersebut. Sebelum Anda menghapus, kirimkan `user.message` yang [meminta agen untuk menghentikan run-nya](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open), atau tunggu hingga setiap run berakhir. Kemudian hapus sesi setelah berstatus `idle`.

Memory store, vault, skill, environment, dan agen adalah sumber daya independen dan tidak terpengaruh oleh penghapusan sesi. File yang Anda unggah melalui Files API juga tidak terpengaruh, tetapi file yang dihasilkan oleh sesi itu sendiri terikat pada sesi tersebut dan dihapus secara permanen bersama sistem file-nya. Unduh apa pun yang perlu Anda simpan sebelum menghapus sesi. File output yang ditulis di akhir giliran terakhir dapat memerlukan beberapa detik setelah sesi menjadi idle untuk muncul di [daftar file sesi](https://platform.claude.com/docs/id/managed-agents/files#listing-and-downloading-session-files), jadi periksa terlebih dahulu bahwa file yang Anda harapkan sudah terdaftar.

<CodeGroup>
  ```bash cURL
  curl -fsSL -X DELETE "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:sessions delete --session-id "$SESSION_ID"
  ```

  ```python Python
  client.beta.sessions.delete(session.id)
  ```

  ```typescript TypeScript
  await client.beta.sessions.delete(session.id);
  ```

  ```csharp C#
  await client.Beta.Sessions.Delete(session.ID);
  ```

  ```go Go
  _, err = client.Beta.Sessions.Delete(ctx, session.ID, anthropic.BetaSessionDeleteParams{})
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().sessions().delete(session.id());
  ```

  ```php PHP
  $client->beta->sessions->delete($session->id);
  ```

  ```ruby Ruby
  client.beta.sessions.delete(session.id)
  ```
</CodeGroup>
