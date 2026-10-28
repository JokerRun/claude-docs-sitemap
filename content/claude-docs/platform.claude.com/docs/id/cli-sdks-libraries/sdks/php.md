---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: 0d152d5f95a41c582b2085c3e96da9a6fa27d86aeb567a474832a15fc2437edd
---

---
title: PHP SDK
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php
description: Instal dan konfigurasikan Anthropic PHP SDK dengan value object dan pola builder
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

## Value object

Disarankan untuk menggunakan konstruktor statis `with` `Base64ImageSource::with(data: "U3RhaW5sZXNzIHJvY2tz", ...)` dan parameter bernama untuk menginisialisasi “value object” (objek nilai).

Namun, builder juga disediakan `(new Base64ImageSource)->withData("U3RhaW5sZXNzIHJvY2tz")`.

## Streaming

SDK menyediakan dukungan untuk respons streaming menggunakan Server-Sent Events (SSE).

```php
$client = new Client();

$stream = $client->messages->createStream(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-5-5',
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
// ...
try {
  $message = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
    model: 'claude-opus-5-5',
  );
} catch (APIConnectionException $e) {
  echo "The server could not be reached", PHP_EOL;
  echo $e->getPrevious()?->getMessage(), PHP_EOL;
} catch (RateLimitException $_) {
  echo "A 429 status code was received; we should back off a bit.", PHP_EOL;
} catch (APIStatusException $e) {
  echo "Another non-200-range status code was received", PHP_EOL;
  echo $e->getMessage();
}
```

Kode error adalah sebagai berikut:

| Penyebab           | Jenis Error                    |
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
use Anthropic\RequestOptions;
// ...
// Konfigurasikan default untuk semua permintaan:
$client = new Client(requestOptions: RequestOptions::with(maxRetries: 0));

// Atau, konfigurasikan per permintaan:
$result = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-5-5',
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

Saat aplikasi Anda mendaftarkan tracer provider OpenTelemetry, SDK memancarkan span untuk setiap permintaan yang dikirimnya. Untuk mengirim span ke platform observabilitas Anda, lihat [Menyiapkan OpenTelemetry dengan Claude SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk).

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
  method: "post",
  path: '/undocumented/endpoint',
  query: ['dog' => 'woof'],
  headers: ['useful-header' => 'interesting-value'],
  body: ['hello' => 'world']
);
```

## Integrasi platform

<Note>
  Untuk panduan pengaturan platform terperinci beserta contoh kode, lihat:

  * [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)
  * [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed)
  * [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)

  Lihat juga [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed).
</Note>

PHP SDK mendukung platform berikut:

* **Agent Platform:** `Anthropic\Vertex\Client`. Gunakan `::fromEnvironment()`.
* **Bedrock:** `Anthropic\Bedrock\MantleClient`. Gunakan `new MantleClient(awsRegion: ...)`.
* **Bedrock (lama):** `Anthropic\Bedrock\Client`. Gunakan `::fromEnvironment()` atau `::withCredentials()`.
* **Claude Platform on AWS:** `Anthropic\Aws\Client` (memerlukan `aws/aws-sdk-php` sebagai dependensi lunak). Gunakan `new Anthropic\Aws\Client(workspaceId: ...)` atau atur `ANTHROPIC_AWS_WORKSPACE_ID`. Tersedia dalam beta.
* **Foundry:** `Anthropic\Foundry\Client`. Gunakan `::withCredentials()`.

Gunakan `MantleClient` untuk proyek baru; `Anthropic\Bedrock\Client` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan API `InvokeModel` Bedrock.

PHP SDK juga mendukung Claude Models on Google Cloud (Anthropic managed) melalui `Anthropic\GoogleCloud\Client`. Klien ini masih dalam tahap beta. `Anthropic\GoogleCloud\Client` memerlukan `google/auth` sebagai “soft dependency” (dependensi opsional). Gunakan `new Anthropic\GoogleCloud\Client(workspaceId: ...)` atau atur variabel lingkungan `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID`. Lihat [Resolusi proyek, lokasi, dan workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution).

## Semantic versioning

Setiap versi mayor SDK ini mengirimkan satu versi API di header `anthropic-version` secara default, dan versi mayor baru hadir bersama setiap versi API baru. Versi mayor pertama yang mengirimkan `2026-10-21` adalah 1.0.0; lihat [Upgrade ke 2026-10-21](https://platform.claude.com/docs/id/api/migration-2026-10-21#upgrade).

Paket ini mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html).

Paket ini menganggap peningkatan pada definisi tipe PHPDoc (non-runtime) sebagai perubahan yang tidak merusak kompatibilitas.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-php)
* [Packagist](https://packagist.org/packages/anthropic-ai/sdk)
* [Referensi API](https://platform.claude.com/docs/id/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/id/build-with-claude/streaming)
