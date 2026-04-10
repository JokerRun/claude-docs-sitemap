---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/java
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 1af22c4c543c491622674e70a0341c85588fee4d14399d426a579562471f6f9f
---

# Java SDK

Instal dan konfigurasi Anthropic Java SDK dengan pola builder dan dukungan async

---

Anthropic Java SDK menyediakan akses yang mudah ke Anthropic REST API dari aplikasi yang ditulis dalam Java. SDK ini menggunakan pola builder untuk membuat permintaan dan mendukung operasi sinkron dan asinkron.

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus Java dan konfigurasi.
</Info>

## Instalasi

<Tabs>
<Tab title="Gradle">
```kotlin
implementation("com.anthropic:anthropic-java:2.20.0")
```
</Tab>
<Tab title="Maven">
```xml
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>anthropic-java</artifactId>
    <version>2.20.0</version>
</dependency>
```
</Tab>
</Tabs>

## Persyaratan

Perpustakaan ini memerlukan Java 8 atau lebih baru.

## Mulai cepat

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

// Mengonfigurasi menggunakan properti sistem `anthropic.apiKey`, `anthropic.authToken` dan `anthropic.baseUrl`
// Atau mengonfigurasi menggunakan variabel lingkungan `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` dan `ANTHROPIC_BASE_URL`
AnthropicClient client = AnthropicOkHttpClient.fromEnv();

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_4_6)
  .build();

Message message = client.messages().create(params);
```

## Konfigurasi klien

### Pengaturan kunci API

Konfigurasi klien menggunakan properti sistem atau variabel lingkungan:

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

// Mengonfigurasi menggunakan properti sistem `anthropic.apiKey`, `anthropic.authToken` dan `anthropic.baseUrl`
// Atau mengonfigurasi menggunakan variabel lingkungan `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` dan `ANTHROPIC_BASE_URL`
AnthropicClient client = AnthropicOkHttpClient.fromEnv();
```

Atau konfigurasi secara manual:

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .apiKey("my-anthropic-api-key")
  .build();
```

Atau gunakan kombinasi dari kedua pendekatan:

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  // Mengonfigurasi menggunakan properti sistem atau variabel lingkungan
  .fromEnv()
  .apiKey("my-anthropic-api-key")
  .build();
```

### Opsi konfigurasi

| Setter      | Properti sistem       | Variabel lingkungan    | Diperlukan | Nilai default                 |
| ----------- | --------------------- | ---------------------- | -------- | ----------------------------- |
| `apiKey`    | `anthropic.apiKey`    | `ANTHROPIC_API_KEY`    | false    | -                             |
| `authToken` | `anthropic.authToken` | `ANTHROPIC_AUTH_TOKEN` | false    | -                             |
| `baseUrl`   | `anthropic.baseUrl`   | `ANTHROPIC_BASE_URL`   | true     | `"https://api.anthropic.com"` |

Properti sistem memiliki prioritas lebih tinggi daripada variabel lingkungan.

<Tip>
Jangan membuat lebih dari satu klien dalam aplikasi yang sama. Setiap klien memiliki kumpulan koneksi dan kumpulan thread, yang lebih efisien untuk dibagikan antar permintaan.
</Tip>

### Memodifikasi konfigurasi

Untuk sementara menggunakan konfigurasi klien yang dimodifikasi sambil menggunakan kembali kumpulan koneksi dan thread yang sama, panggil `withOptions()` pada klien atau layanan apa pun:

```java nocheck
import com.anthropic.client.AnthropicClient;

AnthropicClient clientWithOptions = client.withOptions(optionsBuilder -> {
  optionsBuilder.baseUrl("https://example.com");
  optionsBuilder.maxRetries(42);
});
```

Metode `withOptions()` tidak mempengaruhi klien atau layanan asli.

## Penggunaan async

Klien default bersifat sinkron. Untuk beralih ke eksekusi asinkron, panggil metode `async()`:

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import java.util.concurrent.CompletableFuture;

AnthropicClient client = AnthropicOkHttpClient.fromEnv();

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_4_6)
  .build();

CompletableFuture<Message> message = client.async().messages().create(params);
```

Atau buat klien asinkron dari awal:

```java nocheck
import com.anthropic.client.AnthropicClientAsync;
import com.anthropic.client.okhttp.AnthropicOkHttpClientAsync;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import java.util.concurrent.CompletableFuture;

AnthropicClientAsync client = AnthropicOkHttpClientAsync.fromEnv();

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_4_6)
  .build();

CompletableFuture<Message> message = client.messages().create(params);
```

Klien asinkron mendukung opsi yang sama seperti klien sinkron, kecuali sebagian besar metode mengembalikan `CompletableFuture`s.

## Streaming

SDK mendefinisikan metode yang mengembalikan aliran "chunk" respons, di mana setiap chunk dapat diproses secara individual segera setelah tiba daripada menunggu respons lengkap.

### Streaming sinkron

Metode streaming ini mengembalikan `StreamResponse` untuk klien sinkron:

```java nocheck
import com.anthropic.core.http.StreamResponse;
import com.anthropic.models.messages.RawMessageStreamEvent;

