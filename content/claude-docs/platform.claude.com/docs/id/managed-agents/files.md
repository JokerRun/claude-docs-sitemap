---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/files
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 23e0724aed9de36d63528722d4aa15eff690647c1fcda3a7541dc9c325862c2b
---

# Menambahkan file

Unggah file dan pasang (mount) file tersebut di sandbox Anda untuk dibaca dan diproses.

---

Anda dapat menyediakan file untuk agen Anda dengan mengunggahnya melalui Files API dan memasangnya (mounting) di sandbox sesi.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Mengunggah file

Pertama, unggah file menggunakan [Files API](/docs/id/build-with-claude/files):

<CodeGroup>
  ```bash curl
  file=$(curl --fail-with-body -sS "${auth[@]}" \
    "${base_url}/files" \
    -F file=@data.csv)
  file_id=$(jq -er '.id' <<<"${file}")
  printf 'File ID: %s\n' "${file_id}"
  ```

  ```bash CLI
  FILE_ID=$(ant beta:files upload \
    --file data.csv \
    --transform id --raw-output)
  ```

  ```python Python
  file = client.beta.files.upload(file=Path("data.csv"))
  print(f"File ID: {file.id}")
  ```

  ```typescript TypeScript
  const file = await client.beta.files.upload({
    file: await toFile(readFile("data.csv"), "data.csv", { type: "text/csv" }),
  });
  console.log(`File ID: ${file.id}`);
  ```

  ```csharp C#
  await using var stream = File.OpenRead(csvPath);
  var file = await client.Beta.Files.Upload(new() { File = stream });
  Console.WriteLine($"File ID: {file.ID}");
  ```

  ```go Go
  csvFile, err := os.Open("data.csv")
  if err != nil {
  	panic(err)
  }
  defer csvFile.Close()

  file, err := client.Beta.Files.Upload(ctx, anthropic.BetaFileUploadParams{
  	File: csvFile,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Printf("File ID: %s\n", file.ID)
  ```

  ```java Java
  var file = client.beta().files().upload(
      FileUploadParams.builder().file(dataCsv).build()
  );
  IO.println("File ID: " + file.id());
  ```

  ```php PHP
  $file = $client->beta->files->upload(
      FileParam::fromResource(fopen($csvPath, 'r'), filename: 'data.csv', contentType: 'text/csv'),
  );
  echo "File ID: {$file->id}\n";
  ```

  ```ruby Ruby
  file = client.beta.files.upload(file: Pathname(csv_path))
  puts "File ID: #{file.id}"
  ```
</CodeGroup>

## Memasang file dalam sesi

Pasang file yang telah diunggah ke dalam sandbox dengan menambahkannya ke array `resources` saat membuat sesi:

<Tip>
  `mount_path` bersifat opsional, tetapi pastikan file yang diunggah memiliki nama yang deskriptif agar agen dapat mengidentifikasinya.
</Tip>

