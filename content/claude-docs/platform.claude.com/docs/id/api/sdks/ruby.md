---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/ruby
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 9e59145c3e65933fd8a4a01da6f086afdab802224663cf011165eea5b65caa4f
---

# Ruby SDK

Instal dan konfigurasi Anthropic Ruby SDK dengan tipe Sorbet, pembantu streaming, dan connection pooling

---

Perpustakaan Ruby Anthropic menyediakan akses yang mudah ke Anthropic REST API dari aplikasi Ruby 3.2.0+ apa pun. Dilengkapi dengan tipe komprehensif dan docstring di Yard, RBS, dan RBI. Perpustakaan standar `net/http` digunakan sebagai transport HTTP, dengan connection pooling melalui gem `connection_pool`.

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus Ruby dan konfigurasi.
</Info>

## Instalasi

Tambahkan gem ke `Gemfile` aplikasi Anda dengan Bundler:

```bash
bundle add anthropic
```

## Persyaratan

Ruby 3.2.0 atau lebih tinggi.

## Penggunaan

```ruby hidelines={1..2}
require "anthropic"

anthropic = Anthropic::Client.new(
  api_key: ENV["ANTHROPIC_API_KEY"] # Ini adalah default dan dapat dihilangkan
)

message = anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-7"
)

puts(message.content)
```

## Streaming

SDK menyediakan dukungan untuk respons streaming menggunakan Server-Sent Events (SSE).

```ruby hidelines={1}
require "anthropic"
anthropic = Anthropic::Client.new
stream = anthropic.messages.stream(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-7"
)

stream.each do |message|
  puts(message.type)
end
```

### Pembantu streaming

Perpustakaan ini menyediakan beberapa kemudahan untuk streaming pesan, misalnya:

```ruby hidelines={1}
require "anthropic"
anthropic = Anthropic::Client.new
stream = anthropic.messages.stream(
  max_tokens: 1024,
  messages: [{role: :user, content: "Say hello there!"}],
  model: :"claude-opus-4-7"
)

stream.text.each do |text|
  print(text)
end
```

Streaming dengan `anthropic.messages.stream(...)` mengekspos berbagai pembantu termasuk akumulasi dan acara khusus SDK.

## Skema input dan pemanggilan alat

SDK menyediakan mekanisme pembantu untuk mendefinisikan kelas data terstruktur untuk alat dan membiarkan Claude secara otomatis menjalankannya. Untuk dokumentasi terperinci tentang pola penggunaan alat termasuk tool runner, lihat [Tool Runner (SDK)](/docs/id/agents-and-tools/tool-use/tool-runner).

```ruby hidelines={1}
require "anthropic"
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
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [{role: "user", content: "What's 15 * 7?"}],
  tools: [Calculator.new]
).each_message { puts _1.content }
```

## Output terstruktur

Untuk dokumentasi output terstruktur lengkap termasuk contoh Ruby, lihat [Structured Outputs](/docs/id/build-with-claude/structured-outputs).

## Menangani kesalahan

Ketika perpustakaan tidak dapat terhubung ke API, atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx), subkelas `Anthropic::Errors::APIError` akan dilempar:

```ruby hidelines={1}
require "anthropic"
anthropic = Anthropic::Client.new
begin
  message = anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-4-7"
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

| Penyebab          | Jenis Kesalahan         |
| ----------------- | ----------------------- |
| HTTP 400          | `BadRequestError`       |
| HTTP 401          | `AuthenticationError`   |
| HTTP 403          | `PermissionDeniedError` |
| HTTP 404          | `NotFoundError`         |
| HTTP 409          | `ConflictError`         |
| HTTP 422          | `UnprocessableEntityError` |
| HTTP 429          | `RateLimitError`        |
| HTTP >= 500       | `InternalServerError`   |
| Kesalahan HTTP lainnya | `APIStatusError`   |
| Timeout           | `APITimeoutError`       |
| Kesalahan jaringan | `APIConnectionError`    |

## Percobaan ulang

Kesalahan tertentu akan secara otomatis dicoba ulang 2 kali secara default, dengan backoff eksponensial pendek.

Kesalahan koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, >=500 Internal errors, dan timeout semuanya akan dicoba ulang secara default.

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
  model: :"claude-opus-4-7",
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
  model: :"claude-opus-4-7",
  request_options: {timeout: 5}
)
```