try (StreamResponse<RawMessageStreamEvent> streamResponse = client.messages().createStreaming(params)) {
    streamResponse.stream().forEach(chunk -> {
        System.out.println(chunk);
    });
    System.out.println("No more chunks!");
}
```

### Streaming asinkron

Untuk klien asinkron, metode mengembalikan `AsyncStreamResponse`:

```java nocheck
import com.anthropic.core.http.AsyncStreamResponse;
import com.anthropic.models.messages.RawMessageStreamEvent;
import java.util.Optional;

client.async().messages().createStreaming(params).subscribe(chunk -> {
    System.out.println(chunk);
});

// Jika Anda perlu menangani kesalahan atau penyelesaian aliran
client.async().messages().createStreaming(params).subscribe(new AsyncStreamResponse.Handler<>() {
    @Override
    public void onNext(RawMessageStreamEvent chunk) {
        System.out.println(chunk);
    }

    @Override
    public void onComplete(Optional<Throwable> error) {
        if (error.isPresent()) {
            System.out.println("Something went wrong!");
            throw new RuntimeException(error.get());
        } else {
            System.out.println("No more chunks!");
        }
    }
});

// Atau gunakan futures
client.async().messages().createStreaming(params)
    .subscribe(chunk -> {
        System.out.println(chunk);
    })
    .onCompleteFuture()
    .whenComplete((unused, error) -> {
        if (error != null) {
            System.out.println("Something went wrong!");
            throw new RuntimeException(error);
        } else {
            System.out.println("No more chunks!");
        }
    });
```

Streaming async menggunakan `Executor` kumpulan thread yang di-cache khusus per-klien untuk streaming tanpa memblokir thread saat ini. Untuk menggunakan `Executor` yang berbeda:

```java nocheck
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

Executor executor = Executors.newFixedThreadPool(4);
client.async().messages().createStreaming(params).subscribe(
    chunk -> System.out.println(chunk), executor
);
```

Atau konfigurasi klien secara global menggunakan metode `streamHandlerExecutor`:

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import java.util.concurrent.Executors;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .streamHandlerExecutor(Executors.newFixedThreadPool(4))
  .build();
```

### Streaming dengan akumulator pesan

`MessageAccumulator` dapat merekam aliran peristiwa dalam respons saat diproses dan mengumpulkan objek `Message` yang mirip dengan apa yang akan dikembalikan oleh API non-streaming.

Untuk respons sinkron, tambahkan panggilan `Stream.peek()` ke pipeline aliran untuk mengumpulkan setiap peristiwa:

```java nocheck
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
            .forEach(textDelta -> System.out.print(textDelta.text()));
}

Message message = messageAccumulator.message();
```

Untuk respons asinkron, tambahkan `MessageAccumulator` ke panggilan `subscribe()`:

```java nocheck
import com.anthropic.helpers.MessageAccumulator;
import com.anthropic.models.messages.Message;

MessageAccumulator messageAccumulator = MessageAccumulator.create();

client.messages()
        .createStreaming(createParams)
        .subscribe(event -> messageAccumulator.accumulate(event).contentBlockDelta().stream()
                .flatMap(deltaEvent -> deltaEvent.delta().text().stream())
                .forEach(textDelta -> System.out.print(textDelta.text())))
        .onCompleteFuture()
        .join();

Message message = messageAccumulator.message();
```

`BetaMessageAccumulator` juga tersedia untuk akumulasi objek `BetaMessage`. Digunakan dengan cara yang sama seperti `MessageAccumulator`.

## Output terstruktur

Untuk dokumentasi output terstruktur lengkap termasuk contoh Java, lihat [Output Terstruktur](/docs/id/build-with-claude/structured-outputs).

## Penggunaan alat

[Penggunaan Alat](/docs/id/agents-and-tools/tool-use/overview) memungkinkan Anda mengintegrasikan alat dan fungsi eksternal langsung ke dalam respons model AI. Alih-alih menghasilkan teks biasa, model dapat mengeluarkan instruksi (dengan parameter) untuk memanggil alat atau memanggil fungsi jika sesuai. Anda menentukan skema JSON untuk alat, dan model menggunakan skema untuk memutuskan kapan dan bagaimana menggunakan alat ini.

Fitur penggunaan alat mendukung mode "ketat" (beta) yang menjamin bahwa output JSON dari model AI akan sesuai dengan skema JSON yang Anda berikan dalam parameter input.

SDK dapat menurunkan alat dan parameternya secara otomatis dari struktur kelas Java arbitrer: nama kelas (dikonversi ke snake case) menyediakan nama alat, dan bidang kelas mendefinisikan parameter alat.

### Mendefinisikan alat dengan anotasi

