---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: b25ce2360bdcd581ac2d797bb2b9996cccc67fe8965611dfb64d64c0dd84c975
---

---
title: Python SDK
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python
description: Instal dan konfigurasikan Anthropic Python SDK dengan dukungan klien sinkron dan asinkron
---

Anthropic Python SDK menyediakan akses yang mudah ke Claude API dari aplikasi Python. SDK ini mendukung operasi sinkron dan asinkron, streaming, serta integrasi dengan Amazon Bedrock, Claude Platform di AWS, Google Cloud, dan Microsoft Foundry.

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](https://platform.claude.com/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK khusus Python.
</Info>

## Instalasi

```bash
pip install anthropic
```

Untuk integrasi khusus platform atau performa asinkron yang lebih baik, instal dengan extras:

```bash
# Untuk dukungan Amazon Bedrock
pip install "anthropic[bedrock]"

# Untuk dukungan Google Cloud
pip install "anthropic[vertex]"

# Untuk dukungan Claude Platform di AWS
pip install "anthropic[aws]"

# Dukungan Microsoft Foundry sudah termasuk dalam paket dasar

# Untuk performa async yang lebih baik dengan aiohttp
pip install "anthropic[aiohttp]"
```

## Persyaratan

Diperlukan Python 3.10 atau yang lebih baru. Jika Anda melakukan upgrade dari rilis 0.x SDK, lihat [panduan migrasi v1](https://github.com/anthropics/anthropic-sdk-python/blob/main/MIGRATION.md) untuk daftar perubahan yang tidak kompatibel (breaking changes).

## Penggunaan

```python
import os
from anthropic import Anthropic

client = Anthropic(
    # Ini adalah nilai default dan dapat dihilangkan
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-5",
)

for block in message.content:
    if block.type == "text":
        print(block.text)
```

<Tip>
  Pertimbangkan untuk menggunakan [python-dotenv](https://pypi.org/project/python-dotenv/) untuk menambahkan `ANTHROPIC_API_KEY="my-anthropic-api-key"` ke file `.env` Anda sehingga "API key" (kunci API) Anda tidak tersimpan di source control.
</Tip>

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication).

## Penggunaan asinkron

```python
import os
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


async def main() -> None:
    message = await client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-opus-5",
    )
    print(message.content)


asyncio.run(main())
```

### Menggunakan aiohttp untuk konkurensi yang lebih baik

Untuk performa asinkron yang lebih baik, Anda dapat menggunakan backend HTTP `aiohttp` sebagai pengganti `httpx2` default:

```python
import os
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient


async def main() -> None:
    async with AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        http_client=DefaultAioHttpClient(),
    ) as client:
        message = await client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, Claude",
                }
            ],
            model="claude-opus-5",
        )
        print(message.content)


asyncio.run(main())
```

## Respons streaming

SDK menyediakan dukungan untuk respons streaming menggunakan Server-Sent Events (SSE).

```python
client = Anthropic()

stream = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-5",
    stream=True,
)
for event in stream:
    print(event.type)
```

Klien asinkron menggunakan antarmuka yang persis sama:

```python
client = AsyncAnthropic()

stream = await client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-5",
    stream=True,
)
async for event in stream:
    print(event.type)
```

### Helper streaming

SDK juga menyediakan helper streaming yang menggunakan context manager dan memberikan akses ke teks yang terakumulasi serta pesan akhir:

```python
async def main() -> None:
    async with client.messages.stream(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="claude-opus-5",
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
        print()

        message = await stream.get_final_message()
        print(message.to_json())


asyncio.run(main())
```

Streaming dengan `client.messages.stream(...)` mengekspos berbagai helper termasuk akumulasi dan event khusus SDK.

Sebagai alternatif, Anda dapat menggunakan `client.messages.create(..., stream=True)` yang hanya mengembalikan iterable dari event dalam stream dan menggunakan lebih sedikit memori (tidak membangun objek pesan akhir untuk Anda).

## Penghitungan token

Anda dapat melihat penggunaan yang tepat untuk permintaan tertentu melalui properti respons `usage`:

```python
message = client.messages.create(...)
print(message.usage)
# Usage(input_tokens=25, output_tokens=13)
```

Anda juga dapat menghitung token sebelum membuat permintaan:

```python
count = client.messages.count_tokens(
    model="claude-opus-5", messages=[{"role": "user", "content": "Hello, world"}]
)
print(count.input_tokens)  # 10
```

## Penggunaan alat

SDK ini menyediakan dukungan untuk "tool use" (penggunaan alat), yang juga dikenal sebagai function calling. Untuk detail lebih lanjut, lihat [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

### Helper alat

SDK menyediakan helper untuk mendefinisikan dan menjalankan alat sebagai fungsi Python murni. Decorator `@beta_tool` menghasilkan skema alat dari signature fungsi dan docstring:

```python
import json
from anthropic import Anthropic, beta_tool

client = Anthropic()


@beta_tool
def get_weather(location: str) -> str:
    """Get the weather for a given location.

    Args:
        location: The city and state, for example, San Francisco, CA
    Returns:
        A JSON-encoded string with the location, temperature, and weather condition.
    """
    return json.dumps(
        {
            "location": location,
            "temperature": "68°F",
            "condition": "Sunny",
        }
    )


# Gunakan tool_runner untuk menangani panggilan alat secara otomatis
runner = client.beta.messages.tool_runner(
    max_tokens=1024,
    model="claude-opus-5",
    tools=[get_weather],
    messages=[
        {"role": "user", "content": "What is the weather in SF?"},
    ],
)
for message in runner:
    print(message)
```

Pada setiap iterasi, sebuah permintaan API dibuat. Jika respons menyertakan panggilan ke salah satu alat yang diberikan, alat tersebut dipanggil secara otomatis, dan hasilnya dikembalikan langsung ke model pada iterasi berikutnya.

## Batch pesan

SDK ini menyediakan dukungan untuk [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) di bawah `client.messages.batches`.

### Membuat batch

Message Batches menerima array permintaan, di mana setiap objek memiliki pengenal `custom_id` dan `params` permintaan yang sama dengan Messages API standar:

```python
client.messages.batches.create(
    requests=[
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-opus-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello, world"}],
            },
        },
        {
            "custom_id": "my-second-request",
            "params": {
                "model": "claude-opus-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hi again, friend"}],
            },
        },
    ]
)
```

### Mendapatkan hasil dari batch

Setelah Message Batch selesai diproses, yang ditandai dengan `.processing_status == 'ended'`, Anda dapat mengakses hasilnya dengan `.batches.results()`:

```python
client = anthropic.Anthropic()
batch_id = "batch_abc123"
result_stream = client.messages.batches.results(batch_id)
for entry in result_stream:
    if entry.result.type == "succeeded":
        print(entry.result.message.content)
```

## Unggahan file

Parameter permintaan yang berkaitan dengan unggahan file dapat diberikan dalam berbagai bentuk:

* Objek `PathLike` (misalnya, `pathlib.Path`)
* Tuple `(filename, content, content_type)`
* Objek file-like `BinaryIO`

```python
from pathlib import Path
from anthropic import Anthropic

client = Anthropic()

# Unggah menggunakan jalur file
client.files.upload(
    file=Path("/path/to/file"),
)

# Unggah menggunakan bytes
client.files.upload(
    file=("file.txt", b"my bytes", "text/plain"),
)
```

Klien asinkron menggunakan antarmuka yang persis sama. Jika Anda memberikan instance `PathLike`, isi file akan dibaca secara asinkron secara otomatis.

## Menangani error

Ketika library tidak dapat terhubung ke API, atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx), subclass dari `APIError` akan dimunculkan:

```python
import anthropic
# ...
try:
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-opus-5",
    )
except anthropic.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx2
except anthropic.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except anthropic.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Kode error adalah sebagai berikut:

| Kode status | Tipe error                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 409         | `ConflictError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

## ID permintaan

> Untuk informasi lebih lanjut tentang debugging permintaan, lihat [ID Permintaan](https://platform.claude.com/docs/id/api/errors#request-id).

Semua respons objek dalam SDK menyediakan properti `_request_id` yang ditambahkan dari header respons `request-id` sehingga Anda dapat dengan cepat mencatat permintaan yang gagal dan melaporkannya kembali ke Anthropic.

```python
message = client.messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
)
print(message._request_id)  # e.g., req_018EeWyXxfu5pfWkrYcMdjWG
```

<Note>
  Tidak seperti properti lain yang menggunakan prefiks `_`, properti `_request_id` bersifat publik. Kecuali didokumentasikan sebaliknya, semua properti, metode, dan modul lain dengan prefiks `_` bersifat privat.
</Note>

## Percobaan ulang

Error tertentu secara otomatis dicoba ulang 2 kali secara default, dengan exponential backoff singkat. Error koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, dan error Internal >=500 semuanya dicoba ulang secara default.

Anda dapat menggunakan opsi `max_retries` untuk mengonfigurasi atau menonaktifkan ini:

```python
# Konfigurasikan default untuk semua permintaan:
client = Anthropic(
    max_retries=0,  # default is 2
)

# Atau, konfigurasikan per permintaan:
client.with_options(max_retries=5).messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
)
```

## Timeout

Secara default, permintaan akan timeout setelah 10 menit. Anda dapat mengonfigurasi ini dengan opsi `timeout`, yang menerima float atau objek `httpx2.Timeout`:

```python
import httpx2
from anthropic import Anthropic

# Konfigurasikan nilai default untuk semua permintaan:
client = Anthropic(
    timeout=20.0,  # 20 seconds (default is 10 minutes)
)

# Kontrol yang lebih terperinci:
client = Anthropic(
    timeout=httpx2.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Timpa per permintaan:
client.with_options(timeout=5.0).messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
)
```

Saat timeout, SDK memunculkan `APITimeoutError`.

Perhatikan bahwa permintaan yang timeout akan [dicoba ulang dua kali secara default](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python#retries).

## Permintaan panjang

<Warning>
  Pertimbangkan untuk menggunakan [Messages API](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python#streaming-responses) streaming untuk permintaan yang berjalan lebih lama.
</Warning>

Hindari menetapkan nilai `max_tokens` yang besar tanpa menggunakan streaming. Beberapa jaringan mungkin memutus koneksi idle setelah jangka waktu tertentu, yang dapat menyebabkan permintaan gagal atau [timeout](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python#timeouts) tanpa menerima respons dari Anthropic.

SDK akan memunculkan `ValueError` jika permintaan non-streaming diperkirakan memakan waktu lebih dari sekitar 10 menit. Memberikan `stream=True` atau menimpa opsi `timeout` di tingkat klien atau permintaan akan menonaktifkan error ini.

"Latency" (latensi) permintaan yang diperkirakan lebih lama dari [timeout](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python#timeouts) untuk permintaan non-streaming akan mengakibatkan klien memutus koneksi dan mencoba ulang tanpa menerima respons.

SDK menetapkan opsi [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/overview.html) untuk mengurangi dampak timeout koneksi idle pada beberapa jaringan. Ini dapat ditimpa dengan memberikan opsi `http_client` kustom ke klien.

## Paginasi otomatis

Metode list di Claude API dipaginasi. Anda dapat menggunakan sintaks `for` untuk mengiterasi item di seluruh halaman:

```python
client = Anthropic()

all_batches = []
# Secara otomatis mengambil halaman lainnya sesuai kebutuhan.
for batch in client.messages.batches.list(limit=20):
    all_batches.append(batch)
print(all_batches)
```

Untuk iterasi asinkron:

```python
async def main() -> None:
    all_batches = []
    async for batch in client.messages.batches.list(limit=20):
        all_batches.append(batch)
    print(all_batches)


asyncio.run(main())
```

Sebagai alternatif, Anda dapat menggunakan metode `.has_next_page()`, `.next_page_info()`, atau `.get_next_page()` untuk kontrol yang lebih granular saat bekerja dengan halaman:

```python
first_page = await client.messages.batches.list(limit=20)

if first_page.has_next_page():
    print(f"will fetch next page using these details: {first_page.next_page_info()}")
    next_page = await first_page.get_next_page()
    print(f"number of items we just fetched: {len(next_page.data)}")

# Hapus `await` untuk penggunaan non-async.
```

Atau bekerja langsung dengan data yang dikembalikan:

```python
first_page = await client.messages.batches.list(limit=20)

print(f"next page cursor: {first_page.last_id}")
for batch in first_page.data:
    print(batch.id)

# Hapus `await` untuk penggunaan non-async.
```

## Header default

SDK secara otomatis mengirim header `anthropic-version` yang diatur ke `2023-06-01`.

Jika diperlukan, Anda dapat menimpanya dengan menetapkan header default pada objek klien atau per permintaan.

<Warning>
  Menimpa header default dapat mengakibatkan tipe yang salah dan perilaku lain yang tidak terduga atau tidak terdefinisi dalam SDK.
</Warning>

```python
# Tetapkan header default untuk semua permintaan pada klien
client = Anthropic(
    default_headers={"anthropic-version": "My-Custom-Value"},
)

# Atau timpa per permintaan
client.messages.with_raw_response.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
    extra_headers={"anthropic-version": "My-Custom-Value"},
)
```

## Sistem tipe

### Parameter permintaan

Parameter permintaan bersarang adalah [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict). Respons adalah [model Pydantic](https://docs.pydantic.dev) yang juga memiliki metode helper untuk hal-hal seperti serialisasi kembali ke JSON ([`v1`](https://docs.pydantic.dev/1.10/usage/models/), [`v2`](https://docs.pydantic.dev/latest/concepts/serialization/)).

Permintaan dan respons bertipe menyediakan autocomplete dan dokumentasi di dalam editor Anda. Jika Anda ingin melihat error tipe di VS Code untuk membantu menangkap bug lebih awal, atur `python.analysis.typeCheckingMode` ke `basic`.

### Model respons

Untuk mengonversi model Pydantic menjadi dictionary, gunakan metode helper:

```python
message = client.messages.create(...)

# Konversi ke string JSON
json_str = message.to_json()

# Konversi ke dictionary
data = message.to_dict()
```

### Menangani field null vs field yang hilang

Dalam respons, Anda dapat membedakan antara field yang secara eksplisit `null` dengan field yang tidak dikembalikan (hilang):

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
if response.my_field is None:
    if "my_field" not in response.model_fields_set:
        print("field was not in the response")
    else:
        print("field was null")
```

## Penggunaan lanjutan

### Mengakses data respons mentah (misalnya, header)

`Response` "mentah" yang dikembalikan oleh `httpx2` dapat diakses melalui properti `.with_raw_response` pada klien. Ini berguna untuk mengakses header respons atau metadata lainnya:

```python
client = Anthropic()

response = client.messages.with_raw_response.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
)

print(response.headers.get("request-id"))
message = (
    response.parse()
)  # get the object that `messages.create()` would have returned
print(message.content)
```

Metode-metode ini mengembalikan objek `APIResponse`. Pada klien asinkron, metode ini mengembalikan `AsyncAPIResponse`, dan `.parse()`, `.read()`, `.text()`, serta `.json()` harus di-await.

### Streaming body respons

Pendekatan `.with_raw_response` langsung membaca seluruh body respons saat Anda membuat permintaan. Untuk melakukan streaming body respons, gunakan `.with_streaming_response`, yang memerlukan context manager dan hanya membaca body respons setelah Anda memanggil `.read()`, `.text()`, `.json()`, `.iter_bytes()`, `.iter_text()`, `.iter_lines()`, atau `.parse()`. Pada klien asinkron, ini adalah metode asinkron.

```python
with client.messages.with_streaming_response.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
) as response:
    print(response.headers.get("request-id"))

    for line in response.iter_lines():
        print(line)
```

Context manager diperlukan agar respons dapat ditutup dengan andal.

### Logging

SDK menggunakan modul `logging` dari standard library.

Anda dapat mengaktifkan logging dengan mengatur variabel lingkungan `ANTHROPIC_LOG` ke `debug` atau `info`:

```bash
export ANTHROPIC_LOG=debug
```

### Membuat permintaan kustom/tidak terdokumentasi

Library ini bertipe untuk akses yang mudah ke API yang terdokumentasi. Jika Anda perlu mengakses endpoint, parameter, atau properti respons yang tidak terdokumentasi, library ini tetap dapat digunakan.

#### Endpoint tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi, Anda dapat menggunakan `client.get`, `client.post`, dan verb HTTP lainnya. Opsi pada klien, seperti percobaan ulang, tetap dihormati saat membuat permintaan ini.

```python
import httpx2

response = client.post(
    "/foo",
    cast_to=httpx2.Response,
    body={"my_param": True},
)

print(response.json())
```

#### Parameter permintaan tidak terdokumentasi

Jika Anda ingin secara eksplisit mengirim parameter tambahan, Anda dapat melakukannya dengan opsi permintaan `extra_query`, `extra_body`, dan `extra_headers`.

<Warning>
  Parameter `extra_` menimpa parameter terdokumentasi dengan nama yang sama. Untuk alasan keamanan, pastikan metode ini hanya digunakan dengan data input yang tepercaya.
</Warning>

#### Properti respons tidak terdokumentasi

Untuk mengakses properti respons yang tidak terdokumentasi, Anda dapat mengakses field tambahan seperti `response.unknown_prop`. Anda juga dapat memperoleh semua field tambahan pada model Pydantic sebagai dict dengan `response.model_extra`.

### Mengonfigurasi klien HTTP

SDK mengirim permintaan dengan [httpx2](https://httpx2.pydantic.dev), sebuah fork dari `httpx` yang kompatibel secara API. Untuk menyesuaikan klien HTTP, termasuk proxy dan transport, berikan [klien httpx2](https://httpx2.pydantic.dev/api/#client) Anda sendiri sebagai `http_client`:

```python
import httpx2
from anthropic import Anthropic, DefaultHttpxClient

client = Anthropic(
    # Atau gunakan variabel lingkungan `ANTHROPIC_BASE_URL`
    base_url="http://my.test.server.example.com:8083",
    http_client=DefaultHttpxClient(
        proxy="http://my.test.proxy.example.com",
        transport=httpx2.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

Anda juga dapat menyesuaikan klien per permintaan dengan menggunakan `with_options()`:

```python
client.with_options(http_client=DefaultHttpxClient(...))
```

<Note>
  Gunakan `DefaultHttpxClient` dan `DefaultAsyncHttpxClient` sebagai pengganti `httpx2.Client` dan `httpx2.AsyncClient` mentah untuk memastikan konfigurasi default SDK (seperti timeout dan batas koneksi) tetap dipertahankan. Argumen `http_client` harus berupa klien `httpx2`. Memberikan klien dari paket `httpx` yang terpisah akan memunculkan `TypeError`.
</Note>

Alat tracing dan mocking yang mem-patch `httpx` itu sendiri, seperti `HTTPXClientInstrumentor` dari OpenTelemetry, integrasi `httpx` dari Sentry, `respx`, atau `pytest-httpx`, tidak melihat permintaan SDK secara default. Untuk menggunakannya, panggil `httpx2.alias_httpx()` sekali saat startup, sebelum apa pun mengimpor `httpx`. Ini membuat `import httpx` diresolusikan ke `httpx2` untuk seluruh proses.

### Mengelola sumber daya HTTP

Secara default, library menutup koneksi HTTP yang mendasarinya setiap kali klien di-[garbage collect](https://docs.python.org/3/reference/datamodel.html#object.__del__). Anda dapat menutup klien secara manual menggunakan metode `.close()` jika diinginkan, atau dengan context manager yang menutup saat keluar.

```python
with Anthropic() as client:
    message = client.messages.create(...)

# Klien HTTP ditutup secara otomatis
```

## Fitur beta

Fitur beta tersedia sebelum rilis umum untuk mendapatkan umpan balik awal dan menguji fungsionalitas baru. Anda dapat memeriksa ketersediaan semua kemampuan dan alat Claude di [ikhtisar membangun dengan Claude](https://platform.claude.com/docs/id/build-with-claude/overview).

Anda dapat mengakses sebagian besar fitur API beta melalui properti `beta` pada klien. Untuk mengaktifkan fitur beta tertentu, Anda perlu menambahkan [header beta](https://platform.claude.com/docs/id/api/beta-headers) yang sesuai ke field `betas` saat membuat pesan.

Misalnya, untuk mengaktifkan [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing):

```python
client = Anthropic()

response = client.beta.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    betas=["context-management-2025-06-27"],
)
```

## Integrasi platform

<Note>
  Untuk panduan penyiapan platform yang terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)
  * [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

Kelima kelas klien disertakan dalam paket dasar `anthropic`:

| Penyedia                          | Klien                                          | Dependensi tambahan                |
| --------------------------------- | ---------------------------------------------- | ---------------------------------- |
| Agent Platform                    | `from anthropic import AnthropicVertex`        | `pip install "anthropic[vertex]"`  |
| Bedrock                           | `from anthropic import AnthropicBedrockMantle` | `pip install "anthropic[bedrock]"` |
| Bedrock (jalur `bedrock-runtime`) | `from anthropic import AnthropicBedrock`       | `pip install "anthropic[bedrock]"` |
| Claude Platform di AWS            | `from anthropic import AnthropicAWS`           | `pip install "anthropic[aws]"`     |
| Foundry                           | `from anthropic import AnthropicFoundry`       | Tidak ada                          |

Klien `AnthropicAWS` masih dalam versi beta. Berikan `workspace_id` ke konstruktor atau atur variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID`.

Gunakan `AnthropicBedrockMantle` untuk proyek baru; `AnthropicBedrock` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan API `InvokeModel` Bedrock.

## Semantic versioning

Paket ini secara umum mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan tertentu yang tidak kompatibel ke belakang mungkin dirilis sebagai versi minor:

1. Perubahan yang hanya memengaruhi tipe statis, tanpa merusak perilaku runtime.
2. Perubahan pada internal library yang secara teknis publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
3. Perubahan yang dalam praktiknya tidak diperkirakan berdampak pada sebagian besar pengguna.

### Menentukan versi yang terinstal

Jika Anda telah melakukan upgrade ke versi terbaru tetapi tidak melihat fitur baru yang Anda harapkan, lingkungan Python Anda kemungkinan masih menggunakan versi yang lebih lama. Anda dapat menentukan versi yang digunakan saat runtime dengan:

```python
print(anthropic.__version__)
```

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-python)
* [Referensi API](https://platform.claude.com/docs/id/api/overview)
* [Streaming Pesan](https://platform.claude.com/docs/id/build-with-claude/streaming)
* [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview)
