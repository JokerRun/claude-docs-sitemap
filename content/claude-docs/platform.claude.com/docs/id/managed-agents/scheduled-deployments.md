---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/scheduled-deployments
fetched_at: 2026-10-13T02:33:54.812386Z
sha256: 24abf11eefbb170e6c57019c2266cba28db7015abe64491dc9422ac06b0fd3cc
---

---
title: Deployment terjadwal
url: https://platform.claude.com/docs/id/managed-agents/scheduled-deployments
description: "Buat dan kelola deployment dengan Claude API: jalankan agen pada jadwal cron berulang dan periksa riwayat eksekusinya."
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

**Scheduled deployment** (deployment terjadwal) memungkinkan [agen](https://platform.claude.com/docs/id/managed-agents/agent-setup) untuk memulai [sesi](https://platform.claude.com/docs/id/managed-agents/sessions) secara otonom, sehingga tugas dapat diselesaikan dengan ritme yang dapat diprediksi. Anda membuat dan mengelola deployment dengan Deployments API, bagian dari Claude API.

Untuk konteks peluncuran dan contoh hal-hal yang dijalankan tim secara terjadwal, lihat [scheduled deployments and vaults in Claude Managed Agents](https://claude.com/blog/whats-new-in-claude-managed-agents) di blog.

## Membuat deployment terjadwal

Saat membuat deployment, Anda meneruskan [konfigurasi sesi](https://platform.claude.com/docs/id/managed-agents/sessions) yang diperlukan untuk eksekusi, selain `schedule` (java, php; csharp, go: `Schedule`).

* Deployment memerlukan [konfigurasi agen](https://platform.claude.com/docs/id/managed-agents/agent-setup) dan [konfigurasi environment](https://platform.claude.com/docs/id/managed-agents/environments), serta secara opsional menerima [file](https://platform.claude.com/docs/id/managed-agents/files), [GitHub](https://platform.claude.com/docs/id/managed-agents/github), [memory store](https://platform.claude.com/docs/id/managed-agents/memory), dan [vault](https://platform.claude.com/docs/id/managed-agents/vaults). Deployment yang menargetkan [environment self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory) dapat melampirkan memory store; resource `file` dan `github_repository` memerlukan environment cloud. Formulir deployment di Claude Console saat ini tidak menawarkan memory store untuk environment self-hosted; lampirkan melalui API atau SDK sebagai gantinya.
* Deployment juga memerlukan setidaknya satu event awal, yaitu `user.message` atau `user.define_outcome`, yang memulai pekerjaan setiap sesi. Dalam file deployment untuk `ant apply`, teks di bawah frontmatter menjadi `user.message` tersebut.
* Di dalam `schedule` (java, php; csharp, go: `Schedule`), Anda mendefinisikan `expression` (java, php; csharp, go: `Expression`) cron dan `timezone` (java, php; csharp, go: `Timezone`). Granularitas maksimum yang didukung adalah tingkat menit.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/deployments?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "name": "Weekly compliance scan",
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID",
    "initial_events": [
      {"type": "user.message", "content": [{"type": "text", "text": "Run the weekly compliance scan."}]}
    ],
    "schedule": {
      "type": "cron",
      "expression": "0 20 * * 5",
      "timezone": "America/New_York"
    }
  }
  EOF
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply deployment.md
    ```

    <File filename="deployment.md">
      ```markdown
      ---
      name: Weekly compliance scan
      agent: agent_011CYm1BLqPXpQRk5khsSXrs
      environment_id: env_01595EKxaaTTGwwY3kyXdtbs
      schedule:
        type: cron
        expression: "0 20 * * 5"
        timezone: America/New_York
      ---

      Run the weekly compliance scan.
      ```
    </File>

    [`ant apply`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply) mencetak ID deployment baru dan mencatatnya di `claude-lock.json`. Untuk melihat objek deployment, jalankan `ant beta:deployments retrieve`.
  </CodeGroupItem>

  ```python Python
  deployment = client.beta.deployments.create(
      name="Weekly compliance scan",
      agent=agent.id,
      environment_id=environment.id,
      initial_events=[
          {
              "type": "user.message",
              "content": [{"type": "text", "text": "Run the weekly compliance scan."}],
          },
      ],
      schedule={
          "type": "cron",
          "expression": "0 20 * * 5",
          "timezone": "America/New_York",
      },
  )
  ```

  ```typescript TypeScript
  const deployment = await client.beta.deployments.create({
    name: "Weekly compliance scan",
    agent: agent.id,
    environment_id: environment.id,
    initial_events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "Run the weekly compliance scan." }],
      },
    ],
    schedule: {
      type: "cron",
      expression: "0 20 * * 5",
      timezone: "America/New_York",
    },
  });
  ```

  ```csharp C#
  var deployment = await client.Beta.Deployments.Create(new()
  {
      Name = "Weekly compliance scan",
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      InitialEvents =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
              Content =
              [
                  new BetaManagedAgentsTextBlock
                  {
                      Type = BetaManagedAgentsTextBlockType.Text,
                      Text = "Run the weekly compliance scan.",
                  },
              ],
          },
      ],
      Schedule = new BetaManagedAgentsScheduleParams
      {
          Type = BetaManagedAgentsScheduleParamsType.Cron,
          Expression = "0 20 * * 5",
          Timezone = "America/New_York",
      },
  });
  ```

  ```go Go
  deployment, err := client.Beta.Deployments.New(ctx, anthropic.BetaDeploymentNewParams{
  	Name:          "Weekly compliance scan",
  	Agent:         anthropic.BetaDeploymentNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
  	EnvironmentID: environment.ID,
  	InitialEvents: []anthropic.BetaManagedAgentsDeploymentInitialEventParamsUnion{{
  		OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  			Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
  			Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  				OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  					Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  					Text: "Run the weekly compliance scan.",
  				},
  			}},
  		},
  	}},
  	Schedule: anthropic.BetaManagedAgentsScheduleParams{
  		Type:       anthropic.BetaManagedAgentsScheduleParamsTypeCron,
  		Expression: "0 20 * * 5",
  		Timezone:   "America/New_York",
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var deployment = client.beta().deployments().create(
      DeploymentCreateParams.builder()
          .name("Weekly compliance scan")
          .agent(agent.id())
          .environmentId(environment.id())
          .addInitialEvent(
              BetaManagedAgentsUserMessageEventParams.builder()
                  .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                  .addTextContent("Run the weekly compliance scan.")
                  .build()
          )
          .schedule(
              BetaManagedAgentsScheduleParams.builder()
                  .type(BetaManagedAgentsScheduleParams.Type.CRON)
                  .expression("0 20 * * 5")
                  .timezone("America/New_York")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $deployment = $client->beta->deployments->create(
      name: 'Weekly compliance scan',
      agent: $agent->id,
      environmentID: $environment->id,
      initialEvents: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => 'Run the weekly compliance scan.']],
          ],
      ],
      schedule: [
          'type' => 'cron',
          'expression' => '0 20 * * 5',
          'timezone' => 'America/New_York',
      ],
  );
  ```

  ```ruby Ruby
  deployment = client.beta.deployments.create(
    name: "Weekly compliance scan",
    agent: agent.id,
    environment_id: environment.id,
    initial_events: [
      {
        type: "user.message",
        content: [{type: "text", text: "Run the weekly compliance scan."}]
      }
    ],
    schedule: {
      type: "cron",
      expression: "0 20 * * 5",
      timezone: "America/New_York"
    }
  )
  ```
</CodeGroup>

Respons mencakup objek deployment dengan `schedule.upcoming_runs_at` yang terisi waktu-waktu pemicuan berikutnya, untuk mengonfirmasi bahwa jadwal Anda telah diatur dengan benar.

```json
{
  "id": "depl_01xyz",
  "status": "active",
  "paused_reason": null,
  "schedule": {
    "type": "cron",
    "expression": "0 20 * * 5",
    "timezone": "America/New_York",
    "last_run_at": null,
    "upcoming_runs_at": [
      "2026-05-09T00:00:00Z",
      "2026-05-16T00:00:00Z",
      "2026-05-23T00:00:00Z"
    ]
  }
}
```

Timestamp eksekusi mendatang mencerminkan jadwal persis yang dikonfigurasi. Namun, untuk mendistribusikan beban, eksekusi aktual menerapkan "jitter" (variasi waktu acak) hingga 15% dari interval antar-eksekusi, dengan minimum 5 detik dan maksimum 9 menit.

Maksimum **1.000 deployment terjadwal** didukung per organisasi. Hubungi dukungan Anthropic jika Anda membutuhkan lebih banyak.

Lihat [referensi Create Deployment](https://platform.claude.com/docs/id/api/beta/deployments/create) untuk parameter lengkap dan skema respons.

### Semantik cron dan zona waktu

* **Expression:** Cron POSIX standar (`minute hour day-of-month month day-of-week`). Anda dapat membuat dan memvalidasi ekspresi cron ini di [Claude Console](https://platform.claude.com/workspaces/default/deployments).
* **Timezone:** Pengidentifikasi zona waktu IANA (misalnya, `"America/Los_Angeles"`).
* **DST:** Jadwal cron menggunakan pencocokan waktu jam dinding secara literal, sehingga `"0 20 * * *"` di `America/New_York` dipicu pada pukul 20.00 waktu lokal terlepas dari apakah EST atau EDT sedang berlaku.

<Note>
  Waktu jam dinding yang tidak ada pada hari pergeseran maju (seperti pukul 2 pagi) tidak dipicu. Waktu jam dinding yang terjadi dua kali pada hari pergeseran mundur akan dipicu dua kali. Jadwalkan di luar rentang pukul 1–3 pagi waktu lokal, atau gunakan UTC, jika eksekusi yang terlewat atau ganda tidak dapat diterima.
</Note>

### Menetapkan anggaran untuk setiap eksekusi

Teruskan objek opsional `budget` (java, php; csharp, go: `Budget`) saat Anda membuat atau memperbarui deployment. Objek ini memiliki bentuk yang sama dengan [anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets). Deployment menyalin batas tersebut ke setiap sesi yang dimulainya, sehingga anggaran membatasi setiap eksekusi secara terpisah alih-alih bertindak sebagai batas kumulatif di seluruh eksekusi: deployment dengan batas `"2000"` dapat menghabiskan hingga sekitar $20 pada setiap eksekusi.

Sesi yang dimulai oleh deployment berperilaku persis seperti sesi beranggaran lainnya: sesi dijeda dengan `budget_reached` ketika biaya daftarnya sendiri [mencapai batas](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget). Mengubah anggaran deployment berlaku untuk eksekusi yang dimulai setelahnya; sesi yang sudah berjalan mempertahankan batas yang digunakannya saat dimulai, yang dapat Anda [ubah melalui sesi itu sendiri](https://platform.claude.com/docs/id/managed-agents/session-operations#updating-the-session-budget). Tidak seperti anggaran sesi, anggaran deployment dapat dihapus dengan `"budget": null` (python: `budget=None`; typescript: `budget: null`; ruby: `budget: nil`; go: `Budget: param.NullStruct[anthropic.BetaManagedAgentsBudgetLimitParam]()`; java: `.budget(Optional.empty())`; csharp: `Budget = null`; php: `requestOptions: ['extraBodyParams' => ['budget' => null]]`; cli: `--budget null`) dan ditetapkan kembali nanti.

Contoh berikut menetapkan anggaran pada deployment yang sudah ada:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/deployments/$DEPLOYMENT_ID?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "budget": {
      "type": "limit",
      "max_list_cost": {"amount": "2000", "currency": "USD"}
    }
  }
  EOF
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply deployment.md
    ```

    <File filename="deployment.md">
      ```markdown
      ---
      name: Weekly compliance scan
      agent: agent_011CYm1BLqPXpQRk5khsSXrs
      environment_id: env_01595EKxaaTTGwwY3kyXdtbs
      schedule:
        type: cron
        expression: "0 20 * * 5"
        timezone: America/New_York
      budget:
        type: limit
        max_list_cost:
          amount: "2000"
          currency: USD
      ---

      Run the weekly compliance scan.
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  updated_deployment = client.beta.deployments.update(
      deployment.id,
      budget={
          "type": "limit",
          "max_list_cost": {"amount": "2000", "currency": "USD"},
      },
  )
  print(updated_deployment.budget.max_list_cost.amount)  # 2000
  ```

  ```typescript TypeScript
  const updatedDeployment = await client.beta.deployments.update(deployment.id, {
    budget: {
      type: "limit",
      max_list_cost: { amount: "2000", currency: "USD" },
    },
  });
  console.log(updatedDeployment.budget?.max_list_cost.amount); // 2000
  ```

  ```csharp C#
  var updatedDeployment = await client.Beta.Deployments.Update(deployment.ID, new()
  {
      Budget = new()
      {
          Type = BetaManagedAgentsBudgetLimitType.Limit,
          MaxListCost = new() { Amount = "2000", Currency = BetaCurrency.Usd },
      },
  });
  Console.WriteLine(updatedDeployment.Budget?.MaxListCost.Amount);  // 2000
  ```

  ```go Go
  updatedDeployment, err := client.Beta.Deployments.Update(ctx, deployment.ID, anthropic.BetaDeploymentUpdateParams{
  	Budget: anthropic.BetaManagedAgentsBudgetLimitParam{
  		Type: anthropic.BetaManagedAgentsBudgetLimitTypeLimit,
  		MaxListCost: anthropic.BetaMonetaryAmountParam{
  			Amount:   "2000",
  			Currency: anthropic.BetaCurrencyUsd,
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(updatedDeployment.Budget.MaxListCost.Amount) // 2000
  ```

  ```java Java
  var updatedDeployment = client.beta().deployments().update(
      deployment.id(),
      DeploymentUpdateParams.builder()
          .budget(BetaManagedAgentsBudgetLimit.builder()
              .type(BetaManagedAgentsBudgetLimit.Type.LIMIT)
              .maxListCost(BetaMonetaryAmount.builder()
                  .amount("2000")
                  .currency(BetaCurrency.USD)
                  .build())
              .build())
          .build()
  );
  IO.println(updatedDeployment.budget().orElseThrow().maxListCost().amount());  // 2000
  ```

  ```php PHP
  $updatedDeployment = $client->beta->deployments->update(
      $deployment->id,
      budget: [
          'type' => 'limit',
          'max_list_cost' => ['amount' => '2000', 'currency' => 'USD'],
      ],
  );
  echo "{$updatedDeployment->budget->maxListCost->amount}\n"; // 2000
  ```

  ```ruby Ruby
  updated_deployment = client.beta.deployments.update(
    deployment.id,
    budget: {
      type: "limit",
      max_list_cost: {amount: "2000", currency: "USD"}
    }
  )
  puts updated_deployment.budget.max_list_cost.amount # 2000
  ```
