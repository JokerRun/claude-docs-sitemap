---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/environments
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: dd9bd58188edab808fcf373a458fc538023e3a1fa0d0d7b7c28525a7107646df
---

---
title: Penyiapan environment cloud
url: https://platform.claude.com/docs/id/managed-agents/environments
description: Sesuaikan sandbox cloud untuk sesi Anda.
---

Environment (lingkungan) mendefinisikan konfigurasi sandbox tempat agen Anda berjalan. Anda membuat environment satu kali, lalu mereferensikan ID-nya setiap kali Anda memulai sesi. Beberapa sesi dapat berbagi environment yang sama, tetapi setiap sesi mendapatkan sandbox terisolasinya sendiri (container Linux baru).

Halaman ini membahas environment `type: cloud`. Untuk menjalankan sandbox di infrastruktur Anda sendiri, lihat [Sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes).

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK menetapkan header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Membuat environment

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
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

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:environments create < python-dev.environment.yaml
    ```

    <File filename="python-dev.environment.yaml">
      ```yaml
      name: python-dev
      config:
        type: cloud
        networking:
          type: unrestricted
      ```
    </File>
  </MultiFileExample>

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

Gunakan `name` yang unik dan deskriptif agar Anda dapat membedakan environment satu dengan lainnya.

## Menggunakan environment dalam sesi

Teruskan ID environment sebagai string saat [membuat sesi](https://platform.claude.com/docs/id/managed-agents/sessions).

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
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
  ant beta:sessions create --agent "$AGENT_ID" --environment-id "$ENVIRONMENT_ID"
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

Field `packages` melakukan pra-instalasi paket ke dalam sandbox sebelum agen dimulai. Paket diinstal oleh package manager masing-masing dan di-cache di seluruh sesi yang berbagi environment yang sama. Ketika beberapa package manager ditentukan, mereka dijalankan dalam urutan alfabetis (apt, cargo, gem, go, npm, pip). Anda dapat secara opsional mengunci versi tertentu. Paket yang tidak dikunci akan menginstal versi terbaru. Jika environment menggunakan [jaringan](https://platform.claude.com/docs/id/managed-agents/environments#networking) `limited`, atur juga `networking.allow_package_managers` ke `true`; jika tidak, permintaan akan ditolak dengan error 400.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
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

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:environments create < environment.yaml
    ```

    <File filename="environment.yaml">
      ```yaml
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
      ```
    </File>
  </MultiFileExample>

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
  using Anthropic.Models.Beta.Environments;

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
  import com.anthropic.models.beta.environments.*;
  import java.util.List;

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
| `apt`   | Paket sistem (apt-get) | `"graphviz"`                                |
| `cargo` | Rust (cargo)           | `"hyperfine@1.18.0"`                        |
| `gem`   | Ruby (gem)             | `"rails:7.1.0"`                             |
| `go`    | Modul Go               | `"golang.org/x/tools/cmd/goimports@latest"` |
| `npm`   | Node.js (npm)          | `"express@4.18.0"`                          |
| `pip`   | Python (pip)           | `"sqlalchemy==2.0.30"`                      |

### Jaringan

Field `networking` mengontrol akses jaringan keluar dari sandbox. Field ini tidak memengaruhi alat `web_search` atau `web_fetch`, yang berjalan di server Anthropic; untuk membatasi situs yang dapat dijangkau alat-alat tersebut, atur `allowed_domains` atau `blocked_domains` pada entri alat tersebut di toolset agen. Lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools#restrict-web-search-and-web-fetch-domains).

| Mode           | Deskripsi                                                                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `unrestricted` | Akses jaringan keluar penuh, kecuali untuk blocklist keamanan umum. Ini adalah default.                                                                                 |
| `limited`      | Membatasi akses jaringan sandbox ke host yang ada di `allowed_hosts`. Atur `allow_package_managers` dan `allow_mcp_servers` ke `true` untuk mengizinkan akses tambahan. |

Contoh berikut membuat environment dengan jaringan `limited`:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
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

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:environments create < environment.yaml
    ```

    <File filename="environment.yaml">
      ```yaml
      name: api-access
      config:
        type: cloud
        networking:
          type: limited
          allowed_hosts:
            - api.example.com
          allow_mcp_servers: true
          allow_package_managers: true
      ```
    </File>
  </MultiFileExample>

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
  using Anthropic.Models.Beta.Environments;

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
  import com.anthropic.models.beta.environments.*;
  import java.util.List;

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
  Untuk deployment produksi, gunakan jaringan `limited` dengan daftar `allowed_hosts` yang eksplisit. Ikuti prinsip hak akses minimum (least privilege) dengan hanya memberikan akses jaringan minimum yang dibutuhkan agen Anda, dan audit domain yang diizinkan secara berkala.
</Info>

Saat menggunakan jaringan `limited`:

* `allowed_hosts` menentukan domain yang dapat dijangkau sandbox. Tentukan hostname saja atau pola wildcard (seperti `*.example.com`). Jangan sertakan skema URL, port, atau path.
* `allow_mcp_servers` mengizinkan akses keluar ke endpoint server MCP yang dikonfigurasi pada agen, di luar yang tercantum dalam array `allowed_hosts`. Default-nya `false`.
* `allow_package_managers` mengizinkan akses keluar ke registry paket publik (seperti PyPI dan npm) di luar yang tercantum dalam array `allowed_hosts`. Default-nya `false`. Atur ke `true` setiap kali environment menentukan `packages`; jika tidak, permintaan akan ditolak dengan error 400, bahkan jika host registry tercantum dalam `allowed_hosts`.

## Siklus hidup environment

* Environment tetap ada hingga diarsipkan atau dihapus secara eksplisit.
* Setiap sesi mendapatkan instance sandbox-nya sendiri, bahkan ketika beberapa sesi mereferensikan environment yang sama. Sesi tidak berbagi state filesystem.
* Environment tidak memiliki versi. Jika Anda sering memperbarui environment, simpan catatan perubahan Anda sendiri agar Anda dapat mengetahui konfigurasi mana yang digunakan setiap sesi.

## Mengelola environment

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
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

## Runtime pra-instal

Sandbox cloud sudah menyertakan runtime bahasa umum, database, dan alat command-line secara bawaan. Lihat [Referensi sandbox cloud](https://platform.claude.com/docs/id/managed-agents/cloud-sandboxes-reference) untuk daftar lengkapnya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi sandbox cloud" icon="book" href="https://platform.claude.com/docs/id/managed-agents/cloud-sandboxes-reference">
    Paket, database, dan utilitas pra-instal yang tersedia di sandbox cloud.
  </Card>

  <Card title="Memulai sesi" icon="play" href="https://platform.claude.com/docs/id/managed-agents/sessions">
    Buat sesi untuk menjalankan agen Anda dan mulai menjalankan tugas.
  </Card>
</CardGroup>
