---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/csharp
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 85f5cf00d7a76256e35e1318c917378ac7eedda3f7d7424ab2d1a8fcbb3dda4b
---

# SDK C#

Instal dan konfigurasikan Anthropic C# SDK untuk aplikasi .NET dengan integrasi IChatClient

---

Anthropic C# SDK menyediakan akses yang mudah ke REST API Anthropic dari aplikasi yang ditulis dalam C#.

<Info>
  SDK C# saat ini dalam tahap beta. API dapat berubah antar versi.
</Info>

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK yang spesifik untuk C#.
</Info>

<Warning>
  Mulai versi 10+, paket `Anthropic` kini menjadi SDK Anthropic resmi untuk C#. Versi paket 3.X dan di bawahnya sebelumnya digunakan untuk SDK buatan komunitas tryAGI, yang telah dipindahkan ke [`tryAGI.Anthropic`](https://www.nuget.org/packages/tryagi.Anthropic/). Jika Anda perlu terus menggunakan klien sebelumnya dalam proyek Anda, perbarui referensi paket Anda ke `tryAGI.Anthropic`.
</Warning>

## Instalasi

Instal paket dari [NuGet](https://www.nuget.org/packages/Anthropic):

```bash
dotnet add package Anthropic
```

## Persyaratan

Pustaka ini memerlukan .NET Standard 2.0 atau yang lebih baru.

## Penggunaan

```csharp
using System;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

MessageCreateParams parameters = new()
{
    MaxTokens = 1024,
    Messages =
    [
        new()
        {
            Role = Role.User,
            Content = "Hello, Claude",
        },
    ],
    Model = Model.ClaudeOpus4_8,
};

var message = await client.Messages.Create(parameters);

foreach (var block in message.Content)
{
    if (block.TryPickText(out var textBlock))
    {
        Console.WriteLine(textBlock.Text);
    }
}
```

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](/docs/id/manage-claude/authentication).

## Konfigurasi klien

Konfigurasikan klien menggunakan variabel lingkungan:

```csharp
using Anthropic;

// Dikonfigurasi menggunakan variabel lingkungan ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, dan ANTHROPIC_BASE_URL
AnthropicClient client = new();
```

Atau secara manual:

```csharp
using Anthropic;

AnthropicClient client = new() { ApiKey = "my-anthropic-api-key" };
```

Atau menggunakan kombinasi dari kedua pendekatan tersebut.

Lihat tabel ini untuk opsi yang tersedia:

| Properti    | Variabel lingkungan    | Wajib | Nilai default                 |
| ----------- | ---------------------- | ----- | ----------------------------- |
| `ApiKey`    | `ANTHROPIC_API_KEY`    | false | -                             |
| `AuthToken` | `ANTHROPIC_AUTH_TOKEN` | false | -                             |
| `BaseUrl`   | `ANTHROPIC_BASE_URL`   | true  | `"https://api.anthropic.com"` |

### Memodifikasi konfigurasi

Untuk menggunakan konfigurasi klien yang dimodifikasi secara sementara, sambil tetap menggunakan kembali koneksi dan thread pool yang sama, panggil `WithOptions` pada klien atau layanan mana pun:

```csharp
using System;

var message = await client
    .WithOptions(options =>
        options with
        {
            BaseUrl = "https://example.com",
            Timeout = TimeSpan.FromSeconds(42),
        }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

Menggunakan [ekspresi `with`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/with-expression) memudahkan pembuatan opsi yang dimodifikasi.

Metode `WithOptions` tidak memengaruhi klien atau layanan aslinya.

## Streaming

SDK mendefinisikan metode yang mengembalikan stream "chunk" respons, di mana setiap chunk dapat diproses secara individual segera setelah tiba alih-alih menunggu respons lengkap. Metode streaming umumnya sesuai dengan respons [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) atau [JSONL](https://jsonlines.org).

Metode streaming selalu memiliki akhiran `Streaming` pada namanya, bahkan jika tidak memiliki varian non-streaming.

Metode streaming ini mengembalikan [`IAsyncEnumerable`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1):

```csharp
using System;
using Anthropic.Models.Messages;

