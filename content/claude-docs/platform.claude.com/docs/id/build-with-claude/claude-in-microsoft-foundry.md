---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 1bad9d12011aa0ca4e0531df4b23db61c1981f70a1d7ed43bf9d4ad29b97e632
---

# Claude di Microsoft Foundry

Akses model Claude melalui Microsoft Foundry dengan endpoint asli Azure dan autentikasi.

---

Panduan ini memandu Anda melalui proses pengaturan dan pembuatan panggilan API ke Claude di Foundry dalam Python, TypeScript, atau menggunakan permintaan HTTP langsung. Ketika Anda dapat mengakses Claude di Foundry, Anda ditagih untuk penggunaan Claude di Microsoft Marketplace dengan langganan Azure Anda, memungkinkan Anda mengakses kemampuan terbaru Claude sambil mengelola biaya melalui langganan Azure Anda.

Ketersediaan regional: Saat peluncuran, Claude tersedia sebagai jenis penyebaran Global Standard dalam sumber daya Foundry (US DataZone akan segera hadir). Harga Claude di Microsoft Marketplace menggunakan harga API standar Anthropic. Kunjungi [halaman harga](https://claude.com/pricing#api) untuk detail.

<Note>
Foundry didukung oleh SDK C#, Java, PHP, Python, dan TypeScript. SDK Go dan Ruby saat ini tidak mendukung Microsoft Foundry. Untuk integrasi platform SDK yang tersedia, lihat [Client SDKs](/docs/id/api/client-sdks).
</Note>

## Pratinjau

Dalam integrasi platform pratinjau ini, model Claude berjalan di infrastruktur Anthropic. Ini adalah integrasi komersial untuk penagihan dan akses melalui Azure. Sebagai pemroses independen untuk Microsoft, pelanggan yang menggunakan Claude melalui Microsoft Foundry tunduk pada syarat penggunaan data Anthropic. Anthropic terus memberikan komitmen keamanan dan data terdepan di industri, termasuk ketersediaan retensi data nol.

## Prasyarat

Sebelum Anda mulai, pastikan Anda memiliki:

- Langganan Azure yang aktif
- Akses ke [Foundry](https://ai.azure.com/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) terinstal (opsional, untuk manajemen sumber daya)

## Instal SDK

[Client SDKs](/docs/id/api/client-sdks) Anthropic mendukung Foundry melalui paket khusus platform.

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
implementation("com.anthropic:anthropic-java-foundry:2.20.0")
```
</Tab>
<Tab title="Maven">
```xml
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>anthropic-java-foundry</artifactId>
    <version>2.20.0</version>
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

## Penyediaan

Foundry menggunakan hierarki dua tingkat: **sumber daya** berisi konfigurasi keamanan dan penagihan Anda, sementara **penyebaran** adalah instans model yang Anda panggil melalui API. Anda akan terlebih dahulu membuat sumber daya Foundry, kemudian membuat satu atau lebih penyebaran Claude di dalamnya.

### Penyediaan sumber daya Foundry

Buat sumber daya Foundry, yang diperlukan untuk menggunakan dan mengelola layanan di Azure. Anda dapat mengikuti instruksi ini untuk membuat [sumber daya Foundry](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal#create-a-new-azure-ai-foundry-resource). Atau, Anda dapat memulai dengan membuat [proyek Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/create-projects?tabs=ai-foundry), yang melibatkan pembuatan sumber daya Foundry.

Untuk menyediakan sumber daya Anda:

1. Navigasikan ke [portal Foundry](https://ai.azure.com/)
2. Buat sumber daya Foundry baru atau pilih yang sudah ada
3. Konfigurasi manajemen akses menggunakan kunci API yang dikeluarkan Azure atau Entra ID untuk kontrol akses berbasis peran
4. Secara opsional konfigurasi sumber daya untuk menjadi bagian dari jaringan pribadi (Azure Virtual Network) untuk keamanan yang ditingkatkan
5. Catat nama sumber daya Anda. Anda akan menggunakannya sebagai `{resource}` dalam titik akhir API (misalnya, `https://{resource}.services.ai.azure.com/anthropic/v1/*`)

### Membuat penyebaran Foundry

Setelah membuat sumber daya Anda, sebarkan model Claude untuk membuatnya tersedia untuk panggilan API:

1. Di portal Foundry, navigasikan ke sumber daya Anda
2. Buka **Models + endpoints** dan pilih **+ Deploy model** > **Deploy base model**
3. Cari dan pilih model Claude (misalnya, `claude-sonnet-4-6`)
4. Konfigurasi pengaturan penyebaran:
   - **Deployment name:** Secara default ke ID model, tetapi Anda dapat menyesuaikannya (misalnya, `my-claude-deployment`). Nama penyebaran tidak dapat diubah setelah dibuat.
   - **Deployment type:** Pilih Global Standard (direkomendasikan untuk Claude)
5. Pilih **Deploy** dan tunggu penyediaan selesai
6. Setelah disebarkan, Anda dapat menemukan URL titik akhir dan kunci Anda di bawah **Keys and Endpoint**

<Note>
  Nama penyebaran yang Anda pilih menjadi nilai yang Anda teruskan dalam parameter `model` dari permintaan API Anda. Anda dapat membuat beberapa penyebaran model yang sama dengan nama berbeda untuk mengelola konfigurasi terpisah atau batas laju.
</Note>

## Autentikasi

Claude di Foundry mendukung dua metode autentikasi: kunci API dan token Entra ID. Kedua metode menggunakan titik akhir yang dihosting Azure dalam format `https://{resource}.services.ai.azure.com/anthropic/v1/*`.

### Autentikasi kunci API

Setelah menyediakan sumber daya Claude Foundry Anda, Anda dapat memperoleh kunci API dari portal Foundry:

1. Navigasikan ke sumber daya Anda di portal Foundry
2. Buka bagian **Keys and Endpoint**
3. Salin salah satu kunci API yang disediakan
4. Gunakan header `api-key` atau `x-api-key` dalam permintaan Anda, atau berikan ke SDK

SDK Python dan TypeScript memerlukan kunci API dan nama sumber daya atau URL dasar. SDK akan secara otomatis membaca ini dari variabel lingkungan berikut jika ditentukan:

- `ANTHROPIC_FOUNDRY_API_KEY` - Kunci API Anda
- `ANTHROPIC_FOUNDRY_RESOURCE` - Nama sumber daya Anda (misalnya, `example-resource`)
- `ANTHROPIC_FOUNDRY_BASE_URL` - Alternatif untuk nama sumber daya; URL dasar lengkap (misalnya, `https://example-resource.services.ai.azure.com/anthropic/`)

<Note>
Parameter `resource` dan `base_url` saling eksklusif. Berikan nama sumber daya (yang digunakan SDK untuk membuat URL sebagai `https://{resource}.services.ai.azure.com/anthropic/`) atau URL dasar lengkap secara langsung.
</Note>

**Contoh menggunakan kunci API:**

<Tabs>
<Tab title="Shell">

```bash nocheck
curl https://{resource}.services.ai.azure.com/anthropic/v1/messages \
  -H "content-type: application/json" \
  -H "api-key: YOUR_AZURE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-7",
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
  --model claude-opus-4-7 \
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
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
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
    Model = "claude-opus-4-7",
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Hello!" }],
});

Console.WriteLine(
    string.Join("", response.Content
        .Where(c => c.Value is TextBlock)
        .Select(c => (c.Value as TextBlock)!.Text)));
```
</Tab>

<Tab title="Java">

```java Java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.foundry.backends.FoundryBackend;
import com.anthropic.models.messages.MessageCreateParams;

// Requires env vars: ANTHROPIC_FOUNDRY_API_KEY, ANTHROPIC_FOUNDRY_RESOURCE
AnthropicClient client = AnthropicOkHttpClient.builder()
  .backend(FoundryBackend.fromEnv())
  .build();

MessageCreateParams params = MessageCreateParams.builder()
  .model("claude-opus-4-7")
  .maxTokens(1024)
  .addUserMessage("Hello!")
  .build();

client.messages().create(params).content().stream()
  .flatMap(block -> block.text().stream())
  .forEach(textBlock -> System.out.println(textBlock.text()));
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
    model: 'claude-opus-4-7',
);
echo $message->content[0]->text;
```
</Tab>

<Tab title="Ruby">
<Note>
SDK Ruby Anthropic saat ini tidak mendukung Microsoft Azure AI Foundry. Anda dapat menggunakan `Anthropic::Client` standar dengan `base_url` kustom yang menunjuk ke titik akhir Foundry Anda, tetapi autentikasi khusus Azure (Entra ID) tidak tertanam. Untuk dukungan Foundry penuh, gunakan SDK Python atau TypeScript.
</Note>
</Tab>
</Tabs>

<Warning>
Jaga keamanan kunci API Anda. Jangan pernah komitkan ke kontrol versi atau bagikan secara publik. Siapa pun yang memiliki akses ke kunci API Anda dapat membuat permintaan ke Claude melalui sumber daya Foundry Anda.
</Warning>

## Autentikasi Microsoft Entra

Untuk keamanan yang ditingkatkan dan manajemen akses terpusat, Anda dapat menggunakan token Entra ID (sebelumnya Azure Active Directory):

1. Aktifkan autentikasi Entra untuk sumber daya Foundry Anda
2. Dapatkan token akses dari Entra ID
3. Gunakan token dalam header `Authorization: Bearer {TOKEN}`

**Contoh menggunakan Entra ID:**

<Tabs>
<Tab title="Shell">

```bash nocheck
# Get Azure Entra ID token
ACCESS_TOKEN=$(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)

# Make request with token. Replace {resource} with your resource name
curl https://{resource}.services.ai.azure.com/anthropic/v1/messages \
  -H "content-type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-7",
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

# Get Azure Entra ID token using token provider pattern
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
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
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
    Model = "claude-opus-4-7",
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Hello!" }],
});

Console.WriteLine(
    string.Join("", response.Content
        .Where(c => c.Value is TextBlock)
        .Select(c => (c.Value as TextBlock)!.Text)));
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
  .model("claude-opus-4-7")
  .maxTokens(1024)
  .addUserMessage("Hello!")
  .build();

client.messages().create(params).content().stream()
  .flatMap(block -> block.text().stream())
  .forEach(textBlock -> System.out.println(textBlock.text()));
```
</Tab>

<Tab title="PHP">

```php PHP nocheck
<?php

use Anthropic\Foundry;

// Azure Entra ID authentication
$client = Foundry\Client::withCredentials(
    authToken: $token,
    baseUrl: 'https://example-resource.services.ai.azure.com/anthropic/v1',
);

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Hello!']
    ],
    model: 'claude-opus-4-7',
);
echo $message->content[0]->text;
```
</Tab>

<Tab title="Ruby">
<Note>
SDK Ruby Anthropic saat ini tidak mendukung Microsoft Azure AI Foundry. Anda dapat menggunakan `Anthropic::Client` standar dengan `base_url` kustom yang menunjuk ke titik akhir Foundry Anda, tetapi autentikasi khusus Azure (Entra ID) tidak tertanam. Untuk dukungan Foundry penuh, gunakan SDK Python atau TypeScript.
</Note>
</Tab>
</Tabs>

<Note>
Autentikasi Azure Entra ID memungkinkan Anda mengelola akses menggunakan Azure RBAC, mengintegrasikan dengan manajemen identitas organisasi Anda, dan menghindari pengelolaan kunci API secara manual.
</Note>

## ID permintaan korelasi

Foundry menyertakan pengidentifikasi permintaan dalam header respons HTTP untuk debugging dan pelacakan. Saat menghubungi dukungan, berikan nilai `request-id` dan `apim-request-id` untuk membantu tim dengan cepat menemukan dan menyelidiki permintaan Anda di seluruh sistem Anthropic dan Azure.

## Fitur yang didukung

Claude di Foundry mendukung sebagian besar fitur Claude yang kuat. Anda dapat menemukan semua fitur yang saat ini didukung dalam [dokumentasi gambaran umum](/docs/id/build-with-claude/overview).

### Jendela konteks

Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6 memiliki [jendela konteks 1M-token](/docs/id/build-with-claude/context-windows) di Microsoft Foundry. Model Claude lainnya, termasuk Sonnet 4.5, memiliki jendela konteks 200k-token.

### Fitur yang tidak didukung

- Admin API (titik akhir `/v1/organizations/*`)
- Models API (`/v1/models`)
- Message Batch API (`/v1/messages/batches`)

## Respons API

Respons API dari Claude di Foundry mengikuti [format respons API Claude](/docs/id/api/messages/create) standar. Ini termasuk objek `usage` dalam badan respons, yang memberikan informasi konsumsi token terperinci untuk permintaan Anda. Objek `usage` konsisten di semua platform (API pihak pertama, Foundry, Amazon Bedrock, dan Google Vertex AI).

Untuk detail tentang header respons khusus Foundry, lihat [bagian ID permintaan korelasi](#correlation-request-ids).

## ID model API dan penyebaran

Model Claude berikut tersedia melalui Foundry. Model generasi terbaru (Opus 4.7, Opus 4.6, Sonnet 4.6, dan Haiku 4.5) menawarkan kemampuan paling canggih:

| Model             | Nama Penyebaran Default     |
| :---------------- | :-------------------------- |
| Claude Opus 4.7   | `claude-opus-4-7`           |
| Claude Opus 4.6     | `claude-opus-4-6`             |
| Claude Opus 4.5   | `claude-opus-4-5`           |
| Claude Sonnet 4.6 | `claude-sonnet-4-6`         |
| Claude Sonnet 4.5 | `claude-sonnet-4-5`         |
| Claude Opus 4.1   | `claude-opus-4-1`           |
| Claude Haiku 4.5  | `claude-haiku-4-5`          |

Secara default, nama penyebaran cocok dengan ID model yang ditunjukkan di atas. Namun, Anda dapat membuat penyebaran kustom dengan nama berbeda di portal Foundry untuk mengelola konfigurasi, versi, atau batas laju yang berbeda. Gunakan nama penyebaran (tidak harus ID model) dalam permintaan API Anda.

## Pemantauan dan logging

Azure menyediakan kemampuan pemantauan dan logging komprehensif untuk penggunaan Claude Anda melalui pola Azure standar:

- **Azure Monitor:** Lacak penggunaan API, latensi, dan tingkat kesalahan
- **Azure Log Analytics:** Kueri dan analisis log permintaan/respons
- **Cost Management:** Pantau dan perkirakan biaya yang terkait dengan penggunaan Claude

Anthropic merekomendasikan logging aktivitas Anda setidaknya pada dasar 30 hari bergulir untuk memahami pola penggunaan dan menyelidiki potensi masalah.

<Note>
Layanan logging Azure dikonfigurasi dalam langganan Azure Anda. Mengaktifkan logging tidak memberikan Microsoft atau Anthropic akses ke konten Anda di luar apa yang diperlukan untuk penagihan dan operasi layanan.
</Note>

## Pemecahan masalah

### Kesalahan autentikasi

**Error:** `401 Unauthorized` atau `Invalid API key`

- **Solusi:** Verifikasi kunci API Anda benar. Anda dapat memperoleh kunci API baru dari portal Azure di bawah **Keys and Endpoint** untuk sumber daya Claude Anda.
- **Solusi:** Jika menggunakan Azure Entra ID, pastikan token akses Anda valid dan belum kedaluwarsa. Token biasanya kedaluwarsa setelah 1 jam.

**Error:** `403 Forbidden`

- **Solusi:** Akun Azure Anda mungkin kekurangan izin yang diperlukan. Pastikan Anda memiliki peran Azure RBAC yang sesuai ditugaskan (misalnya, "Cognitive Services OpenAI User").

### Pembatasan laju

**Error:** `429 Too Many Requests`

- **Solusi:** Anda telah melampaui batas laju Anda. Implementasikan logika backoff eksponensial dan coba lagi dalam aplikasi Anda.
- **Solusi:** Pertimbangkan untuk meminta peningkatan batas laju melalui portal Azure atau dukungan Azure.

#### Header batas laju

Foundry tidak menyertakan header batas laju standar Anthropic (`anthropic-ratelimit-tokens-limit`, `anthropic-ratelimit-tokens-remaining`, `anthropic-ratelimit-tokens-reset`, `anthropic-ratelimit-input-tokens-limit`, `anthropic-ratelimit-input-tokens-remaining`, `anthropic-ratelimit-input-tokens-reset`, `anthropic-ratelimit-output-tokens-limit`, `anthropic-ratelimit-output-tokens-remaining`, dan `anthropic-ratelimit-output-tokens-reset`) dalam respons. Kelola pembatasan laju melalui alat pemantauan Azure sebagai gantinya.

### Kesalahan model dan penyebaran

**Error:** `Model not found` atau `Deployment not found`

- **Solusi:** Verifikasi Anda menggunakan nama penyebaran yang benar. Jika Anda belum membuat penyebaran kustom, gunakan ID model default (misalnya, `claude-sonnet-4-6`).
- **Solusi:** Pastikan model/penyebaran tersedia di wilayah Azure Anda.

**Error:** `Invalid model parameter`

- **Solusi:** Parameter model harus berisi nama penyebaran Anda, yang dapat disesuaikan di portal Foundry. Verifikasi penyebaran ada dan dikonfigurasi dengan benar.

<Info>
[Claude Mythos Preview](https://anthropic.com/glasswing) adalah pratinjau penelitian yang tersedia untuk pelanggan yang diundang di Microsoft Foundry. Untuk informasi lebih lanjut, lihat [Project Glasswing](https://anthropic.com/glasswing).
</Info>

## Sumber daya tambahan

- **Dokumentasi Foundry:** [ai.azure.com/catalog](https://ai.azure.com/catalog/publishers/anthropic)
- **Harga Azure:** [azure.microsoft.com/en-us/pricing](https://azure.microsoft.com/en-us/pricing/)
- **Detail harga Anthropic:** [Dokumentasi Harga](/docs/id/about-claude/pricing#third-party-platform-pricing)
- **Panduan autentikasi:** Lihat [bagian autentikasi](#authentication) di atas
- **Portal Azure:** [portal.azure.com](https://portal.azure.com/)