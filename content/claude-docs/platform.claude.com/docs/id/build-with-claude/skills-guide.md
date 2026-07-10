---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/skills-guide
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: e3fd704f58399f0df7596174c7f2ff6f26afa1d1d8c3c470cc4ccafb0762688a
---

# Menggunakan Agent Skills dengan API

Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.

---

Agent Skills memperluas kemampuan Claude melalui folder terorganisir yang berisi instruksi, skrip, dan sumber daya. Panduan ini menunjukkan cara menggunakan Skills bawaan maupun kustom dengan Claude API.

<Note>
  Untuk referensi API lengkap termasuk skema request/response dan semua parameter, lihat:

  * [Referensi API Manajemen Skill](/docs/id/api/beta/skills/list) - Operasi CRUD untuk Skills
  * [Referensi API Versi Skill](/docs/id/api/beta/skills/versions/list) - Manajemen versi
</Note>

<Note>
  Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Tautan cepat

<CardGroup cols={2}>
  <Card title="Mulai dengan Agent Skills" icon="rocket" href="/docs/id/agents-and-tools/agent-skills/quickstart">
    Buat Skill pertama Anda
  </Card>

  <Card title="Buat Skills kustom" icon="hammer" href="/docs/id/agents-and-tools/agent-skills/best-practices">
    Praktik terbaik untuk menulis Skills
  </Card>
</CardGroup>

## Ikhtisar

<Note>
  Untuk pembahasan mendalam tentang arsitektur dan penerapan Agent Skills di dunia nyata, baca postingan blog engineering: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

Skills terintegrasi dengan Messages API melalui [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool). Baik menggunakan Skills bawaan yang dikelola oleh Anthropic maupun Skills kustom yang Anda unggah, bentuk integrasinya identik: keduanya memerlukan eksekusi kode dan menggunakan struktur `container` yang sama.

### Menggunakan Skills

Skills terintegrasi secara identik di Messages API terlepas dari sumbernya. Anda menentukan Skills dalam parameter `container` dengan `skill_id`, `type`, dan `version` opsional, dan Skills tersebut dieksekusi di lingkungan eksekusi kode.

**Anda dapat menggunakan Skills dari dua sumber:**

| Aspek            | Skills Anthropic                           | Skills Kustom                                                           |
| ---------------- | ------------------------------------------ | ----------------------------------------------------------------------- |
| **Nilai type**   | `anthropic`                                | `custom`                                                                |
| **ID Skill**     | Nama pendek: `pptx`, `xlsx`, `docx`, `pdf` | Dihasilkan otomatis: `skill_01AbCdEfGhIjKlMnOpQrStUv`                   |
| **Format versi** | Berbasis tanggal: `20251013` atau `latest` | Timestamp epoch: `1759178010641129` atau `latest`                       |
| **Manajemen**    | Bawaan dan dikelola oleh Anthropic         | Unggah dan kelola melalui [Skills API](/docs/id/api/beta/skills/create) |
| **Ketersediaan** | Tersedia untuk semua pengguna              | Privat untuk workspace Anda                                             |

Kedua sumber skill dikembalikan oleh [endpoint List Skills](/docs/id/api/beta/skills/list) (gunakan parameter `source` untuk memfilter). Bentuk integrasi dan lingkungan eksekusinya identik. Satu-satunya perbedaan adalah dari mana Skills berasal dan bagaimana Skills tersebut dikelola.

### Prasyarat

Untuk menggunakan Skills, Anda memerlukan:

1. **Kunci API Claude** dari [Console](/settings/keys)

2. **Header beta:**

   * `code-execution-2025-08-25` - Mengaktifkan eksekusi kode (diperlukan untuk Skills)
   * `skills-2025-10-02` - Mengaktifkan Skills API
   * `files-api-2025-04-14` - Untuk mengunggah/mengunduh file ke/dari container

3. **[Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool)** diaktifkan dalam request Anda

***

## Menggunakan Skills dalam Messages

### Parameter container

Skills ditentukan menggunakan parameter `container` di Messages API. Anda dapat menyertakan hingga 8 Skills per request.

Strukturnya identik untuk Skills Anthropic maupun kustom. Tentukan `type` dan `skill_id` yang diperlukan, dan secara opsional sertakan `version` untuk mengunci ke versi tertentu:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
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
  model: claude-opus-4-8
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
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
      Model = "claude-opus-4-8",
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
  	Model:     "claude-opus-4-8",
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
          .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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

Ketika Skills membuat dokumen (Excel, PowerPoint, PDF, Word), Skills mengembalikan atribut `file_id` dalam respons. Anda harus menggunakan Files API untuk mengunduh file-file ini.

**Cara kerjanya:**

1. Skills membuat file selama eksekusi kode.
2. Respons menyertakan `file_id` untuk setiap file yang dibuat.
3. Gunakan Files API untuk mengunduh konten file yang sebenarnya.
4. Simpan secara lokal atau proses sesuai kebutuhan.

