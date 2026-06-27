---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/environments
fetched_at: 2026-06-27T03:14:28.973816Z
sha256: 7b19929f463c5f7540f06875d8f821aae69780f6630f9d50e6c7952d16d2b3cf
---

# Penyiapan lingkungan cloud

Sesuaikan sandbox cloud untuk sesi Anda.

---

Lingkungan (environment) mendefinisikan konfigurasi sandbox tempat agen Anda berjalan. Anda membuat lingkungan satu kali, lalu mereferensikan ID-nya setiap kali Anda memulai sesi. Beberapa sesi dapat berbagi lingkungan yang sama, tetapi setiap sesi mendapatkan sandbox terisolasinya sendiri (kontainer Linux yang baru).

Halaman ini membahas lingkungan dengan `type: cloud`. Untuk menjalankan sandbox pada infrastruktur Anda sendiri, lihat [Sandbox yang di-host sendiri](/docs/id/managed-agents/self-hosted-sandboxes).

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Membuat lingkungan \{#create-an-environment}

<CodeGroup defaultLanguage="CLI">
  
````bash
environment=$(curl -fsS https://api.anthropic.com/v1/environments \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  --data @- <<'EOF'
{
  "name": "python-dev",
  "config": {
    "type": "cloud",
    "networking": {"type": "unrestricted"}
  }
}
EOF
)
environment_id=$(jq -r '.id' <<< "$environment")

echo "Environment ID: $environment_id"
````

  
````bash
ant beta:environments create \
  --name "python-dev" \
  --config '{type: cloud, networking: {type: unrestricted}}'
````

  
````python
environment = client.beta.environments.create(
    name="python-dev",
    config={
        "type": "cloud",
        "networking": {"type": "unrestricted"},
    },
)

print(f"Environment ID: {environment.id}")
````

  
````typescript
const environment = await client.beta.environments.create({
  name: "python-dev",
  config: {
    type: "cloud",
    networking: { type: "unrestricted" },
  },
});

console.log(`Environment ID: ${environment.id}`);
````

  
````csharp
var environment = await client.Beta.Environments.Create(new()
{
    Name = "python-dev",
    Config = new BetaCloudConfigParams
    {
        Networking = new BetaUnrestrictedNetwork(),
    },
});

Console.WriteLine($"Environment ID: {environment.ID}");
````

  
````go
environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
	Name: "python-dev",
	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
		OfCloud: &anthropic.BetaCloudConfigParams{
			Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
				OfUnrestricted: &anthropic.BetaUnrestrictedNetworkParam{},
			},
		},
	},
})
if err != nil {
	panic(err)
}

fmt.Printf("Environment ID: %s\n", environment.ID)
````

  
````java
var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
    .name("python-dev")
    .config(BetaCloudConfigParams.builder()
        .networking(BetaUnrestrictedNetwork.builder().build())
        .build())
    .build());
IO.println("Environment ID: " + environment.id());
````

  
````php
$environment = $client->beta->environments->create(
    name: 'python-dev',
    config: ['type' => 'cloud', 'networking' => ['type' => 'unrestricted']],
);
echo "Environment ID: {$environment->id}\n";
````

  
````ruby
environment = client.beta.environments.create(
  name: "python-dev",
  config: {
    type: "cloud",
    networking: {type: "unrestricted"}
  }
)

puts "Environment ID: #{environment.id}"
````

</CodeGroup>

`name` harus unik dalam organisasi dan workspace Anda.

## Menggunakan lingkungan dalam sesi \{#use-the-environment-in-a-session}

Berikan ID lingkungan sebagai string saat [membuat sesi](/docs/id/managed-agents/sessions).

<CodeGroup>
  
````bash
session=$(curl -fsS https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  --data @- <<EOF
{
  "agent": "$agent_id",
  "environment_id": "$environment_id"
}
EOF
)
````

  
````python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
)
````

  
````typescript
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
});
````

  
````csharp
var session = await client.Beta.Sessions.Create(new()
{
    Agent = agent.ID,
    EnvironmentID = environment.ID,
});
````

  
````go
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfString: anthropic.String(agent.ID),
	},
	EnvironmentID: environment.ID,
})
if err != nil {
	panic(err)
}
````

  
````java
var session = client.beta().sessions().create(SessionCreateParams.builder()
    .agent(agent.id())
    .environmentId(environment.id())
    .build());
