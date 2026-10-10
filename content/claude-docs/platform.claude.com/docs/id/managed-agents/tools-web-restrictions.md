---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: c2b1b301928e007286792bef6c7a9f5131d09c4f2157df0ede8583e7901e6e1a
---

---
title: Membatasi domain web search dan web fetch
url: https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions
description: Kontrol situs mana yang dapat dijangkau oleh alat web search dan web fetch milik agen, batasi konten yang diambil, dan lokalkan hasil pencarian.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Untuk mengontrol situs mana yang dapat dijangkau oleh alat web agen, tetapkan daftar domain pada entri `web_search` dan `web_fetch` dari [toolset agen](https://platform.claude.com/docs/id/managed-agents/tools#configuring-the-toolset). Setiap entri `configs` ini menerima salah satu dari dua daftar:

* **`allowed_domains`:** Alat hanya dapat menjangkau host-host ini.
* **`blocked_domains`:** Alat tidak pernah dapat menjangkau host-host ini.

Setiap alat memiliki daftarnya sendiri, sehingga `web_search` dan `web_fetch` dapat memiliki pembatasan yang berbeda.

<Note>
  `web_search` dan `web_fetch` berjalan di server Anthropic, bukan di sandbox. Environment cloud dengan [jaringan](https://platform.claude.com/docs/id/managed-agents/environments#networking) `limited` juga menerapkan `allowed_hosts`-nya pada alat-alat tersebut; lihat [Menetapkan daftar domain pada agen](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#set-domain-lists-on-an-agent). Jaringan `unrestricted` dan environment self-hosted tidak membatasinya. Daftar per alat membatasi alat-alat ini lebih lanjut. Pengaturan web search dan web fetch tingkat organisasi di Claude Console berlaku untuk Messages API. Pengaturan tersebut tidak berlaku untuk sesi Managed Agents.
</Note>

## Menetapkan daftar domain pada agen

Contoh berikut membuat agen yang membatasi `web_search` ke dua situs dan memblokir satu host untuk `web_fetch`. Contoh ini juga menetapkan `user_location` dan `max_content_tokens`, yang dijelaskan di [Pengaturan](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#settings). Contoh tersebut kemudian mencetak array `configs` dari respons.

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
    "model": "claude-opus-5-5",
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

  <CodeGroupItem>
    ```bash CLI
    ant apply agent.md
    ```

    <File filename="agent.md">
      ```markdown
      ---
      name: Research Agent
      model: claude-opus-5-5
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
      ---
      ```
    </File>

    [`ant apply`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply) membuat agen dan mencetak ID-nya, bukan array `configs`.
  </CodeGroupItem>

  ```python Python
  client = Anthropic()

  agent = client.beta.agents.create(
      name="Research Agent",
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
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
      Model = BetaManagedAgentsModel.ClaudeOpus5_5,
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
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5_5,
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
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5_5)
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
      model: 'claude-opus-5-5',
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
    model: "claude-opus-5-5",
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

Dalam environment cloud dengan [jaringan](https://platform.claude.com/docs/id/managed-agents/environments#networking) `limited`, `allowed_hosts` milik environment juga berlaku untuk `web_search` dan `web_fetch`. Pembuatan sesi gagal dengan error 400 ketika `allowed_domains` dari alat web yang diaktifkan memiliki entri yang tidak berada dalam `allowed_hosts`. Begitu pula pembaruan sesi yang menambahkan entri semacam itu. Untuk memperbaikinya, tambahkan host ke `allowed_hosts` atau hapus entri dari `allowed_domains`. Saat runtime, panggilan `web_fetch` untuk URL pada host yang tidak cocok dengan `allowed_hosts` mengembalikan hasil error `url_not_allowed`. `web_search` menghilangkan hasil dari host semacam itu. Kedua daftar dicocokkan secara berbeda: entri alat mencakup subdomainnya, tetapi entri `allowed_hosts` hanya cocok dengan satu host yang persis sama kecuali diawali dengan `*.`. Misalnya, entri alat `docs.example.com` tidak berada dalam `allowed_hosts` berisi `["example.com"]`, tetapi berada dalam `["docs.example.com"]` atau `["*.example.com"]`.

Di Claude Console, tetapkan domain yang diizinkan atau diblokir dari baris `web_search` dan `web_fetch` pada kartu **Built-in tools** di formulir agen. Tetapkan `max_content_tokens` dan `user_location` di tampilan **Raw** dari konfigurasi agen.

## Pengaturan

Selain `enabled` dan `permission_policy`, entri alat web menerima pengaturan berikut:

| Pengaturan           | Berlaku untuk             | Deskripsi                                                                                                                                                                                                                           |
| -------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed_domains`    | `web_search`, `web_fetch` | Satu-satunya host yang dapat dijangkau alat. Lihat [Aturan daftar domain](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#domain-list-rules).                                                             |
| `blocked_domains`    | `web_search`, `web_fetch` | Host yang tidak dapat dijangkau alat. Lihat [Aturan daftar domain](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#domain-list-rules).                                                                    |
| `max_content_tokens` | `web_fetch`               | Membatasi jumlah konten halaman yang diambil yang disertakan dalam konteks. Harus berupa bilangan bulat positif. Lihat [batas konten](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#content-limits). |
| `user_location`      | `web_search`              | Melokalkan hasil pencarian. Sebuah objek dengan field yang sama seperti parameter [`user_location`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool#localization) pada Messages API.                  |

Untuk cara SDK mendefinisikan tipe entri-entri ini, lihat [Jenis entri konfigurasi di SDK](https://platform.claude.com/docs/id/managed-agents/tools#config-entry-types-in-the-sdks).

## Ketika domain tidak diizinkan

`web_search` menghilangkan hasil yang tidak diizinkan oleh daftar domainnya. Panggilan `web_fetch` untuk URL yang tidak diizinkan oleh daftar domainnya mengembalikan hasil error kepada agen. Event `agent.tool_result` memiliki `is_error: true`, dan kontennya menyebutkan kode error `url_not_allowed`.

## Aturan daftar domain

Aturan-aturan ini berlaku sama untuk `allowed_domains` dan `blocked_domains`. Permintaan yang melanggar salah satunya akan ditolak, seperti yang dijelaskan di [Error validasi](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#validation-errors).

* **Satu daftar per entri:** Tetapkan `allowed_domains` atau `blocked_domains` pada sebuah entri, bukan keduanya.
* **Ukuran daftar:** Setiap daftar berisi 1 hingga 64 domain, masing-masing 1 hingga 255 karakter.
* **Tidak boleh ada daftar kosong:** Untuk tidak menerapkan pembatasan, hilangkan field tersebut atau kirim `null`.
* **Tidak boleh ada duplikat:** Sebuah domain hanya boleh muncul sekali dalam daftar. `www.example.com` dan `example.com` dihitung sebagai domain yang berbeda.

### Apa yang dicocokkan oleh domain yang terdaftar

Domain yang terdaftar cocok dengan host tersebut dan semua subdomainnya. `example.com` mencakup `docs.example.com`, tetapi `docs.example.com` tidak mencakup `example.com` atau `api.example.com`.

Awalan `www.` adalah subdomain seperti yang lainnya, sehingga `www.example.com` tidak mencakup `example.com`. Daftarkan domain polos untuk mencakup keduanya.

Hostname dibandingkan tanpa memperhatikan huruf besar/kecil.

### Format domain

Setiap domain adalah nama domain yang dapat didaftarkan, atau subdomainnya, yang ditulis sebagai hostname polos. Domain dapat berisi huruf ASCII, angka, tanda hubung, garis bawah, dan titik. Satu `/` di akhir akan diabaikan.

| Tidak diterima                                                                               | Contoh                   | Gunakan sebagai gantinya               |
| -------------------------------------------------------------------------------------------- | ------------------------ | -------------------------------------- |
| Skema                                                                                        | `https://example.com`    | `example.com`                          |
| Port                                                                                         | `example.com:443`        | `example.com`                          |
| Wildcard                                                                                     | `*.example.com`          | `example.com`                          |
| Path pada domain `web_fetch`                                                                 | `example.com/*`          | `example.com`                          |
| Alamat IP dalam bentuk apa pun, baik IPv4, IPv6, dalam kurung siku, maupun singkatan numerik | `127.1`                  | Nama domain situs                      |
| Top-level domain polos atau sufiks registri                                                  | `com`, `co.uk`, `gov.uk` | Domain lengkap seperti `example.co.uk` |
| Nama satu label                                                                              | `intranet`               | Domain lengkap seperti `example.co.uk` |
| Karakter non-ASCII, seperti pada nama domain internasional                                   |                          | Bentuk `xn--` (Punycode)               |

Domain juga ditolak jika berisi kredensial atau spasi, atau jika salah satu labelnya diawali atau diakhiri dengan tanda hubung. `localhost` dan host yang berakhiran `.localhost`, `.local`, `.internal`, `.localdomain`, atau `.invalid` juga ditolak.

### Sufiks path pada domain web search

Domain `web_search` dapat membawa sufiks path, seperti `example.com/blog`. Path tidak boleh berisi spasi, `?`, `#`, atau karakter apa pun dari `$ , | ^ !`.

Utamakan hostname polos untuk `web_search` juga. Penyedia pencarian mencocokkan sufiks path sebagai pola URL, bukan sebagai aturan host yang ketat.

## Error validasi

API memvalidasi pengaturan ini saat Anda [membuat agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#create-an-agent) atau [memperbarui agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-an-agent). API juga memvalidasinya saat Anda membuat atau memperbarui sesi yang menyertakan `tools`.

Pelanggaran format dan batas ditolak dengan 400 `invalid_request_error`:

| Pelanggaran                            | Pesan error                                                                                                                                                                    |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sebuah entri menetapkan kedua daftar.  | Menyertakan `Only one of allowed_domains or blocked_domains may be set.`                                                                                                       |
| Sebuah daftar kosong.                  | Menyertakan `allowed_domains: Empty list of domains is ambiguous. Provide at least one domain or null.`                                                                        |
| Sebuah domain melanggar aturan format. | Menyebutkan daftar domain tersebut dan posisinya yang berbasis nol. Misalnya, `allowed_domains.0: IP addresses are not supported; provide a plain hostname like "example.com"` |

Pada permintaan yang sama, API juga menolak tiga pengaturan yang bergantung pada penyedia pencarian dan pengambilan:

* Domain dalam `allowed_domains` yang tidak diizinkan untuk diakses oleh crawler Anthropic.
* `user_location.country` yang tidak didukung oleh penyedia pencarian. Pesannya diakhiri dengan `user_location.country: not a country the search provider supports`.
* `user_location.timezone` yang bukan nama IANA yang valid.

Dalam environment cloud dengan [jaringan](https://platform.claude.com/docs/id/managed-agents/environments#networking) `limited`, pembuatan dan pembaruan sesi juga memeriksa `allowed_domains` terhadap `allowed_hosts` milik environment. Lihat aturannya di [Menetapkan daftar domain pada agen](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#set-domain-lists-on-an-agent).

### Ketika pengaturan yang diterima tidak lagi valid

Sesi memeriksa konfigurasi lagi saat pertama kali menginisialisasi alat. Jika pengaturan yang sebelumnya diterima tidak lagi valid pada saat itu, sesi memancarkan event [`session.error`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming). Sesi kemudian kembali ke `idle` tanpa mencoba ulang.

Untuk melanjutkan sesi:

1. Perbaiki pengaturan dengan [memperbarui alat sesi](https://platform.claude.com/docs/id/managed-agents/session-operations#updating-the-agent-configuration).
2. Perbarui juga agennya, sehingga sesi baru dimulai dengan konfigurasi yang sudah diperbaiki.
3. Kirim `user.message` baru.

## Sesi multiagen dan berbasis outcome

Dalam [sesi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), setiap daftar domain yang berlaku untuk sebuah thread diberlakukan secara bersamaan. Agen yang tercantum dalam `subagents.predefined_agents` terikat oleh tiga set daftar:

* `allowed_domains` dan `blocked_domains` miliknya sendiri
* Milik agen mana pun yang memanggilnya
* Daftar saat ini dari agen yang dijalankan oleh sesi

Pengaturan digabungkan sebagai berikut:

| Pengaturan                            | Cara penggabungannya                                                                                                                                                                                                             |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed_domains`                     | Alat dapat menjangkau sebuah host hanya jika setiap daftar mencakupnya.                                                                                                                                                          |
| `blocked_domains`                     | Daftar-daftar dijumlahkan.                                                                                                                                                                                                       |
| `max_content_tokens`, `user_location` | Tidak digabungkan. Sebuah thread menggunakan nilai dari konfigurasi alatnya sendiri jika ditetapkan. Jika tidak, thread menggunakan nilai dari agen yang memanggilnya, dan jika tidak juga, konfigurasi saat ini dari agen sesi. |

Oleh karena itu, agen yang tercantum dapat mempersempit apa yang dijangkau alat tetapi tidak pernah memperluasnya:

* Agen tercantum yang menetapkan `blocked_domains` tetap menggunakan `allowed_domains` dari agen sesi dan memblokir host tersebut di dalamnya.
* Agen tercantum yang menetapkan `allowed_domains` sendiri hanya dapat menjangkau host yang tercakup baik oleh daftarnya maupun daftar agen sesi.

Entri `{"type": "self"}` dalam `subagents.predefined_agents` tidak memiliki pengaturan web sendiri dan mengikuti pengaturan saat ini dari agen sesi.

Jika daftar `allowed_domains` yang digabungkan tidak memiliki domain yang sama, alat tetap tersedia bagi agen tersebut tetapi setiap panggilan gagal. Setiap panggilan mengembalikan error `url_not_allowed` yang menyatakan bahwa tidak ada domain yang diizinkan. Deskripsi alat juga memberi tahu model hal yang sama. Untuk menghindari hal ini, pastikan `allowed_domains` setiap agen tercantum berada di dalam `allowed_domains` agen sesi.

Grader dalam [sesi berbasis outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes) berjalan tanpa `web_search` dan `web_fetch`, terlepas dari pengaturan ini.

## Mengubah daftar di tengah sesi

Anda dapat mengubah daftar pada sesi yang sedang idle dengan [memperbarui alatnya](https://platform.claude.com/docs/id/managed-agents/session-operations#updating-the-agent-configuration). Daftar baru berlaku untuk sisa sesi.

Dalam sesi multiagen, setiap thread menerapkan daftar baru mulai dari giliran berikutnya. Untuk agen yang tercantum dalam `subagents.predefined_agents`, pembaruan tidak mengubah daftar milik agen itu sendiri. Daftar tersebut tetap seperti yang ditetapkan oleh definisi agen saat sesi dibuat.

## Perbedaan dari alat Messages API

Pengaturan ini menggunakan field `allowed_domains` dan `blocked_domains` yang sama seperti [pemfilteran domain](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering) pada alat server Messages API. Managed Agents berbeda dalam empat hal:

* Setiap daftar [dibatasi hingga 64 domain](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#domain-list-rules).
* Domain yang didaftarkan untuk `web_fetch` [tidak boleh menyertakan path](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#domain-format).
* Domain [harus berupa ASCII](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions#domain-format). Messages API menerima entri Unicode, meskipun tidak merekomendasikannya.
* `max_uses`, `citations`, dan `cache_control` tidak tersedia pada toolset.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Alat" icon="tool" href="https://platform.claude.com/docs/id/managed-agents/tools">
    Lihat alat bawaan, aktifkan atau nonaktifkan, dan definisikan alat kustom.
  </Card>

  <Card title="Kebijakan izin" icon="lock" href="https://platform.claude.com/docs/id/managed-agents/permission-policies">
    Kontrol kapan alat agen dan MCP dieksekusi.
  </Card>

  <Card title="Penyiapan lingkungan cloud" icon="settings" href="https://platform.claude.com/docs/id/managed-agents/environments">
    Kontrol akses jaringan keluar milik sandbox itu sendiri.
  </Card>

  <Card title="Orkestrasi multiagen" icon="sitemap" href="https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration">
    Koordinasikan beberapa agen dalam satu sesi.
  </Card>
</CardGroup>
