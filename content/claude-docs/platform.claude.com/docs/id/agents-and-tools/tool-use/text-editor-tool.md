---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: dd09aabf177cad9e8bc6e99d677bfa605f1edd15070bddda10dc33959adde95f
---

# Alat editor teks

---

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Claude dapat menggunakan alat editor teks dengan skema Anthropic untuk melihat dan memodifikasi file teks, membantu Anda melakukan debug, memperbaiki, dan meningkatkan kode atau dokumen teks lainnya. Ini memungkinkan Claude untuk berinteraksi langsung dengan file Anda, memberikan bantuan langsung alih-alih hanya menyarankan perubahan.

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Kapan menggunakan alat editor teks \{#when-to-use-the-text-editor-tool}

Beberapa contoh kapan menggunakan alat editor teks adalah:
- **Debugging kode:** Minta Claude mengidentifikasi dan memperbaiki bug dalam kode Anda, mulai dari kesalahan sintaks hingga masalah logika.
- **Refactoring kode:** Biarkan Claude meningkatkan struktur, keterbacaan, dan performa kode Anda melalui pengeditan yang ditargetkan.
- **Pembuatan dokumentasi:** Minta Claude menambahkan docstring, komentar, atau file README ke basis kode Anda.
- **Pembuatan pengujian:** Minta Claude membuat unit test untuk kode Anda berdasarkan pemahamannya terhadap implementasi.

## Menggunakan alat editor teks \{#use-the-text-editor-tool}

Sediakan alat editor teks (bernama `str_replace_based_edit_tool`) kepada Claude menggunakan Messages API.

Anda dapat secara opsional menentukan parameter `max_characters` untuk mengontrol pemotongan saat melihat file berukuran besar.

<Note>
`max_characters` hanya kompatibel dengan `text_editor_20250728` dan versi alat editor teks yang lebih baru.
</Note>

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
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool",
        "max_characters": 10000
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "There'\''s a syntax error in my primes.py file. Can you help me fix it?"
      }
    ]
  }'
```

```bash CLI
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --tool '{type: text_editor_20250728, name: str_replace_based_edit_tool, max_characters: 10000}' \
  --message '{role: user, content: There is a syntax error in my primes.py file. Can you help me fix it?}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[
        {
            "type": "text_editor_20250728",
            "name": "str_replace_based_edit_tool",
            "max_characters": 10000,
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "There's a syntax error in my primes.py file. Can you help me fix it?",
        }
    ],
)

print(response)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const response = await anthropic.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool",
      max_characters: 10000
    }
  ],
  messages: [
    {
      role: "user",
      content: "There's a syntax error in my primes.py file. Can you help me fix it?"
    }
  ]
});

console.log(response);
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

var client = new AnthropicClient();

var response = await client.Messages.Create(
    new()
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Tools = [new ToolTextEditor20250728 { MaxCharacters = 10000 }],
        Messages =
        [
            new()
            {
                Role = Role.User,
                Content = "There's a syntax error in my primes.py file. Can you help me fix it?",
            },
        ],
    }
);

Console.WriteLine(response);
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Tools: []anthropic.ToolUnionParam{
			{OfTextEditor20250728: &anthropic.ToolTextEditor20250728Param{
				MaxCharacters: anthropic.Int(10000),
			}},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("There's a syntax error in my primes.py file. Can you help me fix it?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..5,7..8,-1..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.ToolTextEditor20250728;

void main() {
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  ToolTextEditor20250728 editorTool =
    ToolTextEditor20250728.builder()
      .maxCharacters(10000L)
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .maxTokens(1024)
    .addTool(editorTool)
    .addUserMessage("There's a syntax error in my primes.py file. Can you help me fix it?")
    .build();

  Message message = client.messages().create(params);
  IO.println(message);
}
```

```php PHP hidelines={1..5}
<?php

use Anthropic\Client;
use Anthropic\Messages\ToolTextEditor20250728;

$client = new Client();

$response = $client->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 1024,
    tools: [ToolTextEditor20250728::with(maxCharacters: 10000)],
    messages: [
        [
            'role' => 'user',
            'content' => "There's a syntax error in my primes.py file. Can you help me fix it?",
        ],
    ],
);

echo $response;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool",
      max_characters: 10000
    }
  ],
  messages: [
    {
      role: "user",
      content: "There's a syntax error in my primes.py file. Can you help me fix it?"
    }
  ]
)

puts response
```
</CodeGroup>

Alat editor teks dapat digunakan dengan cara berikut:

<Steps>
  <Step title="Sediakan alat editor teks dan prompt pengguna kepada Claude">
    - Sertakan alat editor teks dalam permintaan API Anda
    - Sediakan prompt pengguna yang mungkin memerlukan pemeriksaan atau modifikasi file, seperti "Bisakah Anda memperbaiki kesalahan sintaks dalam kode saya?"
  </Step>
  <Step title="Claude menggunakan alat untuk memeriksa file atau direktori">
    - Claude menilai apa yang perlu dilihatnya dan menggunakan perintah `view` untuk memeriksa isi file atau menampilkan daftar isi direktori
    - Respons API akan berisi blok konten `tool_use` dengan perintah `view`
  </Step>
  <Step title="Jalankan perintah view dan kembalikan hasilnya">
    - Ekstrak path file atau direktori dari permintaan penggunaan alat Claude
    - Baca isi file atau tampilkan daftar isi direktori
    - Jika parameter `max_characters` ditentukan dalam konfigurasi alat, potong isi file hingga panjang tersebut
    - Kembalikan hasilnya kepada Claude dengan melanjutkan percakapan menggunakan pesan `user` baru yang berisi blok konten `tool_result`
  </Step>
  <Step title="Claude menggunakan alat untuk memodifikasi file">
    - Setelah memeriksa file atau direktori, Claude mungkin menggunakan perintah seperti `str_replace` untuk membuat perubahan atau `insert` untuk menambahkan teks pada nomor baris tertentu.
    - Jika Claude menggunakan perintah `str_replace`, Claude menyusun permintaan penggunaan alat yang diformat dengan benar berisi teks lama dan teks baru untuk menggantikannya
  </Step>
  <Step title="Jalankan pengeditan dan kembalikan hasilnya">
    - Ekstrak path file, teks lama, dan teks baru dari permintaan penggunaan alat Claude
    - Lakukan penggantian teks dalam file
    - Kembalikan hasilnya kepada Claude
  </Step>
  <Step title="Claude memberikan analisis dan penjelasannya">
    - Setelah memeriksa dan mungkin mengedit file, Claude memberikan penjelasan lengkap tentang apa yang ditemukannya dan perubahan apa yang dibuatnya
  </Step>
</Steps>

### Perintah alat editor teks \{#text-editor-tool-commands}

Alat editor teks mendukung beberapa perintah untuk melihat dan memodifikasi file:

#### view \{#view}

Perintah `view` memungkinkan Claude untuk memeriksa isi file atau menampilkan daftar isi direktori. Perintah ini dapat membaca seluruh file atau rentang baris tertentu.

Parameter:
- `command`: Harus bernilai "view"
- `path`: Path ke file atau direktori yang akan dilihat
- `view_range` (opsional): Array berisi dua bilangan bulat yang menentukan nomor baris awal dan akhir yang akan dilihat. Nomor baris dimulai dari 1, dan -1 untuk baris akhir berarti membaca hingga akhir file. Parameter ini hanya berlaku saat melihat file, bukan direktori.

<section title="Contoh perintah view">

Contoh untuk melihat file:

```json
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "str_replace_based_edit_tool",
  "input": {
    "command": "view",
    "path": "primes.py"
  }
}
```

Contoh untuk melihat direktori:

```json
{
  "type": "tool_use",
  "id": "toolu_02B19r91rw91mr917835mr9",
  "name": "str_replace_based_edit_tool",
  "input": {
    "command": "view",
    "path": "src/"
  }
}
```

</section>

#### str_replace \{#str-replace}

Perintah `str_replace` memungkinkan Claude untuk mengganti string tertentu dalam file dengan string baru. Ini digunakan untuk membuat pengeditan yang presisi.

Parameter:
- `command`: Harus bernilai "str_replace"
- `path`: Path ke file yang akan dimodifikasi
- `old_str`: Teks yang akan diganti (harus cocok persis, termasuk spasi dan indentasi)
- `new_str`: Teks baru yang akan disisipkan menggantikan teks lama

<section title="Contoh perintah str_replace">

```json
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "str_replace_based_edit_tool",
  "input": {
    "command": "str_replace",
    "path": "primes.py",
    "old_str": "for num in range(2, limit + 1)",
    "new_str": "for num in range(2, limit + 1):"
  }
}
```

</section>

#### create \{#create}

Perintah `create` memungkinkan Claude untuk membuat file baru dengan konten yang ditentukan.

Parameter:
- `command`: Harus bernilai "create"
- `path`: Path tempat file baru akan dibuat
- `file_text`: Konten yang akan ditulis ke file baru

<section title="Contoh perintah create">

```json
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "str_replace_based_edit_tool",
  "input": {
    "command": "create",
    "path": "test_primes.py",
    "file_text": "import unittest\nimport primes\n\nclass TestPrimes(unittest.TestCase):\n    def test_is_prime(self):\n        self.assertTrue(primes.is_prime(2))\n        self.assertTrue(primes.is_prime(3))\n        self.assertFalse(primes.is_prime(4))\n\nif __name__ == '__main__':\n    unittest.main()"
  }
}
```

</section>

#### insert \{#insert}

Perintah `insert` memungkinkan Claude untuk menyisipkan teks pada lokasi tertentu dalam file.

Parameter:
- `command`: Harus bernilai "insert"
- `path`: Path ke file yang akan dimodifikasi
- `insert_line`: Nomor baris setelahnya teks akan disisipkan (0 untuk awal file)
- `insert_text`: Teks yang akan disisipkan

<section title="Contoh perintah insert">

```json
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "str_replace_based_edit_tool",
  "input": {
    "command": "insert",
    "path": "primes.py",
    "insert_line": 0,
    "insert_text": "\"\"\"Module for working with prime numbers.\n\nThis module provides functions to check if a number is prime\nand to generate a list of prime numbers up to a given limit.\n\"\"\"\n"
  }
}
```

</section>

### Contoh: Memperbaiki kesalahan sintaks dengan alat editor teks \{#example-fixing-a-syntax-error-with-the-text-editor-tool}

Contoh ini mendemonstrasikan bagaimana Claude menggunakan alat editor teks untuk memperbaiki kesalahan sintaks dalam file Python.

Pertama, aplikasi Anda menyediakan alat editor teks dan prompt untuk memperbaiki kesalahan sintaks kepada Claude:

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
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool"
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "There'\''s a syntax error in my primes.py file. Can you help me fix it?"
      }
    ]
  }'
```

