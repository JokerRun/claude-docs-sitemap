---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/vision
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: 4536d9132b0dd0f71d27c110d8fabaac73e86fcd607885cfea723b714c7ea0ed
---

# Vision

Kemampuan vision Claude memungkinkannya untuk memahami dan menganalisis gambar, membuka kemungkinan menarik untuk interaksi multimodal.

---

Panduan ini menjelaskan cara mengirim gambar ke Claude, batasan dan biaya yang berlaku, serta di mana menemukan panduan untuk [alur kerja berbasis koordinat](/docs/id/build-with-claude/vision-coordinates).

***

## Mengirim gambar ke Claude

Gunakan kemampuan vision Claude melalui:

* [claude.ai](https://claude.ai/). Unggah gambar seperti Anda mengunggah file, atau seret dan lepas gambar langsung ke jendela chat.
* [Anthropic Workbench](/workbench/). Tombol untuk menambahkan gambar muncul di kanan atas setiap blok pesan User.
* Permintaan API. Lihat contoh berikut.

Pada API, berikan gambar ke Claude sebagai blok konten `image` menggunakan salah satu dari tiga jenis sumber:

1. Gambar yang dienkode base64 yang disematkan dalam body permintaan
2. Referensi URL ke gambar yang dihosting secara online
3. `file_id` yang dikembalikan oleh [Files API](/docs/id/build-with-claude/files) (unggah sekali, referensikan berkali-kali)

<Note>
  Pada Amazon Bedrock dan Google Cloud, saat ini hanya sumber yang dienkode base64 yang tersedia.
</Note>

<Tip>
  Sama seperti [menempatkan dokumen panjang sebelum kueri Anda](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#long-context-prompting) meningkatkan hasil dalam prompt teks, Claude bekerja paling baik ketika gambar ditempatkan sebelum teks. Gambar yang ditempatkan setelah teks atau disisipkan di antara teks tetap berfungsi dengan baik, tetapi jika kasus penggunaan Anda memungkinkan, lebih baik gunakan struktur gambar-lalu-teks.
</Tip>

### Contoh gambar yang dienkode base64

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {
              "type": "base64",
              "media_type": "image/jpeg",
              "data": "$BASE64_IMAGE_DATA"
            }
          },
          {
            "type": "text",
            "text": "Describe this image."
          }
        ]
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  curl -sSo ./image.jpg \
    https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg

  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: image
          source:
            type: base64
            media_type: image/jpeg
            data: "@./image.jpg"
        - type: text
          text: Describe this image.
  YAML
  ```

  ```python Python
  image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
  image1_media_type = "image/png"

  client = anthropic.Anthropic()
  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "image",
                      "source": {
                          "type": "base64",
                          "media_type": image1_media_type,
                          "data": image1_data,
                      },
                  },
                  {"type": "text", "text": "Describe this image."},
              ],
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const message = await anthropic.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: "image/jpeg",
              data: imageData // Base64-encoded image data as string
            }
          },
          {
            type: "text",
            text: "Describe this image."
          }
        ]
      }
    ]
  });

  console.log(message);
  ```

  ```csharp C#
  using System.Collections.Generic;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  string imageData = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC";

  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
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
                          MediaType = MediaType.ImagePng,
                      })
                  )),
                  new ContentBlockParam(new TextBlockParam("Describe this image.")),
              }),
          }
      ]
  });

  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  imageData := "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewImageBlockBase64("image/png", imageData),
  			anthropic.NewTextBlock("Describe this image."),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(message)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();
  String imageData = ""; // Base64-encoded image data as string

  List<ContentBlockParam> contentBlockParams = List.of(
    ContentBlockParam.ofImage(
      ImageBlockParam.builder()
        .source(
          Base64ImageSource.builder()
            .mediaType(Base64ImageSource.MediaType.IMAGE_JPEG)
            .data(imageData)
            .build()
        )
        .build()
    ),
    ContentBlockParam.ofText(TextBlockParam.builder().text("Describe this image.").build())
  );
  Message message = client
    .messages()
    .create(
      MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024)
        .addUserMessageOfBlockParams(contentBlockParams)
        .build()
    );

  System.out.println(message);
  ```

  ```php PHP
  $client = new Client();

  $imageData = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC";

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
                          'media_type' => 'image/png',
                          'data' => $imageData,
                      ],
                  ],
                  ['type' => 'text', 'text' => 'Describe this image.'],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: "image/png",
              data: image_data
            }
          },
          { type: "text", text: "Describe this image." }
        ]
      }
    ]
  )

  puts message
  ```
</CodeGroup>

### Contoh gambar berbasis URL

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "image",
              "source": {
                "type": "url",
                "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
              }
            },
            {
              "type": "text",
              "text": "Describe this image."
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
  messages:
    - role: user
      content:
        - type: image
          source:
            type: url
            url: https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg
        - type: text
          text: Describe this image.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "image",
                      "source": {
                          "type": "url",
                          "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                      },
                  },
                  {"type": "text", "text": "Describe this image."},
              ],
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const message = await anthropic.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "url",
              url: "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
            }
          },
          {
            type: "text",
            text: "Describe this image."
          }
        ]
      }
    ]
  });

  console.log(message);
  ```

  ```csharp C#
  using System.Collections.Generic;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
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
                          Url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                      })
                  )),
                  new ContentBlockParam(new TextBlockParam("Describe this image.")),
              }),
          }
      ]
  });

  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewImageBlock(anthropic.URLImageSourceParam{
  				URL: "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
  			}),
  			anthropic.NewTextBlock("Describe this image."),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(message)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  List<ContentBlockParam> contentBlockParams = List.of(
    ContentBlockParam.ofImage(
      ImageBlockParam.builder()
        .source(
          UrlImageSource.builder()
            .url(
              "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
            )
            .build()
        )
        .build()
    ),
    ContentBlockParam.ofText(TextBlockParam.builder().text("Describe this image.").build())
  );
  Message message = client
    .messages()
    .create(
      MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024)
        .addUserMessageOfBlockParams(contentBlockParams)
        .build()
    );
  System.out.println(message);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'image',
                      'source' => [
                          'type' => 'url',
                          'url' => 'https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg',
                      ],
                  ],
                  ['type' => 'text', 'text' => 'Describe this image.'],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "url",
              url: "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
            }
          },
          { type: "text", text: "Describe this image." }
        ]
      }
    ]
  )

  puts message
  ```
