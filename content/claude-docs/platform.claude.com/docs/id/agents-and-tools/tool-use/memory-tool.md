---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 1da44a86bc9ebce827826dd36d2c7336a982abb14a0643182ea017ccdbcac1ef
---

# Alat memori

Alat memori memungkinkan Claude menyimpan dan mengambil informasi di seluruh percakapan melalui direktori file memori.

---

Alat memori memungkinkan Claude menyimpan dan mengambil informasi di seluruh percakapan melalui direktori file memori. Claude dapat membuat, membaca, memperbarui, dan menghapus file yang bertahan di antara sesi, memungkinkannya membangun pengetahuan seiring waktu tanpa menyimpan semuanya di jendela konteks.

Ini adalah primitif kunci untuk pengambilan konteks just-in-time: daripada memuat semua informasi yang relevan di awal, agen menyimpan apa yang mereka pelajari dalam memori dan menariknya kembali sesuai permintaan. Ini membuat konteks aktif tetap fokus pada apa yang saat ini relevan, penting untuk alur kerja jangka panjang di mana memuat semuanya sekaligus akan membanjiri jendela konteks. Lihat [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) untuk pola yang lebih luas.

Alat memori beroperasi di sisi klien: Anda mengontrol di mana dan bagaimana data disimpan melalui infrastruktur Anda sendiri.

