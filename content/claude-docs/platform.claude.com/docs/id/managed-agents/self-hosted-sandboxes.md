---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: 466bc4bb577b6a1d49f6204fa360ab5b25da59091b52c7b253ae81928ec8ca2c
---

# Sandbox yang di-hosting sendiri

Jalankan sesi agen di lingkungan sandbox yang di-hosting sendiri milik Anda.

---

Secara default, Managed Agents mengeksekusi alat dan kode di dalam [sandbox cloud yang dikelola Anthropic](/docs/id/managed-agents/cloud-sandboxes-reference). Sandbox yang di-hosting sendiri (self-hosted sandbox) mempertahankan orkestrasi di sisi Anthropic tetapi memindahkan eksekusi alat ke infrastruktur yang Anda kendalikan, sehingga kode agen, filesystem, dan egress jaringan tidak pernah meninggalkan lingkungan Anda.

Eksekusi alat tetap berada di host Anda: filesystem yang dibaca dan ditulis oleh agen, proses yang dijalankannya, dan jaringan yang dapat dijangkaunya semuanya berada di bawah kendali Anda. Input dan output alat tetap mengalir ke control plane Anthropic (tempat Claude berjalan) sehingga model dapat melihat hasil dan menentukan apa yang harus dilakukan selanjutnya. Lihat [model keamanan](/docs/id/managed-agents/self-hosted-sandboxes-security) untuk batas aliran data selengkapnya.

<Note>
  Sandbox yang di-hosting sendiri mendukung semua model Claude yang tersedia di Managed Agents, termasuk Claude Opus 4.8. Model dikonfigurasi pada [agen](/docs/id/managed-agents/agent-setup), bukan pada lingkungan.
</Note>

## Perbedaannya dengan lingkungan cloud

|                                 | Lingkungan cloud                | Sandbox yang di-hosting sendiri |
| ------------------------------- | ------------------------------- | ------------------------------- |
| Tempat alat berjalan            | Sandbox yang dikelola Anthropic | Infrastruktur Anda              |
| Jangkauan jaringan              | Kontrol egress Anthropic        | Kebijakan jaringan Anda         |
| Pemasangan file dan repo GitHub | Dikelola oleh Anthropic         | Dikelola oleh Anda              |
| Siklus hidup                    | Dikelola oleh Anthropic         | Dikelola oleh Anda              |

Hosting sendiri cocok ketika agen perlu beroperasi pada data yang tidak boleh meninggalkan batas jaringan Anda, menjangkau layanan internal yang tidak dapat dirutekan secara publik, atau berjalan di bawah kontrol kepatuhan dan audit organisasi Anda sendiri.

Untuk kelayakan Zero Data Retention dan HIPAA BAA, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

## Kapan menggabungkannya dengan MCP tunnel

Hosting sendiri mengontrol *di mana kode agen dieksekusi*. [MCP tunnel](/docs/id/agents-and-tools/mcp-tunnels/overview) mengontrol *bagaimana Anthropic menjangkau server MCP di jaringan Anda*. Keduanya independen: sesi yang berjalan di sandbox cloud Anthropic tetap dapat menjangkau server MCP privat melalui tunnel, dan sesi yang di-hosting sendiri dapat menggunakan server MCP yang di-tunnel maupun yang publik. Gunakan keduanya ketika Anda ingin eksekusi dan akses alat tetap berada di dalam batas Anda.

## Environment worker

