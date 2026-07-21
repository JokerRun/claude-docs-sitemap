---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 8f8cf214d6b76e2240e67142e7e8d51ca6871103181ae477e362dabdf562414a
---

# Opsi autentikasi CLI

Autentikasi CLI ant dengan login interaktif, kunci API, profil bernama, dan Workload Identity Federation.

---

CLI `ant` mendukung beberapa sumber kredensial. [Quickstart](/docs/id/cli-sdks-libraries/cli/quickstart#authentication) membahas jalur cepat satu perintah (`ant auth login`). Halaman ini membahas setiap opsi secara lengkap.

## Login interaktif

`ant auth login` memungkinkan Anda memanggil API tanpa membuat atau mengelola kunci API. Perintah ini membuka alur OAuth berbasis browser terhadap Claude Console dan menyimpan kredensial yang dihasilkan di bawah `$ANTHROPIC_CONFIG_DIR` (lihat [Direktori konfigurasi](/docs/id/manage-claude/wif-reference#configuration-directory) untuk default spesifik OS). Pada host jarak jauh atau di lingkungan mana pun tanpa browser lokal, berikan `--no-browser` untuk mencetak URL otorisasi dan tempelkan kode yang dikembalikan ke terminal.

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

Selama alur browser, Anda memilih organisasi lalu sebuah [workspace](/docs/id/manage-claude/workspaces). Token yang diterbitkan [dicakup ke workspace tersebut](/docs/id/manage-claude/workspaces#api-keys-and-resource-scoping), sehingga CLI hanya dapat melihat sumber daya yang termasuk di dalamnya. Berikan `--workspace-id` untuk mengikat langsung dan melewati pemilih. Untuk bekerja di lebih dari satu workspace, lihat [Beralih antar workspace](#switch-between-workspaces).

Login interaktif ditujukan untuk pengembangan lokal dan scripting di mesin Anda sendiri. Untuk beban kerja non-interaktif seperti CI, server, dan kontainer, gunakan [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation) sebagai gantinya.

Login menulis kredensial ke `credentials/<profile>.json`. Login pertama untuk sebuah profil juga membuat `configs/<profile>.json` dan menetapkannya sebagai profil aktif. Untuk menghapus kredensial yang tersimpan, jalankan `ant auth logout`, atau `ant auth logout --all` untuk menghapus setiap profil.

## Akses admin

Secara default, `ant auth login` meminta token yang dicakup ke workspace. Untuk mengelola sumber daya yang didokumentasikan di halaman [Admin API](/docs/id/manage-claude/admin-api), minta scope `org:admin` di bawah profil khusus:

```bash CLI
ant auth login --profile admin --scope "org:admin"

# Cetak bearer token untuk header Authorization:
ant auth print-credentials --profile admin --access-token
```

Scope `org:admin` hanya diberikan kepada anggota organisasi dengan peran admin, owner, atau primary owner. Token yang diterbitkan memiliki akses ke seluruh organisasi, dan pengikatan workspace apa pun pada profil tidak membatasinya. Pisahkan profil admin dari profil harian Anda agar perintah rutin tidak pernah berjalan dengan akses yang ditingkatkan.

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

    Buka terminal baru agar perubahan diterapkan.
  </Tab>
</Tabs>

Untuk mengganti kunci pada satu pemanggilan, berikan `--api-key`. Untuk mengarahkan ke host API yang berbeda, atur `ANTHROPIC_BASE_URL` atau berikan `--base-url`.

## Memeriksa status autentikasi

`ant auth status` mencetak sumber kredensial yang dipilih CLI (variabel lingkungan kunci API, login OAuth, federasi, atau profil), profil aktif, workspace tempat token aktif terikat, dan jalur direktori konfigurasi. Gunakan ini untuk mendiagnosis mengapa suatu beban kerja memilih kredensial atau workspace yang salah.

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

Baca baris `(active)` untuk melihat sumber kredensial dan workspace mana yang terpilih. Perintah ini melaporkan status alih-alih melakukan pemeriksaan kesehatan, jadi jangan membuat skrip berdasarkan status keluarnya. Untuk urutan lengkap sumber kredensial, lihat [Prioritas kredensial](/docs/id/manage-claude/wif-reference#credential-precedence).

## Beralih antar workspace

Token login interaktif terikat ke satu workspace. Untuk menggunakan CLI terhadap lebih dari satu workspace, login ke masing-masing di bawah profil bernama tersendiri, lalu beralih di antaranya:

```bash CLI
# 1. Buat profil (interaktif; pilih workspace lain di
#    browser, atau berikan --workspace-id untuk melewati pemilih):
# ant auth login --profile other-ws

# 2. Jadikan sebagai default untuk perintah berikutnya:
ant profile activate other-ws

# 3. Atau pilih untuk satu perintah saja tanpa mengubah default:
ant --profile other-ws models list
ANTHROPIC_PROFILE=other-ws ant models list
```

Jalankan [`ant auth status`](#check-authentication-status) untuk mengonfirmasi profil dan workspace mana yang aktif.

<Note>
  Profil hanya diperiksa ketika tidak ada kunci API yang diatur. Jika `ANTHROPIC_API_KEY` ada di lingkungan Anda, variabel tersebut mengesampingkan setiap profil dan semua perintah ini menggunakan workspace apa pun yang menjadi cakupan kunci tersebut. Hapus pengaturannya sebelum beralih profil.
</Note>

## Mengelola profil

Subperintah `ant profile` memeriksa dan mengedit status profil secara langsung:

```bash CLI
ant profile list
ant profile get --profile other-ws
ant profile set workspace_id wrkspc_01... --profile other-ws
```

Kunci yang dapat ditulis untuk `ant profile set` adalah `workspace_id`, `base_url`, `organization_id`, `scope`, `client_id`, dan `console_url`. Mengatur `workspace_id` mencatat workspace target dalam konfigurasi profil tetapi tidak mengikat ulang kredensial yang sudah diterbitkan; jalankan `ant auth login` lagi di bawah profil tersebut untuk menerbitkan token bagi workspace baru.

Untuk skema file profil dan blok federasi, lihat [File konfigurasi profil](/docs/id/manage-claude/wif-reference#profile-configuration-file). Untuk Workload Identity Federation, lihat [Ikhtisar autentikasi](/docs/id/manage-claude/authentication) dan [Referensi WIF](/docs/id/manage-claude/wif-reference).

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Menggunakan CLI" icon="terminal" href="/docs/id/cli-sdks-libraries/cli/using">
    Struktur perintah, format output, transformasi GJSON, dan body permintaan
  </Card>

  <Card title="Scripting dan otomatisasi CLI" icon="code" href="/docs/id/cli-sdks-libraries/cli/scripting">
    Kontrol versi sumber daya API, pola scripting, dan penggunaan dari Claude Code
  </Card>

  <Card title="Workload Identity Federation" icon="cloud" href="/docs/id/manage-claude/workload-identity-federation">
    Autentikasi non-interaktif untuk CI, server, dan kontainer
  </Card>
</CardGroup>
