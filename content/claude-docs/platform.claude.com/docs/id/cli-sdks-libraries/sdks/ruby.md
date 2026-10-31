---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/ruby
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: d7c42a0357d9d5ca18e85614b0876e0c2457a4736e8a5896758eafcd6d7b8127
---

---
title: Ruby SDK
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/ruby
description: Instal dan konfigurasikan Anthropic Ruby SDK dengan tipe Sorbet, helper streaming, dan connection pooling
---

Library Ruby Anthropic menyediakan akses yang mudah ke Claude API dari aplikasi Ruby 3.2.0+ mana pun. Library ini dilengkapi dengan tipe dan docstring yang komprehensif dalam YARD, RBS, dan RBI. `net/http` dari library standar digunakan sebagai transport HTTP, dengan “connection pooling” (penggabungan koneksi) melalui gem `connection_pool`.

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](https://platform.claude.com/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK yang khusus untuk Ruby.
</Info>

## Instalasi

Tambahkan gem ke `Gemfile` aplikasi Anda dengan Bundler:

```bash
bundle add anthropic
```

## Persyaratan

Ruby 3.2.0 atau lebih tinggi.

## Penggunaan

```ruby
anthropic = Anthropic::Client.new(
  api_key: ENV["ANTHROPIC_API_KEY"] # This is the default and can be omitted
)

message = anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5-5"
)

message.content.each do |block|
  puts block.text if block.type == :text
end
```

Untuk opsi autentikasi termasuk “Workload Identity Federation” (federasi identitas beban kerja), lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication). Jika kunci API Anda adalah [kunci akun pribadi atau akun layanan](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) yang tidak dibatasi pada suatu workspace, atur ID workspace di header permintaan `anthropic-workspace-id`; [Pilih workspace](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace) menunjukkan opsi per permintaan untuk SDK ini.

## Streaming

SDK menyediakan dukungan untuk respons streaming menggunakan “Server-Sent Events” (peristiwa yang dikirim server), atau SSE.

```ruby
anthropic = Anthropic::Client.new
stream = anthropic.messages.stream(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5-5"
)

stream.each do |message|
  puts(message.type)
end
```

### Helper streaming

Library ini menyediakan beberapa kemudahan untuk streaming pesan, misalnya:

```ruby
anthropic = Anthropic::Client.new
stream = anthropic.messages.stream(
  max_tokens: 1024,
  messages: [{role: :user, content: "Say hello there!"}],
  model: :"claude-opus-5-5"
)

stream.text.each do |text|
  print(text)
end
```

Streaming dengan `anthropic.messages.stream(...)` menyediakan berbagai helper termasuk akumulasi dan event khusus SDK.

## Skema input dan pemanggilan alat

SDK menyediakan mekanisme helper untuk mendefinisikan kelas data terstruktur untuk alat dan memungkinkan Claude mengeksekusinya secara otomatis. Untuk dokumentasi terperinci tentang pola penggunaan alat termasuk tool runner, lihat [Tool Runner (SDK)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner).

```ruby
anthropic = Anthropic::Client.new
class CalculatorInput < Anthropic::BaseModel
  required :lhs, Float
  required :rhs, Float
  required :operator, Anthropic::InputSchema::EnumOf[:+, :-, :*, :/]
end

class Calculator < Anthropic::BaseTool
  input_schema CalculatorInput

  def call(expr)
    expr.lhs.public_send(expr.operator, expr.rhs)
  end
end

# Menangani loop eksekusi alat secara otomatis
anthropic.beta.messages.tool_runner(
  model: "claude-opus-5-5",
  max_tokens: 1024,
  messages: [{role: "user", content: "What's 15 * 7?"}],
  tools: [Calculator.new]
).each_message { |message| puts message.content }
```

## Output terstruktur

Untuk dokumentasi lengkap tentang output terstruktur termasuk contoh Ruby, lihat [Output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs).

## Menangani error

Ketika library tidak dapat terhubung ke API, atau jika API mengembalikan kode status yang tidak berhasil (yaitu, respons 4xx atau 5xx), subkelas dari `Anthropic::Errors::APIError` akan dimunculkan:

