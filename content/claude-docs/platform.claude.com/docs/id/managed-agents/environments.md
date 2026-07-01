---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/environments
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: ffb3ad842e684f0d6834964904b58db04dab790eeebccfb142c053ca3e763be3
---

# Penyiapan lingkungan cloud

Sesuaikan sandbox cloud untuk sesi Anda.

---

Lingkungan mendefinisikan konfigurasi sandbox tempat agen Anda berjalan. Anda membuat lingkungan satu kali, lalu mereferensikan ID-nya setiap kali Anda memulai sesi. Beberapa sesi dapat berbagi lingkungan yang sama, tetapi setiap sesi mendapatkan sandbox terisolasinya sendiri (kontainer Linux yang baru).

Halaman ini membahas lingkungan `type: cloud`. Untuk menjalankan sandbox pada infrastruktur Anda sendiri, lihat [Sandbox yang di-host sendiri](/docs/id/managed-agents/self-hosted-sandboxes).

<Note>
  Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Membuat lingkungan

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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
  ```

  ```bash CLI
  ant beta:environments create \
    --name "python-dev" \
    --config '{type: cloud, networking: {type: unrestricted}}'
  ```

  ```python Python
  environment = client.beta.environments.create(
      name="python-dev",
      config={
          "type": "cloud",
          "networking": {"type": "unrestricted"},
      },
  )

  print(f"Environment ID: {environment.id}")
  ```

  ```typescript TypeScript
  const environment = await client.beta.environments.create({
    name: "python-dev",
    config: {
      type: "cloud",
      networking: { type: "unrestricted" },
    },
  });

  console.log(`Environment ID: ${environment.id}`);
  ```

  ```csharp C#
  var environment = await client.Beta.Environments.Create(new()
  {
      Name = "python-dev",
      Config = new BetaCloudConfigParams
      {
          Networking = new BetaUnrestrictedNetwork(),
      },
  });

  Console.WriteLine($"Environment ID: {environment.ID}");
  ```

  ```go Go
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
  ```

  ```java Java
  var environment = client.beta().environments().create(EnvironmentCreateParams.builder()
      .name("python-dev")
      .config(BetaCloudConfigParams.builder()
          .networking(BetaUnrestrictedNetwork.builder().build())
          .build())
      .build());
  IO.println("Environment ID: " + environment.id());
  ```

  ```php PHP
  $environment = $client->beta->environments->create(
      name: 'python-dev',
      config: ['type' => 'cloud', 'networking' => ['type' => 'unrestricted']],
  );
  echo "Environment ID: {$environment->id}\n";
  ```

  ```ruby Ruby
  environment = client.beta.environments.create(
    name: "python-dev",
    config: {
      type: "cloud",
      networking: {type: "unrestricted"}
    }
  )

  puts "Environment ID: #{environment.id}"
  ```
</CodeGroup>

Gunakan `name` yang unik dan deskriptif agar Anda dapat membedakan antar lingkungan.

## Menggunakan lingkungan dalam sesi

Teruskan ID lingkungan sebagai string saat [membuat sesi](/docs/id/managed-agents/sessions).

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID"
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id
  )
  ```
</CodeGroup>

## Opsi konfigurasi

### Paket

Field `packages` melakukan pra-instalasi paket ke dalam sandbox sebelum agen dimulai. Paket diinstal oleh package manager masing-masing dan di-cache di seluruh sesi yang berbagi lingkungan yang sama. Ketika beberapa package manager ditentukan, mereka dijalankan dalam urutan alfabetis (apt, cargo, gem, go, npm, pip). Anda dapat secara opsional menyematkan versi tertentu. Paket yang tidak disematkan akan menginstal versi terbaru.

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

| Field   | Package manager        | Contoh                                      |
| ------- | ---------------------- | ------------------------------------------- |
| `apt`   | Paket sistem (apt-get) | `"ffmpeg"`                                  |
| `cargo` | Rust (cargo)           | `"ripgrep@14.0.0"`                          |
| `gem`   | Ruby (gem)             | `"rails:7.1.0"`                             |
| `go`    | Modul Go               | `"golang.org/x/tools/cmd/goimports@latest"` |
| `npm`   | Node.js (npm)          | `"express@4.18.0"`                          |
| `pip`   | Python (pip)           | `"pandas==2.2.0"`                           |

### Jaringan

