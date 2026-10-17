---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes
fetched_at: 2026-10-17T02:19:22.559852Z
sha256: 0d23dd014d025711d12a55b261f79a85e61fc0c0ad3dbedb452384cb99b5bb03
---

---
title: Sandbox yang di-host sendiri
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes
description: Jalankan sesi Claude Managed Agents di sandbox yang di-host sendiri, sehingga eksekusi alat, file, dan lalu lintas jaringan keluar tetap berada di infrastruktur Anda sendiri.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

"Self-hosted sandboxes" (sandbox yang di-host sendiri) memindahkan eksekusi alat agen dari sandbox cloud yang dikelola Anthropic ke infrastruktur yang Anda kendalikan, sementara Anthropic tetap menjalankan agen. Untuk mempelajari apa artinya dan memutuskan apakah ini cocok untuk agen Anda, lihat [Memilih lingkungan agen](https://platform.claude.com/docs/id/managed-agents/choosing-an-environment).

## Cara kerjanya

Lingkungan `self_hosted` berfungsi sebagai antrean kerja. Anda menjalankan **environment worker** (worker lingkungan), yaitu proses di infrastruktur Anda sendiri yang melayani antrean tersebut:

1. Anda membuat [sesi](https://platform.claude.com/docs/id/managed-agents/sessions) yang menargetkan lingkungan tersebut. Anthropic memasukkan sesi ke antrean sebagai item kerja.
2. Worker Anda mengklaim item kerja dan mengunduh [skill](https://platform.claude.com/docs/id/managed-agents/skills) milik agen serta [memory store](https://platform.claude.com/docs/id/managed-agents/memory) milik sesi.
3. Claude berjalan di sisi Anthropic dan meminta pemanggilan alat. Worker Anda menjalankan setiap pemanggilan secara lokal dan mengirimkan hasilnya kembali.

Input dan output alat tetap mengalir ke "control plane" (bidang kendali) Anthropic, sehingga model dapat melihat hasil dan menentukan langkah selanjutnya. Anthropic menyimpan skill dan memory store. Sandbox Anda menyimpan salinannya untuk sesi tersebut. Lihat [Model keamanan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security) untuk batas aliran data selengkapnya.

Sandbox yang di-host sendiri mendukung setiap model Claude yang tersedia di Managed Agents. Model dikonfigurasi pada agen, bukan pada lingkungan.

CLI `ant` serta SDK Python, TypeScript, dan Go menyertakan worker siap pakai. Penyedia sandbox seperti Cloudflare, Daytona, dan Modal juga menerbitkan [panduan platform](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#platform-guides) mereka sendiri.

## Mulai cepat

Panduan mulai cepat ini menjalankan satu worker yang selalu aktif dengan CLI `ant`, mengirimkan sebuah sesi kepadanya, dan memastikan bahwa pemanggilan alat agen berjalan di host Anda.

### Prasyarat

* **Sebuah agen:** Jika Anda belum memilikinya, selesaikan [Memulai dengan Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/quickstart) terlebih dahulu dan catat ID agennya.
* **Sebuah host Linux:** Host memerlukan `/bin/bash` tepat di path tersebut. Worker hanya memerlukan HTTPS keluar.
* **Sebuah kunci API Claude:** Anda menggunakannya dari mesin Anda sendiri untuk membuat sesi dan membaca statistik antrean. Jangan simpan di host worker, karena pemanggilan alat agen dapat membacanya.
* **CLI `ant` atau SDK di mesin Anda sendiri:** Langkah statistik dan sesi dalam panduan mulai cepat ini dijalankan di sana, bukan di host worker. Instal CLI dengan cara yang sama seperti [langkah instalasi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-your-first-session) untuk worker, atau instal [SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview).

<Note>
  Di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), worker melakukan autentikasi dengan AWS IAM (SigV4) atau [kunci API yang dibuat di AWS Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#api-key-authentication), bukan kunci lingkungan. Lampirkan kebijakan terkelola [`AnthropicSelfHostedEnvironmentAccess`](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#managed-policies) ke principal IAM yang digunakan worker Anda. Kunci lingkungan yang dibuat di Claude Console tidak berfungsi dengan endpoint Claude Platform on AWS.
</Note>

### Jalankan sesi pertama Anda

<Steps>
  <Step title="Buat lingkungan yang di-host sendiri">
    Di Claude Console, buka halaman [Environments](https://platform.claude.com/environments) (`platform.claude.com/environments`), klik **Create environment**, dan di bawah **Hosting** pilih **Self-hosted**.

    Atau melalui API:

    <CodeGroup defaultLanguage="CLI">
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

      <CodeGroupItem>
        ```bash CLI
        ant apply environment.yaml
        ```

        <File filename="environment.yaml">
          ```yaml
          # yaml-language-server: $schema=https://platform.claude.com/schemas/ant/beta/environment.json
          name: self-hosted
          config:
            type: self_hosted
          ```
        </File>
      </CodeGroupItem>

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
      $client = new \Anthropic\Client();

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
    Di Console, buka lingkungan tersebut dan klik **Generate environment key**. Kunci lingkungan mengautentikasi worker ke antreannya. Anda hanya dapat membuatnya di Console, bahkan untuk lingkungan yang Anda buat melalui API.

    Ekspor ID lingkungan dan kunci di host worker:

    ```bash
    export ANTHROPIC_ENVIRONMENT_KEY="sk-ant-oat01-..."
    export ANTHROPIC_ENVIRONMENT_ID="env_..."
    ```
  </Step>

  <Step title="Instal CLI ant">
    Jalankan ini di host worker.

    <Tabs>
      <Tab title="curl (Linux/WSL)">
        Untuk lingkungan Linux, unduh binary rilis secara langsung.

        ```bash
        VERSION=1.42.0
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
    Buat direktori kerja, lalu jalankan worker. `--workdir` secara default menggunakan direktori saat ini, jadi berikan `/workspace` agar sesuai dengan default sistem.

    ```bash
    sudo mkdir -p /workspace && sudo chown "$USER" /workspace
    ant beta:worker poll --workdir /workspace
    ```

    Worker membaca dua variabel yang Anda ekspor dan melakukan polling hingga Anda menghentikannya.
  </Step>

  <Step title="Verifikasi bahwa worker terhubung">
    Di mesin Anda sendiri, atur `ANTHROPIC_API_KEY` ke kunci API Claude Anda (bukan kunci lingkungan) dan `ANTHROPIC_ENVIRONMENT_ID` (python, ruby: `environment_id`; typescript, java, csharp: `environmentId`; go: `environmentID`; php: `$environmentId`) ke ID lingkungan. Pastikan bahwa `workers_polling` (java, php: `workersPolling`; csharp, go: `WorkersPolling`) bernilai setidaknya 1:

    <CodeGroup>
      ```bash cURL
      curl -sS --fail-with-body "https://api.anthropic.com/v1/environments/$ANTHROPIC_ENVIRONMENT_ID/work/stats" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01"
      ```

      ```bash CLI
      ant beta:environments:work stats --environment-id "$ANTHROPIC_ENVIRONMENT_ID"
      ```

      ```python Python
      client = anthropic.Anthropic()

      stats = client.beta.environments.work.stats(environment_id)
      print(f"workers_polling={stats.workers_polling}")
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const stats = await client.beta.environments.work.stats(environmentId);

      console.log(`workers_polling=${stats.workers_polling}`);
      ```

      ```csharp C#
      var client = new AnthropicClient();

      var stats = await client.Beta.Environments.Work.Stats(environmentId);

      Console.WriteLine($"workers_polling={stats.WorkersPolling}");
      ```

      ```go Go
      client := anthropic.NewClient()

      stats, err := client.Beta.Environments.Work.Stats(
      	context.Background(),
      	environmentID,
      	anthropic.BetaEnvironmentWorkStatsParams{},
      )
      if err != nil {
      	panic(err)
      }

      fmt.Printf("workers_polling=%d\n", stats.WorkersPolling)
      ```

      ```java Java
      var client = AnthropicOkHttpClient.fromEnv();

      var stats = client.beta().environments().work().stats(environmentId);

      IO.println("workers_polling=" + stats.workersPolling().orElse(null));
      ```

      ```php PHP
      $client = new Client();

      $stats = $client->beta->environments->work->stats($environmentId);

      printf("workers_polling=%d\n", $stats->workersPolling);
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      stats = client.beta.environments.work.stats(environment_id)

      puts "workers_polling=#{stats.workers_polling}"
      ```
    </CodeGroup>

    Jika `workers_polling` (java, php: `workersPolling`; csharp, go: `WorkersPolling`) tetap bernilai 0, lihat [Pemecahan masalah](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#troubleshooting).
  </Step>

  <Step title="Mulai sesi">
    Atur `AGENT_ID` (python, ruby: `agent_id`; typescript, java, csharp: `agentId`; go: `agentID`; php: `$agentId`) ke ID agen Anda. Buat sesi yang menargetkan lingkungan tersebut, lalu kirimkan sebuah tugas:

    <CodeGroup>
      ```bash cURL
      SESSION_ID=$(curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d '{
          "agent": "'"$AGENT_ID"'",
          "environment_id": "'"$ANTHROPIC_ENVIRONMENT_ID"'"
        }' | jq -er '.id'
      )

      curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d '{
          "events": [
            {
              "type": "user.message",
              "content": [
                {
                  "type": "text",
                  "text": "Write the output of \"uname -a\" to hello.txt in your working directory."
                }
              ]
            }
          ]
        }'
      ```

      ```bash CLI
      SESSION_ID=$(ant beta:sessions create \
        --agent "$AGENT_ID" \
        --environment-id "$ANTHROPIC_ENVIRONMENT_ID" \
        --transform id --raw-output)

      ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
      events:
        - type: user.message
          content:
            - type: text
              text: Write the output of "uname -a" to hello.txt in your working directory.
      YAML
      ```

      ```python Python
      session = client.beta.sessions.create(
          agent=agent_id,
          environment_id=environment_id,
      )

      client.beta.sessions.events.send(
          session.id,
          events=[
              {
                  "type": "user.message",
                  "content": [
                      {
                          "type": "text",
                          "text": 'Write the output of "uname -a" to hello.txt in your working directory.',
                      },
                  ],
              },
          ],
      )
      ```

      ```typescript TypeScript
      const session = await client.beta.sessions.create({
        agent: agentId,
        environment_id: environmentId
      });

      await client.beta.sessions.events.send(session.id, {
        events: [
          {
            type: "user.message",
            content: [
              {
                type: "text",
                text: 'Write the output of "uname -a" to hello.txt in your working directory.'
              }
            ]
          }
        ]
      });
      ```

      ```csharp C#
      var session = await client.Beta.Sessions.Create(new()
      {
          Agent = agentId,
          EnvironmentID = environmentId,
      });

      await client.Beta.Sessions.Events.Send(session.ID, new()
      {
          Events =
          [
              new BetaManagedAgentsUserMessageEventParams
              {
                  Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
                  Content =
                  [
                      new BetaManagedAgentsTextBlock
                      {
                          Type = BetaManagedAgentsTextBlockType.Text,
                          Text = "Write the output of \"uname -a\" to hello.txt in your working directory.",
                      },
                  ],
              },
          ],
      });
      ```

      ```go Go
      session, err := client.Beta.Sessions.New(context.Background(), anthropic.BetaSessionNewParams{
      	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agentID)},
      	EnvironmentID: environmentID,
      })
      if err != nil {
      	panic(err)
      }

      _, err = client.Beta.Sessions.Events.Send(context.Background(), session.ID, anthropic.BetaSessionEventSendParams{
      	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
      		OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
      			Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
      			Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
      				OfText: &anthropic.BetaManagedAgentsTextBlockParam{
      					Type: anthropic.BetaManagedAgentsTextBlockTypeText,
      					Text: "Write the output of \"uname -a\" to hello.txt in your working directory.",
      				},
      			}},
      		},
      	}},
      })
      if err != nil {
      	panic(err)
      }
      ```

      ```java Java
      var session = client.beta().sessions().create(SessionCreateParams.builder()
          .agent(agentId)
          .environmentId(environmentId)
          .build());

      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                  .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                  .addTextContent("Write the output of \"uname -a\" to hello.txt in your working directory.")
                  .build())
              .build());
      ```

      ```php PHP
      $session = $client->beta->sessions->create(
          agent: $agentId,
          environmentID: $environmentId,
      );

      $client->beta->sessions->events->send(
          $session->id,
          events: [
              [
                  'type' => 'user.message',
                  'content' => [['type' => 'text', 'text' => 'Write the output of "uname -a" to hello.txt in your working directory.']],
              ],
          ],
      );
      ```

      ```ruby Ruby
      session = client.beta.sessions.create(
        agent: agent_id,
        environment_id: environment_id
      )

      client.beta.sessions.events.send_(
        session.id,
        events: [
          {
            type: :"user.message",
            content: [{type: :text, text: 'Write the output of "uname -a" to hello.txt in your working directory.'}]
          }
        ]
      )
      ```
    </CodeGroup>

    Sesi menunggu di antrean lingkungan hingga sebuah worker mengklaimnya. Jika tidak ada worker yang terhubung, sesi tetap berada dalam antrean alih-alih gagal.
  </Step>

  <Step title="Pastikan alat berjalan di host Anda">
    Di host worker, baca file yang ditulis oleh agen:

    ```bash
    cat /workspace/hello.txt
    ```

    File tersebut mendeskripsikan kernel host Anda sendiri, jadi pemanggilan alat agen berjalan di sana. Untuk mengikuti pekerjaan agen secara langsung, lihat [Aliran event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming).
  </Step>
</Steps>

## Sumber daya sesi

Sandbox yang di-host sendiri hanya mendukung sumber daya `memory_store`. Sesi pada lingkungan yang di-host sendiri yang menyertakan sumber daya `file` atau `github_repository` akan ditolak dengan error 400:

```text wrap
Environment env_... is a self-hosted environment. `resources` are not supported with self-hosted environments.
```

[Deployment](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments) yang menargetkan lingkungan yang di-host sendiri mengikuti aturan yang sama. Untuk memberikan file input tersendiri kepada sebuah sesi, lihat [Menyiapkan file untuk sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#stage-files-for-a-session).

## Sandbox yang di-host sendiri dan tunnel MCP

Hosting sendiri mengendalikan *di mana kode agen dieksekusi*. [Tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) mengendalikan *bagaimana Anthropic menjangkau server MCP di jaringan Anda*. Keduanya independen:

* Sesi di sandbox cloud Anthropic dapat menjangkau server MCP privat melalui tunnel. Misalnya, server MCP privat mungkin berada di depan database atau API internal di balik firewall Anda.
* Sesi yang di-host sendiri dapat menggunakan server MCP melalui tunnel maupun server MCP publik.

Gunakan keduanya ketika Anda ingin eksekusi dan akses alat tetap berada di dalam batas Anda. Untuk melewati tunnel, [bungkus server MCP sebagai alat kustom](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools#wrap-an-mcp-server-as-custom-tools) yang dilayani oleh worker Anda.

## Panduan platform

Halaman-halaman ini menjelaskan cara membangun worker di platform sandboxing apa pun. Panduan khusus platform juga tersedia:

* [AWS Lambda MicroVMs](https://docs.aws.amazon.com/lambda/latest/dg/microvms-integrations-claude-managed-agents.html)
* [Blaxel](https://docs.blaxel.ai/Tutorials/Claude-Managed-Agents)
* [Cloudflare](https://developers.cloudflare.com/sandbox/claude-managed-agents/)
* [Daytona](https://www.daytona.io/docs/en/guides/claude/claude-managed-agents)
* [E2B](https://e2b.dev/docs/agents/claude-managed-agents)
* [Fly.io](https://docs.sprites.dev/integrations/claude-managed-agents/)
* [GKE Agent Sandbox](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/tree/main/ai-ml/anthropic-agent-sandbox)
* [Modal](https://github.com/modal-labs/claude-managed-agents-modal-sandbox)
* [Namespace](https://namespace.so/docs/integrations/claude)
* [Superserve](https://docs.superserve.ai/integrations/managed-agents/claude-managed-agents)
* [Vercel](https://vercel.com/kb/guide/run-claude-managed-agent-tools-with-vercel-sandbox)

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Deploy worker" icon="play" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers">
    Jalankan worker SDK, picu worker dari webhook, atau berikan sandbox tersendiri untuk setiap sesi.
  </Card>

  <Card title="Memory store" icon="brain" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory">
    Siapkan host, konfigurasikan sinkronisasi, dan tangani store hanya-baca serta konflik.
  </Card>

  <Card title="Alat kustom dan server MCP" icon="tool" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools">
    Layani alat Anda sendiri dari worker, termasuk alat dari server MCP di dalam jaringan Anda.
  </Card>

  <Card title="Pemantauan dan pemecahan masalah" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations">
    Baca kedalaman antrean, hentikan sesi dan worker dengan bersih, dan perbaiki kegagalan umum.
  </Card>

  <Card title="Referensi worker" icon="book" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference">
    Flag CLI, variabel lingkungan, path sistem file, dan opsi helper SDK.
  </Card>

  <Card title="Model keamanan" icon="lock" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security">
    Model tanggung jawab bersama untuk lingkungan sandbox yang di-host sendiri.
  </Card>
</CardGroup>
