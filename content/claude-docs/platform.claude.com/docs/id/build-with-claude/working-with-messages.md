---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/working-with-messages
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 60811dab4f230e4192dec91261088a3d0b567d51b6479a2b896ec94759445340
---

---
title: Menggunakan Messages API
url: https://platform.claude.com/docs/id/build-with-claude/working-with-messages
description: Pola praktis dan contoh untuk menggunakan Messages API secara efektif
---

Anthropic menawarkan dua cara untuk membangun dengan Claude, masing-masing cocok untuk kasus penggunaan yang berbeda:

|                        | Messages API                                    | Claude Managed Agents                                                                    |
| ---------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Apa itu**            | Akses langsung untuk memberikan prompt ke model | Harness agen siap pakai yang dapat dikonfigurasi dan berjalan di infrastruktur terkelola |
| **Paling cocok untuk** | Loop agen kustom dan kontrol yang terperinci    | Tugas yang berjalan lama dan pekerjaan asinkron                                          |

Panduan ini membahas pola umum untuk bekerja dengan Messages API, termasuk permintaan dasar, percakapan multi-giliran, teknik prefill, dan kemampuan vision. Untuk spesifikasi API lengkap, lihat [referensi Messages API](https://platform.claude.com/docs/id/api/messages/create). Untuk harness agen terkelola, lihat [ikhtisar Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview).

<Note>
  Untuk mempelajari bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku untuk fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

## Permintaan dan respons dasar

<Note>
  Parameter sampling `temperature`, `top_p`, dan `top_k` tidak didukung pada model Claude 4.7 dan yang lebih baru serta Claude Mythos Preview. Mengaturnya ke nilai non-default akan mengembalikan error 400. Hilangkan parameter tersebut dari payload permintaan dan gunakan prompting untuk mengarahkan perilaku model sebagai gantinya. Lihat [panduan migrasi](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-47).
</Note>

<CodeGroup>
  ```bash cURL
  #!/bin/sh
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello, Claude"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  message = anthropic.Anthropic().messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(message)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const message = await anthropic.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  console.log(message);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello, Claude" }]
  };
  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
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
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(1024L)
      .addUserMessage("Hello, Claude")
      .build();

  Message response = client.messages().create(params);
  System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: 'claude-opus-5',
  );
  echo json_encode($message, JSON_PRETTY_PRINT), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "Hello, Claude" }
    ]
  )
  puts message
  ```
</CodeGroup>

```json Output
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello!"
    }
  ],
  "model": "claude-opus-5",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 6
  }
}
```

Respons penolakan (`stop_reason: "refusal"`) juga menyertakan objek `stop_details` yang mengidentifikasi kategori kebijakan yang memicu penolakan tersebut, pada setiap model. Lihat [Menangani stop reason](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk referensi field dan contoh kode penanganannya.

## Beberapa giliran percakapan

Messages API bersifat stateless (tanpa status), yang berarti Anda selalu mengirimkan riwayat percakapan lengkap ke API. Anda dapat menggunakan pola ini untuk membangun percakapan dari waktu ke waktu. Giliran percakapan sebelumnya tidak harus benar-benar berasal dari Claude. Anda dapat menggunakan pesan `assistant` sintetis.

<CodeGroup>
  ```bash cURL
  #!/bin/sh
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello, Claude"},
        {"role": "assistant", "content": "Hello!"},
        {"role": "user", "content": "Can you describe LLMs to me?"}

      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' \
    --message '{role: assistant, content: "Hello!"}' \
    --message '{role: user, content: "Can you describe LLMs to me?"}'
  ```

  ```python Python
  message = anthropic.Anthropic().messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {"role": "user", "content": "Hello, Claude"},
          {"role": "assistant", "content": "Hello!"},
          {"role": "user", "content": "Can you describe LLMs to me?"},
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const message = await anthropic.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "Hello, Claude" },
      { role: "assistant", content: "Hello!" },
      { role: "user", content: "Can you describe LLMs to me?" }
    ]
  });
  console.log(message);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages =
      [
          new() { Role = Role.User, Content = "Hello, Claude" },
          new() { Role = Role.Assistant, Content = "Hello!" },
          new() { Role = Role.User, Content = "Can you describe LLMs to me?" }
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  		anthropic.NewAssistantMessage(anthropic.NewTextBlock("Hello!")),
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Can you describe LLMs to me?")),
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
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(1024L)
      .addUserMessage("Hello, Claude")
      .addAssistantMessage("Hello!")
      .addUserMessage("Can you describe LLMs to me?")
      .build();

  Message response = client.messages().create(params);
  System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Hello, Claude'],
          ['role' => 'assistant', 'content' => 'Hello!'],
          ['role' => 'user', 'content' => 'Can you describe LLMs to me?'],
      ],
      model: 'claude-opus-5',
  );

  echo json_encode($message, JSON_PRETTY_PRINT), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "Hello, Claude" },
      { role: "assistant", content: "Hello!" },
      { role: "user", content: "Can you describe LLMs to me?" }
    ]
  )
  puts message
  ```
</CodeGroup>

```json Output
{
  "id": "msg_018gCsTGsXkYJVqYPxTgDHBU",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Sure, I'd be happy to provide..."
    }
  ],
  "model": "claude-opus-5",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 30,
    "output_tokens": 309
  }
}
```

### Role system dalam messages

Pada Claude Fable 5.1, [Claude Mythos 5.1](https://anthropic.com/glasswing), Claude Fable 5, [Claude Mythos 5](https://anthropic.com/glasswing), Claude Opus 4.8, dan Claude Opus 5, Anda dapat menyertakan pesan dengan `"role": "system"` setelah giliran user (tunduk pada [aturan penempatan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)) untuk menambahkan instruksi sistem baru di tengah percakapan. Pesan `system` tidak boleh menjadi entri pertama dalam `messages`. Gunakan field `system` tingkat atas untuk instruksi yang berlaku sejak awal.

Pesan sistem di tengah percakapan memiliki otoritas yang sama dengan field `system` tingkat atas, tetapi karena ditambahkan di akhir riwayat pesan, pesan tersebut tidak membatalkan prefiks yang telah di-cache sebelumnya. Gunakan field `system` tingkat atas untuk instruksi yang harus berlaku sejak giliran pertama, dan pesan sistem di tengah percakapan untuk instruksi yang baru menjadi relevan kemudian.

Lihat [Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) untuk panduan lengkapnya, termasuk cara menggabungkannya dengan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching).

## Melakukan prefill pada respons Claude

Anda dapat mengisi sebagian respons Claude terlebih dahulu (prefill) pada posisi terakhir dalam daftar pesan input. Gunakan teknik ini untuk membentuk respons Claude. Contoh berikut menggunakan `"max_tokens": 1` untuk mendapatkan satu jawaban pilihan ganda dari Claude.

<Warning>
  Prefill tidak didukung pada model Claude 4.6 dan yang lebih baru serta [Claude Mythos Preview](https://anthropic.com/glasswing). Permintaan yang menggunakan prefill dengan model-model ini akan mengembalikan error 400. Sebagai gantinya, gunakan [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) pada model yang mendukungnya, atau instruksi prompt sistem. Lihat [panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide) untuk pola migrasi.
</Warning>

<CodeGroup>
  ```bash cURL
  #!/bin/sh
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5",
      "max_tokens": 1,
      "messages": [
        {"role": "user", "content": "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae"},
        {"role": "assistant", "content": "The answer is ("}
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-sonnet-4-5
  max_tokens: 1
  messages:
    - role: user
      content: "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae"
    - role: assistant
      content: "The answer is ("
  YAML
  ```

  ```python Python
  message = anthropic.Anthropic().messages.create(
      model="claude-sonnet-4-5",
      max_tokens=1,
      messages=[
          {
              "role": "user",
              "content": "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae",
          },
          {"role": "assistant", "content": "The answer is ("},
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const message = await anthropic.messages.create({
    model: "claude-sonnet-4-5",
    max_tokens: 1,
    messages: [
      {
        role: "user",
        content: "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae"
      },
      { role: "assistant", content: "The answer is (" }
    ]
  });
  console.log(message);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet4_5,
      MaxTokens = 1,
      Messages = [
          new() { Role = Role.User, Content = "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae" },
          new() { Role = Role.Assistant, Content = "The answer is (" }
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet4_5,
  	MaxTokens: 1,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae")),
  		anthropic.NewAssistantMessage(anthropic.NewTextBlock("The answer is (")),
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
      .model(Model.CLAUDE_SONNET_4_5)
      .maxTokens(1L)
      .addUserMessage("What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae")
      .addAssistantMessage("The answer is (")
      .build();

  Message response = client.messages().create(params);
  System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1,
      messages: [
          ['role' => 'user', 'content' => 'What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae'],
          ['role' => 'assistant', 'content' => 'The answer is ('],
      ],
      model: 'claude-sonnet-4-5',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-sonnet-4-5",
    max_tokens: 1,
    messages: [
      {
        role: "user",
        content: "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae"
      },
      { role: "assistant", content: "The answer is (" }
    ]
  )
  puts message
  ```
</CodeGroup>

```json Output
{
  "id": "msg_01Q8Faay6S7QPTvEUUQARt7h",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "C"
    }
  ],
  "model": "claude-sonnet-4-5",
  "stop_reason": "max_tokens",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 42,
    "output_tokens": 1
  }
}
```

## Vision

Claude dapat membaca teks maupun gambar dalam permintaan. Anda dapat menyediakan gambar menggunakan tipe sumber `base64`, `url`, atau `file`. Tipe sumber `file` mereferensikan gambar yang diunggah melalui [Files API](https://platform.claude.com/docs/id/build-with-claude/files). Tipe media yang didukung adalah `image/jpeg`, `image/png`, `image/gif`, dan `image/webp`. Lihat [panduan vision](https://platform.claude.com/docs/id/build-with-claude/vision) untuk detail lebih lanjut.

<CodeGroup>
  ```bash cURL
  #!/bin/sh

  # Opsi 1: Gambar yang dienkode Base64
  IMAGE_URL="https://platform.claude.com/docs/images/vision-example.jpg"
  IMAGE_MEDIA_TYPE="image/jpeg"
  IMAGE_BASE64=$(curl "$IMAGE_URL" | base64 | tr -d '\n')

  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "model": "claude-opus-5",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": [
        {"type": "image", "source": {
          "type": "base64",
          "media_type": "$IMAGE_MEDIA_TYPE",
          "data": "$IMAGE_BASE64"
        }},
        {"type": "text", "text": "What is in the above image?"}
      ]}
    ]
  }
  EOF

  # Opsi 2: Gambar yang dirujuk melalui URL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": [
          {"type": "image", "source": {
            "type": "url",
            "url": "https://platform.claude.com/docs/images/vision-example.jpg"
          }},
          {"type": "text", "text": "What is in the above image?"}
        ]}
      ]
    }'
  ```

  ```bash CLI
  IMAGE_URL="https://platform.claude.com/docs/images/vision-example.jpg"

  # Opsi 1: Gambar berenkode Base64 (CLI otomatis mengenkode referensi @file biner)
  curl -s "$IMAGE_URL" -o ./vision-example.jpg

  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: image
          source:
            type: base64
            media_type: image/jpeg
            data: "@./vision-example.jpg"
        - type: text
          text: What is in the above image?
  YAML

  # Opsi 2: Gambar yang dirujuk melalui URL
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: image
          source:
            type: url
            url: $IMAGE_URL
        - type: text
          text: What is in the above image?
  YAML
  ```

  ```python Python
  import base64
  import httpx2

  # Opsi 1: Gambar yang dienkode Base64
  image_url = "https://platform.claude.com/docs/images/vision-example.jpg"
  image_media_type = "image/jpeg"
  image_data = base64.standard_b64encode(httpx2.get(image_url).content).decode("utf-8")

  message = anthropic.Anthropic().messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "image",
                      "source": {
                          "type": "base64",
                          "media_type": image_media_type,
                          "data": image_data,
                      },
                  },
                  {"type": "text", "text": "What is in the above image?"},
              ],
          }
      ],
  )
  print(message)

  # Opsi 2: Gambar yang direferensikan melalui URL
  message_from_url = anthropic.Anthropic().messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "image",
                      "source": {
                          "type": "url",
                          "url": "https://platform.claude.com/docs/images/vision-example.jpg",
                      },
                  },
                  {"type": "text", "text": "What is in the above image?"},
              ],
          }
      ],
  )
  print(message_from_url)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  // Opsi 1: Gambar yang dienkode Base64
  const imageUrl = "https://platform.claude.com/docs/images/vision-example.jpg";
  const imageMediaType = "image/jpeg";
  const imageArrayBuffer = await (await fetch(imageUrl)).arrayBuffer();
  const imageData = Buffer.from(imageArrayBuffer).toString("base64");

  const message = await anthropic.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: imageMediaType,
              data: imageData
            }
          },
          {
            type: "text",
            text: "What is in the above image?"
          }
        ]
      }
    ]
  });
  console.log(message);

  // Opsi 2: Gambar yang dirujuk melalui URL
  const messageFromUrl = await anthropic.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "url",
              url: "https://platform.claude.com/docs/images/vision-example.jpg"
            }
          },
          {
            type: "text",
            text: "What is in the above image?"
          }
        ]
      }
    ]
  });
  console.log(messageFromUrl);
  ```

  ```csharp C#
  using System.Collections.Generic;
  using System.Net.Http;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  // Opsi 1: Gambar yang dienkode Base64
  string imageUrl = "https://platform.claude.com/docs/images/vision-example.jpg";

  using HttpClient httpClient = new();
  byte[] imageBytes = await httpClient.GetByteArrayAsync(imageUrl);
  string imageData = Convert.ToBase64String(imageBytes);

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new MessageParamContent(new List<ContentBlockParam>
              {
                  new ContentBlockParam(new ImageBlockParam(
                      new ImageBlockParamSource(new Base64ImageSource()
                      {
                          Data = imageData,
                          MediaType = MediaType.ImageJpeg,
                      })
                  )),
                  new ContentBlockParam(new TextBlockParam("What is in the above image?")),
              }),
          }
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);

  // Opsi 2: Gambar yang dirujuk melalui URL
  var parametersFromUrl = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new MessageParamContent(new List<ContentBlockParam>
              {
                  new ContentBlockParam(new ImageBlockParam(
                      new ImageBlockParamSource(new UrlImageSource()
                      {
                          Url = "https://platform.claude.com/docs/images/vision-example.jpg",
                      })
                  )),
                  new ContentBlockParam(new TextBlockParam("What is in the above image?")),
              }),
          }
      ]
  };

  var messageFromUrl = await client.Messages.Create(parametersFromUrl);
  Console.WriteLine(messageFromUrl);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Opsi 1: Gambar berenkode Base64
  imageURL := "https://platform.claude.com/docs/images/vision-example.jpg"

  req, err := http.NewRequest("GET", imageURL, nil)
  if err != nil {
  	log.Fatal(err)
  }
  req.Header.Set("User-Agent", "AnthropicDocsBot/1.0")

  resp, err := http.DefaultClient.Do(req)
  if err != nil {
  	log.Fatal(err)
  }
  defer resp.Body.Close()

  imageBytes, err := io.ReadAll(resp.Body)
  if err != nil {
  	log.Fatal(err)
  }
  imageData := base64.StdEncoding.EncodeToString(imageBytes)

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewImageBlockBase64("image/jpeg", imageData),
  			anthropic.NewTextBlock("What is in the above image?"),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message)

  // Opsi 2: Gambar yang dirujuk melalui URL
  messageFromURL, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewImageBlock(anthropic.URLImageSourceParam{
  				URL: "https://platform.claude.com/docs/images/vision-example.jpg",
  			}),
  			anthropic.NewTextBlock("What is in the above image?"),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(messageFromURL)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Opsi 1: Gambar yang dienkode Base64
  String imageUrl = "https://platform.claude.com/docs/images/vision-example.jpg";

  HttpClient httpClient = HttpClient.newHttpClient();
  HttpRequest request = HttpRequest.newBuilder().uri(URI.create(imageUrl)).build();
  HttpResponse<byte[]> response = httpClient.send(request, HttpResponse.BodyHandlers.ofByteArray());
  String imageData = Base64.getEncoder().encodeToString(response.body());

  List<ContentBlockParam> base64Content = List.of(
      ContentBlockParam.ofImage(
          ImageBlockParam.builder()
              .source(Base64ImageSource.builder()
                  .data(imageData)
                  .mediaType(Base64ImageSource.MediaType.IMAGE_JPEG)
                  .build())
              .build()),
      ContentBlockParam.ofText(
          TextBlockParam.builder()
              .text("What is in the above image?")
              .build())
  );

  Message message = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .addUserMessageOfBlockParams(base64Content)
          .build());
  System.out.println(message);

  // Opsi 2: Gambar yang dirujuk melalui URL
  List<ContentBlockParam> urlContent = List.of(
      ContentBlockParam.ofImage(
          ImageBlockParam.builder()
              .source(UrlImageSource.builder()
                  .url("https://platform.claude.com/docs/images/vision-example.jpg")
                  .build())
              .build()),
      ContentBlockParam.ofText(
          TextBlockParam.builder()
              .text("What is in the above image?")
              .build())
  );

  Message messageFromUrl = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .addUserMessageOfBlockParams(urlContent)
          .build());
  System.out.println(messageFromUrl);
  ```

  ```php PHP
  $client = new Client();

  // Opsi 1: Gambar yang dienkode Base64
  $image_url = 'https://platform.claude.com/docs/images/vision-example.jpg';
  $image_media_type = "image/jpeg";
  $image_data = base64_encode(file_get_contents($image_url));

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'image',
                      'source' => [
                          'type' => 'base64',
                          'media_type' => $image_media_type,
                          'data' => $image_data,
                      ],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What is in the above image?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-5',
  );
  echo $message;

  // Opsi 2: Gambar yang direferensikan melalui URL
  $message_from_url = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'image',
                      'source' => [
                          'type' => 'url',
                          'url' => 'https://platform.claude.com/docs/images/vision-example.jpg',
                      ],
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What is in the above image?',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-5',
  );
  echo $message_from_url;
  ```

  ```ruby Ruby
  require "base64"
  require "net/http"

  client = Anthropic::Client.new

  # Opsi 1: Gambar yang dienkode Base64
  image_url = "https://platform.claude.com/docs/images/vision-example.jpg"
  image_media_type = "image/jpeg"
  image_data = Base64.strict_encode64(Net::HTTP.get(URI(image_url)))

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: image_media_type,
              data: image_data
            }
          },
          {
            type: "text",
            text: "What is in the above image?"
          }
        ]
      }
    ]
  )
  puts message

  # Opsi 2: Gambar yang dirujuk melalui URL
  message_from_url = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "url",
              url: "https://platform.claude.com/docs/images/vision-example.jpg"
            }
          },
          {
            type: "text",
            text: "What is in the above image?"
          }
        ]
      }
    ]
  )
  puts message_from_url
  ```
</CodeGroup>

```json Output
{
  "id": "msg_011CdKmWtV3oFx1C5yUbf5CY",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "This image is a beautiful minimalist/flat-design illustration of a sunset landscape. Here's what it contains:\n\n**Sky & Sun:**\n- A warm gradient sky transitioning from golden-yellow at the top to deep orange toward the horizon\n- A large pale yellow sun positioned in the upper-right area\n\n**Birds:**\n- Three small silhouetted birds flying in the upper-left portion of the sky, depicted as simple \"M\" or \"v\" shapes\n\n**Mountains:**\n- Multiple layered mountain peaks in purple and maroon tones\n- The mountains overlap to create depth, with varying shades of dusty purple and deep burgundy\n\n**Water:**\n- A dark purple body of water at the bottom of the image\n- A reflection of the sun shown as horizontal cream/peach colored lines in the center-bottom area\n\nThe overall style is clean, geometric, and uses a warm sunset color palette (oranges, yellows, purples, and maroons), giving it a peaceful, serene aesthetic typical of modern vector/flat design artwork."
    }
  ],
  "model": "claude-opus-5",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 1030,
    "output_tokens": 350
  }
}
```

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Stop reason dan fallback" icon="list" href="https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons">
    Tangani setiap nilai `stop_reason` dan tentukan apa yang harus dilakukan ketika respons berakhir.
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview">
    Berikan Claude alat untuk memanggil layanan eksternal dan API dari dalam Messages API.
  </Card>

  <Card title="Alat computer use" icon="computer" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool">
    Kendalikan lingkungan komputer desktop dengan Messages API.
  </Card>

  <Card title="Alat browser use" icon="browser" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool">
    Biarkan Claude menavigasi, membaca, dan berinteraksi dengan halaman web di browser yang Anda jalankan.
  </Card>

  <Card title="Output terstruktur" icon="code-brackets" href="https://platform.claude.com/docs/id/build-with-claude/structured-outputs">
    Dapatkan output JSON yang terjamin dan tervalidasi skema dari Claude.
  </Card>

  <Card title="Anggaran tugas" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/task-budgets">
    Tetapkan anggaran token yang bersifat anjuran di seluruh loop agentik penuh dengan `output_config.task_budget`.
  </Card>
</CardGroup>