Pada timeout, `Anthropic::Errors::APITimeoutError` dilempar.

Perhatikan bahwa permintaan yang timeout dicoba ulang secara default.

## Paginasi

Metode daftar dalam Claude API dipaginasi.

Perpustakaan ini menyediakan iterator auto-paging dengan setiap respons daftar, sehingga Anda tidak perlu meminta halaman berturut-turut secara manual:

```ruby hidelines={1}
require "anthropic"
anthropic = Anthropic::Client.new
page = anthropic.messages.batches.list(limit: 20)

# Ambil item tunggal dari halaman.
batch = page.data[0]
puts(batch.id)

# Secara otomatis mengambil lebih banyak halaman sesuai kebutuhan.
page.auto_paging_each do |batch|
  puts(batch.id)
end
```

Alternatifnya, Anda dapat menggunakan metode `#next_page?` dan `#next_page` untuk kontrol yang lebih granular saat bekerja dengan halaman.

```ruby hidelines={1}
require "anthropic"
anthropic = Anthropic::Client.new
page = anthropic.messages.batches.list(limit: 20)
while page.next_page?
  page = page.next_page
  page.data&.each { |batch| puts(batch.id) }
end
```

## Unggahan file

Parameter permintaan yang sesuai dengan unggahan file dapat diteruskan sebagai konten mentah, instance [`Pathname`](https://rubyapi.org/3.2/o/pathname), [`StringIO`](https://rubyapi.org/3.2/o/stringio), atau lebih.

```ruby hidelines={1} nocheck
require "anthropic"
anthropic = Anthropic::Client.new
require "pathname"

# Gunakan `Pathname` untuk mengirim nama file dan/atau menghindari paging file besar ke memori:
file_metadata = anthropic.beta.files.upload(file: Pathname("/path/to/file"))

# Alternatifnya, teruskan konten file atau `StringIO` secara langsung:
file_metadata = anthropic.beta.files.upload(file: File.read("/path/to/file"))

# Atau, untuk mengontrol nama file dan/atau jenis konten:
file = Anthropic::FilePart.new(File.read("/path/to/file"), filename: "/path/to/file", content_type: "...")
file_metadata = anthropic.beta.files.upload(file: file)

puts(file_metadata.id)
```

Perhatikan bahwa Anda juga dapat meneruskan deskriptor `IO` mentah, tetapi ini menonaktifkan percobaan ulang, karena perpustakaan tidak dapat memastikan apakah deskriptor adalah file atau pipe (yang tidak dapat diputar ulang).

## Sorbet

Perpustakaan ini menyediakan definisi [RBI](https://sorbet.org/docs/rbi) komprehensif, dan tidak memiliki ketergantungan pada sorbet-runtime.

Anda dapat menyediakan parameter permintaan yang aman tipe seperti ini:

```ruby hidelines={1}
require "anthropic"
anthropic = Anthropic::Client.new
anthropic.messages.create(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-4-7"
)
```

Atau, secara setara:

```ruby hidelines={1}
require "anthropic"
anthropic = Anthropic::Client.new
# Hash berfungsi, tetapi tidak aman tipe:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-4-7"
)

# Anda juga dapat splat kelas Params lengkap:
params = Anthropic::MessageCreateParams.new(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-4-7"
)
anthropic.messages.create(**params)
```

### Enum

Karena perpustakaan ini tidak bergantung pada `sorbet-runtime`, ia tidak dapat menyediakan instance [`T::Enum`](https://sorbet.org/docs/tenum). Sebagai gantinya, SDK menyediakan "tagged symbols", yang selalu primitif pada runtime:

```ruby nocheck
# :auto
puts(Anthropic::MessageCreateParams::ServiceTier::AUTO)

# Revealed type: `T.all(Anthropic::MessageCreateParams::ServiceTier, Symbol)`
T.reveal_type(Anthropic::MessageCreateParams::ServiceTier::AUTO)
```

Parameter enum memiliki tipe "relaxed", sehingga Anda dapat meneruskan konstanta enum atau nilai literalnya:

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

1. Semua bidang, termasuk yang tidak dikenal, dapat diakses dengan sintaks `obj[:prop]`, dan dapat didestruktur dengan `obj => {prop: prop}` atau sintaks pattern-matching.

2. Kesetaraan struktural untuk persamaan; jika dua panggilan API mengembalikan nilai yang sama, membandingkan respons dengan == akan mengembalikan true.

3. Baik instance maupun kelas itu sendiri dapat dicetak dengan indah.

4. Pembantu seperti `#to_h`, `#deep_to_h`, `#to_json`, dan `#to_yaml`.

## Concurrency dan connection pooling

Instance `Anthropic::Client` adalah threadsafe, tetapi hanya fork-safe ketika tidak ada permintaan HTTP yang sedang berlangsung.

Setiap instance `Anthropic::Client` memiliki pool koneksi HTTP sendiri dengan ukuran default 99. Dengan demikian, rekomendasi adalah untuk membuat instance klien sekali per aplikasi dalam sebagian besar pengaturan.

Ketika semua koneksi yang tersedia dari pool diperiksa, permintaan menunggu koneksi baru menjadi tersedia, dengan waktu antrian dihitung menuju timeout permintaan.

Kecuali ditentukan lain, kelas lain dalam SDK tidak memiliki kunci yang melindungi struktur data dasarnya.

## Membuat permintaan kustom atau tidak terdokumentasi

### Properti tidak terdokumentasi

Anda dapat mengirim parameter tidak terdokumentasi ke titik akhir mana pun, dan membaca properti respons tidak terdokumentasi, seperti ini:

<Warning>
Parameter `extra_` dengan nama yang sama menggantikan parameter yang terdokumentasi. Untuk alasan keamanan, pastikan metode ini hanya digunakan dengan data input yang terpercaya.
</Warning>

```ruby hidelines={1} nocheck
require "anthropic"
anthropic = Anthropic::Client.new
value = "example"
message =
  anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-4-7",
    request_options: {
      extra_query: {my_query_parameter: value},
      extra_body: {my_body_parameter: value},
      extra_headers: {"my-header": value}
    }
  )

puts(message[:my_undocumented_property])
```

### Parameter permintaan tidak terdokumentasi

Jika Anda ingin secara eksplisit mengirim parameter tambahan, Anda dapat melakukannya dengan `extra_query`, `extra_body`, dan `extra_headers` di bawah parameter `request_options:` saat membuat permintaan, seperti yang terlihat dalam contoh di atas.

### Titik akhir tidak terdokumentasi

Untuk membuat permintaan ke titik akhir tidak terdokumentasi sambil mempertahankan manfaat auth, percobaan ulang, dan sebagainya, Anda dapat membuat permintaan menggunakan `anthropic.request`, seperti ini:

```ruby nocheck
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
- [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock)
- [Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)
</Note>

Ruby SDK mendukung Bedrock dan Vertex AI melalui kelas klien khusus:

- **Bedrock:** `Anthropic::BedrockClient`. Memerlukan gem `aws-sdk-bedrockruntime`.
- **Vertex AI:** `Anthropic::VertexClient`. Memerlukan gem `googleauth`.

## Semantic versioning

Paket ini mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html). Karena perpustakaan dalam pengembangan awal dan memiliki versi utama `0`, API dapat berubah kapan saja.

Paket ini menganggap peningkatan pada definisi tipe (non-runtime) `*.rbi` dan `*.rbs` sebagai perubahan non-breaking.

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-ruby)
- [Dokumentasi RubyDoc](https://gemdocs.org/gems/anthropic)
- [Referensi API](/docs/id/api/overview)
- [Panduan streaming](/docs/id/build-with-claude/streaming)