---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 7ba8ed1eeadc27a68edbbf37cdd85a8437d47a74133a1f84f08826c56e5fb5ec
---

# Alat memori

---

Alat memori memungkinkan Claude untuk menyimpan dan mengambil informasi di seluruh percakapan melalui direktori file memori. Claude dapat membuat, membaca, memperbarui, dan menghapus file yang tetap ada di antara sesi, memungkinkannya membangun pengetahuan dari waktu ke waktu tanpa menyimpan semuanya di dalam "context window" (jendela konteks).

Ini adalah primitif utama untuk pengambilan konteks tepat waktu (just-in-time): alih-alih memuat semua informasi yang relevan di awal, agen menyimpan apa yang mereka pelajari di memori dan mengambilnya kembali sesuai kebutuhan. Hal ini menjaga konteks aktif tetap fokus pada apa yang saat ini relevan, yang sangat penting untuk alur kerja jangka panjang di mana memuat semuanya sekaligus akan membebani jendela konteks. Lihat [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) untuk pola yang lebih luas.

Alat memori beroperasi di sisi klien: Anda mengontrol di mana dan bagaimana data disimpan melalui infrastruktur Anda sendiri.

<Note>
  Hubungi kami melalui [formulir umpan balik](https://forms.gle/YXC2EKGMhjN1c4L88) untuk membagikan masukan Anda tentang fitur ini.
</Note>

<Note>
  Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

## Kasus penggunaan

* Mempertahankan konteks proyek di seluruh beberapa eksekusi agen
* Belajar dari interaksi, keputusan, dan umpan balik sebelumnya
* Membangun basis pengetahuan dari waktu ke waktu
* Memungkinkan pembelajaran lintas percakapan di mana Claude menjadi lebih baik dalam alur kerja yang berulang

## Cara kerjanya

Ketika diaktifkan, Claude secara otomatis memeriksa direktori memorinya sebelum memulai tugas. Claude dapat membuat, membaca, memperbarui, dan menghapus file di direktori `/memories` untuk menyimpan apa yang dipelajarinya saat bekerja, kemudian mereferensikan memori tersebut dalam percakapan mendatang untuk menangani tugas serupa dengan lebih efektif atau melanjutkan dari titik terakhir.

Karena ini adalah alat sisi klien, Claude membuat panggilan alat untuk melakukan operasi memori, dan aplikasi Anda mengeksekusi operasi tersebut secara lokal. Ini memberi Anda kontrol penuh atas di mana dan bagaimana memori disimpan. Untuk keamanan, Anda harus membatasi semua operasi memori ke direktori `/memories`.

### Contoh: Cara kerja panggilan alat memori

Ketika Anda meminta Claude untuk membantu suatu tugas, Claude secara otomatis memeriksa direktori memorinya terlebih dahulu. Berikut adalah tampilan interaksi yang umum:

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

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Memulai

Untuk menggunakan alat memori:

1. Tambahkan alat memori ke permintaan Anda
2. Implementasikan handler sisi klien untuk operasi memori

<Note>
  Untuk menangani operasi alat memori di aplikasi Anda, Anda perlu mengimplementasikan handler untuk setiap perintah memori. SDK menyediakan helper alat memori yang menangani antarmuka alat. Anda dapat membuat subclass dari `BetaAbstractMemoryTool` (Python dan C#), menggunakan `betaMemoryTool` (TypeScript), atau mengimplementasikan `BetaMemoryToolHandler` (Java) untuk mengimplementasikan backend memori Anda sendiri (berbasis file, database, penyimpanan cloud, file terenkripsi, dll.).

  Untuk contoh yang berfungsi, lihat:

  * Python: [examples/memory/basic.py](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/memory/basic.py)
  * TypeScript: [examples/tools-helpers-memory.ts](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/examples/tools-helpers-memory.ts)
  * Java: [BetaMemoryToolExample.java](https://github.com/anthropics/anthropic-sdk-java/blob/main/anthropic-java-example/src/main/java/com/anthropic/example/BetaMemoryToolExample.java)
  * C#: [MemoryToolExample](https://github.com/anthropics/anthropic-sdk-csharp/tree/main/examples/MemoryToolExample)
</Note>

## Penggunaan dasar

<CodeGroup>
  ````bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 2048,
          "messages": [
              {
                  "role": "user",
                  "content": "I'\''m working on a Python web scraper that keeps crashing with a timeout error. Here'\''s the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this."
              }
          ],
          "tools": [{
              "type": "memory_20250818",
              "name": "memory"
          }]
      }'
  ````

  ````bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 2048
  tools:
    - type: memory_20250818
      name: memory
  messages:
    - role: user
      content: |
        I'm working on a Python web scraper that keeps crashing with a
        timeout error. Here's the problematic function:

        ```python
        def fetch_page(url, retries=3):
            for i in range(retries):
                try:
                    response = requests.get(url, timeout=5)
                    return response.text
                except requests.exceptions.Timeout:
                    if i == retries - 1:
                        raise
                    time.sleep(1)
        ```

        Please help me debug this.
  YAML
  ````

  ````python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=2048,
      messages=[
          {
              "role": "user",
              "content": "I'm working on a Python web scraper that keeps crashing with a timeout error. Here's the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this.",
          }
      ],
      tools=[{"type": "memory_20250818", "name": "memory"}],
  )

  print(message)
  ````

  ````typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const message = await anthropic.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content:
          "I'm working on a Python web scraper that keeps crashing with a timeout error. Here's the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this."
      }
    ],
    tools: [{ type: "memory_20250818", name: "memory" }]
  });

  console.log(message);
  ````

  ````csharp C#
  using System;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  public class Program
  {
      public static async Task Main(string[] args)
      {
          AnthropicClient client = new()
          {
              ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
          };

          var parameters = new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 2048,
              Messages = [
                  new()
                  {
                      Role = Role.User,
                      Content = "I'm working on a Python web scraper that keeps crashing with a timeout error. Here's the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this."
                  }
              ],
              Tools = [new ToolUnion(new MemoryTool20250818())]
          };

          var message = await client.Messages.Create(parameters);
          Console.WriteLine(message);
      }
  }
  ````

  ````go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 2048,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("I'm working on a Python web scraper that keeps crashing with a timeout error. Here's the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this.")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfMemoryTool20250818: &anthropic.BetaMemoryTool20250818Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ````

  ````java Java
  import com.anthropic.models.messages.MemoryTool20250818;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(2048L)
              .addUserMessage("I'm working on a Python web scraper that keeps crashing with a timeout error. Here's the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this.")
              .addTool(MemoryTool20250818.builder().build())
              .build();

          Message response = client.messages().create(params);
          System.out.println(response);
  ````

  ````php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 2048,
      messages: [
          [
              'role' => 'user',
              'content' => "I'm working on a Python web scraper that keeps crashing with a timeout error. Here's the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this.",
          ],
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'type' => 'memory_20250818',
              'name' => 'memory',
          ],
      ],
  );
  ````

  ````ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: "I'm working on a Python web scraper that keeps crashing with a timeout error. Here's the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this."
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
  ````
