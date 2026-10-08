---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 74611375acf1698f07e0d4737f158073aaf2bac315e174c0e0171a4fb35b78cb
---

---
title: Menerapkan worker self-hosted
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers
description: "Pilih cara worker sandbox self-hosted mengklaim pekerjaan dan tempat sesi berjalan: always-on atau dipicu webhook, dalam satu proses atau satu sandbox per sesi."
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

[Quickstart](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#quickstart) menjalankan satu worker CLI `ant` yang melakukan polling secara terus-menerus dan menjalankan setiap sesi dalam satu proses. Halaman ini membahas cara lain untuk menjalankan worker dan cara memilih di antaranya.

## Pilih pola deployment

Saat menerapkan worker, Anda perlu membuat dua pilihan: bagaimana worker mengklaim pekerjaan, dan di mana setiap sesi berjalan.

**Bagaimana worker mengklaim pekerjaan:**

* **Always-on:** Proses yang berjalan lama melakukan polling antrean secara terus-menerus dan hanya memerlukan HTTPS keluar. Ini adalah penyiapan paling sederhana.
* **Dipicu webhook:** Sebuah handler aktif pada `session.status_run_started` dan mulai melakukan polling. Ini menghindari poller yang menganggur, tetapi memerlukan endpoint [webhook](https://platform.claude.com/docs/id/managed-agents/webhooks) yang dapat dijangkau oleh Anthropic.

**Di mana setiap sesi berjalan:**

* **Dalam proses:** Worker yang mengklaim sebuah sesi juga menjalankan pemanggilan alatnya, dalam satu direktori kerja bersama.
* **Sandbox per sesi:** Sebuah poller meluncurkan sandbox baru untuk setiap sesi yang diklaim. Pilih ini untuk isolasi yang lebih kuat: sistem file baru, batas sumber daya, atau kontrol jaringan per sesi.

Worker CLI dan SDK mendukung kombinasi yang berbeda:

| Kemampuan                                                                                            | CLI `ant`                                  | SDK (Python, TypeScript, Go)                     |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------ |
| Polling always-on                                                                                    | Ya                                         | Ya                                               |
| Dipicu webhook                                                                                       | Tidak                                      | Ya                                               |
| Sandbox per sesi                                                                                     | Ya                                         | Ya                                               |
| [Memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory)      | Ya, dengan pengaturan sinkronisasi default | Ya, dengan sinkronisasi yang dapat dikonfigurasi |
| [Alat kustom](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools) | Tidak                                      | Ya                                               |

Lihat [Referensi worker self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference) untuk setiap flag CLI dan opsi SDK. Untuk kontrol lebih, panggil [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work) secara langsung dan implementasikan worker Anda sendiri.

## Menjalankan worker always-on

Kedua worker melakukan autentikasi dengan [environment key](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-your-first-session) dari quickstart.

Dengan CLI `ant`:

```bash
ant beta:worker poll --workdir /workspace
```

Dengan SDK, `EnvironmentWorker` melakukan pekerjaan yang sama:

<CodeGroup exclude="shell">
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

  ```csharp C#
  // EnvironmentWorker saat ini belum tersedia di SDK C#. Gunakan worker CLI ant sebagai gantinya.
  ```

  ```go Go
  package main

  import (
  	"context"
  	"log"
  	"os"
  	"os/signal"
  	"syscall"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/lib/environments"
  	"github.com/anthropics/anthropic-sdk-go/option"
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

  ```java Java
  // EnvironmentWorker saat ini belum tersedia di Java SDK. Gunakan worker CLI ant sebagai gantinya.
  ```

  ```php PHP
  // EnvironmentWorker saat ini belum tersedia di PHP SDK. Gunakan worker CLI ant sebagai gantinya.
  ```

  ```ruby Ruby
  # EnvironmentWorker saat ini belum tersedia di Ruby SDK. Gunakan worker CLI ant sebagai gantinya.
  ```
</CodeGroup>

## Memicu worker dari webhook

<Steps>
  <Step title="Berlangganan webhook sesi">
    Di [Console](https://platform.claude.com/settings/workspaces/default/webhooks), tentukan endpoint webhook yang mendengarkan event `session.status_run_started`. Lihat [Webhook](https://platform.claude.com/docs/id/managed-agents/webhooks) untuk detailnya.
  </Step>

  <Step title="Ekspor kunci penandatanganan webhook">
    Bersama dengan ID environment dan kunci dari [quickstart](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-your-first-session), ekspor kunci penandatanganan webhook di host handler Anda. Handler menggunakannya untuk memverifikasi payload yang masuk.

    ```bash
    export ANTHROPIC_WEBHOOK_SIGNING_KEY="whsec_..."
    ```
  </Step>

  <Step title="Implementasikan handler webhook">
    Panggil worker saat `session.status_run_started` terpicu. Handler menguras antrean dan menyerahkan setiap work item yang diklaim ke `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`), yang mengunduh skill, mengeksekusi pemanggilan alat, mengirimkan hasil kembali, lalu kembali.

    <CodeGroup exclude="shell">
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
        # Dibatalkan oleh shutdown() agar work item yang sedang berjalan dapat mengunggah file memori yang berubah dan
        # menghapus direktori store-nya sebelum proses berakhir.
        inflight: set[asyncio.Task[None]] = set()


        # Await ini dari hook shutdown milik host, misalnya shutdown lifespan ASGI (kode setelah
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
                # Dilindungi (shielded): pengiriman yang terputus atau timeout tidak boleh membatalkan item; shutdown() yang melakukannya.
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

      ```csharp C#
      // EnvironmentWorker saat ini belum tersedia di SDK C#.
      // Untuk menangani item pekerjaan secara langsung, lihat endpoint Environments Work.
      ```

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

      	"github.com/anthropics/anthropic-sdk-go"
      	"github.com/anthropics/anthropic-sdk-go/lib/environments"
      	"github.com/anthropics/anthropic-sdk-go/option"
      	"github.com/anthropics/anthropic-sdk-go/packages/param"
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
      	// Dibatalkan pada SIGINT atau SIGTERM (diatur di main) agar work item yang sedang berjalan dapat
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
      	// Lepaskan dari r.Context(): sesi dapat bertahan lebih lama dari batas waktu pengiriman webhook.
      	// Konteks shutdown tingkat proses tetap mengakhiri item dengan bersih pada SIGTERM.
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
      			// Secret per sesi inilah yang memungkinkan worker memasang memory store milik sesi.
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
      	// Saat ada sinyal, berhenti menerima pengiriman dan kembali hanya setelah handler yang sedang berjalan,
      	// dan karenanya teardown memori work item mereka, telah selesai.
      	<-ctx.Done()
      	if err := server.Shutdown(context.Background()); err != nil {
      		slog.Error("http shutdown", "err", err)
      	}
      }

      ```

      ```java Java
      // EnvironmentWorker saat ini belum tersedia di Java SDK.
      // Untuk menangani item kerja secara langsung, lihat endpoint Environments Work.
      ```

      ```php PHP
      // EnvironmentWorker saat ini belum tersedia di PHP SDK.
      // Untuk menangani item kerja secara langsung, lihat endpoint Environments Work.
      ```

      ```ruby Ruby
      # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
      # Untuk menangani item pekerjaan secara langsung, lihat endpoint Environments Work.
      ```
    </CodeGroup>

    Karena handler mengklaim pekerjaan sendiri, handler harus [meneruskan secret work item](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#forward-the-work-items-secret), seperti yang dilakukan argumen `work_secret` (typescript: `workSecret`; go: `WorkSecret`) di sini.
  </Step>
</Steps>

Handler ini menjalankan setiap item yang diklaim dalam satu proses di satu host. Jika sesi Anda melampirkan memory store yang sama, lihat [Mengisolasi sesi yang berbagi store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#isolate-sessions-that-share-a-store).

## Menjalankan satu sandbox per sesi

Sebuah poller di host mengklaim pekerjaan dan memanggil skrip Anda sekali per work item. Skrip tersebut meluncurkan sandbox untuk satu sesi itu.

<Steps>
  <Step title="Bangun image sandbox">
    Instal `ant` dan tetapkan `ant beta:worker run` sebagai entrypoint. Saat sandbox dimulai, sandbox membaca detail sesi dari variabel lingkungan, menangani sesi tersebut, lalu keluar. Image dasar harus menyediakan `/bin/bash`; `curl` hanya digunakan saat build.

    ```dockerfile
    FROM your-base-image
    ARG ANT_VERSION=1.39.0
    ARG TARGETARCH
    RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo arm64 || echo amd64) && \
        curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${ANT_VERSION}/ant_${ANT_VERSION}_linux_${ARCH}.tar.gz" \
          | tar -xz -C /usr/local/bin ant
    WORKDIR /workspace
    VOLUME /workspace
    ENTRYPOINT ["ant", "beta:worker", "run"]
    ```
  </Step>

  <Step title="Tulis skrip spawn">
    Skrip meneruskan detail sesi ke sandbox baru. Skrip ini memerlukan `jq` di host poller.

    ```bash
    #!/bin/bash
    # spawn.sh: dipanggil sekali per item kerja yang diklaim
    # Item kerja yang diklaim diterima sebagai JSON melalui stdin.
    ANTHROPIC_WORK_SECRET="$(jq -r '.secret // empty')"
    export ANTHROPIC_WORK_SECRET
    mkdir -p "/host/outputs/$ANTHROPIC_SESSION_ID"
    exec docker run --rm \
      -e ANTHROPIC_SESSION_ID -e ANTHROPIC_ENVIRONMENT_KEY \
      -e ANTHROPIC_WORK_ID -e ANTHROPIC_ENVIRONMENT_ID -e ANTHROPIC_BASE_URL \
      -e ANTHROPIC_WORK_SECRET \
      -v "/host/outputs/$ANTHROPIC_SESSION_ID":/workspace \
      your-image
    ```

    Poller menetapkan variabel `ANTHROPIC_*` yang diteruskan oleh skrip, kecuali secret. Lihat [Variabel lingkungan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#environment-variables).

    `/host/outputs` adalah direktori host yang Anda pilih. Memasangnya di `/workspace` memungkinkan Anda mengambil hasil kerja sesi setelah sandbox keluar. Mount tersebut juga menangkap pohon `skills/` yang diunduh dan file perantara apa pun.
  </Step>

  <Step title="Mulai poller">
    ```bash
    ant beta:worker poll --on-work ./spawn.sh
    ```
  </Step>
</Steps>

### Meneruskan secret work item

Setiap work item yang diklaim dapat membawa `secret` per sesi, yang diterbitkan oleh Anthropic. Worker yang menjalankan sesi memerlukannya untuk me-mount [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory).

Worker yang mengklaim dan menjalankan sesi dalam satu proses (`ant beta:worker poll` tanpa `--on-work`, atau `EnvironmentWorker` dengan `run()` (go: `Run()`)) meneruskan secret itu sendiri. Ketika kode Anda sendiri berada di antara klaim dan worker, Anda yang meneruskannya:

| Anda mengklaim pekerjaan dengan                                | Secret tiba sebagai                                               | Teruskan ke worker sebagai                                                                                                                                                                 |
| -------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ant beta:worker poll --on-work`                               | Field `secret` dari JSON work item pada standard input skrip Anda | `ANTHROPIC_WORK_SECRET` di lingkungan sandbox                                                                                                                                              |
| `work.poller()` (go: `environments.NewWorkPoller()`) milik SDK | Field `secret` dari setiap work item yang diklaim                 | `ANTHROPIC_WORK_SECRET` di lingkungan sandbox, atau argumen `work_secret` (typescript: `workSecret`; go: `WorkSecret`) ke `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`) |

Teruskan secret hanya ke sandbox yang melayani sesi tersebut, dan jangan pernah mencatatnya di log. Lihat [Model keamanan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security) untuk mengetahui hubungannya dengan environment key.

### Meluncurkan sandbox dari poller SDK

Untuk mengklaim pekerjaan dari kode Anda sendiri alih-alih `ant beta:worker poll --on-work`, gunakan `work.poller()` (go: `environments.NewWorkPoller()`). Fungsi ini melakukan polling antrean dan memberi Anda setiap sesi yang diklaim, lalu Anda meluncurkan sandbox:

<CodeGroup>
  ```bash cURL
  # Work poller adalah helper SDK (Python, TypeScript, Go), bukan endpoint
  # mentah. Dari shell, gunakan `ant beta:worker poll --on-work` sebagai gantinya.
  ```

  ```bash CLI
  # Work poller adalah helper SDK (Python, TypeScript, Go), bukan endpoint
  # mentah. Dari shell, gunakan `ant beta:worker poll --on-work` sebagai gantinya.
  ```

  ```python Python
  import asyncio
  import os

  from anthropic import AsyncAnthropic
  from anthropic.types.beta.environments import BetaSelfHostedWork

  SANDBOX_ENV = (
      "ANTHROPIC_ENVIRONMENT_ID",
      "ANTHROPIC_ENVIRONMENT_KEY",
      "ANTHROPIC_WORK_ID",
      "ANTHROPIC_SESSION_ID",
      "ANTHROPIC_WORK_SECRET",
      "ANTHROPIC_BASE_URL",  # forwarded only when set on this host
  )


  async def launch_container(work: BetaSelfHostedWork) -> None:
      print(f"claimed session {work.data.id}")
      # Ganti `docker run` dengan peluncur sandbox Anda sendiri. Teruskan kunci
      # environment (jangan pernah kunci API Anda) dan secret per sesi milik item kerja: worker
      # di dalamnya memerlukan secret tersebut untuk me-mount memory store sesi.
      env = os.environ | {
          "ANTHROPIC_WORK_ID": work.id,
          "ANTHROPIC_SESSION_ID": work.data.id,
          "ANTHROPIC_WORK_SECRET": work.secret or "",
      }
      forward = [arg for name in SANDBOX_ENV for arg in ("-e", name)]
      launcher = await asyncio.create_subprocess_exec(
          "docker", "run", "--rm", "--detach", *forward, "your-image", env=env
      )
      await launcher.wait()


  async def main() -> None:
      environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
      environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
      async with AsyncAnthropic(auth_token=environment_key) as client:
          async for work in client.beta.environments.work.poller(
              environment_id=environment_id,
              environment_key=environment_key,
              auto_stop=False,  # the launched sandbox owns the stop call
          ):
              await launch_container(work)


  asyncio.run(main())
  ```

  ```typescript TypeScript
  import { spawn } from "node:child_process";
  import { once } from "node:events";
  import Anthropic from "@anthropic-ai/sdk";
  import { WorkPoller } from "@anthropic-ai/sdk/helpers/beta/environments";
  import type { BetaSelfHostedWork } from "@anthropic-ai/sdk/resources/beta/environments";

  const SANDBOX_ENV = [
    "ANTHROPIC_ENVIRONMENT_ID",
    "ANTHROPIC_ENVIRONMENT_KEY",
    "ANTHROPIC_WORK_ID",
    "ANTHROPIC_SESSION_ID",
    "ANTHROPIC_WORK_SECRET",
    "ANTHROPIC_BASE_URL" // forwarded only when set on this host
  ];

  const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
  const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
  const client = new Anthropic({ authToken: environmentKey });

  async function launchContainer(work: BetaSelfHostedWork): Promise<void> {
    console.log(`claimed session ${work.data.id}`);
    // Ganti `docker run` dengan peluncur sandbox Anda sendiri. Teruskan kunci environment
    // (jangan pernah kunci API Anda) dan secret per sesi milik work item: worker
    // di dalamnya memerlukan secret tersebut untuk me-mount memory store sesi.
    const env = {
      ...process.env,
      ANTHROPIC_WORK_ID: work.id,
      ANTHROPIC_SESSION_ID: work.data.id,
      ANTHROPIC_WORK_SECRET: work.secret ?? ""
    };
    const forward = SANDBOX_ENV.flatMap((name) => ["-e", name]);
    const launcher = spawn("docker", ["run", "--rm", "--detach", ...forward, "your-image"], {
      env,
      stdio: "inherit"
    });
    await once(launcher, "close");
  }

  const poller = new WorkPoller({
    client,
    environmentId,
    environmentKey,
    autoStop: false // the launched sandbox owns the stop call
  });

  for await (const work of poller) {
    await launchContainer(work);
  }
  ```

  ```csharp C#
  // Helper untuk polling pekerjaan saat ini belum tersedia di SDK C#.
  // Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"log"
  	"os"
  	"os/exec"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/lib/environments"
  	"github.com/anthropics/anthropic-sdk-go/option"
  	"github.com/anthropics/anthropic-sdk-go/packages/param"
  )

  var sandboxEnv = []string{
  	"ANTHROPIC_ENVIRONMENT_ID",
  	"ANTHROPIC_ENVIRONMENT_KEY",
  	"ANTHROPIC_WORK_ID",
  	"ANTHROPIC_SESSION_ID",
  	"ANTHROPIC_WORK_SECRET",
  	"ANTHROPIC_BASE_URL", // forwarded only when set on this host
  }

  func launchContainer(ctx context.Context, work *anthropic.BetaSelfHostedWork) error {
  	fmt.Printf("claimed session %s\n", work.Data.ID)
  	// Ganti `docker run` dengan peluncur sandbox Anda sendiri. Teruskan kunci environment
  	// (jangan pernah kunci API Anda) dan secret per sesi milik work item: worker
  	// di dalamnya memerlukan secret tersebut untuk me-mount memory store sesi.
  	args := []string{"run", "--rm", "--detach"}
  	for _, name := range sandboxEnv {
  		args = append(args, "-e", name)
  	}
  	launcher := exec.CommandContext(ctx, "docker", append(args, "your-image")...)
  	launcher.Env = append(os.Environ(),
  		"ANTHROPIC_WORK_ID="+work.ID,
  		"ANTHROPIC_SESSION_ID="+work.Data.ID,
  		"ANTHROPIC_WORK_SECRET="+work.Secret,
  	)
  	launcher.Stdout, launcher.Stderr = os.Stdout, os.Stderr
  	return launcher.Run()
  }

  func main() {
  	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")
  	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")

  	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

  	ctx := context.Background()

  	poller := environments.NewWorkPoller(ctx, client, environments.WorkPollerOptions{
  		EnvironmentID:  environmentID,
  		EnvironmentKey: environmentKey,
  		AutoStop:       param.NewOpt(false), // the launched sandbox owns the stop call
  	})
  	defer poller.Close()

  	for work, err := range poller.All() {
  		if err != nil {
  			log.Fatal(err)
  		}
  		if err := launchContainer(ctx, work); err != nil {
  			log.Fatal(err)
  		}
  	}
  }
  ```

  ```java Java
  // Helper untuk polling pekerjaan saat ini belum tersedia di Java SDK.
  // Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```

  ```php PHP
  // Helper polling pekerjaan saat ini belum tersedia di PHP SDK.
  // Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```

  ```ruby Ruby
  # Helper polling pekerjaan saat ini belum tersedia di Ruby SDK.
  # Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```
</CodeGroup>

### Menjalankan worker SDK di dalam sandbox

Ganti entrypoint `ant beta:worker run` dengan entrypoint SDK ketika sandbox harus [melayani alat kustom](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools) atau menggunakan [pengaturan sinkronisasi memori non-default](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#configure-sync). Entrypoint membuat `EnvironmentWorker` dan memanggil `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`), yang membaca variabel `ANTHROPIC_*` yang sama yang diteruskan oleh skrip spawn.

<CodeGroup exclude="shell">
  ```python Python
  import asyncio
  import contextlib
  import os
  import signal
  from anthropic import AsyncAnthropic
  from anthropic.lib.environments import EnvironmentWorker


  async def main() -> None:
      async with AsyncAnthropic(auth_token=os.environ["ANTHROPIC_ENVIRONMENT_KEY"]) as client:
          worker = EnvironmentWorker(client, workdir="/workspace")
          # Tanpa argumen, handle_item() membaca variabel ANTHROPIC_* yang diteruskan oleh
          # skrip spawn, termasuk ANTHROPIC_WORK_SECRET.
          task = asyncio.create_task(worker.handle_item())
          # Membatalkan task saat container dihentikan memungkinkan worker mengunggah
          # file memori yang berubah dan menghapus direktori store sebelum keluar.
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

  const client = new Anthropic({ authToken: process.env.ANTHROPIC_ENVIRONMENT_KEY });
  const controller = new AbortController();
  // Membatalkan saat container dihentikan memungkinkan worker mengunggah file memori yang berubah
  // dan menghapus direktori store sebelum keluar.
  process.once("SIGTERM", () => controller.abort());
  process.once("SIGINT", () => controller.abort());

  // Tanpa argumen, handleItem() membaca variabel ANTHROPIC_* yang diteruskan oleh skrip
  // spawn, termasuk ANTHROPIC_WORK_SECRET.
  await new EnvironmentWorker({
    client,
    workdir: "/workspace",
    signal: controller.signal
  }).handleItem();
  ```

  ```csharp C#
  // EnvironmentWorker saat ini belum tersedia di SDK C#.
  ```

  ```go Go
  package main

  import (
  	"context"
  	"log"
  	"os"
  	"os/signal"
  	"syscall"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/lib/environments"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  func main() {
  	// Membatalkan context saat container dihentikan memungkinkan worker mengunggah
  	// file memori yang berubah dan menghapus direktori store sebelum keluar.
  	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
  	defer stop()

  	client := anthropic.NewClient(option.WithAuthToken(os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")))
  	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  		Workdir: "/workspace",
  	})
  	// Dengan opsi bernilai nol, HandleItem membaca variabel ANTHROPIC_* yang diteruskan
  	// oleh skrip spawn, termasuk ANTHROPIC_WORK_SECRET.
  	if err := worker.HandleItem(ctx, environments.HandleItemOptions{}); err != nil {
  		log.Fatalf("worker: %v", err)
  	}
  }

  ```

  ```java Java
  // EnvironmentWorker saat ini belum tersedia di Java SDK.
  ```

  ```php PHP
  // EnvironmentWorker saat ini belum tersedia di PHP SDK.
  ```

  ```ruby Ruby
  # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
  ```
</CodeGroup>

## Menyiapkan file untuk sesi

Anthropic tidak me-mount file atau repositori GitHub ke dalam sandbox self-hosted. Untuk menyediakan file khusus sesi:

1. Teruskan referensi file, seperti path S3 atau SHA commit, di field `metadata` sesi.
2. Di skrip spawn atau handler `--on-work` Anda, ambil sesi (`GET /v1/sessions/{session_id}`) dan baca `metadata`. Work item yang diklaim membawa ID sesi tetapi tidak membawa metadata.
3. Siapkan file ke dalam direktori kerja sebelum eksekusi alat dimulai.

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ANTHROPIC_ENVIRONMENT_ID",
    "metadata": {"input_file": "s3://my-bucket/data.csv"}
  }
  EOF
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ANTHROPIC_ENVIRONMENT_ID" \
    --metadata '{"input_file": "s3://my-bucket/data.csv"}'
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      metadata={"input_file": "s3://my-bucket/data.csv"},
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    metadata: { input_file: "s3://my-bucket/data.csv" }
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Metadata = new Dictionary<string, string> { ["input_file"] = "s3://my-bucket/data.csv" },
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
  	EnvironmentID: environment.ID,
  	Metadata: map[string]string{
  		"input_file": "s3://my-bucket/data.csv",
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .metadata(SessionCreateParams.Metadata.builder()
          .putAdditionalProperty("input_file", JsonValue.from("s3://my-bucket/data.csv"))
          .build())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      metadata: ['input_file' => 's3://my-bucket/data.csv'],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    metadata: {input_file: "s3://my-bucket/data.csv"}
  )
  ```
</CodeGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Memantau dan memecahkan masalah" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations">
    Baca kedalaman antrean, hentikan sesi dan worker dengan bersih, dan perbaiki kegagalan umum.
  </Card>

  <Card title="Model keamanan" icon="lock" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security">
    Model tanggung jawab bersama untuk environment sandbox self-hosted.
  </Card>
</CardGroup>
