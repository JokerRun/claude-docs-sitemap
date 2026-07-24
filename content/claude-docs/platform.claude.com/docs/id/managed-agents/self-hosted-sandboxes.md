---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: e590627c08166840cf5258147486c5905081bb13339ba529d1a43005e2bd0f02
---

# Sandbox yang di-hosting sendiri

Jalankan sesi Claude Managed Agents di sandbox yang di-hosting sendiri, menjaga eksekusi alat, file, dan egress jaringan di infrastruktur Anda sendiri.

---

Secara default, Managed Agents mengeksekusi alat dan kode di dalam [sandbox cloud yang dikelola Anthropic](/docs/id/managed-agents/cloud-sandboxes-reference). Sandbox yang di-hosting sendiri (self-hosted sandboxes) menjaga orkestrasi di sisi Anthropic tetapi memindahkan eksekusi alat ke infrastruktur yang Anda kendalikan, sehingga kode agen, filesystem, dan egress jaringan tidak pernah meninggalkan lingkungan Anda.

Eksekusi alat tetap berada di host Anda: filesystem yang dibaca dan ditulis oleh agen, proses yang dijalankannya, dan jaringan yang dapat dijangkaunya semuanya berada di bawah kendali Anda. Input dan output alat tetap mengalir ke control plane Anthropic (tempat Claude berjalan) sehingga model dapat melihat hasil dan menentukan apa yang harus dilakukan selanjutnya. Lihat [model keamanan](/docs/id/managed-agents/self-hosted-sandboxes-security) untuk batas aliran data lengkap.

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

Self-hosting cocok ketika agen perlu beroperasi pada data yang tidak boleh meninggalkan batas jaringan Anda, menjangkau layanan internal yang tidak dapat dirutekan secara publik, atau berjalan di bawah kontrol kepatuhan dan audit organisasi Anda sendiri.

Untuk kelayakan Zero Data Retention dan HIPAA BAA, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

## Kapan menggabungkan dengan tunnel MCP

