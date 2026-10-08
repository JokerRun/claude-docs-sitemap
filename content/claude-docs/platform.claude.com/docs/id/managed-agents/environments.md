---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/environments
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: cc11775d88f0f62f1efdf7b1196a9d2ea88830434d7d2fd09ff3d60a96cd0149
---

---
title: Penyiapan environment cloud
url: https://platform.claude.com/docs/id/managed-agents/environments
description: Sesuaikan sandbox cloud untuk sesi Anda.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Environment (lingkungan) mendefinisikan konfigurasi sandbox tempat agen Anda berjalan. Anda membuat environment satu kali, lalu mereferensikan ID-nya setiap kali Anda memulai sesi. Beberapa sesi dapat berbagi environment yang sama, tetapi setiap sesi mendapatkan sandbox terisolasinya sendiri (container Linux baru).

Halaman ini membahas environment `type: cloud`. Untuk menjalankan sandbox di infrastruktur Anda sendiri, lihat [Sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes).

## Membuat environment

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsS https://api.anthropic.com/v1/environments \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<'EOF'
  {
    "name": "python-dev",
    "config": {
      "type": "cloud",
      "networking": {"type": "limited", "allow_package_managers": true}
    }
  }
  EOF
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply environment.yaml
    ```

    <File filename="environment.yaml">
      ```yaml
      # yaml-language-server: $schema=https://platform.claude.com/schemas/ant/beta/environment.json
      name: python-dev
      config:
        type: cloud
        networking:
          type: limited
          allow_package_managers: true
      ```
    </File>

    [`ant apply`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply) membuat lingkungan dari `environment.yaml`, mencetak ID-nya, dan mencatatnya di `claude-lock.json`. Commit `claude-lock.json` agar `ant apply` berikutnya memperbarui lingkungan ini alih-alih mencoba membuatnya lagi.
  </CodeGroupItem>

  ```python Python
  environment = client.beta.environments.create(
      name="python-dev",
      config={
          "type": "cloud",
          "networking": {"type": "limited", "allow_package_managers": True},
      },
  )

  print(f"Environment ID: {environment.id}")
  ```

  ```typescript TypeScript
  const environment = await client.beta.environments.create({
    name: "python-dev",
    config: {
      type: "cloud",
      networking: { type: "limited", allow_package_managers: true },
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
          Networking = new BetaLimitedNetworkParams
          {
              AllowPackageManagers = true,
          },
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
  				OfLimited: &anthropic.BetaLimitedNetworkParams{
  					AllowPackageManagers: anthropic.Bool(true),
  				},
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
          .networking(BetaLimitedNetworkParams.builder()
              .allowPackageManagers(true)
              .build())
          .build())
      .build());
  IO.println("Environment ID: " + environment.id());
  ```

  ```php PHP
  $environment = $client->beta->environments->create(
      name: 'python-dev',
      config: [
          'type' => 'cloud',
          'networking' => ['type' => 'limited', 'allow_package_managers' => true],
      ],
  );
  echo "Environment ID: {$environment->id}\n";
  ```

  ```ruby Ruby
  environment = client.beta.environments.create(
    name: "python-dev",
    config: {
      type: "cloud",
      networking: {type: "limited", allow_package_managers: true}
    }
  )

  puts "Environment ID: #{environment.id}"
  ```
</CodeGroup>

Gunakan `name` yang unik dan deskriptif agar Anda dapat membedakan environment satu sama lain. Contoh ini menggunakan [jaringan](https://platform.claude.com/docs/id/managed-agents/environments#networking) `limited` dengan package manager diizinkan, sehingga sandbox dapat menjangkau registri paket dan host kode. Agar sandbox dapat menjangkau host lain, tambahkan host tersebut ke `allowed_hosts`.

## Menggunakan environment dalam sesi

Teruskan ID environment sebagai string saat [membuat sesi](https://platform.claude.com/docs/id/managed-agents/sessions).

<CodeGroup>
  ```bash cURL
  curl -fsS https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
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
  curl -fsS https://api.anthropic.com/v1/environments \
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
      "networking": {"type": "limited", "allow_package_managers": true}
    }
  }
  EOF
  ```

  <CodeGroupItem>
    ```bash CLI
    ant apply environment.yaml
    ```

    <File filename="environment.yaml">
      ```yaml
      # yaml-language-server: $schema=https://platform.claude.com/schemas/ant/beta/environment.json
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
          type: limited
          allow_package_managers: true
      ```
    </File>
  </CodeGroupItem>

  ```python Python
  environment = client.beta.environments.create(
      name="data-analysis",
      config={
          "type": "cloud",
          "packages": {
              "pip": ["pandas", "numpy", "scikit-learn"],
              "npm": ["express"],
          },
          "networking": {"type": "limited", "allow_package_managers": True},
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
      networking: { type: "limited", allow_package_managers: true }
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
          Networking = new BetaLimitedNetworkParams
          {
              AllowPackageManagers = true,
          },
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
  				OfLimited: &anthropic.BetaLimitedNetworkParams{
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
      .name("data-analysis")
      .config(BetaCloudConfigParams.builder()
          .packages(BetaPackagesParams.builder()
              .pip(List.of("pandas", "numpy", "scikit-learn"))
              .npm(List.of("express"))
              .build())
          .networking(BetaLimitedNetworkParams.builder()
              .allowPackageManagers(true)
              .build())
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
          'networking' => ['type' => 'limited', 'allow_package_managers' => true],
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
      networking: {type: "limited", allow_package_managers: true}
    }
  )
  ```
</CodeGroup>

Package manager yang didukung:

| Field   | Manajer paket          | Contoh                                      |
| ------- | ---------------------- | ------------------------------------------- |
| `apt`   | Paket sistem (apt-get) | `"graphviz"`                                |
| `cargo` | Rust (cargo)           | `"hyperfine@1.18.0"`                        |
| `gem`   | Ruby (gem)             | `"rails:7.1.0"`                             |
| `go`    | Modul Go               | `"golang.org/x/tools/cmd/goimports@latest"` |
| `npm`   | Node.js (npm)          | `"express@4.18.0"`                          |
| `pip`   | Python (pip)           | `"sqlalchemy==2.0.30"`                      |

### Jaringan

Field `networking` mengontrol akses jaringan keluar (outbound) sandbox.

Dengan jaringan `limited`, `allowed_hosts` juga berlaku untuk alat `web_search` dan `web_fetch`, yang berjalan di server Anthropic. Panggilan `web_fetch` untuk URL pada host yang tidak cocok dengan `allowed_hosts` mengembalikan hasil error kepada agen. `web_search` menghilangkan hasil dari host yang tidak cocok dengan `allowed_hosts`. `allow_package_managers` dan `allow_mcp_servers` tidak menambahkan host apa pun untuk alat-alat ini. Ketika `allowed_hosts` tidak mencantumkan host apa pun, tidak ada panggilan `web_fetch` atau `web_search` yang mengembalikan halaman atau hasil pencarian. Host yang Anda tambahkan ke `allowed_hosts` untuk alat-alat ini juga terbuka bagi sandbox. Jaringan `unrestricted` dan environment self-hosted tidak membatasi alat-alat ini. Untuk membatasinya lebih lanjut, atur `allowed_domains` atau `blocked_domains` pada entri alat di toolset agen. Lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions).

| Mode           | Deskripsi                                                                                                                                                                                                                                                       |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `limited`      | Membatasi akses jaringan sandbox ke host di `allowed_hosts`. Atur `allow_package_managers` dan `allow_mcp_servers` ke `true` untuk mengizinkan akses tambahan. Gunakan mode ini kecuali agen harus menjangkau situs yang tidak dapat Anda cantumkan sebelumnya. |
| `unrestricted` | Akses jaringan keluar penuh, kecuali untuk daftar blokir keamanan umum. Sebelum Anda menggunakannya, baca [Risiko jaringan tanpa batasan](https://platform.claude.com/docs/id/managed-agents/environments#risks-of-unrestricted-networking).                    |

<Note>
  Atur `networking` secara eksplisit dalam permintaan API; permintaan pembuatan yang menghilangkannya akan mendapatkan `unrestricted`. Formulir Claude Console untuk membuat environment dimulai dengan **Limited** terpilih dan tidak ada hal lain yang diizinkan.
</Note>

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

  <CodeGroupItem>
    ```bash CLI
    ant apply environment.yaml
    ```

    <File filename="environment.yaml">
      ```yaml
      # yaml-language-server: $schema=https://platform.claude.com/schemas/ant/beta/environment.json
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
  </CodeGroupItem>

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
  Gunakan jaringan `limited` dengan daftar `allowed_hosts` yang eksplisit. Ikuti prinsip hak akses minimum (least privilege) dengan hanya memberikan akses jaringan minimum yang dibutuhkan agen Anda, dan audit domain yang diizinkan secara berkala.
</Info>

Dengan jaringan `limited` dan tanpa field lain yang diatur, tidak ada host yang diizinkan. File, memory store, dan repositori GitHub yang Anda lampirkan ke sesi tetap tersedia. Ketika permintaan dari sandbox pada port 80 atau 443 ditolak karena host-nya tidak diizinkan, responsnya adalah 403 yang menyebutkan host yang diblokir.

Saat menggunakan jaringan `limited`:

* `allowed_hosts` menentukan domain yang dapat dijangkau sandbox. Tentukan hostname saja atau pola wildcard (seperti `*.example.com`). Jangan sertakan skema URL, port, atau path. Hostname tanpa wildcard hanya cocok dengan host yang persis sama: `example.com` tidak cocok dengan `www.example.com`. `*.example.com` cocok dengan setiap subdomain dari `example.com`, tetapi tidak dengan `example.com` itu sendiri.
* `allow_mcp_servers` mengizinkan akses keluar ke endpoint server MCP yang dikonfigurasi pada agen, di luar yang tercantum dalam array `allowed_hosts`. Default-nya `false`. Selama nilainya `false`, pembuatan sesi gagal dengan error 400 jika agen mendeklarasikan server MCP yang host-nya tidak ada di `allowed_hosts`. Hal yang sama berlaku untuk [agen yang dapat menerima delegasi tugas darinya](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration). Untuk memperbaikinya, tambahkan host ke `allowed_hosts` atau atur `allow_mcp_servers` ke `true`.
* `allow_package_managers` mengizinkan akses keluar ke sekumpulan registri paket publik dan host kode di luar yang tercantum dalam array `allowed_hosts`. Lihat [Host package manager](https://platform.claude.com/docs/id/managed-agents/environments#package-manager-hosts) untuk daftarnya. Default-nya `false`. Atur ke `true` setiap kali environment menentukan `packages`; jika tidak, permintaan akan ditolak dengan error 400, bahkan jika host registri tercantum di `allowed_hosts`.

#### Host package manager

Ketika `allow_package_managers` bernilai `true`, sandbox dapat menjangkau host berikut selain yang ada di `allowed_hosts`. Anthropic memelihara daftar ini dan dapat mengubahnya.

| Ekosistem    | Host                                                                                                                                                                                       |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Hosting kode | `github.com`, `api.github.com`, `codeload.github.com`, `raw.githubusercontent.com`, `objects.githubusercontent.com`, `release-assets.githubusercontent.com`, `gitlab.com`, `bitbucket.org` |
| Node.js      | `registry.npmjs.org`, `registry.yarnpkg.com`, `nodejs.org`                                                                                                                                 |
| Python       | `pypi.org`, `files.pythonhosted.org`                                                                                                                                                       |
| Rust         | `crates.io`, `index.crates.io`, `static.crates.io`, `static.rust-lang.org`                                                                                                                 |
| Go           | `proxy.golang.org`, `sum.golang.org`                                                                                                                                                       |
| Java         | `repo1.maven.org`, `repo.maven.apache.org`, `services.gradle.org`, `plugins.gradle.org`, `plugins-artifacts.gradle.org`                                                                    |
| Ruby         | `rubygems.org`, `index.rubygems.org`                                                                                                                                                       |
| PHP          | `packagist.org`, `repo.packagist.org`                                                                                                                                                      |
| Ubuntu (apt) | `archive.ubuntu.com`, `security.ubuntu.com`, `ppa.launchpad.net`                                                                                                                           |
| Container    | `registry-1.docker.io`, `auth.docker.io`, `production.cloudflare.docker.com`, `download.docker.com`, `ghcr.io`                                                                             |

<Warning>
  Akses jaringan diberikan per host, bukan per operasi. Sandbox dapat mengirim permintaan apa pun ke host yang diizinkan, termasuk unggahan seperti `git push` dan publikasi paket, dengan kredensial apa pun yang diberikan oleh perintah. Jika agen memproses input yang tidak tepercaya (file repositori, konten web yang diambil, atau output alat pihak ketiga), prompt injection yang berhasil dapat menggunakan host yang diizinkan untuk menyalin file keluar dari sandbox. Untuk mengurangi risiko ini, atur [kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) alat `bash` ke `always_ask` atau `auto`. Jika environment tidak menentukan `packages`, sebagai gantinya Anda dapat membiarkan `allow_package_managers` tetap bernilai `false` dan hanya mencantumkan host yang dibutuhkan agen Anda di `allowed_hosts`.
</Warning>

#### Risiko jaringan tanpa batasan

Dengan jaringan `unrestricted`, kode di sandbox dapat mengirim permintaan ke host mana pun di internet, kecuali host yang ada di daftar blokir keamanan umum. Sebelum Anda memilih mode ini, pertimbangkan apa yang dapat dilakukan agen dengan akses tersebut:

* **Agen dapat mengubah hal-hal di situs eksternal, tidak hanya membacanya:** Alat `bash` dapat mengirim permintaan apa pun. Agen dapat mengirim data, mengirimkan formulir, memanggil API, dan menjalankan skrip yang mengubah data di situs eksternal. Bahkan permintaan yang hanya mengambil URL dapat mengubah data di beberapa situs.
* **Tidak ada yang menjeda permintaan ini secara default:** [Kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) default toolset agen adalah `always_allow`, sehingga perintah `bash` berjalan tanpa persetujuan.
* **Apa pun di sandbox dapat keluar darinya:** Ini termasuk file, output alat, dan kredensial atau rahasia apa pun yang Anda masukkan ke sandbox.
* **Konten yang diambil dapat mengarahkan agen:** Halaman web, respons API, dan konten lain yang dibaca agen dapat berisi instruksi (prompt injection) yang mengubah apa yang dilakukannya selanjutnya.
* **Agen bertindak atas nama Anda:** Tindakannya dapat melanggar ketentuan layanan suatu situs, atau membuat akun dan catatan di sana.
* **Perilaku model bukanlah kontrol keamanan:** Agen dapat bertindak di situs eksternal dengan cara yang tidak Anda minta, termasuk mencoba ulang dengan cara berbeda setelah situs memblokir permintaan. Gunakan pengaturan jaringan dan kebijakan izin untuk membatasi apa yang dapat dilakukannya.
* **Daftar blokir keamanan bukanlah daftar izin (allowlist):** Daftar ini tidak membatasi situs lain mana yang dijangkau agen, atau apa yang dilakukan agen di situs tersebut.

Untuk mengurangi risiko ini, gunakan jaringan `limited` dengan daftar host yang eksplisit. Nilai `networking` berikut mengizinkan `api.example.com`, ditambah [host package manager](https://platform.claude.com/docs/id/managed-agents/environments#package-manager-hosts) untuk agen yang memasang paket:

```json
{
  "type": "limited",
  "allowed_hosts": ["api.example.com"],
  "allow_package_managers": true
}
```

Agen yang hanya menggunakan alat `web_search` dan `web_fetch` tidak memerlukan jaringan `unrestricted` jika Anda dapat mencantumkan situs yang dibutuhkannya. Dengan jaringan `limited`, `allowed_hosts` juga berlaku untuk alat-alat tersebut (lihat [Jaringan](https://platform.claude.com/docs/id/managed-agents/environments#networking)), jadi cantumkan situs-situs tersebut di `allowed_hosts`. Mencantumkannya juga di `allowed_domains` milik `web_search` membuatnya mencari di situs-situs tersebut. Host yang Anda tambahkan ke `allowed_hosts` juga terbuka bagi sandbox. Untuk membatasi alat-alat tersebut lebih lanjut, lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions).

Gunakan `unrestricted` hanya ketika agen harus menjangkau situs yang tidak dapat Anda cantumkan sebelumnya. Dalam hal ini, jauhkan rahasia dan file sensitif dari sandbox, dan berikan agen hanya kredensial yang dibutuhkan tugas tersebut. Pertimbangkan untuk mengatur kebijakan izin alat `bash` ke `always_ask` atau `auto`, dan [pantau event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming).

## Siklus hidup environment

* Environment tetap ada hingga diarsipkan atau dihapus secara eksplisit.
* Setiap sesi mendapatkan instance sandbox-nya sendiri, bahkan ketika beberapa sesi mereferensikan environment yang sama. Sesi tidak berbagi state filesystem.
* Environment tidak memiliki versi. Jika Anda sering memperbarui environment, simpan catatan perubahan Anda sendiri agar Anda dapat mengetahui konfigurasi mana yang digunakan setiap sesi.

## Mengelola environment

<CodeGroup>
  ```bash cURL
  # Daftar environment
  curl -fsS https://api.anthropic.com/v1/environments \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"

  # Ambil environment tertentu
  curl -fsS "https://api.anthropic.com/v1/environments/$ENVIRONMENT_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"

  # Arsipkan environment (hanya-baca, sesi yang ada tetap berjalan)
  curl -fsS -X POST "https://api.anthropic.com/v1/environments/$ENVIRONMENT_ID/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"

  # Hapus environment (hanya jika tidak ada sesi yang mereferensikannya)
  curl -fsS -X DELETE "https://api.anthropic.com/v1/environments/$ENVIRONMENT_ID" \
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
