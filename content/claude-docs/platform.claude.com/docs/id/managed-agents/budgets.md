---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/budgets
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 081f05cf3221bb78cd9df975868522cc6e69fe75d6d3fe52c27acafba0ff6b20
---

---
title: Anggaran sesi
url: https://platform.claude.com/docs/id/managed-agents/budgets
description: Batasi pengeluaran sesi dengan anggaran dolar yang ketat, diberlakukan berdasarkan tarif daftar publik.
---

"Session budget" (anggaran sesi) adalah batas atas pengeluaran ketat opsional yang Anda tetapkan saat [membuat sesi](https://platform.claude.com/docs/id/managed-agents/sessions). Platform secara terus-menerus menghitung harga semua yang dikonsumsi sesi berdasarkan tarif daftar publik (**list cost** atau biaya daftar sesi) dan berhenti mengeluarkan permintaan model baru setelah biaya tersebut mencapai anggaran. Permintaan yang sedang berjalan saat batas terlampaui tetap diselesaikan, sehingga biaya daftar akhir dapat berakhir [sedikit melewati anggaran](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget). Sesi yang mencapai anggarannya akan dijeda dan menjadi [idle](https://platform.claude.com/docs/id/managed-agents/session-operations#session-statuses) alih-alih dihentikan; mengubah atau menghapus anggaran akan melanjutkan pekerjaannya secara otomatis. Deployment menerima anggaran yang sama dan menerapkannya ke setiap sesi yang dimulainya; lihat [Anggaran pada deployment](https://platform.claude.com/docs/id/managed-agents/budgets#budgets-on-deployments).

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK menetapkan header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Menetapkan anggaran saat pembuatan sesi

Teruskan field opsional `budget` saat Anda membuat sesi:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  session=$(curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID",
    "budget": {
      "type": "limit",
      "max_list_cost": {"amount": "125", "currency": "USD"}
    }
  }
  EOF
  )
  SESSION_ID=$(jq -r '.id' <<< "$session")
  ```

  ```bash CLI
  # Biarkan jumlah tetap dalam tanda kutip agar dikirim sebagai string, bukan angka.
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --budget '{type: limit, max_list_cost: {amount: "125", currency: USD}}' \
    --transform id --raw-output)
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
          Type = BetaManagedAgentsBudgetLimitType.Limit,
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
  		Type: anthropic.BetaManagedAgentsBudgetLimitTypeLimit,
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
          .type(BetaManagedAgentsBudgetLimit.Type.LIMIT)
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

Objek `budget` memiliki dua field:

* `type` selalu bernilai `"limit"`.
* `max_list_cost` adalah batas itu sendiri: `amount` adalah bilangan bulat dalam sen AS yang ditulis sebagai string tanpa nol di depan (`"125"` berarti $1,25 dan `"50"` berarti 50 sen) dan harus lebih besar dari nol. Bentuk desimal seperti `"25.00"` ditolak. Nilai amount berupa string, bukan angka, sehingga tidak pernah ada pembulatan float yang diterapkan padanya. `currency` adalah kode mata uang ISO-4217 dalam huruf kapital; `USD` adalah satu-satunya mata uang yang didukung.

