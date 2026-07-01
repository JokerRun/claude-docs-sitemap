---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: c69daca9689addbe1f46492dcf94e1e32cc1f3b65edfc05ee57e04493a9a80ae
---

# Alat memori

Biarkan Claude menyimpan dan mengambil informasi di seluruh percakapan dengan mengimplementasikan operasi file alat memori di aplikasi Anda.

---

Alat memori memungkinkan Claude menyimpan dan mengambil informasi di seluruh percakapan dalam sebuah direktori file memori. Claude dapat membuat, membaca, memperbarui, dan menghapus file yang tetap ada di antara sesi, sehingga membangun pengetahuan dari waktu ke waktu tanpa menyimpan semuanya di dalam "context window" (jendela konteks).

Memori mendukung pengambilan konteks secara "just-in-time" (tepat waktu). Alih-alih memuat semua informasi yang relevan di awal, agen mencatat apa yang dipelajarinya dalam file memori dan membacanya kembali sesuai kebutuhan. Ini menjaga konteks aktif tetap terfokus pada tugas saat ini, yang penting untuk sesi jangka panjang yang jika tidak demikian akan membebani jendela konteks. Lihat [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) untuk pola yang lebih luas.

Alat memori beroperasi di sisi klien: Claude meminta operasi file, dan aplikasi Anda yang mengeksekusinya. Anda mengontrol di mana dan bagaimana data disimpan melalui infrastruktur Anda sendiri.

