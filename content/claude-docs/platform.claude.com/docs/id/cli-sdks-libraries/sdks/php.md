---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 3f97204419c23d6317848170fc2c137812c1293c6669fbeb75a3961536845f03
---

# PHP SDK

Instal dan konfigurasikan Anthropic PHP SDK dengan value object dan pola builder

---

Pustaka Anthropic PHP menyediakan akses yang mudah ke Anthropic REST API dari aplikasi PHP 8.1.0+ apa pun.

<Info>
  PHP SDK saat ini masih dalam tahap beta. API dapat berubah antar versi.
</Info>

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK yang spesifik untuk PHP.
</Info>

## Instalasi

SDK ini menggunakan [PSR-18](https://www.php-fig.org/psr/psr-18/) untuk HTTP dan secara otomatis mendeteksi klien PSR-18 apa pun yang terinstal. [Guzzle](https://docs.guzzlephp.org/) direkomendasikan karena SDK mengonfigurasinya untuk streaming tanpa pengaturan tambahan:

```bash
composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7"
```

## Persyaratan

PHP 8.1.0 atau lebih tinggi.

## Penggunaan

Pustaka ini menggunakan "named parameters" (parameter bernama) untuk menentukan argumen opsional. Parameter dengan nilai default harus ditetapkan berdasarkan nama.

```php
$client = new Client();

$message = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-8',
);

echo $message->content[0]->text;
```

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](/docs/id/manage-claude/authentication).

## Value object

Disarankan untuk menggunakan konstruktor statis `with` seperti `Base64ImageSource::with(data: "U3RhaW5sZXNzIHJvY2tz", ...)` dan parameter bernama untuk menginisialisasi value object.

Namun, builder juga disediakan `(new Base64ImageSource)->withData("U3RhaW5sZXNzIHJvY2tz")`.

## Streaming

SDK menyediakan dukungan untuk respons streaming menggunakan Server-Sent Events (SSE).

```php
$client = new Client();

$stream = $client->messages->createStream(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-8',
);

foreach ($stream as $event) {
  echo $event->type . PHP_EOL;
}
```

Streaming memerlukan klien HTTP yang mengembalikan body respons secara bertahap. Ketika Guzzle adalah klien PSR-18 yang terdeteksi, SDK mengonfigurasinya untuk streaming secara otomatis. Dengan klien yang melakukan buffering, loop `foreach` akan menghasilkan semua event sekaligus ketika respons selesai, bukan secara bertahap; jika Anda mengamati gejala tersebut, instal Guzzle atau sediakan klien PSR-18 yang mendukung streaming melalui opsi permintaan `streamingTransporter`:

```php
$client = new Anthropic\Client(
  requestOptions: Anthropic\RequestOptions::with(streamingTransporter: $myStreamingClient),
);
```

## Penanganan error

Ketika pustaka tidak dapat terhubung ke API, atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx), subkelas dari `Anthropic\Core\Exceptions\APIException` akan dilemparkan:

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
    model: 'claude-opus-4-8',
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

| Penyebab           | Tipe Error                     |
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

Error tertentu secara otomatis dicoba ulang dua kali secara default, dengan exponential backoff singkat.

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
  model: 'claude-opus-4-8',
  requestOptions: RequestOptions::with(maxRetries: 5),
);
```

## Paginasi

Metode list di Claude API menggunakan paginasi.

Pustaka ini menyediakan iterator dengan paginasi otomatis pada setiap respons list, sehingga Anda tidak perlu meminta halaman berikutnya secara manual:

```php
$client = new Client();

$page = $client->beta->messages->batches->list(limit: 20);

// ambil item dari halaman saat ini
foreach ($page->getItems() as $item) {
  echo $item->id, PHP_EOL;
}
// buat permintaan jaringan tambahan untuk mengambil item dari semua halaman, termasuk dan setelah halaman saat ini
foreach ($page->pagingEachItem() as $item) {
  echo $item->id, PHP_EOL;
}
```

## Penggunaan lanjutan

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
  model: 'claude-opus-4-8',
  requestOptions: RequestOptions::with(
    extraQueryParams: ['my_query_parameter' => 'value'],
    extraBodyParams: ['my_body_parameter' => 'value'],
    extraHeaders: ['my-header' => 'value'],
  ),
);
```

### Parameter permintaan yang tidak terdokumentasi

Jika Anda ingin secara eksplisit mengirim parameter tambahan, Anda dapat melakukannya dengan opsi `extraQueryParams`, `extraBodyParams`, dan `extraHeaders` di bawah `RequestOptions::with()` saat membuat permintaan, seperti yang terlihat pada contoh sebelumnya.

### Endpoint yang tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi sambil tetap mendapatkan manfaat autentikasi, percobaan ulang, dan fitur klien lainnya, Anda dapat membuat permintaan menggunakan `client->request`, sebagai berikut:

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
  Untuk panduan pengaturan platform yang terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (legacy)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai)
  * [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry)
  * [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws)
</Note>

PHP SDK mendukung platform berikut:

* **Bedrock:** `Anthropic\Bedrock\MantleClient`. Gunakan `new MantleClient(awsRegion: ...)`.
* **Bedrock (legacy):** `Anthropic\Bedrock\Client`. Gunakan `::fromEnvironment()` atau `::withCredentials()`.
* **Agent Platform:** `Anthropic\Vertex\Client`. Gunakan `::fromEnvironment()`.
* **Foundry:** `Anthropic\Foundry\Client`. Gunakan `::withCredentials()`.
* **Claude Platform di AWS:** `Anthropic\Aws\Client` (memerlukan `aws/aws-sdk-php` sebagai soft dependency). Gunakan `new Anthropic\Aws\Client(workspaceId: ...)` atau atur `ANTHROPIC_AWS_WORKSPACE_ID`. Tersedia dalam versi beta.

Gunakan `MantleClient` untuk proyek baru; `Anthropic\Bedrock\Client` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan Bedrock `InvokeModel` API.

## Semantic versioning

Paket ini mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html). Karena pustaka ini masih dalam pengembangan awal dan memiliki versi mayor `0`, API dapat berubah kapan saja.

Paket ini menganggap peningkatan pada definisi tipe PHPDoc (non-runtime) sebagai perubahan yang tidak bersifat breaking.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-php)
* [Packagist](https://packagist.org/packages/anthropic-ai/sdk)
* [Referensi API](/docs/id/api/overview)
* [Streaming Messages](/docs/id/build-with-claude/streaming)
