---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/cli
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 622578e0ea81eb04b04993c91ce167cf8d87cc3aadb39284735989accc2d134c
---

# CLI

Berinteraksi dengan Claude API langsung dari terminal Anda dengan alat baris perintah ant

---

CLI `ant` menyediakan akses ke Claude API dari terminal Anda. Setiap sumber daya API diekspos sebagai subperintah, dengan pemformatan output, penyaringan respons, dan dukungan untuk input file YAML atau JSON yang membuatnya praktis untuk eksplorasi interaktif dan otomasi.

Dibandingkan dengan memanggil API dengan `curl`, `ant` memungkinkan Anda membangun badan permintaan dari flag yang diketik atau YAML yang disalurkan daripada JSON yang ditulis tangan, menggabungkan konten file ke dalam bidang string dengan referensi `@path`, dan mengekstrak bidang dari respons dengan kueri `--transform` bawaan — tidak diperlukan alat JSON terpisah. Titik akhir daftar secara otomatis melakukan pagination. Claude Code memahami cara menggunakan `ant` secara native.

<Info>
Untuk parameter spesifik titik akhir dan skema respons, lihat [referensi API](/docs/id/api/cli/messages/create). Halaman ini mencakup fitur dan alur kerja khusus CLI yang berlaku di semua titik akhir.
</Info>

## Instalasi

<Tabs>
<Tab title="Homebrew (macOS)">

```bash
brew install anthropics/tap/ant
```

Di macOS, hapus quarantine dari biner:

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