Anggaran hanya dapat dilampirkan saat sesi dibuat. Menambahkan anggaran ke sesi yang sudah ada dan belum memilikinya akan ditolak dengan error 400. Batas pada sesi yang memiliki anggaran dapat [diubah](https://platform.claude.com/docs/id/managed-agents/budgets#change-the-budget) atau [dihapus](https://platform.claude.com/docs/id/managed-agents/budgets#remove-the-budget) kapan saja.

## Cara biaya daftar diukur

Platform menghitung harga apa yang dikonsumsi sesi, secara terus-menerus, berdasarkan tarif daftar publik:

* **Token model**, berdasarkan harga daftar setiap model yang dilayani
* **Pencarian web**, seharga $10 per 1.000 pencarian
* **Waktu berjalan sesi**, seharga $0,08 per jam

Total dolar berjalan ini adalah **biaya daftar** (list cost) sesi, dan inilah yang dibandingkan dengan anggaran. Biaya daftar bukanlah harga kontrak Anda: jika organisasi Anda telah menegosiasikan diskon, sesi mencapai batasnya ketika total harga daftar mencapainya, dan pengeluaran yang ditagihkan kepada Anda mungkin lebih rendah dari batas tersebut.

Pemberlakuan menggunakan biaya daftar yang tepat dan tidak dibulatkan. Angka `list_cost` yang dilaporkan pada sesi dan event-nya berupa sen bulat, dibulatkan ke sen terdekat, sehingga angka yang dilaporkan dapat berbeda hingga setengah sen di atas atau di bawah jumlah tepat yang digunakan pemberlakuan.

## Ketika sesi mencapai anggarannya

Batas diberlakukan di antara permintaan model, bukan di tengah permintaan. Sebelum setiap permintaan model, platform memeriksa biaya daftar yang telah dikonsumsi sesi, dan setelah total tersebut mencapai batas, setiap thread dijeda sebelum permintaan berikutnya. Permintaan yang membawa total melewati batas diterima saat sesi masih di bawah batas dan berjalan hingga selesai, sehingga `list_cost` yang tercatat pada sesi yang dijeda bernilai sama dengan atau sedikit melewati `max_list_cost`: sesi dengan batas `"50"` (50 sen) dapat dijeda dengan `list_cost` sebesar `"53"`. Ini adalah hal yang diharapkan, bukan kesalahan penagihan, dan kelebihannya dibatasi oleh satu permintaan model per thread. Perlakukan anggaran sebagai batas untuk pekerjaan baru, bukan titik berhenti yang tepat, dan tentukan ukuran batas dengan mempertimbangkan margin satu permintaan tersebut.

Sesi yang mencapai anggarannya menjadi idle dengan `stop_reason` bernilai `budget_reached`; sesi tidak dihentikan, dan riwayat serta sandbox-nya dipertahankan seperti sesi idle lainnya. Pada [event stream](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) Anda akan melihat, secara berurutan:

1. Event `session.thread_status_idle` dengan `stop_reason` bernilai `budget_reached` saat setiap thread dijeda.
2. Event [`session.usage`](https://platform.claude.com/docs/id/managed-agents/budgets#monitor-spend) dengan penggunaan kumulatif dan biaya daftar sesi.
3. Event `session.status_idle` dengan `stop_reason` bernilai `budget_reached`. Event usage selalu langsung mendahului event idle ini.

Thread yang permintaan terakhirnya melewati batas sekaligus menyelesaikan gilirannya melaporkan `end_turn` pada event `session.thread_status_idle` miliknya sendiri, sementara sesi tetap melaporkan `budget_reached`; perlakukan `stop_reason` tingkat sesi sebagai sinyal bahwa sesi dijeda pada anggarannya.

### Event yang diterima pada batas

Selama sesi berada pada atau melebihi anggarannya, sesi hanya menerima event yang menyelesaikan pekerjaan yang sudah berjalan:

* `user.tool_confirmation`
* `user.tool_result`
* `user.custom_tool_result`
* `user.interrupt`

Event apa pun yang akan memulai pekerjaan baru, seperti `user.message`, ditolak dengan error 400 yang menyebutkan daftar ini. Hasil yang diselesaikan dicatat tanpa memicu permintaan model baru; sesi tetap dijeda pada anggarannya.

`user.interrupt` yang dikirim saat sesi dijeda pada anggarannya (semua thread dijeda pada batas) diterima dan diabaikan: event tersebut tidak muncul dalam daftar event dan tidak mengubah apa pun. Ubah atau hapus anggaran untuk melanjutkan.

## Melanjutkan sesi yang mencapai anggarannya

Ubah atau hapus anggaran dengan pembaruan sesi. Pembaruan yang diterima akan melanjutkan pekerjaan sesi yang dijeda secara otomatis; tidak diperlukan tindakan klien lebih lanjut.

### Mengubah anggaran

Perbarui sesi dengan `max_list_cost` baru. Nilai baru dapat lebih tinggi atau lebih rendah dari batas saat ini, tetapi harus benar-benar lebih besar dari biaya daftar yang telah dikonsumsi sesi; jika tidak, pembaruan ditolak dengan error 400: `budget.max_list_cost must be greater than the session's consumed list cost`. Karena biaya yang dikonsumsi biasanya berada [sedikit melewati batas lama](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget) saat sesi dijeda, dasarkan nilai baru pada `usage.list_cost` yang dilaporkan sesi, bukan pada `max_list_cost` lama. Tetapkan satu sen atau lebih di atas angka tersebut: nilai yang dilaporkan dibulatkan dan dapat berada sedikit di bawah biaya konsumsi tepat yang digunakan pemeriksaan.

<CodeGroup defaultLanguage="CLI">
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
          Type = BetaManagedAgentsBudgetLimitType.Limit,
          MaxListCost = new() { Amount = "500", Currency = BetaCurrency.Usd },
      },
  });
  Console.WriteLine(updatedSession.Budget?.MaxListCost.Amount);  // 500
  ```

  ```go Go
  updatedSession, err := client.Beta.Sessions.Update(ctx, session.ID, anthropic.BetaSessionUpdateParams{
  	Budget: anthropic.BetaManagedAgentsBudgetLimitParam{
  		Type: anthropic.BetaManagedAgentsBudgetLimitTypeLimit,
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
          .type(BetaManagedAgentsBudgetLimit.Type.LIMIT)
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

Tetapkan `budget` ke `null` untuk menghapus batas sepenuhnya. Pekerjaan sesi yang dijeda dilanjutkan, dan event `session.updated` yang dihasilkan membawa `budget` bernilai `null`.

<CodeGroup defaultLanguage="CLI">
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
  // github.com/anthropics/anthropic-sdk-go/packages/param) mengirim null eksplisit.
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
  // update(budget: null) menghilangkan field tersebut, jadi kirim null eksplisit melalui klien mentah.
  $unbudgetedSession = $client->beta->sessions->raw
      ->update($session->id, ['budget' => null])
      ->parse();
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

Objek sesi membawa `budget` miliknya dan objek `usage` dengan pengeluaran yang dilacak: `usage.list_cost` adalah biaya daftar yang telah dikonsumsi sesi, dan `usage.active_seconds` adalah waktu berjalan yang menjadi dasar penghitungan biaya runtime-nya. Pada sesi yang dijeda dengan `budget_reached`, perkirakan `usage.list_cost` bernilai sama dengan atau sedikit melewati `max_list_cost`: [permintaan yang melewati batas](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget) selesai sebelum jeda. `active_seconds` tingkat sesi menghitung aktivitas yang tumpang tindih dari thread konkuren hanya sekali. Respons pengambilan thread membawa dua field yang sama pada `usage` milik thread itu sendiri, dihitung per thread. Angka per thread dibulatkan secara independen dan tidak mencakup biaya waktu berjalan sesi, sehingga jumlahnya tidak persis sama dengan `list_cost` sesi; angka sesi adalah angka yang menjadi acuan pemberlakuan anggaran.

Event `session.usage` adalah snapshot penggunaan kumulatif sesi dan biaya daftar yang dilacak. Event ini membawa total token sesi, `list_cost`, `active_seconds`, jumlah permintaan `server_tool_use` (`web_search_requests`, yang dihitung ke dalam biaya daftar per permintaan, dan `web_fetch_requests`, yang bernilai `0` karena permintaan web fetch tidak dikenai biaya per permintaan dan tidak diukur), serta salinan `budget` sesi, atau `null` jika sesi tidak memilikinya. Event ini muncul dalam daftar event dan stream sesi. Sesi memancarkan satu event ini tepat sebelum menjadi idle, apa pun alasan berhentinya, sehingga sesi yang mencapai anggarannya selalu memancarkan satu event ini tepat sebelum event idle budget-reached.

Untuk membaca penggunaan dari stream dan objek sesi, lihat [Melacak penggunaan](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#tracking-usage).

## Anggaran dalam sesi multiagen

Sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) memiliki satu anggaran yang dibagi di antara semua thread-nya; tidak ada batas per thread. Konsumsi setiap thread dihitung berdasarkan model yang dilayaninya sendiri, dan thread dijeda secara independen saat batas bersama tercapai. Konsultasi [advisor](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor) dihitung terhadap anggaran yang sama, dengan harga berdasarkan tarif model advisor. Satu thread dapat dijeda pada `budget_reached` sementara thread lain menyelesaikan permintaannya yang sedang berjalan.

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

Batas disalin ke setiap sesi yang dimulai deployment, sehingga batas tersebut membatasi setiap run secara terpisah, bukan pengeluaran kumulatif deployment. Mengubah anggaran deployment berlaku untuk sesi yang dimulai deployment setelahnya, bukan untuk sesi yang sudah berjalan. Tidak seperti sesi, anggaran deployment dapat dihapus dengan `null` dan ditetapkan kembali nanti. Lihat [Menetapkan anggaran pada setiap run](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments#set-a-budget-on-each-run).

## Model tanpa harga daftar

Anggaran hanya dapat melacak konsumsi yang dapat dihitung harganya oleh platform. Membuat sesi beranggaran yang agennya, atau agen maupun advisor mana pun pada [daftar multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration)-nya, menggunakan model tanpa harga daftar publik akan ditolak dengan error 400 yang menyatakan bahwa tidak ada harga daftar yang tersedia untuk model tersebut.

Jika penggunaan sesi beranggaran kemudian mencakup model tanpa harga daftar, anggaran tidak dapat lagi mengukur pengeluaran sesi: sesi dapat dijeda dengan `stop_reason` bernilai `budget_reached`, dan mengubah anggaran akan ditolak. Hapus anggaran untuk melanjutkan sesi.

## Referensi error

Permintaan terkait anggaran ditolak dalam kasus-kasus berikut:

| Kondisi                                                                                                                                                                                                                                                      | Status |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| Event yang memulai pekerjaan (misalnya, `user.message`) dikirim saat sesi berada pada atau melebihi anggarannya; error menyebutkan [event penyelesaian yang diterima](https://platform.claude.com/docs/id/managed-agents/budgets#events-accepted-at-the-cap) | 400    |
| Anggaran ditetapkan ke nilai yang sama dengan atau di bawah biaya daftar yang telah dikonsumsi sesi                                                                                                                                                          | 400    |
| Anggaran ditambahkan ke sesi yang dibuat tanpa anggaran, atau ditambahkan kembali setelah dihapus                                                                                                                                                            | 400    |
| `amount` bukan bilangan bulat dalam sen (misalnya, `"25.00"`), bernilai nol atau negatif, atau `currency` bukan `USD`                                                                                                                                        | 400    |
| Pembuatan beranggaran mereferensikan model [tanpa harga daftar publik](https://platform.claude.com/docs/id/managed-agents/budgets#models-without-a-list-price)                                                                                               | 400    |

<Note>
  Anggaran sesi adalah batas ketat dalam dolar AS (ditulis dalam sen) pada satu sesi, yang diberlakukan oleh platform. Anggaran ini berbeda dari [task budget](https://platform.claude.com/docs/id/build-with-claude/task-budgets) pada Messages API, yang merupakan anggaran bersifat anjuran dalam satuan token yang digunakan model untuk mengatur dirinya sendiri dalam satu loop agentik.
</Note>
