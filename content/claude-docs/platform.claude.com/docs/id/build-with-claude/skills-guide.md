---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/skills-guide
fetched_at: 2026-08-21T02:32:13.524433Z
sha256: fa32d261cb43a2e39090bd7c7ae4e278b9892a6c1531f9a296b7d5b6577a201a
---

---
title: Menggunakan Agent Skills dengan API
url: https://platform.claude.com/docs/id/build-with-claude/skills-guide
description: Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.
---

Agent Skills memperluas kemampuan Claude melalui folder terorganisir yang berisi instruksi, skrip, dan sumber daya. Panduan ini menunjukkan cara menggunakan Skill bawaan maupun Skill kustom dengan Claude API.

<Note>
  Untuk referensi API lengkap termasuk skema permintaan/respons dan semua parameter, lihat:

  * [Referensi API Manajemen Skill](https://platform.claude.com/docs/id/api/beta/skills/list) - Operasi CRUD untuk Skill
  * [Referensi API Versi Skill](https://platform.claude.com/docs/id/api/beta/skills/versions/list) - Manajemen versi
</Note>

<Note>
  Untuk mengetahui bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku pada fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

## Tautan cepat

<CardGroup cols={2}>
  <Card title="Memulai dengan Agent Skills di API" icon="rocket" href="https://platform.claude.com/docs/id/agents-and-tools/agent-skills/quickstart">
    Pelajari cara menggunakan Agent Skills untuk membuat dokumen dengan Claude API dalam waktu kurang dari 10 menit.
  </Card>

  <Card title="Praktik terbaik penulisan Skill" icon="hammer" href="https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices">
    Pelajari cara menulis Skill yang efektif agar Claude dapat menemukan dan menggunakannya dengan sukses.
  </Card>
</CardGroup>

## Ikhtisar

<Note>
  Untuk melihat secara mendetail arsitektur dan penerapan Agent Skills di dunia nyata, baca postingan blog teknik: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

Skill terintegrasi dengan Messages API melalui [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool). Baik menggunakan Skill bawaan yang dikelola oleh Anthropic maupun Skill kustom yang telah Anda unggah, bentuk integrasinya identik: keduanya memerlukan eksekusi kode dan menggunakan struktur `container` yang sama.

### Menggunakan Skill

Skill terintegrasi secara identik di Messages API terlepas dari sumbernya. Anda menentukan Skill dalam parameter `container` dengan `skill_id`, `type`, dan `version` opsional, dan Skill tersebut berjalan di lingkungan eksekusi kode.

Anda dapat menggunakan Skill dari dua sumber:

| Aspek            | Skill Anthropic                            | Skill Kustom                                                                                       |
| ---------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| **Nilai type**   | `anthropic`                                | `custom`                                                                                           |
| **Skill ID**     | Nama pendek: `pptx`, `xlsx`, `docx`, `pdf` | Dihasilkan otomatis: `skill_01AbCdEfGhIjKlMnOpQrStUv`                                              |
| **Format versi** | Berbasis tanggal: `20251013` atau `latest` | ID versi: `skver_01AbCdEfGhIjKlMnOpQrStUv` atau `latest`                                           |
| **Pengelolaan**  | Dibuat dan dikelola oleh Anthropic         | Unggah dan kelola melalui [Skills API](https://platform.claude.com/docs/id/api/beta/skills/create) |
| **Ketersediaan** | Tersedia untuk semua pengguna              | Privat untuk workspace Anda                                                                        |

Kedua sumber Skill dikembalikan oleh [endpoint List Skills](https://platform.claude.com/docs/id/api/beta/skills/list) (gunakan parameter `source` untuk memfilter). Bentuk integrasi dan lingkungan eksekusinya identik. Satu-satunya perbedaan adalah dari mana Skill berasal dan bagaimana Skill dikelola.

### Prasyarat

Untuk menggunakan Skill, Anda memerlukan:

1. **Kunci API Claude** dari [Claude Console](https://platform.claude.com/settings/keys)
2. **[Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool)** diaktifkan dalam permintaan Anda

Skill tersedia secara umum di Claude API dan tidak memerlukan header `anthropic-beta`, baik untuk Skills API maupun untuk `container.skills` dalam permintaan Messages. Contoh-contoh dalam panduan ini tetap mengirimkan header beta `skills-2025-10-02` (ditambah `code-execution-2025-08-25` dalam permintaan Messages) dan menggunakan namespace `beta` dari SDK. Kedua header tetap merupakan opt-in yang valid, sehingga contoh-contoh tersebut berfungsi sebagaimana tertulis, dan Anda dapat menghilangkannya dalam permintaan Anda sendiri.

Skill memerlukan alat eksekusi kode, jadi gunakan model dari [daftar kompatibilitas modelnya](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility).

***

## Menggunakan Skill dalam Messages

### Parameter container

Skill ditentukan menggunakan parameter `container` di Messages API. Anda dapat menyertakan hingga 20 Skill untuk setiap permintaan.

Strukturnya identik untuk Skill Anthropic maupun kustom. Tentukan `type` dan `skill_id` yang wajib, dan secara opsional sertakan `version` untuk mengunci ke versi tertentu:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "anthropic",
            "skill_id": "pptx",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Create a presentation about renewable energy"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: pptx
        version: latest
  messages:
    - role: user
      content: Create a presentation about renewable energy
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
      },
      messages=[
          {"role": "user", "content": "Create a presentation about renewable energy"}
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        {
          type: "anthropic",
          skill_id: "pptx",
          version: "latest"
        }
      ]
    },
    messages: [
      {
        role: "user",
        content: "Create a presentation about renewable energy"
      }
    ],
    tools: [
      {
        type: "code_execution_20250825",
        name: "code_execution"
      }
    ]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "pptx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Create a presentation about renewable energy" }],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var message = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas: []anthropic.AnthropicBeta{
  		"code-execution-2025-08-25",
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "pptx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a presentation about renewable energy")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addBeta("code-execution-2025-08-25")
          .addBeta("skills-2025-10-02")
          .container(BetaContainerParams.builder()
              .addSkill(BetaSkillParams.builder()
                  .type(BetaSkillParams.Type.ANTHROPIC)
                  .skillId("pptx")
                  .version("latest")
                  .build())
              .build())
          .addUserMessage("Create a presentation about renewable energy")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response = client.beta().messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Create a presentation about renewable energy']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              [
                  'type' => 'anthropic',
                  'skill_id' => 'pptx',
                  'version' => 'latest'
              ]
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        {
          type: "anthropic",
          skill_id: "pptx",
          version: "latest"
        }
      ]
    },
    messages: [
      { role: "user", content: "Create a presentation about renewable energy" }
    ],
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )
  puts message
  ```
</CodeGroup>

### Mengunduh file yang dihasilkan

Ketika Skill membuat dokumen (Excel, PowerPoint, PDF, Word), Skill mengembalikan atribut `file_id` dalam respons. Anda harus menggunakan Files API untuk mengunduh file-file ini.

**Cara kerjanya:**

1. Skill membuat file selama eksekusi kode.
2. Respons menyertakan `file_id` untuk setiap file yang dibuat, di dalam blok hasil alat eksekusi kode (lihat [Format respons](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#response-format)).
3. Gunakan Files API untuk mengunduh konten file yang sebenarnya.
4. Simpan secara lokal atau proses sesuai kebutuhan.

Untuk menyediakan file input agar dapat diproses oleh Skill, [unggah file tersebut dengan Files API](https://platform.claude.com/docs/id/build-with-claude/files#uploading-a-file) dan referensikan dalam permintaan Anda dengan [blok unggahan container](https://platform.claude.com/docs/id/build-with-claude/files#container-upload-blocks).

**Contoh: membuat dan mengunduh file Excel**

<CodeGroup>
  ```bash cURL
  # Langkah 1: Gunakan Skill untuk membuat file
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Create an Excel file with a simple budget spreadsheet"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }')

  # Langkah 2: Ekstrak file_id dari respons (menggunakan jq)
  FILE_ID=$(echo "$RESPONSE" | jq -r '.content[] | select(.type=="bash_code_execution_tool_result") | .content | select(.type=="bash_code_execution_result") | .content[] | select(.file_id) | .file_id')

  # Langkah 3: Dapatkan nama file dari metadata
  FILENAME=$(curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" | jq -r '.filename')

  # Langkah 4: Unduh file menggunakan Files API
  curl "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    --output "$FILENAME"

  echo "Downloaded: $FILENAME"
  ```

  ```bash CLI
  # Langkah 1: Gunakan Skill xlsx untuk membuat file
  # Langkah 2: Ekstrak file_id dari respons dengan --transform (path GJSON)
  FILE_ID=$(ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 \
    --transform 'content.#.content.content.#.file_id|@flatten|0' \
    --raw-output <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
  messages:
    - role: user
      content: Create an Excel file with a simple budget spreadsheet
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  )

  # Langkah 3: Dapatkan nama file dari metadata file
  FILENAME=$(ant beta:files retrieve-metadata \
    --file-id "$FILE_ID" \
    --transform filename \
    --raw-output)

  # Langkah 4: Unduh file menggunakan Files API
  ant beta:files download \
    --file-id "$FILE_ID" \
    --output "$FILENAME" > /dev/null

  printf 'Downloaded: %s\n' "$FILENAME"
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Langkah 1: Gunakan Skill untuk membuat file
  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Create an Excel file with a simple budget spreadsheet",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )


  # Langkah 2: Ekstrak ID file dari respons
  def extract_file_ids(response):
      file_ids = []
      for item in response.content:
          if item.type == "bash_code_execution_tool_result":
              content_item = item.content
              if content_item.type == "bash_code_execution_result":
                  # setiap item konten adalah blok bash_code_execution_output yang membawa file_id
                  for file in content_item.content:
                      file_ids.append(file.file_id)
      return file_ids


  # Langkah 3: Unduh file menggunakan Files API
  for file_id in extract_file_ids(response):
      file_metadata = client.beta.files.retrieve_metadata(file_id=file_id)
      file_content = client.beta.files.download(file_id=file_id)

      # Langkah 4: Simpan ke disk
      file_content.write_to_file(file_metadata.filename)
      print(f"Downloaded: {file_metadata.filename}")
  ```

  ```typescript TypeScript
  import { writeFile } from "node:fs/promises";

  const client = new Anthropic();

  // Langkah 1: Gunakan Skill untuk membuat file
  const response = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Create an Excel file with a simple budget spreadsheet"
      }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Langkah 2: Ekstrak ID file dari respons
  const fileIds: string[] = [];
  for (const block of response.content) {
    if (
      block.type === "bash_code_execution_tool_result" &&
      block.content.type === "bash_code_execution_result"
    ) {
      for (const outputBlock of block.content.content) {
        fileIds.push(outputBlock.file_id);
      }
    }
  }

  // Langkah 3: Unduh setiap file dan simpan ke disk
  for (const fileId of fileIds) {
    const fileMetadata = await client.beta.files.retrieveMetadata(fileId);
    const fileResponse = await client.beta.files.download(fileId);

    await writeFile(fileMetadata.filename, Buffer.from(await fileResponse.arrayBuffer()));
    console.log(`Downloaded: ${fileMetadata.filename}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Langkah 1: Gunakan Skill untuk membuat file
  var parameters = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Create an Excel file with a simple budget spreadsheet" }],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var response = await client.Beta.Messages.Create(parameters);

  // Langkah 2: Ekstrak ID file dari respons
  List<string> fileIds = [];
  foreach (var block in response.Content)
  {
      if (block.TryPickBashCodeExecutionToolResult(out var toolResult)
          && toolResult.Content.TryPickBetaBashCodeExecutionResultBlock(out var result))
      {
          foreach (var output in result.Content)
          {
              fileIds.Add(output.FileID);
          }
      }
  }

  // Langkah 3: Unduh setiap file dan simpan ke disk
  foreach (var fileId in fileIds)
  {
      var fileMetadata = await client.Beta.Files.RetrieveMetadata(fileId);
      using var download = await client.Beta.Files.Download(fileId);
      using var downloadStream = await download.ReadAsStream();
      using var outputFile = File.Create(fileMetadata.Filename);
      await downloadStream.CopyToAsync(outputFile);
      Console.WriteLine($"Downloaded: {fileMetadata.Filename}");
  }
  ```

  ```go Go
  func main() {
  	client := anthropic.NewClient()

  	// Langkah 1: Gunakan Skill untuk membuat file
  	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     "claude-opus-5",
  		MaxTokens: 4096,
  		Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
  		Container: anthropic.BetaMessageNewParamsContainerUnion{
  			OfContainers: &anthropic.BetaContainerParams{
  				Skills: []anthropic.BetaSkillParams{
  					{
  						Type:    anthropic.BetaSkillParamsTypeAnthropic,
  						SkillID: "xlsx",
  						Version: anthropic.String("latest"),
  					},
  				},
  			},
  		},
  		Messages: []anthropic.BetaMessageParam{
  			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create an Excel file with a simple budget spreadsheet")),
  		},
  		Tools: []anthropic.BetaToolUnionParam{
  			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Langkah 2: Ekstrak ID file dari respons
  	fileIDs := extractFileIDs(response)

  	// Langkah 3: Unduh file menggunakan Files API
  	for _, fileID := range fileIDs {
  		fileMetadata, err := client.Beta.Files.GetMetadata(context.TODO(), fileID, anthropic.BetaFileGetMetadataParams{})
  		if err != nil {
  			log.Fatal(err)
  		}

  		fileContent, err := client.Beta.Files.Download(context.TODO(), fileID, anthropic.BetaFileDownloadParams{})
  		if err != nil {
  			log.Fatal(err)
  		}

  		// Langkah 4: Simpan ke disk
  		out, err := os.Create(fileMetadata.Filename)
  		if err != nil {
  			log.Fatal(err)
  		}
  		if _, err := io.Copy(out, fileContent.Body); err != nil {
  			log.Fatal(err)
  		}
  		out.Close()
  		fileContent.Body.Close()
  		fmt.Printf("Downloaded: %s\n", fileMetadata.Filename)
  	}
  }

  func extractFileIDs(response *anthropic.BetaMessage) []string {
  	var fileIDs []string
  	for _, item := range response.Content {
  		switch v := item.AsAny().(type) {
  		case anthropic.BetaBashCodeExecutionToolResultBlock:
  			if v.Content.Type == "bash_code_execution_result" {
  				for _, output := range v.Content.Content {
  					fileIDs = append(fileIDs, output.FileID)
  				}
  			}
  		}
  	}
  	return fileIDs
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  import com.anthropic.models.beta.messages.BetaContentBlock;
  import com.anthropic.models.beta.files.FileMetadata;
  import com.anthropic.core.http.HttpResponse;
  // ...
  void main() throws Exception {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Langkah 1: Gunakan Skill untuk membuat file
      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addBeta("code-execution-2025-08-25")
          .addBeta("skills-2025-10-02")
          .container(BetaContainerParams.builder()
              .addSkill(BetaSkillParams.builder()
                  .type(BetaSkillParams.Type.ANTHROPIC)
                  .skillId("xlsx")
                  .version("latest")
                  .build())
              .build())
          .addUserMessage("Create an Excel file with a simple budget spreadsheet")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response = client.beta().messages().create(params);

      // Langkah 2: Ekstrak ID file dari respons
      List<String> fileIds = new ArrayList<>();
      for (BetaContentBlock block : response.content()) {
          if (block.isBashCodeExecutionToolResult()) {
              var content = block.asBashCodeExecutionToolResult().content();
              if (content.isBetaBashCodeExecutionResultBlock()) {
                  for (var outputBlock : content.asBetaBashCodeExecutionResultBlock().content()) {
                      fileIds.add(outputBlock.fileId());
                  }
              }
          }
      }

      // Langkah 3: Unduh file menggunakan Files API
      for (String fileId : fileIds) {
          FileMetadata fileMetadata = client.beta().files().retrieveMetadata(fileId);
          HttpResponse fileContent = client.beta().files().download(fileId);

          // Langkah 4: Simpan ke disk
          try (InputStream is = fileContent.body();
               FileOutputStream fos = new FileOutputStream(fileMetadata.filename())) {
              is.transferTo(fos);
          }
          System.out.println("Downloaded: " + fileMetadata.filename());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  // Langkah 1: Gunakan Skill untuk membuat file
  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Create an Excel file with a simple budget spreadsheet']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  // Langkah 2: Ekstrak ID file dari respons
  function extractFileIds($response) {
      $fileIds = [];
      foreach ($response->content as $item) {
          if ($item->type === 'bash_code_execution_tool_result') {
              $contentItem = $item->content;
              if ($contentItem->type === 'bash_code_execution_result') {
                  foreach ($contentItem->content as $file) {
                      $fileIds[] = $file->fileID;
                  }
              }
          }
      }
      return $fileIds;
  }

  // Langkah 3: Unduh file menggunakan Files API
  foreach (extractFileIds($response) as $fileId) {
      $fileMetadata = $client->beta->files->retrieveMetadata($fileId);
      $fileContent  = $client->beta->files->download($fileId);

      // Langkah 4: Simpan ke disk
      file_put_contents($fileMetadata->filename, $fileContent);
      echo "Downloaded: {$fileMetadata->filename}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Langkah 1: Gunakan Skill untuk membuat file
  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Create an Excel file with a simple budget spreadsheet"
      }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )

  # Langkah 2: Ekstrak ID file dari respons
  def extract_file_ids(response)
    file_ids = []
    response.content.each do |item|
      if item.type == :bash_code_execution_tool_result
        content_item = item.content
        if content_item.type == :bash_code_execution_result
          content_item.content.each do |file|
            file_ids << file.file_id
          end
        end
      end
    end
    file_ids
  end

  # Langkah 3: Unduh file menggunakan Files API
  extract_file_ids(response).each do |file_id|
    file_metadata = client.beta.files.retrieve_metadata(file_id)

    file_content = client.beta.files.download(file_id)

    # Langkah 4: Simpan ke disk
    File.binwrite(file_metadata.filename, file_content.read)
    puts "Downloaded: #{file_metadata.filename}"
  end
  ```
</CodeGroup>

**Operasi Files API tambahan:**

<CodeGroup>
  ```bash cURL
  # Dapatkan metadata file
  curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"

  # Daftar semua file
  curl "https://api.anthropic.com/v1/files" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"

  # Hapus file
  curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```

  ```bash CLI
  # Dapatkan metadata file
  ant beta:files retrieve-metadata \
    --file-id "$FILE_ID" \
    --transform '{filename,size_bytes}' \
    --format yaml

  # Daftar semua file
  ant beta:files list \
    --transform '{filename,created_at}' \
    --format yaml

  # Hapus file
  ant beta:files delete --file-id "$FILE_ID" >/dev/null
  ```

  ```python Python
  client = anthropic.Anthropic()
  file_id = "file_011CNha8iCJcU1wXNR6q4V8w"
  # Dapatkan metadata file
  file_info = client.beta.files.retrieve_metadata(file_id=file_id)
  print(f"Filename: {file_info.filename}, Size: {file_info.size_bytes} bytes")

  # Daftar semua file
  for file in client.beta.files.list():
      print(f"{file.filename} - {file.created_at}")

  # Hapus file
  client.beta.files.delete(file_id=file_id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const fileId = "file_011CNha8iCJcU1wXNR6q4V8w";

  // Dapatkan metadata file
  const fileInfo = await client.beta.files.retrieveMetadata(fileId);
  console.log(`Filename: ${fileInfo.filename}, Size: ${fileInfo.size_bytes} bytes`);

  // Daftar semua file
  for await (const file of client.beta.files.list()) {
    console.log(`${file.filename} - ${file.created_at}`);
  }

  // Hapus file
  await client.beta.files.delete(fileId);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var fileId = "file_011CNha8iCJcU1wXNR6q4V8w";

  // Dapatkan metadata file
  var fileInfo = await client.Beta.Files.RetrieveMetadata(fileId);
  Console.WriteLine($"Filename: {fileInfo.Filename}, Size: {fileInfo.SizeBytes} bytes");

  // Daftar file
  await foreach (var file in (await client.Beta.Files.List()).Paginate())
  {
      Console.WriteLine($"{file.Filename} - {file.CreatedAt}");
  }

  // Hapus file
  await client.Beta.Files.Delete(fileId);
  ```

  ```go Go
  client := anthropic.NewClient()
  fileID := "file_011CNha8iCJcU1wXNR6q4V8w"

  // Dapatkan metadata file
  fileInfo, err := client.Beta.Files.GetMetadata(context.TODO(), fileID, anthropic.BetaFileGetMetadataParams{})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Printf("Filename: %s, Size: %d bytes\n", fileInfo.Filename, fileInfo.SizeBytes)

  // Daftar semua file
  files := client.Beta.Files.ListAutoPaging(context.TODO(), anthropic.BetaFileListParams{})
  for files.Next() {
  	file := files.Current()
  	fmt.Printf("%s - %s\n", file.Filename, file.CreatedAt)
  }
  if files.Err() != nil {
  	log.Fatal(files.Err())
  }

  // Hapus file
  _, err = client.Beta.Files.Delete(context.TODO(), fileID, anthropic.BetaFileDeleteParams{})
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.files.FileMetadata;
  import com.anthropic.models.beta.files.FileListPage;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();
      String fileId = "file_011CNha8iCJcU1wXNR6q4V8w";

      // Dapatkan metadata file
      FileMetadata fileInfo = client.beta().files().retrieveMetadata(fileId);
      System.out.println("Filename: " + fileInfo.filename() + ", Size: " + fileInfo.sizeBytes() + " bytes");

      // Daftar file (halaman pertama)
      FileListPage files = client.beta().files().list();
      for (var file : files.data()) {
          System.out.println(file.filename() + " - " + file.createdAt());
      }

      // Hapus file
      client.beta().files().delete(fileId);
  }
  ```

  ```php PHP
  $client = new Client();
  $fileId = 'file_011CNha8iCJcU1wXNR6q4V8w';

  // Dapatkan metadata file
  $fileInfo = $client->beta->files->retrieveMetadata($fileId);
  echo "Filename: {$fileInfo->filename}, Size: {$fileInfo->sizeBytes} bytes\n";

  // Daftar file (halaman pertama)
  $files = $client->beta->files->list();
  foreach ($files->data as $file) {
      echo "{$file->filename} - {$file->createdAt->format(DATE_ATOM)}\n";
  }

  // Hapus file
  $client->beta->files->delete($fileId);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  file_id = "file_011CNha8iCJcU1wXNR6q4V8w"

  # Dapatkan metadata file
  file_info = client.beta.files.retrieve_metadata(file_id)
  puts "Filename: #{file_info.filename}, Size: #{file_info.size_bytes} bytes"

  # Daftar semua file
  client.beta.files.list.auto_paging_each do |file|
    puts "#{file.filename} - #{file.created_at}"
  end

  # Hapus file
  client.beta.files.delete(file_id)
  ```
</CodeGroup>

<Note>
  Untuk detail lengkap, lihat [Files API](https://platform.claude.com/docs/id/build-with-claude/files).
</Note>

### Percakapan multi-giliran

Objek `container` dalam respons membawa `id` container dan timestamp `expires_at` (lihat [Penggunaan ulang container](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#container-reuse) untuk detail masa aktif). Gunakan kembali container yang sama di beberapa pesan dengan menentukan ID container:

<CodeGroup>
  ```bash cURL
  # Penggunaan ulang kontainer multi-giliran tidak cocok untuk perintah shell
  # sekali jalan; salah satu opsi SDK akan lebih sesuai. Ambil
  # container.id dari respons pertama, lalu kirimkan di permintaan berikutnya sebagai
  # "container": {"id": "...", "skills": [...]} bersama riwayat percakapan.
  ```

  ```bash CLI
  # Permintaan pertama membuat kontainer
  CONTAINER_ID=$(ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 \
    --transform container.id \
    --raw-output <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - {type: anthropic, skill_id: xlsx, version: latest}
  messages:
    - role: user
      content: Create a sample sales dataset and analyze it
  tools:
    - {type: code_execution_20250825, name: code_execution}
  YAML
  )

  # Lanjutkan percakapan dengan kontainer yang sama
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    id: $CONTAINER_ID  # Reuse container
    skills:
      - {type: anthropic, skill_id: xlsx, version: latest}
  messages:
    - role: user
      content: Create a sample sales dataset and analyze it
    - role: assistant
      content: []  # the assistant's text from the first response
    - role: user
      content: What was the total revenue?
  tools:
    - {type: code_execution_20250825, name: code_execution}
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Permintaan pertama membuat kontainer
  response1 = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      messages=[
          {"role": "user", "content": "Create a sample sales dataset and analyze it"}
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Lanjutkan percakapan dengan kontainer yang sama
  messages = [
      {"role": "user", "content": "Create a sample sales dataset and analyze it"},
      {
          # Teruskan teks asisten; container.id membawa status eksekusi
          "role": "assistant",
          "content": "\n".join(
              block.text for block in response1.content if block.type == "text"
          ),
      },
      {"role": "user", "content": "What was the total revenue?"},
  ]

  response2 = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "id": response1.container.id,  # Reuse container
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}],
      },
      messages=messages,
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Permintaan pertama membuat kontainer
  const response1 = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [{ role: "user", content: "Create a sample sales dataset and analyze it" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Lanjutkan percakapan dengan kontainer yang sama
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Create a sample sales dataset and analyze it" },
    {
      role: "assistant",
      // Teruskan teks asisten; container.id membawa status eksekusi
      content: response1.content
        .filter((block) => block.type === "text")
        .map((block) => block.text)
        .join("\n")
    },
    { role: "user", content: "What was the total revenue?" }
  ];

  const response2 = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      id: response1.container!.id, // Reuse container
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages,
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Permintaan pertama dengan sebuah Skill
  var parameters1 = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Create a sample sales dataset and analyze it" }],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var response1 = await client.Beta.Messages.Create(parameters1);

  // Lanjutkan percakapan dalam kontainer yang sama
  // Teruskan teks asisten; container.id membawa status eksekusi
  var assistantText = string.Join(
      "\n",
      response1.Content.Select(block => block.TryPickText(out var text) ? text.Text : null).Where(text => text is not null)
  );

  var parameters2 = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          ID = response1.Container!.ID,
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
          ],
      },
      Messages =
      [
          new() { Role = Role.User, Content = "Create a sample sales dataset and analyze it" },
          new() { Role = Role.Assistant, Content = assistantText },
          new() { Role = Role.User, Content = "What was the total revenue?" },
      ],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var response2 = await client.Beta.Messages.Create(parameters2);
  Console.WriteLine(response2);
  ```

  ```go Go
  client := anthropic.NewClient()

  response1, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a sample sales dataset and analyze it")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Teruskan teks asisten; container.id membawa status eksekusi
  var textParts []string
  for _, block := range response1.Content {
  	if block.Type == "text" {
  		textParts = append(textParts, block.Text)
  	}
  }
  assistantText := strings.Join(textParts, "\n")

  response2, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			ID: anthropic.String(response1.Container.ID), // Reuse container
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a sample sales dataset and analyze it")),
  		{
  			Role:    anthropic.BetaMessageParamRoleAssistant,
  			Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock(assistantText)},
  		},
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What was the total revenue?")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response2)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  import com.anthropic.models.beta.messages.BetaContentBlock;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params1 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addBeta("code-execution-2025-08-25")
          .addBeta("skills-2025-10-02")
          .container(BetaContainerParams.builder()
              .addSkill(BetaSkillParams.builder()
                  .type(BetaSkillParams.Type.ANTHROPIC)
                  .skillId("xlsx")
                  .version("latest")
                  .build())
              .build())
          .addUserMessage("Create a sample sales dataset and analyze it")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response1 = client.beta().messages().create(params1);

      MessageCreateParams params2 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addBeta("code-execution-2025-08-25")
          .addBeta("skills-2025-10-02")
          .container(BetaContainerParams.builder()
              .id(response1.container().get().id())
              .addSkill(BetaSkillParams.builder()
                  .type(BetaSkillParams.Type.ANTHROPIC)
                  .skillId("xlsx")
                  .version("latest")
                  .build())
              .build())
          .addUserMessage("Create a sample sales dataset and analyze it")
          // Teruskan teks asisten; container.id membawa status eksekusi
          .addAssistantMessage(response1.content().stream()
              .filter(BetaContentBlock::isText)
              .map(block -> block.asText().text())
              .collect(Collectors.joining("\n")))
          .addUserMessage("What was the total revenue?")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response2 = client.beta().messages().create(params2);
      System.out.println(response2);
  }
  ```

  ```php PHP
  $client = new Client();

  $response1 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Create a sample sales dataset and analyze it']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  $messages = [
      ['role' => 'user', 'content' => 'Create a sample sales dataset and analyze it'],
      // Teruskan teks asisten; container.id membawa status eksekusi
      ['role' => 'assistant', 'content' => implode("\n", array_map(
          fn ($block) => $block->text,
          array_filter($response1->content, fn ($block) => $block->type === 'text'),
      ))],
      ['role' => 'user', 'content' => 'What was the total revenue?']
  ];

  $response2 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'id' => $response1->container->id,
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  echo $response2;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response1 = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [
      { role: "user", content: "Create a sample sales dataset and analyze it" }
    ],
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )

  messages = [
    { role: "user", content: "Create a sample sales dataset and analyze it" },
    {
      # Teruskan teks asisten; container.id membawa status eksekusi
      role: "assistant",
      content: response1.content.filter_map { |block| block.text if block.type == :text }.join("\n")
    },
    { role: "user", content: "What was the total revenue?" }
  ]

  response2 = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      id: response1.container.id,
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" }
      ]
    },
    messages: messages,
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )

  puts response2
  ```
</CodeGroup>

### Operasi yang berjalan lama

Skill mungkin melakukan operasi yang memerlukan beberapa giliran. Tangani stop reason `pause_turn`:

<CodeGroup>
  ```bash cURL
  # Permintaan awal
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Generate and process a large sample dataset"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }')

  # Jika stop_reason adalah "pause_turn", lanjutkan dalam kontainer yang sama, dengan menambahkan
  # array konten dari respons sebelumnya ke messages sebagai giliran asisten.
  # Ulangi permintaan lanjutan ini hingga stop_reason bukan lagi "pause_turn".
  STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason')
  CONTAINER_ID=$(echo "$RESPONSE" | jq -r '.container.id')

  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-5\",
      \"max_tokens\": 4096,
      \"container\": {
        \"id\": \"$CONTAINER_ID\",
        \"skills\": [{
          \"type\": \"custom\",
          \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
          \"version\": \"latest\"
        }]
      },
      \"messages\": [],
      \"tools\": [{
        \"type\": \"code_execution_20250825\",
        \"name\": \"code_execution\"
      }]
    }")
  ```

  ```bash CLI
  RESP=$(mktemp)

  # Permintaan awal: tangkap respons JSON lengkap ke file sementara
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 \
    > "$RESP" <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Generate and process a large sample dataset
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML

  # Jika stop_reason adalah "pause_turn", lanjutkan di kontainer yang sama,
  # tambahkan array content dari respons sebelumnya ke messages sebagai
  # giliran asisten. Ulangi hingga stop_reason bukan lagi "pause_turn".
  CONTAINER_ID=$(jq -r '.container.id' "$RESP")

  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 \
    > "$RESP" <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    id: $CONTAINER_ID
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages: [] # replace with conversation history + prior assistant content
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  messages = [{"role": "user", "content": "Generate and process a large sample dataset"}]
  max_retries = 10

  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": "latest",
              }
          ]
      },
      messages=messages,
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Tangani pause_turn untuk operasi yang lama
  for _ in range(max_retries):
      if response.stop_reason != "pause_turn":
          break

      messages.append({"role": "assistant", "content": response.content})
      response = client.beta.messages.create(
          model="claude-opus-5",
          max_tokens=4096,
          betas=["code-execution-2025-08-25", "skills-2025-10-02"],
          container={
              "id": response.container.id,
              "skills": [
                  {
                      "type": "custom",
                      "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                      "version": "latest",
                  }
              ],
          },
          messages=messages,
          tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
      )
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Generate and process a large sample dataset" }
  ];
  const maxRetries = 10;

  let response = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{ type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }]
    },
    messages,
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Tangani pause_turn untuk operasi yang lama
  for (let i = 0; i < maxRetries; i++) {
    if (response.stop_reason !== "pause_turn") {
      break;
    }

    messages.push({
      role: "assistant",
      content: response.content as Anthropic.Beta.Messages.BetaContentBlockParam[]
    });
    response = await client.beta.messages.create({
      model: "claude-opus-5",
      max_tokens: 4096,
      betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
      container: {
        id: response.container!.id,
        skills: [
          { type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }
        ]
      },
      messages,
      tools: [{ type: "code_execution_20250825", name: "code_execution" }]
    });
  }
  ```

  ```csharp C#
  using System.Text.Json;
  // ...
  AnthropicClient client = new();

  List<BetaMessageParam> messages =
  [
      new() { Role = Role.User, Content = "Generate and process a large sample dataset" },
  ];

  var maxRetries = 10;
  string? containerId = null;
  BetaMessage? response = null;

  for (var i = 0; i < maxRetries; i++)
  {
      var parameters = new MessageCreateParams
      {
          Model = "claude-opus-5",
          MaxTokens = 4096,
          Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
          Container = containerId is null
              ? new BetaContainerParams
              {
                  Skills =
                  [
                      new BetaSkillParams
                      {
                          Type = BetaSkillParamsType.Custom,
                          SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                          Version = "latest",
                      },
                  ],
              }
              : new BetaContainerParams
              {
                  ID = containerId,
                  Skills =
                  [
                      new BetaSkillParams
                      {
                          Type = BetaSkillParamsType.Custom,
                          SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                          Version = "latest",
                      },
                  ],
              },
          Messages = messages,
          Tools = [new BetaCodeExecutionTool20250825()],
      };

      response = await client.Beta.Messages.Create(parameters);
      containerId = response.Container!.ID;

      if (response.StopReason != BetaStopReason.PauseTurn)
      {
          break;
      }

      // Tambahkan konten giliran yang dijeda dan lanjutkan
      var assistantContent = JsonSerializer.SerializeToElement(
          response.Content.Select(block => block.Json).ToArray()
      );
      messages.Add(new() { Role = Role.Assistant, Content = new BetaMessageParamContent(assistantContent) });
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  messages := []anthropic.BetaMessageParam{
  	anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Generate and process a large sample dataset")),
  }
  maxRetries := 10

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: messages,
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for i := 0; i < maxRetries; i++ {
  	if response.StopReason != anthropic.BetaStopReasonPauseTurn {
  		break
  	}

  	messages = append(messages, response.ToParam())

  	response, err = client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     "claude-opus-5",
  		MaxTokens: 4096,
  		Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
  		Container: anthropic.BetaMessageNewParamsContainerUnion{
  			OfContainers: &anthropic.BetaContainerParams{
  				ID: anthropic.String(response.Container.ID), // Reuse container
  				Skills: []anthropic.BetaSkillParams{
  					{
  						Type:    anthropic.BetaSkillParamsTypeCustom,
  						SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  						Version: anthropic.String("latest"),
  					},
  				},
  			},
  		},
  		Messages: messages,
  		Tools: []anthropic.BetaToolUnionParam{
  			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  }

  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  import com.anthropic.models.beta.messages.BetaStopReason;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      List<BetaMessageParam> messages = new ArrayList<>();
      messages.add(
          BetaMessageParam.builder()
              .role(BetaMessageParam.Role.USER)
              .content("Generate and process a large sample dataset")
              .build()
      );
      int maxRetries = 10;

      BetaMessage response = client.beta().messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5)
              .maxTokens(4096L)
              .addBeta("code-execution-2025-08-25")
              .addBeta("skills-2025-10-02")
              .container(BetaContainerParams.builder()
                  .addSkill(BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.CUSTOM)
                      .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                      .version("latest")
                      .build())
                  .build())
              .messages(messages)
              .addTool(BetaCodeExecutionTool20250825.builder().build())
              .build());

      for (int i = 0; i < maxRetries; i++) {
          if (!response.stopReason().isPresent()
                  || !response.stopReason().get().equals(BetaStopReason.PAUSE_TURN)) {
              break;
          }

          messages.add(response.toParam());

          response = client.beta().messages().create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
                  .maxTokens(4096L)
                  .addBeta("code-execution-2025-08-25")
                  .addBeta("skills-2025-10-02")
                  .container(BetaContainerParams.builder()
                      .id(response.container().get().id())
                      .addSkill(BetaSkillParams.builder()
                          .type(BetaSkillParams.Type.CUSTOM)
                          .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                          .version("latest")
                          .build())
                      .build())
                  .messages(messages)
                  .addTool(BetaCodeExecutionTool20250825.builder().build())
                  .build());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $messages = [
      ['role' => 'user', 'content' => 'Generate and process a large sample dataset']
  ];
  $maxRetries = 10;

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              [
                  'type' => 'custom',
                  'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                  'version' => 'latest'
              ]
          ]
      ],
      tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
  );

  for ($i = 0; $i < $maxRetries; $i++) {
      if ($response->stopReason !== 'pause_turn') {
          break;
      }

      $messages[] = ['role' => 'assistant', 'content' => $response->content];

      $response = $client->beta->messages->create(
          maxTokens: 4096,
          messages: $messages,
          model: 'claude-opus-5',
          betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
          container: [
              'id' => $response->container->id,
              'skills' => [
                  [
                      'type' => 'custom',
                      'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                      'version' => 'latest'
                  ]
              ]
          ],
          tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
      );
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  messages = [
    { role: "user", content: "Generate and process a large sample dataset" }
  ]
  max_retries = 10

  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: messages,
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )

  max_retries.times do
    break if response.stop_reason != :pause_turn

    messages << { role: "assistant", content: response.content }

    response = client.beta.messages.create(
      model: "claude-opus-5",
      max_tokens: 4096,
      betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
      container: {
        id: response.container.id,
        skills: [
          {
            type: "custom",
            skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
            version: "latest"
          }
        ]
      },
      messages: messages,
      tools: [{ type: "code_execution_20250825", name: "code_execution" }]
    )
  end
  ```
</CodeGroup>

<Note>
  Respons mungkin menyertakan stop reason `pause_turn`, yang menunjukkan bahwa API menjeda operasi Skill yang berjalan lama. Anda dapat memberikan respons tersebut apa adanya dalam permintaan berikutnya agar Claude melanjutkan gilirannya, atau memodifikasi konten jika Anda ingin menginterupsi percakapan dan memberikan panduan tambahan.
</Note>

### Menggunakan beberapa Skill

Gabungkan beberapa Skill dalam satu permintaan untuk menangani alur kerja yang kompleks:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "anthropic",
            "skill_id": "xlsx",
            "version": "latest"
          },
          {
            "type": "anthropic",
            "skill_id": "pptx",
            "version": "latest"
          },
          {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Analyze sales data and create a presentation"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
      - type: anthropic
        skill_id: pptx
        version: latest
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Analyze sales data and create a presentation
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {"type": "anthropic", "skill_id": "pptx", "version": "latest"},
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": "latest",
              },
          ]
      },
      messages=[
          {"role": "user", "content": "Analyze sales data and create a presentation"}
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        {
          type: "anthropic",
          skill_id: "xlsx",
          version: "latest"
        },
        {
          type: "anthropic",
          skill_id: "pptx",
          version: "latest"
        },
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: [
      {
        role: "user",
        content: "Analyze sales data and create a presentation"
      }
    ],
    tools: [
      {
        type: "code_execution_20250825",
        name: "code_execution"
      }
    ]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "pptx",
                  Version = "latest",
              },
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Custom,
                  SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Analyze sales data and create a presentation" }],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var message = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas: []anthropic.AnthropicBeta{
  		"code-execution-2025-08-25",
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "pptx",
  					Version: anthropic.String("latest"),
  				},
  				{
  					Type:    anthropic.BetaSkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Analyze sales data and create a presentation")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addBeta("code-execution-2025-08-25")
          .addBeta("skills-2025-10-02")
          .container(BetaContainerParams.builder()
              .skills(List.of(
                  BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.ANTHROPIC)
                      .skillId("xlsx")
                      .version("latest")
                      .build(),
                  BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.ANTHROPIC)
                      .skillId("pptx")
                      .version("latest")
                      .build(),
                  BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.CUSTOM)
                      .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                      .version("latest")
                      .build()
              ))
              .build())
          .addUserMessage("Analyze sales data and create a presentation")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response = client.beta().messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze sales data and create a presentation']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              [
                  'type' => 'anthropic',
                  'skill_id' => 'xlsx',
                  'version' => 'latest'
              ],
              [
                  'type' => 'anthropic',
                  'skill_id' => 'pptx',
                  'version' => 'latest'
              ],
              [
                  'type' => 'custom',
                  'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                  'version' => 'latest'
              ]
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        {
          type: "anthropic",
          skill_id: "xlsx",
          version: "latest"
        },
        {
          type: "anthropic",
          skill_id: "pptx",
          version: "latest"
        },
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: [
      { role: "user", content: "Analyze sales data and create a presentation" }
    ],
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )
  puts message
  ```
</CodeGroup>

***

## Mengelola Skill kustom

<Warning id="workspace-scoped-access">
  **Skill kustom dapat diakses oleh seluruh workspace Anda, tidak dibatasi pada pengguna akhir, percakapan, atau sesi tertentu.** Kunci API apa pun di workspace yang sama dapat membaca, memanggil, dan menghapus setiap Skill kustom yang diunggah di sana, dan semua kunci Anda berbagi Default Workspace organisasi Anda kecuali Anda telah menetapkannya ke [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces#api-keys-and-resource-scoping) terpisah.

  Jika Anda membangun platform multi-tenant di atas Skills API, buat [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces) terpisah untuk setiap tenant. Workspace adalah batas isolasi untuk Skill kustom, sehingga satu workspace per tenant memberikan isolasi ketat bagi Skill setiap tenant dari tenant lainnya. Setiap organisasi dapat memiliki hingga 100 workspace secara default (lihat [Cara kerja workspace](https://platform.claude.com/docs/id/manage-claude/workspaces#how-workspaces-work)); jika Anda memerlukan lebih banyak untuk isolasi tenant, hubungi tim akun Anda.
</Warning>

### Membuat Skill

Bundel Skill adalah direktori yang berisi file `SKILL.md` di tingkat atas dengan frontmatter YAML `name` dan `description`, ditambah skrip atau sumber daya pendukung apa pun. Lihat [Memulai dengan Agent Skills di API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/quickstart) untuk membuatnya, dan daftar **Persyaratan** setelah contoh-contoh untuk batasan lengkapnya.

Unggah Skill kustom Anda agar tersedia di workspace Anda. Anda dapat mengunggah arsip zip atau objek file individual. SDK Python juga menyediakan helper `files_from_dir` yang menerima path direktori.

File diidentifikasi berdasarkan nama file yang Anda lampirkan (sufiks `;filename=` dalam contoh cURL dan argumen nama file dalam contoh SDK). Untuk skill dalam panduan ini, buat zip dengan `zip -r financial_skill.zip financial_skill/` dan gantikan placeholder `example_skill.zip` dalam opsi unggah zip dengan file tersebut.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "files[]=@financial_skill/SKILL.md;filename=financial_skill/SKILL.md" \
    -F "files[]=@financial_skill/analyze.py;filename=financial_skill/analyze.py"
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    zip -r financial_skill.zip financial_skill/
    ant beta:skills create \
      --file financial_skill.zip \
      --beta skills-2025-10-02
    ```

    <File filename="financial_skill/SKILL.md">
      ```markdown
      ---
      name: financial-skill
      description: Docs example skill.
      ---
      ```
    </File>

    <File filename="financial_skill/analyze.py">
      ```python
      print("financial analysis helper")
      ```
    </File>
  </MultiFileExample>

  ```python Python
  from anthropic.lib import files_from_dir

  client = anthropic.Anthropic()

  # Opsi 1: Menggunakan file zip
  skill = client.beta.skills.create(
      files=[open("example_skill.zip", "rb")],
  )

  # Opsi 2: Menggunakan tuple file (filename, file_content, mime_type)
  skill = client.beta.skills.create(
      files=[
          (
              "financial_skill/SKILL.md",
              open("financial_skill/SKILL.md", "rb"),
              "text/markdown",
          ),
          (
              "financial_skill/analyze.py",
              open("financial_skill/analyze.py", "rb"),
              "text/x-python",
          ),
      ],
  )

  # Opsi 3: Menggunakan helper files_from_dir (hanya Python)
  skill = client.beta.skills.create(
      files=files_from_dir("financial_skill"),
  )

  print(f"Created skill: {skill.id}")
  print(f"Latest version: {skill.latest_version}")
  ```

  ```typescript TypeScript
  import { toFile } from "@anthropic-ai/sdk";
  import fs from "node:fs";
  // ...

  const client = new Anthropic();

  // Opsi 1: Menggunakan file zip
  const skillFromZip = await client.beta.skills.create({
    files: [await toFile(fs.createReadStream("example_skill.zip"), "example_skill.zip")]
  });

  // Opsi 2: Menggunakan objek file individual
  const skill = await client.beta.skills.create({
    files: [
      await toFile(fs.createReadStream("financial_skill/SKILL.md"), "financial_skill/SKILL.md", {
        type: "text/markdown"
      }),
      await toFile(
        fs.createReadStream("financial_skill/analyze.py"),
        "financial_skill/analyze.py",
        { type: "text/x-python" }
      )
    ]
  });

  console.log(`Created skill: ${skill.id}`);
  console.log(`Latest version: ${skill.latest_version}`);
  ```

  ```csharp C#
  using Anthropic.Core;
  // ...

  AnthropicClient client = new();

  // Opsi 1: Menggunakan file zip
  var parameters = new SkillCreateParams
  {
      Files = [File.OpenRead("example_skill.zip")],
  };

  var skill = await client.Beta.Skills.Create(parameters);

  // Opsi 2: Menggunakan file individual (nama file dengan kualifikasi path mempertahankan tata letak direktori Skill)
  var parameters2 = new SkillCreateParams
  {
      Files =
      [
          new BinaryContent
          {
              Stream = File.OpenRead("financial_skill/SKILL.md"),
              FileName = "financial_skill/SKILL.md",
          },
          new BinaryContent
          {
              Stream = File.OpenRead("financial_skill/analyze.py"),
              FileName = "financial_skill/analyze.py",
          },
      ],
  };

  var skill2 = await client.Beta.Skills.Create(parameters2);

  Console.WriteLine($"Created skill: {skill.ID}");
  Console.WriteLine($"Latest version: {skill.LatestVersion}");
  Console.WriteLine($"Created skill 2: {skill2.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  // Opsi 1: Menggunakan file zip
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

  // Opsi 2: Menggunakan file individual
  skillMd, err := os.Open("financial_skill/SKILL.md")
  if err != nil {
  	log.Fatal(err)
  }
  defer skillMd.Close()

  analyzePy, err := os.Open("financial_skill/analyze.py")
  if err != nil {
  	log.Fatal(err)
  }
  defer analyzePy.Close()

  skill2, err := client.Beta.Skills.New(context.TODO(), anthropic.BetaSkillNewParams{
  	Files: []io.Reader{
  		anthropic.File(skillMd, "financial_skill/SKILL.md", "text/markdown"),
  		anthropic.File(analyzePy, "financial_skill/analyze.py", "text/x-python"),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("Created skill: %s\n", skill.ID)
  fmt.Printf("Latest version: %s\n", skill.LatestVersion)
  fmt.Printf("Created skill 2: %s\n", skill2.ID)
  ```

  ```java Java
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.beta.skills.SkillCreateParams;
  import com.anthropic.models.beta.skills.SkillCreateResponse;
  // ...
  void main() throws Exception {
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Opsi 1: Menggunakan file zip
      SkillCreateParams params = SkillCreateParams.builder()
          .addFile(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("example_skill.zip")))
              .filename("example_skill.zip")
              .contentType("application/zip")
              .build())
          .build();

      SkillCreateResponse skill = client.beta().skills().create(params);

      // Opsi 2: Menggunakan file individual (nama file dengan kualifikasi path mempertahankan tata letak direktori Skill)
      SkillCreateParams params2 = SkillCreateParams.builder()
          .addFile(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("financial_skill/SKILL.md")))
              .filename("financial_skill/SKILL.md")
              .contentType("text/markdown")
              .build())
          .addFile(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("financial_skill/analyze.py")))
              .filename("financial_skill/analyze.py")
              .contentType("text/x-python")
              .build())
          .build();

      SkillCreateResponse skill2 = client.beta().skills().create(params2);

      System.out.println("Created skill: " + skill.id());
      System.out.println("Latest version: " + skill.latestVersion().orElseThrow());
      System.out.println("Created skill 2: " + skill2.id());
  }
  ```

  ```php PHP
  use Anthropic\Core\FileParam;
  // ...

  $client = new Client();

  // Opsi 1: Menggunakan file zip
  $skill = $client->beta->skills->create(
      files: [
          FileParam::fromResource(fopen('example_skill.zip', 'r'))
      ],
  );

  // Opsi 2: Menggunakan file individual
  $skill = $client->beta->skills->create(
      files: [
          FileParam::fromResource(fopen('financial_skill/SKILL.md', 'r'), 'financial_skill/SKILL.md', 'text/markdown'),
          FileParam::fromResource(fopen('financial_skill/analyze.py', 'r'), 'financial_skill/analyze.py', 'text/x-python')
      ],
  );

  echo "Created skill: {$skill->id}\n";
  echo "Latest version: {$skill->latestVersion}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Opsi 1: Menggunakan file zip
  skill = client.beta.skills.create(
    files: [
      File.open("example_skill.zip", "rb")
    ]
  )

  # Opsi 2: Menggunakan file individual
  skill = client.beta.skills.create(
    files: [
      Anthropic::FilePart.new(
        Pathname("financial_skill/SKILL.md"),
        filename: "financial_skill/SKILL.md",
        content_type: "text/markdown"
      ),
      Anthropic::FilePart.new(
        Pathname("financial_skill/analyze.py"),
        filename: "financial_skill/analyze.py",
        content_type: "text/x-python"
      )
    ]
  )

  puts "Created skill: #{skill.id}"
  puts "Latest version: #{skill.latest_version}"
  ```
