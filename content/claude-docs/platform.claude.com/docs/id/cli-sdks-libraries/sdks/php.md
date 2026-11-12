---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php
fetched_at: 2026-11-12T02:13:38.637181Z
sha256: eb4c30a7c55f107be9cf94dcd3dd20b3c0ed4d0ceef5a26af0b82db2adb58345
---

---
title: PHP SDK
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php
description: Instal dan konfigurasikan Anthropic PHP SDK dengan objek nilai dan pola builder
---

Library PHP Anthropic menyediakan akses yang mudah ke Claude API dari aplikasi PHP 8.1.0+ mana pun.

<Info>
  Untuk dokumentasi fitur API beserta contoh kode, lihat [referensi API](https://platform.claude.com/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK yang khusus untuk PHP.
</Info>

## Instalasi

SDK menggunakan [PSR-18](https://www.php-fig.org/psr/psr-18/) untuk HTTP dan secara otomatis mendeteksi klien PSR-18 apa pun yang terinstal. [Guzzle](https://docs.guzzlephp.org/) direkomendasikan karena SDK mengonfigurasinya untuk streaming tanpa pengaturan tambahan:

```bash
composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7"
```

## Persyaratan

PHP 8.1.0 atau lebih tinggi.

## Penggunaan

Library ini menggunakan “named parameters” (parameter bernama) untuk menentukan argumen opsional. Parameter dengan nilai default harus diatur berdasarkan nama.

```php
$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
    model: 'claude-opus-5-5',
);

$textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
echo $textBlock->text;
```

Untuk opsi autentikasi termasuk “Workload Identity Federation” (federasi identitas beban kerja), lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication). Jika kunci API Anda adalah [kunci akun pribadi atau akun layanan](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) yang tidak dibatasi pada suatu workspace, atur ID workspace di header permintaan `anthropic-workspace-id`; [Pilih workspace](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace) menunjukkan opsi per permintaan untuk SDK ini.

## Objek nilai

Cara yang direkomendasikan untuk menginisialisasi “value object” (objek nilai) adalah dengan konstruktor statis `with` `Base64ImageSource::with(data: 'U3RhaW5sZXNzIHJvY2tz', ...)` menggunakan parameter bernama.

Namun, builder juga disediakan, misalnya `(new Base64ImageSource())->withData('U3RhaW5sZXNzIHJvY2tz')`.

## Streaming

SDK menyediakan dukungan untuk respons streaming menggunakan Server-Sent Events (SSE).

```php
$client = new Client();

$stream = $client->messages->createStream(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
    model: Model::CLAUDE_OPUS_5_5,
);

foreach ($stream as $event) {
    echo $event->type . PHP_EOL;
}
```

Streaming memerlukan klien HTTP yang mengembalikan body respons secara bertahap. Ketika Guzzle adalah klien PSR-18 yang terdeteksi, SDK mengonfigurasinya untuk streaming secara otomatis. Dengan klien yang melakukan buffering, loop `foreach` menghasilkan semua event sekaligus saat respons selesai alih-alih secara bertahap; jika Anda mengamati gejala tersebut, instal Guzzle atau sediakan klien PSR-18 yang mendukung streaming melalui opsi permintaan `streamingTransporter`:

```php
$client = new Client(
    requestOptions: RequestOptions::with(streamingTransporter: $myStreamingClient),
);
```

## Penanganan error

Ketika library tidak dapat terhubung ke API, atau jika API mengembalikan kode status yang tidak berhasil (yaitu, respons 4xx atau 5xx), subclass dari `Anthropic\Core\Exceptions\APIException` akan dilemparkan:

```php
<?php
// ...
use Anthropic\Core\Exceptions\APIConnectionException;
use Anthropic\Core\Exceptions\APIStatusException;
use Anthropic\Core\Exceptions\RateLimitException;
use Anthropic\Messages\Model;
// ...
try {
    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [['role' => 'user', 'content' => 'Hello, Claude']],
        model: Model::CLAUDE_OPUS_5_5,
    );
} catch (APIConnectionException $e) {
    echo 'The server could not be reached', PHP_EOL;
    echo $e->getPrevious()?->getMessage(), PHP_EOL;
} catch (RateLimitException $_) {
    echo 'A 429 status code was received; we should back off a bit.', PHP_EOL;
} catch (APIStatusException $e) {
    echo 'Another non-200-range status code was received', PHP_EOL;
    echo $e->getMessage();
}
```

Kode error adalah sebagai berikut:

| Penyebab           | Jenis error                    |
| ------------------ | ------------------------------ |
| HTTP 400           | `BadRequestException`          |
| HTTP 401           | `AuthenticationException`      |
| HTTP 403           | `PermissionDeniedException`    |
| HTTP 404           | `NotFoundException`            |
| HTTP 409           | `ConflictException`            |
| HTTP 422           | `UnprocessableEntityException` |
| HTTP 429           | `RateLimitException`           |
| HTTP >= 500        | `InternalServerException`      |
| Error HTTP lainnya | `APIStatusException`           |
| Timeout            | `APITimeoutException`          |
| Error jaringan     | `APIConnectionException`       |

## Percobaan ulang

Error tertentu secara otomatis dicoba ulang dua kali secara default, dengan “exponential backoff” (penundaan eksponensial) yang singkat.

Error koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, error Internal >=500, dan timeout semuanya dicoba ulang secara default.

Anda dapat menggunakan opsi `maxRetries` untuk mengonfigurasi atau menonaktifkan ini:

```php
use Anthropic\Messages\Model;
use Anthropic\RequestOptions;
// ...
// Konfigurasikan default untuk semua permintaan:
$client = new Client(requestOptions: RequestOptions::with(maxRetries: 0));

// Atau, konfigurasikan per permintaan:
$result = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
    model: Model::CLAUDE_OPUS_5_5,
    requestOptions: RequestOptions::with(maxRetries: 5),
);
```

## Paginasi

Metode list di Claude API menggunakan paginasi.

Library ini menyediakan iterator dengan paginasi otomatis pada setiap respons list, sehingga Anda tidak perlu meminta halaman berikutnya secara manual:

```php
$client = new Client();

$page = $client->beta->messages->batches->list(limit: 20);

// ambil item dari halaman saat ini
foreach ($page->getItems() as $item) {
    echo $item->id, PHP_EOL;
}
// buat permintaan jaringan tambahan untuk mengambil item dari semua halaman, termasuk dan setelah halaman saat ini
// ...
foreach ($page->pagingEachItem() as $item) {
    echo $item->id, PHP_EOL;
// ...
}
```

## Penggunaan lanjutan

### Tracing OpenTelemetry

Saat aplikasi Anda mendaftarkan tracer provider OpenTelemetry, SDK memancarkan span untuk setiap permintaan yang dikirimnya. Untuk mengirim span ke platform observabilitas Anda, lihat [Menyiapkan OpenTelemetry dengan Anthropic SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk).

### Properti yang tidak terdokumentasi

Anda dapat mengirim parameter yang tidak terdokumentasi ke endpoint mana pun, dan membaca properti respons yang tidak terdokumentasi, sebagai berikut:

<Note>
  Parameter `extra*` dengan nama yang sama akan menimpa parameter yang terdokumentasi.
</Note>

```php
<?php
// ...
use Anthropic\RequestOptions;
// ...
$message = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
    model: 'claude-opus-5-5',
    requestOptions: RequestOptions::with(
        extraQueryParams: ['my_query_parameter' => 'value'],
        extraBodyParams: ['my_body_parameter' => 'value'],
        extraHeaders: ['my-header' => 'value'],
    ),
);
```

### Parameter permintaan yang tidak terdokumentasi

Jika Anda ingin mengirim parameter tambahan secara eksplisit, Anda dapat melakukannya dengan opsi `extraQueryParams`, `extraBodyParams`, dan `extraHeaders` di bawah `RequestOptions::with()` saat membuat permintaan, seperti yang terlihat pada contoh sebelumnya.

### Endpoint yang tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi sambil tetap mempertahankan manfaat autentikasi, percobaan ulang, dan fitur klien lainnya, Anda dapat membuat permintaan menggunakan `client->request`, sebagai berikut:

```php
$client = new Client();

$response = $client->request(
    method: 'post',
    path: '/undocumented/endpoint',
    query: ['dog' => 'woof'],
    headers: ['useful-header' => 'interesting-value'],
    body: ['hello' => 'world']
);
```

### Middleware

Middleware menjalankan kode Anda di sekitar setiap permintaan HTTP yang dikirim klien. [Middleware SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/middleware) menunjukkan cara mendaftarkan middleware dan urutan eksekusi beberapa middleware. Bagian ini membahas detail yang khusus untuk PHP SDK.

Middleware adalah callable yang menerima permintaan dan `$next`, atau instance dari kelas yang mengimplementasikan `Anthropic\Middleware`, yang metode `handle()`-nya memiliki signature yang sama. Opsi permintaan `middleware` menerima keduanya:

```php
use Anthropic\Middleware;
use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;

final class TracingMiddleware implements Middleware
{
    public function handle(RequestInterface $request, \Closure $next): ResponseInterface
    {
        return $next($request->withHeader('x-trace-id', bin2hex(random_bytes(8))));
    }
}

$client = new Client(requestOptions: ['middleware' => [new TracingMiddleware()]]);
```

`$next` menjalankan sisa rantai dan mengirim permintaan. Panggil sekali untuk meneruskan permintaan, lewati pemanggilan untuk mengembalikan respons Anda sendiri (seperti respons yang di-cache), atau panggil beberapa kali untuk mengirim permintaan lanjutan (seperti percobaan ulang kustom).

SDK juga meneruskan argumen ketiga ke setiap middleware: `Anthropic\RequestOptions` milik permintaan, yang menggabungkan opsi klien dengan opsi pemanggilan. Untuk membaca opsi seperti `fallbackState`, deklarasikan parameter ketiga yang opsional, `?RequestOptions $options = null`. Perlakukan objek tersebut sebagai read-only, karena setiap middleware dan setiap percobaan ulang permintaan berbagi objek yang sama. Jika callable Anda sudah memiliki parameter ketiga dengan tujuan lain, tulis ulang callable tersebut, karena SDK mengisi parameter itu pada setiap pemanggilan.

Saat runtime:

* **Percobaan ulang:** Middleware berjalan sekali untuk setiap percobaan HTTP, di dalam loop percobaan ulang SDK, sehingga berjalan lagi pada setiap percobaan ulang.
* **Respons error:** `$next` mengembalikan respons untuk setiap status HTTP. SDK melemparkan [exception bertipe](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php#error-handling) miliknya hanya setelah seluruh rantai selesai, sehingga middleware dapat memeriksa atau mengganti respons 4xx atau 5xx.
* **Exception:** Exception yang dilemparkan middleware mencapai kode Anda tanpa perubahan, kecuali dalam dua kasus. SDK menangani `ClientExceptionInterface` PSR-18 sebagai error koneksi, yang muncul sebagai `APIConnectionException`. SDK mencoba ulang percobaan setelah `Anthropic\Core\Exceptions\RetryableException`, dan melemparkan exception tersebut tanpa perubahan ketika tidak ada percobaan ulang yang tersisa.
* **Autentikasi:** SDK memperbarui token OAuth, serta menandatangani atau mengotorisasi permintaan Amazon Bedrock dan Google Cloud, di dalam `$next` paling dalam. Oleh karena itu, permintaan yang diubah oleh middleware Anda ditandatangani setelah perubahan, dan ditandatangani lagi setiap kali Anda memanggil `$next`.
* **Body respons:** Middleware yang membaca body respons harus me-rewind-nya, atau mengembalikan `$response->withBody(...)` dengan body baru, sehingga SDK masih dapat mendekodenya. Body streaming tidak dapat di-rewind, jadi teruskan tanpa dibaca.

## Integrasi platform

<Note>
  Untuk panduan pengaturan platform terperinci beserta contoh kode, lihat:

  * [Amazon Bedrock (`bedrock-mantle`)](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (`bedrock-runtime`)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)
  * [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed)
  * [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)

  Lihat juga [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed).
</Note>

PHP SDK mendukung platform berikut:

* **Claude Models on Google Cloud (Google managed):** `Anthropic\Vertex\Client`. Gunakan `::fromEnvironment()`.
* **Amazon Bedrock (`bedrock-mantle`):** `Anthropic\Bedrock\MantleClient`. Gunakan `new MantleClient(awsRegion: ...)`.
* **Amazon Bedrock (`bedrock-runtime`):** `Anthropic\Bedrock\Client`, untuk API `InvokeModel`. Gunakan `::fromEnvironment()` atau `::withCredentials()`.
* **Claude Platform on AWS:** `Anthropic\Aws\Client` (memerlukan `aws/aws-sdk-php` sebagai dependensi lunak). Gunakan `new Anthropic\Aws\Client(workspaceId: ...)` atau atur `ANTHROPIC_AWS_WORKSPACE_ID`. Tersedia dalam beta.
* **Foundry:** `Anthropic\Foundry\Client`. Gunakan `::withCredentials()`.

PHP SDK juga mendukung Claude Models on Google Cloud (Anthropic managed) melalui `Anthropic\GoogleCloud\Client`. Klien ini masih dalam tahap beta. `Anthropic\GoogleCloud\Client` memerlukan `google/auth` sebagai “soft dependency” (dependensi opsional). Gunakan `new Anthropic\GoogleCloud\Client(workspaceId: ...)` atau atur variabel lingkungan `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID`. Lihat [Resolusi proyek, lokasi, dan workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution).

## Pembuatan versi semantik

Paket ini mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html).

Paket ini menganggap peningkatan pada definisi tipe PHPDoc (non-runtime) sebagai perubahan yang tidak merusak kompatibilitas.

Setiap permintaan ke Claude API menggunakan versi API. Dengan SDK ini, permintaan Anda menggunakan versi API yang berlaku saat versi mayor SDK Anda dirilis, sehingga Anda beralih ke versi API baru dengan melakukan upgrade ke versi mayor baru. Versi 1.0.0 adalah yang pertama menggunakan `2026-10-21`. Lihat [Migrasi ke versi API 2026-10-21](https://platform.claude.com/docs/id/api/migration-2026-10-21#upgrade) untuk cara melakukan upgrade.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-php)
* [Packagist](https://packagist.org/packages/anthropic-ai/sdk)
* [Referensi API](https://platform.claude.com/docs/id/api/overview)
* [Streaming pesan](https://platform.claude.com/docs/id/build-with-claude/streaming)
