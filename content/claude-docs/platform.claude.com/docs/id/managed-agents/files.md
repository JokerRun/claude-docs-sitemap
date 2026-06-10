---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/files
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: c5f31acc24bce55daef46d669ce2ffb342a6152b08912bf45fb76184813a60d2
---

# Menambahkan file

Unggah file dan pasang di sandbox Anda untuk dibaca dan diproses.

---

Anda dapat menyediakan file untuk agen Anda dengan mengunggahnya melalui Files API dan memasangnya di sandbox sesi.

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Mengunggah file \{#uploading-files}

Pertama, unggah file menggunakan [Files API](/docs/id/build-with-claude/files):

<CodeGroup>
  
````bash
file=$(curl --fail-with-body -sS "${auth[@]}" \
  "${base_url}/files" \
  -F file=@data.csv)
file_id=$(jq -er '.id' <<<"${file}")
printf 'File ID: %s\n' "${file_id}"
````

  
````bash
FILE_ID=$(ant beta:files upload \
  --file data.csv \
  --transform id --raw-output)
````

  
````python
file = client.beta.files.upload(file=Path("data.csv"))
print(f"File ID: {file.id}")
````

  
````typescript
const file = await client.beta.files.upload({
  file: await toFile(readFile("data.csv"), "data.csv", { type: "text/csv" }),
});
console.log(`File ID: ${file.id}`);
````

  
````csharp
await using var stream = File.OpenRead(csvPath);
var file = await client.Beta.Files.Upload(new() { File = stream });
Console.WriteLine($"File ID: {file.ID}");
````

  
````go
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
````

  
````java
var file = client.beta().files().upload(
    FileUploadParams.builder().file(dataCsv).build()
);
IO.println("File ID: " + file.id());
````

  
````php
$file = $client->beta->files->upload(
    FileParam::fromResource(fopen($csvPath, 'r'), filename: 'data.csv', contentType: 'text/csv'),
);
echo "File ID: {$file->id}\n";
````

  
````ruby
file = client.beta.files.upload(file: Pathname(csv_path))
puts "File ID: #{file.id}"
````

</CodeGroup>

## Memasang file dalam sesi \{#mounting-files-in-a-session}

Pasang file yang telah diunggah ke dalam sandbox dengan menambahkannya ke array `resources` saat membuat sesi:

<Tip>
`mount_path` bersifat opsional, tetapi pastikan file yang diunggah memiliki nama yang deskriptif agar agen dapat mengidentifikasinya.
</Tip>

<CodeGroup>
  
````bash
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
          mount_path: "/workspace/data.csv"
        }
      ]
    }' | curl --fail-with-body -sS "${auth[@]}" "${base_url}/sessions" --json @-
)
session_id=$(jq -er '.id' <<<"${session}")
````

  
````bash
SESSION_ID=$(ant beta:sessions create \
  --agent "$AGENT_ID" \
  --environment-id "$ENVIRONMENT_ID" \
  --transform id --raw-output <<EOF
resources:
  - type: file
    file_id: $FILE_ID
    mount_path: /workspace/data.csv
EOF
)
````

  
````python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    resources=[
        {
            "type": "file",
            "file_id": file.id,
            "mount_path": "/workspace/data.csv",
        },
    ],
)
````

  
````typescript
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  resources: [
    {
      type: "file",
      file_id: file.id,
      mount_path: "/workspace/data.csv",
    },
  ],
});
````

  
````csharp
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
            MountPath = "/workspace/data.csv",
        },
    ],
});
````

  
````go
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfString: anthropic.String(agent.ID),
	},
	EnvironmentID: environment.ID,
	Resources: []anthropic.BetaSessionNewParamsResourceUnion{{
		OfFile: &anthropic.BetaManagedAgentsFileResourceParams{
			Type:      anthropic.BetaManagedAgentsFileResourceParamsTypeFile,
			FileID:    file.ID,
			MountPath: anthropic.String("/workspace/data.csv"),
		},
	}},
})
if err != nil {
	panic(err)
}
````

  
````java
var session = client.beta().sessions().create(
    SessionCreateParams.builder()
        .agent(agent.id())
        .environmentId(environment.id())
        .addResource(
            BetaManagedAgentsFileResourceParams.builder()
                .type(BetaManagedAgentsFileResourceParams.Type.FILE)
                .fileId(file.id())
                .mountPath("/workspace/data.csv")
                .build()
        )
        .build()
);
````

  
````php
$session = $client->beta->sessions->create(
    agent: $agent->id,
    environmentID: $environment->id,
    resources: [
        BetaManagedAgentsFileResourceParams::with(
            type: 'file',
            fileID: $file->id,
            mountPath: '/workspace/data.csv',
        ),
    ],
);
````

  
````ruby
session = client.beta.sessions.create(
  agent: agent.id,
  environment_id: environment.id,
  resources: [
    {
      type: "file",
      file_id: file.id,
      mount_path: "/workspace/data.csv"
    }
  ]
)
````

