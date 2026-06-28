---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: f1e0c2d24efac58a423a52e72548ed82a7e59dea37ad323a4546bc0c0939696c
---

# Referensi MCP tunnels

Bidang konfigurasi proxy, REST API Tunnels, persyaratan sertifikat, dan komponen setup.

---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

## Konfigurasi proxy

[Proxy](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) membaca konfigurasinya dari `/etc/mcp-gateway/config.yaml` (Compose) atau ConfigMap yang di-render (Helm, diisi dari `gateway.config.*`).

| Bidang                            | Deskripsi                                                                                                                                                                                                                                                     | Default                                           |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `listen_addr`                     | Alamat dan port untuk mendengarkan.                                                                                                                                                                                                                           | Wajib                                             |
| `log_level`                       | Tingkat detail logging: `debug`, `info`, `warn`, atau `error`.                                                                                                                                                                                                | `info`                                            |
| `shutdown_timeout`                | Berapa lama menunggu permintaan yang sedang berjalan selama graceful shutdown.                                                                                                                                                                                | `30s`                                             |
| `tunnel_domain`                   | Domain dasar yang ditetapkan untuk tunnel. Ketika diatur, pencarian rute menghapus sufiks ini dari hostname yang masuk sehingga kunci `routes` dapat berupa subdomain saja (`wiki`). Ketika kosong, kunci `routes` harus berupa hostname lengkap yang persis. | Wajib ketika kunci `routes` berupa subdomain saja |
| `tls.cert_file`                   | Path ke sertifikat TLS server.                                                                                                                                                                                                                                | Wajib                                             |
| `tls.key_file`                    | Path ke kunci privat TLS server.                                                                                                                                                                                                                              | Wajib                                             |
| `routes`                          | Map dari subdomain atau hostname lengkap ke URL upstream. Lihat [Pencocokan rute](#pencocokan-rute).                                                                                                                                                          | Wajib                                             |
| `upstream.allowed_ips`            | Rentang CIDR IPv4 atau alamat tunggal yang diizinkan untuk dihubungi oleh proxy. Saling eksklusif dengan `disable_ip_validation`.                                                                                                                             | Rentang privat RFC1918                            |
| `upstream.disable_ip_validation`  | Menonaktifkan validasi IP upstream sepenuhnya. Saling eksklusif dengan `allowed_ips`.                                                                                                                                                                         | `false`                                           |
| `upstream.tls.ca_file`            | Bundle CA untuk memvalidasi TLS upstream.                                                                                                                                                                                                                     | Tidak ada                                         |
| `upstream.tls.include_system_cas` | Juga mempercayai bundle CA sistem untuk TLS upstream.                                                                                                                                                                                                         | `false`                                           |

Untuk rute upstream `https://`, atur setidaknya salah satu dari `upstream.tls.ca_file` atau `upstream.tls.include_system_cas`; jika tidak, proxy tidak memiliki trust anchor untuk sertifikat upstream.

### Pencocokan rute

`routes` adalah map string datar (`map[string]string`), bukan list. Proxy mencari hostname yang masuk dengan pencocokan persis terlebih dahulu, kemudian dengan menghapus sufiks `tunnel_domain` dan mencocokkan subdomain yang tersisa. Pencocokan hanya mempertimbangkan hostname; path permintaan dan query string diteruskan ke [server MCP upstream](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) tanpa perubahan.

Setiap nilai upstream harus persis berupa `scheme://host:port`. Port bersifat wajib. Menyertakan path akan ditolak saat pemuatan konfigurasi dengan pesan `invalid upstream (must be scheme://host:port)`.

## API Tunnels

Lihat [referensi Admin API MCP tunnels](/docs/id/api/admin/mcp_tunnels) untuk semua endpoint, skema permintaan dan respons, serta contoh per bahasa pemrograman.

<Warning>
  Semua endpoint MCP tunnels memerlukan bearer token dengan scope `org:manage_tunnels` yang diperoleh melalui [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation). Kunci Admin API tidak diterima.
</Warning>

Header yang wajib pada setiap permintaan:

| Header              | Nilai                                         |
| ------------------- | --------------------------------------------- |
| `Authorization`     | `Bearer <token>` (token hasil pertukaran WIF) |
| `anthropic-version` | `2023-06-01`                                  |
| `anthropic-beta`    | `mcp-tunnels-2026-05-19`                      |

## Persyaratan sertifikat

[Komponen setup](/docs/id/agents-and-tools/mcp-tunnels/concepts#components) menghasilkan sertifikat yang sesuai secara otomatis. Persyaratan ini hanya berlaku jika Anda menerbitkan sertifikat melalui PKI Anda sendiri.

### Sertifikat CA

Unggah dengan `POST /v1/organizations/tunnels/{tunnel_id}/certificates`. Sebuah tunnel dapat menyimpan hingga dua sertifikat CA aktif sekaligus, yang memungkinkan rotasi tanpa downtime.

* Dikodekan PEM, sertifikat tunggal, hingga 8 kB.
* Ekstensi `BasicConstraints` ada dengan `CA:TRUE`, ditandai critical.
* Ekstensi `SubjectKeyIdentifier` ada.
* `KeyUsage` mencakup `keyCertSign`.
* Berada dalam periode validitasnya.
* RSA 2048-bit atau lebih besar, atau ECDSA P-256 atau lebih besar, dengan tanda tangan SHA-256 atau lebih kuat.

### Sertifikat server

Disajikan oleh proxy selama [inner TLS](/docs/id/agents-and-tools/mcp-tunnels/concepts#components).

* Ditandatangani langsung oleh CA yang terdaftar (tanpa intermediate).
* Ekstensi `AuthorityKeyIdentifier` ada dan cocok dengan `SubjectKeyIdentifier` milik CA.
* Subject Alternative Name mencakup nama DNS yang cocok dengan `<route>.<tunnel-domain>`. Wildcard `*.<tunnel-domain>` mencakup semua rute.
* Jika ekstensi `ExtendedKeyUsage` ada, ekstensi tersebut mencakup `serverAuth`.
* Berada dalam periode validitasnya.
* RSA 2048-bit atau lebih besar, atau ECDSA P-256 atau lebih besar, dengan tanda tangan SHA-256 atau lebih kuat.

Komponen setup menghasilkan CA ECDSA P-256 dengan validitas lima tahun dan sertifikat server RSA 4096-bit dengan SAN wildcard dan validitas 90 hari.

## Komponen setup

Komponen setup disertakan di dalam image `mcp-proxy` sebagai binary `setup`. Jalankan dengan `docker compose run --rm setup <subcommand>` (Compose) atau andalkan hook dan CronJob dari chart (Helm).

### `setup init`

Menghubungkan ke tunnel yang Anda buat di Console, menghasilkan CA dan sertifikat server, mendaftarkan CA, mengambil token tunnel, dan menulis semua output ke tujuan.

| Flag              | Deskripsi                                                                                                                                                 | Default                                                                                           |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `--api-url`       | URL dasar API Claude. Juga dibaca dari `API_URL`.                                                                                                         | Wajib                                                                                             |
| `--tunnel-id`     | ID tunnel yang akan dihubungkan (`tnl_...`). Juga dibaca dari `TUNNEL_ID`.                                                                                | Wajib                                                                                             |
| `--output`        | Tujuan output: `dir:/path` atau `k8s-secret:NAME`. Chart Helm meneruskan `k8s-secret:<release>`.                                                          | `k8s-secret:mcp-tunnel` (terdeteksi otomatis ketika berjalan di pod Kubernetes; wajib jika tidak) |
| `--cert-duration` | Periode validitas sertifikat server.                                                                                                                      | `2160h` (90 hari)                                                                                 |
| `--token-version` | String deteksi perubahan. Nilai baru memicu rotasi token saat dijalankan ulang. Chart Helm dan contoh Compose keduanya meneruskan `1` sebagai nilai awal. | Tidak ada                                                                                         |

Perintah ini mengautentikasi melalui [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation). Perintah ini membaca `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_WORKSPACE_ID` (opsional), dan tepat salah satu dari `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN`. Lihat [referensi WIF](/docs/id/manage-claude/wif-reference) untuk semantik terkini dari variabel-variabel ini; komponen setup menurunkan service account dari federation rule, sehingga tidak memerlukan `ANTHROPIC_SERVICE_ACCOUNT_ID` secara terpisah.

### `setup renew-cert`

Menerbitkan sertifikat server baru yang ditandatangani oleh CA yang tersimpan. Tidak melakukan panggilan API.

| Flag              | Deskripsi                                                                                        | Default                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `--output`        | Tujuan output: `dir:/path` atau `k8s-secret:NAME`. Chart Helm meneruskan `k8s-secret:<release>`. | `k8s-secret:mcp-tunnel` (terdeteksi otomatis ketika berjalan di pod Kubernetes; wajib jika tidak) |
| `--cert-duration` | Periode validitas sertifikat baru.                                                               | `2160h` (90 hari)                                                                                 |
| `--renew-before`  | Lewati pembaruan jika sertifikat yang ada memiliki sisa durasi lebih dari nilai ini.             | `0` (selalu perbarui)                                                                             |

Mengatur `--renew-before=720h` membuat perintah ini menjadi no-op ketika masih tersisa lebih dari 30 hari validitas, sehingga aman untuk dijalankan pada jadwal tetap.
