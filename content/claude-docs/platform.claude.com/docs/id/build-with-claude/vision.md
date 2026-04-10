---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/vision
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 810efbea69ff4b675ef14ab0062720d3228d73ff3246293123abe27abe1d37a4
---

# Vision

Kemampuan vision Claude memungkinkannya memahami dan menganalisis gambar, membuka kemungkinan menarik untuk interaksi multimodal.

---

Panduan ini menjelaskan cara bekerja dengan gambar di Claude, termasuk praktik terbaik, contoh kode, dan batasan yang perlu diperhatikan.

---

## Cara menggunakan vision

Gunakan kemampuan vision Claude melalui:

- [claude.ai](https://claude.ai/). Unggah gambar seperti Anda mengunggah file, atau seret dan lepas gambar langsung ke jendela obrolan.
- [Console Workbench](/workbench/). Tombol untuk menambahkan gambar muncul di kanan atas setiap blok pesan Pengguna.
- **Permintaan API**. Lihat contoh-contoh dalam panduan ini.

---

## Sebelum Anda mengunggah

### Dasar-dasar dan batasan

Anda dapat menyertakan beberapa gambar dalam satu permintaan: hingga 20 untuk [claude.ai](https://claude.ai/), dan hingga 600 untuk permintaan API (100 untuk model dengan jendela konteks 200k token). Claude menganalisis semua gambar yang diberikan saat merumuskan responsnya. Ini dapat membantu untuk membandingkan atau mengontraskan gambar.

Jika Anda mengirimkan gambar yang lebih besar dari 8000x8000 px, gambar tersebut akan ditolak. Jika Anda mengirimkan lebih dari 20 gambar dalam satu permintaan API, batasnya adalah 2000x2000 px.

<Note>
Meskipun API mendukung hingga 600 gambar per permintaan, [batas ukuran permintaan](/docs/id/api/overview#request-size-limits) (32&nbsp;MB untuk endpoint standar; lebih rendah di beberapa platform pihak ketiga) dapat tercapai lebih dulu. Untuk banyak gambar, pertimbangkan untuk mengunggah dengan [Files API](#files-api-image-example) dan mereferensikan dengan `file_id` agar payload permintaan tetap kecil.

Bahkan saat menggunakan Files API, permintaan dengan banyak gambar besar dapat gagal sebelum mencapai jumlah 600 gambar. Kurangi dimensi gambar atau ukuran file (misalnya, dengan downsampling) sebelum mengunggah (lihat [Evaluasi ukuran gambar](#evaluate-image-size)).
</Note>

### Evaluasi ukuran gambar

Untuk performa optimal, ubah ukuran gambar sebelum mengunggah jika terlalu besar. Jika sisi panjang gambar Anda lebih dari 1568 piksel, atau gambar Anda lebih dari ~1.600 token, gambar tersebut pertama-tama akan diperkecil, dengan mempertahankan rasio aspek, hingga berada dalam batas ukuran.

Jika gambar input Anda terlalu besar dan perlu diubah ukurannya, hal ini meningkatkan latensi [time-to-first-token](/docs/id/about-claude/glossary), tanpa manfaat pada kualitas output. Gambar yang sangat kecil di bawah 200 piksel pada sisi mana pun dapat menurunkan kualitas output.

<Tip>
  Untuk meningkatkan [time-to-first-token](/docs/id/about-claude/glossary), pertimbangkan
  untuk mengubah ukuran gambar menjadi tidak lebih dari 1,15 megapiksel (dan dalam 1568 piksel di
  kedua dimensi).
</Tip>

Berikut adalah tabel ukuran gambar maksimum yang diterima oleh API yang tidak akan diubah ukurannya untuk rasio aspek umum. Dengan Claude Sonnet 4.6, gambar-gambar ini menggunakan sekitar 1.600 token dan sekitar $4,80/1k gambar.

| Rasio aspek  | Ukuran gambar |
| ------------ | ------------- |
| 1&#58;1      | 1092x1092 px  |
| 3&#58;4      | 951x1268 px   |
| 2&#58;3      | 896x1344 px   |
| 9&#58;16     | 819x1456 px   |
| 1&#58;2      | 784x1568 px   |

### Hitung biaya gambar

Setiap gambar yang Anda sertakan dalam permintaan ke Claude dihitung terhadap penggunaan token Anda. Untuk menghitung perkiraan biaya, kalikan perkiraan jumlah token gambar dengan [harga per token model](https://claude.com/pricing) yang Anda gunakan.

Jika gambar Anda tidak perlu diubah ukurannya, Anda dapat memperkirakan jumlah token yang digunakan melalui algoritma ini: `tokens = (width px * height px)/750`

Berikut adalah contoh perkiraan tokenisasi dan biaya untuk berbagai ukuran gambar dalam batasan ukuran API berdasarkan harga per token Claude Sonnet 4.6 sebesar $3 per juta token input:

| Ukuran gambar                 | \# Token     | Biaya / gambar | Biaya / 1k gambar |
| ----------------------------- | ------------ | -------------- | ----------------- |
| 200x200 px(0,04 megapiksel)   | \~54         | \~$0,00016     | \~$0,16           |
| 1000x1000 px(1 megapiksel)    | \~1334       | \~$0,004       | \~$4,00           |
| 1092x1092 px(1,19 megapiksel) | \~1590       | \~$0,0048      | \~$4,80           |

### Memastikan kualitas gambar

Saat memberikan gambar ke Claude, perhatikan hal-hal berikut untuk hasil terbaik:

- **Format gambar**: Gunakan format gambar yang didukung: JPEG, PNG, GIF, atau WebP.
- **Kejernihan gambar**: Pastikan gambar jelas dan tidak terlalu buram atau berpiksel.
- **Teks**: Jika gambar mengandung teks penting, pastikan teks tersebut terbaca dan tidak terlalu kecil. Hindari memotong konteks visual utama hanya untuk memperbesar teks.

---

## Contoh prompt

Banyak [teknik prompting](/docs/id/build-with-claude/prompt-engineering/overview) yang bekerja dengan baik untuk interaksi berbasis teks dengan Claude juga dapat diterapkan pada prompt berbasis gambar.

Contoh-contoh ini mendemonstrasikan struktur prompt praktik terbaik yang melibatkan gambar.

<Tip>
  Sama seperti [menempatkan dokumen panjang sebelum kueri Anda](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#long-context-prompting) meningkatkan hasil dalam prompt teks, Claude bekerja paling baik ketika gambar ditempatkan sebelum teks. Gambar yang ditempatkan setelah teks atau disisipkan dengan teks tetap bekerja dengan baik, tetapi jika kasus penggunaan Anda memungkinkan, lebih baik gunakan struktur gambar-kemudian-teks.
</Tip>

### Tentang contoh prompt

Contoh-contoh berikut mendemonstrasikan cara menggunakan kemampuan vision Claude menggunakan berbagai bahasa pemrograman dan pendekatan. Anda dapat memberikan gambar ke Claude dengan tiga cara:

1. Sebagai gambar yang dikodekan base64 dalam blok konten `image`
2. Sebagai referensi URL ke gambar yang dihosting secara online
3. Menggunakan Files API (unggah sekali, gunakan berkali-kali)

Contoh prompt base64 menggunakan variabel-variabel ini:

<CodeGroup>
```bash Shell
    # Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan JSON Anda

    # Untuk gambar yang dikodekan base64, Anda perlu mengkodekan gambar terlebih dahulu
    # Contoh cara mengkodekan gambar ke base64 di bash:
    BASE64_IMAGE_DATA=$(curl -s "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg" | base64)

    # Data yang dikodekan sekarang dapat digunakan dalam panggilan API Anda
```

```python Python
import base64
import httpx

# Untuk gambar yang dikodekan base64
image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image1_media_type = "image/jpeg"
image1_data = base64.standard_b64encode(httpx.get(image1_url).content).decode("utf-8")

image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
image2_media_type = "image/jpeg"
image2_data = base64.standard_b64encode(httpx.get(image2_url).content).decode("utf-8")

# Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```

```typescript TypeScript nocheck
import axios from "axios";

// Untuk gambar yang dikodekan base64
async function getBase64Image(url: string): Promise<string> {
  const response = await axios.get(url, { responseType: "arraybuffer" });
  return Buffer.from(response.data, "binary").toString("base64");
}

// Penggunaan
async function prepareImages() {
  const imageData = await getBase64Image(
    "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
  );
  // Sekarang Anda dapat menggunakan imageData dalam panggilan API Anda
}

// Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```

```csharp C#
using System;
using System.Net.Http;
using System.Threading.Tasks;

// Untuk gambar yang dikodekan base64
async Task<string> DownloadAndEncodeImageAsync(string url)
{
    using var client = new HttpClient();
    var bytes = await client.GetByteArrayAsync(url);
    return Convert.ToBase64String(bytes);
}

// Penggunaan:
// var imageData = await DownloadAndEncodeImageAsync("https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg");
// Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```

```go Go hidelines={1..9,-8..}
package main

import (
	"encoding/base64"
	"fmt"
	"io"
	"net/http"
)

func downloadAndEncodeImage(url string) (string, error) {
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return "", err
	}
	req.Header.Set("User-Agent", "AnthropicDocsBot/1.0")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return base64.StdEncoding.EncodeToString(data), nil
}

func main() {
	imageData, err := downloadAndEncodeImage("https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg")
	if err != nil {
		panic(err)
	}
	fmt.Println(imageData[:50])
}
```

```java Java nocheck hidelines={1..7,-1}
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Base64;

public class ImageHandlingExample {

  public static void main(String[] args) throws IOException, InterruptedException {
    // Untuk gambar yang dikodekan base64
    String image1Url =
      "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
    String image1MediaType = "image/jpeg";
    String image1Data = downloadAndEncodeImage(image1Url);

    String image2Url =
      "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg";
    String image2MediaType = "image/jpeg";
    String image2Data = downloadAndEncodeImage(image2Url);

    // Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
  }

  private static String downloadAndEncodeImage(String imageUrl) throws IOException {
    try (InputStream inputStream = new URL(imageUrl).openStream()) {
      return Base64.getEncoder().encodeToString(inputStream.readAllBytes());
    }
  }
}
```

```php PHP nocheck hidelines={1}
<?php
// Untuk gambar yang dikodekan base64
function downloadAndEncodeImage($url) {
    $imageData = file_get_contents($url);
    return base64_encode($imageData);
}

$image1Url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
$image1MediaType = "image/jpeg";
$image1Data = downloadAndEncodeImage($image1Url);

// Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```

```ruby Ruby
require "base64"
require "net/http"
require "uri"

# Untuk gambar yang dikodekan base64
def download_and_encode_image(url)
  uri = URI.parse(url)
  response = Net::HTTP.get_response(uri)
  Base64.strict_encode64(response.body)
end

image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image1_media_type = "image/jpeg"
image1_data = download_and_encode_image(image1_url)

# Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```
</CodeGroup>

Berikut adalah contoh cara menyertakan gambar dalam permintaan Messages API menggunakan gambar yang dikodekan base64 dan referensi URL:

### Contoh gambar yang dikodekan base64

<CodeGroup>
    ```bash Shell hidelines={1..2}
    BASE64_IMAGE_DATA=$(curl -s "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg" | base64 | tr -d '\n')

    curl https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d @- <<EOF
    {
      "model": "claude-opus-4-6",
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
    model: claude-opus-4-6
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
    ```python Python hidelines={1..2}
    import anthropic

    image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image1_media_type = "image/png"

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-6",
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
    
    ```typescript TypeScript nocheck hidelines={1..2}
    import Anthropic from "@anthropic-ai/sdk";

    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY
    });

    async function main() {
      const message = await anthropic.messages.create({
        model: "claude-opus-4-6",
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
                  data: imageData // Data gambar yang dikodekan Base64 sebagai string
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
    }

    main();
    ```
    ```csharp C#
    using System.Collections.Generic;
    using Anthropic;
    using Anthropic.Models.Messages;

    AnthropicClient client = new();

    string imageData = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC";

    var message = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_6,
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

    	imageData := "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"

    	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus4_6,
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
    }
    ```

    
    ```java Java nocheck hidelines={1..8,-2..}
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.*;
    import java.util.List;

    public class VisionExample {

      public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();
        String imageData = ""; // Data gambar yang dikodekan Base64 sebagai string

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
              .model(Model.CLAUDE_OPUS_4_6)
              .maxTokens(1024)
              .addUserMessageOfBlockParams(contentBlockParams)
              .build()
          );

        System.out.println(message);
      }
    }
    ```
    ```php PHP hidelines={1..4}
    <?php

    use Anthropic\Client;

    $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

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
        model: 'claude-opus-4-6',
    );

    print_r($message);
    ```
    ```ruby Ruby hidelines={1..2}
    require "anthropic"

    client = Anthropic::Client.new

    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"

    message = client.messages.create(
      model: "claude-opus-4-6",
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
    ```bash Shell
    curl https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d '{
        "model": "claude-opus-4-6",
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
    model: claude-opus-4-6
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
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-6",
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
    ```typescript TypeScript hidelines={1..2}
    import Anthropic from "@anthropic-ai/sdk";

    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY
    });

    async function main() {
      const message = await anthropic.messages.create({
        model: "claude-opus-4-6",
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
    }

    main();
    ```
    ```csharp C#
    using System.Collections.Generic;
    using Anthropic;
    using Anthropic.Models.Messages;

    AnthropicClient client = new();

    var message = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_6,
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

    	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus4_6,
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
    }
    ```
    ```java Java hidelines={1..9,-2..}
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.*;
    import java.io.IOException;
    import java.util.List;

    public class VisionExample {

      public static void main(String[] args) throws IOException, InterruptedException {
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
              .model(Model.CLAUDE_OPUS_4_6)
              .maxTokens(1024)
              .addUserMessageOfBlockParams(contentBlockParams)
              .build()
          );
        System.out.println(message);
      }
    }
    ```
    ```php PHP hidelines={1..4}
    <?php

    use Anthropic\Client;

    $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

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
        model: 'claude-opus-4-6',
    );

    print_r($message);
    ```
    ```ruby Ruby hidelines={1..2}
    require "anthropic"

    client = Anthropic::Client.new

    message = client.messages.create(
      model: "claude-opus-4-6",
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
  Dalam percakapan multi-giliran dan alur kerja agentik, setiap permintaan mengirim ulang
  seluruh riwayat percakapan. Jika gambar dikodekan dalam base64, seluruh byte gambar
  disertakan dalam payload pada setiap giliran, yang dapat secara signifikan meningkatkan
  ukuran permintaan dan latensi seiring berkembangnya percakapan. Mengunggah gambar ke
  Files API dan mereferensikannya dengan `file_id` menjaga payload permintaan tetap kecil
  terlepas dari berapa banyak gambar yang terakumulasi dalam riwayat percakapan.
</Tip>

<CodeGroup>
```bash Shell hidelines={1..2}
cd "$(mktemp -d)"
curl -sSo image.jpg https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg
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
    "model": "claude-opus-4-6",
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

```bash CLI hidelines={1}
cd "$(mktemp -d)"
curl -sSo image.jpg \
  https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg

# Pertama, unggah gambar Anda ke Files API
FILE_ID=$(ant beta:files upload \
  --file ./image.jpg \
  --transform id --format yaml)

# Kemudian gunakan file_id yang dikembalikan dalam pesan Anda
ant beta:messages create \
  --beta files-api-2025-04-14 \
  --transform content --format yaml <<YAML
model: claude-opus-4-6
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

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Unggah file gambar
with open("image.jpg", "rb") as f:
    file_upload = client.beta.files.upload(file=("image.jpg", f, "image/jpeg"))

# Gunakan file yang diunggah dalam sebuah pesan
message = client.beta.messages.create(
    model="claude-opus-4-6",
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

```typescript TypeScript nocheck
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

const anthropic = new Anthropic();

async function main() {
  // Unggah file gambar
  const fileUpload = await anthropic.beta.files.upload({
    file: await toFile(fs.createReadStream("image.jpg"), undefined, { type: "image/jpeg" }),
    betas: ["files-api-2025-04-14"]
  });

  // Gunakan file yang diunggah dalam sebuah pesan
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-6",
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
}

main();
```

```csharp C# nocheck
using Anthropic;

var client = new AnthropicClient();

// Unggah file gambar
var fileUpload = await client.Beta.Files.Upload(
    new FileUploadParams { File = File.OpenRead("image.jpg") });

// Gunakan file yang diunggah dalam sebuah pesan
var response = await client.Beta.Messages.Create(
    new MessageCreateParams
    {
        Model = "claude-opus-4-6",
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

```go Go nocheck hidelines={1..12,-1}
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	// Unggah file gambar
	file, err := os.Open("image.jpg")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	fileUpload, err := client.Beta.Files.Upload(context.Background(),
		anthropic.BetaFileUploadParams{
			File:  file,
			Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
		})
	if err != nil {
		log.Fatal(err)
	}

	// Gunakan file yang diunggah dalam sebuah pesan
	message, err := client.Beta.Messages.New(context.Background(),
		anthropic.BetaMessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_6,
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
}
```

```java Java nocheck hidelines={1..2,5..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileUploadParams;
import com.anthropic.models.messages.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class ImageFilesExample {

  public static void main(String[] args) throws IOException {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Unggah file gambar
    FileMetadata file = client
      .beta()
      .files()
      .upload(
        FileUploadParams.builder().file(Files.newInputStream(Path.of("image.jpg"))).build()
      );

    // Gunakan file yang diunggah dalam sebuah pesan
    ImageBlockParam imageParam = ImageBlockParam.builder().fileSource(file.id()).build();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
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
  }
}
```

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

// Unggah file gambar
$fileUpload = $client->beta->files->upload(
    file: fopen('image.jpg', 'r'),
    betas: ['files-api-2025-04-14'],
);

// Gunakan file yang diunggah dalam sebuah pesan
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
    model: 'claude-opus-4-6',
    betas: ['files-api-2025-04-14'],
);

print_r($message->content);
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Unggah file gambar
file_upload = client.beta.files.upload(
  file: File.open("image.jpg", "rb")
)

# Gunakan file yang diunggah dalam sebuah pesan
message = client.beta.messages.create(
  model: "claude-opus-4-6",
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

Lihat [contoh Messages API](/docs/id/api/messages/create) untuk contoh kode dan detail parameter lebih lanjut.

<section title="Contoh: Satu gambar">

Sebaiknya tempatkan gambar lebih awal dalam prompt daripada pertanyaan tentang gambar tersebut atau instruksi untuk tugas yang menggunakannya.

Minta Claude untuk mendeskripsikan satu gambar.

| Peran | Konten                              |
| ----- | ----------------------------------- |
| User  | \[Image\] Describe this image. |

<Tabs>
  <Tab title="Menggunakan Base64">
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image1_media_type = "image/png"

    message = client.messages.create(
        model="claude-opus-4-6",
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
    ```
  </Tab>
  <Tab title="Menggunakan URL">
    ```python Python
    message = client.messages.create(
        model="claude-opus-4-6",
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
    ```
  </Tab>
</Tabs>

</section>
<section title="Contoh: Beberapa gambar">

Dalam situasi di mana ada beberapa gambar, perkenalkan setiap gambar dengan `Image 1:` dan `Image 2:` dan seterusnya. Anda tidak perlu baris baru di antara gambar atau antara gambar dan prompt.

Minta Claude untuk mendeskripsikan perbedaan antara beberapa gambar.
| Peran | Konten |
| ----- | ------------------------------------------------------------------------- |
| User  | Image 1: \[Image 1\] Image 2: \[Image 2\] How are these images different? |

<Tabs>
  <Tab title="Menggunakan Base64">
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image1_media_type = "image/png"
    image2_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image2_media_type = "image/png"

    message = client.messages.create(
        model="claude-opus-4-6",
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
                            "media_type": image1_media_type,
                            "data": image1_data,
                        },
                    },
                    {"type": "text", "text": "Image 2:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image2_media_type,
                            "data": image2_data,
                        },
                    },
                    {"type": "text", "text": "How are these images different?"},
                ],
            }
        ],
    )
    ```
  </Tab>
  <Tab title="Menggunakan URL">
    ```python Python
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Image 1:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                        },
                    },
                    {"type": "text", "text": "Image 2:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg",
                        },
                    },
                    {"type": "text", "text": "How are these images different?"},
                ],
            }
        ],
    )
    ```
  </Tab>
</Tabs>

</section>
<section title="Contoh: Beberapa gambar dengan system prompt">

Minta Claude untuk mendeskripsikan perbedaan antara beberapa gambar, sambil memberikan system prompt tentang cara merespons.

| Konten  |                                                                           |
| ------- | ------------------------------------------------------------------------- |
| System  | Respond only in Spanish.                                                  |
| User    | Image 1: \[Image 1\] Image 2: \[Image 2\] How are these images different? |

<Tabs>
  <Tab title="Menggunakan Base64">
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image1_media_type = "image/png"
    image2_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image2_media_type = "image/png"

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system="Respond only in Spanish.",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Image 1:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image1_media_type,
                            "data": image1_data,
                        },
                    },
                    {"type": "text", "text": "Image 2:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image2_media_type,
                            "data": image2_data,
                        },
                    },
                    {"type": "text", "text": "How are these images different?"},
                ],
            }
        ],
    )
    ```
  </Tab>
  <Tab title="Menggunakan URL">
    ```python Python
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system="Respond only in Spanish.",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Image 1:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                        },
                    },
                    {"type": "text", "text": "Image 2:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg",
                        },
                    },
                    {"type": "text", "text": "How are these images different?"},
                ],
            }
        ],
    )
    ```
  </Tab>
</Tabs>

</section>
<section title="Contoh: Empat gambar dalam dua giliran percakapan">

Kemampuan visi Claude bersinar dalam percakapan multimodal yang memadukan gambar dan teks. Anda dapat melakukan pertukaran bolak-balik yang diperpanjang dengan Claude, menambahkan gambar baru atau pertanyaan lanjutan kapan saja. Ini memungkinkan alur kerja yang kuat untuk analisis gambar iteratif, perbandingan, atau menggabungkan visual dengan pengetahuan lainnya.

Minta Claude untuk membandingkan dua gambar, lalu ajukan pertanyaan lanjutan yang membandingkan gambar pertama dengan dua gambar baru.
| Peran     | Konten |
| --------- | ------------------------------------------------------------------------------------ |
| User      | Image 1: \[Image 1\] Image 2: \[Image 2\] How are these images different? |
| Assistant | \[Claude's response\] |
| User      | Image 1: \[Image 3\] Image 2: \[Image 4\] Are these images similar to the first two? |
| Assistant | \[Claude's response\] |

Saat menggunakan API, cukup masukkan gambar baru ke dalam array Messages dalam peran `user` sebagai bagian dari struktur [percakapan multi-giliran](/docs/id/api/messages/create) standar apa pun.

</section>

---

## Keterbatasan

Meskipun kemampuan pemahaman gambar Claude adalah yang terdepan, ada beberapa keterbatasan yang perlu diperhatikan:

- **Identifikasi orang**: Claude [tidak dapat digunakan](https://www.anthropic.com/legal/aup) untuk menamai orang dalam gambar dan menolak untuk melakukannya.
- **Akurasi**: Claude mungkin berhalusinasi atau membuat kesalahan saat menginterpretasikan gambar berkualitas rendah, diputar, atau sangat kecil di bawah 200 piksel.
- **Penalaran spasial**: Kemampuan penalaran spasial Claude terbatas. Claude mungkin kesulitan dengan tugas yang memerlukan lokalisasi atau tata letak yang tepat, seperti membaca wajah jam analog atau mendeskripsikan posisi tepat bidak catur.
- **Menghitung**: Claude dapat memberikan perkiraan jumlah objek dalam gambar tetapi mungkin tidak selalu tepat, terutama dengan jumlah besar objek kecil.
- **Gambar yang dihasilkan AI**: Claude tidak mengetahui apakah sebuah gambar dihasilkan oleh AI dan mungkin salah jika ditanya. Jangan mengandalkannya untuk mendeteksi gambar palsu atau sintetis.
- **Konten tidak pantas**: Claude tidak memproses gambar yang tidak pantas atau eksplisit yang melanggar [Kebijakan Penggunaan yang Dapat Diterima](https://www.anthropic.com/legal/aup).
- **Aplikasi kesehatan**: Meskipun Claude dapat menganalisis gambar medis umum, Claude tidak dirancang untuk menginterpretasikan pemindaian diagnostik kompleks seperti CT atau MRI. Output Claude tidak boleh dianggap sebagai pengganti saran atau diagnosis medis profesional.

Selalu tinjau dan verifikasi interpretasi gambar Claude dengan cermat, terutama untuk kasus penggunaan berisiko tinggi. Jangan gunakan Claude untuk tugas yang memerlukan presisi sempurna atau analisis gambar sensitif tanpa pengawasan manusia.

---

## FAQ

  <section title="Jenis file gambar apa yang didukung Claude?">

    Claude saat ini mendukung format gambar JPEG, PNG, GIF, dan WebP, khususnya:
    - `image/jpeg`
    - `image/png`
    - `image/gif`
    - `image/webp`
  
</section>

{" "}

<section title="Bisakah Claude membaca URL gambar?">

  Ya, Claude dapat memproses gambar dari URL dengan blok sumber gambar URL dalam API.
  Cukup gunakan tipe sumber "url" alih-alih "base64" dalam permintaan API Anda.
  Contoh:
  ```json
  {
    "type": "image",
    "source": {
      "type": "url",
      "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
    }
  }
  ```

</section>

  <section title="Apakah ada batas ukuran file gambar yang dapat saya unggah?">

    Ya, ada batasnya:
    - API: Maksimum 5&nbsp;MB per gambar
    - claude.ai: Maksimum 10&nbsp;MB per gambar

    Gambar yang lebih besar dari batas ini ditolak dan mengembalikan kesalahan saat menggunakan API.

  
</section>

  <section title="Berapa banyak gambar yang dapat saya sertakan dalam satu permintaan?">

    Batas gambar adalah:
    - Messages API: Hingga 600 gambar per permintaan (100 untuk model dengan jendela konteks 200k token)
    - claude.ai: Hingga 20 gambar per giliran

    Permintaan yang melebihi batas ini ditolak dan mengembalikan kesalahan. Permintaan dengan banyak gambar besar juga mungkin gagal sebelum mencapai batas ini; lihat [Dasar-dasar dan batas](#basics-and-limits) untuk detailnya.

  
</section>

{" "}

<section title="Apakah Claude membaca metadata gambar?">

  Tidak, Claude tidak mengurai atau menerima metadata apa pun dari gambar yang diteruskan kepadanya.

</section>

{" "}

<section title="Bisakah saya menghapus gambar yang telah saya unggah?">

  Tidak. Unggahan gambar bersifat sementara dan tidak disimpan melampaui durasi permintaan API.
  Gambar yang diunggah secara otomatis dihapus setelah diproses.

</section>

{" "}

<section title="Di mana saya dapat menemukan detail tentang privasi data untuk unggahan gambar?">

  Lihat halaman kebijakan privasi Anthropic untuk informasi tentang bagaimana gambar yang diunggah
  dan data lainnya ditangani. Anthropic tidak menggunakan gambar yang diunggah untuk melatih model.

</section>

  <section title="Bagaimana jika interpretasi gambar Claude tampak salah?">

    Jika interpretasi gambar Claude tampak tidak benar:
    1. Pastikan gambar jelas, berkualitas tinggi, dan berorientasi dengan benar.
    2. Coba teknik rekayasa prompt untuk meningkatkan hasil.
    3. Jika masalah berlanjut, tandai output di claude.ai (jempol atas/bawah) atau hubungi [tim dukungan](https://support.claude.com/).

    Umpan balik Anda membantu meningkatkan Claude!

  
</section>

  <section title="Bisakah Claude menghasilkan atau mengedit gambar?">

    Tidak, Claude adalah model pemahaman gambar saja. Claude dapat menginterpretasikan dan menganalisis gambar, tetapi tidak dapat menghasilkan, memproduksi, mengedit, memanipulasi, atau membuat gambar.
  
</section>

---

## Pelajari lebih dalam tentang visi

Siap mulai membangun dengan gambar menggunakan Claude? Berikut beberapa sumber daya yang berguna:

- [Multimodal cookbook](https://platform.claude.com/cookbook/multimodal-getting-started-with-vision): Cookbook ini memiliki tips tentang [memulai dengan gambar](https://platform.claude.com/cookbook/multimodal-getting-started-with-vision) dan [teknik praktik terbaik](https://platform.claude.com/cookbook/multimodal-best-practices-for-vision) untuk memastikan kinerja kualitas tertinggi dengan gambar. Lihat bagaimana Anda dapat secara efektif memberi prompt Claude dengan gambar untuk melaksanakan tugas seperti [menginterpretasikan dan menganalisis grafik](https://platform.claude.com/cookbook/multimodal-reading-charts-graphs-powerpoints) atau [mengekstrak konten dari formulir](https://platform.claude.com/cookbook/multimodal-how-to-transcribe-text).
- [Referensi API](/docs/id/api/messages/create): Dokumentasi untuk Messages API, termasuk contoh [panggilan API yang melibatkan gambar](/docs/id/build-with-claude/working-with-messages#vision).

Jika Anda memiliki pertanyaan lain, hubungi [tim dukungan](https://support.claude.com/). Anda juga dapat bergabung dengan [komunitas pengembang](https://www.anthropic.com/discord) untuk terhubung dengan kreator lain dan mendapatkan bantuan dari para ahli Anthropic.