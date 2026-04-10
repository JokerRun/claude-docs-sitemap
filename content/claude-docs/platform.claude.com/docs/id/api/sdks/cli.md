---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/cli
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 59c7655860e5ef6da42b5b0cc3450b2e24d83891c8b370aa63a37c5d2f96382c
---

# CLI

Berinteraksi dengan Claude API langsung dari terminal Anda menggunakan alat baris perintah ant

---

CLI `ant` menyediakan akses ke Claude API dari terminal Anda. Setiap sumber daya API diekspos sebagai subperintah, dengan pemformatan output, pemfilteran respons, dan dukungan untuk input file YAML atau JSON yang membuatnya praktis untuk eksplorasi interaktif maupun otomasi.

Dibandingkan dengan memanggil API menggunakan `curl`, `ant` memungkinkan Anda membangun badan permintaan dari flag bertipe atau YAML yang di-pipe daripada JSON yang ditulis tangan, menyisipkan konten file ke dalam bidang string dengan referensi `@path`, dan mengekstrak bidang dari respons dengan kueri `--transform` bawaan — tidak diperlukan alat JSON terpisah. Endpoint daftar melakukan paginasi secara otomatis. Claude Code memahami cara menggunakan `ant` secara native.

<Info>
Untuk parameter khusus endpoint dan skema respons, lihat [referensi API](/docs/id/api/cli/messages/create). Halaman ini mencakup fitur dan alur kerja khusus CLI yang berlaku di semua endpoint.
</Info>

## Instalasi

<Tabs>
<Tab title="Homebrew (macOS)">

```bash
brew install anthropics/tap/ant
```

Di macOS, hapus karantina biner:

```bash
xattr -d com.apple.quarantine "$(brew --prefix)/bin/ant"
```

</Tab>
<Tab title="curl (Linux/WSL)">

Untuk lingkungan Linux, unduh biner rilis secara langsung.

```bash
VERSION=1.0.0
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m | sed -e 's/x86_64/amd64/' -e 's/aarch64/arm64/')
curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_${OS}_${ARCH}.tar.gz" \
  | sudo tar -xz -C /usr/local/bin ant
```

