---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/ruby
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 870489607da23226eac775ffaed3cdf724fb0f78263413f219eec4330a280bd7
---

# Ruby SDK

Instal dan konfigurasikan Anthropic Ruby SDK dengan tipe Sorbet, helper streaming, dan connection pooling

---

Library Ruby Anthropic menyediakan akses yang mudah ke REST API Anthropic dari aplikasi Ruby 3.2.0+ mana pun. Library ini dilengkapi dengan tipe dan docstring yang komprehensif dalam Yard, RBS, dan RBI. `net/http` dari standard library digunakan sebagai transport HTTP, dengan "connection pooling" (pengumpulan koneksi) melalui gem `connection_pool`.

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK yang spesifik untuk Ruby.
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
  model: :"claude-opus-4-8"
)

message.content.each do |block|
  puts block.text if block.type == :text
end
```

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](/docs/id/manage-claude/authentication).

## Streaming

SDK menyediakan dukungan untuk streaming respons menggunakan Server-Sent Events (SSE).

```ruby
anthropic = Anthropic::Client.new
stream = anthropic.messages.stream(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-8"
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
  model: :"claude-opus-4-8"
)

stream.text.each do |text|
  print(text)
end
```

Streaming dengan `anthropic.messages.stream(...)` mengekspos berbagai helper termasuk akumulasi dan event khusus SDK.

## Skema input dan pemanggilan alat

SDK menyediakan mekanisme helper untuk mendefinisikan kelas data terstruktur untuk alat dan membiarkan Claude mengeksekusinya secara otomatis. Untuk dokumentasi terperinci tentang pola penggunaan alat termasuk tool runner, lihat [Tool Runner (SDK)](/docs/id/agents-and-tools/tool-use/tool-runner).

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

# Secara otomatis menangani loop eksekusi alat
anthropic.beta.messages.tool_runner(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{role: "user", content: "What's 15 * 7?"}],
  tools: [Calculator.new]
).each_message { |message| puts message.content }
```

## Output terstruktur

Untuk dokumentasi lengkap tentang output terstruktur termasuk contoh Ruby, lihat [Output terstruktur](/docs/id/build-with-claude/structured-outputs).

## Menangani error

Ketika library tidak dapat terhubung ke API, atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx), subclass dari `Anthropic::Errors::APIError` akan dimunculkan:

```ruby
anthropic = Anthropic::Client.new
begin
  message = anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-4-8"
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

Error tertentu akan secara otomatis dicoba ulang 2 kali secara default, dengan "exponential backoff" (penundaan eksponensial) yang singkat.

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
  model: :"claude-opus-4-8",
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
  model: :"claude-opus-4-8",
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

## Unggah file

Parameter permintaan yang berkaitan dengan unggahan file dapat diberikan sebagai konten mentah, instance [`Pathname`](https://rubyapi.org/3.2/o/pathname), [`StringIO`](https://rubyapi.org/3.2/o/stringio), atau lainnya.

```ruby
anthropic = Anthropic::Client.new
require "pathname"

# Gunakan `Pathname` untuk mengirim nama file dan/atau menghindari memuat file besar ke dalam memori:
file_metadata = anthropic.beta.files.upload(file: Pathname("/path/to/file"))

# Sebagai alternatif, berikan isi file atau `StringIO` secara langsung:
file_metadata = anthropic.beta.files.upload(file: File.read("/path/to/file"))

# Atau, untuk mengontrol nama file dan/atau tipe konten:
file = Anthropic::FilePart.new(File.read("/path/to/file"), filename: "/path/to/file", content_type: "...")
file_metadata = anthropic.beta.files.upload(file: file)

puts(file_metadata.id)
```

Perhatikan bahwa Anda juga dapat memberikan deskriptor `IO` mentah, tetapi ini menonaktifkan percobaan ulang, karena library tidak dapat memastikan apakah deskriptor tersebut adalah file atau pipe (yang tidak dapat di-rewind).

## Sorbet

Library ini menyediakan definisi [RBI](https://sorbet.org/docs/rbi) yang komprehensif, dan tidak memiliki dependensi pada sorbet-runtime.

Anda dapat memberikan parameter permintaan yang typesafe seperti berikut:

```ruby
anthropic = Anthropic::Client.new
anthropic.messages.create(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-4-8"
)
```

Atau, secara ekuivalen:

```ruby
anthropic = Anthropic::Client.new
# Hash dapat digunakan, tetapi tidak typesafe:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-8"
)

# Anda juga dapat melakukan splat pada kelas Params lengkap:
params = Anthropic::MessageCreateParams.new(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-4-8"
)
anthropic.messages.create(**params)
```

### Enum

Karena library ini tidak bergantung pada `sorbet-runtime`, library ini tidak dapat menyediakan instance [`T::Enum`](https://sorbet.org/docs/tenum). Sebagai gantinya, SDK menyediakan "tagged symbols", yang selalu berupa primitif saat runtime:

```ruby
# :auto
puts(Anthropic::MessageCreateParams::ServiceTier::AUTO)