Field `networking` mengontrol akses jaringan keluar dari sandbox. Field ini tidak memengaruhi domain yang diizinkan untuk alat `web_search` atau `web_fetch`.

| Mode           | Deskripsi                                                                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `unrestricted` | Akses jaringan keluar penuh, kecuali untuk daftar blokir keamanan umum. Ini adalah default.                                                                             |
| `limited`      | Membatasi akses jaringan sandbox ke host yang ada di `allowed_hosts`. Atur `allow_package_managers` dan `allow_mcp_servers` ke `true` untuk mengizinkan akses tambahan. |

Contoh berikut membuat lingkungan dengan jaringan `limited`:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -fsS https://api.anthropic.com/v1/environments \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "api-access",
      "config": {
        "type": "cloud",
        "networking": {
          "type": "limited",
          "allowed_hosts": ["api.example.com"],
          "allow_mcp_servers": true,
          "allow_package_managers": true
        }
      }
    }'
  ```

  ```bash CLI
  ant beta:environments create <<'YAML'
  name: api-access
  config:
    type: cloud
    networking:
      type: limited
      allowed_hosts:
        - api.example.com
      allow_mcp_servers: true
      allow_package_managers: true
  YAML
  ```

  ```python Python
  environment = client.beta.environments.create(
      name="api-access",
      config={
          "type": "cloud",
          "networking": {
              "type": "limited",
              "allowed_hosts": ["api.example.com"],
              "allow_mcp_servers": True,
              "allow_package_managers": True,
          },
      },
  )
  ```

  ```typescript TypeScript
  const environment = await client.beta.environments.create({
    name: "api-access",
    config: {
      type: "cloud",
      networking: {
        type: "limited",
        allowed_hosts: ["api.example.com"],
        allow_mcp_servers: true,
        allow_package_managers: true
      }
    }
  });
  ```

  ```csharp C#
  var environment = await client.Beta.Environments.Create(new()
  {
      Name = "api-access",
      Config = new BetaCloudConfigParams
      {
          Networking = new BetaLimitedNetworkParams
          {
              AllowedHosts = ["api.example.com"],
              AllowMcpServers = true,
              AllowPackageManagers = true,
          },
      },
  });
  ```

  ```go Go
  environment, err := client.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
  	Name: "api-access",
  	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
  		OfCloud: &anthropic.BetaCloudConfigParams{
  			Networking: anthropic.BetaCloudConfigParamsNetworkingUnion{
  				OfLimited: &anthropic.BetaLimitedNetworkParams{
  					AllowedHosts:         []string{"api.example.com"},
  					AllowMCPServers:      anthropic.Bool(true),
  					AllowPackageManagers: anthropic.Bool(true),
  				},
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
      .name("api-access")
      .config(BetaCloudConfigParams.builder()
          .networking(BetaLimitedNetworkParams.builder()
              .allowedHosts(List.of("api.example.com"))
              .allowMcpServers(true)
              .allowPackageManagers(true)
              .build())
          .build())
      .build());
  ```

  ```php PHP
  $environment = $client->beta->environments->create(
      name: 'api-access',
      config: [
          'type' => 'cloud',
          'networking' => [
              'type' => 'limited',
              'allowed_hosts' => ['api.example.com'],
              'allow_mcp_servers' => true,
              'allow_package_managers' => true,
          ],
      ],
  );
  ```

  ```ruby Ruby
  environment = client.beta.environments.create(
    name: "api-access",
    config: {
      type: "cloud",
      networking: {
        type: "limited",
        allowed_hosts: %w[api.example.com],
        allow_mcp_servers: true,
        allow_package_managers: true
      }
    }
  )
  ```
</CodeGroup>

<Info>
  Untuk deployment produksi, gunakan jaringan `limited` dengan daftar `allowed_hosts` yang eksplisit. Ikuti prinsip hak istimewa paling rendah (least privilege) dengan hanya memberikan akses jaringan minimum yang dibutuhkan agen Anda, dan audit domain yang diizinkan secara berkala.
</Info>

Saat menggunakan jaringan `limited`:

* `allowed_hosts` menentukan domain yang dapat dijangkau oleh sandbox. Tentukan hostname biasa atau pola wildcard (seperti `*.example.com`). Jangan sertakan skema URL, port, atau path.
* `allow_mcp_servers` mengizinkan akses keluar ke endpoint server MCP yang dikonfigurasi pada agen, di luar yang tercantum dalam array `allowed_hosts`. Default-nya adalah `false`.
* `allow_package_managers` mengizinkan akses keluar ke registri paket publik (seperti PyPI dan npm) di luar yang tercantum dalam array `allowed_hosts`. Default-nya adalah `false`.

## Siklus hidup lingkungan

* Lingkungan tetap ada hingga diarsipkan atau dihapus secara eksplisit.
* Setiap sesi mendapatkan instance sandbox-nya sendiri, bahkan ketika beberapa sesi mereferensikan lingkungan yang sama. Sesi tidak berbagi state filesystem.
* Lingkungan tidak memiliki versi. Jika Anda sering memperbarui lingkungan, simpan catatan perubahan Anda sendiri agar Anda dapat mengetahui konfigurasi mana yang digunakan setiap sesi.

## Mengelola lingkungan

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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
  ```

  ```bash CLI
  # Daftar environment
  ant beta:environments list

  # Ambil environment tertentu
  ant beta:environments retrieve --environment-id "$ENVIRONMENT_ID"

  # Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
  ant beta:environments archive --environment-id "$ENVIRONMENT_ID"

  # Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
  ant beta:environments delete --environment-id "$ENVIRONMENT_ID"
  ```

  ```python Python
  # Daftar environment
  environments = client.beta.environments.list()

  # Ambil environment tertentu
  env = client.beta.environments.retrieve(environment.id)

  # Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
  client.beta.environments.archive(environment.id)

  # Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
  client.beta.environments.delete(environment.id)
  ```

  ```typescript TypeScript
  // Daftar environment
  const environments = await client.beta.environments.list();

  // Ambil environment tertentu
  const env = await client.beta.environments.retrieve(environment.id);

  // Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
  await client.beta.environments.archive(environment.id);

  // Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
  await client.beta.environments.delete(environment.id);
  ```

  ```csharp C#
  // Daftar environment
  var environments = await client.Beta.Environments.List();

  // Ambil environment tertentu
  var env = await client.Beta.Environments.Retrieve(environment.ID);

  // Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
  await client.Beta.Environments.Archive(environment.ID);

  // Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
  await client.Beta.Environments.Delete(environment.ID);
  ```

  ```go Go
  // Daftar environment
  environments, err := client.Beta.Environments.List(ctx, anthropic.BetaEnvironmentListParams{})
  // ...

  // Ambil environment tertentu
  env, err := client.Beta.Environments.Get(ctx, environment.ID, anthropic.BetaEnvironmentGetParams{})
  // ...

  // Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
  _, err = client.Beta.Environments.Archive(ctx, environment.ID, anthropic.BetaEnvironmentArchiveParams{})
  // ...

  // Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
  _, err = client.Beta.Environments.Delete(ctx, environment.ID, anthropic.BetaEnvironmentDeleteParams{})
  ```

  ```java Java
  // Daftar environment
  var environments = client.beta().environments().list();
  // Ambil environment tertentu
  var env = client.beta().environments().retrieve(environment.id());
  // Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
  client.beta().environments().archive(environment.id());
  // Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
  client.beta().environments().delete(environment.id());
  ```

  ```php PHP
  // Daftar environment
  $environments = $client->beta->environments->list();
  // Ambil environment tertentu
  $env = $client->beta->environments->retrieve($environment->id);
  // Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
  $client->beta->environments->archive($environment->id);
  // Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
  $client->beta->environments->delete($environment->id);
  ```

  ```ruby Ruby
  # Daftar environment
  environments = client.beta.environments.list

  # Ambil environment tertentu
  env = client.beta.environments.retrieve(environment.id)

  # Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
  client.beta.environments.archive(environment.id)

  # Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
  client.beta.environments.delete(environment.id)
  ```
</CodeGroup>

## Runtime yang sudah terinstal

Sandbox cloud menyertakan runtime umum secara bawaan. Lihat [Referensi sandbox cloud](/docs/id/managed-agents/cloud-sandboxes-reference) untuk daftar lengkap bahasa, database, dan utilitas yang sudah terinstal.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi sandbox cloud" icon="book" href="/docs/id/managed-agents/cloud-sandboxes-reference">
    Paket, database, dan utilitas yang sudah terinstal dan tersedia di sandbox cloud.
  </Card>

  <Card title="Memulai sesi" icon="play" href="/docs/id/managed-agents/sessions">
    Buat sesi untuk menjalankan agen Anda dan mulai menjalankan tugas.
  </Card>
</CardGroup>