</CodeGroup>

### Contoh gambar Files API

Untuk gambar yang akan Anda gunakan berulang kali atau ketika Anda ingin menghindari overhead encoding, gunakan [Files API](/docs/id/build-with-claude/files). Unggah gambar sekali, lalu referensikan `file_id` yang dikembalikan dalam pesan berikutnya alih-alih mengirim ulang data base64.

<Tip>
  Dalam percakapan multi-giliran dan alur kerja agentic, setiap permintaan mengirim ulang seluruh riwayat percakapan. Jika gambar dienkode base64, seluruh byte gambar disertakan dalam payload pada setiap giliran, yang dapat secara signifikan meningkatkan ukuran permintaan dan latensi seiring bertambahnya percakapan. Mengunggah gambar ke Files API dan mereferensikannya dengan `file_id` menjaga payload permintaan tetap kecil terlepas dari berapa banyak gambar yang terakumulasi dalam riwayat percakapan.
</Tip>

<CodeGroup>
  ```bash cURL
  # Pertama, unggah gambar Anda ke Files API
  curl -X POST https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -F "file=@image.jpg"

  # Kemudian gunakan file_id yang dikembalikan dalam pesan Anda
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "image",
              "source": {
                "type": "file",
                "file_id": "file_abc123"
              }
            },
            {
              "type": "text",
              "text": "Describe this image."
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  curl -sSo image.jpg \
    https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg

  # Pertama, unggah gambar Anda ke Files API
  FILE_ID=$(ant beta:files upload \
    --file ./image.jpg \
    --transform id --raw-output)

  # Kemudian gunakan file_id yang dikembalikan dalam pesan Anda
  ant beta:messages create \
    --beta files-api-2025-04-14 \
    --transform content --format yaml <<YAML
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: image
          source:
            type: file
            file_id: $FILE_ID
        - type: text
          text: Describe this image.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Unggah file gambar
  with open("image.jpg", "rb") as f:
      file_upload = client.beta.files.upload(file=("image.jpg", f, "image/jpeg"))

  # Gunakan file yang diunggah dalam pesan
  message = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      betas=["files-api-2025-04-14"],
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "image",
                      "source": {"type": "file", "file_id": file_upload.id},
                  },
                  {"type": "text", "text": "Describe this image."},
              ],
          }
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  import Anthropic, { toFile } from "@anthropic-ai/sdk";
  import fs from "node:fs";

  const anthropic = new Anthropic();

  // Unggah file gambar
  const fileUpload = await anthropic.beta.files.upload({
    file: await toFile(fs.createReadStream("image.jpg"), undefined, { type: "image/jpeg" })
  });

  // Gunakan file yang diunggah dalam pesan
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    betas: ["files-api-2025-04-14"],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "file",
              file_id: fileUpload.id
            }
          },
          {
            type: "text",
            text: "Describe this image."
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  using Anthropic;

  var client = new AnthropicClient();

  // Unggah file gambar
  var fileUpload = await client.Beta.Files.Upload(
      new FileUploadParams { File = File.OpenRead("image.jpg") });

  // Gunakan file yang diunggah dalam pesan
  var response = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = "claude-opus-4-8",
          MaxTokens = 1024,
          Betas = new[] { "files-api-2025-04-14" },
          Messages = new[]
          {
              new BetaMessageParam
              {
                  Role = "user",
                  Content = new object[]
                  {
                      new
                      {
                          type = "image",
                          source = new { type = "file", file_id = fileUpload.Id }
                      },
                      new { type = "text", text = "Describe this image." }
                  }
              }
          }
      });

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Unggah file gambar
  file, err := os.Open("image.jpg")
  if err != nil {
  	log.Fatal(err)
  }
  defer file.Close()

  fileUpload, err := client.Beta.Files.Upload(context.Background(),
  	anthropic.BetaFileUploadParams{
  		File: file,
  	})
  if err != nil {
  	log.Fatal(err)
  }

  // Gunakan file yang diunggah dalam pesan
  message, err := client.Beta.Messages.New(context.Background(),
  	anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
  		Messages: []anthropic.BetaMessageParam{
  			anthropic.NewBetaUserMessage(
  				anthropic.NewBetaImageBlock(anthropic.BetaFileImageSourceParam{
  					FileID: fileUpload.ID,
  				}),
  				anthropic.NewBetaTextBlock("Describe this image."),
  			),
  		},
  	})
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(message.Content)
  ```

  ```java Java
  import com.anthropic.models.beta.files.FileMetadata;
  import com.anthropic.models.beta.files.FileUploadParams;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Unggah file gambar
      FileMetadata file = client
        .beta()
        .files()
        .upload(
          FileUploadParams.builder().file(Files.newInputStream(Path.of("image.jpg"))).build()
        );

      // Gunakan file yang diunggah dalam pesan
      ImageBlockParam imageParam = ImageBlockParam.builder().fileSource(file.id()).build();

      MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024)
        .addUserMessageOfBlockParams(
          List.of(
            ContentBlockParam.ofImage(imageParam),
            ContentBlockParam.ofText(
              TextBlockParam.builder().text("Describe this image.").build()
            )
          )
        )
        .build();

      Message message = client.messages().create(params);
      System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  // Unggah file gambar
  $fileUpload = $client->beta->files->upload(
      file: fopen('image.jpg', 'r'),
  );

  // Gunakan file yang diunggah dalam pesan
  $message = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'image',
                      'source' => ['type' => 'file', 'file_id' => $fileUpload->id],
                  ],
                  ['type' => 'text', 'text' => 'Describe this image.'],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
      betas: ['files-api-2025-04-14'],
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Unggah file gambar
  file_upload = client.beta.files.upload(
    file: File.open("image.jpg", "rb")
  )

  # Gunakan file yang diunggah dalam pesan
  message = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    betas: ["files-api-2025-04-14"],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: { type: "file", file_id: file_upload.id }
          },
          { type: "text", text: "Describe this image." }
        ]
      }
    ]
  )

  puts message.content
  ```
