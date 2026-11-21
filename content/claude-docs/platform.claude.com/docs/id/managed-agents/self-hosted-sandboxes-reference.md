---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference
fetched_at: 2026-11-21T02:12:50.066053Z
sha256: 353f014f5b087bfaca2a7166874753f7cb7af2df0b4dca1d72693d35c82482b9
---

---
title: Referensi worker self-hosted
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference
description: "Referensi untuk worker sandbox self-hosted: flag CLI ant, variabel lingkungan, persyaratan host, path sistem file, dan opsi helper SDK."
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Tidak memiliki kelayakan ZDR, kecuali untuk Managed Agents yang di-host sendiri. Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya.
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
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

Halaman ini mendokumentasikan worker siap pakai yang melayani environment `self_hosted`. Untuk panduan berorientasi tugas, mulailah dengan [Sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) dan [Menerapkan worker self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers).

## Perintah dan flag CLI

| Perintah | Deskripsi |
| ----- | ----- |
| `ant beta:worker poll` | Mengklaim item pekerjaan dari antrean environment dan menjalankan setiap sesi di dalam proses. Dengan `--on-work`, memanggil skrip Anda untuk setiap item pekerjaan sebagai gantinya. |
| `ant beta:worker run` | Menangani satu sesi yang diklaim lalu keluar. Gunakan sebagai entrypoint dari sandbox per sesi. |