```java nocheck
import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;

enum Unit {
  CELSIUS,
  FAHRENHEIT;

  public String toString() {
    switch (this) {
      case CELSIUS:
        return "C";
      case FAHRENHEIT:
      default:
        return "F";
    }
  }

  public double fromKelvin(double temperatureK) {
    switch (this) {
      case CELSIUS:
        return temperatureK - 273.15;
      case FAHRENHEIT:
      default:
        return (temperatureK - 273.15) * 1.8 + 32.0;
    }
  }
}

@JsonClassDescription("Get the weather in a given location")
static class GetWeather {

  @JsonPropertyDescription("The city and state, e.g. San Francisco, CA")
  public String location;

  @JsonPropertyDescription("The unit of temperature")
  public Unit unit;

  public Weather execute() {
    double temperatureK;
    switch (location) {
      case "San Francisco, CA":
        temperatureK = 300.0;
        break;
      case "New York, NY":
        temperatureK = 310.0;
        break;
      case "Dallas, TX":
        temperatureK = 305.0;
        break;
      default:
        temperatureK = 295;
        break;
    }
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

Ketika kelas alat Anda didefinisikan, tambahkan ke parameter pesan menggunakan `MessageCreateParams.addTool(Class<T>)` dan kemudian panggil jika diminta untuk melakukannya dalam respons model AI. `BetaToolUseBlock.input(Class<T>)` dapat digunakan untuk menguraikan parameter alat dalam bentuk JSON ke instance kelas yang mendefinisikan alat Anda.

Setelah memanggil alat, gunakan `BetaToolResultBlockParam.Builder.contentAsJson(Object)` untuk meneruskan hasil alat kembali ke model AI:

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.*;
import com.anthropic.models.messages.Model;
import java.util.List;

AnthropicClient client = AnthropicOkHttpClient.fromEnv();

MessageCreateParams.Builder createParamsBuilder = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_6)
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
              // Tambahkan pesan dengan hasil penggunaan alat yang diminta.
              .addUserMessageOfBetaContentBlockParams(
                      List.of(BetaContentBlockParam.ofToolResult(BetaToolResultBlockParam.builder()
                              .toolUseId(toolUseBlock.id())
                              .contentAsJson(callTool(toolUseBlock))
                              .build()))));

client.beta().messages().create(createParamsBuilder.build()).content().stream()
        .flatMap(contentBlock -> contentBlock.text().stream())
        .forEach(textBlock -> System.out.println(textBlock.text()));

private static Object callTool(BetaToolUseBlock toolUseBlock) {
  if (!"get_weather".equals(toolUseBlock.name())) {
    throw new IllegalArgumentException("Unknown tool: " + toolUseBlock.name());
  }

  GetWeather tool = toolUseBlock.input(GetWeather.class);
  return tool != null ? tool.execute() : new Weather("unknown");
}
```

### Konversi nama alat

Nama alat diturunkan dari nama kelas alat camel case (misalnya, `GetWeather`) dan dikonversi ke snake case (misalnya, `get_weather`). Batas kata dimulai di mana karakter saat ini bukan karakter pertama, huruf besar, dan baik karakter sebelumnya huruf kecil, atau karakter berikutnya huruf kecil. Misalnya, `MyJSONParser` menjadi `my_json_parser` dan `ParseJSON` menjadi `parse_json`. Konversi ini dapat ditimpa menggunakan anotasi `@JsonTypeName`.

### Validasi skema JSON alat lokal

Seperti untuk output terstruktur, Anda dapat melakukan validasi lokal untuk memeriksa bahwa skema JSON yang diturunkan dari kelas alat Anda menghormati pembatasan Anthropic. Validasi lokal diaktifkan secara default, tetapi dapat dinonaktifkan:

```java nocheck
MessageCreateParams.Builder createParamsBuilder = MessageCreateParams.builder()
  .model(Model.CLAUDE_OPUS_4_6)
  .maxTokens(2048)
  .addTool(GetWeather.class, JsonSchemaLocalValidation.NO)
  .addUserMessage("What's the temperature in New York?");
```

### Memberi anotasi pada kelas alat

Anda dapat menggunakan anotasi untuk menambahkan informasi lebih lanjut tentang alat ke skema JSON:

- `@JsonClassDescription` - Tambahkan deskripsi ke kelas alat yang merinci kapan dan bagaimana menggunakan alat tersebut.
- `@JsonTypeName` - Atur nama alat ke sesuatu selain nama sederhana kelas yang dikonversi ke snake case.
- `@JsonPropertyDescription` - Tambahkan deskripsi terperinci ke parameter alat.
- `@JsonIgnore` - Kecualikan bidang `public` atau metode getter dari skema JSON yang dihasilkan untuk parameter alat.
- `@JsonProperty` - Sertakan bidang non-`public` atau metode getter dalam skema JSON yang dihasilkan untuk parameter alat.

## Batch pesan