Self-hosting mengontrol *di mana kode agen dieksekusi*. [Tunnel MCP](/docs/id/agents-and-tools/mcp-tunnels/overview) mengontrol *bagaimana Anthropic menjangkau server MCP di jaringan Anda*. Keduanya independen: sesi yang berjalan di sandbox cloud Anthropic masih dapat menjangkau server MCP privat melalui tunnel, dan sesi yang di-hosting sendiri dapat menggunakan server MCP yang di-tunnel maupun yang publik. Gunakan keduanya ketika Anda ingin eksekusi dan akses alat tetap berada di dalam batas Anda. Untuk memberikan agen alat dari server MCP di dalam jaringan Anda tanpa menjalankan tunnel, Anda juga dapat [membungkus server sebagai alat kustom](#wrap-an-mcp-server-as-custom-tools) yang dilayani oleh worker Anda.

## Environment worker

<Tip>
  Panduan ini menjelaskan cara membangun worker dengan platform sandboxing generik apa pun. Panduan tambahan yang spesifik untuk platform tersedia untuk [AWS Lambda MicroVMs](https://docs.aws.amazon.com/lambda/latest/dg/microvms-integrations-claude-managed-agents.html), [Blaxel](https://docs.blaxel.ai/Tutorials/Claude-Managed-Agents), [Cloudflare](https://developers.cloudflare.com/sandbox/claude-managed-agents/), [Daytona](https://www.daytona.io/docs/en/guides/claude/claude-managed-agents), [E2B](https://e2b.dev/docs/agents/claude-managed-agents), [GKE Agent Sandbox](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/tree/main/ai-ml/anthropic-agent-sandbox), [Modal](https://github.com/modal-labs/claude-managed-agents-modal-sandbox), [Namespace](https://namespace.so/docs/integrations/claude), [Superserve](https://docs.superserve.ai/integrations/managed-agents/claude-managed-agents), dan [Vercel](https://vercel.com/kb/guide/run-claude-managed-agent-tools-with-vercel-sandbox).
</Tip>

Environment worker adalah proses yang Anda jalankan di infrastruktur Anda sendiri. Worker ini menerima permintaan eksekusi alat dari Anthropic dan menjalankannya secara lokal. Lingkungan `self_hosted` bertindak sebagai antrean kerja: ketika sebuah [sesi](/docs/id/managed-agents/sessions) ditugaskan padanya, Anthropic memasukkan sesi tersebut ke antrean sebagai work item. Worker Anda mengklaim work item dari antrean tersebut, membuat konteks eksekusi untuk masing-masing, mengunduh [skills](/docs/id/managed-agents/skills) agen (sumber daya berbasis filesystem yang dapat digunakan kembali yang memberikan agen keahlian spesifik domain), menjalankan panggilan alat, dan mengirimkan hasilnya kembali.

Work item diklaim dengan melakukan polling pada antrean lingkungan: baik oleh **worker always-on** yang melakukan polling secara terus-menerus, atau **handler yang dipicu webhook** yang bangun saat `session.status_run_started` dan mulai melakukan polling.

CLI dan SDK keduanya menyertakan worker yang sudah jadi. CLI `ant` hanya mendukung pola always-on; SDK mendukung baik always-on maupun yang dipicu webhook. Keduanya dapat dikonfigurasi: lihat [Self-hosted worker](/docs/id/managed-agents/reference#self-hosted-worker) di referensi untuk flag CLI, dan [SDK helpers](#sdk-helpers) di halaman ini untuk opsi SDK. Untuk kontrol lebih, panggil [endpoint Environments Work](/docs/id/api/beta/environments/work) secara langsung dan implementasikan worker Anda sendiri.

### Filesystem sandbox

* **`/workspace`:** direktori kerja default sistem untuk eksekusi alat dan pengunduhan skill. Flag `--workdir` pada CLI secara default menggunakan direktori saat ini; berikan `--workdir /workspace` agar sesuai dengan default sistem. Skill diunduh ke `<workdir>/skills/<name>/`. Jika Anda menggunakan direktori kerja yang berbeda, perbarui prompt sistem agen Anda agar Claude dapat menemukan file skill.
* **Output:** pada lingkungan yang di-hosting sendiri, prompt sistem sesi menghilangkan instruksi `/mnt/session/outputs` yang digunakan pada sandbox yang dikelola Anthropic, sehingga hasil akhir berada di mana pun agen menulisnya di filesystem sandbox Anda, biasanya di bawah direktori kerja.

## Sebelum Anda mulai

Anda memerlukan:

* **Agen yang sudah ada.** Jika Anda belum memilikinya, selesaikan [Quickstart](/docs/id/managed-agents/quickstart) terlebih dahulu dan catat ID agennya.
* **Host Linux** dengan `/bin/bash` di path yang persis tersebut. Alat bash worker memanggilnya secara langsung, tanpa memeriksa `PATH`. SDK TypeScript juga memerlukan `unzip` dan `tar` pada `PATH` serta Node.js 22 atau yang lebih baru; SDK Python dan Go menggunakan pustaka standar mereka untuk ekstraksi arsip dan tidak memiliki persyaratan biner tambahan.
* **CLI `ant` atau SDK Anthropic** (Python, TypeScript, atau Go) di host worker.
* **Dua kredensial:** environment key (dibuat di Console pada langkah-langkah berikut) mengautentikasi worker ke antreannya; kunci API Claude Anda membuat sesi dan membaca statistik antrean dari luar host worker. Pembuatan kunci hanya dapat dilakukan melalui Console.

<Note>
  Pada [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), worker mengautentikasi dengan AWS IAM (SigV4) atau [kunci API yang dibuat di AWS Console](/docs/id/build-with-claude/claude-platform-on-aws#api-key-authentication), bukan environment key. Lampirkan managed policy [`AnthropicSelfHostedEnvironmentAccess`](/docs/id/api/claude-platform-on-aws-iam-actions#managed-policies) ke principal IAM tempat worker Anda berjalan. Environment key yang dibuat di Claude Console tidak berfungsi dengan endpoint Claude Platform on AWS.
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

  <Step title="Buat environment key">
    Di Console, buka lingkungan dan klik **Generate environment key**. Pembuatan kunci hanya dapat dilakukan melalui Console, terlepas dari apakah Anda membuat lingkungan melalui Console atau API. Kemudian ekspor ID lingkungan dan kunci di host worker:

    ```bash
    export ANTHROPIC_ENVIRONMENT_KEY="sk-ant-oat01-..."
    export ANTHROPIC_ENVIRONMENT_ID="env_..."
    ```
  </Step>
</Steps>

<Note>
  Skill dapat menyertakan executable yang dapat dijalankan langsung oleh agen. Worker CLI dan SDK mempertahankan izin executable yang tercatat dalam bundel skill saat mengekstraknya. Jika Anda mengimplementasikan pengunduhan skill secara manual, Anda bertanggung jawab untuk mengatur izin executable.
</Note>

## Menjalankan worker

Pilih **always-on** untuk pengaturan paling sederhana: proses yang berjalan lama melakukan polling antrean secara terus-menerus dan hanya memerlukan HTTPS keluar. Pilih **webhook-triggered** untuk menghindari menjalankan poller yang menganggur; ini memerlukan endpoint webhook yang dapat dijangkau Anthropic (lihat [Webhooks](/docs/id/managed-agents/webhooks) untuk pengaturan endpoint dan verifikasi tanda tangan).

<Tabs>
  <Tab title="Always-on (ant CLI)">
    <Steps>
      <Step title="Instal CLI ant">
        Jalankan ini di host worker.

        <Tabs>
          <Tab title="curl (Linux/WSL)">
            Untuk lingkungan Linux, unduh binary rilis secara langsung.

            ```bash
            VERSION=1.19.0
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

        `ant beta:worker poll` mengklaim work item yang ditugaskan ke lingkungan, mengunduh skill, mengeksekusi panggilan alat di direktori kerja, dan mengirimkan hasilnya kembali. Perintah ini membaca `ANTHROPIC_ENVIRONMENT_KEY` dan `ANTHROPIC_ENVIRONMENT_ID` dari environment.

        ```bash
        ant beta:worker poll \
          --workdir "/workspace"
        ```

        Worker keluar dengan bersih pada SIGTERM atau SIGINT: worker membatalkan panggilan alat yang sedang berjalan, mengirimkan hasil errornya, dan melepaskan work item sebelum berhenti.

        **Sandbox per sesi**

        Jika Anda memerlukan isolasi yang lebih kuat (filesystem baru, batas sumber daya, atau kontrol jaringan per sesi), jalankan setiap sesi di sandbox-nya sendiri. Bangun image dengan `ant` terinstal dan `ant beta:worker run` sebagai entrypoint. Image dasar harus menyediakan `/bin/bash`; `curl` hanya digunakan saat build. Ketika sandbox dimulai, ia membaca detail sesi dari variabel environment, menangani sesi tersebut, dan keluar:

        ```text
        FROM your-base-image
        ARG ANT_VERSION=1.19.0
        ARG TARGETARCH
        RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo arm64 || echo amd64) && \
            curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${ANT_VERSION}/ant_${ANT_VERSION}_linux_${ARCH}.tar.gz" \
              | tar -xz -C /usr/local/bin ant
        WORKDIR /workspace
        VOLUME /workspace
        ENTRYPOINT ["ant", "beta:worker", "run"]
        ```

        Kemudian tulis skrip spawn yang meneruskan detail sesi ke sandbox baru. Poller menyuntikkan `ANTHROPIC_SESSION_ID`, `ANTHROPIC_WORK_ID`, `ANTHROPIC_ENVIRONMENT_ID`, dan `ANTHROPIC_ENVIRONMENT_KEY` ke dalam environment skrip. `ANTHROPIC_BASE_URL` bersifat opsional dan hanya diteruskan jika diatur di host poller; variabel ini menimpa endpoint API default. Dalam contoh, `/host/outputs` adalah direktori host yang Anda pilih; direktori ini di-bind-mount ke direktori kerja sandbox (`/workspace`) sehingga Anda dapat mengambil hasil sesi setelah sandbox keluar. Pada lingkungan yang di-hosting sendiri, agen menulis hasil di bawah direktori kerja alih-alih `/mnt/session/outputs` (lihat [Filesystem sandbox](#sandbox-filesystem)), sehingga memasang direktori kerja adalah cara untuk menangkapnya; mount tersebut juga mengambil pohon `skills/` yang diunduh dan file perantara apa pun yang dibuat agen.

        ```bash
        #!/bin/bash
        # spawn.sh: dipanggil sekali untuk setiap item pekerjaan yang diklaim
        mkdir -p "/host/outputs/$ANTHROPIC_SESSION_ID"
        exec docker run --rm \
          -e ANTHROPIC_SESSION_ID -e ANTHROPIC_ENVIRONMENT_KEY \
          -e ANTHROPIC_WORK_ID -e ANTHROPIC_ENVIRONMENT_ID -e ANTHROPIC_BASE_URL \
          -v "/host/outputs/$ANTHROPIC_SESSION_ID":/workspace \
          your-image
        ```

        Mulai poller yang menunjuk ke skrip:

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
        `EnvironmentWorker` mengklaim work item yang ditugaskan ke lingkungan, mengunduh skill, mengeksekusi panggilan alat di direktori kerja, dan mengirimkan hasilnya kembali. Autentikasi dengan environment key yang Anda buat di [Sebelum Anda mulai](#before-you-begin).

        <CodeGroup exclude="shell">
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

  <Tab title="Webhook-triggered (SDK)">
    <Steps>
      <Step title="Berlangganan webhook sesi">
        Di [Console](https://platform.claude.com/settings/workspaces/default/webhooks), definisikan endpoint webhook yang mendengarkan event `session.status_run_started`. Lihat [Webhooks](/docs/id/managed-agents/webhooks) untuk detailnya.
      </Step>

      <Step title="Ekspor kunci penandatanganan webhook">
        Selain ID lingkungan dan kunci dari [Sebelum Anda mulai](#before-you-begin), ekspor kunci penandatanganan webhook di host handler Anda sehingga handler dapat memverifikasi payload yang masuk. Verifikasi tanda tangan di handler Python memerlukan extra webhooks: `pip install "anthropic[webhooks]"`.

        ```bash
        export ANTHROPIC_WEBHOOK_SIGNING_KEY="whsec_..."
        ```
      </Step>

      <Step title="Implementasikan handler webhook">
        `EnvironmentWorker` mengklaim work item, mengunduh skill, mengeksekusi panggilan alat di direktori kerja, mengirimkan hasilnya kembali, dan keluar. Panggil saat `session.status_run_started` terpicu.

        <CodeGroup exclude="shell">
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

* **`EnvironmentWorker`:** worker siap pakai. Menangani polling, pengaturan, dan eksekusi dari awal hingga akhir.

  * `.run()`: berjalan tanpa batas, mengambil sesi saat tiba.
  * `.handle_item()`: menangani satu work item yang diklaim dan keluar. Berikan pengidentifikasi work, sesi, dan lingkungan secara eksplisit, atau biarkan ia membaca variabel `ANTHROPIC_*` yang diatur oleh `ant beta:worker poll --on-work` untuk proses yang dijalankannya.

* **`work.poller()`:** melakukan polling antrean kerja atas nama Anda dan memberikan setiap sesi yang diklaim. Gunakan ini ketika Anda ingin memutuskan apa yang terjadi untuk setiap sesi, misalnya meluncurkan sandbox alih-alih menjalankan alat secara in-process.

  * `drain`: apakah berhenti melakukan polling setelah antrean kosong alih-alih menunggu pekerjaan baru.
  * `block_ms`: berapa lama menunggu pekerjaan tiba sebelum kembali, dalam milidetik. Harus antara 1 dan 999 (waktu tunggu per polling; helper melakukan polling ulang secara otomatis). Berikan `null` (`None` di Python, `param.Null[int64]()` di Go) untuk pemeriksaan non-blocking; menghilangkan parameter menggunakan long-poll default 999 ms.
  * `reclaim_older_than_ms`: mengklaim ulang work item yang telah diklaim tetapi tidak pernah di-acknowledge dalam jumlah milidetik ini.
  * `auto_stop`: apakah mengirimkan sinyal stop untuk setiap work item setelah badan loop Anda selesai dengannya. Poller Go tidak memiliki opsi untuk menonaktifkan dan selalu mengirimkan sinyal stop, jadi blokir di badan loop hingga sesi selesai alih-alih melepaskannya.

* **`client.beta.sessions.events.tool_runner()`:** menjalankan panggilan alat untuk satu sesi, dengan ID sesi dan daftar alat. Gunakan ketika Anda sudah mengklaim pekerjaan dan hanya memerlukan lapisan eksekusi.

Gunakan work poller secara langsung ketika Anda ingin meluncurkan proses per sesi Anda sendiri, misalnya menjalankan sandbox untuk setiap sesi yang diklaim:

<CodeGroup>
  ```bash cURL
  # Work poller adalah helper SDK (Python, TypeScript, Go), bukan endpoint
  # mentah. Dari shell, gunakan `ant beta:worker poll --on-work` sebagai gantinya;
  # lihat tab Always-on (ant CLI).
  ```

  ```bash CLI
  # Work poller adalah helper SDK (Python, TypeScript, Go), bukan endpoint
  # mentah. Dari shell, gunakan `ant beta:worker poll --on-work` sebagai gantinya;
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
    // ANTHROPIC_ENVIRONMENT_KEY ke dalam sandbox yang diluncurkan,
    // jangan pernah kunci API Anda.
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
  	// memanggil work.Stop saat fungsi ini kembali (tidak ada opsi untuk
  	// menonaktifkan auto-stop), jadi blokir di sini hingga sesi selesai
  	// alih-alih melepaskannya seperti pada tab Python dan TypeScript.
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

**`AgentToolContext`** adalah konteks eksekusi untuk panggilan alat. Ia mendefinisikan direktori kerja dan kebijakan path, dan dapat mengunduh skill sesi. **`beta_agent_toolset_20260401(env)`** menerima `AgentToolContext` dan mengembalikan implementasi alat standar (`bash`, `read`, `write`, `edit`, `glob`, `grep`).

**Dengan `EnvironmentWorker`:** keduanya dikelola secara otomatis. Berikan factory `tools` untuk menyesuaikan daftar alat:

<CodeGroup exclude="shell">
  ```python Python
  EnvironmentWorker(client, ..., tools=lambda env: [beta_bash_tool(env), my_custom_tool])
  ```

  ```typescript TypeScript
  new EnvironmentWorker({
    client,
    environmentId,
    environmentKey,
    tools: (ctx) => [betaBashTool(ctx), myCustomTool]
  });
  ```

  ```csharp C#
  // EnvironmentWorker saat ini belum tersedia di SDK C#.
  // Untuk menjawab panggilan alat kustom secara langsung, lihat stream peristiwa sesi.
  ```

  ```go Go
  worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  	EnvironmentID:  environmentID,
  	EnvironmentKey: environmentKey,
  	ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
  		return []anthropic.BetaTool{agenttoolset.BetaBashTool(env), myCustomTool}
  	},
  })
  ```

  ```java Java
  // EnvironmentWorker saat ini belum tersedia di Java SDK.
  // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
  ```

  ```php PHP
  // EnvironmentWorker saat ini belum tersedia di SDK PHP.
  // Untuk menjawab panggilan alat kustom secara langsung, lihat stream peristiwa sesi.
  ```

  ```ruby Ruby
  # EnvironmentWorker saat ini belum tersedia di SDK Ruby.
  # Untuk menjawab panggilan alat kustom secara langsung, lihat stream peristiwa sesi.
  ```
</CodeGroup>

**Dengan `work.poller()` dan `tool_runner()`:** berikan daftar alat sebagai `tools` ke `client.beta.sessions.events.tool_runner()`. Untuk membangun daftar tersebut, siapkan `AgentToolContext` sendiri dan panggil `beta_agent_toolset_20260401(env)`:

<CodeGroup exclude="shell">
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

### Verifikasi worker terhubung

Dari shell terpisah, dengan `ANTHROPIC_API_KEY` diatur ke kunci API Claude Anda (bukan environment key), konfirmasikan bahwa `workers_polling` setidaknya 1:

```bash
ant beta:environments:work stats --environment-id "$ANTHROPIC_ENVIRONMENT_ID"
```

Jika `workers_polling` tetap di 0, worker tidak menjangkau antrean: konfirmasikan bahwa `ANTHROPIC_ENVIRONMENT_KEY` dan `ANTHROPIC_ENVIRONMENT_ID` diatur di host worker. Lihat [Membaca kedalaman antrean](#read-queue-depth) untuk respons statistik lengkap dan contoh bahasa lainnya.

## Memulai sesi

Setelah worker Anda berjalan, buat sesi yang menargetkan lingkungan tersebut. Atur `AGENT_ID` ke ID agen yang Anda catat di [Sebelum Anda mulai](#before-you-begin). Sesi masuk ke antrean kerja lingkungan dan menunggu di sana hingga worker mengklaimnya; jika tidak ada worker yang terhubung, sesi tetap dalam antrean alih-alih gagal.

Anthropic tidak memasang file atau repositori GitHub ke dalam sandbox yang di-hosting sendiri. Untuk membuat file spesifik sesi tersedia, berikan referensi file (seperti path S3 atau SHA commit) di field `metadata` sesi. Work item yang diklaim tidak membawa metadata sesi, tetapi membawa ID sesi: skrip spawn atau handler `--on-work` Anda mengambil sesi (`GET /v1/sessions/{session_id}`) untuk membaca field `metadata`, kemudian menyiapkan file ke direktori kerja sebelum eksekusi alat dimulai.

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
  Sandbox yang di-hosting sendiri tidak mendukung entri `resources`; sesi yang menyertakan resource apa pun pada lingkungan yang di-hosting sendiri akan ditolak.
</Note>

Lihat [Self-hosted worker](/docs/id/managed-agents/reference#self-hosted-worker) di referensi untuk daftar lengkap flag CLI, dan [SDK helpers](#sdk-helpers) untuk opsi helper SDK.

## Melayani alat kustom dari sandbox Anda

[Alat kustom](/docs/id/managed-agents/tools#custom-tools) adalah alat yang dieksekusi oleh kode Anda sendiri: agen memancarkan event `agent.custom_tool_use` dan menunggu `user.custom_tool_result` yang cocok. Worker dapat menjadi kode tersebut, dan karena berjalan di dalam sandbox Anda, alat tersebut menjangkau layanan internal, kredensial, dan egress jaringan yang Anda konfigurasikan untuk sandbox, dan tidak lebih. Environment key mengotorisasi pengiriman hasil alat kustom, sehingga kunci API Claude Anda tetap tidak berada di host worker.

<Note>
  Melayani alat kustom memerlukan worker SDK: worker CLI `ant` tidak memiliki cara untuk mendaftarkan implementasi alat kustom. Dalam pola sandbox-per-sesi, jalankan `EnvironmentWorker` di dalam sandbox dengan `handle_item()` (`handleItem` di TypeScript, `HandleItem` di Go) sebagai pengganti `ant beta:worker run`.
</Note>

<Steps>
  <Step title="Deklarasikan alat pada agen">
    Tambahkan entri `custom` ke `tools` agen yang `name`-nya cocok dengan alat yang didaftarkan worker Anda. Lihat [Alat kustom](/docs/id/managed-agents/tools#custom-tools) untuk bentuk deklarasi lengkap.

    ```json
    {
      "type": "custom",
      "name": "get_order_status",
      "description": "Look up an order in the internal fulfillment system by order ID.",
      "input_schema": {
        "type": "object",
        "properties": {
          "order_id": { "type": "string", "description": "The order ID" }
        },
        "required": ["order_id"]
      }
    }
    ```
  </Step>

  <Step title="Daftarkan implementasi dengan worker">
    Berikan alat melalui factory `tools` worker (lihat [SDK helpers](#sdk-helpers)), bersama dengan toolset bawaan:

    <CodeGroup exclude="shell">
      ```python Python
      import asyncio
      import os
      from anthropic import AsyncAnthropic, beta_async_tool
      from anthropic.lib.environments import EnvironmentWorker
      from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401


      @beta_async_tool
      async def get_order_status(order_id: str) -> str:
          """Look up an order in the internal fulfillment system by order ID."""
          # Berjalan di host worker: dapat memanggil apa pun yang bisa dijangkau sandbox.
          return f"Order {order_id}: shipped"


      async def main() -> None:
          environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
          environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
          async with AsyncAnthropic(auth_token=environment_key) as client:
              await EnvironmentWorker(
                  client,
                  environment_id=environment_id,
                  environment_key=environment_key,
                  workdir="/workspace",
                  tools=lambda env: [*beta_agent_toolset_20260401(env), get_order_status],
              ).run()


      asyncio.run(main())
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";
      import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";
      import { betaTool } from "@anthropic-ai/sdk/helpers/beta/json-schema";
      import { betaAgentToolset20260401 } from "@anthropic-ai/sdk/tools/agent-toolset/node";

      const getOrderStatus = betaTool({
        name: "get_order_status",
        description: "Look up an order in the internal fulfillment system by order ID.",
        inputSchema: {
          type: "object",
          properties: { order_id: { type: "string", description: "The order ID" } },
          required: ["order_id"]
        },
        // Berjalan di host worker: panggil apa pun yang dapat dijangkau sandbox.
        run: async ({ order_id }) => `Order ${order_id}: shipped`
      });

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
        signal: controller.signal,
        tools: (ctx) => [...betaAgentToolset20260401(ctx), getOrderStatus]
      }).run();
      ```

      ```csharp C#
      // EnvironmentWorker saat ini belum tersedia di SDK C#.
      // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
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
      	"github.com/anthropics/anthropic-sdk-go/toolrunner"
      	"github.com/anthropics/anthropic-sdk-go/tools/agenttoolset"
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
      		// Berjalan di host worker: dapat memanggil apa pun yang bisa dijangkau sandbox.
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
      		Workdir:        "/workspace",
      		ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
      			return append(agenttoolset.BetaAgentToolset20260401(env), getOrderStatus)
      		},
      	})
      	if err := worker.Run(ctx); err != nil {
      		log.Fatalf("worker: %v", err)
      	}
      }

      ```

      ```java Java
      // EnvironmentWorker saat ini belum tersedia di Java SDK.
      // Untuk menjawab panggilan alat kustom secara langsung, lihat stream event sesi.
      ```

      ```php PHP
      // EnvironmentWorker saat ini belum tersedia di SDK PHP.
      // Untuk menjawab panggilan alat kustom secara langsung, lihat stream peristiwa sesi.
      ```

      ```ruby Ruby
      # EnvironmentWorker saat ini belum tersedia di SDK Ruby.
      # Untuk menjawab panggilan alat kustom secara langsung, lihat stream peristiwa sesi.
      ```
    </CodeGroup>
  </Step>
</Steps>

Worker hanya menjawab alat yang terdaftar padanya. Alat kustom yang dideklarasikan pada agen tetapi tidak terdaftar pada worker atau klien mana pun membuat sesi terjeda dengan stop reason `requires_action` hingga sesuatu mengirimkan hasilnya; lihat [Menangani panggilan alat kustom](/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) untuk alur event.

### Membungkus server MCP sebagai alat kustom

[Konektor MCP](/docs/id/managed-agents/mcp-connector) terhubung ke server MCP dari sisi Anthropic, sehingga server harus mengekspos endpoint HTTP yang dapat dijangkau Anthropic, secara langsung atau melalui [tunnel MCP](/docs/id/agents-and-tools/mcp-tunnels/overview). Untuk menggunakan server yang hanya dapat dijangkau oleh jaringan Anda, jadikan worker sebagai klien MCP dan deklarasikan alat server sebagai alat kustom. Server MCP tidak memerlukan konektivitas masuk dari luar jaringan Anda; Anthropic menerima definisi alat yang Anda deklarasikan pada agen, input setiap panggilan, dan hasil yang dikirimkan kembali oleh worker Anda. Saat runtime, model memanggil alat yang dibungkus seperti alat kustom lainnya:

1. Agen memancarkan event `agent.custom_tool_use`.
2. Worker, di dalam sandbox Anda, meneruskan panggilan melalui sesi MCP yang terbuka ke server di jaringan Anda.
3. Worker mengirimkan respons server sebagai `user.custom_tool_result`.

[Helper MCP sisi klien](/docs/id/agents-and-tools/mcp-connector#client-side-mcp-helpers) dari SDK mengonversi alat server menjadi alat yang dapat dijalankan yang diterima worker; instal SDK MCP bersama SDK Anthropic (`pip install "anthropic[mcp]" "mcp>=1.24"`, `npm install @modelcontextprotocol/sdk`, `go get github.com/modelcontextprotocol/go-sdk`). Contoh-contoh terhubung tanpa autentikasi; untuk mengirim kredensial, konfigurasikan klien HTTP atau opsi permintaan yang Anda berikan ke transport MCP (`http_client` di Python, `requestInit` di TypeScript, `HTTPClient` di Go).

<Steps>
  <Step title="Deklarasikan alat server pada agen">
    Daftar alat server MCP dan deklarasikan masing-masing sebagai alat `custom`; `name`, `description`, dan `inputSchema` MCP dipetakan satu-ke-satu ke field alat kustom. Jika server melakukan paginasi pada daftar alatnya, deklarasikan setiap halaman; worker harus mendaftar halaman yang sama.

    <CodeGroup exclude="shell">
      ```python Python
      import asyncio
      from typing import Any, cast
      from anthropic import AsyncAnthropic
      from anthropic.types.beta import BetaManagedAgentsCustomToolParams
      from mcp import ClientSession, types
      # Memerlukan mcp >= 1.24, yang mengganti nama streamablehttp_client menjadi streamable_http_client.
      from mcp.client.streamable_http import streamable_http_client

      MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp"


      def to_custom_tool(tool: types.Tool) -> BetaManagedAgentsCustomToolParams:
          # Field MCP dipetakan satu-ke-satu ke deklarasi alat kustom. Cast ini
          # meneruskan dictionary skema ke parameter bertipe milik SDK tanpa perubahan.
          return {
              "type": "custom",
              "name": tool.name,
              "description": tool.description or tool.name,
              "input_schema": cast(Any, tool.inputSchema),
          }


      async def main() -> None:
          # Jalankan ini di tempat Anda membuat agen, bukan di host worker: skrip ini
          # melakukan autentikasi dengan kunci API Claude Anda (ANTHROPIC_API_KEY).
          async with (
              streamable_http_client(MCP_SERVER_URL) as (read, write, _),
              ClientSession(read, write) as mcp_session,
              AsyncAnthropic() as client,
          ):
              await mcp_session.initialize()
              listed = await mcp_session.list_tools()
              agent = await client.beta.agents.create(
                  name="Internal tools agent",
                  model="claude-opus-4-8",
                  tools=[
                      {"type": "agent_toolset_20260401"},
                      *[to_custom_tool(tool) for tool in listed.tools],
                  ],
              )
              print(agent.id)


      asyncio.run(main())
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";
      import { Client } from "@modelcontextprotocol/sdk/client/index.js";
      import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

      const MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp";

      // Jalankan ini di tempat Anda membuat agen, bukan di host worker: kode ini
      // melakukan autentikasi dengan kunci API Claude Anda (ANTHROPIC_API_KEY).
      const client = new Anthropic();

      const mcpClient = new Client({ name: "declare-agent-tools", version: "1.0.0" });
      await mcpClient.connect(new StreamableHTTPClientTransport(new URL(MCP_SERVER_URL)));
      const { tools } = await mcpClient.listTools();

      const agent = await client.beta.agents.create({
        name: "Internal tools agent",
        model: "claude-opus-4-8",
        tools: [
          { type: "agent_toolset_20260401" },
          // Field MCP dipetakan satu-ke-satu ke deklarasi alat kustom.
          ...tools.map((tool) => ({
            type: "custom" as const,
            name: tool.name,
            description: tool.description || tool.name,
            input_schema: tool.inputSchema
          }))
        ]
      });
      console.log(agent.id);

      await mcpClient.close();
      ```

      ```csharp C#
      // Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      // C# bekerja dengan cara yang sama setelah Anda mendaftar alat server dengan klien MCP.
      ```

      ```go Go
      package main

      import (
      	"context"
      	"encoding/json"
      	"fmt"
      	"log"

      	"github.com/anthropics/anthropic-sdk-go"
      	mcpsdk "github.com/modelcontextprotocol/go-sdk/mcp"
      )

      const mcpServerURL = "http://mcp.internal.example.com:8000/mcp"

      // toCustomTool memetakan satu definisi alat MCP ke sebuah deklarasi alat kustom.
      // Field-field dipetakan satu-ke-satu: parameter bertipe membawa `properties` dan
      // `required`, dan setiap kata kunci JSON Schema lain yang dikeluarkan server dibawa dalam
      // ExtraFields sehingga skema yang dideklarasikan cocok dengan skema server.
      func toCustomTool(tool *mcpsdk.Tool) (anthropic.BetaAgentNewParamsToolUnion, error) {
      	raw, err := json.Marshal(tool.InputSchema)
      	if err != nil {
      		return anthropic.BetaAgentNewParamsToolUnion{}, err
      	}
      	var schema map[string]any
      	if err := json.Unmarshal(raw, &schema); err != nil {
      		return anthropic.BetaAgentNewParamsToolUnion{}, err
      	}

      	inputSchema := anthropic.BetaManagedAgentsCustomToolInputSchemaParam{ExtraFields: map[string]any{}}
      	for keyword, value := range schema {
      		switch keyword {
      		case "type":
      			// Tipe parameter selalu melakukan marshal "type": "object".
      		case "properties":
      			properties, _ := value.(map[string]any)
      			inputSchema.Properties = properties
      		case "required":
      			entries, _ := value.([]any)
      			for _, entry := range entries {
      				if name, isString := entry.(string); isString {
      					inputSchema.Required = append(inputSchema.Required, name)
      				}
      			}
      		default:
      			inputSchema.ExtraFields[keyword] = value
      		}
      	}

      	description := tool.Description
      	if description == "" {
      		description = tool.Name
      	}
      	return anthropic.BetaAgentNewParamsToolUnion{
      		OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
      			Type:        anthropic.BetaManagedAgentsCustomToolParamsTypeCustom,
      			Name:        tool.Name,
      			Description: description,
      			InputSchema: inputSchema,
      		},
      	}, nil
      }

      func main() {
      	ctx := context.Background()

      	// Jalankan ini di tempat Anda membuat agen, bukan di host worker: kode ini
      	// melakukan autentikasi dengan kunci API Claude Anda (ANTHROPIC_API_KEY).
      	client := anthropic.NewClient()

      	mcpClient := mcpsdk.NewClient(&mcpsdk.Implementation{Name: "declare-agent-tools", Version: "1.0.0"}, nil)
      	session, err := mcpClient.Connect(ctx, &mcpsdk.StreamableClientTransport{Endpoint: mcpServerURL}, nil)
      	if err != nil {
      		log.Fatalf("connect to MCP server: %v", err)
      	}
      	defer session.Close()

      	listed, err := session.ListTools(ctx, nil)
      	if err != nil {
      		log.Fatalf("list MCP tools: %v", err)
      	}

      	tools := []anthropic.BetaAgentNewParamsToolUnion{
      		{OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
      			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
      		}},
      	}
      	for _, tool := range listed.Tools {
      		custom, err := toCustomTool(tool)
      		if err != nil {
      			log.Fatalf("convert MCP tool %s: %v", tool.Name, err)
      		}
      		tools = append(tools, custom)
      	}

      	agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
      		Name:  "Internal tools agent",
      		Model: anthropic.BetaManagedAgentsModelConfigParams{ID: "claude-opus-4-8"},
      		Tools: tools,
      	})
      	if err != nil {
      		log.Fatalf("create agent: %v", err)
      	}
      	fmt.Println(agent.ID)
      }

      ```

      ```java Java
      // Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      // Java bekerja dengan cara yang sama setelah Anda mencantumkan alat-alat server dengan klien MCP.
      ```

      ```php PHP
      // Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      // PHP bekerja dengan cara yang sama setelah Anda mencantumkan daftar alat server dengan klien MCP.
      ```

      ```ruby Ruby
      # Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      # Ruby bekerja dengan cara yang sama setelah Anda mencantumkan daftar alat server dengan klien MCP.
      ```
    </CodeGroup>
  </Step>

  <Step title="Layani alat dari worker">
    Hubungkan ke server MCP yang sama saat startup, konversi alatnya dengan helper MCP, dan daftarkan bersama toolset bawaan. Jaga satu sesi MCP tetap terbuka selama masa hidup worker.

    <CodeGroup exclude="shell">
      ```python Python
      import asyncio
      import os
      from datetime import timedelta
      from anthropic import AsyncAnthropic
      from anthropic.lib.environments import EnvironmentWorker
      from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401
      from anthropic.lib.tools.mcp import async_mcp_tool
      from mcp import ClientSession
      # Memerlukan mcp >= 1.24, yang mengganti nama streamablehttp_client menjadi streamable_http_client.
      from mcp.client.streamable_http import streamable_http_client

      MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp"


      async def main() -> None:
          environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
          environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
          # Hubungkan ke server MCP sekali saat startup dan biarkan sesi tetap terbuka selama
          # masa hidup worker. Timeout mengubah panggilan alat yang macet menjadi hasil
          # error alih-alih panggilan yang terhenti.
          async with (
              streamable_http_client(MCP_SERVER_URL) as (read, write, _),
              ClientSession(read, write, read_timeout_seconds=timedelta(seconds=60)) as mcp_session,
              AsyncAnthropic(auth_token=environment_key) as client,
          ):
              await mcp_session.initialize()
              listed = await mcp_session.list_tools()
              mcp_tools = [async_mcp_tool(tool, mcp_session) for tool in listed.tools]
              await EnvironmentWorker(
                  client,
                  environment_id=environment_id,
                  environment_key=environment_key,
                  workdir="/workspace",
                  tools=lambda env: [*beta_agent_toolset_20260401(env), *mcp_tools],
              ).run()


      asyncio.run(main())
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";
      import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";
      import {
        mcpTools,
        type MCPCallToolResultLike,
        type MCPClientLike
      } from "@anthropic-ai/sdk/helpers/beta/mcp";
      import { betaAgentToolset20260401 } from "@anthropic-ai/sdk/tools/agent-toolset/node";
      import { Client } from "@modelcontextprotocol/sdk/client/index.js";
      import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

      const MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp";

      const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
      const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
      const client = new Anthropic({ authToken: environmentKey });
      const controller = new AbortController();
      process.once("SIGTERM", () => controller.abort());

      // Hubungkan ke server MCP sekali saat startup dan pertahankan koneksi tetap terbuka
      // selama worker berjalan.
      const mcpClient = new Client({ name: "sandbox-worker", version: "1.0.0" });
      await mcpClient.connect(new StreamableHTTPClientTransport(new URL(MCP_SERVER_URL)));
      const { tools } = await mcpClient.listTools();

      // Tipe kembalian callTool dari MCP SDK masih menyertakan bentuk hasil lawas yang
      // tidak diterima mcpTools; persempit tipenya. Hapus ini setelah MCPClientLike diperluas.
      const mcpClientForTools: MCPClientLike = {
        callTool: (params) => mcpClient.callTool(params) as Promise<MCPCallToolResultLike>
      };

      await new EnvironmentWorker({
        client,
        environmentId,
        environmentKey,
        workdir: "/workspace",
        signal: controller.signal,
        tools: (ctx) => [...betaAgentToolset20260401(ctx), ...mcpTools(tools, mcpClientForTools)]
      }).run();
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
      	"github.com/anthropics/anthropic-sdk-go/mcp"
      	"github.com/anthropics/anthropic-sdk-go/option"
      	"github.com/anthropics/anthropic-sdk-go/tools/agenttoolset"
      	mcpsdk "github.com/modelcontextprotocol/go-sdk/mcp"
      )

      const mcpServerURL = "http://mcp.internal.example.com:8000/mcp"

      func main() {
      	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
      	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

      	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
      	defer stop()

      	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

      	// Hubungkan ke server MCP sekali saat startup dan biarkan sesi tetap terbuka selama
      	// worker berjalan.
      	mcpClient := mcpsdk.NewClient(&mcpsdk.Implementation{Name: "sandbox-worker", Version: "1.0.0"}, nil)
      	session, err := mcpClient.Connect(ctx, &mcpsdk.StreamableClientTransport{Endpoint: mcpServerURL}, nil)
      	if err != nil {
      		log.Fatalf("connect to MCP server: %v", err)
      	}
      	defer session.Close()

      	listed, err := session.ListTools(ctx, nil)
      	if err != nil {
      		log.Fatalf("list MCP tools: %v", err)
      	}
      	mcpTools, err := mcp.NewBetaTools(listed.Tools, session)
      	if err != nil {
      		log.Fatalf("convert MCP tools: %v", err)
      	}

      	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
      		EnvironmentID:  environmentID,
      		EnvironmentKey: environmentKey,
      		Workdir:        "/workspace",
      		ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
      			return append(agenttoolset.BetaAgentToolset20260401(env), mcpTools...)
      		},
      	})
      	if err := worker.Run(ctx); err != nil {
      		log.Fatalf("worker: %v", err)
      	}
      }

      ```

      ```java Java
      // EnvironmentWorker saat ini belum tersedia di SDK Java.
      ```

      ```php PHP
      // EnvironmentWorker saat ini belum tersedia di SDK PHP.
      ```

      ```ruby Ruby
      # EnvironmentWorker saat ini belum tersedia di SDK Ruby.
      ```
    </CodeGroup>
  </Step>
</Steps>

Perhatikan hal-hal berikut saat Anda membungkus server MCP:

* **Alat dideklarasikan, bukan ditemukan saat runtime.** Worker mendaftar alat server MCP sekali saat startup dan tidak dapat menambahkan alat ke sesi yang sedang berjalan. Ketika alat server berubah, deklarasikan lagi, pada agen atau pada sesi yang menganggur melalui [Memperbarui konfigurasi agen](/docs/id/managed-agents/session-operations#updating-the-agent-configuration), dan mulai ulang worker.
* **Nama dan deskripsi harus sesuai dengan API Managed Agents.** Nama alat kustom bersifat unik per agen dan menggunakan huruf, angka, garis bawah, dan tanda hubung (1–128 karakter); deskripsi wajib ada (1–4.096 karakter); dan array `tools` agen menerima paling banyak 128 entri (setiap alat yang dibungkus adalah satu entri, dan toolset bawaan adalah satu entri lagi). API menolak deklarasi yang menggunakan ulang nama alat, menamai alat kustom dengan nama alat agen bawaan seperti `bash` atau `read`, atau menggunakan prefiks `mcp__` yang dicadangkan. Helper MCP mempertahankan nama dan deskripsi server, jadi ganti nama atau pangkas jika diperlukan. Ketika dua server mengekspos nama alat yang sama, definisikan wrapper sendiri dengan nama berprefiks dan buat ia memanggil nama alat asli server.
* **Sebagian besar skema diteruskan tanpa perubahan.** API menerima kata kunci JSON Schema yang umum dipancarkan server MCP, seperti `additionalProperties` dan `title`. API menolak kata kunci referensi seperti `$ref` di mana pun dalam `input_schema` alat kustom, jadi inline-kan skema yang difaktorkan oleh generator seperti pydantic ke dalam `$defs`. API juga menolak `oneOf`, `anyOf`, dan `allOf` tingkat atas, serta nama properti di luar huruf, angka, garis bawah, titik, dan tanda hubung (1–64 karakter).
* **Kegagalan alat muncul sebagai hasil alat error.** Ketika server MCP melaporkan error alat, worker mengirimkan hasil alat error yang dapat direaksi oleh model. Konten MCP yang tidak memiliki padanan hasil alat, seperti blok audio dan tautan resource, juga muncul sebagai error. Atur timeout pada klien MCP untuk kegagalan yang lebih cepat dan lebih jelas, seperti yang dilakukan contoh worker Python dengan `read_timeout_seconds`. Tanpa itu, panggilan yang macet menjadi hasil error hanya ketika timeout permintaan default SDK MCP TypeScript terpicu (sekitar satu menit) atau ketika backstop worker sendiri terpicu: sekitar dua setengah menit di Python, dan dua menit di Go, di mana worker membatalkan panggilan alat yang melebihi default 120 detiknya dan mengirimkan hasil error.
* **Bungkus server yang Anda operasikan atau percayai.** Nama, deskripsi, dan hasil alat yang dibungkus masuk ke konteks model seperti alat lainnya: input yang tidak tepercaya yang dapat memengaruhi apa yang dilakukan agen dengan alat lainnya, termasuk `bash` di host worker. Deklarasikan hanya alat yang Anda maksudkan untuk digunakan agen.
* **Kebijakan izin tidak berlaku untuk alat kustom.** [Kebijakan izin](/docs/id/managed-agents/permission-policies#custom-tools) mengatur toolset bawaan dan MCP; worker mengeksekusi setiap panggilan alat yang dibungkus yang dibuat model, jadi letakkan langkah persetujuan apa pun di kode alat Anda sendiri.

## Pemantauan dan operasi

Panggilan-panggilan ini dijalankan dari perangkat pemantauan atau operasi Anda, diautentikasi dengan kunci API Claude Anda, untuk mengamati dan mengelola armada worker. Loop klaim dan keep-alive ditangani di dalam helper worker, jadi Anda tidak memanggil endpoint tersebut secara langsung.

<Warning>
  Endpoint ini menerima kunci API organisasi Anda atau environment key. Panggil dari luar host worker dengan kunci API organisasi Anda. Mengatur `ANTHROPIC_API_KEY` di host worker mengekspos kredensial berlingkup organisasi ke panggilan alat agen.
</Warning>

### Membaca kedalaman antrean

`work.stats` mengembalikan status antrean untuk sebuah lingkungan:

* `depth` adalah jumlah item yang menunggu untuk diklaim. Skalakan armada worker Anda atau buat peringatan pada backlog berdasarkan nilai ini.
* `pending` adalah jumlah item yang diklaim oleh worker tetapi belum di-acknowledge. Helper worker meng-acknowledge setiap item sebelum memprosesnya, sehingga nilai ini tetap mendekati nol dalam operasi normal; nilai non-nol yang berkelanjutan berarti worker macet antara mengklaim dan meng-acknowledge.
* `oldest_queued_at` adalah timestamp item tertua yang masih ada di antrean, menunggu untuk diklaim atau diklaim tetapi belum di-acknowledge, atau `null` ketika tidak ada.
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

### Menghentikan sesi secara halus

Gunakan `work.stop` untuk meminta worker yang menangani sesi tertentu agar mematikannya. Secara default, work item berpindah ke `stopping`: worker menyadarinya pada lease heartbeat berikutnya, membatalkan panggilan alat yang sedang berjalan pada sesi tersebut, dan mengonfirmasi penghentian, pada saat itu work item menjadi `stopped`. Berikan `force: true` dalam body permintaan (dengan CLI, gunakan `--force`) untuk menandai work item sebagai `stopped` segera tanpa menunggu konfirmasi dari worker.

Karena panggilan ini dijalankan dari perangkat operasional Anda dan bukan dari host worker, `ANTHROPIC_WORK_ID` tidak diatur secara otomatis. Atur nilainya ke ID work item target sebelum menjalankan contoh-contoh berikut. Untuk menemukan ID sebuah work item, daftarkan work item milik environment melalui [endpoint Environments Work](/docs/id/api/beta/environments/work).

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
    Model tanggung jawab bersama untuk environment sandbox yang di-hosting sendiri.
  </Card>

  <Card title="Memulai sesi" icon="settings" href="/docs/id/managed-agents/sessions">
    Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.
  </Card>

  <Card title="Tunnel MCP" icon="bolt" href="/docs/id/agents-and-tools/mcp-tunnels/overview">
    Hubungkan Claude secara aman ke server MCP yang berjalan di jaringan privat Anda tanpa membuka port masuk atau mengekspos layanan ke internet publik.
  </Card>
</CardGroup>