</CodeGroup>

## Perintah alat

Implementasi sisi klien Anda perlu menangani perintah alat memori berikut. Meskipun spesifikasi ini menjelaskan perilaku yang direkomendasikan yang paling dikenal oleh Claude, Anda dapat memodifikasi implementasi Anda dan mengembalikan string sesuai kebutuhan untuk kasus penggunaan Anda.

### view

Menampilkan isi direktori atau isi file dengan rentang baris opsional:

```json
{
  "command": "view",
  "path": "/memories",
  "view_range": [1, 10] // Optional: view specific lines
}
```

#### Nilai yang dikembalikan

**Untuk direktori:** Kembalikan daftar yang menampilkan file dan direktori beserta ukurannya:

```text
Here're the files and directories up to 2 levels deep in {path}, excluding hidden items and node_modules:
{size}    {path}
{size}    {path}/{filename1}
{size}    {path}/{filename2}
```

* Mencantumkan file hingga kedalaman 2 level
* Menampilkan ukuran yang mudah dibaca manusia (misalnya, `5.5K`, `1.2M`)
* Mengecualikan item tersembunyi (file yang dimulai dengan `.`) dan `node_modules`
* Menggunakan karakter tab antara ukuran dan path

**Untuk file:** Kembalikan isi file dengan header dan nomor baris:

```text wrap
Here's the content of {path} with line numbers:
{line_numbers}{tab}{content}
```

Format nomor baris:

* **Lebar**: 6 karakter, rata kanan dengan padding spasi
* **Pemisah**: Karakter tab antara nomor baris dan konten
* **Pengindeksan**: Dimulai dari 1 (baris pertama adalah baris 1)
* **Batas baris**: File dengan lebih dari 999.999 baris harus mengembalikan error: `"File {path} exceeds maximum line limit of 999,999 lines."`