SDK menyediakan dukungan untuk [Message Batches API](/docs/id/build-with-claude/batch-processing) di bawah namespace `client.messages().batches()`. Lihat [bagian pagination](#pagination) untuk cara mengulangi hasil batch.

## Unggahan file

SDK mendefinisikan metode yang menerima file melalui antarmuka `MultipartField`:

```java nocheck
import com.anthropic.core.MultipartField;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileUploadParams;
import java.io.InputStream;
import java.nio.file.Paths;

FileUploadParams params = FileUploadParams.builder()
  .file(
    MultipartField.<InputStream>builder()
      .value(Files.newInputStream(Paths.get("/path/to/file.pdf")))
      .contentType("application/pdf")
      .build()
  )
  .addBeta(AnthropicBeta.FILES_API_2025_04_14)
  .build();

FileMetadata fileMetadata = client.beta().files().upload(params);
```

Atau dari `InputStream`:

```java nocheck
import com.anthropic.core.MultipartField;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileUploadParams;
import java.io.InputStream;
import java.net.URL;

FileUploadParams params = FileUploadParams.builder()
  .file(
    MultipartField.<InputStream>builder()
      .value(new URL("https://example.com/path/to/file").openStream())
      .filename("document.pdf")
      .contentType("application/pdf")
      .build()
  )
  .addBeta(AnthropicBeta.FILES_API_2025_04_14)
  .build();

FileMetadata fileMetadata = client.beta().files().upload(params);
```

Atau array `byte[]`:

```java nocheck
import com.anthropic.core.MultipartField;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileUploadParams;

FileUploadParams params = FileUploadParams.builder()
  .file(
    MultipartField.<byte[]>builder()
      .value("content".getBytes())
      .filename("document.txt")
      .contentType("text/plain")
      .build()
  )
  .addBeta(AnthropicBeta.FILES_API_2025_04_14)
  .build();

FileMetadata fileMetadata = client.beta().files().upload(params);
```

### Respons biner

SDK mendefinisikan metode yang mengembalikan respons biner untuk respons API yang tidak perlu diuraikan sebagai JSON:

```java nocheck
import com.anthropic.core.http.HttpResponse;
import com.anthropic.models.beta.files.FileDownloadParams;

HttpResponse response = client.beta().files().download("file_id");
```

Untuk menyimpan konten respons ke file:

```java nocheck
import com.anthropic.core.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

try (HttpResponse response = client.beta().files().download(params)) {
    Files.copy(
        response.body(),
        Paths.get(path),
        StandardCopyOption.REPLACE_EXISTING
    );
} catch (Exception e) {
    System.out.println("Something went wrong!");
    throw new RuntimeException(e);
}
```

Atau transfer konten respons ke `OutputStream` apa pun:

```java nocheck
import com.anthropic.core.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Paths;

try (HttpResponse response = client.beta().files().download(params)) {
    response.body().transferTo(Files.newOutputStream(Paths.get(path)));
} catch (Exception e) {
    System.out.println("Something went wrong!");
    throw new RuntimeException(e);
}
```

## Penanganan kesalahan

SDK melempar tipe pengecualian khusus yang tidak dicentang:

- `AnthropicServiceException` - Kelas dasar untuk kesalahan HTTP.
- `AnthropicIoException` - Kesalahan jaringan I/O.
- `AnthropicRetryableException` - Kesalahan generik yang menunjukkan kegagalan yang dapat dicoba ulang.
- `AnthropicInvalidDataException` - Kegagalan untuk menginterpretasikan data yang berhasil diuraikan (misalnya, saat mengakses properti yang seharusnya diperlukan, tetapi API secara tidak terduga menghilangkannya).
- `AnthropicException` - Kelas dasar untuk semua pengecualian.

### Pemetaan kode status

| Status | Pengecualian |
| ------ | --------- |
| 400    | `BadRequestException` |
| 401    | `UnauthorizedException` |
| 403    | `PermissionDeniedException` |
| 404    | `NotFoundException` |
| 422    | `UnprocessableEntityException` |
| 429    | `RateLimitException` |
| 5xx    | `InternalServerException` |
| others | `UnexpectedStatusCodeException` |

`SseException` dilempar untuk kesalahan yang ditemui selama streaming SSE setelah respons HTTP awal yang berhasil.

```java nocheck
import com.anthropic.errors.*;

try {
    Message message = client.messages().create(params);
} catch (RateLimitException e) {
    System.out.println("Rate limited, retry after: " + e.headers());
} catch (UnauthorizedException e) {
    System.out.println("Invalid API key");
} catch (AnthropicServiceException e) {
    System.out.println("API error: " + e.statusCode());
} catch (AnthropicIoException e) {
    System.out.println("Network error: " + e.getMessage());
}
```

## ID permintaan

Saat menggunakan respons mentah, Anda dapat mengakses header respons `request-id` menggunakan metode `requestId()`:

```java nocheck
import com.anthropic.core.http.HttpResponseFor;
import com.anthropic.models.messages.Message;
import java.util.Optional;

HttpResponseFor<Message> message = client.messages().withRawResponse().create(params);

Optional<String> requestId = message.requestId();
```

Ini dapat digunakan untuk dengan cepat mencatat permintaan yang gagal dan melaporkannya kembali ke Anthropic. Untuk informasi lebih lanjut tentang debugging permintaan, lihat [dokumentasi kesalahan API](/docs/id/api/errors#request-id).

## Percobaan ulang

SDK secara otomatis mencoba ulang 2 kali secara default, dengan backoff eksponensial pendek antara permintaan.

Hanya tipe kesalahan berikut yang dicoba ulang:

- Kesalahan koneksi (misalnya, karena masalah konektivitas jaringan)
- 408 Request Timeout
- 409 Conflict
- 429 Rate Limit
- 5xx Internal

API juga dapat secara eksplisit menginstruksikan SDK untuk mencoba ulang atau tidak mencoba ulang permintaan.

Untuk menetapkan jumlah percobaan ulang khusus, konfigurasi klien menggunakan metode `maxRetries`:

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder().fromEnv().maxRetries(4).build();
```

## Batas waktu

Permintaan habis waktu setelah 10 menit secara default.

Namun, untuk metode yang menerima `maxTokens`, jika Anda menentukan nilai `maxTokens` besar dan tidak streaming, maka batas waktu default akan dihitung secara dinamis menggunakan rumus ini:

```java nocheck
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

Ini menghasilkan batas waktu hingga 60 menit, diskalakan oleh parameter `maxTokens`, kecuali ditimpa.

Untuk menetapkan batas waktu khusus per-permintaan:

```java nocheck
import com.anthropic.models.messages.Message;

Message message = client
  .messages()
  .create(params, RequestOptions.builder().timeout(Duration.ofSeconds(30)).build());
```

Atau konfigurasi default untuk semua panggilan metode di tingkat klien:

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import java.time.Duration;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .timeout(Duration.ofSeconds(30))
  .build();
```

## Permintaan panjang

<Warning>
Pertimbangkan menggunakan [streaming](#streaming) untuk permintaan yang berjalan lebih lama.
</Warning>

Hindari menetapkan nilai `maxTokens` besar tanpa menggunakan streaming. Beberapa jaringan dapat menghapus koneksi idle setelah periode waktu tertentu, yang dapat menyebabkan permintaan gagal atau [habis waktu](#timeouts) tanpa menerima respons dari Anthropic. SDK secara berkala melakukan ping ke API untuk menjaga koneksi tetap hidup dan mengurangi dampak jaringan ini.

SDK melempar kesalahan jika permintaan non-streaming diperkirakan akan memakan waktu lebih lama dari 10 menit. Menggunakan [metode streaming](#streaming) atau [menimpa batas waktu](#timeouts) di tingkat klien atau permintaan menonaktifkan kesalahan.

## Pagination

SDK menyediakan cara yang mudah untuk mengakses hasil yang dipaginasi baik satu halaman sekaligus atau item demi item di semua halaman.

### Auto-pagination

Untuk mengulangi semua hasil di semua halaman, gunakan metode `autoPager()`, yang secara otomatis mengambil lebih banyak halaman sesuai kebutuhan.

```java nocheck
import com.anthropic.models.messages.batches.BatchListPage;
import com.anthropic.models.messages.batches.MessageBatch;

BatchListPage page = client.messages().batches().list();

// Proses sebagai Iterable
for (MessageBatch batch : page.autoPager()) {
    System.out.println(batch);
}

// Proses sebagai Stream
page.autoPager()
    .stream()
    .limit(50)
    .forEach(batch -> System.out.println(batch));
```

Saat menggunakan klien asinkron, metode mengembalikan `AsyncStreamResponse`:

```java nocheck
import com.anthropic.core.http.AsyncStreamResponse;
import com.anthropic.models.messages.batches.BatchListPageAsync;
import com.anthropic.models.messages.batches.MessageBatch;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

CompletableFuture<BatchListPageAsync> pageFuture = client.async().messages().batches().list();

pageFuture.thenAccept(page -> page.autoPager().subscribe(batch -> {
    System.out.println(batch);
}));

// Jika Anda perlu menangani kesalahan atau penyelesaian aliran
pageFuture.thenAccept(page -> page.autoPager().subscribe(new AsyncStreamResponse.Handler<>() {
    @Override
    public void onNext(MessageBatch batch) {
        System.out.println(batch);
    }

    @Override
    public void onComplete(Optional<Throwable> error) {
        if (error.isPresent()) {
            System.out.println("Something went wrong!");
            throw new RuntimeException(error.get());
        } else {
            System.out.println("No more!");
        }
    }
}));

// Atau gunakan futures
pageFuture.thenAccept(page -> page.autoPager()
    .subscribe(batch -> {
        System.out.println(batch);
    })
    .onCompleteFuture()
    .whenComplete((unused, error) -> {
        if (error != null) {
            System.out.println("Something went wrong!");
            throw new RuntimeException(error);
        } else {
            System.out.println("No more!");
        }
    }));
```

### Pagination manual

Untuk mengakses item halaman individual dan secara manual meminta halaman berikutnya:

```java nocheck
import com.anthropic.models.messages.batches.BatchListPage;
import com.anthropic.models.messages.batches.MessageBatch;

BatchListPage page = client.messages().batches().list();
while (true) {
    for (MessageBatch batch : page.items()) {
        System.out.println(batch);
    }

    if (!page.hasNextPage()) {
        break;
    }

    page = page.nextPage();
}
```

## Sistem tipe

### Immutability dan builders

Setiap kelas dalam SDK memiliki builder terkait untuk membangunnya. Setiap kelas tidak dapat diubah setelah dibangun. Jika kelas memiliki builder terkait, maka memiliki metode `toBuilder()`, yang dapat digunakan untuk mengonversinya kembali ke builder untuk membuat salinan yang dimodifikasi.

```java nocheck
MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_4_6)
  .build();

// Buat salinan yang dimodifikasi menggunakan toBuilder()
MessageCreateParams modified = params.toBuilder().maxTokens(2048L).build();
```

Karena setiap kelas tidak dapat diubah, modifikasi builder tidak akan pernah mempengaruhi instance kelas yang sudah dibangun.

### Permintaan dan respons

Untuk mengirim permintaan ke Claude API, bangun instance dari beberapa kelas `Params` dan teruskan ke metode klien yang sesuai. Ketika respons diterima, respons dideserialisasi ke instance kelas Java.

Misalnya, `client.messages().create(...)` harus dipanggil dengan instance `MessageCreateParams`, dan akan mengembalikan instance `Message`.

### Parameter yang tidak terdokumentasi

Untuk menetapkan parameter yang tidak terdokumentasi, panggil metode `putAdditionalHeader`, `putAdditionalQueryParam`, atau `putAdditionalBodyProperty` pada kelas `Params` apa pun:

```java nocheck
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.MessageCreateParams;

MessageCreateParams params = MessageCreateParams.builder()
  .putAdditionalHeader("Secret-Header", "42")
  .putAdditionalQueryParam("secret_query_param", "42")
  .putAdditionalBodyProperty("secretProperty", JsonValue.from("42"))
  .build();
```

Ini dapat diakses pada objek yang dibangun nanti menggunakan metode `_additionalHeaders()`, `_additionalQueryParams()`, dan `_additionalBodyProperties()`.

<Warning>
Nilai yang diteruskan ke metode ini menimpa nilai yang diteruskan ke metode sebelumnya. Untuk alasan keamanan, pastikan metode ini hanya digunakan dengan data input yang terpercaya.
</Warning>

Untuk menetapkan parameter yang tidak terdokumentasi pada header bersarang, parameter kueri, atau kelas body:

```java nocheck
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Metadata;

MessageCreateParams params = MessageCreateParams.builder()
  .metadata(
    Metadata.builder().putAdditionalProperty("secretProperty", JsonValue.from("42")).build()
  )
  .build();
```

Properti ini dapat diakses pada objek yang dibangun bersarang nanti menggunakan metode `_additionalProperties()`.

Untuk menetapkan parameter atau properti yang terdokumentasi ke nilai yang tidak terdokumentasi atau belum didukung, teruskan objek `JsonValue` ke setter-nya:

```java nocheck
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(JsonValue.from(3.14))
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_4_6)
  .build();
