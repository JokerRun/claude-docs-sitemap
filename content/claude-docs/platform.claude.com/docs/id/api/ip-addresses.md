---
source: platform
url: https://platform.claude.com/docs/id/api/ip-addresses
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: b27ad7131b5e45516582064f4c6a447b14919cc2501cf379d4295a9607972aa5
---

---
title: Alamat IP
url: https://platform.claude.com/docs/id/api/ip-addresses
description: Layanan Anthropic menggunakan alamat IP tetap untuk koneksi masuk dan keluar. Anda dapat menggunakan alamat-alamat ini untuk mengonfigurasi aturan firewall Anda demi akses yang aman ke Claude API dan Console. Alamat-alamat ini tidak akan berubah tanpa pemberitahuan.
---

<Note>
  **[Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Endpoint masuk (`aws-external-anthropic.{region}.api.aws`) me-resolve ke rentang IP AWS. Panggilan alat keluar (MCP connector, web search, dan web fetch) berasal dari rentang Anthropic yang tercantum di halaman ini. Lihat [rentang alamat IP AWS](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html) untuk allowlisting koneksi masuk.
</Note>

## Alamat IP masuk

Ini adalah alamat IP tempat layanan Anthropic menerima koneksi masuk.

### IPv4

`160.79.104.0/23`

### IPv6

`2607:6bc0::/48`

## Alamat IP keluar

Ini adalah alamat IP stabil yang digunakan Anthropic untuk permintaan keluar (misalnya, saat melakukan panggilan alat MCP ke server eksternal).

### IPv4

`160.79.104.0/21`

### Alamat IP yang sudah tidak digunakan

Alamat IP berikut tidak lagi digunakan oleh Anthropic. Jika Anda sebelumnya telah memasukkan alamat-alamat ini ke dalam allowlist, Anda harus menghapusnya dari aturan firewall Anda.

```text wrap
34.162.46.92/32
34.162.102.82/32
34.162.136.91/32
34.162.142.92/32
34.162.183.95/32
```
