---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/environments
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: b7d45cfe4815ac5548d6ebbab6e7523f6e3bfcd8e1e62ae425ba0f2ac3e6eacc
---

# Penyiapan lingkungan cloud

Sesuaikan kontainer cloud untuk sesi Anda.

---

Lingkungan mendefinisikan konfigurasi kontainer tempat agen Anda berjalan. Anda membuat lingkungan sekali, kemudian mereferensikan ID-nya setiap kali Anda memulai sesi. Beberapa sesi dapat berbagi lingkungan yang sama, tetapi setiap sesi mendapatkan instans kontainer terisolasi sendiri.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis.
</Note>

## Buat lingkungan

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
    Config = new()
    {
        Networking = new UnrestrictedNetwork(),
    },
});

Console.WriteLine($"Environment ID: {environment.ID}");
````

  
````go
environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
	Name: "python-dev",
	Config: anthropic.BetaCloudConfigParams{
		Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
			OfUnrestricted: &anthropic.UnrestrictedNetworkParam{},
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
        .networking(UnrestrictedNetwork.builder().build())
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

`name` harus unik dalam organisasi dan ruang kerja Anda.

## Gunakan lingkungan dalam sesi

Teruskan ID lingkungan sebagai string saat membuat sesi.

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

## Opsi konfigurasi

### Paket

Bidang `packages` pra-menginstal paket ke dalam kontainer sebelum agen dimulai. Paket diinstal oleh manajer paket masing-masing dan di-cache di seluruh sesi yang berbagi lingkungan yang sama. Ketika beberapa manajer paket ditentukan, mereka berjalan dalam urutan abjad (apt, cargo, gem, go, npm, pip). Anda dapat secara opsional menyematkan versi spesifik; defaultnya adalah terbaru.

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
    Config = new()
    {
        Packages = new()
        {
            Pip = ["pandas", "numpy", "scikit-learn"],
            Npm = ["express"],
        },
        Networking = new UnrestrictedNetwork(),
    },
});
```

```go Go
environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
	Name: "data-analysis",
	Config: anthropic.BetaCloudConfigParams{
		Packages: anthropic.BetaPackagesParams{
			Pip: []string{"pandas", "numpy", "scikit-learn"},
			Npm: []string{"express"},
		},
		Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
			OfUnrestricted: &anthropic.UnrestrictedNetworkParam{},
		},
	},
})
if err != nil {
	panic(err)
}
```

```java Java
var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
    .name("data-analysis")
    .config(BetaCloudConfigParams.builder()
        .packages(BetaPackagesParams.builder()
            .pip(List.of("pandas", "numpy", "scikit-learn"))
            .npm(List.of("express"))
            .build())
        .networking(UnrestrictedNetwork.builder().build())
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

Manajer paket yang didukung:

| Bidang | Manajer paket | Contoh |
| --- | --- | --- |
| `apt` | Paket sistem (apt-get) | `"ffmpeg"` |
| `cargo` | Rust (cargo) | `"ripgrep@14.0.0"` |
| `gem` | Ruby (gem) | `"rails:7.1.0"` |
| `go` | Modul Go | `"golang.org/x/tools/cmd/goimports@latest"` |
| `npm` | Node.js (npm) | `"express@4.18.0"` |
| `pip` | Python (pip) | `"pandas==2.2.0"` |

### Jaringan

Bidang `networking` mengontrol akses jaringan keluar kontainer. Ini tidak memengaruhi domain yang diizinkan oleh alat `web_search` atau `web_fetch`.

| Mode | Deskripsi |
| --- | --- |
| `unrestricted` | Akses jaringan keluar penuh, kecuali untuk daftar pemblokiran keamanan umum. Ini adalah default. |
| `limited` | Membatasi akses jaringan kontainer ke daftar `allowed_hosts`. Akses lebih lanjut diaktifkan melalui bool `allow_package_managers` dan `allow_mcp_servers`. |

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
Untuk penerapan produksi, gunakan jaringan `limited` dengan daftar `allowed_hosts` eksplisit. Ikuti prinsip hak istimewa minimal dengan memberikan hanya akses jaringan minimum yang diperlukan agen Anda, dan audit domain yang diizinkan secara teratur.
</Info>

Saat menggunakan jaringan `limited`:
- `allowed_hosts` menentukan domain yang dapat dijangkau kontainer. Ini harus diawali dengan HTTPS.
- `allow_mcp_servers` memungkinkan akses keluar ke titik akhir server MCP yang dikonfigurasi pada agen, di luar yang tercantum dalam array `allowed_hosts`. Default ke `false`.
- `allow_package_managers` memungkinkan akses keluar ke registri paket publik (PyPI, npm, dll.) di luar yang tercantum dalam array `allowed_hosts`. Default ke `false`.

## Siklus hidup lingkungan

- Lingkungan bertahan sampai secara eksplisit diarsipkan atau dihapus.
- Beberapa sesi dapat mereferensikan lingkungan yang sama.
- Setiap sesi mendapatkan instans kontainer sendiri. Sesi tidak berbagi status sistem file.
- Lingkungan tidak diversi. Jika Anda sering memperbarui lingkungan Anda, Anda mungkin ingin mencatat pembaruan ini di sisi Anda, untuk memetakan status lingkungan dengan sesi.

## Kelola lingkungan

<CodeGroup defaultLanguage="CLI">
  
````bash
# List environments
environments=$(curl -fsS https://api.anthropic.com/v1/environments \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01")

# Retrieve a specific environment
env=$(curl -fsS "https://api.anthropic.com/v1/environments/$environment_id" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01")

# Archive an environment (read-only, existing sessions continue)
curl -fsS -X POST "https://api.anthropic.com/v1/environments/$environment_id/archive" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"

# Delete an environment (only if no sessions reference it)
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
# List environments
environments = client.beta.environments.list()

# Retrieve a specific environment
env = client.beta.environments.retrieve(environment.id)

# Archive an environment (read-only, existing sessions continue)
client.beta.environments.archive(environment.id)

# Delete an environment (only if no sessions reference it)
client.beta.environments.delete(environment.id)
````

  
````typescript
// List environments
const environments = await client.beta.environments.list();

// Retrieve a specific environment
const env = await client.beta.environments.retrieve(environment.id);

// Archive an environment (read-only, existing sessions continue)
await client.beta.environments.archive(environment.id);

// Delete an environment (only if no sessions reference it)
await client.beta.environments.delete(environment.id);
````

  
````csharp
// List environments
var environments = await client.Beta.Environments.List();

// Retrieve a specific environment
var env = await client.Beta.Environments.Retrieve(environment.ID);

// Archive an environment (read-only, existing sessions continue)
await client.Beta.Environments.Archive(environment.ID);

// Delete an environment (only if no sessions reference it)
await client.Beta.Environments.Delete(environment.ID);
````

  
````go
// List environments
environments, err := client.Beta.Environments.List(ctx, anthropic.BetaEnvironmentListParams{})
if err != nil {
	panic(err)
}

// Retrieve a specific environment
env, err := client.Beta.Environments.Get(ctx, environment.ID, anthropic.BetaEnvironmentGetParams{})
if err != nil {
	panic(err)
}

// Archive an environment (read-only, existing sessions continue)
_, err = client.Beta.Environments.Archive(ctx, environment.ID, anthropic.BetaEnvironmentArchiveParams{})
if err != nil {
	panic(err)
}

// Delete an environment (only if no sessions reference it)
_, err = client.Beta.Environments.Delete(ctx, environment.ID, anthropic.BetaEnvironmentDeleteParams{})
if err != nil {
	panic(err)
}
````

  
````java
// List environments
var environments = client.beta().environments().list();
// Retrieve a specific environment
var env = client.beta().environments().retrieve(environment.id());
// Archive an environment (read-only, existing sessions continue)
client.beta().environments().archive(environment.id());
// Delete an environment (only if no sessions reference it)
client.beta().environments().delete(environment.id());
````

  
````php
// List environments
$environments = $client->beta->environments->list();
// Retrieve a specific environment
$env = $client->beta->environments->retrieve($environment->id);
// Archive an environment (read-only, existing sessions continue)
$client->beta->environments->archive($environment->id);
// Delete an environment (only if no sessions reference it)
$client->beta->environments->delete($environment->id);
````

  
````ruby
# List environments
environments = client.beta.environments.list

# Retrieve a specific environment
env = client.beta.environments.retrieve(environment.id)

# Archive an environment (read-only, existing sessions continue)
client.beta.environments.archive(environment.id)

# Delete an environment (only if no sessions reference it)
client.beta.environments.delete(environment.id)
````

</CodeGroup>

## Runtime pra-instal

Kontainer cloud menyertakan runtime umum di luar kotak. Lihat [Referensi Kontainer](/docs/id/managed-agents/cloud-containers) untuk daftar lengkap bahasa, database, dan utilitas yang pra-diinstal.