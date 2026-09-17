---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/sessions-connect
fetched_at: 2026-09-17T02:21:00.513769Z
sha256: 79c10971a1028dcd7568ea8ea7c1dcdc12974df4e650624b8f2164c6bc7417a4
---

---
title: Terhubung ke sesi Managed Agents dari terminal Anda
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/sessions-connect
description: Hubungkan CLI ant ke sesi Claude Managed Agents untuk mengikuti transkripnya secara langsung, mengirim pesan, mengizinkan atau menolak panggilan alat, atau membuka penampil sesi di browser Anda.
---

`ant beta:sessions connect` menghubungkan terminal Anda ke [sesi](https://platform.claude.com/docs/id/managed-agents/sessions) Claude Managed Agents yang sudah ada. Perintah ini memuat transkrip sesi dan mengikutinya secara langsung saat agen bekerja. Anda juga dapat turun tangan: mengirim pesan, menginterupsi agen, atau mengizinkan maupun menolak "tool call" (panggilan alat) yang sedang menunggu persetujuan. Dengan `--web`, perintah ini justru membuka sesi di penampil sesi Claude Console di browser Anda.

Perintah ini memerlukan CLI versi 1.32.0 atau yang lebih baru. Untuk menginstal atau memperbarui CLI dan melakukan autentikasi, lihat [panduan memulai cepat CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart).

## Terhubung ke sesi

Berikan ID sesi di workspace Anda. Anda dapat menyalinnya dari respons pembuatan, dari `ant beta:sessions list`, atau dari Console.

```bash CLI
ant beta:sessions connect sesn_011CZkZAtmR3yMPDzynEDxu7
```

Tanpa `--web`, perintah ini memerlukan terminal interaktif. Dalam skrip, gunakan `ant beta:sessions:events stream` dan `ant beta:sessions:events send` sebagai gantinya. Lihat [Skrip dan otomatisasi CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting).

Tekan Ctrl+C untuk memutuskan koneksi. Sesi tetap berjalan, dan menghubungkan kembali akan memuat seluruh riwayatnya.

## Mengikuti dan mengarahkan sesi

Tampilan terminal menampilkan percakapan secara langsung: pesan dan panggilan alat, beserta durasi dan hasil setiap panggilan. Bilah status menunjukkan apakah sesi sedang berjalan, idle, atau menunggu persetujuan Anda. Dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), tampilan mengikuti thread utama sesi, yang mencakup pesan yang dipertukarkan koordinator dengan agen-agen yang didelegasikannya.

| Tombol             | Tindakan                                                                                                                                           |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Enter              | Kirim input Anda sebagai event `user.message`. Alt+Enter atau Ctrl+J memulai baris baru.                                                           |
| Esc                | Interupsi agen saat sedang berjalan (`user.interrupt`).                                                                                            |
| Ctrl+O             | Tampilkan atau sembunyikan detail: input dan hasil alat, penggunaan token, dan event status. `--verbose` (`-v`) memulai dengan detail ditampilkan. |
| Page Up, Page Down | Gulir transkrip. Menggulir ke atas menjeda pengikutan; End melanjutkannya.                                                                         |
| Ctrl+C             | Putuskan koneksi. Ctrl+D pada baris input kosong juga memutuskan koneksi.                                                                          |

Saat panggilan alat menunggu persetujuan Anda, baris input berubah menjadi **Allow tool call?** Hal ini terjadi di bawah kebijakan `always_ask`, atau di bawah `auto` ketika server tidak mencapai keputusan. Pilih **Yes**, **No**, atau **No, and tell the agent why**. CLI mengirimkan pilihan Anda sebagai event [`user.tool_confirmation`](https://platform.claude.com/docs/id/managed-agents/permission-policies#respond-to-confirmation-requests), dengan alasan apa pun yang Anda ketik sebagai `deny_message`-nya.

Jika sesi berstatus `terminated` atau telah dihapus, tampilan bersifat hanya-baca.

## Membuka penampil sesi di browser Anda

```bash CLI
ant beta:sessions connect sesn_011CZkZAtmR3yMPDzynEDxu7 --web
```

`--web` menyajikan penampil sesi Console dari server lokal di `127.0.0.1`, mencetak URL-nya, dan membukanya di browser Anda. Tambahkan `--no-browser` untuk melewati pembukaan browser. Anda juga dapat mengirim pesan, menginterupsi agen, dan mengizinkan atau menolak panggilan alat dari browser. Tidak seperti tampilan terminal, penampil browser mengikuti setiap thread dari sesi multiagen.

URL tersebut hanya dapat dibuka satu kali, dalam waktu dua menit setelah dicetak. Memuat ulang tab tersebut tetap berfungsi, tetapi untuk membuka penampil di tempat lain, jalankan perintah lagi. Kredensial Anda tidak pernah meninggalkan CLI: halaman hanya mengirim permintaan ke proses `ant` lokal, yang kemudian membuat permintaan API. Server berjalan hingga Anda menekan Ctrl+C.
