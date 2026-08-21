---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/quickstart
fetched_at: 2026-08-21T02:32:13.524433Z
sha256: 083993654bae53acd5a7ef1131526c164fba85eb38c327285ab2b3b73e92aaef
---

---
title: Memulai dengan Agent Skills di API
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/quickstart
description: Pelajari cara menggunakan Agent Skills untuk membuat dokumen dengan Claude API dalam waktu kurang dari 10 menit.
---

Tutorial ini menunjukkan cara menggunakan Agent Skills untuk membuat presentasi PowerPoint. Anda akan mempelajari cara mengaktifkan Skills, membuat permintaan, dan mengakses file yang dihasilkan.

## Prasyarat

* [Kunci API Claude](https://platform.claude.com/settings/keys) atau [ant CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication) yang sudah login
* [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk bahasa Anda, atau `curl` dan `jq`
* Pemahaman dasar tentang cara membuat permintaan API

## Gambaran umum Agent Skills

Agent Skills bawaan memperluas kemampuan Claude dengan keahlian khusus untuk tugas-tugas seperti membuat dokumen, menganalisis data, dan memproses file. Anthropic menyediakan Agent Skills bawaan berikut di API:

* **PowerPoint (pptx):** Membuat dan mengedit presentasi
* **Excel (xlsx):** Membuat dan menganalisis spreadsheet
* **Word (docx):** Membuat dan mengedit dokumen
* **PDF (pdf):** Menghasilkan dokumen PDF

<Note>
  Untuk membuat Skills kustom, lihat [Agent Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) untuk contoh membangun Skills Anda sendiri dengan keahlian spesifik domain.
</Note>

## Langkah 1: Daftar Skills yang tersedia

Pertama, periksa Skills apa saja yang tersedia. Gunakan Skills API untuk mendaftar semua Skills yang dikelola Anthropic. Setiap tab bahasa adalah cuplikan dari satu skrip berkelanjutan, dengan semua import dan pengaturan klien di bagian atas:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # List Anthropic-managed Skills
  curl --fail-with-body -sS "https://api.anthropic.com/v1/skills?source=anthropic" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  # List Anthropic-managed Skills
  ant skills list --source anthropic
  ```

  ```python Python
  # List Anthropic-managed Skills
  skills = client.skills.list(source="anthropic")

  for skill in skills.data:
      print(f"{skill.id}: {skill.display_name}")
  ```

  ```typescript TypeScript
  // List Anthropic-managed Skills
  const skills = await client.skills.list({ source: "anthropic" });

  for (const skill of skills.data) {
    console.log(`${skill.id}: ${skill.display_name}`);
  }
  ```

  ```csharp C#
  // List Anthropic-managed Skills
  var skills = await client.Skills.List(new SkillListParams { Source = "anthropic" });

  foreach (var skill in skills.Items)
  {
      Console.WriteLine($"{skill.ID}: {skill.DisplayName}");
  }
  ```

  ```go Go
  // List Anthropic-managed Skills
  skills, err := client.Skills.List(ctx, anthropic.SkillListParams{
  	Source: anthropic.String("anthropic"),
  })
  if err != nil {
  	panic(err)
  }

  for _, skill := range skills.Data {
  	fmt.Printf("%s: %s\n", skill.ID, skill.DisplayName)
  }
  ```

  ```java Java
  // List Anthropic-managed Skills
  SkillListPage skills = client.skills().list(
      SkillListParams.builder().source("anthropic").build()
  );

  for (Skill skill : skills.data()) {
      IO.println(skill.id() + ": " + skill.displayName());
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Skills API under the beta namespace; field names can differ from other SDKs.
  // List Anthropic-managed Skills
  $skills = $client->beta->skills->list(source: 'anthropic');

  foreach ($skills->data as $skill) {
      echo "{$skill->id}: {$skill->displayTitle}\n";
  }
  ```

  ```ruby Ruby
  # List Anthropic-managed Skills
  skills = client.skills.list(source: "anthropic")

  skills.data.each do |skill|
    puts "#{skill.id}: #{skill.display_name}"
  end
  ```
</CodeGroup>

Anda akan melihat Skills berikut: `pptx`, `xlsx`, `docx`, dan `pdf`.

API ini mengembalikan metadata setiap Skill: nama dan deskripsinya. Claude memuat metadata ini saat startup untuk menentukan Skills mana yang tersedia. Ini adalah tingkat pertama dari **progressive disclosure** (pengungkapan bertahap), di mana Claude menemukan Skills tanpa memuat instruksi lengkapnya terlebih dahulu.

## Langkah 2: Buat presentasi

Gunakan Skill PowerPoint untuk membuat presentasi tentang energi terbarukan. Tentukan Skills menggunakan parameter `container` di Messages API:

<CodeGroup>
  ```bash cURL
  # Create a message with the PowerPoint Skill
  response=$(
    curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d @- <<'EOF'
  {
    "model": "claude-opus-5",
    "max_tokens": 16000,
    "container": {
      "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
    },
    "messages": [
      {"role": "user", "content": "Create a presentation about renewable energy with 5 slides"}
    ],
    "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
  }
  EOF
  )
  ```

  ```bash CLI
  # Create a message with the PowerPoint Skill
  response=$(ant messages create --format json <<'YAML'
  model: claude-opus-5
  max_tokens: 16000
  container:
    skills:
      - type: anthropic
        skill_id: pptx
        version: latest
  messages:
    - role: user
      content: Create a presentation about renewable energy with 5 slides
  tools:
    - type: code_execution_20260521
      name: code_execution
  YAML
  )
  ```

  ```python Python
  # Create a message with the PowerPoint Skill
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      container={
          "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Create a presentation about renewable energy with 5 slides",
          }
      ],
      tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
  )

  print(f"stop_reason={response.stop_reason}, blocks={len(response.content)}")
  ```

  ```typescript TypeScript
  // Create a message with the PowerPoint Skill
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    container: {
      skills: [{ type: "anthropic", skill_id: "pptx", version: "latest" }],
    },
    messages: [
      {
        role: "user",
        content: "Create a presentation about renewable energy with 5 slides",
      },
    ],
    tools: [{ type: "code_execution_20260521", name: "code_execution" }],
  });

  console.log(
    `stop_reason=${response.stop_reason}, blocks=${response.content.length}`,
  );
  ```

  ```csharp C#
  // Create a message with the PowerPoint Skill
  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 16000,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "pptx",
                  Version = "latest",
              },
          ],
      },
      Messages =
      [
          new MessageParam
          {
              Role = Role.User,
              Content = "Create a presentation about renewable energy with 5 slides",
          },
      ],
      Tools = [new CodeExecutionTool20260521()],
  });

  Console.WriteLine($"stop_reason={response.StopReason?.Raw()}, blocks={response.Content.Count}");
  ```

  ```go Go
  // Create a message with the PowerPoint Skill
  response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 16000,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "pptx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewTextBlock("Create a presentation about renewable energy with 5 slides"),
  		),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20260521: &anthropic.CodeExecutionTool20260521Param{}},
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("stop_reason=%s, blocks=%d\n", response.StopReason, len(response.Content))
  ```

  ```java Java
  // Create a message with the PowerPoint Skill
  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(16000)
          .container(
              ContainerParams.builder()
                  .addSkill(
                      SkillParams.builder()
                          .type(SkillParams.Type.ANTHROPIC)
                          .skillId("pptx")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Create a presentation about renewable energy with 5 slides")
          .addTool(CodeExecutionTool20260521.builder().build())
          .build()
  );

  IO.println(
      "stop_reason=" + response.stopReason().orElse(null)
          + ", blocks=" + response.content().size()
  );
  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  // Create a message with the PowerPoint Skill
  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [['type' => 'anthropic', 'skill_id' => 'pptx', 'version' => 'latest']],
      ],
      messages: [
          [
              'role' => 'user',
              'content' => 'Create a presentation about renewable energy with 5 slides',
          ],
      ],
      tools: [['type' => 'code_execution_20260521', 'name' => 'code_execution']],
  );

  printf("stop_reason=%s, blocks=%d\n", $response->stopReason, count($response->content));
  ```

  ```ruby Ruby
  # Create a message with the PowerPoint Skill
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 16_000,
    container: {
      skills: [{type: "anthropic", skill_id: "pptx", version: "latest"}]
    },
    messages: [
      {
        role: "user",
        content: "Create a presentation about renewable energy with 5 slides"
      }
    ],
    tools: [{type: "code_execution_20260521", name: "code_execution"}]
  )

  puts "stop_reason=#{response.stop_reason}, blocks=#{response.content.length}"
  ```
</CodeGroup>

Permintaan ini mencakup bagian-bagian berikut:

* **`model`:** [Model yang mendukung alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility)
* **`container.skills`:** Menentukan Skills mana yang dapat digunakan Claude
* **`type: "anthropic"`:** Menunjukkan bahwa ini adalah Skill yang dikelola Anthropic
* **`skill_id: "pptx"`:** Pengidentifikasi Skill PowerPoint
* **`version: "latest"`:** Versi Skill yang diatur ke versi yang paling baru dipublikasikan
* **`tools`:** Mengaktifkan eksekusi kode (diperlukan untuk Skills)
* **Header beta:** `skills-2025-10-02`

<Note>
  Contoh-contoh di halaman ini menggunakan versi alat `code_execution_20260521`, yang tersedia secara umum dan hanya memerlukan header beta `skills-2025-10-02`. Kode pada Langkah 3 mem-parsing tipe hasil yang dikembalikan oleh versi alat saat ini. Skills juga bekerja dengan versi [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) yang lebih lama seperti `code_execution_20250825`: versi alat eksekusi kode apa pun yang berlaku saat ini memenuhi persyaratan Skills. Jika Anda menggunakan versi yang berbeda, pastikan `type` alat dan header beta apa pun tetap konsisten dengan halaman alat eksekusi kode, dan selalu sertakan `skills-2025-10-02`.
</Note>

Ketika Anda membuat permintaan ini, Claude secara otomatis mencocokkan tugas Anda dengan Skill yang relevan. Karena Anda meminta presentasi, Claude menentukan bahwa Skill PowerPoint relevan dan memuat instruksi lengkapnya: tingkat kedua dari progressive disclosure. Kemudian Claude menjalankan kode Skill tersebut untuk membuat presentasi Anda.

## Langkah 3: Unduh file yang dibuat

Presentasi dibuat di dalam container eksekusi kode dan disimpan sebagai file. `response` dari Langkah 2 menyertakan referensi file dengan ID file. Ekstrak ID file dan unduh file tersebut dengan Files API. Contoh ini menyimpannya ke direktori temp sistem Anda:

<CodeGroup>
  ```bash cURL
  # Extract the file ID. The code execution tool runs the Skill's code through
  # its Bash sub-tool, and generated files appear as bash_code_execution_output
  # items inside the bash_code_execution_tool_result block.
  file_id=$(jq -r '
    last(
      .content[]
      | select(.type == "bash_code_execution_tool_result")
      | .content
      | select(.type == "bash_code_execution_result")
      | .content[].file_id
    ) // empty
  ' <<<"$response")

  if [[ -n "$file_id" ]]; then
    # Download the file and save it
    output_path="${TMPDIR:-/tmp}/renewable_energy.pptx"
    curl --fail-with-body -sS "https://api.anthropic.com/v1/files/$file_id/content" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -o "$output_path"
    echo "Presentation saved to $output_path"
  fi
  ```

  ```bash CLI
  # Extract the file ID. The code execution tool runs the Skill's code through
  # its Bash sub-tool, and generated files appear as bash_code_execution_output
  # items inside the bash_code_execution_tool_result block.
  file_id=$(jq -r '
    last(
      .content[]
      | select(.type == "bash_code_execution_tool_result")
      | .content
      | select(.type == "bash_code_execution_result")
      | .content[].file_id
    ) // empty
  ' <<<"$response")

  if [[ -n "$file_id" ]]; then
    # Download the file and save it
    output_path="${TMPDIR:-/tmp}/renewable_energy.pptx"
    ant files download --file-id "$file_id" --output "$output_path"
    echo "Presentation saved to $output_path"
  fi
  ```

  ```python Python
  # Extract the file ID. The code execution tool runs the Skill's code through
  # its Bash sub-tool, and generated files appear as bash_code_execution_output
  # items inside the bash_code_execution_tool_result block.
  file_id = None
  for block in response.content:
      if block.type == "bash_code_execution_tool_result":
          if block.content.type == "bash_code_execution_result":
              for output in block.content.content:
                  file_id = output.file_id

  if file_id:
      # Download the file and save it
      output_path = Path(tempfile.gettempdir()) / "renewable_energy.pptx"
      file_content = client.files.download(file_id=file_id)
      file_content.write_to_file(output_path)
      print(f"Presentation saved to {output_path}")
  ```

  ```typescript TypeScript
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  let fileId: string | undefined;
  for (const block of response.content) {
    if (
      block.type === "bash_code_execution_tool_result" &&
      block.content.type === "bash_code_execution_result"
    ) {
      for (const output of block.content.content) {
        fileId = output.file_id;
      }
    }
  }

  if (fileId) {
    // Download the file and save it
    const outputPath = path.join(os.tmpdir(), "renewable_energy.pptx");
    const fileContent = await client.files.download(fileId);
    await fs.writeFile(outputPath, Buffer.from(await fileContent.arrayBuffer()));
    console.log(`Presentation saved to ${outputPath}`);
  }
  ```

  ```csharp C#
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  string? fileId = null;
  foreach (var block in response.Content)
  {
      if (block.TryPickBashCodeExecutionToolResult(out var bashResult)
          && bashResult.Content.TryPickBashCodeExecutionResultBlock(out var bashResultBlock))
      {
          foreach (var output in bashResultBlock.Content)
          {
              fileId = output.FileID;
          }
      }
  }

  if (fileId is not null)
  {
      // Download the file and save it
      var outputPath = Path.Combine(Path.GetTempPath(), "renewable_energy.pptx");
      using var download = await client.Files.Download(fileId);
      await using var source = await download.ReadAsStream();
      await using var destination = File.Create(outputPath);
      await source.CopyToAsync(destination);
      Console.WriteLine($"Presentation saved to {outputPath}");
  }
  ```

  ```go Go
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  var fileID string
  for _, block := range response.Content {
  	switch result := block.AsAny().(type) {
  	case anthropic.BashCodeExecutionToolResultBlock:
  		if result.Content.Type == "bash_code_execution_result" {
  			for _, output := range result.Content.Content {
  				fileID = output.FileID
  			}
  		}
  	}
  }

  if fileID != "" {
  	// Download the file and save it
  	outputPath := filepath.Join(os.TempDir(), "renewable_energy.pptx")
  	fileContent, err := client.Files.Download(ctx, fileID)
  	if err != nil {
  		panic(err)
  	}
  	defer fileContent.Body.Close()
  	outFile, err := os.Create(outputPath)
  	if err != nil {
  		panic(err)
  	}
  	defer outFile.Close()
  	if _, err := io.Copy(outFile, fileContent.Body); err != nil {
  		panic(err)
  	}
  	fmt.Printf("Presentation saved to %s\n", outputPath)
  }
  ```

  ```java Java
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  String fileId = null;
  for (ContentBlock block : response.content()) {
      if (block.isBashCodeExecutionToolResult()) {
          var content = block.asBashCodeExecutionToolResult().content();
          if (content.isBashCodeExecutionResultBlock()) {
              for (var output : content.asBashCodeExecutionResultBlock().content()) {
                  fileId = output.fileId();
              }
          }
      }
  }

  if (fileId != null) {
      // Download the file and save it
      Path outputPath = Files.createTempFile("renewable_energy", ".pptx");
      try (HttpResponse fileContent = client.files().download(fileId)) {
          Files.copy(fileContent.body(), outputPath, StandardCopyOption.REPLACE_EXISTING);
      }
      IO.println("Presentation saved to " + outputPath);
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  $fileId = null;
  foreach ($response->content as $block) {
      if ($block->type !== 'bash_code_execution_tool_result') {
          continue;
      }
      $resultBlock = $block->content;
      if ($resultBlock->type !== 'bash_code_execution_result') {
          continue;
      }
      foreach ($resultBlock->content as $output) {
          $fileId = $output->fileID;
      }
  }

  if ($fileId !== null) {
      // Download the file and save it
      $outputPath = sys_get_temp_dir() . '/renewable_energy.pptx';
      $fileContent = $client->beta->files->download($fileId);
      file_put_contents($outputPath, $fileContent);
      echo "Presentation saved to {$outputPath}\n";
  }
  ```

  ```ruby Ruby
  # Extract the file ID. The code execution tool runs the Skill's code through
  # its Bash sub-tool, and generated files appear as bash_code_execution_output
  # items inside the bash_code_execution_tool_result block.
  file_id = nil
  response.content.each do |block|
    next unless block.type == :bash_code_execution_tool_result

    if block.content[:type].to_s == "bash_code_execution_result"
      Array(block.content[:content]).each { |output| file_id = output[:file_id] }
    end
  end

  if file_id
    # Download the file and save it
    output_path = File.join(Dir.tmpdir, "renewable_energy.pptx")
    file_content = client.files.download(file_id)
    File.binwrite(output_path, file_content.read)
    puts "Presentation saved to #{output_path}"
  end
  ```
</CodeGroup>

<Note>
  Untuk detail lengkap tentang bekerja dengan file yang dihasilkan, lihat [Mengambil file yang dihasilkan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#retrieve-generated-files) di dokumentasi alat eksekusi kode.
</Note>

## Coba contoh lainnya

Coba variasi berikut:

### Buat spreadsheet

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 16000,
      "container": {
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      "messages": [
        {"role": "user", "content": "Create a quarterly sales tracking spreadsheet with sample data"}
      ],
      "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
    }' | jq -r '"stop_reason=\(.stop_reason)"'
  ```

  ```bash CLI
  ant beta:messages create --format json \
    --beta skills-2025-10-02 <<'YAML' | jq -r '"stop_reason=\(.stop_reason)"'
  model: claude-opus-5
  max_tokens: 16000
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
  messages:
    - role: user
      content: Create a quarterly sales tracking spreadsheet with sample data
  tools:
    - type: code_execution_20260521
      name: code_execution
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      betas=["skills-2025-10-02"],
      container={
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Create a quarterly sales tracking spreadsheet with sample data",
          }
      ],
      tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    betas: ["skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Create a quarterly sales tracking spreadsheet with sample data"
      }
    ],
    tools: [{ type: "code_execution_20260521", name: "code_execution" }]
  });
  ```

  ```csharp C#
  var response = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 16000,
          Betas = ["skills-2025-10-02"],
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
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = "Create a quarterly sales tracking spreadsheet with sample data",
              },
          ],
          Tools = [new BetaCodeExecutionTool20260521()],
      }
  );
  ```

  ```go Go
  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 16000,
  	Betas: []anthropic.AnthropicBeta{
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
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a quarterly sales tracking spreadsheet with sample data")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{
  			OfCodeExecutionTool20260521: &anthropic.BetaCodeExecutionTool20260521Param{},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  BetaMessage response = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(CLAUDE_OPUS_5)
          .maxTokens(16000)
          .addBeta(AnthropicBeta.SKILLS_2025_10_02)
          .container(
              BetaContainerParams.builder()
                  .addSkill(
                      BetaSkillParams.builder()
                          .type(ANTHROPIC)
                          .skillId("xlsx")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Create a quarterly sales tracking spreadsheet with sample data")
          .addTool(BetaCodeExecutionTool20260521.builder().build())
          .build()
  );

  ```

  ```php PHP
  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest'],
          ],
      ],
      messages: [
          [
              'role' => 'user',
              'content' => 'Create a quarterly sales tracking spreadsheet with sample data',
          ],
      ],
      tools: [new BetaCodeExecutionTool20260521()],
  );
  ```

  ```ruby Ruby
  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 16_000,
    betas: ["skills-2025-10-02"],
    container: {
      skills: [{type: "anthropic", skill_id: "xlsx", version: "latest"}]
    },
    messages: [
      {
        role: "user",
        content: "Create a quarterly sales tracking spreadsheet with sample data"
      }
    ],
    tools: [{type: "code_execution_20260521", name: "code_execution"}]
  )
  ```
</CodeGroup>

### Buat dokumen Word

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 16000,
      "container": {
        "skills": [{"type": "anthropic", "skill_id": "docx", "version": "latest"}]
      },
      "messages": [
        {"role": "user", "content": "Write a 2-page report on the benefits of renewable energy"}
      ],
      "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
    }' | jq -r '"stop_reason=\(.stop_reason)"'
  ```

  ```bash CLI
  ant beta:messages create --format json \
    --beta skills-2025-10-02 <<'YAML' | jq -r '"stop_reason=\(.stop_reason)"'
  model: claude-opus-5
  max_tokens: 16000
  container:
    skills:
      - type: anthropic
        skill_id: docx
        version: latest
  messages:
    - role: user
      content: Write a 2-page report on the benefits of renewable energy
  tools:
    - type: code_execution_20260521
      name: code_execution
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      betas=["skills-2025-10-02"],
      container={
          "skills": [{"type": "anthropic", "skill_id": "docx", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Write a 2-page report on the benefits of renewable energy",
          }
      ],
      tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    betas: ["skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "docx", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Write a 2-page report on the benefits of renewable energy"
      }
    ],
    tools: [{ type: "code_execution_20260521", name: "code_execution" }]
  });
  ```

  ```csharp C#
  var response = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 16000,
          Betas = ["skills-2025-10-02"],
          Container = new BetaContainerParams
          {
              Skills =
              [
                  new BetaSkillParams
                  {
                      Type = BetaSkillParamsType.Anthropic,
                      SkillID = "docx",
                      Version = "latest",
                  },
              ],
          },
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = "Write a 2-page report on the benefits of renewable energy",
              },
          ],
          Tools = [new BetaCodeExecutionTool20260521()],
      }
  );
  ```

  ```go Go
  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 16000,
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "docx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Write a 2-page report on the benefits of renewable energy")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{
  			OfCodeExecutionTool20260521: &anthropic.BetaCodeExecutionTool20260521Param{},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  BetaMessage response = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(CLAUDE_OPUS_5)
          .maxTokens(16000)
          .addBeta(AnthropicBeta.SKILLS_2025_10_02)
          .container(
              BetaContainerParams.builder()
                  .addSkill(
                      BetaSkillParams.builder()
                          .type(ANTHROPIC)
                          .skillId("docx")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Write a 2-page report on the benefits of renewable energy")
          .addTool(BetaCodeExecutionTool20260521.builder().build())
          .build()
  );

  ```

  ```php PHP
  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'docx', 'version' => 'latest'],
          ],
      ],
      messages: [
          [
              'role' => 'user',
              'content' => 'Write a 2-page report on the benefits of renewable energy',
          ],
      ],
      tools: [new BetaCodeExecutionTool20260521()],
  );
  ```

  ```ruby Ruby
  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 16_000,
    betas: ["skills-2025-10-02"],
    container: {
      skills: [{type: "anthropic", skill_id: "docx", version: "latest"}]
    },
    messages: [
      {
        role: "user",
        content: "Write a 2-page report on the benefits of renewable energy"
      }
    ],
    tools: [{type: "code_execution_20260521", name: "code_execution"}]
  )
  ```
</CodeGroup>

### Hasilkan PDF

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 16000,
      "container": {
        "skills": [{"type": "anthropic", "skill_id": "pdf", "version": "latest"}]
      },
      "messages": [
        {"role": "user", "content": "Generate a PDF invoice template"}
      ],
      "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
    }' | jq -r '"stop_reason=\(.stop_reason)"'
  ```

  ```bash CLI
  ant beta:messages create --format json \
    --beta skills-2025-10-02 <<'YAML' | jq -r '"stop_reason=\(.stop_reason)"'
  model: claude-opus-5
  max_tokens: 16000
  container:
    skills:
      - type: anthropic
        skill_id: pdf
        version: latest
  messages:
    - role: user
      content: Generate a PDF invoice template
  tools:
    - type: code_execution_20260521
      name: code_execution
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      betas=["skills-2025-10-02"],
      container={
          "skills": [{"type": "anthropic", "skill_id": "pdf", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Generate a PDF invoice template",
          }
      ],
      tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    betas: ["skills-2025-10-02"],
    container: {
      skills: [{ type: "anthropic", skill_id: "pdf", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Generate a PDF invoice template"
      }
    ],
    tools: [{ type: "code_execution_20260521", name: "code_execution" }]
  });
  ```

  ```csharp C#
  var response = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 16000,
          Betas = ["skills-2025-10-02"],
          Container = new BetaContainerParams
          {
              Skills =
              [
                  new BetaSkillParams
                  {
                      Type = BetaSkillParamsType.Anthropic,
                      SkillID = "pdf",
                      Version = "latest",
                  },
              ],
          },
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = "Generate a PDF invoice template",
              },
          ],
          Tools = [new BetaCodeExecutionTool20260521()],
      }
  );
  ```

  ```go Go
  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 16000,
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "pdf",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Generate a PDF invoice template")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{
  			OfCodeExecutionTool20260521: &anthropic.BetaCodeExecutionTool20260521Param{},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  BetaMessage response = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(CLAUDE_OPUS_5)
          .maxTokens(16000)
          .addBeta(AnthropicBeta.SKILLS_2025_10_02)
          .container(
              BetaContainerParams.builder()
                  .addSkill(
                      BetaSkillParams.builder()
                          .type(ANTHROPIC)
                          .skillId("pdf")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Generate a PDF invoice template")
          .addTool(BetaCodeExecutionTool20260521.builder().build())
          .build()
  );

  ```

  ```php PHP
  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'pdf', 'version' => 'latest'],
          ],
      ],
      messages: [
          [
              'role' => 'user',
              'content' => 'Generate a PDF invoice template',
          ],
      ],
      tools: [new BetaCodeExecutionTool20260521()],
  );
  ```

  ```ruby Ruby
  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 16_000,
    betas: ["skills-2025-10-02"],
    container: {
      skills: [{type: "anthropic", skill_id: "pdf", version: "latest"}]
    },
    messages: [
      {
        role: "user",
        content: "Generate a PDF invoice template"
      }
    ],
    tools: [{type: "code_execution_20260521", name: "code_execution"}]
  )
  ```
</CodeGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Praktik terbaik penulisan Skill" icon="edit" href="https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices">
    Pelajari cara menulis Skills yang efektif yang dapat ditemukan dan digunakan Claude dengan sukses.
  </Card>

  <Card title="Menggunakan Agent Skills dengan API" icon="book" href="https://platform.claude.com/docs/id/build-with-claude/skills-guide">
    Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.
  </Card>

  <Card title="Buat Skills kustom" icon="code" href="https://platform.claude.com/docs/id/api/skills/create-skill">
    Unggah Skills Anda sendiri untuk tugas-tugas khusus.
  </Card>

  <Card title="Gunakan Skills di Claude Code" icon="terminal" href="https://code.claude.com/docs/id/skills">
    Pelajari tentang Skills di Claude Code.
  </Card>

  <Card title="Agent Skills Cookbook" icon="book" href="https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction">
    Jelajahi contoh Skills dan pola implementasi.
  </Card>
</CardGroup>