# Tipe yang terungkap: `T.all(Anthropic::MessageCreateParams::ServiceTier, Symbol)`
T.reveal_type(Anthropic::MessageCreateParams::ServiceTier::AUTO)
```

Parameter enum memiliki tipe yang "longgar", sehingga Anda dapat memberikan konstanta enum atau nilai literalnya:

```ruby
# Menggunakan konstanta enum mempertahankan informasi tipe yang ditandai:
anthropic.messages.create(
  service_tier: Anthropic::MessageCreateParams::ServiceTier::AUTO,
  # ...
)

# Nilai literal juga diperbolehkan:
anthropic.messages.create(
  service_tier: :auto,
  # ...
)
```

## BaseModel

Semua objek parameter dan respons mewarisi dari `Anthropic::Internal::Type::BaseModel`, yang menyediakan beberapa kemudahan, termasuk:

1. Semua field, termasuk yang tidak dikenal, dapat diakses dengan sintaks `obj[:prop]`, dan dapat di-destructure dengan `obj => {prop: prop}` atau sintaks pattern-matching.

2. Ekuivalensi struktural untuk kesetaraan; jika dua panggilan API mengembalikan nilai yang sama, membandingkan respons dengan == akan mengembalikan true.

3. Baik instance maupun kelasnya sendiri dapat di-pretty-print.

4. Helper seperti `#to_h`, `#deep_to_h`, `#to_json`, dan `#to_yaml`.

## Konkurensi dan connection pooling

Instance `Anthropic::Client` bersifat threadsafe, tetapi hanya fork-safe ketika tidak ada permintaan HTTP yang sedang berlangsung.

Setiap instance `Anthropic::Client` memiliki pool koneksi HTTP sendiri dengan ukuran default 99. Oleh karena itu, rekomendasinya adalah membuat client satu kali per aplikasi dalam sebagian besar situasi.

Ketika semua koneksi yang tersedia dari pool sudah digunakan, permintaan akan menunggu koneksi baru tersedia, dengan waktu antrean dihitung ke dalam timeout permintaan.

Kecuali ditentukan lain, kelas lain dalam SDK tidak memiliki lock yang melindungi struktur data yang mendasarinya.

## Membuat permintaan kustom atau tidak terdokumentasi

### Properti tidak terdokumentasi

Anda dapat mengirim parameter yang tidak terdokumentasi ke endpoint mana pun, dan membaca properti respons yang tidak terdokumentasi, seperti berikut:

<Warning>
  Parameter `extra_` dengan nama yang sama akan menimpa parameter yang terdokumentasi. Untuk alasan keamanan, pastikan metode ini hanya digunakan dengan data input yang tepercaya.
</Warning>

```ruby
anthropic = Anthropic::Client.new
value = "example"
message =
  anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-4-8",
    request_options: {
      extra_query: {my_query_parameter: value},
      extra_body: {my_body_parameter: value},
      extra_headers: {"my-header": value}
    }
  )

puts(message[:my_undocumented_property])
```

### Parameter permintaan tidak terdokumentasi

Jika Anda ingin secara eksplisit mengirim parameter tambahan, Anda dapat melakukannya dengan `extra_query`, `extra_body`, dan `extra_headers` di bawah parameter `request_options:` saat membuat permintaan, seperti yang terlihat pada contoh di atas.

### Endpoint tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi sambil tetap mendapatkan manfaat dari autentikasi, percobaan ulang, dan sebagainya, Anda dapat membuat permintaan menggunakan `anthropic.request`, seperti berikut:

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
  Untuk panduan penyiapan platform yang terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai)
</Note>

Ruby SDK mendukung platform berikut:

* **Agent Platform:** `Anthropic::VertexClient`. Memerlukan gem `googleauth`.
* **Bedrock:** `Anthropic::BedrockMantleClient`, atau `Anthropic::BedrockClient` untuk jalur `bedrock-runtime`. `Anthropic::BedrockMantleClient` memerlukan gem `aws-sdk-core`; `Anthropic::BedrockClient` memerlukan gem `aws-sdk-bedrockruntime`.
* **Claude Platform di AWS:** Bagian dari gem `anthropic` utama (memerlukan gem `aws-sdk-core`). Menyediakan `Anthropic::AWSClient`. Berikan `workspace_id:` ke konstruktor atau atur variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID` (lihat [Workspaces](/docs/id/build-with-claude/claude-platform-on-aws#workspaces)). Tersedia dalam beta.
* **Foundry:** Saat ini tidak didukung di Ruby SDK. Lihat [Claude di Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) untuk SDK yang didukung.

Gunakan `Anthropic::BedrockMantleClient` untuk proyek baru; `Anthropic::BedrockClient` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan API `InvokeModel` Bedrock.

## Semantic versioning

Paket ini mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html). Karena library ini masih dalam pengembangan awal dan memiliki versi mayor `0`, API dapat berubah kapan saja.

Paket ini menganggap peningkatan pada definisi tipe `*.rbi` dan `*.rbs` (non-runtime) sebagai perubahan yang tidak merusak (non-breaking).

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-ruby)
* [Dokumentasi YARD](https://gemdocs.org/gems/anthropic)
* [Referensi API](/docs/id/api/overview)
* [Streaming Messages](/docs/id/build-with-claude/streaming)
