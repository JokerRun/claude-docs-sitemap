---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 9897da3ec75fd2942b638d746ad8cd3a29c3fb03d867f2b71d2f912b189eb0e1
---

# Claude di Vertex AI

Model Claude dari Anthropic kini tersedia secara umum melalui [Vertex AI](https://cloud.google.com/vertex-ai).

---

Vertex API untuk mengakses Claude hampir identik dengan [Messages API](/docs/id/api/messages/create) dan mendukung semua opsi yang sama, dengan dua perbedaan utama:

* Di Vertex, `model` tidak diteruskan dalam badan permintaan. Sebaliknya, model ditentukan dalam URL endpoint Google Cloud.
* Di Vertex, `anthropic_version` diteruskan dalam badan permintaan (bukan sebagai header), dan harus diatur ke nilai `vertex-2023-10-16`.

Vertex juga didukung oleh [client SDKs](/docs/id/api/client-sdks) resmi Anthropic. Panduan ini memandu Anda membuat permintaan ke Claude di Vertex AI menggunakan salah satu client SDKs Anthropic.

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

<Tab title="C#">
```bash
dotnet add package Anthropic.Vertex
```
</Tab>

<Tab title="Go">
```bash
go get github.com/anthropics/anthropic-sdk-go
```
</Tab>

<Tab title="Java">
<CodeGroup>
```groovy Gradle
implementation("com.anthropic:anthropic-java-vertex:2.20.0")
```

```xml Maven
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>anthropic-java-vertex</artifactId>
    <version>2.20.0</version>
</dependency>
```

```java Java nocheck hidelines={7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.vertex.backends.VertexBackend;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;

public class BasicMessage {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.builder()
            .backend(VertexBackend.fromEnv())
            .build();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(1024L)
            .addUserMessage("What is the capital of France?")
            .build();

        Message response = client.messages().create(params);
        response.content().stream()
            .flatMap(block -> block.text().stream())
            .forEach(textBlock -> System.out.println(textBlock.text()));
    }
}
```
</CodeGroup>
</Tab>

<Tab title="PHP">
```bash
composer require anthropic-ai/sdk google/auth
```
</Tab>

<Tab title="Ruby">
```bash
# Gemfile
gem "anthropic"
gem "googleauth"
```
</Tab>
</Tabs>

## Mengakses Vertex AI

### Ketersediaan model

Perhatikan bahwa ketersediaan model Anthropic bervariasi menurut wilayah. Cari "Claude" di [Vertex AI Model Garden](https://cloud.google.com/model-garden) atau buka [Gunakan Claude 3](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) untuk informasi terbaru.

#### ID model API

| Model                          | ID model Vertex AI API |
| ------------------------------ | ------------------------ |
| Claude Opus 4.7                    | claude-opus-4-7 |
| Claude Opus 4.6                  | claude-opus-4-6 |
| Claude Sonnet 4.6              | claude-sonnet-4-6 |
| Claude Sonnet 4.5              | claude-sonnet-4-5@20250929 |
| Claude Sonnet 4 <Tooltip tooltipContent="Deprecated as of April 14, 2026. Retiring September 14, 2026.">⚠️</Tooltip> | claude-sonnet-4@20250514 |
| Claude Sonnet 3.7 <Tooltip tooltipContent="Retired as of February 19, 2026.">⚠️</Tooltip> | claude-3-7-sonnet@20250219 |
| Claude Opus 4.5                | claude-opus-4-5@20251101 |
| Claude Opus 4.1                | claude-opus-4-1@20250805 |
| Claude Opus 4 <Tooltip tooltipContent="Deprecated as of April 14, 2026. Retiring September 14, 2026.">⚠️</Tooltip> | claude-opus-4@20250514   |
| Claude Haiku 4.5               | claude-haiku-4-5@20251001 |
| Claude Haiku 3.5 <Tooltip tooltipContent="Retired as of February 19, 2026.">⚠️</Tooltip> | claude-3-5-haiku@20241022 |
| Claude Haiku 3 <Tooltip tooltipContent="Deprecated as of February 19, 2026. Retiring April 19, 2026.">⚠️</Tooltip> | claude-3-haiku@20240307  |

### Membuat permintaan

Sebelum menjalankan permintaan, Anda mungkin perlu menjalankan `gcloud auth application-default login` untuk autentikasi dengan GCP.

Contoh berikut menunjukkan cara menghasilkan teks dari Claude di Vertex AI:
<CodeGroup>

  
  ```bash Shell nocheck
  MODEL_ID=claude-opus-4-7
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

  ```bash CLI
  # The ant CLI does not yet support Vertex AI.
  ```

  
  ```python Python nocheck
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "global"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-7",
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

  
  ```typescript TypeScript nocheck
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
      model: "claude-opus-4-7",
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

  
  ```csharp C# nocheck
  using Anthropic;
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "global";

  var client = new AnthropicClient
  {
      Backend = new VertexBackend(projectId, region)
  };

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_7,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  
  ```go Go nocheck hidelines={1..2,10..11,-1}
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
  		Model:     "claude-opus-4-7",
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

  
  ```java Java nocheck hidelines={6..9,-2..}
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
            .model("claude-opus-4-7")
            .maxTokens(100)
            .addUserMessage("Hey Claude!")
            .build()
        );

      System.out.println(message);
    }
  }
  ```

  
  ```php PHP nocheck
  <?php

  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      location: 'global',
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      model: 'claude-opus-4-7',
  );
  echo $message->content[0]->text;
  ```

  
  ```ruby Ruby nocheck
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-4-7",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

