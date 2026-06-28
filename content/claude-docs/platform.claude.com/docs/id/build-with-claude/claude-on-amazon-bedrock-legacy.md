---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 9d98990493b048e99100935cf4f0170f672682e7aa064780f9739ed72f90aaf8
---

# Claude di Amazon Bedrock (legacy)

Integrasi Amazon Bedrock legacy untuk model Claude, menggunakan API InvokeModel dan Converse dengan pengidentifikasi model berversi ARN.

---

<Note>
  Halaman ini membahas integrasi Amazon Bedrock legacy: API `InvokeModel` dan `Converse` dengan pengidentifikasi model berversi ARN dan encoding event-stream AWS. Untuk model yang tersedia di endpoint Bedrock Messages-API, lihat [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), yang menggunakan Messages API di `/anthropic/v1/messages` dengan streaming SSE. Untuk alternatif yang dioperasikan Anthropic dengan penagihan AWS Marketplace dan biasanya akses fitur di hari yang sama, lihat [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws). Pengguna Bedrock yang sudah ada dapat mengikuti [panduan migrasi](/docs/id/build-with-claude/claude-platform-on-aws#migrating-from-amazon-bedrock).
</Note>

Memanggil Claude melalui Bedrock sedikit berbeda dari cara Anda memanggil Claude di Claude API secara langsung. Panduan ini memandu Anda menyelesaikan panggilan API ke Claude di Bedrock menggunakan salah satu [SDK klien](/docs/id/cli-sdks-libraries/overview) Anthropic.

Perhatikan bahwa panduan ini mengasumsikan Anda telah mendaftar untuk [akun AWS](https://portal.aws.amazon.com/billing/signup) dan mengonfigurasi akses terprogram.

## Menginstal dan mengonfigurasi AWS CLI

1. [Instal versi AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) pada atau lebih baru dari versi `2.13.23`
2. Konfigurasikan kredensial AWS Anda menggunakan perintah AWS configure (lihat [Configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)) atau temukan kredensial Anda dengan menavigasi ke "Command line or programmatic access" di dalam dashboard AWS Anda dan mengikuti petunjuk di modal popup.
3. Verifikasi bahwa kredensial Anda berfungsi:

```bash AWS CLI
aws sts get-caller-identity
```

## Menginstal SDK untuk mengakses Bedrock

[SDK klien](/docs/id/cli-sdks-libraries/overview) Anthropic mendukung Bedrock. Anda juga dapat menggunakan AWS SDK seperti `boto3` secara langsung.

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
      implementation("com.anthropic:anthropic-java-bedrock:2.40.0")
      ```

      ```xml Maven
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java-bedrock</artifactId>
          <version>2.40.0</version>
      </dependency>
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.bedrock.backends.BedrockBackend;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.Model;
      // ...
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
    pip install "boto3>=1.28.59"
    ```
  </Tab>
</Tabs>

## Mengakses Bedrock

### Berlangganan model Anthropic

Buka [AWS Console > Bedrock > Model Access](https://console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess) dan minta akses ke model Anthropic. Perhatikan bahwa ketersediaan model Anthropic bervariasi berdasarkan wilayah. Lihat [dokumentasi AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) untuk informasi terbaru.

#### ID model API

<Note>
  Claude Fable 5, Claude Opus 4.8, dan Claude Opus 4.7 dapat dijangkau melalui `InvokeModel` di `bedrock-runtime`. Permintaan ini dilayani oleh infrastruktur yang sama dengan endpoint [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock). Untuk bentuk permintaan Messages API native dan paritas fitur penuh, gunakan halaman tersebut. Claude Fable 5, Claude Opus 4.8, dan Claude Opus 4.7 tidak disertakan dalam tabel model di halaman ini karena tidak memiliki ID model berversi ARN.
</Note>

Istilah siklus hidup (Deprecated, Retired) didefinisikan di [Penghentian model](/docs/id/about-claude/model-deprecations). Tanggal siklus hidup pada platform yang dioperasikan mitra ditetapkan oleh mitra dan dapat berbeda dari jadwal Claude API. Untuk tanggal penghentian terkini dari model apa pun di Amazon Bedrock, lihat [halaman siklus hidup model Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html).

| Model                        | ID model Bedrock dasar                    | `global` | `us`  | `eu`  | `jp`  | `apac` |
| ---------------------------- | ----------------------------------------- | -------- | ----- | ----- | ----- | ------ |
| Claude Opus 4.6              | anthropic.claude-opus-4-6-v1              | Ya       | Ya    | Ya    | Ya    | Ya     |
| Claude Sonnet 4.6            | anthropic.claude-sonnet-4-6               | Ya       | Ya    | Ya    | Ya    | Tidak  |
| Claude Sonnet 4.5            | anthropic.claude-sonnet-4-5-20250929-v1:0 | Ya       | Ya    | Ya    | Ya    | Tidak  |
| Claude Sonnet 4 Deprecated.  | anthropic.claude-sonnet-4-20250514-v1:0   | Ya       | Ya    | Ya    | Tidak | Ya     |
| Claude Sonnet 3.7 Retired.   | anthropic.claude-3-7-sonnet-20250219-v1:0 | Tidak    | Tidak | Tidak | Tidak | Tidak  |
| Claude Opus 4.5              | anthropic.claude-opus-4-5-20251101-v1:0   | Ya       | Ya    | Ya    | Tidak | Tidak  |
| Claude Opus 4.1 Deprecated.  | anthropic.claude-opus-4-1-20250805-v1:0   | Tidak    | Ya    | Tidak | Tidak | Tidak  |
| Claude Opus 4 Retired.       | anthropic.claude-opus-4-20250514-v1:0     | Tidak    | Tidak | Tidak | Tidak | Tidak  |
| Claude Haiku 4.5             | anthropic.claude-haiku-4-5-20251001-v1:0  | Ya       | Ya    | Ya    | Tidak | Tidak  |
| Claude Haiku 3.5 Deprecated. | anthropic.claude-3-5-haiku-20241022-v1:0  | Tidak    | Ya    | Tidak | Tidak | Tidak  |

Untuk informasi lebih lanjut tentang ID model regional vs global, lihat bagian [Endpoint global vs regional](#global-vs-regional-endpoints).

### Menampilkan daftar model yang tersedia

Contoh berikut menunjukkan cara mencetak daftar semua model Claude yang tersedia melalui Bedrock:

<CodeGroup>
  ```bash AWS CLI
  aws bedrock list-foundation-models --region=us-west-2 --by-provider anthropic --query "modelSummaries[*].modelId"
  ```

  ```python Boto3 (Python)
  import boto3

  bedrock = boto3.client(service_name="bedrock")
  response = bedrock.list_foundation_models(byProvider="anthropic")

  for summary in response["modelSummaries"]:
      print(summary["modelId"])
  ```

  ```typescript TypeScript
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

  ```csharp C#
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

  ```go Go
  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/aws/aws-sdk-go-v2/config"
  	"github.com/aws/aws-sdk-go-v2/service/bedrock"
  )
  // ...
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
  ```

  ```java Java
  import software.amazon.awssdk.regions.Region;
  import software.amazon.awssdk.services.bedrock.BedrockClient;
  import software.amazon.awssdk.services.bedrock.model.ListFoundationModelsRequest;
  import software.amazon.awssdk.services.bedrock.model.ListFoundationModelsResponse;
  import software.amazon.awssdk.services.bedrock.model.FoundationModelSummary;
  // ...
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
  ```

  ```php PHP
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

  ```ruby Ruby
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
  # CLI ant tidak mendukung Amazon Bedrock.
  ```

  ```python Python
  from anthropic import AnthropicBedrock

  client = AnthropicBedrock(
      # Autentikasi dengan memberikan kunci di bawah ini atau gunakan penyedia kredensial AWS default, seperti
      # menggunakan ~/.aws/credentials atau variabel lingkungan "AWS_SECRET_ACCESS_KEY" dan "AWS_ACCESS_KEY_ID".
      aws_access_key="<access key>",
      aws_secret_key="<secret key>",
      # Kredensial sementara dapat digunakan dengan aws_session_token.
      # Baca selengkapnya di https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
      aws_session_token="<session_token>",
      # aws_region mengubah region aws tujuan permintaan. Secara default, SDK membaca AWS_REGION,
      # dan jika tidak ada, default-nya adalah us-east-1. Perhatikan bahwa SDK tidak membaca ~/.aws/config untuk region.
      aws_region="us-west-2",
  )

  message = client.messages.create(
      model="global.anthropic.claude-opus-4-6-v1",
      max_tokens=256,
      messages=[{"role": "user", "content": "Hello, world"}],
  )
  print(message.content)
  ```

  ```typescript TypeScript
  import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

  const client = new AnthropicBedrock({
    // Autentikasi dengan menyediakan kunci di bawah ini atau gunakan
    // penyedia kredensial AWS default, seperti
    // ~/.aws/credentials atau variabel lingkungan "AWS_SECRET_ACCESS_KEY"
    // dan "AWS_ACCESS_KEY_ID".
    awsAccessKey: "<access key>",
    awsSecretKey: "<secret key>",

    // Kredensial sementara dapat digunakan dengan awsSessionToken.
    // Baca selengkapnya di https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
    awsSessionToken: "<session_token>",

    // awsRegion mengubah region AWS tujuan permintaan
    // dikirim. Secara default, SDK membaca AWS_REGION, dan jika
    // tidak ada, default-nya adalah us-east-1. Perhatikan bahwa
    // SDK tidak membaca ~/.aws/config untuk region.
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

  ```csharp C#
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

  ```go Go
  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/bedrock"
  )
  // ...
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
  ```

  ```java Java
  import com.anthropic.bedrock.backends.BedrockBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  // ...
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
  ```

  ```php PHP
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

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::BedrockClient.new

  message = client.messages.create(
    model: "global.anthropic.claude-opus-4-6-v1",
    max_tokens: 256,
    messages: [{role: "user", content: "Hello, world"}]
  )

  puts message.content.first.text
  ```

  ```python Boto3 (Python)
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

Lihat [SDK klien](/docs/id/cli-sdks-libraries/overview) untuk detail lebih lanjut, dan [dokumentasi resmi Bedrock](https://docs.aws.amazon.com/bedrock/).

### Autentikasi bearer token

Anda dapat mengautentikasi dengan Bedrock menggunakan bearer token alih-alih kredensial AWS. Ini berguna di lingkungan perusahaan di mana tim memerlukan akses ke Bedrock tanpa mengelola kredensial AWS, peran IAM, atau izin tingkat akun.

Pendekatan paling sederhana adalah mengatur variabel lingkungan `AWS_BEARER_TOKEN_BEDROCK`, yang dideteksi secara otomatis oleh setiap SDK saat menyelesaikan kredensial dari lingkungan.

Untuk menyediakan token secara terprogram:

<CodeGroup>
  ```python Python
  from anthropic import AnthropicBedrock

  client = AnthropicBedrock(
      api_key="your-bearer-token",
      aws_region="us-west-2",
  )

  message = client.messages.create(
      model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )
  print(message.content)
  ```

  ```typescript TypeScript
  import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

  const client = new AnthropicBedrock({
    apiKey: "your-bearer-token",
    awsRegion: "us-west-2"
  });

  const message = await client.messages.create({
    model: "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(message);
  ```

  ```csharp C#
  using Anthropic.Bedrock;
  using Anthropic.Models.Messages;

  var client = new AnthropicBedrockClient(
      new AnthropicBedrockApiTokenCredentials
      {
          BearerToken = "your-bearer-token",
          Region = "us-west-2",
      }
  );

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }],
  });
  ```

  ```go Go
  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/bedrock"
  	"github.com/aws/aws-sdk-go-v2/aws"
  )
  // ...
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
  ```

  ```java Java
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

  ```php PHP
  <?php

  use Anthropic\Bedrock;

  $client = Bedrock\Client::withApiKey('your-bearer-token', 'us-west-2');

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Hello!']
      ],
      model: 'us.anthropic.claude-sonnet-4-5-20250929-v1:0',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::BedrockClient.new(
    api_key: "your-bearer-token",
    aws_region: "us-west-2"
  )

  message = client.messages.create(
    model: "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello!"}]
  )
  puts message.content.first.text
  ```
