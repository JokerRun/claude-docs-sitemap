---
source: platform
url: https://platform.claude.com/docs/id/api/ip-addresses
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: d55db8dcceb967f5552e1ff20429bcd0e11a1b52197770b264480fb93024fcc2
---

---
title: Alamat IP
url: https://platform.claude.com/docs/id/api/ip-addresses
description: Layanan Anthropic menggunakan alamat IP tetap untuk koneksi masuk maupun keluar. Anda dapat menggunakan alamat-alamat ini untuk mengonfigurasi aturan firewall Anda agar dapat mengakses Claude API dan Console dengan aman. Alamat-alamat ini tidak akan berubah tanpa pemberitahuan.
---

<Note>
  **[Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Endpoint masuk (`aws-external-anthropic.{region}.api.aws`) di-resolve ke rentang IP AWS. Panggilan alat keluar (konektor MCP, web search, dan web fetch) berasal dari rentang Anthropic yang tercantum di halaman ini. Lihat [rentang alamat IP AWS](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html) untuk allowlisting koneksi masuk.
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

Alamat IP berikut tidak lagi digunakan oleh Anthropic. Jika Anda sebelumnya telah memasukkan alamat-alamat ini ke dalam allowlist, Anda sebaiknya menghapusnya dari aturan firewall Anda.

```text wrap
34.162.46.92/32
34.162.102.82/32
34.162.136.91/32
34.162.142.92/32
34.162.183.95/32
```