<Tip>
  Panduan ini menjelaskan cara membangun worker dengan platform sandboxing generik apa pun. Panduan tambahan yang spesifik untuk platform tersedia untuk [AWS Lambda MicroVMs](https://docs.aws.amazon.com/lambda/latest/dg/microvms-integrations-claude-managed-agents.html), [Blaxel](https://docs.blaxel.ai/Tutorials/Claude-Managed-Agents), [Cloudflare](https://developers.cloudflare.com/sandbox/claude-managed-agents/), [Daytona](https://www.daytona.io/docs/en/guides/claude/claude-managed-agents), [E2B](https://e2b.dev/docs/agents/claude-managed-agents), [GKE Agent Sandbox](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/tree/main/ai-ml/anthropic-agent-sandbox), [Modal](https://github.com/modal-labs/claude-managed-agents-modal-sandbox), [Namespace](https://namespace.so/docs/integrations/claude), [Superserve](https://docs.superserve.ai/integrations/managed-agents/claude-managed-agents), dan [Vercel](https://vercel.com/kb/guide/run-claude-managed-agent-tools-with-vercel-sandbox).
</Tip>

"Environment worker" (pekerja lingkungan) adalah proses yang Anda jalankan di infrastruktur Anda sendiri. Proses ini menerima permintaan eksekusi alat dari Anthropic dan menjalankannya secara lokal. Lingkungan `self_hosted` bertindak sebagai antrean kerja: ketika sebuah [sesi](/docs/id/managed-agents/sessions) ditugaskan ke lingkungan tersebut, Anthropic memasukkan sesi itu ke antrean sebagai item kerja. Worker Anda mengklaim item kerja dari antrean tersebut, membuat konteks eksekusi untuk masing-masing item, mengunduh [skills](/docs/id/managed-agents/skills) milik agen (sumber daya berbasis filesystem yang dapat digunakan kembali dan memberi agen keahlian spesifik domain), menjalankan panggilan alat, dan mengirimkan kembali hasilnya.

Item kerja diklaim dengan melakukan polling pada antrean lingkungan: baik oleh **worker yang selalu aktif (always-on)** yang melakukan polling secara terus-menerus, atau **handler yang dipicu webhook** yang bangun saat `session.status_run_started` dan mulai melakukan polling.

CLI dan SDK keduanya menyertakan worker yang sudah jadi. CLI `ant` hanya mendukung pola always-on; SDK mendukung baik always-on maupun yang dipicu webhook. Keduanya dapat dikonfigurasi: lihat [Self-hosted worker](/docs/id/managed-agents/reference#self-hosted-worker) di referensi untuk flag CLI, dan [SDK helpers](#sdk-helpers) di halaman ini untuk opsi SDK. Untuk kontrol lebih, panggil [endpoint Environments Work](/docs/id/api/beta/environments/work) secara langsung dan implementasikan worker Anda sendiri.

### Filesystem sandbox

* **`/workspace`:** direktori kerja default sistem untuk eksekusi alat dan pengunduhan skill. Flag `--workdir` pada CLI secara default menggunakan direktori saat ini; berikan `--workdir /workspace` agar sesuai dengan default sistem. Skill diunduh ke `<workdir>/skills/<name>/`. Jika Anda menggunakan direktori kerja yang berbeda, perbarui prompt sistem agen Anda agar Claude dapat menemukan file skill tersebut.
* **`/mnt/session/outputs`:** harness worker menginstruksikan Claude untuk menulis hasil akhir di sini. Dalam mode sandbox, pasang (mount) direktori host pada path ini untuk mengambil output setelah sesi berakhir. Dalam mode in-process, alat file milik worker menulis di bawah direktori kerja, sehingga path ini tidak berlaku.

## Sebelum Anda mulai

Anda memerlukan:

* **Agen yang sudah ada.** Jika Anda belum memilikinya, selesaikan [Quickstart](/docs/id/managed-agents/quickstart) terlebih dahulu dan catat ID agennya.
* **Host Linux** dengan `/bin/bash` pada path persis tersebut. Alat bash milik worker memanggilnya secara langsung, tanpa memeriksa `PATH`. SDK TypeScript juga memerlukan `unzip` dan `tar` pada `PATH` serta Node.js 22 atau yang lebih baru; SDK Python dan Go menggunakan pustaka standar mereka untuk ekstraksi arsip dan tidak memiliki persyaratan biner tambahan.
* **CLI `ant` atau SDK Anthropic** (Python, TypeScript, atau Go) pada host worker.
* **Dua kredensial:** kunci lingkungan (dibuat di Console pada langkah-langkah berikut) mengautentikasi worker ke antreannya; kunci API (API key) Claude Anda membuat sesi dan membaca statistik antrean dari luar host worker. Pembuatan kunci hanya dapat dilakukan melalui Console.

<Note>
  Pada [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), worker mengautentikasi dengan AWS IAM (SigV4) atau [kunci API yang dibuat di AWS Console](/docs/id/build-with-claude/claude-platform-on-aws#api-key-authentication), bukan kunci lingkungan. Lampirkan managed policy [`AnthropicSelfHostedEnvironmentAccess`](/docs/id/api/claude-platform-on-aws-iam-actions#managed-policies) ke principal IAM tempat worker Anda berjalan. Kunci lingkungan yang dibuat di Claude Console tidak berfungsi dengan endpoint Claude Platform on AWS.
</Note>

<Steps>
  <Step title="Buat lingkungan yang di-hosting sendiri">
    Di [Console](https://platform.claude.com/workspaces/default/environments): **Workspace > Environments > New > Self-hosted**

    Atau melalui API:

    <CodeGroup>
      ```bash cURL
      curl -sS --fail-with-body https://api.anthropic.com/v1/environments \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d '{
          "name": "self-hosted",
          "config": {"type": "self_hosted"}
        }'
      ```

      ```bash CLI
      ant beta:environments create \
        --name self-hosted \
        --config '{"type": "self_hosted"}'
      ```

      ```python Python
      client = anthropic.Anthropic()

      environment = client.beta.environments.create(
          name="self-hosted", config={"type": "self_hosted"}
      )
      print(environment.id)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const environment = await client.beta.environments.create({
        name: "self-hosted",
        config: { type: "self_hosted" }
      });
      console.log(environment.id);
      ```

      ```csharp C#
      using Anthropic.Models.Beta.Environments;

      var client = new AnthropicClient();

      var environment = await client.Beta.Environments.Create(
          new EnvironmentCreateParams
          {
              Name = "self-hosted",
              Config = new BetaSelfHostedConfigParams(),
          }
      );
      Console.WriteLine(environment.ID);
      ```

      ```go Go
      client := anthropic.NewClient()

      environment, err := client.Beta.Environments.New(context.Background(), anthropic.BetaEnvironmentNewParams{
      	Name: "self-hosted",
      	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
      		OfSelfHosted: &anthropic.BetaSelfHostedConfigParams{},
      	},
      })
      if err != nil {
      	panic(err)
      }
      fmt.Println(environment.ID)
      ```

      ```java Java
      import com.anthropic.models.beta.environments.BetaSelfHostedConfigParams;
      import com.anthropic.models.beta.environments.EnvironmentCreateParams;

      void main() {
          var client = AnthropicOkHttpClient.fromEnv();

          var environment = client.beta().environments().create(
              EnvironmentCreateParams.builder()
                  .name("self-hosted")
                  .config(BetaSelfHostedConfigParams.builder().build())
                  .build()
          );
          IO.println(environment.id());
      }
      ```

      ```php PHP
      $client = new Anthropic\Client();

      $environment = $client->beta->environments->create(
          name: 'self-hosted',
          config: ['type' => 'self_hosted'],
      );
      echo $environment->id, PHP_EOL;
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      environment = client.beta.environments.create(
        name: "self-hosted",
        config: {type: :self_hosted}
      )
      puts environment.id
      ```
    </CodeGroup>
  </Step>

  <Step title="Buat kunci lingkungan">
    Di Console, buka lingkungan tersebut dan klik **Generate environment key**. Pembuatan kunci hanya dapat dilakukan melalui Console, terlepas dari apakah Anda membuat lingkungan melalui Console atau API. Kemudian ekspor ID lingkungan dan kuncinya pada host worker:

    ```bash
    export ANTHROPIC_ENVIRONMENT_KEY="sk-ant-oat01-..."
    export ANTHROPIC_ENVIRONMENT_ID="env_..."
    ```
  </Step>
</Steps>

<Note>
  Skill dapat menyertakan executable yang mungkin dijalankan langsung oleh agen. Worker CLI dan SDK mempertahankan izin executable yang tercatat dalam bundel skill saat mengekstraknya. Jika Anda mengimplementasikan pengunduhan skill secara manual, Anda bertanggung jawab untuk mengatur izin executable.
</Note>

## Menjalankan worker

Pilih **always-on** untuk penyiapan paling sederhana: proses yang berjalan lama melakukan polling antrean secara terus-menerus dan hanya memerlukan HTTPS keluar. Pilih **dipicu webhook** untuk menghindari menjalankan poller yang menganggur; ini memerlukan endpoint webhook yang dapat dijangkau Anthropic (lihat [Webhooks](/docs/id/managed-agents/webhooks) untuk penyiapan endpoint dan verifikasi tanda tangan).

<Tabs>
  <Tab title="Always-on (ant CLI)">
    <Steps>
      <Step title="Instal CLI ant">
        Jalankan ini pada host worker.

        <Tabs>
          <Tab title="curl (Linux/WSL)">
            Untuk lingkungan Linux, unduh biner rilis secara langsung.

            ```bash
            VERSION=1.15.0
            OS=$(uname -s | tr '[:upper:]' '[:lower:]')
            case $(uname -m) in
              x86_64) ARCH=amd64 ;;
              aarch64) ARCH=arm64 ;;
            esac
            curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_${OS}_${ARCH}.tar.gz" \
              | sudo tar -xz -C /usr/local/bin ant
            ```

            Anda dapat menemukan semua rilis di [halaman rilis GitHub](https://github.com/anthropics/anthropic-cli/releases).
          </Tab>

          <Tab title="Homebrew (macOS)">
            ```bash
            brew install anthropics/tap/ant
            ```
          </Tab>
        </Tabs>
      </Step>

      <Step title="Jalankan worker">
        **In-process**

        `ant beta:worker poll` mengklaim item kerja yang ditugaskan ke lingkungan, mengunduh skill, mengeksekusi panggilan alat di direktori kerja, dan mengirimkan kembali hasilnya. Perintah ini membaca `ANTHROPIC_ENVIRONMENT_KEY` dan `ANTHROPIC_ENVIRONMENT_ID` dari environment.

        ```bash
        ant beta:worker poll \
          --workdir "/workspace"
        ```

        Worker keluar dengan bersih saat menerima SIGTERM atau SIGINT, menyelesaikan panggilan alat yang sedang berjalan sebelum berhenti.

        **Sandbox per sesi**

        Jika Anda memerlukan isolasi yang lebih kuat (filesystem yang baru, batas sumber daya, atau kontrol jaringan per sesi), jalankan setiap sesi di sandbox-nya sendiri. Bangun image dengan `ant` terinstal dan `ant beta:worker run` sebagai entrypoint. Image dasar harus menyediakan `/bin/bash`; `curl` hanya digunakan pada saat build. Ketika sandbox dimulai, ia membaca detail sesi dari variabel environment, menangani sesi tersebut, dan keluar:

        ```text
        FROM your-base-image
        ARG ANT_VERSION=1.15.0
        ARG TARGETARCH
        RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo arm64 || echo amd64) && \
            curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${ANT_VERSION}/ant_${ANT_VERSION}_linux_${ARCH}.tar.gz" \
              | tar -xz -C /usr/local/bin ant
        WORKDIR /workspace
        VOLUME /mnt/session/outputs
        ENTRYPOINT ["ant", "beta:worker", "run"]
        ```

        Kemudian tulis skrip spawn yang meneruskan detail sesi ke sandbox yang baru. Poller menyuntikkan `ANTHROPIC_SESSION_ID`, `ANTHROPIC_WORK_ID`, `ANTHROPIC_ENVIRONMENT_ID`, dan `ANTHROPIC_ENVIRONMENT_KEY` ke environment skrip tersebut. `ANTHROPIC_BASE_URL` bersifat opsional dan hanya diteruskan jika telah diatur pada host poller; variabel ini menimpa endpoint API default. Dalam contoh ini, `/host/outputs` adalah direktori host yang Anda pilih; direktori ini di-bind-mount ke `/mnt/session/outputs` milik sandbox sehingga Anda dapat mengambil hasil sesi setelah sandbox keluar.

        ```bash
        #!/bin/bash
        # spawn.sh: dipanggil sekali untuk setiap item pekerjaan yang diklaim
        mkdir -p "/host/outputs/$ANTHROPIC_SESSION_ID"
        exec docker run --rm \
          -e ANTHROPIC_SESSION_ID -e ANTHROPIC_ENVIRONMENT_KEY \
          -e ANTHROPIC_WORK_ID -e ANTHROPIC_ENVIRONMENT_ID -e ANTHROPIC_BASE_URL \
          -v "/host/outputs/$ANTHROPIC_SESSION_ID":/mnt/session/outputs \
          your-image
        ```

        Mulai poller dengan mengarahkannya ke skrip tersebut:

        ```bash
        ant beta:worker poll \
          --on-work ./spawn.sh
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Always-on (SDK)">
    <Steps>
      <Step title="Jalankan worker">
        `EnvironmentWorker` mengklaim item kerja yang ditugaskan ke lingkungan, mengunduh skill, mengeksekusi panggilan alat di direktori kerja, dan mengirimkan kembali hasilnya. Autentikasi dengan kunci lingkungan yang Anda buat di [Sebelum Anda mulai](#before-you-begin).

        <CodeGroup>
          ```python Python
          import asyncio
          import os
          from anthropic import AsyncAnthropic
          from anthropic.lib.environments import EnvironmentWorker


          async def main() -> None:
              environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
              environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
              async with AsyncAnthropic(auth_token=environment_key) as client:
                  await EnvironmentWorker(
                      client,
                      environment_id=environment_id,
                      environment_key=environment_key,
                      workdir="/workspace",
                  ).run()


          asyncio.run(main())
          ```

          ```typescript TypeScript
          import Anthropic from "@anthropic-ai/sdk";
          import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";

          const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
          const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
          const client = new Anthropic({ authToken: environmentKey });
          const controller = new AbortController();
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
          // EnvironmentWorker saat ini belum tersedia di SDK C#. Lihat tab Always-on (ant CLI).
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
          // EnvironmentWorker saat ini belum tersedia di Java SDK. Lihat tab Always-on (ant CLI).
          ```

          ```php PHP
          // EnvironmentWorker saat ini belum tersedia di SDK PHP. Lihat tab Always-on (ant CLI).
          ```

          ```ruby Ruby
          # EnvironmentWorker saat ini belum tersedia di SDK Ruby. Lihat tab Always-on (ant CLI).
          ```
        </CodeGroup>
      </Step>
    </Steps>
  </Tab>

  <Tab title="Dipicu webhook (SDK)">
    <Steps>
      <Step title="Berlangganan webhook sesi">
        Di [Console](https://platform.claude.com/settings/workspaces/default/webhooks), tentukan endpoint webhook yang mendengarkan event `session.status_run_started`. Lihat [Webhooks](/docs/id/managed-agents/webhooks) untuk detailnya.
      </Step>

      <Step title="Ekspor kunci penandatanganan webhook">
        Selain ID dan kunci lingkungan dari [Sebelum Anda mulai](#before-you-begin), ekspor kunci penandatanganan webhook pada host handler Anda agar handler dapat memverifikasi payload yang masuk. Verifikasi tanda tangan pada handler Python memerlukan extra webhooks: `pip install "anthropic[webhooks]"`.

        ```bash
        export ANTHROPIC_WEBHOOK_SIGNING_KEY="whsec_..."
        ```
      </Step>

      <Step title="Implementasikan handler webhook">
        `EnvironmentWorker` mengklaim item kerja, mengunduh skill, mengeksekusi panggilan alat di direktori kerja, mengirimkan kembali hasilnya, dan keluar. Panggil handler ini ketika `session.status_run_started` terpicu.

        <CodeGroup>
          ```python Python
          import os
          import anthropic

          environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
          environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
          client = anthropic.AsyncAnthropic(
              auth_token=environment_key,
          )


          async def handle(raw: bytes, headers: dict[str, str]) -> dict:
              event = client.beta.webhooks.unwrap(raw.decode(), headers=headers)
              if event.data.type != "session.status_run_started":
                  return {"status": "ignored"}
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
                  )
              return {"status": "ok"}
          ```

          ```typescript TypeScript
          import Anthropic from "@anthropic-ai/sdk";

          const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
          const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
          const client = new Anthropic({
            authToken: environmentKey
          });

          export async function handle(req: Request): Promise<Response> {
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
              autoStop: false
            })) {
              await client.beta.environments.work.worker({ workdir: "/workspace" }).handleItem({
                workId: work.id,
                environmentId,
                sessionId: work.data.id,
                environmentKey
              });
            }
            return Response.json({ status: "ok" });
          }
          ```

          ```csharp C#
          // EnvironmentWorker saat ini belum tersedia di SDK C#.
          // Untuk menangani work item secara langsung, lihat endpoint Environments Work.
          ```

          ```go Go
          package main

          import (
          	"context"
          	"encoding/json"
          	"io"
          	"log/slog"
          	"net/http"
          	"os"

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

          	// SDK Go tidak menyediakan fungsi praktis RunOne: kuras item yang tertunda
          	// dengan WorkPoller dan jalankan masing-masing dengan HandleItem.
          	// Lepaskan dari r.Context(): sesi dapat bertahan melebihi batas waktu pengiriman webhook.
          	ctx := context.Background()
          	poller := environments.NewWorkPoller(ctx, client, environments.WorkPollerOptions{
          		EnvironmentID:      environmentID,
          		EnvironmentKey:     environmentKey,
          		BlockMs:            param.Null[int64](),
          		ReclaimOlderThanMs: param.NewOpt[int64](2000),
          		Drain:              true,
          	})
          	defer poller.Close()
          	for poller.Next() {
          		item := poller.Current()
          		if err := worker.HandleItem(ctx, environments.HandleItemOptions{
          			WorkID:         item.ID,
          			EnvironmentID:  item.EnvironmentID,
          			SessionID:      item.Data.ID,
          			EnvironmentKey: environmentKey,
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
          	http.HandleFunc("POST /webhook", handle)
          	if err := http.ListenAndServe(":8080", nil); err != nil {
          		slog.Error("http server", "err", err)
          		os.Exit(1)
          	}
          }

          ```

          ```java Java
          // EnvironmentWorker saat ini belum tersedia di Java SDK.
          // Untuk menangani work item secara langsung, lihat endpoint Environments Work.
          ```

          ```php PHP
          // EnvironmentWorker saat ini belum tersedia di SDK PHP.
          // Untuk menangani work item secara langsung, lihat endpoint Environments Work.
          ```

          ```ruby Ruby
          # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
          # Untuk menangani work item secara langsung, lihat endpoint Environments Work.
          ```
        </CodeGroup>
      </Step>
    </Steps>
  </Tab>
</Tabs>

### SDK helpers

SDK menyediakan tiga helper pada tingkat kontrol yang berbeda. `EnvironmentWorker` mencakup sebagian besar kasus penggunaan; turun ke helper tingkat lebih rendah ketika Anda perlu meluncurkan proses per sesi Anda sendiri atau menjalankan alat terhadap sesi yang sudah diklaim.

* **`EnvironmentWorker`:** worker siap pakai. Menangani polling, penyiapan, dan eksekusi dari awal hingga akhir.

  * `.run()`: berjalan tanpa batas waktu, mengambil sesi saat sesi tersebut tiba.
  * `.handle_item()`: menangani satu item kerja yang telah diklaim lalu keluar. Berikan pengidentifikasi work, session, dan environment secara eksplisit, atau biarkan ia membaca variabel `ANTHROPIC_*` yang diatur oleh `ant beta:worker poll --on-work` untuk proses yang dijalankannya.

* **`work.poller()`:** melakukan polling antrean kerja atas nama Anda dan memberikan setiap sesi yang diklaim. Gunakan ini ketika Anda ingin menentukan apa yang terjadi untuk setiap sesi, misalnya meluncurkan sandbox alih-alih menjalankan alat secara in-process.

  * `drain`: apakah berhenti melakukan polling setelah antrean kosong alih-alih menunggu pekerjaan baru.
  * `block_ms`: berapa lama menunggu pekerjaan tiba sebelum kembali, dalam milidetik. Harus antara 1 dan 999 (waktu tunggu per polling; helper melakukan polling ulang secara otomatis). Berikan `null` (`None` di Python, `param.Null[int64]()` di Go) untuk pemeriksaan non-blocking; menghilangkan parameter ini menggunakan long-poll default 999 ms.
  * `reclaim_older_than_ms`: mengklaim ulang item kerja yang telah diklaim tetapi tidak pernah di-acknowledge dalam jumlah milidetik ini.
  * `auto_stop`: apakah mengirimkan sinyal stop untuk setiap item kerja setelah badan loop Anda selesai dengannya. Poller Go tidak memiliki opsi untuk menonaktifkan ini dan selalu mengirimkan sinyal stop, jadi blokir di badan loop hingga sesi selesai alih-alih melepaskannya.

* **`client.beta.sessions.events.tool_runner()`:** menjalankan panggilan alat untuk satu sesi, dengan ID sesi dan daftar alat. Gunakan ketika Anda sudah mengklaim pekerjaan dan hanya memerlukan lapisan eksekusi.

Gunakan work poller secara langsung ketika Anda ingin meluncurkan proses per sesi Anda sendiri, misalnya menjalankan sandbox untuk setiap sesi yang diklaim:

<CodeGroup>
  ```bash cURL
  # Work poller adalah helper SDK (Python, TypeScript, Go), bukan endpoint
  # mentah. Dari shell, gunakan `ant beta:worker poll --on-work` sebagai gantinya;
  # lihat tab Always-on (ant CLI).
  ```

  ```bash CLI
  # Work poller adalah helper SDK (Python, TypeScript, Go), bukan
  # endpoint mentah. Dari shell, gunakan `ant beta:worker poll --on-work`;
  # lihat tab Always-on (ant CLI).
  ```

  ```python Python
  import asyncio
  import os

  from anthropic import AsyncAnthropic
  from anthropic.types.beta.environments import BetaSelfHostedWork


  async def launch_container(work: BetaSelfHostedWork) -> None:
      # Ganti dengan peluncur sandbox per-sesi Anda sendiri. Teruskan
      # ANTHROPIC_ENVIRONMENT_KEY ke dalam sandbox yang diluncurkan, jangan pernah
      # kunci API Anda.
      print(f"claimed session {work.data.id}")


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
  import Anthropic from "@anthropic-ai/sdk";
  import { WorkPoller } from "@anthropic-ai/sdk/helpers/beta/environments";
  import type { BetaSelfHostedWork } from "@anthropic-ai/sdk/resources/beta/environments";

  const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
  const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
  const client = new Anthropic({ authToken: environmentKey });

  async function launchContainer(work: BetaSelfHostedWork): Promise<void> {
    // Ganti dengan peluncur sandbox per-sesi Anda sendiri. Teruskan
    // ANTHROPIC_ENVIRONMENT_KEY ke dalam sandbox yang diluncurkan, jangan pernah
    // kunci API Anda.
    console.log(`claimed session ${work.data.id}`);
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

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/lib/environments"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  func launchContainer(work *anthropic.BetaSelfHostedWork) {
  	// Ganti dengan peluncur sandbox per-sesi Anda sendiri. Poller Go
  	// memanggil work.Stop saat fungsi ini kembali (tidak ada opsi
  	// untuk menonaktifkan auto-stop), jadi blokir di sini sampai sesi
  	// selesai alih-alih melepaskannya seperti pada tab Python dan TypeScript.
  	fmt.Printf("claimed session %s\n", work.Data.ID)
  }

  func main() {
  	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")
  	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")

  	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

  	ctx := context.Background()

  	poller := environments.NewWorkPoller(ctx, client, environments.WorkPollerOptions{
  		EnvironmentID:  environmentID,
  		EnvironmentKey: environmentKey,
  	})
  	defer poller.Close()

  	for work, err := range poller.All() {
  		if err != nil {
  			log.Fatal(err)
  		}
  		launchContainer(work)
  	}
  }
  ```

  ```java Java
  // Helper untuk polling pekerjaan saat ini belum tersedia di Java SDK.
  // Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```

  ```php PHP
  // Helper untuk polling pekerjaan saat ini belum tersedia di SDK PHP.
  // Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```

  ```ruby Ruby
  # Helper untuk polling pekerjaan saat ini belum tersedia di Ruby SDK.
  # Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```
</CodeGroup>

**`AgentToolContext`** adalah konteks eksekusi untuk panggilan alat. Ia mendefinisikan direktori kerja dan kebijakan path, serta dapat mengunduh skill milik sesi. **`beta_agent_toolset_20260401(env)`** menerima `AgentToolContext` dan mengembalikan implementasi alat standar (`bash`, `read`, `write`, `edit`, `glob`, `grep`).

**Dengan `EnvironmentWorker`:** keduanya dikelola secara otomatis. Berikan factory `tools` untuk menyesuaikan daftar alat:

```python Python
EnvironmentWorker(client, ..., tools=lambda env: [beta_bash_tool(env), my_custom_tool])
```

**Dengan `work.poller()` dan `tool_runner()`:** berikan daftar alat sebagai `tools` ke `client.beta.sessions.events.tool_runner()`. Untuk membangun daftar tersebut, siapkan `AgentToolContext` sendiri dan panggil `beta_agent_toolset_20260401(env)`:

<CodeGroup>
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

  ```csharp C#
  // AgentToolContext saat ini belum tersedia di SDK C#.
  ```

  ```go Go
  env := &agenttoolset.AgentToolContext{Workdir: "/workspace"}
  if err := env.SetupSkills(ctx, client, work.Data.ID); err != nil {
  	panic(err)
  }
  // skills diunduh ke /workspace/skills/<name>/
  tools := agenttoolset.BetaAgentToolset20260401(env)
  ```

  ```java Java
  // AgentToolContext saat ini belum tersedia di Java SDK.
  ```

  ```php PHP
  // AgentToolContext saat ini belum tersedia di SDK PHP.
  ```

  ```ruby Ruby
  # AgentToolContext saat ini belum tersedia di SDK Ruby.
  ```
</CodeGroup>

### Verifikasi bahwa worker terhubung

Dari shell terpisah, dengan `ANTHROPIC_API_KEY` diatur ke kunci API Claude Anda (bukan kunci lingkungan), pastikan `workers_polling` setidaknya bernilai 1:

```bash
ant beta:environments:work stats --environment-id "$ANTHROPIC_ENVIRONMENT_ID"
```

Jika `workers_polling` tetap 0, worker tidak menjangkau antrean: pastikan `ANTHROPIC_ENVIRONMENT_KEY` dan `ANTHROPIC_ENVIRONMENT_ID` telah diatur pada host worker. Lihat [Membaca kedalaman antrean](#read-queue-depth) untuk respons statistik lengkap dan contoh bahasa lainnya.

## Memulai sesi

Setelah worker Anda berjalan, buat sesi yang menargetkan lingkungan tersebut. Atur `AGENT_ID` ke ID agen yang Anda catat di [Sebelum Anda mulai](#before-you-begin). Sesi masuk ke antrean kerja lingkungan dan menunggu di sana hingga worker mengklaimnya; jika tidak ada worker yang terhubung, sesi tetap berada dalam antrean alih-alih gagal.

Anthropic tidak memasang file atau repositori GitHub ke dalam sandbox yang di-hosting sendiri. Untuk membuat file spesifik sesi tersedia, berikan referensi file (seperti path S3 atau SHA commit) di field `metadata` sesi. Skrip spawn atau handler `--on-work` Anda membaca metadata tersebut dari item kerja yang diklaim (poller CLI menyalurkan JSON item kerja ke stdin skrip, dan handler SDK dapat membacanya melalui [endpoint Environments Work](/docs/id/api/beta/environments/work)) dan menyiapkan file ke direktori kerja sebelum eksekusi alat dimulai.

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

<Note>
  [Memory](/docs/id/managed-agents/memory) saat ini tidak didukung dengan sandbox yang di-hosting sendiri.
</Note>

Lihat [Self-hosted worker](/docs/id/managed-agents/reference#self-hosted-worker) di referensi untuk daftar lengkap flag CLI, dan [SDK helpers](#sdk-helpers) untuk opsi helper SDK.

## Pemantauan dan operasi

Panggilan-panggilan ini dijalankan dari perangkat pemantauan atau operasi Anda, diautentikasi dengan kunci API Claude Anda, untuk mengamati dan mengelola armada worker. Loop klaim dan keep-alive ditangani di dalam helper worker, sehingga Anda tidak memanggil endpoint tersebut secara langsung.

<Warning>
  Endpoint ini mengautentikasi dengan kunci API organisasi Anda, bukan kunci lingkungan. Panggil endpoint ini dari luar host worker. Mengatur `ANTHROPIC_API_KEY` pada host worker akan mengekspos kredensial berlingkup organisasi ke panggilan alat agen.
</Warning>

### Membaca kedalaman antrean

`work.stats` mengembalikan status antrean untuk sebuah lingkungan:

* `depth` adalah jumlah item yang menunggu untuk diklaim. Skalakan armada worker Anda atau buat peringatan berdasarkan backlog menggunakan nilai ini.
* `pending` adalah jumlah item yang telah diklaim oleh worker dan sedang diproses.
* `oldest_queued_at` adalah timestamp item tertua yang masih dalam antrean atau sedang diproses, atau `null` jika tidak ada.
* `workers_polling` adalah jumlah worker yang telah melakukan polling dalam 30 detik terakhir. Gunakan ini untuk peringatan liveness.

<CodeGroup>
  ```bash cURL
  curl -sS "https://api.anthropic.com/v1/environments/$ANTHROPIC_ENVIRONMENT_ID/work/stats" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:environments:work stats --environment-id "$ANTHROPIC_ENVIRONMENT_ID"
  ```

  ```python Python
  import os

  import anthropic

  client = anthropic.Anthropic()

  stats = client.beta.environments.work.stats(os.environ["ANTHROPIC_ENVIRONMENT_ID"])
  print(f"depth={stats.depth} pending={stats.pending}")
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const stats = await client.beta.environments.work.stats(process.env.ANTHROPIC_ENVIRONMENT_ID!);

  console.log(`depth=${stats.depth} pending=${stats.pending}`);
  ```

  ```csharp C#
  using Anthropic;

  var client = new AnthropicClient();

  var environmentId = Environment.GetEnvironmentVariable("ANTHROPIC_ENVIRONMENT_ID")!;

  var stats = await client.Beta.Environments.Work.Stats(environmentId);

  Console.WriteLine($"depth={stats.Depth} pending={stats.Pending}");
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	client := anthropic.NewClient()
  	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

  	stats, err := client.Beta.Environments.Work.Stats(
  		context.Background(),
  		environmentID,
  		anthropic.BetaEnvironmentWorkStatsParams{},
  	)
  	if err != nil {
  		panic(err)
  	}

  	fmt.Printf("depth=%d pending=%d\n", stats.Depth, stats.Pending)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.beta.environments.work.BetaSelfHostedWorkQueueStats;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaSelfHostedWorkQueueStats stats = client.beta()
          .environments()
          .work()
          .stats(System.getenv("ANTHROPIC_ENVIRONMENT_ID"));

      IO.println("depth=" + stats.depth() + " pending=" + stats.pending());
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Client;

  $client = new Client();

  $stats = $client->beta->environments->work->stats(getenv('ANTHROPIC_ENVIRONMENT_ID'));

  printf("depth=%d pending=%d\n", $stats->depth, $stats->pending);
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  stats = client.beta.environments.work.stats(ENV.fetch("ANTHROPIC_ENVIRONMENT_ID"))

  puts "depth=#{stats.depth} pending=#{stats.pending}"
  ```
</CodeGroup>

```text wrap
{
  "type": "work_queue_stats",
  "depth": 0,
  "pending": 0,
  "oldest_queued_at": null,
  "workers_polling": 0
}
```

### Menghentikan sesi dengan baik

Gunakan `work.stop` untuk meminta worker yang menangani sesi tertentu agar mematikannya dengan bersih. Worker menyelesaikan panggilan alat yang sedang berjalan, mengirimkan status akhir, dan melepaskan sesi. Berikan `force: true` di body permintaan (dengan CLI, berikan `--force`) untuk menginterupsi segera alih-alih menunggu panggilan alat saat ini selesai.

Karena panggilan ini dijalankan dari perangkat operasi Anda dan bukan dari host worker, `ANTHROPIC_WORK_ID` tidak diatur secara otomatis. Atur variabel ini ke ID item kerja target sebelum menjalankan contoh berikut. Untuk menemukan ID item kerja, daftarkan item kerja lingkungan melalui [endpoint Environments Work](/docs/id/api/beta/environments/work).

<CodeGroup>
  ```bash cURL
  curl -sS "https://api.anthropic.com/v1/environments/$ANTHROPIC_ENVIRONMENT_ID/work/$ANTHROPIC_WORK_ID/stop" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{}'
  ```

  ```bash CLI
  ant beta:environments:work stop \
    --environment-id "$ANTHROPIC_ENVIRONMENT_ID" \
    --work-id "$ANTHROPIC_WORK_ID"
  ```

  ```python Python
  import os

  import anthropic

  client = anthropic.Anthropic()

  work = client.beta.environments.work.stop(
      os.environ["ANTHROPIC_WORK_ID"],
      environment_id=os.environ["ANTHROPIC_ENVIRONMENT_ID"],
  )
  print(work.state)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const work = await client.beta.environments.work.stop(process.env.ANTHROPIC_WORK_ID!, {
    environment_id: process.env.ANTHROPIC_ENVIRONMENT_ID!
  });

  console.log(work.state);
  ```

  ```csharp C#
  using Anthropic;

  var client = new AnthropicClient();

  var work = await client.Beta.Environments.Work.Stop(
      Environment.GetEnvironmentVariable("ANTHROPIC_WORK_ID")!,
      new()
      {
          EnvironmentID = Environment.GetEnvironmentVariable("ANTHROPIC_ENVIRONMENT_ID")!
      }
  );

  Console.WriteLine(work.State);
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	client := anthropic.NewClient()

  	work, err := client.Beta.Environments.Work.Stop(
  		context.Background(),
  		os.Getenv("ANTHROPIC_WORK_ID"),
  		anthropic.BetaEnvironmentWorkStopParams{
  			EnvironmentID: os.Getenv("ANTHROPIC_ENVIRONMENT_ID"),
  		},
  	)
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(work.State)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.beta.environments.work.BetaSelfHostedWork;
  import com.anthropic.models.beta.environments.work.BetaSelfHostedWorkStopRequest;
  import com.anthropic.models.beta.environments.work.WorkStopParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaSelfHostedWork work = client.beta().environments().work().stop(
          WorkStopParams.builder()
              .environmentId(System.getenv("ANTHROPIC_ENVIRONMENT_ID"))
              .workId(System.getenv("ANTHROPIC_WORK_ID"))
              .betaSelfHostedWorkStopRequest(BetaSelfHostedWorkStopRequest.builder().build())
              .build()
      );

      IO.println(work.state());
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Client;

  $client = new Client();

  $work = $client->beta->environments->work->stop(
      getenv('ANTHROPIC_WORK_ID'),
      environmentID: getenv('ANTHROPIC_ENVIRONMENT_ID'),
  );

  echo $work->state . "\n";
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  work = client.beta.environments.work.stop(
    ENV.fetch("ANTHROPIC_WORK_ID"),
    environment_id: ENV.fetch("ANTHROPIC_ENVIRONMENT_ID")
  )

  puts work.state
  ```
</CodeGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Model keamanan" icon="lock" href="/docs/id/managed-agents/self-hosted-sandboxes-security">
    Model tanggung jawab bersama untuk lingkungan sandbox yang di-hosting sendiri.
  </Card>

  <Card title="Memulai sesi" icon="settings" href="/docs/id/managed-agents/sessions">
    Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.
  </Card>

  <Card title="MCP tunnels" icon="bolt" href="/docs/id/agents-and-tools/mcp-tunnels/overview">
    Hubungkan Claude secara aman ke server MCP yang berjalan di jaringan privat Anda tanpa membuka port masuk atau mengekspos layanan ke internet publik.
  </Card>
</CardGroup>