```bash CLI
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --tool '{type: text_editor_20250728, name: str_replace_based_edit_tool}' \
  --message '{role: user, content: There is a syntax error in my primes.py file. Can you help me fix it?}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}],
    messages=[
        {
            "role": "user",
            "content": "There's a syntax error in my primes.py file. Can you help me fix it?",
        }
    ],
)

print(response)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const response = await anthropic.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool"
    }
  ],
  messages: [
    {
      role: "user",
      content: "There's a syntax error in my primes.py file. Can you help me fix it?"
    }
  ]
});

console.log(response);
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

var client = new AnthropicClient();

var response = await client.Messages.Create(
    new()
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Tools = [new ToolTextEditor20250728()],
        Messages =
        [
            new()
            {
                Role = Role.User,
                Content = "There's a syntax error in my primes.py file. Can you help me fix it?",
            },
        ],
    }
);

Console.WriteLine(response);
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Tools: []anthropic.ToolUnionParam{
			{OfTextEditor20250728: &anthropic.ToolTextEditor20250728Param{}},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("There's a syntax error in my primes.py file. Can you help me fix it?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..5,7..8,-1..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.ToolTextEditor20250728;

void main() {
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  ToolTextEditor20250728 editorTool =
    ToolTextEditor20250728.builder().build();

  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .maxTokens(1024)
    .addTool(editorTool)
    .addUserMessage("There's a syntax error in my primes.py file. Can you help me fix it?")
    .build();

  Message message = client.messages().create(params);
  IO.println(message);
}
```

```php PHP hidelines={1..5}
<?php

use Anthropic\Client;
use Anthropic\Messages\ToolTextEditor20250728;

$client = new Client();

$response = $client->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 1024,
    tools: [new ToolTextEditor20250728()],
    messages: [
        [
            'role' => 'user',
            'content' => "There's a syntax error in my primes.py file. Can you help me fix it?",
        ],
    ],
);

echo $response;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [{type: "text_editor_20250728", name: "str_replace_based_edit_tool"}],
  messages: [
    {
      role: "user",
      content: "There's a syntax error in my primes.py file. Can you help me fix it?"
    }
  ]
)

puts response
```
</CodeGroup>

Claude menggunakan alat editor teks terlebih dahulu untuk melihat file:

```json Output
{
  "id": "msg_01XAbCDeFgHiJkLmNoPQrStU",
  "model": "claude-opus-4-8",
  "stop_reason": "tool_use",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll help you fix the syntax error in your primes.py file. First, let me take a look at the file to identify the issue."
    },
    {
      "type": "tool_use",
      "id": "toolu_01AbCdEfGhIjKlMnOpQrStU",
      "name": "str_replace_based_edit_tool",
      "input": {
        "command": "view",
        "path": "primes.py"
      }
    }
  ]
}
```

Aplikasi Anda kemudian harus membaca file dan mengembalikan isinya kepada Claude:

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
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool"
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "There'\''s a syntax error in my primes.py file. Can you help me fix it?"
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "I'\''ll help you fix the syntax error in your primes.py file. First, let me take a look at the file to identify the issue."
          },
          {
            "type": "tool_use",
            "id": "toolu_01AbCdEfGhIjKlMnOpQrStU",
            "name": "str_replace_based_edit_tool",
            "input": {
              "command": "view",
              "path": "primes.py"
            }
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "tool_result",
            "tool_use_id": "toolu_01AbCdEfGhIjKlMnOpQrStU",
            "content": "1: def is_prime(n):\n2:     \"\"\"Check if a number is prime.\"\"\"\n3:     if n <= 1:\n4:         return False\n5:     if n <= 3:\n6:         return True\n7:     if n % 2 == 0 or n % 3 == 0:\n8:         return False\n9:     i = 5\n10:     while i * i <= n:\n11:         if n % i == 0 or n % (i + 2) == 0:\n12:             return False\n13:         i += 6\n14:     return True\n15: \n16: def get_primes(limit):\n17:     \"\"\"Generate a list of prime numbers up to the given limit.\"\"\"\n18:     primes = []\n19:     for num in range(2, limit + 1)\n20:         if is_prime(num):\n21:             primes.append(num)\n22:     return primes\n23: \n24: def main():\n25:     \"\"\"Main function to demonstrate prime number generation.\"\"\"\n26:     limit = 100\n27:     prime_list = get_primes(limit)\n28:     print(f\"Prime numbers up to {limit}:\")\n29:     print(prime_list)\n30:     print(f\"Found {len(prime_list)} prime numbers.\")\n31: \n32: if __name__ == \"__main__\":\n33:     main()"
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
  - type: text_editor_20250728
    name: str_replace_based_edit_tool
messages:
  - role: user
    content: There's a syntax error in my primes.py file. Can you help me fix it?
  - role: assistant
    content:
      - type: text
        text: >-
          I'll help you fix the syntax error in your primes.py file. First,
          let me take a look at the file to identify the issue.
      - type: tool_use
        id: toolu_01AbCdEfGhIjKlMnOpQrStU
        name: str_replace_based_edit_tool
        input:
          command: view
          path: primes.py
  - role: user
    content:
      - type: tool_result
        tool_use_id: toolu_01AbCdEfGhIjKlMnOpQrStU
        content: |-
          1: def is_prime(n):
          2:     """Check if a number is prime."""
          3:     if n <= 1:
          4:         return False
          5:     if n <= 3:
          6:         return True
          7:     if n % 2 == 0 or n % 3 == 0:
          8:         return False
          9:     i = 5
          10:     while i * i <= n:
          11:         if n % i == 0 or n % (i + 2) == 0:
          12:             return False
          13:         i += 6
          14:     return True
          15:
          16: def get_primes(limit):
          17:     """Generate a list of prime numbers up to the given limit."""
          18:     primes = []
          19:     for num in range(2, limit + 1)
          20:         if is_prime(num):
          21:             primes.append(num)
          22:     return primes
          23:
          24: def main():
          25:     """Main function to demonstrate prime number generation."""
          26:     limit = 100
          27:     prime_list = get_primes(limit)
          28:     print(f"Prime numbers up to {limit}:")
          29:     print(prime_list)
          30:     print(f"Found {len(prime_list)} prime numbers.")
          31:
          32: if __name__ == "__main__":
          33:     main()
YAML
```

```python Python
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}],
    messages=[
        {
            "role": "user",
            "content": "There's a syntax error in my primes.py file. Can you help me fix it?",
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I'll help you fix the syntax error in your primes.py file. First, let me take a look at the file to identify the issue.",
                },
                {
                    "type": "tool_use",
                    "id": "toolu_01AbCdEfGhIjKlMnOpQrStU",
                    "name": "str_replace_based_edit_tool",
                    "input": {"command": "view", "path": "primes.py"},
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_01AbCdEfGhIjKlMnOpQrStU",
                    "content": '1: def is_prime(n):\n2:     """Check if a number is prime."""\n3:     if n <= 1:\n4:         return False\n5:     if n <= 3:\n6:         return True\n7:     if n % 2 == 0 or n % 3 == 0:\n8:         return False\n9:     i = 5\n10:     while i * i <= n:\n11:         if n % i == 0 or n % (i + 2) == 0:\n12:             return False\n13:         i += 6\n14:     return True\n15: \n16: def get_primes(limit):\n17:     """Generate a list of prime numbers up to the given limit."""\n18:     primes = []\n19:     for num in range(2, limit + 1)\n20:         if is_prime(num):\n21:             primes.append(num)\n22:     return primes\n23: \n24: def main():\n25:     """Main function to demonstrate prime number generation."""\n26:     limit = 100\n27:     prime_list = get_primes(limit)\n28:     print(f"Prime numbers up to {limit}:")\n29:     print(prime_list)\n30:     print(f"Found {len(prime_list)} prime numbers.")\n31: \n32: if __name__ == "__main__":\n33:     main()',
                }
            ],
        },
    ],
)

