---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/vision
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 98f9201bfbcd0a4d21eef0ecce4ad86581e837572cdfdc9e99dbb40e70f57a6b
---

# Vision

Kemampuan vision Claude memungkinkannya untuk memahami dan menganalisis gambar, membuka kemungkinan menarik untuk interaksi multimodal.

---

Panduan ini menjelaskan cara bekerja dengan gambar di Claude, termasuk praktik terbaik, contoh kode, dan batasan yang perlu diperhatikan.

---

## Cara menggunakan vision \{#how-to-use-vision}

Gunakan kemampuan vision Claude melalui:

- [claude.ai](https://claude.ai/). Unggah gambar seperti Anda mengunggah file, atau seret dan lepas gambar langsung ke jendela chat.
- [Console Workbench](/workbench/). Tombol untuk menambahkan gambar muncul di kanan atas setiap blok pesan User.
- Permintaan API. Lihat contoh-contoh dalam panduan ini.

Beberapa gambar dapat disertakan dalam satu permintaan, yang akan dianalisis Claude secara bersamaan saat merumuskan responsnya. Ini dapat berguna untuk membandingkan atau mengontraskan gambar.

---

## Sebelum Anda mengunggah \{#before-you-upload}

### Batasan umum \{#general-limits}

Jumlah maksimal gambar per pesan atau permintaan adalah:
  - 20 per pesan di [claude.ai](https://claude.ai/).
  - 100 per permintaan di API, untuk model dengan jendela konteks 200k token.
  - 600 per permintaan di API, untuk semua model lainnya.

Dimensi maksimal per gambar adalah 8000x8000 px. Jika Anda mengirimkan lebih dari 20 gambar dalam satu permintaan API, batas ini dikurangi menjadi 2000x2000 px.

Ukuran maksimal per gambar adalah:
  - 10&nbsp;MB (dikodekan base64) saat menggunakan Claude API secara langsung.
  - 5&nbsp;MB (dikodekan base64) di Amazon Bedrock dan Vertex AI.
  - 10&nbsp;MB di [claude.ai](https://claude.ai/).

<Note>
Meskipun API mendukung hingga 600 gambar per permintaan, [batas ukuran permintaan](/docs/id/api/overview#request-size-limits) (32&nbsp;MB untuk endpoint standar; lebih rendah pada beberapa platform yang dioperasikan mitra, misalnya Amazon Bedrock dan Vertex AI) dapat tercapai terlebih dahulu. Untuk banyak gambar, pertimbangkan untuk mengunggah dengan [Files API](#files-api-image-example) dan mereferensikan melalui `file_id` agar payload permintaan tetap kecil.

Bahkan saat menggunakan Files API, permintaan dengan banyak gambar besar dapat gagal sebelum mencapai jumlah 600 gambar. Kurangi dimensi gambar atau ukuran file (misalnya, dengan downsampling) sebelum mengunggah (lihat [Mengevaluasi ukuran gambar](#evaluate-image-size)).
</Note>

### Mengevaluasi ukuran gambar \{#evaluate-image-size}

Sebuah gambar menggunakan sekitar `width * height / 750` token, di mana lebar dan tinggi dinyatakan dalam piksel.

Resolusi gambar native maksimal adalah:

- Untuk Claude Fable 5 dan Claude Mythos 5: 4784 token, dan paling banyak 2576 piksel pada sisi terpanjang.
- Untuk Claude Opus 4.8: 4784 token, dan paling banyak 2576 piksel pada sisi terpanjang.
- Untuk Claude Opus 4.7: 4784 token, dan paling banyak 2576 piksel pada sisi terpanjang.
- Untuk model lainnya: 1568 token, dan paling banyak 1568 piksel pada sisi terpanjang.

Jika gambar input Anda lebih besar dari resolusi native ini, gambar akan terlebih dahulu diubah ukurannya ke ukuran terbesar yang memungkinkan sambil mempertahankan rasio aspek. Selain itu, gambar diberi padding di sudut bawah dan kanan hingga kelipatan 28 piksel.

<Note>
Saat meminta Claude untuk menghasilkan koordinat (titik, bounding box, dll.), koordinat tersebut akan dinyatakan relatif terhadap gambar yang telah diubah ukurannya/diberi padding dan perlu diskalakan ulang/ditranslasikan di sisi klien berdasarkan dimensi asli dan dimensi yang telah diubah ukurannya.
</Note>

Untuk meminimalkan latency dan menyederhanakan alur kerja berbasis koordinat, Anda sebaiknya mengubah ukuran gambar sebelum mengunggahnya.

### Menghitung biaya gambar \{#calculate-image-costs}

Setiap gambar yang Anda sertakan dalam permintaan ke Claude dihitung terhadap penggunaan token Anda. Untuk menghitung perkiraan biaya, kalikan perkiraan jumlah token gambar yang dihitung seperti di atas dengan [harga per token dari model](https://claude.com/pricing) yang Anda gunakan.

Berikut adalah contoh perkiraan tokenisasi dan biaya untuk berbagai ukuran gambar dalam batasan ukuran API berdasarkan harga per token Claude Sonnet 4.6 sebesar $3 per juta token input:

| Ukuran gambar                 | \# Token     | Biaya / gambar | Biaya / 1k gambar |
| ----------------------------- | ------------ | -------------- | ----------------- |
| 200x200 px(0,04 megapiksel)   | \~54         | \~$0,00016     | \~$0,16           |
| 1000x1000 px(1 megapiksel)    | \~1334       | \~$0,004       | \~$4,00           |
| 1092x1092 px(1,19 megapiksel) | \~1568       | \~$0,0047      | \~$4,70           |
| 1920x1080 px(2,07 megapiksel) | \~1568       | \~$0,0047      | \~$4,70           |
| 2000x1500 px(3 megapiksel)    | \~1568       | \~$0,0047      | \~$4,70           |

Perhatikan bahwa tiga gambar terakhir diperkecil sebelum diproses.

#### Dukungan gambar resolusi tinggi \{#high-resolution-image-support-on-claude-opus-4-7}

Claude Opus 4.7 adalah model Claude pertama dengan dukungan gambar resolusi tinggi; Claude Opus 4.8, Claude Fable 5, Claude Mythos 5, dan model-model selanjutnya juga mendukungnya. Resolusi gambar maksimum adalah 2576 piksel pada sisi terpanjang, naik dari 1568 px pada model sebelumnya. Ini membuka peningkatan performa pada beban kerja yang banyak menggunakan vision dan sangat berharga untuk penggunaan komputer, pemahaman screenshot, dan analisis dokumen.

Dukungan resolusi tinggi bersifat otomatis pada Claude Opus 4.7 dan model-model selanjutnya dan tidak memerlukan header beta atau opt-in di sisi klien.

Gambar resolusi tinggi pada Claude Opus 4.7, Claude Opus 4.8, Claude Fable 5, dan Claude Mythos 5 dapat menggunakan hingga sekitar 3x lebih banyak token gambar dibandingkan model sebelumnya (4784 versus 1568 token per gambar). Jika Anda tidak memerlukan fidelitas tambahan, lakukan downsample pada gambar sebelum mengirim untuk mengontrol biaya token.

Berikut adalah ukuran gambar yang sama yang ditokenisasi untuk Claude Opus 4.7 dan Claude Opus 4.8, berdasarkan harga per token mereka sebesar $5 per juta token input:

| Ukuran gambar                 | \# Token     | Biaya / gambar | Biaya / 1k gambar |
| ----------------------------- | ------------ | -------------- | ----------------- |
| 200x200 px(0,04 megapiksel)   | \~54         | \~$0,00027     | \~$0,27           |
| 1000x1000 px(1 megapiksel)    | \~1334       | \~$0,0067      | \~$6,70           |
| 1092x1092 px(1,19 megapiksel) | \~1590       | \~$0,0080      | \~$8,00           |
| 1920x1080 px(2,07 megapiksel) | \~2765       | \~$0,014       | \~$14,00          |
| 2000x1500 px(3 megapiksel)    | \~4000       | \~$0,020       | \~$20,00          |

### Memastikan kualitas gambar \{#ensure-image-quality}

Saat memberikan gambar ke Claude, perhatikan hal-hal berikut untuk hasil terbaik:

- **Format gambar**: Gunakan format gambar yang didukung: JPEG, PNG, GIF, atau WebP.\
  Animasi tidak didukung, dan hanya frame pertama yang akan digunakan.
- **Kejelasan gambar**: Pastikan gambar jelas dan tidak terlalu buram atau pecah (pixelated).
- **Teks**: Jika gambar berisi teks penting, pastikan teks tersebut dapat dibaca dan tidak terlalu kecil. Hindari memotong konteks visual penting hanya untuk memperbesar teks.
- **Pengubahan ukuran**: Perhatikan bahwa gambar Anda mungkin diubah ukurannya jika terlalu besar (lihat di atas); ini misalnya dapat membuat teks kurang terbaca. Pertimbangkan untuk mengubah ukuran gambar Anda terlebih dahulu, memotongnya, atau keduanya.
- **Kompresi gambar**: Mengompresi gambar sebelum mengirimnya, menggunakan format lossy seperti JPEG atau WebP (mode lossy), dapat mengurangi latency dengan mengurangi ukuran permintaan. Namun, ini dapat menimbulkan artefak yang merugikan performa model, terutama ketika beberapa tahap kompresi diterapkan. Misalnya, kompresi JPEG yang berat dapat membuat teks sulit dibaca. Pastikan pengaturan kompresi Anda sesuai untuk tugas tersebut dengan memeriksa gambar aktual yang dikirim ke API.

---

## Contoh prompt \{#prompt-examples}

Banyak [teknik prompting](/docs/id/build-with-claude/prompt-engineering/overview) yang bekerja dengan baik untuk interaksi berbasis teks dengan Claude juga dapat diterapkan pada prompt berbasis gambar.

Contoh-contoh ini mendemonstrasikan struktur prompt praktik terbaik yang melibatkan gambar.

<Tip>
  Sama seperti [menempatkan dokumen panjang sebelum kueri Anda](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#long-context-prompting) meningkatkan hasil dalam prompt teks, Claude bekerja paling baik ketika gambar ditempatkan sebelum teks. Gambar yang ditempatkan setelah teks atau disisipkan di antara teks tetap berfungsi dengan baik, tetapi jika kasus penggunaan Anda memungkinkan, lebih baik gunakan struktur gambar-lalu-teks.
</Tip>

### Tentang contoh prompt \{#about-the-prompt-examples}

Contoh-contoh berikut mendemonstrasikan cara menggunakan kemampuan vision Claude menggunakan berbagai bahasa pemrograman dan pendekatan. Anda dapat memberikan gambar ke Claude dengan tiga cara:

1. Sebagai gambar yang dikodekan base64 dalam blok konten `image`
2. Sebagai referensi URL ke gambar yang di-hosting secara online
3. Menggunakan Files API (unggah sekali, gunakan berkali-kali)

<Note>
Di Amazon Bedrock dan Vertex AI, saat ini hanya sumber yang dikodekan base64 yang tersedia.
</Note>

Contoh prompt base64 menggunakan variabel-variabel ini:

<CodeGroup>
```bash cURL
    # Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan JSON Anda

    # Untuk gambar yang dienkode base64, Anda perlu mengenkode gambar terlebih dahulu
    # Contoh cara mengenkode gambar ke base64 di bash:
    BASE64_IMAGE_DATA=$(curl -s "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg" | base64)

    # Data yang telah dienkode sekarang dapat digunakan dalam panggilan API Anda
```

```python Python
import base64
import httpx

# Untuk gambar yang dienkode base64
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

// Untuk gambar yang dienkode base64
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

// Untuk gambar berbasis URL, Anda dapat menggunakan URL tersebut langsung dalam permintaan Anda
```

```csharp C#
using System;
using System.Net.Http;
using System.Threading.Tasks;

// Untuk gambar yang dienkode base64
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
    // Untuk gambar yang dienkode base64
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
// Untuk gambar yang dienkode base64
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

# Untuk gambar yang dienkode base64
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

Di bawah ini adalah contoh cara menyertakan gambar dalam permintaan Messages API menggunakan gambar yang dikodekan base64 dan referensi URL:

### Contoh gambar yang dikodekan base64 \{#base64-encoded-image-example}

<CodeGroup>
    ```bash cURL hidelines={1..2}
    BASE64_IMAGE_DATA=$(curl -s "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg" | base64 | tr -d '\n')

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
    ```python Python hidelines={1..2}
    import anthropic

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
    
    ```typescript TypeScript nocheck hidelines={1..2}
    import Anthropic from "@anthropic-ai/sdk";

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
      }
    }
    ```
    ```php PHP hidelines={1..4}
    <?php

    use Anthropic\Client;

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
    ```ruby Ruby hidelines={1..2}
    require "anthropic"

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

### Contoh gambar berbasis URL \{#url-based-image-example}

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
    ```python Python hidelines={1..2}
    import anthropic

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
    ```typescript TypeScript hidelines={1..2}
    import Anthropic from "@anthropic-ai/sdk";

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
              .model(Model.CLAUDE_OPUS_4_8)
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
    ```ruby Ruby hidelines={1..2}
    require "anthropic"

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

### Contoh gambar Files API \{#files-api-image-example}

Untuk gambar yang akan Anda gunakan berulang kali atau ketika Anda ingin menghindari overhead encoding, gunakan [Files API](/docs/id/build-with-claude/files). Unggah gambar sekali, lalu referensikan `file_id` yang dikembalikan dalam pesan berikutnya alih-alih mengirim ulang data base64.

<Tip>
  Dalam percakapan multi-turn dan alur kerja agentic, setiap permintaan mengirim
  ulang seluruh riwayat percakapan. Jika gambar dikodekan base64, seluruh byte
  gambar disertakan dalam payload pada setiap turn, yang dapat secara signifikan
  meningkatkan ukuran permintaan dan latency seiring bertambahnya percakapan.
  Mengunggah gambar ke Files API dan mereferensikannya melalui `file_id` menjaga
  payload permintaan tetap kecil terlepas dari berapa banyak gambar yang
  terakumulasi dalam riwayat percakapan.
</Tip>

<CodeGroup>
```bash cURL hidelines={1..2}
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

```bash CLI nocheck hidelines={1}
cd "$(mktemp -d)"
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

```python Python nocheck hidelines={1..2}
import anthropic

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

```typescript TypeScript nocheck
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

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

```csharp C# nocheck
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
  }
}
```

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

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

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

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

Lihat [contoh Messages API](/docs/id/api/messages/create) untuk contoh kode dan detail parameter lebih lanjut.

<section title="Contoh: Satu gambar">

Sebaiknya tempatkan gambar lebih awal dalam prompt daripada pertanyaan tentang gambar tersebut atau instruksi untuk tugas yang menggunakannya.

Minta Claude untuk mendeskripsikan satu gambar.

| Role | Konten                             |
| ---- | ---------------------------------- |
| User | \[Gambar\] Deskripsikan gambar ini. |

<Tabs>
  <Tab title="Menggunakan Base64">
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image1_media_type = "image/png"

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
    ```
  </Tab>
  <Tab title="Menggunakan URL">
    ```python Python
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
    ```
  </Tab>
</Tabs>

</section>
<section title="Contoh: Beberapa gambar">

Dalam situasi di mana terdapat beberapa gambar, perkenalkan setiap gambar dengan `Image 1:` dan `Image 2:` dan seterusnya. Anda tidak memerlukan baris baru di antara gambar atau di antara gambar dan prompt.

Minta Claude untuk mendeskripsikan perbedaan antara beberapa gambar.
| Role | Konten |
| ---- | ------------------------------------------------------------------------------- |
| User | Image 1: \[Gambar 1\] Image 2: \[Gambar 2\] Apa perbedaan antara gambar-gambar ini? |

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
<section title="Contoh: Beberapa gambar dengan prompt sistem">

Minta Claude untuk mendeskripsikan perbedaan antara beberapa gambar, sambil memberikan prompt sistem tentang cara merespons.

| Konten  |                                                                                     |
| ------- | ----------------------------------------------------------------------------------- |
| System  | Respond only in Spanish.                                                            |
| User    | Image 1: \[Gambar 1\] Image 2: \[Gambar 2\] Apa perbedaan antara gambar-gambar ini? |

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
        model="claude-opus-4-8",
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
        model="claude-opus-4-8",
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
<section title="Contoh: Empat gambar dalam dua turn percakapan">

Kemampuan vision Claude bersinar dalam percakapan multimodal yang menggabungkan gambar dan teks. Anda dapat melakukan pertukaran bolak-balik yang panjang dengan Claude, menambahkan gambar baru atau pertanyaan lanjutan kapan saja. Ini memungkinkan alur kerja yang kuat untuk analisis gambar iteratif, perbandingan, atau menggabungkan visual dengan pengetahuan lainnya.

Minta Claude untuk mengontraskan dua gambar, lalu ajukan pertanyaan lanjutan yang membandingkan gambar pertama dengan dua gambar baru.
| Role | Konten |
| --------- | ------------------------------------------------------------------------------------------- |
| User | Image 1: \[Gambar 1\] Image 2: \[Gambar 2\] Apa perbedaan antara gambar-gambar ini? |
| Assistant | \[Respons Claude\] |
| User | Image 1: \[Gambar 3\] Image 2: \[Gambar 4\] Apakah gambar-gambar ini mirip dengan dua yang pertama? |
| Assistant | \[Respons Claude\] |

Saat menggunakan API, sisipkan gambar baru ke dalam array Messages dalam role `user` sebagai bagian dari struktur [percakapan multiturn](/docs/id/api/messages/create) standar.

</section>

---

## Batasan \{#limitations}

Meskipun kemampuan pemahaman gambar Claude sangat canggih, ada beberapa batasan yang perlu diperhatikan:

- **Identifikasi orang**: Claude [tidak dapat digunakan](https://www.anthropic.com/legal/aup) untuk menyebutkan nama orang dalam gambar dan akan menolak melakukannya.
- **Akurasi**: Claude mungkin berhalusinasi atau membuat kesalahan saat menginterpretasikan gambar berkualitas rendah, terputar, atau sangat kecil di bawah 200 piksel.
- **Penalaran spasial**: Kemampuan penalaran spasial Claude terbatas. Claude mungkin kesulitan dengan tugas yang memerlukan lokalisasi atau tata letak yang presisi, seperti membaca jarum jam analog atau mendeskripsikan posisi tepat bidak catur.
- **Menghitung**: Claude dapat memberikan perkiraan jumlah objek dalam gambar tetapi mungkin tidak selalu akurat secara presisi, terutama dengan jumlah besar objek kecil.
- **Gambar yang dihasilkan AI**: Claude tidak mengetahui apakah suatu gambar dihasilkan oleh AI dan mungkin salah jika ditanya. Jangan mengandalkannya untuk mendeteksi gambar palsu atau sintetis.
- **Konten yang tidak pantas**: Claude tidak memproses gambar yang tidak pantas atau eksplisit yang melanggar [Kebijakan Penggunaan yang Dapat Diterima](https://www.anthropic.com/legal/aup).
- **Aplikasi kesehatan**: Meskipun Claude dapat menganalisis gambar medis umum, Claude tidak dirancang untuk menginterpretasikan pemindaian diagnostik kompleks seperti CT atau MRI. Output Claude tidak boleh dianggap sebagai pengganti saran atau diagnosis medis profesional.

Selalu tinjau dan verifikasi interpretasi gambar Claude dengan cermat, terutama untuk kasus penggunaan berisiko tinggi. Jangan gunakan Claude untuk tugas yang memerlukan presisi sempurna atau analisis gambar sensitif tanpa pengawasan manusia.

---

## FAQ \{#faq}

  <section title="Jenis file gambar apa yang didukung Claude?">

    Claude saat ini mendukung format gambar JPEG, PNG, GIF, dan WebP, secara spesifik:
    - `image/jpeg`
    - `image/png`
    - `image/gif`
    - `image/webp`
  
</section>

{" "}

<section title="Bisakah Claude membaca URL gambar?">

  Ya, Claude dapat memproses gambar dari URL dengan blok sumber gambar URL di API.
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

  <section title="Apakah ada batasan ukuran file gambar yang dapat saya unggah?">

    Ya, ada batasan:
    - Claude API: Maksimum 10&nbsp;MB per gambar
    - Amazon Bedrock dan Vertex AI: Maksimum 5&nbsp;MB per gambar
    - claude.ai: Maksimum 10&nbsp;MB per gambar

    Gambar yang lebih besar dari batasan ini akan ditolak dan mengembalikan error saat menggunakan API.

    Ini adalah batasan per gambar. [Batas ukuran permintaan](/docs/id/api/overview#request-size-limits) keseluruhan (32&nbsp;MB pada Claude API; lebih rendah pada Amazon Bedrock dan Vertex AI) juga berlaku, sehingga permintaan dengan banyak gambar besar dapat melebihinya sebelum mencapai batas per gambar. Pada Claude API, unggah dengan [Files API](/docs/id/build-with-claude/files) dan referensikan melalui `file_id` agar payload permintaan tetap kecil. Files API saat ini tidak tersedia di Amazon Bedrock atau Vertex AI, jadi kurangi ukuran gambar pada platform tersebut sebagai gantinya.

  
</section>

  <section title="Berapa banyak gambar yang dapat saya sertakan dalam satu permintaan?">

    Batasan gambar adalah:
    - Messages API: Hingga 600 gambar per permintaan (100 untuk model dengan jendela konteks 200k token)
    - claude.ai: Hingga 20 gambar per turn

    Permintaan yang melebihi batasan ini akan ditolak dan mengembalikan error. Permintaan dengan banyak gambar besar juga dapat gagal sebelum mencapai batasan ini; lihat [Batasan umum](#general-limits) untuk detailnya.

  
</section>

{" "}

<section title="Apakah Claude membaca metadata gambar?">

  Tidak, Claude tidak mem-parsing atau menerima metadata apa pun dari gambar yang diberikan kepadanya.

</section>

{" "}

<section title="Bisakah saya menghapus gambar yang telah saya unggah?">

  Tidak. Unggahan gambar bersifat sementara dan tidak disimpan di luar durasi
  permintaan API. Gambar yang diunggah secara otomatis dihapus setelah
  diproses.

</section>

{" "}

<section title="Di mana saya dapat menemukan detail tentang privasi data untuk unggahan gambar?">

  Lihat halaman kebijakan privasi Anthropic untuk informasi tentang bagaimana
  gambar yang diunggah dan data lainnya ditangani. Anthropic tidak menggunakan
  gambar yang diunggah untuk melatih model.

</section>

  <section title="Bagaimana jika interpretasi gambar Claude tampak salah?">

    Jika interpretasi gambar Claude tampak tidak benar:
    1. Pastikan gambar jelas, berkualitas tinggi, dan berorientasi dengan benar.
    2. Coba teknik prompt engineering untuk meningkatkan hasil.
    3. Jika masalah berlanjut, tandai output di claude.ai (jempol ke atas/bawah) atau hubungi [tim dukungan](https://support.claude.com/).

    Umpan balik Anda membantu meningkatkan Claude!

  
</section>

  <section title="Bisakah Claude menghasilkan atau mengedit gambar?">

    Tidak, Claude hanya merupakan model pemahaman gambar. Claude dapat menginterpretasikan dan menganalisis gambar, tetapi tidak dapat menghasilkan, memproduksi, mengedit, memanipulasi, atau membuat gambar.
  
</section>

---

## Pelajari vision lebih dalam \{#dive-deeper-into-vision}

Siap untuk mulai membangun dengan gambar menggunakan Claude? Berikut beberapa sumber daya yang bermanfaat:

- [Multimodal cookbook](https://platform.claude.com/cookbook/multimodal-getting-started-with-vision): Cookbook ini memiliki tips tentang [memulai dengan gambar](https://platform.claude.com/cookbook/multimodal-getting-started-with-vision) dan [teknik praktik terbaik](https://platform.claude.com/cookbook/multimodal-best-practices-for-vision) untuk memastikan performa kualitas tertinggi dengan gambar. Lihat bagaimana Anda dapat secara efektif memberikan prompt kepada Claude dengan gambar untuk melakukan tugas seperti [menginterpretasikan dan menganalisis grafik](https://platform.claude.com/cookbook/multimodal-reading-charts-graphs-powerpoints) atau [mengekstrak konten dari formulir](https://platform.claude.com/cookbook/multimodal-how-to-transcribe-text).
- [Referensi API](/docs/id/api/messages/create): Dokumentasi untuk Messages API, termasuk contoh [panggilan API yang melibatkan gambar](/docs/id/build-with-claude/working-with-messages#vision).

Jika Anda memiliki pertanyaan lain, hubungi [tim dukungan](https://support.claude.com/). Anda juga dapat bergabung dengan [komunitas developer](https://www.anthropic.com/discord) untuk terhubung dengan kreator lain dan mendapatkan bantuan dari para ahli Anthropic.