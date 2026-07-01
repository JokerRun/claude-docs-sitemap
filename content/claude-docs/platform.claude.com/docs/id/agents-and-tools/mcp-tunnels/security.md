---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: e370b78ce019a4d63e50025c306a92f96790ee231891fa897a7f39d7f182a261
---

# Keamanan tunnel MCP

Panduan penguatan keamanan, rotasi kredensial, respons terhadap pelanggaran, dan pembongkaran untuk deployment tunnel MCP.

---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

Arsitektur tunnel menyediakan pengaturan default yang kuat (konektivitas hanya keluar, enkripsi end-to-end, dan validasi IP), tetapi keamanan keseluruhan dari [tunnel stack](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) Anda juga bergantung pada cara Anda mengonfigurasi dan mengoperasikannya. Halaman ini membahas penguatan keamanan yang direkomendasikan, respons terhadap pelanggaran, dan cara menonaktifkan tunnel.

## Praktik terbaik

* **Wajibkan OAuth pada setiap server MCP.** Konfigurasikan setiap [server MCP upstream](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) untuk mewajibkan OAuth seperti yang dijelaskan dalam [spesifikasi otorisasi MCP](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization). OAuth memberikan pertahanan berlapis di atas autentikasi transport tunnel dan memungkinkan otorisasi tingkat pengguna pada lapisan data.
* **Aktifkan SSO untuk organisasi Anda.** Tunnel, aturan federasi, dan akun layanan dikelola di Claude Console. SSO menerapkan kontrol sesi dari penyedia identitas Anda pada admin yang dapat mengubahnya.
* **Batasi `upstream.allowed_ips`.** Gunakan rentang CIDR terkecil yang mencakup server MCP Anda. Ini adalah pertahanan SSRF utama dari [proxy](/docs/id/agents-and-tools/mcp-tunnels/concepts#components).
* **Pantau log.** Buat peringatan untuk warning, error, dan pola lalu lintas yang tidak biasa dari tunnel stack.
* **Rotasi kredensial.** Lakukan rotasi sertifikat server dan token tunnel secara berkala, dan segera lakukan jika Anda mencurigai adanya kompromi.
* **Jaga image tetap diperbarui.** Pantau rilis proxy baru dan pin image berdasarkan digest SHA-256.
* **Batasi jangkauan jaringan.** Proxy dan [cloudflared](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) seharusnya hanya dapat menjangkau tujuan yang tercantum dalam [persyaratan jaringan](/docs/id/agents-and-tools/mcp-tunnels/overview#network-requirements). Gunakan NetworkPolicy (Kubernetes) atau aturan firewall host (Compose).
* **Batasi cakupan server MCP.** Setiap server seharusnya hanya mengekspos alat dan data yang diperlukan untuk tujuannya.
* **Lindungi kredensial saat disimpan.** Terapkan praktik manajemen rahasia organisasi Anda pada kunci privat dan token tunnel.

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
    Pengarsipan akan membatalkan token tunnel dan melepaskan domain. Di Console, [arsipkan tunnel](/docs/id/agents-and-tools/mcp-tunnels/console#archive-a-tunnel) dari daftar **MCP tunnels**. Untuk mengarsipkan melalui API, lihat [Archive a tunnel](/docs/id/api/beta/tunnels/archive).
  </Step>

  <Step title="Hubungi Anthropic">
    Laporkan dugaan kompromi tersebut ke dukungan Anthropic.
  </Step>

  <Step title="Rotasi kredensial downstream">
    Sediakan ulang tunnel baru dan lakukan rotasi pada semua token OAuth yang diterbitkan oleh server MCP yang terdampak.
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
    Di Console, [arsipkan tunnel](/docs/id/agents-and-tools/mcp-tunnels/console#archive-a-tunnel) dari daftar **MCP tunnels**.
  </Step>

  <Step title="Hapus kredensial yang tersimpan">
    <Tabs>
      <Tab title="Helm">
        Dengan akses terprogram, komponen setup membuat satu Secret yang dinamai sesuai release. Tanpa akses terprogram, Anda membuat `mcp-tunnel-token` dan `mcp-tunnel-cert` sendiri. Hapus mana pun yang berlaku:

        ```bash
        kubectl -n mcp-tunnel delete secret \
          mcp-tunnel mcp-tunnel-token mcp-tunnel-cert \
          --ignore-not-found
        ```
      </Tab>

      <Tab title="Docker Compose">
        Kunci privat dan sertifikat berada di `data/`. Token tunnel berada di `data/tunnel-token` (alur terprogram) atau di environment shell Anda (alur manual). Direktori `config/` dan `docker-compose.yaml` tidak berisi rahasia; simpan jika Anda berencana untuk menyediakan ulang, atau hapus juga.

        ```bash
        sudo rm -rf data
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