print(response)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const response = await anthropic.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool"
    }
  ],
  messages: [
    {
      role: "user",
      content: "There's a syntax error in my primes.py file. Can you help me fix it?"
    },
    {
      role: "assistant",
      content: [
        {
          type: "text",
          text: "I'll help you fix the syntax error in your primes.py file. First, let me take a look at the file to identify the issue."
        },
        {
          type: "tool_use",
          id: "toolu_01AbCdEfGhIjKlMnOpQrStU",
          name: "str_replace_based_edit_tool",
          input: {
            command: "view",
            path: "primes.py"
          }
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: "toolu_01AbCdEfGhIjKlMnOpQrStU",
          content:
            '1: def is_prime(n):\n2:     """Check if a number is prime."""\n3:     if n <= 1:\n4:         return False\n5:     if n <= 3:\n6:         return True\n7:     if n % 2 == 0 or n % 3 == 0:\n8:         return False\n9:     i = 5\n10:     while i * i <= n:\n11:         if n % i == 0 or n % (i + 2) == 0:\n12:             return False\n13:         i += 6\n14:     return True\n15: \n16: def get_primes(limit):\n17:     """Generate a list of prime numbers up to the given limit."""\n18:     primes = []\n19:     for num in range(2, limit + 1)\n20:         if is_prime(num):\n21:             primes.append(num)\n22:     return primes\n23: \n24: def main():\n25:     """Main function to demonstrate prime number generation."""\n26:     limit = 100\n27:     prime_list = get_primes(limit)\n28:     print(f"Prime numbers up to {limit}:")\n29:     print(prime_list)\n30:     print(f"Found {len(prime_list)} prime numbers.")\n31: \n32: if __name__ == "__main__":\n33:     main()'
        }
      ]
    }
  ]
});

console.log(response);
```

```csharp C# hidelines={1..4}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

var client = new AnthropicClient();

var response = await client.Messages.Create(
    new()
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Tools = [new ToolTextEditor20250728()],
        Messages =
        [
            new()
            {
                Role = Role.User,
                Content = "There's a syntax error in my primes.py file. Can you help me fix it?",
            },
            new()
            {
                Role = Role.Assistant,
                Content = new MessageParamContent(new List<ContentBlockParam>
                {
                    new ContentBlockParam(new TextBlockParam()
                    {
                        Text = "I'll help you fix the syntax error in your primes.py file. First, let me take a look at the file to identify the issue.",
                    }),
                    new ContentBlockParam(new ToolUseBlockParam()
                    {
                        ID = "toolu_01AbCdEfGhIjKlMnOpQrStU",
                        Name = "str_replace_based_edit_tool",
                        Input = new Dictionary<string, JsonElement>
                        {
                            ["command"] = JsonSerializer.SerializeToElement("view"),
                            ["path"] = JsonSerializer.SerializeToElement("primes.py"),
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
                        ToolUseID = "toolu_01AbCdEfGhIjKlMnOpQrStU",
                        Content = "1: def is_prime(n):\n2:     \"\"\"Check if a number is prime.\"\"\"\n3:     if n <= 1:\n4:         return False\n5:     if n <= 3:\n6:         return True\n7:     if n % 2 == 0 or n % 3 == 0:\n8:         return False\n9:     i = 5\n10:     while i * i <= n:\n11:         if n % i == 0 or n % (i + 2) == 0:\n12:             return False\n13:         i += 6\n14:     return True\n15: \n16: def get_primes(limit):\n17:     \"\"\"Generate a list of prime numbers up to the given limit.\"\"\"\n18:     primes = []\n19:     for num in range(2, limit + 1)\n20:         if is_prime(num):\n21:             primes.append(num)\n22:     return primes\n23: \n24: def main():\n25:     \"\"\"Main function to demonstrate prime number generation.\"\"\"\n26:     limit = 100\n27:     prime_list = get_primes(limit)\n28:     print(f\"Prime numbers up to {limit}:\")\n29:     print(prime_list)\n30:     print(f\"Found {len(prime_list)} prime numbers.\")\n31: \n32: if __name__ == \"__main__\":\n33:     main()",
                    }),
                }),
            },
        ],
    }
);

Console.WriteLine(response);
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Tools: []anthropic.ToolUnionParam{
			{OfTextEditor20250728: &anthropic.ToolTextEditor20250728Param{}},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("There's a syntax error in my primes.py file. Can you help me fix it?")),
			anthropic.NewAssistantMessage(
				anthropic.NewTextBlock("I'll help you fix the syntax error in your primes.py file. First, let me take a look at the file to identify the issue."),
				anthropic.NewToolUseBlock(
					"toolu_01AbCdEfGhIjKlMnOpQrStU",
					map[string]any{"command": "view", "path": "primes.py"},
					"str_replace_based_edit_tool",
				),
			),
			anthropic.NewUserMessage(
				anthropic.NewToolResultBlock(
					"toolu_01AbCdEfGhIjKlMnOpQrStU",
					"1: def is_prime(n):\n2:     \"\"\"Check if a number is prime.\"\"\"\n3:     if n <= 1:\n4:         return False\n5:     if n <= 3:\n6:         return True\n7:     if n % 2 == 0 or n % 3 == 0:\n8:         return False\n9:     i = 5\n10:     while i * i <= n:\n11:         if n % i == 0 or n % (i + 2) == 0:\n12:             return False\n13:         i += 6\n14:     return True\n15: \n16: def get_primes(limit):\n17:     \"\"\"Generate a list of prime numbers up to the given limit.\"\"\"\n18:     primes = []\n19:     for num in range(2, limit + 1)\n20:         if is_prime(num):\n21:             primes.append(num)\n22:     return primes\n23: \n24: def main():\n25:     \"\"\"Main function to demonstrate prime number generation.\"\"\"\n26:     limit = 100\n27:     prime_list = get_primes(limit)\n28:     print(f\"Prime numbers up to {limit}:\")\n29:     print(prime_list)\n30:     print(f\"Found {len(prime_list)} prime numbers.\")\n31: \n32: if __name__ == \"__main__\":\n33:     main()",
					false,
				),
			),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..9,11..16,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolTextEditor20250728;
import com.anthropic.models.messages.ToolUseBlockParam;
import java.util.List;

public class TextEditorToolResultExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024)
      .addTool(ToolTextEditor20250728.builder().build())
      .addUserMessage("There's a syntax error in my primes.py file. Can you help me fix it?")
      .addAssistantMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofText(
            TextBlockParam.builder()
              .text("I'll help you fix the syntax error in your primes.py file. First, let me take a look at the file to identify the issue.")
              .build()
          ),
          ContentBlockParam.ofToolUse(
            ToolUseBlockParam.builder()
              .id("toolu_01AbCdEfGhIjKlMnOpQrStU")
              .name("str_replace_based_edit_tool")
              .input(
                ToolUseBlockParam.Input.builder()
                  .putAdditionalProperty("command", JsonValue.from("view"))
                  .putAdditionalProperty("path", JsonValue.from("primes.py"))
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
              .toolUseId("toolu_01AbCdEfGhIjKlMnOpQrStU")
              .content("1: def is_prime(n):\n2:     \"\"\"Check if a number is prime.\"\"\"\n3:     if n <= 1:\n4:         return False\n5:     if n <= 3:\n6:         return True\n7:     if n % 2 == 0 or n % 3 == 0:\n8:         return False\n9:     i = 5\n10:     while i * i <= n:\n11:         if n % i == 0 or n % (i + 2) == 0:\n12:             return False\n13:         i += 6\n14:     return True\n15: \n16: def get_primes(limit):\n17:     \"\"\"Generate a list of prime numbers up to the given limit.\"\"\"\n18:     primes = []\n19:     for num in range(2, limit + 1)\n20:         if is_prime(num):\n21:             primes.append(num)\n22:     return primes\n23: \n24: def main():\n25:     \"\"\"Main function to demonstrate prime number generation.\"\"\"\n26:     limit = 100\n27:     prime_list = get_primes(limit)\n28:     print(f\"Prime numbers up to {limit}:\")\n29:     print(prime_list)\n30:     print(f\"Found {len(prime_list)} prime numbers.\")\n31: \n32: if __name__ == \"__main__\":\n33:     main()")
              .build()
          )
        )
      )
      .build();

    Message message = client.messages().create(params);
    System.out.println(message);
  }
}
```

```php PHP hidelines={1..5}
<?php