</CodeGroup>

## Pencatatan aktivitas

Bedrock menyediakan [layanan pencatatan invokasi](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) yang memungkinkan pelanggan mencatat prompt dan completion yang terkait dengan penggunaan Anda.

Anthropic merekomendasikan agar Anda mencatat aktivitas Anda setidaknya secara bergulir selama 30 hari untuk memahami aktivitas Anda dan menyelidiki potensi penyalahgunaan.

<Note>
  Mengaktifkan layanan ini tidak memberikan AWS atau Anthropic akses apa pun ke konten Anda.
</Note>

## Dukungan fitur

Untuk daftar fitur lengkap dengan ketersediaan Amazon Bedrock, lihat [Ikhtisar fitur](/docs/id/build-with-claude/overview).

### Sorotan fitur yang didukung

* [Messages API](/docs/id/api/messages/create)
* [Caching prompt](/docs/id/build-with-claude/prompt-caching)
* [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking)
* [Penggunaan alat](/docs/id/agents-and-tools/tool-use/overview), termasuk [alat Bash](/docs/id/agents-and-tools/tool-use/bash-tool), [alat Computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool), [alat Memory](/docs/id/agents-and-tools/tool-use/memory-tool), dan [alat Text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool)
* [Sitasi](/docs/id/build-with-claude/citations)
* [Output terstruktur](/docs/id/build-with-claude/structured-outputs)

