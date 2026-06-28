---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 299bf440846ba444b3344f55b687a243d34a5a5e1f5f70264ce124a18428c47b
---

# Claude di Vertex AI

Model Claude dari Anthropic tersedia melalui [Vertex AI](https://cloud.google.com/vertex-ai).

---

API Vertex untuk mengakses Claude hampir identik dengan [Messages API](/docs/id/api/messages/create), dengan dua perbedaan utama dalam format permintaan:

* Di Vertex, `model` tidak dikirimkan dalam body permintaan. Sebagai gantinya, model ditentukan dalam URL endpoint Google Cloud.
* Di Vertex, `anthropic_version` dikirimkan dalam body permintaan (bukan sebagai header), dan harus diatur ke nilai `vertex-2023-10-16`.

Vertex juga didukung oleh [client SDK](/docs/id/cli-sdks-libraries/overview) resmi Anthropic. Panduan ini memandu Anda dalam membuat permintaan ke Claude di Vertex AI menggunakan salah satu client SDK Anthropic.

Perhatikan bahwa panduan ini mengasumsikan Anda sudah memiliki proyek GCP yang dapat menggunakan Vertex AI. Lihat [Model Claude Anthropic di Vertex AI](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) untuk informasi lebih lanjut tentang penyiapan yang diperlukan dan panduan lengkapnya.

## Menginstal SDK untuk mengakses Vertex AI

Pertama, instal [client SDK](/docs/id/cli-sdks-libraries/overview) Anthropic untuk bahasa pemrograman pilihan Anda.

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
      implementation("com.anthropic:anthropic-java-vertex:2.40.0")
      ```

      ```xml Maven
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java-vertex</artifactId>
          <version>2.40.0</version>
      </dependency>
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.vertex.backends.VertexBackend;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.Model;
      // ...
              AnthropicClient client = AnthropicOkHttpClient.builder()
                  .backend(VertexBackend.fromEnv())
                  .build();

              MessageCreateParams params = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_4_8)
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