<Note>
  Hubungi kami melalui [formulir umpan balik](https://forms.gle/YXC2EKGMhjN1c4L88) untuk membagikan masukan Anda tentang fitur ini.
</Note>

<Note>
  Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

## Kasus penggunaan

* Mempertahankan konteks proyek di beberapa sesi agen
* Menerapkan pelajaran dari interaksi, keputusan, dan umpan balik sebelumnya ke tugas baru
* Membangun basis pengetahuan dari waktu ke waktu

## Cara kerjanya

Ketika alat memori diaktifkan, Claude secara otomatis memeriksa direktori memorinya sebelum memulai tugas. Saat bekerja, Claude menyimpan apa yang dipelajarinya dalam file di bawah `/memories` dan membacanya kembali di percakapan selanjutnya untuk melanjutkan pekerjaan sebelumnya.

Karena alat memori bersifat sisi klien, Claude hanya meminta operasi memori. Aplikasi Anda mengeksekusi setiap permintaan terhadap penyimpanan yang Anda kontrol dan mengembalikan hasilnya dalam blok `tool_result` (lihat [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls)). Path `/memories` adalah prefiks yang dipetakan oleh handler Anda ke penyimpanan nyata, seperti direktori per pengguna atau key dalam database. Memori sepenuhnya berada di aplikasi Anda. Percakapan selanjutnya melanjutkan dari memori yang sama ketika mengirimkan entri `tools` yang sama dan handler Anda melayani penyimpanan yang sama. Untuk keamanan, batasi semua operasi memori ke direktori `/memories` (lihat [Perlindungan path traversal](#path-traversal-protection)).

### Contoh: Cara kerja panggilan alat memori

Interaksi yang umum terlihat seperti ini:

**1. Permintaan pengguna:**

```text wrap
"Help me respond to this customer service ticket."
```

**2. Claude memeriksa direktori memori:**

```text wrap
"I'll help you respond to the customer service ticket. Let me check my memory for any previous context."
```

Claude memanggil alat memori:

```json
{
  "type": "tool_use",
  "id": "toolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "name": "memory",
  "input": {
    "command": "view",
    "path": "/memories"
  }
}
```

**3. Aplikasi Anda mengembalikan isi direktori:**

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "content": "Here're the files and directories up to 2 levels deep in /memories, excluding hidden items and node_modules:\n4.0K\t/memories\n1.5K\t/memories/customer_service_guidelines.xml\n2.0K\t/memories/refund_policies.xml"
}
```

**4. Claude membaca file yang relevan:**

```json
{
  "type": "tool_use",
  "id": "toolu_01D5E6F7G8H9I0J1K2L3M4N5",
  "name": "memory",
  "input": {
    "command": "view",
    "path": "/memories/customer_service_guidelines.xml"
  }
}
```

**5. Aplikasi Anda mengembalikan isi file:**

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01D5E6F7G8H9I0J1K2L3M4N5",
  "content": "Here's the content of /memories/customer_service_guidelines.xml with line numbers:\n     1\t<guidelines>\n     2\t<addressing_customers>\n     3\t- Always address customers by their first name\n     4\t- Use empathetic language\n..."
}
```

**6. Claude menggunakan memori untuk membantu:**

```text wrap
"Based on your customer service guidelines, I can help you craft a response. Please share the ticket details..."
```

Alat memori tersedia di semua model Claude 4 dan yang lebih baru. Untuk daftar lengkap alat yang disediakan Anthropic, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Memulai

Alat memori tersedia secara umum di Messages API: tidak diperlukan header beta. Menggunakannya memerlukan dua langkah:

1. Tambahkan alat memori ke permintaan Anda. Entri `tools` `{"type": "memory_20250818", "name": "memory"}` adalah keseluruhan konfigurasi: `name` harus berupa `memory`, dan Anda tidak mendefinisikan skema input untuk alat yang disediakan Anthropic.
2. Implementasikan handler sisi klien untuk setiap perintah memori. Handler Anda harus menolak path di luar `/memories`, jadi baca [Perlindungan path traversal](#path-traversal-protection) sebelum Anda menulisnya.

## Penggunaan dasar

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 2048,
      "messages": [
        {
          "role": "user",
          "content": "Help me respond to this customer service ticket."
        }
      ],
      "tools": [{
        "type": "memory_20250818",
        "name": "memory"
      }]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 2048
  tools:
    - type: memory_20250818
      name: memory
  messages:
    - role: user
      content: Help me respond to this customer service ticket.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=2048,
      messages=[
          {
              "role": "user",
              "content": "Help me respond to this customer service ticket.",
          }
      ],
      tools=[{"type": "memory_20250818", "name": "memory"}],
  )

  print(message)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const message = await anthropic.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: "Help me respond to this customer service ticket."
      }
    ],
    tools: [{ type: "memory_20250818", name: "memory" }]
  });

  console.log(message);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var message = await client.Messages.Create(
      new()
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 2048,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "Help me respond to this customer service ticket.",
              },
          ],
          Tools = [new MemoryTool20250818()],
      }
  );

  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 2048,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Help me respond to this customer service ticket.")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfMemoryTool20250818: &anthropic.MemoryTool20250818Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message)
  ```

  ```java Java
  import com.anthropic.models.messages.MemoryTool20250818;
  // ...
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(2048L)
      .addTool(MemoryTool20250818.builder().build())
      .addUserMessage("Help me respond to this customer service ticket.")
      .build();

    Message message = client.messages().create(params);
    IO.println(message);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      model: Model::CLAUDE_OPUS_4_8,
      maxTokens: 2048,
      messages: [
          [
              'role' => 'user',
              'content' => 'Help me respond to this customer service ticket.',
          ],
      ],
      tools: [new MemoryTool20250818],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_4_8,
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: "Help me respond to this customer service ticket."
      }
    ],
    tools: [
      {
        type: "memory_20250818",
        name: "memory"
      }
    ]
  )
  puts message
  ```
</CodeGroup>

## Mengimplementasikan handler memori

Balasan Claude terhadap permintaan seperti yang sebelumnya diakhiri dengan blok `tool_use` yang meminta operasi memori, seperti `view /memories`. Aplikasi Anda mengeksekusi operasi tersebut dan mengembalikan hasilnya dalam blok `tool_result`, lalu mengirim percakapan kembali agar Claude dapat melanjutkan: ini adalah [loop penggunaan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) standar.

Empat SDK menyediakan helper alat memori yang menangani antarmuka alat dan loop tersebut. Buat subclass dari `BetaAbstractMemoryTool` (Python dan C#), gunakan `betaMemoryTool` (TypeScript), atau implementasikan `BetaMemoryToolHandler` (Java) untuk mendukung memori dengan penyimpanan Anda sendiri, seperti file di disk, database, penyimpanan cloud, atau file terenkripsi. Python dan TypeScript juga menyertakan implementasi filesystem lokal siap pakai, `BetaLocalFilesystemMemoryTool`. Antarmuka helper dan tool-runner berada di namespace beta masing-masing SDK meskipun alat memori itu sendiri sudah tersedia secara umum. SDK Go dan Ruby tidak memiliki helper memori, sehingga contoh-contoh tersebut menjalankan loop penggunaan alat sendiri, dan PHP membungkus closure handler Anda dalam `BetaRunnableTool` generiknya. Ketiganya menggunakan penyimpanan dalam memori yang Anda ganti dengan penyimpanan Anda sendiri.

<CodeGroup>
  ```python Python
  import anthropic
  from anthropic.tools import BetaLocalFilesystemMemoryTool

  client = anthropic.Anthropic()
  memory = BetaLocalFilesystemMemoryTool(base_path="./memory")

  runner = client.beta.messages.tool_runner(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Remember that customer Acme Corp prefers email follow-ups.",
          }
      ],
      tools=[memory],
  )

  final_message = runner.until_done()
  print(final_message.content)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { betaMemoryTool } from "@anthropic-ai/sdk/helpers/beta/memory";
  import { BetaLocalFilesystemMemoryTool } from "@anthropic-ai/sdk/tools/memory/node";

  const client = new Anthropic();

  const backend = await BetaLocalFilesystemMemoryTool.init("./memory");
  const memory = betaMemoryTool(backend); // or pass your own handlers object

  const runner = client.beta.messages.toolRunner({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "Remember that customer Acme Corp prefers email follow-ups."
      }
    ],
    tools: [memory],
    max_iterations: 10
  });

  const finalMessage = await runner;
  console.log(finalMessage.content);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Helpers.Beta;
  using Anthropic.Models.Beta.Messages;

  var client = new AnthropicClient();

  // Subkelas Anda dari BetaAbstractMemoryTool
  var memory = new FilesystemMemoryTool("./memories");

  var runner = client.Beta.Messages.ToolRunner(
      new MessageCreateParams
      {
          Model = Anthropic.Models.Messages.Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "Remember that customer Acme Corp prefers email follow-ups.",
              },
          ],
      },
      [memory],
      maxIterations: 10
  );

  var finalMessage = await runner.RunUntilDoneAsync();
  Console.WriteLine(finalMessage);
  ```

  ```go Go
  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"
  	"slices"
  	"sort"
  	"strings"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  // Penyimpanan dalam memori yang memetakan path file memori ke isinya.
  // Gunakan penyimpanan Anda sendiri di lingkungan produksi.
  var store = map[string]string{}

  type memoryCommand struct {
  	Command    string `json:"command"`
  	Path       string `json:"path"`
  	FileText   string `json:"file_text"`
  	OldStr     string `json:"old_str"`
  	NewStr     string `json:"new_str"`
  	InsertLine int    `json:"insert_line"`
  	InsertText string `json:"insert_text"`
  	OldPath    string `json:"old_path"`
  	NewPath    string `json:"new_path"`
  }

  func executeMemory(raw json.RawMessage) string {
  	var cmd memoryCommand
  	if err := json.Unmarshal(raw, &cmd); err != nil {
  		return "Error: invalid memory command"
  	}
  	switch cmd.Command {
  	case "view":
  		if content, ok := store[cmd.Path]; ok {
  			lines := strings.Split(strings.TrimSuffix(content, "\n"), "\n")
  			for i, line := range lines {
  				lines[i] = fmt.Sprintf("%6d\t%s", i+1, line)
  			}
  			return fmt.Sprintf("Here's the content of %s with line numbers:\n%s", cmd.Path, strings.Join(lines, "\n"))
  		}
  		if cmd.Path == "/memories" {
  			listing := []string{"1.0K\t/memories"}
  			for path := range store {
  				listing = append(listing, "1.0K\t"+path)
  			}
  			sort.Strings(listing[1:])
  			return fmt.Sprintf("Here're the files and directories up to 2 levels deep in %s, excluding hidden items and node_modules:\n%s", cmd.Path, strings.Join(listing, "\n"))
  		}
  		return fmt.Sprintf("The path %s does not exist. Please provide a valid path.", cmd.Path)
  	case "create":
  		store[cmd.Path] = cmd.FileText
  		return "File created successfully at: " + cmd.Path
  	case "str_replace":
  		content, ok := store[cmd.Path]
  		if !ok || !strings.Contains(content, cmd.OldStr) {
  			return fmt.Sprintf("No replacement was performed, old_str `%s` did not appear verbatim in %s.", cmd.OldStr, cmd.Path)
  		}
  		store[cmd.Path] = strings.Replace(content, cmd.OldStr, cmd.NewStr, 1)
  		return "The memory file has been edited."
  	case "insert":
  		content, ok := store[cmd.Path]
  		if !ok {
  			return fmt.Sprintf("Error: The path %s does not exist", cmd.Path)
  		}
  		lines := strings.Split(content, "\n")
  		if cmd.InsertLine < 0 || cmd.InsertLine > len(lines) {
  			return fmt.Sprintf("Error: Invalid `insert_line` parameter: %d. It should be within the range of lines of the file: [0, %d]", cmd.InsertLine, len(lines))
  		}
  		lines = slices.Insert(lines, cmd.InsertLine, strings.TrimSuffix(cmd.InsertText, "\n"))
  		store[cmd.Path] = strings.Join(lines, "\n")
  		return fmt.Sprintf("The file %s has been edited.", cmd.Path)
  	case "delete":
  		if _, ok := store[cmd.Path]; !ok {
  			return fmt.Sprintf("Error: The path %s does not exist", cmd.Path)
  		}
  		delete(store, cmd.Path)
  		return "Successfully deleted " + cmd.Path
  	case "rename":
  		if _, ok := store[cmd.OldPath]; !ok {
  			return fmt.Sprintf("Error: The path %s does not exist", cmd.OldPath)
  		}
  		if _, ok := store[cmd.NewPath]; ok {
  			return fmt.Sprintf("Error: The destination %s already exists", cmd.NewPath)
  		}
  		store[cmd.NewPath] = store[cmd.OldPath]
  		delete(store, cmd.OldPath)
  		return fmt.Sprintf("Successfully renamed %s to %s", cmd.OldPath, cmd.NewPath)
  	default:
  		return "Error: unknown command " + cmd.Command
  	}
  }

  func main() {
  	client := anthropic.NewClient()
  	tools := []anthropic.ToolUnionParam{{OfMemoryTool20250818: &anthropic.MemoryTool20250818Param{}}}
  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Remember that customer Acme Corp prefers email follow-ups.")),
  	}

  	for {
  		message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus4_8,
  			MaxTokens: 1024,
  			Messages:  messages,
  			Tools:     tools,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  		if message.StopReason != anthropic.StopReasonToolUse {
  			for _, block := range message.Content {
  				if block.Type == "text" {
  					fmt.Println(block.Text)
  				}
  			}
  			break
  		}
  		results := []anthropic.ContentBlockParamUnion{}
  		for _, block := range message.Content {
  			if block.Type == "tool_use" {
  				results = append(results, anthropic.NewToolResultBlock(block.ID, executeMemory(block.Input), false))
  			}
  		}
  		messages = append(messages, message.ToParam(), anthropic.NewUserMessage(results...))
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.helpers.BetaMemoryToolHandler;
  import com.anthropic.helpers.BetaToolRunner;
  import com.anthropic.models.beta.messages.BetaMemoryTool20250818;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.MessageCreateParams; // beta package, not models.messages
  import com.anthropic.models.beta.messages.ToolRunnerCreateParams;
  import com.anthropic.models.messages.Model;
  import java.nio.file.Path;

  void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Implementasi BetaMemoryToolHandler Anda untuk enam perintah memori
    BetaMemoryToolHandler handler = new FileSystemMemoryToolHandler(Path.of("memories"));

    MessageCreateParams createParams = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addTool(BetaMemoryTool20250818.builder().build())
      .addUserMessage("Remember that customer Acme Corp prefers email follow-ups.")
      .build();

    ToolRunnerCreateParams runnerParams = ToolRunnerCreateParams.builder()
      .betaMemoryToolHandler(handler)
      .initialMessageParams(createParams)
      .maxIterations(10)
      .build();

    BetaToolRunner runner = client.beta().messages().toolRunner(runnerParams);
    for (BetaMessage message : runner) {
      IO.println(message);
    }
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Beta\Messages\BetaMemoryTool20250818;
  use Anthropic\Client;
  use Anthropic\Lib\Tools\BetaRunnableTool;
  use Anthropic\Messages\Model;

  $client = new Client();

  // Penyimpanan dalam memori yang memetakan path file memori ke kontennya.
  // Gunakan penyimpanan Anda sendiri di lingkungan produksi.
  $store = [];

  $memory = new BetaRunnableTool(
      definition: new BetaMemoryTool20250818,
      run: function (array $input) use (&$store): string {
          $path = $input['path'] ?? '';
          switch ($input['command']) {
              case 'view':
                  if (isset($store[$path])) {
                      $numbered = [];
                      foreach (explode("\n", preg_replace('/\n\z/', '', $store[$path])) as $i => $line) {
                          $numbered[] = sprintf("%6d\t%s", $i + 1, $line);
                      }
                      return "Here's the content of {$path} with line numbers:\n" . implode("\n", $numbered);
                  }
                  if ($path === '/memories') {
                      $listing = ["1.0K\t/memories"];
                      foreach (array_keys($store) as $stored) {
                          $listing[] = "1.0K\t{$stored}";
                      }
                      return "Here're the files and directories up to 2 levels deep in {$path}, excluding hidden items and node_modules:\n" . implode("\n", $listing);
                  }
                  return "The path {$path} does not exist. Please provide a valid path.";
              case 'create':
                  $store[$path] = $input['file_text'];
                  return "File created successfully at: {$path}";
              case 'str_replace':
                  $position = strpos($store[$path] ?? '', $input['old_str']);
                  if ($position === false) {
                      return "No replacement was performed, old_str `{$input['old_str']}` did not appear verbatim in {$path}.";
                  }
                  $store[$path] = substr_replace($store[$path], $input['new_str'] ?? '', $position, strlen($input['old_str']));
                  return 'The memory file has been edited.';
              case 'insert':
                  if (!isset($store[$path])) {
                      return "Error: The path {$path} does not exist";
                  }
                  $lines = explode("\n", $store[$path]);
                  if ($input['insert_line'] < 0 || $input['insert_line'] > count($lines)) {
                      return "Error: Invalid `insert_line` parameter: {$input['insert_line']}. It should be within the range of lines of the file: [0, " . count($lines) . "]";
                  }
                  array_splice($lines, $input['insert_line'], 0, [preg_replace('/\n\z/', '', $input['insert_text'])]);
                  $store[$path] = implode("\n", $lines);
                  return "The file {$path} has been edited.";
              case 'delete':
                  if (!isset($store[$path])) {
                      return "Error: The path {$path} does not exist";
                  }
                  unset($store[$path]);
                  return "Successfully deleted {$path}";
              case 'rename':
                  if (!isset($store[$input['old_path']])) {
                      return "Error: The path {$input['old_path']} does not exist";
                  }
                  if (isset($store[$input['new_path']])) {
                      return "Error: The destination {$input['new_path']} already exists";
                  }
                  $store[$input['new_path']] = $store[$input['old_path']];
                  unset($store[$input['old_path']]);
                  return "Successfully renamed {$input['old_path']} to {$input['new_path']}";
              default:
                  return "Error: unknown command {$input['command']}";
          }
      },
  );

  $runner = $client->beta->messages->toolRunner(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Remember that customer Acme Corp prefers email follow-ups.']],
      model: Model::CLAUDE_OPUS_4_8,
      tools: [$memory],
      maxIterations: 10,
  );

  $finalMessage = $runner->runUntilDone();
  print_r($finalMessage->content);
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new
  TOOLS = [{type: "memory_20250818", name: "memory"}].freeze

  # Penyimpanan dalam memori yang memetakan path file memori ke isinya.
  # Gunakan penyimpanan Anda sendiri di lingkungan produksi.
  STORE = {}

  def execute_memory(input)
    path = input[:path]
    case input[:command]
    when "view"
      if STORE.key?(path)
        lines = STORE[path].chomp.split("\n", -1)
        lines = [""] if lines.empty?
        numbered = lines.each_with_index.map { |line, i| format("%6d\t%s", i + 1, line) }
        "Here's the content of #{path} with line numbers:\n#{numbered.join("\n")}"
      elsif path == "/memories"
        listing = ["1.0K\t/memories"] + STORE.keys.map { |stored| "1.0K\t#{stored}" }
        "Here're the files and directories up to 2 levels deep in #{path}, excluding hidden items and node_modules:\n#{listing.join("\n")}"
      else
        "The path #{path} does not exist. Please provide a valid path."
      end
    when "create"
      STORE[path] = input[:file_text]
      "File created successfully at: #{path}"
    when "str_replace"
      unless STORE.key?(path) && STORE[path].include?(input[:old_str])
        return "No replacement was performed, old_str `#{input[:old_str]}` did not appear verbatim in #{path}."
      end
      STORE[path] = STORE[path].sub(input[:old_str]) { input[:new_str].to_s }
      "The memory file has been edited."
    when "insert"
      return "Error: The path #{path} does not exist" unless STORE.key?(path)
      lines = STORE[path].split("\n", -1)
      lines = [""] if lines.empty?
      if input[:insert_line] < 0 || input[:insert_line] > lines.length
        return "Error: Invalid `insert_line` parameter: #{input[:insert_line]}. It should be within the range of lines of the file: [0, #{lines.length}]"
      end
      lines.insert(input[:insert_line], input[:insert_text].chomp)
      STORE[path] = lines.join("\n")
      "The file #{path} has been edited."
    when "delete"
      return "Error: The path #{path} does not exist" unless STORE.key?(path)
      STORE.delete(path)
      "Successfully deleted #{path}"
    when "rename"
      return "Error: The path #{input[:old_path]} does not exist" unless STORE.key?(input[:old_path])
      return "Error: The destination #{input[:new_path]} already exists" if STORE.key?(input[:new_path])
      STORE[input[:new_path]] = STORE.delete(input[:old_path])
      "Successfully renamed #{input[:old_path]} to #{input[:new_path]}"
    else
      "Error: unknown command #{input[:command]}"
    end
  end

  messages = [{role: "user", content: "Remember that customer Acme Corp prefers email follow-ups."}]
  loop do
    message = client.messages.create(
      model: Anthropic::Model::CLAUDE_OPUS_4_8,
      max_tokens: 1024,
      messages: messages,
      tools: TOOLS
    )
    unless message.stop_reason == :tool_use
      puts message.content
      break
    end
    tool_results = message.content.filter_map do |block|
      next unless block.type == :tool_use
      {type: "tool_result", tool_use_id: block.id, content: execute_memory(block.input)}
    end
    messages << {role: "assistant", content: message.content} << {role: "user", content: tool_results}
  end
  ```
</CodeGroup>

Penyimpanan dalam memori pada contoh Go, PHP, dan Ruby membuat contoh-contoh tersebut mandiri: masing-masing melakukan dispatch berdasarkan field `command` dalam `input` blok `tool_use` dan mengembalikan string yang dijelaskan di bawah [Perintah alat](#tool-commands). Handler produksi juga memerlukan [validasi path](#path-traversal-protection) yang dilewati oleh penyimpanan demonstrasi ini. Untuk contoh lengkap dari SDK itu sendiri, lihat:

* Python: [examples/memory/basic.py](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/memory/basic.py)
* TypeScript: [examples/tools-helpers-memory.ts](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/examples/tools-helpers-memory.ts)
* C#: [MemoryToolExample](https://github.com/anthropics/anthropic-sdk-csharp/tree/main/examples/MemoryToolExample)
* Java: [BetaMemoryToolExample.java](https://github.com/anthropics/anthropic-sdk-java/blob/main/anthropic-java-example/src/main/java/com/anthropic/example/BetaMemoryToolExample.java)

## Perintah alat

Implementasi sisi klien Anda harus menangani perintah-perintah berikut. Spesifikasi ini menjelaskan perilaku dan string pengembalian yang direkomendasikan: Claude membaca teks apa pun yang terdapat dalam hasil alat Anda, jadi Anda dapat mengembalikan string yang berbeda jika aplikasi Anda membutuhkannya.

### view

Menampilkan isi direktori atau isi file dengan rentang baris opsional:

```json
{
  "command": "view",
  "path": "/memories/notes.txt",
  "view_range": [1, 10]
}
```

`view_range` bersifat opsional dan berlaku untuk tampilan file teks: `[start_line, end_line]` mengembalikan baris-baris tersebut, dan `[start_line, -1]` mengembalikan semuanya dari `start_line` hingga akhir file.

#### Nilai pengembalian

**Untuk direktori:** Kembalikan daftar yang menampilkan file dan direktori beserta ukurannya:

```text
Here're the files and directories up to 2 levels deep in {path}, excluding hidden items and node_modules:
{size}\t{path}
{size}\t{path}/{filename1}
{size}\t{path}/{filename2}
```

* Mencantumkan file hingga kedalaman 2 level
* Menampilkan ukuran yang mudah dibaca manusia (misalnya, `5.5K`, `1.2M`)
* Mengecualikan item tersembunyi (file yang dimulai dengan `.`) dan `node_modules`
* Menggunakan karakter tab antara ukuran dan path

`view` pertama terhadap `/memories` pada penyimpanan kosong bukanlah error. Alat memori filesystem lokal dari SDK (`BetaLocalFilesystemMemoryTool`) membuat root memori sebelum panggilan pertama Claude dan mengembalikan header daftar diikuti oleh satu baris ukuran-dan-path untuk direktori kosong itu sendiri.

**Untuk file:** Kembalikan isi file dengan header dan nomor baris:

```text wrap
Here's the content of {path} with line numbers:
{line_numbers}{tab}{content}
```

Format nomor baris:

* **Lebar:** 6 karakter, rata kanan dengan padding spasi
* **Pemisah:** Karakter tab antara nomor baris dan konten
* **Pengindeksan:** Dimulai dari 1 (baris pertama adalah baris 1)
* **Batas baris:** File dengan lebih dari 999.999 baris harus mengembalikan error: `"File {path} exceeds maximum line limit of 999,999 lines."`

**Contoh output:**

```text
Here's the content of /memories/notes.txt with line numbers:
     1	Hello World
     2	This is line two
    10	Line ten
   100	Line one hundred
```

Deskripsi alat Claude juga menyatakan bahwa `view` menampilkan file gambar (`.jpg`, `.jpeg`, dan `.png`) dan memotong tampilan teks dari file yang lebih panjang dari 16.000 karakter. Antisipasi panggilan `view` pada path gambar dan tampilan berentang lanjutan untuk file panjang.

#### Penanganan error

* **File atau direktori tidak ada:** `"The path {path} does not exist. Please provide a valid path."`

### create

Membuat file baru:

```json
{
  "command": "create",
  "path": "/memories/notes.txt",
  "file_text": "Meeting notes:\n- Discussed project timeline\n- Next steps defined\n"
}
```

#### Nilai pengembalian

* **Berhasil:** `"File created successfully at: {path}"`

#### Penanganan error

* **File sudah ada:** `"Error: File {path} already exists"`

Deskripsi alat Claude menyatakan bahwa `create` "membuat atau menimpa" file, jadi antisipasi panggilan `create` pada path yang sudah ada. Mengembalikan error adalah perilaku referensi, dan menimpa sebagai gantinya adalah pilihan implementasi yang valid.

### str\_replace

Mengganti teks dalam file:

```json
{
  "command": "str_replace",
  "path": "/memories/preferences.txt",
  "old_str": "Favorite color: blue",
  "new_str": "Favorite color: green"
}
```

`new_str` bersifat opsional untuk `str_replace`: ketika dihilangkan, `old_str` dihapus tanpa pengganti.

#### Nilai pengembalian

* **Berhasil:** `"The memory file has been edited."` diikuti oleh cuplikan file yang telah diedit dengan nomor baris

#### Penanganan error

* **File tidak ada:** `"Error: The path {path} does not exist. Please provide a valid path."`
* **Teks tidak ditemukan:** ``"No replacement was performed, old_str `\{old_str}` did not appear verbatim in {path}."``
* **Teks duplikat:** Ketika `old_str` muncul beberapa kali, kembalikan: ``"No replacement was performed. Multiple occurrences of old_str `\{old_str}` in lines: {line_numbers}. Please ensure it is unique"``

#### Penanganan direktori

Jika path adalah direktori, kembalikan error "file does not exist".

### insert

Menyisipkan teks pada baris tertentu:

```json
{
  "command": "insert",
  "path": "/memories/todo.txt",
  "insert_line": 2,
  "insert_text": "- Review memory tool documentation\n"
}
```

`insert_text` disisipkan setelah baris `insert_line`, dan `0` menyisipkan di awal file.

#### Nilai pengembalian

* **Berhasil:** `"The file {path} has been edited."`

#### Penanganan error

* **File tidak ada:** `"Error: The path {path} does not exist"`
* **Nomor baris tidak valid:** ``"Error: Invalid `insert_line` parameter: {insert_line}. It should be within the range of lines of the file: [0, {n_lines}]"``

#### Penanganan direktori

Jika path adalah direktori, kembalikan error "file does not exist".

### delete

Menghapus file atau direktori:

```json
{
  "command": "delete",
  "path": "/memories/old_file.txt"
}
```

#### Nilai pengembalian

* **Berhasil:** `"Successfully deleted {path}"`

#### Penanganan error

* **File atau direktori tidak ada:** `"Error: The path {path} does not exist"`

#### Penanganan direktori

Menghapus direktori dan semua isinya secara rekursif. Deskripsi alat memberi tahu Claude bahwa ia tidak dapat menghapus direktori `/memories` itu sendiri, jadi tolak `delete` yang path-nya adalah root memori.

### rename

Mengganti nama atau memindahkan file atau direktori:

```json
{
  "command": "rename",
  "old_path": "/memories/draft.txt",
  "new_path": "/memories/final.txt"
}
```

#### Nilai pengembalian

* **Berhasil:** `"Successfully renamed {old_path} to {new_path}"`

#### Penanganan error

* **Sumber tidak ada:** `"Error: The path {old_path} does not exist"`
* **Tujuan sudah ada:** Kembalikan error (jangan menimpa): `"Error: The destination {new_path} already exists"`

#### Penanganan direktori

Mengganti nama direktori. Deskripsi alat memberi tahu Claude bahwa ia tidak dapat mengganti nama direktori `/memories` itu sendiri, jadi tolak `rename` yang `old_path`-nya adalah root memori.

## Panduan prompting

Ketika alat memori ada dalam `tools` permintaan Anda, API secara otomatis menambahkan instruksi ini ke prompt sistem. Anda tidak perlu mengirimkannya sendiri:

```text wrap
IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
MEMORY PROTOCOL:
1. Use the `view` command of your `memory` tool to check for earlier progress.
2. ... (work on the task) ...
   - As you make progress, record status / progress / thoughts etc in your memory.
ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
```

Deskripsi alat Claude sudah memberitahunya untuk menjaga direktori memori tetap terorganisir, jadi Anda tidak perlu mengulangi instruksi tersebut. Jika Claude masih membuat file memori yang berantakan, Anda dapat memperkuatnya dalam prompt Anda:

```text wrap
Note: when editing your memory folder, always try to keep its content up-to-date, coherent and organized. You can rename or delete files that are no longer relevant. Do not create new files unless necessary.
```

Anda juga dapat memandu apa yang Claude tulis ke memori. Misalnya: "Only write down information relevant to \<topic> in your memory system."

## Pertimbangan keamanan

Aplikasi Anda mengeksekusi setiap operasi file yang diminta Claude, jadi pengamanan berikut adalah tanggung jawab Anda:

### Informasi sensitif

Claude biasanya menolak untuk menulis informasi sensitif ke file memori. Untuk jaminan yang lebih kuat, tambahkan validasi yang menghapus data sensitif sebelum handler Anda menulis file.

### Ukuran penyimpanan file

Lacak ukuran file memori dan batasi seberapa besar file dapat bertambah. Pertimbangkan untuk membatasi berapa banyak karakter yang dikembalikan perintah `view`, dan biarkan Claude menelusuri sisanya dengan `view_range`.

### Kedaluwarsa memori

Hapus secara berkala file memori yang sudah lama tidak diakses.

### Perlindungan path traversal

<Warning>
  Path berbahaya seperti `/memories/../../secrets.env` dapat menjangkau file di luar direktori `/memories`. Implementasi Anda harus memvalidasi setiap path di setiap perintah untuk mencegah serangan "directory traversal" (penelusuran direktori).
</Warning>

Pertimbangkan pengamanan berikut:

* Validasi bahwa semua path dimulai dengan `/memories`
* Resolusikan path ke bentuk kanonisnya dan verifikasi bahwa path tetap berada di dalam direktori memori
* Tolak path yang berisi urutan seperti `../`, `..\\`, atau pola traversal lainnya
* Waspadai urutan traversal yang di-encode URL (`%2e%2e%2f`)
* Gunakan utilitas keamanan path bawaan bahasa Anda (misalnya, `pathlib.Path.resolve()` dan `relative_to()` di Python)

## Penanganan error

Alat memori menggunakan pola penanganan error yang serupa dengan [alat text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool#handle-errors). Pesan error setiap perintah tercantum di bawah [Perintah alat](#tool-commands). Untuk mengembalikan error ke Claude, atur `is_error` ke `true` pada hasil alat dan letakkan pesan di `content`:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "content": "Error: The path /memories/notes.txt does not exist",
  "is_error": true
}
```

## Integrasi context editing

Alat memori berpasangan dengan "context editing" (pengeditan konteks) untuk mengelola percakapan jangka panjang. Untuk detailnya, lihat [Context editing](/docs/id/build-with-claude/context-editing).

## Menggunakan dengan compaction

Alat memori juga dapat dipasangkan dengan [compaction](/docs/id/build-with-claude/compaction), yang meringkas konteks percakapan lama di sisi server. Context editing menghapus hasil alat tertentu di klien. Compaction secara otomatis meringkas seluruh percakapan di server ketika percakapan mendekati batas jendela konteks.

Untuk agen jangka panjang, pertimbangkan untuk menggunakan keduanya: compaction menjaga konteks aktif tetap kecil tanpa pembukuan sisi klien, dan memori mempertahankan informasi yang harus bertahan dari peringkasan.

## Pola pengembangan perangkat lunak multi-sesi

Untuk proyek perangkat lunak yang mencakup beberapa sesi agen, siapkan file memori secara sengaja alih-alih menulisnya secara ad hoc seiring berjalannya pekerjaan. Pola berikut mengubah memori menjadi mekanisme pemulihan: setiap sesi baru melanjutkan dari keadaan yang dicatat oleh sesi terakhir.

### Cara kerja pola ini

1. **Sesi inisialisasi:** Sesi pertama menyiapkan file memori sebelum pekerjaan substantif dimulai. Ini mencakup log kemajuan (melacak apa yang telah dilakukan dan apa yang berikutnya), daftar periksa fitur (mendefinisikan cakupan pekerjaan), dan referensi ke skrip startup atau inisialisasi apa pun yang dibutuhkan proyek.

2. **Sesi berikutnya:** Setiap sesi baru dibuka dengan membaca file memori tersebut. Ini memulihkan keadaan proyek tanpa menjelajahi ulang basis kode atau menelusuri kembali keputusan sebelumnya.

3. **Pembaruan akhir sesi:** Sebelum sesi berakhir, sesi memperbarui log kemajuan dengan apa yang telah diselesaikan dan apa yang tersisa. Ini memastikan sesi berikutnya memiliki titik awal yang akurat.

### Prinsip utama

Kerjakan satu fitur pada satu waktu. Tandai fitur sebagai selesai hanya setelah verifikasi end-to-end mengonfirmasi bahwa fitur tersebut berfungsi, bukan ketika kodenya selesai ditulis. Ini menjaga log kemajuan tetap akurat dari sesi ke sesi.

<Tip>
  Untuk studi kasus terperinci tentang pola ini dalam praktik, termasuk skrip inisialisasi, struktur file kemajuan, dan pemulihan berbasis git, lihat [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
</Tip>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Alat Bash" icon="terminal" href="/docs/id/agents-and-tools/tool-use/bash-tool">
    Jalankan perintah shell dalam sesi bash yang persisten.
  </Card>

  <Card title="Context editing" icon="edit" href="/docs/id/build-with-claude/context-editing">
    Kelola konteks percakapan secara otomatis seiring pertumbuhannya dengan context editing.
  </Card>

  <Card title="Compaction" icon="stack" href="/docs/id/build-with-claude/compaction">
    Pemadatan konteks sisi server untuk mengelola percakapan panjang yang mendekati batas jendela konteks.
  </Card>

  <Card title="Referensi alat" icon="book" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>
</CardGroup>
