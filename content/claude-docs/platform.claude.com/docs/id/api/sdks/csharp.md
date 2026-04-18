---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/csharp
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 523f8332983fc0b54f59a9629100b099a8e9e08868037e3f29967d31e3d33560
---

# C# SDK

Instal dan konfigurasi Anthropic C# SDK untuk aplikasi .NET dengan integrasi IChatClient

---

Anthropic C# SDK menyediakan akses yang mudah ke Anthropic REST API dari aplikasi yang ditulis dalam C#.

<Info>
C# SDK saat ini dalam beta. API mungkin berubah antar versi.
</Info>

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus C# dan konfigurasi.
</Info>

<Warning>
Mulai dari versi 10+, paket `Anthropic` sekarang adalah SDK Anthropic resmi untuk C#. Versi paket 3.X dan di bawahnya sebelumnya digunakan untuk SDK yang dibangun komunitas tryAGI, yang telah pindah ke [`tryAGI.Anthropic`](https://www.nuget.org/packages/tryagi.Anthropic/). Jika Anda perlu terus menggunakan klien sebelumnya dalam proyek Anda, perbarui referensi paket Anda ke `tryAGI.Anthropic`.
</Warning>

## Instalasi

Instal paket dari [NuGet](https://www.nuget.org/packages/Anthropic):

```bash
dotnet add package Anthropic
```

## Persyaratan

Perpustakaan ini memerlukan .NET Standard 2.0 atau lebih baru.

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
    Model = "claude-opus-4-7",
};

var message = await client.Messages.Create(parameters);

Console.WriteLine(message);
```

## Konfigurasi klien

Konfigurasi klien menggunakan variabel lingkungan:

```csharp
using Anthropic;

// Dikonfigurasi menggunakan variabel lingkungan ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN dan ANTHROPIC_BASE_URL
AnthropicClient client = new();
```

Atau secara manual:

```csharp
using Anthropic;

AnthropicClient client = new() { ApiKey = "my-anthropic-api-key" };
```

Atau menggunakan kombinasi dari kedua pendekatan.

Lihat tabel ini untuk opsi yang tersedia:

| Properti    | Variabel lingkungan    | Diperlukan | Nilai default                 |
| ----------- | ---------------------- | -------- | ----------------------------- |
| `ApiKey`    | `ANTHROPIC_API_KEY`    | false    | -                             |
| `AuthToken` | `ANTHROPIC_AUTH_TOKEN` | false    | -                             |
| `BaseUrl`   | `ANTHROPIC_BASE_URL`   | true     | `"https://api.anthropic.com"` |

### Memodifikasi konfigurasi

Untuk sementara menggunakan konfigurasi klien yang dimodifikasi, sambil menggunakan kembali koneksi dan thread pool yang sama, panggil `WithOptions` pada klien atau layanan apa pun:

```csharp nocheck
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

Menggunakan [`with` expression](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/with-expression) memudahkan untuk membangun opsi yang dimodifikasi.

Metode `WithOptions` tidak mempengaruhi klien atau layanan asli.

## Streaming

