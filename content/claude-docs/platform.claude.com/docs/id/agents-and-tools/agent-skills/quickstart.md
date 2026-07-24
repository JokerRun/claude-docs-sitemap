---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/quickstart
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 88c07dd0a98515ee1a72b0a7154ea442dba66d67b976ea956a7e6d0fa202c294
---

# Memulai dengan Agent Skills di API

Pelajari cara menggunakan Agent Skills untuk membuat dokumen dengan Claude API dalam waktu kurang dari 10 menit.

---

Tutorial ini menunjukkan cara menggunakan Agent Skills untuk membuat presentasi PowerPoint. Anda akan mempelajari cara mengaktifkan Skills, membuat permintaan, dan mengakses file yang dihasilkan.

## Prasyarat

* [Kunci API Claude](/settings/keys) atau [ant CLI](/docs/id/cli-sdks-libraries/cli/authentication) yang sudah login
* [SDK klien](/docs/id/cli-sdks-libraries/overview) untuk bahasa Anda, atau `curl` dan `jq`
* Pemahaman dasar tentang cara membuat permintaan API

## Ikhtisar Agent Skills

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
  # Daftar Skills yang dikelola Anthropic
  curl --fail-with-body -sS "https://api.anthropic.com/v1/skills?source=anthropic" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" |
    jq -r '.data[] | "\(.id): \(.display_title)"'
  ```

  ```bash CLI
  # Menampilkan daftar Skill yang dikelola Anthropic
  ant beta:skills list --source anthropic
  ```

  ```python Python
  # Daftar Skills yang dikelola Anthropic
  skills = client.beta.skills.list(source="anthropic")

  for skill in skills.data:
      print(f"{skill.id}: {skill.display_title}")
  ```

  ```typescript TypeScript
  // Daftar Skills yang dikelola Anthropic
  const skills = await client.beta.skills.list({ source: "anthropic" });

  for (const skill of skills.data) {
    console.log(`${skill.id}: ${skill.display_title}`);
  }
  ```

  ```csharp C#
  // Daftar Skill yang dikelola Anthropic
  var skills = await client.Beta.Skills.List(new SkillListParams { Source = "anthropic" });

  foreach (var skill in skills.Items)
  {
      Console.WriteLine($"{skill.ID}: {skill.DisplayTitle}");
  }
  ```

  ```go Go
  // Daftar Skill yang dikelola Anthropic
  skills, err := client.Beta.Skills.List(ctx, anthropic.BetaSkillListParams{
  	Source: anthropic.String("anthropic"),
  })
  if err != nil {
  	panic(err)
  }

  for _, skill := range skills.Data {
  	fmt.Printf("%s: %s\n", skill.ID, skill.DisplayTitle)
  }
  ```

  ```java Java
  // Daftar Skills yang dikelola Anthropic
  SkillListPage skills = client.beta().skills().list(
      SkillListParams.builder().source("anthropic").build()
  );

  for (SkillListResponse skill : skills.data()) {
      IO.println(skill.id() + ": " + skill.displayTitle().orElse(""));
  }
  ```

  ```php PHP
  // Daftar Skills yang dikelola Anthropic
  $skills = $client->beta->skills->list(source: 'anthropic');

  foreach ($skills->data as $skill) {
      echo "{$skill->id}: {$skill->displayTitle}\n";
  }
  ```

  ```ruby Ruby
  # Daftar Skills yang dikelola Anthropic
  skills = client.beta.skills.list(source: "anthropic")

  skills.data.each do |skill|
    puts "#{skill.id}: #{skill.display_title}"
  end
  ```
</CodeGroup>

Anda akan melihat Skills berikut: `pptx`, `xlsx`, `docx`, dan `pdf`.

API ini mengembalikan metadata setiap Skill: nama dan deskripsinya. Claude memuat metadata ini saat startup untuk menentukan Skills mana yang tersedia. Ini adalah tingkat pertama dari **progressive disclosure** (pengungkapan bertahap), di mana Claude menemukan Skills tanpa memuat instruksi lengkapnya terlebih dahulu.

## Langkah 2: Buat presentasi

Gunakan Skill PowerPoint untuk membuat presentasi tentang energi terbarukan. Tentukan Skills menggunakan parameter `container` di Messages API:

<CodeGroup>
  ```bash cURL
  # Buat pesan dengan Skill PowerPoint
  response=$(
    curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: skills-2025-10-02" \
      -d @- <<'EOF'
  {
    "model": "claude-opus-4-8",
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
  jq -r '"stop_reason=\(.stop_reason), blocks=\(.content | length)"' <<<"$response"
  ```

  ```bash CLI
  # Membuat pesan dengan Skill PowerPoint
  response=$(ant beta:messages create --format json \
    --beta skills-2025-10-02 <<'YAML'
  model: claude-opus-4-8
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

  jq -r '"stop_reason=\(.stop_reason), blocks=\(.content | length)"' <<<"$response"
  ```

  ```python Python
  # Buat pesan dengan Skill PowerPoint
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      betas=["skills-2025-10-02"],
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
  // Buat pesan dengan Skill PowerPoint
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    betas: ["skills-2025-10-02"],
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
  // Buat pesan dengan Skill PowerPoint
  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Betas = ["skills-2025-10-02"],
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
      Messages =
      [
          new BetaMessageParam
          {
              Role = Role.User,
              Content = "Create a presentation about renewable energy with 5 slides",
          },
      ],
      Tools = [new BetaCodeExecutionTool20260521()],
  });

  Console.WriteLine($"stop_reason={response.StopReason?.Raw()}, blocks={response.Content.Count}");
  ```

  ```go Go
  // Buat pesan dengan Skill PowerPoint
  response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Betas: []anthropic.AnthropicBeta{
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
  		anthropic.NewBetaUserMessage(
  			anthropic.NewBetaTextBlock("Create a presentation about renewable energy with 5 slides"),
  		),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20260521: &anthropic.BetaCodeExecutionTool20260521Param{}},
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("stop_reason=%s, blocks=%d\n", response.StopReason, len(response.Content))
  ```

  ```java Java
  // Buat pesan dengan Skill PowerPoint
  BetaMessage response = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(16000)
          .addBeta(AnthropicBeta.SKILLS_2025_10_02)
          .container(
              BetaContainerParams.builder()
                  .addSkill(
                      BetaSkillParams.builder()
                          .type(BetaSkillParams.Type.ANTHROPIC)
                          .skillId("pptx")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Create a presentation about renewable energy with 5 slides")
          .addTool(BetaCodeExecutionTool20260521.builder().build())
          .build()
  );

  IO.println(
      "stop_reason=" + response.stopReason().orElse(null)
          + ", blocks=" + response.content().size()
  );
  ```

  ```php PHP
  // Buat pesan dengan Skill PowerPoint
  $response = $client->beta->messages->create(
      model: 'claude-opus-4-8',
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
  # Buat pesan dengan Skill PowerPoint
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16_000,
    betas: ["skills-2025-10-02"],
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

* **`model`:** [Model yang mendukung alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility)
* **`container.skills`:** Menentukan Skills mana yang dapat digunakan Claude
* **`type: "anthropic"`:** Menunjukkan bahwa ini adalah Skill yang dikelola Anthropic
* **`skill_id: "pptx"`:** Pengidentifikasi Skill PowerPoint
* **`version: "latest"`:** Versi Skill yang diatur ke versi yang paling baru dipublikasikan
* **`tools`:** Mengaktifkan eksekusi kode (diperlukan untuk Skills)
* **Header beta:** `skills-2025-10-02`

<Note>
  Contoh-contoh di halaman ini menggunakan versi alat `code_execution_20260521`, yang tersedia secara umum dan hanya memerlukan header beta `skills-2025-10-02`. Kode pada Langkah 3 mem-parsing tipe hasil yang dikembalikan oleh versi alat saat ini. Skills juga bekerja dengan versi [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) yang lebih lama seperti `code_execution_20250825`: versi alat eksekusi kode apa pun yang berlaku saat ini memenuhi persyaratan Skills. Jika Anda menggunakan versi yang berbeda, pastikan `type` alat dan header beta apa pun tetap konsisten dengan halaman alat eksekusi kode, dan selalu sertakan `skills-2025-10-02`.
</Note>

Ketika Anda membuat permintaan ini, Claude secara otomatis mencocokkan tugas Anda dengan Skill yang relevan. Karena Anda meminta presentasi, Claude menentukan bahwa Skill PowerPoint relevan dan memuat instruksi lengkapnya: tingkat kedua dari progressive disclosure. Kemudian Claude menjalankan kode Skill tersebut untuk membuat presentasi Anda.

## Langkah 3: Unduh file yang dibuat

Presentasi dibuat di dalam container eksekusi kode dan disimpan sebagai file. `response` dari Langkah 2 menyertakan referensi file dengan ID file. Ekstrak ID file dan unduh file tersebut dengan Files API. Contoh ini menyimpannya ke direktori temp sistem Anda:

<CodeGroup>
  ```bash cURL
  # Ekstrak ID file. Alat eksekusi kode menjalankan kode Skill melalui
  # sub-alat Bash-nya, dan file yang dihasilkan muncul sebagai item bash_code_execution_output
  # di dalam blok bash_code_execution_tool_result.
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
    # Unduh file dan simpan
    output_path="${TMPDIR:-/tmp}/renewable_energy.pptx"
    curl --fail-with-body -sS "https://api.anthropic.com/v1/files/$file_id/content" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: files-api-2025-04-14" \
      -o "$output_path"
    echo "Presentation saved to $output_path"
  fi
  ```

  ```bash CLI
  # Ekstrak ID file. Alat eksekusi kode menjalankan kode Skill melalui
  # sub-alat Bash-nya, dan file yang dihasilkan muncul sebagai item bash_code_execution_output
  # di dalam blok bash_code_execution_tool_result.
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
    # Unduh file dan simpan
    output_path="${TMPDIR:-/tmp}/renewable_energy.pptx"
    ant beta:files download --file-id "$file_id" --output "$output_path"
    echo "Presentation saved to $output_path"
  fi
  ```

  ```python Python
  # Ekstrak ID file. Alat eksekusi kode menjalankan kode Skill melalui
  # sub-alat Bash-nya, dan file yang dihasilkan muncul sebagai item bash_code_execution_output
  # di dalam blok bash_code_execution_tool_result.
  file_id = None
  for block in response.content:
      if block.type == "bash_code_execution_tool_result":
          if block.content.type == "bash_code_execution_result":
              for output in block.content.content:
                  file_id = output.file_id

  if file_id:
      # Unduh file dan simpan
      output_path = Path(tempfile.gettempdir()) / "renewable_energy.pptx"
      file_content = client.beta.files.download(file_id=file_id)
      file_content.write_to_file(output_path)
      print(f"Presentation saved to {output_path}")
  ```

  ```typescript TypeScript
  // Ekstrak ID file. Alat eksekusi kode menjalankan kode Skill melalui
  // sub-alat Bash-nya, dan file yang dihasilkan muncul sebagai item bash_code_execution_output
  // di dalam blok bash_code_execution_tool_result.
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
    // Unduh file dan simpan
    const outputPath = path.join(os.tmpdir(), "renewable_energy.pptx");
    const fileContent = await client.beta.files.download(fileId);
    await fs.writeFile(outputPath, Buffer.from(await fileContent.arrayBuffer()));
    console.log(`Presentation saved to ${outputPath}`);
  }
  ```

  ```csharp C#
  // Ekstrak ID file. Alat eksekusi kode menjalankan kode Skill melalui
  // sub-alat Bash-nya, dan file yang dihasilkan muncul sebagai item
  // bash_code_execution_output di dalam blok bash_code_execution_tool_result.
  string? fileId = null;
  foreach (var block in response.Content)
  {
      if (block.TryPickBashCodeExecutionToolResult(out var bashResult)
          && bashResult.Content.TryPickBetaBashCodeExecutionResultBlock(out var bashResultBlock))
      {
          foreach (var output in bashResultBlock.Content)
          {
              fileId = output.FileID;
          }
      }
  }

  if (fileId is not null)
  {
      // Unduh file dan simpan
      var outputPath = Path.Combine(Path.GetTempPath(), "renewable_energy.pptx");
      using var download = await client.Beta.Files.Download(fileId);
      await using var source = await download.ReadAsStream();
      await using var destination = File.Create(outputPath);
      await source.CopyToAsync(destination);
      Console.WriteLine($"Presentation saved to {outputPath}");
  }
  ```

  ```go Go
  // Ekstrak ID file. Alat eksekusi kode menjalankan kode Skill melalui
  // sub-alat Bash-nya, dan file yang dihasilkan muncul sebagai item bash_code_execution_output
  // di dalam blok bash_code_execution_tool_result.
  var fileID string
  for _, block := range response.Content {
  	switch result := block.AsAny().(type) {
  	case anthropic.BetaBashCodeExecutionToolResultBlock:
  		if result.Content.Type == "bash_code_execution_result" {
  			for _, output := range result.Content.Content {
  				fileID = output.FileID
  			}
  		}
  	}
  }

  if fileID != "" {
  	// Unduh file dan simpan
  	outputPath := filepath.Join(os.TempDir(), "renewable_energy.pptx")
  	fileContent, err := client.Beta.Files.Download(ctx, fileID, anthropic.BetaFileDownloadParams{})
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
  // Ekstrak ID file. Alat eksekusi kode menjalankan kode Skill melalui
  // sub-alat Bash-nya, dan file yang dihasilkan muncul sebagai item bash_code_execution_output
  // di dalam blok bash_code_execution_tool_result.
  String fileId = null;
  for (BetaContentBlock block : response.content()) {
      if (block.isBashCodeExecutionToolResult()) {
          var content = block.asBashCodeExecutionToolResult().content();
          if (content.isBetaBashCodeExecutionResultBlock()) {
              for (var output : content.asBetaBashCodeExecutionResultBlock().content()) {
                  fileId = output.fileId();
              }
          }
      }
  }

  if (fileId != null) {
      // Unduh file dan simpan
      Path outputPath = Files.createTempFile("renewable_energy", ".pptx");
      try (HttpResponse fileContent = client.beta().files().download(fileId)) {
          Files.copy(fileContent.body(), outputPath, StandardCopyOption.REPLACE_EXISTING);
      }
      IO.println("Presentation saved to " + outputPath);
  }
  ```

  ```php PHP
  // Ekstrak ID file. Alat eksekusi kode menjalankan kode Skill melalui
  // sub-alat Bash-nya, dan file yang dihasilkan muncul sebagai item bash_code_execution_output
  // di dalam blok bash_code_execution_tool_result.
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
      // Unduh file dan simpan
      $outputPath = sys_get_temp_dir() . '/renewable_energy.pptx';
      $fileContent = $client->beta->files->download($fileId);
      file_put_contents($outputPath, $fileContent);
      echo "Presentation saved to {$outputPath}\n";
  }
  ```

  ```ruby Ruby
  # Ekstrak ID file. Alat eksekusi kode menjalankan kode Skill melalui
  # sub-alat Bash-nya, dan file yang dihasilkan muncul sebagai item
  # bash_code_execution_output di dalam blok bash_code_execution_tool_result.
  file_id = nil
  response.content.each do |block|
    next unless block.type == :bash_code_execution_tool_result

    if block.content[:type].to_s == "bash_code_execution_result"
      Array(block.content[:content]).each { |output| file_id = output[:file_id] }
    end
  end

  if file_id
    # Unduh file dan simpan
    output_path = File.join(Dir.tmpdir, "renewable_energy.pptx")
    file_content = client.beta.files.download(file_id)
    File.binwrite(output_path, file_content.read)
    puts "Presentation saved to #{output_path}"
  end
  ```
</CodeGroup>

<Note>
  Untuk detail lengkap tentang bekerja dengan file yang dihasilkan, lihat [Mengambil file yang dihasilkan](/docs/id/agents-and-tools/tool-use/code-execution-tool#retrieve-generated-files) di dokumentasi alat eksekusi kode.
</Note>

## Coba lebih banyak contoh

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
      "model": "claude-opus-4-8",
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
  model: claude-opus-4-8
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
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
          Model = Model.ClaudeOpus4_8,
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
  	Model:     anthropic.ModelClaudeOpus4_8,
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
          .model(CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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
      "model": "claude-opus-4-8",
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
  model: claude-opus-4-8
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
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
          Model = Model.ClaudeOpus4_8,
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
  	Model:     anthropic.ModelClaudeOpus4_8,
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
          .model(CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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
      "model": "claude-opus-4-8",
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
  model: claude-opus-4-8
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
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
          Model = Model.ClaudeOpus4_8,
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
  	Model:     anthropic.ModelClaudeOpus4_8,
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
          .model(CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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
  <Card title="Praktik terbaik penulisan Skill" icon="edit" href="/docs/id/agents-and-tools/agent-skills/best-practices">
    Pelajari cara menulis Skills yang efektif yang dapat ditemukan dan digunakan Claude dengan sukses.
  </Card>

  <Card title="Menggunakan Agent Skills dengan API" icon="book" href="/docs/id/build-with-claude/skills-guide">
    Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.
  </Card>

  <Card title="Buat Skills kustom" icon="code" href="/docs/id/api/skills/create-skill">
    Unggah Skills Anda sendiri untuk tugas-tugas khusus.
  </Card>

  <Card title="Gunakan Skills di Claude Code" icon="terminal" href="https://code.claude.com/docs/id/skills">
    Pelajari tentang Skills di Claude Code.
  </Card>

  <Card title="Agent Skills Cookbook" icon="book" href="https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction">
    Jelajahi contoh Skills dan pola implementasi.
  </Card>
</CardGroup>
