---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 02367430a3574aebff196fd64b2659727a510cb6d29e722d684ad2654683ecbd
---

# Claude di Amazon Bedrock

Model Claude dari Anthropic kini tersedia secara umum melalui Amazon Bedrock.

---

<Note>
Halaman ini mencakup integrasi Amazon Bedrock yang tersedia saat ini (API `InvokeModel` dan `Converse` dengan pengenal model berversi ARN dan pengkodean event-stream AWS). Pratinjau penelitian dari penawaran yang dikelola AWS baru, dengan Messages API di `/anthropic/v1/messages` dan streaming SSE, didokumentasikan di [Claude di Amazon Bedrock (pratinjau penelitian)](/docs/id/build-with-claude/claude-in-amazon-bedrock-research-preview).
</Note>

Memanggil Claude melalui Bedrock sedikit berbeda dari cara Anda memanggil Claude saat menggunakan SDK klien Anthropic. Panduan ini memandu Anda menyelesaikan panggilan API ke Claude di Bedrock menggunakan salah satu [SDK klien](/docs/id/api/client-sdks) Anthropic.

Perhatikan bahwa panduan ini mengasumsikan Anda telah mendaftar untuk [akun AWS](https://portal.aws.amazon.com/billing/signup) dan mengonfigurasi akses pemrograman.

## Instal dan konfigurasikan AWS CLI

1. [Instal versi AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) pada versi `2.13.23` atau lebih baru
2. Konfigurasikan kredensial AWS Anda menggunakan perintah AWS configure (lihat [Konfigurasikan AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)) atau temukan kredensial Anda dengan menavigasi ke "Command line or programmatic access" dalam dasbor AWS Anda dan mengikuti petunjuk dalam modal popup.
3. Verifikasi bahwa kredensial Anda berfungsi:

```bash Shell
aws sts get-caller-identity
```

## Instal SDK untuk mengakses Bedrock

[SDK klien](/docs/id/api/client-sdks) Anthropic mendukung Bedrock. Anda juga dapat menggunakan SDK AWS seperti `boto3` secara langsung.

<Tabs>
<Tab title="Python">
```bash
pip install -U "anthropic[bedrock]"
```
</Tab>

<Tab title="TypeScript">
```bash
npm install @anthropic-ai/bedrock-sdk
```
</Tab>

<Tab title="C#">
```bash
dotnet add package Anthropic.Bedrock
```
</Tab>

<Tab title="Go">
```bash
go get github.com/anthropics/anthropic-sdk-go/bedrock
```
</Tab>

<Tab title="Java">
<CodeGroup>
```groovy Gradle
implementation("com.anthropic:anthropic-java-bedrock:2.20.0")
```

```xml Maven
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>anthropic-java-bedrock</artifactId>
    <version>2.20.0</version>
</dependency>
```

```java Java nocheck hidelines={7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.bedrock.backends.BedrockBackend;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;

public class BasicMessage {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.builder()
            .backend(BedrockBackend.fromEnv())
            .build();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
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
composer require anthropic-ai/sdk aws/aws-sdk-php
```
</Tab>

<Tab title="Ruby">
```bash
# Gemfile
gem "anthropic"
gem "aws-sdk-bedrockruntime"
```
</Tab>

<Tab title="Boto3 (Python)">
```bash
pip install boto3>=1.28.59
```
</Tab>
</Tabs>

## Mengakses Bedrock

### Berlangganan model Anthropic

Buka [AWS Console > Bedrock > Model Access](https://console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess) dan minta akses ke model Anthropic. Perhatikan bahwa ketersediaan model Anthropic bervariasi menurut wilayah. Lihat [dokumentasi AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) untuk informasi terbaru.

#### ID model API

<Note>
  Claude Opus 4.7 tersedia di AWS melalui
  [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock-research-preview),
  saat ini dalam pratinjau penelitian. Ini tidak tersedia melalui katalog model
  Bedrock standar yang didokumentasikan di halaman ini.
</Note>

| Model | ID model Bedrock dasar | `global` | `us` | `eu` | `jp` | `apac` |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Claude Opus 4.6 | anthropic.claude-opus-4-6-v1 | Ya | Ya | Ya | Ya | Ya |
| Claude Sonnet 4.6 | anthropic.claude-sonnet-4-6 | Ya | Ya | Ya | Ya | Tidak |
| Claude Sonnet 4.5 | anthropic.claude-sonnet-4-5-20250929-v1:0 | Ya | Ya | Ya | Ya | Tidak |
| Claude Sonnet 4 <Tooltip tooltipContent="Tidak direkomendasikan sejak 14 April 2026. Pensiun 14 Oktober 2026.">⚠️</Tooltip> | anthropic.claude-sonnet-4-20250514-v1:0 | Ya | Ya | Ya | Tidak | Ya |
| Claude Sonnet 3.7 <Tooltip tooltipContent="Pensiun sejak 19 Februari 2026.">⚠️</Tooltip> | anthropic.claude-3-7-sonnet-20250219-v1:0 | Tidak | Ya | Ya | Tidak | Ya |
| Claude Opus 4.5 | anthropic.claude-opus-4-5-20251101-v1:0 | Ya | Ya | Ya | Tidak | Tidak |
| Claude Opus 4.1 | anthropic.claude-opus-4-1-20250805-v1:0 | Tidak | Ya | Tidak | Tidak | Tidak |
| Claude Opus 4 <Tooltip tooltipContent="Tidak direkomendasikan sejak 14 April 2026. Pensiun 14 Oktober 2026.">⚠️</Tooltip> | anthropic.claude-opus-4-20250514-v1:0 | Tidak | Ya | Tidak | Tidak | Tidak |
| Claude Haiku 4.5 | anthropic.claude-haiku-4-5-20251001-v1:0 | Ya | Ya | Ya | Tidak | Tidak |
| Claude Haiku 3.5 <Tooltip tooltipContent="Pensiun sejak 19 Februari 2026.">⚠️</Tooltip> | anthropic.claude-3-5-haiku-20241022-v1:0 | Tidak | Ya | Tidak | Tidak | Tidak |
| Claude Haiku 3 <Tooltip tooltipContent="Tidak direkomendasikan sejak 19 Februari 2026. Pensiun 19 April 2026.">⚠️</Tooltip> | anthropic.claude-3-haiku-20240307-v1:0 | Tidak | Ya | Ya | Tidak | Ya |

Untuk informasi lebih lanjut tentang ID model regional vs global, lihat bagian [Global vs regional endpoints](#global-vs-regional-endpoints) di bawah.

### Daftar model yang tersedia

Contoh berikut menunjukkan cara mencetak daftar semua model Claude yang tersedia melalui Bedrock:

<CodeGroup>
  ```bash AWS CLI
  aws bedrock list-foundation-models --region=us-west-2 --by-provider anthropic --query "modelSummaries[*].modelId"
  ```

  
  ```python Boto3 (Python) nocheck
  import boto3

  bedrock = boto3.client(service_name="bedrock")
  response = bedrock.list_foundation_models(byProvider="anthropic")

  for summary in response["modelSummaries"]:
      print(summary["modelId"])
  ```

  
  ```typescript TypeScript nocheck
  import { BedrockClient, ListFoundationModelsCommand } from "@aws-sdk/client-bedrock";

  const client = new BedrockClient({ region: "us-west-2" });

  const command = new ListFoundationModelsCommand({ byProvider: "anthropic" });
  const response = await client.send(command);

  if (response.modelSummaries) {
    for (const summary of response.modelSummaries) {
      console.log(summary.modelId);
    }
  }
  ```

  
  ```csharp C# nocheck
  using System;
  using System.Threading.Tasks;
  using Amazon;
  using Amazon.Bedrock;
  using Amazon.Bedrock.Model;

  public class ListAnthropicModels
  {
      public static async Task Main(string[] args)
      {
          var client = new AmazonBedrockClient(RegionEndpoint.USWest2);

          var request = new ListFoundationModelsRequest
          {
              ByProvider = "anthropic"
          };

          var response = await client.ListFoundationModelsAsync(request);

          foreach (var summary in response.ModelSummaries)
          {
              Console.WriteLine(summary.ModelId);
          }
      }
  }
  ```

  
  ```go Go nocheck hidelines={1..2,11..12,-1}
  package main

  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/aws/aws-sdk-go-v2/config"
  	"github.com/aws/aws-sdk-go-v2/service/bedrock"
  )

  func main() {
  	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion("us-west-2"))
  	if err != nil {
  		log.Fatal(err)
  	}

  	client := bedrock.NewFromConfig(cfg)

  	byProvider := "anthropic"
  	response, err := client.ListFoundationModels(context.TODO(), &bedrock.ListFoundationModelsInput{
  		ByProvider: &byProvider,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for _, summary := range response.ModelSummaries {
  		fmt.Println(*summary.ModelId)
  	}
  }
  ```

  
  ```java Java nocheck hidelines={6..8,-2..}
  import software.amazon.awssdk.regions.Region;
  import software.amazon.awssdk.services.bedrock.BedrockClient;
  import software.amazon.awssdk.services.bedrock.model.ListFoundationModelsRequest;
  import software.amazon.awssdk.services.bedrock.model.ListFoundationModelsResponse;
  import software.amazon.awssdk.services.bedrock.model.FoundationModelSummary;

  public class ListAnthropicModels {
      public static void main(String[] args) {
          BedrockClient client = BedrockClient.builder()
              .region(Region.US_WEST_2)
              .build();

          ListFoundationModelsRequest request = ListFoundationModelsRequest.builder()
              .byProvider("anthropic")
              .build();

          ListFoundationModelsResponse response = client.listFoundationModels(request);

          for (FoundationModelSummary summary : response.modelSummaries()) {
              System.out.println(summary.modelId());
          }

          client.close();
      }
  }
  ```

  
  ```php PHP nocheck
  <?php

  use Aws\Bedrock\BedrockClient;

  $client = new BedrockClient([
      'region' => 'us-west-2',
      'version' => 'latest'
  ]);

  $result = $client->listFoundationModels([
      'byProvider' => 'anthropic'
  ]);

  foreach ($result['modelSummaries'] as $summary) {
      echo $summary['modelId'] . PHP_EOL;
  }
  ```

  
  ```ruby Ruby nocheck
  require "aws-sdk-bedrock"

  client = Aws::Bedrock::Client.new(region: "us-west-2")

  response = client.list_foundation_models({
    by_provider: "anthropic"
  })

  response.model_summaries.each do |summary|
    puts summary.model_id
  end
  ```
</CodeGroup>

### Membuat permintaan

Contoh berikut menunjukkan cara menghasilkan teks dari Claude di Bedrock:

<CodeGroup>
  ```bash CLI
  # CLI ant belum mendukung Amazon Bedrock.
  ```

  
  ```python Python nocheck
  from anthropic import AnthropicBedrock

  client = AnthropicBedrock(
      # Autentikasi dengan memberikan kunci di bawah atau gunakan penyedia kredensial AWS default, seperti
      # menggunakan ~/.aws/credentials atau variabel lingkungan "AWS_SECRET_ACCESS_KEY" dan "AWS_ACCESS_KEY_ID".
      aws_access_key="<access key>",
      aws_secret_key="<secret key>",
      # Kredensial sementara dapat digunakan dengan aws_session_token.
      # Baca lebih lanjut di https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
      aws_session_token="<session_token>",
      # aws_region mengubah wilayah aws tempat permintaan dibuat. Secara default, kami membaca AWS_REGION,
      # dan jika itu tidak ada, kami default ke us-east-1. Perhatikan bahwa kami tidak membaca ~/.aws/config untuk wilayah.
      aws_region="us-west-2",
  )

  message = client.messages.create(
      model="global.anthropic.claude-opus-4-6-v1",
      max_tokens=256,
      messages=[{"role": "user", "content": "Hello, world"}],
  )
  print(message.content)
  ```

  
  ```typescript TypeScript nocheck
  import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

  const client = new AnthropicBedrock({
    // Autentikasi dengan memberikan kunci di bawah atau gunakan
    // penyedia kredensial AWS default, seperti
    // ~/.aws/credentials atau variabel lingkungan "AWS_SECRET_ACCESS_KEY" dan
    // "AWS_ACCESS_KEY_ID".
    awsAccessKey: "<access key>",
    awsSecretKey: "<secret key>",

    // Kredensial sementara dapat digunakan dengan awsSessionToken.
    // Baca lebih lanjut di https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
    awsSessionToken: "<session_token>",

    // awsRegion mengubah wilayah aws tempat permintaan dibuat.
    // Secara default, kami membaca AWS_REGION, dan jika itu
    // tidak ada, kami default ke us-east-1. Perhatikan bahwa kami tidak
    // membaca ~/.aws/config untuk wilayah.
    awsRegion: "us-west-2"
  });

  async function main() {
    const message = await client.messages.create({
      model: "global.anthropic.claude-opus-4-6-v1",
      max_tokens: 256,
      messages: [{ role: "user", content: "Hello, world" }]
    });
    console.log(message);
  }
  main().catch(console.error);
  ```

  
  ```csharp C# nocheck
  using Anthropic.Bedrock;
  using Anthropic.Models.Messages;

  AnthropicBedrockClient client = new(
      await AnthropicBedrockCredentialsHelper.FromEnv()
      ?? throw new InvalidOperationException("AWS credentials not configured.")
  );

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = "global.anthropic.claude-opus-4-6-v1",
      MaxTokens = 256,
      Messages = [new() { Role = Role.User, Content = "Hello, world" }],
  });

  Console.WriteLine(
      string.Join("", response.Content
          .Where(c => c.Value is TextBlock)
          .Select(c => (c.Value as TextBlock)!.Text)));
  ```

  
  ```go Go nocheck hidelines={1..2,10..11,-1}
  package main

  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/bedrock"
  )

  func main() {
  	// Menggunakan rantai penyedia kredensial AWS default
  	client := anthropic.NewClient(
  		bedrock.WithLoadDefaultConfig(context.Background()),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "global.anthropic.claude-opus-4-6-v1",
  		MaxTokens: 256,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, world")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("%+v\n", message.Content)
  }
  ```

  
  ```java Java nocheck hidelines={6..9,-2..}
  import com.anthropic.bedrock.backends.BedrockBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;

  public class BedrockExample {

    public static void main(String[] args) {
      // Menggunakan rantai penyedia kredensial AWS default
      AnthropicClient client = AnthropicOkHttpClient.builder()
        .backend(BedrockBackend.fromEnv())
        .build();

      Message message = client
        .messages()
        .create(
          MessageCreateParams.builder()
            .model("global.anthropic.claude-opus-4-6-v1")
            .maxTokens(256)
            .addUserMessage("Hello, world")
            .build()
        );

      System.out.println(message.content());
    }
  }
  ```

  
  ```php PHP nocheck
  <?php

  use Anthropic\Bedrock;

  $client = Bedrock\Client::withCredentials(
      accessKeyId: getenv("AWS_ACCESS_KEY_ID"),
      secretAccessKey: getenv("AWS_SECRET_ACCESS_KEY"),
      region: 'us-west-2',
      securityToken: getenv("AWS_SESSION_TOKEN"),
  );

  $message = $client->messages->create(
      maxTokens: 256,
      messages: [
          ['role' => 'user', 'content' => 'Hello, world']
      ],
      model: 'global.anthropic.claude-opus-4-6-v1',
  );
  echo $message->content[0]->text;
  ```

  
  ```ruby Ruby nocheck
  require "anthropic"

  client = Anthropic::BedrockClient.new

  message = client.messages.create(
    model: "global.anthropic.claude-opus-4-6-v1",
    max_tokens: 256,
    messages: [{role: "user", content: "Hello, world"}]
  )

  puts message.content.first.text
  ```

  
  ```python Boto3 (Python) nocheck
  import boto3
  import json

  bedrock = boto3.client(service_name="bedrock-runtime")
  body = json.dumps(
      {
          "max_tokens": 256,
          "messages": [{"role": "user", "content": "Hello, world"}],
          "anthropic_version": "bedrock-2023-05-31",
      }
  )

  response = bedrock.invoke_model(
      body=body, modelId="global.anthropic.claude-opus-4-6-v1"
  )

  response_body = json.loads(response.get("body").read())
  print(response_body.get("content"))
  ```
</CodeGroup>

Lihat [SDK klien](/docs/id/api/client-sdks) untuk detail lebih lanjut, dan [dokumentasi Bedrock resmi](https://docs.aws.amazon.com/bedrock/).

### Autentikasi token pembawa

Anda dapat mengautentikasi dengan Bedrock menggunakan token pembawa alih-alih kredensial AWS. Ini berguna di lingkungan perusahaan di mana tim memerlukan akses ke Bedrock tanpa mengelola kredensial AWS, peran IAM, atau izin tingkat akun.

<Note>
Autentikasi token pembawa didukung dalam SDK C#, Go, dan Java. SDK PHP, Python, TypeScript, dan Ruby hanya menggunakan penandatanganan AWS SigV4.
</Note>

Pendekatan paling sederhana adalah mengatur variabel lingkungan `AWS_BEARER_TOKEN_BEDROCK`, yang secara otomatis terdeteksi oleh resolusi kredensial `fromEnv()`.

Untuk memberikan token secara terprogram:

<CodeGroup>

```csharp C# nocheck
using Anthropic.Bedrock;
using Anthropic.Models.Messages;

var client = new AnthropicBedrockClient(
    new AnthropicBedrockApiTokenCredentials
    {
        BearerToken = "your-bearer-token",
        Region = "us-east-1",
    }
);

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Hello!" }],
});
```

```go Go nocheck hidelines={1..2,11..12,-1}
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/bedrock"
	"github.com/aws/aws-sdk-go-v2/aws"
)

func main() {
	cfg := aws.Config{
		Region:                  "us-west-2",
		BearerAuthTokenProvider: bedrock.NewStaticBearerTokenProvider("your-bearer-token"),
	}
	client := anthropic.NewClient(
		bedrock.WithConfig(cfg),
	)

	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
		},
	})
	if err != nil {
		panic(err)
	}
	fmt.Println(message.Content[0].Text)
}
```

```java Java nocheck
import com.anthropic.bedrock.backends.BedrockBackend;
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;

// Opsi 1: Atur variabel lingkungan AWS_BEARER_TOKEN_BEDROCK dan gunakan fromEnv()
AnthropicClient client = AnthropicOkHttpClient.builder()
  .backend(BedrockBackend.fromEnv())
  .build();

// Opsi 2: Berikan token secara terprogram
client = AnthropicOkHttpClient.builder()
  .backend(BedrockBackend.builder()
    .apiKey("your-bearer-token")
    .build())
  .build();

MessageCreateParams params = MessageCreateParams.builder()
  .model("us.anthropic.claude-sonnet-4-5-20250929-v1:0")
  .maxTokens(1024)
  .addUserMessage("Hello!")
  .build();

client.messages().create(params).content().stream()
  .flatMap(block -> block.text().stream())
  .forEach(textBlock -> System.out.println(textBlock.text()));
```

</CodeGroup>

## Pencatatan aktivitas

Bedrock menyediakan [layanan pencatatan invokasi](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) yang memungkinkan pelanggan untuk mencatat prompt dan penyelesaian yang terkait dengan penggunaan Anda.

Anthropic merekomendasikan agar Anda mencatat aktivitas Anda setidaknya pada dasar 30 hari yang bergulir untuk memahami aktivitas Anda dan menyelidiki potensi penyalahgunaan.

<Note>
Mengaktifkan layanan ini tidak memberikan AWS atau Anthropic akses apa pun ke konten Anda.
</Note>

## Dukungan fitur
Untuk semua fitur yang saat ini didukung di Bedrock, lihat [ikhtisar fitur API](/docs/id/api/overview).

### Dukungan PDF di Bedrock

Dukungan PDF tersedia di Amazon Bedrock melalui API Converse dan API InvokeModel. Untuk informasi terperinci tentang kemampuan dan batasan pemrosesan PDF, lihat [dokumentasi dukungan PDF](/docs/id/build-with-claude/pdf-support#amazon-bedrock-pdf-support).

**Pertimbangan penting untuk pengguna API Converse:**
- Analisis PDF visual (bagan, gambar, tata letak) memerlukan kutipan untuk diaktifkan
- Tanpa kutipan, hanya ekstraksi teks dasar yang tersedia
- Untuk kontrol penuh tanpa kutipan paksa, gunakan API InvokeModel

Untuk detail lebih lanjut tentang dua mode pemrosesan dokumen dan batasan mereka, lihat [panduan dukungan PDF](/docs/id/build-with-claude/pdf-support#amazon-bedrock-pdf-support).

### Jendela konteks

Claude Opus 4.6 dan Claude Sonnet 4.6 memiliki [jendela konteks 1M-token](/docs/id/build-with-claude/context-windows) di Amazon Bedrock. Model Claude lainnya, termasuk Sonnet 4.5 dan Sonnet 4 (tidak direkomendasikan), memiliki jendela konteks 200k-token.

Amazon Bedrock membatasi muatan permintaan hingga 20 MB. Saat mengirim dokumen besar atau banyak gambar, Anda mungkin mencapai batas ini sebelum batas token.

## Global vs regional endpoints

Mulai dengan **Claude Sonnet 4.5 dan semua model di masa depan**, Amazon Bedrock menawarkan dua jenis endpoint:

- **Endpoint global:** Perutean dinamis untuk ketersediaan maksimal
- **Endpoint regional:** Perutean data yang dijamin melalui wilayah geografis tertentu

Endpoint regional mencakup premium harga 10% dibandingkan endpoint global.

<Note>
Ini berlaku untuk Claude Sonnet 4.5 dan model di masa depan saja. Model yang lebih lama (Claude Sonnet 4 (tidak direkomendasikan), Opus 4 (tidak direkomendasikan), dan sebelumnya) mempertahankan struktur harga yang ada.
</Note>

### Kapan menggunakan setiap opsi

**Endpoint global (direkomendasikan):**
- Memberikan ketersediaan dan uptime maksimal
- Secara dinamis merutekan permintaan ke wilayah dengan kapasitas yang tersedia
- Tidak ada premium harga
- Terbaik untuk aplikasi di mana residensi data fleksibel

**Endpoint regional (CRIS):**
- Merutekan lalu lintas melalui wilayah geografis tertentu
- Diperlukan untuk persyaratan residensi data dan kepatuhan
- Tersedia untuk AS, EU, Jepang, dan Australia
- Premium harga 10% mencerminkan biaya infrastruktur untuk kapasitas regional khusus

### Implementasi

**Menggunakan endpoint global (default untuk Opus 4.6, Sonnet 4.5, dan Sonnet 4 (tidak direkomendasikan)):**

ID model untuk Claude Sonnet 4.5 dan 4 (tidak direkomendasikan) sudah mencakup awalan `global.`:

<CodeGroup>
```bash CLI
# CLI ant belum mendukung Amazon Bedrock.
```

```python Python nocheck
from anthropic import AnthropicBedrock

client = AnthropicBedrock(aws_region="us-west-2")

message = client.messages.create(
    model="global.anthropic.claude-opus-4-6-v1",
    max_tokens=256,
    messages=[{"role": "user", "content": "Hello, world"}],
)
```

```typescript TypeScript nocheck
import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

const client = new AnthropicBedrock({
  awsRegion: "us-west-2"
});

const message = await client.messages.create({
  model: "global.anthropic.claude-opus-4-6-v1",
  max_tokens: 256,
  messages: [{ role: "user", content: "Hello, world" }]
});
```

```csharp C# nocheck
using Anthropic.Bedrock;
using Anthropic.Models.Messages;

// Klien C# Bedrock menggunakan ID model dengan awalan wilayah untuk perutean global
AnthropicBedrockClient client = new(
    await AnthropicBedrockCredentialsHelper.FromEnv()
    ?? throw new InvalidOperationException("AWS credentials not configured.")
);

var response = await client.Messages.Create(new MessageCreateParams
{
    // Gunakan awalan "global." untuk inferensi lintas wilayah global
    Model = "global.anthropic.claude-opus-4-6-v1",
    MaxTokens = 256,
    Messages = [new() { Role = Role.User, Content = "Hello, world" }],
});
```

```go Go hidelines={1..2,9..10,-1}
package main

import (
	"context"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/bedrock"
)

func main() {
	// Menggunakan rantai penyedia kredensial AWS default
	client := anthropic.NewClient(
		bedrock.WithLoadDefaultConfig(context.Background()),
	)

	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:     "global.anthropic.claude-opus-4-6-v1",
		MaxTokens: 256,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, world")),
		},
	})
	_ = message
}
```

```java Java nocheck
import com.anthropic.bedrock.backends.BedrockBackend;
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;

// Menggunakan rantai penyedia kredensial AWS default
AnthropicClient client = AnthropicOkHttpClient.builder()
  .backend(BedrockBackend.fromEnv())
  .build();

var message = client
  .messages()
  .create(
    MessageCreateParams.builder()
      .model("global.anthropic.claude-opus-4-6-v1")
      .maxTokens(256)
      .addUserMessage("Hello, world")
      .build()
  );
```

```php PHP nocheck
<?php

use Anthropic\Bedrock;

$client = Bedrock\Client::fromEnvironment();

$message = $client->messages->create(
    maxTokens: 256,
    messages: [
        ['role' => 'user', 'content' => 'Hello, world']
    ],
    model: 'global.anthropic.claude-opus-4-6-v1',
);
```

```ruby Ruby nocheck
require "anthropic"

# Kredensial default menyelesaikan wilayah dari variabel lingkungan AWS_REGION
client = Anthropic::BedrockClient.new

message = client.messages.create(
  # Gunakan awalan "global." untuk inferensi lintas wilayah global
  model: "global.anthropic.claude-opus-4-6-v1",
  max_tokens: 256,
  messages: [{role: "user", content: "Hello, world"}]
)
```
</CodeGroup>

**Menggunakan endpoint regional (CRIS):**

Untuk menggunakan endpoint regional, hapus awalan `global.` dari ID model:

<CodeGroup>
```bash CLI
# CLI ant belum mendukung Amazon Bedrock.
```

```python Python nocheck
from anthropic import AnthropicBedrock

client = AnthropicBedrock(aws_region="us-west-2")

# Menggunakan endpoint regional AS (CRIS)
message = client.messages.create(
    model="anthropic.claude-opus-4-6-v1",  # Tanpa awalan global.
    max_tokens=256,
    messages=[{"role": "user", "content": "Hello, world"}],
)
```

```typescript TypeScript nocheck
import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

const client = new AnthropicBedrock({
  awsRegion: "us-west-2"
});

// Menggunakan endpoint regional AS (CRIS)
const message = await client.messages.create({
  model: "anthropic.claude-opus-4-6-v1", // Tanpa awalan global.
  max_tokens: 256,
  messages: [{ role: "user", content: "Hello, world" }]
});
```

```csharp C# nocheck
using Anthropic.Bedrock;
using Anthropic.Models.Messages;

AnthropicBedrockClient client = new(
    new AnthropicBedrockPrivateKeyCredentials { Region = "us-west-2" }
);

// Menggunakan endpoint regional AS (CRIS)
var response = await client.Messages.Create(new MessageCreateParams
{
    Model = "anthropic.claude-opus-4-6-v1", // Tanpa awalan global.
    MaxTokens = 256,
    Messages = [new() { Role = Role.User, Content = "Hello, world" }],
});
```

```go Go hidelines={1..2,9..10,-1}
package main

import (
	"context"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/bedrock"
)

func main() {
	// Menggunakan rantai penyedia kredensial AWS default
	client := anthropic.NewClient(
		bedrock.WithLoadDefaultConfig(context.Background()),
	)

	// Menggunakan endpoint regional AS (CRIS)
	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:     "us.anthropic.claude-opus-4-6-v1", // Awalan regional
		MaxTokens: 256,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, world")),
		},
	})
	_ = message
}
```

```java Java nocheck
import com.anthropic.bedrock.backends.BedrockBackend;
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;

// Menggunakan rantai penyedia kredensial AWS default
AnthropicClient client = AnthropicOkHttpClient.builder()
  .backend(BedrockBackend.fromEnv())
  .build();

// Menggunakan endpoint regional AS (CRIS)
var message = client
  .messages()
  .create(
    MessageCreateParams.builder()
      .model("us.anthropic.claude-opus-4-6-v1") // Awalan regional
      .maxTokens(256)
      .addUserMessage("Hello, world")
      .build()
  );
```

```php PHP nocheck
<?php

use Anthropic\Bedrock;

$client = Bedrock\Client::fromEnvironment();

$message = $client->messages->create(
    maxTokens: 256,
    messages: [
        ['role' => 'user', 'content' => 'Hello, world']
    ],
    model: 'anthropic.claude-opus-4-6-v1',
);
```

```ruby Ruby nocheck
require "anthropic"

# Menggunakan endpoint regional AS (CRIS)
client = Anthropic::BedrockClient.new(aws_region: "us-west-2")

message = client.messages.create(
  model: "anthropic.claude-opus-4-6-v1", # Tanpa awalan global.
  max_tokens: 256,
  messages: [{role: "user", content: "Hello, world"}]
)
```
</CodeGroup>

<Note>
**Claude Mythos Preview** adalah model pratinjau penelitian yang tersedia untuk pelanggan yang diundang di Amazon Bedrock. Untuk informasi lebih lanjut, lihat [Project Glasswing](https://anthropic.com/glasswing).
</Note>

### Sumber daya tambahan

- **Harga AWS Bedrock:** [aws.amazon.com/bedrock/pricing](https://aws.amazon.com/bedrock/pricing/)
- **Dokumentasi harga AWS:** [Panduan harga Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-pricing.html)
- **Posting blog AWS:** [Memperkenalkan Claude Sonnet 4.5 di Amazon Bedrock](https://aws.amazon.com/blogs/aws/introducing-claude-sonnet-4-5-in-amazon-bedrock-anthropics-most-intelligent-model-best-for-coding-and-complex-agents/)
- **Detail harga Anthropic:** [Dokumentasi harga](/docs/id/about-claude/pricing#third-party-platform-pricing)