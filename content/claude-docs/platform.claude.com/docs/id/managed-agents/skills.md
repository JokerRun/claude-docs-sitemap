---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/skills
fetched_at: 2026-07-02T03:13:49.360020Z
sha256: b5ac61d90057cd201c10fada41402a3c19a70f5183dd90bded6b858b8b995eba
---

# Skills

Lampirkan keahlian berbasis sistem file yang dapat digunakan kembali ke agen Anda untuk alur kerja spesifik domain.

---

Skills adalah sumber daya berbasis sistem file yang dapat digunakan kembali yang memberikan keahlian spesifik domain kepada agen Anda: alur kerja, konteks, dan praktik terbaik yang mengubah agen serbaguna menjadi spesialis. Tidak seperti prompt (instruksi tingkat percakapan untuk tugas satu kali), skills dimuat sesuai permintaan, hanya memengaruhi "context window" (jendela konteks) saat diperlukan.

Anda dapat melampirkan dua jenis skill. Keduanya bekerja dengan cara yang sama: agen Anda memanggilnya secara otomatis ketika relevan dengan tugas.

* **Skill bawaan Anthropic:** Tugas dokumen umum seperti penanganan PowerPoint, Excel, Word, dan PDF (`pptx`, `xlsx`, `docx`, `pdf`).
* **Skill kustom:** Skill yang Anda buat dan unggah ke workspace Anda.