**Contoh output:**

```text
Here's the content of /memories/notes.txt with line numbers:
     1	Hello World
     2	This is line two
    10	Line ten
   100	Line one hundred
```

#### Penanganan error

* **File/direktori tidak ada**: `"The path {path} does not exist. Please provide a valid path."`

### create

Membuat file baru:

```json
{
  "command": "create",
  "path": "/memories/notes.txt",
  "file_text": "Meeting notes:\n- Discussed project timeline\n- Next steps defined\n"
}
```

#### Nilai yang dikembalikan

* **Berhasil**: `"File created successfully at: {path}"`

#### Penanganan error

* **File sudah ada**: `"Error: File {path} already exists"`

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

#### Nilai yang dikembalikan

* **Berhasil**: `"The memory file has been edited."` diikuti dengan cuplikan file yang telah diedit beserta nomor baris

#### Penanganan error

* **File tidak ada**: `"Error: The path {path} does not exist. Please provide a valid path."`
* **Teks tidak ditemukan**: ``"No replacement was performed, old_str `\{old_str}` did not appear verbatim in {path}."``
* **Teks duplikat**: Ketika `old_str` muncul beberapa kali, kembalikan: ``"No replacement was performed. Multiple occurrences of old_str `\{old_str}` in lines: {line_numbers}. Please ensure it is unique"``

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

#### Nilai yang dikembalikan

* **Berhasil**: `"The file {path} has been edited."`

#### Penanganan error

* **File tidak ada**: `"Error: The path {path} does not exist"`
* **Nomor baris tidak valid**: ``"Error: Invalid `insert_line` parameter: {insert_line}. It should be within the range of lines of the file: [0, {n_lines}]"``

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

#### Nilai yang dikembalikan

* **Berhasil**: `"Successfully deleted {path}"`

#### Penanganan error

* **File/direktori tidak ada**: `"Error: The path {path} does not exist"`

#### Penanganan direktori

Menghapus direktori dan semua isinya secara rekursif.

### rename

Mengganti nama atau memindahkan file/direktori:

```json
{
  "command": "rename",
  "old_path": "/memories/draft.txt",
  "new_path": "/memories/final.txt"
}
```

#### Nilai yang dikembalikan

* **Berhasil**: `"Successfully renamed {old_path} to {new_path}"`

#### Penanganan error

* **Sumber tidak ada**: `"Error: The path {old_path} does not exist"`
* **Tujuan sudah ada**: Kembalikan error (jangan menimpa): `"Error: The destination {new_path} already exists"`

#### Penanganan direktori

Mengganti nama direktori.

## Panduan prompting

Instruksi ini secara otomatis disertakan dalam prompt sistem ketika alat memori diaktifkan:

```text wrap
IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
MEMORY PROTOCOL:
1. Use the `view` command of your `memory` tool to check for earlier progress.
2. ... (work on the task) ...
     - As you make progress, record status / progress / thoughts etc in your memory.
ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
```

Jika Anda mengamati Claude membuat file memori yang berantakan, Anda dapat menyertakan instruksi ini:

> Note: when editing your memory folder, always try to keep its content up-to-date, coherent and organized. You can rename or delete files that are no longer relevant. Do not create new files unless necessary.

Anda juga dapat memandu apa yang Claude tulis ke memori. Misalnya: "Only write down information relevant to \<topic> in your memory system."

## Pertimbangan keamanan

Berikut adalah pertimbangan keamanan penting saat mengimplementasikan penyimpanan memori Anda:

### Informasi sensitif

Claude biasanya akan menolak untuk menuliskan informasi sensitif dalam file memori. Namun, Anda mungkin ingin mengimplementasikan validasi yang lebih ketat yang menghapus informasi yang berpotensi sensitif.

### Ukuran penyimpanan file

Pertimbangkan untuk melacak ukuran file memori dan mencegah file tumbuh terlalu besar. Pertimbangkan untuk menambahkan jumlah karakter maksimum yang dapat dikembalikan oleh perintah baca memori, dan biarkan Claude melakukan paginasi melalui konten.

### Kedaluwarsa memori

Pertimbangkan untuk membersihkan file memori secara berkala yang belum diakses dalam waktu lama.

### Perlindungan path traversal