Perhatikan bahwa ketersediaan model Anthropic bervariasi berdasarkan region. Cari "Claude" di [Vertex AI Model Garden](https://cloud.google.com/model-garden) atau kunjungi [Model Claude Anthropic](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) untuk informasi terbaru.

#### ID model API

Istilah siklus hidup (Deprecated, Retired) didefinisikan dalam [Deprekasi model](/docs/id/about-claude/model-deprecations). Tanggal siklus hidup pada platform yang dioperasikan mitra ditetapkan oleh mitra dan dapat berbeda dari jadwal API Claude. Untuk tanggal penghentian terkini dari model apa pun di Vertex AI, lihat [dokumentasi Google Cloud untuk model Claude di Vertex AI](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude).

| Model                        | ID model API Vertex AI      |
| ---------------------------- | --------------------------- |
| Claude Fable 5               | claude-fable-5              |
| Claude Opus 4.8              | claude-opus-4-8             |
| Claude Opus 4.7              | claude-opus-4-7             |
| Claude Opus 4.6              | claude-opus-4-6             |
| Claude Sonnet 4.6            | claude-sonnet-4-6           |
| Claude Sonnet 4.5            | claude-sonnet-4-5\@20250929 |
| Claude Sonnet 4 Deprecated.  | claude-sonnet-4\@20250514   |
| Claude Sonnet 3.7 Retired.   | claude-3-7-sonnet\@20250219 |
| Claude Opus 4.5              | claude-opus-4-5\@20251101   |
| Claude Opus 4.1 Deprecated.  | claude-opus-4-1\@20250805   |
| Claude Opus 4 Deprecated.    | claude-opus-4\@20250514     |
| Claude Haiku 4.5             | claude-haiku-4-5\@20251001  |
| Claude Haiku 3.5 Deprecated. | claude-3-5-haiku\@20241022  |

<Tip>
  Melakukan upgrade ke model Claude yang lebih baru? Di Claude Code, jalankan `/claude-api migrate` untuk menerapkan penggantian ID model dan perubahan parameter yang bersifat breaking di seluruh codebase Anda. Skill ini mendeteksi platform cloud mana yang ditargetkan oleh kode Anda dan menyesuaikan format ID model serta perubahan fitur untuk platform tersebut. Lihat [Migrasi ke model Claude yang lebih baru](/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

### Membuat permintaan

Sebelum menjalankan permintaan, Anda mungkin perlu menjalankan `gcloud auth application-default login` untuk melakukan autentikasi dengan GCP.

Contoh berikut menunjukkan cara menghasilkan teks dari Claude di Vertex AI:

<CodeGroup>
  ```bash cURL
  MODEL_ID=claude-opus-4-8
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
    "max_tokens": 100
  }'
  ```

  ```bash CLI
  # CLI ant tidak mendukung Vertex AI.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "global"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-8",
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

  // Melalui alur standar `google-auth-library`.
  const client = new AnthropicVertex({
    projectId,
    region
  });

  async function main() {
    const result = await client.messages.create({
      model: "claude-opus-4-8",
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

  ```csharp C#
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
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Menggunakan kredensial Google Cloud default
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("%+v\n", message)
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.vertex.backends.VertexBackend;
  // ...
      // Menggunakan kredensial Google Cloud default
      AnthropicClient client = AnthropicOkHttpClient.builder()
        .backend(VertexBackend.fromEnv())
        .build();

      Message message = client
        .messages()
        .create(
          MessageCreateParams.builder()
            .model("claude-opus-4-8")
            .maxTokens(100)
            .addUserMessage("Hey Claude!")
            .build()
        );

      System.out.println(message);
  ```

  ```php PHP
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
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

Lihat [client SDK](/docs/id/cli-sdks-libraries/overview) dan [dokumentasi resmi Vertex AI](https://cloud.google.com/vertex-ai/docs) untuk detail lebih lanjut.

Claude juga tersedia melalui [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

## Retensi data

Penanganan data untuk penawaran ini diatur oleh Google Cloud Vertex AI. Untuk detailnya, lihat [Vertex AI dan zero data retention](https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance).

## Pencatatan aktivitas

Vertex menyediakan [layanan pencatatan permintaan-respons](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging) yang memungkinkan pelanggan mencatat prompt dan completion yang terkait dengan penggunaan Anda.

Anthropic merekomendasikan agar Anda mencatat aktivitas Anda setidaknya secara bergulir selama 30 hari untuk memahami aktivitas Anda dan menyelidiki potensi penyalahgunaan.

<Note>
  Mengaktifkan layanan ini tidak memberikan akses apa pun kepada Google atau Anthropic terhadap konten Anda.
</Note>

## Dukungan fitur

Untuk daftar fitur lengkap beserta ketersediaannya di Vertex AI, lihat [Ikhtisar fitur](/docs/id/build-with-claude/overview).

### Sorotan fitur yang didukung

* [Messages API](/docs/id/api/messages/create)
* [Caching prompt](/docs/id/build-with-claude/prompt-caching)
* [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking)
* [Penggunaan alat](/docs/id/agents-and-tools/tool-use/overview), termasuk [Bash tool](/docs/id/agents-and-tools/tool-use/bash-tool), [Computer use tool](/docs/id/agents-and-tools/tool-use/computer-use-tool), [Memory tool](/docs/id/agents-and-tools/tool-use/memory-tool), dan [Text editor tool](/docs/id/agents-and-tools/tool-use/text-editor-tool)
* [Web search tool](/docs/id/agents-and-tools/tool-use/web-search-tool)
* [Citations](/docs/id/build-with-claude/citations)
* [Structured outputs](/docs/id/build-with-claude/structured-outputs)

### Fitur yang tidak didukung

* Sumber input (sumber URL untuk gambar dan dokumen, Files API)
* Alat sisi server (code execution, web fetch, advisor)
* Infrastruktur agen (Agent Skills, MCP connector, programmatic tool calling)
* Endpoint API (Message Batches, Models, Admin, Compliance, Usage and Cost)
* Claude Managed Agents
* Fallback sisi server ([parameter `fallbacks`](/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback); gunakan [pola fallback sisi klien](/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) sebagai gantinya)

### Jendela konteks

Claude Fable 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6 memiliki ["context window" (jendela konteks) 1 juta token](/docs/id/build-with-claude/context-windows) di Vertex AI. Model Claude lainnya, termasuk Sonnet 4.5 dan Sonnet 4 (deprecated), memiliki jendela konteks 200 ribu token.

Vertex AI membatasi payload permintaan hingga 30 MB. Saat mengirim dokumen besar atau banyak gambar, Anda mungkin mencapai batas ini sebelum mencapai batas token.

## Endpoint global, multi-region, dan regional

Vertex AI menawarkan tiga jenis endpoint:

* **Endpoint global:** Perutean dinamis untuk ketersediaan maksimum
* **Endpoint multi-region:** Perutean dinamis dalam area geografis (misalnya, Amerika Serikat atau Uni Eropa) untuk residensi data dengan ketersediaan tinggi
* **Endpoint regional:** Perutean data yang dijamin melalui region geografis tertentu

Endpoint regional dan multi-region dikenakan premium harga 10% dibandingkan endpoint global.

<Note>
  Ini berlaku untuk Claude Sonnet 4.5 dan model yang lebih baru saja. Model yang lebih lama (Claude Sonnet 4 (deprecated), Opus 4 (deprecated), dan sebelumnya) mempertahankan struktur harga yang sudah ada.
</Note>

### Kapan menggunakan setiap opsi

**Endpoint global (direkomendasikan):**

* Menyediakan ketersediaan dan uptime maksimum
* Merutekan permintaan secara dinamis ke region dengan kapasitas yang tersedia
* Tanpa premium harga
* Terbaik untuk aplikasi di mana residensi data bersifat fleksibel
* Hanya mendukung lalu lintas pay-as-you-go (provisioned throughput memerlukan endpoint regional)

**Endpoint multi-region:**

* Merutekan permintaan secara dinamis di seluruh region dalam area geografis (saat ini `us` dan `eu`)
* Berguna ketika Anda membutuhkan residensi data dalam geografi yang luas tetapi menginginkan ketersediaan yang lebih tinggi daripada satu region
* Premium harga 10% dibandingkan endpoint global
* Hanya mendukung lalu lintas pay-as-you-go (provisioned throughput memerlukan endpoint regional)

**Endpoint regional:**

* Merutekan lalu lintas melalui region geografis tertentu
* Diperlukan untuk residensi data region tunggal, mandat kepatuhan yang ketat, atau provisioned throughput
* Mendukung pay-as-you-go dan provisioned throughput
* Premium harga 10% mencerminkan biaya infrastruktur untuk kapasitas regional khusus

### Implementasi

**Menggunakan endpoint global (direkomendasikan):**

Atur parameter `region` ke `"global"` saat menginisialisasi klien:

<CodeGroup>
  ```bash CLI
  # CLI ant tidak mendukung Vertex AI.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "global"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  ```

  ```csharp C#
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
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Menggunakan kredensial Google Cloud default
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
  	)

  	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	_ = message
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.vertex.backends.VertexBackend;

  void main() {
      // Menggunakan kredensial Google Cloud default
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .region("global")
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model("claude-opus-4-8")
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
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
      model: 'claude-opus-4-8',
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

**Menggunakan endpoint multi-region:**

Atur parameter `region` ke pengidentifikasi multi-region: `"us"` untuk Amerika Serikat atau `"eu"` untuk Uni Eropa. SDK merutekan permintaan ke endpoint multi-region yang sesuai (`https://aiplatform.us.rep.googleapis.com` atau `https://aiplatform.eu.rep.googleapis.com`), yang secara dinamis menyeimbangkan lalu lintas di seluruh region dalam geografi tersebut.

<CodeGroup>
  ```bash CLI
  # CLI ant tidak mendukung Vertex AI.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "us"  # Multi-region identifier: "us" or "eu"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-8",
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
  const region = "us"; // Multi-region identifier: "us" or "eu"

  const client = new AnthropicVertex({
    projectId,
    region
  });

  const result = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  ```

  ```csharp C#
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
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Pengidentifikasi multi-region: "us" atau "eu"
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "us", "MY_PROJECT_ID"),
  	)

  	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	_ = message
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.vertex.backends.VertexBackend;

  void main() {
      // Pengidentifikasi multi-region: "us" atau "eu"
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
                  .model("claude-opus-4-8")
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
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
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "us", # Multi-region identifier: "us" or "eu"
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

**Menggunakan endpoint regional:**

Tentukan region spesifik seperti `"us-east1"` atau `"europe-west1"`:

<CodeGroup>
  ```bash CLI
  # CLI ant tidak mendukung Vertex AI.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "us-east1"  # Specify a specific region

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  ```

  ```csharp C#
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
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Tentukan region tertentu
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "us-east1", "MY_PROJECT_ID"),
  	)

  	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	_ = message
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.vertex.backends.VertexBackend;

  void main() {
      // Menggunakan kredensial Google Cloud default dengan region tertentu
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
                  .model("claude-opus-4-8")
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
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
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "us-east1", # Specify a specific region
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

<Note>
  Claude Mythos Preview adalah pratinjau riset yang tersedia untuk pelanggan yang diundang di Vertex AI. Untuk informasi lebih lanjut, lihat [Project Glasswing](https://anthropic.com/glasswing).
</Note>

## Sumber daya tambahan

* **Harga Vertex AI:** [cloud.google.com/vertex-ai/generative-ai/pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
* **Dokumentasi model Claude:** [Claude di Vertex AI](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude)
* **Postingan blog Google:** [Endpoint global untuk model Claude](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai)
* **Detail harga Anthropic:** [Harga platform cloud](/docs/id/about-claude/pricing#cloud-platform-pricing)