use Anthropic\Client;
use Anthropic\Messages\ToolTextEditor20250728;

$client = new Client();

$response = $client->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 1024,
    tools: [new ToolTextEditor20250728()],
    messages: [
        [
            'role' => 'user',
            'content' => "There's a syntax error in my primes.py file. Can you help me fix it?",
        ],
        [
            'role' => 'assistant',
            'content' => [
                [
                    'type' => 'text',
                    'text' => "I'll help you fix the syntax error in your primes.py file. First, let me take a look at the file to identify the issue.",
                ],
                [
                    'type' => 'tool_use',
                    'id' => 'toolu_01AbCdEfGhIjKlMnOpQrStU',
                    'name' => 'str_replace_based_edit_tool',
                    'input' => ['command' => 'view', 'path' => 'primes.py'],
                ],
            ],
        ],
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'tool_result',
                    'tool_use_id' => 'toolu_01AbCdEfGhIjKlMnOpQrStU',
                    'content' => "1: def is_prime(n):\n2:     \"\"\"Check if a number is prime.\"\"\"\n3:     if n <= 1:\n4:         return False\n5:     if n <= 3:\n6:         return True\n7:     if n % 2 == 0 or n % 3 == 0:\n8:         return False\n9:     i = 5\n10:     while i * i <= n:\n11:         if n % i == 0 or n % (i + 2) == 0:\n12:             return False\n13:         i += 6\n14:     return True\n15: \n16: def get_primes(limit):\n17:     \"\"\"Generate a list of prime numbers up to the given limit.\"\"\"\n18:     primes = []\n19:     for num in range(2, limit + 1)\n20:         if is_prime(num):\n21:             primes.append(num)\n22:     return primes\n23: \n24: def main():\n25:     \"\"\"Main function to demonstrate prime number generation.\"\"\"\n26:     limit = 100\n27:     prime_list = get_primes(limit)\n28:     print(f\"Prime numbers up to {limit}:\")\n29:     print(prime_list)\n30:     print(f\"Found {len(prime_list)} prime numbers.\")\n31: \n32: if __name__ == \"__main__\":\n33:     main()",
                ],
            ],
        ],
    ],
);

echo $response;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [{type: "text_editor_20250728", name: "str_replace_based_edit_tool"}],
  messages: [
    {
      role: "user",
      content: "There's a syntax error in my primes.py file. Can you help me fix it?"
    },
    {
      role: "assistant",
      content: [
        {
          type: "text",
          text: "I'll help you fix the syntax error in your primes.py file. First, let me take a look at the file to identify the issue."
        },
        {
          type: "tool_use",
          id: "toolu_01AbCdEfGhIjKlMnOpQrStU",
          name: "str_replace_based_edit_tool",
          input: {command: "view", path: "primes.py"}
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: "toolu_01AbCdEfGhIjKlMnOpQrStU",
          content: "1: def is_prime(n):\n2:     \"\"\"Check if a number is prime.\"\"\"\n3:     if n <= 1:\n4:         return False\n5:     if n <= 3:\n6:         return True\n7:     if n % 2 == 0 or n % 3 == 0:\n8:         return False\n9:     i = 5\n10:     while i * i <= n:\n11:         if n % i == 0 or n % (i + 2) == 0:\n12:             return False\n13:         i += 6\n14:     return True\n15: \n16: def get_primes(limit):\n17:     \"\"\"Generate a list of prime numbers up to the given limit.\"\"\"\n18:     primes = []\n19:     for num in range(2, limit + 1)\n20:         if is_prime(num):\n21:             primes.append(num)\n22:     return primes\n23: \n24: def main():\n25:     \"\"\"Main function to demonstrate prime number generation.\"\"\"\n26:     limit = 100\n27:     prime_list = get_primes(limit)\n28:     print(f\"Prime numbers up to {limit}:\")\n29:     print(prime_list)\n30:     print(f\"Found {len(prime_list)} prime numbers.\")\n31: \n32: if __name__ == \"__main__\":\n33:     main()"
        }
      ]
    }
  ]
)

puts response
```
</CodeGroup>

<Tip>
**Nomor baris**

Dalam contoh di atas, hasil alat `view` menyertakan isi file dengan nomor baris yang ditambahkan di awal setiap baris (misalnya, "1: def is_prime(n):"). Nomor baris tidak wajib, tetapi sangat penting untuk berhasil menggunakan parameter `view_range` guna memeriksa bagian tertentu dari file dan parameter `insert_line` untuk menambahkan konten pada lokasi yang tepat.
</Tip>

Claude mengidentifikasi kesalahan sintaks dan menggunakan perintah `str_replace` untuk memperbaikinya:

```json Output
{
  "id": "msg_01VwXyZAbCdEfGhIjKlMnO",
  "model": "claude-opus-4-8",
  "stop_reason": "tool_use",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I found the syntax error in your primes.py file. In the `get_primes` function, there is a missing colon (:) at the end of the for loop line. Let me fix that for you."
    },
    {
      "type": "tool_use",
      "id": "toolu_01PqRsTuVwXyZAbCdEfGh",
      "name": "str_replace_based_edit_tool",
      "input": {
        "command": "str_replace",
        "path": "primes.py",
        "old_str": "    for num in range(2, limit + 1)",
        "new_str": "    for num in range(2, limit + 1):"
      }
    }
  ]
}
```

Aplikasi Anda kemudian harus melakukan pengeditan dan mengembalikan hasilnya:

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
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool"
      }
    ],
    "messages": [
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "I found the syntax error in your primes.py file. In the `get_primes` function, there is a missing colon (:) at the end of the for loop line. Let me fix that for you."
          },
          {
            "type": "tool_use",
            "id": "toolu_01PqRsTuVwXyZAbCdEfGh",
            "name": "str_replace_based_edit_tool",
            "input": {
              "command": "str_replace",
              "path": "primes.py",
              "old_str": "    for num in range(2, limit + 1)",
              "new_str": "    for num in range(2, limit + 1):"
            }
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "tool_result",
            "tool_use_id": "toolu_01PqRsTuVwXyZAbCdEfGh",
            "content": "Successfully replaced text at exactly one location."
          }
        ]
      }
    ]
  }'
```

```bash CLI nocheck
ant messages create <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
tools:
  - type: text_editor_20250728
    name: str_replace_based_edit_tool
messages:
  # Pesan-pesan sebelumnya...
  - role: assistant
    content:
      - type: text
        text: >-
          I found the syntax error in your primes.py file. In the `get_primes`
          function, there is a missing colon (:) at the end of the for loop
          line. Let me fix that for you.
      - type: tool_use
        id: toolu_01PqRsTuVwXyZAbCdEfGh
        name: str_replace_based_edit_tool
        input:
          command: str_replace
          path: primes.py
          old_str: "    for num in range(2, limit + 1)"
          new_str: "    for num in range(2, limit + 1):"
  - role: user
    content:
      - type: tool_result
        tool_use_id: toolu_01PqRsTuVwXyZAbCdEfGh
        content: Successfully replaced text at exactly one location.
YAML
```

```python Python
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}],
    messages=[
        # Pesan-pesan sebelumnya...
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I found the syntax error in your primes.py file. In the `get_primes` function, there is a missing colon (:) at the end of the for loop line. Let me fix that for you.",
                },
                {
                    "type": "tool_use",
                    "id": "toolu_01PqRsTuVwXyZAbCdEfGh",
                    "name": "str_replace_based_edit_tool",
                    "input": {
                        "command": "str_replace",
                        "path": "primes.py",
                        "old_str": "    for num in range(2, limit + 1)",
                        "new_str": "    for num in range(2, limit + 1):",
                    },
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_01PqRsTuVwXyZAbCdEfGh",
                    "content": "Successfully replaced text at exactly one location.",
                }
            ],
        },
    ],
)

print(response)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool"
    }
  ],
  messages: [
    // Pesan-pesan sebelumnya...
    {
      role: "assistant",
      content: [
        {
          type: "text",
          text: "I found the syntax error in your primes.py file. In the `get_primes` function, there is a missing colon (:) at the end of the for loop line. Let me fix that for you."
        },
        {
          type: "tool_use",
          id: "toolu_01PqRsTuVwXyZAbCdEfGh",
          name: "str_replace_based_edit_tool",
          input: {
            command: "str_replace",
            path: "primes.py",
            old_str: "    for num in range(2, limit + 1)",
            new_str: "    for num in range(2, limit + 1):"
          }
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: "toolu_01PqRsTuVwXyZAbCdEfGh",
          content: "Successfully replaced text at exactly one location."
        }
      ]
    }
  ]
});

console.log(response);
```