````

  
````php
$session = $client->beta->sessions->create(
    agent: $agent->id,
    environmentID: $environment->id,
);
````

  
````ruby
session = client.beta.sessions.create(
  agent: agent.id,
  environment_id: environment.id
)
````

</CodeGroup>

## Opsi konfigurasi \{#configuration-options}

### Paket \{#packages}

Field `packages` melakukan pra-instalasi paket ke dalam sandbox sebelum agen dimulai. Paket diinstal oleh package manager masing-masing dan di-cache di seluruh sesi yang berbagi lingkungan yang sama. Ketika beberapa package manager ditentukan, mereka dijalankan dalam urutan alfabetis (apt, cargo, gem, go, npm, pip). Anda dapat secara opsional menyematkan versi tertentu; default-nya adalah versi terbaru.

<CodeGroup defaultLanguage="CLI">
```bash curl
environment=$(curl -fsS https://api.anthropic.com/v1/environments \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  --data @- <<'EOF'
{
  "name": "data-analysis",
  "config": {
    "type": "cloud",
    "packages": {
      "pip": ["pandas", "numpy", "scikit-learn"],
      "npm": ["express"]
    },
    "networking": {"type": "unrestricted"}
  }
}
EOF
)
```

```bash CLI
ant beta:environments create <<'YAML'
name: data-analysis
config:
  type: cloud
  packages:
    pip:
      - pandas
      - numpy
      - scikit-learn
    npm:
      - express
  networking:
    type: unrestricted
YAML
```

```python Python
environment = client.beta.environments.create(
    name="data-analysis",
    config={
        "type": "cloud",
        "packages": {
            "pip": ["pandas", "numpy", "scikit-learn"],
            "npm": ["express"],
        },
        "networking": {"type": "unrestricted"},
    },
)
```

```typescript TypeScript
const environment = await client.beta.environments.create({
  name: "data-analysis",
  config: {
    type: "cloud",
    packages: {
      pip: ["pandas", "numpy", "scikit-learn"],
      npm: ["express"]
    },
    networking: { type: "unrestricted" }
  }
});
```

```csharp C#
var environment = await client.Beta.Environments.Create(new()
{
    Name = "data-analysis",
    Config = new BetaCloudConfigParams
    {
        Packages = new()
        {
            Pip = ["pandas", "numpy", "scikit-learn"],
            Npm = ["express"],
        },
        Networking = new BetaUnrestrictedNetwork(),
    },
});
```

```go Go
environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
	Name: "data-analysis",
	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
		OfCloud: &anthropic.BetaCloudConfigParams{
			Packages: anthropic.BetaPackagesParams{
				Pip: []string{"pandas", "numpy", "scikit-learn"},
				Npm: []string{"express"},
			},
			Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
				OfUnrestricted: &anthropic.BetaUnrestrictedNetworkParam{},
			},
		},
	},
})
if err != nil {
	panic(err)
}
_ = environment
```

```java Java
var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
    .name("data-analysis")
    .config(BetaCloudConfigParams.builder()
        .packages(BetaPackagesParams.builder()
            .pip(List.of("pandas", "numpy", "scikit-learn"))
            .npm(List.of("express"))
            .build())
        .networking(BetaUnrestrictedNetwork.builder().build())
        .build())
    .build());
```

```php PHP
$environment = $client->beta->environments->create(
    name: 'data-analysis',
    config: [
        'type' => 'cloud',
        'packages' => [
            'pip' => ['pandas', 'numpy', 'scikit-learn'],
            'npm' => ['express'],
        ],
        'networking' => ['type' => 'unrestricted'],
    ],
);
```

```ruby Ruby
environment = client.beta.environments.create(
  name: "data-analysis",
  config: {
    type: "cloud",
    packages: {
      pip: %w[pandas numpy scikit-learn],
      npm: %w[express]
    },
    networking: {type: "unrestricted"}
  }
)
```
</CodeGroup>

Package manager yang didukung:

| Field | Package manager | Contoh |
| --- | --- | --- |
| `apt` | Paket sistem (apt-get) | `"ffmpeg"` |
| `cargo` | Rust (cargo) | `"ripgrep@14.0.0"` |
| `gem` | Ruby (gem) | `"rails:7.1.0"` |
| `go` | Modul Go | `"golang.org/x/tools/cmd/goimports@latest"` |
| `npm` | Node.js (npm) | `"express@4.18.0"` |
| `pip` | Python (pip) | `"pandas==2.2.0"` |

### Jaringan \{#networking}

Field `networking` mengontrol akses jaringan keluar dari sandbox. Ini tidak memengaruhi domain yang diizinkan untuk alat `web_search` atau `web_fetch`.

| Mode | Deskripsi |
| --- | --- |
| `unrestricted` | Akses jaringan keluar penuh, kecuali untuk daftar blokir keamanan umum. Ini adalah default. |
| `limited` | Membatasi akses jaringan sandbox ke daftar `allowed_hosts`. Akses lebih lanjut diaktifkan melalui bool `allow_package_managers` dan `allow_mcp_servers`.|

<CodeGroup>
```bash curl
config=$(cat <<'EOF'
{
  "type": "cloud",
  "networking": {
    "type": "limited",
    "allowed_hosts": ["api.example.com"],
    "allow_mcp_servers": true,
    "allow_package_managers": true
  }
}
EOF
)
```

```python Python
config = {
    "type": "cloud",
    "networking": {
        "type": "limited",
        "allowed_hosts": ["api.example.com"],
        "allow_mcp_servers": True,
        "allow_package_managers": True,
    },
}
```

```typescript TypeScript
const config = {
  type: "cloud",
  networking: {
    type: "limited",
    allowed_hosts: ["api.example.com"],
    allow_mcp_servers: true,
    allow_package_managers: true
  }
};
```

```csharp C#
var config = new BetaCloudConfigParams
{
    Networking = new BetaLimitedNetworkParams
    {
        AllowedHosts = ["api.example.com"],
        AllowMcpServers = true,
        AllowPackageManagers = true,
    },
};
```

```go Go
config := anthropic.BetaCloudConfigParams{
	Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
		OfLimited: &anthropic.BetaLimitedNetworkParams{
			AllowedHosts:         []string{"api.example.com"},
			AllowMCPServers:      anthropic.Bool(true),
			AllowPackageManagers: anthropic.Bool(true),
		},
	},
}
_ = config
```

```java Java
var config = BetaCloudConfigParams.builder()
    .networking(BetaLimitedNetworkParams.builder()
        .allowedHosts(List.of("api.example.com"))
        .allowMcpServers(true)
        .allowPackageManagers(true)
        .build())
    .build();
```

```php PHP
$config = [
    'type' => 'cloud',
    'networking' => [
        'type' => 'limited',
        'allowed_hosts' => ['api.example.com'],
        'allow_mcp_servers' => true,
        'allow_package_managers' => true,
    ],
];
```

```ruby Ruby
config = {
  type: "cloud",
  networking: {
    type: "limited",
    allowed_hosts: %w[api.example.com],
    allow_mcp_servers: true,
    allow_package_managers: true
  }
}
```
</CodeGroup>

<Info>
Untuk deployment produksi, gunakan jaringan `limited` dengan daftar `allowed_hosts` yang eksplisit. Ikuti prinsip hak istimewa minimum (least privilege) dengan hanya memberikan akses jaringan minimum yang dibutuhkan agen Anda, dan audit domain yang diizinkan secara berkala.
</Info>

Saat menggunakan jaringan `limited`:
- `allowed_hosts` menentukan domain yang dapat dijangkau oleh sandbox. Tentukan hostname biasa atau pola wildcard (seperti `*.example.com`); jangan sertakan skema URL.
- `allow_mcp_servers` mengizinkan akses keluar ke endpoint server MCP yang dikonfigurasi pada agen, di luar yang tercantum dalam array `allowed_hosts`. Default-nya adalah `false`.
- `allow_package_managers` mengizinkan akses keluar ke registri paket publik (seperti PyPI dan npm) di luar yang tercantum dalam array `allowed_hosts`. Default-nya adalah `false`.

## Siklus hidup lingkungan \{#environment-lifecycle}

