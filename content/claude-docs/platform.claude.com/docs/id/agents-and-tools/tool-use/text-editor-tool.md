---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: fdc0606ab4b275ec2852e1306f75a076dd9c3cb5225b9ab6aa9dd0fc35368d5b
---

# Alat text editor

Berikan Claude alat text editor yang didefinisikan Anthropic untuk melihat, membuat, dan mengedit file, serta menangani perintah view, str_replace, create, dan insert.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Claude dapat menggunakan alat text editor dengan skema Anthropic untuk melihat dan memodifikasi file teks, membantu Anda melakukan debug, memperbaiki, dan meningkatkan kode atau dokumen teks lainnya. Ini memungkinkan Claude berinteraksi langsung dengan file Anda, memberikan bantuan langsung alih-alih hanya menyarankan perubahan.

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Kapan menggunakan alat text editor

Beberapa contoh kapan menggunakan alat text editor adalah:

* **Debugging kode:** Minta Claude mengidentifikasi dan memperbaiki bug dalam kode Anda, mulai dari kesalahan sintaks hingga masalah logika.
* **Refactoring kode:** Biarkan Claude meningkatkan struktur, keterbacaan, dan performa kode Anda melalui pengeditan yang terarah.
* **Pembuatan dokumentasi:** Minta Claude menambahkan docstring, komentar, atau file README ke basis kode Anda.
* **Pembuatan pengujian:** Minta Claude membuat unit test untuk kode Anda berdasarkan analisisnya terhadap implementasi.

## Menggunakan alat text editor

Sediakan alat text editor (bernama `str_replace_based_edit_tool`) kepada Claude menggunakan Messages API.

Anda dapat secara opsional menentukan parameter `max_characters` untuk mengontrol pemotongan saat melihat file berukuran besar.

<Note>
  `max_characters` hanya kompatibel dengan `text_editor_20250728` dan versi alat text editor yang lebih baru.
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

  ```python Python
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

  ```typescript TypeScript
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

  ```csharp C#
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

  ```go Go
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
  ```

  ```java Java
  import com.anthropic.models.messages.ToolTextEditor20250728;
  // ...
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

  ```php PHP
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

  ```ruby Ruby
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

Gunakan alat text editor dengan cara berikut:

<Steps>
  <Step title="Sediakan alat text editor dan prompt pengguna kepada Claude">
    * Sertakan alat text editor dalam permintaan API Anda
    * Berikan prompt pengguna yang mungkin memerlukan pemeriksaan atau modifikasi file, seperti "Bisakah Anda memperbaiki kesalahan sintaks dalam kode saya?"
  </Step>

  <Step title="Claude menggunakan alat untuk memeriksa file atau direktori">
    * Claude menilai apa yang perlu dilihatnya dan menggunakan perintah `view` untuk memeriksa isi file atau menampilkan daftar isi direktori
    * Respons API akan berisi blok konten `tool_use` dengan perintah `view`
  </Step>

  <Step title="Jalankan perintah view dan kembalikan hasilnya">
    * Ekstrak jalur file atau direktori dari permintaan penggunaan alat Claude
    * Baca isi file atau tampilkan daftar isi direktori
    * Jika parameter `max_characters` ditentukan dalam konfigurasi alat, potong isi file hingga panjang tersebut
    * Kembalikan hasilnya kepada Claude dengan melanjutkan percakapan menggunakan pesan `user` baru yang berisi blok konten `tool_result`
  </Step>

  <Step title="Claude menggunakan alat untuk memodifikasi file">
    * Setelah memeriksa file atau direktori, Claude dapat menggunakan perintah seperti `str_replace` untuk membuat perubahan atau `insert` untuk menambahkan teks pada nomor baris tertentu.
    * Jika Claude menggunakan perintah `str_replace`, Claude menyusun permintaan penggunaan alat yang diformat dengan benar berisi teks lama dan teks baru untuk menggantikannya
  </Step>

  <Step title="Jalankan pengeditan dan kembalikan hasilnya">
    * Ekstrak jalur file, teks lama, dan teks baru dari permintaan penggunaan alat Claude
    * Lakukan penggantian teks dalam file
    * Kembalikan hasilnya kepada Claude
  </Step>

  <Step title="Claude memberikan analisis dan penjelasannya">
    * Setelah memeriksa dan mungkin mengedit file, Claude memberikan penjelasan lengkap tentang apa yang ditemukannya dan perubahan apa yang dibuatnya
  </Step>
</Steps>

### Perintah alat text editor

Alat text editor mendukung beberapa perintah untuk melihat dan memodifikasi file:

#### view