Lihat [client SDKs](/docs/id/api/client-sdks) dan [dokumentasi Vertex AI](https://cloud.google.com/vertex-ai/docs) resmi untuk detail lebih lanjut.

Claude juga tersedia melalui [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock) dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

## Pencatatan aktivitas

Vertex menyediakan [layanan pencatatan permintaan-respons](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging) yang memungkinkan pelanggan untuk mencatat prompt dan penyelesaian yang terkait dengan penggunaan Anda.

Anthropic merekomendasikan agar Anda mencatat aktivitas Anda setidaknya pada dasar rolling 30 hari untuk memahami aktivitas Anda dan menyelidiki potensi penyalahgunaan.

<Note>
Mengaktifkan layanan ini tidak memberikan Google atau Anthropic akses apa pun ke konten Anda.
</Note>

## Dukungan fitur
Untuk semua fitur yang saat ini didukung di Vertex AI, lihat [ringkasan fitur API](/docs/id/api/overview).

### Jendela konteks

Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6 memiliki [jendela konteks 1M-token](/docs/id/build-with-claude/context-windows) di Vertex AI. Model Claude lainnya, termasuk Sonnet 4.5 dan Sonnet 4 (deprecated), memiliki jendela konteks 200k-token.

Vertex AI membatasi payload permintaan hingga 30 MB. Saat mengirim dokumen besar atau banyak gambar, Anda mungkin mencapai batas ini sebelum batas token.

## Endpoint global, multi-region, dan regional

Google Vertex AI menawarkan tiga jenis endpoint:

- **Endpoint global:** Perutean dinamis untuk ketersediaan maksimal
- **Endpoint multi-region:** Perutean dinamis dalam area geografis (misalnya, Amerika Serikat atau Uni Eropa) untuk residensi data dengan ketersediaan tinggi
- **Endpoint regional:** Perutean data terjamin melalui wilayah geografis tertentu

Endpoint regional dan multi-region mencakup premium harga 10% di atas endpoint global.

<Note>
Ini berlaku untuk Claude Sonnet 4.5 dan model masa depan saja. Model yang lebih lama (Claude Sonnet 4 (deprecated), Opus 4 (deprecated), dan sebelumnya) mempertahankan struktur harga yang ada.
</Note>

### Kapan menggunakan setiap opsi

**Endpoint global (direkomendasikan):**
- Memberikan ketersediaan dan uptime maksimal
- Secara dinamis merutkan permintaan ke wilayah dengan kapasitas tersedia
- Tidak ada premium harga
- Terbaik untuk aplikasi di mana residensi data fleksibel
- Hanya mendukung lalu lintas bayar sesuai penggunaan (throughput yang disediakan memerlukan endpoint regional)

**Endpoint multi-region:**
- Secara dinamis merutkan permintaan di seluruh wilayah dalam area geografis (saat ini `us` dan `eu`)
- Berguna ketika Anda memerlukan residensi data dalam geografi yang luas tetapi menginginkan ketersediaan lebih tinggi daripada satu wilayah
- Premium harga 10% di atas endpoint global
- Hanya mendukung lalu lintas bayar sesuai penggunaan (throughput yang disediakan memerlukan endpoint regional)

**Endpoint regional:**
- Merutkan lalu lintas melalui wilayah geografis tertentu
- Diperlukan untuk residensi data satu wilayah, mandat kepatuhan ketat, atau throughput yang disediakan
- Mendukung lalu lintas bayar sesuai penggunaan dan throughput yang disediakan
- Premium harga 10% mencerminkan biaya infrastruktur untuk kapasitas regional yang didedikasikan

### Implementasi

**Menggunakan endpoint global (direkomendasikan):**

Atur parameter `region` ke `"global"` saat menginisialisasi klien:

<CodeGroup>

```bash CLI
# The ant CLI does not yet support Vertex AI.
```

```python Python nocheck
from anthropic import AnthropicVertex

project_id = "MY_PROJECT_ID"
region = "global"

client = AnthropicVertex(project_id=project_id, region=region)

message = client.messages.create(
    model="claude-opus-4-7",
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

```typescript TypeScript nocheck
import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

const projectId = "MY_PROJECT_ID";
const region = "global";

const client = new AnthropicVertex({
  projectId,
  region
});

const result = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 100,
  messages: [
    {
      role: "user",
      content: "Hey Claude!"
    }
  ]
});
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Messages;
using Anthropic.Vertex;

