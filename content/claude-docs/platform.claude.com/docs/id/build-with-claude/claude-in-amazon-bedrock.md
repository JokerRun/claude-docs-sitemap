---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 1186dd84a048c460f4d7784e67d7af437c4ca42e517e3610fbcc24a9fd941fce
---

# Claude in Amazon Bedrock (Opus 4.7 dan yang lebih baru)

Akses model Claude melalui Amazon Bedrock dengan autentikasi, penagihan, dan batas keamanan native AWS.

---

Panduan ini memandu Anda dalam menyiapkan dan melakukan panggilan API ke Claude in Amazon Bedrock. Claude in Amazon Bedrock berjalan pada infrastruktur yang dikelola AWS dengan nol akses operator (personel Anthropic tidak memiliki akses ke infrastruktur inferensi), memungkinkan Anda membangun aplikasi sensitif sepenuhnya di dalam batas keamanan AWS sambil menggunakan bentuk Messages API yang sama dengan yang Anda gunakan pada API pihak pertama Anthropic.

<Note>
  Halaman ini membahas Claude in Amazon Bedrock, yang menyajikan Claude melalui Messages API di `/anthropic/v1/messages` pada infrastruktur yang dikelola AWS. Integrasi Amazon Bedrock sebelumnya (API `InvokeModel` dan `Converse` dengan pengidentifikasi model berversi ARN) tetap tersedia dan didokumentasikan di [Claude on Amazon Bedrock (Opus 4.6 dan yang lebih lama)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy). Untuk alternatif yang dioperasikan Anthropic di AWS dengan penagihan AWS Marketplace dan akses fitur yang biasanya tersedia di hari yang sama, lihat [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws).
</Note>

## Akses

Claude Fable 5, Claude Opus 4.8, Claude Sonnet 5, Claude Opus 4.7, dan Claude Haiku 4.5 terbuka untuk semua pelanggan Amazon Bedrock. Claude Mythos Preview memerlukan undangan; lihat [Project Glasswing](https://anthropic.com/glasswing). Untuk ketersediaan region, lihat [Region](#regions).

## Prasyarat

Sebelum memulai, pastikan Anda memiliki:

* Akun AWS dengan [akses model Amazon Bedrock](https://console.aws.amazon.com/bedrock/home#/modelaccess) yang diaktifkan untuk model Claude yang ingin Anda gunakan.
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) yang terinstal dan terkonfigurasi (opsional, untuk manajemen kredensial).

Claude Mythos Preview juga memerlukan akun AWS khusus yang telah dimasukkan ke dalam daftar izin (allowlist) oleh tim Bedrock Marketplace. Account executive Anthropic Anda dapat mengirimkan ID akun Anda untuk dimasukkan ke daftar izin (biasanya diproses dalam 24 jam), dan AWS akan mengirimkan email sambutan setelah selesai.

## Autentikasi

Claude in Amazon Bedrock mendukung tiga jalur autentikasi. Pilih yang paling sesuai dengan persyaratan keamanan Anda.

### Service role Bedrock (direkomendasikan)

Gunakan service role Bedrock dengan kunci yang dikelola AWS untuk akses jangka panjang yang paling aman:

<Steps>
  <Step title="Admin: sediakan service role">
    Administrator AWS menyediakan service role Bedrock dan memberikan izin `iam:PassRole` kepada developer pada ARN service role tersebut.
  </Step>

  <Step title="Developer: teruskan role">
    Saat memanggil API, Bedrock mengambil alih (assume) service role atas nama Anda. Lihat [dokumentasi Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-mantle.html) untuk cara mengaitkan role dengan permintaan Anda.
  </Step>
</Steps>

### IAM assumed role

Untuk akses terfederasi identitas dengan sesi maksimum 12 jam:

<Steps>
  <Step title="Admin: konfigurasikan IAM role">
    Buat IAM role yang dibatasi cakupannya pada model Claude Anda. Trust policy menyebutkan penyedia identitas Anda (SAML, OIDC, atau AWS Identity Center). Permissions policy hanya memberikan `bedrock-mantle:CreateInference` pada ARN model yang diizinkan.
  </Step>

  <Step title="Developer: autentikasi dan assume">
    Lakukan autentikasi melalui penyedia identitas korporat Anda, lalu assume IAM role tersebut. AWS STS menerbitkan kredensial sementara yang digunakan SDK atau CLI untuk menandatangani permintaan.
  </Step>
</Steps>

### Bearer token

Untuk akses jangka pendek tanpa IAM role (maksimum 12 jam, paling tidak disarankan):

<Steps>
  <Step title="Admin: batasi jenis token">
    Blokir kunci jangka panjang dengan melampirkan kebijakan yang menolak `bedrock:CallWithBearerToken` kecuali kondisi `bedrock:BearerTokenType` cocok dengan token jangka pendek.
  </Step>

  <Step title="Developer: buat token">
    Gunakan CLI `aws-bedrock-token-generator` untuk membuat bearer token. Teruskan token tersebut di header `x-api-key` pada setiap permintaan.
  </Step>
</Steps>

## Instal SDK

[SDK klien](/docs/id/cli-sdks-libraries/overview) Anthropic mendukung Claude in Amazon Bedrock melalui paket atau modul khusus Bedrock.

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
    <Tabs>
      <Tab title="Gradle">
        ```kotlin
        implementation("com.anthropic:anthropic-java-bedrock:2.50.0")
        ```
      </Tab>

      <Tab title="Maven">
        ```xml
        <dependency>
            <groupId>com.anthropic</groupId>
            <artifactId>anthropic-java-bedrock</artifactId>
            <version>2.50.0</version>
        </dependency>
        ```
      </Tab>
    </Tabs>
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
    gem "aws-sdk-core"
    ```
  </Tab>
</Tabs>

## Membuat permintaan pertama Anda

Endpoint mengikuti pola `https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages`. Berbeda dengan integrasi berbasis `InvokeModel`, endpoint ini menggunakan streaming SSE standar dan bentuk body permintaan yang sama dengan API pihak pertama Anthropic.

SDK menyelesaikan kredensial dan region menggunakan urutan prioritas AWS standar: argumen konstruktor, lalu variabel lingkungan (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_REGION`), lalu file konfigurasi AWS dan rantai kredensial (SSO, assumed role, ECS task role, IMDS).