</CodeGroup>

## Eksekusi deployment

Deployment dapat gagal dipicu karena berbagai alasan: misalnya, jika resource `environment` telah diarsipkan, atau jika pembuatan sesi terkena batas laju. Setiap upaya mengeksekusi deployment menghasilkan catatan **deployment run** (eksekusi deployment), sehingga Anda dapat melacak keberhasilan dan kegagalan secara independen dari siklus hidup sesi.

Deployment yang berhasil menghasilkan sesi aktif, dan eksekusi deployment yang berhasil berisi `session_id` (java: `sessionId`; php: `sessionID`; csharp, go: `SessionID`) terkait. Untuk mengikuti siklus hidup sesi, lacak event sesi melalui [event stream](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) atau [webhook](https://platform.claude.com/docs/id/managed-agents/webhooks). Perubahan siklus hidup deployment dan hasil setiap eksekusi terjadwal juga dikirimkan sebagai event webhook, yang tercantum di tab Deployment events dan Deployment run events pada [Jenis event yang didukung](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types).

Tampilkan daftar semua eksekusi deployment untuk sebuah deployment sebagai berikut:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/deployment_runs?beta=true&deployment_id=$DEPLOYMENT_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:deployment-runs list --deployment-id "$DEPLOYMENT_ID"
  ```

  ```python Python
  for run in client.beta.deployment_runs.list(
      deployment_id=deployment.id,
  ):
      print(run.created_at, run.session_id or run.error.type)
  ```

  ```typescript TypeScript
  for await (const run of client.beta.deploymentRuns.list({
    deployment_id: deployment.id,
  })) {
    console.log(run.created_at, run.session_id ?? run.error?.type);
  }
  ```

  ```csharp C#
  var runs = await client.Beta.DeploymentRuns.List(
      new() { DeploymentID = deployment.ID }
  );
  await foreach (var run in runs.Paginate())
  {
      // The Error union exposes .Message directly; the discriminator is read
      // from .Json until a common .Type accessor is added.
      var outcome = run.SessionID ?? run.Error!.Json.GetProperty("type").GetString();
      Console.WriteLine($"{run.CreatedAt} {outcome}");
  }
  ```

  ```go Go
  runs := client.Beta.DeploymentRuns.ListAutoPaging(ctx, anthropic.BetaDeploymentRunListParams{
  	DeploymentID: anthropic.String(deployment.ID),
  })
  for runs.Next() {
  	run := runs.Current()
  	if run.SessionID != "" {
  		fmt.Println(run.CreatedAt.Format(time.RFC3339), run.SessionID)
  	} else {
  		fmt.Println(run.CreatedAt.Format(time.RFC3339), run.Error.Type)
  	}
  }
  if err := runs.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  for (var run : client.beta().deploymentRuns().list(
          DeploymentRunListParams.builder()
              .deploymentId(deployment.id())
              .build()).autoPager()) {
      // The Error union does not yet expose common .type()/.message()
      // accessors; .toString() includes both.
      IO.println(run.createdAt() + " "
          + run.sessionId().orElseGet(() -> run.error().orElseThrow().toString()));
  }
  ```

  ```php PHP
  foreach ($client->beta->deploymentRuns->list(
      deploymentID: $deployment->id,
  )->pagingEachItem() as $run) {
      $outcome = $run->sessionID ?? $run->error->type;
      echo "{$run->createdAt->format(DATE_ATOM)} {$outcome}\n";
  }
  ```

  ```ruby Ruby
  client.beta.deployment_runs.list(
    deployment_id: deployment.id
  ).auto_paging_each do
    puts "#{it.created_at} #{it.session_id || it.error.type}"
  end
  ```
</CodeGroup>

Anda juga dapat memfilter eksekusi deployment yang mengalami error:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/deployment_runs?beta=true&deployment_id=$DEPLOYMENT_ID&has_error=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:deployment-runs list --deployment-id "$DEPLOYMENT_ID" --has-error
  ```

  ```python Python
  for run in client.beta.deployment_runs.list(
      deployment_id=deployment.id,
      has_error=True,
  ):
      print(run.created_at, run.error.type, run.error.message)
  ```

  ```typescript TypeScript
  for await (const run of client.beta.deploymentRuns.list({
    deployment_id: deployment.id,
    has_error: true,
  })) {
    console.log(run.created_at, run.error?.type, run.error?.message);
  }
  ```

  ```csharp C#
  var failedRuns = await client.Beta.DeploymentRuns.List(
      new() { DeploymentID = deployment.ID, HasError = true }
  );
  await foreach (var failedRun in failedRuns.Paginate())
  {
      var error = failedRun.Error!;
      var errorType = error.Json.GetProperty("type").GetString();
      Console.WriteLine($"{failedRun.CreatedAt} {errorType} {error.Message}");
  }
  ```

  ```go Go
  failedRuns := client.Beta.DeploymentRuns.ListAutoPaging(ctx, anthropic.BetaDeploymentRunListParams{
  	DeploymentID: anthropic.String(deployment.ID),
  	HasError:     anthropic.Bool(true),
  })
  for failedRuns.Next() {
  	failedRun := failedRuns.Current()
  	fmt.Println(failedRun.CreatedAt.Format(time.RFC3339), failedRun.Error.Type, failedRun.Error.Message)
  }
  if err := failedRuns.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  for (var run : client.beta().deploymentRuns().list(
          DeploymentRunListParams.builder()
              .deploymentId(deployment.id())
              .hasError(true)
              .build()).autoPager()) {
      IO.println(run.createdAt() + " " + run.error().orElseThrow());
  }
  ```

  ```php PHP
  foreach ($client->beta->deploymentRuns->list(
      deploymentID: $deployment->id,
      hasError: true,
  )->pagingEachItem() as $run) {
      echo "{$run->createdAt->format(DATE_ATOM)} {$run->error->type} {$run->error->message}\n";
  }
  ```

  ```ruby Ruby
  client.beta.deployment_runs.list(
    deployment_id: deployment.id,
    has_error: true
  ).auto_paging_each do
    puts "#{it.created_at} #{it.error.type} #{it.error.message}"
  end
  ```
</CodeGroup>

Eksekusi yang gagal menyertakan `error` dengan `type` yang menjelaskan mengapa pembuatan sesi ditolak (misalnya, `environment_archived_error`, `agent_archived_error`, atau `session_rate_limited_error`). Lihat [referensi List Deployment Runs](https://platform.claude.com/docs/id/api/beta/deployment_runs/list) untuk semua parameter filter dan skema respons.

```json
{
  "type": "deployment_run",
  "id": "drun_01abc124",
  "deployment_id": "depl_01xyz",
  "trigger_context": { "type": "schedule", "scheduled_at": "2026-05-09T00:00:00Z" },
  "session_id": null,
  "error": {
    "type": "environment_archived_error",
    "message": "environment `env_01abc` is archived"
  },
  "agent": { "type": "agent", "id": "agent_01ghi789", "version": 3 },
  "created_at": "2026-05-09T00:00:01Z"
}
```

Untuk mengambil satu eksekusi berdasarkan ID, panggil [`GET /v1/deployment_runs/{deployment_run_id}`](https://platform.claude.com/docs/id/api/beta/deployment_runs/retrieve). [Event webhook `deployment_run`](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types) membawa ID eksekusi sebagai `data.id`-nya.

## Mengelola siklus hidup deployment

Setiap perubahan siklus hidup memancarkan [event webhook](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types), sehingga Anda dapat bereaksi terhadap deployment yang dijeda, dilanjutkan, atau diarsipkan tanpa polling; lihat tab Deployment events.

**Pause** (jeda) menghentikan pemicu terjadwal mulai saat itu dan seterusnya; sesi yang sedang berjalan dari eksekusi deployment sebelumnya tetap dieksekusi. Eksekusi manual melalui endpoint `run` tetap diizinkan selama dijeda. Menjeda akan mengatur `paused_reason` menjadi `{"type": "manual"}`; melanjutkan akan menghapusnya.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/deployments/$DEPLOYMENT_ID/pause?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:deployments pause --deployment-id "$DEPLOYMENT_ID"
  ```

  ```python Python
  client.beta.deployments.pause(deployment.id)
  ```

  ```typescript TypeScript
  await client.beta.deployments.pause(deployment.id);
  ```

  ```csharp C#
  await client.Beta.Deployments.Pause(deployment.ID);
  ```

  ```go Go
  if _, err := client.Beta.Deployments.Pause(ctx, deployment.ID, anthropic.BetaDeploymentPauseParams{}); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().deployments().pause(deployment.id());
  ```

  ```php PHP
  $client->beta->deployments->pause($deployment->id);
  ```

  ```ruby Ruby
  client.beta.deployments.pause(deployment.id)
  ```
</CodeGroup>

**Unpause** (lanjutkan) melanjutkan jadwal dari kemunculan terjadwal berikutnya. Pemicu yang terlewat tidak diisi ulang.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/deployments/$DEPLOYMENT_ID/unpause?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:deployments unpause --deployment-id "$DEPLOYMENT_ID"
  ```

  ```python Python
  client.beta.deployments.unpause(deployment.id)
  ```

  ```typescript TypeScript
  await client.beta.deployments.unpause(deployment.id);
  ```

  ```csharp C#
  await client.Beta.Deployments.Unpause(deployment.ID);
  ```

  ```go Go
  if _, err := client.Beta.Deployments.Unpause(ctx, deployment.ID, anthropic.BetaDeploymentUnpauseParams{}); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().deployments().unpause(deployment.id());
  ```

  ```php PHP
  $client->beta->deployments->unpause($deployment->id);
  ```

  ```ruby Ruby
  client.beta.deployments.unpause(deployment.id)
  ```
</CodeGroup>

**Archive** (arsipkan), tidak seperti **pause**, bersifat final: jadwal berakhir dan deployment tidak dapat dimodifikasi.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/deployments/$DEPLOYMENT_ID/archive?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:deployments archive --deployment-id "$DEPLOYMENT_ID"
  ```

  ```python Python
  client.beta.deployments.archive(deployment.id)
  ```

  ```typescript TypeScript
  await client.beta.deployments.archive(deployment.id);
  ```

  ```csharp C#
  await client.Beta.Deployments.Archive(deployment.ID);
  ```

  ```go Go
  if _, err := client.Beta.Deployments.Archive(ctx, deployment.ID, anthropic.BetaDeploymentArchiveParams{}); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().deployments().archive(deployment.id());
  ```

  ```php PHP
  $client->beta->deployments->archive($deployment->id);
  ```

  ```ruby Ruby
  client.beta.deployments.archive(deployment.id)
  ```
</CodeGroup>

### Perilaku saat gagal

Respons batas laju pembuatan sesi langsung dicatat sebagai eksekusi `session_rate_limited_error` tanpa percobaan ulang; jadwal akan mencoba lagi pada kemunculan terjadwal berikutnya. Batas laju pada panggilan API yang mendasarinya di dalam sesi ditangani oleh sesi itu sendiri.

Jika agen sebuah deployment telah diarsipkan, deployment tersebut otomatis diarsipkan dalam operasi yang sama. Jika agen telah dihapus, pemicu terjadwal berikutnya mendeteksi agen yang hilang dan secara otomatis mengarsipkan deployment. Dalam kedua kasus, tidak ada eksekusi deployment yang dicatat. Jika subagen yang direferensikan oleh agen telah diarsipkan, pemicu berikutnya mencatat eksekusi gagal dengan `error.type: "agent_archived_error"` dan deployment otomatis dijeda sehingga Anda dapat memperbarui agen dan melanjutkannya. Error pembuatan sesi lain yang tidak dapat dipulihkan, seperti environment atau vault yang diarsipkan, berperilaku sama: pemicu mencatat eksekusi gagal dan deployment otomatis dijeda. `paused_reason.error.type` milik deployment mencerminkan `error.type` dari eksekusi yang gagal.

## Memicu eksekusi manual

Untuk menjalankan deployment di luar jadwalnya, panggil [endpoint `run`](https://platform.claude.com/docs/id/api/beta/deployments/run). Ini langsung membuat sesi dan menulis eksekusi deployment dengan `trigger_context.type: "manual"`. Hal ini memungkinkan Anda menguji deployment sebelum menerapkan jadwal.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/deployments/$DEPLOYMENT_ID/run?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:deployments run --deployment-id "$DEPLOYMENT_ID"
  ```

  ```python Python
  run = client.beta.deployments.run(deployment.id)
  ```

  ```typescript TypeScript
  const run = await client.beta.deployments.run(deployment.id);
  ```

  ```csharp C#
  var manualRun = await client.Beta.Deployments.Run(deployment.ID);
  ```

  ```go Go
  manualRun, err := client.Beta.Deployments.Run(ctx, deployment.ID, anthropic.BetaDeploymentRunParams{})
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var run = client.beta().deployments().run(deployment.id());
  ```

  ```php PHP
  $run = $client->beta->deployments->run($deployment->id);
  ```

  ```ruby Ruby
  run = client.beta.deployments.run(deployment.id)
  ```
</CodeGroup>
