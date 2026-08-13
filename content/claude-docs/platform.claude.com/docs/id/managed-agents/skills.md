---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/skills
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: f613df721c29d60dceec827b4b2d58800f142211fec8dfc2144c3bdd2f2ccd06
---

---
title: Skills
url: https://platform.claude.com/docs/id/managed-agents/skills
description: Lampirkan keahlian berbasis sistem file yang dapat digunakan kembali ke agen Anda untuk alur kerja spesifik domain.
---

Skills adalah sumber daya berbasis sistem file yang dapat digunakan kembali yang memberikan keahlian spesifik domain kepada agen Anda: alur kerja, konteks, dan praktik terbaik yang mengubah agen serbaguna menjadi spesialis. Setiap skill yang Anda tambahkan menimbulkan biaya kecil pada "context window" (jendela konteks) sesi, menambahkan instruksi dan metadata yang membantu model menggunakan skill tersebut. Pelajari lebih lanjut di ikhtisar [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview).

Skills mencapai agen Anda melalui dua cara: lampirkan melalui array `skills` milik agen, atau [muat dari repositori GitHub](https://platform.claude.com/docs/id/managed-agents/skills#load-skills-from-a-github-repository) yang di-mount pada sesi. Skills yang dilampirkan terdiri dari dua jenis. Semua skills bekerja dengan cara yang sama: agen Anda memanggilnya secara otomatis ketika relevan dengan tugas.

* **Skills bawaan Anthropic:** Tugas dokumen umum seperti penanganan PowerPoint, Excel, Word, dan PDF (`pptx`, `xlsx`, `docx`, `pdf`).
* **Skills kustom:** Skills yang Anda tulis dan unggah ke workspace Anda.

Untuk mempelajari cara menulis skills kustom, lihat [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview) dan [Praktik terbaik penulisan skill](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices). Untuk mengunggah skill kustom ke workspace Anda, lihat [Membuat skill kustom](https://platform.claude.com/docs/id/managed-agents/skills#create-a-custom-skill).

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Membuat skill kustom

Skill kustom adalah direktori yang berisi file `SKILL.md` beserta file pendukung lainnya, diunggah ke workspace Anda sebagai arsip zip atau sebagai file individual. Membuat skill akan mengembalikan ID `skill_*` yang Anda referensikan saat melampirkannya ke agen. Skills bawaan Anthropic sudah tersedia di setiap workspace dan tidak memerlukan langkah ini. Untuk hanya menggunakan skills bawaan, lewati ke [Melampirkan skills ke agen](https://platform.claude.com/docs/id/managed-agents/skills#attach-skills-to-an-agent).

Ketika Anda memanggil Skills API secara langsung dengan cURL, sertakan header `anthropic-beta: skills-2025-10-02` secara eksplisit. CLI dan SDK mengirimkannya secara otomatis.

Contoh-contoh ini menghilangkan field opsional `display_title`, sehingga judul skill diturunkan dari `SKILL.md`. `display_title` yang diteruskan secara eksplisit harus unik di antara skills kustom dalam workspace Anda.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "files[]=@example_skill.zip"
  ```

  ```bash CLI
  ant beta:skills create \
    --file example_skill.zip
  ```

  ```python Python
  import anthropic
  from anthropic.lib import files_from_dir

  client = anthropic.Anthropic()

  skill = client.beta.skills.create(
      files=files_from_dir("example_skill"),
  )

  print(f"Created skill: {skill.id}")
  print(f"Latest version: {skill.latest_version}")
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { toFile } from "@anthropic-ai/sdk";
  import fs from "node:fs";

  const client = new Anthropic();

  const skill = await client.beta.skills.create({
    files: [await toFile(fs.createReadStream("example_skill.zip"), "example_skill.zip")]
  });

  console.log(`Created skill: ${skill.id}`);
  console.log(`Latest version: ${skill.latest_version}`);
  ```

  ```csharp C#
  using System.IO;
  using Anthropic;
  using Anthropic.Models.Beta.Skills;

  AnthropicClient client = new();

  var parameters = new SkillCreateParams
  {
      Files = [
          new FileStream("example_skill.zip", FileMode.Open, FileAccess.Read)
      ],
  };

  var skill = await client.Beta.Skills.Create(parameters);

  Console.WriteLine($"Created skill: {skill.ID}");
  Console.WriteLine($"Latest version: {skill.LatestVersion}");
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"io"
  	"log"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	client := anthropic.NewClient()

  	zipFile, err := os.Open("example_skill.zip")
  	if err != nil {
  		log.Fatal(err)
  	}
  	defer zipFile.Close()

  	skill, err := client.Beta.Skills.New(context.TODO(), anthropic.BetaSkillNewParams{
  		Files: []io.Reader{zipFile},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	fmt.Printf("Created skill: %s\n", skill.ID)
  	fmt.Printf("Latest version: %s\n", skill.LatestVersion)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.beta.skills.SkillCreateParams;
  import com.anthropic.models.beta.skills.SkillCreateResponse;
  import java.io.IOException;
  import java.io.InputStream;
  import java.nio.file.Files;
  import java.nio.file.Path;

  void main() throws IOException {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      SkillCreateParams params = SkillCreateParams.builder()
          .addFile(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("example_skill.zip")))
              .filename("example_skill.zip")
              .contentType("application/zip")
              .build())
          .build();

      SkillCreateResponse skill = client.beta().skills().create(params);

      IO.println("Created skill: " + skill.id());
      IO.println("Latest version: " + skill.latestVersion().orElseThrow());
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Client;
  use Anthropic\Core\FileParam;

  $client = new Client();

  $skill = $client->beta->skills->create(
      files: [
          FileParam::fromResource(fopen('example_skill.zip', 'r'))
      ],
  );

  echo "Created skill: {$skill->id}\n";
  echo "Latest version: {$skill->latestVersion}\n";
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  skill = client.beta.skills.create(
    files: [
      File.open("example_skill.zip", "rb")
    ]
  )

  puts "Created skill: #{skill.id}"
  puts "Latest version: #{skill.latest_version}"
  ```
</CodeGroup>

Untuk membuat daftar, mengambil, menghapus, dan membuat versi skills kustom, lihat [Mengelola skills kustom](https://platform.claude.com/docs/id/build-with-claude/skills-guide#managing-custom-skills). Untuk skema permintaan dan respons lengkap, lihat [referensi API Create Skill](https://platform.claude.com/docs/id/api/beta/skills/create). Bundel skill diunggah langsung ke Skills API, bukan melalui [Files API](https://platform.claude.com/docs/id/build-with-claude/files).

## Melampirkan skills ke agen

Lampirkan skills saat membuat agen. Setiap [sesi](https://platform.claude.com/docs/id/managed-agents/sessions) mendukung hingga 500 skills, dihitung sebagai himpunan yang telah dideduplikasi di seluruh agen dalam sesi (lihat [Orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration)).

<Note>
  Me-mount lebih banyak skills meningkatkan waktu yang diperlukan sandbox sesi untuk memulai. Lampirkan hanya skills yang dibutuhkan setiap agen untuk tugasnya.
</Note>

Setiap entri dalam array `skills` menggunakan field berikut:

| Field      | Deskripsi                                                                                                                                                                                                                                                                           |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`     | Bernilai `anthropic` untuk skills bawaan atau `custom` untuk skills yang ditulis di workspace.                                                                                                                                                                                      |
| `skill_id` | Pengidentifikasi skill. Untuk skills Anthropic, gunakan nama pendek (misalnya, `xlsx`). Untuk skills kustom, gunakan ID `skill_*` yang dikembalikan saat pembuatan (lihat [Membuat skill kustom](https://platform.claude.com/docs/id/managed-agents/skills#create-a-custom-skill)). |
| `version`  | Sematkan ke versi tertentu atau gunakan `latest`. Opsional. Default-nya adalah `latest` jika dihilangkan. Berlaku untuk skills Anthropic maupun kustom.                                                                                                                             |

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -sS https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    --json @- <<'EOF'
  {
    "name": "Financial Analyst",
    "model": "claude-opus-5",
    "system": "You are a financial analysis agent.",
    "skills": [
      {"type": "anthropic", "skill_id": "xlsx"},
      {"type": "custom", "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv", "version": "latest"}
    ]
  }
  EOF
  )
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Financial Analyst
  model: claude-opus-5
  system: You are a financial analysis agent.
  skills:
    - type: anthropic
      skill_id: xlsx
    - type: custom
      skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
      version: latest
  YAML
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Financial Analyst",
      model="claude-opus-5",
      system="You are a financial analysis agent.",
      skills=[
          {
              "type": "anthropic",
              "skill_id": "xlsx",
          },
          {
              "type": "custom",
              "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
              "version": "latest",
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Financial Analyst",
    model: "claude-opus-5",
    system: "You are a financial analysis agent.",
    skills: [
      {
        type: "anthropic",
        skill_id: "xlsx"
      },
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "latest"
      }
    ]
  });
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Agents;

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Financial Analyst",
      Model = BetaManagedAgentsModel.ClaudeOpus5,
      System = "You are a financial analysis agent.",
      Skills =
      [
          new BetaManagedAgentsAnthropicSkillParams { Type = BetaManagedAgentsAnthropicSkillParamsType.Anthropic, SkillID = "xlsx" },
          new BetaManagedAgentsCustomSkillParams { Type = BetaManagedAgentsCustomSkillParamsType.Custom, SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv", Version = "latest" },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Financial Analyst",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-5",
  	},
  	System: anthropic.String("You are a financial analysis agent."),
  	Skills: []anthropic.BetaManagedAgentsSkillParamsUnion{
  		{OfAnthropic: &anthropic.BetaManagedAgentsAnthropicSkillParams{
  			SkillID: "xlsx",
  			Type:    anthropic.BetaManagedAgentsAnthropicSkillParamsTypeAnthropic,
  		}},
  		{OfCustom: &anthropic.BetaManagedAgentsCustomSkillParams{
  			SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  			Type:    anthropic.BetaManagedAgentsCustomSkillParamsTypeCustom,
  			Version: anthropic.String("latest"),
  		}},
  	},
  })
  if err != nil {
  	panic(err)
  }
  _ = agent
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;

  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Financial Analyst")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
          .system("You are a financial analysis agent.")
          .addSkill(
              BetaManagedAgentsAnthropicSkillParams.builder()
                  .type(BetaManagedAgentsAnthropicSkillParams.Type.ANTHROPIC)
                  .skillId("xlsx")
                  .build()
          )
          .addSkill(
              BetaManagedAgentsCustomSkillParams.builder()
                  .type(BetaManagedAgentsCustomSkillParams.Type.CUSTOM)
                  .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                  .version("latest")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Financial Analyst',
      model: 'claude-opus-5',
      system: 'You are a financial analysis agent.',
      skills: [
          ['type' => 'anthropic', 'skill_id' => 'xlsx'],
          ['type' => 'custom', 'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv', 'version' => 'latest'],
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Financial Analyst",
    model: "claude-opus-5",
    system_: "You are a financial analysis agent.",
    skills: [
      {type: "anthropic", skill_id: "xlsx"},
      {type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest"}
    ]
  )
  ```
</CodeGroup>

## Memuat skills dari repositori GitHub

Skills juga dapat berada di dalam codebase Anda. Ketika sebuah sesi me-mount repositori melalui [resource `github_repository`](https://platform.claude.com/docs/id/managed-agents/github), direktori `.claude/skills` di root repositori dipindai saat sesi dimulai, dan setiap skill yang ditemukan di sana menjadi tersedia untuk agen. Tidak diperlukan unggahan dan tidak diperlukan entri dalam array `skills` milik agen. Agen melihat nama, deskripsi, dan path setiap skill yang ditemukan di dalam sandbox, dan membaca `SKILL.md` milik skill tersebut ketika sebuah tugas cocok, termasuk skrip dan sumber daya apa pun yang disertakan skill tersebut. Penemuan ini bergantung pada tool `read` milik agen dari [toolset agen](https://platform.claude.com/docs/id/managed-agents/tools), yang diaktifkan secara default; agen dengan `read` yang dinonaktifkan tidak memuat skills repositori.

<Warning>
  Skills repositori adalah instruksi agen, sehingga repositori yang di-mount merupakan bagian dari batas kepercayaan agen Anda. Siapa pun yang dapat melakukan commit ke repositori (pull request eksternal yang di-merge, dependensi yang disusupi, seorang kontributor) dapat menambahkan atau mengubah skill, platform memuatnya saat sesi dimulai tanpa langkah peninjauan, dan tool sesi seperti `bash` dan `web_fetch` memberikan instruksi tersebut jangkauan nyata. Mount hanya repositori yang Anda percaya, dan tinjau `.claude/skills` sebelum me-mount repositori yang menerima kontribusi dari luar.
</Warning>

<Note>
  Penemuan skill repositori berjalan di sandbox cloud. [Sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) tidak mendukung resource repositori GitHub.
</Note>

Penemuan menemukan skills tepat di `.claude/skills/<skill-name>/SKILL.md`, satu tingkat direktori di dalam root repositori:

```text wrap
your-repo/
├── .claude/
│   └── skills/
│       ├── code-review/
│       │   └── SKILL.md
│       └── release-process/
│           ├── SKILL.md
│           └── scripts/
│               └── run_checks.sh
└── src/
```

Lokasi yang tidak cocok dengan tata letak ini tidak ditemukan saat sesi dimulai:

* `.claude/skills/SKILL.md`: sebuah `SKILL.md` tanpa direktori skill yang membungkusnya
* `.claude/skills/tools/code-review/SKILL.md`: bersarang lebih dari satu tingkat direktori
* `skills/code-review/SKILL.md`: direktori `skills` di luar `.claude`

Direktori `.claude/skills` di tempat lain dalam repositori, seperti di dalam subdirektori paket, tidak diumumkan saat sesi dimulai; skills tersebut masih dapat muncul ketika agen membaca file di bawah subtree tersebut.

Skills repositori menggunakan format `SKILL.md` yang sama dengan skills kustom yang Anda unggah. Untuk format dan panduan penulisan, lihat [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview) dan [Praktik terbaik penulisan skill](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices).

Untuk memuat skills dari repositori, buat sesi yang me-mount repositori tersebut. Ini adalah permintaan yang sama seperti yang ditunjukkan di [Mengakses GitHub](https://platform.claude.com/docs/id/managed-agents/github#token-permissions); `mount_path` bersifat opsional dan default-nya adalah `/workspace/<repo-name>`:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  session_id=$(curl -fsS https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<JSON | jq -r '.id'
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id",
    "resources": [
      {
        "type": "github_repository",
        "url": "https://github.com/org/repo",
        "mount_path": "/workspace/repo",
        "authorization_token": "ghp_your_github_token"
      }
    ]
  }
  JSON
  )
  ```

  ```bash CLI
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --transform id --raw-output <<'EOF'
  resources:
    - type: github_repository
      url: https://github.com/org/repo
      mount_path: /workspace/repo
      authorization_token: ghp_your_github_token
  EOF
  )
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      resources=[
          {
              "type": "github_repository",
              "url": "https://github.com/org/repo",
              "mount_path": "/workspace/repo",
              "authorization_token": "ghp_your_github_token",
          },
      ],
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "github_repository",
        url: "https://github.com/org/repo",
        mount_path: "/workspace/repo",
        authorization_token: "ghp_your_github_token",
      },
    ],
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Resources =
      [
          new BetaManagedAgentsGitHubRepositoryResourceParams
          {
              Type = "github_repository",
              Url = "https://github.com/org/repo",
              MountPath = "/workspace/repo",
              AuthorizationToken = "ghp_your_github_token",
          },
      ],
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
  	EnvironmentID: environment.ID,
  	Resources: []anthropic.BetaSessionNewParamsResourceUnion{
  		{
  			OfGitHubRepository: &anthropic.BetaManagedAgentsGitHubRepositoryResourceParams{
  				Type:               anthropic.BetaManagedAgentsGitHubRepositoryResourceParamsTypeGitHubRepository,
  				URL:                "https://github.com/org/repo",
  				MountPath:          anthropic.String("/workspace/repo"),
  				AuthorizationToken: "ghp_your_github_token",
  			},
  		},
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
      .addResource(BetaManagedAgentsGitHubRepositoryResourceParams.builder()
          .type(BetaManagedAgentsGitHubRepositoryResourceParams.Type.GITHUB_REPOSITORY)
          .url("https://github.com/org/repo")
          .mountPath("/workspace/repo")
          .authorizationToken("ghp_your_github_token")
          .build())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      resources: [
          [
              'type' => 'github_repository',
              'url' => 'https://github.com/org/repo',
              'mountPath' => '/workspace/repo',
              'authorizationToken' => 'ghp_your_github_token',
          ],
      ],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "github_repository",
        url: "https://github.com/org/repo",
        mount_path: "/workspace/repo",
        authorization_token: "ghp_your_github_token"
      }
    ]
  )
  ```
</CodeGroup>

Untuk repositori privat, `authorization_token` milik resource harus memiliki akses ke repositori tersebut. Ini adalah alur personal access token yang sama yang digunakan untuk mount repositori apa pun; lihat [Mengakses GitHub](https://platform.claude.com/docs/id/managed-agents/github#token-permissions).

Skills yang ditemukan mengikuti keadaan checkout dari repositori: branch atau commit `checkout` ketika resource menetapkannya, jika tidak maka branch default repositori. Pemindaian berjalan sekali, saat sesi dimulai. Commit yang di-push di tengah sesi tidak diambil; untuk memuat skills yang diperbarui, mulai sesi baru.

Skills repositori bekerja berdampingan dengan skills yang dilampirkan melalui array `skills` milik agen. Jika sebuah skill repositori memiliki nama yang sama dengan skill yang dilampirkan, atau dengan skill dari repositori lain yang di-mount, keduanya tersedia; masing-masing diumumkan dengan path-nya sendiri.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Penyiapan lingkungan cloud" icon="settings" href="https://platform.claude.com/docs/id/managed-agents/environments">
    Sesuaikan sandbox cloud untuk sesi Anda.
  </Card>

  <Card title="Menggunakan Agent Skills dengan API" icon="code" href="https://platform.claude.com/docs/id/build-with-claude/skills-guide">
    Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.
  </Card>

  <Card title="Files API" icon="file" href="https://platform.claude.com/docs/id/build-with-claude/files">
    Unggah file sekali dan referensikan di seluruh permintaan API.
  </Card>

  <Card title="Memulai dengan Agent Skills di API" icon="graduation-cap" href="https://platform.claude.com/docs/id/agents-and-tools/agent-skills/quickstart">
    Pelajari cara menggunakan Agent Skills untuk membuat dokumen dengan Claude API dalam waktu kurang dari 10 menit.
  </Card>
</CardGroup>