MessageCreateParams parameters = new()
{
    MaxTokens = 1024,
    Messages =
    [
        new()
        {
            Role = Role.User,
            Content = "Hello, Claude",
        },
    ],
    Model = Model.ClaudeOpus4_8,
};

await foreach (var message in client.Messages.CreateStreaming(parameters))
{
    Console.WriteLine(message);
}
```

## Penanganan kesalahan

SDK melemparkan tipe exception unchecked kustom:

* `AnthropicApiException`: Kelas dasar untuk kesalahan API. Lihat tabel ini untuk mengetahui subkelas exception mana yang dilemparkan untuk setiap kode status HTTP:

| Status  | Exception                                |
| ------- | ---------------------------------------- |
| 400     | `AnthropicBadRequestException`           |
| 401     | `AnthropicUnauthorizedException`         |
| 403     | `AnthropicForbiddenException`            |
| 404     | `AnthropicNotFoundException`             |
| 422     | `AnthropicUnprocessableEntityException`  |
| 429     | `AnthropicRateLimitException`            |
| 5xx     | `Anthropic5xxException`                  |
| lainnya | `AnthropicUnexpectedStatusCodeException` |

Selain itu, semua kesalahan 4xx mewarisi dari `Anthropic4xxException`.

* `AnthropicSseException`: dilemparkan untuk kesalahan yang ditemui selama streaming SSE setelah respons HTTP awal yang berhasil.

* `AnthropicIOException`: Kesalahan jaringan I/O.

* `AnthropicInvalidDataException`: Kegagalan menafsirkan data yang berhasil diurai. Misalnya, saat mengakses properti yang seharusnya wajib, tetapi API secara tak terduga menghilangkannya dari respons.

* `AnthropicException`: Kelas dasar untuk semua exception.

## Percobaan ulang

SDK secara otomatis mencoba ulang 2 kali secara default, dengan exponential backoff singkat di antara permintaan.

Hanya tipe kesalahan berikut yang dicoba ulang:

* Kesalahan koneksi (misalnya, karena masalah konektivitas jaringan)
* 408 Request Timeout
* 409 Conflict
* 429 Rate Limit
* 5xx Internal

API juga dapat secara eksplisit menginstruksikan SDK untuk mencoba ulang atau tidak mencoba ulang suatu permintaan.

Untuk mengatur jumlah percobaan ulang kustom, konfigurasikan klien menggunakan properti `MaxRetries`:

```csharp
using Anthropic;

AnthropicClient client = new() { MaxRetries = 3 };
```

Atau konfigurasikan satu panggilan metode menggunakan `WithOptions`:

```csharp
using System;