Perintah `view` memungkinkan Claude memeriksa isi file atau menampilkan daftar isi direktori. Perintah ini dapat membaca seluruh file atau rentang baris tertentu.

Parameter:

* `command`: Harus "view"
* `path`: Jalur ke file atau direktori yang akan dilihat
* `view_range` (opsional): Array berisi dua bilangan bulat yang menentukan nomor baris awal dan akhir yang akan dilihat. Nomor baris dimulai dari 1, dan -1 untuk baris akhir berarti membaca hingga akhir file. Parameter ini hanya berlaku saat melihat file, bukan direktori.

<Accordion title="Contoh perintah view">
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
</Accordion>

#### str\_replace

Perintah `str_replace` memungkinkan Claude mengganti string tertentu dalam file dengan string baru. Ini digunakan untuk membuat pengeditan yang presisi.

Parameter:

* `command`: Harus "str\_replace"
* `path`: Jalur ke file yang akan dimodifikasi
* `old_str`: Teks yang akan diganti (harus cocok persis, termasuk spasi dan indentasi)
* `new_str`: Teks baru yang akan disisipkan menggantikan teks lama

<Accordion title="Contoh perintah str_replace">
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
</Accordion>

#### create

Perintah `create` memungkinkan Claude membuat file baru dengan konten yang ditentukan.

Parameter:

* `command`: Harus "create"
* `path`: Jalur tempat file baru harus dibuat
* `file_text`: Konten yang akan ditulis ke file baru

<Accordion title="Contoh perintah create">
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
</Accordion>

#### insert

Perintah `insert` memungkinkan Claude menyisipkan teks di lokasi tertentu dalam file.

Parameter:

* `command`: Harus "insert"
* `path`: Jalur ke file yang akan dimodifikasi
* `insert_line`: Nomor baris setelah mana teks akan disisipkan (0 untuk awal file)
* `insert_text`: Teks yang akan disisipkan

<Accordion title="Contoh perintah insert">
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
</Accordion>

### Contoh: Memperbaiki kesalahan sintaks dengan alat text editor

Contoh ini menunjukkan bagaimana Claude menggunakan alat text editor untuk memperbaiki kesalahan sintaks dalam file Python.

Pertama, aplikasi Anda menyediakan alat text editor dan prompt kepada Claude untuk memperbaiki kesalahan sintaks:

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

  ```python Python
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

  ```typescript TypeScript
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

  ```csharp C#
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

  ```go Go
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
  ```

  ```java Java
  import com.anthropic.models.messages.ToolTextEditor20250728;
  // ...
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

  ```php PHP
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

  ```ruby Ruby
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

Claude menggunakan alat text editor terlebih dahulu untuk melihat file:

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

  ```typescript TypeScript
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

  ```csharp C#
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

  ```go Go
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
  ```

  ```java Java
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
  ```

  ```php PHP
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

  ```ruby Ruby
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

  Pada contoh sebelumnya, hasil alat `view` menyertakan isi file dengan nomor baris yang ditambahkan di awal setiap baris (misalnya, "1: def is\_prime(n):"). Nomor baris tidak wajib, tetapi sangat penting untuk berhasil menggunakan parameter `view_range` dalam memeriksa bagian tertentu dari file dan parameter `insert_line` untuk menambahkan konten di lokasi yang tepat.
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

  ```bash CLI
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

  ```csharp C#
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

  ```go Go
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
  ```

  ```java Java
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
  ```

  ```php PHP
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

  ```ruby Ruby
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

````json Output
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
````

## Mengimplementasikan alat text editor

Alat text editor diimplementasikan sebagai alat tanpa skema. Saat menggunakan alat ini, Anda tidak perlu menyediakan skema input seperti pada alat lainnya; skema sudah terpasang dalam model Claude dan tidak dapat dimodifikasi.

Tipe alatnya adalah `type: "text_editor_20250728"` untuk model Claude 4.

