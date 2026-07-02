---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/session-operations
fetched_at: 2026-07-02T03:13:49.360020Z
sha256: 204617b0946de1cc0878dbec46e9344f7cc96dfefc5c0ff09e619ccfd14fd150
---

# Operasi sesi

Mengambil, membuat daftar, memperbarui, mengarsipkan, dan menghapus sesi Claude Managed Agents.

---

Setelah sebuah sesi ada, gunakan operasi-operasi ini untuk membaca, memperbarui, mengarsipkan, atau menghapusnya. Lihat [Memulai sesi](/docs/id/managed-agents/sessions) untuk membuat sesi dan mengirimkan pekerjaan kepadanya.

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Status sesi

Sesi berjalan melalui status-status berikut. Lihat [Memulai sesi](/docs/id/managed-agents/sessions) untuk siklus hidup sesi.

| Status         | Deskripsi                                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------------------- |
| `idle`         | Agen sedang menunggu input, termasuk pesan pengguna atau konfirmasi alat. Sesi dimulai dalam status `idle`. |
| `running`      | Agen sedang aktif mengeksekusi.                                                                             |
| `rescheduling` | Terjadi kesalahan sementara, mencoba ulang secara otomatis.                                                 |
| `terminated`   | Sesi telah berakhir karena kesalahan yang tidak dapat dipulihkan.                                           |

## Memperbarui konfigurasi agen

Anda dapat memperbarui `agent.tools` dan `agent.mcp_servers` milik sebuah sesi, termasuk kebijakan izin, di tengah sesi tanpa membuat versi agen baru. Pembaruan bersifat lokal untuk sesi tersebut dan tidak disebarkan kembali ke agen yang mendasarinya.

