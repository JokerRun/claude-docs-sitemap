---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/scheduled-deployments
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 488ca6eca0608789ac301b27d1d9fbd0da5c32c4ea01f94854591f07ddcba13d
---

# Deployment terjadwal

Jalankan agen pada jadwal cron berulang dan periksa riwayat eksekusinya.

---

Sebuah **scheduled deployment** (deployment terjadwal) memungkinkan sebuah [agen](/docs/id/managed-agents/agent-setup) untuk memulai [sesi](/docs/id/managed-agents/sessions) secara otonom, memungkinkan penyelesaian tugas dengan irama yang dapat diprediksi.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK mengatur header beta secara otomatis.
</Note>

## Membuat scheduled deployment \{#create-a-scheduled-deployment}

Saat membuat deployment, Anda meneruskan [konfigurasi sesi](/docs/id/managed-agents/sessions) yang diperlukan untuk eksekusi, selain sebuah `schedule`.

- Deployment memerlukan [konfigurasi agen](/docs/id/managed-agents/agent-setup) dan [konfigurasi lingkungan](/docs/id/managed-agents/environments), dan secara opsional menerima [file](/docs/id/managed-agents/files), [GitHub](/docs/id/managed-agents/github), [memory store](/docs/id/managed-agents/memory), dan [vault](/docs/id/managed-agents/vaults).
- Deployment juga memerlukan event `user.message` awal yang memulai pekerjaan sesi.
- Dalam `schedule`, Anda mendefinisikan sebuah `expression` cron dan sebuah `timezone`. Granularitas maksimum yang didukung adalah pada tingkat menit.

<CodeGroup defaultLanguage="CLI">
  
````bash
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
````

  
````bash
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
````

  
````python
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
````

  
````typescript
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
````

  
````csharp
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
````

  
````go
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
````

  
````java
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
````

  
````php
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
````

  
````ruby
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
````

</CodeGroup>

Respons menyertakan objek deployment dengan `schedule.upcoming_runs_at` yang terisi dengan waktu pemicuan mendatang berikutnya, untuk mengonfirmasi bahwa jadwal Anda telah diatur dengan benar.

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

Timestamp eksekusi mendatang didasarkan pada jadwal persis yang dikonfigurasi. Namun, untuk mendistribusikan beban, deployment dapat menerapkan jitter hingga 10 detik.

Maksimum **1.000 scheduled deployment** didukung per organisasi. Hubungi dukungan Anthropic jika Anda membutuhkan lebih banyak.

### Semantik cron dan timezone \{#cron-and-timezone-semantics}

