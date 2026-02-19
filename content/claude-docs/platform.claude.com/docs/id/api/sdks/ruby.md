---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/ruby
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: 804b90a8467f9be55df1dd1fe607cbd68741fae64314421911c948541d8ebbda
---

# Ruby SDK

Instal dan konfigurasi Anthropic Ruby SDK dengan tipe Sorbet, pembantu streaming, dan connection pooling

---

Perpustakaan Ruby Anthropic menyediakan akses yang mudah ke Anthropic REST API dari aplikasi Ruby 3.2.0+ apa pun. Dilengkapi dengan tipe komprehensif dan docstring di Yard, RBS, dan RBI. Perpustakaan standar `net/http` digunakan sebagai transport HTTP, dengan connection pooling melalui gem `connection_pool`.

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus Ruby dan konfigurasi.
</Info>

## Instalasi

Untuk menggunakan gem ini, instal melalui Bundler dengan menambahkan berikut ke `Gemfile` aplikasi Anda:

```ruby
gem "anthropic", "~> 1.16.3"
```

## Persyaratan

Ruby 3.2.0 atau lebih tinggi.

## Penggunaan

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(
  api_key: ENV["ANTHROPIC_API_KEY"] # Ini adalah default dan dapat dihilangkan
)

message = anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-6"
)

puts(message.content)
```

## Streaming

Kami menyediakan dukungan untuk respons streaming menggunakan Server-Sent Events (SSE).

```ruby
stream = anthropic.messages.stream(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-6"
)

stream.each do |message|
  puts(message.type)
end
```

### Pembantu streaming

Perpustakaan ini menyediakan beberapa kemudahan untuk pesan streaming, misalnya:

```ruby
stream = anthropic.messages.stream(
  max_tokens: 1024,
  messages: [{role: :user, content: "Say hello there!"}],
  model: :"claude-opus-4-6"
)

stream.text.each do |text|
  print(text)
end
```

Streaming dengan `anthropic.messages.stream(...)` mengekspos berbagai pembantu termasuk akumulasi dan peristiwa khusus SDK.

## Skema Input dan Pemanggilan Alat

SDK menyediakan mekanisme pembantu untuk menentukan kelas data terstruktur untuk alat dan membiarkan Claude secara otomatis menjalankannya. Untuk dokumentasi terperinci tentang pola penggunaan alat termasuk tool runner, lihat [Mengimplementasikan Penggunaan Alat](/docs/id/agents-and-tools/tool-use/implement-tool-use).

```ruby
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
client.beta.messages.tool_runner(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{role: "user", content: "What's 15 * 7?"}],
  tools: [Calculator.new]
).each_message { puts _1.content }
```

## Menangani kesalahan

Ketika perpustakaan tidak dapat terhubung ke API, atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx), subkelas `Anthropic::Errors::APIError` akan dilempar:

```ruby
begin
  message = anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-4-6"
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

Kode kesalahan adalah sebagai berikut:

| Penyebab          | Tipe Kesalahan             |
| ----------------- | -------------------------- |
| HTTP 400          | `BadRequestError`          |
| HTTP 401          | `AuthenticationError`      |
| HTTP 403          | `PermissionDeniedError`    |
| HTTP 404          | `NotFoundError`            |
| HTTP 409          | `ConflictError`            |
| HTTP 422          | `UnprocessableEntityError` |
| HTTP 429          | `RateLimitError`           |
| HTTP >= 500       | `InternalServerError`      |
| Kesalahan HTTP lainnya | `APIStatusError`           |
| Timeout           | `APITimeoutError`          |
| Kesalahan jaringan | `APIConnectionError`       |

## Percobaan Ulang

Kesalahan tertentu akan secara otomatis dicoba ulang 2 kali secara default, dengan backoff eksponensial singkat.

Kesalahan koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, >=500 kesalahan Internal, dan timeout semuanya akan dicoba ulang secara default.

Anda dapat menggunakan opsi `max_retries` untuk mengonfigurasi atau menonaktifkan ini:

```ruby
# Konfigurasi default untuk semua permintaan:
anthropic = Anthropic::Client.new(
  max_retries: 0 # default adalah 2
)

# Atau, konfigurasi per-permintaan:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-6",
  request_options: {max_retries: 5}
)
```

## Timeout

Secara default, permintaan akan timeout setelah 600 detik. Anda dapat menggunakan opsi timeout untuk mengonfigurasi atau menonaktifkan ini:

```ruby
# Konfigurasi default untuk semua permintaan:
anthropic = Anthropic::Client.new(
  timeout: nil # default adalah 600
)

# Atau, konfigurasi per-permintaan:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-6",
  request_options: {timeout: 5}
)
```

