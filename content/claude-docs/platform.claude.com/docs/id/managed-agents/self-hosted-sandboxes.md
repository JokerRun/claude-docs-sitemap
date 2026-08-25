---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 6ac4f23c4a372ae55c2d0199048ef6735b06513a8134d86971d5d302b69916d0
---

---
title: Sandbox yang di-hosting sendiri
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes
description: Jalankan sesi Claude Managed Agents di sandbox yang di-hosting sendiri, sehingga eksekusi alat, file, dan egress jaringan tetap berada di infrastruktur Anda sendiri.
---

Secara default, Managed Agents mengeksekusi alat dan kode di dalam [sandbox cloud yang dikelola Anthropic](https://platform.claude.com/docs/id/managed-agents/cloud-sandboxes-reference). "Self-hosted sandboxes" (sandbox yang di-hosting sendiri) mempertahankan orkestrasi di sisi Anthropic tetapi memindahkan eksekusi alat ke infrastruktur yang Anda kendalikan, sehingga kode, sistem file, dan egress jaringan agen tidak pernah meninggalkan lingkungan Anda.

Eksekusi alat tetap berada di host Anda: sistem file yang dibaca dan ditulis agen, proses yang dijalankannya, dan jaringan yang dapat dijangkaunya semuanya berada di bawah kendali Anda. Input dan output alat tetap mengalir ke control plane Anthropic (tempat Claude berjalan) sehingga model dapat melihat hasil dan menentukan apa yang harus dilakukan selanjutnya. [Skills](https://platform.claude.com/docs/id/managed-agents/skills) agen dan isi dari setiap [memory store](https://platform.claude.com/docs/id/managed-agents/memory) yang dilampirkan ke sesi disimpan oleh Anthropic dan disalin ke sandbox Anda untuk sesi tersebut; perubahan yang dibuat agen pada file memori disinkronkan kembali ke store. Lihat [model keamanan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security) untuk batas aliran data selengkapnya.

<Note>
  Sandbox yang di-hosting sendiri mendukung semua model Claude yang tersedia di Managed Agents, termasuk Claude Opus 4.8 dan Claude Opus 5. Model dikonfigurasi pada [agen](https://platform.claude.com/docs/id/managed-agents/agent-setup), bukan pada environment.
</Note>

## Perbedaannya dengan environment cloud

|                                 | Environment cloud                         | Sandbox yang di-hosting sendiri                            |
| ------------------------------- | ----------------------------------------- | ---------------------------------------------------------- |
| Tempat alat berjalan            | Sandbox yang dikelola Anthropic           | Infrastruktur Anda                                         |
| Jangkauan jaringan              | Kontrol egress Anthropic                  | Kebijakan jaringan Anda                                    |
| Pemasangan file dan repo GitHub | Dikelola oleh Anthropic                   | Dikelola oleh Anda                                         |
| Memory store                    | Dipasang oleh Anthropic di `/mnt/memory/` | Diunduh ke `/mnt/memory/` dan disinkronkan oleh worker SDK |
| Siklus hidup                    | Dikelola oleh Anthropic                   | Dikelola oleh Anda                                         |

Hosting sendiri cocok ketika agen perlu beroperasi pada data yang tidak boleh meninggalkan batas jaringan Anda, menjangkau layanan internal yang tidak dapat dirutekan secara publik, atau berjalan di bawah kontrol kepatuhan dan audit organisasi Anda sendiri.

Untuk kelayakan Zero Data Retention dan HIPAA BAA, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

## Kapan menggabungkannya dengan tunnel MCP

Hosting sendiri mengontrol *di mana kode agen dieksekusi*. [Tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) mengontrol *bagaimana Anthropic menjangkau server MCP di jaringan Anda*. Keduanya independen: sesi yang berjalan di sandbox cloud Anthropic tetap dapat menjangkau server MCP privat melalui tunnel, dan sesi yang di-hosting sendiri dapat menggunakan server MCP yang di-tunnel maupun publik. Gunakan keduanya ketika Anda ingin eksekusi dan akses alat tetap berada di dalam batas Anda. Untuk memberi agen alat dari server MCP di dalam jaringan Anda tanpa menjalankan tunnel, Anda juga dapat [membungkus server sebagai alat kustom](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#wrap-an-mcp-server-as-custom-tools) yang dilayani oleh worker Anda.

## Environment worker

<Tip>
  Panduan ini menjelaskan cara membangun worker dengan platform sandboxing generik apa pun. Panduan tambahan khusus platform tersedia untuk [AWS Lambda MicroVMs](https://docs.aws.amazon.com/lambda/latest/dg/microvms-integrations-claude-managed-agents.html), [Blaxel](https://docs.blaxel.ai/Tutorials/Claude-Managed-Agents), [Cloudflare](https://developers.cloudflare.com/sandbox/claude-managed-agents/), [Daytona](https://www.daytona.io/docs/en/guides/claude/claude-managed-agents), [E2B](https://e2b.dev/docs/agents/claude-managed-agents), [Fly.io](https://docs.sprites.dev/integrations/claude-managed-agents/), [GKE Agent Sandbox](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/tree/main/ai-ml/anthropic-agent-sandbox), [Modal](https://github.com/modal-labs/claude-managed-agents-modal-sandbox), [Namespace](https://namespace.so/docs/integrations/claude), [Superserve](https://docs.superserve.ai/integrations/managed-agents/claude-managed-agents), dan [Vercel](https://vercel.com/kb/guide/run-claude-managed-agent-tools-with-vercel-sandbox).
</Tip>

"Environment worker" (worker environment) adalah proses yang Anda jalankan di infrastruktur Anda sendiri. Proses ini menerima permintaan eksekusi alat dari Anthropic dan menjalankannya secara lokal. Environment `self_hosted` bertindak sebagai antrean kerja: ketika sebuah [sesi](https://platform.claude.com/docs/id/managed-agents/sessions) ditugaskan kepadanya, Anthropic memasukkan sesi tersebut ke antrean sebagai item kerja. Worker Anda mengklaim item kerja dari antrean tersebut, membuat konteks eksekusi untuk masing-masing, mengunduh [skills](https://platform.claude.com/docs/id/managed-agents/skills) agen (sumber daya berbasis sistem file yang dapat digunakan ulang dan memberi agen keahlian khusus domain), menjalankan panggilan alat, dan mengirimkan hasilnya kembali.

Item kerja diklaim dengan melakukan polling pada antrean environment: baik oleh **worker yang selalu aktif** yang melakukan polling terus-menerus, atau **handler yang dipicu webhook** yang aktif saat `session.status_run_started` dan mulai melakukan polling.

CLI dan SDK sama-sama menyediakan worker siap pakai. CLI `ant` hanya mendukung pola selalu aktif; SDK mendukung pola selalu aktif maupun dipicu webhook. Keduanya dapat dikonfigurasi: lihat [Worker yang di-hosting sendiri](https://platform.claude.com/docs/id/managed-agents/reference#self-hosted-worker) di referensi untuk flag CLI, dan [Helper SDK](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#sdk-helpers) di halaman ini untuk opsi SDK. Untuk kontrol lebih besar, panggil [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work) secara langsung dan implementasikan worker Anda sendiri.

### Sistem file sandbox

* **`/workspace`:** direktori kerja default sistem untuk eksekusi alat dan pengunduhan skill. Flag `--workdir` pada CLI secara default menggunakan direktori saat ini; berikan `--workdir /workspace` agar sesuai dengan default sistem. Skills diunduh ke `<workdir>/skills/<name>/`. Jika Anda menggunakan direktori kerja yang berbeda, perbarui prompt sistem agen Anda agar Claude dapat menemukan file skill.
* **Output:** pada environment yang di-hosting sendiri, prompt sistem sesi menghilangkan instruksi `/mnt/session/outputs` yang digunakan pada sandbox yang dikelola Anthropic, sehingga hasil akhir berada di mana pun agen menulisnya di sistem file sandbox Anda, biasanya di bawah direktori kerja.
* **`/mnt/memory/`:** memory store yang dilampirkan ke sesi diwujudkan di sini oleh worker SDK, satu direktori per store di `mount_path` store tersebut (misalnya, `/mnt/memory/user-preferences/`). Worker membuat direktori ini saat mengklaim sesi dan menghapusnya saat sesi berakhir; lihat [Menggunakan memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores).

## Sebelum Anda mulai

Anda memerlukan:

* **Agen yang sudah ada.** Jika Anda belum memilikinya, selesaikan [Quickstart](https://platform.claude.com/docs/id/managed-agents/quickstart) terlebih dahulu dan catat ID agennya.
* **Host Linux** dengan `/bin/bash` di path yang persis tersebut. Alat bash milik worker memanggilnya secara langsung, tanpa memeriksa `PATH`. SDK TypeScript juga memerlukan `unzip` dan `tar` di `PATH` serta Node.js 22 atau lebih baru; SDK Python dan Go menggunakan pustaka standarnya untuk ekstraksi arsip dan tidak memiliki persyaratan biner tambahan.
* **CLI `ant` atau SDK Anthropic** (Python, TypeScript, atau Go) di host worker.
* **Kredensial:** kunci environment (dibuat di Console pada langkah-langkah berikut) mengautentikasi worker ke antreannya; kunci API Claude Anda membuat sesi dan membaca statistik antrean dari luar host worker. Pembuatan kunci hanya dapat dilakukan di Console. Item kerja yang diklaim juga membawa `secret` per sesi yang digunakan worker untuk memasang [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores); Anda tidak membuatnya, tetapi dalam pola sandbox-per-sesi Anda sendiri yang meneruskannya ke dalam sandbox (lihat [Menjalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session)).
* **Untuk memory store, host yang sudah disiapkan.** Jika sesi pada environment ini akan melampirkan memory store, siapkan `/mnt/memory` di host worker sebelum Anda memulai worker; lihat [Menyiapkan host](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#prepare-the-host).

<Note>
  Pada [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), worker mengautentikasi dengan AWS IAM (SigV4) atau [kunci API yang dibuat di AWS Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#api-key-authentication), bukan kunci environment. Lampirkan managed policy [`AnthropicSelfHostedEnvironmentAccess`](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#managed-policies) ke principal IAM yang digunakan worker Anda. Kunci environment yang dibuat di Claude Console tidak berfungsi dengan endpoint Claude Platform on AWS.

  Memory store tidak dapat dilampirkan ke sesi pada environment yang di-hosting sendiri di Claude Platform on AWS.
</Note>

<Steps>
  <Step title="Buat environment yang di-hosting sendiri">
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

      <MultiFileExample language="cli" label="CLI">
        ```bash CLI
        ant beta:environments create < environment.yaml
        ```

        <File filename="environment.yaml">
          ```yaml
          name: self-hosted
          config:
            type: self_hosted
          ```
        </File>
      </MultiFileExample>

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

  <Step title="Buat kunci environment">
    Di Console, buka environment dan klik **Generate environment key**. Pembuatan kunci hanya dapat dilakukan di Console, terlepas dari apakah Anda membuat environment melalui Console atau API. Kemudian ekspor ID dan kunci environment di host worker:

    ```bash
    export ANTHROPIC_ENVIRONMENT_KEY="sk-ant-oat01-..."
    export ANTHROPIC_ENVIRONMENT_ID="env_..."
    ```
  </Step>
</Steps>

<Note>
  Skills dapat menyertakan file executable yang mungkin dijalankan agen secara langsung. Worker CLI dan SDK mempertahankan izin executable yang tercatat dalam bundel skill saat mengekstraknya. Jika Anda mengimplementasikan pengunduhan skills secara manual, Anda bertanggung jawab untuk mengatur izin executable.
</Note>

## Menjalankan worker

Pilih **selalu aktif** untuk penyiapan paling sederhana: proses yang berjalan lama melakukan polling antrean terus-menerus dan hanya memerlukan HTTPS keluar. Pilih **dipicu webhook** untuk menghindari menjalankan poller yang menganggur; pola ini memerlukan endpoint webhook yang dapat dijangkau Anthropic (lihat [Webhooks](https://platform.claude.com/docs/id/managed-agents/webhooks) untuk penyiapan endpoint dan verifikasi tanda tangan).

<Tabs>
  <Tab title="Selalu aktif (CLI ant)">
    <Steps>
      <Step title="Instal CLI ant">
        Jalankan ini di host worker.

        <Tabs>
          <Tab title="curl (Linux/WSL)">
            Untuk environment Linux, unduh biner rilis secara langsung.

            ```bash
            VERSION=1.26.1
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
        **Dalam proses**

        `ant beta:worker poll` mengklaim item kerja yang ditugaskan ke environment, mengunduh skills, mengeksekusi panggilan alat di direktori kerja, dan mengirimkan hasilnya kembali. Perintah ini membaca `ANTHROPIC_ENVIRONMENT_KEY` dan `ANTHROPIC_ENVIRONMENT_ID` dari environment.

        ```bash
        ant beta:worker poll --workdir "/workspace"
        ```

        Worker keluar dengan bersih saat menerima SIGTERM atau SIGINT: worker membatalkan panggilan alat yang sedang berjalan, mengirimkan hasil error-nya, dan melepaskan item kerja sebelum berhenti.

        **Sandbox per sesi**

        Jika Anda memerlukan isolasi yang lebih kuat (sistem file baru, batas sumber daya, atau kontrol jaringan per sesi), jalankan setiap sesi di sandbox-nya sendiri. Bangun image dengan `ant` terinstal dan `ant beta:worker run` sebagai entrypoint. Image dasar harus menyediakan `/bin/bash`; `curl` hanya digunakan saat build. Ketika sandbox dimulai, sandbox membaca detail sesi dari variabel environment, menangani sesi tersebut, lalu keluar:

        ```text
        FROM your-base-image
        ARG ANT_VERSION=1.26.1
        ARG TARGETARCH
        RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo arm64 || echo amd64) && \
            curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${ANT_VERSION}/ant_${ANT_VERSION}_linux_${ARCH}.tar.gz" \
              | tar -xz -C /usr/local/bin ant
        WORKDIR /workspace
        VOLUME /workspace
        ENTRYPOINT ["ant", "beta:worker", "run"]
        ```

        Kemudian tulis skrip spawn yang meneruskan detail sesi ke sandbox baru. Poller menyuntikkan `ANTHROPIC_SESSION_ID`, `ANTHROPIC_WORK_ID`, `ANTHROPIC_ENVIRONMENT_ID`, dan `ANTHROPIC_ENVIRONMENT_KEY` ke environment skrip, dan menulis item kerja yang diklaim ke standard input skrip sebagai JSON, termasuk `secret` per sesi milik item kerja ketika Anthropic menerbitkannya. `ANTHROPIC_BASE_URL` bersifat opsional dan hanya diteruskan jika diatur di host poller; variabel ini menimpa endpoint API default. Dalam contoh, `/host/outputs` adalah direktori host yang Anda pilih; direktori ini di-bind-mount ke direktori kerja sandbox (`/workspace`) sehingga Anda dapat mengambil hasil sesi setelah sandbox keluar. Pada environment yang di-hosting sendiri, agen menulis hasil di bawah direktori kerja, bukan `/mnt/session/outputs` (lihat [Sistem file sandbox](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#sandbox-filesystem)), sehingga memasang direktori kerja adalah cara untuk menangkapnya; mount tersebut juga mengambil pohon `skills/` yang diunduh dan file perantara apa pun yang dibuat agen.

        ```bash
        #!/bin/bash
        # spawn.sh: dipanggil sekali per item pekerjaan yang diklaim
        mkdir -p "/host/outputs/$ANTHROPIC_SESSION_ID"
        exec docker run --rm \
          -e ANTHROPIC_SESSION_ID -e ANTHROPIC_ENVIRONMENT_KEY \
          -e ANTHROPIC_WORK_ID -e ANTHROPIC_ENVIRONMENT_ID -e ANTHROPIC_BASE_URL \
          -v "/host/outputs/$ANTHROPIC_SESSION_ID":/workspace \
          your-image
        ```

        Entrypoint `ant beta:worker run` tidak memasang [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores). Jika sesi pada environment ini melampirkan memory store, pertahankan poller, tetapi bangun image per sesi berbasis worker SDK dan perluas skrip spawn untuk meneruskan `secret` item kerja ke dalam sandbox, seperti ditunjukkan di [Menjalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session).

        Mulai poller yang menunjuk ke skrip:

        ```bash
        ant beta:worker poll --on-work ./spawn.sh
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Selalu aktif (SDK)">
    <Steps>
      <Step title="Jalankan worker">
        `EnvironmentWorker` mengklaim item kerja yang ditugaskan ke environment, mengunduh skills, mengeksekusi panggilan alat di direktori kerja, dan mengirimkan hasilnya kembali. Autentikasi dengan kunci environment yang Anda buat di [Sebelum Anda mulai](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#before-you-begin).

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
          // EnvironmentWorker saat ini belum tersedia di C# SDK. Lihat tab Always-on (ant CLI).
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
          // EnvironmentWorker saat ini belum tersedia di PHP SDK. Lihat tab Always-on (ant CLI).
          ```

          ```ruby Ruby
          # EnvironmentWorker saat ini belum tersedia di Ruby SDK. Lihat tab Always-on (ant CLI).
          ```
        </CodeGroup>
      </Step>
    </Steps>
  </Tab>

  <Tab title="Dipicu webhook (SDK)">
    <Steps>
      <Step title="Berlangganan webhook sesi">
        Di [Console](https://platform.claude.com/settings/workspaces/default/webhooks), definisikan endpoint webhook yang mendengarkan event `session.status_run_started`. Lihat [Webhooks](https://platform.claude.com/docs/id/managed-agents/webhooks) untuk detailnya.
      </Step>

      <Step title="Ekspor kunci penandatanganan webhook">
        Selain ID dan kunci environment dari [Sebelum Anda mulai](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#before-you-begin), ekspor kunci penandatanganan webhook di host handler Anda agar handler dapat memverifikasi payload yang masuk. Verifikasi tanda tangan di handler Python memerlukan extra webhooks: `pip install "anthropic[webhooks]"`.

        ```bash
        export ANTHROPIC_WEBHOOK_SIGNING_KEY="whsec_..."
        ```
      </Step>

      <Step title="Implementasikan handler webhook">
        `EnvironmentWorker` mengklaim item kerja, mengunduh skills, mengeksekusi panggilan alat di direktori kerja, mengirimkan hasilnya kembali, lalu keluar. Panggil saat `session.status_run_started` terpicu.

        Ketika Anda sendiri menyerahkan item kerja yang diklaim ke `handle_item()`, seperti yang dilakukan handler ini, teruskan `secret` item kerja sebagai `work_secret` (`workSecret` di TypeScript, `WorkSecret` di Go) agar sesi dapat memasang [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores) apa pun yang dilampirkan padanya. Handler seperti ini menjalankan setiap item yang diklaim dalam satu proses di satu host, sehingga dua sesi yang melampirkan memory store yang sama tidak dapat berjalan melaluinya secara bersamaan (lihat [Menyiapkan host](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#prepare-the-host)); jika sesi Anda berbagi store, luncurkan [satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session) sebagai gantinya.

        <CodeGroup exclude="shell">
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
          // EnvironmentWorker saat ini belum tersedia di C# SDK.
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
          // Untuk menangani item pekerjaan secara langsung, lihat endpoint Environments Work.
          ```

          ```php PHP
          // EnvironmentWorker saat ini belum tersedia di PHP SDK.
          // Untuk menangani item pekerjaan secara langsung, lihat endpoint Environments Work.
          ```

          ```ruby Ruby
          # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
          # Untuk menangani item pekerjaan secara langsung, lihat endpoint Environments Work.
          ```
        </CodeGroup>
      </Step>
    </Steps>
  </Tab>
</Tabs>

### Helper SDK

SDK menyediakan tiga helper dengan tingkat kontrol yang berbeda. `EnvironmentWorker` mencakup sebagian besar kasus penggunaan; turun ke helper tingkat lebih rendah ketika Anda perlu meluncurkan proses per sesi Anda sendiri atau menjalankan alat terhadap sesi yang sudah diklaim.

* **`EnvironmentWorker`:** worker siap pakai. Menangani polling, penyiapan, dan eksekusi dari awal hingga akhir.

  * `.run()`: berjalan tanpa batas waktu, mengambil sesi saat sesi tiba.
  * `.handle_item()`: menangani satu item kerja yang diklaim lalu keluar. Berikan pengidentifikasi work, sesi, dan environment secara eksplisit, atau biarkan membaca variabel `ANTHROPIC_*` yang diatur `ant beta:worker poll --on-work` untuk proses yang dijalankannya. Agar sesi dapat memasang [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores)-nya, berikan juga `secret` item kerja sebagai `work_secret` (`workSecret` di TypeScript, `WorkSecret` di Go) atau atur `ANTHROPIC_WORK_SECRET`; `ant beta:worker poll --on-work` tidak mengatur variabel tersebut, jadi baca secret dari JSON item kerja yang ditulisnya ke standard input skrip Anda, seperti ditunjukkan di [Menjalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session).
  * `memory_sync_interval` (`memorySyncIntervalMs` di TypeScript, `MemorySyncInterval` di Go) dan `memory_sync_deletions` (`memorySyncDeletions`, `MemorySyncDeletions`): seberapa sering memory store yang dilampirkan direkonsiliasi dengan server saat sesi berjalan, dan apakah file yang dihapus agen secara lokal juga dihapus dari store. Lihat [Mengonfigurasi sinkronisasi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#configure-sync) untuk satuan, default, dan cara menonaktifkan dukungan memori.

* **`work.poller()`:** melakukan polling antrean kerja atas nama Anda dan memberikan setiap sesi yang diklaim kepada Anda. Gunakan ini ketika Anda ingin memutuskan apa yang terjadi untuk setiap sesi, misalnya meluncurkan sandbox alih-alih menjalankan alat dalam proses.

  * `drain`: apakah berhenti melakukan polling setelah antrean kosong alih-alih menunggu pekerjaan baru.
  * `block_ms`: berapa lama menunggu pekerjaan tiba sebelum kembali, dalam milidetik. Harus antara 1 dan 999 (waktu tunggu per polling; helper melakukan polling ulang secara otomatis). Berikan `null` (`None` di Python, `param.Null[int64]()` di Go) untuk pemeriksaan non-blocking; menghilangkan parameter ini menggunakan long-poll default 999 ms.
  * `reclaim_older_than_ms`: mengklaim ulang item kerja yang sudah diklaim tetapi tidak pernah dikonfirmasi dalam jumlah milidetik ini.
  * `auto_stop` (`autoStop` di TypeScript, `AutoStop` di Go): apakah mengirimkan sinyal berhenti untuk setiap item kerja setelah badan loop Anda selesai menanganinya. Matikan setiap kali apa pun yang menjalankan item kerja mengirimkan sinyal berhenti sendiri: `handle_item()` melakukannya, jadi atur ke false ketika Anda menyerahkan item yang diklaim ke `handle_item()` seperti yang dilakukan handler webhook di halaman ini, dan begitu pula sandbox yang Anda luncurkan yang memiliki panggilan berhenti tersebut.

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
      # environment (jangan pernah kunci API Anda) dan secret per-sesi milik item kerja: worker
      # di dalamnya memerlukan secret tersebut untuk memasang penyimpanan memori sesi.
      env = os.environ | {
          "ANTHROPIC_WORK_ID": work.id,
          "ANTHROPIC_SESSION_ID": work.data.id,
          "ANTHROPIC_WORK_SECRET": work.secret or "",
      }
      forward = [arg for name in SANDBOX_ENV for arg in ("-e", name)]
      launcher = await asyncio.create_subprocess_exec(
          "docker", "run", "--rm", "--detach", *forward, "your-sdk-worker-image", env=env
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
    // Ganti `docker run` dengan peluncur sandbox Anda sendiri. Teruskan kunci
    // environment (jangan pernah kunci API Anda) dan secret per sesi milik item kerja:
    // worker di dalamnya memerlukan secret tersebut untuk memasang penyimpanan memori sesi.
    const env = {
      ...process.env,
      ANTHROPIC_WORK_ID: work.id,
      ANTHROPIC_SESSION_ID: work.data.id,
      ANTHROPIC_WORK_SECRET: work.secret ?? ""
    };
    const forward = SANDBOX_ENV.flatMap((name) => ["-e", name]);
    const launcher = spawn(
      "docker",
      ["run", "--rm", "--detach", ...forward, "your-sdk-worker-image"],
      { env, stdio: "inherit" }
    );
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
  // Helper polling pekerjaan saat ini belum tersedia di C# SDK.
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
  	// Ganti `docker run` dengan peluncur sandbox Anda sendiri. Teruskan kunci
  	// environment (jangan pernah kunci API Anda) dan secret per sesi milik item kerja:
  	// worker di dalamnya memerlukan secret tersebut untuk memasang penyimpanan memori sesi.
  	args := []string{"run", "--rm", "--detach"}
  	for _, name := range sandboxEnv {
  		args = append(args, "-e", name)
  	}
  	launcher := exec.CommandContext(ctx, "docker", append(args, "your-sdk-worker-image")...)
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
  // Helper work-polling saat ini belum tersedia di Java SDK.
  // Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```

  ```php PHP
  // Helper work-polling saat ini belum tersedia di PHP SDK.
  // Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```

  ```ruby Ruby
  # Helper work-polling saat ini belum tersedia di Ruby SDK.
  # Untuk mengklaim pekerjaan secara langsung, lihat endpoint Environments Work.
  ```
</CodeGroup>

Apa pun yang meluncurkan sandbox harus meneruskan `secret` item kerja yang diklaim ke dalamnya (misalnya sebagai `ANTHROPIC_WORK_SECRET`) bersama pengidentifikasi sesi, work, dan environment, agar worker di dalamnya dapat memasang [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores) sesi; lihat [Menjalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session).

**`AgentToolContext`** adalah konteks eksekusi untuk panggilan alat. Konteks ini mendefinisikan direktori kerja dan kebijakan path, serta dapat mengunduh skills sesi. Alat file (`read`, `write`, `edit`, `glob`, `grep`) dibatasi pada direktori kerja ditambah direktori apa pun yang tercantum di `allowed_roots` (`allowedRoots` di TypeScript, `AllowedRoots` di Go), dan `write` serta `edit` juga menolak path di bawah `read_only_roots` (`readOnlyRoots`, `ReadOnlyRoots`). `EnvironmentWorker` sendiri menambahkan direktori memory store sesi ke daftar ini. Pembatasan ini hanya merupakan pagar pengaman untuk alat file, bukan sandbox; pembatasan ini tidak membatasi `bash`. **`beta_agent_toolset_20260401(env)`** menerima `AgentToolContext` dan mengembalikan implementasi alat standar (`bash`, `read`, `write`, `edit`, `glob`, `grep`).

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
  // EnvironmentWorker saat ini belum tersedia di C# SDK.
  // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
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
  // EnvironmentWorker saat ini belum tersedia di PHP SDK.
  // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
  ```

  ```ruby Ruby
  # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
  # Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
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
  // AgentToolContext saat ini belum tersedia di C# SDK.
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
  // AgentToolContext saat ini belum tersedia di PHP SDK.
  ```

  ```ruby Ruby
  # AgentToolContext saat ini belum tersedia di Ruby SDK.
  ```
</CodeGroup>

### Memverifikasi worker terhubung

Dari shell terpisah, dengan `ANTHROPIC_API_KEY` diatur ke kunci API Claude Anda (bukan kunci environment), pastikan `workers_polling` bernilai setidaknya 1:

```bash
ant beta:environments:work stats --environment-id "$ANTHROPIC_ENVIRONMENT_ID"
```

Jika `workers_polling` tetap 0, worker tidak menjangkau antrean: pastikan `ANTHROPIC_ENVIRONMENT_KEY` dan `ANTHROPIC_ENVIRONMENT_ID` diatur di host worker. Lihat [Membaca kedalaman antrean](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#read-queue-depth) untuk respons statistik lengkap dan contoh bahasa lainnya.

## Memulai sesi

Setelah worker Anda berjalan, buat sesi yang menargetkan environment. Atur `AGENT_ID` ke ID agen yang Anda catat di [Sebelum Anda mulai](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#before-you-begin). Sesi masuk ke antrean kerja environment dan menunggu di sana hingga worker mengklaimnya; jika tidak ada worker yang terhubung, sesi tetap dalam antrean alih-alih gagal.

Anthropic tidak memasang file atau repositori GitHub ke sandbox yang di-hosting sendiri. Untuk menyediakan file khusus sesi, berikan referensi file (seperti path S3 atau SHA commit) di field `metadata` sesi. Item kerja yang diklaim tidak membawa metadata sesi, tetapi membawa ID sesi: skrip spawn atau handler `--on-work` Anda mengambil sesi (`GET /v1/sessions/{session_id}`) untuk membaca field `metadata`, lalu menyiapkan file ke direktori kerja sebelum eksekusi alat dimulai.

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
  Sandbox yang di-hosting sendiri hanya mendukung resource `memory_store`; lihat [Menggunakan memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores). Sesi pada environment yang di-hosting sendiri yang menyertakan resource `file` atau `github_repository` ditolak dengan error 400:

  ```text wrap
  Environment env_... is a self-hosted environment. `resources` are not supported with self-hosted environments.
  ```

  [Deployment](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments) yang menargetkan environment yang di-hosting sendiri mengikuti aturan yang sama.
</Note>

Lihat [Worker yang di-hosting sendiri](https://platform.claude.com/docs/id/managed-agents/reference#self-hosted-worker) di referensi untuk daftar lengkap flag CLI, dan [Helper SDK](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#sdk-helpers) untuk opsi helper SDK.

## Menggunakan memory store

Sesi pada environment yang di-hosting sendiri melampirkan [memory store](https://platform.claude.com/docs/id/managed-agents/memory) persis seperti sesi pada environment cloud: cantumkan di `resources` saat Anda membuat sesi, seperti ditunjukkan di [Melampirkan memory store ke sesi](https://platform.claude.com/docs/id/managed-agents/memory#attach-a-memory-store-to-a-session). Satu sesi menerima hingga 8 memory store. Pada environment yang di-hosting sendiri, worker SDK, bukan infrastruktur Anthropic, yang mewujudkan setiap store untuk agen, sehingga memory store di sana memerlukan `EnvironmentWorker` (atau metode `handle_item()`-nya) dari SDK Python, TypeScript, atau Go.

Worker CLI `ant` (`ant beta:worker poll` dan `ant beta:worker run`) tidak memasang memory store. Untuk menggabungkan poller CLI dengan memory store, jalankan worker SDK di dalam sandbox per sesi seperti dijelaskan di [Menjalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session).

Memory store tidak dapat dilampirkan ke sesi pada environment yang di-hosting sendiri di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws).

### Cara worker menangani memori

Ketika worker mengklaim item kerja yang sesinya memiliki memory store terlampir, worker:

1. Mengunduh setiap store yang dilampirkan ke `mount_path`-nya di host worker, dengan autentikasi menggunakan `secret` per sesi milik item kerja. `mount_path` adalah direktori yang sama di bawah `/mnt/memory/` yang digunakan sesi cloud (misalnya, `/mnt/memory/user-preferences/` untuk store bernama "User Preferences"), dan prompt sistem sesi menjelaskannya kepada agen.
2. Menambahkan direktori tersebut ke allowed roots alat file, dan direktori store yang dilampirkan dengan `access: "read_only"` ke read-only roots-nya, sehingga agen mengerjakan memori dengan alat `read`, `write`, `edit`, `glob`, dan `grep` yang sama dengan yang digunakannya di direktori kerja.
3. Merekonsiliasi perubahan lokal dan remote setelah panggilan alat, paling banyak sekali per interval sinkronisasi (15 detik secara default): memori yang berubah di store ditulis ke disk, dan file yang diubah agen diunggah ke store.
4. Menjalankan sinkronisasi akhir saat sesi berakhir, menyelesaikan unggahan yang masih tertunda hingga 30 detik, lalu menghapus direktori yang dibuatnya. Worker yang dibatalkan saat sesi berjalan melewatkan sinkronisasi akhir tetapi tetap mengunggah file yang berubah dan menghapus direktori sebelum keluar.

Memory store di sisi Anthropic tetap menjadi sumber kebenaran. [Versi memori](https://platform.claude.com/docs/id/managed-agents/memory#audit-memory-changes), redaksi, serta melihat atau mengedit memori di Console berfungsi seperti pada sesi cloud, dan pembacaan serta penulisan memori oleh agen muncul di [event stream](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) sebagai event alat biasa. Karena setiap worker melakukan sinkronisasi berdasarkan interval, perubahan yang ditulis di satu sesi baru terlihat oleh sesi lain yang sedang berjalan setelah keduanya melakukan sinkronisasi, biasanya jauh di bawah satu menit pada interval default; sesi pada sandbox cloud melihat perubahan satu sama lain hampir seketika.

Setiap direktori store berisi file penanda bernama `.anthropic-memory-store` yang mengikat direktori ke store-nya. Biarkan file tersebut di tempatnya: worker tidak menyinkronkan direktori yang penandanya hilang atau diubah.

### Menyiapkan host

Memory store pada sandbox yang di-hosting sendiri memerlukan sistem file POSIX di host worker (host Linux dari [Sebelum Anda mulai](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#before-you-begin)); host Windows tidak didukung, karena worker memerlukan `O_NOFOLLOW` saat membuka file memori. Sistem file yang peka huruf besar-kecil direkomendasikan, agar path memori yang hanya berbeda dalam huruf besar-kecil tidak bertabrakan.

Sebelum Anda memulai worker, buat direktori induk dan jadikan dapat ditulis oleh pengguna yang menjalankan worker:

```bash
sudo mkdir -p /mnt/memory && sudo chown "$USER" /mnt/memory
```

Jangan membuat direktori per store sendiri. Worker membuat direktori `mount_path` setiap store (misalnya, `/mnt/memory/user-preferences`) saat sesi dimulai, menolak memulai pekerjaan sesi jika sudah ada sesuatu di path tersebut, dan menghapus direktori saat sesi berakhir. Dua aturan operasional berikut berlaku:

* **Jalankan satu sesi per sistem file ketika sesi melampirkan store yang sama.** Dua sesi tidak dapat memasang store yang sama di satu host secara bersamaan, karena keduanya memerlukan path yang sama. Memberi setiap sesi sandbox-nya sendiri, seperti dijelaskan di [Menjalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session), memenuhi aturan ini.
* **Hentikan worker dengan baik.** Ketika Anda menghentikan worker saat sesi berjalan, `EnvironmentWorker` mengunggah file memori sesi yang berubah dan menghapus direktori store-nya hanya jika worker dibatalkan, bukan dimatikan paksa: proses yang dimatikan paksa tidak menjalankan teardown, dan worker tidak memasang signal handler sendiri. Hubungkan SIGTERM dan SIGINT ke pembatalan di proses yang menjalankannya: batalkan `signal` yang Anda berikan ke worker di TypeScript, batalkan context di Go, dan di Python batalkan task yang menjalankan `run()` atau `handle_item()`. Lakukan itu dari signal handler ketika worker Anda adalah prosesnya, seperti yang dilakukan worker mandiri di halaman ini, atau dari hook shutdown server Anda sendiri ketika worker berjalan di dalam handler webhook, yang tidak boleh mengambil alih sinyal server. Kemudian hentikan worker dengan SIGTERM dan beri waktu setidaknya 30 detik untuk keluar sebelum hard kill apa pun, karena unggahan akhir dapat memakan waktu selama itu. Jika worker dimatikan paksa sebelum teardown-nya berjalan, hapus direktori store yang tersisa di bawah `/mnt/memory/` sebelum sesi berikutnya yang melampirkan store tersebut; setiap edit di dalamnya yang belum tersinkronisasi akan hilang.

### Jalankan satu sandbox per sesi

Pola sandbox-per-sesi di [Jalankan worker](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-a-worker) memberi setiap sesi filesystem yang baru, yang merupakan hal yang diminta oleh [Siapkan host](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#prepare-the-host) ketika sesi-sesi melampirkan store yang sama. Pertahankan `ant beta:worker poll --on-work` (atau work poller milik SDK) sebagai poller di host.

Entrypoint `ant beta:worker run` yang ditunjukkan di sana tidak me-mount memory store, jadi bangun image per-sesi di sekitar worker SDK sebagai gantinya: entrypoint-nya membangun `EnvironmentWorker` dan memanggil `handle_item()` (`handleItem` di TypeScript, `HandleItem` di Go), yang membaca pengenal sesi, work, dan environment dari variabel `ANTHROPIC_*` serta `secret` per-sesi milik work item dari `ANTHROPIC_WORK_SECRET`. Anda juga dapat meneruskan secret secara eksplisit sebagai `work_secret` (`workSecret` di TypeScript, `WorkSecret` di Go).

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
  // EnvironmentWorker saat ini belum tersedia di C# SDK.
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

`ant beta:worker poll --on-work` tidak menetapkan `ANTHROPIC_WORK_SECRET` untuk skrip yang dijalankannya, sehingga skrip spawn membaca secret dari JSON work item pada standard input-nya dan meneruskannya ke dalam sandbox:

```bash
#!/bin/bash
# spawn.sh: dipanggil sekali per item kerja yang diklaim
# Item kerja yang diklaim tiba sebagai JSON di stdin. Secret-nya adalah
# kredensial per sesi yang diperlukan oleh endpoint memory store.
ANTHROPIC_WORK_SECRET="$(jq -r '.secret // empty')"
export ANTHROPIC_WORK_SECRET
mkdir -p "/host/outputs/$ANTHROPIC_SESSION_ID"
exec docker run --rm \
  -e ANTHROPIC_SESSION_ID -e ANTHROPIC_ENVIRONMENT_KEY \
  -e ANTHROPIC_WORK_ID -e ANTHROPIC_ENVIRONMENT_ID -e ANTHROPIC_BASE_URL \
  -e ANTHROPIC_WORK_SECRET \
  -v "/host/outputs/$ANTHROPIC_SESSION_ID":/workspace \
  your-sdk-worker-image
```

Jika Anda mengklaim work dengan work poller milik SDK sebagai gantinya, teruskan `secret` dari setiap item yang diklaim ke dalam sandbox yang Anda luncurkan dengan cara yang sama. Teruskan hanya ke dalam sandbox yang melayani sesi tersebut, dan jangan pernah mencatatnya ke log.

Image sandbox juga memerlukan `/mnt/memory` yang dapat ditulis (lihat [Siapkan host](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#prepare-the-host)). Karena setiap sandbox melayani satu sesi dan dibuang setelahnya, tidak ada direktori sisa yang perlu dibersihkan, dan direktori memori tidak perlu di-bind-mount ke host: worker mengunggah isinya ke store sebelum sandbox keluar. Jika Anda menghentikan container sebelum sesinya berakhir, kirim sinyal yang diubah entrypoint menjadi pembatalan (lihat [Siapkan host](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#prepare-the-host)) alih-alih mematikannya secara paksa, agar unggahan tersebut tetap berjalan. Beri container waktu untuk menyelesaikan unggahan juga: Docker mengikuti sinyal stop dengan SIGKILL setelah 10 detik secara default, jadi naikkan batas itu menjadi setidaknya 30 detik seperti yang diminta Siapkan host, dengan `--stop-timeout` pada `docker run` atau periode tenggang terminasi milik orkestrator Anda.

### Konfigurasikan sinkronisasi

Dua opsi `EnvironmentWorker` mengontrol perilaku memori:

* **`memory_sync_interval`** (Python, dalam detik; `memorySyncIntervalMs` di TypeScript, dalam milidetik; `MemorySyncInterval` di Go, sebuah durasi): seberapa sering store yang terlampir direkonsiliasi dengan server saat sesi berjalan. Default-nya 15 detik; minimumnya 5 detik. Interval yang lebih pendek mempersempit jendela waktu di mana sesi lain melihat memori yang usang, dengan biaya lebih banyak permintaan memory store. `None` di Python, `null` di TypeScript, atau durasi negatif di Go menonaktifkan dukungan memori sepenuhnya: worker tidak mengunduh maupun menyinkronkan store, dan sesi dengan memory store terlampir berjalan tanpanya meskipun prompt sistemnya masih mendeskripsikannya, jadi nonaktifkan dukungan memori hanya pada worker yang sesinya tidak melampirkan memory store. Selama dukungan memori diaktifkan, work item yang tiba tanpa `secret` per-sesi untuk sesi dengan store terlampir akan gagal alih-alih berjalan tanpa memori (lihat [Pecahkan masalah mount memori](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#troubleshoot-memory-mounts)).
* **`memory_sync_deletions`** (`memorySyncDeletions` di TypeScript, `MemorySyncDeletions` di Go): apakah file yang dihapus agen secara lokal juga dihapus dari store. Nilainya adalah salah satu dari `"enabled"` (default), `"log_only"`, atau `"disabled"` di Python dan TypeScript, dan salah satu dari konstanta `environments.MemorySyncDeletionsEnabled` (nilai nol), `environments.MemorySyncDeletionsLogOnly`, atau `environments.MemorySyncDeletionsDisabled` di Go. Ketika diaktifkan, worker menghapus memori dari store setelah sinkronisasi berikutnya mengonfirmasi bahwa file tersebut masih tidak ada; dalam mode log-only, worker menjalankan pemeriksaan yang sama tetapi hanya mencatat ke log apa yang akan dihapusnya, yang memungkinkan Anda mengamati apa yang akan dihapus worker Anda sebelum Anda mempercayai mode enabled; ketika dinonaktifkan, worker tidak pernah menghapus dari store. Unggahan dan unduhan tidak terpengaruh oleh pengaturan ini.

Tetapkan opsi-opsi ini di tempat Anda membangun worker, baik melalui konstruktor `EnvironmentWorker` atau, di Python dan TypeScript, factory `client.beta.environments.work.worker()` yang digunakan oleh handler webhook.

Sebagai contoh, untuk menyinkronkan setiap 10 detik dan hanya mencatat ke log penghapusan yang akan dilakukan worker:

<CodeGroup exclude="shell">
  ```python Python
  worker = EnvironmentWorker(
      client,
      environment_id=environment_id,
      environment_key=environment_key,
      workdir="/workspace",
      memory_sync_interval=10,  # seconds
      memory_sync_deletions="log_only",
  )
  ```

  ```typescript TypeScript
  const worker = new EnvironmentWorker({
    client,
    environmentId,
    environmentKey,
    workdir: "/workspace",
    memorySyncIntervalMs: 10_000,
    memorySyncDeletions: "log_only"
  });
  ```

  ```csharp C#
  // EnvironmentWorker saat ini belum tersedia di C# SDK.
  ```

  ```go Go
  worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  	EnvironmentID:       environmentID,
  	EnvironmentKey:      environmentKey,
  	Workdir:             "/workspace",
  	MemorySyncInterval:  10 * time.Second,
  	MemorySyncDeletions: environments.MemorySyncDeletionsLogOnly,
  })
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

### Store read-only dan konflik

Untuk store yang dilampirkan dengan `access: "read_only"`, alat `write` dan `edit` menolak mengubah file di dalam direktorinya, dan worker tidak pernah mengunggah apa pun darinya. Perubahan yang dibuat melalui `bash`, atau melalui alat kustom atau server MCP yang Anda layani dari sandbox, tidak diblokir secara lokal: perubahan tersebut tidak pernah disinkronkan ke store, dan perubahan remote berikutnya pada memori itu akan menimpanya. Jika Anda memerlukan salinan lokal itu sendiri tetap tidak berubah selama sesi, nonaktifkan alat `bash` untuk agen tersebut dan jangan berikan alat kustom yang menulis ke filesystem sandbox; jangan me-mount path store sebagai read-only, karena worker itu sendiri harus membuat direktori dan menulis memori yang diunduh ke dalamnya.

Konflik diselesaikan dengan memihak store. Ketika agen mengubah file memori yang juga berubah di store sejak sesi terakhir menyinkronkannya, worker mempertahankan versi store pada sinkronisasi berikutnya, menimpa file lokal dengannya, dan mencatat peringatan ke log; alat `write` dan `edit` itu sendiri berhasil dan tidak ada error yang sampai ke agen. Jika perubahan agen masih berlaku, agen dapat membaca ulang file setelah sinkronisasi dan membuat perubahan itu lagi.

### Pecahkan masalah mount memori

Worker mencatat kegagalan mount dan sinkronisasi latar belakang ke log alih-alih melaporkannya ke sesi; hanya penolakan read-only yang sampai ke agen, sebagai error alat (lihat [Store read-only dan konflik](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#read-only-stores-and-conflicts)). Jika memory store tidak dapat di-mount ketika worker mengklaim sesi, worker menggagalkan work item: sesi tidak memancarkan event error dan tetap idle.

| Gejala                                                                                                                           | Penyebab                                                                                                                                                                                                | Perbaikan                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Log worker berisi `the work item carried no sessions token` (di Go, error `ErrSessionMemoryNoToken`) dan work item gagal.        | `secret` per-sesi milik work item tidak sampai ke worker: memory store pada sandbox self-hosted tidak diaktifkan untuk organisasi Anda, atau skrip spawn Anda tidak meneruskan secret ke dalam sandbox. | Dalam pola sandbox-per-sesi, teruskan `ANTHROPIC_WORK_SECRET` ke dalam sandbox seperti ditunjukkan di [Jalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session). Jika worker melakukan polling dan menjalankan sesi dalam satu proses dan masih mencatat ini ke log, hubungi dukungan. |
| Log worker berisi `something already exists at the memory store's path`.                                                         | Direktori sisa dari sesi sebelumnya, biasanya sesi yang worker-nya dimatikan secara paksa sebelum teardown-nya berjalan.                                                                                | Hapus direktori sisa yang disebutkan oleh baris log. Edit di dalamnya yang belum tersinkronisasi akan hilang.                                                                                                                                                                                                                                                       |
| Log worker berisi `cannot create the memory store's folder` dan `the worker host must make this mount path writable`.            | Pengguna yang menjalankan worker tidak dapat membuat direktori di bawah `/mnt/memory`.                                                                                                                  | Buat `/mnt/memory` dan `chown` ke pengguna tersebut; lihat [Siapkan host](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#prepare-the-host).                                                                                                                                                                                               |
| Sesi berada dalam status `idle` dengan stop reason `requires_action` dan tanpa event error tak lama setelah worker mengklaimnya. | Worker menggagalkan work item karena tidak dapat me-mount memory store, karena salah satu alasan sebelumnya.                                                                                            | Perbaiki penyebabnya di host, lalu kirim event [`user.interrupt`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#integrating-events): work milik sesi diantrekan lagi dan worker berikutnya yang mengklaimnya mencoba ulang mount tersebut.                                                                                                |

## Layani alat kustom dari sandbox Anda

[Alat kustom](https://platform.claude.com/docs/id/managed-agents/tools#custom-tools) adalah alat yang dieksekusi oleh kode Anda sendiri: agen memancarkan event `agent.custom_tool_use` dan menunggu `user.custom_tool_result` yang cocok. Worker dapat menjadi kode tersebut, dan karena berjalan di dalam sandbox Anda, alat tersebut menjangkau layanan internal, kredensial, dan egress jaringan yang Anda konfigurasikan untuk sandbox, dan tidak lebih dari itu. Kunci environment mengotorisasi pengiriman hasil alat kustom, sehingga kunci API Claude Anda tetap berada di luar host worker.

<Note>
  Melayani alat kustom memerlukan worker SDK: worker CLI `ant` tidak memiliki cara untuk mendaftarkan implementasi alat kustom. Dalam pola sandbox-per-sesi, jalankan `EnvironmentWorker` di dalam sandbox dengan `handle_item()` (`handleItem` di TypeScript, `HandleItem` di Go) sebagai pengganti `ant beta:worker run`.
</Note>

<Steps>
  <Step title="Deklarasikan alat pada agen">
    Tambahkan entri `custom` ke `tools` milik agen yang `name`-nya cocok dengan alat yang didaftarkan worker Anda. Lihat [Alat kustom](https://platform.claude.com/docs/id/managed-agents/tools#custom-tools) untuk bentuk deklarasi lengkapnya.

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

  <Step title="Daftarkan implementasi pada worker">
    Teruskan alat melalui factory `tools` milik worker (lihat [Helper SDK](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#sdk-helpers)), bersama toolset bawaan:

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
      // EnvironmentWorker saat ini belum tersedia di C# SDK.
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
      // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
      ```

      ```php PHP
      // EnvironmentWorker saat ini belum tersedia di PHP SDK.
      // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
      ```

      ```ruby Ruby
      # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
      # Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
      ```
    </CodeGroup>
  </Step>
</Steps>

Worker hanya menjawab alat yang terdaftar padanya. Alat kustom yang dideklarasikan pada agen tetapi tidak terdaftar pada worker atau klien mana pun membuat sesi terjeda dengan stop reason `requires_action` sampai sesuatu mengirimkan hasilnya; lihat [Menangani panggilan alat kustom](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) untuk alur event-nya.

### Bungkus server MCP sebagai alat kustom

[Konektor MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) terhubung ke server MCP dari sisi Anthropic, sehingga server harus mengekspos endpoint HTTP yang dapat dijangkau Anthropic, secara langsung atau melalui [tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview). Untuk menggunakan server yang hanya dapat dijangkau oleh jaringan Anda, jadikan worker sebagai klien MCP sebagai gantinya dan deklarasikan alat-alat server sebagai alat kustom. Server MCP tidak memerlukan konektivitas masuk dari luar jaringan Anda; Anthropic menerima definisi alat yang Anda deklarasikan pada agen, input setiap panggilan, dan hasil yang dikirim balik oleh worker Anda. Saat runtime, model memanggil alat yang dibungkus seperti alat kustom lainnya:

1. Agen memancarkan event `agent.custom_tool_use`.
2. Worker, di dalam sandbox Anda, meneruskan panggilan melalui sesi MCP terbukanya ke server di jaringan Anda.
3. Worker mengirimkan respons server sebagai `user.custom_tool_result`.

[Helper MCP sisi klien](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#client-side-mcp-helpers) milik SDK mengonversi alat-alat server menjadi alat yang dapat dijalankan yang diterima worker; instal SDK MCP bersama SDK Anthropic (`pip install "anthropic[mcp]" "mcp>=1.24"`, `npm install @modelcontextprotocol/sdk`, `go get github.com/modelcontextprotocol/go-sdk`). Contoh-contoh ini terhubung tanpa autentikasi; untuk mengirim kredensial, konfigurasikan klien HTTP atau opsi permintaan yang Anda serahkan ke transport MCP (`http_client` di Python, `requestInit` di TypeScript, `HTTPClient` di Go).

<Steps>
  <Step title="Deklarasikan alat-alat server pada agen">
    Daftar alat-alat server MCP dan deklarasikan masing-masing sebagai alat `custom`; `name`, `description`, dan `inputSchema` MCP dipetakan satu-ke-satu ke field alat kustom. Jika server memaginasi daftar alatnya, deklarasikan setiap halaman; worker harus mendaftar halaman yang sama.

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
                  model="claude-opus-5",
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
        model: "claude-opus-5",
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

      // toCustomTool memetakan satu definisi alat MCP ke deklarasi alat kustom.
      // Field-nya dipetakan satu ke satu: parameter bertipe membawa `properties` dan
      // `required`, dan setiap kata kunci JSON Schema lain yang dikeluarkan server disalurkan di
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
      			// Tipe parameter selalu di-marshal sebagai "type": "object".
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

      	// Jalankan ini di mana pun Anda membuat agen, bukan di host worker: ini
      	// mengautentikasi dengan kunci API Claude Anda (ANTHROPIC_API_KEY).
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
      		Model: anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus5},
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
      // Java bekerja dengan cara yang sama setelah Anda mendaftar alat server dengan klien MCP.
      ```

      ```php PHP
      // Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      // PHP bekerja dengan cara yang sama setelah Anda mendaftar alat server dengan klien MCP.
      ```

      ```ruby Ruby
      # Lihat tab Python, TypeScript, dan Go. Mendeklarasikan alat kustom dari
      # Ruby bekerja dengan cara yang sama setelah Anda mendaftar alat server dengan klien MCP.
      ```
    </CodeGroup>
  </Step>

  <Step title="Layani alat-alat dari worker">
    Hubungkan ke server MCP yang sama saat startup, konversi alat-alatnya dengan helper MCP, dan daftarkan bersama toolset bawaan. Pertahankan satu sesi MCP terbuka selama masa hidup worker.

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
      // EnvironmentWorker saat ini belum tersedia di C# SDK.
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
      // EnvironmentWorker saat ini belum tersedia di Java SDK.
      ```

      ```php PHP
      // EnvironmentWorker saat ini belum tersedia di PHP SDK.
      ```

      ```ruby Ruby
      # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
      ```
    </CodeGroup>
  </Step>
</Steps>

Perhatikan hal-hal berikut ketika Anda membungkus server MCP:

* **Alat dideklarasikan, bukan ditemukan saat runtime.** Worker mendaftar alat-alat server MCP sekali saat startup dan tidak dapat menambahkan alat ke sesi yang sedang berjalan. Ketika alat-alat server berubah, deklarasikan lagi, pada agen atau pada sesi idle melalui [Memperbarui konfigurasi agen](https://platform.claude.com/docs/id/managed-agents/session-operations#updating-the-agent-configuration), dan mulai ulang worker.
* **Nama dan deskripsi harus sesuai dengan Managed Agents API.** Nama alat kustom bersifat unik per agen dan menggunakan huruf, angka, garis bawah, dan tanda hubung (1–128 karakter); deskripsi yang tidak kosong wajib ada; dan array `tools` milik agen menerima paling banyak 128 entri (setiap alat yang dibungkus adalah satu entri, dan toolset bawaan adalah satu entri lagi). API menolak deklarasi yang menggunakan ulang nama alat, menamai alat kustom dengan nama alat agen bawaan seperti `bash` atau `read`, atau menggunakan prefiks `mcp__` yang dicadangkan. Helper MCP mempertahankan nama dan deskripsi server, jadi ganti nama atau pangkas bila diperlukan. Ketika dua server mengekspos nama alat yang sama, definisikan wrapper-nya sendiri dengan nama berprefiks dan buat wrapper itu memanggil nama alat asli milik server.
* **Sebagian besar skema diteruskan tanpa perubahan.** API menerima kata kunci JSON Schema yang umum dipancarkan server MCP, seperti `additionalProperties` dan `title`. API menolak kata kunci referensi seperti `$ref` di mana pun dalam `input_schema` alat kustom, jadi inline-kan skema yang difaktorkan oleh generator seperti pydantic ke dalam `$defs`. API juga menolak `oneOf`, `anyOf`, dan `allOf` tingkat atas, serta nama properti di luar huruf, angka, garis bawah, titik, dan tanda hubung (1–64 karakter).
* **Kegagalan alat muncul sebagai hasil alat error.** Ketika server MCP melaporkan error alat, worker mengirimkan hasil alat error yang dapat ditanggapi model. Konten MCP yang tidak memiliki padanan hasil alat, seperti blok audio dan tautan resource, juga muncul sebagai error. Tetapkan timeout pada klien MCP untuk kegagalan yang lebih cepat dan lebih jelas, seperti yang dilakukan contoh worker Python dengan `read_timeout_seconds`. Tanpa timeout, panggilan yang macet baru menjadi hasil error ketika timeout permintaan default SDK MCP TypeScript terpicu (sekitar satu menit) atau ketika backstop milik worker sendiri terpicu: sekitar dua setengah menit di Python, dan dua menit di Go, di mana worker membatalkan panggilan alat yang melampaui default 120 detiknya dan mengirimkan hasil error.
* **Bungkus server yang Anda operasikan atau percayai.** Nama, deskripsi, dan hasil alat yang dibungkus masuk ke konteks model seperti alat lainnya: input tidak tepercaya yang dapat memengaruhi apa yang dilakukan agen dengan alat-alat lainnya, termasuk `bash` di host worker. Deklarasikan hanya alat yang Anda maksudkan untuk digunakan agen.
* **Kebijakan izin tidak berlaku untuk alat kustom.** [Kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies#custom-tools) mengatur toolset bawaan dan MCP; worker mengeksekusi setiap panggilan alat yang dibungkus yang dibuat model, jadi tempatkan langkah persetujuan apa pun di kode alat Anda sendiri.

## Pemantauan dan operasi

Panggilan-panggilan ini dijalankan dari tooling pemantauan atau operasi Anda, diautentikasi dengan kunci API Claude Anda, untuk mengamati dan mengelola armada worker. Loop klaim dan keep-alive ditangani di dalam helper worker, sehingga Anda tidak memanggil endpoint tersebut secara langsung.

<Warning>
  Endpoint-endpoint ini menerima kunci API organisasi Anda atau kunci environment. Panggil dari luar host worker dengan kunci API organisasi Anda. Menetapkan `ANTHROPIC_API_KEY` di host worker mengekspos kredensial bercakupan organisasi ke panggilan alat agen.
</Warning>

### Baca kedalaman antrean

`work.stats` mengembalikan status antrean untuk sebuah environment:

* `depth` adalah jumlah item yang menunggu untuk diklaim. Skalakan armada worker Anda atau buat peringatan atas backlog berdasarkan nilai ini.
* `pending` adalah jumlah item yang diklaim oleh worker tetapi belum di-acknowledge. Helper worker meng-acknowledge setiap item sebelum memprosesnya, sehingga nilai ini tetap mendekati nol dalam operasi normal; nilai bukan nol yang berkelanjutan berarti sebuah worker macet di antara mengklaim dan meng-acknowledge.
* `oldest_queued_at` adalah timestamp item tertua yang masih berada di antrean, menunggu untuk diklaim atau sudah diklaim tetapi belum di-acknowledge, atau `null` ketika tidak ada.
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

### Hentikan sesi dengan anggun

Gunakan `work.stop` untuk meminta worker yang menangani sesi tertentu agar mematikannya. Secara default work item berpindah ke `stopping`: worker menyadarinya pada heartbeat lease berikutnya, membatalkan panggilan alat sesi yang sedang berjalan, dan mengonfirmasi pematian, dan pada titik itu work item menjadi `stopped`. Teruskan `force: true` di body permintaan (dengan CLI, teruskan `--force`) untuk menandai work item sebagai `stopped` segera alih-alih menunggu konfirmasi worker.

Karena panggilan-panggilan ini dijalankan dari tooling operasi Anda alih-alih host worker, `ANTHROPIC_WORK_ID` tidak ditetapkan secara otomatis. Tetapkan ke ID work item target sebelum menjalankan contoh-contoh berikut. Untuk menemukan ID work item, daftar work item milik environment melalui [endpoint Environments Work](https://platform.claude.com/docs/id/api/beta/environments/work).

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
  <Card title="Model keamanan" icon="lock" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security">
    Model tanggung jawab bersama untuk environment sandbox self-hosted.
  </Card>

  <Card title="Mulai sesi" icon="settings" href="https://platform.claude.com/docs/id/managed-agents/sessions">
    Buat sesi untuk menjalankan agen Anda dan mulai mengeksekusi tugas.
  </Card>

  <Card title="Tunnel MCP" icon="bolt" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview">
    Hubungkan Claude dengan aman ke server MCP yang berjalan di jaringan privat Anda tanpa membuka port masuk atau mengekspos layanan ke internet publik.
  </Card>
</CardGroup>
