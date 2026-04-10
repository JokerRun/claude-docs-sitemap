---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: c89598892909b9a399d5a0a75e878c404f3373816768d67f394f9e347a6422de
---

# Alat Bash

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Alat bash memungkinkan Claude untuk menjalankan perintah shell dalam sesi bash yang persisten, memungkinkan operasi sistem, eksekusi skrip, dan otomasi baris perintah. Akses shell adalah kemampuan agen yang mendasar. Pada [Terminal-Bench 2.0](https://github.com/terminal-bench/terminal-bench), sebuah tolok ukur yang mengevaluasi tugas terminal dunia nyata menggunakan validasi khusus shell, Claude menunjukkan peningkatan kinerja yang signifikan dengan akses ke sesi bash yang persisten.

## Ikhtisar

Alat bash menyediakan Claude dengan:
- Sesi bash persisten yang mempertahankan status
- Kemampuan untuk menjalankan perintah shell apa pun
- Akses ke variabel lingkungan dan direktori kerja
- Kemampuan chaining perintah dan skrip

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Kasus penggunaan

- **Alur kerja pengembangan:** Jalankan perintah build, pengujian, dan alat pengembangan
- **Otomasi sistem:** Jalankan skrip, kelola file, otomasi tugas
- **Pemrosesan data:** Proses file, jalankan skrip analisis, kelola dataset
- **Pengaturan lingkungan:** Instal paket, konfigurasi lingkungan

## Mulai cepat

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "tools": [
      {
        "type": "bash_20250124",
        "name": "bash"
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "List all Python files in the current directory."
      }
    ]
  }'
```

```bash CLI
ant messages create \
  --model claude-opus-4-6 \
  --max-tokens 1024 \
  --tool '{type: bash_20250124, name: bash}' \
  --message '{role: user, content: List all Python files in the current directory.}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[{"type": "bash_20250124", "name": "bash"}],
    messages=[
        {"role": "user", "content": "List all Python files in the current directory."}
    ],
)

print(response)
```
</CodeGroup>

## Cara kerjanya

Alat bash mempertahankan sesi yang persisten:

1. Claude menentukan perintah apa yang akan dijalankan
2. Anda menjalankan perintah dalam shell bash
3. Kembalikan output (stdout dan stderr) ke Claude
4. Status sesi tetap ada di antara perintah (variabel lingkungan, direktori kerja)

## Parameter

| Parameter | Diperlukan | Deskripsi |
|-----------|----------|-------------|
| `command` | Ya* | Perintah bash yang akan dijalankan |
| `restart` | Tidak | Atur ke `true` untuk memulai ulang sesi bash |

*Diperlukan kecuali menggunakan `restart`

<section title="Contoh penggunaan">

Jalankan perintah:

```json
{
  "command": "ls -la *.py"
}
```

Mulai ulang sesi:

```json
{
  "restart": true
}
```

</section>

## Contoh: Otomasi multi-langkah

Claude dapat merangkai perintah untuk menyelesaikan tugas yang kompleks:

```text
Permintaan pengguna:
"Instal pustaka requests dan buat skrip Python sederhana yang
mengambil lelucon dari API, lalu jalankan."

Penggunaan alat Claude:
1. Instal paket
   {"command": "pip install requests"}

2. Buat skrip
   {"command": "cat > fetch_joke.py << 'EOF'\nimport requests\nresponse = requests.get('https://official-joke-api.appspot.com/random_joke')\njoke = response.json()\nprint(f\"Setup: {joke['setup']}\")\nprint(f\"Punchline: {joke['punchline']}\")\nEOF"}

3. Jalankan skrip
   {"command": "python fetch_joke.py"}
