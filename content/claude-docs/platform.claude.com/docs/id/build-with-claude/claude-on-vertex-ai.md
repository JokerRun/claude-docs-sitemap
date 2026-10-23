---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai
fetched_at: 2026-10-23T02:21:28.653315Z
sha256: 0323e47cc245772b87142a3eb8224a516df888ca87505653eaa6bbb4ac8151ce
---

---
title: Claude Models on Google Cloud (Google managed)
url: https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed
description: Google mengoperasikan Claude Models on Google Cloud (Google managed) sebagai bagian dari Google Cloud's Agent Platform. Anda dapat memanggil Claude dengan SDK klien Anthropic.
---

[Claude Models on Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/overview) membandingkan kedua penawaran Google Cloud. Halaman tersebut juga menunjukkan cara mengetahui penawaran mana yang Anda gunakan.

## Sebelum melakukan panggilan API

Untuk menggunakan Claude Models on Google Cloud (Google managed), Anda memerlukan:

1. Proyek Google Cloud yang dapat menggunakan Agent Platform. Untuk langkah-langkah penyiapan, lihat halaman [Anthropic Claude models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) dari Google Cloud.
2. [gcloud CLI](https://cloud.google.com/sdk/docs/install) yang terinstal, untuk pengembangan lokal.
3. Untuk identitas yang melakukan panggilan, peran IAM yang mencakup izin `aiplatform.endpoints.predict`, seperti Agent Platform User (`roles/aiplatform.user`). Untuk detailnya, lihat halaman [Agent Platform partner models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/use-partner-models) dari Google Cloud.
4. Kredensial Google Cloud untuk identitas tersebut. Untuk contoh SDK, Anda mungkin perlu menjalankan `gcloud auth application-default login` untuk melakukan autentikasi dengan Google Cloud. Contoh cURL untuk Claude Models on Google Cloud (Google managed) mendapatkan token-nya dengan `gcloud auth print-access-token`. Perintah tersebut menggunakan login milik gcloud CLI sendiri, bukan Application Default Credentials. Untuk contoh-contoh tersebut, jalankan `gcloud auth login` atau `gcloud init` terlebih dahulu.

### Menginstal SDK

[SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) Anthropic mendukung Claude Models on Google Cloud (Google managed) melalui `AnthropicVertex` (csharp: `AnthropicVertexClient`; go: `vertex.WithGoogleAuth`; java: `VertexBackend`; php: `Anthropic\Vertex\Client`; ruby: `Anthropic::VertexClient`). Instal paket yang menyediakannya:

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U "anthropic[vertex]"
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
    <CodeGroup exclude="shell, python, typescript, csharp, go, php, ruby">
      ```groovy Gradle
      implementation("com.anthropic:anthropic-java:3.1.0")
      implementation("com.anthropic:anthropic-java-vertex:3.1.0")
      ```

      ```xml Maven
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java</artifactId>
          <version>3.1.0</version>
      </dependency>
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java-vertex</artifactId>
          <version>3.1.0</version>
      </dependency>
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

CLI `ant` tidak mendukung Claude Models on Google Cloud (Google managed).

## Membuat permintaan

Permintaan ke Claude Models on Google Cloud (Google managed) dikirim ke URL endpoint Agent Platform yang diakhiri dengan `:rawPredict`. Permintaan streaming menggunakan `:streamRawPredict` sebagai gantinya.

Sebuah permintaan hampir identik dengan permintaan [Messages API](https://platform.claude.com/docs/id/api/messages/create). Perbedaannya terdapat pada dua hal utama:

* **Model:** URL endpoint menyebutkan nama model. Dalam permintaan cURL, jangan sertakan `model` di dalam body.
* **Versi:** Dalam permintaan cURL, teruskan `anthropic_version` di dalam body, bukan sebagai header. Atur nilainya ke `vertex-2023-10-16`, atau ke [versi API `2026-10-21`](https://platform.claude.com/docs/id/api/migration-2026-10-21).

Contoh-contoh berikut menggunakan endpoint global. Untuk jenis endpoint lainnya, lihat [Endpoint global, multi-region, dan regional](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#global-multi-region-and-regional-endpoints).

<CodeGroup exclude="shell:CLI">
  ```bash cURL
  curl https://aiplatform.googleapis.com/v1/projects/MY_PROJECT_ID/locations/global/publishers/anthropic/models/claude-opus-5-5:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
      "max_tokens": 100
    }'
  ```

  <CodeGroupItem language="CLI">
    CLI `ant` tidak mendukung Claude Models on Google Cloud (Google managed).
  </CodeGroupItem>

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "global"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-5-5",
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

  const result = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  console.log(JSON.stringify(result, null, 2));
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "global";

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 100,
      Messages = [new UserMessageParam { Content = "Hey Claude!" }]
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
  	// Menggunakan kredensial default Google Cloud
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
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
  import com.anthropic.models.messages.Model;
  import com.anthropic.vertex.backends.VertexBackend;
  import com.google.auth.oauth2.GoogleCredentials;

  void main() throws Exception {
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .googleCredentials(GoogleCredentials.getApplicationDefault())
                  .region("global")
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      Message message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5_5)
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Messages\TextBlock;
  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      region: 'global',
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      model: 'claude-opus-5-5',
  );

  foreach ($message->content as $block) {
      if ($block instanceof TextBlock) {
          echo $block->text . PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

### ID model API

| Model                                                                                                 | Agent Platform API model ID  |
| :---------------------------------------------------------------------------------------------------- | :--------------------------- |
| Claude Fable 5.1                                                                                      | `claude-fable-5-1`           |
| Claude Mythos 5.1 ([limited availability](https://support.claude.com/en/articles/14604842))           | `claude-mythos-5-1`          |
| Claude Fable 5                                                                                        | `claude-fable-5`             |
| Claude Mythos 5 ([limited availability](https://support.claude.com/en/articles/14604842))             | `claude-mythos-5`            |
| Claude Opus 5.5                                                                                       | `claude-opus-5-5`            |
| Claude Opus 5                                                                                         | `claude-opus-5`              |
| Claude Opus 4.8                                                                                       | `claude-opus-4-8`            |
| Claude Opus 4.7                                                                                       | `claude-opus-4-7`            |
| Claude Opus 4.6                                                                                       | `claude-opus-4-6`            |
| Claude Opus 4.5                                                                                       | `claude-opus-4-5@20251101`   |
| Claude Opus 4.1 ([deprecated](https://platform.claude.com/docs/id/about-claude/model-deprecations))   | `claude-opus-4-1@20250805`   |
| Claude Opus 4 ([deprecated](https://platform.claude.com/docs/id/about-claude/model-deprecations))     | `claude-opus-4@20250514`     |
| Claude Sonnet 5.5                                                                                     | `claude-sonnet-5-5`          |
| Claude Sonnet 5                                                                                       | `claude-sonnet-5`            |
| Claude Sonnet 4.6                                                                                     | `claude-sonnet-4-6`          |
| Claude Sonnet 4.5 ([deprecated](https://platform.claude.com/docs/id/about-claude/model-deprecations)) | `claude-sonnet-4-5@20250929` |
| Claude Sonnet 4 ([deprecated](https://platform.claude.com/docs/id/about-claude/model-deprecations))   | `claude-sonnet-4@20250514`   |
| Claude Haiku 5.5                                                                                      | `claude-haiku-5-5`           |
| Claude Haiku 4.5                                                                                      | `claude-haiku-4-5@20251001`  |
| Claude Haiku 3.5 ([deprecated](https://platform.claude.com/docs/id/about-claude/model-deprecations))  | `claude-3-5-haiku@20241022`  |

Claude Models on Google Cloud (Google managed) menawarkan model Claude yang berbeda di region yang berbeda. Untuk memeriksa model mana yang ditawarkan suatu region, cari "Claude" di [Model Garden](https://cloud.google.com/model-garden) atau lihat halaman [Anthropic Claude models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) dari Google Cloud.

Google menetapkan tanggal siklus hidup untuk model-model yang dilayani oleh Claude Models on Google Cloud (Google managed). Tanggal-tanggal ini dapat berbeda dari jadwal Claude API. Untuk tanggal penghentian terkini suatu model, lihat halaman [Anthropic Claude models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) dari Google Cloud. Untuk arti Deprecated dan Retired, lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

<Note>
  Claude Mythos Preview adalah pratinjau riset. Claude Models on Google Cloud (Google managed) menawarkannya kepada pelanggan yang diundang. Untuk informasi lebih lanjut, lihat [Project Glasswing](https://anthropic.com/glasswing).
</Note>

<Tip>
  Meng-upgrade ke model Claude yang lebih baru? [Skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) di Claude Code menerapkan penggantian ID model dan perubahan parameter yang bersifat breaking di seluruh basis kode Anda:

  Biarkan Claude Code memigrasikan kode Anda

  ```text
  /claude-api migrate proyek ini ke model Claude Opus terbaru
  ```

  Skill ini mendeteksi platform cloud mana yang ditargetkan oleh kode Anda dan menyesuaikan format ID model serta perubahan fitur untuk platform tersebut.
</Tip>

## Endpoint global, multi-region, dan regional

Claude Models on Google Cloud (Google managed) menawarkan tiga jenis endpoint. Anda memilih salah satunya melalui nilai region yang Anda teruskan saat membuat klien. Dalam permintaan cURL, jenis endpoint menentukan host dan segmen `locations` dari URL.

| Jenis endpoint                | Nilai region                        | Host                                                                       |
| ----------------------------- | ----------------------------------- | -------------------------------------------------------------------------- |
| **Global** (direkomendasikan) | `"global"`                          | `aiplatform.googleapis.com`                                                |
| **Multi-region**              | `"us"` atau `"eu"`                  | `aiplatform.us.rep.googleapis.com`<br />`aiplatform.eu.rep.googleapis.com` |
| **Regional**                  | Sebuah region, seperti `"us-east5"` | `{region}-aiplatform.googleapis.com`                                       |

Jenis-jenis endpoint berbeda dalam hal ke mana permintaan dikirim:

* **Global:** Permintaan dikirim ke region mana pun yang memiliki kapasitas tersedia. Gunakan ini ketika Anda menginginkan ketersediaan maksimum dan residensi data bersifat fleksibel.
* **Multi-region:** Permintaan dikirim ke region mana pun di Amerika Serikat (`"us"`) atau Uni Eropa (`"eu"`). Gunakan ini ketika Anda memerlukan residensi data dalam wilayah geografis yang luas dan ketersediaan yang lebih tinggi daripada satu region.
* **Regional:** Permintaan hanya dikirim ke region yang Anda sebutkan, seperti `"us-east5"` atau `"europe-west1"`. Gunakan ini ketika Anda memerlukan residensi data dalam satu region atau harus memenuhi mandat kepatuhan yang ketat.

Endpoint multi-region dan regional berbiaya 10% lebih mahal daripada endpoint global. Ketiga jenis endpoint menerima lalu lintas pay-as-you-go, dan provisioned throughput memerlukan endpoint regional.

Endpoint regional hanya melayani Claude Sonnet 4.6 dan model-model sebelumnya. Untuk model yang lebih baru, gunakan endpoint global atau multi-region.

<Note>
  Biaya tambahan untuk endpoint multi-region dan regional hanya berlaku untuk Claude Sonnet 4.5 (deprecated) dan model-model setelahnya. Untuk model-model yang mempertahankan harga sebelumnya, lihat [Harga platform cloud](https://platform.claude.com/docs/id/about-claude/pricing#cloud-platform-pricing). Untuk endpoint regional, biaya tambahan tersebut mencerminkan biaya infrastruktur untuk kapasitas regional khusus.
</Note>

Contoh-contoh berikut menggunakan endpoint multi-region `us`. Baris yang disorot mengatur region. Untuk permintaan lengkap pada endpoint global, lihat [Membuat permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#accessing-vertex-ai).

<CodeGroup exclude="shell:CLI">
  ```bash cURL
  # Pengenal multi-region, "us" atau "eu", muncul di nama host dan di path
  curl https://aiplatform.us.rep.googleapis.com/v1/projects/MY_PROJECT_ID/locations/us/publishers/anthropic/models/claude-opus-5-5:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
      "max_tokens": 100
    }'
  ```

  <CodeGroupItem language="CLI">
    CLI `ant` tidak mendukung Claude Models on Google Cloud (Google managed).
  </CodeGroupItem>

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "us"  # Multi-region identifier: "us" or "eu"

  client = AnthropicVertex(project_id=project_id, region=region)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "us"; // Multi-region identifier: "us" or "eu"

  const client = new AnthropicVertex({
    projectId,
    region
  });
  ```

  ```csharp C#
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "us"; // Multi-region identifier: "us" or "eu"

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));
  ```

  ```go Go
  import (
  	"context"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Pengenal multi-region: "us" atau "eu"
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "us", "MY_PROJECT_ID"),
  	)
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.vertex.backends.VertexBackend;
  import com.google.auth.oauth2.GoogleCredentials;

  void main() throws Exception {
      // Pengenal multi-region: "us" atau "eu"
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .googleCredentials(GoogleCredentials.getApplicationDefault())
                  .region("us")
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();
  }
  ```

  ```php PHP
  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      region: 'us', // Multi-region identifier: "us" or "eu"
      projectId: 'MY_PROJECT_ID',
  );
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "us", # Multi-region identifier: "us" or "eu"
    project_id: "MY_PROJECT_ID"
  )
  ```
