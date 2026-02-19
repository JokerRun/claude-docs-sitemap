---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/php
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: 80c3de3ddf654dab84642d2f88ccf9e2928614512d6e9e368ff97b4c43dcc651
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

```php
<?php

use Anthropic\Client;

$client = new Client(
  apiKey: getenv("ANTHROPIC_API_KEY") ?: "my-anthropic-api-key"
);

$message = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-6',
);

var_dump($message->content);
```

## Value objects

Disarankan untuk menggunakan konstruktor statis `with` `Base64ImageSource::with(data: "U3RhaW5sZXNzIHJvY2tz", ...)` dan parameter bernama untuk menginisialisasi value objects.

Namun, builder juga disediakan `(new Base64ImageSource)->withData("U3RhaW5sZXNzIHJvY2tz")`.

## Streaming

SDK menyediakan dukungan untuk streaming respons menggunakan Server-Sent Events (SSE).

```php
<?php

use Anthropic\Client;

$client = new Client(
  apiKey: getenv("ANTHROPIC_API_KEY") ?: "my-anthropic-api-key"
);

$stream = $client->messages->createStream(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-6',
);

foreach ($stream as $message) {
  var_dump($message);
}
```

## Penanganan kesalahan

Ketika perpustakaan tidak dapat terhubung ke API, atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx), subclass dari `Anthropic\Core\Exceptions\APIException` akan dilempar:

```php
<?php

use Anthropic\Core\Exceptions\APIConnectionException;
use Anthropic\Core\Exceptions\APIStatusException;
use Anthropic\Core\Exceptions\RateLimitException;

try {
  $message = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
    model: 'claude-opus-4-6',
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

Kesalahan tertentu secara otomatis dicoba ulang 2 kali secara default, dengan backoff eksponensial singkat.

Kesalahan koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, >=500 Internal errors, dan timeouts semuanya dicoba ulang secara default.

Anda dapat menggunakan opsi `maxRetries` untuk mengonfigurasi atau menonaktifkan ini:

```php
<?php

use Anthropic\Client;
use Anthropic\RequestOptions;

// Configure the default for all requests:
$client = new Client(maxRetries: 0);

// Or, configure per-request:
$result = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-6',
  requestOptions: RequestOptions::with(maxRetries: 5),
);
```

## Paginasi

Metode daftar dalam Claude API dipaginasi.

Perpustakaan ini menyediakan iterator auto-paginating dengan setiap respons daftar, sehingga Anda tidak perlu meminta halaman berturut-turut secara manual:

```php
<?php

use Anthropic\Client;

$client = new Client(
  apiKey: getenv("ANTHROPIC_API_KEY") ?: "my-anthropic-api-key"
);

$page = $client->messages->batches->list();

var_dump($page);

// fetch items from the current page
foreach ($page->getItems() as $item) {
  var_dump($item->id);
}
// make additional network requests to fetch items from all pages, including and after the current page
foreach ($page->pagingEachItem() as $item) {
  var_dump($item->id);
}
```

## Penggunaan lanjutan

### Properti yang tidak didokumentasikan

Anda dapat mengirim parameter yang tidak didokumentasikan ke titik akhir apa pun, dan membaca properti respons yang tidak didokumentasikan, seperti ini:

<Note>
Parameter `extra*` dengan nama yang sama menggantikan parameter yang didokumentasikan.
</Note>

```php
<?php

use Anthropic\RequestOptions;

$message = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-4-6',
  requestOptions: RequestOptions::with(
    extraQueryParams: ['my_query_parameter' => 'value'],
    extraBodyParams: ['my_body_parameter' => 'value'],
    extraHeaders: ['my-header' => 'value'],
  ),
);
```

### Parameter permintaan yang tidak didokumentasikan

Jika Anda ingin secara eksplisit mengirim parameter tambahan, Anda dapat melakukannya dengan opsi `extraQueryParams`, `extraBodyParams`, dan `extraHeaders` di bawah `RequestOptions::with()` saat membuat permintaan, seperti yang terlihat dalam contoh di atas.

### Titik akhir yang tidak didokumentasikan

Untuk membuat permintaan ke titik akhir yang tidak didokumentasikan sambil mempertahankan manfaat auth, retries, dan sebagainya, Anda dapat membuat permintaan menggunakan `client->request`, seperti ini:

```php
<?php

$response = $client->request(
  method: "post",
  path: '/undocumented/endpoint',
  query: ['dog' => 'woof'],
  headers: ['useful-header' => 'interesting-value'],
  body: ['hello' => 'world']
);
```

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-php)
- [Packagist](https://packagist.org/packages/anthropic-ai/sdk)
- [Referensi API](/docs/id/api/overview)
- [Panduan Streaming](/docs/id/build-with-claude/streaming)