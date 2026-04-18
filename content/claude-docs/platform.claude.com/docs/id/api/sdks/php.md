---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/php
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 2bdcf333ace62335fb9cc6aed965ec0f6918477eced9a58a66d6ee91b5685dc2
---

# PHP SDK

Instal dan konfigurasi Anthropic PHP SDK dengan value objects dan builder patterns

---

Perpustakaan PHP Anthropic menyediakan akses yang mudah ke Anthropic REST API dari aplikasi PHP 8.1.0+ apa pun.

<Info>
PHP SDK saat ini dalam beta. API mungkin berubah antar versi.
</Info>

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus PHP dan konfigurasi.
</Info>

## Instalasi

```bash
composer require "anthropic-ai/sdk"
```

## Persyaratan

PHP 8.1.0 atau lebih tinggi.

## Penggunaan

Perpustakaan ini menggunakan parameter bernama untuk menentukan argumen opsional. Parameter dengan nilai default harus diatur berdasarkan nama.

```php hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(
  apiKey: getenv("ANTHROPIC_API_KEY") ?: "my-anthropic-api-key"
);

$message = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-7',
);

var_dump($message->content);
```

## Value objects

Disarankan untuk menggunakan konstruktor statis `with` `Base64ImageSource::with(data: "U3RhaW5sZXNzIHJvY2tz", ...)` dan parameter bernama untuk menginisialisasi value objects.

Namun, builder juga disediakan `(new Base64ImageSource)->withData("U3RhaW5sZXNzIHJvY2tz")`.

## Streaming

SDK menyediakan dukungan untuk streaming respons menggunakan Server-Sent Events (SSE).

```php hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(
  apiKey: getenv("ANTHROPIC_API_KEY") ?: "my-anthropic-api-key"
);

$stream = $client->messages->createStream(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-7',
);

foreach ($stream as $message) {
  var_dump($message);
}
```

## Penanganan kesalahan

Ketika perpustakaan tidak dapat terhubung ke API, atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx), subkelas `Anthropic\Core\Exceptions\APIException` akan dilempar:

```php hidelines={2..3,7..9}
<?php
use Anthropic\Client;

use Anthropic\Core\Exceptions\APIConnectionException;
use Anthropic\Core\Exceptions\APIStatusException;
use Anthropic\Core\Exceptions\RateLimitException;

$client = new Client();

try {
  $message = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
    model: 'claude-opus-4-7',
  );
} catch (APIConnectionException $e) {
  echo "The server could not be reached", PHP_EOL;
  var_dump($e->getPrevious());
} catch (RateLimitException $_) {
  echo "A 429 status code was received; we should back off a bit.", PHP_EOL;
} catch (APIStatusException $e) {
  echo "Another non-200-range status code was received", PHP_EOL;
  echo $e->getMessage();
}
```

Kode kesalahan adalah sebagai berikut:

| Penyebab          | Jenis Kesalahan                |
| ----------------- | ------------------------------ |
| HTTP 400          | `BadRequestException`          |
| HTTP 401          | `AuthenticationException`      |
| HTTP 403          | `PermissionDeniedException`    |
| HTTP 404          | `NotFoundException`            |
| HTTP 409          | `ConflictException`            |
| HTTP 422          | `UnprocessableEntityException` |
| HTTP 429          | `RateLimitException`           |
| HTTP >= 500       | `InternalServerException`      |
| Kesalahan HTTP lainnya | `APIStatusException`           |
| Timeout           | `APITimeoutException`          |
| Kesalahan jaringan | `APIConnectionException`       |

## Percobaan ulang

Kesalahan tertentu secara otomatis dicoba ulang 2 kali secara default, dengan backoff eksponensial pendek.

Kesalahan koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, >=500 Internal errors, dan timeout semuanya dicoba ulang secara default.

Anda dapat menggunakan opsi `maxRetries` untuk mengonfigurasi atau menonaktifkan ini:

```php hidelines={1..3,5}
<?php

use Anthropic\Client;
use Anthropic\RequestOptions;

// Konfigurasi default untuk semua permintaan:
$client = new Client(requestOptions: RequestOptions::with(maxRetries: 0));

// Atau, konfigurasi per-permintaan:
$result = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-7',
  requestOptions: RequestOptions::with(maxRetries: 5),
);
```

## Paginasi

Metode daftar dalam Claude API dipaginasi.

Perpustakaan ini menyediakan iterator auto-paginating dengan setiap respons daftar, sehingga Anda tidak perlu meminta halaman berturut-turut secara manual:

```php hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(
  apiKey: getenv("ANTHROPIC_API_KEY") ?: "my-anthropic-api-key"
);

$page = $client->beta->messages->batches->list(limit: 20);

var_dump($page);

// ambil item dari halaman saat ini
foreach ($page->getItems() as $item) {
  var_dump($item->id);
}
// buat permintaan jaringan tambahan untuk mengambil item dari semua halaman, termasuk dan setelah halaman saat ini
foreach ($page->pagingEachItem() as $item) {
  var_dump($item->id);
}
```

## Penggunaan lanjutan

### Properti yang tidak terdokumentasi

Anda dapat mengirim parameter yang tidak terdokumentasi ke titik akhir apa pun, dan membaca properti respons yang tidak terdokumentasi, seperti ini:

<Note>
Parameter `extra*` dengan nama yang sama menggantikan parameter yang terdokumentasi.
</Note>

```php hidelines={2..3,5..7}
<?php
use Anthropic\Client;

use Anthropic\RequestOptions;

$client = new Client();

$message = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-7',
  requestOptions: RequestOptions::with(
    extraQueryParams: ['my_query_parameter' => 'value'],
    extraBodyParams: ['my_body_parameter' => 'value'],
    extraHeaders: ['my-header' => 'value'],
  ),
);
```

### Parameter permintaan yang tidak terdokumentasi

Jika Anda ingin secara eksplisit mengirim parameter tambahan, Anda dapat melakukannya dengan opsi `extraQueryParams`, `extraBodyParams`, dan `extraHeaders` di bawah `RequestOptions::with()` saat membuat permintaan, seperti yang terlihat dalam contoh di atas.

### Titik akhir yang tidak terdokumentasi

Untuk membuat permintaan ke titik akhir yang tidak terdokumentasi sambil mempertahankan manfaat auth, retry, dan sebagainya, Anda dapat membuat permintaan menggunakan `client->request`, seperti ini:

```php hidelines={1..2} nocheck
<?php
use Anthropic\Client;
$client = new Client();

$response = $client->request(
  method: "post",
  path: '/undocumented/endpoint',
  query: ['dog' => 'woof'],
  headers: ['useful-header' => 'interesting-value'],
  body: ['hello' => 'world']
);
```

## Semantic versioning

Paket ini mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html). Karena perpustakaan dalam pengembangan awal dan memiliki versi utama `0`, API dapat berubah kapan saja.

Paket ini menganggap peningkatan pada definisi tipe PHPDoc (non-runtime) sebagai perubahan yang tidak merusak.

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-php)
- [Packagist](https://packagist.org/packages/anthropic-ai/sdk)
- [Referensi API](/docs/id/api/overview)
- [Panduan Streaming](/docs/id/build-with-claude/streaming)