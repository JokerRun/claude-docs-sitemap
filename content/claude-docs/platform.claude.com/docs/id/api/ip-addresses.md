---
source: platform
url: https://platform.claude.com/docs/id/api/ip-addresses
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 6d0edf8dfd95c4687f0ff78883e9f70837f60f6a6c813a961695f4f679538971
---

# Alamat IP

Layanan Anthropic menggunakan alamat IP tetap untuk koneksi masuk dan keluar. Anda dapat menggunakan alamat-alamat ini untuk mengonfigurasi aturan firewall Anda untuk akses aman ke Claude API dan Console. Alamat-alamat ini tidak akan berubah tanpa pemberitahuan.

---

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

### Alamat IP yang sudah dihentikan

Alamat IP berikut tidak lagi digunakan oleh Anthropic. Jika Anda sebelumnya telah memasukkan alamat-alamat ini ke daftar izin, Anda harus menghapusnya dari aturan firewall Anda.

```text
34.162.46.92/32
34.162.102.82/32
34.162.136.91/32
34.162.142.92/32
34.162.183.95/32
```