### Fitur yang tidak didukung

* Sumber input (sumber URL untuk gambar dan dokumen, Files API)
* Alat sisi server (eksekusi kode, pencarian web, pengambilan web, advisor)
* Infrastruktur agen (Agent Skills, konektor MCP, pemanggilan alat terprogram)
* Endpoint API (Message Batches, Models, Admin, Compliance, Usage and Cost)
* Claude Managed Agents
* Fallback sisi server ([parameter `fallbacks`](/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback); gunakan [pola fallback sisi klien](/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) sebagai gantinya)

### Dukungan PDF di Bedrock

Dukungan PDF tersedia di Bedrock melalui Converse API dan InvokeModel API. Untuk informasi terperinci tentang kemampuan dan batasan pemrosesan PDF, lihat [Dukungan PDF Amazon Bedrock](/docs/id/build-with-claude/pdf-support#amazon-bedrock-pdf-support).

**Pertimbangan penting untuk pengguna Converse API:**

* Analisis PDF visual (grafik, gambar, tata letak) memerlukan sitasi untuk diaktifkan
* Tanpa sitasi, hanya ekstraksi teks dasar yang tersedia
* Untuk kontrol penuh tanpa sitasi yang dipaksakan, gunakan InvokeModel API

### Jendela konteks

Claude Fable 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6 memiliki [jendela konteks 1 juta token](/docs/id/build-with-claude/context-windows) di Amazon Bedrock. Model Claude lainnya, termasuk Sonnet 4.5 dan Sonnet 4 (deprecated), memiliki jendela konteks 200 ribu token.

Bedrock membatasi payload permintaan hingga 20 MB. Saat mengirim dokumen besar atau banyak gambar, Anda mungkin mencapai batas ini sebelum batas token.

## Endpoint global vs regional

Mulai dari **Claude Sonnet 4.5 dan semua model mendatang**, Bedrock menawarkan dua jenis endpoint:

* **Endpoint global:** Perutean dinamis untuk ketersediaan maksimum
* **Endpoint regional:** Perutean data yang dijamin melalui wilayah geografis tertentu

Endpoint regional menyertakan premium harga 10% dibandingkan endpoint global.

<Note>
  Ini berlaku untuk Claude Sonnet 4.5 dan model mendatang saja. Model yang lebih lama (Claude Sonnet 4 (deprecated) dan sebelumnya) mempertahankan struktur harga yang sudah ada.
</Note>

### Kapan menggunakan setiap opsi

**Endpoint global (direkomendasikan):**

* Menyediakan ketersediaan dan uptime maksimum
* Merutekan permintaan secara dinamis ke wilayah dengan kapasitas yang tersedia
* Tidak ada premium harga
* Terbaik untuk aplikasi di mana residensi data bersifat fleksibel

**Endpoint regional (CRIS):**

* Merutekan lalu lintas melalui wilayah geografis tertentu
* Diperlukan untuk persyaratan residensi data dan kepatuhan
* Tersedia untuk AS, UE, Jepang, dan Asia-Pasifik
* Premium harga 10% mencerminkan biaya infrastruktur untuk kapasitas regional khusus

### Implementasi

**Menggunakan endpoint global (default untuk Opus 4.6, Sonnet 4.6, dan Sonnet 4.5):**

ID model untuk Claude Opus 4.6, Sonnet 4.6, dan Sonnet 4.5 sudah menyertakan prefiks `global.`:

<CodeGroup>
  ```bash CLI
  # CLI ant tidak mendukung Amazon Bedrock.
  ```

  ```python Python
  from anthropic import AnthropicBedrock

  client = AnthropicBedrock(aws_region="us-west-2")

  message = client.messages.create(
      model="global.anthropic.claude-opus-4-6-v1",
      max_tokens=256,
      messages=[{"role": "user", "content": "Hello, world"}],
  )
  ```

  ```typescript TypeScript
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

  ```csharp C#
  using Anthropic.Bedrock;
  using Anthropic.Models.Messages;

  // Klien Bedrock C# menggunakan ID model dengan prefiks region untuk routing global
  AnthropicBedrockClient client = new(
      await AnthropicBedrockCredentialsHelper.FromEnv()
      ?? throw new InvalidOperationException("AWS credentials not configured.")
  );

  var response = await client.Messages.Create(new MessageCreateParams
  {
      // Gunakan prefiks "global." untuk inferensi lintas region global
      Model = "global.anthropic.claude-opus-4-6-v1",
      MaxTokens = 256,
      Messages = [new() { Role = Role.User, Content = "Hello, world" }],
  });
  ```

  ```go Go
  import (
  	"context"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/bedrock"
  )
  // ...
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
  ```

  ```java Java
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

  ```php PHP
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

  ```ruby Ruby
  require "anthropic"

  # Kredensial default mengambil region dari variabel lingkungan AWS_REGION
  client = Anthropic::BedrockClient.new

  message = client.messages.create(
    # Gunakan prefiks "global." untuk inferensi lintas region global
    model: "global.anthropic.claude-opus-4-6-v1",
    max_tokens: 256,
    messages: [{role: "user", content: "Hello, world"}]
  )
  ```
</CodeGroup>

**Menggunakan endpoint regional (CRIS):**

Untuk menggunakan endpoint regional, ganti prefiks `global.` dengan prefiks regional seperti `us.`:

<CodeGroup>
  ```bash CLI
  # CLI ant tidak mendukung Amazon Bedrock.
  ```

  ```python Python
  from anthropic import AnthropicBedrock

  client = AnthropicBedrock(aws_region="us-west-2")

  # Menggunakan endpoint regional AS (CRIS)
  message = client.messages.create(
      model="us.anthropic.claude-opus-4-6-v1",  # Regional prefix
      max_tokens=256,
      messages=[{"role": "user", "content": "Hello, world"}],
  )
  ```

  ```typescript TypeScript
  import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

  const client = new AnthropicBedrock({
    awsRegion: "us-west-2"
  });

  // Menggunakan endpoint regional AS (CRIS)
  const message = await client.messages.create({
    model: "us.anthropic.claude-opus-4-6-v1", // Regional prefix
    max_tokens: 256,
    messages: [{ role: "user", content: "Hello, world" }]
  });
  ```

  ```csharp C#
  using Anthropic.Bedrock;
  using Anthropic.Models.Messages;

  AnthropicBedrockClient client = new(
      new AnthropicBedrockPrivateKeyCredentials { Region = "us-west-2" }
  );

  // Menggunakan endpoint regional AS (CRIS)
  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = "us.anthropic.claude-opus-4-6-v1", // Regional prefix
      MaxTokens = 256,
      Messages = [new() { Role = Role.User, Content = "Hello, world" }],
  });
  ```

  ```go Go
  import (
  	"context"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/bedrock"
  )
  // ...
  	// Menggunakan rantai penyedia kredensial AWS default
  	client := anthropic.NewClient(
  		bedrock.WithLoadDefaultConfig(context.Background()),
  	)

  	// Menggunakan endpoint regional AS (CRIS)
  	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "us.anthropic.claude-opus-4-6-v1", // Regional prefix
  		MaxTokens: 256,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, world")),
  		},
  	})
  	_ = message
  ```

  ```java Java
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
        .model("us.anthropic.claude-opus-4-6-v1") // Regional prefix
        .maxTokens(256)
        .addUserMessage("Hello, world")
        .build()
    );
  ```

  ```php PHP
  <?php

  use Anthropic\Bedrock;

  $client = Bedrock\Client::fromEnvironment();

  $message = $client->messages->create(
      maxTokens: 256,
      messages: [
          ['role' => 'user', 'content' => 'Hello, world']
      ],
      model: 'us.anthropic.claude-opus-4-6-v1',
  );
  ```

  ```ruby Ruby
  require "anthropic"

  # Menggunakan endpoint regional AS (CRIS)
  client = Anthropic::BedrockClient.new(aws_region: "us-west-2")

  message = client.messages.create(
    model: "us.anthropic.claude-opus-4-6-v1", # Regional prefix
    max_tokens: 256,
    messages: [{role: "user", content: "Hello, world"}]
  )
  ```
</CodeGroup>

<Note>
  **Claude Mythos Preview** adalah model pratinjau riset yang tersedia untuk pelanggan yang diundang di Amazon Bedrock. Untuk informasi lebih lanjut, lihat [Project Glasswing](https://anthropic.com/glasswing).
</Note>

## Sumber daya tambahan

* **Harga Bedrock:** [aws.amazon.com/bedrock/pricing](https://aws.amazon.com/bedrock/pricing/)
* **Dokumentasi harga AWS:** [Panduan harga Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-pricing.html)
* **Postingan blog AWS:** [Introducing Claude Sonnet 4.5 in Amazon Bedrock](https://aws.amazon.com/blogs/aws/introducing-claude-sonnet-4-5-in-amazon-bedrock-anthropics-most-intelligent-model-best-for-coding-and-complex-agents/)
* **Detail harga Anthropic:** [Harga platform cloud](/docs/id/about-claude/pricing#cloud-platform-pricing)