- **Expression:** Cron POSIX standar (`minute hour day-of-month month day-of-week`). Anda dapat menghasilkan dan memvalidasi ekspresi cron ini di [Claude Console](https://platform.claude.com/workspaces/default/deployments).
- **Timezone:** Pengidentifikasi timezone IANA (misalnya, `"America/Los_Angeles"`).
- **DST:** Jadwal cron menggunakan pencocokan waktu jam dinding secara literal, sehingga `"0 20 * * *"` di `America/New_York` terpicu pada pukul 8:00 malam waktu setempat terlepas dari apakah EST atau EDT sedang berlaku.

<Note>
Waktu jam dinding yang tidak ada pada hari spring-forward (seperti pukul 2 pagi) tidak dipicu. Waktu jam dinding yang terjadi dua kali pada hari fall-back terpicu dua kali. Jadwalkan di luar jendela pukul 1–3 pagi waktu setempat, atau gunakan UTC, ketika eksekusi yang terlewat atau duplikat tidak dapat diterima.
</Note>

## Deployment run \{#deployment-runs}

Deployment dapat gagal terpicu karena berbagai alasan: misalnya, jika sumber daya `environment` telah diarsipkan, atau jika pembuatan sesi dibatasi oleh batas laju. Setiap upaya mengeksekusi deployment menghasilkan catatan **deployment run**, memungkinkan Anda melacak keberhasilan dan kegagalan secara independen dari siklus hidup sesi.

Deployment yang berhasil menghasilkan sesi aktif, dan deployment run yang berhasil berisi `session_id` terkait. Untuk mengikuti siklus hidup sesi, lacak event sesi melalui [event stream](/docs/id/managed-agents/events-and-streaming) atau [webhooks](/docs/id/managed-agents/webhooks).

Daftarkan semua deployment run untuk sebuah deployment sebagai berikut:

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS "https://api.anthropic.com/v1/deployment_runs?beta=true&deployment_id=$DEPLOYMENT_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:deployment-runs list --deployment-id "$DEPLOYMENT_ID"
````

  
````python
for run in client.beta.deployment_runs.list(
    deployment_id=deployment.id,
):
    print(run.created_at, run.session_id or run.error.type)
````

  
````typescript
for await (const run of client.beta.deploymentRuns.list({
  deployment_id: deployment.id,
})) {
  console.log(run.created_at, run.session_id ?? run.error?.type);
}
````

  
````csharp
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
````

  
````go
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
````

  
````java
for (var run : client.beta().deploymentRuns().list(
        DeploymentRunListParams.builder()
            .deploymentId(deployment.id())
            .build()).autoPager()) {
    // The Error union does not yet expose common .type()/.message()
    // accessors; .toString() includes both.
    IO.println(run.createdAt() + " "
        + run.sessionId().orElseGet(() -> run.error().orElseThrow().toString()));
}
````

  
````php
foreach ($client->beta->deploymentRuns->list(
    deploymentID: $deployment->id,
)->pagingEachItem() as $run) {
    $outcome = $run->sessionID ?? $run->error->type;
    echo "{$run->createdAt->format(DATE_ATOM)} {$outcome}\n";
}
````

  
````ruby
client.beta.deployment_runs.list(
  deployment_id: deployment.id
).auto_paging_each do
  puts "#{it.created_at} #{it.session_id || it.error.type}"
end
````

</CodeGroup>

Anda juga dapat memfilter deployment run yang memiliki error:

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS "https://api.anthropic.com/v1/deployment_runs?beta=true&deployment_id=$DEPLOYMENT_ID&has_error=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:deployment-runs list --deployment-id "$DEPLOYMENT_ID" --has-error
````

  
````python
for run in client.beta.deployment_runs.list(
    deployment_id=deployment.id,
    has_error=True,
):
    print(run.created_at, run.error.type, run.error.message)
````

  
````typescript
for await (const run of client.beta.deploymentRuns.list({
  deployment_id: deployment.id,
  has_error: true,
})) {
  console.log(run.created_at, run.error?.type, run.error?.message);
}
````

  
````csharp
var failedRuns = await client.Beta.DeploymentRuns.List(
    new() { DeploymentID = deployment.ID, HasError = true }
);
await foreach (var failedRun in failedRuns.Paginate())
{
    var error = failedRun.Error!;
    var errorType = error.Json.GetProperty("type").GetString();
    Console.WriteLine($"{failedRun.CreatedAt} {errorType} {error.Message}");
}
````

  
````go
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
````

  
````java
for (var run : client.beta().deploymentRuns().list(
        DeploymentRunListParams.builder()
            .deploymentId(deployment.id())
            .hasError(true)
            .build()).autoPager()) {
    IO.println(run.createdAt() + " " + run.error().orElseThrow());
}
````

  
````php
foreach ($client->beta->deploymentRuns->list(
    deploymentID: $deployment->id,
    hasError: true,
)->pagingEachItem() as $run) {
    echo "{$run->createdAt->format(DATE_ATOM)} {$run->error->type} {$run->error->message}\n";
}
````

  
````ruby
client.beta.deployment_runs.list(
  deployment_id: deployment.id,
  has_error: true
).auto_paging_each do
  puts "#{it.created_at} #{it.error.type} #{it.error.message}"
end
````

</CodeGroup>

Run yang gagal menyertakan `error` dengan `type` yang menjelaskan mengapa pembuatan sesi ditolak (misalnya, `environment_archived_error`, `agent_archived_error`, atau `session_rate_limited_error`).

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

## Mengelola siklus hidup deployment \{#managing-deployment-lifecycle}

**Pause** menekan pemicu terjadwal ke depannya; sesi yang sedang berjalan dari deployment run sebelumnya terus dieksekusi. Run manual melalui endpoint `run` masih diizinkan saat dijeda. Menjeda mengatur `paused_reason` menjadi `{"type": "manual"}`; membatalkan jeda menghapusnya.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/deployments/$DEPLOYMENT_ID/pause?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:deployments pause --deployment-id "$DEPLOYMENT_ID"
````

  
````python
client.beta.deployments.pause(deployment.id)
````

  
````typescript
await client.beta.deployments.pause(deployment.id);
````

  
````csharp
await client.Beta.Deployments.Pause(deployment.ID);
````

  
````go
if _, err := client.Beta.Deployments.Pause(ctx, deployment.ID, anthropic.BetaDeploymentPauseParams{}); err != nil {
	panic(err)
}
````

  
````java
client.beta().deployments().pause(deployment.id());
````

  
````php
$client->beta->deployments->pause($deployment->id);
````

  
````ruby
client.beta.deployments.pause(deployment.id)
````

</CodeGroup>

**Unpause** melanjutkan jadwal dari kemunculan terjadwal berikutnya. Pemicu yang terlewat tidak dijalankan ulang.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/deployments/$DEPLOYMENT_ID/unpause?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:deployments unpause --deployment-id "$DEPLOYMENT_ID"
````

  
````python
client.beta.deployments.unpause(deployment.id)
````

  
````typescript
await client.beta.deployments.unpause(deployment.id);
````

  
````csharp
await client.Beta.Deployments.Unpause(deployment.ID);
````

  
````go
if _, err := client.Beta.Deployments.Unpause(ctx, deployment.ID, anthropic.BetaDeploymentUnpauseParams{}); err != nil {
	panic(err)
}
````

  
````java
client.beta().deployments().unpause(deployment.id());
````

  
````php
$client->beta->deployments->unpause($deployment->id);
````

  
````ruby
client.beta.deployments.unpause(deployment.id)
````

</CodeGroup>

**Archive**, tidak seperti **pause**, bersifat terminal: jadwal berakhir dan deployment tidak dapat dimodifikasi.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/deployments/$DEPLOYMENT_ID/archive?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:deployments archive --deployment-id "$DEPLOYMENT_ID"
````

  
````python
client.beta.deployments.archive(deployment.id)
````

  
````typescript
await client.beta.deployments.archive(deployment.id);
````

  
````csharp
await client.Beta.Deployments.Archive(deployment.ID);
````

  
````go
if _, err := client.Beta.Deployments.Archive(ctx, deployment.ID, anthropic.BetaDeploymentArchiveParams{}); err != nil {
	panic(err)
}
````

  
````java
client.beta().deployments().archive(deployment.id());
````

  
````php
$client->beta->deployments->archive($deployment->id);
````

  
````ruby
client.beta.deployments.archive(deployment.id)
````

</CodeGroup>

### Perilaku kegagalan \{#failure-behavior}

Respons batas laju pembuatan sesi dicatat segera sebagai run `session_rate_limited_error` tanpa percobaan ulang; jadwal mencoba lagi pada kemunculan terjadwal berikutnya. Batas laju pada panggilan API yang mendasari dalam sebuah sesi ditangani oleh sesi itu sendiri.

Jika agen dari sebuah deployment telah diarsipkan atau dihapus, deployment tersebut secara otomatis diarsipkan dalam operasi yang sama; tidak ada deployment run yang dicatat. Jika subagen yang direferensikan oleh agen telah diarsipkan, pemicu berikutnya mencatat run yang gagal dengan `error.type: "agent_archived_error"` dan deployment secara otomatis dijeda sehingga Anda dapat memperbarui agen dan melanjutkan.

## Memicu run manual \{#trigger-a-manual-run}

Untuk menjalankan deployment di luar jadwalnya, panggil endpoint `run`. Ini membuat sesi segera dan menulis deployment run dengan `trigger_context.type: "manual"`. Ini memungkinkan Anda menguji deployment sebelum berkomitmen pada jadwal.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/deployments/$DEPLOYMENT_ID/run?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:deployments run --deployment-id "$DEPLOYMENT_ID"
````

  
````python
run = client.beta.deployments.run(deployment.id)
````

  
````typescript
const run = await client.beta.deployments.run(deployment.id);
````

  
````csharp
var manualRun = await client.Beta.Deployments.Run(deployment.ID);
````

  
````go
manualRun, err := client.Beta.Deployments.Run(ctx, deployment.ID, anthropic.BetaDeploymentRunParams{})
if err != nil {
	panic(err)
}
````

  
````java
var run = client.beta().deployments().run(deployment.id());
````

  
````php
$run = $client->beta->deployments->run($deployment->id);
````

  
````ruby
run = client.beta.deployments.run(deployment.id)
````

</CodeGroup>