</CodeGroup>

**Persyaratan:**

* Harus menyertakan file `SKILL.md` di root unggahan (atau di bagian atas satu folder pembungkus)

* `display_name` bersifat opsional: jika dihilangkan, nilainya diturunkan dari `name` di `SKILL.md`; nilai eksplisit boleh hingga 255 karakter dan tidak perlu unik dalam workspace

* Total ukuran unggahan harus di bawah 30 MB (tidak terkompresi)

* Persyaratan frontmatter YAML:

  * `name`: Maksimum 64 karakter, hanya huruf kecil/angka/tanda hubung, tanpa tag XML, tanpa kata yang dicadangkan ("anthropic", "claude")
  * `description`: Maksimum 1024 karakter, tidak kosong, tanpa tag XML

Untuk skema permintaan/respons lengkap, lihat [referensi API Create Skill](https://platform.claude.com/docs/id/api/beta/skills/create).

### Membuat daftar Skill

Ambil semua Skill yang tersedia untuk workspace Anda, termasuk Skill bawaan Anthropic dan Skill kustom Anda. Gunakan parameter `source` untuk memfilter berdasarkan jenis skill:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # Daftar semua Skill
  curl "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"

  # Daftar hanya Skill kustom
  curl "https://api.anthropic.com/v1/skills?source=custom" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"
  ```

  ```bash CLI
  # Daftar semua Skill
  ant beta:skills list

  # Daftar hanya Skill kustom
  ant beta:skills list --source custom
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Daftar semua Skill
  for skill in client.beta.skills.list():
      print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

  # Daftar hanya Skill kustom
  custom_skills = client.beta.skills.list(source="custom")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Daftar semua Skill
  for await (const skill of client.beta.skills.list()) {
    console.log(`${skill.id}: ${skill.display_title} (source: ${skill.source})`);
  }

  // Daftar hanya Skill kustom
  const customSkills = await client.beta.skills.list({
    source: "custom"
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Daftar semua Skill
  await foreach (var skill in (await client.Beta.Skills.List()).Paginate())
  {
      Console.WriteLine($"{skill.ID}: {skill.DisplayTitle} (source: {skill.Source})");
  }

  // Daftar hanya Skill kustom
  var customSkills = await client.Beta.Skills.List(new SkillListParams { Source = "custom" });
  ```

  ```go Go
  client := anthropic.NewClient()

  // Daftar semua Skill
  skills := client.Beta.Skills.ListAutoPaging(context.TODO(), anthropic.BetaSkillListParams{})

  for skills.Next() {
  	skill := skills.Current()
  	fmt.Printf("%s: %s (source: %s)\n", skill.ID, skill.DisplayTitle, skill.Source)
  }
  if skills.Err() != nil {
  	log.Fatal(skills.Err())
  }

  // Daftar hanya Skill kustom
  customSkills := client.Beta.Skills.ListAutoPaging(context.TODO(), anthropic.BetaSkillListParams{
  	Source: anthropic.String("custom"),
  })

  for customSkills.Next() {
  	skill := customSkills.Current()
  	fmt.Printf("%s: %s (source: %s)\n", skill.ID, skill.DisplayTitle, skill.Source)
  }
  if customSkills.Err() != nil {
  	log.Fatal(customSkills.Err())
  }
  ```

  ```java Java
  import com.anthropic.models.beta.skills.SkillListParams;
  import com.anthropic.models.beta.skills.SkillListPage;
  import com.anthropic.models.beta.skills.SkillListResponse;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Daftar Skill (halaman pertama)
      SkillListPage skills = client.beta().skills().list();

      for (SkillListResponse skill : skills.data()) {
          System.out.println(skill.id() + ": " + skill.displayTitle().orElseThrow() + " (source: " + skill.source() + ")");
      }

      // Daftar hanya Skill kustom
      SkillListParams customParams = SkillListParams.builder()
          .source("custom")
          .build();

      SkillListPage customSkills = client.beta().skills().list(customParams);
  }
  ```

  ```php PHP
  $client = new Client();

  // Daftar Skill (halaman pertama)
  $skills = $client->beta->skills->list();

  foreach ($skills->data as $skill) {
      echo "{$skill->id}: {$skill->displayTitle} (source: {$skill->source})\n";
  }

  // Daftar hanya Skill kustom
  $customSkills = $client->beta->skills->list(
      source: 'custom',
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Daftar semua Skill
  client.beta.skills.list.auto_paging_each do |skill|
    puts "#{skill.id}: #{skill.display_title} (source: #{skill.source})"
  end

  # Daftar hanya Skill kustom
  custom_skills = client.beta.skills.list(
    source: "custom"
  )
  ```
</CodeGroup>

Lihat [referensi API List Skills](https://platform.claude.com/docs/id/api/beta/skills/list) untuk opsi paginasi dan pemfilteran.

### Mengambil Skill

Dapatkan detail tentang Skill tertentu:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"
  ```

  ```bash CLI
  ant beta:skills retrieve \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv
  ```

  ```python Python
  client = anthropic.Anthropic()

  skill = client.beta.skills.retrieve(skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv")

  print(f"Skill: {skill.display_title}")
  print(f"Latest version: {skill.latest_version}")
  print(f"Created: {skill.created_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const skill = await client.beta.skills.retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv");

  console.log(`Skill: ${skill.display_title}`);
  console.log(`Latest version: ${skill.latest_version}`);
  console.log(`Created: ${skill.created_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var skill = await client.Beta.Skills.Retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv");

  Console.WriteLine($"Skill: {skill.DisplayTitle}");
  Console.WriteLine($"Latest version: {skill.LatestVersion}");
  Console.WriteLine($"Created: {skill.CreatedAt}");
  ```

  ```go Go
  client := anthropic.NewClient()

  skill, err := client.Beta.Skills.Get(
  	context.TODO(),
  	"skill_01AbCdEfGhIjKlMnOpQrStUv",
  	anthropic.BetaSkillGetParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("Skill: %s\n", skill.DisplayTitle)
  fmt.Printf("Latest version: %s\n", skill.LatestVersion)
  fmt.Printf("Created: %s\n", skill.CreatedAt)
  ```

  ```java Java
  import com.anthropic.models.beta.skills.SkillRetrieveResponse;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      SkillRetrieveResponse skill = client.beta().skills().retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv");

      System.out.println("Skill: " + skill.displayTitle().orElseThrow());
      System.out.println("Latest version: " + skill.latestVersion().orElseThrow());
      System.out.println("Created: " + skill.createdAt());
  }
  ```

  ```php PHP
  $client = new Client();

  $skill = $client->beta->skills->retrieve(
      skillID: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
  );

  echo "Skill: " . $skill->displayTitle . "\n";
  echo "Latest version: " . $skill->latestVersion . "\n";
  echo "Created: " . $skill->createdAt . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  skill = client.beta.skills.retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv")

  puts "Skill: #{skill.display_title}"
  puts "Latest version: #{skill.latest_version}"
  puts "Created: #{skill.created_at}"
  ```
</CodeGroup>

### Menghapus Skill

Menghapus Skill juga menghapus semua versinya. Penghapusan berantai ini adalah perilaku khusus GA, jadi tidak seperti contoh lain dalam panduan ini, contoh-contoh berikut memanggil permukaan GA secara langsung alih-alih namespace `beta`.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant skills delete \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv >/dev/null
  ```

  ```python Python
  client = anthropic.Anthropic()

  client.skills.delete(skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  await client.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
  ```

  ```csharp C#
  AnthropicClient client = new();

  await client.Skills.Delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
  ```

  ```go Go
  client := anthropic.NewClient()

  _, err := client.Skills.Delete(
  	context.TODO(),
  	"skill_01AbCdEfGhIjKlMnOpQrStUv",
  )
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      client.skills().delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
  }
  ```

  ```php PHP
  $client = new Client();

  $client->skills->delete(
      skillID: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  client.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv")
  ```
</CodeGroup>

### Pembuatan versi

Skill mendukung pembuatan versi untuk mengelola pembaruan dengan aman:

**Skill Anthropic:**

* Versi menggunakan format tanggal: `20251013`
* Versi baru dirilis seiring pembaruan dilakukan
* Tentukan versi yang tepat untuk stabilitas

**Skill Kustom:**

* ID versi yang dihasilkan otomatis: `skver_01AbCdEfGhIjKlMnOpQrStUv`
* Gunakan `"latest"` untuk selalu mendapatkan versi terbaru
* Buat versi baru saat memperbarui file Skill

Versi baru adalah snapshot lengkap, bukan delta: unggah seluruh kumpulan file Skill setiap kali. File yang Anda hilangkan tidak akan dibawa ke versi baru, dan `name` di `SKILL.md` versi baru harus cocok dengan nama Skill yang sudah ada. Contoh berikut mengunggah ulang bundel `financial_skill/` lengkap dari [Membuat Skill](https://platform.claude.com/docs/id/build-with-claude/skills-guide#creating-a-skill).

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # Buat versi baru
  NEW_VERSION=$(curl -X POST "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "files[]=@financial_skill/SKILL.md;filename=financial_skill/SKILL.md" \
    -F "files[]=@financial_skill/analyze.py;filename=financial_skill/analyze.py")

  VERSION_NUMBER=$(echo "$NEW_VERSION" | jq -r '.version')

  # Gunakan versi tertentu
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-5\",
      \"max_tokens\": 4096,
      \"container\": {
        \"skills\": [{
          \"type\": \"custom\",
          \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
          \"version\": \"$VERSION_NUMBER\"
        }]
      },
      \"messages\": [{\"role\": \"user\", \"content\": \"Use updated Skill\"}],
      \"tools\": [{\"type\": \"code_execution_20250825\", \"name\": \"code_execution\"}]
    }"

  # Gunakan versi terbaru
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [{
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "latest"
        }]
      },
      "messages": [{"role": "user", "content": "Use latest Skill version"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  # Buat versi baru
  VERSION_NUMBER=$(ant beta:skills:versions create \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
    --file financial_skill.zip \
    --transform version \
    --raw-output)

  # Gunakan versi tertentu
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: "$VERSION_NUMBER"
  messages:
    - role: user
      content: Use updated Skill
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML

  # Gunakan versi terbaru
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Use latest Skill version
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  from anthropic.lib import files_from_dir

  client = anthropic.Anthropic()

  # Buat versi baru

  new_version = client.beta.skills.versions.create(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      files=files_from_dir("financial_skill"),
  )

  # Gunakan versi tertentu
  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": new_version.version,
              }
          ]
      },
      messages=[{"role": "user", "content": "Use updated Skill"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Gunakan versi terbaru
  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": "latest",
              }
          ]
      },
      messages=[{"role": "user", "content": "Use latest Skill version"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  import fs from "node:fs";

  const client = new Anthropic();

  // Buat versi baru dari zip bundel financial_skill/ lengkap
  const newVersion = await client.beta.skills.versions.create("skill_01AbCdEfGhIjKlMnOpQrStUv", {
    files: [fs.createReadStream("financial_skill.zip")]
  });

  // Gunakan versi tertentu
  const specificVersionResponse = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: newVersion.version
        }
      ]
    },
    messages: [{ role: "user", content: "Use updated Skill" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Gunakan versi terbaru
  const latestVersionResponse = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: [{ role: "user", content: "Use latest Skill version" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
  ```

  ```csharp C#
  using Anthropic.Core;
  using Anthropic.Models.Beta.Skills.Versions;
  // ...
  AnthropicClient client = new();

  // Buat versi baru
  var versionParams = new VersionCreateParams
  {
      Files =
      [
          new BinaryContent
          {
              Stream = File.OpenRead("financial_skill/SKILL.md"),
              FileName = "financial_skill/SKILL.md",
          },
          new BinaryContent
          {
              Stream = File.OpenRead("financial_skill/analyze.py"),
              FileName = "financial_skill/analyze.py",
          },
      ],
  };

  var newVersion = await client.Beta.Skills.Versions.Create("skill_01AbCdEfGhIjKlMnOpQrStUv", versionParams);

  // Gunakan versi tertentu
  var specificVersionParams = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Custom,
                  SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  Version = newVersion.Version,
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Use updated Skill" }],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var response = await client.Beta.Messages.Create(specificVersionParams);
  Console.WriteLine(response);

  // Gunakan versi terbaru
  var latestVersionParams = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Custom,
                  SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Use latest Skill version" }],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var latestResponse = await client.Beta.Messages.Create(latestVersionParams);
  Console.WriteLine(latestResponse);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Buat versi baru
  skillMd, err := os.Open("financial_skill/SKILL.md")
  if err != nil {
  	log.Fatal(err)
  }
  defer skillMd.Close()
  analyzePy, err := os.Open("financial_skill/analyze.py")
  if err != nil {
  	log.Fatal(err)
  }
  defer analyzePy.Close()

  newVersion, err := client.Beta.Skills.Versions.New(
  	context.TODO(),
  	"skill_01AbCdEfGhIjKlMnOpQrStUv",
  	anthropic.BetaSkillVersionNewParams{
  		Files: []io.Reader{
  			anthropic.File(skillMd, "financial_skill/SKILL.md", "text/markdown"),
  			anthropic.File(analyzePy, "financial_skill/analyze.py", "text/x-python"),
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  // Gunakan versi tertentu
  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String(newVersion.Version),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Use updated Skill")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)

  // Gunakan versi terbaru
  latestResponse, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Use latest Skill version")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(latestResponse)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.messages.Model;
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  import com.anthropic.models.beta.skills.versions.VersionCreateParams;
  import com.anthropic.models.beta.skills.versions.VersionCreateResponse;
  import java.io.InputStream;
  import java.nio.file.Files;
  import java.nio.file.Path;

  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Buat versi baru dari zip bundel financial_skill/ lengkap
  VersionCreateParams versionParams = VersionCreateParams.builder()
      .addFile(MultipartField.<InputStream>builder()
          .value(Files.newInputStream(Path.of("financial_skill.zip")))
          .filename("financial_skill.zip")
          .contentType("application/zip")
          .build())
      .build();

  VersionCreateResponse newVersion = client.beta().skills().versions()
      .create("skill_01AbCdEfGhIjKlMnOpQrStUv", versionParams);

  // Gunakan versi tertentu
  MessageCreateParams specificVersionParams = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(4096L)
      .addBeta("code-execution-2025-08-25")
      .addBeta("skills-2025-10-02")
      .container(BetaContainerParams.builder()
          .addSkill(BetaSkillParams.builder()
              .type(BetaSkillParams.Type.CUSTOM)
              .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
              .version(newVersion.version())
              .build())
          .build())
      .addUserMessage("Use updated Skill")
      .addTool(BetaCodeExecutionTool20250825.builder().build())
      .build();

  BetaMessage response = client.beta().messages().create(specificVersionParams);
  System.out.println(response);

  // Gunakan versi terbaru
  MessageCreateParams latestVersionParams = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(4096L)
      .addBeta("code-execution-2025-08-25")
      .addBeta("skills-2025-10-02")
      .container(BetaContainerParams.builder()
          .addSkill(BetaSkillParams.builder()
              .type(BetaSkillParams.Type.CUSTOM)
              .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
              .version("latest")
              .build())
          .build())
      .addUserMessage("Use latest Skill version")
      .addTool(BetaCodeExecutionTool20250825.builder().build())
      .build();

  BetaMessage latestResponse = client.beta().messages().create(latestVersionParams);
  System.out.println(latestResponse);
  ```

  ```php PHP
  use Anthropic\Core\FileParam;

  // ...
  $client = new Client();

  // Buat versi baru
  $newVersion = $client->beta->skills->versions->create(
      skillID: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
      files: [
          FileParam::fromResource(fopen('financial_skill/SKILL.md', 'r'), 'financial_skill/SKILL.md', 'text/markdown'),
          FileParam::fromResource(fopen('financial_skill/analyze.py', 'r'), 'financial_skill/analyze.py', 'text/x-python'),
      ],
  );

  // Gunakan versi tertentu
  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [['role' => 'user', 'content' => 'Use updated Skill']],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [[
              'type' => 'custom',
              'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
              'version' => $newVersion->version
          ]]
      ],
      tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
  );
  echo $response;

  // Gunakan versi terbaru
  $latestResponse = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [['role' => 'user', 'content' => 'Use latest Skill version']],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [[
              'type' => 'custom',
              'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
              'version' => 'latest'
          ]]
      ],
      tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
  );
  echo $latestResponse;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Buat versi baru
  new_version = client.beta.skills.versions.create(
    "skill_01AbCdEfGhIjKlMnOpQrStUv",
    files: [
      Anthropic::FilePart.new(
        Pathname("financial_skill/SKILL.md"),
        filename: "financial_skill/SKILL.md",
        content_type: "text/markdown"
      ),
      Anthropic::FilePart.new(
        Pathname("financial_skill/analyze.py"),
        filename: "financial_skill/analyze.py",
        content_type: "text/x-python"
      )
    ]
  )

  # Gunakan versi tertentu
  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: new_version.version
      }]
    },
    messages: [{ role: "user", content: "Use updated Skill" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts response

  # Gunakan versi terbaru
  latest_response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "latest"
      }]
    },
    messages: [{ role: "user", content: "Use latest Skill version" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts latest_response
  ```
</CodeGroup>

Lihat [referensi API Create Skill Version](https://platform.claude.com/docs/id/api/beta/skills/versions/create) untuk detail lengkap.

***

## Cara Skill dimuat

Ketika Anda menentukan Skill dalam container:

1. **Penemuan metadata:** Claude melihat metadata untuk setiap Skill (nama, deskripsi) dalam prompt sistem.
2. **Pemuatan file:** File Skill disalin ke dalam container di `/skills/{skill-name}/`. Direktori tersebut adalah nama Skill (`pptx` untuk Skill Anthropic, `name` dari `SKILL.md` untuk Skill kustom), bukan ID `skill_01...`-nya.
3. **Penggunaan otomatis:** Claude secara otomatis memuat dan menggunakan Skill ketika relevan dengan permintaan Anda.
4. **Komposisi:** Beberapa Skill dapat dikomposisikan bersama untuk alur kerja yang kompleks.

Claude memuat instruksi Skill lengkap hanya ketika diperlukan.

***

## Kasus penggunaan

Skill cocok untuk pekerjaan organisasi maupun pribadi. Organisasi menggunakannya untuk menerapkan format merek pada dokumen, menyusun catatan dan laporan berdasarkan templat perusahaan, dan menjalankan prosedur analitis khusus perusahaan. Individu menggunakannya untuk templat dokumen kustom, pipeline data khusus, serta konvensi pembuatan kode atau deployment.

### Contoh: pemodelan keuangan

Gabungkan Skill Excel dan Skill analisis DCF kustom:

<CodeGroup>
  ```bash cURL
  # Buat Skill analisis DCF kustom
  DCF_SKILL=$(curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "files[]=@dcf_skill/SKILL.md;filename=dcf_skill/SKILL.md")

  DCF_SKILL_ID=$(echo "$DCF_SKILL" | jq -r '.id')

  # Gunakan dengan Excel untuk membuat model keuangan
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-5\",
      \"max_tokens\": 4096,
      \"container\": {
        \"skills\": [
          {
            \"type\": \"anthropic\",
            \"skill_id\": \"xlsx\",
            \"version\": \"latest\"
          },
          {
            \"type\": \"custom\",
            \"skill_id\": \"$DCF_SKILL_ID\",
            \"version\": \"latest\"
          }
        ]
      },
      \"messages\": [{
        \"role\": \"user\",
        \"content\": \"Build a DCF valuation model for a SaaS company\"
      }],
      \"tools\": [{
        \"type\": \"code_execution_20250825\",
        \"name\": \"code_execution\"
      }]
    }"
  ```

  ```bash CLI
  # Create custom DCF analysis Skill
  DCF_SKILL_ID=$(ant beta:skills create \
    --file dcf_skill.zip \
    --transform id \
    --raw-output)

  # Use with Excel to create financial model
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
      - type: custom
        skill_id: $DCF_SKILL_ID
        version: latest
  messages:
    - role: user
      content: Build a DCF valuation model for a SaaS company
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  from anthropic.lib import files_from_dir

  client = anthropic.Anthropic()

  # Buat Skill analisis DCF kustom

  dcf_skill = client.beta.skills.create(
      files=files_from_dir("/path/to/dcf_skill"),
  )

  # Gunakan dengan Excel untuk membuat model keuangan
  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {"type": "custom", "skill_id": dcf_skill.id, "version": "latest"},
          ]
      },
      messages=[
          {
              "role": "user",
              "content": "Build a DCF valuation model for a SaaS company",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  print(response)
  ```

  ```typescript TypeScript
  import Anthropic, { toFile } from "@anthropic-ai/sdk";
  import fs from "node:fs";

  const client = new Anthropic();

  // Buat Skill analisis DCF kustom
  const dcfSkill = await client.beta.skills.create({
    files: [await toFile(fs.createReadStream("dcf_skill.zip"), "dcf_skill.zip")]
  });

  // Gunakan dengan Excel untuk membuat model keuangan
  const response = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "custom", skill_id: dcfSkill.id, version: "latest" }
      ]
    },
    messages: [
      {
        role: "user",
        content: "Build a DCF valuation model for a SaaS company"
      }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
  console.log(response);
  ```

  ```csharp C#
  using Anthropic.Core;
  // ...
  AnthropicClient client = new();

  // Buat Skill analisis DCF kustom
  var dcfSkill = await client.Beta.Skills.Create(new SkillCreateParams
  {
      Files =
      [
          new BinaryContent
          {
              Stream = File.OpenRead("dcf_skill/SKILL.md"),
              FileName = "dcf_skill/SKILL.md",
          },
      ],
  });

  // Gunakan dengan Excel untuk membuat model keuangan
  var parameters = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Custom,
                  SkillID = dcfSkill.ID,
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Build a DCF valuation model for a SaaS company" }],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var message = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Skill analisis DCF kustom (ID diperoleh dari respons create Skills API)
  dcfSkillID := "skill_01AbCdEfGhIjKlMnOpQrStUv"

  // Gunakan dengan Excel untuk membuat model keuangan
  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas: []anthropic.AnthropicBeta{
  		"code-execution-2025-08-25",
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  				{
  					Type:    anthropic.BetaSkillParamsTypeCustom,
  					SkillID: dcfSkillID,
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Build a DCF valuation model for a SaaS company")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Skill analisis DCF kustom (ID diperoleh dari respons create Skills API)
      String dcfSkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv";

      // Gunakan bersama Excel Skill untuk membuat model keuangan
      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addBeta("code-execution-2025-08-25")
          .addBeta("skills-2025-10-02")
          .container(BetaContainerParams.builder()
              .skills(List.of(
                  BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.ANTHROPIC)
                      .skillId("xlsx")
                      .version("latest")
                      .build(),
                  BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.CUSTOM)
                      .skillId(dcfSkillId)
                      .version("latest")
                      .build()
              ))
              .build())
          .addUserMessage("Build a DCF valuation model for a SaaS company")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response = client.beta().messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  // Skill analisis DCF kustom (ID diperoleh dari respons create Skills API)
  $dcfSkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv";

  // Gunakan dengan Excel untuk membuat model keuangan
  $message = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Build a DCF valuation model for a SaaS company']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest'],
              ['type' => 'custom', 'skill_id' => $dcfSkillId, 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );
  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Buat Skill analisis DCF kustom
  dcf_skill = client.beta.skills.create(
    files: [
      Anthropic::FilePart.new(
        Pathname("dcf_skill/SKILL.md"),
        filename: "dcf_skill/SKILL.md",
        content_type: "text/markdown"
      )
    ]
  )

  # Gunakan dengan Excel untuk membuat model keuangan
  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "custom", skill_id: dcf_skill.id, version: "latest" }
      ]
    },
    messages: [
      { role: "user", content: "Build a DCF valuation model for a SaaS company" }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts response
  ```
</CodeGroup>

***

## Batasan dan kendala

### Batasan permintaan

* **Maksimum Skill per permintaan:** 20

* **Ukuran unggahan Skill maksimum:** 30 MB (semua file digabungkan, tidak terkompresi)

* **Persyaratan frontmatter YAML:**

  * `name`: Maksimum 64 karakter, hanya huruf kecil/angka/tanda hubung, tanpa tag XML, tanpa kata yang dicadangkan ("anthropic", "claude")
  * `description`: Maksimum 1024 karakter, tidak kosong, tanpa tag XML

### Kendala lingkungan

Skill berjalan di container eksekusi kode dengan batasan berikut:

* **Tanpa akses jaringan:** Tidak dapat melakukan panggilan API eksternal
* **Tanpa instalasi paket saat runtime:** Hanya paket yang sudah terinstal yang tersedia
* **Lingkungan terisolasi:** Container baru dibuat kecuali Anda menentukan ID container yang sudah ada

Lihat [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk paket yang tersedia.

***

## Praktik terbaik

### Kapan menggunakan beberapa Skill

Gabungkan Skill ketika tugas melibatkan beberapa jenis dokumen atau domain:

**Kasus penggunaan yang baik:**

* Analisis data (Excel) + pembuatan presentasi (PowerPoint)
* Pembuatan laporan (Word) + ekspor ke PDF
* Logika domain kustom + pembuatan dokumen

**Hindari:**

* Menyertakan Skill yang tidak digunakan (memengaruhi performa)

### Strategi manajemen versi

Tab SDK di bagian ini menunjukkan nilai `container` yang harus disertakan dalam permintaan Messages. Tab cURL dan CLI menunjukkan permintaan lengkap.

**Untuk produksi:** kunci ke versi tertentu, sehingga pembaruan Skill tidak pernah mengubah perilaku yang telah Anda deploy. Jika Anda menghilangkan `version` atau mengaturnya ke `"latest"`, permintaan menggunakan versi terbaru dari Skill, sehingga versi yang diunggah oleh siapa pun di [workspace](https://platform.claude.com/docs/id/build-with-claude/skills-guide#workspace-scoped-access) langsung mengubah apa yang dijalankan oleh agen produksi Anda. ID versi berasal dari respons create-version di [Pembuatan versi](https://platform.claude.com/docs/id/build-with-claude/skills-guide#versioning) atau dari [API List Skill Versions](https://platform.claude.com/docs/id/api/beta/skills/versions/list). ID selalu berupa string: beri tanda kutip pada ID timestamp epoch dalam JSON atau YAML.

<CodeGroup>
  ```bash cURL
  # Sematkan ke versi tertentu untuk stabilitas
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [{
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "1759178010641129"
        }]
      },
      "messages": [{"role": "user", "content": "Analyze the sales data"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  # Sematkan ke versi tertentu untuk stabilitas
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: "1759178010641129"  # quoted: the API requires a string
  messages:
    - role: user
      content: Analyze the sales data
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  # Sematkan ke versi tertentu untuk stabilitas
  container = {
      "skills": [
          {
              "type": "custom",
              "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
              "version": "1759178010641129",
          }
      ]
  }
  ```

  ```typescript TypeScript
  // Sematkan ke versi tertentu untuk stabilitas
  const container: Anthropic.Beta.Messages.BetaContainerParams = {
    skills: [
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "1759178010641129"
      }
    ]
  };
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Messages;

  // Sematkan ke versi tertentu untuk stabilitas
  var container = new BetaContainerParams
  {
      Skills =
      [
          new BetaSkillParams
          {
              Type = BetaSkillParamsType.Custom,
              SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
              Version = "1759178010641129",
          },
      ],
  };
  ```

  ```go Go
  // Sematkan ke versi tertentu untuk stabilitas
  container := anthropic.BetaMessageNewParamsContainerUnion{
  	OfContainers: &anthropic.BetaContainerParams{
  		Skills: []anthropic.BetaSkillParams{
  			{
  				Type:    anthropic.BetaSkillParamsTypeCustom,
  				SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  				Version: anthropic.String("1759178010641129"),
  			},
  		},
  	},
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;

  void main() {
      // Sematkan ke versi tertentu untuk stabilitas
      BetaContainerParams container = BetaContainerParams.builder()
          .addSkill(BetaSkillParams.builder()
              .type(BetaSkillParams.Type.CUSTOM)
              .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
              .version("1759178010641129")
              .build())
          .build();
  }
  ```

  ```php PHP
  // Sematkan ke versi tertentu untuk stabilitas
  $container = [
      'skills' => [[
          'type' => 'custom',
          'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
          'version' => '1759178010641129'
      ]]
  ];
  ```

  ```ruby Ruby
  # Sematkan ke versi tertentu untuk stabilitas
  container = {
    skills: [{
      type: "custom",
      skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
      version: "1759178010641129"
    }]
  }
  ```
</CodeGroup>

**Untuk pengembangan:** gunakan `latest` untuk mengambil versi terbaru secara otomatis saat Anda melakukan iterasi.

<CodeGroup>
  ```bash cURL
  # Gunakan latest untuk pengembangan aktif
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [{
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "latest"
        }]
      },
      "messages": [{"role": "user", "content": "Analyze the sales data"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  # Gunakan latest untuk pengembangan aktif
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Analyze the sales data
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  # Gunakan latest untuk pengembangan aktif
  container = {
      "skills": [
          {
              "type": "custom",
              "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
              "version": "latest",
          }
      ]
  }
  ```

  ```typescript TypeScript
  // Gunakan latest untuk pengembangan aktif
  const container: Anthropic.Beta.Messages.BetaContainerParams = {
    skills: [
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "latest"
      }
    ]
  };
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Messages;

  // Gunakan versi terbaru untuk pengembangan aktif
  var container = new BetaContainerParams
  {
      Skills =
      [
          new BetaSkillParams
          {
              Type = BetaSkillParamsType.Custom,
              SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
              Version = "latest",
          },
      ],
  };
  ```

  ```go Go
  // Gunakan latest untuk pengembangan aktif
  container := anthropic.BetaMessageNewParamsContainerUnion{
  	OfContainers: &anthropic.BetaContainerParams{
  		Skills: []anthropic.BetaSkillParams{
  			{
  				Type:    anthropic.BetaSkillParamsTypeCustom,
  				SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  				Version: anthropic.String("latest"),
  			},
  		},
  	},
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;

  void main() {
      // Gunakan versi terbaru untuk pengembangan aktif
      BetaContainerParams container = BetaContainerParams.builder()
          .addSkill(BetaSkillParams.builder()
              .type(BetaSkillParams.Type.CUSTOM)
              .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
              .version("latest")
              .build())
          .build();
  }
  ```

  ```php PHP
  // Gunakan latest untuk pengembangan aktif
  $container = [
      'skills' => [[
          'type' => 'custom',
          'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
          'version' => 'latest'
      ]]
  ];
  ```

  ```ruby Ruby
  # Gunakan latest untuk pengembangan aktif
  container = {
    skills: [{
      type: "custom",
      skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
      version: "latest"
    }]
  }
  ```
</CodeGroup>

### Pertimbangan caching prompt

Jika Anda menggunakan [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching), mengubah daftar Skill dalam container Anda akan merusak cache. Skill dirender ke dalam prompt sistem dalam urutan tetap, sehingga daftar yang sama menghasilkan prefiks yang sama dan dapat di-cache:

<CodeGroup>
  ```bash cURL
  # Skill dirender ke dalam prompt sistem dalam urutan tetap yang ramah cache
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
      },
      "messages": [{"role": "user", "content": "Analyze sales data"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'

  # Mengubah daftar Skill ([xlsx] vs [xlsx, pptx]) mengubah prefiks: cache miss, sedangkan daftar yang identik adalah cache hit
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
          {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
        ]
      },
      "messages": [{"role": "user", "content": "Create a presentation"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  # Skill dirender ke dalam prompt sistem dalam urutan tetap yang ramah cache
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
  messages:
    - role: user
      content: Analyze sales data
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML

  # Mengubah daftar Skill ([xlsx] vs [xlsx, pptx]) mengubah prefiks: cache miss, sedangkan daftar yang identik adalah cache hit
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
      - type: anthropic
        skill_id: pptx
        version: latest
  messages:
    - role: user
      content: Create a presentation
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Skill dirender ke dalam prompt sistem dengan urutan tetap yang ramah cache
  response1 = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=[
          "code-execution-2025-08-25",
          "skills-2025-10-02",
      ],
      container={
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      messages=[{"role": "user", "content": "Analyze sales data"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Mengubah daftar Skill ([xlsx] vs [xlsx, pptx]) mengubah prefiks: cache miss, sedangkan daftar yang identik adalah cache hit
  response2 = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      betas=[
          "code-execution-2025-08-25",
          "skills-2025-10-02",
      ],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {
                  "type": "anthropic",
                  "skill_id": "pptx",
                  "version": "latest",
              },  # prefix change: cache miss
          ]
      },
      messages=[{"role": "user", "content": "Create a presentation"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Skill dirender ke dalam prompt sistem dalam urutan tetap yang ramah cache
  const response1 = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [{ role: "user", content: "Analyze sales data" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Mengubah daftar Skill ([xlsx] vs [xlsx, pptx]) mengubah prefiks: cache miss, sedangkan daftar yang identik adalah cache hit
  const response2 = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "anthropic", skill_id: "pptx", version: "latest" } // prefix change: cache miss
      ]
    },
    messages: [{ role: "user", content: "Create a presentation" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Skill di-render ke dalam prompt sistem dengan urutan tetap yang ramah cache
  var parameters1 = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Analyze sales data" }],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var response1 = await client.Beta.Messages.Create(parameters1);
  Console.WriteLine(response1);

  // Kumpulan Skill berbeda ([xlsx] vs [xlsx, pptx]) = prefiks berbeda: cache miss (kumpulan identik adalah cache hit)
  var parameters2 = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "pptx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Create a presentation" }],
      Tools = [new BetaCodeExecutionTool20250825()],
  };

  var response2 = await client.Beta.Messages.Create(parameters2);
  Console.WriteLine(response2);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Skill dirender ke dalam prompt sistem dalam urutan tetap yang ramah cache
  response1, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas: []anthropic.AnthropicBeta{
  		"code-execution-2025-08-25",
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Analyze sales data")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response1)

  // Mengubah daftar Skill ([xlsx] vs [xlsx, pptx]) mengubah prefiks: cache miss, sedangkan daftar yang identik adalah cache hit
  response2, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas: []anthropic.AnthropicBeta{
  		"code-execution-2025-08-25",
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "pptx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a presentation")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response2)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Skill dirender ke dalam prompt sistem dalam urutan tetap yang ramah cache
      MessageCreateParams params1 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addBeta("code-execution-2025-08-25")
          .addBeta("skills-2025-10-02")
          .container(BetaContainerParams.builder()
              .skills(List.of(
                  BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.ANTHROPIC)
                      .skillId("xlsx")
                      .version("latest")
                      .build()
              ))
              .build())
          .addUserMessage("Analyze sales data")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response1 = client.beta().messages().create(params1);
      System.out.println(response1);

      // Mengubah daftar Skill ([xlsx] vs [xlsx, pptx]) mengubah prefiks: cache miss, sedangkan daftar yang identik adalah cache hit
      MessageCreateParams params2 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addBeta("code-execution-2025-08-25")
          .addBeta("skills-2025-10-02")
          .container(BetaContainerParams.builder()
              .skills(List.of(
                  BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.ANTHROPIC)
                      .skillId("xlsx")
                      .version("latest")
                      .build(),
                  BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.ANTHROPIC)
                      .skillId("pptx")
                      .version("latest")
                      .build()
              ))
              .build())
          .addUserMessage("Create a presentation")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response2 = client.beta().messages().create(params2);
      System.out.println(response2);
  }
  ```

  ```php PHP
  $client = new Client();

  // Skill dirender ke dalam prompt sistem dengan urutan tetap yang ramah cache
  $response1 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze sales data']
      ],
      model: 'claude-opus-5',
      betas: [
          'code-execution-2025-08-25',
          'skills-2025-10-02',
      ],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );
  echo $response1;

  // Mengubah daftar Skill ([xlsx] vs [xlsx, pptx]) mengubah prefiks: cache miss, sedangkan daftar yang identik adalah cache hit
  $response2 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Create a presentation']
      ],
      model: 'claude-opus-5',
      betas: [
          'code-execution-2025-08-25',
          'skills-2025-10-02',
      ],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest'],
              ['type' => 'anthropic', 'skill_id' => 'pptx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );
  echo $response2;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Skill dirender ke dalam prompt sistem dalam urutan tetap yang ramah cache
  response1 = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: [
      "code-execution-2025-08-25",
      "skills-2025-10-02",
    ],
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [{ role: "user", content: "Analyze sales data" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts response1

  # Mengubah daftar Skill ([xlsx] vs [xlsx, pptx]) mengubah prefiks: cache miss, sedangkan daftar yang identik adalah cache hit
  response2 = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    betas: [
      "code-execution-2025-08-25",
      "skills-2025-10-02",
    ],
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "anthropic", skill_id: "pptx", version: "latest" } # prefix change: cache miss
      ]
    },
    messages: [{ role: "user", content: "Create a presentation" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts response2
  ```
</CodeGroup>

Untuk performa caching terbaik, jaga agar daftar Skill Anda, termasuk urutannya, konsisten di seluruh permintaan. Mengunci versi Skill kustom juga membantu: dengan `"latest"`, menerbitkan versi baru dapat membatalkan prefiks yang di-cache jika hal itu mengubah deskripsi Skill.

### Penanganan error

Tangani error terkait Skill dengan baik:

<CodeGroup>
  ```bash cURL
  # Alur penanganan error ini tidak cocok diterapkan pada perintah shell sekali jalan;
  # salah satu opsi SDK akan lebih sesuai. Permintaan yang gagal
  # mengembalikan HTTP 400 dengan JSON error yang .error.message-nya menyebutkan
  # masalah Skill tersebut.
  ```

  ```bash CLI
  if ! RESULT=$(ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 \
    --transform-error error.message \
    --format-error yaml 2>&1 <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Process data
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ); then
    case "$RESULT" in
      *skill*)
        printf 'Skill error: %s\n' "$RESULT"
        # Tangani error spesifik skill
        ;;
      *)
        printf '%s\n' "$RESULT" >&2
        exit 1
        ;;
    esac
  fi
  ```

  ```python Python
  client = anthropic.Anthropic()

  try:
      response = client.beta.messages.create(
          model="claude-opus-5",
          max_tokens=4096,
          betas=["code-execution-2025-08-25", "skills-2025-10-02"],
          container={
              "skills": [
                  {
                      "type": "custom",
                      "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                      "version": "latest",
                  }
              ]
          },
          messages=[{"role": "user", "content": "Process data"}],
          tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
      )
  except anthropic.BadRequestError as e:
      if "skill" in str(e):
          print(f"Skill error: {e}")
          # Tangani error spesifik skill
      else:
          raise
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  try {
    const response = await client.beta.messages.create({
      model: "claude-opus-5",
      max_tokens: 4096,
      betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
      container: {
        skills: [
          { type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }
        ]
      },
      messages: [{ role: "user", content: "Process data" }],
      tools: [{ type: "code_execution_20250825", name: "code_execution" }]
    });
    console.log(response);
  } catch (error) {
    if (error instanceof Anthropic.BadRequestError && error.message.includes("skill")) {
      console.error(`Skill error: ${error.message}`);
      // Tangani error spesifik skill
    } else {
      throw error;
    }
  }
  ```

  ```csharp C#
  using Anthropic.Exceptions;
  // ...
  AnthropicClient client = new();

  try
  {
      var parameters = new MessageCreateParams
      {
          Model = "claude-opus-5",
          MaxTokens = 4096,
          Betas = ["code-execution-2025-08-25", "skills-2025-10-02"],
          Container = new BetaContainerParams
          {
              Skills =
              [
                  new BetaSkillParams
                  {
                      Type = BetaSkillParamsType.Custom,
                      SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                      Version = "latest",
                  },
              ],
          },
          Messages = [new() { Role = Role.User, Content = "Process data" }],
          Tools = [new BetaCodeExecutionTool20250825()],
      };

      var response = await client.Beta.Messages.Create(parameters);
      Console.WriteLine(response);
  }
  catch (AnthropicBadRequestException e) when (e.Message.Contains("skill"))
  {
      Console.WriteLine($"Skill error: {e.Message}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Betas:     []anthropic.AnthropicBeta{"code-execution-2025-08-25", anthropic.AnthropicBetaSkills2025_10_02},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Process data")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  })

  if err != nil {
  	var apierr *anthropic.Error
  	if errors.As(err, &apierr) && apierr.Type() == anthropic.ErrorTypeInvalidRequestError &&
  		strings.Contains(apierr.Error(), "skill") {
  		fmt.Printf("Skill error: %v\n", apierr)
  	} else {
  		log.Fatal(err)
  	}
  	return
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.errors.BadRequestException;
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      try {
          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5)
              .maxTokens(4096L)
              .addBeta("code-execution-2025-08-25")
              .addBeta("skills-2025-10-02")
              .container(BetaContainerParams.builder()
                  .addSkill(BetaSkillParams.builder()
                      .type(BetaSkillParams.Type.CUSTOM)
                      .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                      .version("latest")
                      .build())
                  .build())
              .addUserMessage("Process data")
              .addTool(BetaCodeExecutionTool20250825.builder().build())
              .build();

          BetaMessage response = client.beta().messages().create(params);
          System.out.println(response);
      } catch (BadRequestException e) {
          if (e.getMessage().contains("skill")) {
              System.err.println("Skill error: " + e.getMessage());
          } else {
              throw e;
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Core\Exceptions\BadRequestException;

  $client = new Client();

  try {
      $message = $client->beta->messages->create(
          maxTokens: 4096,
          messages: [
              ['role' => 'user', 'content' => 'Process data']
          ],
          model: 'claude-opus-5',
          betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
          container: [
              'skills' => [
                  [
                      'type' => 'custom',
                      'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                      'version' => 'latest'
                  ]
              ]
          ],
          tools: [
              ['type' => 'code_execution_20250825', 'name' => 'code_execution']
          ]
      );
      echo $message;
  } catch (BadRequestException $e) {
      if (str_contains($e->getMessage(), 'skill')) {
          echo "Skill error: " . $e->getMessage();
      } else {
          throw $e;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  begin
    response = client.beta.messages.create(
      model: "claude-opus-5",
      max_tokens: 4096,
      betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
      container: {
        skills: [
          {
            type: "custom",
            skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
            version: "latest"
          }
        ]
      },
      messages: [{ role: "user", content: "Process data" }],
      tools: [{ type: "code_execution_20250825", name: "code_execution" }]
    )
  rescue Anthropic::Errors::BadRequestError => e
    if e.message.include?("skill")
      puts "Skill error: #{e.message}"
    else
      raise
    end
  end
  ```
</CodeGroup>

***

## Retensi data

Agent Skills tidak tercakup dalam pengaturan ZDR. Definisi Skill dan data eksekusi disimpan sesuai dengan kebijakan retensi data standar Anthropic.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

## Pencatatan audit

Jika organisasi Anda telah mengaktifkan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api), [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed)-nya mencatat pembuatan dan penghapusan Skill serta versi Skill yang dilakukan dengan kunci API Claude atau dari Claude Console. Operasi yang terjadi saat Compliance API dinonaktifkan tidak dicatat dan tidak dapat dipulihkan kemudian, jadi [siapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) sebelum Anda mengandalkan jejak audit ini.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Referensi API" icon="book" href="https://platform.claude.com/docs/id/api/beta/skills/create">
    Referensi API lengkap dengan semua endpoint
  </Card>

  <Card title="Praktik terbaik penulisan Skill" icon="edit" href="https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices">
    Pelajari cara menulis Skill yang efektif agar Claude dapat menemukan dan menggunakannya dengan sukses.
  </Card>

  <Card title="Alat eksekusi kode" icon="terminal" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan kode Python dan bash dalam container sandbox untuk menganalisis data, menghasilkan file, dan melakukan iterasi pada solusi.
  </Card>
</CardGroup>
