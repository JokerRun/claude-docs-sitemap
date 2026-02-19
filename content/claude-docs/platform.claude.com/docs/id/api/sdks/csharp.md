---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/csharp
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: c2ed92243305576dafaf1f2d5cc973d39f7fe3216a5494f9aea9289744534237
---

# C# SDK

Instal dan konfigurasikan Anthropic C# SDK untuk aplikasi .NET dengan integrasi IChatClient

---

Anthropic C# SDK menyediakan akses yang mudah ke Anthropic REST API dari aplikasi yang ditulis dalam C#.

<Info>
C# SDK saat ini dalam beta. API mungkin berubah antar versi.
</Info>

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus C# dan konfigurasi.
</Info>

<Warning>
Mulai dari versi 10+, paket `Anthropic` sekarang adalah SDK Anthropic resmi untuk C#. Versi paket 3.X dan di bawahnya sebelumnya digunakan untuk SDK yang dibangun komunitas tryAGI, yang telah pindah ke [`tryAGI.Anthropic`](https://www.nuget.org/packages/tryagi.Anthropic/). Jika Anda perlu terus menggunakan klien sebelumnya di proyek Anda, perbarui referensi paket Anda ke `tryAGI.Anthropic`.
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
    Model = "claude-opus-4-6",
};

var message = await client.Messages.Create(parameters);

Console.WriteLine(message);
```

## Konfigurasi klien

Konfigurasikan klien menggunakan variabel lingkungan:

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

Menggunakan [ekspresi `with`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/with-expression) memudahkan untuk membuat opsi yang dimodifikasi.

Metode `WithOptions` tidak mempengaruhi klien atau layanan asli.

## Streaming

SDK mendefinisikan metode yang mengembalikan aliran respons "chunk", di mana setiap chunk dapat diproses secara individual segera setelah tiba daripada menunggu respons lengkap. Metode streaming mengembalikan [`IAsyncEnumerable`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1):

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
    Model = "claude-opus-4-6",
};

await foreach (var message in client.Messages.CreateStreaming(parameters))
{
    Console.WriteLine(message);
}
```

## Penanganan kesalahan

SDK melempar jenis pengecualian unchecked khusus:

- `AnthropicApiException`: Kelas dasar untuk kesalahan API. Lihat tabel ini untuk mengetahui subkelas pengecualian mana yang dilempar untuk setiap kode status HTTP:

| Status | Pengecualian                             |
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

- `AnthropicInvalidDataException`: Kegagalan untuk menginterpretasikan data yang berhasil diurai. Misalnya, saat mengakses properti yang seharusnya diperlukan, tetapi API secara tidak terduga menghilangkannya dari respons.

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

Untuk menetapkan jumlah percobaan ulang khusus, konfigurasikan klien menggunakan properti `MaxRetries`:

```csharp
using Anthropic;

AnthropicClient client = new() { MaxRetries = 3 };
```

Atau konfigurasikan panggilan metode tunggal menggunakan `WithOptions`:

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

Permintaan habis waktu setelah 10 menit secara default.

Untuk menetapkan batas waktu khusus, konfigurasikan klien menggunakan opsi `Timeout`:

```csharp
using System;
using Anthropic;

AnthropicClient client = new() { Timeout = TimeSpan.FromSeconds(42) };
```

Atau konfigurasikan panggilan metode tunggal menggunakan `WithOptions`:

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

### Paginasi otomatis

Untuk mengulangi semua hasil di semua halaman, gunakan metode `Paginate`, yang secara otomatis mengambil lebih banyak halaman sesuai kebutuhan. Metode mengembalikan [`IAsyncEnumerable`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1):

```csharp
using System;

var page = await client.Messages.Batches.List(parameters);
await foreach (var item in page.Paginate())
{
    Console.WriteLine(item);
}
```

### Paginasi manual

Untuk mengakses item halaman individual dan secara manual meminta halaman berikutnya, gunakan properti `Items`, dan metode `HasNext` dan `Next`:

```csharp
using System;

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

Dalam kasus yang jarang terjadi, API dapat mengembalikan respons yang tidak sesuai dengan jenis yang diharapkan. Secara default, SDK tidak akan melempar pengecualian dalam hal ini. Ini akan melempar `AnthropicInvalidDataException` hanya jika Anda secara langsung mengakses properti.

Jika Anda lebih suka memeriksa bahwa respons sepenuhnya well-typed di awal, maka panggil `Validate`:

```csharp
var message = await client.Messages.Create(parameters);
message.Validate();
```

Atau konfigurasikan klien menggunakan opsi `ResponseValidation`:

```csharp
using Anthropic;