var projectId = "MY_PROJECT_ID";
var region = "global";

var client = new AnthropicClient
{
    Backend = new VertexBackend(projectId, region)
};

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 100,
    Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
```

```go Go nocheck hidelines={1..2,9..10,-1}
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
		Model:     "claude-opus-4-7",
		MaxTokens: 100,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
		},
	})
	_ = message
}
```

```java Java nocheck
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
      .model("claude-opus-4-7")
      .maxTokens(100)
      .addUserMessage("Hey Claude!")
      .build()
  );
```

```php PHP nocheck
<?php

use Anthropic\Vertex;

$client = Vertex\Client::fromEnvironment(
    location: 'global',
    projectId: 'MY_PROJECT_ID',
);

$message = $client->messages->create(
    maxTokens: 100,
    messages: [
        ['role' => 'user', 'content' => 'Hey Claude!']
    ],
    model: 'claude-opus-4-7',
);

echo $message->content[0]->text;
```

```ruby Ruby nocheck
require "anthropic"

client = Anthropic::VertexClient.new(
  region: "global",
  project_id: "MY_PROJECT_ID"
)

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 100,
  messages: [{role: "user", content: "Hey Claude!"}]
)

puts message.content.first.text
```
</CodeGroup>

**Menggunakan endpoint multi-region:**

Atur parameter `region` ke pengidentifikasi multi-region: `"us"` untuk Amerika Serikat atau `"eu"` untuk Uni Eropa. SDK merutkan permintaan ke endpoint multi-region yang sesuai (`https://aiplatform.us.rep.googleapis.com` atau `https://aiplatform.eu.rep.googleapis.com`), yang secara dinamis menyeimbangkan lalu lintas di seluruh wilayah dalam geografi tersebut.

<CodeGroup>

```python Python nocheck
from anthropic import AnthropicVertex

project_id = "MY_PROJECT_ID"
region = "us"  # Multi-region identifier: "us" or "eu"

client = AnthropicVertex(project_id=project_id, region=region)

message = client.messages.create(
    model="claude-opus-4-7",
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

```typescript TypeScript nocheck
import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

const projectId = "MY_PROJECT_ID";
const region = "us"; // Multi-region identifier: "us" or "eu"

const client = new AnthropicVertex({
  projectId,
  region
});

const result = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 100,
  messages: [
    {
      role: "user",
      content: "Hey Claude!"
    }
  ]
});
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Messages;
using Anthropic.Vertex;

var projectId = "MY_PROJECT_ID";
var region = "us"; // Multi-region identifier: "us" or "eu"

var client = new AnthropicClient
{
    Backend = new VertexBackend(projectId, region)
};

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 100,
    Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
```

```go Go nocheck hidelines={1..2,9..10,-1}
package main

import (
	"context"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/vertex"
)