| Flag | Deskripsi |
| ----- | ----- |
| `--environment-id` | Environment yang di-poll untuk mendapatkan pekerjaan. Juga dibaca dari `ANTHROPIC_ENVIRONMENT_ID`. |
| `--environment-key` | Mengautentikasi worker dengan environment ini. Juga dibaca dari `ANTHROPIC_ENVIRONMENT_KEY`. |
| `--workdir` | Direktori tempat worker mengunduh skill, dan tempat alat membaca serta menulis file. Default-nya `.` (direktori saat ini). Direktori ini harus sudah ada sebelum worker dimulai. |
| `--on-work` | Skrip yang dipanggil untuk setiap item pekerjaan yang diklaim alih-alih menjalankan alat di dalam proses. Menerima detail sesi sebagai variabel lingkungan dan item pekerjaan sebagai JSON pada standard input. |
| `--max-idle` | Berapa lama worker menunggu selama sesi dalam keadaan idle sebelum `ant beta:worker run` keluar atau `ant beta:worker poll` beralih ke item pekerjaan berikutnya. Waktu idle dengan [alasan berhenti `requires_action`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#respond-when-the-session-goes-idle) tidak dihitung. Default-nya `60s`. Atur ke `0` untuk menonaktifkan batas waktu. Dengan skrip `--on-work`, `ant beta:worker poll` mengabaikan flag ini. Sebagai gantinya, teruskan flag ini ke perintah `ant beta:worker run` yang dijalankan oleh skrip Anda. |
| `--log-format` | Format output log. Gunakan `json` untuk penyerapan log terstruktur. Default-nya `text`. |

## Variabel lingkungan

| Variabel | Deskripsi | Diatur oleh |
| ----- | ----- | ----- |
| `ANTHROPIC_ENVIRONMENT_ID` | Environment yang antreannya dilayani oleh worker. | Anda, di host worker. Poller meneruskannya ke skrip `--on-work`. |
| `ANTHROPIC_ENVIRONMENT_KEY` | Mengautentikasi worker ke antreannya. | Anda, di host worker. Poller meneruskannya ke skrip `--on-work`. |
| `ANTHROPIC_SESSION_ID` | Sesi yang diwakili oleh item pekerjaan yang diklaim. | Poller, untuk skrip `--on-work`. |
| `ANTHROPIC_WORK_ID` | Item pekerjaan yang diklaim. | Poller, untuk skrip `--on-work`. |
| `ANTHROPIC_WORK_SECRET` | Secret milik item pekerjaan untuk sesinya. | Anda. Poller tidak mengaturnya. Lihat [Meneruskan secret item pekerjaan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#forward-the-work-items-secret). |
| `ANTHROPIC_BASE_URL` | Menimpa endpoint API default. Opsional. | Anda, di host worker. |
| `ANTHROPIC_WEBHOOK_SIGNING_KEY` | Memverifikasi payload webhook yang masuk. | Anda, di host penangan webhook. |

## Persyaratan host

| Worker | Persyaratan |
| ----- | ----- |
| Semua worker | Host Linux atau macOS dengan `/bin/bash` tepat di path tersebut. Alat `bash` milik worker menjalankannya secara langsung, tanpa merujuk ke `PATH`. Di macOS, itu adalah Bash 3.2 bawaan sistem. |
| TypeScript SDK | `unzip` dan `tar` pada `PATH`, serta Node.js 22 atau lebih baru. |
| Python dan Go SDK | Tidak ada binary tambahan. SDK ini menggunakan pustaka standarnya untuk ekstraksi arsip. |

[Memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#requirements) menambahkan persyaratannya sendiri.

Di macOS, volume root bersifat read-only, sehingga `mkdir` tidak dapat membuat `/workspace`. Atur direktori kerja worker ke direktori yang dapat Anda tulisi, seperti direktori `workspace` di direktori home Anda. Untuk menggunakan memory store di macOS, terlebih dahulu [siapkan host macOS](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#prepare-a-macos-host).

## Sistem file sandbox

| Path | Isi |
| ----- | ----- |
| `/workspace` | Direktori kerja dalam contoh-contoh di halaman sandbox self-hosted. Ini bukan default worker: worker menggunakan direktori saat ini kecuali Anda mengatur `--workdir` atau `workdir` (go: `Workdir`). Sandbox cloud Anthropic menyimpan skill dan repositori di `/workspace`. Jika Anda menggunakan direktori kerja yang berbeda, perbarui prompt sistem agen Anda agar Claude dapat menemukan file skill. |
| `<workdir>/skills/<name>/` | Skill agen yang telah diunduh. |
| `/mnt/memory/<store>/` | Salinan lokal dari setiap memory store yang terlampir, satu direktori per store. API mengembalikan path lengkap setiap direktori di field `mount_path` (java, php: `mountPath`; csharp, go: `MountPath`) pada resource memory store milik sesi (misalnya, `/mnt/memory/user-preferences/`). |

Worker membuat direktori memory store saat mengklaim sesi. Worker menghapusnya saat selesai menangani sesi tersebut atau saat Anda [menghentikan worker dengan baik](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#stop-workers-gracefully). Tindakan ini hanya menghapus salinan lokal, dan memori tetap berada di store.

Skill dapat menyertakan file yang dapat dieksekusi, yang bisa langsung dijalankan oleh agen. Worker CLI dan SDK mempertahankan izin eksekusi yang tercatat dalam bundel skill saat mengekstraknya. Jika Anda mengunduh skill sendiri, atur sendiri izin eksekusinya.

### Saat worker selesai menangani sesi

Worker selesai menangani sesi dalam salah satu kasus berikut:

* Sesi berakhir.
* Anda [menghentikan item pekerjaan milik sesi tersebut](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#stop-a-session-gracefully).
* Sesi tetap idle selama batas idle worker. Sesi itu sendiri tetap terbuka. Ketika Anda kemudian mengirimkan event baru ke sesi tersebut, seperti pesan pengguna, worker yang sama atau worker lain akan mengklaimnya. Worker tersebut mengunduh store lagi.

Batas idle default-nya adalah 60 detik. Untuk mengubahnya, gunakan [`--max-idle`](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#cli-commands-and-flags) untuk worker CLI `ant` atau [`max_idle` (typescript: `maxIdleMs`; go: `MaxIdle`)](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#environment-worker) untuk `EnvironmentWorker`. [Helm chart `cma-sandboxes`](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#run-sandboxes-on-kubernetes) memulai worker-nya dengan batas 30 menit sebagai gantinya. Untuk mengubah batas tersebut, ubah pengaturan `sandbox.idleTimeout` milik chart.

### Hasil akhir

Sandbox self-hosted tidak memiliki direktori `/mnt/session/outputs`. Pada sandbox cloud Anthropic, prompt sistem sesi memberi tahu agen untuk menyalin hasil akhir ke sana. Pada environment self-hosted, prompt sistem menghilangkan instruksi tersebut. Hasil akhir tetap berada di mana pun agen menuliskannya, biasanya di bawah direktori kerja, dan worker tidak mengunggahnya.

Untuk mengumpulkan hasil akhir di satu tempat, berikan path lengkap sebuah direktori di prompt sistem agen Anda. Pilih direktori yang dapat ditulisi oleh alat file worker:

* **Di dalam direktori kerja:** Misalnya, `/workspace/outputs` jika direktori kerjanya adalah `/workspace`.
* **Di tempat lain, hanya dengan worker SDK:** Tambahkan direktori tersebut ke `allowed_roots` (typescript: `allowedRoots`; go: `AllowedRoots`). Lihat [AgentToolContext dan toolset agen](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#agent-tool-context-and-the-agent-toolset).

## Helper SDK

SDK Python, TypeScript, dan Go menyediakan tiga helper dengan tingkat kontrol yang berbeda:

| Helper | Fungsinya | Gunakan saat |
| ----- | ----- | ----- |
| [`EnvironmentWorker`](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#environment-worker) | Menangani polling, penyiapan, dan menjalankan alat secara menyeluruh. | Sebagian besar kasus. |
| [`work.poller()` (typescript: `new WorkPoller()`; go: `environments.NewWorkPoller()`)](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#work-poller) | Melakukan polling pada antrean kerja dan memberikan setiap sesi yang diklaim kepada Anda. | Anda menentukan cara menangani setiap sesi, misalnya dengan meluncurkan sandbox alih-alih menjalankan alat di dalam proses. |
| [`client.beta.sessions.events.tool_runner()` (typescript: `client.beta.sessions.events.toolRunner()`; go: `client.Beta.Sessions.Events.NewToolRunner()`)](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#session-tool-runner) | Menjalankan pemanggilan alat untuk satu sesi, berdasarkan ID sesi dan daftar alat. | Anda sudah mengklaim pekerjaan dan hanya perlu menjalankan alat. |

### EnvironmentWorker

| Metode | Deskripsi |
| ----- | ----- |
| `run()` (go: `Run()`) | Berjalan tanpa batas waktu, mengambil sesi saat sesi tersebut tiba. |
| `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`) | Menangani satu item pekerjaan yang sudah diklaim oleh poller. Poller tersebut dapat berupa `ant beta:worker poll --on-work` atau kode Anda sendiri. Metode ini kembali saat worker selesai menangani sesi milik item tersebut. Anda dapat meneruskan `work_id` (typescript: `workId`; go: `WorkID`), `session_id` (typescript: `sessionId`; go: `SessionID`), `environment_id` (typescript: `environmentId`; go: `EnvironmentID`), dan `work_secret` (typescript: `workSecret`; go: `WorkSecret`). Untuk setiap nilai yang tidak Anda teruskan, metode ini membaca [variabel `ANTHROPIC_*`](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#environment-variables) yang sesuai. |

| Opsi | Deskripsi |
| ----- | ----- |
| `tools` (go: `ToolsFunc`) | Factory yang menerima `AgentToolContext` milik sesi dan mengembalikan daftar alat. Default-nya adalah toolset agen standar. |
| `max_idle` (typescript: `maxIdleMs`; go: `MaxIdle`) | Berapa lama worker menunggu selama sesi dalam keadaan idle sebelum selesai menangani sesi tersebut. Waktu idle dengan [alasan berhenti `requires_action`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#respond-when-the-session-goes-idle) tidak dihitung. Default-nya 60 detik. Untuk menunggu 5 menit, atur ke `300` (typescript: `300_000`; go: `anthropic.Ptr(5 * time.Minute)`). Untuk menonaktifkan batas ini, atur ke `None` (typescript: `0`; go: `new(time.Duration)`). |
| `memory_sync_interval` (typescript: `memorySyncIntervalMs`; go: `MemorySyncInterval`) | Waktu terpendek antara dua sinkronisasi memory store yang terlampir selama sesi berjalan. Worker memeriksa interval ini setelah setiap pemanggilan alat yang berjalan di sandbox Anda, bukan berdasarkan timer. Default-nya 15 detik. Lihat [Interval sinkronisasi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#sync-interval). |
| `memory_sync_deletions` (typescript: `memorySyncDeletions`; go: `MemorySyncDeletions`) | Apakah file yang dihapus agen secara lokal juga dihapus dari store. Lihat [Penghapusan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#deletions). |

`EnvironmentWorker` mengelola `AgentToolContext` dan toolset secara otomatis. Teruskan factory `tools` (go: `ToolsFunc`) untuk menyesuaikan daftar alat:

<CodeGroup exclude="shell, csharp, java, php, ruby">
  <CodeGroupItem language="cURL">
    Worker adalah proses yang berjalan lama, bukan satu permintaan HTTP. Untuk menyesuaikan daftar alat, gunakan `EnvironmentWorker` di SDK Python, TypeScript, atau Go.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Worker CLI `ant` selalu menggunakan toolset agen standar. Untuk menyesuaikan daftar alat, gunakan `EnvironmentWorker` di SDK Python, TypeScript, atau Go.
  </CodeGroupItem>

  ```python Python
  import asyncio
  import contextlib
  import os
  import signal
  from anthropic import AsyncAnthropic, beta_async_tool
  from anthropic.lib.environments import EnvironmentWorker
  from anthropic.lib.tools.agent_toolset import beta_bash_tool


  @beta_async_tool
  async def get_order_status(order_id: str) -> str:
      """Look up an order in the internal fulfillment system by order ID."""
      return f"Order {order_id}: shipped"


  async def main() -> None:
      environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
      environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
      async with AsyncAnthropic(auth_token=environment_key) as client:
          worker = EnvironmentWorker(
              client,
              environment_id=environment_id,
              environment_key=environment_key,
              # Daftarkan setiap alat yang dapat dipanggil agen. Worker tidak menjawab alat lain.
              tools=lambda env: [beta_bash_tool(env), get_order_status],
          )
          task = asyncio.create_task(worker.run())
          loop = asyncio.get_running_loop()
          for signum in (signal.SIGINT, signal.SIGTERM):
              loop.add_signal_handler(signum, task.cancel)
          with contextlib.suppress(asyncio.CancelledError):
              await task


  asyncio.run(main())
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";
  import { betaTool } from "@anthropic-ai/sdk/helpers/beta/json-schema";
  import { betaBashTool } from "@anthropic-ai/sdk/tools/agent-toolset/node";

  const getOrderStatus = betaTool({
    name: "get_order_status",
    description: "Look up an order in the internal fulfillment system by order ID.",
    inputSchema: {
      type: "object",
      properties: { order_id: { type: "string", description: "The order ID" } },
      required: ["order_id"]
    },
    run: async ({ order_id }) => `Order ${order_id}: shipped`
  });

  const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
  const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
  const client = new Anthropic({ authToken: environmentKey });
  const controller = new AbortController();
  process.once("SIGINT", () => controller.abort());
  process.once("SIGTERM", () => controller.abort());

  await new EnvironmentWorker({
    client,
    environmentId,
    environmentKey,
    signal: controller.signal,
    // Daftarkan setiap alat yang dapat dipanggil agen. Worker tidak menjawab alat lain.
    tools: (ctx) => [betaBashTool(ctx), getOrderStatus]
  }).run();
  ```

  <CodeGroupItem language="C#">
    C# SDK tidak memiliki `EnvironmentWorker`. Untuk menjawab pemanggilan alat kustom dari kode Anda sendiri, kirim setiap hasil pada aliran event sesi, seperti pada [Mengembalikan hasil alat kustom](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#return-a-custom-tool-result).
  </CodeGroupItem>

  ```go Go
  package main

  import (
  	"context"
  	"log"
  	"os"
  	"os/signal"
  	"syscall"

  	"github.com/anthropics/anthropic-sdk-go/v2"
  	"github.com/anthropics/anthropic-sdk-go/v2/lib/environments"
  	"github.com/anthropics/anthropic-sdk-go/v2/option"
  	"github.com/anthropics/anthropic-sdk-go/v2/toolrunner"
  	"github.com/anthropics/anthropic-sdk-go/v2/tools/agenttoolset"
  )

  type orderStatusInput struct {
  	OrderID string `json:"order_id"`
  }

  func main() {
  	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
  	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

  	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
  	defer stop()

  	getOrderStatus := toolrunner.NewBetaTool(
  		"get_order_status",
  		"Look up an order in the internal fulfillment system by order ID.",
  		anthropic.BetaToolInputSchemaParam{
  			Properties: map[string]any{
  				"order_id": map[string]any{"type": "string", "description": "The order ID"},
  			},
  			Required: []string{"order_id"},
  		},
  		func(ctx context.Context, input orderStatusInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
  			return anthropic.BetaToolResultBlockParamContentUnion{
  				OfText: &anthropic.BetaTextBlockParam{Text: "Order " + input.OrderID + ": shipped"},
  			}, nil
  		},
  	)

  	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

  	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  		EnvironmentID:  environmentID,
  		EnvironmentKey: environmentKey,
  		// Daftarkan setiap alat yang dapat dipanggil agen. Worker tidak menjawab alat lain.
  		ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
  			return []anthropic.BetaTool{agenttoolset.BetaBashTool(env), getOrderStatus}
  		},
  	})
  	if err := worker.Run(ctx); err != nil {
  		log.Fatalf("worker: %v", err)
  	}
  }
  ```

  <CodeGroupItem language="Java">
    Java SDK tidak memiliki `EnvironmentWorker`. Untuk menjawab pemanggilan alat kustom dari kode Anda sendiri, kirim setiap hasil pada aliran event sesi, seperti pada [Mengembalikan hasil alat kustom](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#return-a-custom-tool-result).
  </CodeGroupItem>

  <CodeGroupItem language="PHP">
    PHP SDK tidak memiliki `EnvironmentWorker`. Untuk menjawab pemanggilan alat kustom dari kode Anda sendiri, kirim setiap hasil pada aliran event sesi, seperti pada [Mengembalikan hasil alat kustom](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#return-a-custom-tool-result).
  </CodeGroupItem>

  <CodeGroupItem language="Ruby">
    Ruby SDK tidak memiliki `EnvironmentWorker`. Untuk menjawab pemanggilan alat kustom dari kode Anda sendiri, kirim setiap hasil pada aliran event sesi, seperti pada [Mengembalikan hasil alat kustom](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#return-a-custom-tool-result).
  </CodeGroupItem>
</CodeGroup>

### Work poller

| Opsi | Deskripsi |
| ----- | ----- |
| `drain` (go: `Drain`) | Apakah polling dihentikan setelah antrean kosong alih-alih menunggu pekerjaan baru. |
| `block_ms` (typescript: `blockMs`; go: `BlockMs`) | Berapa lama setiap polling menunggu pekerjaan tiba sebelum kembali, dalam milidetik. Harus antara 1 dan 999. Helper melakukan polling ulang secara otomatis. Teruskan `null` (python: `None`; go: `param.Null[int64]()`) untuk pemeriksaan non-blocking. Default-nya long-polling 999ms. |
| `reclaim_older_than_ms` (typescript: `reclaimOlderThanMs`; go: `ReclaimOlderThanMs`) | Mengklaim ulang item pekerjaan yang telah diklaim tetapi tidak pernah di-acknowledge dalam jumlah milidetik ini. |
| `auto_stop` (typescript: `autoStop`; go: `AutoStop`) | Apakah poller mengirim sinyal berhenti untuk setiap item pekerjaan setelah badan loop Anda selesai memprosesnya. Default-nya `true` (python: `True`). Atur ke `false` (python: `False`; go: `param.NewOpt(false)`) dalam dua kasus yang dijelaskan setelah tabel ini. |

Atur `auto_stop` (typescript: `autoStop`; go: `AutoStop`) ke `false` (python: `False`; go: `param.NewOpt(false)`) dalam dua kasus:

1. Loop Anda memanggil `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`), yang mengirim sinyal berhenti sendiri.
2. Loop Anda meluncurkan sandbox untuk item tersebut lalu beralih ke item berikutnya. Worker di sandbox tersebut harus mengirim sinyal berhenti saat pekerjaan sesi berakhir, seperti yang dilakukan `ant beta:worker run` dan `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`).

Untuk contoh lengkap, lihat [Meluncurkan sandbox dari poller SDK](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#launch-sandboxes-from-the-sdk-poller).

### Tool runner sesi

`client.beta.sessions.events.tool_runner()` (typescript: `client.beta.sessions.events.toolRunner()`; go: `client.Beta.Sessions.Events.NewToolRunner()`) menerima daftar alat sebagai `tools` (go: `Tools`). Untuk membangun daftar tersebut, siapkan `AgentToolContext` sendiri dan panggil `beta_agent_toolset_20260401(env)` (typescript: `betaAgentToolset20260401(ctx)`; go: `agenttoolset.BetaAgentToolset20260401(env)`):

<CodeGroup exclude="shell, csharp, java, php, ruby">
  <CodeGroupItem language="cURL">
    `AgentToolContext` adalah helper di SDK Python, TypeScript, dan Go. cURL tidak memiliki padanannya. Gunakan salah satu SDK tersebut.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    `AgentToolContext` adalah helper di SDK Python, TypeScript, dan Go. CLI `ant` tidak memiliki padanannya. Gunakan salah satu SDK tersebut.
  </CodeGroupItem>

  ```python Python
  from anthropic.lib.tools.agent_toolset import (
      AgentToolContext,
      beta_agent_toolset_20260401,
  )

  async with AgentToolContext(
      workdir="/workspace", client=client, session_id=work.data.id
  ) as env:
      # skills diunduh ke /workspace/skills/<name>/
      tools = beta_agent_toolset_20260401(env)
  ```

  ```typescript TypeScript
  import {
    setupSkills,
    betaAgentToolset20260401
  } from "@anthropic-ai/sdk/tools/agent-toolset/node";

  const ctx = { workdir: "/workspace", client, sessionId: work.data.id };
  await setupSkills(ctx);
  const tools = betaAgentToolset20260401(ctx);
  ```

  <CodeGroupItem language="C#">
    C# SDK tidak memiliki `AgentToolContext`.
  </CodeGroupItem>

  ```go Go
  env := &agenttoolset.AgentToolContext{Workdir: "/workspace"}
  if err := env.SetupSkills(ctx, client, work.Data.ID); err != nil {
  	panic(err)
  }
  // skills diunduh ke /workspace/skills/<name>/
  tools := agenttoolset.BetaAgentToolset20260401(env)
  ```

  <CodeGroupItem language="Java">
    Java SDK tidak memiliki `AgentToolContext`.
  </CodeGroupItem>

  <CodeGroupItem language="PHP">
    PHP SDK tidak memiliki `AgentToolContext`.
  </CodeGroupItem>

  <CodeGroupItem language="Ruby">
    Ruby SDK tidak memiliki `AgentToolContext`.
  </CodeGroupItem>
</CodeGroup>

### AgentToolContext dan toolset agen

`AgentToolContext` adalah konteks eksekusi untuk pemanggilan alat. Konteks ini mendefinisikan direktori kerja dan kebijakan path, serta dapat mengunduh skill milik sesi.

| Opsi | Deskripsi |
| ----- | ----- |
| `allowed_roots` (typescript: `allowedRoots`; go: `AllowedRoots`) | Direktori, selain direktori kerja, yang dapat dijangkau oleh alat file (`read`, `write`, `edit`, `glob`, `grep`). |
| `read_only_roots` (typescript: `readOnlyRoots`; go: `ReadOnlyRoots`) | Direktori yang path di bawahnya ditolak oleh `write` dan `edit`. |

`EnvironmentWorker` sendiri menambahkan direktori memory store milik sesi ke `allowed_roots` (typescript: `allowedRoots`; go: `AllowedRoots`), dan direktori store yang dilampirkan dengan `access: "read_only"` ke `read_only_roots` (typescript: `readOnlyRoots`; go: `ReadOnlyRoots`).

Pembatasan ini hanyalah pengaman untuk alat file, bukan sandbox. Pembatasan ini tidak membatasi `bash`.

`beta_agent_toolset_20260401(env)` (typescript: `betaAgentToolset20260401(ctx)`; go: `agenttoolset.BetaAgentToolset20260401(env)`) menerima `AgentToolContext` dan mengembalikan implementasi alat standar (`bash`, `read`, `write`, `edit`, `glob`, `grep`).
