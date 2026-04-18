---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock-research-preview
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 7c33a2ec5f416a1d79d103c19119ab1a6e03d7135d54ca39e920572898717e64
---

# Claude di Amazon Bedrock

Akses model Claude melalui Amazon Bedrock dengan autentikasi asli AWS, penagihan, dan batas keamanan.

---

Panduan ini memandu Anda melalui pengaturan dan pembuatan panggilan API ke Claude di Amazon Bedrock. Claude di Amazon Bedrock berjalan pada infrastruktur yang dikelola AWS tanpa akses operator (personel Anthropic tidak memiliki akses ke infrastruktur inferensi), memungkinkan Anda membangun aplikasi sensitif sepenuhnya di dalam batas keamanan AWS sambil menggunakan bentuk Messages API yang sama yang Anda gunakan dengan API pihak pertama Anthropic.

<Note>
Halaman ini mencakup penawaran Claude di Amazon Bedrock yang baru, yang mengekspos Messages API di `/anthropic/v1/messages`. Untuk integrasi Bedrock warisan (API `InvokeModel` dengan pengenal model versi ARN dan pengkodean aliran peristiwa AWS), lihat [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock).
</Note>

## Pratinjau penelitian

Claude di Amazon Bedrock berada dalam pratinjau penelitian, tersedia di wilayah US East (N. Virginia) `us-east-1` saat peluncuran. Hubungi eksekutif akun Anthropic Anda untuk meminta akses.

## Prasyarat

Sebelum Anda memulai, pastikan Anda memiliki:

- **Akun AWS baru** di `us-east-1`. Pratinjau penelitian memerlukan akun khusus untuk isolasi. Eksekutif akun Anthropic Anda akan mengirimkan ID akun Anda ke tim Bedrock Marketplace untuk daftar putih (biasanya diproses dalam 24 jam).
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) diinstal dan dikonfigurasi (opsional, untuk manajemen kredensial)
- Setelah daftar putih, AWS mengirimkan email sambutan dengan ID model Anda dan detail pengaturan tambahan.

## Autentikasi

Claude di Amazon Bedrock mendukung tiga jalur autentikasi. Pilih yang paling sesuai dengan persyaratan keamanan Anda.

### Peran layanan Bedrock (direkomendasikan)

Gunakan peran layanan Bedrock dengan kunci yang dikelola AWS untuk akses jangka panjang yang paling aman:

<Steps>
<Step title="Admin: menyediakan peran layanan">
Administrator AWS menyediakan peran layanan Bedrock dan memberikan izin `iam:PassRole` kepada pengembang pada ARN peran layanan.
</Step>
<Step title="Developer: lewatkan peran">
Saat memanggil API, lewatkan ARN peran layanan sebagai parameter permintaan. Bedrock mengasumsikan peran atas nama Anda dan menandatangani permintaan dengan kredensial yang dikelola AWS. Contoh kode yang menunjukkan di mana parameter ARN berada akan ditambahkan ketika paket SDK dipublikasikan.
</Step>
</Steps>

### Peran yang diasumsikan IAM

Untuk akses yang difederasikan identitas dengan sesi maksimal 12 jam:

<Steps>
<Step title="Admin: konfigurasi peran IAM">
Buat peran IAM yang dibatasi pada model Claude Anda. Kebijakan kepercayaan menamai penyedia identitas Anda (SAML, OIDC, atau AWS Identity Center). Kebijakan izin memberikan `bedrock-mantle:CreateInference` hanya pada ARN model yang diizinkan.
</Step>
<Step title="Developer: autentikasi dan asumsikan">
Autentikasi melalui penyedia identitas perusahaan Anda, kemudian asumsikan peran IAM. AWS STS mengeluarkan kredensial sementara yang digunakan SDK atau CLI untuk menandatangani permintaan.
</Step>
</Steps>

### Token pembawa

Untuk akses jangka pendek tanpa peran IAM (maksimal 12 jam, paling tidak disukai):

<Steps>
<Step title="Admin: batasi jenis token">
Blokir kunci jangka panjang dengan melampirkan kebijakan yang menolak `bedrock:CallWithBearerToken` kecuali kondisi `bedrock:BearerTokenType` cocok dengan token jangka pendek.
</Step>
<Step title="Developer: cetak token">
Gunakan CLI `aws-bedrock-token-generator` (tautan tertunda publikasi) untuk mencetak token pembawa. Lewatkan di header `x-api-key` pada setiap permintaan.
</Step>
</Steps>

## Instal SDK

[SDK klien](/docs/id/api/client-sdks) Anthropic mendukung Claude di Amazon Bedrock melalui paket atau modul khusus Bedrock.

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
implementation("com.anthropic:anthropic-java-bedrock:2.20.0")
```
</Tab>
<Tab title="Maven">
```xml
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>anthropic-java-bedrock</artifactId>
    <version>2.20.0</version>
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
gem "aws-sigv4"
```
</Tab>
</Tabs>

## Membuat permintaan pertama Anda

Titik akhir mengikuti pola `https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages`. Tidak seperti integrasi Bedrock warisan, titik akhir ini menggunakan streaming SSE standar dan bentuk badan permintaan yang sama dengan API pihak pertama Anthropic.

SDK menyelesaikan kredensial dan wilayah menggunakan urutan prioritas AWS standar: argumen konstruktor, kemudian variabel lingkungan (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_REGION`), kemudian file konfigurasi AWS dan rantai kredensial (SSO, peran yang diasumsikan, peran tugas ECS, IMDS).

<CodeGroup>