```

### Pembuatan JsonValue

Cara paling langsung untuk membuat `JsonValue` adalah menggunakan metode `from(...)` nya:

```java nocheck
import com.anthropic.core.JsonValue;
import java.util.List;
import java.util.Map;

// Create primitive JSON values
JsonValue nullValue = JsonValue.from(null);

JsonValue booleanValue = JsonValue.from(true);

JsonValue numberValue = JsonValue.from(42);

JsonValue stringValue = JsonValue.from("Hello World!");

// Create a JSON array value equivalent to `["Hello", "World"]`
JsonValue arrayValue = JsonValue.from(List.of("Hello", "World"));

// Create a JSON object value equivalent to `{ "a": 1, "b": 2 }`
JsonValue objectValue = JsonValue.from(Map.of("a", 1, "b", 2));

// Create an arbitrarily nested JSON equivalent to:
// { "a": [1, 2], "b": [3, 4] }
JsonValue complexValue = JsonValue.from(Map.of("a", List.of(1, 2), "b", List.of(3, 4)));
```

### Menghilangkan parameter yang diperlukan secara paksa

Biasanya metode `build` kelas `Builder` akan melempar `IllegalStateException` jika ada parameter atau properti yang diperlukan tidak diatur. Untuk menghilangkan parameter atau properti yang diperlukan secara paksa, teruskan `JsonMissing`:

```java nocheck
import com.anthropic.core.JsonMissing;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