Anda dapat menemukan semua rilis di [halaman rilis GitHub](https://github.com/anthropics/anthropic-cli/releases).

</Tab>
<Tab title="Go">

Anda juga dapat menginstal CLI dari sumber menggunakan `go install`. Memerlukan Go 1.22 atau lebih baru.

```bash
go install github.com/anthropics/anthropic-cli/cmd/ant@latest
```

Biner ditempatkan di `$(go env GOPATH)/bin`. Tambahkan ke `PATH` Anda jika belum ada:

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

CLI membaca kunci API Anda dari variabel lingkungan `ANTHROPIC_API_KEY`.

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

Dapatkan kunci dari [Claude Console](https://platform.claude.com/settings/keys). Untuk mengarahkan ke host API yang berbeda, atur `ANTHROPIC_BASE_URL` atau teruskan `--base-url` pada perintah apa pun.

## Kirim permintaan pertama Anda

Dengan biner terinstal dan `ANTHROPIC_API_KEY` telah diatur, panggil [Messages API](/docs/id/api/cli/messages/create):

```bash
ant messages create \
  --model claude-opus-4-6 \
  --max-tokens 1024 \
  --message '{role: user, content: "Hello, Claude"}'
```

```json Output
{
  "model": "claude-opus-4-6",
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

Responsnya adalah objek API lengkap, dicetak dengan rapi karena stdout adalah terminal. Sisa halaman ini mencakup cara membentuk ulang output tersebut, meneruskan badan permintaan yang kompleks, dan menghubungkan perintah bersama.

## Struktur perintah

Perintah mengikuti pola `resource action`. Sumber daya bersarang menggunakan titik dua:

```text
ant <resource>[:<subresource>] <action> [flags]
```

Jalankan `ant --help` untuk daftar sumber daya lengkap, atau tambahkan `--help` ke subperintah apa pun untuk melihat flagnya.

Sumber daya yang saat ini dalam beta — termasuk agents, sessions, deployments, environments, dan skills — berada di bawah awalan `beta:`. Perintah dalam namespace ini secara otomatis mengirimkan header `anthropic-beta` yang sesuai untuk sumber daya tersebut, sehingga Anda tidak perlu meneruskannya sendiri. Gunakan `--beta <header>` hanya untuk mengganti default — misalnya, untuk memilih versi skema yang berbeda.

```bash
ant models list
ant messages create --model claude-opus-4-6 --max-tokens 1024 ...
ant beta:agents retrieve --agent-id agent_01...
ant beta:sessions:events list --session-id session_01...
```

### Flag global

| Flag | Deskripsi |
| --- | --- |
| `--format` | Format output: `auto`, `json`, `jsonl`, `yaml`, `pretty`, `raw`, `explore` |
| `--transform` | Filter atau bentuk ulang respons dengan [path GJSON](#transform-output-with-gjson) |
| `--base-url` | Ganti URL dasar API |
| `--debug` | Cetak permintaan dan respons HTTP lengkap ke stderr |
| `--format-error`, `--transform-error` | Sama seperti `--format` dan `--transform` tetapi diterapkan pada [respons error](#inspect-errors) |

## Format output

Format `auto` default mencetak JSON dengan rapi saat menulis ke terminal dan mengeluarkan JSON kompak saat di-pipe. Ganti dengan `--format`:

```bash
ant models retrieve --model-id claude-opus-4-6 --format yaml
```

```yaml Output
type: model
id: claude-opus-4-6
display_name: Claude Opus 4.6
created_at: "2026-02-04T00:00:00Z"
...
```

Endpoint daftar melakukan paginasi otomatis. Dalam format default, setiap item ditulis secara terpisah (satu objek JSON kompak per baris dalam mode `jsonl`, aliran dokumen YAML dalam mode `yaml`), yang mengalir dengan bersih ke dalam `head`, `grep`, dan filter `--transform`.

### Penjelajah interaktif

Saat terhubung ke terminal, `--format explore` membuka TUI lipat-dan-cari untuk menelusuri respons besar. Tombol panah memperluas dan menciutkan node, `/` mencari, `q` keluar.

```bash
ant models list --format explore
```

## Transformasi output dengan GJSON

Gunakan `--transform` untuk membentuk ulang respons sebelum dicetak. Ekspresi adalah [path GJSON](https://github.com/tidwall/gjson/blob/master/SYNTAX.md). Untuk endpoint daftar, transformasi dijalankan terhadap setiap item secara individual, bukan terhadap envelope:

```bash
ant beta:agents list \
  --transform "{id,name,model}" \
  --format jsonl
```

```jsonl Output
{"id": "agent_011CYm1BLqPX...", "name": "Docs CLI Test Agent", "model": "claude-sonnet-4-6"}
{"id": "agent_011CYkVwfaEt...", "name": "Coffee Making Assistant", "model": "claude-sonnet-4-6"}
{"id": "agent_011CYixHhtUP...", "name": "Coding Assistant", "model": "claude-opus-4-5"}
```

### Ekstrak skalar

Untuk menangkap satu bidang sebagai string tanpa tanda kutip — misalnya, ID sumber daya yang baru dibuat — pasangkan `--transform` dengan `--format yaml`. YAML mengeluarkan nilai skalar tanpa tanda kutip, sehingga hasilnya siap untuk ditetapkan ke variabel shell:

```bash
AGENT_ID=$(ant beta:agents create \
  --name "My Agent" \
  --model claude-sonnet-4-6 \
  --transform id --format yaml)

printf '%s\n' "$AGENT_ID"
```

```text Output
agent_011CYm1BLqPXpQRk5khsSXrs
```

<Note>
`--transform` tidak diterapkan saat `--format raw` diatur. Gunakan `--format yaml` untuk skalar tanpa tanda kutip, atau `--format jsonl` untuk menjaga hasil sebagai data terstruktur untuk pemrosesan lebih lanjut.
</Note>

## Meneruskan badan permintaan

Mekanisme input yang tepat bergantung pada bentuk data: gunakan **flag** untuk bidang skalar dan nilai terstruktur pendek, pipe dokumen **stdin** untuk badan bersarang atau multi-baris, dan gunakan **referensi `@file`** untuk menarik konten file ke dalam bidang string atau biner apa pun.

### Flag

Bidang skalar dipetakan langsung ke flag. Bidang terstruktur menerima sintaks mirip YAML yang lebih longgar (kunci tanpa tanda kutip, tanda kutip opsional di sekitar string) atau JSON ketat:

```bash
ant beta:sessions create \
  --agent '{type: agent, id: agent_011CYm1BLqPXpQRk5khsSXrs, version: 1}' \
  --environment env_01595EKxaaTTGwwY3kyXdtbs \
  --title "CLI docs test session"
```

Flag yang dapat diulang membangun array. Setiap `--tool` atau `--event` menambahkan satu elemen:

```bash
ant beta:agents create \
  --name "Research Agent" \
  --model claude-opus-4-6 \
  --tool '{type: agent_toolset_20260401}' \
  --tool '{type: custom, name: search_docs, input_schema: {type: object, properties: {query: {type: string}}}}'
```

### Stdin

Pipe dokumen JSON atau YAML ke stdin untuk menyediakan badan permintaan lengkap. Bidang dari stdin digabungkan dengan flag, dengan flag yang lebih diutamakan. Di sini `version` adalah token penguncian optimistis yang dikembalikan oleh `retrieve` sebelumnya, dan `$AGENT_ID` ditangkap seperti pada [Ekstrak skalar](#extract-a-scalar):

```bash
echo '{"description": "Updated test agent.", "version": 1}' | \
  ant beta:agents update --agent-id "$AGENT_ID"
```

Heredoc bekerja dengan cara yang sama dan nyaman untuk YAML multi-baris. Kutip pembatas (seperti `<<'YAML'`) untuk menonaktifkan ekspansi variabel di dalam badan.

```bash
ant beta:agents create <<'YAML'
name: Research Agent
model: claude-opus-4-6
system: |
  You are a research assistant. Cite sources for every claim.
tools:
  - type: agent_toolset_20260401
YAML
```

### Referensi file

Flag yang mengambil path file, seperti `--file` pada perintah upload, menerima path biasa:

```bash
ant beta:files upload --file ./report.pdf
```

Untuk menyisipkan konten file ke dalam bidang bernilai string, awali path dengan `@`:

```bash
ant beta:agents create \
  --name "Researcher" --model claude-sonnet-4-6 \
  --system @./prompts/researcher.txt
```

Di dalam nilai flag terstruktur, bungkus path dalam tanda kutip. Untuk mengirim PDF ke Messages API:

```bash
ant messages create \
  --model claude-opus-4-6 \
  --max-tokens 1024 \
  --message '{role: user, content: [
    {type: document, source: {type: base64, media_type: application/pdf, data: "@./scan.pdf"}},
    {type: text, text: "Extract the text from this scanned document."}
  ]}' \
  --transform 'content.0.text' --format yaml