<CodeGroup>
  ```bash curl
  session=$(
    jq -n \
      --arg agent_id "${agent_id}" \
      --arg environment_id "${environment_id}" \
      --arg file_id "${file_id}" \
      '{
        agent: $agent_id,
        environment_id: $environment_id,
        resources: [
          {
            type: "file",
            file_id: $file_id,
            mount_path: "/data.csv"
          }
        ]
      }' | curl --fail-with-body -sS "${auth[@]}" "${base_url}/sessions" --json @-
  )
  session_id=$(jq -er '.id' <<<"${session}")
  ```

  ```bash CLI
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --transform id --raw-output <<EOF
  resources:
    - type: file
      file_id: $FILE_ID
      mount_path: /data.csv
  EOF
  )
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
        mount_path: "/data.csv",
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
          new BetaManagedAgentsFileResourceParams
          {
              Type = "file",
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
  			Type:      anthropic.BetaManagedAgentsFileResourceParamsTypeFile,
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
                  .type(BetaManagedAgentsFileResourceParams.Type.FILE)
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
              type: 'file',
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

Dengan `mount_path` di atas, agen membaca file di `/mnt/session/uploads/data.csv` (lihat [Jalur file](#file-paths)).

Sebuah `file_id` baru dibuat yang merujuk pada instans file dalam sesi tersebut. Salinan ini tidak dihitung terhadap [batas penyimpanan](/docs/id/build-with-claude/files) Anda.

## Beberapa file

Pasang beberapa file dengan menambahkan entri ke array `resources`:

<CodeGroup>
  ```json curl
  "resources": [
    { "type": "file", "file_id": "file_abc123", "mount_path": "/data.csv" },
    { "type": "file", "file_id": "file_def456", "mount_path": "/config.json" },
    { "type": "file", "file_id": "file_ghi789", "mount_path": "/src/main.py" }
  ]
  ```

  ```yaml CLI
  resources:
    - type: file
      file_id: file_abc123
      mount_path: /data.csv
    - type: file
      file_id: file_def456
      mount_path: /config.json
    - type: file
      file_id: file_ghi789
      mount_path: /src/main.py
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
  var resources = new[]
  {
      new BetaManagedAgentsFileResourceParams { Type = BetaManagedAgentsFileResourceParamsType.File, FileID = "file_abc123", MountPath = "/data.csv" },
      new BetaManagedAgentsFileResourceParams { Type = BetaManagedAgentsFileResourceParamsType.File, FileID = "file_def456", MountPath = "/config.json" },
      new BetaManagedAgentsFileResourceParams { Type = BetaManagedAgentsFileResourceParamsType.File, FileID = "file_ghi789", MountPath = "/src/main.py" },
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
  var resources = List.of(
      BetaManagedAgentsFileResourceParams.builder()
          .type(BetaManagedAgentsFileResourceParams.Type.FILE).fileId("file_abc123").mountPath("/data.csv").build(),
      BetaManagedAgentsFileResourceParams.builder()
          .type(BetaManagedAgentsFileResourceParams.Type.FILE).fileId("file_def456").mountPath("/config.json").build(),
      BetaManagedAgentsFileResourceParams.builder()
          .type(BetaManagedAgentsFileResourceParams.Type.FILE).fileId("file_ghi789").mountPath("/src/main.py").build()
  );
  ```

  ```php PHP
  $resources = [
      ['type' => 'file', 'file_id' => 'file_abc123', 'mount_path' => '/data.csv'],
      ['type' => 'file', 'file_id' => 'file_def456', 'mount_path' => '/config.json'],
      ['type' => 'file', 'file_id' => 'file_ghi789', 'mount_path' => '/src/main.py'],
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

Maksimum 500 file didukung per sesi.

## Mengelola file pada sesi yang sedang berjalan

Anda dapat menambahkan atau menghapus file dari sesi setelah pembuatan menggunakan API sumber daya sesi. Setiap sumber daya memiliki `id` yang dikembalikan saat ditambahkan (atau didaftar), yang Anda gunakan untuk penghapusan.

<CodeGroup>
  ```bash curl
  resource=$(
    jq -n --arg file_id "${file_id}" '{type: "file", file_id: $file_id}' \
      | curl --fail-with-body -sS "${auth[@]}" \
          "${base_url}/sessions/${session_id}/resources" --json @-
  )
  resource_id=$(jq -er '.id' <<<"${resource}")
  printf '%s\n' "${resource_id}"  # "sesrsc_01ABC..."
  ```

  ```bash CLI
  RESOURCE_ID=$(ant beta:sessions:resources add \
    --session-id "$SESSION_ID" \
    --type file \
    --file-id "$FILE_ID" \
    --transform id --raw-output)
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
    file_id: file.id,
  });
  console.log(resource.id); // "sesrsc_01ABC..."
  ```

  ```csharp C#
  var resource = await client.Beta.Sessions.Resources.Add(session.ID, new()
  {
      Type = "file",
      FileID = file.ID,
  });
  Console.WriteLine(resource.ID);  // "sesrsc_01ABC..."
  ```

  ```go Go
  resource, err := client.Beta.Sessions.Resources.Add(ctx, session.ID, anthropic.BetaSessionResourceAddParams{
  	BetaManagedAgentsFileResourceParams: anthropic.BetaManagedAgentsFileResourceParams{
  		Type:   anthropic.BetaManagedAgentsFileResourceParamsTypeFile,
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
                  .type(BetaManagedAgentsFileResourceParams.Type.FILE)
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
      type: 'file',
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

Daftarkan semua sumber daya pada sesi dengan `resources.list`. Untuk menghapus file, panggil `resources.delete` dengan ID sumber daya:

<CodeGroup>
  ```bash curl
  curl --fail-with-body -sS "${auth[@]}" \
    "${base_url}/sessions/${session_id}/resources" \
    | jq -r '.data[] | "\(.id) \(.type)"'

  curl --fail-with-body -sS "${auth[@]}" -X DELETE \
    "${base_url}/sessions/${session_id}/resources/${resource_id}" >/dev/null
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
    console.log(entry.id, entry.type);
  }

  await client.beta.sessions.resources.delete(resource.id, {
    session_id: session.id,
  });
  ```

  ```csharp C#
  var listed = await client.Beta.Sessions.Resources.List(session.ID);
  await foreach (var entry in listed.Paginate())
  {
      var type = entry.Match<string>(repo => repo.Type, fileRes => fileRes.Type, memoryStore => memoryStore.Type);
      Console.WriteLine($"{entry.ID} {type}");
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
      if (entry.isFile()) {
          var fileResource = entry.asFile();
          IO.println(fileResource.id() + " " + fileResource.type());
      } else if (entry.isGitHubRepository()) {
          var repoResource = entry.asGitHubRepository();
          IO.println(repoResource.id() + " " + repoResource.type());
      }
  }

  client.beta().sessions().resources().delete(
      resource.id(),
      ResourceDeleteParams.builder().sessionId(session.id()).build()
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

## Mendaftar dan mengunduh file sesi

Gunakan [Files API](/docs/id/build-with-claude/files) untuk mendaftar file yang tercakup dalam sebuah sesi dan mengunduhnya.

<CodeGroup>
  ```bash curl
  # Menampilkan daftar file yang terkait dengan sebuah sesi
  curl -fsSL "https://api.anthropic.com/v1/files?scope_id=sesn_abc123" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"

  # Mengunduh file
  curl -fsSL "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -o output.txt
  ```

  ```bash CLI
  # Menampilkan daftar file yang terkait dengan sebuah sesi
  ant beta:files list --scope-id sesn_abc123 \
    --beta managed-agents-2026-04-01

  # Mengunduh file
  ant beta:files download --file-id "$FILE_ID" --output output.txt
  ```

  ```python Python
  # Menampilkan daftar file yang terkait dengan sebuah sesi
  files = client.beta.files.list(
      scope_id="sesn_abc123",
      betas=["managed-agents-2026-04-01"],
  )
  for file in files:
      print(file.id, file.filename)

  # Mengunduh file
  content = client.beta.files.download(files.data[0].id)
  content.write_to_file("output.txt")
  ```

  ```typescript TypeScript
  // Mencantumkan file yang terkait dengan sebuah sesi
  const files = await client.beta.files.list({
    scope_id: "sesn_abc123",
    betas: ["managed-agents-2026-04-01"]
  });
  for (const file of files.data) {
    console.log(file.id, file.filename);
  }

  // Mengunduh file
  const content = await client.beta.files.download(files.data[0].id);
  await content.writeToFile("output.txt");
  ```

  ```csharp C#
  // Mencantumkan file yang terkait dengan sebuah sesi
  var files = await client.Beta.Files.List(new FileListParams
  {
      ScopeID = "sesn_abc123",
      Betas = ["managed-agents-2026-04-01"],
  });

  // Mengunduh file
  byte[] content = await client.Beta.Files.Download(files.Data[0].ID);
  await File.WriteAllBytesAsync("output.txt", content);
  ```

  ```go Go
  // Mencantumkan file yang terkait dengan sebuah sesi
  files, err := client.Beta.Files.List(ctx, anthropic.BetaFileListParams{
  	ScopeID: anthropic.String("sesn_abc123"),
  	Betas:   []anthropic.AnthropicBeta{"managed-agents-2026-04-01"},
  })
  if err != nil {
  	panic(err)
  }

  // Mengunduh file
  resp, err := client.Beta.Files.Download(ctx, files.Data[0].ID, anthropic.BetaFileDownloadParams{})
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
  // Mencantumkan file yang terkait dengan sebuah sesi
  var files = client.beta().files().list(FileListParams.builder()
      .scopeId("sesn_abc123")
      .addBeta(AnthropicBeta.of("managed-agents-2026-04-01"))
      .build());

  // Mengunduh file
  try (HttpResponse response = client.beta().files().download(files.data().get(0).id())) {
      try (InputStream body = response.body()) {
          Files.copy(body, Path.of("output.txt"), StandardCopyOption.REPLACE_EXISTING);
      }
  }
  ```

  ```php PHP
  // Menampilkan daftar file yang terkait dengan sebuah sesi
  $files = $client->beta->files->list(
      scopeID: 'sesn_abc123',
      betas: ['managed-agents-2026-04-01'],
  );

  // Mengunduh file
  $content = $client->beta->files->download($files->data[0]->id);
  file_put_contents('output.txt', $content);
  ```

  ```ruby Ruby
  # Mencantumkan file yang terkait dengan sebuah sesi
  files = client.beta.files.list(
    scope_id: "sesn_abc123",
    betas: ["managed-agents-2026-04-01"]
  )

  # Mengunduh file
  content = client.beta.files.download(files.data[0].id)
  File.binwrite("output.txt", content.read)
  ```
</CodeGroup>

## Tipe file yang didukung

Agen dapat bekerja dengan tipe file apa pun, termasuk:

* Kode sumber (`.py`, `.js`, `.ts`, `.go`, `.rs`, dan lainnya)
* File data (`.csv`, `.json`, `.xml`, `.yaml`)
* Dokumen (`.txt`, `.md`)
* Arsip (`.zip`, `.tar.gz`) - agen dapat mengekstraknya menggunakan bash
* File biner - agen dapat memprosesnya dengan alat yang sesuai

## Jalur file

<Note>
  File yang dipasang di sandbox adalah salinan hanya-baca. Agen dapat membacanya tetapi tidak dapat memodifikasi file asli yang diunggah. Untuk bekerja dengan versi yang dimodifikasi, agen menulis ke jalur baru di dalam sandbox.
</Note>

* Jalur yang Anda tentukan berakar di bawah direktori uploads milik sesi: `mount_path` berupa `/data.csv` menempatkan file di `/mnt/session/uploads/data.csv` dalam sandbox
* Jika Anda menghilangkan `mount_path`, file ditempatkan di `/mnt/session/uploads/<file_id>`
* Direktori induk dibuat secara otomatis
* Jalur harus absolut (dimulai dengan `/`)
