---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 7e3ebe47e753500526b752c94c8f9dc6601633e2524e879016a247a53743747d
---

---
title: Keamanan MCP tunnels
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security
description: Panduan hardening, rotasi kredensial, respons terhadap pelanggaran, dan pembongkaran untuk deployment MCP tunnel.
---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

Arsitektur tunnel menyediakan default yang kuat (konektivitas hanya-keluar, enkripsi end-to-end, dan validasi IP), tetapi keamanan keseluruhan [tunnel stack](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) Anda juga bergantung pada cara Anda mengonfigurasi dan mengoperasikannya. Halaman ini membahas hardening (penguatan keamanan) yang direkomendasikan, respons terhadap pelanggaran, dan cara menonaktifkan tunnel.

## Praktik terbaik

* **Wajibkan OAuth pada setiap server MCP.** Konfigurasikan setiap [server MCP upstream](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) agar mewajibkan OAuth seperti yang dijelaskan dalam [spesifikasi otorisasi MCP](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization). OAuth menyediakan defense in depth (pertahanan berlapis) di atas autentikasi transport tunnel dan memungkinkan otorisasi tingkat pengguna pada lapisan data.
* **Aktifkan SSO untuk organisasi Anda.** Tunnel, aturan federasi, dan service account dikelola di Claude Console. SSO menerapkan kontrol sesi dari penyedia identitas Anda pada admin yang dapat mengubahnya.
* **Batasi `upstream.allowed_ips`.** Gunakan rentang CIDR terkecil yang mencakup server MCP Anda. Ini adalah pertahanan SSRF utama milik [proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components).
* **Pantau log.** Buat peringatan untuk warning, error, dan pola lalu lintas yang tidak biasa dari tunnel stack.
* **Rotasi kredensial.** Rotasi sertifikat server dan token tunnel secara terjadwal, dan segera lakukan jika Anda mencurigai adanya kompromi.
* **Jaga image tetap terbaru.** Pantau rilis proxy baru dan pin image berdasarkan digest SHA-256.
* **Batasi jangkauan jaringan.** Proxy dan [cloudflared](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) seharusnya hanya dapat menjangkau tujuan yang tercantum dalam [persyaratan jaringan](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#network-requirements). Gunakan NetworkPolicy (Kubernetes) atau aturan firewall host (Compose).
* **Batasi cakupan server MCP.** Setiap server seharusnya hanya mengekspos alat dan data yang diperlukan untuk tujuannya.
* **Lindungi kredensial saat disimpan (at rest).** Terapkan praktik manajemen rahasia organisasi Anda pada private key dan token tunnel.

## Merespons dugaan pelanggaran

Jika Anda yakin token tunnel, kunci TLS, atau host proxy Anda telah dikompromikan:

<Steps>
  <Step title="Hentikan tunnel stack">
    <Tabs>
      <Tab title="Helm">
        ```bash
        helm uninstall mcp-tunnel -n mcp-tunnel
        ```
      </Tab>

      <Tab title="Docker Compose">
        ```bash
        docker compose down --timeout 0
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Lepaskan server MCP upstream">
    Hapus server MCP upstream dari sesi Managed Agent mana pun yang menggunakannya, dan berhenti meneruskan URL-nya dalam blok `mcp_servers` pada permintaan Messages API.
  </Step>

  <Step title="Arsipkan tunnel">
    Pengarsipan membatalkan token tunnel dan melepaskan domain. Di Console, [arsipkan tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#archive-a-tunnel) dari daftar **MCP tunnels**. Untuk mengarsipkan melalui API, lihat [Arsipkan tunnel](https://platform.claude.com/docs/id/api/beta/tunnels/archive).
  </Step>

  <Step title="Hubungi Anthropic">
    Laporkan dugaan kompromi tersebut ke dukungan Anthropic.
  </Step>

  <Step title="Rotasi kredensial downstream">
    Sediakan ulang tunnel baru dan rotasi token OAuth apa pun yang diterbitkan oleh server MCP yang terdampak.
  </Step>

  <Step title="Tinjau log sebelum memulihkan layanan">
    Periksa log proxy, cloudflared, dan server MCP untuk rentang waktu dugaan kompromi sebelum mengaktifkan tunnel baru.
  </Step>
</Steps>

## Membongkar tunnel

Ikuti langkah-langkah berikut untuk menonaktifkan tunnel dan menghapus semua kredensial yang tersimpan.

<Steps>
  <Step title="Hentikan tunnel stack">
    <Tabs>
      <Tab title="Helm">
        ```bash
        helm uninstall mcp-tunnel -n mcp-tunnel
        ```
      </Tab>

      <Tab title="Docker Compose">
        ```bash
        docker compose down
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Arsipkan tunnel">
    Di Console, [arsipkan tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#archive-a-tunnel) dari daftar **MCP tunnels**.
  </Step>

  <Step title="Hapus kredensial yang tersimpan">
    <Tabs>
      <Tab title="Helm">
        Dengan akses programatik, komponen setup membuat satu Secret yang dinamai sesuai release. Tanpa akses programatik, Anda membuat `mcp-tunnel-token` dan `mcp-tunnel-cert` sendiri. Hapus mana pun yang berlaku:

        ```bash
        kubectl -n mcp-tunnel delete secret \
          mcp-tunnel mcp-tunnel-token mcp-tunnel-cert \
          --ignore-not-found
        ```
      </Tab>

      <Tab title="Docker Compose">
        Private key dan sertifikat berada di `data/`. Token tunnel berada di `data/tunnel-token` (alur programatik) atau di environment shell Anda (alur manual). Direktori `config/` dan `docker-compose.yaml` tidak berisi rahasia; simpan jika Anda berencana menyediakan ulang, atau hapus juga.

        ```bash
        sudo rm -rf data
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