```ruby
anthropic = Anthropic::Client.new
begin
  message = anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-5-5"
  )
rescue Anthropic::Errors::APIConnectionError => e
  puts("The server could not be reached")
  puts(e.cause)  # an underlying Exception, likely raised within `net/http`
rescue Anthropic::Errors::RateLimitError => e
  puts("A 429 status code was received; we should back off a bit.")
rescue Anthropic::Errors::APIStatusError => e
  puts("Another non-200-range status code was received")
  puts(e.status)
end
```

Kode error adalah sebagai berikut:

| Penyebab           | Tipe Error                 |
| ------------------ | -------------------------- |
| HTTP 400           | `BadRequestError`          |
| HTTP 401           | `AuthenticationError`      |
| HTTP 403           | `PermissionDeniedError`    |
| HTTP 404           | `NotFoundError`            |
| HTTP 409           | `ConflictError`            |
| HTTP 422           | `UnprocessableEntityError` |
| HTTP 429           | `RateLimitError`           |
| HTTP >= 500        | `InternalServerError`      |
| Error HTTP lainnya | `APIStatusError`           |
| Timeout            | `APITimeoutError`          |
| Error jaringan     | `APIConnectionError`       |

## Percobaan ulang

Error tertentu akan dicoba ulang secara otomatis sebanyak 2 kali secara default, dengan “exponential backoff” (penundaan eksponensial) yang singkat.

Error koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, error Internal >=500, dan timeout semuanya dicoba ulang secara default.

Anda dapat menggunakan opsi `max_retries` untuk mengonfigurasi atau menonaktifkan ini:

```ruby
# Konfigurasikan default untuk semua permintaan:
anthropic = Anthropic::Client.new(
  max_retries: 0 # default is 2
)

# Atau, konfigurasikan per permintaan:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5-5",
  request_options: {max_retries: 5}
)
```

## Timeout

Secara default, permintaan akan timeout setelah 10 menit. Anda dapat menggunakan opsi `timeout` untuk mengonfigurasi ini:

```ruby
# Konfigurasikan default untuk semua permintaan:
anthropic = Anthropic::Client.new(
  timeout: 20 # 20 seconds (default is 10 minutes)
)

# Atau, konfigurasikan per permintaan:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5-5",
  request_options: {timeout: 5}
)
```

Saat timeout, `Anthropic::Errors::APITimeoutError` akan dimunculkan.

Perhatikan bahwa permintaan yang timeout akan dicoba ulang secara default.

## Paginasi

Metode list di Claude API menggunakan paginasi.

Library ini menyediakan iterator dengan paginasi otomatis pada setiap respons list, sehingga Anda tidak perlu meminta halaman berikutnya secara manual:

```ruby
anthropic = Anthropic::Client.new
page = anthropic.messages.batches.list(limit: 20)

# Mengambil satu item dari halaman.
batch = page.data[0]
puts(batch.id)

# Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
page.auto_paging_each do |batch|
  puts(batch.id)
end
```

Sebagai alternatif, Anda dapat menggunakan metode `#next_page?` dan `#next_page` untuk kontrol yang lebih terperinci saat bekerja dengan halaman.

```ruby
anthropic = Anthropic::Client.new
page = anthropic.messages.batches.list(limit: 20)
loop do
  page.data&.each { |batch| puts(batch.id) }
  break unless page.next_page?
  page = page.next_page
end
```

## Unggahan file