```csharp C# hidelines={1..4}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

var client = new AnthropicClient();

var response = await client.Messages.Create(
    new()
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Tools = [new ToolTextEditor20250728()],
        Messages =
        [
            // Pesan-pesan sebelumnya...
            new()
            {
                Role = Role.Assistant,
                Content = new MessageParamContent(new List<ContentBlockParam>
                {
                    new ContentBlockParam(new TextBlockParam()
                    {
                        Text = "I found the syntax error in your primes.py file. In the `get_primes` function, there is a missing colon (:) at the end of the for loop line. Let me fix that for you.",
                    }),
                    new ContentBlockParam(new ToolUseBlockParam()
                    {
                        ID = "toolu_01PqRsTuVwXyZAbCdEfGh",
                        Name = "str_replace_based_edit_tool",
                        Input = new Dictionary<string, JsonElement>
                        {
                            ["command"] = JsonSerializer.SerializeToElement("str_replace"),
                            ["path"] = JsonSerializer.SerializeToElement("primes.py"),
                            ["old_str"] = JsonSerializer.SerializeToElement("    for num in range(2, limit + 1)"),
                            ["new_str"] = JsonSerializer.SerializeToElement("    for num in range(2, limit + 1):"),
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
                        ToolUseID = "toolu_01PqRsTuVwXyZAbCdEfGh",
                        Content = "Successfully replaced text at exactly one location.",
                    }),
                }),
            },
        ],
    }
);

Console.WriteLine(response);
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Tools: []anthropic.ToolUnionParam{
			{OfTextEditor20250728: &anthropic.ToolTextEditor20250728Param{}},
		},
		Messages: []anthropic.MessageParam{
			// Pesan-pesan sebelumnya...
			anthropic.NewAssistantMessage(
				anthropic.NewTextBlock("I found the syntax error in your primes.py file. In the `get_primes` function, there is a missing colon (:) at the end of the for loop line. Let me fix that for you."),
				anthropic.NewToolUseBlock(
					"toolu_01PqRsTuVwXyZAbCdEfGh",
					map[string]any{
						"command": "str_replace",
						"path":    "primes.py",
						"old_str": "    for num in range(2, limit + 1)",
						"new_str": "    for num in range(2, limit + 1):",
					},
					"str_replace_based_edit_tool",
				),
			),
			anthropic.NewUserMessage(
				anthropic.NewToolResultBlock(
					"toolu_01PqRsTuVwXyZAbCdEfGh",
					"Successfully replaced text at exactly one location.",
					false,
				),
			),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..9,11..16,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolTextEditor20250728;
import com.anthropic.models.messages.ToolUseBlockParam;
import java.util.List;

public class TextEditorConversationExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024)
      .addTool(ToolTextEditor20250728.builder().build())
      // Pesan-pesan sebelumnya akan ditempatkan di sini
      .addAssistantMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofText(
            TextBlockParam.builder()
              .text(
                "I found the syntax error in your primes.py file. In the `get_primes` function, there is a missing colon (:) at the end of the for loop line. Let me fix that for you."
              )
              .build()
          ),
          ContentBlockParam.ofToolUse(
            ToolUseBlockParam.builder()
              .id("toolu_01PqRsTuVwXyZAbCdEfGh")
              .name("str_replace_based_edit_tool")
              .input(
                ToolUseBlockParam.Input.builder()
                  .putAdditionalProperty("command", JsonValue.from("str_replace"))
                  .putAdditionalProperty("path", JsonValue.from("primes.py"))
                  .putAdditionalProperty(
                    "old_str",
                    JsonValue.from("    for num in range(2, limit + 1)")
                  )
                  .putAdditionalProperty(
                    "new_str",
                    JsonValue.from("    for num in range(2, limit + 1):")
                  )
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
              .toolUseId("toolu_01PqRsTuVwXyZAbCdEfGh")
              .content("Successfully replaced text at exactly one location.")
              .build()
          )
        )
      )
      .build();

    Message message = client.messages().create(params);
    System.out.println(message);
  }
}
```

```php PHP hidelines={1..5}
<?php

use Anthropic\Client;
use Anthropic\Messages\ToolTextEditor20250728;

$client = new Client();

$response = $client->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 1024,
    tools: [new ToolTextEditor20250728()],
    messages: [
        // Pesan-pesan sebelumnya...
        [
            'role' => 'assistant',
            'content' => [
                [
                    'type' => 'text',
                    'text' => 'I found the syntax error in your primes.py file. In the `get_primes` function, there is a missing colon (:) at the end of the for loop line. Let me fix that for you.',
                ],
                [
                    'type' => 'tool_use',
                    'id' => 'toolu_01PqRsTuVwXyZAbCdEfGh',
                    'name' => 'str_replace_based_edit_tool',
                    'input' => [
                        'command' => 'str_replace',
                        'path' => 'primes.py',
                        'old_str' => '    for num in range(2, limit + 1)',
                        'new_str' => '    for num in range(2, limit + 1):',
                    ],
                ],
            ],
        ],
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'tool_result',
                    'tool_use_id' => 'toolu_01PqRsTuVwXyZAbCdEfGh',
                    'content' => 'Successfully replaced text at exactly one location.',
                ],
            ],
        ],
    ],
);

echo $response;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [{type: "text_editor_20250728", name: "str_replace_based_edit_tool"}],
  messages: [
    # Pesan-pesan sebelumnya...
    {
      role: "assistant",
      content: [
        {
          type: "text",
          text: "I found the syntax error in your primes.py file. In the `get_primes` function, there is a missing colon (:) at the end of the for loop line. Let me fix that for you."
        },
        {
          type: "tool_use",
          id: "toolu_01PqRsTuVwXyZAbCdEfGh",
          name: "str_replace_based_edit_tool",
          input: {
            command: "str_replace",
            path: "primes.py",
            old_str: "    for num in range(2, limit + 1)",
            new_str: "    for num in range(2, limit + 1):"
          }
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: "toolu_01PqRsTuVwXyZAbCdEfGh",
          content: "Successfully replaced text at exactly one location."
        }
      ]
    }
  ]
)

puts response
```
</CodeGroup>

Terakhir, Claude memberikan penjelasan lengkap tentang perbaikan tersebut:

```json Output
{
  "id": "msg_01IjKlMnOpQrStUvWxYzAb",
  "model": "claude-opus-4-8",
  "stop_reason": "end_turn",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I've fixed the syntax error in your primes.py file. The issue was in the `get_primes` function at line 19. There was a missing colon (:) at the end of the for loop line.\n\nHere's what I changed:\n\nFrom:\n```python\nfor num in range(2, limit + 1)\n```\n\nTo:\n```python\nfor num in range(2, limit + 1):\n```\n\nIn Python, a colon is required at the end of statements that start a new code block, such as for loops, if statements, function definitions, etc. Without the colon, Python raises a syntax error because it doesn't know where the code block begins.\n\nYour code should now run correctly. The function will properly generate a list of prime numbers up to the specified limit."
    }
  ]
}
```

## Mengimplementasikan alat editor teks \{#implement-the-text-editor-tool}

Alat editor teks diimplementasikan sebagai alat tanpa skema. Saat menggunakan alat ini, Anda tidak perlu menyediakan skema input seperti pada alat lainnya; skema sudah tertanam dalam model Claude dan tidak dapat dimodifikasi.

Tipe alat adalah `type: "text_editor_20250728"` untuk model Claude 4.

