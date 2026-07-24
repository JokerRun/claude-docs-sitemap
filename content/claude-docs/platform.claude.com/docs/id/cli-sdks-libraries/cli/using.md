---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/using
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 966e6229932fa7238380e381f0fd09ff378b72f167481f6f8ff22648d93589cc
---

# Menggunakan CLI

Struktur perintah, format output, transformasi GJSON, body permintaan, dan debugging untuk CLI ant.

---

Halaman ini membahas mekanisme input dan output CLI `ant` yang berlaku di semua endpoint. Untuk instalasi dan autentikasi, lihat [Quickstart](/docs/id/cli-sdks-libraries/cli/quickstart). Untuk merangkai perintah dan mengelola versi sumber daya, lihat [Scripting dan otomatisasi CLI](/docs/id/cli-sdks-libraries/cli/scripting).

## Struktur perintah

Perintah mengikuti pola `resource action`. Sumber daya bersarang menggunakan tanda titik dua:

```text wrap
ant <resource>[:<subresource>] <action> [flags]
```

Jalankan `ant --help` untuk daftar sumber daya lengkap, atau tambahkan `--help` ke subperintah mana pun untuk melihat flag-nya.

Sumber daya dalam tahap beta (termasuk agents, sessions, deployments, environments, dan skills) berada di bawah prefiks `beta:`. Perintah dalam namespace ini secara otomatis mengirimkan header `anthropic-beta` yang sesuai untuk sumber daya tersebut, sehingga Anda tidak perlu meneruskannya sendiri. Gunakan `--beta <header>` hanya untuk menimpa nilai default (misalnya, untuk memilih versi skema yang berbeda).

```bash
ant models list
ant messages create --model claude-opus-4-8 --max-tokens 1024 ...
ant beta:agents retrieve --agent-id agent_01...
ant beta:sessions:events list --session-id session_01...
```

### Flag global

| Flag                                  | Deskripsi                                                                                                                                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--profile`                           | Profil bernama yang digunakan untuk pemanggilan ini (setara dengan mengatur `ANTHROPIC_PROFILE`). Lihat [Beralih antar workspace](/docs/id/cli-sdks-libraries/cli/authentication#switch-between-workspaces). |
| `--format`                            | Format output: `auto`, `json`, `jsonl`, `yaml`, `pretty`, `raw`, `explore`                                                                                                                                   |
| `--transform`                         | Memfilter atau membentuk ulang respons dengan [path GJSON](#transform-output-with-gjson)                                                                                                                     |
| `-r`, `--raw-output`                  | Mencetak hasil string tanpa tanda kutip di sekelilingnya, seperti `jq -r`                                                                                                                                    |
| `--base-url`                          | Menimpa URL dasar API                                                                                                                                                                                        |
| `--debug`                             | Mencetak permintaan dan respons HTTP lengkap ke stderr                                                                                                                                                       |
| `--format-error`, `--transform-error` | Sama seperti `--format` dan `--transform` tetapi diterapkan pada [respons error](/docs/id/cli-sdks-libraries/cli/scripting#inspect-errors)                                                                   |

## Format output

`auto` mencetak JSON dengan format rapi (pretty-print) dan merupakan default untuk perintah yang membuat atau memodifikasi sumber daya. Perintah list dan retrieve secara default menggunakan [explorer interaktif](#interactive-explorer) saat menulis ke terminal, dan JSON dengan format rapi saat di-pipe. Timpa salah satu default tersebut dengan `--format`:

```bash
ant models retrieve --model-id claude-opus-4-8 --format yaml
```

```yaml Output
type: model
id: claude-opus-4-8
display_name: Claude Opus 4.8
created_at: "2026-02-04T00:00:00Z"
...
```

Endpoint list melakukan paginasi otomatis. Dalam format default, setiap item ditulis secara terpisah (satu objek JSON kompak per baris dalam mode `jsonl`, aliran dokumen YAML dalam mode `yaml`), yang mengalir dengan mulus ke `head`, `grep`, dan filter `--transform`.

### Explorer interaktif

Explorer adalah TUI lipat-dan-cari untuk menjelajahi respons berukuran besar. Tombol panah memperluas dan menciutkan node, `/` untuk mencari, `q` untuk keluar. Perintah list dan retrieve membukanya secara default saat terhubung ke terminal. Berikan `--format explore` untuk membukanya secara eksplisit:

```bash
ant models list --format explore
```

## Transformasi output dengan GJSON

Gunakan `--transform` untuk membentuk ulang respons sebelum dicetak. Ekspresinya adalah [path GJSON](https://github.com/tidwall/gjson/blob/master/SYNTAX.md). Untuk endpoint list, transformasi dijalankan terhadap setiap item secara individual, bukan terhadap envelope-nya:

```bash
ant beta:agents list \
  --transform "{id,name,model}" \
  --format jsonl
```

```jsonl Output
{"id": "agent_011CYm1BLqPX...", "name": "Docs CLI Test Agent", "model": "claude-opus-4-8"}
{"id": "agent_011CYkVwfaEt...", "name": "Coffee Making Assistant", "model": "claude-opus-4-8"}
{"id": "agent_011CYixHhtUP...", "name": "Coding Assistant", "model": "claude-opus-4-8"}
```

### Mengekstrak nilai skalar

Untuk menangkap satu field sebagai string tanpa tanda kutip (misalnya, ID dari sumber daya yang baru dibuat), padukan `--transform` dengan `--raw-output`. Hasilnya dicetak tanpa tanda kutip JSON dan siap untuk ditetapkan ke variabel shell:

```bash
AGENT_ID=$(ant beta:agents create \
  --name "My Agent" \
  --model '{id: claude-opus-4-8}' \
  --transform id --raw-output)