</CodeGroup>

Lihat [contoh Messages API](/docs/id/api/messages/create) untuk lebih banyak contoh kode dan detail parameter.

### Beberapa gambar

Anda dapat menyertakan beberapa gambar dalam satu permintaan, dan Claude menganalisisnya secara bersamaan. Ini berguna untuk membandingkan gambar, menanyakan perbedaan, atau bekerja dengan urutan seperti halaman-halaman dokumen. Saat mengirim beberapa gambar, perkenalkan masing-masing dengan label teks singkat (`Image 1:`, `Image 2:`, dan seterusnya) sehingga Anda dapat merujuknya berdasarkan nama dalam prompt Anda dan dalam giliran lanjutan.

```python Python
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Image 1:"},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC",
                    },
                },
                {"type": "text", "text": "Image 2:"},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGNgYPgPAAEDAQAIicLsAAAAAElFTkSuQmCC",
                    },
                },
                {"type": "text", "text": "How are these images different?"},
            ],
        }
    ],
)
print(message)
```

Dalam percakapan multi-giliran, tambahkan gambar baru di giliran `user` berikutnya dengan cara yang sama. Claude memiliki akses ke setiap gambar dari giliran sebelumnya, sehingga pertanyaan lanjutan seperti "Apakah ini mirip dengan dua yang pertama?" berfungsi tanpa menyertakan gambar sebelumnya lagi dalam konten giliran baru.