SDK mendefinisikan metode yang mengembalikan aliran respons "chunk", di mana setiap chunk dapat diproses secara individual segera setelah tiba daripada menunggu respons lengkap. Metode streaming umumnya sesuai dengan respons [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) atau [JSONL](https://jsonlines.org).

Metode streaming selalu memiliki akhiran `Streaming` dalam namanya, bahkan jika tidak memiliki varian non-streaming.

Metode streaming ini mengembalikan [`IAsyncEnumerable`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1):

```csharp nocheck
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
    Model = "claude-opus-4-7",
};

await foreach (var message in client.Messages.CreateStreaming(parameters))
{
    Console.WriteLine(message);
}
```

## Penanganan kesalahan

SDK melempar jenis pengecualian unchecked khusus:

- `AnthropicApiException`: Kelas dasar untuk kesalahan API. Lihat tabel ini untuk mengetahui subkelas pengecualian mana yang dilempar untuk setiap kode status HTTP:

| Status | Pengecualian                                |
| ------ | ---------------------------------------- |
| 400    | `AnthropicBadRequestException`           |
| 401    | `AnthropicUnauthorizedException`         |
| 403    | `AnthropicForbiddenException`            |
| 404    | `AnthropicNotFoundException`             |
| 422    | `AnthropicUnprocessableEntityException`  |
| 429    | `AnthropicRateLimitException`            |
| 5xx    | `Anthropic5xxException`                  |
| lainnya | `AnthropicUnexpectedStatusCodeException` |

Selain itu, semua kesalahan 4xx mewarisi dari `Anthropic4xxException`.

- `AnthropicSseException`: dilempar untuk kesalahan yang ditemui selama streaming SSE setelah respons HTTP awal yang berhasil.

- `AnthropicIOException`: Kesalahan jaringan I/O.

- `AnthropicInvalidDataException`: Kegagalan untuk menginterpretasikan data yang berhasil diuraikan. Misalnya, saat mengakses properti yang seharusnya diperlukan, tetapi API secara tidak terduga menghilangkannya dari respons.

- `AnthropicException`: Kelas dasar untuk semua pengecualian.

## Percobaan ulang

SDK secara otomatis mencoba ulang 2 kali secara default, dengan backoff eksponensial pendek antara permintaan.

Hanya jenis kesalahan berikut yang dicoba ulang:

- Kesalahan koneksi (misalnya, karena masalah konektivitas jaringan)
- 408 Request Timeout
- 409 Conflict
- 429 Rate Limit
- 5xx Internal

API juga dapat secara eksplisit menginstruksikan SDK untuk mencoba ulang atau tidak mencoba ulang permintaan.

Untuk menetapkan jumlah percobaan ulang khusus, konfigurasi klien menggunakan properti `MaxRetries`:

```csharp
using Anthropic;

AnthropicClient client = new() { MaxRetries = 3 };
```

Atau konfigurasi panggilan metode tunggal menggunakan `WithOptions`:

```csharp nocheck
using System;

var message = await client
    .WithOptions(options =>
        options with { MaxRetries = 3 }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## Batas waktu

Permintaan habis waktu setelah 10 menit secara default.

Untuk menetapkan batas waktu khusus, konfigurasi klien menggunakan opsi `Timeout`:

```csharp
using System;
using Anthropic;

AnthropicClient client = new() { Timeout = TimeSpan.FromSeconds(42) };
```

Atau konfigurasi panggilan metode tunggal menggunakan `WithOptions`:

```csharp nocheck
using System;

var message = await client
    .WithOptions(options =>
        options with { Timeout = TimeSpan.FromSeconds(42) }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## Paginasi

SDK mendefinisikan metode yang mengembalikan daftar hasil yang dipaginasi. Ini menyediakan cara yang mudah untuk mengakses hasil baik satu halaman sekaligus atau item demi item di semua halaman.

### Paginasi otomatis

Untuk mengulangi semua hasil di semua halaman, gunakan metode `Paginate`, yang secara otomatis mengambil lebih banyak halaman sesuai kebutuhan. Metode mengembalikan [`IAsyncEnumerable`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1):

```csharp nocheck
using System;

var page = await client.Messages.Batches.List(parameters);
await foreach (var item in page.Paginate())
{
    Console.WriteLine(item);
}
```

### Paginasi manual

Untuk mengakses item halaman individual dan secara manual meminta halaman berikutnya, gunakan properti `Items`, dan metode `HasNext` dan `Next`:

```csharp hidelines={1..5}
using Anthropic;
using System;

AnthropicClient client = new();

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

Dalam kasus yang jarang terjadi, API mungkin mengembalikan respons yang tidak sesuai dengan jenis yang diharapkan. Secara default, SDK tidak melempar pengecualian dalam hal ini. Ini melempar `AnthropicInvalidDataException` hanya jika Anda secara langsung mengakses properti.

Jika Anda lebih suka memeriksa bahwa respons sepenuhnya well-typed di awal, maka panggil `Validate`:

```csharp nocheck
var message = await client.Messages.Create(parameters);
message.Validate();
```

Atau konfigurasi klien menggunakan opsi `ResponseValidation`:

```csharp
using Anthropic;

AnthropicClient client = new() { ResponseValidation = true };
```

Atau konfigurasi panggilan metode tunggal menggunakan `WithOptions`:

```csharp nocheck
using System;

var message = await client
    .WithOptions(options =>
        options with { ResponseValidation = true }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## Integrasi IChatClient

SDK menyediakan implementasi antarmuka `IChatClient` dari perpustakaan `Microsoft.Extensions.AI.Abstractions`. Ini memungkinkan `AnthropicClient` (dan `Anthropic.Services.IBetaService`) digunakan dengan perpustakaan lain yang terintegrasi dengan abstraksi inti ini. Misalnya, alat dalam perpustakaan MCP C# SDK (`ModelContextProtocol`) dapat digunakan langsung dengan `AnthropicClient` yang diekspos melalui `IChatClient`.

```csharp nocheck
using Anthropic;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

// Dikonfigurasi menggunakan variabel lingkungan ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN dan ANTHROPIC_BASE_URL
IChatClient chatClient = client.AsIChatClient("claude-opus-4-7")
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

Untuk mengirim permintaan ke Claude API, bangun instance kelas `Params` dan teruskan ke metode klien yang sesuai. Ketika respons diterima, respons dideserialisasi menjadi instance kelas C#.

Misalnya, `client.Messages.Create` harus dipanggil dengan instance `MessageCreateParams`, dan akan mengembalikan instance `Task<Message>`.

## Penggunaan lanjutan

### Respons biner

SDK mendefinisikan metode yang mengembalikan respons biner, yang digunakan untuk respons API yang tidak perlu diuraikan, seperti data non-JSON.

Metode ini mengembalikan `HttpResponse`:

```csharp nocheck
using System;
using Anthropic.Models.Beta.Files;

FileDownloadParams parameters = new() { FileID = "file_id" };

var response = await client.Beta.Files.Download(parameters);

Console.WriteLine(response);
```

Untuk menyimpan konten respons ke file, atau [`Stream`](https://learn.microsoft.com/en-us/dotnet/api/system.io.stream) apa pun, gunakan metode [`CopyToAsync`](https://learn.microsoft.com/en-us/dotnet/api/system.io.stream.copytoasync):

```csharp nocheck
using System.IO;

using var response = await client.Beta.Files.Download(parameters);
using var contentStream = await response.ReadAsStream();
using var fileStream = File.Open(path, FileMode.OpenOrCreate);
await contentStream.CopyToAsync(fileStream); // Atau Stream lainnya
```

### Respons mentah

SDK mendefinisikan metode yang mendeserialisasi respons menjadi instance kelas C#. Untuk mengakses header respons, kode status, atau badan respons mentah, awali panggilan metode HTTP apa pun pada klien atau layanan dengan `WithRawResponse`:

```csharp nocheck
var response = await client.WithRawResponse.Messages.Create(parameters);
var statusCode = response.StatusCode;
var headers = response.Headers;
```

`HttpResponseMessage` mentah juga dapat diakses melalui properti `RawMessage`.

Untuk respons non-streaming, Anda dapat mendeserialisasi respons menjadi instance kelas C# jika diperlukan:

```csharp nocheck
using System;
using Anthropic.Models.Messages;

var response = await client.WithRawResponse.Messages.Create(parameters);
Message deserialized = await response.Deserialize();
Console.WriteLine(deserialized);
```

Untuk respons streaming, Anda dapat mendeserialisasi respons ke `IAsyncEnumerable` jika diperlukan:

```csharp nocheck
using System;

var response = await client.WithRawResponse.Messages.CreateStreaming(parameters);
await foreach (var item in response.Enumerate())
{
    Console.WriteLine(item);
}
```

### Logging

<Warning>
Semua pesan log dimaksudkan hanya untuk debugging. Format dan konten pesan log mungkin berubah antar rilis.
</Warning>

Aktifkan debug logging melalui variabel lingkungan:

```bash
export ANTHROPIC_LOG=debug
```

### Fungsionalitas API yang tidak didokumentasikan

SDK diketik untuk penggunaan yang mudah dari API yang didokumentasikan. Namun, SDK juga mendukung bekerja dengan bagian API yang tidak didokumentasikan atau belum didukung.

## Integrasi platform

<Note>
Untuk panduan setup platform terperinci dengan contoh kode, lihat:
- [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock)
- [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

C# SDK mendukung Bedrock dan Foundry melalui paket NuGet terpisah:

- **Bedrock:** `Anthropic.Bedrock`. Menggunakan `AnthropicBedrockClient` dengan `AnthropicBedrockCredentialsHelper.FromEnv()` atau kredensial eksplisit.
- **Foundry:** `Anthropic.Foundry`. Menggunakan `AnthropicFoundryClient` dengan `DefaultAnthropicFoundryCredentials.FromEnv()` atau kredensial eksplisit.

## Semantic versioning

<Warning>
Meskipun paket ini diversi sebagai 10+, saat ini dalam beta. Selama periode beta, perubahan breaking mungkin terjadi dalam rilis minor atau patch. Setelah perpustakaan mencapai rilis stabil, konvensi SemVer akan diikuti lebih ketat. Bagikan umpan balik dengan [mengajukan masalah](https://www.github.com/anthropics/anthropic-sdk-csharp/issues/new).
</Warning>

Paket ini umumnya mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan backward-incompatible tertentu mungkin dirilis sebagai versi minor:

1. Perubahan pada internal perpustakaan yang secara teknis publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal. _(Silakan buka masalah GitHub untuk memberi tahu pemelihara jika Anda mengandalkan internal tersebut.)_
2. Perubahan yang tidak diharapkan berdampak pada sebagian besar pengguna dalam praktik.

Kompatibilitas backward diambil dengan serius untuk memastikan Anda dapat mengandalkan pengalaman upgrade yang lancar.

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-csharp)
- [Paket NuGet](https://www.nuget.org/packages/Anthropic)
- [Referensi API](/docs/id/api/overview)
- [Panduan streaming](/docs/id/build-with-claude/streaming)