func main() {
	// Multi-region identifier: "us" or "eu"
	client := anthropic.NewClient(
		vertex.WithGoogleAuth(context.Background(), "us", "MY_PROJECT_ID"),
	)

	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 100,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
		},
	})
	_ = message
}
```

```java Java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.vertex.backends.VertexBackend;

// Multi-region identifier: "us" or "eu"
AnthropicClient client = AnthropicOkHttpClient.builder()
  .backend(
    VertexBackend.builder()
      .region("us")
      .project("MY_PROJECT_ID")
      .build()
  )
  .build();

var message = client
  .messages()
  .create(
    MessageCreateParams.builder()
      .model("claude-opus-4-7")
      .maxTokens(100)
      .addUserMessage("Hey Claude!")
      .build()
  );
```

```php PHP nocheck
<?php

use Anthropic\Vertex;

$client = Vertex\Client::fromEnvironment(
    location: 'us', // Multi-region identifier: "us" or "eu"
    projectId: 'MY_PROJECT_ID',
);

$message = $client->messages->create(
    maxTokens: 100,
    messages: [
        ['role' => 'user', 'content' => 'Hey Claude!']
    ],
    model: 'claude-opus-4-7',
);
echo $message->content[0]->text;
```

```ruby Ruby nocheck
require "anthropic"

client = Anthropic::VertexClient.new(
  region: "us", # Multi-region identifier: "us" or "eu"
  project_id: "MY_PROJECT_ID"
)

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 100,
  messages: [{role: "user", content: "Hey Claude!"}]
)

puts message.content.first.text
```
</CodeGroup>

**Menggunakan endpoint regional:**

Tentukan wilayah tertentu seperti `"us-east1"` atau `"europe-west1"`:

<CodeGroup>

```bash CLI
# The ant CLI does not yet support Vertex AI.
```

```python Python nocheck
from anthropic import AnthropicVertex

project_id = "MY_PROJECT_ID"
region = "us-east1"  # Specify a specific region

client = AnthropicVertex(project_id=project_id, region=region)

message = client.messages.create(
    model="claude-opus-4-7",
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

```typescript TypeScript nocheck
import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

const projectId = "MY_PROJECT_ID";
const region = "us-east1"; // Specify a specific region

const client = new AnthropicVertex({
  projectId,
  region
});

const result = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 100,
  messages: [
    {
      role: "user",
      content: "Hey Claude!"
    }
  ]
});
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Messages;
using Anthropic.Vertex;

var projectId = "MY_PROJECT_ID";
var region = "us-east1";

AnthropicClient client = new()
{
    Backend = new VertexBackend(projectId, region)
};

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 100,
    Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
```

```go Go nocheck hidelines={1..2,9..10,-1}
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
		Model:     "claude-opus-4-7",
		MaxTokens: 100,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
		},
	})
	_ = message
}
```

```java Java nocheck
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
      .model("claude-opus-4-7")
      .maxTokens(100)
      .addUserMessage("Hey Claude!")
      .build()
  );
```

```php PHP nocheck
<?php

use Anthropic\Vertex;

$client = Vertex\Client::fromEnvironment(
    location: 'us-east1',
    projectId: 'MY_PROJECT_ID',
);

$message = $client->messages->create(
    maxTokens: 100,
    messages: [
        ['role' => 'user', 'content' => 'Hey Claude!']
    ],
    model: 'claude-opus-4-7',
);
echo $message->content[0]->text;
```

```ruby Ruby nocheck
require "anthropic"

client = Anthropic::VertexClient.new(
  region: "us-east1", # Specify a specific region
  project_id: "MY_PROJECT_ID"
)

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 100,
  messages: [{role: "user", content: "Hey Claude!"}]
)

puts message.content.first.text
```
</CodeGroup>

<Note>
Claude Mythos Preview adalah pratinjau penelitian yang tersedia untuk pelanggan yang diundang di Google Vertex AI. Untuk informasi lebih lanjut, lihat [Project Glasswing](https://anthropic.com/glasswing).
</Note>

### Sumber daya tambahan

- **Harga Google Vertex AI:** [cloud.google.com/vertex-ai/generative-ai/pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- **Dokumentasi model Claude:** [Claude di Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude)
- **Posting blog Google:** [Global endpoint untuk model Claude](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai)
- **Detail harga Anthropic:** [Dokumentasi harga](/docs/id/about-claude/pricing#third-party-platform-pricing)