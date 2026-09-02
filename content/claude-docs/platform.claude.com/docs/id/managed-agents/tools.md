---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/tools
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: f9f01bc3da6439a49dd51c4fb88e2e21dfcf0b6a1b1c34b073a0ea0e1d16da69
---

---
title: Alat
url: https://platform.claude.com/docs/id/managed-agents/tools
description: Konfigurasikan alat yang tersedia untuk agen Anda.
---

Claude Managed Agents menyediakan serangkaian alat bawaan yang dapat digunakan Claude secara otonom di dalam sebuah [sesi](https://platform.claude.com/docs/id/managed-agents/sessions). Anda mengontrol alat mana yang tersedia dengan menentukannya dalam konfigurasi agen.

Claude Managed Agents juga mendukung alat kustom yang didefinisikan pengguna. Aplikasi Anda mengeksekusi alat-alat ini secara terpisah dan mengembalikan hasilnya ke Claude, yang menggunakannya untuk melanjutkan tugas. Untuk memberi agen alat dari server MCP, gunakan [konektor MCP](https://platform.claude.com/docs/id/managed-agents/mcp-connector) sebagai gantinya.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK menetapkan header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Alat yang tersedia

Toolset agen mencakup alat-alat berikut. Semuanya diaktifkan secara default ketika Anda menyertakan toolset dalam konfigurasi agen Anda. Setiap entri dalam array `configs` diidentifikasi berdasarkan `name`-nya, menggunakan nilai pada kolom Nama, dan menerima field `type` opsional dengan nilai yang sama. Entri `web_search` dan `web_fetch` menerima pengaturan tambahan; lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools#restrict-web-search-and-web-fetch-domains).

| Alat       | Nama         | Deskripsi                                             |
| ---------- | ------------ | ----------------------------------------------------- |
| Bash       | `bash`       | Mengeksekusi perintah bash dalam sesi shell           |
| Read       | `read`       | Membaca file dari filesystem sandbox                  |
| Write      | `write`      | Menulis file ke filesystem sandbox                    |
| Edit       | `edit`       | Melakukan penggantian string dalam sebuah file        |
| Glob       | `glob`       | Pencocokan pola file yang cepat menggunakan pola glob |
| Grep       | `grep`       | Pencarian teks menggunakan pola regex                 |
| Web fetch  | `web_fetch`  | Mengambil konten dari sebuah URL                      |
| Web search | `web_search` | Mencari informasi di web                              |

Ketika output alat melebihi 100.000 karakter (sekitar 25.000 token), output tersebut secara otomatis ditulis ke sebuah file di [sandbox](https://platform.claude.com/docs/id/managed-agents/environments). Model menerima pratinjau terpotong beserta path file dan dapat membaca konten lengkapnya dari sana.

## Mengonfigurasi toolset

Aktifkan toolset lengkap dengan `agent_toolset_20260401` saat membuat agen. Gunakan array `configs` untuk menonaktifkan alat tertentu atau menimpa pengaturannya. Setiap entri config juga dapat menetapkan `permission_policy` yang mengontrol apakah panggilan alat tersebut disetujui otomatis atau memerlukan konfirmasi. Lihat [Kebijakan izin](https://platform.claude.com/docs/id/managed-agents/permission-policies) untuk jenis kebijakan yang tersedia.

Entri config untuk `web_search` dan `web_fetch` juga menerima filter domain dan pengaturan web lainnya; lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools#restrict-web-search-and-web-fetch-domains).

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "Coding Assistant",
    "model": "claude-opus-5",
    "tools": [
      {
        "type": "agent_toolset_20260401",
        "configs": [
          {"name": "web_fetch", "enabled": false}
        ]
      }
    ]
  }
  EOF
  )
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Coding Assistant
  model: claude-opus-5
  tools:
    - type: agent_toolset_20260401
      configs:
        - name: web_fetch
          enabled: false
  YAML
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Coding Assistant",
      model="claude-opus-5",
      tools=[
          {
              "type": "agent_toolset_20260401",
              "configs": [
                  {"name": "web_fetch", "enabled": False},
              ],
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Coding Assistant",
    model: "claude-opus-5",
    tools: [
      {
        type: "agent_toolset_20260401",
        configs: [{ name: "web_fetch", enabled: false }]
      }
    ]
  });
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Agents;

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = new("claude-opus-5"),
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
              Configs =
              [
                  new BetaManagedAgentsWebFetchToolConfigParams { Enabled = false },
              ],
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Coding Assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-5",
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			Configs: []anthropic.BetaManagedAgentsAgentToolConfigParamsUnion{{
  				OfWebFetch: &anthropic.BetaManagedAgentsWebFetchToolConfigParams{
  					Enabled: anthropic.Bool(false),
  				},
  			}},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  _ = agent
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;

  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("Coding Assistant")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
      .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
          .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
          .addConfig(BetaManagedAgentsWebFetchToolConfigParams.builder()
              .enabled(false)
              .build())
          .build())
      .build());
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsWebFetchToolConfigParams;

  $agent = $client->beta->agents->create(
      name: 'Coding Assistant',
      model: 'claude-opus-5',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
              configs: [
                  BetaManagedAgentsWebFetchToolConfigParams::with(enabled: false),
              ],
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Coding Assistant",
    model: "claude-opus-5",
    tools: [
      {
        type: :agent_toolset_20260401,
        configs: [
          {name: :web_fetch, enabled: false}
        ]
      }
    ]
  )
  ```
</CodeGroup>

### Menonaktifkan alat tertentu

Untuk menonaktifkan sebuah alat, tetapkan `enabled: false` pada entri config-nya di objek toolset dalam array `tools` agen Anda:

```json
{
  "type": "agent_toolset_20260401",
  "configs": [
    { "name": "web_fetch", "enabled": false },
    { "name": "web_search", "enabled": false }
  ]
}
```

### Mengaktifkan hanya alat tertentu

Objek `default_config` menetapkan baseline untuk setiap alat dalam set, dan entri `configs` per alat menimpanya. Untuk memulai dengan semuanya nonaktif dan hanya mengaktifkan yang Anda butuhkan, tetapkan `default_config.enabled` ke `false`:

```json
{
  "type": "agent_toolset_20260401",
  "default_config": { "enabled": false },
  "configs": [
    { "name": "bash", "enabled": true },
    { "name": "read", "enabled": true },
    { "name": "write", "enabled": true }
  ]
}
```

### Membatasi domain web search dan web fetch

Untuk mengontrol situs mana yang dapat dijangkau oleh alat web agen, tetapkan `allowed_domains` (alat hanya dapat menjangkau host ini) atau `blocked_domains` (alat tidak pernah dapat menjangkau host ini) pada entri `web_search` dan `web_fetch` dalam array `configs` toolset. Setiap alat memiliki daftarnya sendiri, sehingga `web_search` dan `web_fetch` dapat memiliki pembatasan yang berbeda. Domain yang terdaftar mencakup host tersebut dan semua subdomainnya. Saat runtime, panggilan `web_fetch` untuk URL yang tidak diizinkan oleh daftarnya mengembalikan hasil error ke agen (`is_error: true` pada event `agent.tool_result`, dengan konten yang menyebutkan kode error `url_not_allowed`), dan `web_search` menghilangkan hasil yang tidak diizinkan oleh daftarnya.

Toolset berikut membatasi `web_search` ke dua situs dan melokalkan hasilnya, serta memblokir satu host untuk `web_fetch` sambil membatasi seberapa banyak konten yang diambil masuk ke dalam konteks:

```json
{
  "type": "agent_toolset_20260401",
  "configs": [
    {
      "type": "web_search",
      "name": "web_search",
      "allowed_domains": ["docs.example.com", "arxiv.org"],
      "user_location": {
        "type": "approximate",
        "country": "US",
        "timezone": "America/Los_Angeles"
      }
    },
    {
      "type": "web_fetch",
      "name": "web_fetch",
      "blocked_domains": ["ads.example.com"],
      "max_content_tokens": 50000
    }
  ]
}
```

<Note>
  Dalam SDK Python, TypeScript, Go, Java, C#, Ruby, dan PHP, setiap entri `configs` memiliki tipe per alat: sebuah union dengan satu anggota per alat bawaan, yang dibedakan berdasarkan `type`. `type` bersifat opsional saat Anda membuat entri (server menyimpulkannya dari `name`) dan selalu ada pada respons. Pengetikan ini tidak mengubah JSON hasil serialisasi entri, sehingga permintaan yang entrinya hanya menetapkan `name`, `enabled`, dan `permission_policy` valid dengan atau tanpa `type`. Dalam SDK tempat Anda membuat entri dari nilai bertipe alih-alih dictionary atau hash biasa (Go, Java, C#, dan PHP), tipe elemen `configs` adalah union itu sendiri: buat setiap entri dari tipe anggota per alatnya.
</Note>

Permintaan berikut membuat agen dengan toolset ini dan mencetak array `configs` dari respons:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "Research Agent",
    "model": "claude-opus-5",
    "tools": [
      {
        "type": "agent_toolset_20260401",
        "configs": [
          {
            "type": "web_search",
            "name": "web_search",
            "allowed_domains": ["docs.example.com", "arxiv.org"],
            "user_location": {
              "type": "approximate",
              "country": "US",
              "timezone": "America/Los_Angeles"
            }
          },
          {
            "type": "web_fetch",
            "name": "web_fetch",
            "blocked_domains": ["ads.example.com"],
            "max_content_tokens": 50000
          }
        ]
      }
    ]
  }
  EOF
  )
  jq '.tools[0].configs' <<< "$agent"
  ```

  ```bash CLI
  ant beta:agents create --transform tools.0.configs <<'YAML'
  name: Research Agent
  model: claude-opus-5
  tools:
    - type: agent_toolset_20260401
      configs:
        - type: web_search
          name: web_search
          allowed_domains: [docs.example.com, arxiv.org]
          user_location:
            type: approximate
            country: US
            timezone: America/Los_Angeles
        - type: web_fetch
          name: web_fetch
          blocked_domains: [ads.example.com]
          max_content_tokens: 50000
  YAML
  ```

  ```python Python
  client = Anthropic()

  agent = client.beta.agents.create(
      name="Research Agent",
      model="claude-opus-5",
      tools=[
          {
              "type": "agent_toolset_20260401",
              "configs": [
                  {
                      "name": "web_search",
                      "allowed_domains": ["docs.example.com", "arxiv.org"],
                      "user_location": {
                          "type": "approximate",
                          "country": "US",
                          "timezone": "America/Los_Angeles",
                      },
                  },
                  {
                      "name": "web_fetch",
                      "blocked_domains": ["ads.example.com"],
                      "max_content_tokens": 50_000,
                  },
              ],
          }
      ],
  )

  for tool in agent.tools:
      if tool.type == "agent_toolset_20260401":
          print(json.dumps([config.to_dict() for config in tool.configs], indent=2))
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const agent = await client.beta.agents.create({
    name: "Research Agent",
    model: "claude-opus-5",
    tools: [
      {
        type: "agent_toolset_20260401",
        configs: [
          {
            name: "web_search",
            allowed_domains: ["docs.example.com", "arxiv.org"],
            user_location: {
              type: "approximate",
              country: "US",
              timezone: "America/Los_Angeles"
            }
          },
          {
            name: "web_fetch",
            blocked_domains: ["ads.example.com"],
            max_content_tokens: 50_000
          }
        ]
      }
    ]
  });

  for (const tool of agent.tools) {
    if (tool.type === "agent_toolset_20260401") {
      console.log(JSON.stringify(tool.configs, null, 2));
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Agents;

  AnthropicClient client = new();

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Research Agent",
      Model = BetaManagedAgentsModel.ClaudeOpus5,
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
              Configs =
              [
                  new BetaManagedAgentsWebSearchToolConfigParams
                  {
                      AllowedDomains = ["docs.example.com", "arxiv.org"],
                      UserLocation = new()
                      {
                          Country = "US",
                          Timezone = "America/Los_Angeles",
                      },
                  },
                  new BetaManagedAgentsWebFetchToolConfigParams
                  {
                      BlockedDomains = ["ads.example.com"],
                      MaxContentTokens = 50_000,
                  },
              ],
          },
      ],
  });

  JsonSerializerOptions jsonOptions = new() { WriteIndented = true };
  foreach (var tool in agent.Tools)
  {
      if (tool.TryPickBetaManagedAgentsAgentToolset20260401(out var toolset))
      {
          Console.WriteLine(JsonSerializer.Serialize(toolset.Configs, jsonOptions));
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Research Agent",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5,
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			Configs: []anthropic.BetaManagedAgentsAgentToolConfigParamsUnion{
  				{OfWebSearch: &anthropic.BetaManagedAgentsWebSearchToolConfigParams{
  					AllowedDomains: []string{"docs.example.com", "arxiv.org"},
  					UserLocation: anthropic.BetaManagedAgentsUserLocationParam{
  						Country:  anthropic.String("US"),
  						Timezone: anthropic.String("America/Los_Angeles"),
  					},
  				}},
  				{OfWebFetch: &anthropic.BetaManagedAgentsWebFetchToolConfigParams{
  					BlockedDomains:   []string{"ads.example.com"},
  					MaxContentTokens: anthropic.Int(50000),
  				}},
  			},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }

  for _, tool := range agent.Tools {
  	switch toolset := tool.AsAny().(type) {
  	case anthropic.BetaManagedAgentsAgentToolset20260401:
  		configs := make([]json.RawMessage, len(toolset.Configs))
  		for i, config := range toolset.Configs {
  			configs[i] = json.RawMessage(config.RawJSON())
  		}
  		output, err := json.MarshalIndent(configs, "", "  ")
  		if err != nil {
  			panic(err)
  		}
  		fmt.Println(string(output))
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.agents.AgentCreateParams;
  import com.anthropic.models.beta.agents.BetaManagedAgentsAgentToolset20260401Params;
  import com.anthropic.models.beta.agents.BetaManagedAgentsModel;
  import com.anthropic.models.beta.agents.BetaManagedAgentsUserLocation;
  import com.anthropic.models.beta.agents.BetaManagedAgentsWebFetchToolConfigParams;
  import com.anthropic.models.beta.agents.BetaManagedAgentsWebSearchToolConfigParams;

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      var agent = client.beta().agents().create(AgentCreateParams.builder()
          .name("Research Agent")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
          .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
              .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
              .addConfig(BetaManagedAgentsWebSearchToolConfigParams.builder()
                  .allowedDomains(List.of("docs.example.com", "arxiv.org"))
                  .userLocation(BetaManagedAgentsUserLocation.builder()
                      .country("US")
                      .timezone("America/Los_Angeles")
                      .build())
                  .build())
              .addConfig(BetaManagedAgentsWebFetchToolConfigParams.builder()
                  .blockedDomains(List.of("ads.example.com"))
                  .maxContentTokens(50_000)
                  .build())
              .build())
          .build());

      for (var tool : agent.tools()) {
          if (tool.isAgentToolset20260401()) {
              var configs = tool.asAgentToolset20260401().configs();
              IO.println(ObjectMappers.jsonMapper().valueToTree(configs));
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401;
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsUserLocation;
  use Anthropic\Beta\Agents\BetaManagedAgentsWebFetchToolConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsWebSearchToolConfigParams;
  // ...

  $client = new Client();

  $agent = $client->beta->agents->create(
      name: 'Research Agent',
      model: 'claude-opus-5',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
              configs: [
                  BetaManagedAgentsWebSearchToolConfigParams::with(
                      allowedDomains: ['docs.example.com', 'arxiv.org'],
                      userLocation: BetaManagedAgentsUserLocation::with(
                          country: 'US',
                          timezone: 'America/Los_Angeles',
                      ),
                  ),
                  BetaManagedAgentsWebFetchToolConfigParams::with(
                      blockedDomains: ['ads.example.com'],
                      maxContentTokens: 50_000,
                  ),
              ],
          ),
      ],
  );

  foreach ($agent->tools as $tool) {
      if ($tool instanceof BetaManagedAgentsAgentToolset20260401) {
          echo json_encode($tool->configs, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  agent = client.beta.agents.create(
    name: "Research Agent",
    model: "claude-opus-5",
    tools: [
      {
        type: :agent_toolset_20260401,
        configs: [
          {
            name: :web_search,
            allowed_domains: ["docs.example.com", "arxiv.org"],
            user_location: {type: :approximate, country: "US", timezone: "America/Los_Angeles"}
          },
          {
            name: :web_fetch,
            blocked_domains: ["ads.example.com"],
            max_content_tokens: 50_000
          }
        ]
      }
    ]
  )

  case agent.tools.first
  in Anthropic::Models::Beta::BetaManagedAgentsAgentToolset20260401 => toolset
    puts JSON.pretty_generate(toolset.configs.map(&:to_h))
  end
  ```