<Warning>
  Input path berbahaya dapat mencoba mengakses file di luar direktori `/memories`. Implementasi Anda **HARUS** memvalidasi semua path untuk mencegah serangan directory traversal.
</Warning>

Pertimbangkan langkah-langkah pengamanan berikut:

* Validasi bahwa semua path dimulai dengan `/memories`
* Resolusikan path ke bentuk kanoniknya dan verifikasi bahwa path tersebut tetap berada di dalam direktori memori
* Tolak path yang berisi urutan seperti `../`, `..\\`, atau pola traversal lainnya
* Waspadai urutan traversal yang di-encode URL (`%2e%2e%2f`)
* Gunakan utilitas keamanan path bawaan bahasa pemrograman Anda (misalnya, `pathlib.Path.resolve()` dan `relative_to()` di Python)

## Penanganan error

Alat memori menggunakan pola penanganan error yang serupa dengan [alat text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool#handle-errors). Lihat bagian perintah alat individual di atas untuk pesan error dan perilaku yang terperinci. Error umum meliputi file tidak ditemukan, error izin, path tidak valid, dan kecocokan teks duplikat.

## Integrasi pengeditan konteks

Alat memori berpasangan dengan pengeditan konteks untuk mengelola percakapan yang berjalan lama. Untuk detailnya, lihat [Pengeditan konteks](/docs/id/build-with-claude/context-editing).

## Menggunakan dengan Compaction

Alat memori juga dapat dipasangkan dengan [compaction](/docs/id/build-with-claude/compaction), yang menyediakan peringkasan sisi server dari konteks percakapan yang lebih lama. Sementara pengeditan konteks menghapus hasil alat tertentu di sisi klien, compaction secara otomatis meringkas seluruh percakapan di sisi server ketika mendekati batas jendela konteks.

Untuk alur kerja agentik yang berjalan lama, pertimbangkan untuk menggunakan keduanya: compaction menjaga konteks aktif tetap terkelola tanpa pembukuan sisi klien, dan memori mempertahankan informasi penting melintasi batas compaction sehingga tidak ada hal kritis yang hilang dalam ringkasan.

## Pola pengembangan perangkat lunak multi-sesi

Untuk proyek perangkat lunak jangka panjang yang mencakup beberapa sesi agen, file memori perlu di-bootstrap secara sengaja, bukan hanya ditulis secara ad hoc saat pekerjaan berlangsung. Pola di bawah ini mengubah memori menjadi mekanisme pemulihan terstruktur, sehingga setiap sesi baru dapat melanjutkan tepat dari titik terakhir sesi sebelumnya.

### Cara kerjanya

1. **Sesi inisialisasi:** Sesi pertama menyiapkan artefak memori sebelum pekerjaan substantif apa pun dimulai. Ini mencakup log kemajuan (melacak apa yang telah dilakukan dan apa yang akan dilakukan selanjutnya), daftar periksa fitur (mendefinisikan cakupan pekerjaan), dan referensi ke skrip startup atau inisialisasi apa pun yang dibutuhkan proyek.

2. **Sesi berikutnya:** Setiap sesi baru dimulai dengan membaca artefak memori tersebut. Ini memulihkan keadaan penuh proyek dalam hitungan detik, tanpa perlu menjelajahi ulang basis kode atau menelusuri kembali keputusan sebelumnya.

3. **Pembaruan akhir sesi:** Sebelum sesi berakhir, sesi tersebut memperbarui log kemajuan dengan apa yang telah diselesaikan dan apa yang tersisa. Ini memastikan sesi berikutnya memiliki titik awal yang akurat.

### Prinsip utama

Kerjakan satu fitur pada satu waktu. Hanya tandai fitur sebagai selesai setelah verifikasi end-to-end mengonfirmasi bahwa fitur tersebut berfungsi, bukan hanya setelah kode ditulis. Ini menjaga log kemajuan tetap dapat dipercaya dan mencegah scope creep menumpuk di seluruh sesi.

<Tip>
  Untuk studi kasus terperinci tentang pola ini dalam praktik, termasuk skrip inisialisasi, struktur file kemajuan, dan pemulihan berbasis git, lihat [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
</Tip>

## Langkah selanjutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Lihat semua alat">
    Direktori alat yang disediakan Anthropic dan propertinya.
  </Card>

  <Card href="/docs/id/build-with-claude/context-editing" title="Pengeditan konteks">
    Kelola panjang percakapan bersama dengan memori.
  </Card>
</CardGroup>
