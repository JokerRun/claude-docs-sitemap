---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry
fetched_at: 2026-06-11T03:14:59.596724Z
sha256: a8b2b27c2196e4bd62e53139eefca01d39ed72606f43102819779fbabfd5fc33
---

# Claude di Microsoft Foundry

Akses model Claude melalui Microsoft Foundry dengan endpoint dan autentikasi native Azure.

---

Panduan ini memandu Anda melalui proses penyiapan dan pembuatan panggilan API ke Claude di Foundry menggunakan salah satu SDK klien Anthropic atau permintaan HTTP langsung. Ketika Anda dapat mengakses Claude di Foundry, Anda ditagih untuk penggunaan Claude di Microsoft Marketplace, memungkinkan Anda mengakses kemampuan terbaru Claude sambil mengelola biaya melalui langganan Azure Anda.

Ketersediaan regional: Saat peluncuran, Claude tersedia sebagai tipe deployment Global Standard di resource Foundry. Harga untuk Claude di Microsoft Marketplace menggunakan harga API standar Anthropic. Kunjungi [Harga](https://claude.com/pricing#api) untuk detailnya.

<Note>
Foundry didukung oleh SDK C#, Java, PHP, Python, dan TypeScript. SDK Go dan Ruby saat ini tidak mendukung Microsoft Foundry.
</Note>

## Pratinjau \{#preview}

Dalam integrasi platform pratinjau ini, model Claude berjalan di infrastruktur Anthropic. Ini adalah integrasi komersial untuk penagihan dan akses melalui Azure. Sebagai pemroses independen untuk Microsoft, pelanggan yang menggunakan Claude melalui Microsoft Foundry tunduk pada ketentuan penggunaan data Anthropic. Anthropic terus menyediakan komitmen keamanan dan data terdepan di industri, termasuk ketersediaan zero data retention (tanpa retensi data).

## Prasyarat \{#prerequisites}

Sebelum memulai, pastikan Anda memiliki:

- Langganan Azure yang aktif
- Akses ke [Foundry](https://ai.azure.com/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) terinstal (opsional, untuk manajemen resource)

## Menginstal SDK \{#install-an-sdk}

[SDK klien](/docs/id/cli-sdks-libraries/overview) Anthropic mendukung Foundry melalui paket atau kelas klien khusus platform.

<Tabs>
<Tab title="Python">
```bash
pip install -U "anthropic"
```
</Tab>

<Tab title="TypeScript">
```bash
npm install @anthropic-ai/foundry-sdk
```
</Tab>

<Tab title="C#">
```bash
dotnet add package Anthropic.Foundry
```
</Tab>

<Tab title="Java">
<Tabs>
<Tab title="Gradle">
```kotlin
implementation("com.anthropic:anthropic-java-foundry:2.40.0")
```
</Tab>
<Tab title="Maven">
```xml
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>anthropic-java-foundry</artifactId>
    <version>2.40.0</version>
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
</Tabs>

## Penyediaan (Provisioning) \{#provisioning}

Foundry menggunakan hierarki dua tingkat: **resource** berisi konfigurasi keamanan dan penagihan Anda, sedangkan **deployment** adalah instance model yang Anda panggil melalui API. Anda akan terlebih dahulu membuat resource Foundry, kemudian membuat satu atau lebih deployment Claude di dalamnya.

### Menyediakan resource Foundry \{#provisioning-foundry-resources}

Buat resource Foundry, yang diperlukan untuk menggunakan dan mengelola layanan di Azure. Anda dapat mengikuti instruksi ini untuk membuat [resource Foundry](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal#create-a-new-azure-ai-foundry-resource). Sebagai alternatif, Anda dapat memulai dengan membuat [proyek Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/create-projects?tabs=ai-foundry), yang melibatkan pembuatan resource Foundry.

Untuk menyediakan resource Anda:

1. Navigasikan ke [portal Foundry](https://ai.azure.com/)
2. Buat resource Foundry baru atau pilih yang sudah ada
3. Konfigurasikan manajemen akses menggunakan kunci API yang diterbitkan Azure atau Entra ID (sebelumnya Azure Active Directory) untuk kontrol akses berbasis peran
4. Secara opsional, konfigurasikan resource agar menjadi bagian dari jaringan privat (Azure Virtual Network) untuk keamanan yang lebih baik
5. Catat nama resource Anda. Anda akan menggunakannya sebagai `{resource}` di endpoint API (misalnya, `https://{resource}.services.ai.azure.com/anthropic/v1/*`)

### Membuat deployment Foundry \{#creating-foundry-deployments}

Setelah membuat resource Anda, deploy model Claude agar tersedia untuk panggilan API:

1. Di portal Foundry, navigasikan ke resource Anda
2. Buka **Models + endpoints** dan pilih **+ Deploy model** > **Deploy base model**
3. Cari dan pilih model Claude (misalnya, `claude-sonnet-4-6`)
4. Konfigurasikan pengaturan deployment:
   - **Deployment name:** Secara default menggunakan ID model, tetapi Anda dapat menyesuaikannya (misalnya, `my-claude-deployment`). Nama deployment tidak dapat diubah setelah dibuat.
   - **Deployment type:** Pilih Global Standard (direkomendasikan untuk Claude)
5. Pilih **Deploy** dan tunggu hingga penyediaan selesai
6. Setelah di-deploy, Anda dapat menemukan URL endpoint dan kunci Anda di bawah **Keys and Endpoint**

<Note>
  Nama deployment yang Anda pilih menjadi nilai yang Anda berikan dalam parameter `model` pada permintaan API Anda. Anda dapat membuat beberapa deployment dari model yang sama dengan nama berbeda untuk mengelola konfigurasi atau batas laju yang terpisah.
</Note>

## Autentikasi \{#authentication}

Claude di Foundry mendukung dua metode autentikasi: kunci API dan token Entra ID. Kedua metode menggunakan endpoint yang di-host Azure dalam format `https://{resource}.services.ai.azure.com/anthropic/v1/*`.

### Autentikasi kunci API \{#api-key-authentication}

Setelah menyediakan resource Claude Foundry Anda, Anda dapat memperoleh kunci API dari portal Foundry:

1. Navigasikan ke resource Anda di portal Foundry
2. Buka bagian **Keys and Endpoint**
3. Salin salah satu kunci API yang disediakan
4. Gunakan header `api-key` atau `x-api-key` dalam permintaan Anda, atau berikan ke SDK

SDK Foundry memerlukan kunci API dan nama resource atau base URL. SDK C#, Java, PHP, Python, dan TypeScript secara otomatis membaca ini dari variabel lingkungan berikut jika didefinisikan:

- `ANTHROPIC_FOUNDRY_API_KEY` - Kunci API Anda
- `ANTHROPIC_FOUNDRY_RESOURCE` - Nama resource Anda (misalnya, `example-resource`)
- `ANTHROPIC_FOUNDRY_BASE_URL` - Alternatif untuk nama resource; base URL lengkap (misalnya, `https://example-resource.services.ai.azure.com/anthropic/`)

<Note>
Parameter `resource` dan `base_url` bersifat saling eksklusif. Berikan nama resource (yang digunakan SDK untuk menyusun URL sebagai `https://{resource}.services.ai.azure.com/anthropic/`) atau base URL lengkap secara langsung.
</Note>

**Contoh menggunakan kunci API:**

<Tabs>
<Tab title="cURL">

```bash cURL nocheck
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
</Tab>

<Tab title="CLI">

```bash CLI nocheck
# ant reads ANTHROPIC_API_KEY and sends it as x-api-key, which Foundry accepts
export ANTHROPIC_API_KEY="YOUR_AZURE_API_KEY"

ant messages create \
  --base-url https://example-resource.services.ai.azure.com/anthropic \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --message '{role: user, content: "Hello!"}' \
  --transform content
```
</Tab>

<Tab title="Python">

```python nocheck
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
</Tab>

<Tab title="TypeScript">

```typescript nocheck
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
</Tab>

<Tab title="C#">

```csharp nocheck
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
</Tab>

<Tab title="Java">

```java Java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.foundry.backends.FoundryBackend;
import com.anthropic.models.messages.MessageCreateParams;

void main() {
    // Requires env vars: ANTHROPIC_FOUNDRY_API_KEY, ANTHROPIC_FOUNDRY_RESOURCE
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
</Tab>

<Tab title="PHP">

```php PHP nocheck
<?php

use Anthropic\Foundry;

$client = Foundry\Client::withCredentials(
    apiKey: getenv('ANTHROPIC_FOUNDRY_API_KEY'),
    baseUrl: 'https://example-resource.services.ai.azure.com/anthropic/v1',
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
</Tab>

<Tab title="Ruby">
<Note>
SDK Ruby Anthropic saat ini tidak mendukung Microsoft Foundry. Anda dapat menggunakan `Anthropic::Client` standar dengan `base_url` kustom yang mengarah ke endpoint Foundry Anda, tetapi autentikasi khusus Azure (Entra ID) tidak tersedia secara bawaan. Untuk dukungan Foundry penuh, gunakan SDK C#, Java, PHP, Python, atau TypeScript.
</Note>
</Tab>
</Tabs>

<Warning>
Jaga keamanan kunci API Anda. Jangan pernah melakukan commit ke version control atau membagikannya secara publik. Siapa pun yang memiliki akses ke kunci API Anda dapat membuat permintaan ke Claude melalui resource Foundry Anda.
</Warning>

### Autentikasi Microsoft Entra \{#microsoft-entra-authentication}

Untuk keamanan yang lebih baik dan manajemen akses terpusat, Anda dapat menggunakan token Entra ID:

1. Aktifkan autentikasi Entra untuk resource Foundry Anda
2. Dapatkan access token dari Entra ID
3. Gunakan token dalam header `Authorization: Bearer {TOKEN}`

**Contoh menggunakan Entra ID:**

<Tabs>
<Tab title="cURL">

```bash cURL nocheck
# Get Microsoft Entra ID token
ACCESS_TOKEN=$(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)

# Make request with token. Replace {resource} with your resource name
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
</Tab>

<Tab title="Python">

```python nocheck
import os
from anthropic import AnthropicFoundry
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Get Microsoft Entra ID token using token provider pattern
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

# Create client with Entra ID authentication
client = AnthropicFoundry(
    resource="example-resource",  # your resource name
    azure_ad_token_provider=token_provider,  # Use token provider for Entra ID auth
)

# Make request
message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)
print(message.content)
```
</Tab>

<Tab title="TypeScript">

```typescript nocheck
import AnthropicFoundry from "@anthropic-ai/foundry-sdk";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

// Get Entra ID token using token provider pattern
const credential = new DefaultAzureCredential();
const tokenProvider = getBearerTokenProvider(
  credential,
  "https://cognitiveservices.azure.com/.default"
);

// Create client with Entra ID authentication
const client = new AnthropicFoundry({
  resource: "example-resource", // your resource name
  azureADTokenProvider: tokenProvider // Use token provider for Entra ID auth
});

// Make request
const message = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }]
});
console.log(message.content);
```
</Tab>

<Tab title="C#">

```csharp nocheck
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
</Tab>

