---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 52b31113af0cb39ae9f84179d40276920a9368b1ce74e49787dd21a9539e9cab
---

# Bash tool

Biarkan Claude meminta perintah shell yang dijalankan aplikasi Anda dalam sesi bash persisten dan dikembalikan sebagai hasil alat.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Bash tool adalah [alat klien](/docs/id/agents-and-tools/tool-use/how-tool-use-works): Claude tidak menjalankan perintah sendiri. Ketika Anda menyertakan alat ini dalam sebuah permintaan, Claude membalas dengan blok `tool_use` yang menyebutkan perintah yang harus dijalankan. Aplikasi Anda menjalankan perintah tersebut dalam sesi bash yang dimilikinya dan mengembalikan output dalam blok `tool_result`.

Aplikasi Anda menjaga satu proses bash tetap hidup di seluruh panggilan alat, sehingga state tetap bertahan di antara perintah. Direktori kerja, variabel lingkungan, dan file apa pun yang dibuat oleh sebuah perintah masih ada untuk perintah berikutnya.

Versi alat saat ini adalah `bash_20250124`. Untuk dukungan model, header beta, dan versi sebelumnya, lihat [Versi alat](#tool-versions). Untuk semua alat yang disediakan Anthropic, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Kasus penggunaan

* **Alur kerja pengembangan:** Menjalankan perintah build, pengujian, dan alat pengembangan
* **Otomatisasi sistem:** Mengeksekusi skrip, mengelola file, mengotomatiskan tugas
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

Claude merespons dengan `stop_reason: "tool_use"` dan blok `tool_use` yang berisi perintah untuk dijalankan oleh aplikasi Anda:

```json Output
{
  "id": "msg_01XAbCDeFgHiJkLmNoPQrStU",
  "model": "claude-opus-4-8",
  "stop_reason": "tool_use",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll list all Python files in the current directory for you."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "bash",
      "input": {
        "command": "ls *.py"
      }
    }
  ]
}
```

Jalankan `input.command` dalam sesi bash Anda dan kirim kembali output-nya sebagai `tool_result`. Lihat [Mengimplementasikan bash tool](#implement-the-bash-tool) untuk siklus bolak-baliknya.

## Cara kerjanya

Setiap panggilan alat adalah satu perjalanan bolak-balik antara Claude dan aplikasi Anda:

1. Claude mengembalikan blok `tool_use` yang berisi `command` yang harus dijalankan.
2. Aplikasi Anda menjalankan perintah tersebut dalam sesi bash-nya.
3. Aplikasi Anda mengembalikan output perintah, stdout dan stderr bersama-sama, ke Claude dalam blok `tool_result`.
4. Claude meminta perintah lain dalam sesi yang sama atau merespons dengan teks.

Claude juga dapat mengembalikan beberapa blok `tool_use` dalam satu respons. Jalankan secara berurutan dalam sesi yang sama dan kembalikan semua hasilnya dalam satu pesan `user`. Lihat [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use).

API bersifat stateless. Tidak ada apa pun tentang sesi shell Anda yang berpindah antar permintaan, sehingga aplikasi Anda yang memutuskan kapan sesi dimulai, berapa lama sesi hidup, dan kapan harus memulai ulang. Untuk siklus permintaan dan respons lengkap, lihat [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

## Parameter

Definisi bash tool memiliki dua field wajib, `type` dan `name`, dan `name` harus berupa `bash`. Alat ini tanpa skema: Anda tidak menyediakan `input_schema`, karena skemanya sudah tertanam dalam model Claude dan tidak dapat dimodifikasi. Tabel berikut mencantumkan field input yang ditetapkan Claude saat memanggil alat.

| Parameter | Wajib | Deskripsi                                     |
| --------- | ----- | --------------------------------------------- |
| `command` | Ya\*  | Perintah bash yang akan dijalankan            |
| `restart` | Tidak | Setel ke `true` untuk memulai ulang sesi bash |

\*Wajib kecuali menggunakan `restart`

Untuk menangani `restart: true`, matikan proses shell, mulai yang baru, dan kembalikan `tool_result` yang mengonfirmasi pemulaian ulang. Sesi yang dimulai ulang dimulai dalam keadaan bersih: direktori kerja, variabel lingkungan, dan proses apa pun yang sedang berjalan akan hilang.

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

## Versi alat

`bash_20250124` adalah versi alat saat ini, dan tidak memerlukan header beta. Setiap model mulai dari Claude Sonnet 3.7 ([dipensiunkan](/docs/id/about-claude/model-deprecations)) dan seterusnya menerimanya, termasuk semua model Claude saat ini.

Versi asli `bash_20241022` adalah bagian dari beta computer use, dan rilis Claude Sonnet 3.5 Oktober 2024 ([dipensiunkan](/docs/id/about-claude/model-deprecations)) adalah satu-satunya model yang menerimanya. Permintaan yang menggunakannya memerlukan header `anthropic-beta: computer-use-2024-10-22`, dan SDK hanya mengeksposnya di namespace beta mereka. Integrasi baru sebaiknya menggunakan `bash_20250124`.

## Contoh: Otomatisasi multilangkah

Claude dapat merangkai perintah di seluruh panggilan alat untuk menyelesaikan tugas multilangkah:

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

## Mengimplementasikan bash tool

Claude menentukan perintah mana yang harus dijalankan. Aplikasi Anda memiliki segala hal lainnya: proses shell, timeout, dan pemeriksaan keamanan. Langkah-langkah berikut menunjukkan implementasi minimal.

<Steps>
  <Step title="Buat sesi bash persisten">
    Mulai satu proses bash yang berumur panjang dan jalankan setiap perintah di dalamnya. Karena pipe ke proses yang hidup tidak pernah melaporkan end-of-file, sesi mencetak baris sentinel unik setelah setiap perintah untuk menandai di mana output perintah tersebut berakhir:

    <CodeGroup exclude="shell">
      ```python Python
      import subprocess
      import uuid


      class BashSession:
          """A bash process that stays alive between commands so state persists."""

          def __init__(self):
              self.process = subprocess.Popen(
                  ["/bin/bash"],
                  stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.STDOUT,  # interleave errors with output, in order
                  start_new_session=True,  # own process group: a timeout can kill every child
                  text=True,
              )

          def execute_command(self, command):
              """Run a command in the session and return its output."""
              sentinel = f"__CLAUDE_BASH_DONE_{uuid.uuid4().hex}__"  # unique per call
              self.process.stdin.write(f"{command}\necho {sentinel}\n")
              self.process.stdin.flush()

              output = []
              for line in self.process.stdout:
                  if sentinel in line:  # this command's output is complete
                      break
                  output.append(line)
              return "".join(output)

          def restart(self):
              self.process.kill()
              self.process.wait()
              self.__init__()


      bash_session = BashSession()
      print(bash_session.execute_command("cd /tmp && pwd"))
      print(bash_session.execute_command("pwd"))  # still /tmp: the session kept its state
      ```

      ```typescript TypeScript
      import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";
      import { createInterface, type Interface } from "node:readline";
      import { randomUUID } from "node:crypto";

      // Proses bash yang tetap hidup di antara perintah sehingga state tetap tersimpan.
      class BashSession {
        process!: ChildProcessWithoutNullStreams;
        private lines!: Interface;

        constructor() {
          this.start();
        }

        private start(): void {
          this.process = spawn("/bin/bash", {
            detached: true // own process group: a timeout can kill every child
          });
          this.process.stdin.write("exec 2>&1\n"); // interleave errors with output, in order
          this.lines = createInterface({ input: this.process.stdout });
        }

        // Menjalankan perintah dalam sesi dan mengembalikan outputnya.
        executeCommand(command: string): Promise<string> {
          const sentinel = `__CLAUDE_BASH_DONE_${randomUUID()}__`; // unique per call
          const output: string[] = [];
          const result = new Promise<string>((resolve) => {
            const onLine = (line: string): void => {
              if (line.includes(sentinel)) {
                // output perintah ini sudah lengkap
                this.lines.off("line", onLine);
                resolve(output.join(""));
              } else {
                output.push(`${line}\n`);
              }
            };
            this.lines.on("line", onLine);
          });
          this.process.stdin.write(`${command}\necho ${sentinel}\n`);
          return result;
        }

        restart(): void {
          this.process.kill("SIGKILL");
          this.lines.close();
          this.start();
        }
      }

      const session = new BashSession();
      console.log(await session.executeCommand("cd /tmp && pwd"));
      console.log(await session.executeCommand("pwd")); // still /tmp: the session kept its state
      session.process.stdin.end(); // closing stdin ends the shell so the script can exit
      ```

      ```csharp C#
      using System.Diagnostics;
      using System.Text;

      var session = new BashSession();
      Console.Write(session.ExecuteCommand("cd /tmp && pwd"));
      Console.Write(session.ExecuteCommand("pwd")); // still /tmp: the session kept its state

      // Proses bash yang tetap hidup di antara perintah sehingga state tetap tersimpan.
      class BashSession
      {
          public Process Process { get; private set; }

          public BashSession()
          {
              Process = Start();
          }

          static Process Start()
          {
              var process = Process.Start(new ProcessStartInfo("/bin/bash")
              {
                  RedirectStandardInput = true,
                  RedirectStandardOutput = true
              })!;
              process.StandardInput.Write("exec 2>&1\n"); // interleave errors with output, in order
              process.StandardInput.Flush();
              return process;
          }

          // Menjalankan perintah dalam sesi dan mengembalikan output-nya.
          public string ExecuteCommand(string command)
          {
              var sentinel = $"__CLAUDE_BASH_DONE_{Guid.NewGuid():N}__"; // unique per call
              Process.StandardInput.Write($"{command}\necho {sentinel}\n");
              Process.StandardInput.Flush();

              var output = new StringBuilder();
              while (Process.StandardOutput.ReadLine() is string line)
              {
                  if (line.Contains(sentinel)) // this command's output is complete
                  {
                      break;
                  }
                  output.Append(line).Append('\n');
              }
              return output.ToString();
          }

          public void Restart()
          {
              Process.Kill(entireProcessTree: true);
              Process.WaitForExit();
              Process = Start();
          }
      }
      ```

      ```go Go
      import (
      	"bufio"
      	"crypto/rand"
      	"encoding/hex"
      	"fmt"
      	"io"
      	"log"
      	"os/exec"
      	"strings"
      	"syscall"
      )

      // BashSession adalah proses bash yang tetap hidup di antara perintah sehingga state tetap tersimpan.
      type BashSession struct {
      	cmd    *exec.Cmd
      	stdin  io.WriteCloser
      	output *bufio.Reader
      }

      func NewBashSession() (*BashSession, error) {
      	cmd := exec.Command("/bin/bash")
      	cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true} // own process group: a timeout can kill every child
      	stdin, err := cmd.StdinPipe()
      	if err != nil {
      		return nil, err
      	}
      	stdout, err := cmd.StdoutPipe()
      	if err != nil {
      		return nil, err
      	}
      	cmd.Stderr = cmd.Stdout // interleave errors with output, in order
      	if err := cmd.Start(); err != nil {
      		return nil, err
      	}
      	return &BashSession{cmd: cmd, stdin: stdin, output: bufio.NewReader(stdout)}, nil
      }

      // ExecuteCommand menjalankan perintah dalam sesi dan mengembalikan keluarannya.
      func (s *BashSession) ExecuteCommand(command string) string {
      	buf := make([]byte, 16)
      	rand.Read(buf)
      	sentinel := fmt.Sprintf("__CLAUDE_BASH_DONE_%s__", hex.EncodeToString(buf)) // unique per call
      	fmt.Fprintf(s.stdin, "%s\necho %s\n", command, sentinel)

      	var output strings.Builder
      	for {
      		line, err := s.output.ReadString('\n')
      		if err != nil || strings.Contains(line, sentinel) { // this command's output is complete
      			break
      		}
      		output.WriteString(line)
      	}
      	return output.String()
      }

      // Restart mematikan shell dan memulai sesi baru sebagai gantinya.
      func (s *BashSession) Restart() error {
      	s.cmd.Process.Kill()
      	s.cmd.Wait()
      	fresh, err := NewBashSession()
      	if err != nil {
      		return err
      	}
      	*s = *fresh
      	return nil
      }

      func main() {
      	session, err := NewBashSession()
      	if err != nil {
      		log.Fatal(err)
      	}
      	fmt.Print(session.ExecuteCommand("cd /tmp && pwd"))
      	fmt.Print(session.ExecuteCommand("pwd")) // still /tmp: the session kept its state
      }
      ```

      ```java Java
      import java.io.BufferedReader;
      import java.io.BufferedWriter;
      import java.io.IOException;
      import java.io.InputStreamReader;
      import java.io.OutputStreamWriter;
      import java.util.UUID;

      // Proses bash yang tetap hidup di antara perintah sehingga state tetap tersimpan.
      class BashSession {
          Process process;
          BufferedWriter stdin;
          BufferedReader output;

          BashSession() throws IOException {
              start();
          }

          void start() throws IOException {
              ProcessBuilder builder = new ProcessBuilder("/bin/bash");
              builder.redirectErrorStream(true); // interleave errors with output, in order
              process = builder.start();
              stdin = new BufferedWriter(new OutputStreamWriter(process.getOutputStream()));
              output = new BufferedReader(new InputStreamReader(process.getInputStream()));
          }

          // Menjalankan perintah dalam sesi dan mengembalikan outputnya.
          String executeCommand(String command) throws IOException {
              String sentinel = "__CLAUDE_BASH_DONE_" + UUID.randomUUID() + "__"; // unique per call
              stdin.write(command + "\necho " + sentinel + "\n");
              stdin.flush();

              StringBuilder result = new StringBuilder();
              String line;
              while ((line = output.readLine()) != null) {
                  if (line.contains(sentinel)) { // this command's output is complete
                      break;
                  }
                  result.append(line).append("\n");
              }
              return result.toString();
          }

          void restart() throws IOException, InterruptedException {
              process.destroyForcibly();
              process.waitFor();
              start();
          }
      }

      void main() throws Exception {
          BashSession session = new BashSession();
          IO.println(session.executeCommand("cd /tmp && pwd"));
          IO.println(session.executeCommand("pwd")); // still /tmp: the session kept its state
      }
      ```

      ```php PHP
      // Proses bash yang tetap hidup di antara perintah sehingga state tetap tersimpan.
      class BashSession
      {
          public $process;
          public $stdin;
          public $output;

          public function __construct()
          {
              $this->start();
          }

          private function start(): void
          {
              // setsid memberi shell process group sendiri: timeout dapat mematikan semua child
              $this->process = proc_open(
                  ['setsid', '/bin/bash'],
                  [0 => ['pipe', 'r'], 1 => ['pipe', 'w'], 2 => ['redirect', 1]], // interleave errors with output
                  $pipes
              );
              $this->stdin = $pipes[0];
              $this->output = $pipes[1];
          }

          // Jalankan perintah dalam sesi dan kembalikan output-nya.
          public function executeCommand(string $command): string
          {
              $sentinel = '__CLAUDE_BASH_DONE_' . bin2hex(random_bytes(16)) . '__'; // unique per call
              fwrite($this->stdin, "{$command}\necho {$sentinel}\n");
              fflush($this->stdin);

              $output = '';
              while (($line = fgets($this->output)) !== false) {
                  if (str_contains($line, $sentinel)) { // this command's output is complete
                      break;
                  }
                  $output .= $line;
              }
              return $output;
          }

          public function restart(): void
          {
              proc_terminate($this->process, 9);
              proc_close($this->process);
              $this->start();
          }
      }

      $session = new BashSession();
      echo $session->executeCommand("cd /tmp && pwd");
      echo $session->executeCommand("pwd"); // still /tmp: the session kept its state
      ```

      ```ruby Ruby
      require "open3"
      require "securerandom"

      # Proses bash yang tetap hidup di antara perintah sehingga state tetap tersimpan.
      class BashSession
        attr_reader :output, :wait_thread

        def initialize
          start
        end

        # Menjalankan perintah dalam sesi dan mengembalikan output-nya.
        def execute_command(command)
          sentinel = "__CLAUDE_BASH_DONE_#{SecureRandom.hex(16)}__" # unique per call
          @stdin.write("#{command}\necho #{sentinel}\n")
          @stdin.flush

          output = +""
          @output.each_line do |line|
            break if line.include?(sentinel) # this command's output is complete

            output << line
          end
          output
        end

        def restart
          Process.kill("KILL", @wait_thread.pid)
          @wait_thread.join
          start
        end

        private

        def start
          # popen2e menggabungkan error dengan output secara berurutan; pgroup memberi shell
          # process group sendiri sehingga timeout dapat mematikan semua proses anak
          @stdin, @output, @wait_thread = Open3.popen2e("/bin/bash", pgroup: true)
        end
      end

      session = BashSession.new
      puts session.execute_command("cd /tmp && pwd")
      puts session.execute_command("pwd") # still /tmp: the session kept its state
      ```
    </CodeGroup>

    Sesi menyisipkan stderr dengan stdout, sehingga pesan kesalahan muncul di tempat terjadinya. Contoh ini tidak menyertakan apa yang juga dibutuhkan oleh implementasi lengkap: timeout yang mematikan shell dan setiap proses yang dimulainya ketika sebuah perintah macet, lalu memulai ulang sesi. Praktik terbaik [Gunakan timeout perintah](#follow-implementation-best-practices) menunjukkan salah satu cara untuk menambahkannya.
  </Step>

  <Step title="Proses panggilan alat Claude">
    Ekstrak dan jalankan perintah dari respons Claude:

    <CodeGroup exclude="shell">
      ```python Python
      tool_results = []
      for content in response.content:
          if content.type == "tool_use" and content.name == "bash":
              if content.input.get("restart"):
                  bash_session.restart()
                  result = "Bash session restarted"
              else:
                  command = content.input.get("command")
                  result = bash_session.execute_command(command)

              # Satu tool_result per blok tool_use, semuanya dikembalikan dalam pesan pengguna berikutnya
              tool_results.append(
                  {"type": "tool_result", "tool_use_id": content.id, "content": result}
              )
      ```

      ```typescript TypeScript
      const toolResults: { type: string; tool_use_id: string; content: string }[] = [];
      for (const block of response.content) {
        if (block.type === "tool_use" && block.name === "bash") {
          let result: string;
          if (block.input.restart) {
            bashSession.restart();
            result = "Bash session restarted";
          } else {
            result = await bashSession.executeCommand(block.input.command ?? "");
          }

          // Satu tool_result per blok tool_use, semuanya dikembalikan dalam pesan pengguna berikutnya
          toolResults.push({ type: "tool_result", tool_use_id: block.id, content: result });
        }
      }
      ```

      ```csharp C#
      var toolResults = new List<ToolResultBlockParam>();
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse) && toolUse.Name == "bash")
          {
              string result;
              if (toolUse.Input.TryGetValue("restart", out var restart) && restart.GetBoolean())
              {
                  bashSession.Restart();
                  result = "Bash session restarted";
              }
              else
              {
                  var command = toolUse.Input["command"].GetString() ?? "";
                  result = bashSession.ExecuteCommand(command);
              }

              // Satu tool_result per blok tool_use, semuanya dikembalikan dalam pesan pengguna berikutnya
              toolResults.Add(new ToolResultBlockParam { ToolUseID = toolUse.ID, Content = result });
          }
      }
      ```

      ```go Go
      var toolResults []anthropic.ContentBlockParamUnion
      for _, block := range response.Content {
      	if block.Type == "tool_use" && block.Name == "bash" {
      		var input struct {
      			Command string `json:"command"`
      			Restart bool   `json:"restart"`
      		}
      		if err := json.Unmarshal(block.Input, &input); err != nil {
      			log.Fatal(err)
      		}

      		var result string
      		if input.Restart {
      			bashSession.Restart()
      			result = "Bash session restarted"
      		} else {
      			result = bashSession.ExecuteCommand(input.Command)
      		}

      		// Satu tool_result per blok tool_use, semuanya dikembalikan dalam pesan pengguna berikutnya
      		toolResults = append(toolResults, anthropic.NewToolResultBlock(block.ID, result, false))
      	}
      }
      ```

      ```java Java
      List<Map<String, Object>> toolResults = new ArrayList<>();
      for (ContentBlock block : response.content()) {
          if (block.type().equals("tool_use") && block.name().equals("bash")) {
              String result;
              if (Boolean.TRUE.equals(block.input().get("restart"))) {
                  bashSession.restart();
                  result = "Bash session restarted";
              } else {
                  String command = (String) block.input().get("command");
                  result = bashSession.executeCommand(command);
              }

              // Satu tool_result per blok tool_use, semuanya dikembalikan dalam pesan user berikutnya
              toolResults.add(Map.of("type", "tool_result", "tool_use_id", block.id(), "content", result));
          }
      }
      ```

      ```php PHP
      $toolResults = [];
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use' && $block->name === 'bash') {
              if (!empty($block->input['restart'])) {
                  $bashSession->restart();
                  $result = 'Bash session restarted';
              } else {
                  $result = $bashSession->executeCommand($block->input['command']);
              }

              // Satu tool_result per blok tool_use, semuanya dikembalikan dalam pesan pengguna berikutnya
              $toolResults[] = ['type' => 'tool_result', 'tool_use_id' => $block->id, 'content' => $result];
          }
      }
      ```

      ```ruby Ruby
      tool_results = []
      response.content.each do |block|
        next unless block.type == "tool_use" && block.name == "bash"

        result =
          if block.input["restart"]
            bash_session.restart
            "Bash session restarted"
          else
            bash_session.execute_command(block.input["command"])
          end

        # Satu tool_result per blok tool_use, semuanya dikembalikan dalam pesan pengguna berikutnya
        tool_results << {type: "tool_result", tool_use_id: block.id, content: result}
      end
      ```
    </CodeGroup>
  </Step>

  <Step title="Kembalikan hasilnya ke Claude">
    Kirim kembali `tool_result` dalam pesan `user` yang melanjutkan percakapan yang sama. Claude meminta perintah lain dalam sesi yang sama atau menyelesaikan jawabannya:

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
            },
            {
              "role": "assistant",
              "content": [
                {
                  "type": "tool_use",
                  "id": "toolu_01A09q90qw90lq917835lq9",
                  "name": "bash",
                  "input": {
                    "command": "ls *.py"
                  }
                }
              ]
            },
            {
              "role": "user",
              "content": [
                {
                  "type": "tool_result",
                  "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
                  "content": "analysis.py\nprocess_data.py\n"
                }
              ]
            }
          ]
        }'
      ```

      ```bash CLI
      ant messages create <<'YAML'
      model: claude-opus-4-8
      max_tokens: 1024
      tools:
        - type: bash_20250124
          name: bash
      messages:
        - role: user
          content: List all Python files in the current directory.
        - role: assistant
          content:
            - type: tool_use
              id: toolu_01A09q90qw90lq917835lq9
              name: bash
              input:
                command: ls *.py
        - role: user
          content:
            - type: tool_result
              tool_use_id: toolu_01A09q90qw90lq917835lq9
              content: |
                analysis.py
                process_data.py
      YAML
      ```

      ```python Python
      client = anthropic.Anthropic()

      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          tools=[{"type": "bash_20250124", "name": "bash"}],
          messages=[
              {"role": "user", "content": "List all Python files in the current directory."},
              {
                  "role": "assistant",
                  "content": [
                      {
                          "type": "tool_use",
                          "id": "toolu_01A09q90qw90lq917835lq9",
                          "name": "bash",
                          "input": {"command": "ls *.py"},
                      }
                  ],
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "tool_result",
                          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
                          "content": "analysis.py\nprocess_data.py\n",
                      }
                  ],
              },
          ],
      )

      print(response.content)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        tools: [{ type: "bash_20250124", name: "bash" }],
        messages: [
          {
            role: "user",
            content: "List all Python files in the current directory."
          },
          {
            role: "assistant",
            content: [
              {
                type: "tool_use",
                id: "toolu_01A09q90qw90lq917835lq9",
                name: "bash",
                input: { command: "ls *.py" }
              }
            ]
          },
          {
            role: "user",
            content: [
              {
                type: "tool_result",
                tool_use_id: "toolu_01A09q90qw90lq917835lq9",
                content: "analysis.py\nprocess_data.py\n"
              }
            ]
          }
        ]
      });

      console.log(response.content);
      ```

      ```csharp C#
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
                  new()
                  {
                      Role = Role.Assistant,
                      Content = new MessageParamContent(new List<ContentBlockParam>
                      {
                          new ContentBlockParam(new ToolUseBlockParam()
                          {
                              ID = "toolu_01A09q90qw90lq917835lq9",
                              Name = "bash",
                              Input = new Dictionary<string, JsonElement>
                              {
                                  ["command"] = JsonSerializer.SerializeToElement("ls *.py"),
                              },
                          }),
                      }),
                  },
                  new()
                  {
                      Role = Role.User,
                      Content = new MessageParamContent(new List<ContentBlockParam>
                      {
                          new ContentBlockParam(new ToolResultBlockParam()
                          {
                              ToolUseID = "toolu_01A09q90qw90lq917835lq9",
                              Content = "analysis.py\nprocess_data.py\n",
                          }),
                      }),
                  },
              ],
          }
      );

      Console.WriteLine(response);
      ```

      ```go Go
      client := anthropic.NewClient()

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 1024,
      	Tools: []anthropic.ToolUnionParam{
      		{OfBashTool20250124: &anthropic.ToolBash20250124Param{}},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("List all Python files in the current directory.")),
      		anthropic.NewAssistantMessage(
      			anthropic.NewToolUseBlock(
      				"toolu_01A09q90qw90lq917835lq9",
      				map[string]any{"command": "ls *.py"},
      				"bash",
      			),
      		),
      		anthropic.NewUserMessage(
      			anthropic.NewToolResultBlock(
      				"toolu_01A09q90qw90lq917835lq9",
      				"analysis.py\nprocess_data.py\n",
      				false,
      			),
      		),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Println(response.Content)
      ```

      ```java Java
      import com.anthropic.core.JsonValue;
      import com.anthropic.models.messages.ContentBlockParam;
      // ...
      import com.anthropic.models.messages.ToolBash20250124;
      import com.anthropic.models.messages.ToolResultBlockParam;
      import com.anthropic.models.messages.ToolUseBlockParam;
      // ...
      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024)
              .addTool(ToolBash20250124.builder().build())
              .addUserMessage("List all Python files in the current directory.")
              .addAssistantMessageOfBlockParams(
                  List.of(
                      ContentBlockParam.ofToolUse(
                          ToolUseBlockParam.builder()
                              .id("toolu_01A09q90qw90lq917835lq9")
                              .name("bash")
                              .input(
                                  ToolUseBlockParam.Input.builder()
                                      .putAdditionalProperty("command", JsonValue.from("ls *.py"))
                                      .build()
                              )
                              .build()
                      )
                  )
              )
              .addUserMessageOfBlockParams(
                  List.of(
                      ContentBlockParam.ofToolResult(
                          ToolResultBlockParam.builder()
                              .toolUseId("toolu_01A09q90qw90lq917835lq9")
                              .content("analysis.py\nprocess_data.py\n")
                              .build()
                      )
                  )
              )
              .build();

          Message response = client.messages().create(params);
          IO.println(response.content());
      }
      ```

      ```php PHP
      use Anthropic\Messages\ToolBash20250124;

      $client = new Client();

      $response = $client->messages->create(
          model: 'claude-opus-4-8',
          maxTokens: 1024,
          tools: [new ToolBash20250124()],
          messages: [
              ['role' => 'user', 'content' => 'List all Python files in the current directory.'],
              [
                  'role' => 'assistant',
                  'content' => [
                      [
                          'type' => 'tool_use',
                          'id' => 'toolu_01A09q90qw90lq917835lq9',
                          'name' => 'bash',
                          'input' => ['command' => 'ls *.py'],
                      ],
                  ],
              ],
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'tool_result',
                          'tool_use_id' => 'toolu_01A09q90qw90lq917835lq9',
                          'content' => "analysis.py\nprocess_data.py\n",
                      ],
                  ],
              ],
          ],
      );

      print_r($response->content);
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      response = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        tools: [{type: "bash_20250124", name: "bash"}],
        messages: [
          {role: "user", content: "List all Python files in the current directory."},
          {
            role: "assistant",
            content: [
              {
                type: "tool_use",
                id: "toolu_01A09q90qw90lq917835lq9",
                name: "bash",
                input: {command: "ls *.py"}
              }
            ]
          },
          {
            role: "user",
            content: [
              {
                type: "tool_result",
                tool_use_id: "toolu_01A09q90qw90lq917835lq9",
                content: "analysis.py\nprocess_data.py\n"
              }
            ]
          }
        ]
      )

      puts response.content
      ```
    </CodeGroup>

    Ulangi siklus jalankan-dan-kembalikan selama `stop_reason` adalah `tool_use`. Untuk loop lengkapnya, lihat [Menangani hasil dari alat klien](/docs/id/agents-and-tools/tool-use/handle-tool-calls#handling-results-from-client-tools).
  </Step>

  <Step title="Implementasikan langkah-langkah keamanan">
    Tambahkan validasi dan pembatasan. Gunakan allowlist alih-alih blocklist: blocklist melewatkan perintah apa pun yang tidak diantisipasinya. Contoh ini juga menolak operator shell yang muncul sebagai kata terpisah:

    <CodeGroup exclude="shell">
      ```python Python
      import shlex

      ALLOWED_COMMANDS = {"ls", "cat", "echo", "pwd", "grep", "find", "wc", "head", "tail"}
      SHELL_OPERATORS = {"&&", "||", "|", ";", "&", ">", "<", ">>"}


      def validate_command(command):
          # Hanya izinkan perintah dari allowlist eksplisit
          try:
              tokens = shlex.split(command)
          except ValueError:
              return False, "Could not parse command"

          if not tokens:
              return False, "Empty command"

          executable = tokens[0]
          if executable not in ALLOWED_COMMANDS:
              return False, f"Command '{executable}' is not in the allowlist"

          # Tolak operator shell yang ditulis sebagai kata terpisah
          for token in tokens[1:]:
              if token in SHELL_OPERATORS or token.startswith(("$", "`")):
                  return False, f"Shell operator '{token}' is not allowed"

          return True, None
      ```

      ```typescript TypeScript
      const ALLOWED_COMMANDS = new Set([
        "ls",
        "cat",
        "echo",
        "pwd",
        "grep",
        "find",
        "wc",
        "head",
        "tail"
      ]);
      const SHELL_OPERATORS = new Set(["&&", "||", "|", ";", "&", ">", "<", ">>"]);

      function validateCommand(command: string): { ok: boolean; reason?: string } {
        // Pisahkan berdasarkan spasi: cukup untuk pemeriksaan tripwire
        const tokens = command.split(/\s+/).filter((token) => token.length > 0);
        if (tokens.length === 0) {
          return { ok: false, reason: "Empty command" };
        }

        // Hanya izinkan perintah dari allowlist eksplisit
        const executable = tokens[0];
        if (!ALLOWED_COMMANDS.has(executable)) {
          return { ok: false, reason: `Command '${executable}' is not in the allowlist` };
        }

        // Tolak operator shell yang ditulis sebagai kata terpisah
        for (const token of tokens.slice(1)) {
          const bare = token.replace(/^["']+/, ""); // a quoted token can still smuggle an expansion
          if (SHELL_OPERATORS.has(token) || bare.startsWith("$") || bare.startsWith("`")) {
            return { ok: false, reason: `Shell operator '${token}' is not allowed` };
          }
        }

        return { ok: true };
      }
      ```

      ```csharp C#
      var allowedCommands = new HashSet<string>
      {
          "ls", "cat", "echo", "pwd", "grep", "find", "wc", "head", "tail"
      };
      var shellOperators = new HashSet<string> { "&&", "||", "|", ";", "&", ">", "<", ">>" };

      (bool Ok, string? Reason) ValidateCommand(string command)
      {
          // Pisahkan berdasarkan spasi: cukup untuk pemeriksaan tripwire
          var tokens = command.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries);
          if (tokens.Length == 0)
          {
              return (false, "Empty command");
          }

          // Hanya izinkan perintah dari allowlist eksplisit
          var executable = tokens[0];
          if (!allowedCommands.Contains(executable))
          {
              return (false, $"Command '{executable}' is not in the allowlist");
          }

          // Tolak operator shell yang ditulis sebagai kata terpisah
          foreach (var token in tokens.Skip(1))
          {
              var bare = token.TrimStart('"', '\''); // a quoted token can still smuggle an expansion
              if (shellOperators.Contains(token) || bare.StartsWith('$') || bare.StartsWith('`'))
              {
                  return (false, $"Shell operator '{token}' is not allowed");
              }
          }

          return (true, null);
      }
      ```

      ```go Go
      var allowedCommands = map[string]bool{
      	"ls": true, "cat": true, "echo": true, "pwd": true, "grep": true,
      	"find": true, "wc": true, "head": true, "tail": true,
      }

      var shellOperators = map[string]bool{
      	"&&": true, "||": true, "|": true, ";": true, "&": true,
      	">": true, "<": true, ">>": true,
      }

      func validateCommand(command string) (bool, string) {
      	// Pisahkan berdasarkan spasi: cukup untuk pemeriksaan tripwire
      	tokens := strings.Fields(command)
      	if len(tokens) == 0 {
      		return false, "Empty command"
      	}

      	// Hanya izinkan perintah dari allowlist eksplisit
      	executable := tokens[0]
      	if !allowedCommands[executable] {
      		return false, fmt.Sprintf("Command %q is not in the allowlist", executable)
      	}

      	// Tolak operator shell yang ditulis sebagai kata terpisah
      	for _, token := range tokens[1:] {
      		bare := strings.TrimLeft(token, `"'`) // a quoted token can still smuggle an expansion
      		if shellOperators[token] || strings.HasPrefix(bare, "$") || strings.HasPrefix(bare, "`") {
      			return false, fmt.Sprintf("Shell operator %q is not allowed", token)
      		}
      	}

      	return true, ""
      }
      ```

      ```java Java
      import java.util.List;
      import java.util.Set;

      static final Set<String> ALLOWED_COMMANDS =
          Set.of("ls", "cat", "echo", "pwd", "grep", "find", "wc", "head", "tail");
      static final Set<String> SHELL_OPERATORS = Set.of("&&", "||", "|", ";", "&", ">", "<", ">>");

      record Validation(boolean ok, String reason) {}

      Validation validateCommand(String command) {
          // Pisahkan berdasarkan spasi: cukup untuk pemeriksaan tripwire
          List<String> tokens = List.of(command.trim().split("\\s+"));
          if (tokens.size() == 1 && tokens.get(0).isEmpty()) {
              return new Validation(false, "Empty command");
          }

          // Hanya izinkan perintah dari allowlist eksplisit
          String executable = tokens.get(0);
          if (!ALLOWED_COMMANDS.contains(executable)) {
              return new Validation(false, "Command '" + executable + "' is not in the allowlist");
          }

          // Tolak operator shell yang ditulis sebagai kata terpisah
          for (String token : tokens.subList(1, tokens.size())) {
              String bare = token.replaceFirst("^[\"']+", ""); // a quoted token can still smuggle an expansion
              if (SHELL_OPERATORS.contains(token) || bare.startsWith("$") || bare.startsWith("`")) {
                  return new Validation(false, "Shell operator '" + token + "' is not allowed");
              }
          }

          return new Validation(true, null);
      }
      ```

      ```php PHP
      const ALLOWED_COMMANDS = ['ls', 'cat', 'echo', 'pwd', 'grep', 'find', 'wc', 'head', 'tail'];
      const SHELL_OPERATORS = ['&&', '||', '|', ';', '&', '>', '<', '>>'];

      function validateCommand(string $command): array
      {
          // Pisahkan berdasarkan spasi: cukup untuk pemeriksaan tripwire
          $tokens = preg_split('/\\s+/', trim($command), -1, PREG_SPLIT_NO_EMPTY);
          if ($tokens === false || $tokens === []) {
              return [false, 'Empty command'];
          }

          // Hanya izinkan perintah dari allowlist eksplisit
          $executable = $tokens[0];
          if (!in_array($executable, ALLOWED_COMMANDS, true)) {
              return [false, "Command '{$executable}' is not in the allowlist"];
          }

          // Tolak operator shell yang ditulis sebagai kata terpisah
          foreach (array_slice($tokens, 1) as $token) {
              $bare = ltrim($token, '"\''); // a quoted token can still smuggle an expansion
              if (in_array($token, SHELL_OPERATORS, true) || str_starts_with($bare, '$') || str_starts_with($bare, '`')) {
                  return [false, "Shell operator '{$token}' is not allowed"];
              }
          }

          return [true, null];
      }
      ```

      ```ruby Ruby
      require "shellwords"

      ALLOWED_COMMANDS = %w[ls cat echo pwd grep find wc head tail].freeze
      SHELL_OPERATORS = ["&&", "||", "|", ";", "&", ">", "<", ">>"].freeze

      def validate_command(command)
        # Hanya izinkan perintah dari allowlist eksplisit
        begin
          tokens = Shellwords.split(command)
        rescue ArgumentError
          return [false, "Could not parse command"]
        end

        return [false, "Empty command"] if tokens.empty?

        executable = tokens[0]
        unless ALLOWED_COMMANDS.include?(executable)
          return [false, "Command '#{executable}' is not in the allowlist"]
        end

        # Tolak operator shell yang ditulis sebagai kata terpisah
        tokens[1..].each do |token|
          if SHELL_OPERATORS.include?(token) || token.start_with?("$", "`")
            return [false, "Shell operator '#{token}' is not allowed"]
          end
        end

        [true, nil]
      end
      ```
    </CodeGroup>

    Pemeriksaan ini adalah tripwire untuk kesalahan yang jelas, bukan batas penegakan. Pemeriksaan ini menolak perangkaian dengan spasi (`&&`), pipe, dan pengalihan yang digunakan oleh contoh-contoh lain di halaman ini. Pemeriksaan ini tidak menangkap operator yang menempel pada sebuah kata, seperti `cat data.txt|grep x`, karena tokenizer menyimpan `data.txt|grep` dalam satu token. Tentukan perintah dan operator mana yang diizinkan oleh aplikasi Anda. Kontrol yang sebenarnya adalah isolasi: jalankan seluruh sesi di dalam container atau mesin virtual (lihat [Keamanan](#security)).
  </Step>
</Steps>

### Menangani kesalahan

Ketika sebuah perintah gagal atau sesi rusak, beri tahu Claude apa yang terjadi. Kembalikan pesan sebagai konten `tool_result` dan setel `is_error` ke `true`, yang menandai panggilan alat sebagai gagal. Lihat [Menangani kesalahan dengan is\_error](/docs/id/agents-and-tools/tool-use/handle-tool-calls#handling-errors-with-is-error).

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
          "content": "Error: command did not finish within 30 seconds",
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
    Perintah yang tidak pernah selesai, seperti perintah yang menunggu input, memblokir sesi selamanya karena baris sentinelnya tidak pernah tiba. Beri setiap perintah tenggat waktu. Ketika tenggat waktu terlewati, hentikan shell dan semua yang dimulai oleh perintah tersebut, lalu mulai ulang sesi:

    <CodeGroup exclude="shell">
      ```python Python
      import concurrent.futures
      import os
      import signal


      def execute_with_timeout(session, command, timeout=30):
          """Run a command in the session, replacing the session if the command hangs."""
          with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
              future = pool.submit(session.execute_command, command)
              try:
                  return future.result(timeout=timeout)
              except concurrent.futures.TimeoutError:
                  # Grup tersebut adalah shell dan setiap proses yang dimulai oleh perintah
                  os.killpg(session.process.pid, signal.SIGKILL)
                  session.restart()
                  return f"Error: command did not finish within {timeout} seconds"
      ```

      ```typescript TypeScript
      // Menjalankan perintah dalam sesi, mengganti sesi jika perintah tersebut macet.
      async function executeWithTimeout(
        session: BashSession,
        command: string,
        timeoutMs = 30000
      ): Promise<string> {
        let timer: NodeJS.Timeout | undefined;
        const timedOut = new Promise<never>((_, reject) => {
          timer = setTimeout(() => reject(new Error("timeout")), timeoutMs);
        });
        try {
          return await Promise.race([session.executeCommand(command), timedOut]);
        } catch {
          // Grup ini adalah shell dan setiap proses yang dimulai oleh perintah tersebut
          if (session.process.pid !== undefined) {
            process.kill(-session.process.pid, "SIGKILL");
          }
          session.restart();
          return `Error: command did not finish within ${timeoutMs / 1000} seconds`;
        } finally {
          clearTimeout(timer);
        }
      }
      ```

      ```csharp C#
      using System.Diagnostics;

      // Menjalankan perintah dalam sesi, mengganti sesi jika perintah macet.
      static string ExecuteWithTimeout(BashSession session, string command, int timeoutSeconds = 30)
      {
          var work = Task.Run(() => session.ExecuteCommand(command));
          if (work.Wait(TimeSpan.FromSeconds(timeoutSeconds)))
          {
              return work.Result;
          }

          // Menghentikan shell dan semua proses yang dimulainya, lalu memulai sesi baru
          session.Process.Kill(entireProcessTree: true);
          session.Restart();
          return $"Error: command did not finish within {timeoutSeconds} seconds";
      }
      ```

      ```go Go
      // executeWithTimeout menjalankan sebuah perintah, dan mengganti sesi jika perintah tersebut macet.
      func executeWithTimeout(session *BashSession, command string, timeoutSeconds int) string {
      	done := make(chan string, 1)
      	go func() { done <- session.ExecuteCommand(command) }()

      	select {
      	case result := <-done:
      		return result
      	case <-time.After(time.Duration(timeoutSeconds) * time.Second):
      		// Grup ini terdiri dari shell dan setiap proses yang dimulai oleh perintah tersebut
      		syscall.Kill(-session.cmd.Process.Pid, syscall.SIGKILL)
      		session.Restart()
      		return fmt.Sprintf("Error: command did not finish within %d seconds", timeoutSeconds)
      	}
      }
      ```

      ```java Java
      // Jalankan perintah dalam sesi, dengan mengganti sesi jika perintah tersebut macet.
      String executeWithTimeout(BashSession session, String command, int timeoutSeconds) throws Exception {
          ExecutorService pool = Executors.newSingleThreadExecutor();
          try {
              Future<String> future = pool.submit(() -> session.executeCommand(command));
              return future.get(timeoutSeconds, TimeUnit.SECONDS);
          } catch (TimeoutException e) {
              // Hentikan shell dan semua proses yang dimulainya, lalu mulai sesi baru
              session.process.descendants().forEach(ProcessHandle::destroyForcibly);
              session.process.destroyForcibly();
              session.restart();
              return "Error: command did not finish within " + timeoutSeconds + " seconds";
          } finally {
              pool.shutdownNow();
          }
      }
      ```

      ```php PHP
      // Jalankan perintah tetapi menyerah jika tidak selesai dalam tenggat waktu. PHP memblokir pada
      // pembacaan pipe, jadi tenggat waktu berada di dalam loop baca: stream_select() menunggu
      // output yang dapat dibaca sebelum setiap fgets() sehingga loop dapat memeriksa tenggat waktu.
      function executeWithTimeout(BashSession $session, string $command, int $timeout = 30): string
      {
          $sentinel = '__CLAUDE_BASH_DONE_' . bin2hex(random_bytes(16)) . '__'; // unique per call
          fwrite($session->stdin, "{$command}\necho {$sentinel}\n");
          fflush($session->stdin);

          $deadline = microtime(true) + $timeout;
          $output = '';
          while (microtime(true) < $deadline) {
              $read = [$session->output];
              $write = null;
              $except = null;
              if (stream_select($read, $write, $except, 1) === 0) {
                  continue; // no output yet; check the deadline again
              }
              $line = fgets($session->output);
              if ($line === false || str_contains($line, $sentinel)) {
                  return $output; // this command's output is complete
              }
              $output .= $line;
          }

          // Grup tersebut adalah shell dan setiap proses yang dimulai oleh perintah itu
          posix_kill(-proc_get_status($session->process)['pid'], 9); // 9 = SIGKILL
          $session->restart();
          return "Error: command did not finish within {$timeout} seconds";
      }
      ```

      ```ruby Ruby
      require "timeout"

      # Jalankan perintah dalam sesi, ganti sesi jika perintah tersebut hang.
      def execute_with_timeout(session, command, timeout: 30)
        Timeout.timeout(timeout) { session.execute_command(command) }
      rescue Timeout::Error
        # Grup ini adalah shell dan semua proses yang dimulai oleh perintah tersebut
        Process.kill("KILL", -session.wait_thread.pid)
        session.restart
        "Error: command did not finish within #{timeout} seconds"
      end
      ```
    </CodeGroup>

    Kill menghentikan perintah yang macet dan semua yang dimulainya. Kembalikan pesan sebagai `tool_result` kesalahan (lihat [Menangani kesalahan](#handle-errors)), yang menandai panggilan alat sebagai gagal.
  </Accordion>

  <Accordion title="Pertahankan state sesi">
    Jaga sesi bash tetap persisten untuk mempertahankan variabel lingkungan dan direktori kerja:

    <CodeGroup exclude="shell">
      ```python Python
      # Perintah yang dijalankan dalam sesi yang sama mempertahankan state
      commands = [
          "cd /tmp",
          "echo 'Hello' > test.txt",
          "cat test.txt",  # The session is still in /tmp
      ]
      ```

      ```typescript TypeScript
      // Perintah yang dijalankan dalam sesi yang sama mempertahankan state
      const commands = [
        "cd /tmp",
        "echo 'Hello' > test.txt",
        "cat test.txt" // The session is still in /tmp
      ];
      ```

      ```csharp C#
      // Perintah yang dijalankan dalam sesi yang sama mempertahankan state
      string[] commands =
      [
          "cd /tmp",
          "echo 'Hello' > test.txt",
          "cat test.txt", // The session is still in /tmp
      ];
      ```

      ```go Go
      // Perintah yang dijalankan dalam sesi yang sama mempertahankan state
      commands := []string{
      	"cd /tmp",
      	"echo 'Hello' > test.txt",
      	"cat test.txt", // The session is still in /tmp
      }
      ```

      ```java Java
      // Perintah yang dijalankan dalam sesi yang sama mempertahankan state
      List<String> commands = List.of(
          "cd /tmp",
          "echo 'Hello' > test.txt",
          "cat test.txt" // The session is still in /tmp
      );
      ```

      ```php PHP
      // Perintah yang dijalankan dalam sesi yang sama mempertahankan state
      $commands = [
          'cd /tmp',
          "echo 'Hello' > test.txt",
          'cat test.txt', // The session is still in /tmp
      ];
      ```

      ```ruby Ruby
      # Perintah yang dijalankan dalam sesi yang sama mempertahankan state
      commands = [
        "cd /tmp",
        "echo 'Hello' > test.txt",
        "cat test.txt" # The session is still in /tmp
      ]
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Tangani output besar">
    Potong output besar untuk mencegah masalah batas token:

    <CodeGroup exclude="shell">
      ```python Python
      def truncate_output(output, max_lines=100):
          lines = output.split("\n")
          if len(lines) > max_lines:
              truncated = "\n".join(lines[:max_lines])
              return f"{truncated}\n\n... Output truncated ({len(lines)} total lines) ..."
          return output
      ```

      ```typescript TypeScript
      function truncateOutput(output: string, maxLines = 100): string {
        const lines = output.split("\n");
        if (lines.length > maxLines) {
          const truncated = lines.slice(0, maxLines).join("\n");
          return `${truncated}\n\n... Output truncated (${lines.length} total lines) ...`;
        }
        return output;
      }
      ```

      ```csharp C#
      string TruncateOutput(string output, int maxLines = 100)
      {
          var lines = output.Split('\n');
          if (lines.Length > maxLines)
          {
              var truncated = string.Join("\n", lines.Take(maxLines));
              return $"{truncated}\n\n... Output truncated ({lines.Length} total lines) ...";
          }
          return output;
      }
      ```

      ```go Go
      func truncateOutput(output string, maxLines int) string {
      	lines := strings.Split(output, "\n")
      	if len(lines) > maxLines {
      		truncated := strings.Join(lines[:maxLines], "\n")
      		return fmt.Sprintf("%s\n\n... Output truncated (%d total lines) ...", truncated, len(lines))
      	}
      	return output
      }
      ```

      ```java Java
      String truncateOutput(String output, int maxLines) {
          String[] lines = output.split("\n", -1);
          if (lines.length > maxLines) {
              String truncated = String.join("\n", Arrays.copyOf(lines, maxLines));
              return truncated + "\n\n... Output truncated (" + lines.length + " total lines) ...";
          }
          return output;
      }
      ```

      ```php PHP
      function truncateOutput(string $output, int $maxLines = 100): string
      {
          $lines = explode("\n", $output);
          if (count($lines) > $maxLines) {
              $truncated = implode("\n", array_slice($lines, 0, $maxLines));
              return "{$truncated}\n\n... Output truncated (" . count($lines) . ' total lines) ...';
          }
          return $output;
      }
      ```

      ```ruby Ruby
      def truncate_output(output, max_lines: 100)
        lines = output.split("\n", -1)
        return output unless lines.length > max_lines

        truncated = lines.first(max_lines).join("\n")
        "#{truncated}\n\n... Output truncated (#{lines.length} total lines) ..."
      end
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Catat semua perintah">
    Simpan jejak audit. Arahkan setiap perintah melalui satu wrapper yang mencatat perintah sebelum dijalankan dan output setelah selesai. Perintah yang macet atau merusak sesi tetap meninggalkan catatan:

    <CodeGroup exclude="shell">
      ```python Python
      import logging

      logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


      def execute_and_log(session, command):
          """Run a command in the session and keep an audit record of it."""
          logging.info("command=%r", command)
          output = session.execute_command(command)
          logging.info("output=%r", output[:200])  # first 200 characters
          return output
      ```

      ```typescript TypeScript
      // Jalankan perintah dalam sesi dan simpan catatan auditnya.
      async function executeAndLog(session: BashSession, command: string): Promise<string> {
        console.error(`command=${JSON.stringify(command)}`);
        const output = await session.executeCommand(command);
        console.error(`output=${JSON.stringify(output.slice(0, 200))}`); // first 200 characters
        return output;
      }
      ```

      ```csharp C#
      // Menjalankan perintah dalam sesi dan menyimpan catatan auditnya.
      static string ExecuteAndLog(BashSession session, string command)
      {
          Console.Error.WriteLine($"command={command}");
          var output = session.ExecuteCommand(command);
          Console.Error.WriteLine($"output={output[..Math.Min(output.Length, 200)]}"); // first 200 characters
          return output;
      }
      ```

      ```go Go
      // executeAndLog menjalankan perintah dalam sesi dan menyimpan catatan auditnya.
      func executeAndLog(session *BashSession, command string) string {
      	log.Printf("command=%q", command)
      	output := session.ExecuteCommand(command)
      	log.Printf("output=%q", output[:min(len(output), 200)]) // first 200 characters
      	return output
      }
      ```

      ```java Java
      static final Logger AUDIT = Logger.getLogger("bash-audit");

      // Jalankan perintah dalam sesi dan simpan catatan auditnya.
      String executeAndLog(BashSession session, String command) throws IOException {
          AUDIT.info("command=" + command);
          String output = session.executeCommand(command);
          AUDIT.info("output=" + output.substring(0, Math.min(output.length(), 200))); // first 200 characters
          return output;
      }
      ```

      ```php PHP
      // Jalankan perintah dalam sesi dan simpan catatan auditnya.
      function executeAndLog(BashSession $session, string $command): string
      {
          error_log("command={$command}");
          $output = $session->executeCommand($command);
          error_log('output=' . substr($output, 0, 200)); // first 200 characters
          return $output;
      }
      ```

      ```ruby Ruby
      require "logger"

      AUDIT = Logger.new($stderr)

      # Jalankan perintah dalam sesi dan simpan catatan auditnya.
      def execute_and_log(session, command)
        AUDIT.info("command=#{command.inspect}")
        output = session.execute_command(command)
        AUDIT.info("output=#{output[0, 200].inspect}") # first 200 characters
        output
      end
      ```
    </CodeGroup>

    Catatan secara default masuk ke `stderr`; arahkan ke file atau pipeline logging Anda untuk menyimpannya. Sertakan apa pun yang mengaitkan catatan dengan permintaan di aplikasi Anda, seperti pengguna akhir dan `tool_use_id`.
  </Accordion>
</AccordionGroup>

## Keamanan

<Warning>
  Aplikasi Anda menjalankan perintah apa pun yang diminta Claude. Jalankan sesi di lingkungan terisolasi, seperti container atau mesin virtual, sebagai pengguna dengan hak istimewa paling rendah yang dapat melakukan pekerjaan tersebut. Perlakukan setiap perintah sebagai input yang tidak tepercaya.
</Warning>

Di luar isolasi, tambahkan kontrol berikut:

* Validasi perintah sebelum menjalankannya, dengan allowlist alih-alih blocklist. Lihat [Mengimplementasikan bash tool](#implement-the-bash-tool).
* Tetapkan batas sumber daya pada proses shell (CPU, memori, dan disk), misalnya dengan `ulimit`.
* Catat setiap perintah dan output-nya sehingga Anda dapat mengaudit apa yang dijalankan.
* Redaksi kredensial dan rahasia lainnya dari output sebelum mengembalikannya ke Claude.

## Harga

Definisi alat bash menambahkan token input berikut ke permintaan Anda. Ini merupakan tambahan dari [prompt sistem penggunaan alat](/docs/id/agents-and-tools/tool-use/overview#pricing) per-model yang berlaku setiap kali ada alat apa pun yang digunakan.

| Model                                                    | Token input tambahan |
| -------------------------------------------------------- | -------------------- |
| Claude Opus 4.7 dan Claude Opus 4.8                      | 325 token            |
| Claude Opus 4.6, Claude Sonnet 4.6, dan versi sebelumnya | 244 token            |

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

Untuk panduan tentang penggunaan git sebagai mekanisme checkpoint-dan-pemulihan dalam alur kerja agen yang berjalan lama, lihat [praktik terbaik manajemen state](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#state-management-best-practices).

### Operasi file

* Memproses data: `wc -l *.csv && ls -lh *.csv`
* Mencari file: `find . -name "*.py" | xargs grep "pattern"`
* Membuat cadangan: `tar -czf backup.tar.gz ./data`

### Tugas sistem

* Memeriksa sumber daya: `df -h && free -m`
* Manajemen proses: `ps aux | grep python`
* Penyiapan lingkungan: `export PATH=$PATH:/new/path && echo $PATH`

## Keterbatasan

* **Tidak ada perintah interaktif:** Sesi tidak dapat menjalankan `vim`, `less`, prompt kata sandi, atau perintah apa pun yang menunggu input pada stdin.
* **Tidak ada aplikasi GUI:** Sesi hanya berbasis baris perintah.
* **Cakupan sesi:** State sesi bash berada di sisi klien. Aplikasi Anda bertanggung jawab untuk mempertahankan sesi shell di antara giliran.
* **Batas output:** API tidak memotong hasil alat (permintaan yang terlalu besar akan ditolak). Potong output besar di aplikasi Anda sebelum mengembalikannya ke Claude.
* **Tidak ada streaming:** Output mencapai Claude hanya ketika aplikasi Anda mengembalikan `tool_result` dalam permintaan berikutnya.

## Menggabungkan dengan alat lain

Bash tool cocok dipadukan dengan [Text editor tool](/docs/id/agents-and-tools/tool-use/text-editor-tool): Claude mengedit file dengan satu alat dan meminta perintah yang menjalankannya dengan alat lainnya.

<Note>
  Jika Anda juga menggunakan [Code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool), Claude memiliki akses ke dua lingkungan eksekusi terpisah: sesi bash lokal Anda dan container sandbox Anthropic. State tidak dibagikan di antara keduanya. Lihat [Menggunakan code execution dengan alat eksekusi lainnya](/docs/id/agents-and-tools/tool-use/code-execution-tool#using-code-execution-with-other-execution-tools) untuk panduan tentang memberi prompt kepada Claude agar membedakan antar lingkungan.
</Note>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Text editor tool" icon="file" href="/docs/id/agents-and-tools/tool-use/text-editor-tool">
    Lihat dan modifikasi file teks untuk men-debug, memperbaiki, dan meningkatkan kode.
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="tool" href="/docs/id/agents-and-tools/tool-use/overview">
    Hubungkan Claude ke alat dan API eksternal. Lihat di mana alat dieksekusi, kapan Claude memanggilnya, dan alat mana yang sesuai dengan tugas Anda.
  </Card>
</CardGroup>