</CodeGroup>

Di Claude Console, tetapkan domain yang diizinkan atau diblokir dari baris `web_search` dan `web_fetch` pada kartu **Built-in tools** di formulir agen; tetapkan `max_content_tokens` dan `user_location` di tampilan **Raw** dari konfigurasi agen.

Selain `enabled` dan `permission_policy`, entri alat web menerima pengaturan berikut:

| Pengaturan           | Berlaku untuk             | Deskripsi                                                                                                                                                                                                                           |
| -------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed_domains`    | `web_search`, `web_fetch` | Satu-satunya host yang dapat dijangkau alat. Tidak dapat digabungkan dengan `blocked_domains` pada entri yang sama.                                                                                                                 |
| `blocked_domains`    | `web_search`, `web_fetch` | Host yang tidak dapat dijangkau alat.                                                                                                                                                                                               |
| `max_content_tokens` | `web_fetch`               | Membatasi jumlah konten halaman yang diambil yang disertakan dalam konteks. Harus berupa bilangan bulat positif. Lihat [batas konten](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#content-limits). |
| `user_location`      | `web_search`              | Melokalkan hasil pencarian. Sebuah objek dengan field yang sama seperti parameter [`user_location`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool#localization) Messages API.                       |

<Note>
  Pengaturan [`networking`](https://platform.claude.com/docs/id/managed-agents/environments#networking) sebuah environment mengontrol lalu lintas keluar milik sandbox itu sendiri. Pengaturan tersebut tidak memengaruhi `web_search` atau `web_fetch`, yang berjalan di server Anthropic baik environment tersebut berupa sandbox cloud maupun self-hosted. Daftar `allowed_domains` dan `blocked_domains` per alat adalah cara untuk membatasi apa yang dapat dijangkau alat-alat ini.
</Note>

<Note>
  Pengaturan web search dan web fetch tingkat organisasi di Claude Console berlaku untuk Messages API dan tidak berlaku untuk sesi Managed Agents. Untuk membatasi alat web sebuah agen, konfigurasikan `allowed_domains` atau `blocked_domains` pada toolset-nya sebagai gantinya.
</Note>

#### Aturan daftar domain

* Tetapkan `allowed_domains` atau `blocked_domains` pada sebuah entri, bukan keduanya. Entri yang menetapkan keduanya akan ditolak.
* Setiap daftar memuat 1 hingga 64 domain, masing-masing 1 hingga 255 karakter. Daftar kosong akan ditolak: untuk tidak menerapkan pembatasan, hilangkan field tersebut atau kirim `null`.
* Setiap domain adalah nama domain yang dapat didaftarkan, atau subdomain darinya, ditulis sebagai hostname biasa: huruf ASCII, angka, tanda hubung, garis bawah, dan titik, tanpa skema, port, kredensial, wildcard, atau spasi, tanpa label yang diawali atau diakhiri tanda hubung, dan tanpa path selain sufiks path `web_search` opsional yang dijelaskan nanti dalam daftar ini. Gunakan `example.com`, bukan `https://example.com`, `example.com:443`, atau `*.example.com`. Hostname dibandingkan tanpa memperhatikan huruf besar/kecil, dan satu `/` di akhir diabaikan.
* Domain yang terdaftar cocok dengan host tersebut dan subdomainnya: `example.com` mencakup `docs.example.com`, tetapi `docs.example.com` tidak mencakup `example.com` atau `api.example.com`. Awalan `www.` adalah subdomain seperti yang lainnya, sehingga `www.example.com` tidak mencakup `example.com`; daftarkan domain polos untuk mencakup keduanya.
* Alamat IP tidak diterima dalam bentuk apa pun, baik IPv4, IPv6, dalam kurung siku, maupun singkatan numerik seperti `127.1`. Daftarkan nama domain situs sebagai gantinya.
* Top-level domain polos atau sufiks registri seperti `com`, `co.uk`, atau `gov.uk` akan ditolak, begitu pula nama berlabel tunggal seperti `intranet`. Daftarkan domain lengkap seperti `example.co.uk`.
* `localhost` dan host yang berakhiran `.localhost`, `.local`, `.internal`, `.localdomain`, atau `.invalid` akan ditolak.
* Gunakan bentuk `xn--` (Punycode) untuk nama domain terinternasionalisasi; domain yang mengandung karakter non-ASCII akan ditolak.
* Domain `web_fetch` tidak dapat menyertakan path: gunakan `example.com`, bukan `example.com/*`. Domain `web_search` dapat membawa sufiks path seperti `example.com/blog`, di mana path tidak boleh mengandung spasi, `?`, `#`, atau karakter apa pun dari `$ , | ^ !`. Utamakan hostname biasa untuk `web_search` juga, karena penyedia pencarian mencocokkan sufiks path sebagai pola URL, bukan sebagai aturan host yang ketat.
* Domain duplikat dalam satu daftar akan ditolak. `www.example.com` dan `example.com` dihitung sebagai domain yang berbeda; lihat aturan pencocokan sebelumnya untuk mengetahui apa yang dicakup masing-masing.