```bash Shell nocheck
curl https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages \
  --aws-sigv4 "aws:amz:us-east-1:bedrock-mantle" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "CLAUDE_MODEL_ID",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello, Claude"}
    ]
  }'
```

```python Python nocheck
from anthropic import AnthropicBedrockMantle

client = AnthropicBedrockMantle(aws_region="us-east-1")

message = client.messages.create(
    model="CLAUDE_MODEL_ID",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)

print(message.content[0].text)
```

```typescript TypeScript nocheck
import AnthropicBedrockMantle from "@anthropic-ai/bedrock-sdk";

const client = new AnthropicBedrockMantle({
  awsRegion: "us-east-1",
});

const message = await client.messages.create({
  model: "CLAUDE_MODEL_ID",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
});

const block = message.content[0];
if (block.type === "text") {
  console.log(block.text);
}
```

```csharp C# nocheck
using Anthropic.Bedrock;
using Anthropic.Models.Messages;

var client = new AnthropicBedrockMantleClient(region: "us-east-1");

var message = await client.Messages.Create(new()
{
    Model = "CLAUDE_MODEL_ID",
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
});

if (message.Content[0].Value is TextBlock block)
    Console.WriteLine(block.Text);
```

```go Go nocheck hidelines={1..2,11..12,-1}
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/bedrock"
	"github.com/aws/aws-sdk-go-v2/config"
)

func main() {
	client := anthropic.NewClient(
		bedrock.WithLoadDefaultConfig(context.Background(), config.WithRegion("us-east-1")),
	)

	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:     "CLAUDE_MODEL_ID",
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
		},
	})
	if err != nil {
		panic(err)
	}

	fmt.Println(message.Content[0].Text)
}
```

```java Java nocheck hidelines={6..7,-1}
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
            .model("CLAUDE_MODEL_ID")
            .maxTokens(1024)
            .addUserMessage("Hello, Claude")
            .build()
    );

    IO.println(message.content().getFirst().asText().text());
}
```

```php PHP nocheck hidelines={1..2}
<?php

use Anthropic\Bedrock\MantleClient;

$client = MantleClient::fromEnvironment(region: 'us-east-1');

$message = $client->messages->create(
    model: 'CLAUDE_MODEL_ID',
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Hello, Claude'],
    ],
);

echo $message->content[0]->text;
```

```ruby Ruby nocheck
require "anthropic"

client = Anthropic::BedrockMantleClient.new(aws_region: "us-east-1")

message = client.messages.create(
  model: "CLAUDE_MODEL_ID",
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}]
)

puts message.content[0].text
```

</CodeGroup>

<Tip>
Jika klien khusus `AnthropicBedrockMantle` belum tersedia di rilis SDK bahasa Anda, Anda dapat menggunakan klien `Anthropic` standar sebagai gantinya: atur `base_url` ke `https://bedrock-mantle.{region}.api.aws/anthropic` dan lewatkan token pembawa Anda sebagai `api_key`. Jalur ini hanya mendukung autentikasi token pembawa. Penandatanganan SigV4 memerlukan klien khusus.
</Tip>

## Model yang didukung

ID model di Claude di Amazon Bedrock membawa awalan penyedia `anthropic.`. Kemampuan dan perilaku model didokumentasikan di halaman [Ikhtisar Model](/docs/id/about-claude/models/overview). Lihat email sambutan AWS Anda untuk ID model yang tepat yang diaktifkan untuk akun Anda.

## Ketersediaan fitur

Claude di Amazon Bedrock mendukung fitur yang berjalan di dalam model. Fitur yang memerlukan infrastruktur yang dioperasikan Anthropic tidak tersedia.

**Didukung:**

- Messages API (`/v1/messages`)
- Prompt caching
- Extended thinking
- Tool use (alat yang ditentukan klien)
- Citations
- Structured outputs
- In-region inference (permintaan tetap di satu wilayah AWS)

**Tidak didukung:**

- Alat yang ditentukan Anthropic (Web Search, Web Fetch, Remote MCP, Memory, Files API, Computer Use, Skills, Code Execution)
- Agent API
- Message Batches API
- Titik akhir `/v1/users`

## Wilayah

Pratinjau penelitian tersedia di `us-east-1` (IAD) saja.

## Kuota

Kuota default adalah 2 juta token input per menit (TPM). Anda dapat meminta hingga 4 juta TPM input tanpa persetujuan Anthropic tambahan. AWS memberlakukan batas permintaan per menit (RPM) di sisi Bedrock; hubungi dukungan AWS untuk penyesuaian RPM.

## Retensi data

Semua data inferensi disimpan selama 30 hari di penyimpanan AWS Anda. Tidak ada opsi retensi data nol pada penawaran ini. Untuk pelanggan standar, Anthropic dapat memeriksa data yang disimpan untuk tinjauan keselamatan dan penyalahgunaan. Untuk pelanggan tingkat Select, hanya AWS yang dapat memeriksa data; Anthropic dapat menjalankan operasi otomatis tetapi tidak tinjauan manual. Untuk detail tentang kelayakan tingkat Select, hubungi eksekutif akun Anthropic Anda.

## Observabilitas

Claude di Amazon Bedrock mengirimkan log ke CloudWatch dan CloudTrail. Anthropic merekomendasikan mempertahankan log aktivitas setidaknya pada basis rolling 30 hari untuk memahami pola penggunaan dan menyelidiki potensi masalah.

## Dukungan

Untuk dukungan pratinjau penelitian, hubungi **bedrock-ant-eap@amazon.com**. Sertakan ID akun AWS Anda dan `request-id` dari respons API yang gagal.