<Steps>
  <Step title="Inisialisasi implementasi editor Anda">
    Buat fungsi pembantu untuk menangani operasi file seperti membaca, menulis, dan memodifikasi file. Pertimbangkan untuk mengimplementasikan fungsionalitas pencadangan untuk memulihkan dari kesalahan.
  </Step>
  <Step title="Tangani panggilan alat editor">
    Buat fungsi yang memproses panggilan alat dari Claude berdasarkan tipe perintah:

    
    <CodeGroup>
    ```python Python
    def handle_editor_tool(tool_call):
        input_params = tool_call.input
        command = input_params.get("command", "")
        file_path = input_params.get("path", "")

        if command == "view":
            # Baca dan kembalikan isi file
            pass
        elif command == "str_replace":
            # Ganti teks dalam file
            pass
        elif command == "create":
            # Buat file baru
            pass
        elif command == "insert":
            # Sisipkan teks di lokasi
            pass
    ```

    ```typescript TypeScript
    function handleEditorTool(toolCall: { input: { command?: string; path?: string } }): void {
      const inputParams = toolCall.input;
      const command = inputParams.command ?? "";
      const filePath = inputParams.path ?? "";

      if (command === "view") {
        // Baca dan kembalikan isi file
      } else if (command === "str_replace") {
        // Ganti teks dalam file
      } else if (command === "create") {
        // Buat file baru
      } else if (command === "insert") {
        // Sisipkan teks di lokasi
      }
    }
    ```

    ```csharp C# hidelines={1..3}
    using System.Collections.Generic;
    using System.Text.Json;

    static string HandleEditorTool(IReadOnlyDictionary<string, JsonElement> input)
    {
        input.TryGetValue("command", out var commandEl);
        input.TryGetValue("path", out var pathEl);
        var command = commandEl.ValueKind == JsonValueKind.String ? commandEl.GetString() : null;
        var filePath = pathEl.ValueKind == JsonValueKind.String ? pathEl.GetString() : null;

        if (command == "view")
        {
            // Baca dan kembalikan isi file
        }
        else if (command == "str_replace")
        {
            // Ganti teks dalam file
        }
        else if (command == "create")
        {
            // Buat file baru
        }
        else if (command == "insert")
        {
            // Sisipkan teks di lokasi
        }
        return "";
    }
    ```

    ```go Go hidelines={1..2,-2..}
    package main

    func handleEditorTool(input map[string]any) string {
    	command, _ := input["command"].(string)
    	filePath, _ := input["path"].(string)
    	_ = filePath

    	switch command {
    	case "view":
    		// Membaca dan mengembalikan isi file
    	case "str_replace":
    		// Mengganti teks dalam file
    	case "create":
    		// Membuat file baru
    	case "insert":
    		// Menyisipkan teks di lokasi tertentu
    	}
    	return ""
    }

    func main() {}
    ```

    ```java Java hidelines={1..2,-2..}
    import java.util.Map;

    static void handleEditorTool(Map<String, Object> input) {
      var command = (String) input.getOrDefault("command", "");
      var filePath = (String) input.getOrDefault("path", "");

      if (command.equals("view")) {
        // Membaca dan mengembalikan isi file
      } else if (command.equals("str_replace")) {
        // Mengganti teks dalam file
      } else if (command.equals("create")) {
        // Membuat file baru
      } else if (command.equals("insert")) {
        // Menyisipkan teks di lokasi tertentu
      }
    }

    void main() {}
    ```

    ```php PHP hidelines={1..2}
    <?php

    function handle_editor_tool(array $input): string
    {
        $command = $input['command'] ?? '';
        $filePath = $input['path'] ?? '';

        if ($command === 'view') {
            // Baca dan kembalikan isi file
        } elseif ($command === 'str_replace') {
            // Ganti teks dalam file
        } elseif ($command === 'create') {
            // Buat file baru
        } elseif ($command === 'insert') {
            // Sisipkan teks di lokasi
        }
        return '';
    }
    ```

    ```ruby Ruby
    def handle_editor_tool(input)
      command = input[:command] || ""
      file_path = input[:path] || ""

      case command
      when "view"
        # Baca dan kembalikan isi file
      when "str_replace"
        # Ganti teks dalam file
      when "create"
        # Buat file baru
      when "insert"
        # Sisipkan teks di lokasi
      end
    end
    ```
    </CodeGroup>
  </Step>
  <Step title="Implementasikan langkah-langkah keamanan">
    Tambahkan validasi dan pemeriksaan keamanan:
    - Validasi path file untuk mencegah directory traversal
    - Buat cadangan sebelum melakukan perubahan
    - Tangani kesalahan dengan baik
    - Implementasikan pemeriksaan izin
  </Step>
  <Step title="Proses respons Claude">
    Ekstrak dan tangani panggilan alat dari respons Claude:

    
    <CodeGroup>
    ```python Python hidelines={1..15}
    from types import SimpleNamespace as _SN

    response = _SN(
        content=[
            _SN(
                type="tool_use", name="str_replace_based_edit_tool", input={}, id="toolu_01"
            )
        ]
    )


    def handle_editor_tool(tc):
        return "ok"


    # Proses penggunaan alat dalam respons Claude
    for content in response.content:
        if content.type == "tool_use":
            # Jalankan alat berdasarkan perintah
            result = handle_editor_tool(content)

            # Kembalikan hasil ke Claude
            tool_result = {
                "type": "tool_result",
                "tool_use_id": content.id,
                "content": result,
            }
    ```

    ```typescript TypeScript hidelines={1..15}
    const response = {
      content: [
        {
          type: "tool_use",
          name: "str_replace_based_edit_tool",
          input: {},
          id: "toolu_01"
        }
      ]
    };

    function handleEditorTool(block: { input: object }): string {
      return "ok";
    }

    // Proses penggunaan alat dalam respons Claude
    for (const block of response.content) {
      if (block.type === "tool_use") {
        // Jalankan alat berdasarkan perintah
        const result = handleEditorTool(block);

        // Kembalikan hasil ke Claude
        const toolResult = {
          type: "tool_result",
          tool_use_id: block.id,
          content: result
        };
      }
    }
    ```

    ```csharp C# hidelines={1..14,-6..}
    using System.Collections.Generic;
    using System.Text.Json;
    using Anthropic.Models.Messages;

    var response = new
    {
        Content = new[]
        {
            new StubBlock(new StubToolUse("toolu_01", new Dictionary<string, JsonElement>())),
        },
    };

    static string HandleEditorTool(IReadOnlyDictionary<string, JsonElement> input) => "ok";

    // Proses penggunaan alat dalam respons Claude
    foreach (var block in response.Content)
    {
        if (block.TryPickToolUse(out var toolUse))
        {
            var result = HandleEditorTool(toolUse.Input);
            var toolResult = new ToolResultBlockParam
            {
                ToolUseID = toolUse.ID,
                Content = result,
            };
        }
    }

    record StubToolUse(string ID, IReadOnlyDictionary<string, JsonElement> Input);
    record StubBlock(StubToolUse ToolUse)
    {
        public bool TryPickToolUse(out StubToolUse toolUse) { toolUse = ToolUse; return true; }
    }
    ```

    ```go Go hidelines={1..20,-1}
    package main

    import (
    	"encoding/json"
    	"log"

    	"github.com/anthropics/anthropic-sdk-go"
    )

    func handleEditorTool(input map[string]any) string {
    	return "ok"
    }

    func main() {
    	response := anthropic.Message{
    		Content: []anthropic.ContentBlockUnion{
    			{Type: "tool_use", Name: "str_replace_based_edit_tool", ID: "toolu_01", Input: json.RawMessage(`{}`)},
    		},
    	}

    	// Proses penggunaan alat dalam respons Claude
    	for _, block := range response.Content {
    		if block.Type == "tool_use" {
    			var input map[string]any
    			if err := json.Unmarshal(block.Input, &input); err != nil {
    				log.Fatal(err)
    			}
    			result := handleEditorTool(input)

    			toolResult := anthropic.NewToolResultBlock(block.ID, result, false)
    			_ = toolResult
    		}
    	}
    }
    ```

    ```java Java hidelines={1..15,-1}
    import java.util.List;
    import java.util.Map;

    record ContentBlock(String type, String name, Map<String, Object> input, String id) {}
    record Response(List<ContentBlock> content) {}

    static String handleEditorTool(ContentBlock block) {
      return "ok";
    }

    void main() {
      var response = new Response(List.of(
        new ContentBlock("tool_use", "str_replace_based_edit_tool", Map.of(), "toolu_01")
      ));

      // Proses penggunaan alat dalam respons Claude
      for (var block : response.content()) {
        if (block.type().equals("tool_use")) {
          // Jalankan alat berdasarkan perintah
          var result = handleEditorTool(block);

          // Kembalikan hasil ke Claude
          var toolResult = Map.of(
            "type", "tool_result",
            "tool_use_id", block.id(),
            "content", result
          );
        }
      }
    }
    ```

    ```php PHP hidelines={1..18}
    <?php

    $response = (object) [
        'content' => [
            (object) [
                'type' => 'tool_use',
                'name' => 'str_replace_based_edit_tool',
                'input' => [],
                'id' => 'toolu_01',
            ],
        ],
    ];

    function handle_editor_tool(array $input): string
    {
        return 'ok';
    }

    // Proses penggunaan alat dalam respons Claude
    foreach ($response->content as $block) {
        if ($block->type === 'tool_use') {
            // Jalankan alat berdasarkan perintah
            $result = handle_editor_tool($block->input);

            // Kembalikan hasil ke Claude
            $toolResult = [
                'type' => 'tool_result',
                'tool_use_id' => $block->id,
                'content' => $result,
            ];
        }
    }
    ```

    ```ruby Ruby hidelines={1..11}
    Block = Struct.new(:type, :name, :input, :id)
    Response = Struct.new(:content)

    response = Response.new([
      Block.new(:tool_use, "str_replace_based_edit_tool", {command: "view", path: "primes.py"}, "toolu_01")
    ])

    def handle_editor_tool(input)
      "ok"
    end

    # Proses penggunaan alat dalam respons Claude
    tool_results = response.content.filter_map do |block|
      next unless block.type == :tool_use

      {type: "tool_result", tool_use_id: block.id, content: handle_editor_tool(block.input)}
    end
    ```
    </CodeGroup>
  </Step>
