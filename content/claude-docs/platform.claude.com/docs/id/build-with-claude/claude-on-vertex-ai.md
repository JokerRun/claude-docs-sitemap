---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: c6ea8f967189cf76c8f3ca260c0d88e63b3a877a2d2eeaeb948a94997183c3cd
---

# Claude di Vertex AI

Model Claude dari Anthropic kini tersedia secara umum melalui [Vertex AI](https://cloud.google.com/vertex-ai).

---

Vertex API untuk mengakses Claude hampir identik dengan [Messages API](/docs/id/api/messages) dan mendukung semua opsi yang sama, dengan dua perbedaan utama:

* Di Vertex, `model` tidak dilewatkan dalam badan permintaan. Sebaliknya, itu ditentukan dalam URL endpoint Google Cloud.
* Di Vertex, `anthropic_version` dilewatkan dalam badan permintaan (bukan sebagai header), dan harus diatur ke nilai `vertex-2023-10-16`.

Vertex juga didukung oleh [client SDKs](/docs/id/api/client-sdks) resmi Anthropic. Panduan ini akan memandu Anda melalui proses membuat permintaan ke Claude di Vertex AI dalam Python atau TypeScript.

Perhatikan bahwa panduan ini mengasumsikan Anda sudah memiliki proyek GCP yang dapat menggunakan Vertex AI. Lihat [menggunakan model Claude 3 dari Anthropic](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) untuk informasi lebih lanjut tentang setup yang diperlukan, serta panduan lengkap.

## Instal SDK untuk mengakses Vertex AI

Pertama, instal [client SDK](/docs/id/api/client-sdks) Anthropic untuk bahasa pilihan Anda.

<Tabs>
<Tab title="Python">
```bash
pip install -U google-cloud-aiplatform "anthropic[vertex]"
```
</Tab>

<Tab title="TypeScript">
```bash
npm install @anthropic-ai/vertex-sdk
```
</Tab>

<Tab title="Java">
<CodeGroup>
```groovy Gradle
implementation("com.anthropic:anthropic-java-vertex:2.+")
```

```xml Maven
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>anthropic-java-vertex</artifactId>
    <version>2.13.0</version>
</dependency>
```
</CodeGroup>
</Tab>

<Tab title="Go">
```bash
go get github.com/anthropics/anthropic-sdk-go
```
</Tab>
</Tabs>

## Mengakses Vertex AI

### Ketersediaan Model

Perhatikan bahwa ketersediaan model Anthropic bervariasi menurut wilayah. Cari "Claude" di [Vertex AI Model Garden](https://cloud.google.com/model-garden) atau buka [Gunakan Claude 3](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) untuk informasi terbaru.

#### ID model API

| Model                          | ID model API Vertex AI |
| ------------------------------ | ------------------------ |
| Claude Opus 4.6                  | claude-opus-4-6 |
| Claude Sonnet 4.6              | claude-sonnet-4-6 |
| Claude Sonnet 4.5              | claude-sonnet-4-5@20250929 |
| Claude Sonnet 4                | claude-sonnet-4@20250514 |
| Claude Sonnet 3.7 <Tooltip tooltipContent="Tidak direkomendasikan sejak 28 Oktober 2025.">⚠️</Tooltip> | claude-3-7-sonnet@20250219 |
| Claude Opus 4.5                | claude-opus-4-5@20251101 |
| Claude Opus 4.1                | claude-opus-4-1@20250805 |
| Claude Opus 4                  | claude-opus-4@20250514   |
| Claude Haiku 4.5               | claude-haiku-4-5@20251001 |
| Claude Haiku 3.5 <Tooltip tooltipContent="Tidak direkomendasikan sejak 19 Desember 2025.">⚠️</Tooltip> | claude-3-5-haiku@20241022 |
| Claude Haiku 3                 | claude-3-haiku@20240307  |

### Membuat permintaan

Sebelum menjalankan permintaan, Anda mungkin perlu menjalankan `gcloud auth application-default login` untuk autentikasi dengan GCP.

Contoh berikut menunjukkan cara menghasilkan teks dari Claude di Vertex AI:
<CodeGroup>

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "global"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-6",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Hey Claude!",
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "global";

  // Goes through the standard `google-auth-library` flow.
  const client = new AnthropicVertex({
    projectId,
    region
  });

  async function main() {
    const result = await client.messages.create({
      model: "claude-opus-4-6",
      max_tokens: 100,
      messages: [
        {
          role: "user",
          content: "Hey Claude!"
        }
      ]
    });
    console.log(JSON.stringify(result, null, 2));
  }

  main();
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.vertex.backends.VertexBackend;

  public class VertexExample {

    public static void main(String[] args) {
      // Uses default Google Cloud credentials
      AnthropicClient client = AnthropicOkHttpClient.builder()
        .backend(VertexBackend.fromEnv())
        .build();

      Message message = client
        .messages()
        .create(
          MessageCreateParams.builder()
            .model("claude-opus-4-6")
            .maxTokens(100)
            .addUserMessage("Hey Claude!")
            .build()
        );

      System.out.println(message);
    }
  }
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )

  func main() {
  	// Uses default Google Cloud credentials
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-6",
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("%+v\n", message)
  }
  ```

  ```bash Shell
  MODEL_ID=claude-opus-4-6
  LOCATION=global
  PROJECT_ID=MY_PROJECT_ID

  curl \
  -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://$LOCATION-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/anthropic/models/${MODEL_ID}:streamRawPredict -d \
  '{
    "anthropic_version": "vertex-2023-10-16",
    "messages": [{
      "role": "user",
      "content": "Hey Claude!"
    }],
    "max_tokens": 100,
  }'
  ```
</CodeGroup>

Lihat [client SDKs](/docs/id/api/client-sdks) kami dan [dokumentasi Vertex AI](https://cloud.google.com/vertex-ai/docs) resmi untuk detail lebih lanjut.

Claude juga tersedia melalui [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock) dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

## Pencatatan aktivitas

Vertex menyediakan [layanan pencatatan permintaan-respons](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging) yang memungkinkan pelanggan untuk mencatat prompt dan penyelesaian yang terkait dengan penggunaan Anda.

Anthropic merekomendasikan agar Anda mencatat aktivitas Anda setidaknya pada dasar rolling 30 hari untuk memahami aktivitas Anda dan menyelidiki potensi penyalahgunaan.

<Note>
Mengaktifkan layanan ini tidak memberikan Google atau Anthropic akses apa pun ke konten Anda.
</Note>

## Dukungan fitur
Anda dapat menemukan semua fitur yang saat ini didukung di Vertex [di sini](/docs/id/api/overview).

## Endpoint global vs regional

Mulai dengan **Claude Sonnet 4.5 dan semua model masa depan**, Google Vertex AI menawarkan dua jenis endpoint:

- **Endpoint global**: Perutean dinamis untuk ketersediaan maksimal
- **Endpoint regional**: Perutean data terjamin melalui wilayah geografis tertentu

Endpoint regional mencakup premium harga 10% dibandingkan endpoint global.

<Note>
Ini berlaku untuk Claude Sonnet 4.5 dan model masa depan saja. Model yang lebih lama (Claude Sonnet 4, Opus 4, dan sebelumnya) mempertahankan struktur harga yang ada.
</Note>

### Kapan menggunakan setiap opsi

**Endpoint global (direkomendasikan):**
- Memberikan ketersediaan dan uptime maksimal
- Secara dinamis merutekan permintaan ke wilayah dengan kapasitas tersedia
- Tidak ada premium harga
- Terbaik untuk aplikasi di mana residensi data fleksibel
- Hanya mendukung lalu lintas bayar sesuai penggunaan (throughput yang disediakan memerlukan endpoint regional)

**Endpoint regional:**
- Merutekan lalu lintas melalui wilayah geografis tertentu
- Diperlukan untuk persyaratan residensi data dan kepatuhan
- Mendukung lalu lintas bayar sesuai penggunaan dan throughput yang disediakan
- Premium harga 10% mencerminkan biaya infrastruktur untuk kapasitas regional yang didedikasikan

### Implementasi

**Menggunakan endpoint global (direkomendasikan):**

Atur parameter `region` ke `"global"` saat menginisialisasi klien:

<CodeGroup>
```python Python
from anthropic import AnthropicVertex

