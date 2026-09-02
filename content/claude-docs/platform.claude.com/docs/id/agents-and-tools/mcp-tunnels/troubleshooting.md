---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: d2d526b83962822d4babb5b9572ac91218eb27a7187eac7c5df1696760f636bf
---

---
title: Memecahkan masalah tunnel MCP
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting
description: Mendiagnosis masalah konektivitas, TLS, validasi IP, dan perutean OAuth dalam stack tunnel.
---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

Sebuah permintaan melalui tunnel dapat gagal di salah satu dari tiga lapisan; diagnosis secara berurutan: koneksi keluar ke [tunnel edge](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components), [inner TLS](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) dari Anthropic ke [proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) Anda, lalu perutean dan validasi IP menuju [server MCP upstream](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components).

## Referensi cepat

| Gejala                                                                                                                                                                       | Penyebab                                                                                                  | Perbaikan                                                                                                                                                                      |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tunnel tidak muncul di pemilih **+ MCP Server** agen                                                                                                                         | Pemilih hanya menampilkan tunnel di workspace sesi yang memiliki setidaknya satu sertifikat aktif.        | Daftarkan sertifikat CA, atau buka sesi di workspace tempat tunnel dibuat.                                                                                                     |
| Pemanggil melihat HTTP 500; [cloudflared](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) mencatat log `No ingress rules were defined` | cloudflared tidak memiliki target lokal.                                                                  | Tambahkan `--url http://localhost:8080` dan `network_mode: "service:mcp-proxy"` ke layanan cloudflared.                                                                        |
| Proxy mencatat log `no route for host`                                                                                                                                       | `tunnel_domain` tidak cocok dengan domain yang ditetapkan, atau `config.yaml` diedit tanpa memulai ulang. | Atur `tunnel_domain` ke domain persis yang ditampilkan di halaman detail tunnel, lalu mulai ulang proxy (`docker compose restart mcp-proxy`).                                  |
| Proxy mencatat log `IP validation failed: <ip> is not a private address`                                                                                                     | Server MCP upstream ter-resolve di luar RFC1918.                                                          | Lihat [Validasi IP upstream](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/troubleshooting#upstream-ip-validation).                                         |
| Proxy keluar dengan `cannot unmarshal !!seq into map[string]string`                                                                                                          | `routes` berupa list YAML.                                                                                | Gunakan `routes: { name: http://host:port }`.                                                                                                                                  |
| Proxy keluar dengan `open /data/tls.key: permission denied`                                                                                                                  | Kunci memiliki izin `0600`; container proxy berjalan sebagai non-root.                                    | `chmod 644 data/tls.key`.                                                                                                                                                      |
| `curl https://<proxy>:8080` gagal dengan `wrong version number`                                                                                                              | Sesuai harapan; listener berupa WebSocket plaintext. TLS terjadi di dalam stream WS.                      | Verifikasi melalui [Managed Agent atau Messages API](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers) sebagai gantinya. |

Bagian-bagian berikut membahas kegagalan yang memerlukan lebih dari perbaikan satu baris.

## OAuth gagal di balik allowlist IP sumber

Alur OAuth gagal ketika allowlist IP sumber pada server otorisasi Anda memblokir backend Anthropic dari menjangkau `/token`, `/register`, dan endpoint discovery. Jika Anda lebih memilih untuk tidak memasukkan rentang egress Anthropic ke allowlist, Anda dapat merutekan panggilan OAuth backend-ke-backend melalui tunnel sambil tetap mempertahankan endpoint `/authorize` yang menghadap browser pada hostname publik Anda yang sudah ada.

<Steps>
  <Step title="Tambahkan rute proxy untuk server otorisasi">
    ```yaml
    routes:
      mcp: http://your-mcp-server:8080
      auth: http://your-auth-server:8080
    ```

    Mulai ulang proxy setelah mengedit `routes` (`docker compose restart mcp-proxy`, atau `helm upgrade`).
  </Step>

  <Step title="Sajikan metadata discovery dengan endpoint terpisah">
    Respons `/.well-known/oauth-authorization-server` dari server otorisasi Anda harus mengarahkan `authorization_endpoint` ke hostname Anda yang sudah ada di allowlist dan semua yang lainnya ke tunnel:

    ```json
    {
      "issuer": "https://auth.<tunnel-domain>",
      "authorization_endpoint": "https://<your-allowlisted-host>/authorize",
      "token_endpoint": "https://auth.<tunnel-domain>/token",
      "registration_endpoint": "https://auth.<tunnel-domain>/register",
      "code_challenge_methods_supported": ["S256"]
    }
    ```
  </Step>

  <Step title="Arahkan server MCP ke issuer tunnel">
    Respons `/.well-known/oauth-protected-resource` dari server MCP Anda harus mereferensikan hostname tunnel sebagai server otorisasinya:

    ```json
    {
      "resource": "https://mcp.<tunnel-domain>",
      "authorization_servers": ["https://auth.<tunnel-domain>"]
    }
    ```
  </Step>
</Steps>

Dengan konfigurasi ini, browser pengguna mengakses `/authorize` pada hostname Anda yang sudah ada (yang sudah diizinkan oleh allowlist Anda), sementara backend Anthropic menjangkau `/token`, `/register`, dan dokumen discovery melalui tunnel.

## Kegagalan autentikasi komponen setup

[Komponen setup](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) (Helm Job atau layanan `setup` Compose) melakukan autentikasi ke Tunnels API dengan menukarkan JWT OIDC melalui aturan federasi Anda. Ketika penukaran gagal, lihat [Memecahkan masalah penukaran yang gagal](https://platform.claude.com/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange) dalam referensi Workload Identity Federation; mode kegagalannya (subject, audience, issuer, JWKS, lifetime) sama.

Penyebab khusus Tunnels:

* Audience default chart adalah `api.anthropic.com` (tanpa skema). Jika audience aturan Anda adalah `https://api.anthropic.com`, atur `api.wif.audience` agar cocok.
* Respons `403` dari Tunnels API setelah penukaran berhasil berarti scope aturan tidak mencakup `workspace:manage_tunnels`, atau service account aturan tersebut bukan anggota workspace tunnel. Atur scope dan tambahkan service account ke workspace.

Pada Helm, komponen setup berjalan sebagai Job hook pre-install. Saat gagal, Job dibiarkan untuk diperiksa (`kubectl logs job/mcp-tunnel-setup -n mcp-tunnel`). Helm tidak mengelola resource hook, jadi hapus Job tersebut sebelum mencoba lagi:

```bash
helm uninstall mcp-tunnel -n mcp-tunnel
kubectl -n mcp-tunnel delete job mcp-tunnel-setup
```

## Tunnel tidak mau terhubung

Periksa log cloudflared terlebih dahulu. Penyebab umum:

* `TUNNEL_TOKEN` tidak ada, kedaluwarsa, atau disalin dengan tidak benar.
* Firewall memblokir TCP/UDP keluar pada port 7844 ke tunnel edge.

cloudflared juga mungkin mencatat peringatan tentang ukuran buffer penerimaan UDP; ini adalah petunjuk penyetelan QUIC, bukan error.

## Error sertifikat

Ketika Anthropic menolak sertifikat proxy selama inner TLS, proxy mencatat log `tls handshake failed`. Verifikasi bahwa:

* Sertifikat server belum kedaluwarsa.
* Subject Alternative Name sertifikat cocok dengan `*.<tunnel-domain>`.
* CA penandatangan terdaftar di Anthropic untuk tunnel ini.

Lihat [persyaratan sertifikat](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#certificate-requirements) untuk aturan validasi lengkap.

## Validasi IP upstream

Untuk perlindungan SSRF, proxy secara default hanya menghubungi alamat dalam rentang privat RFC1918 (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`). Hanya IPv4 yang didukung untuk koneksi proxy-ke-upstream. (Rentang egress cloudflared-ke-edge di [Persyaratan jaringan](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#network-requirements) adalah hop yang berbeda.)

Jika proxy mencatat log `IP validation failed: <ip> is not a private address`, hostname upstream ter-resolve di luar rentang tersebut. Pada Kubernetes, beberapa distribusi terkelola mengalokasikan Service CIDR di luar RFC1918; jika `kubectl get svc kubernetes -n default -o jsonpath='{.spec.clusterIP}'` mengembalikan alamat di luar rentang privat, cari Service CIDR cluster Anda dan tambahkan.

Jika alamat tersebut sah, tambahkan CIDR pencakup yang paling sempit ke `upstream.allowed_ips`. Mengatur `allowed_ips` **menggantikan** default RFC1918 alih-alih memperluasnya, jadi sertakan rentang privat yang digunakan oleh server MCP upstream Anda yang lain:

```yaml config/mcp-proxy.yaml
upstream:
  allowed_ips:
    - 10.0.0.0/8
    - 172.16.0.0/12
    - 192.168.0.0/16
    - 127.0.0.0/8       # loopback, for local testing only
```

<Warning>
  Hindari `0.0.0.0/0` di luar pengujian lokal; ini menonaktifkan perlindungan SSRF sepenuhnya.
</Warning>