```

Sesi mempertahankan status di antara perintah, sehingga file yang dibuat di langkah 2 tersedia di langkah 3.

## Implementasikan alat bash

Alat bash diimplementasikan sebagai alat tanpa skema. Saat menggunakan alat ini, Anda tidak perlu menyediakan skema input seperti alat lainnya; skema sudah tertanam dalam model Claude dan tidak dapat dimodifikasi.

<Steps>
  <Step title="Siapkan lingkungan bash">
    Buat sesi bash persisten yang dapat berinteraksi dengan Claude:
    ```python hidelines={-2..-1}
    import subprocess
    import threading
    import queue


    class BashSession:
        def __init__(self):
            self.process = subprocess.Popen(
                ["/bin/bash"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,
            )
            self.output_queue = queue.Queue()
            self.error_queue = queue.Queue()
            self._start_readers()

        def _start_readers(self): ...
    ```
  </Step>
  <Step title="Tangani eksekusi perintah">
    Buat fungsi untuk menjalankan perintah dan menangkap output:
    ```python hidelines={1..2,-1}
    class BashSession:
        def _read_output(self, timeout): ...
        def execute_command(self, command):
            # Send command to bash
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()

            # Capture output with timeout
            output = self._read_output(timeout=10)
            return output

        process = None
    ```
  </Step>
  <Step title="Proses panggilan alat Claude">
    Ekstrak dan jalankan perintah dari respons Claude:
    ```python hidelines={1..6}
    from types import SimpleNamespace as _SN

    response = _SN(
        content=[_SN(type="tool_use", name="bash", input={"command": "ls"}, id="toolu_01")]
    )
    bash_session = _SN(restart=lambda: None, execute_command=lambda c: "output")
    for content in response.content:
        if content.type == "tool_use" and content.name == "bash":
            if content.input.get("restart"):
                bash_session.restart()
                result = "Bash session restarted"
            else:
                command = content.input.get("command")
                result = bash_session.execute_command(command)

            # Return result to Claude
            tool_result = {
                "type": "tool_result",
                "tool_use_id": content.id,
                "content": result,
            }
    ```
  </Step>
  <Step title="Implementasikan langkah-langkah keamanan">
    Tambahkan validasi dan pembatasan. Gunakan daftar izin daripada daftar blokir, karena daftar blokir mudah dilewati. Tolak operator shell agar perintah yang dirantai tidak dapat melewati daftar izin:
    ```python
    import shlex

    ALLOWED_COMMANDS = {"ls", "cat", "echo", "pwd", "grep", "find", "wc", "head", "tail"}
    SHELL_OPERATORS = {"&&", "||", "|", ";", "&", ">", "<", ">>"}


    def validate_command(command):
        # Allow only commands from an explicit allowlist
        try:
            tokens = shlex.split(command)
        except ValueError:
            return False, "Could not parse command"

        if not tokens:
            return False, "Empty command"

        executable = tokens[0]
        if executable not in ALLOWED_COMMANDS:
            return False, f"Command '{executable}' is not in the allowlist"

        # Reject shell operators that would chain additional commands
        for token in tokens[1:]:
            if token in SHELL_OPERATORS or token.startswith(("$", "`")):
                return False, f"Shell operator '{token}' is not allowed"

        return True, None
    ```
    Pemeriksaan ini adalah lini pertahanan pertama. Untuk isolasi yang lebih kuat, jalankan perintah yang telah divalidasi dengan `shell=False` dan berikan `shlex.split(command)` sebagai daftar argumen, sehingga shell tidak pernah menginterpretasikan string tersebut.
  </Step>
</Steps>

### Tangani kesalahan

Saat mengimplementasikan alat bash, tangani berbagai skenario kesalahan:

<section title="Batas waktu eksekusi perintah">

Jika perintah membutuhkan waktu terlalu lama untuk dijalankan:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Command timed out after 30 seconds",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Perintah tidak ditemukan">

Jika perintah tidak ada:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "bash: nonexistentcommand: command not found",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Izin ditolak">

Jika ada masalah izin:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "bash: /root/sensitive-file: Permission denied",
      "is_error": true
    }
  ]
}
```

</section>

### Ikuti praktik terbaik implementasi

<section title="Gunakan batas waktu perintah">

Implementasikan batas waktu untuk mencegah perintah yang menggantung:
```python hidelines={1..3}
import subprocess


def execute_with_timeout(command, timeout=30):
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds"
```

</section>

<section title="Pertahankan status sesi">

Jaga sesi bash tetap persisten untuk mempertahankan variabel lingkungan dan direktori kerja:
```python
# Commands run in the same session maintain state
commands = [
    "cd /tmp",
    "echo 'Hello' > test.txt",
    "cat test.txt",  # This works because we're still in /tmp
]
```

</section>

<section title="Tangani output besar">

Potong output yang sangat besar untuk mencegah masalah batas token:
```python
def truncate_output(output, max_lines=100):
    lines = output.split("\n")
    if len(lines) > max_lines:
        truncated = "\n".join(lines[:max_lines])
        return f"{truncated}\n\n... Output truncated ({len(lines)} total lines) ..."
    return output
```

</section>

<section title="Catat semua perintah">

Simpan jejak audit dari perintah yang dijalankan:
```python
import logging


def log_command(command, output, user_id):
    logging.info(f"User {user_id} executed: {command}")
    logging.info(f"Output: {output[:200]}...")  # Log first 200 chars
```

</section>

<section title="Sanitasi output">

Hapus informasi sensitif dari output perintah:
```python
def sanitize_output(output):
    # Remove potential secrets or credentials
    import re

    # Example: Remove AWS credentials
    output = re.sub(r"aws_access_key_id\s*=\s*\S+", "aws_access_key_id=***", output)
    output = re.sub(
        r"aws_secret_access_key\s*=\s*\S+", "aws_secret_access_key=***", output
    )
    return output
```

</section>

## Keamanan

<Warning>
Alat bash menyediakan akses sistem langsung. Implementasikan langkah-langkah keamanan penting berikut:
- Menjalankan dalam lingkungan terisolasi (Docker/VM)
- Mengimplementasikan penyaringan perintah dan daftar izin
- Menetapkan batas sumber daya (CPU, memori, disk)
- Mencatat semua perintah yang dijalankan
</Warning>

### Rekomendasi utama
- Gunakan `ulimit` untuk menetapkan batasan sumber daya
- Filter perintah berbahaya (`sudo`, `rm -rf`, dll.)
- Jalankan dengan izin pengguna minimal
- Pantau dan catat semua eksekusi perintah

## Harga

The bash tool adds **245 input tokens** to your API calls.

Additional tokens are consumed by:
- Command outputs (stdout/stderr)
- Error messages
- Large file contents

Lihat [harga penggunaan alat](/docs/id/agents-and-tools/tool-use/overview#pricing) untuk detail harga lengkap.

## Pola umum

### Alur kerja pengembangan
- Menjalankan pengujian: `pytest && coverage report`
- Membangun proyek: `npm install && npm run build`
- Operasi Git: `git status && git add . && git commit -m "message"`

#### Checkpointing berbasis Git

Git berfungsi sebagai mekanisme pemulihan terstruktur dalam alur kerja agen yang berjalan lama, bukan hanya cara untuk menyimpan perubahan:

- **Tangkap baseline:** Sebelum pekerjaan agen dimulai, commit status saat ini. Ini adalah titik awal yang diketahui baik.
- **Commit per fitur:** Setiap fitur yang selesai mendapatkan commit-nya sendiri. Ini berfungsi sebagai titik rollback jika ada yang salah kemudian.
- **Rekonstruksi status di awal sesi:** Baca `git log` bersama file kemajuan untuk memahami apa yang sudah selesai dan apa yang berikutnya.
- **Kembalikan saat gagal:** Jika pekerjaan bermasalah, `git checkout` mengembalikan ke commit terakhir yang baik alih-alih mencoba men-debug status yang rusak.

### Operasi file
- Memproses data: `wc -l *.csv && ls -lh *.csv`
- Mencari file: `find . -name "*.py" | xargs grep "pattern"`
- Membuat cadangan: `tar -czf backup.tar.gz ./data`

### Tugas sistem
- Memeriksa sumber daya: `df -h && free -m`
- Manajemen proses: `ps aux | grep python`
- Pengaturan lingkungan: `export PATH=$PATH:/new/path && echo $PATH`

## Keterbatasan

- **Tidak ada perintah interaktif:** Tidak dapat menangani `vim`, `less`, atau prompt kata sandi
- **Tidak ada aplikasi GUI:** Hanya baris perintah
- **Cakupan sesi:** Status sesi bash berada di sisi klien. API bersifat stateless. Aplikasi Anda bertanggung jawab untuk mempertahankan sesi shell di antara giliran.
- **Batas output:** Output besar mungkin dipotong
- **Tidak ada streaming:** Hasil dikembalikan setelah selesai

## Menggabungkan dengan alat lain

Alat bash paling kuat ketika dikombinasikan dengan [editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) dan alat lainnya.

<Note>
Jika Anda juga menggunakan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool), Claude memiliki akses ke dua lingkungan eksekusi terpisah: sesi bash lokal Anda dan kontainer sandbox Anthropic. Status tidak dibagikan di antara keduanya. Lihat [Menggunakan eksekusi kode dengan alat eksekusi lainnya](/docs/id/agents-and-tools/tool-use/code-execution-tool#using-code-execution-with-other-execution-tools) untuk panduan tentang cara meminta Claude membedakan antara lingkungan.
</Note>

## Langkah berikutnya

<CardGroup cols={2}>
  <Card
    title="Ikhtisar penggunaan alat"
    icon="tool"
    href="/docs/id/agents-and-tools/tool-use/overview"
  >
    Pelajari tentang penggunaan alat dengan Claude
  </Card>

  <Card
    title="Alat editor teks"
    icon="file"
    href="/docs/id/agents-and-tools/tool-use/text-editor-tool"
  >
    Lihat dan edit file teks dengan Claude
  </Card>
</CardGroup>