Untuk mempelajari cara membuat skill kustom, lihat [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) dan [Praktik terbaik pembuatan skill](/docs/id/agents-and-tools/agent-skills/best-practices). Untuk mengunggah skill kustom ke workspace Anda, lihat [Membuat skill kustom](#create-a-custom-skill).

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Membuat skill kustom

Skill kustom adalah direktori yang berisi file `SKILL.md` beserta file pendukung lainnya, yang diunggah ke workspace Anda sebagai arsip zip atau sebagai file individual. Membuat skill akan mengembalikan ID `skill_*` yang Anda referensikan saat melampirkannya ke agen. Skill bawaan Anthropic sudah tersedia di setiap workspace dan tidak memerlukan langkah ini. Untuk hanya menggunakan skill bawaan, lewati ke [Melampirkan skill ke agen](#attach-skills-to-an-agent).

Saat Anda memanggil Skills API secara langsung dengan cURL atau CLI, sertakan header `anthropic-beta: skills-2025-10-02` secara eksplisit. SDK mengirimkannya secara otomatis.

Contoh-contoh ini menghilangkan field opsional `display_title`, sehingga judul skill diturunkan dari `SKILL.md`. `display_title` yang diteruskan secara eksplisit harus unik di antara skill kustom dalam workspace Anda.

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
    --file example_skill.zip \
    --beta skills-2025-10-02
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
  import java.util.List;

  public class SkillCreate {
      public static void main(String[] args) throws IOException {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          SkillCreateParams params = SkillCreateParams.builder()
              .files(MultipartField.<List<InputStream>>builder()
                  .value(List.of(Files.newInputStream(Path.of("example_skill.zip"))))
                  .filename("example_skill.zip")
                  .contentType("application/zip")
                  .build())
              .build();

          SkillCreateResponse skill = client.beta().skills().create(params);

          System.out.println("Created skill: " + skill.id());
          System.out.println("Latest version: " + skill.latestVersion().orElseThrow());
      }
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

Untuk membuat daftar, mengambil, menghapus, dan membuat versi skill kustom, lihat [Mengelola skill kustom](/docs/id/build-with-claude/skills-guide#managing-custom-skills). Untuk skema permintaan dan respons lengkap, lihat [referensi Create Skill API](/docs/id/api/beta/skills/create). Bundel skill diunggah langsung ke Skills API, bukan melalui [Files API](/docs/id/build-with-claude/files).

## Melampirkan skill ke agen

Lampirkan skill saat membuat agen. Setiap [sesi](/docs/id/managed-agents/sessions) mendukung hingga 20 skill secara total, dihitung di seluruh agen dalam sesi tersebut (lihat [Sesi multi-agen](/docs/id/managed-agents/multi-agent)).

Setiap entri dalam array `skills` menggunakan field berikut:

| Field      | Deskripsi                                                                                                                                                                                                                |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `type`     | Bernilai `anthropic` untuk skill bawaan atau `custom` untuk skill yang dibuat di workspace.                                                                                                                              |
| `skill_id` | Pengidentifikasi skill. Untuk skill Anthropic, gunakan nama pendek (misalnya, `xlsx`). Untuk skill kustom, gunakan ID `skill_*` yang dikembalikan saat pembuatan (lihat [Membuat skill kustom](#create-a-custom-skill)). |
| `version`  | Hanya untuk skill kustom. Sematkan ke versi tertentu atau gunakan `latest`. Opsional. Default-nya adalah `latest` jika dihilangkan.                                                                                      |

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -sS https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    --json @- <<'EOF'
  {
    "name": "Financial Analyst",
    "model": "claude-opus-4-8",
    "system": "You are a financial analysis agent.",
    "skills": [
      {"type": "anthropic", "skill_id": "xlsx"},
      {"type": "custom", "skill_id": "skill_abc123", "version": "latest"}
    ]
  }
  EOF
  )
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Financial Analyst
  model: claude-opus-4-8
  system: You are a financial analysis agent.
  skills:
    - type: anthropic
      skill_id: xlsx
    - type: custom
      skill_id: skill_abc123
      version: latest
  YAML
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Financial Analyst",
      model="claude-opus-4-8",
      system="You are a financial analysis agent.",
      skills=[
          {
              "type": "anthropic",
              "skill_id": "xlsx",
          },
          {
              "type": "custom",
              "skill_id": "skill_abc123",
              "version": "latest",
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Financial Analyst",
    model: "claude-opus-4-8",
    system: "You are a financial analysis agent.",
    skills: [
      {
        type: "anthropic",
        skill_id: "xlsx"
      },
      {
        type: "custom",
        skill_id: "skill_abc123",
        version: "latest"
      }
    ]
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Financial Analyst",
      Model = BetaManagedAgentsModel.ClaudeOpus4_8,
      System = "You are a financial analysis agent.",
      Skills =
      [
          new BetaManagedAgentsAnthropicSkillParams { Type = BetaManagedAgentsAnthropicSkillParamsType.Anthropic, SkillID = "xlsx" },
          new BetaManagedAgentsCustomSkillParams { Type = BetaManagedAgentsCustomSkillParamsType.Custom, SkillID = "skill_abc123", Version = "latest" },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Financial Analyst",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-4-8",
  	},
  	System: anthropic.String("You are a financial analysis agent."),
  	Skills: []anthropic.BetaManagedAgentsSkillParamsUnion{
  		{OfAnthropic: &anthropic.BetaManagedAgentsAnthropicSkillParams{
  			SkillID: "xlsx",
  			Type:    anthropic.BetaManagedAgentsAnthropicSkillParamsTypeAnthropic,
  		}},
  		{OfCustom: &anthropic.BetaManagedAgentsCustomSkillParams{
  			SkillID: "skill_abc123",
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
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Financial Analyst")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
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
                  .skillId("skill_abc123")
                  .version("latest")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Financial Analyst',
      model: 'claude-opus-4-8',
      system: 'You are a financial analysis agent.',
      skills: [
          ['type' => 'anthropic', 'skill_id' => 'xlsx'],
          ['type' => 'custom', 'skill_id' => 'skill_abc123', 'version' => 'latest'],
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Financial Analyst",
    model: "claude-opus-4-8",
    system_: "You are a financial analysis agent.",
    skills: [
      {type: "anthropic", skill_id: "xlsx"},
      {type: "custom", skill_id: "skill_abc123", version: "latest"}
    ]
  )
  ```
</CodeGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Penyiapan lingkungan cloud" icon="settings" href="/docs/id/managed-agents/environments">
    Sesuaikan sandbox cloud untuk sesi Anda.
  </Card>

  <Card title="Menggunakan Agent Skills dengan API" icon="code" href="/docs/id/build-with-claude/skills-guide">
    Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.
  </Card>

  <Card title="Files API" icon="file" href="/docs/id/build-with-claude/files">
    Unggah file sekali dan referensikan di seluruh permintaan API.
  </Card>

  <Card title="Memulai dengan Agent Skills di API" icon="graduation-cap" href="/docs/id/agents-and-tools/agent-skills/quickstart">
    Pelajari cara menggunakan Agent Skills untuk membuat dokumen dengan Claude API dalam waktu kurang dari 10 menit.
  </Card>
</CardGroup>