Parameter permintaan yang berkaitan dengan unggahan file dapat diteruskan sebagai konten mentah, instance [`Pathname`](https://rubyapi.org/3.2/o/pathname), [`StringIO`](https://rubyapi.org/3.2/o/stringio), atau lainnya.

```ruby
anthropic = Anthropic::Client.new
require "pathname"

# Gunakan `Pathname` untuk mengirim nama file dan/atau menghindari memuat file besar ke memori:
file_metadata = anthropic.files.upload(file: Pathname("/path/to/file"))

# Sebagai alternatif, teruskan isi file atau `StringIO` secara langsung:
file_metadata = anthropic.files.upload(file: File.read("/path/to/file"))

# Atau, untuk mengontrol nama file dan/atau tipe konten:
file = Anthropic::FilePart.new(File.read("/path/to/file"), filename: "/path/to/file", content_type: "...")
file_metadata = anthropic.files.upload(file: file)

puts(file_metadata.id)
```

Perhatikan bahwa Anda juga dapat meneruskan deskriptor `IO` mentah, tetapi ini menonaktifkan percobaan ulang, karena library tidak dapat memastikan apakah deskriptor tersebut adalah file atau pipe (yang tidak dapat diputar ulang).

## Sorbet

Library ini menyediakan definisi [RBI](https://sorbet.org/docs/rbi) yang komprehensif, dan tidak memiliki dependensi pada sorbet-runtime.

Anda dapat memberikan parameter permintaan yang typesafe seperti ini:

```ruby
anthropic = Anthropic::Client.new
anthropic.messages.create(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-5-5"
)
```

Atau, secara setara:

```ruby
anthropic = Anthropic::Client.new
# Hash dapat digunakan, tetapi tidak typesafe:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5-5"
)

# Anda juga dapat melakukan splat pada seluruh kelas Params:
params = Anthropic::MessageCreateParams.new(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-5-5"
)
anthropic.messages.create(**params)
```

### Enum

Karena library ini tidak bergantung pada `sorbet-runtime`, library ini tidak dapat menyediakan instance [`T::Enum`](https://sorbet.org/docs/tenum). Sebagai gantinya, SDK menyediakan “tagged symbols” (simbol bertag), yang selalu berupa primitif saat runtime:

```ruby
# :auto
puts(Anthropic::MessageCreateParams::ServiceTier::AUTO)

# Tipe yang terungkap: `T.all(Anthropic::MessageCreateParams::ServiceTier, Symbol)`
T.reveal_type(Anthropic::MessageCreateParams::ServiceTier::AUTO)
```

Parameter enum memiliki tipe yang “longgar”, sehingga Anda dapat meneruskan konstanta enum atau nilai literalnya:

```ruby
anthropic = Anthropic::Client.new
# Menggunakan konstanta enum mempertahankan informasi tipe bertag:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: Anthropic::Model::CLAUDE_OPUS_5_5,
  service_tier: Anthropic::MessageCreateParams::ServiceTier::AUTO
)

# Nilai literal juga diperbolehkan:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5-5",
  service_tier: :auto
)
```

## BaseModel

Semua objek parameter dan respons mewarisi dari `Anthropic::Internal::Type::BaseModel`, yang menyediakan beberapa kemudahan, termasuk:

1. Semua field, termasuk yang tidak dikenal, dapat diakses dengan sintaks `obj[:prop]`, dan dapat didestrukturisasi dengan `obj => {prop: prop}` atau sintaks pattern-matching.

2. Ekuivalensi struktural untuk kesetaraan. Jika dua panggilan API mengembalikan nilai yang sama, membandingkan respons dengan == akan mengembalikan true.

3. Baik instance maupun kelasnya sendiri dapat di-pretty-print.

4. Helper seperti `#to_h`, `#deep_to_h`, `#to_json`, dan `#to_yaml`.

## Konkurensi dan connection pooling

Instance `Anthropic::Client` bersifat threadsafe, tetapi hanya fork-safe ketika tidak ada permintaan HTTP yang sedang berlangsung.

Setiap instance `Anthropic::Client` memiliki connection pool HTTP sendiri dengan ukuran default 99. Oleh karena itu, rekomendasinya adalah membuat client sekali per aplikasi di sebagian besar pengaturan.

Ketika semua koneksi yang tersedia dari pool sedang digunakan, permintaan akan menunggu koneksi baru tersedia, dengan waktu antrean dihitung terhadap timeout permintaan.

Kecuali dinyatakan lain, kelas-kelas lain dalam SDK tidak memiliki lock yang melindungi struktur data dasarnya.

## Tracing OpenTelemetry

Saat aplikasi Anda mendaftarkan tracer provider OpenTelemetry, SDK memancarkan span untuk setiap permintaan yang dikirimnya. Untuk mengirim span ke platform observabilitas Anda, lihat [Menyiapkan OpenTelemetry dengan Claude SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk).

## Membuat permintaan kustom atau yang tidak terdokumentasi

### Properti yang tidak terdokumentasi

Anda dapat mengirim parameter yang tidak terdokumentasi ke endpoint mana pun, dan membaca properti respons yang tidak terdokumentasi, seperti ini:

<Warning>
  Parameter `extra_` dengan nama yang sama akan menimpa parameter yang terdokumentasi. Demi alasan keamanan, pastikan metode ini hanya digunakan dengan data input yang tepercaya.
</Warning>

```ruby
anthropic = Anthropic::Client.new
value = "example"
message =
  anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-5-5",
    request_options: {
      extra_query: {my_query_parameter: value},
      extra_body: {my_body_parameter: value},
      extra_headers: {"my-header": value}
    }
  )

puts(message[:my_undocumented_property])
```

### Parameter permintaan yang tidak terdokumentasi

Jika Anda ingin mengirim parameter tambahan secara eksplisit, Anda dapat melakukannya dengan `extra_query`, `extra_body`, dan `extra_headers` di bawah parameter `request_options:` saat membuat permintaan, seperti yang terlihat pada contoh sebelumnya.

### Endpoint yang tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi sambil tetap mempertahankan manfaat autentikasi, percobaan ulang, dan sebagainya, Anda dapat membuat permintaan menggunakan `anthropic.request`, seperti ini:

```ruby
response = anthropic.request(
  method: :post,
  path: '/undocumented/endpoint',
  query: {"dog": "woof"},
  headers: {"useful-header": "interesting-value"},
  body: {"hello": "world"}
)
```

## Integrasi platform

<Note>
  Untuk panduan penyiapan platform terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)
  * [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed)

  Lihat juga [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed).
</Note>

Ruby SDK mendukung platform berikut:

* **Claude Models on Google Cloud (Google managed):** `Anthropic::VertexClient`. Memerlukan gem `googleauth`.
* **Bedrock:** `Anthropic::BedrockMantleClient`, atau `Anthropic::BedrockClient` untuk jalur `bedrock-runtime`. `Anthropic::BedrockMantleClient` memerlukan gem `aws-sdk-core`; `Anthropic::BedrockClient` memerlukan gem `aws-sdk-bedrockruntime`.
* **Claude Platform di AWS:** Bagian dari gem utama `anthropic` (memerlukan gem `aws-sdk-core`). Menyediakan `Anthropic::AWSClient`. Teruskan `workspace_id:` ke konstruktor atau atur variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID` (lihat [Workspace](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#workspaces)). Tersedia dalam beta.
* **Foundry:** Saat ini tidak didukung di Ruby SDK. Lihat [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) untuk SDK yang didukung.

Gunakan `Anthropic::BedrockMantleClient` untuk proyek baru; `Anthropic::BedrockClient` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan API `InvokeModel` Bedrock.

Ruby SDK juga mendukung Claude Models on Google Cloud (Anthropic managed) melalui `Anthropic::GoogleCloudClient`. Klien ini masih dalam tahap beta. Klien ini disertakan dalam gem utama `anthropic` dan memerlukan gem `googleauth`. Berikan `workspace_id:` ke konstruktor atau atur variabel lingkungan `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID`. Lihat [Resolusi proyek, lokasi, dan workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution) untuk mengetahui cara klien menentukan ID workspace.

## Semantic versioning

Setiap versi mayor SDK ini mengirimkan satu versi API di header `anthropic-version` secara default, dan versi mayor baru hadir bersama setiap versi API baru. Versi mayor pertama yang mengirimkan `2026-10-21` adalah 2.0.0; lihat [Migrasi ke versi API 2026-10-21](https://platform.claude.com/docs/id/api/migration-2026-10-21#upgrade).

Paket ini mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html).

Paket ini menganggap peningkatan pada definisi tipe `*.rbi` dan `*.rbs` (non-runtime) sebagai perubahan yang tidak merusak kompatibilitas.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-ruby)
* [Dokumentasi YARD](https://gemdocs.org/gems/anthropic)
* [Referensi API](https://platform.claude.com/docs/id/api/overview)
* [Streaming Pesan](https://platform.claude.com/docs/id/build-with-claude/streaming)
