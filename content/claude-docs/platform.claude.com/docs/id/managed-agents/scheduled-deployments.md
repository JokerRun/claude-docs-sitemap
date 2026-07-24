---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/scheduled-deployments
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 8b475dcd73b7a67f7e688610507911de3d7b641bf8e9d85e47e7d63367836b09
---

# Deployment terjadwal

Buat dan kelola deployment dengan Claude API: jalankan agen pada jadwal cron berulang dan periksa riwayat eksekusinya.

---

Sebuah **scheduled deployment** (deployment terjadwal) memungkinkan sebuah [agen](/docs/id/managed-agents/agent-setup) untuk memulai [sesi](/docs/id/managed-agents/sessions) secara otonom, memungkinkan penyelesaian tugas dengan irama yang dapat diprediksi. Anda membuat dan mengelola deployment dengan Deployments API, bagian dari Claude API.

Untuk konteks peluncuran dan contoh apa yang dijalankan tim secara terjadwal, lihat [scheduled deployments and vaults in Claude Managed Agents](https://claude.com/blog/whats-new-in-claude-managed-agents) di blog.

<Note>
  Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK mengatur header beta secara otomatis.
</Note>

## Membuat deployment terjadwal

Saat membuat deployment, Anda meneruskan [konfigurasi sesi](/docs/id/managed-agents/sessions) yang diperlukan untuk eksekusi, selain sebuah `schedule`.

* Deployment memerlukan [konfigurasi agen](/docs/id/managed-agents/agent-setup) dan [konfigurasi lingkungan](/docs/id/managed-agents/environments), dan secara opsional menerima [file](/docs/id/managed-agents/files), [GitHub](/docs/id/managed-agents/github), [memory store](/docs/id/managed-agents/memory), dan [vault](/docs/id/managed-agents/vaults).
* Deployment juga memerlukan setidaknya satu event awal, `user.message` atau `user.define_outcome`, yang memulai pekerjaan setiap sesi.
* Dalam `schedule`, Anda mendefinisikan `expression` cron dan `timezone`. Granularitas maksimum yang didukung adalah pada tingkat menit.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  DEPLOYMENT_ID=$(
    curl --fail-with-body -sS "https://api.anthropic.com/v1/deployments?beta=true" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
      -H "content-type: application/json" \
      -d @- <<EOF | jq -er '.id'
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
  )
  ```

  ```bash CLI
  DEPLOYMENT_ID=$(ant beta:deployments create <<YAML | jq -er '.id'
  name: Weekly compliance scan
  agent: $AGENT_ID
  environment_id: $ENVIRONMENT_ID
  initial_events:
    - type: user.message
      content:
        - type: text
          text: Run the weekly compliance scan.
  schedule:
    type: cron
    expression: "0 20 * * 5"
    timezone: America/New_York
  YAML
  )
  ```

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

Respons menyertakan objek deployment dengan `schedule.upcoming_runs_at` yang terisi dengan waktu pemicuan berikutnya yang akan datang, untuk mengonfirmasi bahwa jadwal Anda telah diatur dengan benar.

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

Timestamp eksekusi yang akan datang mencerminkan jadwal persis yang dikonfigurasi. Namun, untuk mendistribusikan beban, eksekusi aktual menerapkan jitter hingga 15% dari interval antar eksekusi, dengan minimum 5 detik dan maksimum 9 menit.

Maksimum **1.000 deployment terjadwal** didukung per organisasi. Hubungi dukungan Anthropic jika Anda membutuhkan lebih banyak.

Lihat [referensi Create Deployment](/docs/id/api/beta/deployments/create) untuk parameter lengkap dan skema respons.

### Semantik cron dan zona waktu

* **Expression:** Cron POSIX standar (`minute hour day-of-month month day-of-week`). Anda dapat menghasilkan dan memvalidasi ekspresi cron ini di [Claude Console](https://platform.claude.com/workspaces/default/deployments).
* **Timezone:** Pengidentifikasi zona waktu IANA (misalnya, `"America/Los_Angeles"`).
* **DST:** Jadwal cron menggunakan pencocokan jam dinding literal, sehingga `"0 20 * * *"` di `America/New_York` terpicu pada pukul 8malam waktu setempat terlepas dari apakah EST atau EDT yang berlaku.

<Note>
  Waktu jam dinding yang tidak ada pada hari spring-forward (seperti pukul 2 pagi) tidak akan dipicu. Waktu jam dinding yang terjadi dua kali pada hari fall-back akan terpicu dua kali. Jadwalkan di luar jendela pukul 1–3 pagi waktu setempat, atau gunakan UTC, ketika eksekusi yang terlewat atau terduplikasi tidak dapat diterima.
</Note>

## Eksekusi deployment

Deployment dapat gagal terpicu karena berbagai alasan: misalnya, jika sumber daya `environment` telah diarsipkan, atau jika pembuatan sesi dibatasi oleh batas laju. Setiap upaya mengeksekusi deployment menghasilkan catatan **deployment run** (eksekusi deployment), memungkinkan Anda melacak keberhasilan dan kegagalan secara independen dari siklus hidup sesi.

Deployment yang berhasil menghasilkan sesi aktif, dan eksekusi deployment yang berhasil berisi `session_id` terkait. Untuk mengikuti siklus hidup sesi, lacak event sesi melalui [event stream](/docs/id/managed-agents/events-and-streaming) atau [webhook](/docs/id/managed-agents/webhooks). Perubahan siklus hidup deployment dan hasil dari setiap eksekusi terjadwal juga dikirimkan sebagai event webhook, yang tercantum di tab Deployment events dan Deployment run events pada [Supported event types](/docs/id/managed-agents/webhooks#supported-event-types).

Daftar semua eksekusi deployment untuk sebuah deployment sebagai berikut:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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
      // Union Error mengekspos .Message secara langsung; diskriminatornya dibaca
      // dari .Json sampai accessor .Type yang umum ditambahkan.
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
      // Union Error belum mengekspos accessor umum .type()/.message();
      // .toString() menyertakan keduanya.
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

Anda juga dapat memfilter eksekusi deployment yang memiliki error:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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

Eksekusi yang gagal menyertakan `error` dengan `type` yang menjelaskan mengapa pembuatan sesi ditolak (misalnya, `environment_archived_error`, `agent_archived_error`, atau `session_rate_limited_error`). Lihat [referensi List Deployment Runs](/docs/id/api/beta/deployment_runs/list) untuk semua parameter filter dan skema respons.

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

Untuk mengambil satu eksekusi berdasarkan ID, panggil [`GET /v1/deployment_runs/{deployment_run_id}`](/docs/id/api/beta/deployment_runs/retrieve). Sebuah [event webhook `deployment_run`](/docs/id/managed-agents/webhooks#supported-event-types) membawa ID eksekusi sebagai `data.id`-nya.

## Mengelola siklus hidup deployment

Setiap perubahan siklus hidup memancarkan [event webhook](/docs/id/managed-agents/webhooks#supported-event-types), sehingga Anda dapat bereaksi terhadap deployment yang dijeda, dilanjutkan, atau diarsipkan tanpa polling; lihat tab Deployment events.

**Pause** menekan pemicu terjadwal untuk ke depannya; sesi yang sedang berjalan dari eksekusi deployment sebelumnya tetap dieksekusi. Eksekusi manual melalui endpoint `run` masih diizinkan saat dijeda. Menjeda mengatur `paused_reason` menjadi `{"type": "manual"}`; melanjutkan akan menghapusnya.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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

**Unpause** melanjutkan jadwal dari kemunculan terjadwal berikutnya. Pemicu yang terlewat tidak akan diisi ulang.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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

**Archive**, tidak seperti **pause**, bersifat terminal: jadwal berakhir dan deployment tidak dapat dimodifikasi.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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

### Perilaku kegagalan

Respons batas laju pembuatan sesi langsung dicatat sebagai eksekusi `session_rate_limited_error` tanpa percobaan ulang; jadwal akan mencoba lagi pada kemunculan terjadwal berikutnya. Batas laju pada panggilan API yang mendasari di dalam sesi ditangani oleh sesi itu sendiri.

Jika agen dari sebuah deployment telah diarsipkan, deployment tersebut secara otomatis diarsipkan dalam operasi yang sama. Jika agen telah dihapus, pemicu terjadwal berikutnya mendeteksi agen yang hilang dan secara otomatis mengarsipkan deployment. Dalam kedua kasus tersebut, tidak ada eksekusi deployment yang dicatat. Jika subagen yang direferensikan oleh agen telah diarsipkan, pemicu berikutnya mencatat eksekusi yang gagal dengan `error.type: "agent_archived_error"` dan deployment secara otomatis dijeda sehingga Anda dapat memperbarui agen dan melanjutkan. Error pembuatan sesi lain yang tidak dapat dipulihkan, seperti environment atau vault yang diarsipkan, berperilaku dengan cara yang sama: pemicu mencatat eksekusi yang gagal dan deployment secara otomatis dijeda. `paused_reason.error.type` dari deployment mencerminkan `error.type` dari eksekusi yang gagal.

## Memicu eksekusi manual

Untuk menjalankan deployment di luar jadwalnya, panggil [endpoint `run`](/docs/id/api/beta/deployments/run). Ini membuat sesi secara langsung dan menulis eksekusi deployment dengan `trigger_context.type: "manual"`. Ini memungkinkan Anda menguji deployment sebelum berkomitmen pada jadwal.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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
