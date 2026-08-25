---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 4053cd54b6ed6fe2b794196159097f06eae6a8d94185235a9fa0c03f9b5567d1
---

---
title: Claude di Amazon Bedrock (Opus 4.6 dan sebelumnya)
url: https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy
description: Integrasi Amazon Bedrock lama untuk model Claude, menggunakan API InvokeModel dan Converse dengan pengidentifikasi model berversi ARN.
---

<Note>
  Halaman ini membahas integrasi Amazon Bedrock lama: API `InvokeModel` dan `Converse` dengan pengidentifikasi model berversi ARN dan encoding event-stream AWS. Untuk model yang tersedia di endpoint Bedrock Messages-API, lihat [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), yang menggunakan Messages API di `/anthropic/v1/messages` dengan streaming SSE. Untuk alternatif yang dioperasikan Anthropic dengan penagihan AWS Marketplace dan akses fitur yang biasanya tersedia di hari yang sama, lihat [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Pengguna Bedrock yang sudah ada dapat mengikuti [panduan migrasi](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#migrating-from-amazon-bedrock).
</Note>

Memanggil Claude melalui Bedrock sedikit berbeda dari cara Anda memanggil Claude di Claude API secara langsung. Panduan ini memandu Anda menyelesaikan panggilan API ke Claude di Bedrock menggunakan salah satu [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) Anthropic.

Perhatikan bahwa panduan ini mengasumsikan Anda telah mendaftar [akun AWS](https://portal.aws.amazon.com/billing/signup) dan mengonfigurasi akses programatik.

## Instal dan konfigurasikan AWS CLI

1. [Instal versi AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) versi `2.13.23` atau yang lebih baru.
2. Konfigurasikan kredensial AWS Anda menggunakan perintah AWS configure (lihat [Konfigurasi AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)) atau temukan kredensial Anda dengan membuka "Command line or programmatic access" di dasbor AWS Anda dan mengikuti petunjuk di jendela modal.
3. Verifikasi bahwa kredensial Anda berfungsi:

```bash AWS CLI
aws sts get-caller-identity
```

## Instal SDK untuk mengakses Bedrock

[SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) Anthropic mendukung Bedrock. Anda juga dapat menggunakan AWS SDK seperti `boto3` secara langsung.

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
      implementation("com.anthropic:anthropic-java-bedrock:2.57.0")
      ```

      ```xml Maven
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java-bedrock</artifactId>
          <version>2.57.0</version>
      </dependency>
      ```

      ```java Java
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
    pip install "boto3>=1.28.59"
    ```
  </Tab>
</Tabs>

## Mengakses Bedrock

### Berlangganan model Anthropic

Buka [AWS Console > Bedrock > Model Access](https://console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess) dan minta akses ke model Anthropic. Perhatikan bahwa ketersediaan model Anthropic berbeda-beda menurut wilayah. Lihat [dokumentasi AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) untuk informasi terbaru.

#### ID model API

<Note>
  Claude Opus 5, Claude Sonnet 5, Claude Fable 5, Claude Opus 4.8, dan Claude Opus 4.7 dapat dijangkau melalui `InvokeModel` di `bedrock-runtime`. Permintaan ini dilayani oleh infrastruktur yang sama dengan endpoint [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock). Untuk bentuk permintaan Messages API native dan paritas fitur penuh, gunakan halaman tersebut. Model-model ini tidak dicantumkan dalam tabel model di halaman ini karena tidak memiliki ID model berversi ARN.
</Note>

Istilah siklus hidup (Deprecated, Retired) didefinisikan di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations). Tanggal siklus hidup pada platform yang dioperasikan mitra ditetapkan oleh mitra dan dapat berbeda dari jadwal Claude API. Untuk tanggal penghentian terkini model apa pun di Amazon Bedrock, lihat [halaman siklus hidup model Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html).

AWS menawarkan model Claude yang lebih baru melalui [cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) (inferensi lintas wilayah) alih-alih throughput on-demand. Untuk model-model ini, permintaan yang meneruskan ID model dasar akan gagal dengan error HTTP 400 seperti berikut:

```text wrap
Invocation of model ID anthropic.claude-sonnet-4-5-20250929-v1:0 with on-demand throughput isn't supported. Retry your request with the ID or ARN of an inference profile that contains this model.
```

Untuk memanggil model-model ini, teruskan inference profile alih-alih ID model dasar. ID inference profile adalah ID model dasar dengan prefiks dari kolom yang ditandai "Ya" pada tabel berikut, misalnya us.anthropic.claude-sonnet-4-5-20250929-v1:0. Anda juga dapat meneruskan ARN inference profile lengkap, dalam bentuk `arn:aws:bedrock:{region}:{account-id}:inference-profile/{inference-profile-id}`. Untuk daftar resmi AWS mengenai inference profile yang tersedia, lihat [Supported Regions and models for inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html). Untuk mengetahui bagaimana prefiks memengaruhi perutean dan harga, lihat bagian [Endpoint global versus regional](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#global-vs-regional-endpoints).

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

### Daftar model yang tersedia

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
  using Amazon;
  using Amazon.Bedrock;
  using Amazon.Bedrock.Model;

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

<Tabs>
  <Tab title="cURL">
    <Note>
      Memanggil API `InvokeModel` dengan kredensial AWS memerlukan penandatanganan permintaan SigV4, yang ditangani secara otomatis oleh SDK di tab lainnya. Untuk endpoint Bedrock yang dapat Anda panggil dengan perintah cURL mandiri, lihat [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock#making-your-first-request).
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      CLI `ant` tidak mendukung Amazon Bedrock. Gunakan salah satu contoh SDK sebagai gantinya.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python
    from anthropic import AnthropicBedrock

    client = AnthropicBedrock(
        # Autentikasi dengan menyediakan kunci di bawah ini atau gunakan penyedia kredensial AWS default, seperti
        # menggunakan ~/.aws/credentials atau variabel lingkungan "AWS_SECRET_ACCESS_KEY" dan "AWS_ACCESS_KEY_ID".
        aws_access_key="<access key>",
        aws_secret_key="<secret key>",
        # Kredensial sementara dapat digunakan dengan aws_session_token.
        # Baca selengkapnya di https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
        aws_session_token="<session_token>",
        # aws_region mengubah region aws tujuan permintaan. Jika tidak disediakan, SDK membaca
        # AWS_REGION / AWS_DEFAULT_REGION, lalu region yang dikonfigurasi untuk sesi boto3 atau profil AWS Anda
        # (termasuk ~/.aws/config), dan memunculkan ValueError jika tidak ada region yang dapat ditentukan.
        aws_region="us-west-2",
    )

    message = client.messages.create(
        model="global.anthropic.claude-opus-4-6-v1",
        max_tokens=256,
        messages=[{"role": "user", "content": "Hello, world"}],
    )
    print(message.content)
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

    const client = new AnthropicBedrock({
      // Lakukan autentikasi dengan menyediakan kunci di bawah ini atau gunakan
      // penyedia kredensial AWS default, seperti
      // ~/.aws/credentials atau variabel lingkungan "AWS_SECRET_ACCESS_KEY" dan
      // "AWS_ACCESS_KEY_ID".
      awsAccessKey: "<access key>",
      awsSecretKey: "<secret key>",

      // Kredensial sementara dapat digunakan dengan awsSessionToken.
      // Baca selengkapnya di https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
      awsSessionToken: "<session_token>",

      // awsRegion mengubah region aws tujuan permintaan
      // dikirim. Secara default, SDK membaca AWS_REGION, dan jika
      // tidak ada, menggunakan default us-east-1. Perhatikan bahwa
      // SDK tidak membaca ~/.aws/config untuk region.
      awsRegion: "us-west-2"
    });

    const message = await client.messages.create({
      model: "global.anthropic.claude-opus-4-6-v1",
      max_tokens: 256,
      messages: [{ role: "user", content: "Hello, world" }]
    });
    console.log(message);
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
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
            .Select(block => block.Value)
            .OfType<TextBlock>()
            .Select(textBlock => textBlock.Text)));
    ```
  </Tab>

  <Tab title="Go">
    ```go
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
    	fmt.Println(message.Content)
    ```
  </Tab>

  <Tab title="Java">
    ```java
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
  </Tab>

  <Tab title="PHP">
    ```php
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
  </Tab>

  <Tab title="Ruby">
    ```ruby
    require "anthropic"

    client = Anthropic::BedrockClient.new

    message = client.messages.create(
      model: "global.anthropic.claude-opus-4-6-v1",
      max_tokens: 256,
      messages: [{role: "user", content: "Hello, world"}]
    )

    puts message.content.first.text
    ```
  </Tab>

  <Tab title="Boto3 (Python)">
    ```python
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
  </Tab>
</Tabs>

Lihat [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk detail lebih lanjut, dan [dokumentasi resmi Bedrock](https://docs.aws.amazon.com/bedrock/).

### Autentikasi bearer token

Anda dapat melakukan autentikasi ke Bedrock menggunakan bearer token alih-alih kredensial AWS. Ini berguna di lingkungan perusahaan di mana tim memerlukan akses ke Bedrock tanpa harus mengelola kredensial AWS, IAM role, atau izin tingkat akun.

Pendekatan paling sederhana adalah mengatur variabel lingkungan `AWS_BEARER_TOKEN_BEDROCK`, yang dideteksi secara otomatis oleh setiap SDK saat menyelesaikan kredensial dari lingkungan.

Untuk menyediakan token secara programatik:

<Tabs>
  <Tab title="cURL">
    <Note>
      Bagian ini menunjukkan cara mengonfigurasi bearer token di klien SDK. SDK juga membaca token dari variabel lingkungan `AWS_BEARER_TOKEN_BEDROCK`. Untuk membuat permintaan HTTP langsung dengan bearer token, lihat [dokumentasi Amazon Bedrock](https://docs.aws.amazon.com/bedrock/).
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      CLI `ant` tidak mendukung Amazon Bedrock. Gunakan salah satu contoh SDK sebagai gantinya.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python
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
  </Tab>

  <Tab title="TypeScript">
    ```typescript
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
  </Tab>

  <Tab title="C#">
    ```csharp
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
  </Tab>

  <Tab title="Go">
    ```go
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
  </Tab>

  <Tab title="Java">
    ```java
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
  </Tab>

  <Tab title="PHP">
    ```php
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
  </Tab>

  <Tab title="Ruby">
    ```ruby
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
  </Tab>
</Tabs>

## Pencatatan aktivitas

Bedrock menyediakan [layanan pencatatan pemanggilan](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) yang memungkinkan Anda mencatat prompt dan completion yang terkait dengan penggunaan Anda.

Anthropic merekomendasikan agar Anda mencatat aktivitas Anda setidaknya dalam periode bergulir 30 hari untuk memahami aktivitas Anda dan menyelidiki potensi penyalahgunaan.

<Note>
  Mengaktifkan layanan ini tidak memberikan AWS atau Anthropic akses apa pun ke konten Anda.
</Note>

## Dukungan fitur

Untuk daftar fitur lengkap dengan ketersediaan di Amazon Bedrock, lihat [Ikhtisar fitur](https://platform.claude.com/docs/id/build-with-claude/overview).

### Sorotan fitur yang didukung

* [Messages API](https://platform.claude.com/docs/id/api/messages/create)
* [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)
* [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)
* [Penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview), termasuk [alat Bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool), [alat Computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool), [alat Memory](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool), dan [alat Text editor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool)
* [Kutipan](https://platform.claude.com/docs/id/build-with-claude/citations)
* [Output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs)

### Fitur yang tidak didukung

* Sumber input (sumber URL untuk gambar dan dokumen, Files API)
* Alat sisi server (eksekusi kode, pencarian web, web fetch, advisor)
* Infrastruktur agen (Agent Skills, konektor MCP, pemanggilan alat programatik)
* Endpoint API (Message Batches, Models, Admin, Compliance, Usage and Cost)
* Claude Managed Agents
* Fallback sisi server ([parameter `fallbacks`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback); gunakan [pola fallback sisi klien](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) sebagai gantinya)
* Caching prompt otomatis ([field `cache_control` tingkat atas](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching); gunakan [breakpoint cache eksplisit](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#explicit-cache-breakpoints) sebagai gantinya)
* Toolset [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) dan [browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) (`computer_toolset_20260801` dan `browser_toolset_20260801` saat ini tidak tersedia di Amazon Bedrock; versi beta alat computer use tetap tersedia)

### Dukungan PDF di Bedrock

Dukungan PDF tersedia di Bedrock melalui Converse API maupun InvokeModel API. Untuk informasi terperinci tentang kemampuan dan batasan pemrosesan PDF, lihat [dukungan PDF Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/pdf-support#amazon-bedrock-pdf-support).

**Pertimbangan penting bagi pengguna Converse API:**

* Analisis PDF visual (bagan, gambar, tata letak) memerlukan kutipan diaktifkan
* Tanpa kutipan, hanya ekstraksi teks dasar yang tersedia
* Untuk kontrol penuh tanpa kutipan paksa, gunakan InvokeModel API

### Pesan sistem di tengah percakapan di Bedrock

[Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) tersedia melalui InvokeModel API untuk Claude Fable 5 dan Claude Opus 4.8. Seperti dijelaskan dalam catatan di bawah [ID model API](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#api-model-ids), permintaan ini dilayani oleh infrastruktur yang sama dengan endpoint [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock). Tidak diperlukan header beta. Fitur ini tidak tersedia di Claude Sonnet 5; gunakan field `system` tingkat atas sebagai gantinya. Fitur ini tidak tersedia untuk model berversi ARN dalam tabel model di halaman ini.

**Bagi pengguna Converse API:** Converse API menerima instruksi sistem melalui [parameter `system`](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) tingkat atasnya. Untuk menambahkan instruksi sistem di tengah percakapan, gunakan InvokeModel API.

### Jendela konteks

Claude Fable 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6 memiliki ["context window" (jendela konteks) 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) di Amazon Bedrock. Model Claude lainnya, termasuk Sonnet 4.5 dan Sonnet 4 (deprecated), memiliki jendela konteks 200 ribu token.

Bedrock membatasi payload permintaan hingga 20 MB. Saat mengirim dokumen besar atau banyak gambar, Anda mungkin mencapai batas ini sebelum batas token.

## Endpoint global versus regional

Mulai dari **Claude Sonnet 4.5 dan semua model mendatang**, Bedrock menawarkan dua jenis endpoint:

* **Endpoint global:** Perutean dinamis untuk ketersediaan maksimum
* **Endpoint regional:** Perutean data yang terjamin melalui wilayah geografis tertentu

Endpoint regional dikenakan premi harga 10% di atas endpoint global.

<Note>
  Ini hanya berlaku untuk Claude Sonnet 4.5 dan model mendatang. Model lama (Claude Sonnet 4 (deprecated) dan sebelumnya) mempertahankan struktur harga yang sudah ada.
</Note>

### Kapan menggunakan setiap opsi

**Endpoint global (direkomendasikan):**

* Memberikan ketersediaan dan uptime maksimum
* Merutekan permintaan secara dinamis ke wilayah dengan kapasitas yang tersedia
* Tanpa premi harga
* Terbaik untuk aplikasi dengan residensi data yang fleksibel

**Endpoint regional (CRIS):**

* Merutekan lalu lintas melalui wilayah geografis tertentu
* Diperlukan untuk persyaratan residensi data dan kepatuhan
* Tersedia untuk AS, UE, Jepang, dan Asia-Pasifik
* Premi harga 10% mencerminkan biaya infrastruktur untuk kapasitas regional khusus

### Implementasi

**Menggunakan endpoint global (default untuk Opus 4.6, Sonnet 4.6, dan Sonnet 4.5):**

ID model untuk Claude Opus 4.6, Sonnet 4.6, dan Sonnet 4.5 sudah menyertakan prefiks `global.`:

<Tabs>
  <Tab title="cURL">
    <Note>
      Memanggil API `InvokeModel` dengan kredensial AWS memerlukan penandatanganan permintaan SigV4, yang ditangani secara otomatis oleh SDK di tab lainnya. Untuk endpoint Bedrock yang dapat Anda panggil dengan perintah cURL mandiri, lihat [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock#making-your-first-request).
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      CLI `ant` tidak mendukung Amazon Bedrock. Gunakan salah satu contoh SDK sebagai gantinya.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python
    from anthropic import AnthropicBedrock

    client = AnthropicBedrock(aws_region="us-west-2")

    message = client.messages.create(
        model="global.anthropic.claude-opus-4-6-v1",
        max_tokens=256,
        messages=[{"role": "user", "content": "Hello, world"}],
    )
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
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
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic.Bedrock;
    using Anthropic.Models.Messages;

    // Klien Bedrock C# menggunakan ID model dengan prefiks region untuk perutean global
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
  </Tab>

  <Tab title="Go">
    ```go
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
    ```
  </Tab>

  <Tab title="Java">
    ```java
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
  </Tab>

  <Tab title="PHP">
    ```php
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
  </Tab>

  <Tab title="Ruby">
    ```ruby
    require "anthropic"

    # Kredensial default menentukan region dari env var AWS_REGION
    client = Anthropic::BedrockClient.new

    message = client.messages.create(
      # Gunakan prefiks "global." untuk inferensi lintas-region global
      model: "global.anthropic.claude-opus-4-6-v1",
      max_tokens: 256,
      messages: [{role: "user", content: "Hello, world"}]
    )
    ```
  </Tab>
</Tabs>

**Menggunakan endpoint regional (CRIS):**

Untuk menggunakan endpoint regional, ganti prefiks `global.` dengan prefiks regional seperti `us.`:

<Tabs>
  <Tab title="cURL">
    <Note>
      Memanggil API `InvokeModel` dengan kredensial AWS memerlukan penandatanganan permintaan SigV4, yang ditangani secara otomatis oleh SDK di tab lainnya. Untuk endpoint Bedrock yang dapat Anda panggil dengan perintah cURL mandiri, lihat [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock#making-your-first-request).
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      CLI `ant` tidak mendukung Amazon Bedrock. Gunakan salah satu contoh SDK sebagai gantinya.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python
    from anthropic import AnthropicBedrock

    client = AnthropicBedrock(aws_region="us-west-2")

    # Menggunakan endpoint regional US (CRIS)
    message = client.messages.create(
        model="us.anthropic.claude-opus-4-6-v1",  # Regional prefix
        max_tokens=256,
        messages=[{"role": "user", "content": "Hello, world"}],
    )
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
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
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic.Bedrock;
    using Anthropic.Models.Messages;

    AnthropicBedrockClient client = new(
        new AnthropicBedrockPrivateKeyCredentials { Region = "us-west-2" }
    );

    // Menggunakan endpoint regional US (CRIS)
    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = "us.anthropic.claude-opus-4-6-v1", // Regional prefix
        MaxTokens = 256,
        Messages = [new() { Role = Role.User, Content = "Hello, world" }],
    });
    ```
  </Tab>

  <Tab title="Go">
    ```go
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

    	// Menggunakan endpoint regional US (CRIS)
    	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
    		Model:     "us.anthropic.claude-opus-4-6-v1", // Regional prefix
    		MaxTokens: 256,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, world")),
    		},
    	})
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.anthropic.bedrock.backends.BedrockBackend;
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.MessageCreateParams;

    // Menggunakan rantai penyedia kredensial AWS default
    AnthropicClient client = AnthropicOkHttpClient.builder()
      .backend(BedrockBackend.fromEnv())
      .build();

    // Menggunakan endpoint regional US (CRIS)
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
  </Tab>

  <Tab title="PHP">
    ```php
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
  </Tab>

  <Tab title="Ruby">
    ```ruby
    require "anthropic"

    # Menggunakan endpoint regional AS (CRIS)
    client = Anthropic::BedrockClient.new(aws_region: "us-west-2")

    message = client.messages.create(
      model: "us.anthropic.claude-opus-4-6-v1", # Regional prefix
      max_tokens: 256,
      messages: [{role: "user", content: "Hello, world"}]
    )
    ```
  </Tab>
</Tabs>

<Note>
  **Claude Mythos Preview** adalah model pratinjau riset yang tersedia bagi pelanggan yang diundang di Amazon Bedrock. Untuk informasi lebih lanjut, lihat [Project Glasswing](https://anthropic.com/glasswing).
</Note>

## Sumber daya tambahan

* **Harga Bedrock:** [Halaman harga Amazon Bedrock](https://aws.amazon.com/bedrock/pricing/)
* **Dokumentasi harga AWS:** [Panduan harga Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-pricing.html)
* **Postingan blog AWS:** [Introducing Claude Sonnet 4.5 in Amazon Bedrock](https://aws.amazon.com/blogs/aws/introducing-claude-sonnet-4-5-in-amazon-bedrock-anthropics-most-intelligent-model-best-for-coding-and-complex-agents/)
* **Detail harga Anthropic:** [Harga platform cloud](https://platform.claude.com/docs/id/about-claude/pricing#cloud-platform-pricing)