<Steps>
  <Step title="Inisialisasi implementasi editor Anda">
    Buat fungsi pembantu untuk menangani operasi file seperti membaca, menulis, dan memodifikasi file. Pertimbangkan untuk mengimplementasikan fungsionalitas cadangan untuk memulihkan dari kesalahan.
  </Step>

  <Step title="Tangani panggilan alat editor">
    Buat fungsi yang memproses panggilan alat dari Claude berdasarkan tipe perintah:

    <CodeGroup exclude="shell">
      ```python Python
      def handle_editor_tool(tool_call):
          input_params = tool_call.input
          command = input_params.get("command", "")
          file_path = input_params.get("path", "")

          if command == "view":
              # Membaca dan mengembalikan isi file
              pass
          elif command == "str_replace":
              # Mengganti teks dalam file
              pass
          elif command == "create":
              # Membuat file baru
              pass
          elif command == "insert":
              # Menyisipkan teks di lokasi tertentu
              pass
      ```

      ```typescript TypeScript
      function handleEditorTool(toolCall: { input: { command?: string; path?: string } }): void {
        const inputParams = toolCall.input;
        const command = inputParams.command ?? "";
        const filePath = inputParams.path ?? "";

        if (command === "view") {
          // Membaca dan mengembalikan isi file
        } else if (command === "str_replace") {
          // Mengganti teks dalam file
        } else if (command === "create") {
          // Membuat file baru
        } else if (command === "insert") {
          // Menyisipkan teks di lokasi tertentu
        }
      }
      ```

      ```csharp C#
      static string HandleEditorTool(IReadOnlyDictionary<string, JsonElement> input)
      {
          input.TryGetValue("command", out var commandEl);
          input.TryGetValue("path", out var pathEl);
          var command = commandEl.ValueKind == JsonValueKind.String ? commandEl.GetString() : null;
          var filePath = pathEl.ValueKind == JsonValueKind.String ? pathEl.GetString() : null;

          if (command == "view")
          {
              // Membaca dan mengembalikan isi file
          }
          else if (command == "str_replace")
          {
              // Mengganti teks dalam file
          }
          else if (command == "create")
          {
              // Membuat file baru
          }
          else if (command == "insert")
          {
              // Menyisipkan teks di lokasi tertentu
          }
          return "";
      }
      ```

      ```go Go
      func handleEditorTool(input map[string]any) string {
      	command, _ := input["command"].(string)
      	filePath, _ := input["path"].(string)
      // ...

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
      ```

      ```java Java
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
      ```

      ```php PHP
      function handle_editor_tool(array $input): string
      {
          $command = $input['command'] ?? '';
          $filePath = $input['path'] ?? '';

          if ($command === 'view') {
              // Membaca dan mengembalikan isi file
          } elseif ($command === 'str_replace') {
              // Mengganti teks dalam file
          } elseif ($command === 'create') {
              // Membuat file baru
          } elseif ($command === 'insert') {
              // Menyisipkan teks di lokasi tertentu
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
          # Membaca dan mengembalikan isi file
        when "str_replace"
          # Mengganti teks dalam file
        when "create"
          # Membuat file baru
        when "insert"
          # Menyisipkan teks di lokasi tertentu
        end
      end
      ```
    </CodeGroup>
  </Step>

  <Step title="Implementasikan langkah-langkah keamanan">
    Tambahkan validasi dan pemeriksaan keamanan:

    * Validasi jalur file untuk mencegah directory traversal
    * Buat cadangan sebelum membuat perubahan
    * Tangani kesalahan dengan baik
    * Implementasikan pemeriksaan izin
  </Step>

  <Step title="Proses respons Claude">
    Ekstrak dan tangani panggilan alat dari respons Claude:

    <CodeGroup exclude="shell">
      ```python Python
      # Memproses penggunaan alat dalam respons Claude
      for content in response.content:
          if content.type == "tool_use":
              # Menjalankan alat berdasarkan perintah
              result = handle_editor_tool(content)

              # Mengembalikan hasil ke Claude
              tool_result = {
                  "type": "tool_result",
                  "tool_use_id": content.id,
                  "content": result,
              }
      ```

      ```typescript TypeScript
      // Memproses penggunaan alat dalam respons Claude
      for (const block of response.content) {
        if (block.type === "tool_use") {
          // Menjalankan alat berdasarkan perintah
          const result = handleEditorTool(block);

          // Mengembalikan hasil ke Claude
          const toolResult = {
            type: "tool_result",
            tool_use_id: block.id,
            content: result
          };
        }
      }
      ```

      ```csharp C#
      // Memproses penggunaan alat dalam respons Claude
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
      ```

      ```go Go
      // Proses penggunaan alat dalam respons Claude
      for _, block := range response.Content {
      	if block.Type == "tool_use" {
      		var input map[string]any
      		if err := json.Unmarshal(block.Input, &input); err != nil {
      			log.Fatal(err)
      		}
      		result := handleEditorTool(input)

      		toolResult := anthropic.NewToolResultBlock(block.ID, result, false)
      // ...
      	}
      }
      ```

      ```java Java
      // Memproses penggunaan alat dalam respons Claude
      for (var block : response.content()) {
        if (block.type().equals("tool_use")) {
          // Menjalankan alat berdasarkan perintah
          var result = handleEditorTool(block);

          // Mengembalikan hasil ke Claude
          var toolResult = Map.of(
            "type", "tool_result",
            "tool_use_id", block.id(),
            "content", result
          );
        }
      }
      ```

      ```php PHP
      // Memproses penggunaan alat dalam respons Claude
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              // Menjalankan alat berdasarkan perintah
              $result = handle_editor_tool($block->input);

              // Mengembalikan hasil ke Claude
              $toolResult = [
                  'type' => 'tool_result',
                  'tool_use_id' => $block->id,
                  'content' => $result,
              ];
          }
      }
      ```

      ```ruby Ruby
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
  Saat mengimplementasikan alat text editor, perhatikan hal-hal berikut:

  1. **Keamanan:** Alat ini memiliki akses ke sistem file lokal Anda, jadi implementasikan langkah-langkah keamanan yang tepat.
  2. **Cadangan:** Selalu buat cadangan sebelum mengizinkan pengeditan pada file penting.
  3. **Validasi:** Validasi semua input untuk mencegah perubahan yang tidak diinginkan.
  4. **Pencocokan unik:** Pastikan penggantian cocok dengan tepat satu lokasi untuk menghindari pengeditan yang tidak diinginkan.
</Warning>

### Menangani kesalahan

Saat menggunakan alat text editor, berbagai kesalahan dapat terjadi. Berikut panduan cara menanganinya:

<AccordionGroup>
  <Accordion title="File tidak ditemukan">
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
  </Accordion>

  <Accordion title="Beberapa kecocokan untuk penggantian">
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
  </Accordion>

  <Accordion title="Tidak ada kecocokan untuk penggantian">
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
  </Accordion>

  <Accordion title="Kesalahan izin">
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
  </Accordion>
</AccordionGroup>

### Ikuti praktik terbaik implementasi

<AccordionGroup>
  <Accordion title="Berikan konteks yang jelas">
    Saat meminta Claude memperbaiki atau memodifikasi kode, jelaskan secara spesifik file mana yang perlu diperiksa atau masalah apa yang perlu ditangani. Konteks yang jelas membantu Claude mengidentifikasi file yang tepat dan membuat perubahan yang sesuai.

    **Prompt yang kurang membantu:** "Bisakah Anda memperbaiki kode saya?"

    **Prompt yang lebih baik:** "Ada kesalahan sintaks di file primes.py saya yang mencegahnya berjalan. Bisakah Anda memperbaikinya?"
  </Accordion>

  <Accordion title="Jelaskan jalur file secara eksplisit">
    Tentukan jalur file dengan jelas saat diperlukan, terutama jika Anda bekerja dengan banyak file atau file di direktori yang berbeda.

    **Prompt yang kurang membantu:** "Tinjau file helper saya"

    **Prompt yang lebih baik:** "Bisakah Anda memeriksa file utils/helpers.py saya untuk masalah performa?"
  </Accordion>

  <Accordion title="Buat cadangan sebelum mengedit">
    Implementasikan sistem cadangan dalam aplikasi Anda yang membuat salinan file sebelum mengizinkan Claude mengeditnya, terutama untuk kode penting atau kode produksi.

    <CodeGroup exclude="shell">
      ```python Python
      def backup_file(file_path):
          """Create a backup of a file before editing."""
          backup_path = f"{file_path}.backup"
          if os.path.exists(file_path):
              with open(file_path, "r") as src, open(backup_path, "w") as dst:
                  dst.write(src.read())
      ```

      ```typescript TypeScript
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

      ```csharp C#
      static void BackupFile(string filePath)
      {
          var backupPath = $"{filePath}.backup";
          if (File.Exists(filePath))
          {
              File.Copy(filePath, backupPath, overwrite: true);
          }
      }
      ```

      ```go Go
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
      ```

      ```java Java
      static void backupFile(String filePath) throws IOException {
        Path source = Path.of(filePath);
        Path backupPath = Path.of(filePath + ".backup");
        if (Files.exists(source)) {
          Files.copy(source, backupPath, StandardCopyOption.REPLACE_EXISTING);
        }
      }
      ```

      ```php PHP
      function backup_file(string $filePath): void
      {
          $backupPath = $filePath . '.backup';
          if (file_exists($filePath)) {
              copy($filePath, $backupPath);
          }
      }
      ```

      ```ruby Ruby
      def backup_file(file_path)
        backup_path = "#{file_path}.backup"
        FileUtils.cp(file_path, backup_path) if File.exist?(file_path)
      end
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Tangani penggantian teks unik dengan hati-hati">
    Perintah `str_replace` memerlukan kecocokan persis untuk teks yang akan diganti. Aplikasi Anda harus memastikan bahwa ada tepat satu kecocokan untuk teks lama atau memberikan pesan kesalahan yang sesuai.

    <CodeGroup exclude="shell">
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

      ```typescript TypeScript
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

      ```csharp C#
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

      ```go Go
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
      ```

      ```java Java
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
      ```

      ```php PHP
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
  </Accordion>

  <Accordion title="Verifikasi perubahan">
    Setelah Claude membuat perubahan pada file, verifikasi perubahan tersebut dengan menjalankan pengujian atau memeriksa bahwa kode masih berfungsi seperti yang diharapkan.

    <CodeGroup exclude="shell">
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

      ```typescript TypeScript
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

      ```csharp C#
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

      ```go Go
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
      ```

      ```java Java
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
      ```

      ```php PHP
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
  </Accordion>
</AccordionGroup>

***

## Harga dan penggunaan token

Alat editor teks menggunakan struktur harga yang sama dengan alat lain yang digunakan bersama Claude. Alat ini mengikuti harga token input dan output standar berdasarkan model Claude yang Anda gunakan.

Selain token dasar, token input tambahan berikut diperlukan untuk alat editor teks:

| Alat                                | Token input tambahan |
| ----------------------------------- | -------------------- |
| `text_editor_20250429` (Claude 4.x) | 700 token            |

Untuk informasi lebih rinci tentang harga alat, lihat [Harga penggunaan alat](/docs/id/agents-and-tools/tool-use/overview#pricing).

## Mengintegrasikan alat text editor dengan alat lain

Anda dapat menggunakan alat text editor bersama alat Claude lainnya. Saat menggabungkan alat, pastikan Anda:

* Mencocokkan versi alat dengan model yang Anda gunakan
* Memperhitungkan penggunaan token tambahan untuk semua alat yang disertakan dalam permintaan Anda

## Log perubahan

| Tanggal         | Versi                  | Perubahan                                                                                                                                                                                                                                                                                  |
| --------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 28 Juli 2025    | `text_editor_20250728` | Rilis alat text editor yang diperbarui yang memperbaiki beberapa masalah dan menambahkan parameter opsional `max_characters`. Selain itu identik dengan `text_editor_20250429`.                                                                                                            |
| 29 April 2025   | `text_editor_20250429` | Rilis alat text editor untuk Claude 4. Versi ini menghapus perintah `undo_edit` tetapi mempertahankan semua kemampuan lainnya. Nama alat telah diperbarui untuk mencerminkan arsitekturnya yang berbasis str\_replace.                                                                     |
| 13 Maret 2025   | `text_editor_20250124` | Pengenalan dokumentasi alat text editor mandiri. Versi ini dioptimalkan untuk Claude Sonnet 3.7 tetapi memiliki kemampuan yang identik dengan versi sebelumnya.                                                                                                                            |
| 22 Oktober 2024 | `text_editor_20241022` | Rilis awal alat text editor dengan Claude Sonnet 3.5 (sudah dihentikan; lihat [Penghentian model](/docs/id/about-claude/model-deprecations)). Menyediakan kemampuan untuk melihat, membuat, dan mengedit file melalui perintah `view`, `create`, `str_replace`, `insert`, dan `undo_edit`. |

## Langkah selanjutnya

Berikut beberapa ide tentang cara menggunakan alat text editor dengan cara yang lebih praktis dan lebih andal:

* **Integrasikan dengan alur kerja pengembangan Anda**: Bangun alat text editor ke dalam alat pengembangan atau IDE Anda
* **Buat sistem tinjauan kode**: Minta Claude meninjau kode Anda dan membuat perbaikan
* **Bangun asisten debugging**: Buat sistem di mana Claude dapat membantu Anda mendiagnosis dan memperbaiki masalah dalam kode Anda
* **Implementasikan konversi format file**: Biarkan Claude membantu Anda mengonversi file dari satu format ke format lainnya
* **Otomatiskan dokumentasi**: Siapkan alur kerja agar Claude secara otomatis mendokumentasikan kode Anda

Alat text editor memungkinkan Claude bekerja langsung dengan basis kode Anda, mendukung alur kerja mulai dari debugging hingga dokumentasi otomatis.

<CardGroup cols={3}>
  <Card title="Ikhtisar penggunaan alat" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Pelajari cara mengimplementasikan alur kerja alat untuk digunakan dengan Claude.
  </Card>

  <Card title="Alat bash" icon="terminal" href="/docs/id/agents-and-tools/tool-use/bash-tool">
    Jalankan perintah shell dengan Claude.
  </Card>
</CardGroup>