var message = await client
    .WithOptions(options =>
        options with { MaxRetries = 3 }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## Batas waktu

Permintaan akan habis waktunya setelah 10 menit secara default.

Untuk mengatur batas waktu kustom, konfigurasikan klien menggunakan opsi `Timeout`:

```csharp
using System;
using Anthropic;

AnthropicClient client = new() { Timeout = TimeSpan.FromSeconds(42) };
```

Atau konfigurasikan satu panggilan metode menggunakan `WithOptions`:

```csharp
using System;

var message = await client
    .WithOptions(options =>
        options with { Timeout = TimeSpan.FromSeconds(42) }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## Paginasi

SDK mendefinisikan metode yang mengembalikan daftar hasil yang dipaginasi. SDK menyediakan cara yang mudah untuk mengakses hasil baik satu halaman pada satu waktu maupun item demi item di semua halaman.

### Paginasi otomatis

Untuk melakukan iterasi melalui semua hasil di semua halaman, gunakan metode `Paginate`, yang secara otomatis mengambil lebih banyak halaman sesuai kebutuhan. Metode ini mengembalikan [`IAsyncEnumerable`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1):

```csharp
using System;

var page = await client.Messages.Batches.List(parameters);
await foreach (var item in page.Paginate())
{
    Console.WriteLine(item);
}
```

### Paginasi manual

Untuk mengakses item halaman individual dan meminta halaman berikutnya secara manual, gunakan properti `Items`, serta metode `HasNext` dan `Next`:

```csharp
var page = await client.Messages.Batches.List();
while (true)
{
    foreach (var item in page.Items)
    {
        Console.WriteLine(item);
    }
    if (!page.HasNext())
    {
        break;
    }
    page = await page.Next();
}
```

## Validasi respons

Dalam kasus yang jarang terjadi, API dapat mengembalikan respons yang tidak cocok dengan tipe yang diharapkan. Secara default, SDK tidak melemparkan exception dalam kasus ini. SDK hanya melemparkan `AnthropicInvalidDataException` jika Anda mengakses properti tersebut secara langsung.

Jika Anda lebih suka memeriksa bahwa respons sepenuhnya bertipe dengan benar di awal, maka panggil `Validate`:

```csharp
var message = await client.Messages.Create(parameters);
message.Validate();
```

Atau konfigurasikan klien menggunakan opsi `ResponseValidation`:

```csharp
using Anthropic;

AnthropicClient client = new() { ResponseValidation = true };
```

Atau konfigurasikan satu panggilan metode menggunakan `WithOptions`:

```csharp
using System;

var message = await client
    .WithOptions(options =>
        options with { ResponseValidation = true }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## Integrasi IChatClient

SDK menyediakan implementasi antarmuka `IChatClient` dari pustaka `Microsoft.Extensions.AI.Abstractions`. Ini memungkinkan `AnthropicClient` (dan `Anthropic.Services.IBetaService`) digunakan dengan pustaka lain yang terintegrasi dengan abstraksi inti ini. Misalnya, alat dalam pustaka MCP C# SDK (`ModelContextProtocol`) dapat digunakan secara langsung dengan `AnthropicClient` yang diekspos melalui `IChatClient`.

```csharp
using Anthropic;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

// Dikonfigurasi menggunakan variabel lingkungan ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, dan ANTHROPIC_BASE_URL
AnthropicClient client = new();

IChatClient chatClient = client.AsIChatClient("claude-opus-4-8")
    .AsBuilder()
    .UseFunctionInvocation()
    .Build();

// Menggunakan McpClient dari MCP C# SDK
McpClient learningServer = await McpClient.CreateAsync(
    new HttpClientTransport(new() { Endpoint = new("https://learn.microsoft.com/api/mcp") }));

ChatOptions options = new() { Tools = [.. await learningServer.ListToolsAsync()] };

Console.WriteLine(await chatClient.GetResponseAsync("Tell me about IChatClient", options));
```

## Permintaan dan respons

Untuk mengirim permintaan ke Claude API, buat instans dari kelas `Params` dan teruskan ke metode klien yang sesuai. Ketika respons diterima, respons tersebut dideserialisasi menjadi instans dari kelas C#.

Misalnya, `client.Messages.Create` harus dipanggil dengan instans `MessageCreateParams`, dan akan mengembalikan instans `Task<Message>`.

## Penggunaan lanjutan

### Respons biner

SDK mendefinisikan metode yang mengembalikan respons biner, yang digunakan untuk respons API yang tidak harus diurai, seperti data non-JSON.

Metode ini mengembalikan `HttpResponse`:

```csharp
using System;
using Anthropic.Models.Beta.Files;

FileDownloadParams parameters = new() { FileID = "file_id" };

var response = await client.Beta.Files.Download(parameters);

Console.WriteLine(response);
```

Untuk menyimpan konten respons ke file, atau [`Stream`](https://learn.microsoft.com/en-us/dotnet/api/system.io.stream) apa pun, gunakan metode [`CopyToAsync`](https://learn.microsoft.com/en-us/dotnet/api/system.io.stream.copytoasync):

```csharp
using System.IO;

using var response = await client.Beta.Files.Download(parameters);
using var contentStream = await response.ReadAsStream();
using var fileStream = File.Open(path, FileMode.OpenOrCreate);
await contentStream.CopyToAsync(fileStream); // Or any other Stream
```

### Respons mentah

SDK mendefinisikan metode yang mendeserialisasi respons menjadi instans kelas C#. Untuk mengakses header respons, kode status, atau body respons mentah, awali panggilan metode HTTP apa pun pada klien atau layanan dengan `WithRawResponse`:

```csharp
var response = await client.WithRawResponse.Messages.Create(parameters);
var statusCode = response.StatusCode;
var headers = response.Headers;
```

`HttpResponseMessage` mentah juga dapat diakses melalui properti `RawMessage`.

Untuk respons non-streaming, Anda dapat mendeserialisasi respons menjadi instans kelas C# jika diperlukan:

```csharp
using System;
using Anthropic.Models.Messages;

var response = await client.WithRawResponse.Messages.Create(parameters);
Message deserialized = await response.Deserialize();
Console.WriteLine(deserialized);
```

Untuk respons streaming, Anda dapat mendeserialisasi respons menjadi `IAsyncEnumerable` jika diperlukan:

```csharp
using System;

var response = await client.WithRawResponse.Messages.CreateStreaming(parameters);
await foreach (var item in response.Enumerate())
{
    Console.WriteLine(item);
}
```

### Logging

<Warning>
  Semua pesan log ditujukan hanya untuk debugging. Format dan konten pesan log dapat berubah antar rilis.
</Warning>

Aktifkan debug logging dengan mengatur variabel lingkungan:

```bash
export ANTHROPIC_LOG=debug
```

### Fungsionalitas API yang tidak terdokumentasi

SDK diberi tipe untuk penggunaan yang mudah dari API yang terdokumentasi. Namun, SDK juga mendukung bekerja dengan bagian API yang tidak terdokumentasi atau belum didukung.

## Integrasi platform

<Note>
  Untuk panduan penyiapan platform yang terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai)
  * [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

SDK C# mendukung platform berikut melalui paket NuGet terpisah:

* **Agent Platform:** `Anthropic.Vertex`. Lihat [Claude di Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai) untuk penyiapan klien.
* **Bedrock:** `Anthropic.Bedrock`. Gunakan `AnthropicBedrockMantleClient` untuk endpoint Bedrock Messages-API, atau `AnthropicBedrockClient` (jalur `bedrock-runtime`). `AnthropicBedrockMantleClient` menerima objek konfigurasi `MantleAwsClientOptions` opsional; `AnthropicBedrockClient` menerima `AnthropicBedrockCredentialsHelper.FromEnv()` atau kredensial eksplisit.
* **Claude Platform di AWS:** `Anthropic.Aws`. Gunakan `AnthropicAwsClient`; atur `WorkspaceId` pada klien atau variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID` (lihat [Workspaces](/docs/id/build-with-claude/claude-platform-on-aws#workspaces)). Tersedia dalam tahap beta.
* **Foundry:** `Anthropic.Foundry`. Gunakan `AnthropicFoundryClient` dengan `DefaultAnthropicFoundryCredentials.FromEnv()` atau kredensial eksplisit.

Gunakan `AnthropicBedrockMantleClient` untuk proyek baru; `AnthropicBedrockClient` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan API `InvokeModel` Bedrock.

## Semantic versioning

<Warning>
  Meskipun paket ini diberi versi 10+, paket ini saat ini dalam tahap beta. Selama periode beta, perubahan yang merusak (breaking changes) dapat terjadi pada rilis minor atau patch. Setelah pustaka mencapai rilis stabil, konvensi SemVer akan diikuti dengan lebih ketat. Bagikan umpan balik dengan [mengajukan issue](https://github.com/anthropics/anthropic-sdk-csharp/issues/new).
</Warning>

Paket ini umumnya mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan tertentu yang tidak kompatibel dengan versi sebelumnya dapat dirilis sebagai versi minor:

1. Perubahan pada internal pustaka yang secara teknis publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
2. Perubahan yang tidak diharapkan berdampak pada sebagian besar pengguna dalam praktiknya.

Kompatibilitas mundur ditangani dengan serius untuk memastikan Anda dapat mengandalkan pengalaman pembaruan yang lancar.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-csharp)
* [Paket NuGet](https://www.nuget.org/packages/Anthropic)
* [Referensi API](/docs/id/api/overview)
* [Streaming Messages](/docs/id/build-with-claude/streaming)