printf '%s\n' "$AGENT_ID"
```

```text Output wrap
agent_011CYm1BLqPXpQRk5khsSXrs
```

<Note>
  `--raw-output` berbeda dari `--format raw`. `--raw-output` menghapus tanda kutip JSON dari hasil string, seperti `jq -r`. `--format raw` mencetak byte JSON mentah dari body respons tanpa paginasi otomatis; pada endpoint list, opsi ini menerapkan `--transform` pada envelope paginasi, bukan pada setiap item.
</Note>

## Meneruskan body permintaan

Mekanisme input yang tepat bergantung pada bentuk datanya: gunakan **flag** untuk field skalar dan nilai terstruktur yang pendek, pipe dokumen melalui **stdin** untuk body bersarang atau multibaris, dan gunakan **referensi `@file`** untuk menarik isi file ke dalam field string atau biner mana pun.

### Flag

Field skalar dipetakan langsung ke flag. Field terstruktur menerima sintaks longgar mirip YAML (kunci tanpa tanda kutip, tanda kutip opsional di sekitar string) atau JSON ketat:

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
  --model '{id: claude-opus-4-8}' \
  --tool '{type: agent_toolset_20260401}' \
  --tool '{type: custom, name: search_docs, input_schema: {type: object, properties: {query: {type: string}}}}'
```

### Stdin

Pipe dokumen JSON atau YAML ke stdin untuk menyediakan body permintaan lengkap. Field dari stdin digabungkan dengan flag, dengan flag yang diprioritaskan. Di sini `version` adalah token optimistic-locking yang dikembalikan oleh `retrieve` sebelumnya, dan `$AGENT_ID` ditangkap seperti pada [Mengekstrak nilai skalar](#extract-a-scalar):

```bash
echo '{"description": "Updated test agent.", "version": 1}' | \
  ant beta:agents update --agent-id "$AGENT_ID"
```

Heredoc bekerja dengan cara yang sama dan praktis untuk YAML multibaris. Beri tanda kutip pada delimiter (seperti pada `<<'YAML'`) untuk menonaktifkan ekspansi variabel di dalam body.

```bash
ant beta:agents create <<'YAML'
name: Research Agent
model: claude-opus-4-8
system: |
  You are a research assistant. Cite sources for every claim.
tools:
  - type: agent_toolset_20260401
YAML
```

### Referensi file

Flag yang menerima path file, seperti `--file` pada perintah upload, menerima path biasa:

```bash
ant beta:files upload --file ./report.pdf
```

Untuk menyisipkan isi file ke dalam field bernilai string, awali path dengan `@`:

```bash
ant beta:agents create \
  --name "Researcher" --model '{id: claude-opus-4-8}' \
  --system @./prompts/researcher.txt
```

Di dalam nilai flag terstruktur, bungkus path dengan tanda kutip. Untuk mengirim PDF ke Messages API:

```bash
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --message '{role: user, content: [
    {type: document, source: {type: base64, media_type: application/pdf, data: "@./scan.pdf"}},
    {type: text, text: "Extract the text from this scanned document."}
  ]}' \
  --transform 'content.0.text' --raw-output
```

CLI mendeteksi tipe file dan mengenkode file biner sebagai base64 secara otomatis. Untuk memaksa enkoding tertentu, gunakan `@file://` untuk teks biasa atau `@data://` untuk base64. Escape karakter `@` literal di awal dengan backslash (`\@username`).

## Debugging

Tambahkan `--debug` ke perintah mana pun untuk mencetak permintaan dan respons HTTP yang tepat (header dan body) ke stderr. Kunci API akan disamarkan.

```bash
ant --debug beta:agents list
```

```text Output wrap
GET /v1/agents?beta=true HTTP/1.1
Host: api.anthropic.com
Anthropic-Beta: managed-agents-2026-04-01
Anthropic-Version: 2023-06-01
X-Api-Key: <REDACTED>
...
```

## Sumber daya yang tersedia

Setiap sumber daya API yang diekspos oleh CLI didokumentasikan dalam [referensi API](/docs/id/api/cli/messages/create). Untuk daftar lokal, jalankan `ant --help`, dan tambahkan `--help` ke subperintah mana pun untuk melihat flag dan parameternya.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Scripting dan otomatisasi CLI" icon="code" href="/docs/id/cli-sdks-libraries/cli/scripting">
    Mengelola versi sumber daya API, pola scripting, dan penggunaan dari Claude Code
  </Card>

  <Card title="Referensi API" icon="book" href="/docs/id/api/cli/messages/create">
    Parameter spesifik endpoint, field permintaan, dan skema respons
  </Card>

  <Card title="Opsi autentikasi CLI" icon="lock" href="/docs/id/cli-sdks-libraries/cli/authentication">
    Kunci API, host headless, beberapa workspace, dan profil bernama
  </Card>
</CardGroup>
