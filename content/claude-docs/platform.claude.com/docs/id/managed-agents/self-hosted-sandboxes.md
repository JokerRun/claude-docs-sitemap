---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes
fetched_at: 2026-10-09T02:29:51.005508Z
sha256: ad5992b56ad21feacc06ec51a9d5585a5140aefe8ca755da21ee91e8510839dd
---

---
title: Sandbox self-hosted
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes
description: Jalankan sesi Claude Managed Agents di sandbox self-hosted, sehingga eksekusi alat, file, dan egress jaringan tetap berada di infrastruktur Anda sendiri.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Secara default, Managed Agents mengeksekusi alat dan kode di dalam [sandbox cloud yang dikelola Anthropic](https://platform.claude.com/docs/id/managed-agents/cloud-sandboxes-reference). Sandbox self-hosted tetap menjalankan orkestrasi di sisi Anthropic, tetapi memindahkan eksekusi alat ke infrastruktur yang Anda kendalikan. File, proses, dan lalu lintas jaringan agen tetap berada di lingkungan Anda.

Self-hosting cocok ketika agen perlu:

* Beroperasi pada data yang tidak boleh keluar dari batas jaringan Anda
* Menjangkau layanan internal yang tidak dapat dirutekan secara publik
* Berjalan di bawah kontrol kepatuhan dan audit milik organisasi Anda sendiri

## Cara kerjanya

Environment `self_hosted` berfungsi sebagai antrean kerja. Anda menjalankan **environment worker** (worker lingkungan), yaitu proses di infrastruktur Anda sendiri yang melayani antrean tersebut:

1. Anda membuat [sesi](https://platform.claude.com/docs/id/managed-agents/sessions) yang menargetkan environment tersebut. Anthropic memasukkan sesi ke antrean sebagai work item.
2. Worker Anda mengklaim work item tersebut dan mengunduh [skill](https://platform.claude.com/docs/id/managed-agents/skills) milik agen serta [memory store](https://platform.claude.com/docs/id/managed-agents/memory) milik sesi.
3. Claude berjalan di sisi Anthropic dan meminta pemanggilan alat. Worker Anda menjalankan setiap pemanggilan secara lokal dan mengirimkan hasilnya kembali.

Input dan output alat tetap mengalir ke control plane Anthropic, sehingga model dapat melihat hasilnya dan menentukan langkah berikutnya. Anthropic menyimpan skill dan memory store. Sandbox Anda menyimpan salinannya untuk sesi tersebut. Lihat [Model keamanan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security) untuk batas aliran data selengkapnya.

Sandbox self-hosted mendukung setiap model Claude yang tersedia di Managed Agents. Model dikonfigurasi pada agen, bukan pada environment.

CLI `ant` serta SDK Python, TypeScript, dan Go menyertakan worker siap pakai. Penyedia sandbox seperti Cloudflare, Daytona, dan Modal juga menerbitkan [panduan platform](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#platform-guides) mereka sendiri.

## Mulai cepat

Panduan mulai cepat ini menjalankan satu worker always-on dengan CLI `ant`, mengirimkan sebuah sesi kepadanya, dan memastikan bahwa pemanggilan alat agen berjalan di host Anda.

### Prasyarat

* **Sebuah agen:** Jika Anda belum memilikinya, selesaikan [Memulai dengan Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/quickstart) terlebih dahulu dan catat ID agennya.
* **Host Linux:** Host memerlukan `/bin/bash` tepat di path tersebut. Worker hanya memerlukan HTTPS keluar.
* **Kunci API Claude:** Anda menggunakannya dari mesin Anda sendiri untuk membuat sesi dan membaca statistik antrean. Jauhkan kunci ini dari host worker, tempat pemanggilan alat agen dapat membacanya.
* **CLI `ant` di mesin Anda sendiri:** Perintah sesi dan statistik dalam panduan mulai cepat ini dijalankan di sana, bukan di host worker. Instal dengan cara yang sama seperti [langkah instalasi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#run-your-first-session) untuk worker.

<Note>
  Di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), worker melakukan autentikasi dengan AWS IAM (SigV4) atau [kunci API yang dibuat di AWS Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#api-key-authentication), bukan environment key. Lampirkan managed policy [`AnthropicSelfHostedEnvironmentAccess`](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#managed-policies) ke principal IAM yang digunakan untuk menjalankan worker Anda. Environment key yang dibuat di Claude Console tidak berfungsi dengan endpoint Claude Platform on AWS.
</Note>

### Jalankan sesi pertama Anda

<Steps>
  <Step title="Buat environment self-hosted">
    Di [Console](https://platform.claude.com/workspaces/default/environments): **Workspace > Environments > New > Self-hosted**

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
    Di Console, buka environment tersebut dan klik **Generate environment key**. Environment key mengautentikasi worker ke antreannya. Anda hanya dapat membuatnya di Console, bahkan untuk environment yang Anda buat melalui API.

    Ekspor ID environment dan environment key di host worker:

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
        VERSION=1.39.1
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
    Di mesin Anda sendiri, atur `ANTHROPIC_API_KEY` ke kunci API Claude Anda (bukan environment key) dan `ANTHROPIC_ENVIRONMENT_ID` ke ID environment. Pastikan bahwa `workers_polling` bernilai setidaknya 1:

    ```bash
    ant beta:environments:work stats --environment-id "$ANTHROPIC_ENVIRONMENT_ID"
    ```

    Jika `workers_polling` tetap bernilai 0, lihat [Pemecahan masalah](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#troubleshooting).
  </Step>

  <Step title="Mulai sesi">
    Atur `AGENT_ID` ke ID agen Anda. Buat sesi yang menargetkan environment tersebut, lalu kirimkan sebuah tugas:

    ```bash
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

    Sesi menunggu di antrean environment hingga sebuah worker mengklaimnya. Jika tidak ada worker yang terhubung, sesi tetap berada dalam antrean alih-alih gagal.
  </Step>

  <Step title="Pastikan alat berjalan di host Anda">
    Di host worker, baca file yang ditulis oleh agen:

    ```bash
    cat /workspace/hello.txt
    ```

    File tersebut mendeskripsikan kernel host Anda sendiri, jadi pemanggilan alat agen berjalan di sana. Untuk mengikuti pekerjaan agen secara langsung, lihat [Aliran event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming).
  </Step>
</Steps>

## Perbedaannya dengan environment cloud

|                               | Environment cloud                         | Sandbox self-hosted                                    |
| ----------------------------- | ----------------------------------------- | ------------------------------------------------------ |
| Tempat alat berjalan          | Sandbox yang dikelola Anthropic           | Infrastruktur Anda                                     |
| Jangkauan jaringan            | Kontrol egress Anthropic                  | Kebijakan jaringan Anda                                |
| Mounting file dan repo GitHub | Dikelola oleh Anthropic                   | Dikelola oleh Anda                                     |
| Memory store                  | Di-mount oleh Anthropic di `/mnt/memory/` | Diunduh ke `/mnt/memory/` dan disinkronkan oleh worker |
| Siklus hidup                  | Dikelola oleh Anthropic                   | Dikelola oleh Anda                                     |

Untuk kelayakan Zero Data Retention dan HIPAA BAA, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

### Sumber daya sesi

Sandbox self-hosted hanya mendukung sumber daya `memory_store`. Sesi pada environment self-hosted yang menyertakan sumber daya `file` atau `github_repository` akan ditolak dengan error 400:

```text wrap
Environment env_... is a self-hosted environment. `resources` are not supported with self-hosted environments.
```

[Deployment](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments) yang menargetkan environment self-hosted mengikuti aturan yang sama. Untuk memberikan file input tersendiri kepada sebuah sesi, lihat [Menyiapkan file untuk sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#stage-files-for-a-session).

## Sandbox self-hosted dan tunnel MCP

Self-hosting mengontrol *di mana kode agen dieksekusi*. [Tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) mengontrol *bagaimana Anthropic menjangkau server MCP di jaringan Anda*. Keduanya independen:

* Sesi di sandbox cloud Anthropic dapat menjangkau server MCP privat melalui tunnel.
* Sesi self-hosted dapat menggunakan server MCP melalui tunnel maupun server MCP publik.

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
  <Card title="Menerapkan worker" icon="play" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers">
    Jalankan worker SDK, picu worker dari webhook, atau berikan sandbox tersendiri untuk setiap sesi.
  </Card>

  <Card title="Memory store" icon="brain" href="https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory">
    Siapkan host, konfigurasikan sinkronisasi, dan tangani store read-only serta konflik.
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
    Model tanggung jawab bersama untuk lingkungan sandbox self-hosted.
  </Card>
</CardGroup>
