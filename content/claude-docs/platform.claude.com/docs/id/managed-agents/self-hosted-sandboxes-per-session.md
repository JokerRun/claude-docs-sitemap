---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session
fetched_at: 2026-11-19T02:13:30.221159Z
sha256: ec81735909e6a18242bc4724d3c847b7315dfd9462dff2ec60ac120afac19498
---

---
title: Menjalankan satu sandbox per sesi
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session
description: Berikan setiap sesi sandbox self-hosted miliknya sendiri dengan Helm chart di Kubernetes, skrip spawn, atau poller SDK.
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

Dalam pola sandbox-per-sesi, setiap sesi berjalan di sandbox baru, yang dapat memiliki sistem file, batas sumber daya, dan kontrol jaringannya sendiri. Untuk membandingkannya dengan pola lain, lihat [Pilih pola deployment](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#choose-a-deployment-pattern).

Anda dapat menyiapkannya dengan tiga cara:

* **[Helm chart di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#run-sandboxes-on-kubernetes):** Dispatcher Anthropic mengklaim pekerjaan dan memulai pod untuk setiap sesi di cluster Anda.
* **[Skrip spawn](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#launch-sandboxes-with-a-spawn-script):** CLI `ant` mengklaim pekerjaan dan memanggil skrip Anda, yang meluncurkan sandbox di platform apa pun.
* **[Poller SDK](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#launch-sandboxes-from-the-sdk-poller):** Kode Anda sendiri mengklaim pekerjaan dan meluncurkan sandbox.

Bagian-bagian setelah [Menjalankan sandbox di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#run-sandboxes-on-kubernetes) berlaku untuk skrip spawn dan poller SDK.

## Menjalankan sandbox di Kubernetes

Anthropic menerbitkan Helm chart, `cma-sandboxes`, beserta image-nya. Chart ini menjalankan satu sandbox per sesi di cluster Kubernetes Anda sendiri. Dispatcher-nya melakukan polling pada antrean pekerjaan environment dan memberikan setiap sesi pod miliknya sendiri:

* **Isolasi:** Setiap pod berjalan di bawah [gVisor](https://gvisor.dev/) di balik network policy chart. Pod memiliki sistem file dan batas sumber dayanya sendiri. Hanya dispatcher yang memegang kunci environment.
* **Afinitas sesi:** Setiap pesan dalam sebuah sesi masuk ke sandbox sesi tersebut. Setelah sesi idle selama 30 menit (nilai default dari pengaturan `sandbox.idleTimeout` chart), pod-nya berhenti. Volume `/workspace`-nya tetap ada hingga sesi berakhir. Pesan berikutnya memulai pod pada volume yang sama.
* **Warm pool:** Kecuali di Google Kubernetes Engine (GKE), chart ini menyiapkan dua pod yang siap untuk sesi baru (nilai default dari pengaturan `sandbox.warmPoolSize` chart).

Pod sandbox menjalankan worker CLI `ant`. Pod ini mendukung [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory) dengan pengaturan sinkronisasi default, dan tidak mendukung [alat kustom](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools).

### Menginstal chart

Chart ini berjalan di GKE, Amazon EKS, dan cluster lainnya. Siapkan hal-hal berikut sebelum Anda menginstalnya:

* **Di cluster:** Controller [Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) (di GKE, add-on Agent Sandbox), node yang menjalankan gVisor, dan plugin jaringan yang menerapkan NetworkPolicy.
* **Di namespace Anda sendiri:** Label Pod Security Standard Restricted, Secret berisi ID environment dan [kunci environment](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-your-first-session), serta sertifikat TLS dispatcher.

[Panduan instalasi di GitHub](https://github.com/anthropics/anthropic-cli/blob/main/sandboxes/kubernetes/README.md) berisi langkah-langkah penyiapan untuk setiap jenis cluster. Panduan ini juga membahas upgrade dan rotasi kunci.

Simpan pengaturan Anda sebagai `cma-values.yaml`. Instalasi akan gagal tanpa tiga pengaturan dalam file ini:

<File filename="cma-values.yaml">
  ```yaml
  platform: gke             # or eks, or generic for any other cluster
  egress:
    # The chart already blocks the private ranges. List your other addresses
    # that sandboxes must not reach.
    clusterCIDRs:
      - 203.0.113.10/32     # your cluster's Kubernetes API endpoint
    cmaServer:
      public: true          # the Claude API has a public address
  ```
</File>

Panduan instalasi mencantumkan pengaturan yang bergantung pada cluster Anda, seperti `gke.dns` di GKE Autopilot. Panduan ini juga menjelaskan kapan `egress.clusterIsPrivate: true` menggantikan `egress.clusterCIDRs`.

Kemudian, instal chart:

```bash
helm install cma \
  oci://us-docker.pkg.dev/anthropic-public-registry/sandboxes/charts/cma-sandboxes \
  --version 0.1.0 \
  --namespace cma \
  -f cma-values.yaml \
  --wait
```

Setelah instalasi, jalankan pemeriksaan preflight yang dijelaskan dalam panduan instalasi.

<Warning>
  Jangan hapus chart hanya dengan `helm uninstall`. Perintah tersebut menghapus network policy dan membiarkan sandbox sesi tetap berjalan tanpanya. Hentikan dispatcher dan hapus sandbox terlebih dahulu, sesuai urutan yang diberikan [bagian Removal dalam panduan instalasi](https://github.com/anthropics/anthropic-cli/blob/main/sandboxes/kubernetes/README.md#removal).
</Warning>

### Menambahkan alat ke image sandbox

Image sandbox yang diterbitkan adalah Alpine Linux dengan `bash`, `curl`, `jq`, dan CLI `ant`. Chart menjalankannya dengan sistem file root read-only dan sebagai pengguna non-root, sehingga agen tidak dapat menginstal paket selama sesi.

Untuk memberikan lebih banyak alat kepada agen Anda, seperti Python atau Git, build kedua image dari repositori pada tag rilis. [Bagian Install dalam panduan instalasi](https://github.com/anthropics/anthropic-cli/blob/main/sandboxes/kubernetes/README.md#install) berisi perintah-perintahnya. Push image ke registry Anda sebagai `cma-dispatcher` dan `cma-sandbox`, dengan versi chart sebagai tag. Kemudian, atur `image.registry` ke registry tersebut. Jika Anda mem-pin digest image, gunakan digest dari image Anda sendiri.

### Membatasi egress jaringan

Secara default, network policy chart memungkinkan sandbox menjangkau internet IPv4 publik. Policy ini memblokir rentang alamat privat, server metadata cloud, dan alamat dalam `egress.clusterCIDRs`. Agen yang terkena prompt injection dapat mengirimkan apa yang dibacanya ke alamat mana pun yang dapat dijangkau sandbox-nya. [Network egress](https://github.com/anthropics/anthropic-cli/blob/main/sandboxes/kubernetes/README.md#network-egress) dalam panduan instalasi berisi detailnya.

* **GKE dengan Dataplane V2:** Atur `egress.mode: fqdnGke` untuk membatasi koneksi ke port 443 pada host dalam `egress.fqdnGke.hosts`. Pertahankan `api.anthropic.com` dalam daftar tersebut, dan tambahkan setiap host yang dibutuhkan oleh perintah agen Anda. Tidak seperti default, mode ini tidak memiliki daftar rentang yang diblokir. Mode ini mengizinkan alamat apa pun yang di-resolve dari nama host yang tercantum, jadi cantumkan hanya host yang DNS-nya Anda percayai. Sandbox masih dapat mengirimkan data keluar di dalam lookup DNS.
* **Cluster lain dan GKE tanpa Dataplane V2:** Default adalah satu-satunya mode.
* **Setiap cluster:** Network policy tidak mencakup port yang didengarkan oleh node milik cluster itu sendiri. Lihat [Node isolation you own](https://github.com/anthropics/anthropic-cli/blob/main/sandboxes/kubernetes/README.md#node-isolation-you-own) dalam panduan instalasi.

## Meluncurkan sandbox dengan skrip spawn

Poller di host mengklaim pekerjaan dan memanggil skrip Anda sekali untuk setiap item pekerjaan. Skrip tersebut meluncurkan sandbox untuk satu sesi itu.

<Steps>
  <Step title="Build image sandbox">
    Instal `ant` dan atur `ant beta:worker run` sebagai entrypoint. Saat sandbox dimulai, sandbox membaca detail sesi dari variabel lingkungan, menangani sesi tersebut, lalu keluar. Image dasar harus menyediakan `/bin/bash`; proses build menggunakan `curl` hanya untuk mengunduh `ant`.

    <File filename="Dockerfile">
      ```dockerfile
      FROM your-base-image
      ARG ANT_VERSION=2.11.0
      ARG TARGETARCH
      RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo arm64 || echo amd64) && \
          curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${ANT_VERSION}/ant_${ANT_VERSION}_linux_${ARCH}.tar.gz" \
            | tar -xz -C /usr/local/bin ant
      WORKDIR /workspace
      VOLUME /workspace
      ENTRYPOINT ["ant", "beta:worker", "run"]
      ```
    </File>
  </Step>

  <Step title="Tulis skrip spawn">
    Skrip ini meneruskan detail sesi ke sandbox baru. Skrip ini memerlukan `jq` di host poller.

    <File filename="spawn.sh">
      ```bash
      #!/bin/bash
      # spawn.sh: dipanggil sekali untuk setiap item pekerjaan yang diklaim
      # Item pekerjaan yang diklaim diterima sebagai JSON melalui stdin.
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
    </File>

    Poller mengatur `ANTHROPIC_WORK_ID`, `ANTHROPIC_ENVIRONMENT_ID`, `ANTHROPIC_SESSION_ID`, dan `ANTHROPIC_ENVIRONMENT_KEY`. `ANTHROPIC_BASE_URL` hanya sampai ke skrip jika Anda mengaturnya di host poller. Skrip membaca `ANTHROPIC_WORK_SECRET` dari JSON item pekerjaan pada standard input. Lihat [Variabel lingkungan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#environment-variables).

    `/host/outputs` adalah direktori host yang Anda pilih. Me-mount-nya di `/workspace` memungkinkan Anda mengambil hasil kerja sesi setelah sandbox keluar. Mount ini juga menyertakan tree `skills/` yang diunduh dan file-file perantara apa pun.
  </Step>

  <Step title="Mulai poller">
    ```bash
    ant beta:worker poll --on-work ./spawn.sh
    ```
  </Step>
</Steps>

## Meneruskan secret item pekerjaan

Setiap item pekerjaan yang diklaim dapat membawa `secret` (csharp, go: `Secret`) yang diterbitkan oleh Anthropic untuk sesi tersebut. Worker yang menjalankan sesi memerlukannya untuk me-mount [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory).

Worker yang mengklaim dan menjalankan sesi dalam satu proses meneruskan secret tersebut dengan sendirinya. `EnvironmentWorker` dengan `run()` (go: `Run()`) adalah salah satu worker tersebut, dan `ant beta:worker poll` tanpa `--on-work` adalah yang lainnya. Ketika kode Anda sendiri berada di antara klaim dan worker, Anda yang meneruskan secret:

| Anda mengklaim pekerjaan dengan                                                                                           | Secret tiba sebagai                                                    | Teruskan ke worker sebagai                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ant beta:worker poll --on-work`                                                                                          | Field `secret` dari JSON item pekerjaan pada standard input skrip Anda | `ANTHROPIC_WORK_SECRET` di environment sandbox                                                                                                                                                |
| `work.poller()` (typescript: `new WorkPoller()`; go: `environments.NewWorkPoller()`) dari SDK Python, TypeScript, atau Go | Field `secret` (go: `Secret`) dari setiap item pekerjaan yang diklaim  | `ANTHROPIC_WORK_SECRET` di environment sandbox atau argumen `work_secret` (typescript: `workSecret`; go: `WorkSecret`) untuk `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`) |

Teruskan secret hanya ke sandbox yang melayani sesi tersebut, dan jangan pernah mencatatnya ke log. Lihat [Model keamanan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security) untuk mengetahui hubungannya dengan kunci environment.

## Meluncurkan sandbox dari poller SDK

Untuk mengklaim pekerjaan dari kode Anda sendiri alih-alih `ant beta:worker poll --on-work`, gunakan poller di SDK Python, TypeScript, atau Go: `work.poller()` (typescript: `new WorkPoller()`; go: `environments.NewWorkPoller()`). Poller ini melakukan polling pada antrean dan memberikan setiap sesi yang diklaim kepada Anda, lalu Anda meluncurkan sandbox:

<CodeGroup exclude="shell, csharp, java, php, ruby">
  <CodeGroupItem language="cURL">
    Mengklaim pekerjaan dalam loop dan meluncurkan sandbox untuk setiap sesi membutuhkan lebih banyak logika daripada satu perintah shell. Dari shell, jalankan `ant beta:worker poll --on-work` dengan skrip spawn, seperti pada [Meluncurkan sandbox dengan skrip spawn](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#launch-sandboxes-with-a-spawn-script).
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Untuk mengklaim pekerjaan dari shell dan meluncurkan sandbox untuk setiap sesi, jalankan `ant beta:worker poll --on-work` dengan skrip spawn. Lihat [Meluncurkan sandbox dengan skrip spawn](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#launch-sandboxes-with-a-spawn-script).
  </CodeGroupItem>

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
      # environment (jangan pernah kunci API Anda) dan secret per sesi milik item pekerjaan: worker
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
    // (jangan pernah kunci API Anda) dan secret per sesi milik item pekerjaan: worker
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

  <CodeGroupItem language="C#">
    SDK C# tidak memiliki helper yang melakukan polling untuk pekerjaan. Untuk mengklaim pekerjaan dari kode Anda sendiri, panggil [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work) untuk melakukan polling item dan melakukan acknowledge terhadapnya.
  </CodeGroupItem>

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"log"
  	"os"
  	"os/exec"

  	"github.com/anthropics/anthropic-sdk-go/v2"
  	"github.com/anthropics/anthropic-sdk-go/v2/lib/environments"
  	"github.com/anthropics/anthropic-sdk-go/v2/option"
  	"github.com/anthropics/anthropic-sdk-go/v2/packages/param"
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
  	// Ganti `docker run` dengan peluncur sandbox Anda sendiri. Teruskan kunci
  	// environment (jangan pernah kunci API Anda) dan secret per sesi dari item pekerjaan: worker
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

  <CodeGroupItem language="Java">
    SDK Java tidak memiliki helper yang melakukan polling untuk pekerjaan. Untuk mengklaim pekerjaan dari kode Anda sendiri, panggil [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work) untuk melakukan polling item dan melakukan acknowledge terhadapnya.
  </CodeGroupItem>

  <CodeGroupItem language="PHP">
    SDK PHP tidak memiliki helper yang melakukan polling untuk pekerjaan. Untuk mengklaim pekerjaan dari kode Anda sendiri, panggil [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work) untuk melakukan polling item dan melakukan acknowledge terhadapnya.
  </CodeGroupItem>

  <CodeGroupItem language="Ruby">
    SDK Ruby tidak memiliki helper yang melakukan polling untuk pekerjaan. Untuk mengklaim pekerjaan dari kode Anda sendiri, panggil [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work) untuk melakukan polling item dan melakukan acknowledge terhadapnya.
  </CodeGroupItem>
</CodeGroup>

## Menjalankan worker SDK di dalam sandbox

Ganti entrypoint `ant beta:worker run` dengan entrypoint SDK ketika sandbox harus [melayani alat kustom](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools) atau menggunakan [pengaturan sinkronisasi memori non-default](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#configure-sync). Entrypoint ini membuat `EnvironmentWorker` dan memanggil `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`), yang membaca variabel `ANTHROPIC_*` yang sama dengan yang diteruskan oleh skrip spawn.

<CodeGroup exclude="shell, csharp, java, php, ruby">
  <CodeGroupItem language="cURL">
    Worker adalah proses yang berjalan lama, bukan satu permintaan HTTP. Untuk melayani alat kustom atau mengubah pengaturan sinkronisasi memori, gunakan `EnvironmentWorker` di SDK Python, TypeScript, atau Go.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Worker CLI `ant` (`ant beta:worker run`) tidak dapat melayani alat kustom atau mengubah pengaturan sinkronisasi memori. Untuk melakukan salah satunya, gunakan `EnvironmentWorker` di SDK Python, TypeScript, atau Go.
  </CodeGroupItem>

  ```python Python
  import asyncio
  import contextlib
  import os
  import signal
  from anthropic import AsyncAnthropic
  from anthropic.lib.environments import EnvironmentWorker


  async def main() -> None:
      async with AsyncAnthropic(
          auth_token=os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
      ) as client:
          worker = EnvironmentWorker(client, workdir="/workspace")
          # Tanpa argumen, handle_item() membaca variabel ANTHROPIC_* yang diteruskan
          # oleh skrip spawn, termasuk ANTHROPIC_WORK_SECRET.
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
  // Membatalkan saat container dihentikan memungkinkan worker mengunggah file memori
  // yang berubah dan menghapus direktori store sebelum keluar.
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

  <CodeGroupItem language="C#">
    SDK C# tidak memiliki `EnvironmentWorker`.
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

  <CodeGroupItem language="Java">
    SDK Java tidak memiliki `EnvironmentWorker`.
  </CodeGroupItem>

  <CodeGroupItem language="PHP">
    SDK PHP tidak memiliki `EnvironmentWorker`.
  </CodeGroupItem>

  <CodeGroupItem language="Ruby">
    SDK Ruby tidak memiliki `EnvironmentWorker`.
  </CodeGroupItem>
</CodeGroup>

## Menyiapkan file untuk sesi

Anthropic tidak me-mount file atau repositori GitHub ke dalam sandbox self-hosted. Untuk menyediakan file khusus sesi:

1. Teruskan referensi file, seperti path S3 atau SHA commit, di field `metadata` (csharp, go: `Metadata`) sesi.
2. Di skrip spawn atau handler `--on-work` Anda, ambil sesi (`GET /v1/sessions/{session_id}`) dan baca `metadata` (csharp, go: `Metadata`). Item pekerjaan yang diklaim membawa ID sesi tetapi tidak membawa metadata.
3. Tempatkan file ke direktori kerja sebelum alat apa pun berjalan.

Contoh cURL membaca token akses dari `ANTHROPIC_AUTH_TOKEN`. Untuk mendapatkannya, siapkan Workload Identity Federation dengan scope default `workspace:developer`, seperti yang dijelaskan di [Menyiapkan federasi](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#set-up-federation). Kemudian, tukarkan token identitas workload Anda dengan token akses, seperti yang ditunjukkan di [Autentikasi dari workload Anda](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#authenticate-from-your-workload). Atur `ANTHROPIC_AUTH_TOKEN` hanya di shell tempat Anda menjalankan contoh cURL, karena variabel ini lebih diutamakan daripada pengaturan federasi Anda. [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication) mencantumkan kredensial lain yang diterima API, seperti kunci API dari quickstart.

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "agent": "agent_011CYm1BLqPXpQRk5khsSXrs",
      "environment_id": "env_01595EKxaaTTGwwY3kyXdtbs",
      "metadata": {"input_file": "s3://my-bucket/data.csv"}
    }'
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent agent_011CYm1BLqPXpQRk5khsSXrs \
    --environment-id env_01595EKxaaTTGwwY3kyXdtbs \
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
  <Card title="Memantau dan memecahkan masalah worker self-hosted" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations">
    Baca kedalaman antrean, hentikan sesi dan worker dengan bersih, serta perbaiki kegagalan umum.
  </Card>
</CardGroup>