Pada timeout, `Anthropic::Errors::APITimeoutError` dilempar.

Perhatikan bahwa permintaan yang timeout dicoba ulang secara default.

## Paginasi

Metode daftar dalam Claude API dipaginasi.

Perpustakaan ini menyediakan iterator auto-paging dengan setiap respons daftar, sehingga Anda tidak perlu meminta halaman berturut-turut secara manual:

```ruby
page = anthropic.messages.batches.list(limit: 20)

# Ambil item tunggal dari halaman.
batch = page.data[0]
puts(batch.id)

# Secara otomatis mengambil lebih banyak halaman sesuai kebutuhan.
page.auto_paging_each do |batch|
  puts(batch.id)
end
```

Alternatifnya, Anda dapat menggunakan metode `#next_page?` dan `#next_page` untuk kontrol yang lebih terperinci saat bekerja dengan halaman.

```ruby
if page.next_page?
  new_page = page.next_page
  puts(new_page.data[0].id)
end
```

## Unggahan file

Parameter permintaan yang sesuai dengan unggahan file dapat diteruskan sebagai konten mentah, instance [`Pathname`](https://rubyapi.org/3.2/o/pathname), [`StringIO`](https://rubyapi.org/3.2/o/stringio), atau lainnya.

```ruby
require "pathname"

# Gunakan `Pathname` untuk mengirim nama file dan/atau menghindari paging file besar ke memori:
file_metadata = anthropic.beta.files.upload(file: Pathname("/path/to/file"))

# Alternatifnya, teruskan konten file atau `StringIO` secara langsung:
file_metadata = anthropic.beta.files.upload(file: File.read("/path/to/file"))

# Atau, untuk mengontrol nama file dan/atau tipe konten:
file = Anthropic::FilePart.new(File.read("/path/to/file"), filename: "/path/to/file", content_type: "...")
file_metadata = anthropic.beta.files.upload(file: file)

puts(file_metadata.id)
```

Perhatikan bahwa Anda juga dapat melewatkan deskriptor `IO` mentah, tetapi ini menonaktifkan percobaan ulang, karena perpustakaan tidak dapat memastikan apakah deskriptor adalah file atau pipa (yang tidak dapat diputar ulang).

## Sorbet

Perpustakaan ini menyediakan definisi [RBI](https://sorbet.org/docs/rbi) komprehensif, dan tidak memiliki ketergantungan pada sorbet-runtime.

Anda dapat menyediakan parameter permintaan yang aman tipe seperti ini:

```ruby
anthropic.messages.create(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-4-6"
)
```

Atau, secara setara:

```ruby
# Hash berfungsi, tetapi tidak aman tipe:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-6"
)

# Anda juga dapat splat kelas Params lengkap:
params = Anthropic::MessageCreateParams.new(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-4-6"
)
anthropic.messages.create(**params)
```

### Enum

Karena perpustakaan ini tidak bergantung pada `sorbet-runtime`, ia tidak dapat menyediakan instance [`T::Enum`](https://sorbet.org/docs/tenum). Sebagai gantinya, kami menyediakan "simbol yang ditandai" sebagai gantinya, yang selalu primitif pada waktu runtime:

```ruby
# :auto
puts(Anthropic::MessageCreateParams::ServiceTier::AUTO)

# Tipe yang diungkapkan: `T.all(Anthropic::MessageCreateParams::ServiceTier, Symbol)`
T.reveal_type(Anthropic::MessageCreateParams::ServiceTier::AUTO)
```

Parameter enum memiliki tipe "santai", sehingga Anda dapat melewatkan konstanta enum atau nilai literalnya:

```ruby
# Menggunakan konstanta enum mempertahankan informasi tipe yang ditandai:
anthropic.messages.create(
  service_tier: Anthropic::MessageCreateParams::ServiceTier::AUTO,
  # ...
)

# Nilai literal juga diizinkan:
anthropic.messages.create(
  service_tier: :auto,
  # ...
)
```

## BaseModel

Semua parameter dan objek respons mewarisi dari `Anthropic::Internal::Type::BaseModel`, yang menyediakan beberapa kemudahan, termasuk:

1. Semua bidang, termasuk yang tidak diketahui, dapat diakses dengan sintaks `obj[:prop]`, dan dapat didestruktur dengan `obj => {prop: prop}` atau sintaks pattern-matching.

2. Kesetaraan struktural untuk kesetaraan; jika dua panggilan API mengembalikan nilai yang sama, membandingkan respons dengan == akan mengembalikan true.

3. Baik instance maupun kelas itu sendiri dapat dicetak dengan indah.

4. Pembantu seperti `#to_h`, `#deep_to_h`, `#to_json`, dan `#to_yaml`.

## Concurrency dan connection pooling

Instance `Anthropic::Client` adalah threadsafe, tetapi hanya fork-safe ketika tidak ada permintaan HTTP yang sedang berlangsung.

Setiap instance `Anthropic::Client` memiliki pool koneksi HTTP sendiri dengan ukuran default 99. Oleh karena itu, kami merekomendasikan untuk membuat instance klien sekali per aplikasi dalam sebagian besar pengaturan.

Ketika semua koneksi yang tersedia dari pool diperiksa, permintaan menunggu koneksi baru menjadi tersedia, dengan waktu antrian dihitung menuju timeout permintaan.

Kecuali ditentukan lain, kelas lain dalam SDK tidak memiliki kunci yang melindungi struktur data dasarnya.

## Membuat permintaan khusus atau tidak terdokumentasi

### Properti tidak terdokumentasi

Anda dapat mengirim parameter tidak terdokumentasi ke titik akhir apa pun, dan membaca properti respons tidak terdokumentasi, seperti ini:

<Warning>
Parameter `extra_` dengan nama yang sama mengganti parameter yang terdokumentasi. Untuk alasan keamanan, pastikan metode ini hanya digunakan dengan data input yang terpercaya.
</Warning>

```ruby
message =
  anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-4-6",
    request_options: {
      extra_query: {my_query_parameter: value},
      extra_body: {my_body_parameter: value},
      extra_headers: {"my-header": value}
    }
  )

puts(message[:my_undocumented_property])
```

### Parameter permintaan tidak terdokumentasi

Jika Anda ingin secara eksplisit mengirim param tambahan, Anda dapat melakukannya dengan `extra_query`, `extra_body`, dan `extra_headers` di bawah parameter `request_options:` saat membuat permintaan, seperti yang terlihat dalam contoh di atas.

### Titik akhir tidak terdokumentasi

Untuk membuat permintaan ke titik akhir tidak terdokumentasi sambil mempertahankan manfaat auth, percobaan ulang, dan sebagainya, Anda dapat membuat permintaan menggunakan `client.request`, seperti ini:

```ruby
response = client.request(
  method: :post,
  path: '/undocumented/endpoint',
  query: {"dog": "woof"},
  headers: {"useful-header": "interesting-value"},
  body: {"hello": "world"}
)
```

## Integrasi platform

<Note>
Untuk panduan setup platform terperinci, lihat:
- [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock)
- [Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)
</Note>

### Amazon Bedrock

Perpustakaan ini juga menyediakan dukungan untuk [Anthropic Bedrock API](https://aws.amazon.com/bedrock/claude/) jika Anda menginstal perpustakaan ini dengan gem `aws-sdk-bedrockruntime`.

Anda kemudian dapat membuat instance kelas `Anthropic::BedrockClient` terpisah, dan menggunakan panduan standar AWS untuk mengonfigurasi kredensial. Ini memiliki API yang sama dengan kelas `Anthropic::Client` dasar.

Perhatikan bahwa ID model yang diperlukan berbeda untuk model Bedrock, dan, tergantung pada model yang ingin Anda gunakan, Anda perlu menggunakan ID model AWS untuk model Anthropic -- yang dapat ditemukan di [katalog model Bedrock AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) -- atau ID profil inferensi (misalnya `us.anthropic.claude-3-5-haiku-20241022-v1:0` untuk Claude 3.5 Haiku).

```ruby
require "anthropic"

anthropic = Anthropic::BedrockClient.new

message = anthropic.messages.create(
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "Hello, Claude"
    }
  ],
  model: "anthropic.claude-opus-4-6-v1"
)

puts(message)
```

### Google Vertex AI

Perpustakaan ini juga menyediakan dukungan untuk [Anthropic Vertex API](https://cloud.google.com/vertex-ai?hl=en) jika Anda menginstal perpustakaan ini dengan gem `googleauth`.

Anda kemudian dapat mengimpor dan membuat instance kelas `Anthropic::VertexClient` terpisah, dan menggunakan panduan Google untuk mengonfigurasi [Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc). Ini memiliki API yang sama dengan kelas `Anthropic::Client` dasar.

```ruby
require "anthropic"

anthropic = Anthropic::VertexClient.new(region: "us-east5", project_id: "my-project-id")

message = anthropic.messages.create(
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "Hello, Claude"
    }
  ],
  model: "claude-opus-4-6"
)

puts(message)
```

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-ruby)
- [Dokumentasi RubyDoc](https://gemdocs.org/gems/anthropic)
- [Referensi API](/docs/id/api/overview)
- [Panduan streaming](/docs/id/build-with-claude/streaming)