Dapatkan kunci dari [Claude Console](https://platform.claude.com/settings/keys). Untuk menunjuk ke host API yang berbeda, atur `ANTHROPIC_BASE_URL` atau teruskan `--base-url` pada perintah apa pun.

## Kirim permintaan pertama Anda

Dengan biner terinstal dan `ANTHROPIC_API_KEY` diatur, panggil [Messages API](/docs/id/api/cli/messages/create):

```bash
ant messages create \
  --model claude-opus-4-7 \
  --max-tokens 1024 \
  --message '{role: user, content: "Hello, Claude"}'
```

```json Output
{
  "model": "claude-opus-4-7",
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

Respons adalah objek API lengkap, yang diformat dengan indentasi karena stdout adalah terminal. Sisa halaman ini mencakup cara mengubah bentuk output tersebut, melewatkan badan permintaan yang kompleks, dan menghubungkan perintah bersama-sama.

## Struktur perintah

Perintah mengikuti pola `resource action`. Sumber daya bersarang menggunakan titik dua:

```text
ant <resource>[:<subresource>] <action> [flags]
```

Jalankan `ant --help` untuk daftar sumber daya lengkap, atau tambahkan `--help` ke subperintah apa pun untuk flag-nya.

Sumber daya yang saat ini dalam beta — termasuk agen, sesi, penyebaran, lingkungan, dan keterampilan — berada di bawah awalan `beta:`. Perintah di namespace ini secara otomatis mengirimkan header `anthropic-beta` yang sesuai untuk sumber daya tersebut, jadi Anda tidak perlu meneruskannya sendiri. Gunakan `--beta <header>` hanya untuk mengganti default — misalnya, untuk memilih versi skema yang berbeda.

```bash
ant models list
ant messages create --model claude-opus-4-7 --max-tokens 1024 ...
ant beta:agents retrieve --agent-id agent_01...
ant beta:sessions:events list --session-id session_01...
```

### Flag global

| Flag | Deskripsi |
| --- | --- |
| `--format` | Format output: `auto`, `json`, `jsonl`, `yaml`, `pretty`, `raw`, `explore` |
| `--transform` | Filter atau ubah bentuk respons dengan [jalur GJSON](#transform-output-with-gjson) |
| `--base-url` | Ganti URL dasar API |
| `--debug` | Cetak permintaan dan respons HTTP lengkap ke stderr |
| `--format-error`, `--transform-error` | Sama seperti `--format` dan `--transform` tetapi diterapkan pada [respons kesalahan](#inspect-errors) |

## Format output

Format `auto` default mencetak JSON dengan indentasi saat menulis ke terminal dan mengeluarkan JSON kompak saat disalurkan. Ganti dengan `--format`:

```bash
ant models retrieve --model-id claude-opus-4-7 --format yaml
```

```yaml Output
type: model
id: claude-opus-4-7
display_name: Claude Opus 4.7
created_at: "2026-02-04T00:00:00Z"
...
```

Titik akhir daftar melakukan pagination otomatis. Dalam format default setiap item ditulis secara terpisah (satu objek JSON kompak per baris dalam mode `jsonl`, aliran dokumen YAML dalam mode `yaml`), yang mengalir dengan bersih ke filter `head`, `grep`, dan `--transform`.

### Penjelajah interaktif

Saat terhubung ke terminal, `--format explore` membuka TUI lipat-dan-cari untuk menjelajahi respons besar. Tombol panah memperluas dan menciutkan node, `/` mencari, `q` keluar.

```bash
ant models list --format explore
```

## Ubah bentuk output dengan GJSON

Gunakan `--transform` untuk mengubah bentuk respons sebelum mencetak. Ekspresi adalah [jalur GJSON](https://github.com/tidwall/gjson/blob/master/SYNTAX.md). Untuk titik akhir daftar, transformasi berjalan terhadap setiap item secara individual, bukan amplop:

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

Untuk menangkap satu bidang sebagai string tanpa tanda kutip — misalnya, ID sumber daya yang baru dibuat — pasangkan `--transform` dengan `--format yaml`. YAML mengeluarkan nilai skalar tanpa tanda kutip, jadi hasilnya siap untuk ditetapkan ke variabel shell:

```bash
AGENT_ID=$(ant beta:agents create \
  --name "My Agent" \
  --model '{id: claude-sonnet-4-6}' \
  --transform id --format yaml)

printf '%s\n' "$AGENT_ID"
```

```text Output
agent_011CYm1BLqPXpQRk5khsSXrs
```

<Note>
`--transform` tidak diterapkan saat `--format raw` diatur. Gunakan `--format yaml` untuk skalar tanpa tanda kutip, atau `--format jsonl` untuk menjaga hasil sebagai data terstruktur untuk pemrosesan lebih lanjut.
</Note>

## Melewatkan badan permintaan

Mekanisme input yang tepat tergantung pada bentuk data: gunakan **flag** untuk bidang skalar dan nilai terstruktur pendek, salurkan dokumen **stdin** untuk badan bersarang atau multi-baris, dan gunakan referensi **`@file`** untuk menarik konten file ke bidang string atau biner apa pun.

### Flag

Bidang skalar memetakan langsung ke flag. Bidang terstruktur menerima sintaks mirip YAML yang santai (kunci tanpa tanda kutip, tanda kutip opsional di sekitar string) atau JSON ketat:

```bash
ant beta:sessions create \
  --agent '{type: agent, id: agent_011CYm1BLqPXpQRk5khsSXrs, version: 1}' \
  --environment-id env_01595EKxaaTTGwwY3kyXdtbs \
  --title "CLI docs test session"
```

Flag yang dapat diulang membangun array. Setiap `--tool` atau `--event` menambahkan satu elemen:

```bash
ant beta:agents create \
  --name "Research Agent" \
  --model '{id: claude-opus-4-7}' \
  --tool '{type: agent_toolset_20260401}' \
  --tool '{type: custom, name: search_docs, input_schema: {type: object, properties: {query: {type: string}}}}'
```

### Stdin

Salurkan dokumen JSON atau YAML ke stdin untuk menyediakan badan permintaan lengkap. Bidang dari stdin digabungkan dengan flag, dengan flag mengambil prioritas. Di sini `version` adalah token penguncian optimis yang dikembalikan oleh `retrieve` sebelumnya, dan `$AGENT_ID` ditangkap seperti dalam [Ekstrak skalar](#extract-a-scalar):

```bash
echo '{"description": "Updated test agent.", "version": 1}' | \
  ant beta:agents update --agent-id "$AGENT_ID"
```

Heredoc bekerja dengan cara yang sama dan nyaman untuk YAML multi-baris. Kutip pembatas (seperti dalam `<<'YAML'`) untuk menonaktifkan ekspansi variabel di dalam badan.

```bash
ant beta:agents create <<'YAML'
name: Research Agent
model: claude-opus-4-7
system: |
  You are a research assistant. Cite sources for every claim.
tools:
  - type: agent_toolset_20260401
YAML
```

### Referensi file

Flag yang mengambil jalur file, seperti `--file` pada perintah upload, menerima jalur telanjang:

```bash
ant beta:files upload --file ./report.pdf
```

Untuk menggabungkan konten file ke dalam bidang bernilai string, awali jalur dengan `@`:

```bash
ant beta:agents create \
  --name "Researcher" --model '{id: claude-sonnet-4-6}' \
  --system @./prompts/researcher.txt
```

Di dalam nilai flag terstruktur, bungkus jalur dalam tanda kutip. Untuk mengirim PDF ke Messages API:

```bash
ant messages create \
  --model claude-opus-4-7 \
  --max-tokens 1024 \
  --message '{role: user, content: [
    {type: document, source: {type: base64, media_type: application/pdf, data: "@./scan.pdf"}},
    {type: text, text: "Extract the text from this scanned document."}
  ]}' \
  --transform 'content.0.text' --format yaml