MessageCreateParams params = MessageCreateParams.builder()
  .addUserMessage("Hello, world")
  .model(Model.CLAUDE_OPUS_4_6)
  .maxTokens(JsonMissing.of())
  .build();
```

### Properti respons

Untuk mengakses properti respons yang tidak terdokumentasi, panggil metode `_additionalProperties()`:

```java nocheck
import com.anthropic.core.JsonValue;
import java.util.Map;

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

    // Other methods include `visitMissing`, `visitString`, `visitArray`, and `visitObject`
    // The default implementation of each unimplemented method delegates to `visitDefault`,
    // which throws by default, but can also be overridden
});
```

Untuk mengakses nilai JSON mentah properti, panggil metode dengan awalan `_`:

```java nocheck
import com.anthropic.core.JsonField;
import java.util.Optional;

JsonField<Long> maxTokens = client.messages().create(params)._maxTokens();

if (maxTokens.isMissing()) {
  // The property is absent from the JSON response
} else if (maxTokens.isNull()) {
  // The property was set to literal null
} else {
  // Check if value was provided as a string
  // Other methods include `asNumber()`, `asBoolean()`, etc.
  Optional<String> jsonString = maxTokens.asString();

  // Try to deserialize into a custom type
  MyClass myObject = maxTokens.asUnknown().orElseThrow().convert(MyClass.class);
}
```

### Validasi respons

Secara default, SDK tidak melempar pengecualian ketika API mengembalikan respons yang tidak sesuai dengan tipe yang diharapkan. Ini melempar `AnthropicInvalidDataException` hanya jika Anda secara langsung mengakses properti.

Untuk memeriksa bahwa respons sepenuhnya well-typed di awal, panggil `validate()`:

```java nocheck
import com.anthropic.models.messages.Message;

Message message = client.messages().create(params).validate();
```

Atau konfigurasi per-permintaan:

```java nocheck
import com.anthropic.models.messages.Message;

