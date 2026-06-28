---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 7f1f8fb20baa6d49d664a71efe3e73231b154eb7d2f080e037cac60b60b31155
---

# Alat Bash

---

<Note>
  Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Alat bash memungkinkan Claude untuk mengeksekusi perintah shell dalam sesi bash yang persisten, memungkinkan operasi sistem, eksekusi skrip, dan otomatisasi baris perintah. Akses shell adalah kemampuan agen yang fundamental. Pada [Terminal-Bench 2.0](https://github.com/terminal-bench/terminal-bench), sebuah benchmark yang mengevaluasi tugas terminal dunia nyata menggunakan validasi berbasis shell saja, Claude menunjukkan peningkatan performa yang kuat dengan akses ke sesi bash yang persisten.

## Ikhtisar

Alat bash menyediakan Claude dengan:

* Sesi bash persisten yang mempertahankan state
* Kemampuan untuk menjalankan perintah shell apa pun
* Akses ke variabel lingkungan dan direktori kerja
* Kemampuan perangkaian perintah dan scripting

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Kasus penggunaan

* **Alur kerja pengembangan:** Menjalankan perintah build, pengujian, dan alat pengembangan
* **Otomatisasi sistem:** Mengeksekusi skrip, mengelola file, mengotomatisasi tugas
* **Pemrosesan data:** Memproses file, menjalankan skrip analisis, mengelola dataset
* **Penyiapan lingkungan:** Menginstal paket, mengonfigurasi lingkungan

## Mulai cepat

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
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
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --tool '{type: bash_20250124, name: bash}' \
    --message '{role: user, content: List all Python files in the current directory.}'
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=[{"type": "bash_20250124", "name": "bash"}],
      messages=[
          {"role": "user", "content": "List all Python files in the current directory."}
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [{ type: "bash_20250124", name: "bash" }],
    messages: [
      {
        role: "user",
        content: "List all Python files in the current directory."
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;

  var client = new AnthropicClient();

  var response = await client.Messages.Create(
      new()
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Tools = [new ToolBash20250124()],
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "List all Python files in the current directory.",
              },
          ],
      }
  );

  Console.WriteLine(response);
  ```

  ```go Go
  func main() {
  	client := anthropic.NewClient()

  	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Tools: []anthropic.ToolUnionParam{
  			{OfBashTool20250124: &anthropic.ToolBash20250124Param{}},
  		},
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("List all Python files in the current directory.")),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.ToolBash20250124;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Message response = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024)
              .addTool(ToolBash20250124.builder().build())
              .addUserMessage("List all Python files in the current directory.")
              .build()
      );

      IO.println(response);
  }
  ```

  ```php PHP

  use Anthropic\Client;
  use Anthropic\Messages\ToolBash20250124;

  $client = new Client();

  $response = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      tools: [new ToolBash20250124()],
      messages: [
          ['role' => 'user', 'content' => 'List all Python files in the current directory.'],
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [{type: "bash_20250124", name: "bash"}],
    messages: [
      {role: "user", content: "List all Python files in the current directory."}
    ]
  )

  puts response
  ```
</CodeGroup>

## Cara kerjanya

Alat bash mempertahankan sesi yang persisten:

1. Claude menentukan perintah apa yang akan dijalankan
2. Anda mengeksekusi perintah tersebut dalam shell bash
3. Kembalikan output (stdout dan stderr) ke Claude
4. State sesi tetap bertahan di antara perintah (variabel lingkungan, direktori kerja)

## Parameter

| Parameter | Wajib | Deskripsi                                    |
| --------- | ----- | -------------------------------------------- |
| `command` | Ya\*  | Perintah bash yang akan dijalankan           |
| `restart` | Tidak | Atur ke `true` untuk memulai ulang sesi bash |

\*Wajib kecuali menggunakan `restart`

<Accordion title="Contoh penggunaan">
  Menjalankan perintah:

  ```json
  {
    "command": "ls -la *.py"
  }
  ```

  Memulai ulang sesi:

  ```json
  {
    "restart": true
  }
  ```
</Accordion>

## Contoh: Otomatisasi multi-langkah

Claude dapat merangkai perintah untuk menyelesaikan tugas yang kompleks:

```text
User request:
"Install the requests library and create a simple Python script that
fetches a joke from an API, then run it."

Claude's tool uses:
1. Install package
   {"command": "pip install requests"}

2. Create script
   {"command": "cat > fetch_joke.py << 'EOF'\nimport requests\nresponse = requests.get('https://official-joke-api.appspot.com/random_joke')\njoke = response.json()\nprint(f\"Setup: {joke['setup']}\")\nprint(f\"Punchline: {joke['punchline']}\")\nEOF"}

3. Run script
   {"command": "python fetch_joke.py"}
