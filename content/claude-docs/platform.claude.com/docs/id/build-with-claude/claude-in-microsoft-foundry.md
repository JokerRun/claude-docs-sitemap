---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 5d9b661db93920680ce9b1ba2af7db0d9d45db0151af134aefe61343aef6ee14
---

# Claude di Microsoft Foundry

Akses model Claude melalui Microsoft Foundry dengan endpoint dan autentikasi native Azure.

---

Panduan ini menunjukkan cara menyiapkan dan melakukan panggilan API ke Claude di Microsoft Foundry menggunakan salah satu SDK klien Anthropic atau permintaan HTTP langsung. Saat Anda mengakses Claude di Microsoft Foundry, Anda ditagih untuk penggunaan Claude di Azure Marketplace. Anda dapat menggunakan model Claude terbaru, termasuk Claude Opus 4.8 dan Claude Sonnet 5, serta fitur seperti [jendela konteks 1M token](/docs/id/build-with-claude/context-windows), sambil mengelola biaya melalui langganan Azure Anda.

Claude tersedia dalam tipe deployment Global Standard dan US Data Zone Standard di resource Foundry, ditagih dalam Claude Consumption Units melalui Azure Marketplace. Kunjungi [harga Claude di Microsoft Foundry](/docs/id/about-claude/pricing#claude-in-microsoft-foundry-pricing) untuk detailnya.

## Opsi hosting

Model Claude di Microsoft Foundry tersedia dalam dua opsi hosting. Anda memilih opsi hosting saat mengonfigurasi deployment.

|                           | Dihosting di Azure                                                       | Dihosting di Anthropic                                                                                             |
| ------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| Tempat inferensi berjalan | Layanan yang dioperasikan Anthropic yang berjalan di infrastruktur Azure | Layanan yang dioperasikan Anthropic yang berjalan di infrastruktur Anthropic                                       |
| Ketersediaan model        | Model terbaru dalam keluarga Opus, Sonnet, dan Haiku                     | Semua model Claude yang tersedia di Microsoft Foundry                                                              |
| Tipe deployment           | Global Standard, US Data Zone Standard                                   | Global Standard                                                                                                    |
| Direkomendasikan untuk    | Sebagian besar beban kerja                                               | [Akses ke fitur atau model yang belum dihosting di Azure](#additional-features-not-supported-when-hosted-on-azure) |

<Note>
  Anthropic bertindak sebagai pemroses independen untuk Microsoft. Pelanggan yang menggunakan Claude melalui Microsoft Foundry tunduk pada ketentuan penggunaan data Anthropic. Untuk deployment yang dihosting di Azure, prompt dan completion tetap berada di dalam Azure. Hanya metadata penggunaan dan konten yang ditandai oleh sistem keamanan Anthropic yang keluar ke Anthropic. Anthropic terus memberikan komitmen keamanan dan datanya.
</Note>

## Prasyarat

Sebelum memulai, pastikan Anda memiliki:

* Langganan Azure yang aktif
* Akses ke [portal Foundry](https://ai.azure.com/)
* [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) terinstal (diperlukan untuk contoh cURL Entra ID, opsional untuk lainnya)
* Peran Azure RBAC yang memungkinkan Anda menggunakan resource, seperti **Foundry User** (sebelumnya Azure AI User) atau **Cognitive Services User**

## Instal SDK

[SDK klien](/docs/id/cli-sdks-libraries/overview) Anthropic mendukung Foundry melalui paket atau kelas klien khusus platform. Contoh di halaman ini juga menunjukkan permintaan dengan cURL dan CLI ant. Untuk menyiapkan CLI, lihat [Mulai cepat CLI](/docs/id/cli-sdks-libraries/cli/quickstart).

<Note>
  Foundry didukung oleh SDK C#, Java, PHP, Python, dan TypeScript. Foundry saat ini belum tersedia di SDK Go dan Ruby.
</Note>

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U "anthropic"

    # Untuk autentikasi Entra ID, instal juga pustaka Azure Identity
    pip install azure-identity
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/foundry-sdk

    # Untuk autentikasi Entra ID, instal juga pustaka Azure Identity
    npm install @azure/identity
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic.Foundry
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    # SDK Go belum mendukung Foundry secara native (lihat contoh Autentikasi
    # untuk menggunakan SDK Go standar sebagai solusi alternatif)
    go get github.com/anthropics/anthropic-sdk-go
    ```
  </Tab>

  <Tab title="Java">
    <Tabs>
      <Tab title="Gradle">
        ```kotlin
        implementation("com.anthropic:anthropic-java-foundry:2.50.0")

        // Untuk autentikasi Entra ID, tambahkan juga pustaka Azure Identity
        implementation("com.azure:azure-identity:1.18.3")
        ```
      </Tab>

      <Tab title="Maven">
        ```xml
        <dependency>
            <groupId>com.anthropic</groupId>
            <artifactId>anthropic-java-foundry</artifactId>
            <version>2.50.0</version>
        </dependency>
        <!-- For Entra ID authentication, also add the Azure Identity library -->
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-identity</artifactId>
            <version>1.18.3</version>
        </dependency>
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require anthropic-ai/sdk
    ```
  </Tab>

  <Tab title="Ruby">
    ```bash
    # SDK Ruby belum mendukung Foundry secara native (lihat contoh Autentikasi
    # untuk menggunakan SDK Ruby standar sebagai solusi alternatif)
    # Gemfile
    gem "anthropic"
    ```
  </Tab>
</Tabs>

## Provisioning

Foundry menggunakan hierarki dua tingkat: **resource** berisi konfigurasi keamanan dan penagihan Anda, sedangkan **deployment** adalah instans model yang Anda panggil melalui API. Anda akan terlebih dahulu membuat resource Foundry, lalu membuat satu atau lebih deployment Claude di dalamnya.

### Provisioning resource Foundry

Buat resource Foundry, yang diperlukan untuk menggunakan dan mengelola layanan di Azure. Anda dapat mengikuti instruksi ini untuk membuat [resource Foundry](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal#create-a-new-azure-ai-foundry-resource). Sebagai alternatif, Anda dapat memulai dengan membuat [proyek Foundry](https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects), yang melibatkan pembuatan resource Foundry.

Untuk melakukan provisioning resource Anda:

1. Buka [portal Foundry](https://ai.azure.com/).
2. Buat resource Foundry baru atau pilih yang sudah ada.
3. Konfigurasikan manajemen akses menggunakan kunci API yang diterbitkan Azure atau Entra ID (sebelumnya Azure Active Directory) untuk kontrol akses berbasis peran.
4. Secara opsional, konfigurasikan resource agar menjadi bagian dari jaringan privat (Azure Virtual Network) untuk membatasi akses jaringan ke resource Anda.
5. Catat nama resource Anda. Anda akan menggunakannya sebagai `{resource}` di endpoint API (misalnya, `https://{resource}.services.ai.azure.com/anthropic/v1/*`).

### Membuat deployment Foundry

Setelah membuat resource Anda, deploy model Claude agar tersedia untuk panggilan API. Langkah-langkah ini menjelaskan portal Foundry baru (toggle **New Foundry** aktif):

1. Masuk ke portal Foundry. Dari halaman beranda portal, pilih **Discover** di navigasi kanan atas, lalu **Models** di panel kiri untuk membuka katalog model.

2. Cari dan pilih model Claude (misalnya, claude-opus-4-8). Setiap model muncul satu kali di katalog terlepas dari berapa banyak opsi hosting yang didukungnya.

3. Pada kartu model, pilih **Deploy**, lalu **Custom settings** untuk membuka panel pengaturan deployment. Jika Anda memilih **Default settings**, deployment secara otomatis dikonfigurasi sebagai Dihosting di Azure untuk model yang tersedia di kedua opsi hosting.

4. Pada deployment Claude pertama Anda, tinjau ketentuan Azure Marketplace, pilih industri, dan pilih **Agree and Proceed** untuk menerima ketentuan dan berlangganan penawaran Azure Marketplace.

5. Konfigurasikan deployment:

   * **Nama deployment:** Secara default menggunakan ID model, tetapi Anda dapat menyesuaikannya (misalnya, `my-claude-deployment`). Nama deployment tidak dapat diubah setelah dibuat.
   * **Cakupan region:** Pilih Global, atau untuk model yang dihosting di Azure, Data Zone. Memilih Data Zone membuat deployment US Data Zone Standard, yang menjaga inferensi tetap di Amerika Serikat dan setara dengan mengatur [`inference_geo: "us"`](/docs/id/manage-claude/data-residency#inference-geo) di Claude API.
   * **Versi model:** Perluas **Model version settings** dan pilih versi dari menu dropdown **Model version**. Setiap [opsi hosting](#hosting-options) terdaftar sebagai versi model terpisah, diberi label dengan opsi hostingnya (misalnya, versi 1 untuk Dihosting di Anthropic, versi 2 untuk Dihosting di Azure).

6. Pilih **Deploy** dan tunggu hingga provisioning selesai.

7. Setelah di-deploy, pilih **Build** di navigasi kanan atas, lalu **Models** di panel kiri, dan buka deployment Anda. Tab **Details** menampilkan **Target URI** (URL endpoint Anda) dan **Key** (kunci API Anda).

Jika toggle **New Foundry** nonaktif, Anda berada di tata letak portal klasik. Di sana, buka **Model catalog** di panel kiri untuk menemukan dan men-deploy model, dan buka **Models + endpoints** (di bawah **My assets**) untuk melihat deployment Anda dan detail endpoint-nya.

<Note>
  Nama deployment yang Anda pilih menjadi nilai yang Anda berikan di parameter `model` pada permintaan API Anda. Anda dapat membuat beberapa deployment dari model yang sama dengan nama berbeda untuk mengelola konfigurasi atau batas laju yang terpisah.
</Note>

## Autentikasi

Claude di Microsoft Foundry mendukung dua metode autentikasi: kunci API dan token Entra ID. Kedua metode menggunakan endpoint yang dihosting Azure dalam format `https://{resource}.services.ai.azure.com/anthropic/v1/*`.

### Autentikasi kunci API

Setelah melakukan provisioning resource Claude Foundry Anda, Anda dapat memperoleh kunci API dari portal Foundry:

1. Di portal Foundry, pilih **Build** di navigasi kanan atas, lalu **Models** di panel kiri.
2. Buka deployment Claude Anda dan pilih tab **Details**.
3. Salin nilai **Key** (dan catat **Target URI** untuk endpoint Anda).
4. Gunakan header `api-key` atau `x-api-key` dalam permintaan Anda, atau berikan ke SDK.

SDK Foundry memerlukan kunci API dan nama resource atau base URL. SDK C#, Java, PHP, Python, dan TypeScript secara otomatis membaca ini dari variabel lingkungan berikut jika didefinisikan:

* `ANTHROPIC_FOUNDRY_API_KEY` - Kunci API Anda
* `ANTHROPIC_FOUNDRY_RESOURCE` - Nama resource Anda (misalnya, `example-resource`)
* `ANTHROPIC_FOUNDRY_BASE_URL` - Alternatif untuk nama resource: base URL lengkap (misalnya, `https://example-resource.services.ai.azure.com/anthropic/`). SDK C# tidak membaca variabel ini: SDK tersebut selalu membangun base URL dari nama resource.

<Note>
  Parameter `resource` dan `base_url` bersifat saling eksklusif. Berikan nama resource (yang digunakan SDK untuk membangun URL sebagai `https://{resource}.services.ai.azure.com/anthropic/`) atau base URL lengkap secara langsung.
</Note>

**Contoh menggunakan kunci API:**

<CodeGroup>
  ```bash cURL
  curl https://{resource}.services.ai.azure.com/anthropic/v1/messages \
    -H "content-type: application/json" \
    -H "api-key: YOUR_AZURE_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }'
  ```

  ```bash CLI
  # ant membaca ANTHROPIC_API_KEY dan mengirimkannya sebagai x-api-key, yang diterima oleh Foundry
  export ANTHROPIC_API_KEY="YOUR_AZURE_API_KEY"

  ant messages create \
    --base-url https://example-resource.services.ai.azure.com/anthropic \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello!"}' \
    --transform content
  ```

  ```python Python
  import os
  from anthropic import AnthropicFoundry

  client = AnthropicFoundry(
      api_key=os.environ.get("ANTHROPIC_FOUNDRY_API_KEY"),
      resource="example-resource",  # your resource name
  )

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )
  print(message.content)
  ```

  ```typescript TypeScript
  import AnthropicFoundry from "@anthropic-ai/foundry-sdk";

  const client = new AnthropicFoundry({
    apiKey: process.env.ANTHROPIC_FOUNDRY_API_KEY,
    resource: "example-resource" // your resource name
  });

  const message = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(message.content);
  ```

  ```csharp C#
  using Anthropic.Foundry;
  using Anthropic.Models.Messages;

  var client = new AnthropicFoundryClient(
      new AnthropicFoundryApiKeyCredentials(
          Environment.GetEnvironmentVariable("ANTHROPIC_FOUNDRY_API_KEY")!,
          "example-resource"
      )
  );

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = "claude-opus-4-8",
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }],
  });

  Console.WriteLine(
      string.Join("", response.Content
          .Select(block => block.Value)
          .OfType<TextBlock>()
          .Select(textBlock => textBlock.Text)));
  ```

  ```go Go
  // SDK Go belum mendukung Foundry secara native. Contoh ini menggunakan
  // SDK Go standar sebagai solusi sementara. WithoutEnvironmentDefaults
  // mencegah klien ikut membaca ANTHROPIC_API_KEY atau ANTHROPIC_AUTH_TOKEN
  // dari environment dan mengirimkan kredensial API Claude ke endpoint
  // Foundry Anda. Fitur yang tidak didukung Foundry akan gagal di sisi
  // server, bukan di sisi klien. Untuk dukungan Foundry penuh, gunakan
  // SDK C#, Java, PHP, Python, atau TypeScript.
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  func main() {
  	client := anthropic.NewClient(
  		option.WithoutEnvironmentDefaults(),
  		option.WithBaseURL("https://example-resource.services.ai.azure.com/anthropic"),
  		option.WithAPIKey(os.Getenv("ANTHROPIC_FOUNDRY_API_KEY")),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message.Content)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.foundry.backends.FoundryBackend;
  import com.anthropic.models.messages.MessageCreateParams;

  void main() {
      // Memerlukan variabel lingkungan: ANTHROPIC_FOUNDRY_API_KEY, ANTHROPIC_FOUNDRY_RESOURCE
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(FoundryBackend.fromEnv())
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model("claude-opus-4-8")
          .maxTokens(1024)
          .addUserMessage("Hello!")
          .build();

      client.messages().create(params).content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> System.out.println(textBlock.text()));
  }
  ```

  ```php PHP
  use Anthropic\Foundry;

  $client = Foundry\Client::withCredentials(
      apiKey: getenv('ANTHROPIC_FOUNDRY_API_KEY'),
      baseUrl: 'https://example-resource.services.ai.azure.com/anthropic',
  );

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Hello!']
      ],
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  # SDK Ruby belum mendukung Foundry secara native. Contoh ini menggunakan
  # SDK Ruby standar sebagai solusi sementara. Berikan kredensial secara eksplisit:
  # tanpa itu, klien akan kembali menggunakan variabel lingkungan ANTHROPIC_API_KEY
  # atau ANTHROPIC_AUTH_TOKEN dan dapat mengirimkan kredensial API Claude
  # ke endpoint Foundry Anda. Fitur yang tidak didukung Foundry
  # akan gagal di sisi server, bukan di sisi klien. Untuk dukungan
  # Foundry penuh, gunakan SDK C#, Java, PHP, Python, atau TypeScript.
  require "anthropic"

  client = Anthropic::Client.new(
    base_url: "https://example-resource.services.ai.azure.com/anthropic",
    api_key: ENV.fetch("ANTHROPIC_FOUNDRY_API_KEY")
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

<Warning>
  Jaga keamanan kunci API Anda. Jangan pernah melakukan commit ke version control atau membagikannya secara publik. Siapa pun yang memiliki akses ke kunci API Anda dapat membuat permintaan ke Claude melalui resource Foundry Anda.
</Warning>

### Autentikasi Microsoft Entra

Autentikasi Entra ID memungkinkan Anda mengelola akses dengan Azure RBAC, berintegrasi dengan manajemen identitas organisasi Anda, dan menghindari penanganan kunci API secara manual. Untuk menggunakan token Entra ID:

1. Aktifkan [autentikasi Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/how-to/configure-entra-id) untuk resource Foundry Anda.
2. Dapatkan token akses dari Entra ID.
3. Gunakan token di header `Authorization: Bearer {TOKEN}`.

**Contoh menggunakan Entra ID:**

<CodeGroup>
  ```bash cURL
  # Dapatkan token Microsoft Entra ID
  ACCESS_TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)

  # Buat permintaan dengan token. Ganti {resource} dengan nama resource Anda
  curl https://{resource}.services.ai.azure.com/anthropic/v1/messages \
    -H "content-type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }'
  ```

  ```bash CLI
  # CLI ant dapat mengirim bearer token dengan --auth-token, tetapi variabel
  # lingkungan ANTHROPIC_API_KEY yang sudah disetel lebih diprioritaskan (CLI
  # hanya mencetak pemberitahuan di konsol), sehingga permintaan Anda bisa
  # terautentikasi dengan kredensial yang salah. Untuk alur Entra ID, gunakan
  # contoh cURL atau salah satu contoh SDK sebagai gantinya.
  ```

  ```python Python
  from anthropic import AnthropicFoundry
  from azure.identity import DefaultAzureCredential, get_bearer_token_provider

  # Dapatkan token Microsoft Entra ID menggunakan pola token provider
  token_provider = get_bearer_token_provider(
      DefaultAzureCredential(), "https://ai.azure.com/.default"
  )

  # Buat klien dengan autentikasi Entra ID
  client = AnthropicFoundry(
      resource="example-resource",  # your resource name
      azure_ad_token_provider=token_provider,  # Use token provider for Entra ID auth
  )

  # Buat permintaan
  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )
  print(message.content)
  ```

  ```typescript TypeScript
  import AnthropicFoundry from "@anthropic-ai/foundry-sdk";
  import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

  // Dapatkan token Entra ID menggunakan pola token provider
  const credential = new DefaultAzureCredential();
  const tokenProvider = getBearerTokenProvider(credential, "https://ai.azure.com/.default");

  // Buat klien dengan autentikasi Entra ID
  const client = new AnthropicFoundry({
    resource: "example-resource", // your resource name
    azureADTokenProvider: tokenProvider // Use token provider for Entra ID auth
  });

  // Buat permintaan
  const message = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(message.content);
  ```

  ```csharp C#
  using Anthropic.Foundry;
  using Anthropic.Models.Messages;
  using Azure.Identity;

  var client = new AnthropicFoundryClient(
      new AnthropicFoundryIdentityTokenCredentials(
          new DefaultAzureCredential(),
          "example-resource"
      )
  );

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = "claude-opus-4-8",
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }],
  });

  Console.WriteLine(
      string.Join("", response.Content
          .Select(block => block.Value)
          .OfType<TextBlock>()
          .Select(textBlock => textBlock.Text)));
  ```

  ```go Go
  // SDK Go belum mendukung Foundry secara native. Contoh ini menggunakan
  // SDK Go standar sebagai solusi sementara, dengan token Entra ID statis:
  // pembaruan token otomatis tidak tersedia bawaan, sehingga aplikasi Anda
  // harus memperbarui token sendiri (biasanya kedaluwarsa setelah 1 jam).
  // WithoutEnvironmentDefaults mencegah klien juga membaca ANTHROPIC_API_KEY
  // atau ANTHROPIC_AUTH_TOKEN dari environment dan mengirimkan kredensial
  // Claude API ke endpoint Foundry Anda. Untuk dukungan Foundry penuh,
  // gunakan SDK C#, Java, PHP, Python, atau TypeScript.
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  func main() {
  	// Dapatkan token akses Entra ID, misalnya menggunakan Azure CLI:
  	//   az account get-access-token --resource https://ai.azure.com \
  	//     --query accessToken -o tsv
  	client := anthropic.NewClient(
  		option.WithoutEnvironmentDefaults(),
  		option.WithBaseURL("https://example-resource.services.ai.azure.com/anthropic"),
  		option.WithAuthToken(os.Getenv("AZURE_ACCESS_TOKEN")),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message.Content)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.foundry.backends.FoundryBackend;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.azure.identity.AuthenticationUtil;
  import com.azure.identity.DefaultAzureCredentialBuilder;
  import java.util.function.Supplier;

  void main() {
      Supplier<String> bearerTokenSupplier = AuthenticationUtil.getBearerTokenSupplier(
          new DefaultAzureCredentialBuilder().build(),
          "https://ai.azure.com/.default"
      );

      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(FoundryBackend.builder()
              .bearerTokenSupplier(bearerTokenSupplier)
              .resource("example-resource")
              .build())
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model("claude-opus-4-8")
          .maxTokens(1024)
          .addUserMessage("Hello!")
          .build();

      client.messages().create(params).content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> System.out.println(textBlock.text()));
  }
  ```

  ```php PHP
  use Anthropic\Foundry;

  // Dapatkan token akses Entra ID, misalnya menggunakan Azure CLI:
  //   az account get-access-token --resource https://ai.azure.com \
  //     --query accessToken -o tsv
  $token = getenv('AZURE_ACCESS_TOKEN');

  $client = Foundry\Client::withCredentials(
      authToken: $token,
      baseUrl: 'https://example-resource.services.ai.azure.com/anthropic',
  );

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Hello!']
      ],
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  # SDK Ruby belum mendukung Foundry secara native. Contoh ini menggunakan
  # SDK Ruby standar sebagai solusi sementara, dengan token Entra ID statis:
  # pembaruan token otomatis tidak tersedia bawaan, sehingga aplikasi Anda
  # harus memperbarui token sendiri (biasanya kedaluwarsa setelah 1 jam).
  # Berikan kredensial secara eksplisit: tanpanya, klien akan kembali ke
  # variabel lingkungan ANTHROPIC_API_KEY atau ANTHROPIC_AUTH_TOKEN. Untuk
  # dukungan Foundry penuh, gunakan SDK C#, Java, PHP, Python, atau TypeScript.
  require "anthropic"

  # Dapatkan token akses Entra ID, misalnya menggunakan Azure CLI:
  #   az account get-access-token --resource https://ai.azure.com \
  #     --query accessToken -o tsv
  client = Anthropic::Client.new(
    base_url: "https://example-resource.services.ai.azure.com/anthropic",
    auth_token: ENV.fetch("AZURE_ACCESS_TOKEN")
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

## ID permintaan korelasi

Foundry menyertakan pengidentifikasi permintaan di header respons HTTP untuk debugging dan pelacakan. Saat menghubungi dukungan, berikan nilai `request-id` dan `apim-request-id` (Azure API Management) untuk membantu tim dengan cepat menemukan dan menyelidiki permintaan Anda di sistem Anthropic dan Azure.

## Dukungan fitur

Claude di Microsoft Foundry mendukung sebagian besar fitur Claude. Anda dapat menemukan semua fitur yang saat ini didukung di [Ikhtisar fitur](/docs/id/build-with-claude/overview).

### Jendela konteks

Claude Fable 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6 memiliki [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) di Microsoft Foundry. Model Claude lainnya, termasuk Claude Sonnet 4.5, memiliki jendela konteks 200k token.

### Fitur Claude yang tidak didukung untuk Claude di Microsoft Foundry

* Admin API
* Alat Advisor
* Claude Managed Agents
* Compliance API
* Models API
* Message Batches API
* Fallback sisi server ([parameter `fallbacks`](/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback); gunakan [pola fallback sisi klien](/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) sebagai gantinya)

### Fitur tambahan yang tidak didukung saat dihosting di Azure

Fitur berikut tersedia untuk deployment yang dihosting di Anthropic tetapi tidak didukung untuk deployment yang dihosting di Azure:

* Structured outputs
* Alat sisi server (pencarian web, pengambilan web, eksekusi kode, dan pencarian alat)
* Konektor MCP
* Agent Skills
* Pemanggilan alat terprogram
* Files API

Permintaan yang menggunakan fitur-fitur ini terhadap deployment yang dihosting di Azure mengembalikan error `400 Bad Request` sesuai desain. Claude Code mendeteksi deployment yang dihosting di Azure dan secara otomatis menyesuaikan rangkaian fiturnya.

## Respons API

Respons API dari Claude di Microsoft Foundry mengikuti [format respons Claude API](/docs/id/api/messages/create) standar. Ini termasuk objek `usage` di body respons, yang memberikan informasi konsumsi token terperinci untuk permintaan Anda. Objek `usage` konsisten di semua platform (Claude API, Amazon Bedrock, Claude Platform di AWS, Foundry, dan Google Cloud).

Untuk detail tentang header respons khusus Foundry, lihat [ID permintaan korelasi](#correlation-request-ids).

## ID model API dan deployment

Istilah siklus hidup (Deprecated, Retired) didefinisikan di [Penghentian model](/docs/id/about-claude/model-deprecations). Microsoft Foundry mengikuti jadwal siklus hidup Claude API.

Model Claude berikut tersedia melalui Foundry:

| Model                                                  | Nama deployment default | Dihosting di Azure | Dihosting di Anthropic |
| ------------------------------------------------------ | ----------------------- | ------------------ | ---------------------- |
| Claude Fable 5                                         | claude-fable-5          |                    | ✓                      |
| Claude Opus 4.8                                        | claude-opus-4-8         | ✓                  | ✓                      |
| Claude Opus 4.7                                        | claude-opus-4-7         |                    | ✓                      |
| Claude Opus 4.6                                        | claude-opus-4-6         |                    | ✓                      |
| Claude Opus 4.5                                        | claude-opus-4-5         |                    | ✓                      |
| Claude Opus 4.1 Deprecated. Dihentikan 5 Agustus 2026. | claude-opus-4-1         |                    | ✓                      |
| Claude Sonnet 5                                        | claude-sonnet-5         | ✓                  | ✓                      |
| Claude Sonnet 4.6                                      | claude-sonnet-4-6       |                    | ✓                      |
| Claude Sonnet 4.5                                      | claude-sonnet-4-5       |                    | ✓                      |
| Claude Haiku 4.5                                       | claude-haiku-4-5        | ✓                  | ✓                      |

Secara default, nama deployment sama dengan ID model yang ditampilkan di tabel sebelumnya. Namun, Anda dapat membuat deployment kustom dengan nama berbeda di portal Foundry untuk mengelola konfigurasi, versi, atau batas laju yang berbeda. Gunakan nama deployment (tidak harus ID model) dalam permintaan API Anda.

<Info>
  [Claude Mythos Preview](https://anthropic.com/glasswing) adalah pratinjau riset yang tersedia untuk pelanggan yang diundang di Microsoft Foundry.
</Info>

<Tip>
  Melakukan upgrade ke model Claude yang lebih baru? Di Claude Code, jalankan `/claude-api migrate` untuk menerapkan penggantian ID model dan perubahan parameter yang bersifat breaking di seluruh codebase Anda. Skill ini mendeteksi platform cloud mana yang ditargetkan oleh kode Anda dan menyesuaikan format ID model serta perubahan fitur untuk platform tersebut. Lihat [Migrasi ke model Claude yang lebih baru](/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

## Penagihan

Claude di Microsoft Foundry menagih melalui [Azure Marketplace](https://azuremarketplace.microsoft.com/). Penggunaan didenominasikan dalam Claude Consumption Units (CCU), diukur per jam, dan ditagih bulanan di belakang pada tagihan Azure Anda. CCU bukan kredit prabayar. Tidak ada saldo atau komitmen CCU.

Untuk harga CCU, mekanisme konversi, dan tarif token per model, lihat [harga Claude di Microsoft Foundry](/docs/id/about-claude/pricing#claude-in-microsoft-foundry-pricing).

## Migrasi antar opsi hosting

Untuk memindahkan deployment yang ada dari satu opsi hosting ke opsi lainnya:

1. Buat deployment baru dari versi hosting lain dari model tersebut (Dihosting di Azure atau Dihosting di Anthropic). Ini bisa berada di resource Foundry yang sama, atau yang baru.
2. Perbarui aplikasi Anda untuk memberikan nama deployment baru di parameter `model`.
3. Hapus deployment lama setelah lalu lintas berpindah.

Jika deployment baru berada di resource Foundry yang sama, URL endpoint dan autentikasi Anda tidak berubah. Jika Anda membuat resource baru, perbarui endpoint dan kredensial aplikasi Anda agar mengarah ke sana.

## Pemantauan dan logging

Azure menyediakan pemantauan dan logging untuk penggunaan Claude Anda melalui pola Azure standar:

* **Azure Monitor:** Lacak penggunaan API, latensi, dan tingkat error
* **Azure Log Analytics:** Kueri dan analisis log permintaan/respons
* **Cost Management:** Pantau dan perkirakan biaya yang terkait dengan penggunaan Claude

Anthropic merekomendasikan untuk mencatat aktivitas Anda setidaknya dalam basis bergulir 30 hari untuk memahami pola penggunaan dan menyelidiki potensi masalah.

<Note>
  Layanan logging Azure dikonfigurasi dalam langganan Azure Anda. Mengaktifkan logging tidak memberikan Microsoft atau Anthropic akses ke konten Anda di luar apa yang diperlukan untuk penagihan dan operasi layanan.
</Note>

## Pemecahan masalah

### Error autentikasi

**Error:** `401 Unauthorized` atau `Invalid API key`

* **Solusi:** Verifikasi bahwa kunci API Anda benar. Anda dapat menemukannya di portal Foundry pada tab **Details** deployment Anda (di bawah **Build** > **Models**).
* **Solusi:** Jika menggunakan Microsoft Entra ID, pastikan token akses Anda valid dan belum kedaluwarsa. Token biasanya kedaluwarsa setelah 1 jam.

**Error:** `403 Forbidden`

* **Solusi:** Akun Azure Anda mungkin tidak memiliki izin yang diperlukan. Pastikan Anda memiliki peran Azure RBAC yang sesuai (misalnya, **Foundry User** (sebelumnya Azure AI User) atau **Cognitive Services User**).

### Pembatasan laju

**Error:** `429 Too Many Requests`

* **Solusi:** Anda telah melampaui batas laju Anda. Terapkan exponential backoff dan logika retry di aplikasi Anda.
* **Solusi:** Pertimbangkan untuk meminta peningkatan batas laju melalui portal Azure atau dukungan Azure.

#### Header batas laju

Foundry tidak menyertakan header batas laju standar Anthropic (`anthropic-ratelimit-tokens-limit`, `anthropic-ratelimit-tokens-remaining`, `anthropic-ratelimit-tokens-reset`, `anthropic-ratelimit-input-tokens-limit`, `anthropic-ratelimit-input-tokens-remaining`, `anthropic-ratelimit-input-tokens-reset`, `anthropic-ratelimit-output-tokens-limit`, `anthropic-ratelimit-output-tokens-remaining`, dan `anthropic-ratelimit-output-tokens-reset`) dalam respons. Kelola pembatasan laju melalui alat pemantauan Azure sebagai gantinya.

### Error model dan deployment

**Error:** `Model not found` atau `Deployment not found`

* **Solusi:** Verifikasi bahwa Anda menggunakan nama deployment yang benar. Jika Anda belum membuat deployment kustom, gunakan ID model default (misalnya, claude-opus-4-8).
* **Solusi:** Pastikan model/deployment tersedia di region Azure Anda.

**Error:** `Invalid model parameter`

* **Solusi:** Parameter model harus berisi nama deployment Anda, yang dapat disesuaikan di portal Foundry. Verifikasi bahwa deployment ada dan dikonfigurasi dengan benar.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ikhtisar fitur" icon="stack" href="/docs/id/build-with-claude/overview">
    Jelajahi fitur dan kemampuan lanjutan Claude.
  </Card>

  <Card title="Harga" icon="chart" href="/docs/id/about-claude/pricing#claude-in-microsoft-foundry-pricing">
    Pelajari struktur harga Anthropic untuk model dan fitur.
  </Card>

  <Card title="Penghentian model" icon="arrow-clockwise" href="/docs/id/about-claude/model-deprecations">
    Seiring diluncurkannya model yang lebih aman dan lebih mampu, Anthropic secara berkala menghentikan model yang lebih lama. Lihat semua penghentian API, beserta penggantian yang direkomendasikan.
  </Card>
</CardGroup>

## Sumber daya tambahan

<CardGroup cols={2}>
  <Card title="Katalog model Foundry" icon="grid" href="https://ai.azure.com/catalog/publishers/anthropic">
    Telusuri model Anthropic di katalog Foundry.
  </Card>

  <Card title="Harga Azure AI Foundry" icon="calculator" href="https://azure.microsoft.com/en-us/pricing/details/ai-foundry/#pricing">
    Lihat detail harga Microsoft untuk Azure AI Foundry.
  </Card>

  <Card title="Harga model" icon="table" href="/docs/id/about-claude/pricing#model-pricing">
    Lihat detail harga per model Anthropic.
  </Card>

  <Card title="Portal Azure" icon="cloud" href="https://portal.azure.com/">
    Kelola resource Azure Anda.
  </Card>
</CardGroup>
