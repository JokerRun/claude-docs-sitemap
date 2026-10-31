---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/budgets
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 28f392909081c8e5b070074b1e8e9d5628fb14d074562a111d8c712998e209c3
---

---
title: Anggaran sesi
url: https://platform.claude.com/docs/id/managed-agents/budgets
description: Batasi pengeluaran sesi dengan anggaran dolar yang ketat dan diberlakukan berdasarkan tarif daftar publik.
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
    Claude Models on Google Cloud (Anthropic managed): beta
---

Anggaran sesi adalah batas pengeluaran ketat opsional yang Anda tetapkan saat Anda [membuat sesi](https://platform.claude.com/docs/id/managed-agents/sessions). Platform terus-menerus menghitung harga semua yang dikonsumsi sesi pada tarif daftar publik (**list cost** (biaya daftar) sesi) dan berhenti mengirimkan permintaan model baru setelah biaya tersebut mencapai anggaran. Permintaan yang sedang berjalan saat batas terlampaui tetap diselesaikan, sehingga biaya daftar akhir dapat berada [sedikit melewati anggaran](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget). Sesi yang mencapai anggarannya akan dijeda dan menjadi [idle](https://platform.claude.com/docs/id/managed-agents/session-operations#session-statuses) alih-alih dihentikan; mengubah atau menghapus anggaran akan melanjutkan pekerjaan yang dijeda oleh anggaran tersebut. Deployment menerima anggaran yang sama dan menerapkannya pada setiap sesi yang dimulainya; lihat [Anggaran pada deployment](https://platform.claude.com/docs/id/managed-agents/budgets#budgets-on-deployments).

## Menetapkan anggaran saat pembuatan sesi

Berikan field opsional `budget` (csharp, go: `Budget`) saat Anda membuat sesi:

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "agent": "'"$AGENT_ID"'",
      "environment_id": "'"$ENVIRONMENT_ID"'",
      "budget": {
        "type": "limit",
        "max_list_cost": {"amount": "125", "currency": "USD"}
      }
    }'
  ```

  ```bash CLI
  # Biarkan jumlah tetap dalam tanda kutip agar dikirim sebagai string, bukan angka.
  ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --budget '{type: limit, max_list_cost: {amount: "125", currency: USD}}'
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      budget={
          "type": "limit",
          "max_list_cost": {"amount": "125", "currency": "USD"},
      },
  )
  print(session.id, session.budget.max_list_cost.amount)  # sesn_01... 125
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    budget: {
      type: "limit",
      max_list_cost: { amount: "125", currency: "USD" }
    }
  });
  console.log(session.id, session.budget?.max_list_cost.amount); // sesn_01... 125
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Budget = new()
      {
          MaxListCost = new() { Amount = "125", Currency = BetaCurrency.Usd },
      },
  });
  Console.WriteLine($"{session.ID} {session.Budget?.MaxListCost.Amount}");  // sesn_01... 125
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	Budget: anthropic.BetaManagedAgentsBudgetLimitParam{
  		MaxListCost: anthropic.BetaMonetaryAmountParam{
  			Amount:   "125",
  			Currency: anthropic.BetaCurrencyUsd,
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(session.ID, session.Budget.MaxListCost.Amount) // sesn_01... 125
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .budget(BetaManagedAgentsBudgetLimit.builder()
          .maxListCost(BetaMonetaryAmount.builder()
              .amount("125")
              .currency(BetaCurrency.USD)
              .build())
          .build())
      .build());
  IO.println(session.id() + " " + session.budget().orElseThrow().maxListCost().amount());  // sesn_01... 125
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      budget: [
          'type' => 'limit',
          'max_list_cost' => ['amount' => '125', 'currency' => 'USD'],
      ],
  );
  echo "{$session->id} {$session->budget->maxListCost->amount}\n"; // sesn_01... 125
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    budget: {
      type: "limit",
      max_list_cost: {amount: "125", currency: "USD"}
    }
  )
  puts "#{session.id} #{session.budget.max_list_cost.amount}" # sesn_01... 125
  ```
</CodeGroup>

Objek `budget` (csharp, go: `Budget`) memiliki dua field:

* `type` (csharp, go: `Type`) selalu bernilai `"limit"`.
* `max_list_cost` (java, php: `maxListCost`; csharp, go: `MaxListCost`) adalah batas itu sendiri: `amount` (csharp, go: `Amount`) adalah bilangan bulat sen dolar AS yang ditulis sebagai string tanpa nol di depan (`"125"` adalah $1,25 USD dan `"50"` adalah 50 sen) dan harus lebih besar dari nol. Bentuk desimal seperti `"25.00"` akan ditolak. Jumlah ini berupa string alih-alih angka sehingga tidak pernah ada pembulatan float yang diterapkan padanya. `currency` (csharp, go: `Currency`) adalah kode mata uang ISO-4217 huruf besar; `USD` adalah satu-satunya mata uang yang didukung.

Anggaran hanya dapat dilampirkan saat sesi dibuat. Menambahkan anggaran ke sesi yang sudah ada dan belum memilikinya akan ditolak dengan error 400. Batas pada sesi yang memiliki anggaran dapat [diubah](https://platform.claude.com/docs/id/managed-agents/budgets#change-the-budget) atau [dihapus](https://platform.claude.com/docs/id/managed-agents/budgets#remove-the-budget) kapan saja.

## Cara biaya daftar diukur

Platform menghitung harga apa yang dikonsumsi sesi, secara terus-menerus, berdasarkan tarif daftar publik:

* **Token model**, berdasarkan harga daftar setiap model yang dilayani
* **Pencarian web**, seharga $10 USD per 1.000 pencarian
* **Waktu berjalan sesi**, seharga $0,08 USD per jam

Total dolar berjalan ini adalah **biaya daftar** (list cost) sesi, dan inilah yang dibandingkan dengan anggaran. Biaya daftar bukanlah harga kontrak Anda: jika organisasi Anda telah menegosiasikan diskon, sesi mencapai batasnya ketika total harga daftar mencapainya, dan pengeluaran yang ditagihkan kepada Anda mungkin lebih rendah dari batas tersebut.

Pemberlakuan menggunakan biaya daftar yang tepat dan tidak dibulatkan. Angka `list_cost` (java, php: `listCost`; csharp, go: `ListCost`) yang dilaporkan pada sesi dan event-nya berupa sen bulat, dibulatkan ke sen terdekat, sehingga angka yang dilaporkan dapat berselisih hingga setengah sen di atas atau di bawah jumlah tepat yang digunakan pemberlakuan.

## Ketika sesi mencapai anggarannya

Batas ditegakkan di antara permintaan model, bukan di tengah permintaan. Sebelum setiap permintaan model, platform memeriksa biaya daftar yang telah dikonsumsi sesi, dan setelah total tersebut mencapai batas, setiap thread dijeda sebelum permintaan berikutnya. Permintaan yang membawa total melewati batas telah diterima saat sesi masih di bawah batas dan berjalan hingga selesai. Akibatnya, `list_cost` (java, php: `listCost`; csharp, go: `ListCost`) yang tercatat pada sesi yang dijeda bernilai sama dengan atau sedikit melewati `max_list_cost` (java, php: `maxListCost`; csharp, go: `MaxListCost`). Misalnya, sesi yang dibatasi pada `"50"` (50 sen) dapat dijeda dengan `list_cost` (java, php: `listCost`; csharp, go: `ListCost`) sebesar `"53"`. Hal ini memang diharapkan, bukan kesalahan penagihan. Pengeluaran model yang melewati batas paling banyak sebesar biaya satu permintaan model untuk setiap thread. Pemanggilan alat dalam respons permintaan tersebut tetap berjalan, dan pencarian web serta waktu berjalannya juga dihitung dalam biaya daftar. Perlakukan anggaran sebagai batas untuk pekerjaan baru alih-alih titik berhenti yang tepat, dan tentukan ukuran batas dengan mempertimbangkan margin tersebut.

Sesi yang mencapai anggarannya menjadi idle dengan `stop_reason` (java, php: `stopReason`; csharp, go: `StopReason`) bernilai `budget_reached`; sesi tidak dihentikan, dan riwayat serta sandbox-nya dipertahankan seperti sesi idle lainnya. Pada [event stream](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) Anda akan melihat, secara berurutan:

1. Event `session.thread_status_idle` dengan `stop_reason` (java, php: `stopReason`; csharp, go: `StopReason`) bernilai `budget_reached` saat setiap thread dijeda.
2. Event [`session.usage`](https://platform.claude.com/docs/id/managed-agents/budgets#monitor-spend) dengan penggunaan kumulatif dan biaya daftar sesi.
3. Event `session.status_idle` dengan `stop_reason` (java, php: `stopReason`; csharp, go: `StopReason`) bernilai `budget_reached`. Event penggunaan selalu tepat mendahului event idle ini.

Jika ada [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs#budgets-and-limits) yang terbuka, setiap eksekusi yang belum idle juga mendapatkan event `workflow_run.status_idle`.

Thread yang permintaan terakhirnya sekaligus melewati batas dan menyelesaikan gilirannya melaporkan `end_turn` pada event `session.thread_status_idle` miliknya sendiri, sementara sesi tetap melaporkan `budget_reached`; perlakukan `stop_reason` (java, php: `stopReason`; csharp, go: `StopReason`) tingkat sesi sebagai sinyal bahwa sesi dijeda pada anggarannya.

### Event yang diterima pada batas

Selama sesi berada pada atau melebihi anggarannya, sesi hanya menerima event yang menyelesaikan pekerjaan yang sudah berjalan:

* `user.tool_confirmation`
* `user.tool_result`
* `user.custom_tool_result`
* `user.interrupt`

Event apa pun yang akan memulai pekerjaan baru, seperti `user.message`, ditolak dengan error 400 yang menyebutkan daftar ini. Hasil yang diselesaikan dicatat tanpa memicu permintaan model baru; sesi tetap dijeda pada anggarannya.

`user.interrupt` yang dikirim saat sesi dijeda pada anggarannya (semua thread dijeda pada batas) diterima, dan event tersebut tidak muncul dalam daftar event. Event ini tidak menghentikan thread mana pun, karena setiap thread sudah dijeda. Ubah atau hapus anggaran untuk melanjutkan.

Jika sesi memiliki workflow run yang terbuka, interrupt dapat menjeda run tersebut, seperti halnya interrupt pada waktu lain. Run yang dijeda oleh interrupt tidak dilanjutkan saat Anda mengubah atau menghapus anggaran. Untuk melanjutkannya, ubah atau hapus anggaran, lalu kirim `user.message` yang meminta agen untuk melanjutkan run-nya. Lihat [Menginterupsi sesi dengan run yang terbuka](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open).

## Melanjutkan sesi yang mencapai anggarannya

Ubah atau hapus anggaran dengan pembaruan sesi. Pembaruan yang diterima akan secara otomatis melanjutkan pekerjaan yang dijeda oleh anggaran; tidak diperlukan tindakan klien lebih lanjut.

Setiap [eksekusi workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs#budgets-and-limits) yang dijeda oleh anggaran juga mendapatkan event `workflow_run.status_running`. Eksekusi yang dijeda oleh interupsi, bahkan interupsi yang dikirim saat sesi berada pada anggarannya, tetap dijeda dan tidak mendapatkan event `workflow_run.status_running` dari pembaruan tersebut. Untuk melanjutkannya, kirim `user.message` yang meminta agen melanjutkan eksekusinya. Lihat [Menginterupsi sesi dengan eksekusi yang terbuka](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open).

### Mengubah anggaran

Perbarui sesi dengan `max_list_cost` (java, php: `maxListCost`; csharp, go: `MaxListCost`) yang baru. Nilai baru dapat lebih tinggi atau lebih rendah dari batas saat ini, tetapi harus benar-benar lebih besar dari biaya daftar yang telah dikonsumsi sesi; jika tidak, pembaruan ditolak dengan error 400: `budget.max_list_cost must be greater than the session's consumed list cost`. Karena biaya yang dikonsumsi biasanya berada [sedikit melewati batas lama](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget) saat sesi dijeda, dasarkan nilai baru pada `usage.list_cost` (java, php: `usage.listCost`; csharp, go: `Usage.ListCost`) yang dilaporkan sesi, bukan pada `max_list_cost` (java, php: `maxListCost`; csharp, go: `MaxListCost`) yang lama. Tetapkan nilainya satu sen atau lebih di atas angka tersebut: nilai yang dilaporkan dibulatkan dan dapat berada sedikit di bawah biaya terkonsumsi tepat yang digunakan pemeriksaan.

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "budget": {
        "type": "limit",
        "max_list_cost": {"amount": "500", "currency": "USD"}
      }
    }'
  ```

  ```bash CLI
  ant beta:sessions update \
    --session-id "$SESSION_ID" \
    --budget '{type: limit, max_list_cost: {amount: "500", currency: USD}}'
  ```

  ```python Python
  updated_session = client.beta.sessions.update(
      session.id,
      budget={
          "type": "limit",
          "max_list_cost": {"amount": "500", "currency": "USD"},
      },
  )
  print(updated_session.budget.max_list_cost.amount)  # 500
  ```

  ```typescript TypeScript
  const updatedSession = await client.beta.sessions.update(session.id, {
    budget: {
      type: "limit",
      max_list_cost: { amount: "500", currency: "USD" }
    }
  });
  console.log(updatedSession.budget?.max_list_cost.amount); // 500
  ```

  ```csharp C#
  var updatedSession = await client.Beta.Sessions.Update(session.ID, new()
  {
      Budget = new()
      {
          MaxListCost = new() { Amount = "500", Currency = BetaCurrency.Usd },
      },
  });
  Console.WriteLine(updatedSession.Budget?.MaxListCost.Amount);  // 500
  ```

  ```go Go
  updatedSession, err := client.Beta.Sessions.Update(ctx, session.ID, anthropic.BetaSessionUpdateParams{
  	Budget: anthropic.BetaManagedAgentsBudgetLimitParam{
  		MaxListCost: anthropic.BetaMonetaryAmountParam{
  			Amount:   "500",
  			Currency: anthropic.BetaCurrencyUsd,
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(updatedSession.Budget.MaxListCost.Amount) // 500
  ```

  ```java Java
  var updatedSession = client.beta().sessions().update(session.id(), SessionUpdateParams.builder()
      .budget(BetaManagedAgentsBudgetLimit.builder()
          .maxListCost(BetaMonetaryAmount.builder()
              .amount("500")
              .currency(BetaCurrency.USD)
              .build())
          .build())
      .build());
  IO.println(updatedSession.budget().orElseThrow().maxListCost().amount());  // 500
  ```

  ```php PHP
  $updatedSession = $client->beta->sessions->update(
      $session->id,
      budget: [
          'type' => 'limit',
          'max_list_cost' => ['amount' => '500', 'currency' => 'USD'],
      ],
  );
  echo "{$updatedSession->budget->maxListCost->amount}\n"; // 500
  ```

  ```ruby Ruby
  updated_session = client.beta.sessions.update(
    session.id,
    budget: {
      type: "limit",
      max_list_cost: {amount: "500", currency: "USD"}
    }
  )
  puts updated_session.budget.max_list_cost.amount # 500
  ```
</CodeGroup>

### Menghapus anggaran

Berikan `"budget": null` (python: `budget=None`; typescript: `budget: null`; ruby: `budget: nil`; go: `Budget: param.NullStruct[anthropic.BetaManagedAgentsBudgetLimitParam]()`; java: `.budget(Optional.empty())`; csharp: `Budget = null`; php: `requestOptions: ['extraBodyParams' => ['budget' => null]]`; cli: `--budget null`) untuk menghapus batas sepenuhnya. Pekerjaan yang dijeda oleh anggaran dilanjutkan, dan event `session.updated` yang dihasilkan membawa `budget` (csharp, go: `Budget`) yang diatur ke `null`.

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{"budget": null}'
  ```

  ```bash CLI
  ant beta:sessions update --session-id "$SESSION_ID" --budget null
  ```

  ```python Python
  unbudgeted_session = client.beta.sessions.update(session.id, budget=None)
  print(unbudgeted_session.budget)  # None
  ```

  ```typescript TypeScript
  const unbudgetedSession = await client.beta.sessions.update(session.id, { budget: null });
  console.log(unbudgetedSession.budget); // null
  ```

  ```csharp C#
  // Menetapkan null mengirim null eksplisit; membiarkan Budget tidak diatur akan menghilangkan field tersebut.
  var unbudgetedSession = await client.Beta.Sessions.Update(session.ID, new() { Budget = null });
  Console.WriteLine(unbudgetedSession.Budget is null);  // True: the session no longer has a budget
  ```

  ```go Go
  // Budget bernilai nol dihilangkan dari permintaan; param.NullStruct (dari
  // github.com/anthropics/anthropic-sdk-go/v2/packages/param) mengirim null eksplisit.
  unbudgetedSession, err := client.Beta.Sessions.Update(ctx, session.ID, anthropic.BetaSessionUpdateParams{
  	Budget: param.NullStruct[anthropic.BetaManagedAgentsBudgetLimitParam](),
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(unbudgetedSession.JSON.Budget.Valid()) // false: the session no longer has a budget
  ```

  ```java Java
  // Optional kosong mengirim null eksplisit; membiarkan budget tidak disetel akan menghilangkan field tersebut.
  var unbudgetedSession = client.beta().sessions().update(session.id(), SessionUpdateParams.builder()
      .budget(Optional.empty())
      .build());
  IO.println(unbudgetedSession.budget().isPresent());  // false: the session no longer has a budget
  ```

  ```php PHP
  // update(budget: null) menghilangkan field tersebut, jadi kirim null eksplisit sebagai parameter body tambahan.
  $unbudgetedSession = $client->beta->sessions->update(
      $session->id,
      requestOptions: ['extraBodyParams' => ['budget' => null]],
  );
  echo json_encode($unbudgetedSession->budget), "\n"; // null
  ```

  ```ruby Ruby
  unbudgeted_session = client.beta.sessions.update(session.id, budget: nil)
  p unbudgeted_session.budget # nil
  ```
</CodeGroup>

<Warning>
  Menghapus anggaran sesi bersifat satu arah: sesi yang anggarannya telah dihapus tidak dapat diberi anggaran baru. Untuk mempertahankan batas pada sesi, ubah anggarannya saja.
</Warning>

## Memantau pengeluaran

Objek sesi membawa `budget` (csharp, go: `Budget`) miliknya dan objek `usage` (csharp, go: `Usage`) dengan pengeluaran yang dilacak: `usage.list_cost` (java, php: `usage.listCost`; csharp, go: `Usage.ListCost`) adalah biaya daftar yang telah dikonsumsi sesi, dan `usage.active_seconds` (java, php: `usage.activeSeconds`; csharp, go: `Usage.ActiveSeconds`) adalah waktu berjalan yang menjadi dasar perhitungan biaya runtime-nya. Pada sesi yang dijeda dengan `budget_reached`, harapkan `usage.list_cost` (java, php: `usage.listCost`; csharp, go: `Usage.ListCost`) bernilai sama dengan atau sedikit melewati `max_list_cost` (java, php: `maxListCost`; csharp, go: `MaxListCost`): [permintaan yang melewati batas](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget) telah selesai sebelum jeda. `active_seconds` (java, php: `activeSeconds`; csharp, go: `ActiveSeconds`) tingkat sesi menghitung aktivitas yang tumpang tindih dari thread yang berjalan bersamaan satu kali saja. Respons pengambilan thread membawa dua field yang sama pada `usage` (csharp, go: `Usage`) milik thread itu sendiri, dihitung harganya untuk setiap thread. Angka per thread dibulatkan secara independen dan tidak menyertakan biaya waktu berjalan sesi, sehingga jumlahnya tidak tepat sama dengan `list_cost` (java, php: `listCost`; csharp, go: `ListCost`) sesi; angka sesi adalah yang menjadi acuan penegakan anggaran.

Event `session.usage` adalah snapshot dari penggunaan kumulatif sesi dan biaya daftar yang dilacak. Event ini membawa total token sesi, `list_cost` (java, php: `listCost`; csharp, go: `ListCost`), `active_seconds` (java, php: `activeSeconds`; csharp, go: `ActiveSeconds`), jumlah permintaan `server_tool_use` (java, php: `serverToolUse`; csharp, go: `ServerToolUse`) (`web_search_requests` (java, php: `webSearchRequests`; csharp, go: `WebSearchRequests`), yang dihitung ke dalam biaya daftar per permintaan, dan `web_fetch_requests` (java, php: `webFetchRequests`; csharp, go: `WebFetchRequests`), yang bernilai `0` karena permintaan web fetch tidak dikenakan biaya per permintaan dan tidak diukur), serta `budget` (csharp, go: `Budget`) sesi jika sesi memilikinya. Event ini muncul dalam daftar event dan stream sesi. Sesi memancarkan satu event ini tepat sebelum menjadi idle, apa pun alasan berhentinya, sehingga sesi yang mencapai anggarannya selalu memancarkan satu event ini tepat sebelum event idle karena anggaran tercapai.

Untuk membaca penggunaan dari stream dan objek sesi, lihat [Melacak penggunaan](https://platform.claude.com/docs/id/managed-agents/session-observability#track-usage).

## Anggaran dalam sesi multiagen

Sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) memiliki satu anggaran yang dibagi di seluruh thread-nya; tidak ada batas per thread. Konsumsi setiap thread dihitung harganya berdasarkan model yang melayaninya, dan thread dijeda secara independen saat batas bersama tercapai. Konsultasi [advisor](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor) dihitung terhadap anggaran yang sama, dengan harga sesuai tarif model advisor. Satu thread dapat dijeda dengan `budget_reached` sementara thread lain menyelesaikan permintaan yang sedang berjalan.

Permintaan yang tertunda lebih diutamakan daripada batas: sesi dengan satu thread yang menunggu pada `requires_action` dan thread lain yang dijeda pada `budget_reached` melaporkan `requires_action` di tingkat sesi. Permintaan yang tertunda tetap memerlukan jawaban, dan menjawabnya merupakan [event penyelesaian](https://platform.claude.com/docs/id/managed-agents/budgets#events-accepted-at-the-cap) yang tidak diblokir oleh anggaran.

## Anggaran pada deployment

[Deployment](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments) menerima objek `budget` yang sama saat Anda membuat atau memperbaruinya:

```json
{
  "budget": {
    "type": "limit",
    "max_list_cost": { "amount": "2000", "currency": "USD" }
  }
}
```

Batas disalin ke setiap sesi yang dimulai oleh deployment, sehingga batas tersebut membatasi setiap eksekusi secara terpisah, bukan pengeluaran kumulatif deployment. Mengubah anggaran deployment berlaku untuk sesi yang dimulai deployment setelahnya, bukan untuk sesi yang sudah berjalan. Tidak seperti sesi, anggaran deployment dapat dihapus dengan `"budget": null` (python: `budget=None`; typescript: `budget: null`; ruby: `budget: nil`; go: `Budget: param.NullStruct[anthropic.BetaManagedAgentsBudgetLimitParam]()`; java: `.budget(Optional.empty())`; csharp: `Budget = null`; php: `requestOptions: ['extraBodyParams' => ['budget' => null]]`; cli: `--budget null`) dan ditetapkan lagi nanti. Lihat [Menetapkan anggaran untuk setiap eksekusi](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments#set-a-budget-on-each-run).

## Model tanpa harga daftar

Anggaran hanya dapat melacak konsumsi yang dapat dihitung harganya oleh platform. Pembuatan sesi beranggaran ditolak dengan error 400 jika salah satu dari berikut ini menggunakan model tanpa harga daftar publik:

* Agen sesi
* Agen apa pun yang tercantum dalam daftar `predefined_agents` (java, php: `predefinedAgents`; csharp, go: `PredefinedAgents`) dari `subagents` (csharp, go: `Subagents`) atau `workflows` (csharp, go: `Workflows`)
* Advisor yang ditetapkan dalam [konfigurasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) agen

Error tersebut menyatakan bahwa tidak ada harga daftar yang tersedia untuk model tersebut.

Jika penggunaan sesi beranggaran kemudian mencakup model tanpa harga daftar, anggaran tidak lagi dapat mengukur pengeluaran sesi: sesi dapat dijeda dengan `stop_reason` (java, php: `stopReason`; csharp, go: `StopReason`) bernilai `budget_reached`, dan perubahan anggaran ditolak. Hapus anggaran untuk melanjutkan sesi.

## Referensi error

Permintaan terkait anggaran ditolak dalam kasus-kasus berikut:

| Kondisi                                                                                                                                                                                                                                                      | Status |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| Event yang memulai pekerjaan (misalnya, `user.message`) dikirim saat sesi berada pada atau melebihi anggarannya; error menyebutkan [event penyelesaian yang diterima](https://platform.claude.com/docs/id/managed-agents/budgets#events-accepted-at-the-cap) | 400    |
| Anggaran ditetapkan ke nilai yang sama dengan atau di bawah biaya daftar yang telah dikonsumsi sesi                                                                                                                                                          | 400    |
| Anggaran ditambahkan ke sesi yang dibuat tanpa anggaran, atau ditambahkan kembali setelah dihapus                                                                                                                                                            | 400    |
| `amount` (csharp, go: `Amount`) bukan bilangan bulat dalam sen (misalnya, `"25.00"`), bernilai nol atau negatif, atau `currency` (csharp, go: `Currency`) bukan `USD`                                                                                        | 400    |
| Pembuatan beranggaran mereferensikan model [tanpa harga daftar publik](https://platform.claude.com/docs/id/managed-agents/budgets#models-without-a-list-price)                                                                                               | 400    |

<Note>
  Anggaran sesi adalah batas ketat dalam dolar AS (ditulis dalam sen) pada satu sesi, yang diberlakukan oleh platform. Anggaran ini berbeda dari [task budget](https://platform.claude.com/docs/id/build-with-claude/task-budgets) pada Messages API, yang merupakan anggaran bersifat anjuran dalam satuan token yang digunakan model untuk mengatur dirinya sendiri dalam satu loop agentik.
</Note>

## Ketersediaan

Anggaran sesi dalam versi beta di semua model.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tidak tersedia
* Penggunaan: Gunakan [Anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) sebagai gantinya.

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tersedia

| Status | Platform cloud               |
| ------ | ---------------------------- |
| Beta   | Semua platform yang didukung |

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
