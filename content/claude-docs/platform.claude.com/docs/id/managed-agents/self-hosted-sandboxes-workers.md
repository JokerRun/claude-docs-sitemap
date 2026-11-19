---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers
fetched_at: 2026-11-19T02:13:30.221159Z
sha256: 5f557b54f2ace0e727f3e08d3817626174df50720dac83504fe70cf964c1202f
---

---
title: Menerapkan worker self-hosted
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers
description: Pilih cara worker sandbox self-hosted mengklaim pekerjaan dan tempat sesi berjalan, lalu jalankan worker always-on atau picu worker dari webhook.
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

[Panduan mulai cepat sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#quickstart) menjalankan satu worker CLI `ant` yang melakukan polling secara terus-menerus dan menjalankan setiap sesi dalam satu proses. Halaman ini membantu Anda memilih pola deployment, lalu membahas worker always-on dan worker yang dipicu webhook.

## Pilih pola deployment

Saat menerapkan worker, Anda perlu membuat dua pilihan: bagaimana worker mengklaim pekerjaan, dan di mana setiap sesi berjalan.

**Bagaimana worker mengklaim pekerjaan:**

* **Selalu aktif:** Proses yang berjalan lama melakukan polling antrean secara terus-menerus. Proses ini hanya membuat permintaan HTTPS keluar, sehingga Anda tidak mengekspos endpoint kepada Anthropic.
* **Dipicu webhook:** Sebuah handler aktif pada `session.status_run_started` dan mulai melakukan polling. Ini menghindari poller yang menganggur, tetapi memerlukan endpoint [webhook](https://platform.claude.com/docs/id/managed-agents/webhooks) yang dapat dijangkau oleh Anthropic.

**Di mana setiap sesi berjalan:**

* **Dalam proses:** Worker yang mengklaim sebuah sesi juga menjalankan pemanggilan alatnya, dalam satu direktori kerja bersama.
* **Sandbox per sesi:** Sebuah poller meluncurkan sandbox baru untuk setiap sesi yang diklaim. Pilih ini untuk isolasi yang lebih kuat: sistem file baru, batas sumber daya, atau kontrol jaringan per sesi. Lihat [Menjalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session), yang juga membahas Helm chart untuk Kubernetes.

Worker CLI dan SDK mendukung kombinasi yang berbeda:

| Kemampuan                                                                                                | CLI `ant`                                  | SDK (Python, TypeScript, Go)                     |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------ |
| Polling always-on                                                                                        | Ya                                         | Ya                                               |
| Dipicu webhook                                                                                           | Tidak                                      | Ya                                               |
| [Sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session) | Ya                                         | Ya                                               |
| [Memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory)          | Ya, dengan pengaturan sinkronisasi default | Ya, dengan sinkronisasi yang dapat dikonfigurasi |
| [Alat kustom](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools)     | Tidak                                      | Ya                                               |

Lihat [Referensi worker self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference) untuk setiap flag CLI dan opsi SDK.

Untuk kontrol lebih, panggil [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work) secara langsung dan implementasikan worker Anda sendiri. Worker Anda kemudian melakukan apa yang dilakukan worker SDK. Antara lain, worker tersebut melakukan acknowledge setiap item pekerjaan, mengirim heartbeat, dan mengunduh skill agen. Worker hanya menjalankan pemanggilan alat yang diizinkan oleh [kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies#see-how-each-call-was-evaluated) sesi. Worker mengembalikan setiap hasil sebagai event `user.tool_result` atau `user.custom_tool_result`. Pada akhirnya, worker menghentikan item tersebut. Gunakan kode sumber worker di [SDK Python](https://github.com/anthropics/anthropic-sdk-python/tree/main/src/anthropic/lib/environments), [SDK TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/tree/main/src/lib/environments), atau [SDK Go](https://github.com/anthropics/anthropic-sdk-go/tree/main/lib/environments) sebagai referensi.

## Menjalankan worker always-on

Sampel ini menggunakan `/workspace` sebagai direktori kerja worker. Direktori tersebut harus sudah ada sebelum worker dimulai. Di host baru, buat direktori tersebut dan berikan akses tulis kepada pengguna worker, seperti pada langkah “Mulai worker” di [Jalankan sesi pertama Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-your-first-session).

Di macOS, `mkdir` tidak dapat membuat `/workspace`, karena volume root bersifat read-only. Buat `~/workspace` sebagai gantinya, seperti yang ditunjukkan pada langkah tersebut. Sebagai pengganti `/workspace`, gunakan path lengkap yang dicetak oleh `echo ~/workspace`, karena SDK tidak mengekspansi `~`.

Mulai worker yang melakukan polling antrean secara terus-menerus. Worker ini melakukan autentikasi dengan [kunci lingkungan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-your-first-session) dari quickstart:

<CodeGroup exclude="shell:cURL, csharp, java, php, ruby">
  <CodeGroupItem language="cURL">
    Worker adalah proses yang berjalan lama, bukan satu permintaan HTTP. Jalankan worker CLI `ant` sebagai gantinya: `ant beta:worker poll --workdir /workspace`.
  </CodeGroupItem>

  ```bash CLI
  ant beta:worker poll --workdir /workspace
  ```

  ```python Python
  import asyncio
  import contextlib
  import os
  import signal
  from anthropic import AsyncAnthropic
  from anthropic.lib.environments import EnvironmentWorker


  async def main() -> None:
      environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
      environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
      async with AsyncAnthropic(auth_token=environment_key) as client:
          worker = EnvironmentWorker(
              client,
              environment_id=environment_id,
              environment_key=environment_key,
              workdir="/workspace",
          )
          task = asyncio.create_task(worker.run())
          # Membatalkan task, alih-alih mematikan proses, memungkinkan worker menghentikan
          # item pekerjaan yang sedang berjalan dan mengunggah file memori yang berubah sebelum keluar.
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

  const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
  const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
  const client = new Anthropic({ authToken: environmentKey });
  const controller = new AbortController();
  // Membatalkan pada salah satu sinyal memungkinkan worker mengunggah file memori yang berubah dan menghapus
  // direktori store-nya sebelum proses keluar.
  process.once("SIGINT", () => controller.abort());
  process.once("SIGTERM", () => controller.abort());

  await new EnvironmentWorker({
    client,
    environmentId,
    environmentKey,
    workdir: "/workspace",
    signal: controller.signal
  }).run();
  ```

  <CodeGroupItem language="C#">
    SDK C# tidak memiliki `EnvironmentWorker`. Jalankan worker CLI `ant` sebagai gantinya: `ant beta:worker poll --workdir /workspace`.
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
  )

  func main() {
  	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
  	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

  	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
  	defer stop()

  	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

  	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  		EnvironmentID:  environmentID,
  		EnvironmentKey: environmentKey,
  		Workdir:        "/workspace",
  	})
  	if err := worker.Run(ctx); err != nil {
  		log.Fatalf("worker: %v", err)
  	}
  }
  ```

  <CodeGroupItem language="Java">
    SDK Java tidak memiliki `EnvironmentWorker`. Jalankan worker CLI `ant` sebagai gantinya: `ant beta:worker poll --workdir /workspace`.
  </CodeGroupItem>

  <CodeGroupItem language="PHP">
    SDK PHP tidak memiliki `EnvironmentWorker`. Jalankan worker CLI `ant` sebagai gantinya: `ant beta:worker poll --workdir /workspace`.
  </CodeGroupItem>

  <CodeGroupItem language="Ruby">
    SDK Ruby tidak memiliki `EnvironmentWorker`. Jalankan worker CLI `ant` sebagai gantinya: `ant beta:worker poll --workdir /workspace`.
  </CodeGroupItem>
</CodeGroup>

## Memicu worker dari webhook

<Steps>
  <Step title="Berlangganan webhook sesi">
    Di [Claude Console](https://platform.claude.com/settings/workspaces/default/webhooks), tentukan endpoint webhook yang mendengarkan event `session.status_run_started`. Lihat [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks) untuk detailnya.
  </Step>

  <Step title="Ekspor kunci penandatanganan webhook">
    Bersama dengan ID environment dan kunci dari [Menjalankan sesi pertama Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-your-first-session), ekspor kunci penandatanganan webhook di host handler Anda. Handler menggunakannya untuk memverifikasi payload yang masuk.

    ```bash
    export ANTHROPIC_WEBHOOK_SIGNING_KEY="whsec_..."
    ```
  </Step>

  <Step title="Implementasikan handler webhook">
    Mulai worker saat `session.status_run_started` dipicu. Handler menguras antrean dan menyerahkan setiap item pekerjaan yang diklaim ke `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`) (di SDK Python, TypeScript, dan Go). Metode tersebut mengunduh skill, menjalankan pemanggilan alat, mengirimkan hasil kembali, lalu kembali.

    Sampel menggunakan `/workspace` sebagai direktori kerja. Sebelum Anda memulai handler, buat direktori tersebut di host handler. Pastikan pengguna handler dapat menulis ke direktori tersebut, seperti pada langkah “Mulai worker” di [Jalankan sesi pertama Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-your-first-session).

    <CodeGroup exclude="shell, csharp, java, php, ruby">
      <CodeGroupItem language="cURL">
        Handler ini memerlukan logika lebih dari satu perintah shell. Gunakan SDK Python, TypeScript, atau Go untuk menjalankannya.
      </CodeGroupItem>

      <CodeGroupItem language="CLI">
        Handler ini memerlukan logika lebih dari satu perintah shell. Gunakan SDK Python, TypeScript, atau Go untuk menjalankannya.
      </CodeGroupItem>

      <CodeGroupItem>
        Untuk memverifikasi tanda tangan webhook, instal extra webhooks: `pip install "anthropic[webhooks]"`.

        ```python Python
        import asyncio
        import os
        import anthropic
        import standardwebhooks  # installed by the anthropic[webhooks] extra

        environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
        environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
        client = anthropic.AsyncAnthropic(
            auth_token=environment_key,
        )
        # Dibatalkan oleh shutdown() agar item pekerjaan yang sedang berjalan dapat mengunggah file memori yang berubah dan
        # menghapus direktori store-nya sebelum proses keluar.
        inflight: set[asyncio.Task[None]] = set()


        # Await ini dari shutdown hook host, seperti shutdown lifespan ASGI (kode setelah
        # `yield` dalam lifespan FastAPI), yang dijalankan uvicorn saat SIGTERM. uvicorn membiarkan request terbuka
        # selesai sebelum hook itu berjalan, jadi atur --timeout-graceful-shutdown untuk membatasi waktu tunggu.
        async def shutdown() -> None:
            for task in inflight:
                task.cancel()
            await asyncio.gather(*inflight, return_exceptions=True)


        async def handle(raw: bytes, headers: dict[str, str]) -> tuple[dict[str, str], int]:
            try:
                event = client.beta.webhooks.unwrap(raw.decode(), headers=headers)
            except standardwebhooks.WebhookVerificationError:
                return {"error": "signature verification failed"}, 401
            if event.data.type != "session.status_run_started":
                return {"status": "ignored"}, 200
            task = asyncio.create_task(run_queued_work())
            inflight.add(task)
            task.add_done_callback(inflight.discard)
            try:
                # Di-shield: pengiriman yang terputus atau timeout tidak boleh membatalkan item; shutdown() yang melakukannya.
                await asyncio.shield(task)
            except asyncio.CancelledError:
                return {"status": "shutting down"}, 503
            return {"status": "ok"}, 200


        async def run_queued_work() -> None:
            async for work in client.beta.environments.work.poller(
                environment_id=environment_id,
                environment_key=environment_key,
                block_ms=None,
                reclaim_older_than_ms=2000,
                drain=True,
                auto_stop=False,
            ):
                await client.beta.environments.work.worker(workdir="/workspace").handle_item(
                    work_id=work.id,
                    environment_id=environment_id,
                    session_id=work.data.id,
                    environment_key=environment_key,
                    # Secret per sesi inilah yang memungkinkan worker me-mount memory store milik sesi tersebut.
                    work_secret=work.secret,
                )
        ```
      </CodeGroupItem>

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";

      const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
      const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
      const client = new Anthropic({
        authToken: environmentKey
      });
      // Panggil shutdown.abort() dari handler SIGTERM/SIGINT milik host, bersamaan dengan menutup server,
      // lalu tunggu panggilan handle() yang sedang berjalan sebelum keluar: abort memungkinkan item kerja yang berjalan
      // mengunggah file memori yang berubah dan menghapus direktori store-nya terlebih dahulu.
      export const shutdown = new AbortController();

      export async function handle(req: Request): Promise<Response> {
        // Jangan pernah mengakui pengiriman yang pekerjaannya tidak akan dijalankan di sini; 503 membuat pengirim mencoba lagi.
        if (shutdown.signal.aborted) {
          return Response.json({ status: "shutting down" }, { status: 503 });
        }
        const body = await req.text();
        let event;
        try {
          event = client.beta.webhooks.unwrap(body, { headers: Object.fromEntries(req.headers) });
        } catch {
          return new Response("signature verification failed", { status: 401 });
        }
        if (event.data.type !== "session.status_run_started") {
          return Response.json({ status: "ignored" });
        }

        for await (const work of client.beta.environments.work.poller({
          environmentId,
          environmentKey,
          blockMs: null,
          reclaimOlderThanMs: 2000,
          drain: true,
          autoStop: false,
          signal: shutdown.signal
        })) {
          await client.beta.environments.work.worker({ workdir: "/workspace" }).handleItem({
            workId: work.id,
            environmentId,
            sessionId: work.data.id,
            environmentKey,
            // Secret per sesi inilah yang memungkinkan worker me-mount memory store milik sesi tersebut.
            workSecret: work.secret ?? undefined,
            signal: shutdown.signal
          });
        }
        // Poller dan handleItem kembali secara diam-diam saat abort, sehingga drain yang terpotong berakhir di sini.
        if (shutdown.signal.aborted) {
          return Response.json({ status: "shutting down" }, { status: 503 });
        }
        return Response.json({ status: "ok" });
      }
      ```

      <CodeGroupItem language="C#">
        SDK C# tidak memiliki `EnvironmentWorker`. Untuk menangani item pekerjaan dari kode Anda sendiri, implementasikan worker Anda sendiri, seperti yang dijelaskan di [Pilih pola deployment](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#choose-a-deployment-pattern).
      </CodeGroupItem>

      ```go Go
      package main

      import (
      	"context"
      	"encoding/json"
      	"errors"
      	"io"
      	"log/slog"
      	"net/http"
      	"os"
      	"os/signal"
      	"syscall"

      	"github.com/anthropics/anthropic-sdk-go/v2"
      	"github.com/anthropics/anthropic-sdk-go/v2/lib/environments"
      	"github.com/anthropics/anthropic-sdk-go/v2/option"
      	"github.com/anthropics/anthropic-sdk-go/v2/packages/param"
      )

      var (
      	environmentKey = os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
      	environmentID  = os.Getenv("ANTHROPIC_ENVIRONMENT_ID")
      	client         = anthropic.NewClient(
      		option.WithAuthToken(environmentKey),
      		option.WithWebhookKey(os.Getenv("ANTHROPIC_WEBHOOK_SIGNING_KEY")),
      	)
      	worker = environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
      		Workdir: "/workspace",
      	})
      	// Dibatalkan saat SIGINT atau SIGTERM (diatur di main) agar item pekerjaan yang sedang berjalan dapat
      	// mengunggah file memori yang berubah dan menghapus direktori store-nya sebelum keluar.
      	shutdown context.Context
      )

      func handle(w http.ResponseWriter, r *http.Request) {
      	body, err := io.ReadAll(r.Body)
      	if err != nil {
      		http.Error(w, "bad request", http.StatusBadRequest)
      		return
      	}
      	event, err := client.Beta.Webhooks.Unwrap(body, r.Header)
      	if err != nil {
      		http.Error(w, "signature verification failed", http.StatusUnauthorized)
      		return
      	}
      	if event.Data.Type != "session.status_run_started" {
      		json.NewEncoder(w).Encode(map[string]string{"status": "ignored"})
      		return
      	}

      	// Go SDK tidak menyediakan kemudahan RunOne: kuras item yang tertunda
      	// dengan WorkPoller dan jalankan masing-masing dengan HandleItem.
      	// Lepaskan dari r.Context(): sesi bisa bertahan lebih lama dari batas waktu pengiriman webhook.
      	// Konteks shutdown tingkat proses tetap mengakhiri item dengan bersih saat SIGTERM.
      	ctx := shutdown
      	poller := environments.NewWorkPoller(ctx, client, environments.WorkPollerOptions{
      		EnvironmentID:      environmentID,
      		EnvironmentKey:     environmentKey,
      		BlockMs:            param.Null[int64](),
      		ReclaimOlderThanMs: param.NewOpt[int64](2000),
      		Drain:              true,
      		AutoStop:           param.NewOpt(false),
      	})
      	defer poller.Close()
      	for poller.Next() {
      		item := poller.Current()
      		if err := worker.HandleItem(ctx, environments.HandleItemOptions{
      			WorkID:         item.ID,
      			EnvironmentID:  item.EnvironmentID,
      			SessionID:      item.Data.ID,
      			EnvironmentKey: environmentKey,
      			// Secret per sesi inilah yang memungkinkan worker me-mount memory store milik sesi.
      			WorkSecret: item.Secret,
      		}); err != nil {
      			slog.Error("handle work item", "work_id", item.ID, "err", err)
      			http.Error(w, "internal error", http.StatusInternalServerError)
      			return
      		}
      	}
      	if err := poller.Err(); err != nil {
      		slog.Error("poll work queue", "err", err)
      		http.Error(w, "internal error", http.StatusInternalServerError)
      		return
      	}
      	json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
      }

      func main() {
      	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
      	defer stop()
      	shutdown = ctx

      	server := &http.Server{Addr: ":8080"}
      	http.HandleFunc("POST /webhook", handle)
      	go func() {
      		if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
      			slog.Error("http server", "err", err)
      			os.Exit(1)
      		}
      	}()
      	// Saat menerima sinyal, berhenti menerima pengiriman dan kembali hanya setelah handler
      	// yang sedang berjalan, beserta teardown memori item pekerjaannya, selesai.
      	<-ctx.Done()
      	if err := server.Shutdown(context.Background()); err != nil {
      		slog.Error("http shutdown", "err", err)
      	}
      }
      ```

      <CodeGroupItem language="Java">
        SDK Java tidak memiliki `EnvironmentWorker`. Untuk menangani item pekerjaan dari kode Anda sendiri, implementasikan worker Anda sendiri, seperti yang dijelaskan di [Pilih pola deployment](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#choose-a-deployment-pattern).
      </CodeGroupItem>

      <CodeGroupItem language="PHP">
        SDK PHP tidak memiliki `EnvironmentWorker`. Untuk menangani item pekerjaan dari kode Anda sendiri, implementasikan worker Anda sendiri, seperti yang dijelaskan di [Pilih pola deployment](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#choose-a-deployment-pattern).
      </CodeGroupItem>

      <CodeGroupItem language="Ruby">
        SDK Ruby tidak memiliki `EnvironmentWorker`. Untuk menangani item pekerjaan dari kode Anda sendiri, implementasikan worker Anda sendiri, seperti yang dijelaskan di [Pilih pola deployment](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#choose-a-deployment-pattern).
      </CodeGroupItem>
    </CodeGroup>

    Di SDK Python, TypeScript, dan Go, `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`) memerlukan secret item pekerjaan untuk me-mount memory store. Worker yang melakukan polling dengan `run()` (go: `Run()`) sudah memiliki secret tersebut. Handler ini mengklaim setiap item sendiri, sehingga handler meneruskan secret dalam argumen `work_secret` (typescript: `workSecret`; go: `WorkSecret`). Lihat [Meneruskan secret item pekerjaan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#forward-the-work-items-secret).
  </Step>
</Steps>

Handler ini menjalankan setiap item yang diklaim dalam satu proses, dan menjalankan item dari pengiriman webhook yang terpisah secara bersamaan. Sesi-sesi tersebut berbagi satu sistem file, termasuk `/workspace` dan `/mnt/memory`. Jika sesi Anda melampirkan memory store yang sama, lihat [Mengisolasi sesi yang berbagi store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#isolate-sessions-that-share-a-store).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Menjalankan satu sandbox per sesi" icon="cube" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session">
    Luncurkan sandbox dengan Helm chart di Kubernetes, skrip spawn, atau poller SDK.
  </Card>

  <Card title="Memantau dan memecahkan masalah worker self-hosted" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations">
    Baca kedalaman antrean, hentikan sesi dan worker dengan bersih, dan perbaiki kegagalan umum.
  </Card>

  <Card title="Model keamanan" icon="lock" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security">
    Model tanggung jawab bersama untuk environment sandbox self-hosted.
  </Card>
</CardGroup>

## Ketersediaan

Worker self-hosted siap pakai dalam versi beta di semua model.

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

| Item   | Retensi data nol                                                                                                                                                                                                                                                                                     | HIPAA                                                                        |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Status | Tidak layak                                                                                                                                                                                                                                                                                          | Tidak layak                                                                  |
| Detail | Tidak memiliki kelayakan ZDR, kecuali untuk Managed Agents yang di-host sendiri. Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access#how-long-data-is-kept) | Tidak memiliki kelayakan HIPAA. Berlaku untuk semua subfitur Managed Agents. |

Endpoint yang berlaku:

* `/v1/agents`
* `/v1/sessions`
* `/v1/environments`