```

CLI mendeteksi jenis file dan mengenkode file biner sebagai base64 secara otomatis. Untuk memaksa enkoding tertentu gunakan `@file://` untuk teks biasa atau `@data://` untuk base64. Escape karakter `@` literal di awal dengan garis miring terbalik (`\@username`).

## Kontrol versi sumber daya API

Anda dapat menggunakan CLI untuk mengontrol versi sumber daya API seperti skills, agents, environments, atau deployments sebagai file YAML di repositori Anda dan menjaganya tetap sinkron dengan Claude API.

<Note>
Untuk informasi lebih lanjut tentang sumber daya ini, lihat [Managed Agents](/docs/id/managed-agents/overview).
</Note>

<Steps>
<Step title="Definisikan agent Anda">

Tulis definisi agent ke `summarizer.agent.yaml`:

```yaml summarizer.agent.yaml
name: Summarizer
model: claude-sonnet-4-6
system: |
  You are a helpful assistant that writes concise summaries.
tools:
  - type: agent_toolset_20260401
```

</Step>
<Step title="Buat agent">

```bash
ant beta:agents create < summarizer.agent.yaml
```

```json Output
{
  "id": "agent_011CYm1BLqPXpQRk5khsSXrs",
  "version": 1,
  "name": "Summarizer",
  "model": "claude-sonnet-4-6"
  /* ... */
}
```

Catat `id` dari respons — Anda akan meneruskannya ke perintah pembuatan sesi di bawah.

<Tip>
Masukkan `summarizer.agent.yaml` ke repositori Anda dan jaga agar tetap sinkron dengan API di pipeline CI Anda. Perintah update memerlukan ID agent dan versi saat ini sebagai flag:

```bash CLI
ant beta:agents update --agent-id agent_011CYm1BLqPXpQRk5khsSXrs --version 1 < summarizer.agent.yaml
```
</Tip>

</Step>
<Step title="Definisikan environment">

Sesi berjalan dalam sebuah [environment](/docs/id/api/cli/beta/environments), yang mendefinisikan container tempat sesi dieksekusi. Tulis definisi environment ke `summarizer.environment.yaml`:

```yaml summarizer.environment.yaml
name: summarizer-env
config:
  type: cloud
  networking:
    type: unrestricted
```

</Step>
<Step title="Buat environment">

```bash
ant beta:environments create < summarizer.environment.yaml
```

```json Output
{
  "id": "env_01595EKxaaTTGwwY3kyXdtbs",
  "name": "summarizer-env"
  /* ... */
}
```

Catat `id` dari respons — Anda akan meneruskannya ke perintah pembuatan sesi di bawah.

<Tip>
Masukkan `summarizer.environment.yaml` ke repositori Anda dan jaga agar tetap sinkron dengan API di pipeline CI Anda. Perintah update memerlukan ID environment sebagai flag:

```bash CLI
ant beta:environments update --environment-id env_01595EKxaaTTGwwY3kyXdtbs < summarizer.environment.yaml
```
</Tip>

</Step>
<Step title="Mulai sesi">

Tempelkan `id` agent dan `id` environment dari output sebelumnya ke dalam perintah pembuatan sesi:

```bash highlight={2..3}
ant beta:sessions create \
  --agent agent_011CYm1BLqPXpQRk5khsSXrs \
  --environment env_01595EKxaaTTGwwY3kyXdtbs \
  --title "Summarization task"
```

```json Output
{
  "id": "session_01JZCh78XvmxJjiXVy3oSi7K",
  "status": "running"
  /* ... */
}
```

</Step>
<Step title="Kirim pesan pengguna">

Salin `id` sesi dari output sebelumnya ke `--session-id`:

```bash highlight={2}
ant beta:sessions:events send \
  --session-id session_01JZCh78XvmxJjiXVy3oSi7K \
  --event '{type: user.message, content: [{type: text, text: "Summarize the benefits of type safety in one sentence."}]}'
```

</Step>
<Step title="Baca percakapan">

`--transform` dijalankan terhadap setiap event yang terdaftar, sehingga ini mencetak teks setiap pesan secara berurutan:

```bash highlight={2}
ant beta:sessions:events list \
  --session-id session_01JZCh78XvmxJjiXVy3oSi7K \
  --transform 'content.0.text' --format yaml
```

```text Output
Summarize the benefits of type safety in one sentence.
Type safety catches errors at compile time rather than runtime, reducing bugs, improving code clarity, enabling better tooling support, and making codebases easier to maintain and refactor with confidence.
```

<Tip>
Untuk memantau sesi saat berjalan, gunakan `ant beta:sessions stream --session-id session_01JZCh78XvmxJjiXVy3oSi7K`. Event ditulis ke stdout saat tiba.
</Tip>

</Step>
</Steps>

## Pola skrip

CLI dirancang untuk dikomposisikan dengan alat shell standar.

### Hubungkan output daftar ke perintah kedua

`--transform id --format yaml` pada endpoint daftar mengeluarkan satu ID biasa per baris, sehingga alat standar seperti `head` dan `xargs` dapat diterapkan langsung. Tangkap hasil pertama, lalu teruskan ke perintah lanjutan:

```bash
FIRST_AGENT=$(ant beta:agents list \
  --transform id --format yaml | head -1)

ant beta:agents:versions list \
  --agent-id "$FIRST_AGENT" \
  --transform "{version,created_at}" --format jsonl
```

### Periksa error

Flag `--transform-error` dan `--format-error` mencerminkan pasangan jalur sukses mereka dan mengikuti aturan yang sama — pasangkan dengan `yaml`, bukan `raw`, untuk menerapkan transformasi. Ekstrak hanya pesan error:

```bash
ant beta:agents retrieve --agent-id bogus \
  --transform-error error.message --format-error yaml 2>&1
```

```text Output
GET "https://api.anthropic.com/v1/agents/bogus?beta=true": 404 Not Found
Agent not found.
```

## Gunakan CLI dari Claude Code

[Claude Code](https://docs.claude.com/en/docs/claude-code/overview) mengetahui cara menggunakan CLI `ant` secara bawaan. Dengan CLI terinstal dan `ANTHROPIC_API_KEY` telah diatur, Anda dapat meminta Claude Code untuk beroperasi pada sumber daya API Anda secara langsung — misalnya:

- "Daftarkan sesi agent terbaru saya dan rangkum mana yang mengalami error."
- "Unggah setiap PDF di `./reports` ke Files API dan cetak ID yang dihasilkan."
- "Ambil event untuk sesi `session_01...` dan beri tahu saya di mana agent terhenti."

Claude Code menjalankan shell ke `ant`, mengurai output terstruktur, dan bernalar atas hasilnya — tidak diperlukan kode integrasi khusus.

## Debugging

Tambahkan `--debug` ke perintah apa pun untuk mencetak permintaan dan respons HTTP yang tepat (header dan badan) ke stderr. Kunci API diredaksi.

```bash
ant --debug beta:agents list
```

```text Output
GET /v1/agents?beta=true HTTP/1.1
Host: api.anthropic.com
Anthropic-Beta: managed-agents-2026-04-01
Anthropic-Version: 2023-06-01
X-Api-Key: <REDACTED>
...
```

## Penyelesaian shell

CLI dilengkapi skrip penyelesaian untuk bash, zsh, fish, dan PowerShell. Buat dan instal satu untuk shell Anda:

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
# Untuk mempertahankan antar sesi:
# ant @completion powershell >> $PROFILE
```

</Tab>
</Tabs>

## Sumber daya yang tersedia

Setiap sumber daya API yang diekspos oleh CLI didokumentasikan dalam [referensi API](/docs/id/api/cli/messages/create). Untuk daftar lokal, jalankan `ant --help`, dan tambahkan `--help` ke subperintah apa pun untuk melihat flag dan parameternya.