**Contoh: Membuat dan mengunduh file Excel**

<CodeGroup>
  ```bash cURL
  # Langkah 1: Gunakan Skill untuk membuat file
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
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
  model: claude-opus-4-8
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
    --transform filename --raw-output)

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
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
      Model = "claude-opus-4-8",
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
  		Model:     "claude-opus-4-8",
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
          .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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
  # Mendapatkan metadata file
  curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"

  # Menampilkan daftar semua file
  curl "https://api.anthropic.com/v1/files" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"

  # Menghapus file
  curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```

  ```bash CLI
  # Mendapatkan metadata file
  ant beta:files retrieve-metadata --file-id "$FILE_ID" \
    --transform '{filename,size_bytes}' --format yaml

  # Menampilkan daftar semua file
  ant beta:files list \
    --transform '{filename,created_at}' --format yaml

  # Menghapus file
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

  // Mendapatkan metadata file
  var fileInfo = await client.Beta.Files.RetrieveMetadata(fileId);
  Console.WriteLine($"Filename: {fileInfo.Filename}, Size: {fileInfo.SizeBytes} bytes");

  // Menampilkan daftar file
  await foreach (var file in (await client.Beta.Files.List()).Paginate())
  {
      Console.WriteLine($"{file.Filename} - {file.CreatedAt}");
  }

  // Menghapus file
  await client.Beta.Files.Delete(fileId);
  ```

  ```go Go
  client := anthropic.NewClient()
  fileID := "file_011CNha8iCJcU1wXNR6q4V8w"

  // Mendapatkan metadata file
  fileInfo, err := client.Beta.Files.GetMetadata(context.TODO(), fileID, anthropic.BetaFileGetMetadataParams{})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Printf("Filename: %s, Size: %d bytes\n", fileInfo.Filename, fileInfo.SizeBytes)

  // Menampilkan daftar semua file
  files := client.Beta.Files.ListAutoPaging(context.TODO(), anthropic.BetaFileListParams{})
  for files.Next() {
  	file := files.Current()
  	fmt.Printf("%s - %s\n", file.Filename, file.CreatedAt)
  }
  if files.Err() != nil {
  	log.Fatal(files.Err())
  }

  // Menghapus file
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

      // Mendapatkan metadata file
      FileMetadata fileInfo = client.beta().files().retrieveMetadata(fileId);
      System.out.println("Filename: " + fileInfo.filename() + ", Size: " + fileInfo.sizeBytes() + " bytes");

      // Menampilkan daftar file (halaman pertama)
      FileListPage files = client.beta().files().list();
      for (var file : files.data()) {
          System.out.println(file.filename() + " - " + file.createdAt());
      }

      // Menghapus file
      client.beta().files().delete(fileId);
  }
  ```

  ```php PHP
  $client = new Client();
  $fileId = 'file_011CNha8iCJcU1wXNR6q4V8w';

  // Mendapatkan metadata file
  $fileInfo = $client->beta->files->retrieveMetadata($fileId);
  echo "Filename: {$fileInfo->filename}, Size: {$fileInfo->sizeBytes} bytes\n";

  // Menampilkan daftar file (halaman pertama)
  $files = $client->beta->files->list();
  foreach ($files->data as $file) {
      echo "{$file->filename} - {$file->createdAt->format(DATE_ATOM)}\n";
  }

  // Menghapus file
  $client->beta->files->delete($fileId);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  file_id = "file_011CNha8iCJcU1wXNR6q4V8w"

  # Mendapatkan metadata file
  file_info = client.beta.files.retrieve_metadata(file_id)
  puts "Filename: #{file_info.filename}, Size: #{file_info.size_bytes} bytes"

  # Menampilkan daftar semua file
  client.beta.files.list.auto_paging_each do |file|
    puts "#{file.filename} - #{file.created_at}"
  end

  # Menghapus file
  client.beta.files.delete(file_id)
  ```
</CodeGroup>

<Note>
  Untuk detail lengkap tentang Files API, lihat [dokumentasi Files API](/docs/id/api/files-content).
</Note>

### Percakapan multi-giliran

Gunakan kembali container yang sama di beberapa pesan dengan menentukan ID container:

<CodeGroup>
  ```bash cURL
  # Penggunaan ulang container multi-giliran tidak cocok untuk perintah shell
  # sekali pakai; salah satu opsi SDK akan lebih sesuai. Ambil
  # container.id dari respons pertama, lalu teruskan pada permintaan berikutnya sebagai
  # "container": {"id": "...", "skills": [...]} bersama riwayat percakapan.
  ```

  ```bash CLI
  # Permintaan pertama membuat container
  CONTAINER_ID=$(ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 \
    --transform container.id --raw-output <<'YAML'
  model: claude-opus-4-8
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

  # Lanjutkan percakapan dengan container yang sama
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<YAML
  model: claude-opus-4-8
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

  # Permintaan pertama membuat container
  response1 = client.beta.messages.create(
      model="claude-opus-4-8",
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

  # Lanjutkan percakapan dengan container yang sama
  messages = [
      {"role": "user", "content": "Create a sample sales dataset and analyze it"},
      {
          # Bawa teks asisten ke permintaan berikutnya; container.id membawa status eksekusi
          "role": "assistant",
          "content": "\n".join(
              block.text for block in response1.content if block.type == "text"
          ),
      },
      {"role": "user", "content": "What was the total revenue?"},
  ]

  response2 = client.beta.messages.create(
      model="claude-opus-4-8",
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

  // Permintaan pertama membuat container
  const response1 = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [{ role: "user", content: "Create a sample sales dataset and analyze it" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Lanjutkan percakapan dengan container yang sama
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Create a sample sales dataset and analyze it" },
    {
      role: "assistant",
      // Bawa teks asisten ke permintaan berikutnya; container.id membawa status eksekusi
      content: response1.content
        .filter((block) => block.type === "text")
        .map((block) => block.text)
        .join("\n")
    },
    { role: "user", content: "What was the total revenue?" }
  ];

  const response2 = await client.beta.messages.create({
    model: "claude-opus-4-8",
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
      Model = "claude-opus-4-8",
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

  // Lanjutkan percakapan dalam container yang sama
  // Teruskan teks asisten; container.id membawa status eksekusi
  var assistantText = string.Join(
      "\n",
      response1.Content.Select(block => block.TryPickText(out var text) ? text.Text : null).Where(t => t is not null)
  );

  var parameters2 = new MessageCreateParams
  {
      Model = "claude-opus-4-8",
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
  	Model:     "claude-opus-4-8",
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

  // Teruskan teks asisten ke depan; container.id membawa status eksekusi
  var textParts []string
  for _, block := range response1.Content {
  	if block.Type == "text" {
  		textParts = append(textParts, block.Text)
  	}
  }
  assistantText := strings.Join(textParts, "\n")

  response2, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-4-8",
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
          .model(Model.CLAUDE_OPUS_4_8)
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
          .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
      // Teruskan teks asisten ke langkah berikutnya; container.id membawa status eksekusi
      ['role' => 'assistant', 'content' => implode("\n", array_map(
          fn ($block) => $block->text,
          array_filter($response1->content, fn ($block) => $block->type === 'text'),
      ))],
      ['role' => 'user', 'content' => 'What was the total revenue?']
  ];

  $response2 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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
    model: "claude-opus-4-8",
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

Skills dapat melakukan operasi yang memerlukan beberapa giliran. Tangani alasan berhenti `pause_turn`:

<CodeGroup>
  ```bash cURL
  # Permintaan awal
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
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

  # Jika stop_reason adalah "pause_turn", lanjutkan di container yang sama, dengan menambahkan
  # array content dari respons sebelumnya ke messages sebagai giliran asisten.
  # Ulangi permintaan lanjutan ini sampai stop_reason bukan lagi "pause_turn".
  STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason')
  CONTAINER_ID=$(echo "$RESPONSE" | jq -r '.container.id')

  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-4-8\",
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

  # Permintaan awal: simpan respons JSON lengkap ke file sementara
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 \
    > "$RESP" <<'YAML'
  model: claude-opus-4-8
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

  # Jika stop_reason adalah "pause_turn", lanjutkan di container yang sama,
  # dengan menambahkan array content dari respons sebelumnya ke messages sebagai
  # giliran asisten. Ulangi hingga stop_reason bukan lagi "pause_turn".
  CONTAINER_ID=$(jq -r '.container.id' "$RESP")

  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 \
    > "$RESP" <<YAML
  model: claude-opus-4-8
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
      model="claude-opus-4-8",
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

  # Menangani pause_turn untuk operasi yang panjang
  for _ in range(max_retries):
      if response.stop_reason != "pause_turn":
          break

      messages.append({"role": "assistant", "content": response.content})
      response = client.beta.messages.create(
          model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{ type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }]
    },
    messages,
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Menangani pause_turn untuk operasi yang lama
  for (let i = 0; i < maxRetries; i++) {
    if (response.stop_reason !== "pause_turn") {
      break;
    }

    messages.push({
      role: "assistant",
      content: response.content as Anthropic.Beta.Messages.BetaContentBlockParam[]
    });
    response = await client.beta.messages.create({
      model: "claude-opus-4-8",
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
          Model = "claude-opus-4-8",
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

      // Tambahkan konten dari giliran yang dijeda lalu lanjutkan
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
  	Model:     "claude-opus-4-8",
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
  		Model:     "claude-opus-4-8",
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
              .model(Model.CLAUDE_OPUS_4_8)
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
                  .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
          model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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
      model: "claude-opus-4-8",
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
  Respons dapat menyertakan alasan berhenti `pause_turn`, yang menunjukkan bahwa API menjeda operasi Skill yang berjalan lama. Anda dapat memberikan respons tersebut kembali apa adanya dalam request berikutnya agar Claude melanjutkan gilirannya, atau memodifikasi kontennya jika Anda ingin menginterupsi percakapan dan memberikan panduan tambahan.
</Note>

### Menggunakan beberapa Skills

Gabungkan beberapa Skills dalam satu request untuk menangani alur kerja yang kompleks:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
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
  model: claude-opus-4-8
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
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
      Model = "claude-opus-4-8",
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
  	Model:     "claude-opus-4-8",
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
          .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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

## Mengelola Skills kustom

### Membuat Skill

Bundel Skill adalah direktori yang berisi file `SKILL.md` di tingkat teratas dengan frontmatter YAML `name` dan `description`, ditambah skrip atau sumber daya pendukung apa pun. Lihat [Mulai dengan Agent Skills di API](/docs/id/agents-and-tools/agent-skills/quickstart) untuk membuatnya, dan daftar **Persyaratan** setelah contoh-contoh untuk batasan lengkapnya.

Unggah Skill kustom Anda agar tersedia di workspace Anda. Anda dapat mengunggah arsip zip atau objek file individual; Python SDK juga menyediakan helper `files_from_dir` yang menerima path direktori.

File diidentifikasi berdasarkan nama file yang Anda lampirkan. Unggahan per-file harus mempertahankan direktori tingkat teratas yang sama dalam path-nya (sufiks `;filename=` dalam contoh cURL dan argumen nama file dalam contoh SDK), dan arsip zip harus berisi direktori skill sebagai satu-satunya entri tingkat teratas.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "files[]=@financial_skill/SKILL.md;filename=financial_skill/SKILL.md" \
    -F "files[]=@financial_skill/analyze.py;filename=financial_skill/analyze.py"
  ```

  ```bash CLI
  ant beta:skills create \
    --file example_skill.zip \
    --beta skills-2025-10-02

  # Unggahan per file memerlukan nama file dengan path lengkap, yang saat ini
  # belum dapat diatur oleh CLI. Sebagai gantinya, unggah arsip zip.
  ```

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

  # Opsi 3: Menggunakan helper files_from_dir (khusus Python)
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

  // Opsi 2: Menggunakan file satu per satu (nama file dengan path lengkap mempertahankan tata letak direktori Skill)
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

      // Opsi 2: Menggunakan file individual (nama file dengan path lengkap mempertahankan tata letak direktori Skill)
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

* Harus menyertakan file SKILL.md di tingkat teratas

* Semua file harus menentukan direktori root yang sama dalam path-nya

* Nama direktori tingkat teratas harus cocok dengan `name` di frontmatter SKILL.md (tidak peka huruf besar/kecil dan garis bawah: `Financial_Skill` cocok dengan `financial-skill`)

* `display_title` bersifat opsional: jika dihilangkan, nilainya diturunkan dari `name` di SKILL.md; nilai eksplisit harus unik di antara skill kustom di workspace Anda

* Total ukuran unggahan harus di bawah 30 MB

* Persyaratan frontmatter YAML:

  * `name`: Maksimum 64 karakter, hanya huruf kecil/angka/tanda hubung, tanpa tag XML, tanpa kata yang dicadangkan ("anthropic", "claude")
  * `description`: Maksimum 1024 karakter, tidak boleh kosong, tanpa tag XML

Untuk skema request/response lengkap, lihat [referensi API Create Skill](/docs/id/api/beta/skills/create).

### Menampilkan daftar Skills

Ambil semua Skills yang tersedia untuk workspace Anda, termasuk Skills bawaan Anthropic dan Skills kustom Anda. Gunakan parameter `source` untuk memfilter berdasarkan jenis skill:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # Mencantumkan semua Skill
  curl "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"

  # Mencantumkan hanya Skill kustom
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

  // Daftar semua Skills
  for await (const skill of client.beta.skills.list()) {
    console.log(`${skill.id}: ${skill.display_title} (source: ${skill.source})`);
  }

  // Daftar hanya Skills kustom
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

  // Menampilkan daftar Skill (halaman pertama)
  $skills = $client->beta->skills->list();

  foreach ($skills->data as $skill) {
      echo "{$skill->id}: {$skill->displayTitle} (source: {$skill->source})\n";
  }

  // Menampilkan daftar Skill kustom saja
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

Lihat [referensi API List Skills](/docs/id/api/beta/skills/list) untuk opsi paginasi dan pemfilteran.

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

Untuk menghapus Skill, Anda harus terlebih dahulu menghapus semua versinya:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # Langkah 1: Daftar versi-versinya, lalu hapus satu per satu
  curl "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"

  # Ulangi untuk setiap versi yang dikembalikan oleh daftar
  curl -X DELETE "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions/1759178010641129" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"

  # Langkah 2: Hapus Skill
  curl -X DELETE "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"
  ```

  ```bash CLI
  # Langkah 1: Daftar versi-versinya, lalu hapus satu per satu
  ant beta:skills:versions list \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
    --transform version --raw-output

  # Ulangi untuk setiap id versi yang dikembalikan daftar tersebut
  ant beta:skills:versions delete \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
    --version 1759178010641129 >/dev/null

  # Langkah 2: Hapus Skill
  ant beta:skills delete \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv >/dev/null
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Langkah 1: Hapus semua versi
  for version in client.beta.skills.versions.list(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv"
  ):
      client.beta.skills.versions.delete(
          skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
          version=version.version,
      )

  # Langkah 2: Hapus Skill
  client.beta.skills.delete(skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Langkah 1: Hapus semua versi
  for await (const version of client.beta.skills.versions.list(
    "skill_01AbCdEfGhIjKlMnOpQrStUv"
  )) {
    await client.beta.skills.versions.delete(version.version, {
      skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv"
    });
  }

  // Langkah 2: Hapus Skill
  await client.beta.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Skills.Versions;
  // ...
  AnthropicClient client = new();

  // Langkah 1: Hapus semua versi
  await foreach (var version in (await client.Beta.Skills.Versions.List("skill_01AbCdEfGhIjKlMnOpQrStUv")).Paginate())
  {
      await client.Beta.Skills.Versions.Delete(
          version.Version,
          new VersionDeleteParams { SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv" }
      );
  }

  // Langkah 2: Hapus Skill
  await client.Beta.Skills.Delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
  ```

  ```go Go
  client := anthropic.NewClient()

  // Langkah 1: Hapus semua versi
  versions := client.Beta.Skills.Versions.ListAutoPaging(
  	context.TODO(),
  	"skill_01AbCdEfGhIjKlMnOpQrStUv",
  	anthropic.BetaSkillVersionListParams{},
  )

  for versions.Next() {
  	version := versions.Current()
  	_, err := client.Beta.Skills.Versions.Delete(
  		context.TODO(),
  		version.Version,
  		anthropic.BetaSkillVersionDeleteParams{
  			SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  		},
  	)
  	if err != nil {
  		log.Fatal(err)
  	}
  }
  if versions.Err() != nil {
  	log.Fatal(versions.Err())
  }

  // Langkah 2: Hapus Skill
  _, err := client.Beta.Skills.Delete(
  	context.TODO(),
  	"skill_01AbCdEfGhIjKlMnOpQrStUv",
  	anthropic.BetaSkillDeleteParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.skills.versions.VersionListPage;
  import com.anthropic.models.beta.skills.versions.VersionDeleteParams;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Langkah 1: Hapus semua versi
      VersionListPage versions = client.beta().skills().versions().list("skill_01AbCdEfGhIjKlMnOpQrStUv");

      for (var version : versions.autoPager()) {
          client.beta().skills().versions().delete(
              version.version(),
              VersionDeleteParams.builder()
                  .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                  .build()
          );
      }

      // Langkah 2: Hapus Skill
      client.beta().skills().delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
  }
  ```

  ```php PHP
  $client = new Client();

  // Langkah 1: Hapus semua versi
  $versions = $client->beta->skills->versions->list(
      skillID: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
  );

  foreach ($versions->pagingEachItem() as $version) {
      $client->beta->skills->versions->delete(
          skillID: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
          version: $version->version,
      );
  }

  // Langkah 2: Hapus Skill
  $client->beta->skills->delete(
      skillID: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Langkah 1: Hapus semua versi
  client.beta.skills.versions.list("skill_01AbCdEfGhIjKlMnOpQrStUv").auto_paging_each do |version|
    client.beta.skills.versions.delete(
      version.version,
      skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv"
    )
  end

  # Langkah 2: Hapus Skill
  client.beta.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv")
  ```
</CodeGroup>

Mencoba menghapus Skill yang masih memiliki versi akan mengembalikan error 400.

### Pembuatan versi

Skills mendukung pembuatan versi untuk mengelola pembaruan dengan aman:

**Skills Anthropic:**

* Versi menggunakan format tanggal: `20251013`
* Versi baru dirilis saat pembaruan dilakukan
* Tentukan versi yang tepat untuk stabilitas

**Skills Kustom:**

* Timestamp epoch yang dihasilkan otomatis: `1759178010641129`
* Gunakan `"latest"` untuk selalu mendapatkan versi terbaru
* Buat versi baru saat memperbarui file Skill

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # Membuat versi baru
  NEW_VERSION=$(curl -X POST "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "files[]=@updated_skill/SKILL.md;filename=updated_skill/SKILL.md")

  VERSION_NUMBER=$(echo "$NEW_VERSION" | jq -r '.version')

  # Menggunakan versi spesifik
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-4-8\",
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

  # Menggunakan versi terbaru
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
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
  # Membuat versi baru
  VERSION_NUMBER=$(ant beta:skills:versions create \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
    --file updated_skill.zip \
    --transform version --raw-output)

  # Gunakan versi spesifik
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<YAML
  model: claude-opus-4-8
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: $VERSION_NUMBER
  messages:
    - role: user
      content: Use updated Skill
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML

  # Gunakan versi terbaru
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<'YAML'
  model: claude-opus-4-8
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

  # Membuat versi baru

  new_version = client.beta.skills.versions.create(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      files=files_from_dir("/path/to/updated_skill"),
  )

  # Menggunakan versi tertentu
  response = client.beta.messages.create(
      model="claude-opus-4-8",
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

  # Menggunakan versi terbaru
  response = client.beta.messages.create(
      model="claude-opus-4-8",
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

  // Membuat versi baru menggunakan file zip
  const newVersion = await client.beta.skills.versions.create("skill_01AbCdEfGhIjKlMnOpQrStUv", {
    files: [fs.createReadStream("updated_skill.zip")]
  });

  // Menggunakan versi tertentu
  const specificVersionResponse = await client.beta.messages.create({
    model: "claude-opus-4-8",
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

  // Menggunakan versi terbaru
  const latestVersionResponse = await client.beta.messages.create({
    model: "claude-opus-4-8",
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

  // Membuat versi baru
  var versionParams = new VersionCreateParams
  {
      Files =
      [
          new BinaryContent
          {
              Stream = File.OpenRead("/path/to/updated_skill/SKILL.md"),
              FileName = "updated_skill/SKILL.md",
          },
      ],
  };

  var newVersion = await client.Beta.Skills.Versions.Create("skill_01AbCdEfGhIjKlMnOpQrStUv", versionParams);

  // Menggunakan versi tertentu
  var specificVersionParams = new MessageCreateParams
  {
      Model = "claude-opus-4-8",
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

  // Menggunakan versi terbaru
  var latestVersionParams = new MessageCreateParams
  {
      Model = "claude-opus-4-8",
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
  func main() {
  	client := anthropic.NewClient()

  	// Membuat versi baru
  	skillFile := mustOpen("/path/to/updated_skill/SKILL.md")
  	defer skillFile.Close()

  	newVersion, err := client.Beta.Skills.Versions.New(
  		context.TODO(),
  		"skill_01AbCdEfGhIjKlMnOpQrStUv",
  		anthropic.BetaSkillVersionNewParams{
  			Files: []io.Reader{anthropic.File(skillFile, "updated_skill/SKILL.md", "text/markdown")},
  		},
  	)
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Menggunakan versi tertentu
  	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     "claude-opus-4-8",
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

  	// Menggunakan versi terbaru
  	latestResponse, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     "claude-opus-4-8",
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
  }

  func mustOpen(path string) *os.File {
  	f, err := os.Open(path)
  	if err != nil {
  		log.Fatal(err)
  	}
  	return f
  }
  ```

  ```java Java
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.beta.messages.BetaContainerParams;
  import com.anthropic.models.beta.messages.BetaSkillParams;
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  import com.anthropic.models.beta.skills.versions.VersionCreateParams;
  import com.anthropic.models.beta.skills.versions.VersionCreateResponse;
  // ...
  void main() throws Exception {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Membuat versi baru
      VersionCreateParams versionParams = VersionCreateParams.builder()
          .addFile(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("/path/to/updated_skill/SKILL.md")))
              .filename("updated_skill/SKILL.md")
              .contentType("text/markdown")
              .build())
          .build();

      VersionCreateResponse newVersion = client.beta().skills().versions()
          .create("skill_01AbCdEfGhIjKlMnOpQrStUv", versionParams);

      // Menggunakan versi spesifik
      MessageCreateParams specificVersionParams = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
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

      // Menggunakan versi terbaru
      MessageCreateParams latestVersionParams = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
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
  }
  ```

  ```php PHP
  use Anthropic\Core\FileParam;

  $client = new Client();

  // Membuat versi baru
  $newVersion = $client->beta->skills->versions->create(
      skillID: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
      files: [FileParam::fromResource(fopen('/path/to/updated_skill/SKILL.md', 'r'), 'updated_skill/SKILL.md', 'text/markdown')],
  );

  // Menggunakan versi tertentu
  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [['role' => 'user', 'content' => 'Use updated Skill']],
      model: 'claude-opus-4-8',
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

  // Menggunakan versi terbaru
  $latestResponse = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [['role' => 'user', 'content' => 'Use latest Skill version']],
      model: 'claude-opus-4-8',
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

  # Membuat versi baru
  new_version = client.beta.skills.versions.create(
    "skill_01AbCdEfGhIjKlMnOpQrStUv",
    files: [
      Anthropic::FilePart.new(
        Pathname("/path/to/updated_skill/SKILL.md"),
        filename: "updated_skill/SKILL.md",
        content_type: "text/markdown"
      )
    ]
  )

  # Menggunakan versi tertentu
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
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

  # Menggunakan versi terbaru
  latest_response = client.beta.messages.create(
    model: "claude-opus-4-8",
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

Lihat [referensi API Create Skill Version](/docs/id/api/beta/skills/versions/create) untuk detail lengkap.

***

## Bagaimana Skills dimuat

Ketika Anda menentukan Skills dalam container:

1. **Penemuan metadata:** Claude melihat metadata untuk setiap Skill (name, description) dalam prompt sistem.
2. **Pemuatan file:** File Skill disalin ke dalam container di `/skills/{directory}/`.
3. **Penggunaan otomatis:** Claude secara otomatis memuat dan menggunakan Skills saat relevan dengan request Anda.
4. **Komposisi:** Beberapa Skills dapat digabungkan untuk alur kerja yang kompleks.

Arsitektur "progressive disclosure" (pengungkapan bertahap) memastikan penggunaan konteks yang efisien: Claude hanya memuat instruksi Skill lengkap saat diperlukan.

***

## Kasus penggunaan

### Skills organisasi

**Merek & Komunikasi**

* Menerapkan pemformatan khusus perusahaan (warna, font, tata letak) ke dokumen
* Menghasilkan komunikasi yang mengikuti templat organisasi
* Memastikan pedoman merek yang konsisten di semua output

**Manajemen Proyek**

* Menyusun catatan dengan format khusus perusahaan (OKR, log keputusan)
* Menghasilkan tugas yang mengikuti konvensi tim
* Membuat rekap rapat dan pembaruan status yang terstandarisasi

**Operasi Bisnis**

* Membuat laporan, proposal, dan analisis standar perusahaan
* Menjalankan prosedur analitis khusus perusahaan
* Menghasilkan model keuangan yang mengikuti templat organisasi

### Skills pribadi

**Pembuatan Konten**

* Templat dokumen kustom
* Pemformatan dan penataan gaya khusus
* Pembuatan konten khusus domain

**Analisis Data**

* Pipeline pemrosesan data kustom
* Templat visualisasi khusus
* Metode analitis khusus industri

**Pengembangan & Otomatisasi**

* Templat pembuatan kode
* Kerangka kerja pengujian
* Alur kerja deployment

### Contoh: pemodelan keuangan

Gabungkan Skills Excel dan analisis DCF kustom:

<CodeGroup>
  ```bash cURL
  # Membuat Skill analisis DCF kustom
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
      \"model\": \"claude-opus-4-8\",
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
  # Membuat Skill analisis DCF kustom
  DCF_SKILL_ID=$(ant beta:skills create \
    --file dcf_skill.zip \
    --transform id --raw-output)

  # Gunakan dengan Excel untuk membuat model keuangan
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<YAML
  model: claude-opus-4-8
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

  # Membuat Skill analisis DCF kustom

  dcf_skill = client.beta.skills.create(
      files=files_from_dir("/path/to/dcf_skill"),
  )

  # Gunakan dengan Excel untuk membuat model keuangan
  response = client.beta.messages.create(
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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

  // Membuat Skill analisis DCF kustom
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
      Model = "claude-opus-4-8",
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
  	Model:     "claude-opus-4-8",
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

      // Gunakan bersama Skill Excel untuk membuat model keuangan
      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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

  # Membuat Skill analisis DCF kustom
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
    model: "claude-opus-4-8",
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

### Batasan request

* **Maksimum Skills per request:** 8

* **Maksimum ukuran unggahan Skill:** 30 MB (semua file digabungkan)

* **Persyaratan frontmatter YAML:**

  * `name`: Maksimum 64 karakter, hanya huruf kecil/angka/tanda hubung, tanpa tag XML, tanpa kata yang dicadangkan ("anthropic", "claude")
  * `description`: Maksimum 1024 karakter, tidak boleh kosong, tanpa tag XML

### Kendala lingkungan

Skills berjalan di container eksekusi kode dengan batasan berikut:

* **Tanpa akses jaringan:** Tidak dapat melakukan panggilan API eksternal
* **Tanpa instalasi paket saat runtime:** Hanya paket yang sudah terpasang sebelumnya yang tersedia
* **Lingkungan terisolasi:** Container terisolasi; container baru dibuat kecuali Anda menentukan ID container yang sudah ada

Lihat [Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk paket yang tersedia.

***

## Praktik terbaik

### Kapan menggunakan beberapa Skills

Gabungkan Skills ketika tugas melibatkan beberapa jenis dokumen atau domain:

**Kasus penggunaan yang baik:**

* Analisis data (Excel) + pembuatan presentasi (PowerPoint)
* Pembuatan laporan (Word) + ekspor ke PDF
* Logika domain kustom + pembuatan dokumen

**Hindari:**

* Menyertakan Skills yang tidak digunakan (memengaruhi kinerja)

### Strategi manajemen versi

**Untuk produksi:**

```python
# Sematkan ke versi tertentu untuk stabilitas
container = {
    "skills": [
        {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "1759178010641129",  # Specific version
        }
    ]
}
```

**Untuk pengembangan:**

```python
# Gunakan latest untuk pengembangan aktif
container = {
    "skills": [
        {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest",  # Always get newest
        }
    ]
}
```

### Pertimbangan caching prompt

Saat menggunakan caching prompt, perhatikan bahwa mengubah daftar Skills di container Anda akan merusak cache:

<CodeGroup>
  ```bash cURL
  # Permintaan pertama membuat cache
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
      },
      "messages": [{"role": "user", "content": "Analyze sales data"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'

  # Menambah/menghapus Skills merusak cache
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
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
  # Permintaan pertama membuat cache
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<'YAML'
  model: claude-opus-4-8
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

  # Menambah/menghapus Skills merusak cache
  ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 <<'YAML'
  model: claude-opus-4-8
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

  # Permintaan pertama membuat cache
  response1 = client.beta.messages.create(
      model="claude-opus-4-8",
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

  # Menambah/menghapus Skills merusak cache
  response2 = client.beta.messages.create(
      model="claude-opus-4-8",
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
              },  # Cache miss
          ]
      },
      messages=[{"role": "user", "content": "Create a presentation"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Permintaan pertama membuat cache
  const response1 = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [{ role: "user", content: "Analyze sales data" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Menambah/menghapus Skills merusak cache
  const response2 = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "anthropic", skill_id: "pptx", version: "latest" } // Cache miss
      ]
    },
    messages: [{ role: "user", content: "Create a presentation" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Permintaan pertama membuat cache
  var parameters1 = new MessageCreateParams
  {
      Model = "claude-opus-4-8",
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

  // Set Skill yang berbeda = cache miss
  var parameters2 = new MessageCreateParams
  {
      Model = "claude-opus-4-8",
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

  // Permintaan pertama membuat cache
  response1, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-4-8",
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

  // Menambah/menghapus Skills merusak cache
  response2, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-opus-4-8",
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

      // Permintaan pertama membuat cache
      MessageCreateParams params1 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
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

      // Menambah/menghapus Skills merusak cache
      MessageCreateParams params2 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
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

  // Permintaan pertama membuat cache
  $response1 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze sales data']
      ],
      model: 'claude-opus-4-8',
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

  // Menambah/menghapus Skills merusak cache
  $response2 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Create a presentation']
      ],
      model: 'claude-opus-4-8',
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

  # Permintaan pertama membuat cache
  response1 = client.beta.messages.create(
    model: "claude-opus-4-8",
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

  # Menambah/menghapus Skills merusak cache
  response2 = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    betas: [
      "code-execution-2025-08-25",
      "skills-2025-10-02",
    ],
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "anthropic", skill_id: "pptx", version: "latest" } # Cache miss
      ]
    },
    messages: [{ role: "user", content: "Create a presentation" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts response2
  ```
</CodeGroup>

Untuk kinerja caching terbaik, jaga agar daftar Skills Anda konsisten di seluruh request.

### Penanganan error

Tangani error terkait Skill dengan baik:

<CodeGroup>
  ```bash cURL
  # Alur penanganan error ini tidak cocok diterapkan sebagai perintah shell
  # sekali pakai; salah satu opsi SDK akan lebih sesuai. Permintaan yang gagal
  # mengembalikan HTTP 400 dengan JSON error yang .error.message-nya menyebutkan
  # masalah pada Skill.
  ```

  ```bash CLI
  if ! RESULT=$(ant beta:messages create \
    --beta code-execution-2025-08-25,skills-2025-10-02 \
    --transform-error error.message --format-error yaml 2>&1 <<'YAML'
  model: claude-opus-4-8
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
        # Menangani error khusus skill
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
          model="claude-opus-4-8",
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
          # Menangani error khusus skill
      else:
          raise
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  try {
    const response = await client.beta.messages.create({
      model: "claude-opus-4-8",
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
      // Menangani error khusus skill
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
          Model = "claude-opus-4-8",
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
  	Model:     "claude-opus-4-8",
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
              .model(Model.CLAUDE_OPUS_4_8)
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
          model: 'claude-opus-4-8',
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
      model: "claude-opus-4-8",
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

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Referensi API" icon="book" href="/docs/id/api/beta/skills/create">
    Referensi API lengkap dengan semua endpoint
  </Card>

  <Card title="Praktik terbaik penulisan Skill" icon="edit" href="/docs/id/agents-and-tools/agent-skills/best-practices">
    Pelajari cara menulis Skills yang efektif yang dapat ditemukan dan digunakan Claude dengan sukses
  </Card>

  <Card title="Alat eksekusi kode" icon="terminal" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan kode Python dan bash dalam container sandbox untuk menganalisis data, menghasilkan file, dan mengiterasi solusi
  </Card>
</CardGroup>
