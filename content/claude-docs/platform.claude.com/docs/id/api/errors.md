---
source: platform
url: https://platform.claude.com/docs/id/api/errors
fetched_at: 2026-11-26T02:13:38.275404Z
sha256: cc9fded865eb76b53acff4fd6c6af5773d4cd2e9a28795fa41a160842671b5e9
---

---
title: Error Claude API
url: https://platform.claude.com/docs/id/api/errors
description: Pahami kode status HTTP, bentuk respons error, dan ID permintaan yang dikembalikan oleh Claude API, serta tangani error dengan exception bertipe dari SDK.
---

Untuk mengetahui error SDK yang dihasilkan oleh suatu error API, lihat [Tipe error SDK](https://platform.claude.com/docs/id/api/errors#sdk-error-types). Untuk menangkapnya dalam kode Anda, lihat [Menangani error](https://platform.claude.com/docs/id/api/handle-errors).

## Error HTTP

API mengikuti format kode error HTTP yang dapat diprediksi:

* 400 - `invalid_request_error`: Terdapat masalah pada format atau konten permintaan Anda. API mungkin juga menggunakan tipe error ini untuk kode status 4XX lain yang tidak tercantum di bagian ini. API juga mengembalikan 400 ketika penggunaan mencapai [batas pengeluaran yang Anda tetapkan](https://platform.claude.com/docs/id/api/rate-limits#setting-your-own-spend-limit) untuk organisasi atau workspace. Batas pada [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace) merupakan pengecualian: batas tersebut dapat mengembalikan 429 sebagai gantinya. Jika pesannya menyebutkan masalah pada permintaan Anda, cari masalah tersebut di [Error validasi umum](https://platform.claude.com/docs/id/api/errors#common-validation-errors).

* 401 - `authentication_error`: Terdapat masalah pada [kunci API](https://platform.claude.com/docs/id/get-api-key) Anda (misalnya, formatnya salah, telah dicabut, atau kedaluwarsa; lihat [Kedaluwarsa kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration)). Di Claude Platform on AWS, ini juga dapat menunjukkan masalah pada kredensial AWS atau tanda tangan SigV4 Anda.

  Error 401 yang pesannya diawali dengan `CORS requests are not allowed for this Organization` bukanlah masalah pada kunci API Anda. Permintaan tersebut menyertakan header `Origin`, yang ditambahkan oleh browser, dan organisasi Anda tidak dapat memanggil Claude API langsung dari browser. Pesan tersebut berlanjut dengan `because of custom retention settings` atau `because of its settings`. Yang pertama hanya muncul untuk pengaturan retensi data seperti “zero data retention” (retensi data nol), atau ZDR; yang kedua adalah kasus umum, yang mencakup Compliance API. Tidak ada perubahan pada permintaan browser yang dapat memperbaikinya, jadi kirimkan permintaan dari back end Anda sendiri; lihat [Aplikasi berbasis browser](https://platform.claude.com/docs/id/manage-claude/authentication#browser-based-applications).

* 402 - `billing_error`: Terdapat masalah pada informasi penagihan atau pembayaran Anda. Periksa detail pembayaran Anda di [Claude Console](https://platform.claude.com), atau di AWS Marketplace jika Anda menggunakan Claude Platform on AWS.

* 403 - `permission_error`: Kunci API Anda tidak memiliki izin untuk menggunakan sumber daya yang ditentukan. Periksa akses organisasi dan pengaturan workspace Anda di [Claude Console](https://platform.claude.com).

* 404 - `not_found_error`: Sumber daya yang diminta tidak ditemukan. Periksa path endpoint dan ID sumber daya apa pun di URL permintaan.

* 409 - `conflict_error`: Permintaan bertentangan dengan status sumber daya saat ini. Misalnya, sumber daya dimodifikasi secara bersamaan, atau nilai yang harus unik sudah digunakan. Selesaikan konflik tersebut, lalu coba ulang permintaan.

* 413 - `request_too_large`: Permintaan melebihi jumlah byte maksimum yang diizinkan. Lihat [Batas ukuran permintaan](https://platform.claude.com/docs/id/api/errors#request-size-limits) untuk batas maksimum per endpoint.

* 429 - `rate_limit_error`: Organisasi Anda telah mencapai [“rate limit” (batas laju)](https://platform.claude.com/docs/id/api/rate-limits), mencapai batas pengeluaran bulanan tingkat penggunaannya, atau mencapai batas pengeluaran pada workspace Claude Code. Error 429 akibat batas pengeluaran tingkat tidak memiliki header `retry-after` dan akan terus gagal hingga akses dipulihkan; lihat [Mencapai batas pengeluaran Anda](https://platform.claude.com/docs/id/api/rate-limits#reaching-your-spend-cap) untuk cara mengenalinya. Peningkatan penggunaan yang tajam juga dapat menyebabkan error 429 meskipun Anda masih berada di bawah batas laju Anda; lihat [“Ramp limits” (batas ramp)](https://platform.claude.com/docs/id/api/rate-limits#ramp-limits).

  Untuk membedakan batas pengeluaran dari batas laju dalam kode, periksa [kode error](https://platform.claude.com/docs/id/api/errors#error-codes).

* 500 - `api_error`: Terjadi error tak terduga di dalam sistem Anthropic. Coba ulang hanya jika header `x-should-retry` pada respons tidak bernilai `false` (lihat [Percobaan ulang](https://platform.claude.com/docs/id/api/errors#retries)). Jika error berlanjut, hubungi dukungan dengan menyertakan [ID permintaan](https://platform.claude.com/docs/id/api/errors#request-id). Jika tipe error-nya justru `timeout_error`, lihat entri 504.

* 504 - `timeout_error`: Permintaan mengalami timeout saat diproses. API juga mengembalikan `timeout_error` dengan kode status lain, seperti 500 ketika permintaan mencapai batas waktu server sebelum respons dimulai. Untuk permintaan Messages API yang berjalan lama, gunakan [Messages API dengan streaming](https://platform.claude.com/docs/id/build-with-claude/streaming). Lihat [Permintaan panjang](https://platform.claude.com/docs/id/api/errors#long-requests) untuk opsi lainnya.

* 529 - `overloaded_error`: API sedang kelebihan beban untuk sementara.

  <Warning>
    Error 529 dapat terjadi ketika API mengalami lalu lintas tinggi di seluruh pengguna.
  </Warning>

Saat menerima respons [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming) melalui “server-sent events” (peristiwa yang dikirim server), atau SSE, error dapat terjadi setelah API mengembalikan respons 200. Dalam kasus tersebut, penanganan error tidak mengikuti mekanisme standar ini. Lihat [Event error](https://platform.claude.com/docs/id/build-with-claude/streaming#error-events) untuk bentuk error di tengah stream.

SDK tidak mencoba ulang error di dalam stream. Untuk menangkapnya, lihat [Menangani error dalam stream](https://platform.claude.com/docs/id/api/handle-errors#handle-an-error-in-a-stream).

### Percobaan ulang

Secara default, SDK mencoba ulang permintaan yang gagal hingga dua kali (total tiga percobaan). Untuk mengubah jumlah percobaan ulang, atur `max_retries` (typescript, php: `maxRetries`; java: `.maxRetries()`; csharp: `MaxRetries`; go: `option.WithMaxRetries()`) pada klien. Nilai `0` menonaktifkan percobaan ulang.

Untuk setiap percobaan yang gagal, SDK menentukan dua hal:

* **Apakah SDK mencoba ulang:** Jika respons memiliki header `x-should-retry` (`true` atau `false`), SDK mengikutinya. Jika tidak, SDK mencoba ulang error koneksi, timeout, serta status 408, 409, 429, dan 500 ke atas.
* **Berapa lama SDK menunggu:** Jika respons memiliki header `retry-after`, SDK menunggu selama yang dinyatakan oleh header tersebut. Jika tidak, SDK menggunakan exponential backoff dari 0,5 hingga 8 detik.

Go SDK mencoba ulang beberapa metode create dalam lebih sedikit kasus. Lihat [Percobaan ulang untuk metode create di Go SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go#retries-for-create-methods).

Tanpa SDK, ikuti `x-should-retry` dan `retry-after` dalam kode Anda sendiri, serta gunakan backoff dan batas percobaan ulang.

## Batas ukuran permintaan

Claude API pihak pertama menerapkan batas ukuran permintaan berikut. Untuk platform lain, lihat [ikhtisar API](https://platform.claude.com/docs/id/api/overview#request-size-limits).

| Tipe endpoint | Ukuran permintaan maksimum |
| ----- | ----- |
| Messages API | 128 MB |
| Token Counting API | 128 MB |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing) | 256 MB |
| [Files API](https://platform.claude.com/docs/id/build-with-claude/files) | 500 MB |

Jika Anda melebihi batas ini, Anda akan menerima error 413 `request_too_large`. Pada Claude API pihak pertama, Cloudflare mengembalikan error ini sebelum permintaan mencapai server API.

## Bentuk error

API selalu mengembalikan error sebagai JSON, dengan objek `error` tingkat atas yang selalu menyertakan nilai `type` dan `message`. Respons juga menyertakan field `request_id` untuk memudahkan pelacakan dan debugging. Misalnya:

```json JSON
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "The requested resource could not be found."
  },
  "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"
}
```

Berdasarkan [kebijakan pembuatan versi API](https://platform.claude.com/docs/id/api/versioning), nilai dalam objek-objek ini dapat bertambah, dan nilai `type` baru dapat muncul.

### Kode error

Beberapa error juga memiliki kode error di `error.details.error_code`. Satu `type` dapat mencakup beberapa penyebab, dan sebuah kode menyebutkan salah satunya.

Misalnya, mencapai batas laju dan mencapai [batas pengeluaran bulanan](https://platform.claude.com/docs/id/api/rate-limits#reaching-your-spend-cap) Anda sama-sama menyebabkan 429 `rate_limit_error`. Pada Messages API, respons batas pengeluaran menambahkan sebuah kode:

```json JSON
{
  "type": "error",
  "error": {
    "type": "rate_limit_error",
    "message": "You have reached your API usage limits: ...",
    "details": { "error_code": "enforced_spend_limit_reached" }
  },
  "request_id": "req_018EeWyXxfu5pfWkrYcMdjWG"
}
```

API lain yang mengembalikan 429 ini, seperti Claude Managed Agents, tidak menambahkan kode tersebut. Di sana, hanya `message` yang membedakan kedua penyebab itu, dan Anda sebaiknya tidak mencocokkannya dalam kode. Error 429 akibat batas pengeluaran akan terus gagal hingga akses dipulihkan, jadi batasi percobaan ulang Anda setelah 429.

Kumpulan kode dapat bertambah. Jika sebuah error tidak memiliki kode atau memiliki kode yang tidak Anda kenali, tangani berdasarkan `type` atau status HTTP-nya.

Untuk daftar lengkap kode, lihat [`ErrorDetails`](https://platform.claude.com/docs/id/api/$shared#error_details) di referensi API. Untuk menemukan kode yang dapat dikembalikan oleh suatu metode, lihat [Menangani kode error tertentu](https://platform.claude.com/docs/id/api/handle-errors#handle-a-specific-error-code).

## Tipe error SDK

Bagian ini mencantumkan apa yang perlu ditangkap atau diperiksa di SDK untuk setiap jenis error. Untuk menulis handler, lihat [Menangani error](https://platform.claude.com/docs/id/api/handle-errors).

<Tabs>
  <Tab title="Python">
    Kelas-kelas ini berada dalam paket `anthropic` kecuali jika suatu baris menyebutkan yang lain. Sebuah kelas juga menangkap subclass-nya, jadi letakkan kelas yang lebih sempit terlebih dahulu. Misalnya, `RateLimitError` juga menangkap `EnforcedSpendLimitReachedError`.

    | Untuk menangani | Tangkap |
    | ----- | ----- |
    | Satu [kode error](https://platform.claude.com/docs/id/api/errors#error-codes) | Kelasnya sendiri, seperti `anthropic.EnforcedSpendLimitReachedError` (lihat [Menangani kode error tertentu](https://platform.claude.com/docs/id/api/handle-errors#handle-a-specific-error-code)) |
    | 400 | `BadRequestError` |
    | 401 | `AuthenticationError` |
    | 403 | `PermissionDeniedError` |
    | 404 | `NotFoundError` |
    | 409 | `ConflictError` |
    | 413 | `ContentTooLargeError` |
    | 422 | `UnprocessableEntityError` |
    | 429 | `RateLimitError` |
    | 504 | `GatewayTimeoutError` |
    | 529 | `OverloadedError` |
    | Setiap 5xx, seperti 500, 504, dan 529 | `InternalServerError` |
    | Setiap respons error | `APIStatusError` |
    | Event error di dalam stream | `APIStatusError` |
    | Timeout klien (SDK berhenti menunggu) | `APITimeoutError` |
    | Setiap kegagalan koneksi sebelum respons tiba (termasuk timeout klien) | `APIConnectionError` |
    | Koneksi yang terputus atau macet di tengah stream | `httpx2.TransportError` (`httpx2` adalah library HTTP yang digunakan SDK) |
    | Setiap error dalam tabel ini kecuali stream yang terputus | `APIError` |

    Untuk status yang tidak memiliki baris, seperti 402, tangkap `APIStatusError` dan bandingkan `status_code`-nya.

    Untuk mengakses exception yang mendasarinya atau respons mentah, lihat [Menangani error di Python](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python#handling-errors).
  </Tab>

  <Tab title="TypeScript">
    Kelas-kelas ini adalah properti dari `Anthropic` kecuali jika suatu baris menyatakan lain. Sebuah kelas juga menangkap subclass-nya, jadi letakkan kelas yang lebih sempit terlebih dahulu. Misalnya, `RateLimitError` juga menangkap `EnforcedSpendLimitReachedError`.

    | Untuk menangani | Tangkap |
    | ----- | ----- |
    | Satu [kode error](https://platform.claude.com/docs/id/api/errors#error-codes) | Kelasnya sendiri, seperti `Anthropic.EnforcedSpendLimitReachedError` (lihat [Menangani kode error tertentu](https://platform.claude.com/docs/id/api/handle-errors#handle-a-specific-error-code)) |
    | 400 | `BadRequestError` |
    | 401 | `AuthenticationError` |
    | 403 | `PermissionDeniedError` |
    | 404 | `NotFoundError` |
    | 409 | `ConflictError` |
    | 413 | `ContentTooLargeError` |
    | 422 | `UnprocessableEntityError` |
    | 429 | `RateLimitError` |
    | 504 | `GatewayTimeoutError` |
    | 529 | `OverloadedError` |
    | Setiap 5xx, seperti 500, 504, dan 529 | `InternalServerError` |
    | Timeout klien (SDK berhenti menunggu) | `APIConnectionTimeoutError` |
    | Setiap kegagalan koneksi sebelum respons tiba (termasuk timeout klien) | `APIConnectionError` |
    | Koneksi yang terputus di tengah stream | `AnthropicError` dari `client.messages.stream()`. Dengan `stream: true`, tangkap error milik runtime itu sendiri, seperti `TypeError`. |
    | Event error di dalam stream | `APIError` |
    | Setiap error dalam tabel ini kecuali stream yang terputus | `APIError` |

    Untuk status yang tidak memiliki baris, seperti 402, tangkap `APIError` dan bandingkan `status`-nya.

    Untuk membaca header respons, lihat [Menangani error di TypeScript](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#handling-errors).
  </Tab>

  <Tab title="C#">
    Kelas-kelas ini berada dalam namespace `Anthropic.Exceptions` kecuali jika suatu baris menyebutkan yang lain. Sebuah kelas juga menangkap subclass-nya, jadi letakkan kelas yang lebih sempit terlebih dahulu. Misalnya, `AnthropicRateLimitException` juga menangkap `AnthropicEnforcedSpendLimitReachedException`.

    | Untuk menangani | Tangkap |
    | ----- | ----- |
    | Satu [kode error](https://platform.claude.com/docs/id/api/errors#error-codes) | Kelasnya sendiri, seperti `Anthropic.Models.AnthropicEnforcedSpendLimitReachedException` (lihat [Menangani kode error tertentu](https://platform.claude.com/docs/id/api/handle-errors#handle-a-specific-error-code)) |
    | 400 | `AnthropicBadRequestException` |
    | 401 | `AnthropicUnauthorizedException` |
    | 403 | `AnthropicForbiddenException` |
    | 404 | `AnthropicNotFoundException` |
    | 409 | `AnthropicConflictException` |
    | 413 | `AnthropicContentTooLargeException` |
    | 422 | `AnthropicUnprocessableEntityException` |
    | 429 | `AnthropicRateLimitException` |
    | 504 | `AnthropicGatewayTimeoutException` |
    | 529 | `AnthropicOverloadedException` |
    | Setiap 4xx | `Anthropic4xxException` |
    | Setiap 5xx, seperti 500, 504, dan 529 | `Anthropic5xxException` |
    | Setiap respons error | `AnthropicApiException` |
    | Event error di dalam stream | `AnthropicSseException` |
    | Setiap respons error dan setiap event error di dalam stream | `AnthropicServiceException` |
    | Kegagalan koneksi sebelum respons tiba | `AnthropicIOException` |
    | Koneksi yang terputus di tengah stream | `IOException` milik .NET sendiri, di `System.IO` |
    | Timeout klien (SDK berhenti menunggu) | `TaskCanceledException` milik .NET sendiri, di `System.Threading.Tasks` |
    | Setiap error dalam tabel ini kecuali timeout klien dan stream yang terputus | `AnthropicException` |

    Untuk status yang tidak memiliki barisnya sendiri, seperti 402, tangkap `Anthropic4xxException` dan bandingkan `StatusCode`-nya.
  </Tab>

  <Tab title="Go">
    Go SDK memiliki satu tipe error, yaitu `*anthropic.Error`. Anda membandingkan field-nya alih-alih menangkap sebuah kelas. Dalam tabel ini, `apierr` adalah variabel `*anthropic.Error` yang diisi oleh `errors.As()`.

    | Untuk menangani | Periksa |
    | ----- | ----- |
    | Satu [kode error](https://platform.claude.com/docs/id/api/errors#error-codes) | `apierr.ErrorCode() == anthropic.ErrorCodeEnforcedSpendLimitReached` |
    | Satu status HTTP | `apierr.StatusCode == http.StatusTooManyRequests` |
    | Setiap respons error | `errors.As(err, &apierr)` |
    | Event error di dalam stream | `errors.As(stream.Err(), &apierr)` |
    | Kegagalan koneksi, timeout klien, atau koneksi yang terputus di tengah stream | `err` lain apa pun yang bukan `nil` |

    Setiap kode error memiliki konstantanya sendiri (lihat [Menangani kode error tertentu](https://platform.claude.com/docs/id/api/handle-errors#handle-a-specific-error-code)).

    Untuk mencetak permintaan dan respons mentah dari `*anthropic.Error`, lihat [Penanganan error di Go](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go#error-handling).
  </Tab>

  <Tab title="Java">
    Kelas-kelas ini berada dalam paket `com.anthropic.errors` kecuali jika suatu baris menyebutkan yang lain. Sebuah kelas juga menangkap subclass-nya, jadi letakkan kelas yang lebih sempit terlebih dahulu. Misalnya, `RateLimitException` juga menangkap `EnforcedSpendLimitReachedException`.

    | Untuk menangani | Tangkap |
    | ----- | ----- |
    | Satu [kode error](https://platform.claude.com/docs/id/api/errors#error-codes) | Kelasnya sendiri, seperti `com.anthropic.models.EnforcedSpendLimitReachedException` (lihat [Menangani kode error tertentu](https://platform.claude.com/docs/id/api/handle-errors#handle-a-specific-error-code)) |
    | 400 | `BadRequestException` |
    | 401 | `UnauthorizedException` |
    | 403 | `PermissionDeniedException` |
    | 404 | `NotFoundException` |
    | 409 | `ConflictException` |
    | 413 | `ContentTooLargeException` |
    | 422 | `UnprocessableEntityException` |
    | 429 | `RateLimitException` |
    | 504 | `GatewayTimeoutException` |
    | 529 | `OverloadedException` |
    | Setiap 5xx, seperti 500, 504, dan 529 | `InternalServerException` |
    | Event error di dalam stream | `SseException` |
    | Setiap respons error dan setiap event error di dalam stream | `AnthropicServiceException` |
    | Kegagalan koneksi, timeout klien, atau koneksi yang terputus di tengah stream | `AnthropicIoException` |
    | Setiap error dalam tabel ini | `AnthropicException` |

    Untuk status yang tidak memiliki baris, seperti 402, tangkap `AnthropicServiceException` dan bandingkan `statusCode()`-nya.

    `errorCode()` dan `type()` pada error masing-masing mengembalikan `Optional`.

    Untuk membaca header respons, lihat [Penanganan error di Java](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#error-handling).
  </Tab>

  <Tab title="PHP">
    Kelas-kelas ini berada dalam namespace `Anthropic\Core\Exceptions` kecuali jika suatu baris menyebutkan yang lain. Sebuah kelas juga menangkap subclass-nya, jadi letakkan kelas yang lebih sempit terlebih dahulu. Misalnya, `RateLimitException` juga menangkap `EnforcedSpendLimitReachedException`.

    | Untuk menangani | Tangkap |
    | ----- | ----- |
    | Satu [kode error](https://platform.claude.com/docs/id/api/errors#error-codes) | Kelasnya sendiri, seperti `Anthropic\EnforcedSpendLimitReachedException` (lihat [Menangani kode error tertentu](https://platform.claude.com/docs/id/api/handle-errors#handle-a-specific-error-code)) |
    | 400 | `BadRequestException` |
    | 401 | `AuthenticationException` |
    | 403 | `PermissionDeniedException` |
    | 404 | `NotFoundException` |
    | 409 | `ConflictException` |
    | 413 | `ContentTooLargeException` |
    | 422 | `UnprocessableEntityException` |
    | 429 | `RateLimitException` |
    | 504 | `GatewayTimeoutException` |
    | 529 | `OverloadedException` |
    | Setiap 5xx, seperti 500, 504, dan 529 | `InternalServerException` |
    | Setiap respons error | `APIStatusException` |
    | Event error di dalam stream | `APIStatusException` |
    | Kegagalan koneksi sebelum respons tiba atau timeout klien | `APIConnectionException` |
    | Koneksi yang terputus di tengah stream | Exception milik klien HTTP itu sendiri atau tidak ada (lihat paragraf setelah tabel ini). Dengan Guzzle 7, reset koneksi memunculkan `\RuntimeException` milik PHP. |
    | Setiap error dalam tabel ini kecuali stream yang terputus | `APIException` |

    Jika server menutup koneksi di tengah stream, stream berakhir tanpa error. Periksa apakah event `message_stop` telah tiba.

    Untuk status yang tidak memiliki baris, seperti 402, tangkap `APIStatusException` dan bandingkan `status`-nya.

    Untuk mengakses exception yang mendasarinya, lihat [Penanganan error di PHP](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php#error-handling).
  </Tab>

  <Tab title="Ruby">
    Kelas-kelas ini berada dalam modul `Anthropic::Errors` kecuali jika suatu baris menyebutkan yang lain. Sebuah kelas juga menangkap subclass-nya, jadi letakkan kelas yang lebih sempit terlebih dahulu. Misalnya, `RateLimitError` juga menangkap `EnforcedSpendLimitReachedError`.

    | Untuk menangani | Tangkap |
    | ----- | ----- |
    | Satu [kode error](https://platform.claude.com/docs/id/api/errors#error-codes) | Kelasnya sendiri, seperti `Anthropic::EnforcedSpendLimitReachedError` (lihat [Menangani kode error tertentu](https://platform.claude.com/docs/id/api/handle-errors#handle-a-specific-error-code)) |
    | 400 | `BadRequestError` |
    | 401 | `AuthenticationError` |
    | 403 | `PermissionDeniedError` |
    | 404 | `NotFoundError` |
    | 409 | `ConflictError` |
    | 413 | `ContentTooLargeError` |
    | 422 | `UnprocessableEntityError` |
    | 429 | `RateLimitError` |
    | 504 | `GatewayTimeoutError` |
    | 529 | `OverloadedError` |
    | Setiap 5xx, seperti 500, 504, dan 529 | `InternalServerError` |
    | Setiap respons error | `APIStatusError` |
    | Event error di dalam stream | `APIStatusError` |
    | Timeout klien (SDK berhenti menunggu) | `APITimeoutError` |
    | Setiap kegagalan koneksi (termasuk timeout klien dan koneksi yang terputus di tengah stream) | `APIConnectionError` |
    | Setiap error dalam tabel ini | `APIError` |

    Untuk status yang tidak memiliki baris, seperti 402, tangkap `APIStatusError` dan bandingkan `status`-nya.

    `error_code` dan `type` pada error adalah simbol.

    Untuk mengakses exception yang mendasarinya, lihat [Menangani error di Ruby](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/ruby#handling-errors).
  </Tab>
</Tabs>

Tabel ini didasarkan pada status HTTP dan kode error, bukan pada `error.type`:

* Error 503 dengan `overloaded_error` dihitung sebagai 5xx, bukan sebagai 529.
* Event error di dalam stream tidak pernah cocok dengan baris status atau kelas suatu kode. Status HTTP-nya adalah 200 milik stream atau tidak ada.

Untuk menangani berdasarkan `error.type`, periksa `type` (csharp: `Type`; go: `Type()`; java: `type()`; php: `getType()`) pada error, seperti dalam [Menangani error dalam stream](https://platform.claude.com/docs/id/api/handle-errors#handle-an-error-in-a-stream).

## ID permintaan

Setiap respons API menyertakan header `request-id` yang unik. Header ini berisi nilai seperti `req_018EeWyXxfu5pfWkrYcMdjWG`. Pengenal yang sama muncul sebagai field `request_id` dalam [body respons error](https://platform.claude.com/docs/id/api/errors#error-shapes). Saat menghubungi dukungan mengenai permintaan tertentu, sertakan ID ini untuk membantu menyelesaikan masalah Anda dengan cepat.

Pada [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), respons menyertakan dua ID permintaan: ID permintaan AWS (`x-amzn-requestid`, primer, diindeks di CloudTrail) dan ID permintaan Anthropic (`request-id`, sekunder). Gunakan ID permintaan AWS untuk pencarian CloudTrail dan ID permintaan Anthropic untuk tiket dukungan Anthropic.

Ketika API mengembalikan respons error, baca ID dari error SDK, di `request_id` (typescript: `requestID`; csharp, go: `RequestID`; java: `requestId()`; php: `getRequestID()`). Untuk contohnya, lihat [Menangkap error berdasarkan jenisnya](https://platform.claude.com/docs/id/api/handle-errors#catch-errors-by-kind). Ketika permintaan berhasil, baca ID dari respons.

SDK Python dan TypeScript menyediakan ID permintaan sebagai properti `_request_id` pada objek respons tingkat teratas. SDK C#, Go, Java, dan PHP menyediakannya melalui accessor respons mentah masing-masing, sedangkan SDK Ruby menyediakannya melalui [middleware](https://platform.claude.com/docs/id/cli-sdks-libraries/middleware). Di semua SDK kecuali Ruby, gunakan `with_raw_response` (typescript: `.withResponse()`; java: `.withRawResponse()`; csharp: `WithRawResponse`; go: `option.WithResponseInto()`; php: `->raw`) untuk membaca [header respons](https://platform.claude.com/docs/id/api/overview#response-headers) lainnya, seperti `anthropic-organization-id` dan [`anthropic-workspace-id`](https://platform.claude.com/docs/id/manage-claude/workspaces#identify-the-workspace-behind-an-api-response). Di Ruby, gunakan middleware yang sama. Di Claude Platform on AWS, gunakan juga accessor respons mentah untuk membaca ID permintaan AWS (`x-amzn-requestid`):

<CodeGroup>
  ```bash cURL
  # -i mencetak header respons, termasuk request-id, sebelum body
  curl -sS -i https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  # Header request-id dicetak ke stderr dengan --debug:
  ant --debug messages create \
    --model claude-sonnet-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-sonnet-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(f"Request ID: {message._request_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  console.log("Request ID:", message._request_id);
  ```

  ```csharp C#
  AnthropicClient client = new();

  using var response = await client.WithRawResponse.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 1024,
      Messages = [new UserMessageParam { Content = "Hello, Claude" }]
  });
  Console.WriteLine($"Request ID: {response.RequestID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  var response *http.Response
  _, err := client.Messages.New(
  	context.Background(),
  	anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeSonnet5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  		},
  	},
  	option.WithResponseInto(&response),
  )
  if err != nil {
  	panic(err)
  }

  fmt.Println("Request ID:", response.Header.Get("request-id"))
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.http.HttpResponseFor;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      HttpResponseFor<Message> response = client.messages().withRawResponse().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_5)
              .maxTokens(1024)
              .addUserMessage("Hello, Claude")
              .build()
      );

      IO.println("Request ID: " + response.requestId().orElse(null));
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->raw->create([
      'model' => 'claude-sonnet-5',
      'maxTokens' => 1024,
      'messages' => [['role' => 'user', 'content' => 'Hello, Claude']],
  ]);
  echo 'Request ID: ' . $response->getHeaderLine('request-id') . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Baca header respons di middleware per-permintaan, yang menerima
  # respons HTTP mentah sebelum SDK mem-parsing-nya
  request_id = nil
  read_request_id = lambda do |request, call_next|
    response = call_next.call(request)
    # Kunci dalam response.headers menggunakan huruf kecil
    request_id = response.headers["request-id"]
    response
  end

  client.messages.create(
    model: Anthropic::Model::CLAUDE_SONNET_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    request_options: { middleware: [read_request_id] }
  )
  puts "Request ID: #{request_id}"
  ```

  ```python Python (Claude Platform on AWS)
  from anthropic import AnthropicAWS

  client = AnthropicAWS(aws_region="us-west-2")

  response = client.messages.with_raw_response.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(f"AWS request ID: {response.headers.get('x-amzn-requestid')}")
  message = response.parse()
  print(f"Anthropic request ID: {message._request_id}")
  ```

  ```typescript TypeScript (Claude Platform on AWS)
  import AnthropicAws from "@anthropic-ai/aws-sdk";

  const client = new AnthropicAws({ awsRegion: "us-west-2" });

  const { response: raw, request_id } = await client.messages
    .create({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    })
    .withResponse();
  console.log("AWS request ID:", raw.headers.get("x-amzn-requestid"));
  console.log("Anthropic request ID:", request_id);
  ```
</CodeGroup>

Untuk contoh ID permintaan Claude Platform on AWS dalam bahasa lain, lihat [ID permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#request-ids).

## Permintaan panjang

<Warning>
  Pertimbangkan untuk menggunakan [Messages API dengan streaming](https://platform.claude.com/docs/id/build-with-claude/streaming) atau [Message Batches API](https://platform.claude.com/docs/id/api/messages/batches/create) untuk permintaan yang berjalan lama, terutama yang lebih dari 10 menit.
</Warning>

Hindari menetapkan nilai `max_tokens` yang besar tanpa menggunakan [Messages API dengan streaming](https://platform.claude.com/docs/id/build-with-claude/streaming) atau [Message Batches API](https://platform.claude.com/docs/id/api/messages/batches/create):

* Beberapa jaringan mungkin memutus koneksi yang menganggur setelah periode waktu yang bervariasi, yang dapat menyebabkan permintaan gagal atau mengalami timeout tanpa menerima respons dari Anthropic.
* Keandalan jaringan berbeda-beda. [Message Batches API](https://platform.claude.com/docs/id/api/messages/batches/create) dapat membantu Anda mengelola risiko masalah jaringan dengan memungkinkan Anda melakukan polling untuk hasil alih-alih memerlukan koneksi jaringan yang tidak terputus.

Jika Anda membangun integrasi API langsung, menetapkan [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/programming.html) dapat mengurangi dampak timeout koneksi idle pada beberapa jaringan.

[Anthropic SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) memvalidasi bahwa permintaan Messages API non-streaming Anda tidak diperkirakan melebihi timeout 10 menit. SDK juga menetapkan opsi socket untuk TCP keep-alive.

Jika Anda tidak perlu memproses event secara bertahap, SDK dapat mengonsumsi stream untuk Anda dan mengembalikan objek `Message` lengkap, identik dengan yang dikembalikan oleh panggilan non-streaming:

<CodeGroup exclude="shell:cURL">
  <CodeGroupItem language="cURL">
    Permintaan curl mencetak event stream mentah dan tidak dapat menggabungkannya menjadi pesan akhir. Untuk mendapatkan objek `Message` lengkap dari stream, gunakan [Anthropic SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview).
  </CodeGroupItem>

  ```bash CLI
  # CLI melakukan streaming event; --format jsonl mengeluarkan satu event per baris
  ant messages create --stream --format jsonl <<'YAML'
  model: claude-sonnet-5
  max_tokens: 128000
  messages:
    - role: user
      content: Write a detailed analysis...
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      max_tokens=128000,
      messages=[{"role": "user", "content": "Write a detailed analysis..."}],
      model="claude-sonnet-5",
  ) as stream:
      message = stream.get_final_message()

  print(next(block.text for block in message.content if block.type == "text"))
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    max_tokens: 128000,
    messages: [{ role: "user", content: "Write a detailed analysis..." }],
    model: "claude-sonnet-5"
  });

  const message = await stream.finalMessage();
  const textBlock = message.content.find((block) => block.type === "text");
  if (textBlock && textBlock.type === "text") {
    console.log(textBlock.text);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 128000,
      Messages = [new UserMessageParam { Content = "Write a detailed analysis..." }]
  };

  var message = await client.Messages.CreateStreaming(parameters).Aggregate();
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5,
  	MaxTokens: 128000,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Write a detailed analysis...")),
  	},
  })

  message := anthropic.Message{}
  for stream.Next() {
  	event := stream.Current()
  	if err := message.Accumulate(event); err != nil {
  		log.Fatal(err)
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }

  for _, block := range message.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  		break
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.helpers.MessageAccumulator;
  import com.anthropic.models.messages.ContentBlock;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_5)
          .maxTokens(128000L)
          .addUserMessage("Write a detailed analysis...")
          .build();

      MessageAccumulator accumulator = MessageAccumulator.create();
      try (var streamResponse = client.messages().createStreaming(params)) {
          streamResponse.stream().forEach(accumulator::accumulate);
      }

      Message message = accumulator.message();
      message.content().stream()
          .filter(ContentBlock::isText)
          .findFirst()
          .flatMap(ContentBlock::text)
          .ifPresent(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  use Anthropic\Lib\Streaming\MessageAccumulator;

  $client = new Client();

  $stream = $client->messages->createStream(
      model: 'claude-sonnet-5',
      maxTokens: 128000,
      messages: [['role' => 'user', 'content' => 'Write a detailed analysis...']],
  );

  $accumulator = MessageAccumulator::forMessages();
  foreach ($stream as $event) {
      $accumulator->accumulate($event);
  }

  echo array_find($accumulator->message()->content, static fn ($block): bool => $block->type === 'text')->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.stream(
    model: Anthropic::Model::CLAUDE_SONNET_5,
    max_tokens: 128000,
    messages: [{ role: "user", content: "Write a detailed analysis..." }]
  ).accumulated_message

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

Lihat [Mendapatkan pesan akhir tanpa menangani peristiwa](https://platform.claude.com/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detail lebih lanjut.

## Error validasi umum

### Prefill tidak didukung

Model Claude 4.6 dan yang lebih baru serta [Claude Mythos Preview](https://anthropic.com/glasswing) tidak mendukung “prefill” (pengisian awal) pesan asisten. Mengirim permintaan dengan pesan asisten terakhir yang di-prefill ke salah satu model ini akan mengembalikan 400 `invalid_request_error`:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "This model does not support assistant message prefill. The conversation must end with a user message."
  }
}
```

Gunakan [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) pada model yang mendukungnya, instruksi prompt sistem, atau [`output_config.format`](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#usage) sebagai gantinya.

### Blok thinking tidak dapat dimodifikasi

Jika blok thinking dalam permintaan tidak cocok dengan yang dikembalikan oleh API, permintaan dapat mendapatkan 400 `invalid_request_error`. Pesan error dimulai dengan posisi blok yang bermasalah (misalnya, `messages.1.content.0`) dan berisi:

```text wrap
`thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified. These blocks must remain as they were in the original response.
```

Dengan “tool use” (penggunaan alat), kirim kembali setiap blok `thinking` dan `redacted_thinking` dari giliran asisten persis seperti yang diterima, termasuk blok yang field `thinking`-nya kosong. Jika aplikasi Anda menyaring blok konten berdasarkan tipe sebelum mengirim ulang, sertakan `thinking` dan `redacted_thinking`. Ini adalah kegagalan yang berbeda dari [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check), yang error-nya menyatakan bahwa sebuah blok terikat ke percakapan lain. Mengatur `prefix_mismatch_behavior` mungkin tidak mengatasinya. Lihat [perbaikan untuk blok thinking yang dimodifikasi](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-blocks-modified) di Pemecahan masalah thinking.

### Pemikiran diperpanjang tidak didukung

Model Claude 4.7 dan yang lebih baru tidak mendukung “extended thinking” (pemikiran diperpanjang). Mengirim `thinking: {"type": "enabled"}` ke salah satu model ini akan mengembalikan 400 `invalid_request_error`:

```text wrap
"thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

Sebagai gantinya, gunakan [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking). Untuk pemetaan parameternya, lihat [Migrasi ke pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking). Untuk memperbaiki error berdasarkan gejalanya, lihat [Error 400 menyatakan `"thinking.type.enabled"` tidak didukung](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-enabled).

### Pemikiran adaptif tidak didukung

Model yang hanya mendukung pemikiran diperpanjang (model Claude 4.5 dan yang lebih lama) menolak `thinking: {"type": "adaptive"}` dengan 400 `invalid_request_error`:

```text wrap
adaptive thinking is not supported on this model
```

Gunakan `thinking: {"type": "enabled", "budget_tokens": N}` pada model-model ini; lihat [Pemikiran diperpanjang](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) untuk konfigurasinya dan [perbaikan berbasis gejala untuk error pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-adaptive) di Pemecahan masalah thinking.

### Thinking tidak dapat dinonaktifkan

Pada Claude Fable 5.2, [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview), Claude Fable 5.1, [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview), Claude Fable 5, [Claude Mythos 5](https://platform.claude.com/docs/id/models/mythos-5/overview), Claude Opus 5.5, dan [Claude Mythos Preview](https://anthropic.com/glasswing), thinking selalu aktif. Mengirim `thinking: {"type": "disabled"}` ke salah satu model ini akan mengembalikan 400 `invalid_request_error`. Pada semua model ini kecuali Claude Mythos Preview, pesannya berbunyi:

```text wrap
"thinking.type.disabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

Pada Claude Mythos Preview, satu-satunya model di antara model-model ini yang menerima pemikiran diperpanjang, pesannya berbunyi:

```text wrap
"thinking.type.disabled" is not supported for this model. Thinking defaults to adaptive mode when not specified; use "thinking.type.enabled" with "budget_tokens" for extended thinking.
```

Pada Claude Sonnet 5.5, thinking tidak dapat diatur ke `disabled`. Gunakan `thinking: {"type": "between_tools"}` untuk pengaturan thinking terendah, yang menonaktifkan thinking di awal. Mengirim `thinking: {"type": "disabled"}` akan mengembalikan 400 `invalid_request_error` dengan pesan ini:

```text wrap
To turn thinking off on this model, send "thinking": {"type": "between_tools"} instead of {"type": "disabled"}. The model does not think before responding. The short updates it writes between tool calls come back as thinking blocks.
```

Pada [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `xhigh` atau `max`, permintaan dengan `between_tools` juga mengembalikan 400 `invalid_request_error`. Pesan error menyatakan bahwa thinking dinonaktifkan karena `between_tools` tidak memiliki thinking di awal:

```text wrap
output_config.effort 'xhigh' is not supported when thinking is disabled on this model. Use effort 'high' or below, or enable thinking.
```

Dengan `between_tools`, effort tidak dapat berubah di tengah percakapan: `output_config.effort` per pesan yang berbeda dari level yang sedang berlaku akan mengembalikan error 400. Error tersebut menyebutkan posisi pesan yang menetapkan level baru:

```text wrap
messages.N: output_config.effort 'low' differs from the 'high' in effect before it; effort cannot change when thinking is disabled on this model. Use effort 'high', or enable thinking.
```

Claude Haiku 5.5 menerima `thinking: {"type": "disabled"}` dan menerapkan dua batas effort yang sama yang berlaku untuk `between_tools`: pada effort `xhigh` atau `max`, atau dengan `output_config.effort` per pesan yang berbeda dari level yang berlaku, permintaan akan mengembalikan error 400 `invalid_request_error` dengan pesan yang sesuai seperti yang ditunjukkan sebelumnya.

Dalam kedua pesan tersebut, “enable thinking” berarti pemikiran adaptif: hilangkan field `thinking` atau kirim `thinking: {"type": "adaptive"}`. Claude Sonnet 5.5 dan Claude Haiku 5.5 juga menolak `"enabled"` dengan error 400. Untuk memvariasikan effort di setiap giliran, gunakan pemikiran adaptif.

Mengirim `thinking: {"type": "between_tools"}` ke model apa pun selain Claude Sonnet 5.5 akan mengembalikan 400 `invalid_request_error`:

```text wrap
"thinking.type.between_tools" is not supported for this model.
```

Untuk perbaikannya, lihat [error `between_tools` dan effort](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-between-tools) di Pemecahan masalah thinking.

Hilangkan parameter `thinking` dan permintaan akan berjalan dengan pemikiran adaptif. Untuk menjaga konten thinking agar tidak muncul dalam respons tanpa menonaktifkan thinking, atur `display: "omitted"` pada konfigurasi thinking. Lihat [perbaikan untuk error thinking yang dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-disabled) di Pemecahan masalah thinking.

### Penggunaan alat paksa tidak didukung

Claude Fable 5.2, [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview), Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, dan [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview) tidak mendukung penggunaan alat paksa. Mengirim `tool_choice: {"type": "any"}` atau `tool_choice: {"type": "tool", "name": "..."}` ke salah satu model ini, termasuk pada [endpoint penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting), akan mengembalikan 400 `invalid_request_error`:

```text wrap
tool_choice: type "tool" and "any" are not supported for this model.
```

`tool_choice: {"type": "auto"}` (default) dan `{"type": "none"}` diterima. Gunakan `auto` dengan [penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) untuk menjaga input alat tetap valid sesuai skema, atau [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) ketika Anda membutuhkan respons itu sendiri dalam bentuk JSON yang tetap. Lihat [Memaksa penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use).

### Versi alat penggunaan komputer tidak didukung

Claude Fable 5.2, Claude Mythos 5.2, Claude Opus 5.5, Claude Sonnet 5.5, dan Claude Haiku 5.5 mengembalikan error 400 untuk versi alat [penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) apa pun yang tidak mereka terima. Di Claude API, itu termasuk `computer_20251124` dengan header beta-nya. Model-model ini tidak menerima `computer_20250124` di platform mana pun. Pesan `invalid_request_error` dari Claude API menyebutkan jenis yang ditolak dan, setelah `Did you mean one of`, mencantumkan jenis alat yang diterima model. Untuk Claude Opus 5.5, pesannya dimulai dengan:

```text wrap
'claude-opus-5-5' does not support tool types: computer_20251124.
```

Claude API mengembalikan pesan yang sama untuk jenis alat yang didefinisikan Anthropic apa pun yang tidak didukung oleh model yang diminta. Claude Fable 5.2, Claude Mythos 5.2, Claude Opus 5.5, Claude Sonnet 5.5, dan Claude Haiku 5.5 mendukung penggunaan komputer melalui toolset `computer_toolset_20260801`. Deklarasikan `{"type": "computer_toolset_20260801"}` tanpa header beta dan perbarui loop agen Anda seperti yang dijelaskan di [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124). Untuk beralih dari `computer_20250124`, lihat [Pindahkan penggunaan komputer ke toolset](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#computer-use-toolset) di panduan migrasi Claude Haiku 5.5.

Di Amazon Bedrock, Claude Fable 5.2, Claude Mythos 5.2, Claude Opus 5.5, Claude Sonnet 5.5, dan Claude Haiku 5.5 juga menerima alat `computer_20251124` dengan header beta `computer-use-2025-11-24`. Dengan InvokeModel API dari Amazon Bedrock, kirim `computer-use-2025-11-24` dalam array `anthropic_beta` pada body permintaan alih-alih di header. Untuk API tersebut, lihat [Claude di Amazon Bedrock (`bedrock-runtime`)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy). Untuk model yang digunakan dengan setiap versi sebelumnya, lihat [Versi alat sebelumnya](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#earlier-tool-versions).

### Blok thinking yang terikat ke percakapan yang berbeda

Error 400 `invalid_request_error` ini berarti blok thinking yang Anda kirim kembali gagal dalam [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check). Bandingkan `system`, `tools`, dan pesan-pesan sebelum blok tersebut dengan yang Anda kirim ketika model menghasilkannya. Untuk mengetahui perubahan mana yang berpengaruh, lihat [Apa yang dihitung sebagai perubahan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#what-counts-as-an-edit). Pesan error diawali dengan posisi blok pertama yang gagal dalam pemeriksaan prefiks:

```text wrap
messages.{i}.content.{j}: Invalid `signature` in `thinking` block. The block is bound to a different conversation. Remove the block, or set `thinking.block_binding.prefix_mismatch_behavior` to "drop_block".
```

Mengirim ulang riwayat yang sama akan gagal dengan cara yang sama. Memperbaiki kode yang melakukan pengeditan tidak membantu percakapan ini jika pengeditan tersebut masih ada dalam riwayatnya. Untuk melanjutkan, lakukan salah satu dari berikut ini:

* Kirim header beta `thinking-binding-controls-2026-08-01` dan atur `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"`, pada percobaan ulang dan pada setiap permintaan berikutnya dalam percakapan tersebut. Pada Claude Sonnet 5.5 dan Claude Haiku 5.5, `block_binding` hanya berfungsi dengan `thinking: {"type": "adaptive"}`.
* Hapus blok yang disebutkan oleh error tersebut serta setiap blok `thinking` dan `redacted_thinking` setelahnya, dalam pesan tersebut dan dalam setiap pesan berikutnya. Coba ulang, dan jangan sertakan blok yang dihapus dalam permintaan berikutnya.

Untuk mencegah percakapan baru gagal, [pertahankan riwayat agar bersifat append-only (hanya ditambahkan)](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#what-to-check). Lihat [perbaikan untuk tanda tangan blok thinking yang tidak valid](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-block-signature) di Pemecahan masalah thinking.

Mengirim `thinking.block_binding` tanpa [header beta](https://platform.claude.com/docs/id/api/beta-headers) `thinking-binding-controls-2026-08-01` akan mengembalikan 400 `invalid_request_error` yang pesannya diakhiri dengan:

```text wrap
block_binding: Extra inputs are not permitted
```

Tambahkan header tersebut, aktifkan thinking, atau hapus field-nya.

### Outbound web identity federation dinonaktifkan (Claude Platform on AWS)

Jika setiap permintaan ke [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) mengembalikan `"Outbound web identity federation is disabled for your account"`, jalankan `aws iam enable-outbound-web-identity-federation` satu kali untuk setiap akun AWS. Lihat [Mengaktifkan outbound web identity federation](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#enable-outbound-web-identity-federation) untuk detailnya.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Pemecahan masalah thinking" icon="wrench" href="https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting">
    Perbaikan berbasis gejala untuk error 400 konfigurasi thinking, blok thinking kosong, dan penghentian `max_tokens`.
  </Card>

  <Card title="Batas laju" icon="gauge" href="https://platform.claude.com/docs/id/api/rate-limits">
    Untuk mengurangi penyalahgunaan dan mengelola kapasitas pada API, terdapat batasan seberapa banyak suatu organisasi dapat menggunakan Claude API.
  </Card>

  <Card title="Menangani error" icon="code" href="https://platform.claude.com/docs/id/api/handle-errors">
    Gunakan SDK untuk menangkap error Claude API berdasarkan kode error, status HTTP, atau kegagalan koneksi, dan untuk menangani error yang datang dalam stream.
  </Card>
</CardGroup>