#### Kapan pengaturan divalidasi

Pelanggaran format dan batas ditolak dengan 400 `invalid_request_error` saat Anda [membuat agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#create-an-agent) atau [memperbarui agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-an-agent), dan saat Anda membuat atau memperbarui sesi yang menyediakan `tools`. Misalnya, pesan untuk entri yang menetapkan kedua daftar menyertakan `Only one of allowed_domains or blocked_domains may be set.`, dan pesan untuk daftar kosong menyertakan `allowed_domains: Empty list of domains is ambiguous. Provide at least one domain or null.` Pesan untuk domain yang melanggar aturan format menyebutkan daftarnya dan posisi berbasis nol, misalnya `allowed_domains.0: IP addresses are not supported; provide a plain hostname like "example.com"`.

Permintaan yang sama juga menolak tiga pengaturan yang bergantung pada penyedia pencarian dan pengambilan: domain dalam `allowed_domains` yang tidak diizinkan untuk diakses oleh crawler Anthropic, `user_location.country` yang tidak didukung penyedia pencarian (pesannya diakhiri dengan `user_location.country: not a country the search provider supports`), dan `user_location.timezone` yang bukan nama IANA yang valid. Sesi memeriksa konfigurasi lagi saat pertama kali menginisialisasi alat; jika pengaturan yang sebelumnya diterima tidak lagi valid pada saat itu, sesi memancarkan event [`session.error`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) dan kembali ke `idle` tanpa mencoba ulang. Perbaiki pengaturan dengan [memperbarui alat sesi](https://platform.claude.com/docs/id/managed-agents/session-operations#updating-the-agent-configuration), perbarui juga agennya agar sesi baru dimulai dengan konfigurasi yang sudah diperbaiki, lalu kirim `user.message` baru untuk melanjutkan.

#### Sesi multiagen, outcome, dan pembaruan di tengah sesi

Dalam [sesi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), setiap daftar domain yang berlaku untuk sebuah thread ditegakkan secara bersamaan: agen dalam roster koordinator terikat oleh `allowed_domains` dan `blocked_domains` miliknya sendiri, oleh milik agen mana pun yang memanggilnya, dan oleh daftar koordinator saat ini.

* Allowlist digabungkan menjadi domain yang dicakup oleh semuanya, dan blocklist dijumlahkan, sehingga agen roster dapat mempersempit apa yang dijangkau alat tetapi tidak pernah memperluasnya. Misalnya, agen roster yang menetapkan `blocked_domains` mempertahankan `allowed_domains` koordinator dan memblokir host-host tersebut di dalamnya, dan agen roster yang menetapkan `allowed_domains` sendiri hanya dapat menjangkau host yang dicakup oleh daftarnya maupun daftar koordinator.
* Jika allowlist gabungan tidak memiliki domain yang sama, alat tetap tersedia bagi agen tersebut tetapi setiap panggilan gagal dengan error `url_not_allowed` yang menyatakan bahwa tidak ada domain yang diizinkan, dan deskripsi alat memberi tahu model demikian. Jaga agar allowlist setiap agen roster berada di dalam allowlist koordinator untuk menghindari hal ini.
* `max_content_tokens` dan `user_location` tidak digabungkan: sebuah thread menggunakan nilai dari konfigurasi alatnya sendiri jika ditetapkan, jika tidak dari agen yang memanggilnya, jika tidak dari konfigurasi koordinator saat ini.
* Entri roster `{"type": "self"}` tidak memiliki pengaturan web sendiri dan mengikuti pengaturan koordinator saat ini.
* Grader dalam [sesi berbasis outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) berjalan tanpa `web_search` dan `web_fetch`, terlepas dari pengaturan ini.
* Anda dapat mengubah daftar pada sesi yang idle dengan [memperbarui alatnya](https://platform.claude.com/docs/id/managed-agents/session-operations#updating-the-agent-configuration). Daftar baru berlaku untuk sisa sesi; dalam sesi multiagen, setiap thread menerapkannya mulai giliran berikutnya, sementara daftar milik agen roster sendiri tetap seperti yang ditetapkan definisi agennya saat sesi dibuat.

#### Perbedaan dari alat Messages API

Pengaturan ini menggunakan kosakata `allowed_domains` dan `blocked_domains` yang sama dengan [pemfilteran domain](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering) pada alat server Messages API, dengan perbedaan berikut pada Managed Agents:

* Setiap daftar dibatasi hingga 64 domain.
* Domain yang didaftarkan untuk `web_fetch` tidak dapat menyertakan path.
* Domain harus ASCII: gunakan bentuk `xn--` (Punycode) untuk nama domain terinternasionalisasi. Messages API menerima entri Unicode, meskipun tidak merekomendasikannya.
* `max_uses`, `citations`, dan `cache_control` tidak tersedia pada toolset.

## Alat kustom

Selain alat bawaan, Anda dapat mendefinisikan alat kustom. Alat kustom serupa dengan [alat klien yang didefinisikan pengguna](https://platform.claude.com/docs/id/agents-and-tools/tool-use/how-tool-use-works#user-defined-tools-client-executed) di Messages API.

Setiap alat kustom mendefinisikan sebuah kontrak: Anda menentukan operasi apa yang tersedia dan apa yang dikembalikannya, dan Claude menentukan kapan dan bagaimana memanggilnya. Model tidak pernah mengeksekusi apa pun sendiri. Model memancarkan permintaan terstruktur, kode Anda menjalankan operasinya, dan hasilnya mengalir kembali ke dalam percakapan. Lihat [Aliran event sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) untuk cara menerima panggilan alat kustom dan mengembalikan hasil selama sesi.

Jika sesi Anda berjalan di sandbox self-hosted, worker environment dapat [menyajikan alat kustom dari sandbox Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#serve-custom-tools-from-your-sandbox), termasuk alat yang membungkus server MCP di dalam jaringan Anda.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "Weather Agent",
    "model": "claude-opus-5",
    "tools": [
      {
        "type": "agent_toolset_20260401"
      },
      {
        "type": "custom",
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "City name"}
          },
          "required": ["location"]
        }
      }
    ]
  }
  EOF
  )
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:agents create < agent.yaml
    ```

    <File filename="agent.yaml">
      ```yaml
      name: Weather Agent
      model: claude-opus-5
      tools:
        - type: agent_toolset_20260401
        - type: custom
          name: get_weather
          description: Get current weather for a location
          input_schema:
            type: object
            properties:
              location:
                type: string
                description: City name
            required:
              - location
      ```
    </File>
  </MultiFileExample>

  ```python Python
  agent = client.beta.agents.create(
      name="Weather Agent",
      model="claude-opus-5",
      tools=[
          {
              "type": "agent_toolset_20260401",
          },
          {
              "type": "custom",
              "name": "get_weather",
              "description": "Get current weather for a location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {"type": "string", "description": "City name"},
                  },
                  "required": ["location"],
              },
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Weather Agent",
    model: "claude-opus-5",
    tools: [
      { type: "agent_toolset_20260401" },
      {
        type: "custom",
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: { location: { type: "string", description: "City name" } },
          required: ["location"]
        }
      }
    ]
  });
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic.Models.Beta.Agents;

  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Weather Agent",
      Model = new("claude-opus-5"),
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
          new BetaManagedAgentsCustomToolParams
          {
              Type = "custom",
              Name = "get_weather",
              Description = "Get current weather for a location",
              InputSchema = new()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(
                          new { type = "string", description = "City name" }
                      ),
                  },
                  Required = ["location"],
              },
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Weather Agent",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-5",
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}, {
  		OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
  			Type:        anthropic.BetaManagedAgentsCustomToolParamsTypeCustom,
  			Name:        "get_weather",
  			Description: "Get current weather for a location",
  			InputSchema: anthropic.BetaManagedAgentsCustomToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "City name",
  					},
  				},
  				Required: []string{"location"},
  			},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  _ = agent
  ```

  ```java Java
  import com.anthropic.models.beta.agents.*;
  import java.util.Map;

  var agent = client.beta().agents().create(AgentCreateParams.builder()
      .name("Weather Agent")
      .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
      .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
          .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
          .build())
      .addTool(BetaManagedAgentsCustomToolParams.builder()
          .type(BetaManagedAgentsCustomToolParams.Type.CUSTOM)
          .name("get_weather")
          .description("Get current weather for a location")
          .inputSchema(BetaManagedAgentsCustomToolInputSchema.builder()
              .properties(BetaManagedAgentsCustomToolInputSchema.Properties.builder()
                  .putAdditionalProperty("location", JsonValue.from(Map.of(
                      "type", "string",
                      "description", "City name")))
                  .build())
              .addRequired("location")
              .build())
          .build())
      .build());
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAgentToolset20260401Params;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolInputSchema;
  use Anthropic\Beta\Agents\BetaManagedAgentsCustomToolParams;

  $agent = $client->beta->agents->create(
      name: 'Weather Agent',
      model: 'claude-opus-5',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
          ),
          BetaManagedAgentsCustomToolParams::with(
              type: 'custom',
              name: 'get_weather',
              description: 'Get current weather for a location',
              inputSchema: BetaManagedAgentsCustomToolInputSchema::with(
                  properties: ['location' => ['type' => 'string', 'description' => 'City name']],
                  required: ['location'],
              ),
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Weather Agent",
    model: "claude-opus-5",
    tools: [
      {type: :agent_toolset_20260401},
      {
        type: :custom,
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: :object,
          properties: {location: {type: "string", description: "City name"}},
          required: ["location"]
        }
      }
    ]
  )
  ```
</CodeGroup>

Setelah Anda mendefinisikan alat kustom pada agen, agen akan memanggilnya selama sesi.

### Praktik terbaik untuk definisi alat kustom

* **Berikan deskripsi yang sangat detail.** Ini adalah faktor yang paling penting dalam kinerja alat. Deskripsi Anda harus menjelaskan apa yang dilakukan alat dan kapan menggunakannya (dan kapan tidak). Jelaskan arti setiap parameter dan bagaimana parameter tersebut memengaruhi perilaku alat. Sebutkan peringatan atau keterbatasan penting apa pun. Semakin banyak konteks yang dapat Anda berikan kepada Claude tentang alat Anda, semakin baik Claude dalam menentukan kapan dan bagaimana menggunakannya. Targetkan tiga hingga empat kalimat untuk setiap deskripsi alat, lebih banyak jika alatnya kompleks.
* **Konsolidasikan operasi terkait ke dalam lebih sedikit alat.** Daripada membuat alat terpisah untuk setiap tindakan (`create_pr`, `review_pr`, `merge_pr`), kelompokkan ke dalam satu alat dengan parameter `action`. Alat yang lebih sedikit namun lebih mumpuni mengurangi ambiguitas pemilihan dan membuat permukaan alat Anda lebih mudah dinavigasi oleh Claude.
* **Gunakan namespace yang bermakna dalam nama alat.** Ketika alat Anda mencakup beberapa layanan atau sumber daya, awali nama dengan sumber dayanya (misalnya, `db_query` atau `storage_read`). Ini membuat pemilihan alat tidak ambigu seiring bertambahnya pustaka Anda.
* **Rancang respons alat agar hanya mengembalikan informasi bersinyal tinggi.** Kembalikan pengenal yang semantik dan stabil (misalnya, slug atau UUID) alih-alih referensi internal yang tidak jelas, dan sertakan hanya field yang dibutuhkan Claude untuk menentukan langkah berikutnya. Respons yang membengkak memboroskan konteks dan mempersulit Claude mengekstrak hal yang penting.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Konektor MCP" icon="link" href="https://platform.claude.com/docs/id/managed-agents/mcp-connector">
    Hubungkan server MCP ke agen Anda untuk akses ke alat eksternal dan sumber data.
  </Card>

  <Card title="Kebijakan izin" icon="lock" href="https://platform.claude.com/docs/id/managed-agents/permission-policies">
    Kontrol kapan alat agen dan MCP dieksekusi.
  </Card>

  <Card title="Aliran event sesi" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/events-and-streaming">
    Kirim event, streaming respons, dan interupsi atau alihkan sesi Anda di tengah eksekusi.
  </Card>
</CardGroup>
