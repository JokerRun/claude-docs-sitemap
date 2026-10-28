---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: c2175186e5da2f20f2d02ad9833e8f94c7a6e5a8238cf736926436eda79876ac
---

---
title: Mulai cepat CLI
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart
description: Instal alat baris perintah ant, lakukan autentikasi, dan kirim permintaan pertama Anda ke Claude API.
---

CLI `ant` menyediakan akses ke Claude API dari terminal Anda. Setiap sumber daya API diekspos sebagai subperintah, dengan pemformatan output, pemfilteran respons, dan input file YAML atau JSON.

<Frame caption="CLI ant sedang beraksi.">
  <video aria-label="Rekaman layar CLI ant yang berjalan di terminal.">
    <source src="https://platform.claude.com/docs/videos/ant-cli-demo.webm" type="video/webm" />
    <source src="https://platform.claude.com/docs/videos/ant-cli-demo.mp4" type="video/mp4" />
  </video>
</Frame>

Dibandingkan dengan `curl`, `ant` membangun body permintaan dari flag bertipe atau YAML yang di-pipe alih-alih JSON yang ditulis tangan, dan menyisipkan isi file ke dalam field string dengan referensi `@path`. Alat ini mengekstrak field respons dengan kueri `--transform` bawaan, sehingga Anda tidak memerlukan alat terpisah seperti `jq`, dan melakukan “pagination” (paginasi) pada endpoint daftar secara otomatis.

<Info>
  Untuk parameter khusus endpoint dan skema respons, lihat [referensi API](https://platform.claude.com/docs/id/api/cli/messages/create). Halaman ini membantu Anda mendapatkan perintah yang berfungsi. Untuk semua hal lain yang dapat dilakukan CLI, lihat [Menggunakan CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/using) dan [Scripting dan otomatisasi CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting).
</Info>

## Instalasi

<Tabs>
  <Tab title="Homebrew (macOS)">
    ```bash
    brew install anthropics/tap/ant
    ```
  </Tab>

  <Tab title="curl (Linux/WSL)">
    Untuk lingkungan Linux, unduh binary rilis secara langsung.

    ```bash
    VERSION=2.4.0
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    case $(uname -m) in
      x86_64) ARCH=amd64 ;;
      aarch64) ARCH=arm64 ;;
    esac
    curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_${OS}_${ARCH}.tar.gz" \
      | sudo tar -xz -C /usr/local/bin ant
    ```

    Anda dapat menemukan semua rilis di [halaman rilis GitHub](https://github.com/anthropics/anthropic-cli/releases).
  </Tab>

  <Tab title="Go">
    Anda juga dapat menginstal CLI dari source menggunakan `go install`. Memerlukan Go 1.25 atau yang lebih baru.

    ```bash
    go install github.com/anthropics/anthropic-cli/v2/cmd/ant@latest
    ```

    Binary ditempatkan di `$(go env GOPATH)/bin`. Tambahkan ke `PATH` Anda jika belum ada:

    ```bash
    export PATH="$PATH:$(go env GOPATH)/bin"
    ```
  </Tab>
</Tabs>

Periksa instalasi:

```bash
ant --version
```

## Autentikasi

`ant auth login` membuka alur OAuth berbasis browser terhadap Claude Console dan menyimpan kredensial yang dihasilkan secara lokal, sehingga Anda dapat memanggil API tanpa membuat atau mengelola kunci API.

```bash CLI
ant auth login
```

<Note>
  Untuk cara autentikasi lainnya (variabel lingkungan kunci API, host headless, beberapa workspace, profil bernama, dan Workload Identity Federation), lihat [Opsi autentikasi CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication).
</Note>

## Kirim permintaan pertama Anda

Dengan binary yang sudah terinstal dan terautentikasi, panggil [Messages API](https://platform.claude.com/docs/id/api/cli/messages/create):

```bash
ant messages create \
  --model claude-opus-5-5 \
  --max-tokens 1024 \
  --message '{role: user, content: "Hello, Claude"}'
```

```text Output wrap
{
  "model": "claude-opus-5-5",
  "id": "msg_01YMmR5XodC5nTqMxLZMKaq6",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello! How are you doing today? Is there something I can help you with?"
    }
  ],
  "stop_reason": "end_turn",
  "usage": { "input_tokens": 27, "output_tokens": 20 /*, ... */ }
}
```

Responsnya adalah objek API lengkap, dicetak dengan format rapi karena stdout adalah terminal.

## Penyelesaian shell

CLI menyertakan skrip “shell completion” (penyelesaian shell) untuk bash, zsh, fish, dan PowerShell. Buat dan instal satu untuk shell Anda:

<Tabs>
  <Tab title="zsh">
    ```bash
    ant @completion zsh > "${fpath[1]}/_ant"
    # Mulai ulang shell Anda atau jalankan: autoload -U compinit && compinit
    ```
  </Tab>

  <Tab title="bash">
    ```bash
    ant @completion bash > /etc/bash_completion.d/ant
    ```
  </Tab>

  <Tab title="fish">
    ```bash
    ant @completion fish > ~/.config/fish/completions/ant.fish
    ```
  </Tab>

  <Tab title="PowerShell">
    ```powershell
    ant @completion powershell | Out-String | Invoke-Expression
    # Agar tetap berlaku di seluruh sesi:
    # ant @completion powershell >> $PROFILE
    ```
  </Tab>
</Tabs>

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Opsi autentikasi CLI" icon="lock" href="https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication">
    Kunci API, host headless, beberapa workspace, dan profil bernama
  </Card>

  <Card title="Menggunakan CLI" icon="terminal" href="https://platform.claude.com/docs/id/cli-sdks-libraries/cli/using">
    Struktur perintah, format output, transformasi GJSON, dan body permintaan
  </Card>

  <Card title="Scripting dan otomatisasi CLI" icon="code" href="https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting">
    Kontrol versi untuk sumber daya API, pola scripting, dan penggunaan dari Claude Code
  </Card>
</CardGroup>
