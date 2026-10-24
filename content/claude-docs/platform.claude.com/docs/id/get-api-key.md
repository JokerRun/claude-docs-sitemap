---
source: platform
url: https://platform.claude.com/docs/id/get-api-key
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: 0876cef1ba4a63703cd5ea85799aabb559935b9b6b538bd17470e30b90e1e986
---

---
title: Dapatkan kunci API Claude Anda
url: https://platform.claude.com/docs/id/get-api-key
description: Temukan, buat, dan kelola kunci API Anda untuk Claude API di Claude Console.
---

Kunci API untuk Claude API (juga disebut kunci API Anthropic) berada di Claude Console. Untuk melihat kunci yang sudah ada atau membuat kunci baru, buka halaman [API keys](https://platform.claude.com/settings/keys) (`platform.claude.com/settings/keys`) di Console.

## Pilih jenis kunci

Saat membuat kunci, Anda memilih jenisnya, yang menentukan apa yang dapat dilakukan kunci tersebut, di mana kunci itu berfungsi, dan kapan kunci itu berhenti berfungsi. **Kunci pribadi** bertindak sebagai Anda, dan berhenti berfungsi jika Anda keluar dari suatu organisasi. **Kunci akun layanan** mewakili sebuah [akun layanan](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#service-accounts), yang dapat digunakan oleh workload seperti pipeline CI, layanan produksi, atau agen. Gunakan kunci pribadi untuk pengembangan Anda sendiri, dan kunci akun layanan untuk apa pun yang digunakan bersama.

Anda juga dapat membuat **kunci workspace** (workspace key), yaitu kunci lama (legacy) tanpa pemilik: kunci ini milik workspace tempat Anda membuatnya dan tetap berfungsi setelah pembuatnya meninggalkan organisasi. Lebih disarankan untuk menggunakan kunci pribadi atau kunci akun layanan, karena kunci-kunci ini berhenti berfungsi secara otomatis ketika akun yang terkait dihapus dari organisasi.

## Buat kunci API

<Steps>
  <Step title="Masuk ke Claude Console">
    Buka Claude Console di [platform.claude.com](https://platform.claude.com/) dan masuk, atau buat akun jika Anda belum memilikinya.
  </Step>

  <Step title="Buka halaman API keys">
    Di Claude Console, buka halaman [API keys](https://platform.claude.com/settings/keys) (`platform.claude.com/settings/keys`).
  </Step>

  <Step title="Buat kunci">
    Klik **Create key**, beri nama kunci, pilih [masa kedaluwarsa](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration), dan atur **Linked account** ke diri Anda sendiri atau ke akun layanan. Anda juga dapat memilih [workspace](https://platform.claude.com/settings/workspaces) di Console untuk membatasi cakupan kunci.
  </Step>

  <Step title="Salin dan simpan kunci">
    Console menampilkan kunci lengkap, yang diawali dengan `sk-ant-`, hanya sekali, yaitu saat pembuatan. Salin dan simpan di tempat yang aman, seperti pengelola rahasia (secrets manager). Jika Anda kehilangan kunci, Anda tidak dapat melihatnya lagi di Console. Sebagai gantinya, buat kunci baru.
  </Step>
</Steps>

Jika tombol **Create key** di halaman kunci API dinonaktifkan, peran Anda mungkin tidak mengizinkan Anda membuat kunci di sana. Mintalah admin organisasi untuk mengubah peran Anda, atau untuk membuat kunci akun layanan untuk workload Anda.

## Gunakan kunci API Anda

Atur kunci sebagai variabel lingkungan:

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

[Client SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) membaca `ANTHROPIC_API_KEY` secara otomatis. Permintaan HTTP langsung mengirim kunci sebagai `Authorization: Bearer <key>`. Jika kunci API Anda tidak dibatasi ke suatu workspace, Anda juga harus mengirim header `anthropic-workspace-id` pada setiap permintaan Claude API, seperti yang ditunjukkan di [Memilih workspace](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace). Untuk Admin API, lihat [Kunci API dan Admin API](https://platform.claude.com/docs/id/get-api-key#api-keys-and-the-admin-api).

Untuk membuat permintaan pertama Anda, ikuti [Panduan Memulai Cepat](https://platform.claude.com/docs/id/get-started), dan lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication) untuk detail lengkap, termasuk kredensial berumur pendek dengan Workload Identity Federation.

## Kunci API dan Admin API

[Admin API](https://platform.claude.com/docs/id/api/organization) menyertakan endpoint untuk mengelola kunci API organisasi Anda secara terprogram, seperti [Retrieve API Key](https://platform.claude.com/docs/id/api/organization/api_keys/retrieve) dan [List API Keys](https://platform.claude.com/docs/id/api/organization/api_keys/list). Endpoint ini ditujukan bagi admin organisasi yang mengotomatiskan pengelolaan kunci. Endpoint ini menerima [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys), token OAuth dengan cakupan `org:admin`, atau kunci pribadi maupun kunci akun layanan yang tidak dibatasi pada workspace tertentu; kunci workspace tidak berfungsi di sana. Endpoint ini tidak pernah mengembalikan nilai rahasia kunci, hanya petunjuk yang sebagian disamarkan.

<Note>
  Admin API tidak dapat memulihkan kunci yang hilang atau memberi Anda kunci untuk memanggil Claude API. Untuk mendapatkan kunci API yang dapat digunakan, buat kunci di halaman [API keys](https://platform.claude.com/settings/keys) (`platform.claude.com/settings/keys`) di Claude Console.
</Note>