<Note>
Hubungi kami melalui [formulir umpan balik](https://forms.gle/YXC2EKGMhjN1c4L88) untuk berbagi umpan balik Anda tentang fitur ini.
</Note>

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

## Kasus penggunaan

- Pertahankan konteks proyek di seluruh eksekusi agen yang berbeda
- Pelajari dari interaksi, keputusan, dan umpan balik masa lalu
- Bangun basis pengetahuan seiring waktu
- Aktifkan pembelajaran lintas percakapan di mana Claude meningkat dalam alur kerja berulang

## Cara kerjanya

Ketika diaktifkan, Claude secara otomatis memeriksa direktori memorinya sebelum memulai tugas. Claude dapat membuat, membaca, memperbarui, dan menghapus file di direktori `/memories` untuk menyimpan apa yang dipelajarinya saat bekerja, kemudian mereferensikan memori tersebut dalam percakapan mendatang untuk menangani tugas serupa dengan lebih efektif atau melanjutkan dari mana ia berhenti.

Karena ini adalah alat sisi klien, Claude membuat panggilan alat untuk melakukan operasi memori, dan aplikasi Anda menjalankan operasi tersebut secara lokal. Ini memberi Anda kontrol penuh atas di mana dan bagaimana memori disimpan. Untuk keamanan, Anda harus membatasi semua operasi memori ke direktori `/memories`.

### Contoh: Cara kerja panggilan alat memori

Ketika Anda meminta Claude membantu dengan tugas, Claude secara otomatis memeriksa direktori memorinya terlebih dahulu. Berikut adalah apa yang terlihat seperti interaksi khas:

**1. Permintaan pengguna:**
```text
"Bantu saya merespons tiket layanan pelanggan ini."
```

**2. Claude memeriksa direktori memori:**
```text
"Saya akan membantu Anda merespons tiket layanan pelanggan. Biarkan saya memeriksa memori saya untuk konteks sebelumnya."
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
  "content": "Berikut adalah file dan direktori hingga 2 level dalam /memories, tidak termasuk item tersembunyi dan node_modules:\n4.0K\t/memories\n1.5K\t/memories/customer_service_guidelines.xml\n2.0K\t/memories/refund_policies.xml"
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
  "content": "Berikut adalah isi /memories/customer_service_guidelines.xml dengan nomor baris:\n     1\t<guidelines>\n     2\t<addressing_customers>\n     3\t- Selalu panggil pelanggan dengan nama depan mereka\n     4\t- Gunakan bahasa yang empatik\n..."
}
```

**6. Claude menggunakan memori untuk membantu:**
```text
"Berdasarkan pedoman layanan pelanggan Anda, saya dapat membantu Anda menyusun respons. Silakan bagikan detail tiket..."
```

Untuk dukungan model, lihat [Referensi Alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Memulai

Untuk menggunakan alat memori:

1. Tambahkan alat memori ke permintaan Anda
2. Implementasikan penanganan sisi klien untuk operasi memori

<Note>
Untuk menangani operasi alat memori di aplikasi Anda, Anda perlu mengimplementasikan penanganan untuk setiap perintah memori. SDK menyediakan pembantu alat memori yang menangani antarmuka alat. Anda dapat membuat subkelas `BetaAbstractMemoryTool` (Python) atau menggunakan `betaMemoryTool` (TypeScript) untuk mengimplementasikan backend memori Anda sendiri (berbasis file, database, penyimpanan cloud, file terenkripsi, dll.).

Untuk contoh kerja, lihat:
- Python: [examples/memory/basic.py](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/memory/basic.py)
- TypeScript: [examples/tools-helpers-memory.ts](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/examples/tools-helpers-memory.ts)
</Note>

## Penggunaan dasar

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-7",
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
```

````bash CLI
ant messages create <<'YAML'
model: claude-opus-4-7
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

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-7",
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
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const message = await anthropic.messages.create({
  model: "claude-opus-4-7",
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
```

```csharp C#
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
            Model = Model.ClaudeOpus4_7,
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
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
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
}
```

```java Java hidelines={1..2,4..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MemoryTool20250818;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class MemoryToolExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(2048L)
            .addUserMessage("I'm working on a Python web scraper that keeps crashing with a timeout error. Here's the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this.")
            .addTool(MemoryTool20250818.builder().build())
            .build();

        Message response = client.messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 2048,
    messages: [
        [
            'role' => 'user',
            'content' => "I'm working on a Python web scraper that keeps crashing with a timeout error. Here's the problematic function:\n\n```python\ndef fetch_page(url, retries=3):\n    for i in range(retries):\n        try:\n            response = requests.get(url, timeout=5)\n            return response.text\n        except requests.exceptions.Timeout:\n            if i == retries - 1:\n                raise\n            time.sleep(1)\n```\n\nPlease help me debug this.",
        ],
    ],
    model: 'claude-opus-4-7',
    tools: [
        [
            'type' => 'memory_20250818',
            'name' => 'memory',
        ],
    ],
);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
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
```

</CodeGroup>

## Perintah alat

Implementasi sisi klien Anda perlu menangani perintah alat memori ini. Meskipun spesifikasi ini menjelaskan perilaku yang direkomendasikan yang paling akrab dengan Claude, Anda dapat memodifikasi implementasi Anda dan mengembalikan string sesuai kebutuhan untuk kasus penggunaan Anda.

### view
Menampilkan isi direktori atau isi file dengan rentang baris opsional:

```json
{
  "command": "view",
  "path": "/memories",
  "view_range": [1, 10] // Opsional: lihat baris tertentu
}
```

#### Nilai pengembalian

**Untuk direktori:** Kembalikan daftar yang menunjukkan file dan direktori dengan ukurannya:
```text
Berikut adalah file dan direktori hingga 2 level dalam {path}, tidak termasuk item tersembunyi dan node_modules:
{size}    {path}
{size}    {path}/{filename1}
{size}    {path}/{filename2}
```

- Daftar file hingga 2 level dalam
- Tampilkan ukuran yang dapat dibaca manusia (misalnya, `5.5K`, `1.2M`)
- Kecualikan item tersembunyi (file yang dimulai dengan `.`) dan `node_modules`
- Gunakan karakter tab antara ukuran dan path

**Untuk file:** Kembalikan isi file dengan header dan nomor baris:
```text
Berikut adalah isi {path} dengan nomor baris:
{line_numbers}{tab}{content}
```

Format nomor baris:
- **Lebar**: 6 karakter, rata kanan dengan padding spasi
- **Pemisah**: Karakter tab antara nomor baris dan konten
- **Pengindeksan**: 1-indexed (baris pertama adalah baris 1)
- **Batas baris**: File dengan lebih dari 999.999 baris harus mengembalikan kesalahan: `"File {path} exceeds maximum line limit of 999,999 lines."`

**Contoh output:**
```text
Berikut adalah isi /memories/notes.txt dengan nomor baris:
     1	Hello World
     2	This is line two
    10	Line ten
   100	Line one hundred
```

#### Penanganan kesalahan

- **File/direktori tidak ada**: `"The path {path} does not exist. Please provide a valid path."`

### create
Buat file baru:

```json
{
  "command": "create",
  "path": "/memories/notes.txt",
  "file_text": "Meeting notes:\n- Discussed project timeline\n- Next steps defined\n"
}
```

#### Nilai pengembalian

- **Sukses**: `"File created successfully at: {path}"`

#### Penanganan kesalahan

- **File sudah ada**: `"Error: File {path} already exists"`

### str_replace
Ganti teks dalam file:

```json
{
  "command": "str_replace",
  "path": "/memories/preferences.txt",
  "old_str": "Favorite color: blue",
  "new_str": "Favorite color: green"
}
```

#### Nilai pengembalian

- **Sukses**: `"The memory file has been edited."` diikuti dengan cuplikan file yang diedit dengan nomor baris

#### Penanganan kesalahan

- **File tidak ada**: `"Error: The path {path} does not exist. Please provide a valid path."`
- **Teks tidak ditemukan**: ``"No replacement was performed, old_str `{old_str}` did not appear verbatim in {path}."``
- **Teks duplikat**: Ketika `old_str` muncul beberapa kali, kembalikan: ``"No replacement was performed. Multiple occurrences of old_str `{old_str}` in lines: {line_numbers}. Please ensure it is unique"``

#### Penanganan direktori

Jika path adalah direktori, kembalikan kesalahan "file tidak ada".

### insert
Sisipkan teks pada baris tertentu:

```json
{
  "command": "insert",
  "path": "/memories/todo.txt",
  "insert_line": 2,
  "insert_text": "- Review memory tool documentation\n"
}
```

#### Nilai pengembalian

- **Sukses**: `"The file {path} has been edited."`

#### Penanganan kesalahan

- **File tidak ada**: `"Error: The path {path} does not exist"`
- **Nomor baris tidak valid**: ``"Error: Invalid `insert_line` parameter: {insert_line}. It should be within the range of lines of the file: [0, {n_lines}]"``

#### Penanganan direktori

Jika path adalah direktori, kembalikan kesalahan "file tidak ada".

### delete
Hapus file atau direktori:

```json
{
  "command": "delete",
  "path": "/memories/old_file.txt"
}
```

#### Nilai pengembalian

- **Sukses**: `"Successfully deleted {path}"`

#### Penanganan kesalahan

- **File/direktori tidak ada**: `"Error: The path {path} does not exist"`

#### Penanganan direktori

Menghapus direktori dan semua isinya secara rekursif.

### rename
Ubah nama atau pindahkan file/direktori:

```json
{
  "command": "rename",
  "old_path": "/memories/draft.txt",
  "new_path": "/memories/final.txt"
}
```

#### Nilai pengembalian

- **Sukses**: `"Successfully renamed {old_path} to {new_path}"`

#### Penanganan kesalahan

- **Sumber tidak ada**: `"Error: The path {old_path} does not exist"`
- **Tujuan sudah ada**: Kembalikan kesalahan (jangan timpa): `"Error: The destination {new_path} already exists"`

#### Penanganan direktori

Mengubah nama direktori.

## Panduan prompting

Instruksi ini secara otomatis disertakan dalam prompt sistem ketika alat memori diaktifkan:

```text
IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
MEMORY PROTOCOL:
1. Use the `view` command of your `memory` tool to check for earlier progress.
2. ... (work on the task) ...
     - As you make progress, record status / progress / thoughts etc in your memory.
ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
```

Jika Anda mengamati Claude membuat file memori yang berantakan, Anda dapat menyertakan instruksi ini:

> Catatan: saat mengedit folder memori Anda, selalu coba jaga kontennya tetap terkini, koheren, dan terorganisir. Anda dapat mengubah nama atau menghapus file yang tidak lagi relevan. Jangan buat file baru kecuali diperlukan.

Anda juga dapat memandu apa yang Claude tulis ke memori. Misalnya: "Hanya tulis informasi yang relevan dengan \<topic\> dalam sistem memori Anda."

## Pertimbangan keamanan

Berikut adalah kekhawatiran keamanan penting saat mengimplementasikan penyimpanan memori Anda:

### Informasi sensitif
Claude biasanya akan menolak untuk menulis informasi sensitif dalam file memori. Namun, Anda mungkin ingin mengimplementasikan validasi yang lebih ketat yang menghilangkan informasi yang berpotensi sensitif.

### Ukuran penyimpanan file
Pertimbangkan pelacakan ukuran file memori dan mencegah file tumbuh terlalu besar. Pertimbangkan menambahkan jumlah karakter maksimum yang dapat dikembalikan perintah baca memori, dan biarkan Claude membuka halaman melalui konten.

### Kedaluwarsa memori
Pertimbangkan untuk menghapus file memori secara berkala yang belum diakses dalam waktu yang lama.

### Perlindungan traversal path

<Warning>
Input path yang berbahaya dapat mencoba mengakses file di luar direktori `/memories`. Implementasi Anda **HARUS** memvalidasi semua path untuk mencegah serangan traversal direktori.
</Warning>

Pertimbangkan perlindungan ini:

- Validasi bahwa semua path dimulai dengan `/memories`
- Selesaikan path ke bentuk kanonik mereka dan verifikasi mereka tetap berada dalam direktori memori
- Tolak path yang berisi urutan seperti `../`, `..\\`, atau pola traversal lainnya
- Perhatikan urutan traversal yang dikodekan URL (`%2e%2e%2f`)
- Gunakan utilitas keamanan path bawaan bahasa Anda (misalnya, `pathlib.Path.resolve()` dan `relative_to()` Python)

## Penanganan kesalahan

Alat memori menggunakan pola penanganan kesalahan yang serupa dengan [alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool#handle-errors). Lihat bagian perintah alat individual di atas untuk pesan kesalahan terperinci dan perilaku. Kesalahan umum termasuk file tidak ditemukan, kesalahan izin, path tidak valid, dan kecocokan teks duplikat.

## Integrasi pengeditan konteks

Alat memori berpasangan dengan pengeditan konteks untuk mengelola percakapan jangka panjang. Untuk detail, lihat [Pengeditan konteks](/docs/id/build-with-claude/context-editing).

## Menggunakan dengan Compaction

Alat memori juga dapat dipasangkan dengan [compaction](/docs/id/build-with-claude/compaction), yang menyediakan ringkasan konteks percakapan sisi server. Sementara pengeditan konteks menghapus hasil alat tertentu di sisi klien, compaction secara otomatis merangkum seluruh percakapan di sisi server ketika mendekati batas jendela konteks.

Untuk alur kerja agentic jangka panjang, pertimbangkan menggunakan keduanya: compaction membuat konteks aktif dapat dikelola tanpa pembukuan sisi klien, dan memori bertahan informasi penting di seluruh batas compaction sehingga tidak ada yang kritis hilang dalam ringkasan.

## Pola pengembangan perangkat lunak multi-sesi

Untuk proyek perangkat lunak jangka panjang yang mencakup beberapa sesi agen, file memori perlu di-bootstrap dengan sengaja, bukan hanya ditulis secara ad hoc saat pekerjaan berlangsung. Pola di bawah ini mengubah memori menjadi mekanisme pemulihan terstruktur, sehingga setiap sesi baru dapat melanjutkan tepat di mana sesi terakhir berhenti.

### Cara kerjanya

1. **Sesi initializer:** Sesi pertama menyiapkan artefak memori sebelum pekerjaan substantif dimulai. Ini termasuk log kemajuan (melacak apa yang telah dilakukan dan apa yang akan datang selanjutnya), daftar periksa fitur (mendefinisikan ruang lingkup pekerjaan), dan referensi ke skrip startup atau inisialisasi apa pun yang dibutuhkan proyek.

2. **Sesi berikutnya:** Setiap sesi baru dibuka dengan membaca artefak memori tersebut. Ini memulihkan status penuh proyek dalam hitungan detik, tanpa perlu menjelajahi ulang basis kode atau melacak ulang keputusan sebelumnya.

3. **Pembaruan akhir sesi:** Sebelum sesi berakhir, sesi memperbarui log kemajuan dengan apa yang telah diselesaikan dan apa yang tersisa. Ini memastikan sesi berikutnya memiliki titik awal yang akurat.

### Prinsip kunci

Bekerja pada satu fitur sekaligus. Hanya tandai fitur sebagai selesai setelah verifikasi end-to-end mengkonfirmasi bahwa itu berfungsi, bukan hanya setelah kode ditulis. Ini membuat log kemajuan dapat dipercaya dan mencegah scope creep dari menggabungkan di seluruh sesi.

<Tip>
Untuk studi kasus terperinci tentang pola ini dalam praktik, termasuk skrip initializer, struktur file kemajuan, dan pemulihan berbasis git, lihat [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
</Tip>

## Langkah berikutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Lihat semua alat">
    Direktori alat yang disediakan Anthropic dan propertinya.
  </Card>
  <Card href="/docs/id/build-with-claude/context-editing" title="Pengeditan konteks">
    Kelola panjang percakapan bersama memori.
  </Card>
</CardGroup>