<Tabs>
  <Tab title="cURL">
    ```bash
    curl https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages \
      --aws-sigv4 "aws:amz:us-east-1:bedrock-mantle" \
      --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
      -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
      -H "content-type: application/json" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "anthropic.claude-opus-4-8",
        "max_tokens": 1024,
        "messages": [
          {"role": "user", "content": "Hello, Claude"}
        ]
      }'
    ```
  </Tab>

  <Tab title="CLI">
    CLI `ant` tidak mendukung Amazon Bedrock. Gunakan cURL atau SDK.
  </Tab>

  <Tab title="Python">
    ```python
    from anthropic import AnthropicBedrockMantle

    client = AnthropicBedrockMantle(aws_region="us-east-1")

    message = client.messages.create(
        model="anthropic.claude-opus-4-8",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, Claude"}],
    )

    print(message.content[0].text)
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import { AnthropicBedrockMantle } from "@anthropic-ai/bedrock-sdk";

    const client = new AnthropicBedrockMantle({
      awsRegion: "us-east-1"
    });

    const message = await client.messages.create({
      model: "anthropic.claude-opus-4-8",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    });

    const block = message.content[0];
    if (block.type === "text") {
      console.log(block.text);
    }
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic.Bedrock;
    using Anthropic.Models.Messages;

    var client = new AnthropicBedrockMantleClient(new() { AwsRegion = "us-east-1" });

    var message = await client.Messages.Create(new()
    {
        Model = "anthropic.claude-opus-4-8",
        MaxTokens = 1024,
        Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
    });

    if (message.Content[0].Value is TextBlock block)
        Console.WriteLine(block.Text);
    ```
  </Tab>

  <Tab title="Go">
    ```go
    client, err := bedrock.NewMantleClient(context.Background(), bedrock.MantleClientConfig{
    	AWSRegion: "us-east-1",
    })
    if err != nil {
    	panic(err)
    }

    message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
    	Model:     "anthropic.claude-opus-4-8",
    	MaxTokens: 1024,
    	Messages: []anthropic.MessageParam{
    		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
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
    import com.anthropic.bedrock.backends.BedrockMantleBackend;
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.Message;
    import com.anthropic.models.messages.MessageCreateParams;

    void main() {
        AnthropicClient client = AnthropicOkHttpClient.builder()
            .backend(BedrockMantleBackend.fromEnv())
            .build();

        Message message = client.messages().create(
            MessageCreateParams.builder()
                .model("anthropic.claude-opus-4-8")
                .maxTokens(1024)
                .addUserMessage("Hello, Claude")
                .build()
        );

        IO.println(message.content().getFirst().asText().text());
    }
    ```
  </Tab>

  <Tab title="PHP">
    ```php
    use Anthropic\Bedrock\MantleClient;

    $client = new MantleClient(awsRegion: 'us-east-1');

    $message = $client->messages->create(
        model: 'anthropic.claude-opus-4-8',
        maxTokens: 1024,
        messages: [
            ['role' => 'user', 'content' => 'Hello, Claude'],
        ],
    );

    echo $message->content[0]->text;
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    require "anthropic"

    client = Anthropic::BedrockMantleClient.new(aws_region: "us-east-1")

    message = client.messages.create(
      model: "anthropic.claude-opus-4-8",
      max_tokens: 1024,
      messages: [{role: "user", content: "Hello, Claude"}]
    )

    puts message.content[0].text
    ```
  </Tab>