project_id = "MY_PROJECT_ID"
region = "global"

client = AnthropicVertex(project_id=project_id, region=region)

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Hey Claude!",
        }
    ],
)
print(message)
```

```typescript TypeScript
import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

const projectId = "MY_PROJECT_ID";
const region = "global";

const client = new AnthropicVertex({
  projectId,
  region
});

const result = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 100,
  messages: [
    {
      role: "user",
      content: "Hey Claude!"
    }
  ]
});
```

```java Java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.vertex.backends.VertexBackend;

// Uses default Google Cloud credentials
AnthropicClient client = AnthropicOkHttpClient.builder()
  .backend(VertexBackend.fromEnv())
  .build();

var message = client
  .messages()
  .create(
    MessageCreateParams.builder()
      .model("claude-opus-4-6")
      .maxTokens(100)
      .addUserMessage("Hey Claude!")
      .build()
  );
```

```go Go
package main

import (
	"context"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/vertex"
)

func main() {
	// Uses default Google Cloud credentials
	client := anthropic.NewClient(
		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
	)

	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:     "claude-opus-4-6",
		MaxTokens: 100,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
		},
	})
	_ = message
}
```
</CodeGroup>

**Menggunakan endpoint regional:**

Tentukan wilayah tertentu seperti `"us-east1"` atau `"europe-west1"`:

<CodeGroup>
```python Python
from anthropic import AnthropicVertex

