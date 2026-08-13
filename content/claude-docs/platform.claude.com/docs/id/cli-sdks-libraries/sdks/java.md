---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 2a310053515e4c7604eb31886a205c0380db2618ac7489a0522dad39d8a4c450
---

---
title: Java SDK
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java
description: Instal dan konfigurasikan Anthropic Java SDK dengan pola builder dan dukungan async
---

Anthropic Java SDK menyediakan akses yang mudah ke Anthropic REST API dari aplikasi yang ditulis dalam Java. SDK ini menggunakan pola builder untuk membuat permintaan dan mendukung operasi sinkron maupun asinkron.

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](https://platform.claude.com/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK yang spesifik untuk Java.
</Info>

## Instalasi

<Tabs>
  <Tab title="Gradle">
    ```kotlin
    implementation("com.anthropic:anthropic-java:2.53.0")
    ```
  </Tab>

  <Tab title="Maven">
    ```xml
    <dependency>
        <groupId>com.anthropic</groupId>
        <artifactId>anthropic-java</artifactId>
        <version>2.53.0</version>
    </dependency>
    ```
  </Tab>
</Tabs>

## Persyaratan

Library ini memerlukan Java 8 atau yang lebih baru.

<Note>
  SDK ini mendukung Java 8 dan yang lebih baru. Contoh kode dalam dokumentasi ini ditulis sebagai [compact source files JDK 25](https://openjdk.org/jeps/512), menggunakan entry point `void main()` sederhana dan `IO.println()` untuk output. Pemanggilan API itu sendiri identik pada setiap JDK yang didukung; untuk mengompilasi contoh pada versi yang lebih lama, ganti `IO.println(...)` dengan `System.out.println(...)` dan tempatkan isinya di dalam `public static void main(String[] args)` dalam sebuah class.
</Note>

## Mulai cepat

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

// Mengonfigurasi menggunakan properti sistem `anthropic.apiKey`, `anthropic.authToken`, dan `anthropic.baseUrl`
// Atau mengonfigurasi menggunakan variabel lingkungan `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, dan `ANTHROPIC_BASE_URL`
AnthropicClient client = AnthropicOkHttpClient.fromEnv();

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_5)
  .build();

Message message = client.messages().create(params);
```

## Konfigurasi client

### Pengaturan kunci API

Konfigurasikan client menggunakan system properties atau variabel lingkungan:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

// Mengonfigurasi menggunakan properti sistem `anthropic.apiKey`, `anthropic.authToken`, dan `anthropic.baseUrl`
// Atau mengonfigurasi menggunakan variabel lingkungan `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, dan `ANTHROPIC_BASE_URL`
AnthropicClient client = AnthropicOkHttpClient.fromEnv();
```

Atau konfigurasikan secara manual:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .apiKey("my-anthropic-api-key")
  .build();
```

Atau gunakan kombinasi kedua pendekatan:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  // Mengonfigurasi menggunakan properti sistem atau variabel lingkungan
  .fromEnv()
  .apiKey("my-anthropic-api-key")
  .build();
```

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication).

### Opsi konfigurasi

| Setter      | System property       | Variabel lingkungan    | Wajib | Nilai default                 |
| ----------- | --------------------- | ---------------------- | ----- | ----------------------------- |
| `apiKey`    | `anthropic.apiKey`    | `ANTHROPIC_API_KEY`    | false | -                             |
| `authToken` | `anthropic.authToken` | `ANTHROPIC_AUTH_TOKEN` | false | -                             |
| `baseUrl`   | `anthropic.baseUrl`   | `ANTHROPIC_BASE_URL`   | true  | `"https://api.anthropic.com"` |

System properties memiliki prioritas lebih tinggi daripada variabel lingkungan.

<Tip>
  Jangan membuat lebih dari satu client dalam aplikasi yang sama. Setiap client memiliki connection pool dan thread pool, yang lebih efisien jika dibagikan antar permintaan.
</Tip>

### Memodifikasi konfigurasi

Untuk menggunakan konfigurasi client yang dimodifikasi secara sementara sambil tetap menggunakan connection pool dan thread pool yang sama, panggil `withOptions()` pada client atau service mana pun:

```java
import com.anthropic.client.AnthropicClient;

AnthropicClient clientWithOptions = client.withOptions(optionsBuilder -> {
  optionsBuilder.baseUrl("https://example.com");
  optionsBuilder.maxRetries(42);
});
```

Metode `withOptions()` tidak memengaruhi client atau service asli.

## Penggunaan async

Client default bersifat sinkron. Untuk beralih ke eksekusi asinkron, panggil metode `async()`:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

AnthropicClient client = AnthropicOkHttpClient.fromEnv();

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_5)
  .build();

CompletableFuture<Message> message = client.async().messages().create(params);
```

Atau buat client asinkron sejak awal:

```java
import com.anthropic.client.AnthropicClientAsync;
import com.anthropic.client.okhttp.AnthropicOkHttpClientAsync;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

AnthropicClientAsync client = AnthropicOkHttpClientAsync.fromEnv();

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_5)
  .build();

CompletableFuture<Message> message = client.messages().create(params);
```

Client asinkron mendukung opsi yang sama dengan client sinkron, kecuali sebagian besar metode mengembalikan `CompletableFuture`.

## Streaming

SDK mendefinisikan metode yang mengembalikan stream "chunk" respons, di mana setiap chunk dapat diproses secara individual segera setelah tiba alih-alih menunggu respons lengkap.

### Streaming sinkron

Metode streaming ini mengembalikan `StreamResponse` untuk client sinkron:

```java
import com.anthropic.core.http.StreamResponse;
import com.anthropic.models.messages.RawMessageStreamEvent;

try (StreamResponse<RawMessageStreamEvent> streamResponse = client.messages().createStreaming(params)) {
    streamResponse.stream().forEach(chunk -> {
        IO.println(chunk);
    });
    IO.println("No more chunks!");
}
```

### Streaming asinkron

Untuk client asinkron, metode ini mengembalikan `AsyncStreamResponse`:

```java
import com.anthropic.core.http.AsyncStreamResponse;
import com.anthropic.models.messages.RawMessageStreamEvent;

client.async().messages().createStreaming(params).subscribe(chunk -> {
    IO.println(chunk);
});

// Jika Anda perlu menangani error atau penyelesaian stream
client.async().messages().createStreaming(params).subscribe(new AsyncStreamResponse.Handler<>() {
    @Override
    public void onNext(RawMessageStreamEvent chunk) {
        IO.println(chunk);
    }

    @Override
    public void onComplete(Optional<Throwable> error) {
        if (error.isPresent()) {
            IO.println("Something went wrong!");
            throw new RuntimeException(error.get());
        } else {
            IO.println("No more chunks!");
        }
    }
});

// Atau gunakan futures
client.async().messages().createStreaming(params)
    .subscribe(chunk -> {
        IO.println(chunk);
    })
    .onCompleteFuture()
    .whenComplete((unused, error) -> {
        if (error != null) {
            IO.println("Something went wrong!");
            throw new RuntimeException(error);
        } else {
            IO.println("No more chunks!");
        }
    });
```

Streaming async menggunakan `Executor` cached thread pool khusus per-client untuk melakukan streaming tanpa memblokir thread saat ini. Untuk menggunakan `Executor` yang berbeda:

```java
Executor executor = Executors.newFixedThreadPool(4);
client.async().messages().createStreaming(params).subscribe(
    chunk -> IO.println(chunk), executor
);
```

Atau konfigurasikan client secara global menggunakan metode `streamHandlerExecutor`:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .streamHandlerExecutor(Executors.newFixedThreadPool(4))
  .build();
```

### Streaming dengan message accumulator

`MessageAccumulator` dapat merekam stream event dalam respons saat diproses dan mengakumulasikan objek `Message` yang serupa dengan apa yang akan dikembalikan oleh API non-streaming.

Untuk respons sinkron, tambahkan pemanggilan `Stream.peek()` ke pipeline stream untuk mengakumulasikan setiap event:

```java
import com.anthropic.core.http.StreamResponse;
import com.anthropic.helpers.MessageAccumulator;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.RawMessageStreamEvent;

MessageAccumulator messageAccumulator = MessageAccumulator.create();

try (StreamResponse<RawMessageStreamEvent> streamResponse =
         client.messages().createStreaming(createParams)) {
    streamResponse.stream()
            .peek(messageAccumulator::accumulate)
            .flatMap(event -> event.contentBlockDelta().stream())
            .flatMap(deltaEvent -> deltaEvent.delta().text().stream())
            .forEach(textDelta -> IO.print(textDelta.text()));
}

Message message = messageAccumulator.message();
```

Untuk respons asinkron, tambahkan `MessageAccumulator` ke pemanggilan `subscribe()`:

```java
import com.anthropic.helpers.MessageAccumulator;
import com.anthropic.models.messages.Message;

MessageAccumulator messageAccumulator = MessageAccumulator.create();

client.async().messages()
        .createStreaming(createParams)
        .subscribe(event -> messageAccumulator.accumulate(event).contentBlockDelta().stream()
                .flatMap(deltaEvent -> deltaEvent.delta().text().stream())
                .forEach(textDelta -> IO.print(textDelta.text())))
        .onCompleteFuture()
        .join();

Message message = messageAccumulator.message();
```

`BetaMessageAccumulator` juga tersedia untuk akumulasi objek `BetaMessage`. Penggunaannya sama seperti `MessageAccumulator`.

## Output terstruktur

Untuk dokumentasi lengkap tentang "structured outputs" (output terstruktur) termasuk contoh Java, lihat [Output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs).

## Penggunaan alat

[Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) memungkinkan Anda mengintegrasikan alat dan fungsi eksternal langsung ke dalam respons model AI. Alih-alih menghasilkan teks biasa, model dapat menghasilkan instruksi (dengan parameter) untuk memanggil alat atau fungsi ketika diperlukan. Anda mendefinisikan skema JSON untuk alat, dan model menggunakan skema tersebut untuk menentukan kapan dan bagaimana menggunakan alat-alat ini.

Fitur penggunaan alat mendukung mode "strict" yang menjamin bahwa output JSON dari model AI akan sesuai dengan skema JSON yang Anda berikan dalam parameter input.

SDK dapat menurunkan alat dan parameternya secara otomatis dari struktur class Java arbitrer: nama class (dikonversi ke snake case) menyediakan nama alat, dan field class mendefinisikan parameter alat.

<Note>
  Deklarasikan class alat Anda sebagai class top-level atau nested class `static`. Persyaratan ini berasal dari library Jackson Databind (`com.fasterxml.jackson.databind`), yang digunakan SDK untuk melakukan deserialisasi input alat menjadi instance class Anda dan tidak dapat menginstansiasi inner class non-static.
</Note>

### Mendefinisikan alat dengan anotasi

```java
import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;

enum Unit {
  CELSIUS,
  FAHRENHEIT;

  public String toString() {
    return switch (this) {
      case CELSIUS -> "C";
      case FAHRENHEIT -> "F";
    };
  }

  public double fromKelvin(double temperatureK) {
    return switch (this) {
      case CELSIUS -> temperatureK - 273.15;
      case FAHRENHEIT -> (temperatureK - 273.15) * 1.8 + 32.0;
    };
  }
}

@JsonClassDescription("Get the weather in a given location")
static class GetWeather {

  @JsonPropertyDescription("The city and state, e.g. San Francisco, CA")
  public String location;

  @JsonPropertyDescription("The unit of temperature")
  public Unit unit;

  public Weather execute() {
    double temperatureK = switch (location) {
      case "San Francisco, CA" -> 300.0;
      case "New York, NY" -> 310.0;
      case "Dallas, TX" -> 305.0;
      default -> 295;
    };
    return new Weather(String.format("%.0f%s", unit.fromKelvin(temperatureK), unit));
  }
}

static class Weather {

  public String temperature;

  public Weather(String temperature) {
    this.temperature = temperature;
  }
}
```

### Memanggil alat

Ketika class alat Anda telah didefinisikan, tambahkan ke parameter pesan menggunakan `MessageCreateParams.Builder.addTool(Class<T>)` lalu panggil alat tersebut jika diminta dalam respons model AI. `BetaToolUseBlock.input(Class<T>)` dapat digunakan untuk mem-parse parameter alat dalam bentuk JSON menjadi instance dari class pendefinisi alat Anda.

Setelah memanggil alat, gunakan `BetaToolResultBlockParam.Builder.contentAsJson(Object)` untuk meneruskan hasil alat kembali ke model AI:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.*;
import com.anthropic.models.messages.Model;

AnthropicClient client = AnthropicOkHttpClient.fromEnv();

MessageCreateParams.Builder createParamsBuilder = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_5)
        .maxTokens(2048)
        .addTool(GetWeather.class)
        .addUserMessage("What's the temperature in New York?");

client.beta().messages().create(createParamsBuilder.build()).content().stream()
        .flatMap(contentBlock -> contentBlock.toolUse().stream())
        .forEach(toolUseBlock -> createParamsBuilder
              // Tambahkan pesan yang menunjukkan bahwa penggunaan alat diminta.
              .addAssistantMessageOfBetaContentBlockParams(
                      List.of(BetaContentBlockParam.ofToolUse(BetaToolUseBlockParam.builder()
                              .name(toolUseBlock.name())
                              .id(toolUseBlock.id())
                              .input(toolUseBlock._input())
                              .build())))
              // Tambahkan pesan dengan hasil dari penggunaan alat yang diminta.
              .addUserMessageOfBetaContentBlockParams(
                      List.of(BetaContentBlockParam.ofToolResult(BetaToolResultBlockParam.builder()
                              .toolUseId(toolUseBlock.id())
                              .contentAsJson(callTool(toolUseBlock))
                              .build()))));

client.beta().messages().create(createParamsBuilder.build()).content().stream()
        .flatMap(contentBlock -> contentBlock.text().stream())
        .forEach(textBlock -> IO.println(textBlock.text()));

private static Object callTool(BetaToolUseBlock toolUseBlock) {
  if (!"get_weather".equals(toolUseBlock.name())) {
    throw new IllegalArgumentException("Unknown tool: " + toolUseBlock.name());
  }

  GetWeather tool = toolUseBlock.input(GetWeather.class);
  return tool != null ? tool.execute() : new Weather("unknown");
}
```

### Konversi nama alat

Nama alat diturunkan dari nama class alat dalam camel case (misalnya, `GetWeather`) dan dikonversi ke snake case (misalnya, `get_weather`). Batas kata dimulai ketika karakter saat ini bukan karakter pertama, berupa huruf kapital, dan karakter sebelumnya adalah huruf kecil, atau karakter berikutnya adalah huruf kecil. Misalnya, `MyJSONParser` menjadi `my_json_parser` dan `ParseJSON` menjadi `parse_json`. Konversi ini dapat ditimpa menggunakan anotasi `@JsonTypeName`.

### Validasi skema JSON alat secara lokal

Anda dapat melakukan validasi lokal untuk memeriksa bahwa skema JSON yang diturunkan dari class alat Anda mematuhi batasan Anthropic. Validasi lokal diaktifkan secara default, tetapi dapat dinonaktifkan:

```java
MessageCreateParams.Builder createParamsBuilder = MessageCreateParams.builder()
  .model(Model.CLAUDE_OPUS_5)
  .maxTokens(2048)
  .addTool(GetWeather.class, JsonSchemaLocalValidation.NO)
  .addUserMessage("What's the temperature in New York?");
```

### Menganotasi class alat

Anda dapat menggunakan anotasi untuk menambahkan informasi lebih lanjut tentang alat ke skema JSON:

* `@JsonClassDescription` - Menambahkan deskripsi ke class alat yang merinci kapan dan bagaimana menggunakan alat tersebut.
* `@JsonTypeName` - Mengatur nama alat menjadi sesuatu selain nama sederhana class yang dikonversi ke snake case.
* `@JsonPropertyDescription` - Menambahkan deskripsi terperinci ke parameter alat.
* `@JsonIgnore` - Mengecualikan field `public` atau metode getter dari skema JSON yang dihasilkan untuk parameter alat.
* `@JsonProperty` - Menyertakan field non-`public` atau metode getter dalam skema JSON yang dihasilkan untuk parameter alat.

## Message batches

SDK menyediakan dukungan untuk [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) di bawah namespace `client.messages().batches()`. Lihat [Paginasi](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#pagination) untuk cara membuat daftar dan melakukan paginasi melalui batch.

## Unggah file

SDK mendefinisikan metode yang menerima file melalui class `MultipartField`:

```java
import com.anthropic.core.MultipartField;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileUploadParams;

FileUploadParams params = FileUploadParams.builder()
  .file(
    MultipartField.<InputStream>builder()
      .value(Files.newInputStream(Paths.get("/path/to/file.pdf")))
      .contentType("application/pdf")
      .build()
  )
  .build();

FileMetadata fileMetadata = client.beta().files().upload(params);
```

Atau dari `InputStream`:

```java
import com.anthropic.core.MultipartField;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileUploadParams;

FileUploadParams params = FileUploadParams.builder()
  .file(
    MultipartField.<InputStream>builder()
      .value(URI.create("https://example.com/path/to/file").toURL().openStream())
      .filename("document.pdf")
      .contentType("application/pdf")
      .build()
  )
  .build();

FileMetadata fileMetadata = client.beta().files().upload(params);
```

Atau dari byte dalam memori:

```java
import com.anthropic.core.MultipartField;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileUploadParams;

FileUploadParams params = FileUploadParams.builder()
  .file(
    MultipartField.<InputStream>builder()
      .value(new ByteArrayInputStream("content".getBytes()))
      .filename("document.txt")
      .contentType("text/plain")
      .build()
  )
  .build();

FileMetadata fileMetadata = client.beta().files().upload(params);
```

### Respons biner

SDK mendefinisikan metode yang mengembalikan respons biner untuk respons API yang tidak selalu di-parse sebagai JSON:

```java
import com.anthropic.core.http.HttpResponse;

HttpResponse response = client.beta().files().download("file_abc123");
```

Untuk menyimpan konten respons ke file:

```java
import com.anthropic.core.http.HttpResponse;

try (HttpResponse response = client.beta().files().download(params)) {
    Files.copy(
        response.body(),
        Paths.get(path),
        StandardCopyOption.REPLACE_EXISTING
    );
} catch (Exception e) {
    IO.println("Something went wrong!");
    throw new RuntimeException(e);
}
```

Atau mentransfer konten respons ke `OutputStream` mana pun:

```java
import com.anthropic.core.http.HttpResponse;

try (HttpResponse response = client.beta().files().download(params)) {
    response.body().transferTo(Files.newOutputStream(Paths.get(path)));
} catch (Exception e) {
    IO.println("Something went wrong!");
    throw new RuntimeException(e);
}
```

## Penanganan error

SDK melempar tipe unchecked exception kustom:

* `AnthropicServiceException` - Class dasar untuk error HTTP.
* `AnthropicIoException` - Error jaringan I/O.
* `AnthropicRetryableException` - Error generik yang menunjukkan kegagalan yang dapat dicoba ulang.
* `AnthropicInvalidDataException` - Kegagalan menginterpretasikan data yang berhasil di-parse (misalnya, ketika mengakses properti yang seharusnya wajib, tetapi API secara tak terduga menghilangkannya).
* `AnthropicException` - Class dasar untuk semua exception.

### Pemetaan kode status

| Status  | Exception                       |
| ------- | ------------------------------- |
| 400     | `BadRequestException`           |
| 401     | `UnauthorizedException`         |
| 403     | `PermissionDeniedException`     |
| 404     | `NotFoundException`             |
| 422     | `UnprocessableEntityException`  |
| 429     | `RateLimitException`            |
| 5xx     | `InternalServerException`       |
| lainnya | `UnexpectedStatusCodeException` |

`SseException` dilempar untuk error yang ditemui selama streaming SSE setelah respons HTTP awal yang berhasil.

```java
import com.anthropic.errors.*;

try {
    Message message = client.messages().create(params);
} catch (RateLimitException e) {
    IO.println("Rate limited, retry after: " + e.headers());
} catch (UnauthorizedException e) {
    IO.println("Invalid API key");
} catch (AnthropicServiceException e) {
    IO.println("API error: " + e.statusCode());
} catch (AnthropicIoException e) {
    IO.println("Network error: " + e.getMessage());
}
```

## Request ID

Saat menggunakan [respons mentah](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#raw-response-access), Anda dapat mengakses header respons `request-id` menggunakan metode `requestId()`:

```java
import com.anthropic.core.http.HttpResponseFor;
import com.anthropic.models.messages.Message;

HttpResponseFor<Message> message = client.messages().withRawResponse().create(params);

Optional<String> requestId = message.requestId();
```

Ini dapat digunakan untuk mencatat permintaan yang gagal dengan cepat dan melaporkannya kembali ke Anthropic. Untuk informasi lebih lanjut tentang debugging permintaan, lihat [Request ID](https://platform.claude.com/docs/id/api/errors#request-id).

## Percobaan ulang

SDK secara otomatis mencoba ulang 2 kali secara default, dengan exponential backoff singkat di antara permintaan.

Hanya tipe error berikut yang dicoba ulang:

* Error koneksi (misalnya, karena masalah konektivitas jaringan)
* 408 Request Timeout
* 409 Conflict
* 429 Rate Limit
* 5xx Internal

API juga dapat secara eksplisit menginstruksikan SDK untuk mencoba ulang atau tidak mencoba ulang suatu permintaan.

Untuk mengatur jumlah percobaan ulang kustom, konfigurasikan client menggunakan metode `maxRetries`:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder().fromEnv().maxRetries(4).build();
```

## Timeout

Permintaan mengalami timeout setelah 10 menit secara default.

Namun, untuk metode yang menerima `maxTokens`, jika Anda menentukan nilai `maxTokens` yang besar dan sedang melakukan streaming, maka timeout default akan dihitung secara dinamis menggunakan rumus ini:

```java
Duration.ofSeconds(
    Math.min(
        60 * 60, // 1 hour max
        Math.max(
            10 * 60, // 10 minute minimum
            60 * 60 * maxTokens / 128_000
        )
    )
)
```

Ini menghasilkan timeout hingga 60 menit, diskalakan berdasarkan parameter `maxTokens`, kecuali ditimpa.

Untuk permintaan non-streaming, timeout dinamis diskalakan dari minimum 30 detik hingga maksimum 10 menit berdasarkan `maxTokens`.

Untuk mengatur timeout kustom per-permintaan:

```java
import com.anthropic.models.messages.Message;

Message message = client
  .messages()
  .create(params, RequestOptions.builder().timeout(Duration.ofSeconds(30)).build());
```

Atau konfigurasikan default untuk semua pemanggilan metode di tingkat client:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .timeout(Duration.ofSeconds(30))
  .build();
```

## Permintaan panjang

<Warning>
  Pertimbangkan untuk menggunakan [streaming](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#streaming) untuk permintaan yang berjalan lebih lama.
</Warning>

Hindari mengatur nilai `maxTokens` yang besar tanpa menggunakan streaming. Beberapa jaringan mungkin memutus koneksi idle setelah periode waktu tertentu, yang dapat menyebabkan permintaan gagal atau mengalami [timeout](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#timeouts) tanpa menerima respons dari Anthropic. SDK secara berkala melakukan ping ke API untuk menjaga koneksi tetap aktif dan mengurangi dampak dari jaringan tersebut.

SDK melempar error jika permintaan non-streaming diperkirakan memakan waktu lebih dari 10 menit. Menggunakan [metode streaming](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#streaming) atau [menimpa timeout](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#timeouts) di tingkat client atau permintaan akan menonaktifkan error tersebut.

## Paginasi

SDK menyediakan cara yang mudah untuk mengakses hasil yang dipaginasi baik satu halaman pada satu waktu atau item demi item di seluruh halaman.

### Paginasi otomatis

Untuk melakukan iterasi melalui semua hasil di seluruh halaman, gunakan metode `autoPager()`, yang secara otomatis mengambil lebih banyak halaman sesuai kebutuhan.

```java
import com.anthropic.models.messages.batches.BatchListPage;
import com.anthropic.models.messages.batches.MessageBatch;

BatchListPage page = client.messages().batches().list();

// Proses sebagai Iterable
for (MessageBatch batch : page.autoPager()) {
    IO.println(batch);
}

// Proses sebagai Stream
page.autoPager()
    .stream()
    .limit(50)
    .forEach(batch -> IO.println(batch));
```

Saat menggunakan client asinkron, metode ini mengembalikan `AsyncStreamResponse`:

```java
import com.anthropic.core.http.AsyncStreamResponse;
import com.anthropic.models.messages.batches.BatchListPageAsync;
import com.anthropic.models.messages.batches.MessageBatch;

CompletableFuture<BatchListPageAsync> pageFuture = client.async().messages().batches().list();

pageFuture.thenAccept(page -> page.autoPager().subscribe(batch -> {
    IO.println(batch);
}));

// Jika Anda perlu menangani error atau penyelesaian stream
pageFuture.thenAccept(page -> page.autoPager().subscribe(new AsyncStreamResponse.Handler<>() {
    @Override
    public void onNext(MessageBatch batch) {
        IO.println(batch);
    }

    @Override
    public void onComplete(Optional<Throwable> error) {
        if (error.isPresent()) {
            IO.println("Something went wrong!");
            throw new RuntimeException(error.get());
        } else {
            IO.println("No more!");
        }
    }
}));

// Atau gunakan futures
pageFuture.thenAccept(page -> page.autoPager()
    .subscribe(batch -> {
        IO.println(batch);
    })
    .onCompleteFuture()
    .whenComplete((unused, error) -> {
        if (error != null) {
            IO.println("Something went wrong!");
            throw new RuntimeException(error);
        } else {
            IO.println("No more!");
        }
    }));
```

### Paginasi manual

Untuk mengakses item halaman individual dan meminta halaman berikutnya secara manual:

```java
import com.anthropic.models.messages.batches.BatchListPage;
import com.anthropic.models.messages.batches.MessageBatch;

BatchListPage page = client.messages().batches().list();
while (true) {
    for (MessageBatch batch : page.items()) {
        IO.println(batch);
    }

    if (!page.hasNextPage()) {
        break;
    }

    page = page.nextPage();
}
```

## Sistem tipe

### Immutability dan builder

Setiap class dalam SDK memiliki builder terkait untuk mengonstruksinya. Setiap class bersifat immutable setelah dikonstruksi. Jika class memiliki builder terkait, maka class tersebut memiliki metode `toBuilder()`, yang dapat digunakan untuk mengonversinya kembali ke builder untuk membuat salinan yang dimodifikasi.

```java
MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_5)
  .build();

// Buat salinan yang dimodifikasi menggunakan toBuilder()
MessageCreateParams modified = params.toBuilder().maxTokens(2048L).build();
```

Karena setiap class bersifat immutable, modifikasi builder tidak pernah memengaruhi instance class yang sudah dibangun.

### Permintaan dan respons

Untuk mengirim permintaan ke Claude API, bangun instance dari suatu class `Params` dan teruskan ke metode client yang sesuai. Ketika respons diterima, respons tersebut dideserialisasi menjadi instance dari class Java.

Misalnya, `client.messages().create(...)` harus dipanggil dengan instance `MessageCreateParams`, dan mengembalikan instance `Message`.

### Parameter tidak terdokumentasi

Untuk mengatur parameter yang tidak terdokumentasi, panggil metode `putAdditionalHeader`, `putAdditionalQueryParam`, atau `putAdditionalBodyProperty` pada class `Params` mana pun:

```java
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.MessageCreateParams;

MessageCreateParams params = MessageCreateParams.builder()
  .putAdditionalHeader("Secret-Header", "42")
  .putAdditionalQueryParam("secret_query_param", "42")
  .putAdditionalBodyProperty("secretProperty", JsonValue.from("42"))
  .build();
```

Ini dapat diakses pada objek yang telah dibangun nantinya menggunakan metode `_additionalHeaders()`, `_additionalQueryParams()`, dan `_additionalBodyProperties()`.

<Warning>
  Nilai yang diteruskan ke metode ini menimpa nilai yang diteruskan ke metode sebelumnya. Untuk alasan keamanan, pastikan metode ini hanya digunakan dengan data input yang tepercaya.
</Warning>

Untuk mengatur parameter yang tidak terdokumentasi pada header, query params, atau class body bersarang:

```java
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Metadata;

MessageCreateParams params = MessageCreateParams.builder()
  .metadata(
    Metadata.builder().putAdditionalProperty("secretProperty", JsonValue.from("42")).build()
  )
  .build();
```

Properti ini dapat diakses pada objek bersarang yang telah dibangun nantinya menggunakan metode `_additionalProperties()`.

Untuk mengatur parameter atau properti yang terdokumentasi ke nilai yang tidak terdokumentasi atau belum didukung, teruskan objek `JsonValue` ke setter-nya:

```java
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(JsonValue.from(3.14))
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_5)
  .build();
```

### Pembuatan JsonValue

Cara paling mudah untuk membuat `JsonValue` adalah menggunakan metode `from(...)`:

```java
import com.anthropic.core.JsonValue;

// Membuat nilai JSON primitif
JsonValue nullValue = JsonValue.from(null);

JsonValue booleanValue = JsonValue.from(true);

JsonValue numberValue = JsonValue.from(42);

JsonValue stringValue = JsonValue.from("Hello World!");

// Membuat nilai array JSON yang setara dengan `["Hello", "World"]`
JsonValue arrayValue = JsonValue.from(List.of("Hello", "World"));

// Membuat nilai objek JSON yang setara dengan `{ "a": 1, "b": 2 }`
JsonValue objectValue = JsonValue.from(Map.of("a", 1, "b", 2));

// Membuat JSON bersarang secara arbitrer yang setara dengan:
// { "a": [1, 2], "b": [3, 4] }
JsonValue complexValue = JsonValue.from(Map.of("a", List.of(1, 2), "b", List.of(3, 4)));
```

### Menghilangkan parameter wajib secara paksa

Biasanya metode `build` dari class `Builder` akan melempar `IllegalStateException` jika ada parameter atau properti wajib yang tidak diatur. Untuk menghilangkan parameter atau properti wajib secara paksa, teruskan `JsonMissing`:

```java
import com.anthropic.core.JsonMissing;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

MessageCreateParams params = MessageCreateParams.builder()
  .addUserMessage("Hello, world")
  .model(Model.CLAUDE_OPUS_5)
  .maxTokens(JsonMissing.of())
  .build();
```

### Properti respons

Untuk mengakses properti respons yang tidak terdokumentasi, panggil metode `_additionalProperties()`:

```java
import com.anthropic.core.JsonValue;

Map<String, JsonValue> additionalProperties = client
  .messages()
  .create(params)
  ._additionalProperties();

JsonValue secretPropertyValue = additionalProperties.get("secretProperty");

String result = secretPropertyValue.accept(new JsonValue.Visitor<>() {
    @Override
    public String visitNull() {
        return "It's null!";
    }

    @Override
    public String visitBoolean(boolean value) {
        return "It's a boolean!";
    }

    @Override
    public String visitNumber(Number value) {
        return "It's a number!";
    }

    // Metode lainnya mencakup `visitMissing`, `visitString`, `visitArray`, dan `visitObject`
    // Implementasi default dari setiap metode yang tidak diimplementasikan didelegasikan ke `visitDefault`,
    // yang secara default melempar exception, tetapi juga dapat di-override
});
```

Untuk mengakses nilai JSON mentah dari suatu properti, panggil metodenya yang berawalan `_`:

```java
import com.anthropic.core.JsonField;
import com.anthropic.models.messages.StopReason;

JsonField<StopReason> stopReason = client.messages().create(params)._stopReason();

if (stopReason.isMissing()) {
  // Properti tidak ada dalam respons JSON
} else if (stopReason.isNull()) {
  // Properti disetel ke null literal
} else {
  // Periksa apakah nilai diberikan sebagai string
  // Metode lainnya termasuk `asNumber()`, `asBoolean()`, dll.
  Optional<String> jsonString = stopReason.asString();

  // Coba deserialisasi menjadi tipe kustom
  MyClass myObject = stopReason.asUnknown().orElseThrow().convert(MyClass.class);
}
```

### Validasi respons

Secara default, SDK tidak melempar exception ketika API mengembalikan respons yang tidak cocok dengan tipe yang diharapkan. SDK hanya melempar `AnthropicInvalidDataException` jika Anda mengakses properti secara langsung.

Untuk memeriksa bahwa respons sepenuhnya bertipe dengan benar di awal, panggil `validate()`:

```java
import com.anthropic.models.messages.Message;

Message message = client.messages().create(params).validate();
```

Atau konfigurasikan per-permintaan:

```java
import com.anthropic.models.messages.Message;

Message message = client
  .messages()
  .create(params, RequestOptions.builder().responseValidation(true).build());
```

Atau konfigurasikan default untuk semua pemanggilan metode di tingkat client:

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .responseValidation(true)
  .build();
```

## Kustomisasi HTTP client

### Konfigurasi proxy

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import java.net.Proxy;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .proxy(new Proxy(Proxy.Type.HTTP, new InetSocketAddress("https://example.com", 8080)))
  .build();
```

### Konfigurasi HTTPS / SSL

<Note>
  Sebagian besar aplikasi tidak perlu memanggil metode ini, dan sebaiknya menggunakan default sistem. Default tersebut mencakup optimasi khusus yang dapat hilang jika implementasinya dimodifikasi.
</Note>

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .sslSocketFactory(yourSSLSocketFactory)
  .trustManager(yourTrustManager)
  .hostnameVerifier(yourHostnameVerifier)
  .build();
```

### HTTP client kustom

SDK terdiri dari tiga artifact:

* `anthropic-java-core` - Berisi logika inti SDK, tidak bergantung pada OkHttp. Mengekspos `AnthropicClient`, `AnthropicClientAsync`, dan class implementasinya, yang semuanya dapat bekerja dengan HTTP client apa pun.
* `anthropic-java-client-okhttp` - Bergantung pada OkHttp. Mengekspos `AnthropicOkHttpClient` dan `AnthropicOkHttpClientAsync`.
* `anthropic-java` - Bergantung pada dan mengekspos API dari `anthropic-java-core` dan `anthropic-java-client-okhttp`. Tidak memiliki logika sendiri.

Struktur ini memungkinkan penggantian HTTP client default SDK tanpa menarik dependensi yang tidak perlu.

#### OkHttpClient yang dikustomisasi

<Tip>
  Coba [opsi jaringan](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#retries) yang tersedia sebelum mengganti client default.
</Tip>

Untuk menggunakan `OkHttpClient` yang dikustomisasi:

1. Ganti dependensi `anthropic-java` Anda dengan `anthropic-java-core`.
2. Salin class `OkHttpClient` dari `anthropic-java-client-okhttp` ke dalam kode Anda dan kustomisasi.
3. Konstruksi `AnthropicClientImpl` atau `AnthropicClientAsyncImpl` menggunakan client yang telah Anda kustomisasi.

#### HTTP client yang sepenuhnya kustom

Untuk menggunakan HTTP client yang sepenuhnya kustom:

1. Ganti dependensi `anthropic-java` Anda dengan `anthropic-java-core`.
2. Tulis class yang mengimplementasikan interface `HttpClient`.
3. Konstruksi `AnthropicClientImpl` atau `AnthropicClientAsyncImpl` menggunakan class client baru Anda.

## Integrasi platform

<Note>
  Untuk panduan pengaturan platform terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)
  * [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

Java SDK mendukung platform berikut melalui dependensi terpisah yang menyediakan implementasi `Backend` spesifik platform:

* **Agent Platform:** `com.anthropic:anthropic-java-vertex`: Gunakan `VertexBackend.fromEnv()` atau `VertexBackend.builder()`.
* **Bedrock:** `com.anthropic:anthropic-java-bedrock`: Gunakan `BedrockMantleBackend.fromEnv()` atau `BedrockMantleBackend.builder()` untuk endpoint Bedrock Messages-API, atau `BedrockBackend.fromEnv()` / `BedrockBackend.builder()` (path `bedrock-runtime`).
* **Claude Platform di AWS:** `com.anthropic:anthropic-java-aws`: Gunakan `AwsBackend.fromEnv()` (membaca `ANTHROPIC_AWS_WORKSPACE_ID` dan rantai region/kredensial default AWS) atau `AwsBackend.builder()`. Tersedia dalam beta.
* **Foundry:** `com.anthropic:anthropic-java-foundry`: Gunakan `FoundryBackend.fromEnv()` atau `FoundryBackend.builder()`.

Gunakan `BedrockMantleBackend` untuk proyek baru; `BedrockBackend` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan Bedrock `InvokeModel` API.

Setiap implementasi `Backend` diteruskan ke client dengan `.backend()` pada `AnthropicOkHttpClient.builder()`. Setiap backend cloud menarik class SDK platform cloud masing-masing sebagai dependensi transitif.

## Penggunaan lanjutan

### Akses respons mentah

Untuk mengakses header HTTP, kode status, dan body respons mentah, awali pemanggilan metode HTTP apa pun dengan `withRawResponse()`:

```java
import com.anthropic.core.http.Headers;
import com.anthropic.core.http.HttpResponseFor;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_5)
  .build();

HttpResponseFor<Message> message = client.messages().withRawResponse().create(params);

int statusCode = message.statusCode();

Headers headers = message.headers();
```

Anda masih dapat melakukan deserialisasi respons menjadi instance class Java jika diperlukan:

```java
import com.anthropic.models.messages.Message;

Message parsedMessage = message.parse();
```

### Logging

SDK menggunakan logging interceptor OkHttp standar.

Aktifkan logging dengan mengatur variabel lingkungan `ANTHROPIC_LOG` ke `info`:

```bash
export ANTHROPIC_LOG=info
```

Atau ke `debug` untuk logging yang lebih verbose:

```bash
export ANTHROPIC_LOG=debug
```

<Accordion title="Kompatibilitas Jackson">
  SDK bergantung pada Jackson untuk serialisasi/deserialisasi JSON. SDK kompatibel dengan versi 2.13.4 atau lebih tinggi, tetapi bergantung pada versi 2.18.2 secara default.

  SDK melempar exception jika mendeteksi versi Jackson yang tidak kompatibel saat runtime (misalnya, jika versi default ditimpa dalam konfigurasi Maven atau Gradle Anda).

  Jika SDK melempar exception, tetapi Anda yakin versinya kompatibel, maka nonaktifkan pemeriksaan versi menggunakan `checkJacksonVersionCompatibility` pada `AnthropicOkHttpClient` atau `AnthropicOkHttpClientAsync`.

  <Warning>
    Tidak ada jaminan bahwa SDK bekerja dengan benar ketika pemeriksaan versi Jackson dinonaktifkan.
  </Warning>

  Ada juga bug pada versi Jackson yang lebih lama yang dapat memengaruhi SDK. SDK tidak mengatasi semua bug Jackson dan mengharapkan pengguna untuk meng-upgrade Jackson untuk kasus tersebut.
</Accordion>

<Accordion title="Konfigurasi ProGuard/R8">
  Meskipun SDK menggunakan reflection, SDK tetap dapat digunakan dengan ProGuard dan R8 karena `anthropic-java-core` dipublikasikan dengan file konfigurasi yang berisi keep rules.

  ProGuard dan R8 seharusnya secara otomatis mendeteksi dan menggunakan rules yang dipublikasikan, tetapi Anda juga dapat menyalin keep rules secara manual jika diperlukan.
</Accordion>

### Fungsionalitas API yang tidak terdokumentasi

SDK diberi tipe untuk penggunaan yang mudah dari API yang terdokumentasi. Namun, SDK juga mendukung bekerja dengan bagian API yang tidak terdokumentasi atau belum didukung.

#### Parameter permintaan yang tidak terdokumentasi

Untuk mengatur parameter permintaan yang tidak terdokumentasi, gunakan metode `putAdditionalHeader`, `putAdditionalQueryParam`, atau `putAdditionalBodyProperty` seperti yang dijelaskan dalam [Parameter tidak terdokumentasi](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#undocumented-parameters).

#### Properti respons yang tidak terdokumentasi

Untuk mengakses properti respons yang tidak terdokumentasi, gunakan metode `_additionalProperties()` seperti yang dijelaskan dalam [Properti respons](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#response-properties).

#### Nilai enum baru atau belum dirilis

Class mirip enum dalam SDK, seperti `Model` dan `AnthropicBeta`, bukan tipe `enum` Java tertutup. Masing-masing menyediakan metode factory `of(String)` yang menerima string apa pun, sehingga Anda dapat menggunakan nilai yang belum ditambahkan ke SDK, seperti model atau beta header yang dirilis setelah versi SDK Anda:

```java
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.messages.Model;

Model model = Model.of("some-new-model");
AnthropicBeta beta = AnthropicBeta.of("some-new-beta-2026-01-01");
```

Metode builder yang menerima tipe ini sering kali juga menyediakan overload `String` yang memanggil `of(...)` untuk Anda:

```java
import com.anthropic.models.messages.MessageCreateParams;

MessageCreateParams params = MessageCreateParams.builder()
  .model("some-new-model") // same as .model(Model.of("some-new-model"))
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .build();
```

Utamakan konstanta bertipe (misalnya, `Model.CLAUDE_OPUS_5`) agar Anda mendapatkan autocomplete dan peringatan deprecation. Overload `String` dan `of(...)` terutama untuk mengatur field ke nilai yang tidak terdokumentasi atau belum didukung sambil menunggu rilis SDK yang menyertakannya.

## Fitur beta

Fitur beta tersedia sebelum rilis umum untuk mendapatkan umpan balik awal dan menguji fungsionalitas baru. Anda dapat memeriksa ketersediaan semua kemampuan dan alat Claude di [ikhtisar membangun dengan Claude](https://platform.claude.com/docs/id/build-with-claude/overview).

Anda dapat mengakses sebagian besar fitur API beta melalui metode `beta()` pada client. Untuk mengaktifkan fitur beta tertentu, tambahkan [beta header](https://platform.claude.com/docs/id/api/beta-headers) yang sesuai dengan `.addBeta()` saat membangun parameter pesan.

Misalnya, untuk menggunakan [Files API](https://platform.claude.com/docs/id/build-with-claude/files):

```java
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.messages.BetaContentBlockParam;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaRequestDocumentBlock;
import com.anthropic.models.beta.messages.BetaTextBlockParam;
import com.anthropic.models.beta.messages.MessageCreateParams;
// ...
void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    BetaMessage message = client.beta().messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_5)
            .maxTokens(1024L)
            .addBeta(AnthropicBeta.FILES_API_2025_04_14)
            .addUserMessageOfBetaContentBlockParams(List.of(
                BetaContentBlockParam.ofText(
                    BetaTextBlockParam.builder()
                        .text("Please summarize this document for me.")
                        .build()),
                BetaContentBlockParam.ofDocument(
                    BetaRequestDocumentBlock.builder()
                        .fileSource("file_abc123")
                        .build())))
            .build());
}
```

## Pertanyaan yang sering diajukan

<AccordionGroup>
  <Accordion title="Mengapa SDK tidak menggunakan class enum biasa?">
    Class `enum` Java tidak mudah kompatibel ke depan. Menggunakannya dalam SDK dapat menyebabkan runtime exception jika API diperbarui untuk merespons dengan nilai enum baru.

    Karena class ini bersifat terbuka, Anda juga dapat mengonstruksinya dengan nilai string apa pun melalui metode factory `of(String)`. Lihat [Nilai enum baru atau belum dirilis](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#new-or-unreleased-enum-values) jika Anda perlu menggunakan nilai yang belum ada di versi SDK Anda.
  </Accordion>

  <Accordion title="Mengapa field direpresentasikan menggunakan JsonField<T> alih-alih T biasa?">
    Menggunakan `JsonField<T>` memungkinkan beberapa fitur:

    * Memungkinkan penggunaan fungsionalitas API yang tidak terdokumentasi
    * Memvalidasi respons API secara lazy terhadap bentuk yang diharapkan
    * Merepresentasikan nilai yang tidak ada vs nilai null eksplisit
  </Accordion>

  <Accordion title="Mengapa SDK tidak menggunakan data class?">
    Menambahkan field baru ke data class tidak kompatibel ke belakang, dan SDK menghindari memperkenalkan breaking change setiap kali field ditambahkan ke class.
  </Accordion>

  <Accordion title="Mengapa SDK tidak menggunakan checked exception?">
    Checked exception secara luas dianggap sebagai kesalahan dalam bahasa pemrograman Java. Bahkan, checked exception dihilangkan dari Kotlin karena alasan ini.

    Checked exception:

    * Verbose untuk ditangani
    * Mendorong penanganan error pada tingkat abstraksi yang salah, di mana tidak ada yang dapat dilakukan terhadap error tersebut
    * Merepotkan untuk dipropagasi karena masalah function coloring
    * Tidak bekerja dengan baik dengan lambda (juga karena masalah function coloring)
  </Accordion>
</AccordionGroup>

## Semantic versioning

Paket ini secara umum mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan tertentu yang tidak kompatibel ke belakang dapat dirilis sebagai versi minor:

1. Perubahan pada internal library yang secara teknis bersifat public tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
2. Perubahan yang tidak diharapkan memengaruhi sebagian besar pengguna dalam praktiknya.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-java)
* [Javadocs](https://javadoc.io/doc/com.anthropic/anthropic-java)
* [Referensi API](https://platform.claude.com/docs/id/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/id/build-with-claude/streaming)
* [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview)
