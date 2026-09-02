---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 965bca20f12455980cc93e54a6494b232d58cd2b2ad5d27139ef786094b3b77b
---

---
title: Referensi MCP tunnels
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference
description: Field konfigurasi proxy, Tunnels REST API, persyaratan sertifikat, dan komponen setup.
---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

## Konfigurasi proxy

[Proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) membaca konfigurasinya dari `/etc/mcp-gateway/config.yaml` (Compose) atau ConfigMap yang telah di-render (Helm, diisi dari `gateway.config.*`).

| Field                             | Deskripsi                                                                                                                                                                                                                                                 | Default                                         |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `listen_addr`                     | Alamat dan port untuk mendengarkan.                                                                                                                                                                                                                       | Wajib                                           |
| `log_level`                       | Tingkat verbositas logging: `debug`, `info`, `warn`, atau `error`.                                                                                                                                                                                        | `info`                                          |
| `shutdown_timeout`                | Berapa lama menunggu permintaan yang sedang berjalan selama graceful shutdown.                                                                                                                                                                            | `30s`                                           |
| `tunnel_domain`                   | Domain dasar yang ditetapkan untuk tunnel. Jika diatur, pencarian rute menghapus sufiks ini dari hostname yang masuk sehingga kunci `routes` dapat berupa subdomain saja (`wiki`). Jika kosong, kunci `routes` harus berupa hostname lengkap yang persis. | Wajib jika kunci `routes` berupa subdomain saja |
| `tls.cert_file`                   | Path ke sertifikat TLS server.                                                                                                                                                                                                                            | Wajib                                           |
| `tls.key_file`                    | Path ke private key TLS server.                                                                                                                                                                                                                           | Wajib                                           |
| `routes`                          | Peta dari subdomain atau hostname lengkap ke URL upstream. Lihat [Pencocokan rute](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#route-matching).                                                                            | Wajib                                           |
| `upstream.allowed_ips`            | Rentang CIDR IPv4 atau alamat tunggal yang diizinkan untuk dihubungi oleh proxy. Saling eksklusif dengan `disable_ip_validation`.                                                                                                                         | Rentang privat RFC1918                          |
| `upstream.disable_ip_validation`  | Menonaktifkan validasi IP upstream sepenuhnya. Saling eksklusif dengan `allowed_ips`.                                                                                                                                                                     | `false`                                         |
| `upstream.tls.ca_file`            | Bundle CA untuk memvalidasi TLS upstream.                                                                                                                                                                                                                 | Tidak ada                                       |
| `upstream.tls.include_system_cas` | Juga mempercayai bundle CA sistem untuk TLS upstream.                                                                                                                                                                                                     | `false`                                         |

Untuk rute upstream `https://`, atur setidaknya salah satu dari `upstream.tls.ca_file` atau `upstream.tls.include_system_cas`; jika tidak, proxy tidak memiliki trust anchor untuk sertifikat upstream.

### Pencocokan rute

`routes` adalah peta string datar (`map[string]string`), bukan daftar. Proxy mencari hostname yang masuk dengan pencocokan persis terlebih dahulu, lalu dengan menghapus sufiks `tunnel_domain` dan mencocokkan subdomain yang tersisa. Pencocokan hanya mempertimbangkan hostname; path permintaan dan query string diteruskan ke [server MCP upstream](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) tanpa perubahan.

Setiap nilai upstream harus persis berbentuk `scheme://host:port`. Port bersifat wajib. Menyertakan path akan ditolak saat pemuatan konfigurasi dengan `invalid upstream (must be scheme://host:port)`.

## Tunnels API

Tunnels REST API berada di `/v1/tunnels` dan mendukung pembuatan, pencantuman, dan pengarsipan tunnel, pendaftaran sertifikat CA, serta pengungkapan atau rotasi token tunnel. Lihat [referensi Tunnels API](https://platform.claude.com/docs/id/api/beta/tunnels/list) untuk semua endpoint, skema permintaan dan respons, serta contoh.

<Note>
  Permukaan Admin API sebelumnya di `/v1/organizations/tunnels` (header beta `mcp-tunnels-2026-05-19`, scope `org:manage_tunnels`) tetap berfungsi selama periode migrasi dan tetap didokumentasikan di [referensi Admin API](https://platform.claude.com/docs/id/api/admin/mcp_tunnels) dengan pemberitahuan deprecation. Untuk bermigrasi, perbarui path menjadi `/v1/tunnels`, header beta menjadi `mcp-tunnels-2026-06-22`, dan scope token WIF Anda menjadi `workspace:manage_tunnels`.
</Note>

<Warning>
  Semua endpoint MCP tunnels memerlukan bearer token dengan scope `workspace:manage_tunnels` yang diperoleh melalui [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Kunci API Admin tidak diterima.
</Warning>

Header yang wajib pada setiap permintaan:

| Header              | Nilai                                         |
| ------------------- | --------------------------------------------- |
| `Authorization`     | `Bearer <token>` (token hasil pertukaran WIF) |
| `anthropic-version` | `2023-06-01`                                  |
| `anthropic-beta`    | `mcp-tunnels-2026-06-22`                      |

## Persyaratan sertifikat

[Komponen setup](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) menghasilkan sertifikat yang sesuai secara otomatis. Persyaratan ini hanya berlaku jika Anda menerbitkan sertifikat melalui PKI Anda sendiri.

### Sertifikat CA

Unggah dengan `POST /v1/tunnels/{tunnel_id}/certificates`. Sebuah tunnel dapat menampung hingga dua sertifikat CA aktif sekaligus, yang memungkinkan rotasi tanpa downtime.

* Berenkode PEM, sertifikat tunggal, hingga 8 kB.
* Ekstensi `BasicConstraints` ada dengan `CA:TRUE`, ditandai critical.
* Ekstensi `SubjectKeyIdentifier` ada.
* `KeyUsage` mencakup `keyCertSign`.
* Berada dalam masa berlakunya.
* RSA 2048-bit atau lebih besar, atau ECDSA P-256 atau lebih besar, dengan tanda tangan SHA-256 atau lebih kuat.

### Sertifikat server

Disajikan oleh proxy selama [inner TLS](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components).

* Ditandatangani langsung oleh CA yang terdaftar (tanpa intermediate).
* Ekstensi `AuthorityKeyIdentifier` ada dan cocok dengan `SubjectKeyIdentifier` milik CA.
* Subject Alternative Name mencakup nama DNS yang cocok dengan `<route>.<tunnel-domain>`. Wildcard `*.<tunnel-domain>` mencakup semua rute.
* Jika ekstensi `ExtendedKeyUsage` ada, ekstensi tersebut mencakup `serverAuth`.
* Berada dalam masa berlakunya.
* RSA 2048-bit atau lebih besar, atau ECDSA P-256 atau lebih besar, dengan tanda tangan SHA-256 atau lebih kuat.

Komponen setup menghasilkan CA ECDSA P-256 dengan masa berlaku lima tahun dan sertifikat server RSA 4096-bit dengan SAN wildcard dan masa berlaku 90 hari.

## Komponen setup

Komponen setup dikirimkan di dalam image `mcp-proxy` sebagai binary `setup`. Jalankan dengan `docker compose run --rm setup <subcommand>` (Compose) atau andalkan hook dan CronJob milik chart (Helm).

### `setup init`

Menghubungkan ke tunnel yang sudah ada (atau membuat tunnel baru jika tidak ada ID tunnel yang diberikan), lalu menghasilkan CA dan sertifikat server, mendaftarkan CA, mengambil token tunnel, dan menulis semua output ke tujuan.

| Flag              | Deskripsi                                                                                                                                                                                                    | Default                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| `--api-url`       | URL dasar Claude API. Juga dibaca dari `API_URL`.                                                                                                                                                            | Wajib                                                                                           |
| `--tunnel-id`     | ID tunnel yang akan dihubungkan (`tnl_...`). Juga dibaca dari `TUNNEL_ID`. Jika dihilangkan, tunnel baru akan dibuat; ID tunnel yang sudah tersimpan di output akan digunakan kembali saat dijalankan ulang. | Tidak ada (membuat tunnel)                                                                      |
| `--output`        | Tujuan output: `dir:/path` atau `k8s-secret:NAME`. Chart Helm meneruskan `k8s-secret:<release>`.                                                                                                             | `k8s-secret:mcp-tunnel` (terdeteksi otomatis saat berjalan di pod Kubernetes; wajib jika tidak) |
| `--cert-duration` | Masa berlaku sertifikat server.                                                                                                                                                                              | `2160h` (90 hari)                                                                               |
| `--token-version` | String pendeteksi perubahan. Nilai baru memicu rotasi token saat dijalankan ulang. Chart Helm dan contoh Compose sama-sama meneruskan `1` sebagai nilai awal.                                                | Tidak ada                                                                                       |

Perintah ini melakukan autentikasi melalui [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Perintah ini membaca `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_WORKSPACE_ID` (opsional), dan tepat salah satu dari `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN`. Lihat [referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference) untuk semantik terkini dari variabel-variabel ini; komponen setup menurunkan service account dari federation rule, sehingga tidak memerlukan `ANTHROPIC_SERVICE_ACCOUNT_ID` secara terpisah.

### `setup renew-cert`

Menerbitkan sertifikat server baru yang ditandatangani oleh CA yang tersimpan. Tidak melakukan panggilan API.

| Flag              | Deskripsi                                                                                        | Default                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| `--output`        | Tujuan output: `dir:/path` atau `k8s-secret:NAME`. Chart Helm meneruskan `k8s-secret:<release>`. | `k8s-secret:mcp-tunnel` (terdeteksi otomatis saat berjalan di pod Kubernetes; wajib jika tidak) |
| `--cert-duration` | Masa berlaku sertifikat baru.                                                                    | `2160h` (90 hari)                                                                               |
| `--renew-before`  | Lewati pembaruan jika sertifikat yang ada memiliki sisa masa berlaku lebih dari durasi ini.      | `0` (selalu perbarui)                                                                           |

Mengatur `--renew-before=720h` membuat perintah ini menjadi no-op ketika sisa masa berlaku lebih dari 30 hari, sehingga aman untuk dijalankan pada jadwal tetap.
