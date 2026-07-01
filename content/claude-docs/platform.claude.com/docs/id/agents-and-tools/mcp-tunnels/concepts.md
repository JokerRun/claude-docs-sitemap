---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: 2ce5469158332f31975885a2c8abcc595e149da0ce5cc9a1a523e140ef8562da
---

# Arsitektur dan komponen

Nama kanonis untuk bagian-bagian dari deployment MCP tunnel, dua mode penyediaan kredensial, dan model koneksi.

---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

Halaman ini mendefinisikan istilah-istilah yang digunakan di seluruh dokumentasi [MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/overview). Beberapa komponen muncul dengan nama yang berbeda dalam file konfigurasi, image container, dan teks naratif; tabel berikut memberikan satu nama kanonis untuk masing-masing dan mencantumkan alias yang mungkin Anda temui.

## Komponen

| Istilah                 | Definisi                                                                                                                                                                                                                                                                                                                                        | Juga muncul sebagai                                                                                                                                                                                   |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tunnel stack**        | Dua container yang Anda jalankan di dalam jaringan Anda untuk terhubung ke sebuah tunnel: proxy dan cloudflared. Satu stack melayani satu tunnel dan dapat direplikasi di beberapa host untuk ketersediaan. Dengan akses terprogram, komponen setup berjalan bersama stack untuk menyediakan kredensial.                                        | the stack, the MCP tunnel stack, the tunnel deployment, your deployment                                                                                                                               |
| **Proxy**               | Komponen routing milik Anthropic. Mengakhiri inner TLS, memvalidasi bahwa IP upstream berada dalam rentang yang diizinkan, dan merutekan setiap permintaan ke server MCP upstream berdasarkan hostname.                                                                                                                                         | `mcp-proxy` (nama image, nama service Compose, dan nama container Helm), `mcp-gateway` (path konfigurasi internal container `/etc/mcp-gateway/config.yaml` dan prefiks nilai Helm `gateway.config.*`) |
| **cloudflared**         | Konektor tunnel open-source dari Cloudflare. Menginisiasi koneksi outbound-only dari jaringan Anda ke tunnel edge dan membawa lalu lintas terenkripsi antara edge dan proxy. Tidak terkait dengan Managed Agent.                                                                                                                                | the outbound connector, the tunnel connector                                                                                                                                                          |
| **Komponen setup**      | Binary `setup`, yang disertakan di dalam image `mcp-proxy`. Dengan akses terprogram, komponen ini mengautentikasi melalui Workload Identity Federation, mengambil token tunnel, menghasilkan CA dan sertifikat server, serta mendaftarkan CA tersebut ke Anthropic. Juga menyediakan `renew-cert`.                                              | setup Job (hook pre-install Helm), service `setup` (profil Compose), setup hook, setup binary, setup CLI                                                                                              |
| **Tunnel edge**         | Server edge Cloudflare yang dihubungi oleh cloudflared melalui koneksi keluar (rentang IP `198.41.192.0/19` dan `2606:4700:a0::/44`, port 7844 TCP dan UDP). Tunnel yang berjalan di atasnya disediakan dan dikendalikan oleh Anthropic; Cloudflare mengoperasikan jaringan yang mendasarinya.                                                  | the edge, the Anthropic-operated tunnel edge                                                                                                                                                          |
| **Inner TLS**           | Handshake TLS kedua yang dibawa di dalam stream WebSocket plaintext milik tunnel, antara backend Anthropic dan proxy Anda. Proxy menyajikan sertifikat server yang ditandatangani oleh CA yang Anda daftarkan pada tunnel. Karena hanya Anda yang memegang private key, penyedia transport tidak dapat membaca payload permintaan atau respons. | the inner TLS handshake                                                                                                                                                                               |
| **Server MCP upstream** | Server MCP yang berjalan di jaringan privat Anda yang menjadi tujuan routing dari proxy. Setiap upstream diekspos sebagai satu subdomain di bawah domain tunnel Anda.                                                                                                                                                                           | upstream, routed MCP server, tunneled MCP server                                                                                                                                                      |

## Penyediaan kredensial

Tunnel stack membutuhkan dua kredensial saat runtime: **token tunnel**, yang mengautentikasi koneksi outbound cloudflared, dan **sertifikat server** yang ditandatangani oleh CA yang terdaftar pada tunnel, yang disajikan oleh proxy selama handshake inner TLS. Ada dua cara untuk menyediakannya, yang disajikan di seluruh panduan ini sebagai sepasang tab.

| Mode                 | Bagaimana kredensial mencapai stack                                                                                                                                                                                                                                                                                                                                                   | Nama chart Helm                               | Label tab                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------- |
| **Akses terprogram** | Komponen setup mengautentikasi ke Tunnels API melalui [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation), mengambil token tunnel, menghasilkan CA dan sertifikat server secara lokal, dan mendaftarkan CA tersebut. Tidak ada secret berumur panjang yang disalin secara manual. Memerlukan aturan federasi dengan scope `workspace:manage_tunnels`. | Managed mode (`setup.enabled: true`, default) | **With programmatic access**    |
| **Manual**           | Anda menyalin token tunnel dari Claude Console, menghasilkan CA dan sertifikat server sendiri (misalnya dengan `openssl`), mendaftarkan CA di Console, dan menyediakan token serta sertifikat ke stack sebagai secret. Tidak ada komponen setup yang berjalan.                                                                                                                        | External mode (`setup.enabled: false`)        | **Without programmatic access** |

Mode-mode ini juga disebut sebagai **alur terprogram** (the programmatic flow) dan **alur manual** (the manual flow) dalam panduan deploy.

## Model koneksi

Ada dua arah yang bekerja dalam sebuah tunnel, dan keduanya menunjuk ke arah yang berlawanan:

* **Arah koneksi:** cloudflared melakukan koneksi **outbound** dari jaringan Anda ke tunnel edge. Firewall Anda hanya melihat egress pada port 7844; tidak ada port inbound yang dibuka.
* **Arah permintaan:** setelah koneksi tersebut terbentuk, permintaan MCP bergerak **dari Anthropic menuju jaringan Anda** melalui koneksi tersebut, melewati cloudflared ke proxy, dan terus ke server MCP upstream.

Frasa "outbound-only" menggambarkan koneksinya, bukan permintaan yang dibawa melaluinya.

Inner TLS membentang antara backend Anthropic dan proxy Anda. cloudflared dan tunnel edge berada di antara keduanya pada jalur jaringan tetapi hanya melihat ciphertext; proxy adalah tempat pertama di dalam jaringan Anda di mana payload permintaan MCP dapat dibaca.

```mermaid
sequenceDiagram
  participant A as Anthropic<br/>backend
  participant E as Tunnel edge<br/>(Cloudflare network)
  participant C as cloudflared
  participant P as Proxy
  participant M as Upstream<br/>MCP server

  note over C,M: Inside your network

  C->>E: 1. Outbound connection (port 7844)
  note over C,E: Connection stays open.<br/>No inbound port is opened.

  A->>E: 2. MCP request (outer mTLS)
  E->>C: carried over the open connection
  C->>P: localhost:8080
  note over A,P: Inner TLS spans Anthropic backend to proxy.<br/>Terminates at the proxy.
  P->>M: 3. Route by hostname
  M-->>P: response
  P-->>A: response (same path, reversed)
```

## Lihat juga

* [MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/overview) untuk model keamanan dan tabel tanggung jawab bersama.
* [Referensi MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/reference) untuk field konfigurasi proxy, persyaratan sertifikat, dan komponen setup.