```

Sesi mempertahankan state di antara perintah, sehingga file yang dibuat pada langkah 2 tersedia pada langkah 3.

## Mengimplementasikan alat bash

Alat bash diimplementasikan sebagai alat tanpa skema. Saat menggunakan alat ini, Anda tidak perlu menyediakan skema input seperti pada alat lainnya; skema sudah terintegrasi ke dalam model Claude dan tidak dapat dimodifikasi.

<Steps>
  <Step title="Siapkan lingkungan bash">
    Buat sesi bash persisten yang dapat berinteraksi dengan Claude:

    ```python
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
    ```
  </Step>

  <Step title="Tangani eksekusi perintah">
    Buat fungsi untuk mengeksekusi perintah dan menangkap output:

    ```python
    def execute_command(self, command):
        # Kirim perintah ke bash
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

        # Tangkap output dengan timeout
        output = self._read_output(timeout=10)
        return output

    ```
  </Step>

  <Step title="Proses panggilan alat dari Claude">
    Ekstrak dan eksekusi perintah dari respons Claude:

    ```python
    for content in response.content:
        if content.type == "tool_use" and content.name == "bash":
            if content.input.get("restart"):
                bash_session.restart()
                result = "Bash session restarted"
            else:
                command = content.input.get("command")
                result = bash_session.execute_command(command)

            # Kembalikan hasil ke Claude
            tool_result = {
                "type": "tool_result",
                "tool_use_id": content.id,
                "content": result,
            }
    ```
  </Step>

  <Step title="Implementasikan langkah-langkah keamanan">
    Tambahkan validasi dan pembatasan. Gunakan allowlist (daftar izin) daripada blocklist (daftar blokir), karena blocklist mudah dilewati. Tolak operator shell agar perintah berantai tidak dapat lolos dari allowlist:

    ```python
    import shlex

    ALLOWED_COMMANDS = {"ls", "cat", "echo", "pwd", "grep", "find", "wc", "head", "tail"}
    SHELL_OPERATORS = {"&&", "||", "|", ";", "&", ">", "<", ">>"}


    def validate_command(command):
        # Izinkan hanya perintah dari allowlist eksplisit
        try:
            tokens = shlex.split(command)
        except ValueError:
            return False, "Could not parse command"

        if not tokens:
            return False, "Empty command"

        executable = tokens[0]
        if executable not in ALLOWED_COMMANDS:
            return False, f"Command '{executable}' is not in the allowlist"

        # Tolak operator shell yang akan merangkai perintah tambahan
        for token in tokens[1:]:
            if token in SHELL_OPERATORS or token.startswith(("$", "`")):
                return False, f"Shell operator '{token}' is not allowed"

        return True, None
    ```

    Pemeriksaan ini adalah garis pertahanan pertama. Untuk isolasi yang lebih kuat, jalankan perintah yang telah divalidasi dengan `shell=False` dan berikan `shlex.split(command)` sebagai daftar argumen, sehingga shell tidak pernah menginterpretasikan string tersebut.
  </Step>
</Steps>

### Menangani error

Saat mengimplementasikan alat bash, tangani berbagai skenario error:

<AccordionGroup>
  <Accordion title="Timeout eksekusi perintah">
    Jika sebuah perintah membutuhkan waktu terlalu lama untuk dieksekusi:

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
  </Accordion>

  <Accordion title="Perintah tidak ditemukan">
    Jika sebuah perintah tidak ada:

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
  </Accordion>

  <Accordion title="Izin ditolak">
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
  </Accordion>
</AccordionGroup>

### Ikuti praktik terbaik implementasi

<AccordionGroup>
  <Accordion title="Gunakan timeout perintah">
    Implementasikan timeout untuk mencegah perintah yang menggantung:

    ```python
    def execute_with_timeout(command, timeout=30):
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=timeout
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return f"Command timed out after {timeout} seconds"
    ```
  </Accordion>

  <Accordion title="Pertahankan state sesi">
    Jaga agar sesi bash tetap persisten untuk mempertahankan variabel lingkungan dan direktori kerja:

    ```python
    # Perintah yang dijalankan dalam sesi yang sama mempertahankan state
    commands = [
        "cd /tmp",
        "echo 'Hello' > test.txt",
        "cat test.txt",  # This works because we're still in /tmp
    ]
    ```
  </Accordion>

  <Accordion title="Tangani output besar">
    Potong output yang sangat besar untuk mencegah masalah batas token:

    ```python
    def truncate_output(output, max_lines=100):
        lines = output.split("\n")
        if len(lines) > max_lines:
            truncated = "\n".join(lines[:max_lines])
            return f"{truncated}\n\n... Output truncated ({len(lines)} total lines) ..."
        return output
    ```
  </Accordion>

  <Accordion title="Catat semua perintah">
    Simpan jejak audit dari perintah yang dieksekusi:

    ```python
    import logging


    def log_command(command, output, user_id):
        logging.info(f"User {user_id} executed: {command}")
        logging.info(f"Output: {output[:200]}...")  # Log first 200 chars
    ```
  </Accordion>

  <Accordion title="Sanitasi output">
    Hapus informasi sensitif dari output perintah:

    ```python
    def sanitize_output(output):
        # Hapus potensi rahasia atau kredensial
        import re

        # Contoh: Hapus kredensial AWS
        output = re.sub(r"aws_access_key_id\s*=\s*\S+", "aws_access_key_id=***", output)
        output = re.sub(
            r"aws_secret_access_key\s*=\s*\S+", "aws_secret_access_key=***", output
        )
        return output
    ```
  </Accordion>
</AccordionGroup>

## Keamanan

<Warning>
  Alat bash menyediakan akses sistem langsung. Implementasikan langkah-langkah keamanan penting berikut:

  * Menjalankan dalam lingkungan terisolasi (Docker/VM)
  * Mengimplementasikan pemfilteran perintah dan allowlist
  * Menetapkan batas sumber daya (CPU, memori, disk)
  * Mencatat semua perintah yang dieksekusi
</Warning>

### Rekomendasi utama

* Gunakan `ulimit` untuk menetapkan batasan sumber daya
* Filter perintah berbahaya (`sudo`, `rm -rf`, dll.)
* Jalankan dengan izin pengguna minimal
* Pantau dan catat semua eksekusi perintah

## Harga

Alat bash menambahkan **245 token input** ke panggilan API Anda.

Token tambahan dikonsumsi oleh:

* Output perintah (stdout/stderr)
* Pesan kesalahan
* Konten file berukuran besar

Lihat [harga penggunaan alat](/docs/id/agents-and-tools/tool-use/overview#pricing) untuk detail harga lengkap.

## Pola umum

### Alur kerja pengembangan

* Menjalankan pengujian: `pytest && coverage report`
* Membangun proyek: `npm install && npm run build`
* Operasi Git: `git status && git add . && git commit -m "message"`

#### Checkpointing berbasis Git

Git berfungsi sebagai mekanisme pemulihan terstruktur dalam alur kerja agen yang berjalan lama, bukan hanya cara untuk menyimpan perubahan:

* **Tangkap baseline:** Sebelum pekerjaan agen dimulai, commit state saat ini. Ini adalah titik awal yang diketahui baik.
* **Commit per fitur:** Setiap fitur yang selesai mendapatkan commit-nya sendiri. Ini berfungsi sebagai titik rollback jika terjadi kesalahan di kemudian hari.
* **Rekonstruksi state di awal sesi:** Baca `git log` bersama dengan file progres untuk memahami apa yang sudah dilakukan dan apa yang akan dilakukan selanjutnya.
* **Revert saat gagal:** Jika pekerjaan menyimpang, `git checkout` mengembalikan ke commit baik terakhir alih-alih mencoba men-debug state yang rusak.

### Operasi file

* Memproses data: `wc -l *.csv && ls -lh *.csv`
* Mencari file: `find . -name "*.py" | xargs grep "pattern"`
* Membuat backup: `tar -czf backup.tar.gz ./data`

### Tugas sistem

* Memeriksa sumber daya: `df -h && free -m`
* Manajemen proses: `ps aux | grep python`
* Penyiapan lingkungan: `export PATH=$PATH:/new/path && echo $PATH`

## Keterbatasan

* **Tidak ada perintah interaktif:** Tidak dapat menangani `vim`, `less`, atau prompt kata sandi
* **Tidak ada aplikasi GUI:** Hanya baris perintah
* **Cakupan sesi:** State sesi bash berada di sisi klien. API bersifat stateless. Aplikasi Anda bertanggung jawab untuk mempertahankan sesi shell di antara giliran.
* **Batas output:** Output besar mungkin dipotong
* **Tidak ada streaming:** Hasil dikembalikan setelah selesai

## Menggabungkan dengan alat lain

Alat bash paling kuat ketika digabungkan dengan [text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool) dan alat lainnya.

<Note>
  Jika Anda juga menggunakan [alat code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool), Claude memiliki akses ke dua lingkungan eksekusi terpisah: sesi bash lokal Anda dan container sandbox milik Anthropic. State tidak dibagikan di antara keduanya. Lihat [Menggunakan code execution dengan alat eksekusi lainnya](/docs/id/agents-and-tools/tool-use/code-execution-tool#using-code-execution-with-other-execution-tools) untuk panduan dalam memberikan prompt kepada Claude agar dapat membedakan antara lingkungan tersebut.
</Note>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ikhtisar penggunaan alat" icon="tool" href="/docs/id/agents-and-tools/tool-use/overview">
    Pelajari tentang penggunaan alat dengan Claude
  </Card>

  <Card title="Alat text editor" icon="file" href="/docs/id/agents-and-tools/tool-use/text-editor-tool">
    Lihat dan edit file teks dengan Claude
  </Card>
</CardGroup>