Message message = client
  .messages()
  .create(params, RequestOptions.builder().responseValidation(true).build());
```

Atau konfigurasi default untuk semua panggilan metode di tingkat klien:

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .responseValidation(true)
  .build();
```

## Kustomisasi klien HTTP

### Konfigurasi proxy

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import java.net.InetSocketAddress;
import java.net.Proxy;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .proxy(new Proxy(Proxy.Type.HTTP, new InetSocketAddress("https://example.com", 8080)))
  .build();
```

### Konfigurasi HTTPS / SSL

<Note>
Sebagian besar aplikasi tidak boleh memanggil metode ini, dan sebaliknya menggunakan default sistem. Default mencakup optimisasi khusus yang dapat hilang jika implementasi dimodifikasi.
</Note>

```java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

AnthropicClient client = AnthropicOkHttpClient.builder()
  .fromEnv()
  .sslSocketFactory(yourSSLSocketFactory)
  .trustManager(yourTrustManager)
  .hostnameVerifier(yourHostnameVerifier)
  .build();
```

### Klien HTTP kustom

SDK terdiri dari tiga artefak:

- `anthropic-java-core` - Berisi logika SDK inti, tidak bergantung pada OkHttp. Mengekspos `AnthropicClient`, `AnthropicClientAsync`, dan kelas implementasinya, yang semuanya dapat bekerja dengan klien HTTP apa pun.
- `anthropic-java-client-okhttp` - Bergantung pada OkHttp. Mengekspos `AnthropicOkHttpClient` dan `AnthropicOkHttpClientAsync`.
- `anthropic-java` - Bergantung pada dan mengekspos API dari `anthropic-java-core` dan `anthropic-java-client-okhttp`. Tidak memiliki logika sendiri.

Struktur ini memungkinkan penggantian klien HTTP default SDK tanpa menarik dependensi yang tidak perlu.

#### OkHttpClient yang disesuaikan

<Tip>
Coba [opsi jaringan](#retries) yang tersedia sebelum mengganti klien default.
</Tip>

Untuk menggunakan `OkHttpClient` yang disesuaikan:

1. Ganti dependensi `anthropic-java` Anda dengan `anthropic-java-core`.
2. Salin kelas `OkHttpClient` dari `anthropic-java-client-okhttp` ke dalam kode Anda dan sesuaikan.
3. Bangun `AnthropicClientImpl` atau `AnthropicClientAsyncImpl` menggunakan klien yang disesuaikan Anda.

#### Klien HTTP yang sepenuhnya kustom

Untuk menggunakan klien HTTP yang sepenuhnya kustom:

1. Ganti dependensi `anthropic-java` Anda dengan `anthropic-java-core`.
2. Tulis kelas yang mengimplementasikan antarmuka `HttpClient`.
3. Bangun `AnthropicClientImpl` atau `AnthropicClientAsyncImpl` menggunakan kelas klien baru Anda.

## Integrasi platform

<Note>
Untuk panduan penyiapan platform terperinci dengan contoh kode, lihat:
- [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock)
- [Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)
- [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

Java SDK mendukung Bedrock, Vertex AI, dan Foundry melalui dependensi terpisah yang menyediakan implementasi `Backend` khusus platform:

- **Bedrock:** `com.anthropic:anthropic-java-bedrock`: Menggunakan `BedrockBackend.fromEnv()` atau `BedrockBackend.builder()`
- **Vertex AI:** `com.anthropic:anthropic-java-vertex`: Menggunakan `VertexBackend.fromEnv()` atau `VertexBackend.builder()`
- **Foundry:** `com.anthropic:anthropic-java-foundry`: Menggunakan `FoundryBackend.fromEnv()` atau `FoundryBackend.builder()`

Setiap backend diteruskan ke klien melalui `.backend()` pada `AnthropicOkHttpClient.builder()`. Kelas AWS, Google Cloud, dan Azure disertakan sebagai dependensi transitif dari perpustakaan masing-masing.

## Penggunaan lanjutan

### Akses respons mentah

Untuk mengakses header HTTP, kode status, dan badan respons mentah, awali panggilan metode HTTP apa pun dengan `withRawResponse()`:

```java nocheck
import com.anthropic.core.http.Headers;
import com.anthropic.core.http.HttpResponseFor;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

MessageCreateParams params = MessageCreateParams.builder()
  .maxTokens(1024L)
  .addUserMessage("Hello, Claude")
  .model(Model.CLAUDE_OPUS_4_6)
  .build();

HttpResponseFor<Message> message = client.messages().withRawResponse().create(params);

int statusCode = message.statusCode();

Headers headers = message.headers();
```

Anda masih dapat mendeserialisasi respons ke dalam instance kelas Java jika diperlukan:

```java nocheck
import com.anthropic.models.messages.Message;

