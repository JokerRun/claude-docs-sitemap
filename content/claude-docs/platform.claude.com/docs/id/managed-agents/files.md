---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/files
fetched_at: 2026-10-29T02:15:48.406163Z
sha256: f19a29eb2f6a1ba9874c113c26264e6cd03352b6db186c2a8b95ead3d3125c87
---

---
title: Menambahkan file
url: https://platform.claude.com/docs/id/managed-agents/files
description: Unggah file dan me-mount-nya di sandbox Anda untuk dibaca dan diproses.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Sessions are stateful resources; transcripts persist until you delete them. Applies to all Managed Agents sub-features, including Self-hosted sandboxes.
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
    Claude Models on Google Cloud (Anthropic managed): beta
---

Anda dapat menyediakan file untuk agen Anda dengan mengunggahnya melalui Files API dan me-mount-nya di sandbox sesi.

## Mengunggah file

Pertama, unggah file menggunakan [Files API](https://platform.claude.com/docs/id/build-with-claude/files):

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -F file=@data.csv
  ```

  ```bash CLI
  ant files upload --file data.csv
  ```

  ```python Python
  file = client.files.upload(file=Path("data.csv"))
  print(f"File ID: {file.id}")
  ```

  ```typescript TypeScript
  const file = await client.files.upload({
    file: await toFile(readFile("data.csv"), "data.csv", { type: "text/csv" })
  });
  console.log(`File ID: ${file.id}`);
  ```

  ```csharp C#
  await using var stream = File.OpenRead(csvPath);
  var file = await client.Files.Upload(new() { File = stream });
  Console.WriteLine($"File ID: {file.ID}");
  ```

  ```go Go
  csvFile, err := os.Open("data.csv")
  if err != nil {
  	panic(err)
  }
  defer csvFile.Close()

  file, err := client.Files.Upload(ctx, anthropic.FileUploadParams{
  	File: csvFile,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Printf("File ID: %s\n", file.ID)
  ```

  ```java Java
  var file = client.files().upload(
      FileUploadParams.builder()
          .file(dataCsv)
          .build()
  );
  IO.println("File ID: " + file.id());
  ```

  ```php PHP
  $file = $client->files->upload(
      file: FileParam::fromResource(fopen($csvPath, 'r'), filename: 'data.csv', contentType: 'text/csv'),
  );
  echo "File ID: {$file->id}\n";
  ```

  ```ruby Ruby
  file = client.files.upload(file: Pathname(csv_path))
  puts "File ID: #{file.id}"
  ```
</CodeGroup>

## Me-mount file dalam sesi

Mount file yang telah diunggah ke dalam sandbox dengan menambahkannya ke array `resources` (csharp, go: `Resources`) saat membuat sesi:

<Tip>
  `mount_path` (java, php: `mountPath`; csharp, go: `MountPath`) bersifat opsional, tetapi pastikan file yang diunggah memiliki nama yang deskriptif agar agen dapat mengidentifikasinya.
</Tip>

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "agent": "'"$AGENT_ID"'",
      "environment_id": "'"$ENVIRONMENT_ID"'",
      "resources": [
        {
          "type": "file",
          "file_id": "'"$FILE_ID"'",
          "mount_path": "/data.csv"
        }
      ]
    }'
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" <<EOF
  resources:
    - type: file
      file_id: $FILE_ID
      mount_path: /data.csv
  EOF
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      resources=[
          {
              "type": "file",
              "file_id": file.id,
              "mount_path": "/data.csv",
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
        type: "file",
        file_id: file.id,
        mount_path: "/data.csv"
      }
    ]
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Resources =
      [
          new BetaManagedAgentsFileResourceParams
          {
              FileID = file.ID,
              MountPath = "/data.csv",
          },
      ],
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	Resources: []anthropic.BetaSessionNewParamsResourceUnion{{
  		OfFile: &anthropic.BetaManagedAgentsFileResourceParams{
  			FileID:    file.ID,
  			MountPath: anthropic.String("/data.csv"),
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(
      SessionCreateParams.builder()
          .agent(agent.id())
          .environmentId(environment.id())
          .addResource(
              BetaManagedAgentsFileResourceParams.builder()
                  .fileId(file.id())
                  .mountPath("/data.csv")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      resources: [
          BetaManagedAgentsFileResourceParams::with(
              fileID: $file->id,
              mountPath: '/data.csv',
          ),
      ],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "file",
        file_id: file.id,
        mount_path: "/data.csv"
      }
    ]
  )
  ```
</CodeGroup>

Dengan `mount_path` (java, php: `mountPath`; csharp, go: `MountPath`) di atas, agen membaca file di `/mnt/session/uploads/data.csv` (lihat [Path file](https://platform.claude.com/docs/id/managed-agents/files#file-paths)).

`file_id` (java: `fileId`; php: `fileID`; csharp, go: `FileID`) baru dibuat yang mereferensikan instance file tersebut di dalam sesi. Salinan ini tidak dihitung terhadap [batas penyimpanan](https://platform.claude.com/docs/id/build-with-claude/files) Anda.

## Beberapa file

Mount beberapa file dengan menambahkan entri ke array `resources` (csharp, go: `Resources`):

<CodeGroup>
  ```bash cURL
  curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "agent": "agent_01J8XkN5uT3vHpLqRfWdY2",
      "environment_id": "env_01K2mPsT7hNwR4jXuLvCqD8",
      "resources": [
        {
          "type": "file",
          "file_id": "file_011CNha8iCJcU1wXNR6q4V8w",
          "mount_path": "/data.csv"
        },
        {
          "type": "file",
          "file_id": "file_011CPMxVD3fHLUhvTqtsQA5w",
          "mount_path": "/config.json"
        },
        {
          "type": "file",
          "file_id": "file_011CRb3kQ7tWx9ZsLmDe2Vh4",
          "mount_path": "/src/main.py"
        }
      ]
    }'
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent agent_01J8XkN5uT3vHpLqRfWdY2 \
    --environment-id env_01K2mPsT7hNwR4jXuLvCqD8 <<YAML
  resources:
    - type: file
      file_id: file_011CNha8iCJcU1wXNR6q4V8w
      mount_path: /data.csv
    - type: file
      file_id: file_011CPMxVD3fHLUhvTqtsQA5w
      mount_path: /config.json
    - type: file
      file_id: file_011CRb3kQ7tWx9ZsLmDe2Vh4
      mount_path: /src/main.py
  YAML
  ```

  ```python Python
  resources = [
      {"type": "file", "file_id": "file_abc123", "mount_path": "/data.csv"},
      {"type": "file", "file_id": "file_def456", "mount_path": "/config.json"},
      {"type": "file", "file_id": "file_ghi789", "mount_path": "/src/main.py"},
  ]
  ```

  ```typescript TypeScript
  resources: [
    { type: "file", file_id: "file_abc123", mount_path: "/data.csv" },
    { type: "file", file_id: "file_def456", mount_path: "/config.json" },
    { type: "file", file_id: "file_ghi789", mount_path: "/src/main.py" }
  ]
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Sessions;

  var resources = new[]
  {
      new BetaManagedAgentsFileResourceParams { FileID = "file_abc123", MountPath = "/data.csv" },
      new BetaManagedAgentsFileResourceParams { FileID = "file_def456", MountPath = "/config.json" },
      new BetaManagedAgentsFileResourceParams { FileID = "file_ghi789", MountPath = "/src/main.py" },
  };
  ```

  ```go Go
  resources := []anthropic.BetaSessionNewParamsResourceUnion{
  	{OfFile: &anthropic.BetaManagedAgentsFileResourceParams{Type: "file", FileID: "file_abc123", MountPath: anthropic.String("/data.csv")}},
  	{OfFile: &anthropic.BetaManagedAgentsFileResourceParams{Type: "file", FileID: "file_def456", MountPath: anthropic.String("/config.json")}},
  	{OfFile: &anthropic.BetaManagedAgentsFileResourceParams{Type: "file", FileID: "file_ghi789", MountPath: anthropic.String("/src/main.py")}},
  }
  ```

  ```java Java
  import com.anthropic.models.beta.sessions.*;
  import java.util.List;

  var resources = List.of(
      BetaManagedAgentsFileResourceParams.builder()
          .fileId("file_abc123")
          .mountPath("/data.csv")
          .build(),
      BetaManagedAgentsFileResourceParams.builder()
          .fileId("file_def456")
          .mountPath("/config.json")
          .build(),
      BetaManagedAgentsFileResourceParams.builder()
          .fileId("file_ghi789")
          .mountPath("/src/main.py")
          .build()
  );
  ```

  ```php PHP
  $resources = [
      ['type' => 'file', 'fileID' => 'file_abc123', 'mountPath' => '/data.csv'],
      ['type' => 'file', 'fileID' => 'file_def456', 'mountPath' => '/config.json'],
      ['type' => 'file', 'fileID' => 'file_ghi789', 'mountPath' => '/src/main.py'],
  ];
  ```

  ```ruby Ruby
  resources = [
    {type: "file", file_id: "file_abc123", mount_path: "/data.csv"},
    {type: "file", file_id: "file_def456", mount_path: "/config.json"},
    {type: "file", file_id: "file_ghi789", mount_path: "/src/main.py"}
  ]
  ```
</CodeGroup>

Maksimal 500 file didukung untuk setiap sesi.

## Mengelola file pada sesi yang sedang berjalan

Anda dapat menambahkan atau menghapus file dari sesi setelah dibuat menggunakan API resources sesi. Setiap resource memiliki `id` (csharp, go: `ID`) yang dikembalikan saat ditambahkan (atau didaftarkan), yang Anda gunakan untuk penghapusan.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/resources" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "type": "file",
      "file_id": "'"$FILE_ID"'"
    }'
  ```

  ```bash CLI
  ant beta:sessions:resources add \
    --session-id "$SESSION_ID" \
    --type file \
    --file-id "$FILE_ID"
  ```

  ```python Python
  resource = client.beta.sessions.resources.add(
      session.id,
      type="file",
      file_id=file.id,
  )
  print(resource.id)  # "sesrsc_01ABC..."
  ```

  ```typescript TypeScript
  const resource = await client.beta.sessions.resources.add(session.id, {
    type: "file",
    file_id: file.id
  });
  if (resource.type !== "file") {
    throw new Error(`Unexpected resource type: ${resource.type}`);
  }
  console.log(resource.id); // "sesrsc_01ABC..."
  ```

  ```csharp C#
  var resource = await client.Beta.Sessions.Resources.Add(session.ID, new()
  {
      FileID = file.ID,
  });
  Console.WriteLine(resource.ID);  // "sesrsc_01ABC..."
  ```

  ```go Go
  resource, err := client.Beta.Sessions.Resources.Add(ctx, session.ID, anthropic.BetaSessionResourceAddParams{
  	BetaManagedAgentsFileResourceParams: anthropic.BetaManagedAgentsFileResourceParams{
  		FileID: file.ID,
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(resource.ID) // "sesrsc_01ABC..."
  ```

  ```java Java
  var resource = client.beta().sessions().resources().add(
      session.id(),
      ResourceAddParams.builder()
          .betaManagedAgentsFileResourceParams(
              BetaManagedAgentsFileResourceParams.builder()
                  .fileId(file.id())
                  .build()
          )
          .build()
  );
  IO.println(resource.id()); // "sesrsc_01ABC..."
  ```

  ```php PHP
  $resource = $client->beta->sessions->resources->add(
      $session->id,
      fileID: $file->id,
  );
  echo "{$resource->id}\n";  // "sesrsc_01ABC..."
  ```

  ```ruby Ruby
  resource = client.beta.sessions.resources.add(
    session.id,
    type: "file",
    file_id: file.id
  )
  puts resource.id # "sesrsc_01ABC..."
  ```
</CodeGroup>

Tampilkan daftar semua resource pada sesi dengan `GET /v1/sessions/{session_id}/resources` (python, typescript, ruby: `client.beta.sessions.resources.list()`; go, csharp: `client.Beta.Sessions.Resources.List()`; java: `client.beta().sessions().resources().list()`; php: `$client->beta->sessions->resources->list()`; cli: `ant beta:sessions:resources list`). Untuk menghapus file, panggil `DELETE /v1/sessions/{session_id}/resources/{resource_id}` (python, typescript, ruby: `client.beta.sessions.resources.delete()`; go, csharp: `client.Beta.Sessions.Resources.Delete()`; java: `client.beta().sessions().resources().delete()`; php: `$client->beta->sessions->resources->delete()`; cli: `ant beta:sessions:resources delete`) dengan ID resource:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/resources" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"

  curl --fail-with-body -sS -X DELETE "https://api.anthropic.com/v1/sessions/$SESSION_ID/resources/$RESOURCE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:sessions:resources list --session-id "$SESSION_ID"

  ant beta:sessions:resources delete \
    --session-id "$SESSION_ID" \
    --resource-id "$RESOURCE_ID"
  ```

  ```python Python
  listed = client.beta.sessions.resources.list(session.id)
  for entry in listed.data:
      print(entry.id, entry.type)

  client.beta.sessions.resources.delete(resource.id, session_id=session.id)
  ```

  ```typescript TypeScript
  const listed = await client.beta.sessions.resources.list(session.id);
  for (const entry of listed.data) {
    if (entry.type !== "memory_store") {
      console.log(entry.id, entry.type);
    }
  }

  await client.beta.sessions.resources.delete(resource.id, {
    session_id: session.id
  });
  ```

  ```csharp C#
  var listed = await client.Beta.Sessions.Resources.List(session.ID);
  await foreach (var entry in listed.Paginate())
  {
      Console.WriteLine($"{entry.ID} {entry.Type.Raw()}");
  }

  await client.Beta.Sessions.Resources.Delete(resource.ID, new() { SessionID = session.ID });
  ```

  ```go Go
  listed, err := client.Beta.Sessions.Resources.List(ctx, session.ID, anthropic.BetaSessionResourceListParams{})
  if err != nil {
  	panic(err)
  }
  for _, entry := range listed.Data {
  	fmt.Println(entry.ID, entry.Type)
  }

  if _, err := client.Beta.Sessions.Resources.Delete(ctx, resource.ID, anthropic.BetaSessionResourceDeleteParams{
  	SessionID: session.ID,
  }); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var listed = client.beta().sessions().resources().list(session.id());
  for (var entry : listed.data()) {
      switch (entry.type().value()) {
          case FILE -> {
              var fileResource = entry.asFile();
              IO.println(fileResource.id() + " " + fileResource._type());
          }
          case GITHUB_REPOSITORY -> {
              var repoResource = entry.asGitHubRepository();
              IO.println(repoResource.id() + " " + repoResource._type());
          }
      }
  }

  client.beta().sessions().resources().delete(
      resource.id(),
      ResourceDeleteParams.builder()
          .sessionId(session.id())
          .build()
  );
  ```

  ```php PHP
  $listed = $client->beta->sessions->resources->list($session->id);
  foreach ($listed->data as $entry) {
      echo "{$entry->id} {$entry->type}\n";
  }

  $client->beta->sessions->resources->delete($resource->id, sessionID: $session->id);
  ```

  ```ruby Ruby
  listed = client.beta.sessions.resources.list(session.id)
  listed.data.each { puts "#{it.id} #{it.type}" }

  client.beta.sessions.resources.delete(resource.id, session_id: session.id)
  ```
</CodeGroup>

## Mendaftarkan dan mengunduh file sesi

Gunakan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) untuk mencantumkan file yang dicakup pada suatu sesi dan mengunduhnya. File yang ditulis agen ke `/mnt/session/outputs/` akan muncul dalam daftar tidak lama setelah agen selesai menulisnya, terkadang beberapa detik setelah sesi menjadi idle. Jika file output yang Anda harapkan tidak ada, cantumkan lagi setelah jeda singkat; setelah file muncul dalam daftar, unggahannya sudah selesai.

Pemfilteran berdasarkan `scope_id` (java: `scopeId`; php: `scopeID`; csharp, go: `ScopeID`) memerlukan header beta `managed-agents-2026-04-01`, sehingga contoh daftar memanggil `GET /v1/files` (python, typescript, ruby: `client.beta.files.list()`; go, csharp: `client.Beta.Files.List()`; java: `client.beta().files().list()`; php: `$client->beta->files->list()`; cli: `ant beta:files list`) dan meneruskan header tersebut secara eksplisit.

<CodeGroup>
  ```bash cURL
  # Daftar file yang terkait dengan sebuah sesi
  curl -fsSL "https://api.anthropic.com/v1/files?scope_id=sesn_abc123" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"

  # Unduh sebuah file
  curl -fsSL "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -o output.txt
  ```

  ```bash CLI
  # Daftar file yang terkait dengan sebuah sesi
  ant beta:files list --scope-id sesn_abc123 --beta managed-agents-2026-04-01

  # Unduh sebuah file
  ant files download --file-id "$FILE_ID" --output output.txt
  ```

  ```python Python
  # Daftar file yang terkait dengan sebuah sesi
  files = client.beta.files.list(
      scope_id="sesn_abc123",
      betas=["managed-agents-2026-04-01"],
  )
  for file in files:
      print(file.id, file.filename)

  # Unduh sebuah file
  content = client.files.download(files.data[0].id)
  content.write_to_file("output.txt")
  ```

  ```typescript TypeScript
  import { writeFile } from "node:fs/promises";

  // Daftar file yang terkait dengan sebuah sesi
  const files = await client.beta.files.list({
    scope_id: "sesn_abc123",
    betas: ["managed-agents-2026-04-01"]
  });
  for (const file of files.data) {
    console.log(file.id, file.filename);
  }

  // Unduh sebuah file
  const content = await client.files.download(files.data[0].id);
  await writeFile("output.txt", new Uint8Array(await content.arrayBuffer()));
  ```

  ```csharp C#
  // Daftar file yang terkait dengan sebuah sesi
  var files = await client.Beta.Files.List(new()
  {
      ScopeID = "sesn_abc123",
      Betas = ["managed-agents-2026-04-01"],
  });

  // Unduh sebuah file
  using var content = await client.Files.Download(files.Items[0].ID);
  await using var output = File.Create("output.txt");
  await (await content.ReadAsStream()).CopyToAsync(output);
  ```

  ```go Go
  // Daftar file yang terkait dengan sesi
  files, err := client.Beta.Files.List(ctx, anthropic.BetaFileListParams{
  	ScopeID: anthropic.String("sesn_abc123"),
  	Betas:   []anthropic.AnthropicBeta{"managed-agents-2026-04-01"},
  })
  if err != nil {
  	panic(err)
  }

  // Unduh file
  resp, err := client.Files.Download(ctx, files.Data[0].ID, anthropic.FileDownloadParams{})
  if err != nil {
  	panic(err)
  }
  defer resp.Body.Close()
  out, err := os.Create("output.txt")
  if err != nil {
  	panic(err)
  }
  defer out.Close()
  if _, err := io.Copy(out, resp.Body); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  // Daftar file yang terkait dengan sebuah sesi
  var files = client.beta().files().list(FileListParams.builder()
      .scopeId("sesn_abc123")
      .addBeta(AnthropicBeta.of("managed-agents-2026-04-01"))
      .build());

  // Unduh sebuah file
  try (HttpResponse response = client.files().download(files.data().get(0).id())) {
      try (InputStream body = response.body()) {
          Files.copy(body, Path.of("output.txt"), StandardCopyOption.REPLACE_EXISTING);
      }
  }
  ```

  ```php PHP
  // Daftar file yang terkait dengan sebuah sesi
  $files = $client->beta->files->list(
      scopeID: 'sesn_abc123',
      betas: ['managed-agents-2026-04-01'],
  );
  foreach ($files->getItems() as $file) {
      echo "{$file->id} {$file->filename}\n";
  }

  // Unduh sebuah file
  $content = $client->files->download($files->getItems()[0]->id);
  file_put_contents('output.txt', $content);
  ```

  ```ruby Ruby
  # Daftar file yang terkait dengan sebuah sesi
  files = client.beta.files.list(
    scope_id: "sesn_abc123",
    betas: ["managed-agents-2026-04-01"]
  )

  # Unduh sebuah file
  content = client.files.download(files.data[0].id)
  File.binwrite("output.txt", content.read)
  ```
</CodeGroup>

## Jenis file yang didukung

Agen dapat bekerja dengan jenis file apa pun, termasuk:

* Kode sumber (`.py`, `.js`, `.ts`, `.go`, `.rs`, dan lainnya)
* File data (`.csv`, `.json`, `.xml`, `.yaml`)
* Dokumen (`.txt`, `.md`)
* Arsip (`.zip`, `.tar.gz`) - agen dapat mengekstraknya menggunakan bash
* File biner - agen dapat memprosesnya dengan alat yang sesuai

## Path file

<Note>
  File yang di-mount di sandbox adalah salinan read-only (hanya-baca). Agen dapat membacanya tetapi tidak dapat memodifikasi file asli yang diunggah. Untuk bekerja dengan versi yang dimodifikasi, agen menulis ke path baru di dalam sandbox.
</Note>

* Path yang Anda tentukan berakar di bawah direktori uploads sesi: `mount_path` (java, php: `mountPath`; csharp, go: `MountPath`) bernilai `/data.csv` menempatkan file di `/mnt/session/uploads/data.csv` di dalam sandbox.
* Jika Anda menghilangkan `mount_path` (java, php: `mountPath`; csharp, go: `MountPath`), file ditempatkan di `/mnt/session/uploads/<file_id>`.
* Direktori induk dibuat secara otomatis.
* Path harus absolut (diawali dengan `/`).
* File yang ditulis agen ke `/mnt/session/outputs/` menjadi tersedia melalui Files API, dengan cakupan sesi tersebut; lihat [Mencantumkan dan mengunduh file sesi](https://platform.claude.com/docs/id/managed-agents/files#listing-and-downloading-session-files).