project_id = "MY_PROJECT_ID"
region = "us-east1"  # Specify a specific region

client = AnthropicVertex(project_id=project_id, region=region)

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Hey Claude!",
        }
    ],
)
print(message)
```

```typescript TypeScript
import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

const projectId = "MY_PROJECT_ID";
const region = "us-east1"; // Specify a specific region

const client = new AnthropicVertex({
  projectId,
  region
});

const result = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 100,
  messages: [
    {
      role: "user",
      content: "Hey Claude!"
    }
  ]
});
```

```java Java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.vertex.backends.VertexBackend;

// Uses default Google Cloud credentials with specific region
AnthropicClient client = AnthropicOkHttpClient.builder()
  .backend(
    VertexBackend.builder()
      .region("us-east1") // Specify a specific region
      .project("MY_PROJECT_ID")
      .build()
  )
  .build();

var message = client
  .messages()
  .create(
    MessageCreateParams.builder()
      .model("claude-opus-4-6")
      .maxTokens(100)
      .addUserMessage("Hey Claude!")
      .build()
  );
```

```go Go
package main

import (
	"context"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/vertex"
)

func main() {
	// Specify a specific region
	client := anthropic.NewClient(
		vertex.WithGoogleAuth(context.Background(), "us-east1", "MY_PROJECT_ID"),
	)

	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:     "claude-opus-4-6",
		MaxTokens: 100,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
		},
	})
	_ = message
}
```
</CodeGroup>

### Sumber daya tambahan

- **Harga Vertex AI Google:** [cloud.google.com/vertex-ai/generative-ai/pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- **Dokumentasi model Claude:** [Claude di Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude)
- **Posting blog Google:** [Endpoint global untuk model Claude](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai)
- **Detail harga Anthropic:** [Dokumentasi harga](/docs/id/about-claude/pricing#third-party-platform-pricing)