</Tabs>

<Tip>
  Anda juga dapat menggunakan klien `Anthropic` standar: atur `base_url` ke `https://bedrock-mantle.{region}.api.aws/anthropic` dan teruskan bearer token Anda sebagai `api_key`. Jalur ini hanya mendukung autentikasi bearer-token. Penandatanganan SigV4 memerlukan klien khusus.
</Tip>

## Model yang didukung

ID model di Claude in Amazon Bedrock memiliki prefiks penyedia `anthropic.`. Kemampuan dan perilaku model didokumentasikan di halaman [Ikhtisar model](/docs/id/about-claude/models/overview).

| Model                 | Model ID                        | Akses                                                                        |
| --------------------- | ------------------------------- | ---------------------------------------------------------------------------- |
| Claude Fable 5        | anthropic.claude-fable-5        | Terbuka                                                                      |
| Claude Opus 4.8       | anthropic.claude-opus-4-8       | Terbuka                                                                      |
| Claude Opus 4.7       | anthropic.claude-opus-4-7       | Terbuka                                                                      |
| Claude Sonnet 5       | `anthropic.claude-sonnet-5`     | Terbuka                                                                      |
| Claude Haiku 4.5      | anthropic.claude-haiku-4-5      | Terbuka                                                                      |
| Claude Mythos Preview | anthropic.claude-mythos-preview | Hanya dengan undangan ([Project Glasswing](https://anthropic.com/glasswing)) |

<Tip>
  Melakukan upgrade ke model Claude yang lebih baru? Di Claude Code, jalankan `/claude-api migrate` untuk menerapkan penggantian ID model dan perubahan parameter yang bersifat breaking di seluruh codebase Anda. Skill ini mendeteksi platform cloud mana yang ditargetkan oleh kode Anda dan menyesuaikan format ID model serta perubahan fitur untuk platform tersebut. Lihat [Migrasi ke model Claude yang lebih baru](/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

## Dukungan fitur

Untuk daftar fitur lengkap beserta ketersediaannya di Amazon Bedrock, lihat [Ikhtisar fitur](/docs/id/build-with-claude/overview).

### Sorotan fitur yang didukung

* [Messages API](/docs/id/api/messages/create) (`/anthropic/v1/messages`)
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

## Region

Claude in Amazon Bedrock tersedia di region AWS berikut. Amazon Bedrock menawarkan dua jenis endpoint:

* **Global:** perutean dinamis di semua region yang tersedia untuk ketersediaan maksimum. Tanpa premi harga.
* **Regional:** endpoint diarahkan ke satu region AWS yang Anda tentukan, untuk persyaratan residensi data. Endpoint regional dikenakan premi harga 10% dibandingkan endpoint global. Untuk merutekan ke beberapa region dalam satu geografi, gunakan [inference profile](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) (US, EU, JP, atau AU). Region yang ditandai **Hanya dalam region** di tabel mendukung perutean satu region langsung tanpa inference profile.

Endpoint global tersedia untuk Claude Fable 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, dan Claude Haiku 4.5. Claude Mythos Preview hanya regional dan tersedia di `us-east-1`.

| Region AWS       | Lokasi                      | Jenis endpoint                 |
| ---------------- | --------------------------- | ------------------------------ |
| `af-south-1`     | Afrika (Cape Town)          | Global                         |
| `ap-northeast-1` | Asia Pasifik (Tokyo)        | Global, JP, Hanya dalam region |
| `ap-northeast-2` | Asia Pasifik (Seoul)        | Global                         |
| `ap-northeast-3` | Asia Pasifik (Osaka)        | Global, JP                     |
| `ap-south-1`     | Asia Pasifik (Mumbai)       | Global                         |
| `ap-south-2`     | Asia Pasifik (Hyderabad)    | Global                         |
| `ap-southeast-1` | Asia Pasifik (Singapura)    | Global                         |
| `ap-southeast-2` | Asia Pasifik (Sydney)       | Global, AU                     |
| `ap-southeast-3` | Asia Pasifik (Jakarta)      | Global                         |
| `ap-southeast-4` | Asia Pasifik (Melbourne)    | Global, AU, Hanya dalam region |
| `ca-central-1`   | Kanada (Tengah)             | Global, US                     |
| `ca-west-1`      | Kanada Barat (Calgary)      | Global                         |
| `eu-central-1`   | Eropa (Frankfurt)           | Global, EU                     |
| `eu-central-2`   | Eropa (Zurich)              | Global, EU                     |
| `eu-north-1`     | Eropa (Stockholm)           | Global, EU, Hanya dalam region |
| `eu-south-1`     | Eropa (Milan)               | Global, EU                     |
| `eu-south-2`     | Eropa (Spanyol)             | Global, EU                     |
| `eu-west-1`      | Eropa (Irlandia)            | Global, EU, Hanya dalam region |
| `eu-west-2`      | Eropa (London)              | Global, EU                     |
| `eu-west-3`      | Eropa (Paris)               | Global, EU                     |
| `il-central-1`   | Israel (Tel Aviv)           | Global                         |
| `me-central-1`   | Timur Tengah (UEA)          | Global                         |
| `sa-east-1`      | Amerika Selatan (São Paulo) | Global                         |
| `us-east-1`      | AS Timur (Virginia Utara)   | Global, US, Hanya dalam region |
| `us-east-2`      | AS Timur (Ohio)             | Global, US, Hanya dalam region |
| `us-west-1`      | AS Barat (California Utara) | Global, US                     |
| `us-west-2`      | AS Barat (Oregon)           | Global, US, Hanya dalam region |

## Kuota

Kuota default adalah 2 juta token input per menit (TPM). Anda dapat meminta hingga 4 juta TPM input tanpa persetujuan tambahan dari Anthropic. AWS memberlakukan batas permintaan per menit (RPM) di sisi Bedrock; hubungi dukungan AWS untuk penyesuaian RPM.

## Retensi data

Penanganan data untuk penawaran ini diatur oleh Amazon Bedrock. Untuk detailnya, lihat [Perlindungan data di Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html).

## Pemantauan dan pencatatan log

Claude in Amazon Bedrock mengirimkan log ke CloudWatch dan CloudTrail. Anthropic merekomendasikan untuk menyimpan log aktivitas setidaknya secara bergulir selama 30 hari untuk memahami pola penggunaan dan menyelidiki potensi masalah.

## Dukungan

Untuk dukungan, hubungi **[bedrock-ant-eap@amazon.com](mailto:bedrock-ant-eap@amazon.com)**. Sertakan ID akun AWS Anda dan `request-id` dari respons API yang gagal.

<Note>
  **Claude Mythos Preview** adalah model pratinjau riset yang tersedia bagi pelanggan yang diundang di Amazon Bedrock. Untuk informasi lebih lanjut, lihat [Project Glasswing](https://anthropic.com/glasswing).
</Note>