```

CLI mendeteksi jenis file dan mengenkode file biner sebagai base64 secara otomatis. Untuk memaksa pengkodean spesifik gunakan `@file://` untuk teks biasa atau `@data://` untuk base64. Escape `@` literal di awal dengan garis miring terbalik (`\@username`).

## Kontrol versi sumber daya API

Anda dapat menggunakan CLI untuk mengontrol versi sumber daya API seperti keterampilan, agen, lingkungan, atau penyebaran sebagai file YAML di repositori Anda dan menjaganya tetap sinkron dengan Claude API.

<Note>
Untuk informasi lebih lanjut tentang sumber daya ini, lihat [Managed Agents](/docs/id/managed-agents/overview).
</Note>

<Steps>
<Step title="Tentukan agen Anda">

Tulis definisi agen ke `summarizer.agent.yaml`:

```yaml summarizer.agent.yaml
name: Summarizer
model: claude-sonnet-4-6
system: |
  You are a helpful assistant that writes concise summaries.
tools:
  - type: agent_toolset_20260401
```

</Step>
<Step title="Buat agen">

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
Periksa `summarizer.agent.yaml` ke dalam repositori Anda dan jaga agar tetap sinkron dengan API di pipeline CI Anda. Perintah pembaruan memerlukan ID agen dan versi saat ini sebagai flag:

```bash CLI
ant beta:agents update --agent-id agent_011CYm1BLqPXpQRk5khsSXrs --version 1 < summarizer.agent.yaml
```
</Tip>

</Step>
<Step title="Tentukan lingkungan">

Sesi berjalan di [lingkungan](/docs/id/api/cli/beta/environments), yang menentukan kontainer tempat eksekusinya. Tulis definisi lingkungan ke `summarizer.environment.yaml`:

```yaml summarizer.environment.yaml
name: summarizer-env
config:
  type: cloud
  networking:
    type: unrestricted
```

</Step>
<Step title="Buat lingkungan">

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
Periksa `summarizer.environment.yaml` ke dalam repositori Anda dan jaga agar tetap sinkron dengan API di pipeline CI Anda. Perintah pembaruan memerlukan ID lingkungan sebagai flag:

```bash CLI
ant beta:environments update --environment-id env_01595EKxaaTTGwwY3kyXdtbs < summarizer.environment.yaml
```
</Tip>

