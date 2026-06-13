---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: e5cac346171bc31c92f7179e1634a83464a443776f29e5c239ac8eca364331b7
---

# Claude Platform di AWS

Akses kemampuan platform Claude secara penuh melalui AWS dengan infrastruktur yang dikelola Anthropic.

---

Claude Platform di AWS memberi Anda pengalaman platform Anthropic secara penuh, termasuk Messages API, Agent Skills, eksekusi kode, dan fitur beta, yang dapat diakses melalui akun AWS Anda. Berbeda dengan [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), di mana AWS mengoperasikan stack inferensi, Anthropic mengoperasikan Claude Platform di AWS. AWS menyediakan lapisan autentikasi (SigV4 atau kunci API), kontrol akses berbasis IAM, dan integrasi penagihan melalui AWS Marketplace.

<Note>
SDK Anthropic mendukung Claude Platform di AWS.
</Note>

## Cara kerja integrasi platform \{#how-the-platform-integration-works}

Model Claude berjalan pada infrastruktur yang dikelola Anthropic. Ini adalah integrasi komersial untuk penagihan dan akses melalui AWS. Anthropic adalah pemroses data untuk input dan output inferensi; AWS memproses metadata penagihan dan identitas di bawah model marketplace. Pelanggan yang menggunakan Claude melalui Claude Platform di AWS tunduk pada [ketentuan penggunaan data](https://www.anthropic.com/legal) Anthropic. Anthropic terus memberikan komitmen keamanan dan data terdepan di industri.

Perhatikan karakteristik operasional berikut: data mungkin tidak berada di AWS; inferensi dapat dirutekan ke cloud utama Anthropic; dan sublayanan dapat berpindah di balik layar tanpa pemberitahuan. Atur parameter [`inference_geo`](#data-residency) per permintaan untuk menyematkan inferensi ke geografi tertentu.

Claude Platform di AWS mengikuti kebijakan retensi data yang sama dengan Claude API pihak pertama. Zero Data Retention (ZDR) tersedia berdasarkan permintaan. Hubungi perwakilan akun Anthropic Anda untuk mengaktifkannya bagi organisasi Anda.

## Claude Platform di AWS vs Amazon Bedrock \{#claude-platform-on-aws-vs-amazon-bedrock}

Kedua penawaran ini memungkinkan Anda menggunakan Claude melalui AWS, tetapi keduanya berbeda secara signifikan dalam arsitektur, permukaan API, dan ketersediaan fitur.

| Aspek | Claude Platform di AWS | [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) | [Amazon Bedrock (legacy)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) |
| :--- | :--- | :--- | :--- |
| **Siapa yang mengoperasikan stack** | Anthropic | AWS | AWS |
| **Permukaan API** | Claude API (`/v1/{endpoint}`) | Messages API di `/anthropic/v1/messages` | Bedrock Converse / InvokeModel |
| **Ketersediaan fitur** | Biasanya pada hari yang sama dengan Claude API (lihat [keterbatasan fitur](#features-not-supported)) | Sesuai jadwal rilis Amazon Bedrock | Sesuai jadwal rilis Amazon Bedrock |
| **Agent Skills** | Tersedia (beta) | Tidak tersedia (memerlukan eksekusi kode) | Tidak tersedia |
| **Fitur beta** | Diteruskan dengan header `anthropic-beta` (lihat [keterbatasan fitur](#features-not-supported)) | Header `anthropic-beta` tidak didukung | Header `anthropic-beta` tidak didukung |
| **Autentikasi** | AWS IAM / SigV4 atau kunci API | AWS IAM / SigV4 | AWS IAM / SigV4 atau bearer token |
| **Penagihan** | AWS Marketplace | AWS (layanan native) | AWS (layanan native) |
| **Base URL** | `aws-external-anthropic.{region}.api.aws` | `bedrock-mantle.{region}.api.aws` | `bedrock-runtime.{region}.amazonaws.com` |
| **Klien SDK** | Kelas klien khusus platform (misalnya, `AnthropicAWS` di Python), dalam beta | `AnthropicBedrockMantle` | `AnthropicBedrock` / Bedrock SDK |
| **Konsol** | Claude Console (`platform.claude.com`, akses melalui AWS Console) | Bedrock Console | Bedrock Console |
| **Batas laju dan kuota** | Dikelola oleh Anthropic | Dikelola oleh AWS | Dikelola oleh AWS |
| **Pemroses data inferensi** | Anthropic | AWS | AWS |

Jika Anda membutuhkan Claude yang dioperasikan AWS, lihat [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock). Claude Platform di AWS menggunakan pool kapasitas terpisah dari Claude API pihak pertama maupun Amazon Bedrock. Anda dapat menjalankan beban kerja di lebih dari satu platform dan melakukan failover di antara keduanya.

[AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) didukung untuk menghubungkan VPC Anda ke endpoint Claude Platform di AWS.

**Kapan memilih Bedrock:** Organisasi di industri yang diregulasi yang memerlukan kepatuhan FedRAMP High, IL4, IL5, atau HIPAA-ready, atau yang membutuhkan AWS sebagai satu-satunya pemroses data, sebaiknya menggunakan [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock). Bedrock berjalan sepenuhnya pada infrastruktur yang dikontrol AWS dengan AWS sebagai pihak yang mengoperasikan.

## Menyiapkan akun Anda \{#set-up-your-account}

Penyiapan Claude Platform di AWS terjadi dalam empat fase: mendaftar di halaman layanan AWS Console, menyelesaikan penyiapan organisasi Anthropic Anda, mencatat ID workspace Anda, dan masuk ke Claude Console.

<Note>
Mendaftar melalui AWS Console akan menyediakan organisasi Anthropic baru yang terikat dengan akun AWS Anda. Organisasi ini terpisah dari organisasi yang sudah ada yang dimiliki perusahaan Anda dengan Anthropic, termasuk organisasi Claude Enterprise yang diperoleh melalui AWS Marketplace. Kunci API, workspace, dan pengaturan Claude Console dari organisasi Anthropic pihak pertama tidak terbawa.

Jika Anda memiliki private offer Amazon Bedrock yang sudah ada, hubungi perwakilan akun Anthropic atau AWS Anda sebelum mendaftar agar diskon Anda berlaku sejak permintaan pertama. Diskon tidak dapat diterapkan secara retroaktif pada penggunaan yang terjadi sebelum private offer Anda diterima. Lihat [Private offer](/docs/id/about-claude/pricing#private-offers).
</Note>

<Steps>
<Step title="Mendaftar di AWS Console">
1. Buka [AWS Console](https://console.aws.amazon.com/) dan navigasikan ke halaman layanan **Claude Platform on AWS**.
2. Pilih **Sign up**.
3. Pada halaman Sign-up, tinjau ketentuan (End User License Agreement Anthropic, AWS Privacy Notice, dan AWS Customer Agreement) dan centang kotak persetujuan.
4. Pilih **Continue**.

Halaman menampilkan banner **Sign-up in progress**. Tetap di halaman tersebut. Pendaftaran memerlukan beberapa menit sementara AWS menangani langganan AWS Marketplace untuk Anda, kemudian mengalihkan Anda secara otomatis.

Jika organisasi Anda memiliki private offer dari Anthropic, Console akan mencarinya dan meminta Anda untuk menerimanya di AWS Marketplace. Lihat [Private offer](/docs/id/about-claude/pricing#private-offers) untuk detailnya.

<Note>
Jika Anda menggunakan Claude Platform di AWS, konten Anda (seperti prompt dan completion) diproses oleh Anthropic di luar AWS. Lihat [kebijakan penggunaan data](https://www.anthropic.com/legal) Anthropic untuk detail tentang bagaimana konten dan metadata diproses dan disimpan.
</Note>
</Step>

<Step title="Menyiapkan organisasi Anthropic Anda">
Setelah pendaftaran selesai, Anda dialihkan ke `platform.claude.com/partner-signup`.

1. Masukkan alamat email pemilik organisasi Anda dan pilih **Get started**.
2. Periksa kotak masuk email tersebut untuk tautan penyiapan dan ikuti tautannya. Jika browser Anda menampilkan halaman **Signed in as a different account**, pilih **Log out and continue**.
3. Lengkapi formulir detail organisasi (nama organisasi, jenis entitas, negara, tujuan penggunaan) dan pilih **Complete setup**.

Menyelesaikan penyiapan akan membuat organisasi Anthropic Anda dan menerima Commercial Terms of Service dan Usage Policy Anthropic. Halaman layanan AWS Console sekarang menampilkan navigasi kiri dengan **Home**, **API keys**, **Quickstart**, dan **Workspaces**.
</Step>

<Step title="Membuat workspace Anda dan mencatat ID-nya">
Setelah Anda menyelesaikan penyiapan, AWS Console meminta Anda untuk membuat workspace. Lihat [Workspace](#workspaces) untuk detail tentang pengikatan region, penentuan cakupan resource IAM, dan pembuatan workspace tambahan.

Temukan ID workspace di bawah **Workspaces** pada halaman layanan **Claude Platform on AWS** di AWS Console atau di [Claude Console](#using-the-claude-console). ID workspace menggunakan format `wrkspc_` diikuti oleh pengidentifikasi alfanumerik.
</Step>

<Step title="Masuk ke Claude Console">
Akses ke Claude Console difederasikan melalui AWS IAM:

1. Asumsikan peran IAM dengan izin `aws-external-anthropic:AssumeConsole`. Lihat [Tindakan IAM untuk Claude Platform di AWS](/docs/id/api/claude-platform-on-aws-iam-actions#console-access).
2. Dari halaman layanan **Claude Platform on AWS**, pilih **Open Claude Console**. AWS Console menerbitkan JWT dan mengalihkan Anda ke `platform.claude.com`.
3. Pada saat masuk pertama kali, Anda diminta memasukkan alamat email. Masukkan email kerja Anda. Platform menyediakan pengguna Claude Console Anda secara just-in-time.

Ketika Anda masuk melalui AWS Console, Claude Console dicakupkan ke organisasi Claude Platform di AWS Anda. Indikator **Account managed by AWS** muncul di kiri bawah sidebar Claude Console.
</Step>
</Steps>

### Pemecahan masalah penyiapan akun \{#troubleshooting-account-setup}

- **"Sign-up failed: Failed to enable OutboundWebIdentityFederation":** Jika Anda melihat banner ini pada pengiriman pertama, pilih **Continue** lagi. Pengaktifan IAM dapat memerlukan waktu sejenak untuk berlaku.
- **Tidak ada indikator progres selama pendaftaran:** Pendaftaran memerlukan beberapa menit. Halaman menampilkan banner statis **Sign-up in progress** tanpa bilah progres sementara AWS menyediakan akun Anda.
- **"Signed in as a different account" setelah mengikuti tautan penyiapan:** Pilih **Log out and continue**. Halaman akan mengautentikasi ulang Anda dengan alamat email yang Anda masukkan.
- **Pesan "Not found" selama masuk:** Pesan ini mungkin muncul sebentar selama pengalihan. Anda dapat mengabaikannya.
- **Halaman Usage tidak menampilkan data setelah panggilan API pertama Anda:** Data penggunaan dapat memerlukan beberapa menit untuk muncul di Claude Console.

## Sebelum melakukan panggilan API \{#before-making-api-calls}

Pastikan Anda memiliki:

1. Akun AWS aktif dengan langganan ke Claude Platform di AWS (lihat [Menyiapkan akun Anda](#set-up-your-account))
2. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) terinstal dan terkonfigurasi
3. **Outbound web identity federation diaktifkan** pada akun AWS Anda (langkah penyiapan satu kali; lihat [Mengaktifkan outbound web identity federation](#enable-outbound-web-identity-federation))
4. ID workspace Anda (lihat [Mendapatkan ID workspace Anda](#obtain-your-workspace-id))

### Mengaktifkan outbound web identity federation \{#enable-outbound-web-identity-federation}

Gateway Claude Platform di AWS memanggil `sts:GetWebIdentityToken` di sisi server untuk membuat JWT yang diteruskan ke Anthropic. Kemampuan STS ini **dinonaktifkan secara default** pada setiap akun AWS. Aktifkan sekali per akun:

```bash CLI
aws iam enable-outbound-web-identity-federation
```

Jika responsnya adalah `[ERROR] (FeatureEnabled) ... already enabled`, pengaturan tersebut sudah aktif untuk akun Anda dan Anda dapat melanjutkan. Verifikasi dan ambil URL issuer akun Anda:

```bash CLI
aws iam get-outbound-web-identity-federation-info
```

<Warning>
Tanpa langkah ini, setiap permintaan mengembalikan `"Outbound web identity federation is disabled for your account"`. Ini adalah kesalahan penyiapan yang paling umum.
</Warning>

### Mendapatkan ID workspace Anda \{#obtain-your-workspace-id}

Anda membuat workspace dari AWS Console setelah menyelesaikan penyiapan akun (lihat [Menyiapkan akun Anda](#set-up-your-account)). Workspace terikat pada satu region AWS. Anda dapat menemukan ID workspace di [Claude Console](#using-the-claude-console) di bawah **Workspaces** atau di bagian **Workspaces** pada halaman layanan AWS Console.

Atur variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID` dan `AWS_REGION` agar klien SDK membacanya secara otomatis:

```bash CLI
export ANTHROPIC_AWS_WORKSPACE_ID='wrkspc_01AbCdEf23GhIj'
export AWS_REGION='us-west-2'  # Your workspace's AWS region
```

Region wajib diisi. Klien SDK memunculkan error jika tidak ada region yang diatur. Teruskan `aws_region`/`awsRegion` ke konstruktor, atau atur `AWS_REGION` (atau `AWS_DEFAULT_REGION`). Semua region komersial AWS didukung.

## Autentikasi \{#authentication}

Claude Platform di AWS mendukung dua metode autentikasi: AWS IAM dengan penandatanganan permintaan SigV4 (utama) dan autentikasi kunci API. Keduanya menggunakan base URL dan format permintaan yang sama.

### Autentikasi SigV4 \{#sig-v4-authentication}

SigV4 adalah jalur enterprise-native dan terintegrasi dengan kebijakan, peran, dan audit AWS IAM Anda yang sudah ada. Konfigurasikan kredensial AWS menggunakan metode apa pun yang didukung oleh [rantai penyedia kredensial default AWS](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html):

- Variabel lingkungan (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`)
- File kredensial bersama (`~/.aws/credentials`)
- File konfigurasi bersama (`~/.aws/config`) termasuk SSO dan `credential_process`
- Web identity (`AWS_WEB_IDENTITY_TOKEN_FILE` dan `AWS_ROLE_ARN`) untuk IRSA dan GitHub Actions
- Kredensial kontainer ECS
- Layanan metadata instans EC2 (IMDS)

Verifikasi bahwa kredensial Anda berfungsi:

```bash CLI
aws sts get-caller-identity
```

### Autentikasi kunci API \{#api-key-authentication}

Untuk jalur integrasi yang lebih sederhana (pengembangan lokal dan skrip), Anda dapat mengautentikasi dengan kunci API alih-alih SigV4. Atur variabel lingkungan `ANTHROPIC_AWS_API_KEY` atau teruskan `apiKey` ke konstruktor SDK.

Buat kunci API di **AWS Console** di bawah **Claude Platform on AWS → API keys**. Pilih **Generate a key**, lalu salin nilai kunci tersebut. Berikan tindakan IAM `aws-external-anthropic:CallWithBearerToken` kepada principal yang diizinkan menggunakan autentikasi kunci API.

<Note>
Kunci API untuk Claude Platform di AWS dikelola di AWS Console, bukan Claude Console. Kunci yang dibuat di [Claude Console](https://platform.claude.com/) standar (untuk akses API pihak pertama) tidak berfungsi dengan endpoint Claude Platform di AWS.
</Note>

#### Kunci API jangka pendek \{#short-term-api-keys}

Untuk beban kerja yang perlu menyerahkan kredensial ke proses terpisah (seperti gateway LLM, fungsi serverless, atau alat yang mendukung autentikasi bearer-token tetapi tidak SigV4), buat kunci API jangka pendek dari kredensial AWS Anda alih-alih menyediakan kunci berumur panjang di AWS Console.

AWS menerbitkan pustaka token-generator untuk [JavaScript](https://github.com/aws/token-generator-for-aws-external-anthropic-js), [Python](https://github.com/aws/token-generator-for-aws-external-anthropic-python), dan [Java](https://github.com/aws/token-generator-for-aws-external-anthropic-java). Setiap pustaka membaca kredensial AWS Anda melalui rantai penyedia standar dan mengembalikan token dengan batas waktu yang berfungsi dengan header `x-api-key`. Masa berlaku token secara default adalah 12 jam dan dibatasi pada nilai terkecil di antara durasi yang Anda minta, masa berlaku kredensial AWS Anda, dan 12 jam. Lihat README repositori yang ditautkan untuk instalasi dan opsi konfigurasi lengkap.

Teruskan token yang dihasilkan ke SDK dengan cara yang sama seperti Anda meneruskan kunci API yang dibuat di AWS Console:

<CodeGroup>

```python Python nocheck
from token_generator_for_aws_external_anthropic import TokenGenerator
from anthropic import AnthropicAWS

token = TokenGenerator(region="us-west-2").get_token()

client = AnthropicAWS(api_key=token, aws_region="us-west-2")
```

```typescript TypeScript nocheck
import { getTokenProvider } from "@aws/token-generator-for-aws-external-anthropic";
import AnthropicAws from "@anthropic-ai/aws-sdk";

const tokenProvider = getTokenProvider({ region: "us-west-2" });
const token = await tokenProvider();

const client = new AnthropicAws({ apiKey: token, awsRegion: "us-west-2" });
```

```java Java nocheck
import software.amazon.awsexternalanthropic.TokenGenerator;
import software.amazon.awssdk.regions.Region;
import com.anthropic.aws.backends.AwsBackend;
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

void main() {
    String token = TokenGenerator.builder().region(Region.US_WEST_2).build().getToken();

    AnthropicClient client = AnthropicOkHttpClient.builder()
        .backend(AwsBackend.builder()
            .apiKey(token)
            .region(Region.US_WEST_2)
            .workspaceId(System.getenv("ANTHROPIC_AWS_WORKSPACE_ID"))
            .build())
        .build();
}
```
</CodeGroup>

Jika Anda dapat membuat token secara lokal, proses Anda sudah memiliki kredensial SigV4, dan autentikasi SigV4 biasanya merupakan pilihan yang lebih sederhana. Gunakan kunci jangka pendek ketika proses yang melakukan panggilan API terpisah dari proses yang menyimpan kredensial AWS.

SDK tidak menyegarkan kunci jangka pendek secara otomatis. Ketika token kedaluwarsa, buat yang baru dan konstruksi klien baru. Principal yang menggunakan token tersebut tetap memerlukan tindakan IAM `aws-external-anthropic:CallWithBearerToken`.

### Prioritas kredensial \{#credential-precedence}

Klien khusus platform menyelesaikan autentikasi dalam urutan berikut. Nama argumen bervariasi menurut konvensi bahasa (TypeScript dan PHP menggunakan camelCase seperti yang ditunjukkan; Python dan Ruby menggunakan snake_case; Go menggunakan PascalCase dengan akronim berhuruf kapital; C# dan Java menggunakan idiom properti atau builder bahasa tersebut).

1. Argumen konstruktor `apiKey` → header `x-api-key`
2. Argumen konstruktor `awsAccessKey` + `awsSecretAccessKey` → AWS SigV4
3. Argumen konstruktor `awsProfile` → AWS SigV4 dengan profil bernama
4. Variabel lingkungan `ANTHROPIC_AWS_API_KEY` → header `x-api-key`
5. Rantai penyedia kredensial AWS default → AWS SigV4

### Resolusi region \{#region-resolution}

Klien membaca `AWS_REGION` dari lingkungan jika `aws_region`/`awsRegion` tidak diteruskan ke konstruktor, dengan fallback ke `AWS_DEFAULT_REGION` untuk kompatibilitas dengan SDK AWS standar. Region wajib diisi; tidak ada default fallback. Berbeda dengan `AnthropicBedrock`, yang melakukan fallback ke `us-east-1`, klien `AnthropicAWS`/`AnthropicAws` memunculkan error jika baik argumen konstruktor maupun variabel lingkungan tidak diatur.

## Menginstal SDK \{#install-an-sdk}

[SDK klien](/docs/id/cli-sdks-libraries/overview) Anthropic mendukung Claude Platform di AWS. Setiap SDK menyediakan kelas klien khusus platform yang menangani penandatanganan SigV4, konstruksi base URL berbasis region, dan header `anthropic-workspace-id`.

<Tabs>
<Tab title="Python">
```bash
pip install -U "anthropic[aws]"
```

<Tip>
Pada macOS dengan Homebrew Python atau lingkungan Python lain yang dikelola secara eksternal, `pip install` dapat gagal dengan error PEP 668 `externally-managed-environment`. Buat dan aktifkan virtual environment terlebih dahulu: `python3 -m venv .venv && source .venv/bin/activate`.
</Tip>
</Tab>

<Tab title="TypeScript">
```bash
npm install @anthropic-ai/aws-sdk
```
</Tab>

<Tab title="C#">
```bash
dotnet add package Anthropic.Aws
```
</Tab>

<Tab title="Go">
```bash
go get github.com/anthropics/anthropic-sdk-go
```
</Tab>

<Tab title="Java">
```kotlin Gradle
implementation("com.anthropic:anthropic-java-aws:2.40.0")
```

```xml Maven
<dependency>
  <groupId>com.anthropic</groupId>
  <artifactId>anthropic-java-aws</artifactId>
  <version>2.40.0</version>
</dependency>
```
</Tab>

<Tab title="PHP">
```bash
composer require anthropic-ai/sdk aws/aws-sdk-php
```
</Tab>

<Tab title="Ruby">
```bash
gem install anthropic aws-sdk-core
```
</Tab>
</Tabs>

<Note>
Klien SDK untuk Claude Platform di AWS masih dalam beta.
</Note>

## Model yang tersedia \{#available-models}

Model berikut tersedia di Claude Platform di AWS:

| Model | ID Model |
| :--- | :--- |
| Claude Fable 5 | claude-fable-5 |
| Claude Opus 4.8 | claude-opus-4-8 |
| Claude Opus 4.7 | claude-opus-4-7 |
| Claude Opus 4.6 | claude-opus-4-6 |
| Claude Sonnet 4.6 | claude-sonnet-4-6 |
| Claude Opus 4.5 | claude-opus-4-5 |
| Claude Sonnet 4.5 | claude-sonnet-4-5 |
| Claude Haiku 4.5 | claude-haiku-4-5 |

ID model identik dengan Claude API pihak pertama. Tidak ada ARN bergaya Bedrock atau prefiks `anthropic.`.

Model baru diluncurkan di Claude Platform di AWS secara bersamaan dengan Claude API pihak pertama.

<Tip>
Melakukan upgrade ke model Claude yang lebih baru? Di Claude Code, jalankan `/claude-api migrate` untuk menerapkan penggantian ID model dan perubahan parameter yang bersifat breaking di seluruh codebase Anda. Skill ini mendeteksi platform cloud mana yang ditargetkan oleh kode Anda dan menyesuaikan format ID model serta perubahan fitur untuk platform tersebut. Lihat [Migrasi ke model Claude yang lebih baru](/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

## Membuat permintaan \{#making-requests}

Claude Platform di AWS menggunakan endpoint API yang sama dengan Claude API pihak pertama. Perbedaannya adalah base URL, metode autentikasi, dan header `anthropic-workspace-id` yang wajib yang mengidentifikasi [workspace](#workspaces) mana yang ditargetkan oleh permintaan.

<CodeGroup>

```bash cURL nocheck
# Ganti us-west-2 dengan region AWS Anda di URL dan --aws-sigv4
curl "https://aws-external-anthropic.us-west-2.api.aws/v1/messages" \
  --aws-sigv4 "aws:amz:us-west-2:aws-external-anthropic" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-workspace-id: $ANTHROPIC_AWS_WORKSPACE_ID" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

```python Python nocheck
from anthropic import AnthropicAWS

client = AnthropicAWS()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)
print(message)
```

```typescript TypeScript nocheck
import AnthropicAws from "@anthropic-ai/aws-sdk";

const client = new AnthropicAws();

const message = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }]
});
console.log(message);
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Aws;

var client = new AnthropicAwsClient();

var message = await client.Messages.Create(new()
{
    Model = Model.ClaudeSonnet4_6,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Hello!" }]
});

Console.WriteLine(message);
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	anthropicaws "github.com/anthropics/anthropic-sdk-go/aws"
)

func main() {
	client, err := anthropicaws.NewClient(context.Background(), anthropicaws.ClientConfig{})
	if err != nil {
		panic(err)
	}

	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
		},
	})
	if err != nil {
		panic(err)
	}

	fmt.Println(message)
}
```

```java Java nocheck
import com.anthropic.aws.backends.AwsBackend;
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.builder()
        .backend(AwsBackend.fromEnv())
        .build();

    Message message = client.messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(1024)
            .addUserMessage("Hello!")
            .build()
    );

    IO.println(message);
}
```

```php PHP nocheck hidelines={1}
<?php
use Anthropic\Aws\Client;

$client = new Client();

$message = $client->messages->create(
    model: 'claude-sonnet-4-6',
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello!']],
);

echo $message;
```

```ruby Ruby nocheck
require "anthropic"

client = Anthropic::AWSClient.new

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }]
)

puts message
```
</CodeGroup>

Klien membaca `AWS_REGION` (atau `AWS_DEFAULT_REGION`) dan `ANTHROPIC_AWS_WORKSPACE_ID` dari lingkungan. Anda dapat menimpa salah satunya dengan meneruskan `aws_region` / `awsRegion` atau `workspace_id` / `workspaceId` ke konstruktor. Baik region maupun ID workspace wajib diisi. Konstruktor memunculkan error jika ID workspace tidak dapat diselesaikan; region yang hilang juga memunculkan error.

<Note>
Header `x-amz-security-token` (cURL) hanya diperlukan untuk kredensial sementara seperti peran IAM, SSO, atau STS. Hilangkan header tersebut saat menggunakan kredensial pengguna IAM jangka panjang. Klien SDK menangani ini secara otomatis berdasarkan sumber kredensial.
</Note>

Nilai `--aws-sigv4` mengikuti format `aws:amz:<region>:<service>`. Nama layanan SigV4 adalah `aws-external-anthropic`, dan region harus cocok dengan region di URL endpoint Anda. Ketidakcocokan pada salah satunya menghasilkan error penolakan tanda tangan generik alih-alih diagnostik spesifik.

### Jendela konteks \{#context-window}

Ukuran "context window" (jendela konteks) di Claude Platform di AWS identik dengan Claude API pihak pertama. Lihat [Jendela konteks](/docs/id/build-with-claude/context-windows) untuk batas per model.

## Dukungan fitur \{#feature-support}

Claude Platform di AWS menggunakan endpoint Claude API secara langsung, yang berarti Anda mendapatkan paritas fitur penuh dengan Claude API pihak pertama (kecuali yang disebutkan dalam [keterbatasan fitur](#features-not-supported)):

- **Akses fitur:** Karena Anthropic mengoperasikan kedua platform, sebagian besar fitur baru dan header beta tersedia di Claude Platform di AWS tanpa langkah integrasi terpisah. Lihat [keterbatasan fitur](#features-not-supported) untuk pengecualian.
- **Fitur beta:** Teruskan header `anthropic-beta` standar untuk mengakses fitur beta, sama seperti yang Anda lakukan dengan Claude API.
- **Agent Skills:** Gunakan [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) bawaan dan kustom dengan parameter `container.skills` dan header beta yang sama seperti Claude API. Semua Skills bawaan (PowerPoint, Excel, Word, PDF) berfungsi langsung.
- **Eksekusi kode:** Jalankan kode di sandbox terkelola Anthropic menggunakan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool).
- **Penggunaan alat:** Computer use dan semua [kemampuan penggunaan alat](/docs/id/agents-and-tools/tool-use/overview) lainnya tersedia.
- **Pemikiran diperpanjang:** Aktifkan pemikiran diperpanjang dengan parameter yang sama seperti Claude API.
- **Streaming:** Dukungan streaming SSE penuh untuk respons real-time.
- **Pemrosesan batch:** Kirim permintaan batch untuk beban kerja throughput tinggi.
- **Caching prompt:** Cache alat, prompt sistem, dan riwayat pesan untuk mengurangi latensi dan biaya. Semua kemampuan caching prompt (TTL 5 menit, TTL 1 jam, dan caching otomatis) tersedia.
- **Files API:** Unggah dan referensikan file di seluruh permintaan.
- **Customer-managed encryption keys (CMEK):** [CMEK](/docs/id/manage-claude/cmek) tersedia hanya dengan kunci [AWS KMS](/docs/id/manage-claude/cmek-aws-kms); kunci Google Cloud KMS dan Azure Key Vault tidak dapat didaftarkan. Buat, validasi, dan lampirkan kunci di [Claude Console](#using-the-claude-console); endpoint Admin API `external_keys` saat ini tidak tersedia. Kunci harus berada di region AWS yang sama dengan workspace tempat kunci tersebut dilampirkan.
- **Compliance API:** [Compliance API](/docs/id/manage-claude/compliance-api) tersedia. Akses diotorisasi melalui AWS IAM.

Lihat [tabel perbandingan](#claude-platform-on-aws-vs-amazon-bedrock) untuk perbedaan ketersediaan fitur dari Amazon Bedrock.

### Claude Managed Agents \{#claude-managed-agents}

[Claude Managed Agents](/docs/id/managed-agents/overview) tersedia di Claude Platform di AWS, termasuk [agen](/docs/id/managed-agents/agent-setup), [environment](/docs/id/managed-agents/environments), [sesi](/docs/id/managed-agents/sessions), [credential vault](/docs/id/managed-agents/vaults), [memory store](/docs/id/managed-agents/memory), [webhook](/docs/id/managed-agents/webhooks), [orkestrasi multiagen](/docs/id/managed-agents/multi-agent), dan [sandbox self-hosted](/docs/id/managed-agents/self-hosted-sandboxes).

Perilaku sesi di Claude Platform di AWS berbeda dari Claude Managed Agents pihak pertama dalam satu hal:

- **Autentikasi ulang sesi otonom:** Sebuah sesi dapat berjalan secara otonom, tanpa [event pengguna](/docs/id/managed-agents/reference#event-types) apa pun, hingga 6 jam. Setelah 6 jam, sesi memerlukan autentikasi ulang sebelum dilanjutkan. Untuk mengautentikasi ulang, kirim event peran pengguna apa pun ke sesi (lihat [Event dan streaming](/docs/id/managed-agents/events-and-streaming)). Claude Managed Agents pihak pertama tidak memiliki batas runtime sesi otonom.

### Fitur yang tidak didukung \{#features-not-supported}

Kemampuan berikut saat ini tidak tersedia di Claude Platform di AWS:

- **Kesiapan HIPAA:** Program HIPAA-ready Anthropic tidak tersedia. Lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

- **Admin API:** Endpoint workspace (create, get, list, update, dan archive pada `/v1/organizations/workspaces`) tersedia. Endpoint Admin API lainnya (anggota organisasi, anggota workspace, undangan, kunci API, laporan penggunaan, laporan biaya, laporan batas laju, dan kunci eksternal) saat ini tidak tersedia. Kelola kunci [CMEK](/docs/id/manage-claude/cmek) di Claude Console sebagai gantinya. Lihat data penggunaan dan biaya di [Claude Console](#using-the-claude-console) sebagai gantinya. AWS IAM mengelola keanggotaan organisasi.
- **Manajemen anggota workspace:** Menambahkan atau menghapus pengguna dari workspace individual tidak tersedia. Kebijakan AWS IAM pada ARN workspace mengontrol akses.
- **Batas pengeluaran:** Tidak tersedia. Andalkan kontrol penagihan AWS sebagai gantinya.
- **Workspace Claude Code dan Analytics API:** Workspace Claude Code dengan batas laju otomatis tidak tersedia. Penggunaan Claude Code muncul di tampilan penggunaan umum alih-alih layar khusus.
- **Autentikasi OAuth:** Tidak didukung. Gunakan autentikasi SigV4 atau kunci API.
- **Fast mode:** Tidak tersedia di Claude Platform di AWS.
- **Endpoint API yang kompatibel dengan OpenAI:** Tidak tersedia di Claude Platform di AWS.
- **MCP tunnel:** Hanya server MCP yang diekspos melalui internet publik yang didukung.

## Residensi data \{#data-residency}

Claude Platform di AWS mendukung geografi inferensi berikut:

- **US:** Inferensi tetap berada di dalam pusat data AS. Pengali harga 1,1x berlaku.
- **Global:** Inferensi dapat dirutekan ke pusat data mana pun yang dioperasikan Anthropic di seluruh dunia. Harga standar berlaku.

<Note>
Region AWS tempat workspace Anda terikat mengontrol endpoint gateway mana yang Anda panggil dan di mana resource sisi AWS (IAM, CloudTrail, penagihan) dicakupkan. Ini tidak menyematkan di mana inferensi model berjalan. Untuk menyematkan inferensi ke geografi tertentu, atur `inference_geo` pada setiap permintaan atau konfigurasikan default workspace.
</Note>

Atur geografi inferensi per permintaan dengan parameter `inference_geo`:

<Note>
Parameter `inference_geo` didukung pada Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih baru. Permintaan dengan `inference_geo` pada Claude Opus 4.5, Claude Sonnet 4.5, atau Claude Haiku 4.5 mengembalikan error 400. Lihat [Residensi data](/docs/id/manage-claude/data-residency) untuk detail ketersediaan model.
</Note>

<CodeGroup>

```bash cURL nocheck
# Ganti us-west-2 dengan region AWS Anda di URL dan --aws-sigv4
curl "https://aws-external-anthropic.us-west-2.api.aws/v1/messages" \
  --aws-sigv4 "aws:amz:us-west-2:aws-external-anthropic" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-workspace-id: $ANTHROPIC_AWS_WORKSPACE_ID" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "inference_geo": "us",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

```python Python nocheck
from anthropic import AnthropicAWS

client = AnthropicAWS()
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    inference_geo="us",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(message)
```

```typescript TypeScript nocheck
import AnthropicAws from "@anthropic-ai/aws-sdk";
const client = new AnthropicAws();
const message = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  inference_geo: "us",
  messages: [{ role: "user", content: "Hello!" }]
});
console.log(message);
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Aws;

var client = new AnthropicAwsClient();

var message = await client.Messages.Create(new()
{
    Model = Model.ClaudeSonnet4_6,
    MaxTokens = 1024,
    InferenceGeo = "us",
    Messages = [new() { Role = Role.User, Content = "Hello!" }]
});

Console.WriteLine(message);
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	anthropicaws "github.com/anthropics/anthropic-sdk-go/aws"
)

func main() {
	client, err := anthropicaws.NewClient(context.Background(), anthropicaws.ClientConfig{})
	if err != nil {
		panic(err)
	}

	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:        anthropic.ModelClaudeSonnet4_6,
		MaxTokens:    1024,
		InferenceGeo: anthropic.String("us"),
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
		},
	})
	if err != nil {
		panic(err)
	}

	fmt.Println(message)
}
```

```java Java nocheck
import com.anthropic.aws.backends.AwsBackend;
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.builder()
        .backend(AwsBackend.fromEnv())
        .build();

    Message message = client.messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(1024)
            .inferenceGeo("us")
            .addUserMessage("Hello!")
            .build()
    );

    IO.println(message);
}
```

```php PHP nocheck hidelines={1}
<?php
use Anthropic\Aws\Client;

$client = new Client();

$message = $client->messages->create(
    model: 'claude-sonnet-4-6',
    maxTokens: 1024,
    inferenceGeo: 'us',
    messages: [['role' => 'user', 'content' => 'Hello!']],
);

echo $message;
```

```ruby Ruby nocheck
require "anthropic"

client = Anthropic::AWSClient.new

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  inference_geo: "us",
  messages: [{ role: "user", content: "Hello!" }]
)

puts message
```
</CodeGroup>

Jika Anda menghilangkan `inference_geo`, permintaan menggunakan `default_inference_geo` workspace jika dikonfigurasi, jika tidak maka `global`.

Kontrol geografi inferensi tingkat workspace (`allowed_inference_geos` dan `default_inference_geo`) juga tersedia di Claude Platform di AWS. Lihat [Pembatasan tingkat workspace](/docs/id/manage-claude/data-residency#workspace-level-restrictions).

## Workspace \{#workspaces}

Permintaan inferensi dan resource di Claude Platform di AWS menargetkan sebuah workspace. Anda meneruskan ID workspace dalam header `anthropic-workspace-id` pada panggilan API ini. ID workspace menggunakan format bertag `wrkspc_` diikuti oleh pengidentifikasi alfanumerik (misalnya, `wrkspc_01AbCdEf23GhIj`). Lihat [Mendapatkan ID workspace Anda](#obtain-your-workspace-id) jika Anda belum memilikinya.

### Cakupan workspace \{#workspace-scoping}

Workspace terikat pada satu region AWS. Workspace yang dibuat di `us-west-2` hanya dapat diakses melalui endpoint `us-west-2`. Penggunaan, kuota, biaya, file, batch, dan Skills semuanya diakumulasikan per workspace, memberi Anda rincian per region di Claude Console.

Workspace juga berfungsi sebagai resource IAM utama untuk Claude Platform di AWS. Anda memberikan atau menolak akses ke workspace tertentu melalui kebijakan AWS IAM menggunakan ARN workspace. Segmen resource ARN adalah ID berprefiks `wrkspc_` yang sama yang Anda teruskan dalam header `anthropic-workspace-id`:

```text
arn:aws:aws-external-anthropic:{region}:{account-id}:workspace/{workspace-id}
```

Misalnya:

```text
arn:aws:aws-external-anthropic:us-west-2:123456789012:workspace/wrkspc_01AbCdEf23GhIj
```

Lihat [Kebijakan IAM](#iam-policies) untuk contoh kebijakan.

### Mengelola workspace \{#managing-workspaces}

Buat workspace tambahan, ganti nama workspace, atau arsipkan workspace dari halaman **Workspaces** di AWS Console atau dengan endpoint workspace [Admin API](/docs/id/manage-claude/admin-api). Workspace baru terikat pada region AWS dari endpoint yang Anda panggil untuk membuatnya (lihat [Cakupan workspace](#workspace-scoping)). Halaman Workspaces di Claude Console bersifat read-only.

## Menggunakan Claude Console \{#using-the-claude-console}

Claude Platform di AWS menggunakan Claude Console standar di [platform.claude.com](https://platform.claude.com). Ketika Anda masuk dari AWS Console, indikator **Account managed by AWS** muncul di kiri bawah sidebar Claude Console dan Console dicakupkan ke organisasi Claude Platform di AWS Anda. Console menyediakan analitik penggunaan, rincian biaya, visibilitas batas laju, visibilitas workspace, dan halaman untuk mengelola file, Agent Skills, pekerjaan batch, dan resource Claude Managed Agents (agen, sesi, environment, credential vault, memory store, dan webhook).

### Masuk \{#signing-in}

Akses ke Claude Console difederasikan melalui AWS IAM. Lihat [Menyiapkan akun Anda](#set-up-your-account) untuk alur masuk pertama kali secara lengkap. Singkatnya:

1. Asumsikan peran IAM dengan izin `aws-external-anthropic:AssumeConsole`. Lihat [Tindakan IAM untuk Claude Platform di AWS](/docs/id/api/claude-platform-on-aws-iam-actions#console-access).
2. Navigasikan ke halaman Claude Platform on AWS di [AWS Console](https://console.aws.amazon.com/).
3. Pilih **Open Claude Console**. AWS Console menerbitkan JWT dan mengalihkan Anda ke `platform.claude.com`.
4. Pada saat masuk pertama kali, Anda diminta memasukkan alamat email; masukkan email kerja Anda. Platform menyediakan pengguna Claude Console Anda secara just-in-time.

Dua peran Claude Console tersedia: **Admin** dan **Developer**. Peran Admin memberikan akses ke semua halaman dan pengaturan Claude Console yang tersedia untuk Claude Platform di AWS. Peran Developer memberikan akses baca ke informasi penggunaan, biaya, batas laju, dan workspace. Hubungi perwakilan akun Anthropic Anda untuk menetapkan peran Admin atau Developer ke sebuah principal.

### Halaman yang tersedia \{#available-pages}

Kolom **Through AWS gateway** menunjukkan apakah halaman tersebut membaca dan menulis data melalui gateway AWS (dan karenanya diatur oleh [tindakan IAM](/docs/id/api/claude-platform-on-aws-iam-actions)). Halaman yang ditandai **No** membaca metadata tingkat organisasi langsung dari Anthropic dan melewati pemeriksaan tindakan IAM.

| Halaman | Tersedia | Melalui gateway AWS | Catatan |
| :--- | :--- | :--- | :--- |
| **Usage** | Ya | Tidak | Melihat penggunaan token berdasarkan model, workspace, dan dimensi. Data dapat memerlukan beberapa menit untuk muncul setelah permintaan. |
| **Cost** | Ya | Tidak | Melihat rincian biaya berdasarkan model dan workspace. AWS Cost Explorer menampilkan item baris [Claude Consumption Unit (CCU)](#billing) yang diagregasi. |
| **Limits** | Ya | Tidak | Melihat batas laju (hanya-baca). |
| **Workspaces** | Ya | Tidak | Melihat workspace per-region (hanya-baca). |
| **Files** | Ya | Ya | Melihat dan mengelola file yang diunggah. |
| **Skills** | Ya | Ya | Melihat dan mengelola Agent Skills. |
| **Batches** | Ya | Ya | Melihat dan mengelola pekerjaan pemrosesan batch. |
| **Agents** | Ya | Ya | Melihat dan mengelola definisi agen. |
| **Sessions** | Ya | Ya | Melihat sesi agen dan riwayat peristiwa. |
| **Environments** | Ya | Ya | Melihat dan mengelola konfigurasi sandbox cloud untuk sesi. |
| **Credential vaults** | Ya | Ya | Melihat dan mengelola credential vault untuk autentikasi sesi. |
| **Memory stores** | Ya | Ya | Melihat dan mengelola memori agen yang persisten. |
| **Webhooks** | Ya | Ya | Melihat dan mengelola endpoint webhook di bawah **Settings → Webhooks**. |
| **API keys** | Tidak | N/A | Kelola kunci API di AWS Console (**Claude Platform on AWS → API keys**). Lihat [Autentikasi kunci API](#api-key-authentication). |
| **Members** | Tidak | N/A | Tidak berlaku. AWS IAM mengelola akses. |
| **Billing** | Tidak | N/A | Tidak berlaku. AWS Marketplace mengelola penagihan dan pembuatan faktur. Lihat rincian biaya di halaman Cost. |
| **Claude Code** | Tidak | N/A | Lihat penggunaan Claude Code di halaman Usage. |

### Beralih organisasi \{#switching-organizations}

Claude Console tidak mendukung peralihan organisasi untuk Claude Platform on AWS. Untuk mengakses organisasi yang berbeda, keluar dan autentikasi ulang melalui AWS Console menggunakan peran IAM untuk akun AWS organisasi tersebut.

## Batas laju dan kuota \{#rate-limits-and-quotas}

Claude Platform on AWS menetapkan batas laju Tier 1 saat pendaftaran. Anthropic mengelola batas laju secara langsung, bukan melalui sistem kuota AWS.

Tidak seperti Claude API pihak pertama, kenaikan tier otomatis tidak berlaku. Jika Anda memerlukan batas yang lebih tinggi, hubungi perwakilan akun Anthropic Anda. Untuk detail tier dan batas per-model, lihat [Batas laju](/docs/id/api/rate-limits).

## Penagihan \{#billing}

Claude Platform on AWS menagih melalui [AWS Marketplace](https://aws.amazon.com/marketplace). Penggunaan dinyatakan dalam Claude Consumption Units (CCU), diukur per jam, dan ditagihkan setiap bulan di belakang pada tagihan AWS Anda. CCU bukan kredit prabayar; tidak ada saldo atau komitmen CCU.

Untuk harga CCU, mekanisme konversi, penerapan diskon, dan tarif token per-model, lihat [Harga Claude Platform on AWS](/docs/id/about-claude/pricing#claude-platform-on-aws-pricing).

## Pemantauan dan pencatatan log \{#monitoring-and-logging}

AWS CloudTrail dapat menangkap semua permintaan ke Claude Platform on AWS. Operasi workspace, vault, dan webhook dicatat sebagai Management events secara default. Operasi inferensi, batch, file, skill, model, profil pengguna, dan Claude Managed Agents (selain vault dan webhook) diklasifikasikan sebagai Data events dan memerlukan konfigurasi pencatatan data event secara eksplisit, yang menimbulkan biaya CloudTrail tambahan. Lihat [referensi tindakan IAM](/docs/id/api/claude-platform-on-aws-iam-actions#route-to-action-mapping) untuk klasifikasi tipe event lengkap dan [dokumentasi AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/) untuk detail konfigurasi.

### ID Permintaan \{#request-ids}

Setiap respons menyertakan dua ID permintaan dalam header respons:

- **AWS request ID (`x-amzn-requestid`):** ID utama, diindeks di CloudTrail. Gunakan ini saat menyelidiki permintaan melalui perangkat AWS atau saat menghubungi dukungan AWS.
- **Anthropic request ID (`request-id`):** ID sekunder. Gunakan ini saat menghubungi dukungan Anthropic.

<CodeGroup>

```python Python nocheck
from anthropic import AnthropicAWS

client = AnthropicAWS()

response = client.messages.with_raw_response.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)

print(response.headers.get("x-amzn-requestid"))  # AWS request ID
print(response.headers.get("request-id"))  # Anthropic request ID

message = response.parse()
print(message.content)
```

```typescript TypeScript nocheck
import AnthropicAws from "@anthropic-ai/aws-sdk";

const client = new AnthropicAws();

const { data: message, response } = await client.messages
  .create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  })
  .withResponse();

console.log(response.headers.get("x-amzn-requestid")); // AWS request ID
console.log(response.headers.get("request-id")); // Anthropic request ID
console.log(message.content);
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Aws;

var client = new AnthropicAwsClient();

var response = await client.WithRawResponse.Messages.Create(new()
{
    Model = Model.ClaudeSonnet4_6,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Hello!" }]
});

Console.WriteLine(response.Headers.GetValues("x-amzn-requestid").First()); // AWS request ID
Console.WriteLine(response.Headers.GetValues("request-id").First()); // Anthropic request ID
Console.WriteLine(response.Value.Content);
```

```go Go nocheck hidelines={1..13,-1}
package main

import (
	"context"
	"fmt"
	"net/http"

	"github.com/anthropics/anthropic-sdk-go"
	anthropicaws "github.com/anthropics/anthropic-sdk-go/aws"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
	client, err := anthropicaws.NewClient(context.Background(), anthropicaws.ClientConfig{})
	if err != nil {
		panic(err)
	}

	var response *http.Response
	message, err := client.Messages.New(
		context.Background(),
		anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeSonnet4_6,
			MaxTokens: 1024,
			Messages: []anthropic.MessageParam{
				anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
			},
		},
		option.WithResponseInto(&response),
	)
	if err != nil {
		panic(err)
	}

	fmt.Println(response.Header.Get("x-amzn-requestid")) // AWS request ID
	fmt.Println(response.Header.Get("request-id"))       // Anthropic request ID
	fmt.Println(message.Content)
}
```

```java Java nocheck
import com.anthropic.aws.backends.AwsBackend;
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.http.HttpResponseFor;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.builder()
        .backend(AwsBackend.fromEnv())
        .build();

    HttpResponseFor<Message> response = client.messages().withRawResponse().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(1024)
            .addUserMessage("Hello!")
            .build()
    );

    IO.println(response.headers().values("x-amzn-requestid").get(0)); // AWS request ID
    IO.println(response.requestId().orElse(null)); // Anthropic request ID
    IO.println(response.parse().content());
}
```

```php PHP nocheck hidelines={1}
<?php
use Anthropic\Aws\Client;

$client = new Client();

$response = $client->messages->raw->create(
    model: 'claude-sonnet-4-6',
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello!']],
);

echo $response->getHeaderLine('x-amzn-requestid') . "\n"; // AWS request ID
echo $response->getHeaderLine('request-id') . "\n"; // Anthropic request ID
echo $response->parse()->content;
```

```ruby Ruby nocheck
# Mengakses header respons mentah saat ini tidak didukung di Ruby SDK.
# Untuk memeriksa header x-amzn-requestid, gunakan salah satu contoh SDK lainnya.
```
</CodeGroup>

Anthropic merekomendasikan untuk mencatat aktivitas Anda setidaknya secara bergulir 30 hari untuk memahami pola penggunaan dan menyelidiki potensi masalah apa pun.

<Note>
AWS CloudTrail dikonfigurasi dalam akun AWS Anda. Mengaktifkan pencatatan log tidak memberikan AWS atau Anthropic akses ke konten Anda di luar apa yang diperlukan untuk penagihan dan operasi layanan.
</Note>

## Migrasi dari Amazon Bedrock \{#migrating-from-amazon-bedrock}

Jika saat ini Anda menggunakan Claude di Bedrock, migrasi ke Claude Platform on AWS memerlukan perubahan di seluruh integrasi Anda. Penandatanganan SigV4 tetap didukung, tetapi konteks penandatanganan, URL dasar, format API, ID model, klien dan paket SDK, format streaming, header permintaan, dan ketersediaan region semuanya berubah. Tabel berikut merangkum perbedaannya.

### Apa yang berubah \{#what-changes}

Delta migrasi bergantung pada integrasi Bedrock mana yang Anda gunakan sebelumnya. Tabel berikut menunjukkan [integrasi Bedrock saat ini](/docs/id/build-with-claude/claude-in-amazon-bedrock) (Messages API di `bedrock-mantle.{region}.api.aws`) dan [integrasi InvokeModel lama](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy).

| Aspek | Dari [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) | Dari [Amazon Bedrock (lama)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) | Ke Claude Platform on AWS |
| :--- | :--- | :--- | :--- |
| **URL dasar** | `bedrock-mantle.{region}.api.aws` | `bedrock-runtime.{region}.amazonaws.com` | `aws-external-anthropic.{region}.api.aws` |
| **Format API** | Messages API di `/anthropic/v1/messages` | Bedrock Converse / InvokeModel | Claude API (`/v1/{endpoint}`) |
| **ID Model** | `anthropic.claude-opus-4-6` | `anthropic.claude-opus-4-6-v1` (dengan prefiks opsional `us.`/`global.`) | `claude-opus-4-6` |
| **Klien SDK** | `AnthropicBedrockMantle` | `AnthropicBedrock` / Bedrock SDK | Klien khusus platform (lihat [Instal SDK](#install-an-sdk)), dalam beta |
| **Paket SDK** | `anthropic[bedrock]`, `@anthropic-ai/bedrock-sdk`, dan lainnya | `anthropic[bedrock]`, `@anthropic-ai/bedrock-sdk`, atau AWS SDK | `anthropic[aws]`, `@anthropic-ai/aws-sdk`, dan lainnya (lihat [Instal SDK](#install-an-sdk)) |
| **Nama layanan SigV4** | `bedrock-mantle` | `bedrock` | `aws-external-anthropic` |
| **Format streaming** | SSE | AWS EventStream | SSE (sama dengan Claude API) |
| **Header workspace** | Tidak berlaku | Tidak berlaku | `anthropic-workspace-id` diperlukan |
| **Ketersediaan region** | Lihat [region Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html) | Lihat [region Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html) | Semua region komersial AWS |

Jika Anda menggunakan integrasi Bedrock saat ini, format body permintaan sudah menggunakan Messages API; perubahannya adalah URL dasar, nama layanan SigV4, ID model, dan penambahan header `anthropic-workspace-id`. Jika Anda menggunakan InvokeModel atau Converse API lama, Anda juga perlu menulis ulang bentuk permintaan dan respons ke format Messages API. Lihat [Claude on Amazon Bedrock (lama)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) untuk pemetaan bentuk permintaan.

### Apa yang Anda dapatkan \{#what-you-gain}

- Biasanya akses di hari yang sama ke model dan fitur baru (lihat [batasan fitur](#features-not-supported))
- Agent Skills untuk pembuatan dokumen (PowerPoint, Excel, Word, PDF)
- Eksekusi kode di sandbox terkelola Anthropic
- Fitur beta melalui header `anthropic-beta` (lihat [batasan fitur](#features-not-supported))
- Claude Console untuk visibilitas kuota dan analitik penggunaan
- Dukungan langsung dari Anthropic
- Autentikasi kunci API sebagai alternatif untuk SigV4 (lihat [Autentikasi kunci API](#api-key-authentication))

### Apa yang tetap sama \{#what-stays-the-same}

- Autentikasi AWS IAM (SigV4)
- AWS sebagai pihak yang menerbitkan faktur (saluran penagihan berubah dari layanan AWS native ke AWS Marketplace; lihat [Pertimbangan komersial](#commercial-considerations))
- Pemenuhan komitmen AWS

### Jebakan migrasi \{#migration-pitfalls}

<Warning>
**Aktifkan outbound web identity federation terlebih dahulu.** Jika akun AWS Anda belum pernah menggunakan Claude Platform on AWS sebelumnya, Anda harus [mengaktifkan outbound web identity federation](#enable-outbound-web-identity-federation) satu kali per akun sebelum membuat permintaan. Tanpa langkah ini, semua permintaan gagal dengan error federasi (lihat [Aktifkan outbound web identity federation](#enable-outbound-web-identity-federation) untuk error yang tepat dan cara mengatasinya). Langkah ini tidak diperlukan untuk Bedrock.
</Warning>

<Warning>
**Zero Data Retention (ZDR) bersifat opt-in di Claude Platform on AWS.** Di Bedrock, AWS adalah pemroses data dan Anthropic tidak menyimpan input atau output inferensi; program ZDR Anthropic tidak berlaku di sana. Di Claude Platform on AWS, Anthropic memproses data inferensi sebagai pemroses data independen, dan ZDR mengikuti model Claude API pihak pertama: tersedia berdasarkan permintaan melalui perwakilan akun Anthropic Anda. Konfirmasikan pendaftaran ZDR sebelum memigrasikan beban kerja produksi yang bergantung pada jaminan retensi data.
</Warning>

### Pertimbangan komersial \{#commercial-considerations}

- **Ketentuan layanan Anthropic:** Menggunakan Claude Platform on AWS mengharuskan Anda menerima Commercial Terms of Service dan Usage Policy Anthropic. Jika organisasi Anda belum menerima ketentuan ini (misalnya, jika Anda hanya menggunakan Claude melalui Bedrock), Anda akan diminta untuk menerimanya selama penyiapan akun. Lihat [Siapkan akun Anda](#set-up-your-account).
- **Diskon dan penawaran privat:** Diskon yang dinegosiasikan dan penawaran privat AWS Marketplace tidak ditransfer secara otomatis antara Bedrock dan Claude Platform on AWS. Bekerja samalah dengan perwakilan akun Anthropic Anda untuk menyiapkan ketentuan komersial untuk Claude Platform on AWS.

## Kebijakan IAM \{#iam-policies}

Claude Platform on AWS terintegrasi dengan AWS IAM untuk kontrol akses. Anda memberikan atau menolak akses ke tindakan API tertentu pada workspace tertentu menggunakan sintaks kebijakan IAM standar.

Nama layanan SigV4 dan namespace tindakan IAM adalah `aws-external-anthropic`. Tindakan mengikuti pola `aws-external-anthropic:<Action>` (misalnya, `aws-external-anthropic:CreateInference`).

### Contoh: menolak inferensi batch \{#example-deny-batch-inference}

Kebijakan berikut mengizinkan inferensi real-time sambil memblokir pemrosesan batch:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "aws-external-anthropic:CreateInference",
        "aws-external-anthropic:CountTokens",
        "aws-external-anthropic:GetModel",
        "aws-external-anthropic:ListModels",
        "aws-external-anthropic:GetWorkspace"
      ],
      "Resource": "arn:aws:aws-external-anthropic:*:*:workspace/*"
    },
    {
      "Effect": "Allow",
      "Action": "aws-external-anthropic:ListWorkspaces",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": [
        "aws-external-anthropic:CreateBatchInference",
        "aws-external-anthropic:GetBatchInference",
        "aws-external-anthropic:ListBatchInferences"
      ],
      "Resource": "*"
    }
  ]
}
```

Tindakan `GetBatchInference` mengotorisasi rute metadata batch dan rute hasil batch. Menolaknya akan memblokir kedua pembacaan tersebut. Untuk kebijakan Deny-only yang cocok untuk beban kerja yang sensitif terhadap ZDR, lihat [Penguncian fitur untuk workspace yang sensitif terhadap ZDR](/docs/id/api/claude-platform-on-aws-iam-actions#feature-lockdown-for-a-zdr-sensitive-workspace).

<Note>
`ListWorkspaces` memiliki cakupan akun, sehingga muncul dalam pernyataan Allow terpisah dengan `"Resource": "*"`. Menentukan ARN workspace pada tindakan dengan cakupan akun tidak memiliki efek (lihat [Otomatisasi penyediaan](/docs/id/api/claude-platform-on-aws-iam-actions#provisioning-automation)).

Kebijakan ini mengasumsikan autentikasi AWS SigV4. Jika principal mengautentikasi dengan kunci API, tambahkan juga `aws-external-anthropic:CallWithBearerToken` ke pernyataan Allow `"Resource": "*"`. `CallWithBearerToken` adalah tindakan lapisan autentikasi tanpa rute yang tidak terikat ke ARN workspace. Lihat [Isolasi workspace per-pelanggan](/docs/id/api/claude-platform-on-aws-iam-actions#per-customer-workspace-isolation) untuk pola dua pernyataan.
</Note>

### Kebijakan terkelola \{#managed-policies}

AWS menyediakan lima kebijakan terkelola (`AnthropicFullAccess`, `AnthropicReadOnlyAccess`, `AnthropicInferenceAccess`, `AnthropicLimitedAccess`, dan `AnthropicSelfHostedEnvironmentAccess`) untuk pola akses umum. Untuk tindakan yang diberikan setiap kebijakan, daftar lengkap tindakan IAM, pemetaan rute-ke-tindakan, dan contoh kebijakan tambahan, lihat [Tindakan IAM untuk Claude Platform on AWS](/docs/id/api/claude-platform-on-aws-iam-actions#managed-policies).

## Sumber daya tambahan \{#additional-resources}

- **Claude Console untuk Claude Platform on AWS:** [platform.claude.com](https://platform.claude.com) (akses melalui AWS Console)
- **Detail harga:** [Harga](/docs/id/about-claude/pricing#claude-platform-on-aws-pricing)
- **Bedrock (Claude yang dioperasikan AWS):** [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock)
- **AWS Marketplace:** [aws.amazon.com/marketplace](https://aws.amazon.com/marketplace)