Hanya `tools` dan `mcp_servers` milik agen yang dapat diubah setelah sesi dibuat. Untuk menjalankan sesi dengan nilai `model`, `system`, atau `skills` yang berbeda dari milik agen, gunakan [override konfigurasi agen](/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session) saat Anda membuat sesi. Field `system` yang dikonfigurasi pada agen bersifat tetap selama masa hidup sesi. Pada model yang mendukungnya, Anda tetap dapat mengganti prompt sistem efektif di antara giliran dengan mengirimkan [event `system.message`](/docs/id/managed-agents/events-and-streaming#sending-system-messages).

Semantik pembaruan `tools` atau `mcp_servers` adalah penggantian penuh: array yang diberikan menjadi nilai baru. Untuk mempertahankan entri yang sudah ada, lakukan `GET` pada sesi, modifikasi array-nya, lalu `POST` kembali.

Sesi harus dalam status `idle` untuk memperbarui agen. [Interupsi](/docs/id/managed-agents/events-and-streaming#integrating-events) sesi jika Anda perlu memperbarui agen saat sesi sedang berjalan.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": {
      "tools": [
        {"type": "agent_toolset_20260401"},
        {"type": "mcp_toolset", "mcp_server_name": "linear"}
      ],
      "mcp_servers": [
        {"type": "url", "name": "linear", "url": "https://mcp.linear.app/sse"}
      ]
    }
  }
  EOF
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
              new BetaManagedAgentsAgentToolset20260401Params
              {
                  Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
              },
              new BetaManagedAgentsMcpToolsetParams
              {
                  Type = BetaManagedAgentsMcpToolsetParamsType.McpToolset,
                  McpServerName = "linear",
              },
          ],
          McpServers =
          [
              new()
              {
                  Type = BetaManagedAgentsUrlMcpServerParamsType.Url,
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
  				OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  					Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  				},
  			},
  			{
  				OfMCPToolset: &anthropic.BetaManagedAgentsMCPToolsetParams{
  					Type:          anthropic.BetaManagedAgentsMCPToolsetParamsTypeMCPToolset,
  					MCPServerName: "linear",
  				},
  			},
  		},
  		MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{
  			{
  				Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
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
              .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .build())
              .addTool(BetaManagedAgentsMcpToolsetParams.builder()
                  .type(BetaManagedAgentsMcpToolsetParams.Type.MCP_TOOLSET)
                  .mcpServerName("linear")
                  .build())
              .addMcpServer(BetaManagedAgentsUrlMcpServerParams.builder()
                  .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
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
              BetaManagedAgentsAgentToolset20260401Params::with(type: 'agent_toolset_20260401'),
              BetaManagedAgentsMCPToolsetParams::with(mcpServerName: 'linear', type: 'mcp_toolset'),
          ],
          mcpServers: [
              BetaManagedAgentsURLMCPServerParams::with(
                  name: 'linear',
                  type: 'url',
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

## Mengambil sesi

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  retrieved=$(curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")
  echo "Status: $(jq -r '.status' <<< "$retrieved")"
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

## Membuat daftar sesi

Hasil dari `GET /v1/sessions` dipaginasi. Gunakan parameter kueri `limit` untuk mengontrol ukuran halaman. Setiap respons menyertakan kursor `next_page`; teruskan sebagai parameter `page` pada permintaan berikutnya untuk mengambil halaman selanjutnya. `next_page` bernilai `null` ketika tidak ada hasil lagi.

Untuk kembali satu halaman, teruskan `prev_page` sebagai parameter `page`. `prev_page` bernilai `null` ketika Anda berada di halaman pertama.

Kursor `page` bersifat opaque dan mengenkode `order` dari permintaan yang menghasilkannya. Parameter kueri `order` menetapkan arah pengurutan hasil, `asc` atau `desc` berdasarkan waktu pembuatan; default-nya adalah `desc` (terbaru lebih dulu). Menggunakan kembali kursor dengan `order` yang berbeda akan mengembalikan error 400; parameter kueri lainnya, termasuk filter dan `limit`, dapat berubah di antara permintaan yang dipaginasi. Untuk field paginasi yang digunakan bersama di seluruh endpoint daftar, lihat [Paginasi](/docs/id/api/overview#pagination).

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  first_page=$(curl -sS --fail-with-body \
    "https://api.anthropic.com/v1/sessions?agent_id=$AGENT_ID&limit=1" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")
  jq '{prev_page, next_page}' <<< "$first_page"  # prev_page is null on the first page

  next_cursor=$(jq -r '.next_page' <<< "$first_page")
  second_page=$(curl -sS --fail-with-body \
    "https://api.anthropic.com/v1/sessions?agent_id=$AGENT_ID&limit=1&page=$next_cursor" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")

  prev_cursor=$(jq -r '.prev_page' <<< "$second_page")
  curl -sS --fail-with-body \
    "https://api.anthropic.com/v1/sessions?agent_id=$AGENT_ID&limit=1&page=$prev_cursor" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    | jq '{prev_page, next_page}'
  ```

  ```bash CLI
  # --format raw mengembalikan satu envelope halaman dengan kursor prev_page dan next_page
  # miliknya; output default melakukan auto-paginasi dan hanya mengeluarkan sesi-sesinya.
  cursors=$(ant beta:sessions list \
    --agent-id "$AGENT_ID" \
    --limit 1 \
    --format raw \
    --transform '{prev_page,next_page}')
  printf '%s\n' "$cursors"

  # Kirim kembali kursor next_page sebagai --page untuk mengambil halaman berikutnya.
  NEXT_PAGE=$(jq -r '.next_page' <<< "$cursors")
  ant beta:sessions list \
    --agent-id "$AGENT_ID" \
    --limit 1 \
    --page "$NEXT_PAGE" \
    --format raw \
    --transform '{prev_page,next_page}'
  # Kirim prev_page dari respons itu sebagai --page untuk kembali dengan cara yang sama.
  ```

  ```python Python
  # Atur `limit` rendah agar hasilnya mencakup lebih dari satu halaman.
  first_page = client.beta.sessions.list(limit=1, agent_id=agent.id)
  # `prev_page` bernilai None di halaman pertama; `next_page` None di halaman terakhir.
  print(f"prev_page: {first_page.prev_page}")
  print(f"next_page: {first_page.next_page}")

  # Oper kembali `next_page` sebagai `page` untuk mengambil halaman berikutnya.
  second_page = client.beta.sessions.list(
      limit=1, agent_id=agent.id, page=first_page.next_page
  )
  for listed_session in second_page.data:
      print(f"{listed_session.id}: {listed_session.status}")

  # Oper kembali `prev_page` sebagai `page` untuk kembali ke halaman sebelumnya.
  previous_page = client.beta.sessions.list(
      limit=1, agent_id=agent.id, page=second_page.prev_page
  )
  for listed_session in previous_page.data:
      print(f"{listed_session.id}: {listed_session.status}")
  # Untuk iterasi maju saja, objek halaman juga dapat diiterasi secara langsung.
  ```

  ```typescript TypeScript
  const firstPage = await client.beta.sessions.list({ limit: 1, agent_id: agent.id });
  // prev_page bernilai null di halaman pertama; next_page terisi jika masih ada sesi lain.
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
  // Untuk iterasi maju-saja, objek halaman juga dapat diiterasi secara langsung.
  ```

  ```csharp C#
  // SessionListPage yang dikembalikan `List` mengekspos item tetapi bukan
  // kursor paginasi. Untuk membaca `prev_page` / `next_page`, deserialisasi respons
  // mentah menjadi SessionListPageResponse sebagai gantinya.
  using var page1Response = await client.Beta.Sessions.WithRawResponse.List(
      new SessionListParams { Limit = 1, AgentID = agent.ID }
  );
  var page1 = await page1Response.Deserialize<SessionListPageResponse>();
  Console.WriteLine($"prev_page: {page1.PrevPage ?? "null"}");
  Console.WriteLine($"next_page: {page1.NextPage ?? "null"}");

  // Maju: oper `next_page` dari halaman 1 sebagai kursor `page`.
  using var page2Response = await client.Beta.Sessions.WithRawResponse.List(
      new SessionListParams { Limit = 1, AgentID = agent.ID, Page = page1.NextPage }
  );
  var page2 = await page2Response.Deserialize<SessionListPageResponse>();
  foreach (var listedSession in page2.Data ?? [])
  {
      Console.WriteLine($"Page 2: {listedSession.ID}: {listedSession.Status.Raw()}");
  }

  // Mundur: oper `prev_page` dari halaman 2 sebagai kursor `page` yang sama.
  using var previousPageResponse = await client.Beta.Sessions.WithRawResponse.List(
      new SessionListParams { Limit = 1, AgentID = agent.ID, Page = page2.PrevPage }
  );
  var previousPage = await previousPageResponse.Deserialize<SessionListPageResponse>();
  foreach (var listedSession in previousPage.Data ?? [])
  {
      Console.WriteLine($"Back to page 1: {listedSession.ID}: {listedSession.Status.Raw()}");
  }
  // Untuk iterasi maju-saja, (await client.Beta.Sessions.List(...)).Paginate() mengembalikan IAsyncEnumerable yang otomatis mengikuti next_page.
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

  // Mundur: prev_page halaman 2 adalah kursor untuk halaman sebelumnya.
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
  // Untuk iterasi maju saja, gunakan ListAutoPaging untuk auto-ikuti next_page.
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
  // prev_page adalah Optional kosong di halaman pertama; next_page menunjuk ke halaman 2.
  IO.println("prev_page: " + firstPage.response().prevPage());
  IO.println("next_page: " + firstPage.response().nextPage());

  // Maju dengan meneruskan next_page sebagai kursor halaman.
  var nextCursor = firstPage.response().nextPage().orElseThrow();
  var secondPage = client.beta().sessions().list(params.toBuilder().page(nextCursor).build());

  // Mundur dengan meneruskan prev_page sebagai kursor halaman yang sama.
  var prevCursor = secondPage.response().prevPage().orElseThrow();
  var previousPage = client.beta().sessions().list(params.toBuilder().page(prevCursor).build());
  // Kembali di halaman pertama, jadi prev_page kosong lagi.
  IO.println("prev_page: " + previousPage.response().prevPage());
  // Untuk iterasi maju saja, page.autoPager() mengembalikan Iterable yang otomatis mengikuti next_page.
  ```

  ```php PHP
  // Halaman 1: prevPage bernilai null karena tidak ada yang mendahului halaman pertama.
  $firstPage = $client->beta->sessions->list(agentID: $agent->id, limit: 1);
  echo 'Page 1 prev_page: ' . ($firstPage->prevPage ?? 'null') . "\n";
  echo 'Page 1 next_page: ' . ($firstPage->nextPage ?? 'null') . "\n";

  // Maju: oper kembali nextPage sebagai kursor `page` untuk mengambil halaman 2.
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

  # `prev_page` bernilai nil pada halaman pertama. Kursor halaman-berikutnya diekspos sebagai
  # `next_page_` (underscore di akhir) karena `next_page` biasa adalah method helper
  # yang mengambilkan objek halaman berikutnya untuk Anda.
  puts "prev_page: #{first_page.prev_page.inspect}"
  puts "next_page: #{first_page.next_page_.inspect}"

  # Kirim salah satu kursor kembali sebagai `page` untuk menelusuri daftar di kedua arah.
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
  # Untuk iterasi maju-saja, page.auto_paging_each otomatis mengikuti next_page.
  ```
</CodeGroup>

## Mengarsipkan sesi

Arsipkan sesi untuk mencegah event baru dikirim sambil tetap mempertahankan riwayatnya. Sesi dengan status `running` tidak dapat diarsipkan; kirim [event interupsi](/docs/id/managed-agents/events-and-streaming#integrating-events) jika Anda perlu mengarsipkannya segera.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL -X POST "https://api.anthropic.com/v1/sessions/$SESSION_ID/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:sessions archive \
    --session-id "$SESSION_ID"
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

Hapus sesi untuk menghapus secara permanen catatannya, event-nya, dan sandbox yang terkait. Sesi dengan status `running` tidak dapat dihapus; kirim [event interupsi](/docs/id/managed-agents/events-and-streaming#integrating-events) jika Anda perlu menghapusnya segera.

File, memory store, vault, skill, environment, dan agen adalah sumber daya independen dan tidak terpengaruh oleh penghapusan sesi.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL -X DELETE "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:sessions delete \
    --session-id "$SESSION_ID"
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