</Steps>

<Warning>
Saat mengimplementasikan alat editor teks, perhatikan hal-hal berikut:

1. **Keamanan:** Alat ini memiliki akses ke sistem file lokal Anda, jadi implementasikan langkah-langkah keamanan yang tepat.
2. **Pencadangan:** Selalu buat cadangan sebelum mengizinkan pengeditan pada file penting.
3. **Validasi:** Validasi semua input untuk mencegah perubahan yang tidak diinginkan.
4. **Pencocokan unik:** Pastikan penggantian cocok dengan tepat satu lokasi untuk menghindari pengeditan yang tidak diinginkan.
</Warning>

### Menangani kesalahan \{#handle-errors}

Saat menggunakan alat editor teks, berbagai kesalahan mungkin terjadi. Berikut adalah panduan tentang cara menanganinya:

<section title="File tidak ditemukan">

Jika Claude mencoba melihat atau memodifikasi file yang tidak ada, kembalikan pesan kesalahan yang sesuai dalam `tool_result`:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: File not found",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Beberapa kecocokan untuk penggantian">

Jika perintah `str_replace` Claude cocok dengan beberapa lokasi dalam file, kembalikan pesan kesalahan yang sesuai:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Found 3 matches for replacement text. Please provide more context to make a unique match.",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Tidak ada kecocokan untuk penggantian">

Jika perintah `str_replace` Claude tidak cocok dengan teks apa pun dalam file, kembalikan pesan kesalahan yang sesuai:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: No match found for replacement. Please check your text and try again.",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Kesalahan izin">

Jika ada masalah izin saat membuat, membaca, atau memodifikasi file, kembalikan pesan kesalahan yang sesuai:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Permission denied. Cannot write to file.",
      "is_error": true
    }
  ]
}
```

</section>

### Ikuti praktik terbaik implementasi \{#follow-implementation-best-practices}

<section title="Berikan konteks yang jelas">

Saat meminta Claude untuk memperbaiki atau memodifikasi kode, jelaskan secara spesifik file apa yang perlu diperiksa atau masalah apa yang perlu diatasi. Konteks yang jelas membantu Claude mengidentifikasi file yang tepat dan membuat perubahan yang sesuai.

**Prompt yang kurang membantu**: "Bisakah Anda memperbaiki kode saya?"

**Prompt yang lebih baik**: "Ada kesalahan sintaks di file primes.py saya yang mencegahnya berjalan. Bisakah Anda memperbaikinya?"

</section>

<section title="Jelaskan path file secara eksplisit">

Tentukan path file dengan jelas saat diperlukan, terutama jika Anda bekerja dengan beberapa file atau file di direktori yang berbeda.

**Prompt yang kurang membantu**: "Tinjau file helper saya"

**Prompt yang lebih baik**: "Bisakah Anda memeriksa file utils/helpers.py saya untuk masalah performa?"

</section>

<section title="Buat cadangan sebelum mengedit">

Implementasikan sistem pencadangan dalam aplikasi Anda yang membuat salinan file sebelum mengizinkan Claude mengeditnya, terutama untuk kode penting atau kode produksi.

<CodeGroup>
```python Python hidelines={1..3}
import os


def backup_file(file_path):
    """Create a backup of a file before editing."""
    backup_path = f"{file_path}.backup"
    if os.path.exists(file_path):
        with open(file_path, "r") as src, open(backup_path, "w") as dst:
            dst.write(src.read())
```

```typescript TypeScript hidelines={1..2}
import { access, copyFile } from "node:fs/promises";

async function backupFile(filePath: string): Promise<void> {
  const backupPath = `${filePath}.backup`;
  try {
    await access(filePath);
    await copyFile(filePath, backupPath);
  } catch {
    // File tidak ada; tidak ada yang perlu dicadangkan
  }
}
```

```csharp C# hidelines={1..2}
using System.IO;

static void BackupFile(string filePath)
{
    var backupPath = $"{filePath}.backup";
    if (File.Exists(filePath))
    {
        File.Copy(filePath, backupPath, overwrite: true);
    }
}
```

```go Go hidelines={1..4,-2..}
package main

import "os"

func backupFile(filePath string) error {
	backupPath := filePath + ".backup"
	data, err := os.ReadFile(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil
		}
		return err
	}
	return os.WriteFile(backupPath, data, 0o644)
}

func main() {}
```

```java Java hidelines={1..5,-2..}
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

static void backupFile(String filePath) throws IOException {
  Path source = Path.of(filePath);
  Path backupPath = Path.of(filePath + ".backup");
  if (Files.exists(source)) {
    Files.copy(source, backupPath, StandardCopyOption.REPLACE_EXISTING);
  }
}

void main() {}
```

```php PHP hidelines={1..2}
<?php

function backup_file(string $filePath): void
{
    $backupPath = $filePath . '.backup';
    if (file_exists($filePath)) {
        copy($filePath, $backupPath);
    }
}
```

```ruby Ruby hidelines={1..2}
require "fileutils"

def backup_file(file_path)
  backup_path = "#{file_path}.backup"
  FileUtils.cp(file_path, backup_path) if File.exist?(file_path)
end
```
</CodeGroup>

</section>

<section title="Tangani penggantian teks unik dengan hati-hati">

Perintah `str_replace` memerlukan kecocokan persis untuk teks yang akan diganti. Aplikasi Anda harus memastikan bahwa ada tepat satu kecocokan untuk teks lama atau memberikan pesan kesalahan yang sesuai.

<CodeGroup>
```python Python
def safe_replace(file_path, old_text, new_text):
    """Replace text only if there's exactly one match."""
    with open(file_path, "r") as f:
        content = f.read()

    count = content.count(old_text)
    if count == 0:
        return "Error: No match found"
    elif count > 1:
        return f"Error: Found {count} matches"
    else:
        new_content = content.replace(old_text, new_text)
        with open(file_path, "w") as f:
            f.write(new_content)
        return "Successfully replaced text"
```

```typescript TypeScript hidelines={1..2}
import { readFile, writeFile } from "node:fs/promises";

async function safeReplace(
  filePath: string,
  oldText: string,
  newText: string
): Promise<string> {
  const content = await readFile(filePath, "utf8");

  const count = content.split(oldText).length - 1;
  if (count === 0) {
    return "Error: No match found";
  } else if (count > 1) {
    return `Error: Found ${count} matches`;
  } else {
    const newContent = content.replace(oldText, newText);
    await writeFile(filePath, newContent, "utf8");
    return "Successfully replaced text";
  }
}
```

```csharp C# hidelines={1..2}
using System.IO;

static string SafeReplace(string filePath, string oldText, string newText)
{
    var content = File.ReadAllText(filePath);

    var count = content.Split(oldText).Length - 1;
    if (count == 0)
    {
        return "Error: No match found";
    }
    else if (count > 1)
    {
        return $"Error: Found {count} matches";
    }
    else
    {
        var newContent = content.Replace(oldText, newText);
        File.WriteAllText(filePath, newContent);
        return "Successfully replaced text";
    }
}
```

```go Go hidelines={1..8,-2..}
package main

import (
	"fmt"
	"os"
	"strings"
)

func safeReplace(filePath, oldText, newText string) string {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return fmt.Sprintf("Error: %v", err)
	}
	content := string(data)

	count := strings.Count(content, oldText)
	if count == 0 {
		return "Error: No match found"
	} else if count > 1 {
		return fmt.Sprintf("Error: Found %d matches", count)
	}

	newContent := strings.Replace(content, oldText, newText, 1)
	if err := os.WriteFile(filePath, []byte(newContent), 0o644); err != nil {
		return fmt.Sprintf("Error: %v", err)
	}
	return "Successfully replaced text"
}

func main() {}
```

```java Java hidelines={1..5,-2..}
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.regex.Pattern;

static String safeReplace(String filePath, String oldText, String newText) throws IOException {
  String content = Files.readString(Path.of(filePath));

  int count = content.split(Pattern.quote(oldText), -1).length - 1;
  if (count == 0) {
    return "Error: No match found";
  } else if (count > 1) {
    return "Error: Found " + count + " matches";
  } else {
    String newContent = content.replace(oldText, newText);
    Files.writeString(Path.of(filePath), newContent);
    return "Successfully replaced text";
  }
}

void main() {}
```

```php PHP hidelines={1..2}
<?php