***

## Batasan dan biaya gambar

### Batasan permintaan

Jumlah maksimum gambar per pesan atau permintaan adalah:

* 20 per pesan di [claude.ai](https://claude.ai/).
* 100 per permintaan di API, untuk model dengan jendela konteks 200k token.
* 600 per permintaan di API, untuk semua model lainnya.

Dimensi maksimum per gambar adalah 8000x8000 px.

Jika satu permintaan API berisi lebih dari 20 gambar, batas dimensi per gambar yang lebih ketat berlaku. Pada Amazon Bedrock dan Google Cloud, blok dokumen seperti PDF juga dihitung terhadap ambang batas ini. Gambar yang melebihi batas yang lebih ketat ditolak dengan `invalid_request_error` yang pesannya mereferensikan "many-image requests" dan menyatakan batas saat ini dalam piksel. Untuk tetap di bawah batas pada semua platform, ubah ukuran setiap gambar sehingga tidak ada dimensi yang melebihi 2000 px, atau batasi permintaan hingga 20 atau kurang blok gambar dan dokumen.

Ukuran maksimum per gambar adalah:

* 10 MB (dienkode base64) saat menggunakan Claude API secara langsung.
* 5 MB (dienkode base64) pada Amazon Bedrock dan Google Cloud.
* 10 MB di [claude.ai](https://claude.ai/).

<Note>
  Meskipun API mendukung hingga 600 gambar per permintaan, [batas ukuran permintaan](/docs/id/api/overview#request-size-limits) (32 MB untuk endpoint standar; lebih rendah pada beberapa platform yang dioperasikan mitra, misalnya Amazon Bedrock dan Google Cloud) dapat tercapai terlebih dahulu. Untuk banyak gambar, pertimbangkan untuk mengunggah dengan [Files API](#files-api-image-example) dan mereferensikan dengan `file_id` untuk menjaga payload permintaan tetap kecil.

  Bahkan saat menggunakan Files API, permintaan dengan banyak gambar besar dapat gagal sebelum mencapai jumlah 600 gambar. Kurangi dimensi gambar atau ukuran file (misalnya, dengan downsampling) sebelum mengunggah (lihat [Resolusi dan biaya token](#evaluate-image-size)).
</Note>

### Format yang didukung

Claude mendukung gambar JPEG, PNG, GIF, dan WebP (`image/jpeg`, `image/png`, `image/gif`, `image/webp`). Animasi tidak didukung, dan hanya frame pertama yang digunakan.

### Resolusi dan biaya token

Claude melihat gambar dalam bentuk patch, bukan piksel. Setiap patch adalah blok gambar berukuran 28×28 piksel, yang disebut sebagai token visual. Oleh karena itu, sebuah gambar membutuhkan `⌈width / 28⌉ × ⌈height / 28⌉` token visual.

Setiap model memiliki resolusi gambar native maksimum, yang dinyatakan sebagai batas sisi panjang dan batas token visual. Gambar yang lebih besar dari salah satu batas tersebut diperkecil sebelum diproses; lihat [Cara Claude mengubah ukuran dan menambahkan padding pada gambar](/docs/id/build-with-claude/vision-coordinates#how-claude-resizes-and-pads-images) untuk aturan persisnya.

| Tingkat resolusi | Model                                                                              | Sisi panjang maks | Token visual maks |
| ---------------- | ---------------------------------------------------------------------------------- | ----------------- | ----------------- |
| Resolusi tinggi  | Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5 | 2576 px           | 4784              |
| Standar          | Semua model lainnya                                                                | 1568 px           | 1568              |

Dukungan resolusi tinggi bersifat otomatis pada model yang tercantum dan tidak memerlukan header beta atau opt-in dari sisi klien.

Tabel berikut menunjukkan biaya token visual untuk beberapa ukuran gambar pada setiap tingkat:

| Ukuran gambar                  | Token tingkat standar                                                                                                                             | Token tingkat resolusi tinggi                                                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 200x200 px (0,04 megapiksel)   | 64                                                                                                                                                | 64                                                                                                                                               |
| 1000x1000 px (1 megapiksel)    | 1296                                                                                                                                              | 1296                                                                                                                                             |
| 1092x1092 px (1,19 megapiksel) | 1521                                                                                                                                              | 1521                                                                                                                                             |
| 1920x1080 px (2,07 megapiksel) | <Tooltip tooltipContent="Melebihi batas resolusi tingkat standar; gambar diperkecil sebelum diproses, yang membatasi biaya token.">1560</Tooltip> | 2691                                                                                                                                             |
| 2000x1500 px (3 megapiksel)    | <Tooltip tooltipContent="Melebihi batas resolusi tingkat standar; gambar diperkecil sebelum diproses, yang membatasi biaya token.">1564</Tooltip> | 3888                                                                                                                                             |
| 3840x2160 px (8,29 megapiksel) | <Tooltip tooltipContent="Melebihi batas resolusi tingkat standar; gambar diperkecil sebelum diproses, yang membatasi biaya token.">1560</Tooltip> | <Tooltip tooltipContent="Melebihi batas tingkat resolusi tinggi; gambar diperkecil sebelum diproses, yang membatasi biaya token.">4784</Tooltip> |

Untuk memperkirakan biaya, kalikan jumlah token dengan [harga per token dari model](https://claude.com/pricing) yang Anda gunakan. Misalnya, pada harga Claude Haiku 4.5 sebesar $1 per juta token input (tingkat standar), gambar 1000×1000 berbiaya sekitar $1,30 per seribu gambar. Pada harga Claude Opus 4.8 sebesar $5 per juta (tingkat resolusi tinggi), gambar yang sama berbiaya sekitar $6,48 per seribu dan gambar 4K sekitar $23,92 per seribu.

Gambar resolusi tinggi dapat menggunakan hingga sekitar tiga kali lebih banyak token visual dibandingkan gambar yang sama pada model tingkat standar. Jika Anda tidak memerlukan fidelitas tambahan yang disediakan resolusi tinggi untuk penggunaan komputer, pemahaman screenshot, dan dokumen padat, lakukan downsample pada gambar sebelum mengirim untuk mengontrol biaya token. Untuk meminimalkan latensi dan menyederhanakan [alur kerja berbasis koordinat](/docs/id/build-with-claude/vision-coordinates), lebih baik ubah ukuran gambar sebelum mengunggahnya.

### Panduan kualitas gambar

Saat memberikan gambar ke Claude, perhatikan hal-hal berikut untuk hasil terbaik:

* **Kejernihan gambar:** Pastikan gambar jernih dan tidak terlalu buram atau pecah.
* **Teks:** Jika gambar berisi teks penting, pastikan teks tersebut dapat dibaca dan tidak terlalu kecil. Hindari memotong konteks visual penting hanya untuk memperbesar teks.
* **Pengubahan ukuran:** Perhatikan bahwa gambar Anda mungkin diubah ukurannya jika terlalu besar (lihat [Resolusi dan biaya token](#evaluate-image-size)); ini mungkin, misalnya, membuat teks kurang terbaca. Pertimbangkan untuk mengubah ukuran gambar Anda terlebih dahulu, memotongnya, atau keduanya.
* **Kompresi gambar:** Mengompresi gambar sebelum mengirimnya, menggunakan format lossy seperti JPEG atau WebP (mode lossy), dapat mengurangi latensi dengan mengurangi ukuran permintaan. Namun, ini dapat menimbulkan artefak yang merugikan performa model, terutama ketika beberapa tahap kompresi diterapkan. Misalnya, kompresi JPEG yang berat dapat membuat teks sulit dibaca. Pastikan pengaturan kompresi Anda sesuai untuk tugas dengan memeriksa gambar aktual yang dikirim ke API.

***

## Koordinat dan bounding box

Untuk bounding box, titik, dan koordinat piksel, lihat [Koordinat dan bounding box](/docs/id/build-with-claude/vision-coordinates). Claude mengembalikan koordinat piksel absolut relatif terhadap gambar yang dilihatnya setelah pengubahan ukuran; panduan tersebut membahas cara Claude mengubah ukuran dan menambahkan padding pada gambar serta cara mengubah ukuran terlebih dahulu atau menskalakan ulang agar koordinat selaras dengan gambar asli Anda.

***

## Keterbatasan

Meskipun kemampuan pemahaman gambar Claude sangat canggih, ada beberapa keterbatasan yang perlu diperhatikan:

* **Identifikasi orang:** Claude [tidak dapat digunakan](https://www.anthropic.com/legal/aup) untuk menyebutkan nama orang dalam gambar dan menolak untuk melakukannya.
* **Akurasi:** Claude mungkin berhalusinasi atau membuat kesalahan saat menginterpretasikan gambar berkualitas rendah, diputar, atau sangat kecil di bawah 200 piksel.
* **Penalaran spasial:** Output koordinat dan lokalisasi Claude bersifat perkiraan. Ikuti panduan di [Koordinat dan bounding box](/docs/id/build-with-claude/vision-coordinates) dan verifikasi output sebelum mengandalkannya.
* **Penghitungan:** Claude dapat memberikan perkiraan jumlah objek dalam gambar tetapi mungkin tidak selalu akurat secara presisi, terutama dengan jumlah besar objek kecil.
* **Gambar yang dihasilkan AI:** Claude tidak dapat menentukan apakah suatu gambar dihasilkan oleh AI dan mungkin salah jika ditanya. Jangan mengandalkannya untuk mendeteksi gambar palsu atau sintetis.
* **Konten yang tidak pantas:** Claude tidak memproses gambar yang tidak pantas atau eksplisit yang melanggar [Acceptable Use Policy](https://www.anthropic.com/legal/aup).
* **Aplikasi kesehatan:** Meskipun Claude dapat menganalisis gambar medis umum, Claude tidak dirancang untuk menginterpretasikan pemindaian diagnostik kompleks seperti CT atau MRI. Output Claude tidak boleh dianggap sebagai pengganti saran atau diagnosis medis profesional.

Selalu tinjau dan verifikasi interpretasi gambar Claude dengan cermat, terutama untuk kasus penggunaan berisiko tinggi. Jangan gunakan Claude untuk tugas yang memerlukan presisi sempurna atau analisis gambar sensitif tanpa pengawasan manusia.

***

## FAQ

<AccordionGroup>
  <Accordion title="Jenis file gambar apa yang didukung Claude?">
    JPEG, PNG, GIF, dan WebP. Lihat [Format yang didukung](#supported-formats).
  </Accordion>

  <Accordion title="Bisakah Claude membaca URL gambar?">
    Ya. Gunakan jenis sumber `url` alih-alih `base64` dalam blok konten `image`. Lihat [Contoh gambar berbasis URL](#url-based-image-example).
  </Accordion>

  <Accordion title="Apakah ada batasan ukuran file gambar yang dapat saya unggah?">
    Ya. Lihat [Batasan permintaan](#request-limits) untuk batas ukuran per gambar dan ukuran permintaan keseluruhan di Claude API, Amazon Bedrock, Google Cloud, dan claude.ai.
  </Accordion>

  <Accordion title="Berapa banyak gambar yang dapat saya sertakan dalam satu permintaan?">
    Hingga 600 per permintaan API (100 untuk model dengan jendela konteks 200k token) dan 20 per giliran di claude.ai. Lihat [Batasan permintaan](#request-limits) untuk detail dan batas dimensi per gambar yang lebih rendah yang berlaku di atas 20 gambar.
  </Accordion>

  <Accordion title="Apakah Claude membaca metadata gambar?">
    Tidak, Claude tidak mengurai atau menerima metadata apa pun dari gambar yang diberikan kepadanya.
  </Accordion>

  <Accordion title="Bisakah saya menghapus gambar yang telah saya unggah?">
    Tidak. Unggahan gambar bersifat sementara dan tidak disimpan di luar durasi permintaan API. Gambar yang diunggah secara otomatis dihapus setelah diproses.
  </Accordion>

  <Accordion title="Di mana saya dapat menemukan detail tentang privasi data untuk unggahan gambar?">
    Lihat halaman kebijakan privasi Anthropic untuk informasi tentang bagaimana gambar yang diunggah dan data lainnya ditangani. Anthropic tidak menggunakan gambar yang diunggah untuk melatih model.
  </Accordion>

  <Accordion title="Bagaimana jika interpretasi gambar Claude tampak salah?">
    Jika interpretasi gambar Claude tampak tidak benar:

    1. Pastikan gambar jernih, berkualitas tinggi, dan berorientasi dengan benar.
    2. Coba teknik prompt engineering untuk meningkatkan hasil.
    3. Jika masalah berlanjut, tandai output di claude.ai (jempol ke atas/bawah) atau hubungi [tim dukungan](https://support.claude.com/).

    Umpan balik Anda membantu meningkatkan Claude!
  </Accordion>

  <Accordion title="Bisakah Claude menghasilkan atau mengedit gambar?">
    Tidak, Claude hanya merupakan model pemahaman gambar. Claude dapat menginterpretasikan dan menganalisis gambar, tetapi tidak dapat menghasilkan, memproduksi, mengedit, memanipulasi, atau membuat gambar.
  </Accordion>
</AccordionGroup>

***

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Cookbook multimodal" icon="image" href="https://platform.claude.com/cookbook/multimodal-getting-started-with-vision">
    Dapatkan tips dan teknik praktik terbaik untuk tugas seperti menginterpretasikan grafik dan mengekstrak konten dari formulir.
  </Card>

  <Card title="Referensi API" icon="code" href="/docs/id/api/messages/create">
    Lihat dokumentasi Messages API, termasuk contoh panggilan API yang melibatkan gambar.
  </Card>
</CardGroup>
