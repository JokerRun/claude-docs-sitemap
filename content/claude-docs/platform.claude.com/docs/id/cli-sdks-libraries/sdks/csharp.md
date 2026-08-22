---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/csharp
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: 391e25280e8b7721a9b60e3d86cbd85a277acd00318f5cddb8fc3a02ccd351e5
---

---
title: C# SDK
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/csharp
description: Instal dan konfigurasikan Anthropic C# SDK untuk aplikasi .NET dengan integrasi IChatClient
---

Anthropic C# SDK menyediakan akses yang mudah ke Claude API dari aplikasi yang ditulis dalam C#.

<Info>
  C# SDK saat ini dalam versi beta. API dapat berubah antar versi.
</Info>

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](https://platform.claude.com/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK khusus C#.
</Info>

<Warning>
  Mulai versi 10+, paket `Anthropic` kini menjadi SDK resmi Anthropic untuk C#. Versi paket 3.X dan di bawahnya sebelumnya digunakan untuk SDK buatan komunitas tryAGI, yang telah dipindahkan ke [`tryAGI.Anthropic`](https://www.nuget.org/packages/tryagi.Anthropic/). Jika Anda perlu terus menggunakan klien lama tersebut dalam proyek Anda, perbarui referensi paket Anda ke `tryAGI.Anthropic`.
</Warning>

## Instalasi

Instal paket dari [NuGet](https://www.nuget.org/packages/Anthropic):

```bash
dotnet add package Anthropic
```

## Persyaratan

Library ini memerlukan .NET Standard 2.0 atau yang lebih baru.

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
    Model = Model.ClaudeOpus5,
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

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication).

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

Metode `WithOptions` tidak memengaruhi klien atau layanan asli.

## Streaming

SDK mendefinisikan metode yang mengembalikan stream "chunk" respons, di mana setiap chunk dapat diproses secara individual segera setelah tiba alih-alih menunggu respons lengkap. Metode streaming umumnya berkorespondensi dengan respons [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) atau [JSONL](https://jsonlines.org).

Metode streaming selalu memiliki akhiran `Streaming` pada namanya, meskipun tidak memiliki varian non-streaming.

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
    Model = Model.ClaudeOpus5,
};

await foreach (var message in client.Messages.CreateStreaming(parameters))
{
    Console.WriteLine(message);
}
```

## Penanganan error

SDK melempar tipe exception unchecked kustom:

* `AnthropicApiException`: Kelas dasar untuk error API. Lihat tabel ini untuk mengetahui subkelas exception mana yang dilempar untuk setiap kode status HTTP:

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

Selain itu, semua error 4xx mewarisi dari `Anthropic4xxException`.

* `AnthropicSseException`: dilempar untuk error yang ditemui selama streaming SSE setelah respons HTTP awal yang berhasil.

* `AnthropicIOException`: Error jaringan I/O.

* `AnthropicInvalidDataException`: Kegagalan menginterpretasikan data yang berhasil di-parse. Misalnya, saat mengakses properti yang seharusnya wajib, tetapi API secara tak terduga menghilangkannya dari respons.

* `AnthropicException`: Kelas dasar untuk semua exception.

## Percobaan ulang

SDK secara otomatis mencoba ulang 2 kali secara default, dengan exponential backoff singkat di antara permintaan.

Hanya tipe error berikut yang dicoba ulang:

* Error koneksi (misalnya, karena masalah konektivitas jaringan)
* 408 Request Timeout
* 409 Conflict
* 429 Rate Limit
* 5xx Internal

API juga dapat secara eksplisit menginstruksikan SDK untuk mencoba ulang atau tidak mencoba ulang suatu permintaan.

Untuk menetapkan jumlah percobaan ulang kustom, konfigurasikan klien menggunakan properti `MaxRetries`:

```csharp
using Anthropic;

AnthropicClient client = new() { MaxRetries = 3 };
```

Atau konfigurasikan satu pemanggilan metode menggunakan `WithOptions`:

```csharp
using System;

var message = await client
    .WithOptions(options =>
        options with { MaxRetries = 3 }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## Timeout

Permintaan mengalami timeout setelah 10 menit secara default.

Untuk menetapkan timeout kustom, konfigurasikan klien menggunakan opsi `Timeout`:

```csharp
using System;
using Anthropic;

AnthropicClient client = new() { Timeout = TimeSpan.FromSeconds(42) };
```

Atau konfigurasikan satu pemanggilan metode menggunakan `WithOptions`:

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

SDK mendefinisikan metode yang mengembalikan daftar hasil yang dipaginasi. SDK menyediakan cara yang mudah untuk mengakses hasil baik satu halaman sekaligus maupun item demi item di seluruh halaman.

### Paginasi otomatis

Untuk mengiterasi semua hasil di seluruh halaman, gunakan metode `Paginate`, yang secara otomatis mengambil halaman tambahan sesuai kebutuhan. Metode ini mengembalikan [`IAsyncEnumerable`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1):

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

Dalam kasus yang jarang terjadi, API dapat mengembalikan respons yang tidak sesuai dengan tipe yang diharapkan. Secara default, SDK tidak melempar exception dalam kasus ini. SDK hanya melempar `AnthropicInvalidDataException` jika Anda mengakses properti tersebut secara langsung.

Jika Anda lebih suka memeriksa bahwa respons sepenuhnya bertipe dengan benar sejak awal, panggil `Validate`:

```csharp
var message = await client.Messages.Create(parameters);
message.Validate();
```

Atau konfigurasikan klien menggunakan opsi `ResponseValidation`:

```csharp
using Anthropic;

AnthropicClient client = new() { ResponseValidation = true };
```

Atau konfigurasikan satu pemanggilan metode menggunakan `WithOptions`:

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

SDK menyediakan implementasi antarmuka `IChatClient` dari library `Microsoft.Extensions.AI.Abstractions`. Ini memungkinkan `AnthropicClient` (dan `Anthropic.Services.IBetaService`) digunakan bersama library lain yang terintegrasi dengan abstraksi inti ini. Misalnya, alat dalam library MCP C# SDK (`ModelContextProtocol`) dapat digunakan secara langsung dengan `AnthropicClient` yang diekspos melalui `IChatClient`.

```csharp
using Anthropic;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

// Dikonfigurasi menggunakan variabel lingkungan ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, dan ANTHROPIC_BASE_URL
AnthropicClient client = new();

IChatClient chatClient = client.AsIChatClient("claude-opus-5")
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

Untuk mengirim permintaan ke Claude API, buat instance dari kelas `Params` dan teruskan ke metode klien yang sesuai. Ketika respons diterima, respons tersebut dideserialisasi menjadi instance dari kelas C#.

Misalnya, `client.Messages.Create` harus dipanggil dengan instance `MessageCreateParams`, dan akan mengembalikan instance `Task<Message>`.

## Penggunaan lanjutan

### Respons biner

SDK mendefinisikan metode yang mengembalikan respons biner, yang digunakan untuk respons API yang tidak harus di-parse, seperti data non-JSON.

Metode ini mengembalikan `HttpResponse`:

```csharp
using System;
using Anthropic.Models.Files;

FileDownloadParams parameters = new() { FileID = "file_id" };

var response = await client.Files.Download(parameters);

Console.WriteLine(response);
```

Untuk menyimpan konten respons ke file, atau [`Stream`](https://learn.microsoft.com/en-us/dotnet/api/system.io.stream) apa pun, gunakan metode [`CopyToAsync`](https://learn.microsoft.com/en-us/dotnet/api/system.io.stream.copytoasync):

```csharp
using System.IO;

using var response = await client.Files.Download(parameters);
using var contentStream = await response.ReadAsStream();
using var fileStream = File.Open(path, FileMode.OpenOrCreate);
await contentStream.CopyToAsync(fileStream); // Or any other Stream
```

### Respons mentah

SDK mendefinisikan metode yang mendeserialisasi respons menjadi instance kelas C#. Untuk mengakses header respons, kode status, atau body respons mentah, awali pemanggilan metode HTTP apa pun pada klien atau layanan dengan `WithRawResponse`:

```csharp
var response = await client.WithRawResponse.Messages.Create(parameters);
var statusCode = response.StatusCode;
var headers = response.Headers;
```

`HttpResponseMessage` mentah juga dapat diakses melalui properti `RawMessage`.

Untuk respons non-streaming, Anda dapat mendeserialisasi respons menjadi instance kelas C# jika diperlukan:

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

Aktifkan debug logging dengan menetapkan variabel lingkungan:

```bash
export ANTHROPIC_LOG=debug
```

### Fungsionalitas API yang tidak terdokumentasi

SDK memiliki tipe untuk penggunaan yang mudah atas API yang terdokumentasi. Namun, SDK juga mendukung bekerja dengan bagian API yang tidak terdokumentasi atau belum didukung.

## Integrasi platform

<Note>
  Untuk panduan penyiapan platform yang terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)
  * [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

C# SDK mendukung platform berikut melalui paket NuGet terpisah:

* **Agent Platform:** `Anthropic.Vertex`. Lihat [Claude di Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai) untuk penyiapan klien.
* **Bedrock:** `Anthropic.Bedrock`. Gunakan `AnthropicBedrockMantleClient` untuk endpoint Bedrock Messages-API, atau `AnthropicBedrockClient` (jalur `bedrock-runtime`). `AnthropicBedrockMantleClient` menerima objek konfigurasi `MantleAwsClientOptions` opsional; `AnthropicBedrockClient` menerima `AnthropicBedrockCredentialsHelper.FromEnv()` atau kredensial eksplisit.
* **Claude Platform on AWS:** `Anthropic.Aws`. Gunakan `AnthropicAwsClient`; tetapkan `WorkspaceId` pada klien atau variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID` (lihat [Workspaces](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#workspaces)). Tersedia dalam versi beta.
* **Foundry:** `Anthropic.Foundry`. Gunakan `AnthropicFoundryClient` dengan `DefaultAnthropicFoundryCredentials.FromEnv()` atau kredensial eksplisit.

Gunakan `AnthropicBedrockMantleClient` untuk proyek baru; `AnthropicBedrockClient` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan API `InvokeModel` Bedrock.

## Semantic versioning

<Warning>
  Meskipun paket ini diberi versi 10+, paket ini saat ini dalam versi beta. Selama periode beta, perubahan yang merusak kompatibilitas dapat terjadi pada rilis minor atau patch. Setelah library mencapai rilis stabil, konvensi SemVer akan diikuti dengan lebih ketat. Sampaikan masukan dengan [mengajukan issue](https://github.com/anthropics/anthropic-sdk-csharp/issues/new).
</Warning>

Paket ini secara umum mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan tertentu yang tidak kompatibel ke belakang dapat dirilis sebagai versi minor:

1. Perubahan pada internal library yang secara teknis publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
2. Perubahan yang dalam praktiknya tidak diperkirakan berdampak pada sebagian besar pengguna.

Kompatibilitas ke belakang ditangani dengan serius untuk memastikan Anda dapat mengandalkan pengalaman upgrade yang lancar.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-csharp)
* [Paket NuGet](https://www.nuget.org/packages/Anthropic)
* [Referensi API](https://platform.claude.com/docs/id/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/id/build-with-claude/streaming)
