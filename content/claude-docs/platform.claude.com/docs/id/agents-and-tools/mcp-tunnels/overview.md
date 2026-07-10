---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: ba5b030f3bbb5eb24140ba4b35cb8a03ee9d8bd669582b653119d6cad8b28803
---

# Tunnel MCP

Hubungkan Claude secara aman ke server MCP yang berjalan di jaringan privat Anda tanpa membuka port masuk atau mengekspos layanan ke internet publik.

---

Tunnel MCP memungkinkan Anda menghubungkan Claude ke server Model Context Protocol (MCP) yang berjalan di dalam jaringan privat Anda. Lalu lintas mengalir melalui koneksi keluar-saja (outbound-only), sehingga Anda tidak perlu membuka port firewall masuk, mengekspos layanan ke internet publik, atau memasukkan rentang IP Anthropic ke daftar izin pada origin Anda.

<Note>
  Tunnel MCP berada dalam research preview. [Ajukan akses](https://claude.com/form/claude-managed-agents) untuk mencobanya. Tunnel MCP disediakan "sebagaimana adanya" tanpa komitmen uptime, dukungan, atau kontinuitas apa pun, dan bergantung pada penyedia jaringan pihak ketiga (Cloudflare) yang tidak memberikan komitmen ketersediaan untuk transport yang mendasarinya. Anthropic dapat mengubah atau menghentikan tunnel MCP kapan saja.
</Note>

Untuk kelayakan Zero Data Retention dan HIPAA BAA, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

## Cara kerjanya

[Tunnel stack](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) terdiri dari dua komponen yang berjalan di dalam jaringan Anda:

* **[cloudflared](/docs/id/agents-and-tools/mcp-tunnels/concepts#components):** Konektor tunnel open-source dari Cloudflare. Komponen ini memulai koneksi keluar-saja ke [tunnel edge](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) dan membawa lalu lintas terenkripsi dari Anthropic ke proxy Anda.
* **[Proxy](/docs/id/agents-and-tools/mcp-tunnels/concepts#components):** Komponen routing dari Anthropic. Komponen ini mengakhiri [inner TLS](/docs/id/agents-and-tools/mcp-tunnels/concepts#components), memvalidasi bahwa IP upstream berada dalam rentang yang diizinkan, dan merutekan setiap permintaan ke [server MCP upstream](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) yang benar berdasarkan hostname.

Setiap server MCP yang Anda ekspos mendapatkan hostname di bawah domain tunnel Anda (misalnya, `docs.<your-tunnel-domain>`). Anda melampirkan hostname ini ke sesi Managed Agent di Console, atau meneruskannya ke Messages API melalui [konektor MCP](/docs/id/agents-and-tools/mcp-connector).

## Prasyarat

Sebelum melakukan deployment, pastikan Anda memiliki:

* Target deployment: klaster Kubernetes, atau VM dengan Docker dan Docker Compose.

* Sebuah tunnel. Buat satu di Claude Console (lihat [Membuat tunnel](/docs/id/agents-and-tools/mcp-tunnels/console#create-a-tunnel)) atau melalui API; setup hook pada Helm chart juga dapat membuatkannya untuk Anda selama instalasi.

* Cara bagi stack Anda untuk melakukan autentikasi ke Tunnels API. Pilih salah satu:

  * **[Akses programatik](/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning) (direkomendasikan).** Siapkan [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation) saat Anda membuat tunnel. Stack Anda mencetak token API berumur pendek dari penyedia identitas Anda, mengambil token tunnel, serta menghasilkan dan mendaftarkan sertifikat CA secara otomatis. Memerlukan izin untuk mengelola aturan federasi, issuer OIDC yang terdaftar, dan aturan federasi dengan cakupan `workspace:manage_tunnels`.
  * **[Manual](/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning).** Sediakan kredensial statis sendiri: token tunnel dari Console dan sertifikat server yang ditandatangani oleh CA yang Anda daftarkan di sana. Lihat [Mendapatkan detail koneksi](/docs/id/agents-and-tools/mcp-tunnels/console#get-the-connection-details) dan [Menambahkan sertifikat CA](/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate).

* Satu atau lebih server MCP yang berjalan di jaringan privat Anda. Lihat [Server MCP jarak jauh](/docs/id/agents-and-tools/remote-mcp-servers) untuk contoh.

* Konektivitas keluar seperti yang tercantum di bawah [Persyaratan jaringan](#network-requirements).

### Persyaratan jaringan

| Komponen       | Tujuan                                               | Port / protokol    | Digunakan selama              |
| -------------- | ---------------------------------------------------- | ------------------ | ----------------------------- |
| Komponen setup | `api.anthropic.com`                                  | 443 TCP            | Provisioning dan rotasi token |
| cloudflared    | Tunnel edge (`198.41.192.0/19`, `2606:4700:a0::/44`) | 7844 TCP dan UDP   | Runtime                       |
| Proxy          | Server MCP upstream Anda                             | Sesuai konfigurasi | Runtime                       |

## Model keamanan

### Lapisan keamanan

Tiga lapisan independen melindungi setiap permintaan:

| Lapisan                                                                | Melindungi dari                                                                |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Outer mTLS antara Anthropic dan penyedia transport, dengan validasi IP | Klien tidak sah yang mencapai tunnel                                           |
| Inner TLS dari backend Anthropic ke proxy Anda                         | Inspeksi payload oleh penyedia transport atau perantara jaringan mana pun      |
| OAuth pada setiap server MCP                                           | Penggunaan tidak sah atas alat MCP oleh lalu lintas tunnel yang terautentikasi |

Transport tunnel berjalan di jaringan Cloudflare. Karena proxy mengakhiri inner TLS menggunakan sertifikat yang hanya Anda pegang, Cloudflare tidak dapat membaca payload permintaan atau respons. Anthropic tidak terhubung ke tunnel sampai sertifikat CA terdaftar, sehingga payload selalu terenkripsi saat melintasi jaringan Cloudflare. Cloudflare memang menerima metadata koneksi; lihat [Apa yang dapat diamati oleh penyedia transport](#what-the-transport-provider-can-observe).

### Model tanggung jawab bersama

| Ditangani Anthropic                                                                      | Ditangani organisasi Anda                                                                                                                                                            |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Kontrol akses tunnel                                                                     | Semua konten dan lalu lintas yang melewati tunnel Anda, serta kepatuhan terhadap kebijakan penggunaan yang dapat diterima dari pihak ketiga yang berlaku (termasuk milik Cloudflare) |
| Memvalidasi sertifikat CA Anda sebelum terhubung ke proxy Anda                           | Kepatuhan terhadap panduan deployment di halaman-halaman ini                                                                                                                         |
| Memastikan Claude hanya mengirim permintaan ke tunnel yang dimiliki oleh organisasi Anda | Mengamankan token tunnel dan kunci privat TLS                                                                                                                                        |
|                                                                                          | Mengelola sertifikat server dan memperbaruinya sebelum kedaluwarsa                                                                                                                   |
|                                                                                          | Mengonfigurasi OAuth pada setiap server MCP                                                                                                                                          |
|                                                                                          | Membatasi akses jaringan untuk proxy dan server MCP                                                                                                                                  |
|                                                                                          | Memberi tahu Anthropic jika Anda mencurigai adanya pelanggaran                                                                                                                       |

<Warning>
  Jika penyerang memperoleh token tunnel Anda **dan** salah satu kunci privat TLS Anda, mereka dapat menyamar sebagai proxy Anda dan membaca payload permintaan MCP. Perlakukan keduanya sebagai rahasia bernilai tinggi. Lihat [Keamanan tunnel MCP](/docs/id/agents-and-tools/mcp-tunnels/security) untuk panduan pengerasan (hardening).
</Warning>

### Apa yang dapat diamati oleh penyedia transport

Cloudflare menyediakan transport keluar. Cloudflare tidak dapat membaca payload permintaan atau respons MCP, tetapi menerima metadata koneksi berikut:

* alamat IP egress dari host yang menjalankan cloudflared
* fingerprint host cloudflared
* waktu koneksi dan volume byte
* subdomain `*.tunnel.anthropic.com` yang ditetapkan untuk tunnel Anda

Perjanjian Anthropic dengan Cloudflare membatasi penggunaan telemetri ini oleh Cloudflare. Cloudflare bertindak sebagai subprosesor untuk research preview ini.

## Melakukan deployment tunnel

Jika Anda baru mengenal tunnel MCP, mulailah dengan quickstart untuk mendapatkan tunnel yang berfungsi secara lokal sebelum mengonfigurasi deployment produksi.

<CardGroup cols={2}>
  <Card title="Quickstart" icon="rocket" href="/docs/id/agents-and-tools/mcp-tunnels/quickstart">
    Jalur tersingkat menuju tunnel yang berfungsi: Docker Compose dengan contoh server MCP.
  </Card>

  <Card title="Deploy dengan Helm" icon="stack" href="/docs/id/agents-and-tools/mcp-tunnels/deploy-helm">
    Instal pada klaster Kubernetes menggunakan Helm chart dari Anthropic.
  </Card>

  <Card title="Deploy dengan Docker Compose" icon="cube" href="/docs/id/agents-and-tools/mcp-tunnels/deploy-compose">
    Instal pada VM menggunakan Docker Compose.
  </Card>
</CardGroup>

Memilih di antara keduanya:

* **Target deployment**

  * **Helm** saat melakukan deployment ke Kubernetes.
  * **Docker Compose** untuk satu host atau pengujian lokal.

* **Autentikasi untuk setup**

  * **Akses programatik** (melalui Workload Identity Federation) saat Anda memiliki penyedia identitas OIDC seperti klaster Kubernetes, cloud IAM, atau SPIFFE.
  * **Kredensial manual** saat Anda tidak memilikinya, atau saat Anda sedang melakukan pengujian.

## Menggunakan server MCP yang di-tunnel

Setelah tunnel Anda aktif (memiliki sertifikat CA aktif dan tunnel stack Anda terhubung), server MCP upstream dapat dijangkau dari Claude Managed Agents dan Messages API.

<Note>
  Tunnel MCP yang dibuat melalui Console tidak tersedia sebagai konektor di claude.ai.
</Note>

Dalam kedua kasus tersebut, tunnel membawa lalu lintas terenkripsi ke server MCP Anda tetapi tidak melakukan autentikasi ke server tersebut. Jika server MCP upstream memerlukan autentikasinya sendiri (OAuth, bearer token), sediakan dengan cara yang sama seperti untuk server MCP lainnya; hal ini independen dari tunnel.

### Managed Agents (Console)

1. Di **Managed Agents > Sessions**, buat sesi dan pilih **Create new agent** agar Anda dapat mengedit daftar server MCP.
2. Klik **+ MCP Server** dan buka dropdown. Tunnel di workspace sesi yang memiliki setidaknya satu sertifikat aktif muncul di bagian atas daftar, di atas katalog konektor publik.
3. Pilih tunnel dan sediakan **Subdomain** yang dirutekan proxy Anda ke server MCP tertentu, serta **Path** yang diharapkan oleh server MCP upstream. Baris **Resolves to** menampilkan URL yang tepat.

### Messages API

Teruskan URL server MCP upstream dalam array `mcp_servers`, dengan cara yang sama seperti server MCP jarak jauh lainnya. Body permintaan dan header `anthropic-beta` mengikuti format standar [konektor MCP](/docs/id/agents-and-tools/mcp-connector); hanya `url` yang spesifik untuk tunnel. Contoh berikut menggunakan header beta `mcp-client` dari konektor MCP, yang terpisah dari beta `mcp-tunnels` yang digunakan oleh [Tunnels API](/docs/id/agents-and-tools/mcp-tunnels/reference). Gunakan kunci API untuk workspace tempat tunnel dibuat (Console **Settings > API keys**).

Host pada URL adalah `<subdomain>.<your-tunnel-domain>`. Path bergantung pada server MCP upstream Anda, bukan pada tunnel: transport `streamable-http` dari FastMCP melayani di `/mcp`, dan server lain mungkin menggunakan `/` atau path kustom (periksa dokumentasi server tersebut). Proxy meneruskan path tanpa mengubahnya.

```bash
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: mcp-client-2025-11-20" \
  -d '{
    "model": "claude-opus-4-8",
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

Untuk contoh SDK dalam setiap bahasa, lihat [konektor MCP](/docs/id/agents-and-tools/mcp-connector); satu-satunya nilai yang spesifik untuk tunnel adalah `url`.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Keamanan" icon="lock" href="/docs/id/agents-and-tools/mcp-tunnels/security">
    Panduan pengerasan, rotasi kredensial, dan respons terhadap pelanggaran.
  </Card>

  <Card title="Pemecahan masalah" icon="wrench" href="/docs/id/agents-and-tools/mcp-tunnels/troubleshooting">
    Mendiagnosis masalah konektivitas, TLS, dan routing.
  </Card>

  <Card title="Referensi" icon="book" href="/docs/id/agents-and-tools/mcp-tunnels/reference">
    Field konfigurasi proxy, Tunnels API, persyaratan sertifikat, dan komponen setup.
  </Card>

  <Card title="Konektor MCP" icon="link" href="/docs/id/agents-and-tools/mcp-connector">
    Gunakan server yang di-tunnel dari Messages API.
  </Card>
</CardGroup>