</CodeGroup>

Sebuah `file_id` baru dibuat yang mereferensikan instance file dalam sesi tersebut. Salinan ini tidak dihitung terhadap [batas penyimpanan](/docs/id/build-with-claude/files) Anda.

## Beberapa file \{#multiple-files}

Pasang beberapa file dengan menambahkan entri ke array `resources`:

<CodeGroup>
```json curl hidelines={1,-1}
{
  "resources": [
    { "type": "file", "file_id": "file_abc123", "mount_path": "/workspace/data.csv" },
    { "type": "file", "file_id": "file_def456", "mount_path": "/workspace/config.json" },
    { "type": "file", "file_id": "file_ghi789", "mount_path": "/workspace/src/main.py" }
  ]
}
```

```yaml CLI
resources:
  - type: file
    file_id: file_abc123
    mount_path: /workspace/data.csv
  - type: file
    file_id: file_def456
    mount_path: /workspace/config.json
  - type: file
    file_id: file_ghi789
    mount_path: /workspace/src/main.py
```

```python Python
resources = [
    {"type": "file", "file_id": "file_abc123", "mount_path": "/workspace/data.csv"},
    {"type": "file", "file_id": "file_def456", "mount_path": "/workspace/config.json"},
    {"type": "file", "file_id": "file_ghi789", "mount_path": "/workspace/src/main.py"},
]
```

```typescript TypeScript hidelines={1,-1}
const _ = {
  resources: [
    { type: "file", file_id: "file_abc123", mount_path: "/workspace/data.csv" },
    { type: "file", file_id: "file_def456", mount_path: "/workspace/config.json" },
    { type: "file", file_id: "file_ghi789", mount_path: "/workspace/src/main.py" }
  ]
};
```

```csharp C#
var resources = new[]
{
    new BetaManagedAgentsFileResourceParams { Type = BetaManagedAgentsFileResourceParamsType.File, FileID = "file_abc123", MountPath = "/workspace/data.csv" },
    new BetaManagedAgentsFileResourceParams { Type = BetaManagedAgentsFileResourceParamsType.File, FileID = "file_def456", MountPath = "/workspace/config.json" },
    new BetaManagedAgentsFileResourceParams { Type = BetaManagedAgentsFileResourceParamsType.File, FileID = "file_ghi789", MountPath = "/workspace/src/main.py" },
};
```

```go Go
resources := []anthropic.BetaSessionNewParamsResourceUnion{
	{OfFile: &anthropic.BetaManagedAgentsFileResourceParams{Type: "file", FileID: "file_abc123", MountPath: anthropic.String("/workspace/data.csv")}},
	{OfFile: &anthropic.BetaManagedAgentsFileResourceParams{Type: "file", FileID: "file_def456", MountPath: anthropic.String("/workspace/config.json")}},
	{OfFile: &anthropic.BetaManagedAgentsFileResourceParams{Type: "file", FileID: "file_ghi789", MountPath: anthropic.String("/workspace/src/main.py")}},
}
_ = resources
```

```java Java
var resources = List.of(
    BetaManagedAgentsFileResourceParams.builder()
        .type(BetaManagedAgentsFileResourceParams.Type.FILE).fileId("file_abc123").mountPath("/workspace/data.csv").build(),
    BetaManagedAgentsFileResourceParams.builder()
        .type(BetaManagedAgentsFileResourceParams.Type.FILE).fileId("file_def456").mountPath("/workspace/config.json").build(),
    BetaManagedAgentsFileResourceParams.builder()
        .type(BetaManagedAgentsFileResourceParams.Type.FILE).fileId("file_ghi789").mountPath("/workspace/src/main.py").build()
);
```

```php PHP
$resources = [
    ['type' => 'file', 'file_id' => 'file_abc123', 'mount_path' => '/workspace/data.csv'],
    ['type' => 'file', 'file_id' => 'file_def456', 'mount_path' => '/workspace/config.json'],
    ['type' => 'file', 'file_id' => 'file_ghi789', 'mount_path' => '/workspace/src/main.py'],
];
```

```ruby Ruby
resources = [
  {type: "file", file_id: "file_abc123", mount_path: "/workspace/data.csv"},
  {type: "file", file_id: "file_def456", mount_path: "/workspace/config.json"},
  {type: "file", file_id: "file_ghi789", mount_path: "/workspace/src/main.py"}
]
```
</CodeGroup>

Maksimum 100 file didukung per sesi.

