---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: fe195fe985e23801e3b2bc14a39cdc48e0305e6c554c0871b7bd81e98c519b4e
---

---
title: Tunnel MCP
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview
description: Hubungkan Claude secara aman ke server MCP yang berjalan di jaringan privat Anda tanpa membuka port masuk atau mengekspos layanan ke internet publik.
---

Tunnel MCP memungkinkan Anda menghubungkan Claude ke server "Model Context Protocol", atau MCP, yang berjalan di dalam jaringan privat Anda. Lalu lintas mengalir melalui koneksi yang hanya bersifat keluar (outbound-only), sehingga Anda tidak perlu membuka port firewall masuk, mengekspos layanan ke internet publik, atau memasukkan rentang IP Anthropic ke daftar izin (allowlist) pada origin Anda.

<Note>
  Tunnel MCP berada dalam pratinjau riset (research preview). [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya. Fitur ini disediakan "sebagaimana adanya" tanpa komitmen apa pun terkait waktu aktif, dukungan, atau keberlanjutan, dan bergantung pada penyedia jaringan pihak ketiga (Cloudflare) yang tidak memberikan komitmen ketersediaan untuk transport yang mendasarinya. Anthropic dapat mengubah atau menghentikan tunnel MCP kapan saja.
</Note>

Untuk kelayakan Zero Data Retention dan HIPAA BAA, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

## Cara kerjanya

[Tunnel stack](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) (tumpukan tunnel) terdiri dari dua komponen yang berjalan di dalam jaringan Anda:

* **[cloudflared](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components):** Konektor tunnel sumber terbuka milik Cloudflare. Komponen ini memulai koneksi yang hanya bersifat keluar ke [tunnel edge](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) (tepi tunnel) dan membawa lalu lintas terenkripsi dari Anthropic ke proxy Anda.
* **[Proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components):** Komponen perutean milik Anthropic. Komponen ini mengakhiri [inner TLS](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) (TLS bagian dalam), memvalidasi bahwa IP upstream berada dalam rentang yang diizinkan, dan merutekan setiap permintaan ke [upstream MCP server](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) (server MCP upstream) yang tepat berdasarkan hostname.

Setiap server MCP yang Anda ekspos mendapatkan hostname di bawah domain tunnel Anda (misalnya, `docs.<your-tunnel-domain>`). Anda melampirkan hostname ini ke sesi Managed Agent di Claude Console, atau meneruskannya ke Messages API melalui [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector).

## Prasyarat

Sebelum melakukan deployment, pastikan Anda memiliki:

* Target deployment: klaster Kubernetes, atau VM dengan Docker dan Docker Compose.

* Sebuah tunnel. Buat satu di Claude Console (lihat [Membuat tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#create-a-tunnel)) atau melalui API; setup hook pada Helm chart juga dapat membuatkannya untuk Anda selama instalasi.

* Cara bagi stack Anda untuk melakukan autentikasi ke Tunnels API. Pilih salah satu:

  * **[Akses programatik](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning) (direkomendasikan).** Siapkan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) saat Anda membuat tunnel. Stack Anda mencetak token API berumur pendek dari penyedia identitas Anda, mengambil token tunnel, serta membuat dan mendaftarkan sertifikat CA secara otomatis. Memerlukan izin untuk mengelola aturan federasi, issuer OIDC yang terdaftar, dan aturan federasi dengan cakupan `workspace:manage_tunnels`.
  * **[Manual](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning).** Sediakan sendiri kredensial statis: token tunnel dari Console dan sertifikat server yang ditandatangani oleh CA yang Anda daftarkan di sana. Lihat [Mendapatkan detail koneksi](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#get-the-connection-details) dan [Menambahkan sertifikat CA](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate).

* Satu atau lebih server MCP yang berjalan di jaringan privat Anda. Lihat [Server MCP jarak jauh](https://platform.claude.com/docs/id/agents-and-tools/remote-mcp-servers) untuk contoh.

* Konektivitas keluar seperti yang tercantum di bawah [Persyaratan jaringan](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#network-requirements).

### Persyaratan jaringan

| Komponen       | Tujuan                                               | Port / protokol    | Digunakan selama              |
| -------------- | ---------------------------------------------------- | ------------------ | ----------------------------- |
| Komponen setup | `api.anthropic.com`                                  | 443 TCP            | Provisioning dan rotasi token |
| cloudflared    | Tunnel edge (`198.41.192.0/19`, `2606:4700:a0::/44`) | 7844 TCP dan UDP   | Runtime                       |
| Proxy          | Server MCP upstream Anda                             | Sesuai konfigurasi | Runtime                       |

## Model keamanan

### Lapisan keamanan

Tiga lapisan independen melindungi setiap permintaan:

| Lapisan                                                               | Melindungi dari                                                                  |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| mTLS luar antara Anthropic dan penyedia transport, dengan validasi IP | Klien tidak sah yang menjangkau tunnel                                           |
| TLS dalam dari back end Anthropic ke proxy Anda                       | Inspeksi payload oleh penyedia transport atau perantara jaringan mana pun        |
| OAuth pada setiap server MCP                                          | Penggunaan alat MCP secara tidak sah oleh lalu lintas tunnel yang terautentikasi |

Transport tunnel berjalan di jaringan Cloudflare. Karena proxy mengakhiri TLS dalam menggunakan sertifikat yang hanya Anda miliki, Cloudflare tidak dapat membaca payload permintaan atau respons. Anthropic tidak terhubung ke tunnel sampai sertifikat CA terdaftar, sehingga payload selalu terenkripsi saat melintasi jaringan Cloudflare. Cloudflare memang menerima metadata koneksi; lihat [Apa yang dapat diamati oleh penyedia transport](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#what-the-transport-provider-can-observe).

### Model tanggung jawab bersama

| Ditangani Anthropic                                                                 | Ditangani organisasi Anda                                                                                                                                                             |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Kontrol akses tunnel                                                                | Semua konten dan lalu lintas yang melintasi tunnel Anda, serta kepatuhan terhadap kebijakan penggunaan yang dapat diterima dari pihak ketiga yang berlaku (termasuk milik Cloudflare) |
| Memvalidasi sertifikat CA Anda sebelum terhubung ke proxy Anda                      | Kepatuhan terhadap panduan deployment di halaman-halaman ini                                                                                                                          |
| Memastikan Claude hanya mengirim permintaan ke tunnel yang dimiliki organisasi Anda | Mengamankan token tunnel dan kunci privat TLS                                                                                                                                         |
|                                                                                     | Mengelola sertifikat server dan memperbaruinya sebelum kedaluwarsa                                                                                                                    |
|                                                                                     | Mengonfigurasi OAuth pada setiap server MCP                                                                                                                                           |
|                                                                                     | Membatasi akses jaringan untuk proxy dan server MCP                                                                                                                                   |
|                                                                                     | Memberi tahu Anthropic jika Anda mencurigai adanya pelanggaran keamanan                                                                                                               |

<Warning>
  Jika penyerang memperoleh token tunnel Anda **dan** salah satu kunci privat TLS Anda, mereka dapat menyamar sebagai proxy Anda dan membaca payload permintaan MCP. Perlakukan keduanya sebagai rahasia bernilai tinggi. Lihat [Keamanan tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security) untuk panduan hardening.
</Warning>

### Apa yang dapat diamati oleh penyedia transport

Cloudflare menyediakan transport keluar. Cloudflare tidak dapat membaca payload permintaan atau respons MCP, tetapi menerima metadata koneksi berikut:

* alamat IP egress dari host yang menjalankan cloudflared
* sidik jari (fingerprint) host cloudflared
* waktu koneksi dan volume byte
* subdomain `*.tunnel.anthropic.com` yang ditetapkan untuk tunnel Anda

Perjanjian Anthropic dengan Cloudflare membatasi penggunaan telemetri ini oleh Cloudflare. Cloudflare bertindak sebagai subprosesor untuk pratinjau riset ini.

## Men-deploy tunnel

Jika Anda baru mengenal tunnel MCP, mulailah dengan quickstart untuk mendapatkan tunnel yang berfungsi secara lokal sebelum mengonfigurasi deployment produksi.

<CardGroup cols={2}>
  <Card title="Quickstart" icon="rocket" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/quickstart">
    Jalur terpendek menuju tunnel yang berfungsi: Docker Compose dengan server MCP contoh.
  </Card>

  <Card title="Deploy dengan Helm" icon="stack" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-helm">
    Instal pada klaster Kubernetes menggunakan Helm chart Anthropic.
  </Card>

  <Card title="Deploy dengan Docker Compose" icon="cube" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose">
    Instal pada VM menggunakan Docker Compose.
  </Card>
</CardGroup>

Memilih di antaranya:

* **Target deployment**

  * **Helm** saat men-deploy ke Kubernetes.
  * **Docker Compose** untuk satu host atau pengujian lokal.

* **Autentikasi untuk setup**

  * **Akses programatik** (melalui Workload Identity Federation) jika Anda memiliki penyedia identitas OIDC seperti klaster Kubernetes, cloud IAM, atau SPIFFE.
  * **Kredensial manual** jika Anda tidak memilikinya, atau saat Anda sedang menguji.

## Menggunakan server MCP yang di-tunnel

Setelah tunnel Anda aktif (memiliki sertifikat CA aktif dan tunnel stack Anda terhubung), server MCP upstream dapat dijangkau dari Claude Managed Agents dan Messages API.

<Note>
  Tunnel MCP yang dibuat melalui Console tidak tersedia sebagai konektor di claude.ai.
</Note>

Dalam kedua kasus, tunnel membawa lalu lintas terenkripsi ke server MCP Anda tetapi tidak melakukan autentikasi ke server tersebut. Jika server MCP upstream memerlukan autentikasinya sendiri (OAuth, bearer token), sediakan dengan cara yang sama seperti untuk server MCP lainnya; hal ini independen dari tunnel.

### Managed Agents (Console)

1. Di **Managed Agents > Sessions**, buat sesi dan pilih **Create new agent** agar Anda dapat mengedit daftar server MCP.
2. Klik **+ MCP Server** dan buka dropdown. Tunnel di workspace sesi yang memiliki setidaknya satu sertifikat aktif muncul di bagian atas daftar, di atas katalog konektor publik.
3. Pilih tunnel dan isikan **Subdomain** yang dirutekan proxy Anda ke server MCP tertentu, serta **Path** yang diharapkan oleh server MCP upstream. Baris **Resolves to** menampilkan URL persisnya.

### Messages API

Teruskan URL server MCP upstream dalam array `mcp_servers`, dengan cara yang sama seperti server MCP jarak jauh lainnya. Body permintaan dan header `anthropic-beta` mengikuti format [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector) standar; hanya `url` yang spesifik untuk tunnel. Contoh berikut menggunakan header beta `mcp-client` milik konektor MCP, yang terpisah dari beta `mcp-tunnels` yang digunakan oleh [Tunnels API](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference). Buat permintaan di workspace tempat tunnel dibuat dengan menggunakan kunci API untuk workspace tersebut atau, jika kunci Anda memiliki akses ke beberapa workspace, dengan mengatur [header `anthropic-workspace-id`](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace) ke workspace tersebut.

Host URL adalah `<subdomain>.<your-tunnel-domain>`. Path bergantung pada server MCP upstream Anda, bukan tunnel: transport `streamable-http` milik FastMCP melayani di `/mcp`, dan server lain mungkin menggunakan `/` atau path kustom (periksa dokumentasi server). Proxy meneruskan path tanpa diubah.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: mcp-client-2025-11-20" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1000,
      "messages": [{"role": "user", "content": "Use the hello tool to greet tunnel."}],
      "mcp_servers": [
        {
          "type": "url",
          "url": "https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp",
          "name": "echo"
        }
      ],
      "tools": [{"type": "mcp_toolset", "mcp_server_name": "echo"}]
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta mcp-client-2025-11-20 <<'YAML'
  model: claude-opus-5
  max_tokens: 1000
  messages:
    - role: user
      content: Use the hello tool to greet tunnel.
  mcp_servers:
    - type: url
      url: https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp
      name: echo
  tools:
    - type: mcp_toolset
      mcp_server_name: echo
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=1000,
      messages=[{"role": "user", "content": "Use the hello tool to greet tunnel."}],
      mcp_servers=[
          {
              "type": "url",
              "url": "https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp",
              "name": "echo",
          }
      ],
      tools=[{"type": "mcp_toolset", "mcp_server_name": "echo"}],
      betas=["mcp-client-2025-11-20"],
  )

  print(response)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 1000,
    messages: [
      {
        role: "user",
        content: "Use the hello tool to greet tunnel."
      }
    ],
    mcp_servers: [
      {
        type: "url",
        url: "https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp",
        name: "echo"
      }
    ],
    tools: [
      {
        type: "mcp_toolset",
        mcp_server_name: "echo"
      }
    ],
    betas: ["mcp-client-2025-11-20"]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus5,
      MaxTokens = 1000,
      Messages = new List<BetaMessageParam>
      {
          new() { Role = Role.User, Content = "Use the hello tool to greet tunnel." }
      },
      McpServers = new List<BetaRequestMcpServerUrlDefinition>
      {
          new()
          {
              Url = "https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp",
              Name = "echo"
          }
      },
      Tools = new List<BetaToolUnion>
      {
          new BetaMcpToolset("echo")
      },
      Betas = ["mcp-client-2025-11-20"]
  };

  var message = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1000,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Use the hello tool to greet tunnel.")),
  	},
  	MCPServers: []anthropic.BetaRequestMCPServerURLDefinitionParam{
  		{
  			URL:  "https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp",
  			Name: "echo",
  		},
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfMCPToolset: &anthropic.BetaMCPToolsetParam{
  			MCPServerName: "echo",
  		}},
  	},
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaMCPClient2025_11_20,
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaMcpToolset;
  // ...
  import com.anthropic.models.beta.messages.BetaRequestMcpServerUrlDefinition;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1000L)
          .addUserMessage("Use the hello tool to greet tunnel.")
          .addMcpServer(BetaRequestMcpServerUrlDefinition.builder()
              .url("https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp")
              .name("echo")
              .build())
          .addTool(BetaMcpToolset.builder()
              .mcpServerName("echo")
              .build())
          .addBeta("mcp-client-2025-11-20")
          .build();

      BetaMessage response = client.beta().messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 1000,
      messages: [
          ['role' => 'user', 'content' => 'Use the hello tool to greet tunnel.']
      ],
      model: 'claude-opus-5',
      mcpServers: [
          [
              'type' => 'url',
              'url' => 'https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp',
              'name' => 'echo',
          ],
      ],
      tools: [
          [
              'type' => 'mcp_toolset',
              'mcpServerName' => 'echo',
          ],
      ],
      betas: ['mcp-client-2025-11-20'],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 1000,
    messages: [
      { role: "user", content: "Use the hello tool to greet tunnel." }
    ],
    mcp_servers: [
      {
        type: "url",
        url: "https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp",
        name: "echo"
      }
    ],
    tools: [
      {
        type: "mcp_toolset",
        mcp_server_name: "echo"
      }
    ],
    betas: ["mcp-client-2025-11-20"]
  )

  puts response
  ```
</CodeGroup>

Untuk autentikasi ke server MCP upstream (`authorization_token`) dan opsi `mcp_servers` lainnya, lihat [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Keamanan" icon="lock" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security">
    Panduan hardening, rotasi kredensial, dan respons terhadap pelanggaran keamanan.
  </Card>

  <Card title="Pemecahan masalah" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting">
    Diagnosis masalah konektivitas, TLS, dan perutean.
  </Card>

  <Card title="Referensi" icon="book" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference">
    Field konfigurasi proxy, Tunnels API, persyaratan sertifikat, dan komponen setup.
  </Card>

  <Card title="Konektor MCP" icon="link" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-connector">
    Gunakan server yang di-tunnel dari Messages API.
  </Card>
</CardGroup>
