---
source: platform
url: https://platform.claude.com/docs/id/get-api-key
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 309ba16800554340b5aa28fc201886e20a7ab20b6188babe173a321010595942
---

---
title: Dapatkan kunci API Claude Anda
url: https://platform.claude.com/docs/id/get-api-key
description: Temukan, buat, dan kelola kunci API Anda untuk Claude API di Claude Console.
---

"API key" (kunci API) untuk Claude API (juga disebut kunci API Anthropic) berada di Claude Console. Untuk melihat kunci yang sudah ada atau membuat yang baru, buka [Settings → API keys](https://platform.claude.com/settings/keys).

## Membuat kunci API

<Steps>
  <Step title="Masuk ke Claude Console">
    Buka [platform.claude.com](https://platform.claude.com/) dan masuk, atau buat akun jika Anda belum memilikinya.
  </Step>

  <Step title="Buka halaman API keys">
    Buka [Settings → API keys](https://platform.claude.com/settings/keys).
  </Step>

  <Step title="Buat kunci">
    Klik **Create key**, lalu beri nama pada kunci tersebut. Anda juga dapat memilih [workspace](https://platform.claude.com/settings/workspaces) untuk membatasi cakupan kunci, serta masa kedaluwarsa.
  </Step>

  <Step title="Salin dan simpan kunci">
    Console menampilkan kunci lengkap, yang dimulai dengan `sk-ant-`, hanya satu kali, yaitu saat pembuatan. Salin dan simpan di tempat yang aman, seperti secrets manager. Jika Anda kehilangan kunci, Anda tidak dapat melihatnya lagi di Console. Sebagai gantinya, buat kunci baru.
  </Step>
</Steps>

Jika tombol **Create key** dinonaktifkan, Anda mungkin tidak memiliki izin untuk membuat kunci di workspace tersebut. Minta admin organisasi untuk memberi Anda akses atau membuatkan kunci untuk Anda.

## Menggunakan kunci API Anda

Atur kunci sebagai variabel lingkungan:

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

[SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) membaca `ANTHROPIC_API_KEY` secara otomatis. Permintaan HTTP langsung mengirimkan kunci di header `x-api-key`. Untuk membuat permintaan pertama Anda, ikuti [Quickstart](https://platform.claude.com/docs/id/get-started), dan lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication) untuk gambaran lengkapnya, termasuk kredensial berumur pendek dengan Workload Identity Federation.

## Kunci API dan Admin API

[Admin API](https://platform.claude.com/docs/id/api/admin) mencakup endpoint untuk mengelola kunci API organisasi Anda secara terprogram, seperti [Retrieve API Key](https://platform.claude.com/docs/id/api/admin/api_keys/retrieve) dan [List API Keys](https://platform.claude.com/docs/id/api/admin/api_keys/list). Endpoint ini ditujukan bagi admin organisasi yang mengotomatiskan pengelolaan kunci. Endpoint tersebut memerlukan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys) yang terpisah, dan tidak pernah mengembalikan nilai rahasia sebuah kunci, hanya petunjuk yang sebagian disamarkan.

<Note>
  Admin API tidak dapat memulihkan kunci yang hilang atau memberi Anda kunci untuk memanggil Claude API. Untuk mendapatkan kunci API yang dapat digunakan, buat satu di [Settings → API keys](https://platform.claude.com/settings/keys) di Claude Console.
</Note>