## Mengelola file pada sesi yang sedang berjalan \{#managing-files-on-a-running-session}

Anda dapat menambahkan atau menghapus file dari sesi setelah pembuatan menggunakan API resources sesi. Setiap resource memiliki `id` yang dikembalikan saat ditambahkan (atau didaftarkan), yang Anda gunakan untuk penghapusan.

<CodeGroup>
  
````bash
resource=$(
  jq -n --arg file_id "${file_id}" '{type: "file", file_id: $file_id}' \
    | curl --fail-with-body -sS "${auth[@]}" \
        "${base_url}/sessions/${session_id}/resources" --json @-
)
resource_id=$(jq -er '.id' <<<"${resource}")
printf '%s\n' "${resource_id}"  # "sesrsc_01ABC..."
````

  
````bash
RESOURCE_ID=$(ant beta:sessions:resources add \
  --session-id "$SESSION_ID" \
  --type file \
  --file-id "$FILE_ID" \
  --transform id --raw-output)
````

  
````python
resource = client.beta.sessions.resources.add(
    session.id,
    type="file",
    file_id=file.id,
)
print(resource.id)  # "sesrsc_01ABC..."
````

  
````typescript
const resource = await client.beta.sessions.resources.add(session.id, {
  type: "file",
  file_id: file.id,
});
console.log(resource.id); // "sesrsc_01ABC..."
````

  
````csharp
var resource = await client.Beta.Sessions.Resources.Add(session.ID, new()
{
    Type = "file",
    FileID = file.ID,
});
Console.WriteLine(resource.ID);  // "sesrsc_01ABC..."
````

  
````go
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
````

  
````java
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
````

  
````php
$resource = $client->beta->sessions->resources->add(
    $session->id,
    type: 'file',
    fileID: $file->id,
);
echo "{$resource->id}\n";  // "sesrsc_01ABC..."
````

  
````ruby
resource = client.beta.sessions.resources.add(
  session.id,
  type: "file",
  file_id: file.id
)
puts resource.id # "sesrsc_01ABC..."
````

</CodeGroup>

Daftarkan semua resource pada sesi dengan `resources.list`. Untuk menghapus file, panggil `resources.delete` dengan ID resource:

<CodeGroup>
  
````bash
curl --fail-with-body -sS "${auth[@]}" \
  "${base_url}/sessions/${session_id}/resources" \
  | jq -r '.data[] | "\(.id) \(.type)"'

curl --fail-with-body -sS "${auth[@]}" -X DELETE \
  "${base_url}/sessions/${session_id}/resources/${resource_id}" >/dev/null
````

  
````bash
ant beta:sessions:resources list --session-id "$SESSION_ID"

ant beta:sessions:resources delete \
  --session-id "$SESSION_ID" \
  --resource-id "$RESOURCE_ID"
````

  
````python
listed = client.beta.sessions.resources.list(session.id)
for entry in listed.data:
    print(entry.id, entry.type)

client.beta.sessions.resources.delete(resource.id, session_id=session.id)
````

  
````typescript
const listed = await client.beta.sessions.resources.list(session.id);
for (const entry of listed.data) {
  console.log(entry.id, entry.type);
}

await client.beta.sessions.resources.delete(resource.id, {
  session_id: session.id,
});
````

  
````csharp
var listed = await client.Beta.Sessions.Resources.List(session.ID);
await foreach (var entry in listed.Paginate())
{
    var type = entry.Match<string>(repo => repo.Type, fileRes => fileRes.Type, memoryStore => memoryStore.Type);
    Console.WriteLine($"{entry.ID} {type}");
}

await client.Beta.Sessions.Resources.Delete(resource.ID, new() { SessionID = session.ID });
````

  
````go
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
````

  
````java
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
````

  
````php
$listed = $client->beta->sessions->resources->list($session->id);
foreach ($listed->data as $entry) {
    echo "{$entry->id} {$entry->type}\n";
}

$client->beta->sessions->resources->delete($resource->id, sessionID: $session->id);
````

  
````ruby
listed = client.beta.sessions.resources.list(session.id)
listed.data.each { puts "#{it.id} #{it.type}" }

client.beta.sessions.resources.delete(resource.id, session_id: session.id)
````

</CodeGroup>

## Mendaftarkan dan mengunduh file sesi \{#listing-and-downloading-session-files}

Gunakan [Files API](/docs/id/build-with-claude/files) untuk mendaftarkan file yang tercakup dalam sesi dan mengunduhnya.

<CodeGroup>
```bash curl nocheck
# Daftar file yang terkait dengan sebuah sesi
curl -fsSL "https://api.anthropic.com/v1/files?scope_id=sesn_abc123" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"

# Unduh sebuah file
curl -fsSL "https://api.anthropic.com/v1/files/$FILE_ID/content" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -o output.txt
```