- Lingkungan tetap ada hingga diarsipkan atau dihapus secara eksplisit.
- Beberapa sesi dapat mereferensikan lingkungan yang sama.
- Setiap sesi mendapatkan instance sandbox-nya sendiri. Sesi tidak berbagi state sistem file.
- Lingkungan tidak memiliki versi. Jika Anda sering memperbarui lingkungan Anda, Anda mungkin ingin mencatat pembaruan ini di sisi Anda, untuk memetakan state lingkungan dengan sesi.

## Mengelola lingkungan \{#manage-environments}

<CodeGroup defaultLanguage="CLI">
  
````bash
# Daftar environment
environments=$(curl -fsS https://api.anthropic.com/v1/environments \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01")

# Ambil environment tertentu
env=$(curl -fsS "https://api.anthropic.com/v1/environments/$environment_id" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01")

# Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
curl -fsS -X POST "https://api.anthropic.com/v1/environments/$environment_id/archive" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"

# Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
curl -fsS -X DELETE "https://api.anthropic.com/v1/environments/$environment_id" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
# List environments
ant beta:environments list

# Retrieve a specific environment
ant beta:environments retrieve --environment-id "$ENVIRONMENT_ID"

# Archive an environment (read-only, existing sessions continue)
ant beta:environments archive --environment-id "$ENVIRONMENT_ID"

# Delete an environment (only if no sessions reference it)
ant beta:environments delete --environment-id "$ENVIRONMENT_ID"
````

  
````python
# Daftar environment
environments = client.beta.environments.list()

# Ambil environment tertentu
env = client.beta.environments.retrieve(environment.id)

# Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
client.beta.environments.archive(environment.id)

# Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
client.beta.environments.delete(environment.id)
````

  
````typescript
// Daftar environment
const environments = await client.beta.environments.list();

// Ambil environment tertentu
const env = await client.beta.environments.retrieve(environment.id);

// Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
await client.beta.environments.archive(environment.id);

// Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
await client.beta.environments.delete(environment.id);
````

  
````csharp
// Daftar environment
var environments = await client.Beta.Environments.List();

// Ambil environment tertentu
var env = await client.Beta.Environments.Retrieve(environment.ID);

// Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
await client.Beta.Environments.Archive(environment.ID);

// Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
await client.Beta.Environments.Delete(environment.ID);
````

  
````go
// Daftar environment
environments, err := client.Beta.Environments.List(ctx, anthropic.BetaEnvironmentListParams{})
if err != nil {
	panic(err)
}

// Ambil environment tertentu
env, err := client.Beta.Environments.Get(ctx, environment.ID, anthropic.BetaEnvironmentGetParams{})
if err != nil {
	panic(err)
}

// Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
_, err = client.Beta.Environments.Archive(ctx, environment.ID, anthropic.BetaEnvironmentArchiveParams{})
if err != nil {
	panic(err)
}

// Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
_, err = client.Beta.Environments.Delete(ctx, environment.ID, anthropic.BetaEnvironmentDeleteParams{})
if err != nil {
	panic(err)
}
````

  
````java
// Daftar environment
var environments = client.beta().environments().list();
// Ambil environment tertentu
var env = client.beta().environments().retrieve(environment.id());
// Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
client.beta().environments().archive(environment.id());
// Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
client.beta().environments().delete(environment.id());
````

  
````php
// Daftar environment
$environments = $client->beta->environments->list();
// Ambil environment tertentu
$env = $client->beta->environments->retrieve($environment->id);
// Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
$client->beta->environments->archive($environment->id);
// Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
$client->beta->environments->delete($environment->id);
````

  
````ruby
# Daftar environment
environments = client.beta.environments.list

# Ambil environment tertentu
env = client.beta.environments.retrieve(environment.id)

# Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
client.beta.environments.archive(environment.id)

# Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
client.beta.environments.delete(environment.id)
````

</CodeGroup>

## Runtime yang sudah terinstal \{#pre-installed-runtimes}

Sandbox cloud menyertakan runtime umum secara bawaan. Lihat [Referensi sandbox](/docs/id/managed-agents/cloud-sandboxes-reference) untuk daftar lengkap bahasa, database, dan utilitas yang sudah terinstal.