</Step>
<Step title="Mulai sesi">

Tempel `id` agen dan `id` lingkungan dari output sebelumnya ke dalam perintah pembuatan sesi:

```bash highlight={2..3}
ant beta:sessions create \
  --agent agent_011CYm1BLqPXpQRk5khsSXrs \
  --environment-id env_01595EKxaaTTGwwY3kyXdtbs \
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

Salin `id` sesi dari output sebelumnya ke dalam `--session-id`:

```bash highlight={2}
ant beta:sessions:events send \
  --session-id session_01JZCh78XvmxJjiXVy3oSi7K \
  --event '{type: user.message, content: [{type: text, text: "Summarize the benefits of type safety in one sentence."}]}'
```

</Step>
<Step title="Baca percakapan">

`--transform` berjalan terhadap setiap acara yang terdaftar, jadi ini mencetak teks setiap pesan secara berurutan:

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
Untuk menonton sesi saat berjalan, gunakan `ant beta:sessions stream --session-id session_01JZCh78XvmxJjiXVy3oSi7K`. Acara ditulis ke stdout saat tiba.
</Tip>

</Step>
</Steps>

## Pola skrip

CLI dirancang untuk dikomposisi dengan alat shell standar.

### Hubungkan output daftar ke perintah kedua

`--transform id --format yaml` pada titik akhir daftar mengeluarkan satu ID telanjang per baris, jadi alat standar seperti `head` dan `xargs` berlaku langsung. Tangkap hasil pertama, kemudian teruskan ke perintah lanjutan:

```bash
FIRST_AGENT=$(ant beta:agents list \
  --transform id --format yaml | head -1)

ant beta:agents:versions list \
  --agent-id "$FIRST_AGENT" \
  --transform "{version,created_at}" --format jsonl
```

### Periksa kesalahan

Flag `--transform-error` dan `--format-error` mencerminkan rekan jalur kesuksesan mereka dan mengikuti aturan yang sama — pasangkan dengan `yaml`, bukan `raw`, untuk menerapkan transformasi. Ekstrak hanya pesan kesalahan:

```bash
ant beta:agents retrieve --agent-id bogus \
  --transform-error error.message --format-error yaml 2>&1
```

```text Output
GET "https://api.anthropic.com/v1/agents/bogus?beta=true": 404 Not Found
Agent not found.
```

## Gunakan CLI dari Claude Code

[Claude Code](https://docs.claude.com/en/docs/claude-code/overview) tahu dari kotak cara menggunakan CLI `ant`. Dengan CLI terinstal dan `ANTHROPIC_API_KEY` diatur, Anda dapat meminta Claude Code untuk beroperasi pada sumber daya API Anda secara langsung — misalnya:

- "Daftar sesi agen terbaru saya dan ringkas mana yang mengalami kesalahan."
- "Unggah setiap PDF di `./reports` ke Files API dan cetak ID yang dihasilkan."
- "Tarik acara untuk sesi `session_01...` dan beri tahu saya di mana agen terjebak."

Claude Code shell keluar ke `ant`, mengurai output terstruktur, dan bernalar atas hasil — tidak diperlukan kode integrasi khusus.

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

CLI mengirimkan skrip penyelesaian untuk bash, zsh, fish, dan PowerShell. Hasilkan dan instal satu untuk shell Anda:

<Tabs>
<Tab title="zsh">

```bash
ant @completion zsh > "${fpath[1]}/_ant"
# Restart your shell or run: autoload -U compinit && compinit
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
# To persist across sessions:
# ant @completion powershell >> $PROFILE
```

</Tab>
</Tabs>

## Sumber daya yang tersedia

Setiap sumber daya API yang diekspos CLI didokumentasikan dalam [referensi API](/docs/id/api/cli/messages/create). Untuk daftar lokal, jalankan `ant --help`, dan tambahkan `--help` ke subperintah apa pun untuk flag dan parameternya.