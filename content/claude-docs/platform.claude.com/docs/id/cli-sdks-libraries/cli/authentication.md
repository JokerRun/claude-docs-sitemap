---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication
fetched_at: 2026-10-02T02:24:19.323378Z
sha256: e8df3caae859189203da9e14696be4e75378ec6aa9a0780055d5aa93d7880019
---

---
title: Opsi autentikasi CLI
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication
description: Autentikasi CLI ant dengan login interaktif, kunci API, profil bernama, dan Workload Identity Federation.
---

CLI `ant` mendukung beberapa sumber kredensial. [Quickstart](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart#authentication) mencakup jalur mudah satu perintah (`ant auth login`). Halaman ini mencakup setiap opsi secara lengkap.

## Login interaktif

`ant auth login` memungkinkan Anda memanggil API tanpa membuat atau mengelola kunci API. Ini membuka alur OAuth berbasis browser terhadap Claude Console dan menyimpan kredensial yang dihasilkan di bawah `$ANTHROPIC_CONFIG_DIR` (lihat [Direktori konfigurasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#configuration-directory) untuk default spesifik OS). Pada host jarak jauh atau di lingkungan apa pun tanpa browser lokal, berikan `--no-browser` untuk mencetak URL otorisasi dan tempel kode yang dikembalikan kembali ke terminal.

```bash CLI
ant auth login

# Pada host jarak jauh tanpa browser:
ant auth login --no-browser

# Ikat ke workspace tertentu dan lewati pemilih browser:
ant auth login --workspace-id wrkspc_01...

# Jika profil bernama yang Anda berikan dengan --profile tidak ada,
# profil bernama baru akan dibuat dengan nama tersebut.
ant auth login --profile <profile-name>
```

Selama alur browser, Anda memilih organisasi dan kemudian [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces). Token yang diterbitkan [dibatasi ke workspace tersebut](https://platform.claude.com/docs/id/manage-claude/workspaces#api-keys-and-resource-scoping), sehingga CLI hanya dapat melihat sumber daya yang menjadi miliknya. Berikan `--workspace-id` untuk mengikat secara langsung dan melewati pemilih. Untuk bekerja di lebih dari satu workspace, lihat [Beralih antar workspace](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication#switch-between-workspaces).

Login interaktif ditujukan untuk pengembangan lokal dan scripting di mesin Anda sendiri. Untuk beban kerja non-interaktif seperti CI, server, dan kontainer, gunakan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) sebagai gantinya.

Login menulis kredensial ke `credentials/<profile>.json`. Login pertama untuk sebuah profil juga membuat `configs/<profile>.json` dan menetapkannya sebagai profil aktif. Untuk menghapus kredensial yang tersimpan, jalankan `ant auth logout`, atau `ant auth logout --all` untuk membersihkan setiap profil.

## Akses admin

Secara default, `ant auth login` meminta token yang dibatasi ke workspace. Untuk mengelola sumber daya yang didokumentasikan di halaman [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api), minta scope `org:admin` di bawah profil khusus:

```bash CLI
ant auth login --profile admin --scope "org:admin"

# Cetak bearer token untuk header Authorization:
ant auth print-credentials --profile admin --access-token
```

Scope `org:admin` hanya diberikan kepada anggota organisasi dengan peran admin, owner, atau primary owner. Token yang diterbitkan memiliki akses seluruh organisasi, dan pengikatan workspace apa pun pada profil tidak membatasinya. Jaga agar profil admin tetap terpisah dari profil sehari-hari Anda sehingga perintah rutin tidak pernah berjalan dengan akses yang ditingkatkan.

## Kunci API

CLI juga membaca kunci API Anda dari variabel lingkungan `ANTHROPIC_API_KEY`. Dapatkan kunci dari [Claude Console](https://platform.claude.com/settings/keys).

<Tabs>
  <Tab title="zsh">
    ```bash
    echo 'export ANTHROPIC_API_KEY=sk-ant-api03-...' >> ~/.zshrc
    source ~/.zshrc
    ```
  </Tab>

  <Tab title="bash">
    ```bash
    echo 'export ANTHROPIC_API_KEY=sk-ant-api03-...' >> ~/.bashrc
    source ~/.bashrc
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell
    setx ANTHROPIC_API_KEY "sk-ant-api03-..."
    ```

    Buka terminal baru agar perubahan berlaku.
  </Tab>
</Tabs>

Untuk menimpa kunci untuk satu pemanggilan, berikan `--api-key`. Untuk mengarah ke host API yang berbeda, atur `ANTHROPIC_BASE_URL` atau berikan `--base-url`.

Jika Anda menggunakan kunci API yang dibatasi ke beberapa workspace, seperti [kunci akun personal atau service](https://platform.claude.com/docs/id/manage-claude/authentication#key-types), Anda harus [menentukan workspace](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace) untuk menjalankan perintah Anda. Lakukan ini dengan mengatur variabel lingkungan `ANTHROPIC_WORKSPACE_ID`, yang dibaca CLI secara otomatis, atau dengan menggunakan [flag `--workspace-id`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/using#global-flags). Nilainya harus berupa ID `wrkspc_...`.

```bash CLI
ant messages create \
  --workspace-id wrkspc_01... \
  --model claude-opus-5-5 \
  --max-tokens 1024 \
  --message '{role: user, content: "Hello, Claude"}'
```

## Periksa status autentikasi

`ant auth status` mencetak sumber kredensial yang dipilih CLI (variabel lingkungan kunci API, login OAuth, federasi, atau profil), profil aktif, workspace tempat token aktif terikat, dan jalur direktori konfigurasi. Gunakan untuk mendiagnosis mengapa beban kerja memilih kredensial atau workspace yang salah.

```bash CLI
ant auth status
```

```text
Active profile:  default
Config dir:      ~/.config/anthropic
Profile config:  ~/.config/anthropic/configs/default.json
Credentials:     ~/.config/anthropic/credentials/default.json

Credentials
  (active) * Profile (user_oauth) [via active_config]       sk-ant-oat01-EXA...
...

Workspace
  (active) * Workspace                                      wrkspc_01... (Engineering)
```

Baca baris `(active)` untuk melihat sumber kredensial dan workspace mana yang menang. Perintah ini melaporkan status daripada melakukan pemeriksaan kesehatan, jadi jangan membuat skrip terhadap status keluar. Untuk urutan lengkap sumber kredensial, lihat [Prioritas kredensial](https://platform.claude.com/docs/id/manage-claude/wif-reference#credential-precedence).

## Beralih antar workspace

Token login interaktif terikat ke satu workspace. Untuk menggunakan CLI terhadap lebih dari satu workspace, login ke masing-masing di bawah profil bernama sendiri, lalu beralih di antaranya:

```bash CLI
# 1. Buat profil (interaktif; pilih workspace lain di
#    browser, atau berikan --workspace-id untuk melewati pemilih):
# ant auth login --profile other-ws

# 2. Jadikan sebagai default untuk perintah berikutnya:
ant profile activate other-ws

# 3. Atau pilih untuk satu perintah tanpa mengubah default:
ant --profile other-ws models list
ANTHROPIC_PROFILE=other-ws ant models list
```

Jalankan [`ant auth status`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication#check-authentication-status) untuk mengonfirmasi profil dan workspace mana yang aktif.

<Note>
  Profil hanya dikonsultasikan ketika tidak ada kunci API yang diatur. Jika `ANTHROPIC_API_KEY` ada di lingkungan Anda, ia menimpa setiap profil dan perintah-perintah ini semuanya menggunakan workspace kunci tersebut (atau, untuk kunci multi-workspace, workspace yang diatur dengan `ANTHROPIC_WORKSPACE_ID` atau `--workspace-id`). Hapus pengaturannya sebelum beralih profil.
</Note>

## Kelola profil

Subperintah `ant profile` memeriksa dan mengedit status profil secara langsung:

```bash CLI
ant profile list
ant profile get --profile other-ws
ant profile set workspace_id wrkspc_01... --profile other-ws
```

Kunci yang dapat ditulis untuk `ant profile set` adalah `workspace_id`, `base_url`, `organization_id`, `scope`, `client_id`, dan `console_url`. Mengatur `workspace_id` mencatat workspace target dalam konfigurasi profil tetapi tidak mengikat ulang kredensial yang sudah diterbitkan; jalankan `ant auth login` lagi di bawah profil tersebut untuk mencetak token untuk workspace baru.

Untuk skema file profil dan blok federasi, lihat [File konfigurasi profil](https://platform.claude.com/docs/id/manage-claude/wif-reference#profile-configuration-file). Untuk Workload Identity Federation, lihat [Ikhtisar autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication) dan [referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference).

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Menggunakan CLI" icon="terminal" href="https://platform.claude.com/docs/id/cli-sdks-libraries/cli/using">
    Struktur perintah, format output, transformasi GJSON, dan body permintaan
  </Card>

  <Card title="Scripting dan otomatisasi CLI" icon="code" href="https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting">
    Sumber daya API kontrol versi, pola scripting, dan penggunaan dari Claude Code
  </Card>

  <Card title="Workload Identity Federation" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/workload-identity-federation">
    Autentikasi non-interaktif untuk CI, server, dan kontainer
  </Card>
</CardGroup>