Message parsedMessage = message.parse();
```

### Logging

SDK menggunakan interceptor logging OkHttp standar.

Aktifkan logging dengan menetapkan variabel lingkungan `ANTHROPIC_LOG` ke `info`:

```bash
export ANTHROPIC_LOG=info
```

Atau ke `debug` untuk logging yang lebih verbose:

```bash
export ANTHROPIC_LOG=debug
```

<section title="Kompatibilitas Jackson">

SDK bergantung pada Jackson untuk serialisasi/deserialisasi JSON. Ini kompatibel dengan versi 2.13.4 atau lebih tinggi, tetapi bergantung pada versi 2.18.2 secara default.

SDK melempar pengecualian jika mendeteksi versi Jackson yang tidak kompatibel pada runtime (misalnya jika versi default ditimpa dalam konfigurasi Maven atau Gradle Anda).

Jika SDK melempar pengecualian, tetapi Anda yakin versi tersebut kompatibel, maka nonaktifkan pemeriksaan versi menggunakan `checkJacksonVersionCompatibility` pada `AnthropicOkHttpClient` atau `AnthropicOkHttpClientAsync`.

<Warning>
Tidak ada jaminan bahwa SDK berfungsi dengan benar ketika pemeriksaan versi Jackson dinonaktifkan.
</Warning>

Ada juga bug di versi Jackson yang lebih lama yang dapat mempengaruhi SDK. SDK tidak mengatasi semua bug Jackson dan mengharapkan pengguna untuk meningkatkan Jackson sebagai gantinya.

</section>

<section title="Konfigurasi ProGuard/R8">

Meskipun SDK menggunakan refleksi, SDK masih dapat digunakan dengan ProGuard dan R8 karena `anthropic-java-core` dipublikasikan dengan file konfigurasi yang berisi aturan keep.

ProGuard dan R8 harus secara otomatis mendeteksi dan menggunakan aturan yang dipublikasikan, tetapi Anda juga dapat menyalin aturan keep secara manual jika diperlukan.

</section>

### Fungsionalitas API yang tidak terdokumentasi

SDK diketik untuk penggunaan yang nyaman dari API yang terdokumentasi. Namun, SDK juga mendukung bekerja dengan bagian API yang tidak terdokumentasi atau belum didukung.

#### Endpoint yang tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi, Anda dapat menggunakan metode `putAdditionalHeader`, `putAdditionalQueryParam`, atau `putAdditionalBodyProperty` seperti yang dijelaskan dalam [Parameter yang tidak terdokumentasi](#parameter-yang-tidak-terdokumentasi).

#### Properti respons yang tidak terdokumentasi

Untuk mengakses properti respons yang tidak terdokumentasi, gunakan metode `_additionalProperties()` seperti yang dijelaskan dalam [Properti respons](#properti-respons).

## Fitur beta

Anda dapat mengakses sebagian besar fitur API beta melalui metode `beta()` pada klien. Untuk memeriksa ketersediaan semua kemampuan dan alat Claude, lihat [gambaran umum build with Claude](/docs/id/build-with-claude/overview).

Misalnya, untuk menggunakan output terstruktur:

```java nocheck
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_6)
        .maxTokens(2048)
        .outputFormat(BookList.class)
        .addUserMessage("List some famous late twentieth century novels.")
        .build();

client.beta().messages().create(createParams);
```

## Pertanyaan yang sering diajukan

<section title="Mengapa SDK tidak menggunakan kelas enum biasa?">

Kelas `enum` Java tidak sepele kompatibel ke depan. Menggunakannya dalam SDK dapat menyebabkan pengecualian runtime jika API diperbarui untuk merespons dengan nilai enum baru.

</section>

<section title="Mengapa bidang direpresentasikan menggunakan JsonField<T> bukan hanya T biasa?">

Menggunakan `JsonField<T>` memungkinkan beberapa fitur:

- Memungkinkan penggunaan fungsionalitas API yang tidak terdokumentasi
- Validasi respons API secara malas terhadap bentuk yang diharapkan
- Mewakili nilai yang tidak ada vs secara eksplisit null

</section>

<section title="Mengapa SDK tidak menggunakan kelas data?">

Tidak kompatibel ke belakang untuk menambahkan bidang baru ke kelas data, dan SDK menghindari pengenalan perubahan yang merusak setiap kali bidang ditambahkan ke kelas.

</section>

<section title="Mengapa SDK tidak menggunakan pengecualian yang diperiksa?">

Pengecualian yang diperiksa secara luas dianggap sebagai kesalahan dalam bahasa pemrograman Java. Faktanya, mereka dihilangkan dari Kotlin karena alasan ini.

Pengecualian yang diperiksa:

- Verbose untuk ditangani
- Mendorong penanganan kesalahan pada tingkat abstraksi yang salah, di mana tidak ada yang dapat dilakukan tentang kesalahan
- Membosankan untuk dipropagasi karena masalah pewarnaan fungsi
- Tidak bermain dengan baik dengan lambda (juga karena masalah pewarnaan fungsi)

</section>

## Versioning semantik

Paket ini umumnya mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan tertentu yang tidak kompatibel ke belakang dapat dirilis sebagai versi minor:

1. Perubahan pada internal perpustakaan yang secara teknis publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
2. Perubahan yang tidak diharapkan berdampak pada sebagian besar pengguna dalam praktik.

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-java)
- [Javadocs](https://javadoc.io/doc/com.anthropic/anthropic-java)
- [Referensi API](/docs/id/api/overview)
- [Panduan streaming](/docs/id/build-with-claude/streaming)
- [Panduan penggunaan alat](/docs/id/agents-and-tools/tool-use/overview)