```bash CLI nocheck
# Menampilkan daftar file yang terkait dengan sebuah sesi
ant beta:files list --scope-id sesn_abc123 \
  --beta files-api-2025-04-14 \
  --beta managed-agents-2026-04-01

# Mengunduh file
ant beta:files download --file-id "$FILE_ID" --output output.txt
```

```python Python nocheck
# Daftar file yang terkait dengan sebuah sesi
files = client.beta.files.list(
    scope_id="sesn_abc123",
    betas=["managed-agents-2026-04-01"],
)
for f in files:
    print(f.id, f.filename)

# Unduh sebuah file
content = client.beta.files.download(files.data[0].id)
content.write_to_file("output.txt")
```

```typescript TypeScript nocheck
// Daftar file yang terkait dengan sebuah sesi
const files = await client.beta.files.list({
  scope_id: "sesn_abc123",
  betas: ["managed-agents-2026-04-01"]
});
for (const f of files.data) {
  console.log(f.id, f.filename);
}

// Unduh sebuah file
const content = await client.beta.files.download(files.data[0].id);
await content.writeToFile("output.txt");
```

```csharp C# nocheck
// Mencantumkan file yang terkait dengan sebuah sesi
var files = await client.Beta.Files.List(new FileListParams
{
    ScopeID = "sesn_abc123",
    Betas = ["managed-agents-2026-04-01"],
});

// Mengunduh sebuah file
byte[] content = await client.Beta.Files.Download(files.Data[0].ID);
await File.WriteAllBytesAsync("output.txt", content);
```

```go Go nocheck
// Daftar file yang terkait dengan sebuah sesi
files, err := client.Beta.Files.List(ctx, anthropic.BetaFileListParams{
	ScopeID: anthropic.String("sesn_abc123"),
	Betas:   []anthropic.AnthropicBeta{"managed-agents-2026-04-01"},
})
if err != nil {
	panic(err)
}

// Unduh sebuah file
resp, err := client.Beta.Files.Download(ctx, files.Data[0].ID, anthropic.BetaFileDownloadParams{})
if err != nil {
	panic(err)
}
defer resp.Body.Close()
fileContent, err := io.ReadAll(resp.Body)
if err != nil {
	panic(err)
}
if err := os.WriteFile("output.txt", fileContent, 0644); err != nil {
	panic(err)
}
```

```java Java nocheck
// Daftar file yang terkait dengan sebuah sesi
var files = client.beta().files().list(FileListParams.builder()
    .scopeId("sesn_abc123")
    .addBeta(AnthropicBeta.of("managed-agents-2026-04-01"))
    .build());

// Unduh sebuah file
try (HttpResponse response = client.beta().files().download(files.data().get(0).id())) {
    try (InputStream body = response.body()) {
        Files.copy(body, Path.of("output.txt"), StandardCopyOption.REPLACE_EXISTING);
    }
}
```

```php PHP nocheck
// Menampilkan daftar file yang terkait dengan sebuah sesi
$files = $client->beta->files->list(
    scopeID: 'sesn_abc123',
    betas: ['managed-agents-2026-04-01'],
);

// Mengunduh file
$content = $client->beta->files->download($files->data[0]->id);
file_put_contents('output.txt', $content);
```

```ruby Ruby nocheck
# Daftar file yang terkait dengan sebuah sesi
files = client.beta.files.list(
  scope_id: "sesn_abc123",
  betas: ["managed-agents-2026-04-01"]
)

# Unduh sebuah file
content = client.beta.files.download(files.data[0].id)
File.binwrite("output.txt", content.read)
```
</CodeGroup>

## Tipe file yang didukung \{#supported-file-types}

Agen dapat bekerja dengan tipe file apa pun, termasuk:

- Kode sumber (`.py`, `.js`, `.ts`, `.go`, `.rs`, dan lainnya)
- File data (`.csv`, `.json`, `.xml`, `.yaml`)
- Dokumen (`.txt`, `.md`)
- Arsip (`.zip`, `.tar.gz`) - agen dapat mengekstraknya menggunakan bash
- File biner - agen dapat memprosesnya dengan alat yang sesuai

## Path file \{#file-paths}

<Note>
File yang dipasang di sandbox adalah salinan read-only. Agen dapat membacanya tetapi tidak dapat memodifikasi file asli yang diunggah. Untuk bekerja dengan versi yang dimodifikasi, agen menulis ke path baru di dalam sandbox.
</Note>

- File dipasang pada path persis yang Anda tentukan
- Direktori induk dibuat secara otomatis
- Path harus absolut (dimulai dengan `/`)