</CodeGroup>

## Dukungan fitur

Fitur-fitur yang didukung di Claude Models on Google Cloud (Google managed) meliputi yang berikut:

* [Messages API](https://platform.claude.com/docs/id/api/messages/create)

* ["Prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)

* [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)

* ["Tool use" (penggunaan alat)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview), termasuk alat-alat berikut:

  * [Alat bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool)
  * [Alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool)
  * [Alat computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool)
  * [Alat memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool)
  * [Alat editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool)
  * [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool)

* [Citations](https://platform.claude.com/docs/id/build-with-claude/citations)

* [Structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs)

[Ikhtisar fitur](https://platform.claude.com/docs/id/build-with-claude/overview) mencantumkan setiap fitur dan apakah Claude Models on Google Cloud (Google managed) mendukungnya.

### Fitur yang tidak didukung

Claude Models on Google Cloud (Google managed) tidak mendukung hal-hal berikut:

* **Sumber input:** Sumber URL untuk gambar dan dokumen, serta Files API
* **Alat sisi server:** Code execution, web fetch, dan advisor
* **Infrastruktur agen:** Agent Skills, konektor MCP, dan programmatic tool calling
* **Endpoint API:** Message Batches API, Models API, Admin API, Compliance API, serta Usage and Cost API
* **Claude Managed Agents**
* **Fallback sisi server:** [Parameter `fallbacks`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback)

Sebagai pengganti fallback sisi server, gunakan [pola fallback sisi klien](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback).

### Jendela konteks

Claude Models on Google Cloud (Google managed) menawarkan ["context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) untuk model-model berikut:

* Claude Fable 5.1
* Claude Fable 5
* Claude Opus 5.5
* Claude Opus 5
* Claude Opus 4.8
* Claude Opus 4.7
* Claude Opus 4.6
* Claude Sonnet 5.5
* Claude Sonnet 5
* Claude Sonnet 4.6
* Claude Haiku 5.5

Model Claude lainnya memiliki jendela konteks 200k token. Ini termasuk Claude Sonnet 4.5 (deprecated) dan Claude Sonnet 4 (deprecated).

Agent Platform membatasi payload permintaan hingga 30 MB. Saat Anda mengirim dokumen besar atau banyak gambar, Anda mungkin mencapai batas ini sebelum batas token.

## Penagihan, batas laju, dan logging

### Batas laju

Google Cloud mengelola "rate limit" (batas laju) dan kuota untuk Claude Models on Google Cloud (Google managed). Untuk detailnya, termasuk cara meminta peningkatan kuota, lihat halaman [Quotas for Anthropic Claude models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/quotas) dari Google Cloud.

### Penagihan

Google Cloud menagih Anda untuk Claude Models on Google Cloud (Google managed). Untuk harga, lihat halaman [Generative AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing#claude-models) dari Google Cloud. Harga juga bergantung pada jenis endpoint. Lihat [Endpoint global, multi-region, dan regional](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#global-multi-region-and-regional-endpoints).

### Retensi data

Google Cloud mengatur penanganan data untuk Claude Models on Google Cloud (Google managed). Untuk detailnya, lihat [Agent Platform and zero data retention](https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance).

### Pemantauan dan logging

Untuk mencatat log prompt dan completion untuk Claude Models on Google Cloud (Google managed), gunakan [layanan logging permintaan-respons](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging) dari Agent Platform.

Anthropic merekomendasikan agar Anda menyimpan setidaknya log 30 hari terakhir. Log tersebut membantu Anda memahami aktivitas Anda dan menyelidiki kemungkinan penyalahgunaan.

<Note>
  Mengaktifkan layanan ini tidak memberikan Google atau Anthropic akses apa pun ke konten Anda.
</Note>

## Migrasi dari Claude Models on Google Cloud (Anthropic managed)

Untuk mengetahui apa yang berubah saat Anda berpindah, lihat [Perbedaan kedua penawaran Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/overview#how-the-two-google-cloud-offerings-differ). Untuk berpindah ke Claude Models on Google Cloud (Google managed), ikuti langkah-langkah berikut:

<Steps>
  <Step title="Siapkan akses">
    Periksa bahwa proyek Anda dan identitas yang melakukan panggilan memenuhi persyaratan di [Sebelum melakukan panggilan API](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#before-making-api-calls).
  </Step>

  <Step title="Instal paket SDK">
    Instal paket yang menyediakan klien untuk Claude Models on Google Cloud (Google managed). Lihat [Menginstal SDK](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#install-an-sdk-for-accessing-vertex-ai).
  </Step>

  <Step title="Ganti import dan klien">
    Ubah kode yang mengimpor dan membuat klien Anda. Gunakan `AnthropicVertex` (csharp: `AnthropicVertexClient`; go: `vertex.WithGoogleAuth`; java: `VertexBackend`; php: `Anthropic\Vertex\Client`; ruby: `Anthropic::VertexClient`) sebagai pengganti `AnthropicGoogleCloud` (csharp: `AnthropicGoogleCloudClient`; go: `googlecloud.NewClient`; java: `GoogleCloudBackend`; php: `Anthropic\GoogleCloud\Client`; ruby: `Anthropic::GoogleCloudClient`). Permintaan cURL memerlukan URL baru, header baru, dan body baru. Kode berikut membuat klien untuk Claude Models on Google Cloud (Anthropic managed) yang Anda gunakan saat ini:

    <CodeGroup>
      ```bash cURL
      curl "https://claude.googleapis.com/v1/projects/$ANTHROPIC_GOOGLE_CLOUD_PROJECT/locations/global/workspaces/$ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID/invoke/v1/messages" \
        -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
        -H "content-type: application/json" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
          "model": "claude-opus-5-5",
          "max_tokens": 1024,
          "messages": [
            {"role": "user", "content": "Hello, Claude"}
          ]
        }'
      ```

      ```bash CLI
      ant messages create \
        --model claude-opus-5-5 \
        --max-tokens 1024 \
        --message '{role: user, content: "Hello, Claude"}'
      ```

      ```python Python
      from anthropic import AnthropicGoogleCloud

      client = AnthropicGoogleCloud()
      ```

      ```typescript TypeScript
      import { AnthropicGoogleCloud } from "@anthropic-ai/google-cloud-sdk";

      const client = new AnthropicGoogleCloud();
      ```

      ```csharp C#
      using Anthropic.GoogleCloud;

      var client = new AnthropicGoogleCloudClient();
      ```

      ```go Go
      import (
      	"context"

      	"github.com/anthropics/anthropic-sdk-go"
      	"github.com/anthropics/anthropic-sdk-go/googlecloud"
      )
      // ...
      	client, err := googlecloud.NewClient(context.Background(), googlecloud.ClientConfig{})
      	if err != nil {
      		panic(err)
      	}
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.googlecloud.backends.GoogleCloudBackend;

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.builder()
              .backend(GoogleCloudBackend.fromEnv())
              .build();
      }
      ```

      ```php PHP
      use Anthropic\GoogleCloud\Client;

      $client = new Client();
      ```

      ```ruby Ruby
      require "anthropic"

      client = Anthropic::GoogleCloudClient.new
      ```
    </CodeGroup>

    Kode berikut membuat klien untuk Claude Models on Google Cloud (Google managed). Kode ini menggunakan endpoint global. Untuk jenis endpoint lainnya, lihat [Endpoint global, multi-region, dan regional](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#global-multi-region-and-regional-endpoints).

    <CodeGroup exclude="shell:CLI">
      ```bash cURL
      curl https://aiplatform.googleapis.com/v1/projects/MY_PROJECT_ID/locations/global/publishers/anthropic/models/claude-opus-5-5:rawPredict \
        -H "Authorization: Bearer $(gcloud auth print-access-token)" \
        -H "Content-Type: application/json" \
        -d '{
          "anthropic_version": "vertex-2023-10-16",
          "messages": [{"role": "user", "content": "Hey Claude!"}],
          "max_tokens": 100
        }'
      ```

      <CodeGroupItem language="CLI">
        CLI `ant` tidak mendukung Claude Models on Google Cloud (Google managed). Gunakan cURL atau SDK sebagai gantinya.
      </CodeGroupItem>

      ```python Python
      from anthropic import AnthropicVertex

      project_id = "MY_PROJECT_ID"
      region = "global"

      client = AnthropicVertex(project_id=project_id, region=region)
      ```

      ```typescript TypeScript
      import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

      const projectId = "MY_PROJECT_ID";
      const region = "global";

      const client = new AnthropicVertex({
        projectId,
        region
      });
      ```

      ```csharp C#
      using Anthropic.Vertex;

      var projectId = "MY_PROJECT_ID";
      var region = "global";

      var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));
      ```

      ```go Go
      import (
      	"context"

      	"github.com/anthropics/anthropic-sdk-go"
      	"github.com/anthropics/anthropic-sdk-go/vertex"
      )
      // ...
      	// Menggunakan kredensial default Google Cloud
      	client := anthropic.NewClient(
      		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
      	)
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.vertex.backends.VertexBackend;
      import com.google.auth.oauth2.GoogleCredentials;

      void main() throws Exception {
          AnthropicClient client = AnthropicOkHttpClient.builder()
              .backend(
                  VertexBackend.builder()
                      .googleCredentials(GoogleCredentials.getApplicationDefault())
                      .region("global")
                      .project("MY_PROJECT_ID")
                      .build()
              )
              .build();
      }
      ```

      ```php PHP
      use Anthropic\Vertex;

      $client = Vertex\Client::fromEnvironment(
          region: 'global',
          projectId: 'MY_PROJECT_ID',
      );
      ```

      ```ruby Ruby
      require "anthropic"

      client = Anthropic::VertexClient.new(
        region: "global",
        project_id: "MY_PROJECT_ID"
      )
      ```
    </CodeGroup>

    Kode ini meneruskan ID proyek Anda dan sebuah region saat membuat klien. Ganti `MY_PROJECT_ID` dengan ID proyek Anda. Panggilan Messages API yang Anda lakukan dengan klien tetap seperti semula. Pengecualiannya adalah ID model dan fitur pada langkah berikutnya.
  </Step>

  <Step title="Periksa ID model dan fitur">
    * **ID model:** Jika Anda menggunakan model yang lebih lama dari Claude 4.6, ganti tanda hubung sebelum tanggal snapshot dalam ID-nya dengan `@`. Misalnya, `claude-haiku-4-5-20251001` menjadi `claude-haiku-4-5@20251001`. Untuk model-model dan ID-nya, lihat [ID model API](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#api-model-ids).
    * **Fitur:** Periksa bahwa fitur yang digunakan kode Anda tidak tercantum di [Fitur yang tidak didukung](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#features-not-supported).
  </Step>

  <Step title="Jalankan permintaan uji">
    Jalankan permintaan di [Membuat permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#accessing-vertex-ai) untuk memeriksa bahwa penyiapan Anda berfungsi. Kemudian jalankan kode Anda sendiri. Sebelum Anda memindahkan lalu lintas produksi, baca tentang [batas laju untuk Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#rate-limits).
  </Step>
</Steps>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ikhtisar fitur" icon="stack" href="https://platform.claude.com/docs/id/build-with-claude/overview">
    Jelajahi fitur-fitur Claude.
  </Card>

  <Card title="Model Anthropic Claude di Agent Platform" icon="book" href="https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude">
    Periksa model Claude mana yang ditawarkan setiap region, beserta tanggal penghentiannya.
  </Card>

  <Card title="Dokumentasi Agent Platform" icon="book" href="https://cloud.google.com/vertex-ai/docs">
    Baca dokumentasi Google Cloud's Agent Platform.
  </Card>

  <Card title="Endpoint global untuk model Claude" icon="link" href="https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai">
    Baca postingan blog Google Cloud tentang endpoint global untuk model Claude.
  </Card>
</CardGroup>