function safe_replace(string $filePath, string $oldText, string $newText): string
{
    $content = file_get_contents($filePath);

    $count = substr_count($content, $oldText);
    if ($count === 0) {
        return 'Error: No match found';
    } elseif ($count > 1) {
        return "Error: Found {$count} matches";
    } else {
        $newContent = str_replace($oldText, $newText, $content);
        file_put_contents($filePath, $newContent);
        return 'Successfully replaced text';
    }
}
```

```ruby Ruby
def safe_replace(file_path, old_text, new_text)
  content = File.read(file_path)

  count = content.scan(old_text).length
  if count == 0
    "Error: No match found"
  elsif count > 1
    "Error: Found #{count} matches"
  else
    new_content = content.sub(old_text) { new_text }
    File.write(file_path, new_content)
    "Successfully replaced text"
  end
end
```
</CodeGroup>

</section>

<section title="Verifikasi perubahan">

Setelah Claude membuat perubahan pada file, verifikasi perubahan tersebut dengan menjalankan pengujian atau memeriksa bahwa kode masih berfungsi seperti yang diharapkan.

<CodeGroup>
```python Python
def verify_changes(file_path):
    """Run tests or checks after making changes."""
    try:
        # Untuk file Python, periksa kesalahan sintaks
        if file_path.endswith(".py"):
            import ast

            with open(file_path, "r") as f:
                ast.parse(f.read())
            return "Syntax check passed"
    except Exception as e:
        return f"Verification failed: {str(e)}"
```

```typescript TypeScript hidelines={1..2}
import { execFileSync } from "node:child_process";

function verifyChanges(filePath: string): string {
  try {
    // Untuk file Python, periksa kesalahan sintaks
    if (filePath.endsWith(".py")) {
      execFileSync("python3", ["-m", "py_compile", filePath]);
      return "Syntax check passed";
    }
    return "No checks defined for this file type";
  } catch (err) {
    return `Verification failed: ${err}`;
  }
}
```

```csharp C# hidelines={1..2}
using System.Diagnostics;

static string VerifyChanges(string filePath)
{
    try
    {
        // Untuk file Python, periksa kesalahan sintaks
        if (filePath.EndsWith(".py"))
        {
            var psi = new ProcessStartInfo("python3")
            {
                RedirectStandardError = true,
            };
            psi.ArgumentList.Add("-m");
            psi.ArgumentList.Add("py_compile");
            psi.ArgumentList.Add(filePath);
            using var proc = Process.Start(psi)!;
            proc.WaitForExit();
            if (proc.ExitCode != 0)
            {
                return $"Verification failed: {proc.StandardError.ReadToEnd()}";
            }
            return "Syntax check passed";
        }
        return "No checks defined for this file type";
    }
    catch (Exception e)
    {
        return $"Verification failed: {e.Message}";
    }
}
```

```go Go hidelines={1..8,-2..}
package main

import (
	"fmt"
	"os/exec"
	"strings"
)

func verifyChanges(filePath string) string {
	// Untuk file Python, periksa kesalahan sintaks
	if strings.HasSuffix(filePath, ".py") {
		cmd := exec.Command("python3", "-m", "py_compile", filePath)
		if out, err := cmd.CombinedOutput(); err != nil {
			return fmt.Sprintf("Verification failed: %v: %s", err, out)
		}
		return "Syntax check passed"
	}
	return "No checks defined for this file type"
}

func main() {}
```

```java Java hidelines={1..2,-2..}
import java.io.IOException;

static String verifyChanges(String filePath) {
  try {
    // Untuk file Python, periksa kesalahan sintaks
    if (filePath.endsWith(".py")) {
      Process proc = new ProcessBuilder("python3", "-m", "py_compile", filePath)
        .redirectErrorStream(true)
        .start();
      if (proc.waitFor() != 0) {
        return "Verification failed: " + new String(proc.getInputStream().readAllBytes());
      }
      return "Syntax check passed";
    }
    return "No checks defined for this file type";
  } catch (IOException | InterruptedException e) {
    return "Verification failed: " + e.getMessage();
  }
}

void main() {}
```

```php PHP hidelines={1..2}
<?php

function verify_changes(string $filePath): string
{
    // Untuk file Python, periksa kesalahan sintaks
    if (str_ends_with($filePath, '.py')) {
        exec('python3 -m py_compile ' . escapeshellarg($filePath) . ' 2>&1', $output, $exitCode);
        if ($exitCode !== 0) {
            return 'Verification failed: ' . implode("\n", $output);
        }
        return 'Syntax check passed';
    }
    return 'No checks defined for this file type';
}
```

```ruby Ruby
def verify_changes(file_path)
  # Untuk file Python, periksa kesalahan sintaks
  if file_path.end_with?(".py")
    if system("python3", "-m", "py_compile", file_path)
      "Syntax check passed"
    else
      "Verification failed: syntax error in #{file_path}"
    end
  else
    "No checks defined for this file type"
  end
end
```
</CodeGroup>

</section>

---

## Harga dan penggunaan token \{#pricing-and-token-usage}

Alat editor teks menggunakan struktur harga yang sama dengan alat lain yang digunakan bersama Claude. Alat ini mengikuti harga token input dan output standar berdasarkan model Claude yang Anda gunakan.

Selain token dasar, token input tambahan berikut diperlukan untuk alat editor teks:

| Alat | Token input tambahan |
| ----------------------------------------- | --------------------------------------- |
| `text_editor_20250429` (Claude 4.x) | 700 token |

Untuk informasi lebih detail tentang harga alat, lihat [Harga penggunaan alat](/docs/id/agents-and-tools/tool-use/overview#pricing).

## Mengintegrasikan alat editor teks dengan alat lainnya \{#integrate-the-text-editor-tool-with-other-tools}

Alat editor teks dapat digunakan bersama alat Claude lainnya. Saat menggabungkan alat, pastikan Anda:
- Mencocokkan versi alat dengan model yang Anda gunakan
- Memperhitungkan penggunaan token tambahan untuk semua alat yang disertakan dalam permintaan Anda

## Log perubahan \{#change-log}

| Tanggal | Versi | Perubahan |
| ---- | ------- | ------- |
| 28 Juli 2025 | `text_editor_20250728` | Rilis alat editor teks yang diperbarui yang memperbaiki beberapa masalah dan menambahkan parameter opsional `max_characters`. Selain itu, identik dengan `text_editor_20250429`. |
| 29 April 2025 | `text_editor_20250429` | Rilis alat editor teks untuk Claude 4. Versi ini menghapus perintah `undo_edit` tetapi mempertahankan semua kemampuan lainnya. Nama alat telah diperbarui untuk mencerminkan arsitektur berbasis str_replace. |
| 13 Maret 2025 | `text_editor_20250124` | Pengenalan dokumentasi alat editor teks mandiri. Versi ini dioptimalkan untuk Claude Sonnet 3.7 tetapi memiliki kemampuan yang identik dengan versi sebelumnya. |
| 22 Oktober 2024 | `text_editor_20241022` | Rilis awal alat editor teks dengan Claude Sonnet 3.5 ([sudah dihentikan](/docs/id/about-claude/model-deprecations)). Menyediakan kemampuan untuk melihat, membuat, dan mengedit file melalui perintah `view`, `create`, `str_replace`, `insert`, dan `undo_edit`. |

## Langkah selanjutnya \{#next-steps}

Berikut adalah beberapa ide tentang cara menggunakan alat editor teks dengan cara yang lebih praktis dan canggih:

- **Integrasikan dengan alur kerja pengembangan Anda**: Bangun alat editor teks ke dalam alat pengembangan atau IDE Anda
- **Buat sistem tinjauan kode**: Minta Claude meninjau kode Anda dan membuat perbaikan
- **Bangun asisten debugging**: Buat sistem di mana Claude dapat membantu Anda mendiagnosis dan memperbaiki masalah dalam kode Anda
- **Implementasikan konversi format file**: Biarkan Claude membantu Anda mengonversi file dari satu format ke format lainnya
- **Otomatisasi dokumentasi**: Siapkan alur kerja agar Claude secara otomatis mendokumentasikan kode Anda

Alat editor teks memungkinkan Claude untuk bekerja langsung dengan basis kode Anda, mendukung alur kerja mulai dari debugging hingga dokumentasi otomatis.

<CardGroup cols={3}>
  <Card
    title="Ikhtisar penggunaan alat"
    icon="wrench"
    href="/docs/id/agents-and-tools/tool-use/overview"
  >
    Pelajari cara mengimplementasikan alur kerja alat untuk digunakan dengan Claude.
  </Card>

  <Card
    title="Alat Bash"
    icon="terminal"
    href="/docs/id/agents-and-tools/tool-use/bash-tool"
  >
    Jalankan perintah shell dengan Claude.
  </Card>
</CardGroup>