<Tab title="Java">

```java Java nocheck hidelines={1..2,4,8}
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
        "https://cognitiveservices.azure.com/.default"
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
</Tab>

<Tab title="PHP">

```php PHP nocheck
<?php

use Anthropic\Foundry;

// Obtain an Entra ID access token, for example via the Azure CLI:
//   az account get-access-token --resource https://cognitiveservices.azure.com \
//     --query accessToken -o tsv
$token = getenv('AZURE_ACCESS_TOKEN');

$client = Foundry\Client::withCredentials(
    authToken: $token,
    baseUrl: 'https://example-resource.services.ai.azure.com/anthropic/v1',
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
</Tab>

<Tab title="Ruby">
<Note>
SDK Ruby Anthropic saat ini tidak mendukung Microsoft Foundry. Anda dapat menggunakan `Anthropic::Client` standar dengan `base_url` kustom yang mengarah ke endpoint Foundry Anda, tetapi autentikasi khusus Azure (Entra ID) tidak tersedia secara bawaan. Untuk dukungan Foundry penuh, gunakan SDK C#, Java, PHP, Python, atau TypeScript.
</Note>
</Tab>
</Tabs>

<Note>
Autentikasi Microsoft Entra ID memungkinkan Anda mengelola akses menggunakan Azure RBAC, berintegrasi dengan manajemen identitas organisasi Anda, dan menghindari pengelolaan kunci API secara manual.
</Note>

## ID permintaan korelasi \{#correlation-request-ids}

Foundry menyertakan pengidentifikasi permintaan dalam header respons HTTP untuk debugging dan pelacakan. Saat menghubungi dukungan, berikan nilai `request-id` dan `apim-request-id` untuk membantu tim menemukan dan menyelidiki permintaan Anda dengan cepat di seluruh sistem Anthropic dan Azure.

## Dukungan fitur \{#feature-support}

Claude di Foundry mendukung sebagian besar fitur canggih Claude. Anda dapat menemukan semua fitur yang saat ini didukung di [Ikhtisar fitur](/docs/id/build-with-claude/overview).

### Jendela konteks \{#context-window}

Claude Fable 5, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6 memiliki [jendela konteks 1 juta token](/docs/id/build-with-claude/context-windows) di Microsoft Foundry. Model Claude lainnya, termasuk Claude Opus 4.8 dan Sonnet 4.5, memiliki jendela konteks 200 ribu token.

### Fitur yang tidak didukung \{#features-not-supported}

- Admin API
- Compliance API
- Models API
- Message Batches API
- Fallback sisi server (parameter [`fallbacks`](/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback); gunakan [pola fallback sisi klien](/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) sebagai gantinya)

## Respons API \{#api-responses}

Respons API dari Claude di Foundry mengikuti [format respons Claude API](/docs/id/api/messages/create) standar. Ini mencakup objek `usage` dalam body respons, yang menyediakan informasi konsumsi token terperinci untuk permintaan Anda. Objek `usage` konsisten di semua platform (Claude API, Foundry, Claude Platform di AWS, Amazon Bedrock, dan Vertex AI).

Untuk detail tentang header respons khusus Foundry, lihat [ID permintaan korelasi](#correlation-request-ids).

## ID model API dan deployment \{#api-model-ids-and-deployments}

Istilah siklus hidup (Deprecated, Retired) didefinisikan di [Deprekasi model](/docs/id/about-claude/model-deprecations). Microsoft Foundry mengikuti jadwal siklus hidup Claude API.

Model Claude berikut tersedia melalui Foundry. Model generasi terbaru (Claude Fable 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6, dan Haiku 4.5) menawarkan kemampuan paling canggih:

| Model             | Nama deployment default     |
| :---------------- | :-------------------------- |
| Claude Fable 5    | claude-fable-5 |
| Claude Opus 4.8   | claude-opus-4-8 |
| Claude Opus 4.7   | claude-opus-4-7           |
| Claude Opus 4.6   | claude-opus-4-6           |
| Claude Opus 4.5   | claude-opus-4-5           |
| Claude Opus 4.1 <br /><small>Tidak digunakan lagi. Dihentikan pada 5 Agustus 2026.</small> | claude-opus-4-1           |
| Claude Sonnet 4.6 | claude-sonnet-4-6         |
| Claude Sonnet 4.5 | claude-sonnet-4-5         |
| Claude Haiku 4.5  | claude-haiku-4-5          |

Secara default, nama deployment cocok dengan ID model yang ditampilkan pada tabel sebelumnya. Namun, Anda dapat membuat deployment kustom dengan nama berbeda di portal Foundry untuk mengelola konfigurasi, versi, atau batas laju yang berbeda. Gunakan nama deployment (tidak harus ID model) dalam permintaan API Anda.

<Tip>
Melakukan upgrade ke model Claude yang lebih baru? Di Claude Code, jalankan `/claude-api migrate` untuk menerapkan penggantian ID model dan perubahan parameter yang bersifat breaking di seluruh codebase Anda. Skill ini mendeteksi platform cloud mana yang ditargetkan oleh kode Anda dan menyesuaikan format ID model serta perubahan fitur untuk platform tersebut. Lihat [Migrasi ke model Claude yang lebih baru](/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

## Pemantauan dan logging \{#monitoring-and-logging}

Azure menyediakan kemampuan pemantauan dan logging yang komprehensif untuk penggunaan Claude Anda melalui pola Azure standar:

- **Azure Monitor:** Lacak penggunaan API, latensi, dan tingkat kesalahan
- **Azure Log Analytics:** Kueri dan analisis log permintaan/respons
- **Cost Management:** Pantau dan perkirakan biaya yang terkait dengan penggunaan Claude

Anthropic merekomendasikan untuk mencatat aktivitas Anda setidaknya secara bergulir 30 hari untuk memahami pola penggunaan dan menyelidiki potensi masalah.

<Note>
Layanan logging Azure dikonfigurasi dalam langganan Azure Anda. Mengaktifkan logging tidak memberikan Microsoft atau Anthropic akses ke konten Anda di luar yang diperlukan untuk penagihan dan operasi layanan.
</Note>

## Pemecahan masalah \{#troubleshooting}

### Kesalahan autentikasi \{#authentication-errors}

**Kesalahan:** `401 Unauthorized` atau `Invalid API key`

- **Solusi:** Verifikasi bahwa kunci API Anda benar. Anda dapat memperoleh kunci API baru dari portal Foundry di bawah **Keys and Endpoint** untuk resource Foundry Anda.
- **Solusi:** Jika menggunakan Microsoft Entra ID, pastikan access token Anda valid dan belum kedaluwarsa. Token biasanya kedaluwarsa setelah 1 jam.

**Kesalahan:** `403 Forbidden`

- **Solusi:** Akun Azure Anda mungkin tidak memiliki izin yang diperlukan. Pastikan Anda memiliki peran Azure RBAC yang sesuai (misalnya, "Cognitive Services OpenAI User").

### Pembatasan laju \{#rate-limiting}

**Kesalahan:** `429 Too Many Requests`

- **Solusi:** Anda telah melampaui batas laju Anda. Terapkan logika exponential backoff dan retry dalam aplikasi Anda.
- **Solusi:** Pertimbangkan untuk meminta peningkatan batas laju melalui portal Azure atau dukungan Azure.

#### Header batas laju \{#rate-limit-headers}

Foundry tidak menyertakan header batas laju standar Anthropic (`anthropic-ratelimit-tokens-limit`, `anthropic-ratelimit-tokens-remaining`, `anthropic-ratelimit-tokens-reset`, `anthropic-ratelimit-input-tokens-limit`, `anthropic-ratelimit-input-tokens-remaining`, `anthropic-ratelimit-input-tokens-reset`, `anthropic-ratelimit-output-tokens-limit`, `anthropic-ratelimit-output-tokens-remaining`, dan `anthropic-ratelimit-output-tokens-reset`) dalam respons. Kelola pembatasan laju melalui alat pemantauan Azure sebagai gantinya.

### Kesalahan model dan deployment \{#model-and-deployment-errors}

**Kesalahan:** `Model not found` atau `Deployment not found`

- **Solusi:** Verifikasi bahwa Anda menggunakan nama deployment yang benar. Jika Anda belum membuat deployment kustom, gunakan ID model default (misalnya, `claude-sonnet-4-6`).
- **Solusi:** Pastikan model/deployment tersedia di region Azure Anda.

**Kesalahan:** `Invalid model parameter`

- **Solusi:** Parameter model harus berisi nama deployment Anda, yang dapat disesuaikan di portal Foundry. Verifikasi bahwa deployment tersebut ada dan dikonfigurasi dengan benar.

<Info>
[Claude Mythos Preview](https://anthropic.com/glasswing) adalah pratinjau riset yang tersedia untuk pelanggan yang diundang di Microsoft Foundry. Untuk informasi lebih lanjut, lihat [Project Glasswing](https://anthropic.com/glasswing).
</Info>

## Sumber daya tambahan \{#additional-resources}

- **Dokumentasi Foundry:** [ai.azure.com/catalog](https://ai.azure.com/catalog/publishers/anthropic)
- **Harga Azure:** [azure.microsoft.com/en-us/pricing/details/ai-foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/#pricing)
- **Detail harga Anthropic:** [Harga model](/docs/id/about-claude/pricing#model-pricing)
- **Panduan autentikasi:** Lihat [Autentikasi](#authentication)
- **Portal Azure:** [portal.azure.com](https://portal.azure.com/)