AnthropicClient client = new() { ResponseValidation = true };
```

Atau konfigurasikan panggilan metode tunggal menggunakan `WithOptions`:

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

SDK menyediakan implementasi antarmuka `IChatClient` dari perpustakaan `Microsoft.Extensions.AI.Abstractions`. Ini memungkinkan `AnthropicClient` digunakan dengan perpustakaan lain yang terintegrasi dengan abstraksi inti ini. Misalnya, alat di perpustakaan MCP C# SDK (`ModelContextProtocol`) dapat digunakan langsung dengan `AnthropicClient` yang diekspos melalui `IChatClient`.

```csharp
using Anthropic;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

// Dikonfigurasi menggunakan variabel lingkungan ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN dan ANTHROPIC_BASE_URL
IChatClient chatClient = client.AsIChatClient("claude-opus-4-6")
    .AsBuilder()
    .UseFunctionInvocation()
    .Build();

// Menggunakan McpClient dari MCP C# SDK
McpClient learningServer = await McpClient.CreateAsync(
    new HttpClientTransport(new() { Endpoint = new("https://learn.microsoft.com/api/mcp") }));

ChatOptions options = new() { Tools = [.. await learningServer.ListToolsAsync()] };

Console.WriteLine(await chatClient.GetResponseAsync("Tell me about IChatClient", options));
```

## Kustomisasi klien HTTP

Untuk mengirim permintaan ke Claude API, buat instance dari beberapa kelas `Params` dan teruskan ke metode klien yang sesuai. Ketika respons diterima, itu akan diserialisasi ke dalam instance kelas C#.

Misalnya, `client.Messages.Create` harus dipanggil dengan instance `MessageCreateParams`, dan itu akan mengembalikan instance `Task<Message>`.

## Penggunaan lanjutan

### Respons biner

SDK mendefinisikan metode yang mengembalikan respons biner, yang digunakan untuk respons API yang tidak perlu diurai, seperti data non-JSON.

Metode ini mengembalikan `HttpResponse`:

```csharp
using System;
using Anthropic.Models.Beta.Files;

FileDownloadParams parameters = new() { FileID = "file_id" };

var response = await client.Beta.Files.Download(parameters);

Console.WriteLine(response);
```

Untuk menyimpan konten respons ke file:

```csharp
using System.IO;

using var response = await client.Beta.Files.Download(parameters);
using var contentStream = await response.ReadAsStream();
using var fileStream = File.Open(path, FileMode.OpenOrCreate);
await contentStream.CopyToAsync(fileStream);
```

### Respons mentah

SDK mendefinisikan metode yang mendeserialisasi respons ke dalam instance kelas C#. Untuk mengakses header respons, kode status, atau badan respons mentah, awali panggilan metode HTTP apa pun pada klien atau layanan dengan `WithRawResponse`:

```csharp
var response = await client.WithRawResponse.Messages.Create(parameters);
var statusCode = response.StatusCode;
var headers = response.Headers;
```

`HttpResponseMessage` mentah juga dapat diakses melalui properti `RawMessage`.

Untuk respons non-streaming, Anda dapat mendeserialisasi respons ke dalam instance kelas C# jika diperlukan:

```csharp
using System;
using Anthropic.Models.Messages;

var response = await client.WithRawResponse.Messages.Create(parameters);
Message deserialized = await response.Deserialize();
Console.WriteLine(deserialized);
```

Untuk respons streaming, Anda dapat mendeserialisasi respons ke `IAsyncEnumerable` jika diperlukan:

```csharp
using System;

var response = await client.WithRawResponse.Messages.CreateStreaming(parameters);
await foreach (var item in response.Enumerate())
{
    Console.WriteLine(item);
}
```

### Logging

Aktifkan logging debug melalui variabel lingkungan:

```bash
export ANTHROPIC_LOG=debug
```

### Fungsionalitas API yang tidak terdokumentasi

SDK diketik untuk penggunaan yang nyaman dari API yang terdokumentasi. Namun, itu juga mendukung bekerja dengan bagian API yang tidak terdokumentasi atau belum didukung.

## Fitur beta

<Warning>
Meskipun paket ini diversi sebagai 10+, saat ini dalam beta. Selama periode beta, perubahan yang merusak dapat terjadi dalam rilis minor atau patch. Setelah perpustakaan mencapai rilis stabil, konvensi SemVer akan diikuti lebih ketat. Bagikan umpan balik dengan [mengajukan masalah](https://www.github.com/anthropics/anthropic-sdk-csharp/issues/new).
</Warning>

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-csharp)
- [Paket NuGet](https://www.nuget.org/packages/Anthropic)
- [Referensi API](/docs/id/api/overview)
- [Panduan streaming](/docs/id/build-with-claude/streaming)