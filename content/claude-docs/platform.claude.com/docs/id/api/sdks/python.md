---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/python
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: fcaffc009f71521e35288514c28b0ed8b9b3439d425f54bdc8379f94bf22a85c
---

# Python SDK

Instal dan konfigurasi Anthropic Python SDK dengan dukungan klien sinkron dan asinkron

---

Anthropic Python SDK menyediakan akses yang mudah ke Anthropic REST API dari aplikasi Python. SDK ini mendukung operasi sinkron dan asinkron, streaming, serta integrasi dengan AWS Bedrock dan Google Vertex AI.

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus Python dan konfigurasi.
</Info>

## Instalasi

```bash
pip install anthropic
```

Untuk integrasi khusus platform, instal dengan extras:

```bash
# Untuk dukungan AWS Bedrock
pip install anthropic[bedrock]

# Untuk dukungan Google Vertex AI
pip install anthropic[vertex]

# Untuk performa async yang lebih baik dengan aiohttp
pip install anthropic[aiohttp]
```

## Persyaratan

Python 3.9 atau lebih baru diperlukan.

## Penggunaan

```python
import os
from anthropic import Anthropic

client = Anthropic(
    # Ini adalah default dan dapat dihilangkan
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
    model="claude-opus-4-7",
)
print(message.content)
```

<Tip>
Pertimbangkan menggunakan [python-dotenv](https://pypi.org/project/python-dotenv/) untuk menambahkan `ANTHROPIC_API_KEY="my-anthropic-api-key"` ke file `.env` Anda sehingga kunci API Anda tidak disimpan dalam kontrol sumber.
</Tip>

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
        model="claude-opus-4-7",
    )
    print(message.content)


asyncio.run(main())
```

### Menggunakan aiohttp untuk konkurensi yang lebih baik

Untuk performa async yang lebih baik, Anda dapat menggunakan backend HTTP `aiohttp` sebagai pengganti `httpx` default:

```python nocheck
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
            model="claude-opus-4-7",
        )
        print(message.content)


asyncio.run(main())
```

## Respons streaming

SDK menyediakan dukungan untuk respons streaming menggunakan Server-Sent Events (SSE).

```python hidelines={1..2}
from anthropic import Anthropic

client = Anthropic()

stream = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-4-7",
    stream=True,
)
for event in stream:
    print(event.type)
```

Klien asinkron menggunakan antarmuka yang sama persis:

```python hidelines={1..2}
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

stream = await client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-4-7",
    stream=True,
)
async for event in stream:
    print(event.type)
```

### Pembantu streaming

SDK juga menyediakan pembantu streaming yang menggunakan context manager dan memberikan akses ke teks yang terakumulasi dan pesan akhir:

```python hidelines={1..6}
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()


async def main() -> None:
    async with client.messages.stream(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="claude-opus-4-7",
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
        print()

        message = await stream.get_final_message()
        print(message.to_json())


asyncio.run(main())
```

Streaming dengan `client.messages.stream(...)` mengekspos berbagai pembantu termasuk akumulasi dan event khusus SDK.

Alternatifnya, Anda dapat menggunakan `client.messages.create(..., stream=True)` yang hanya mengembalikan async iterable dari event dalam stream dan menggunakan lebih sedikit memori (tidak membangun objek pesan akhir untuk Anda).

## Penghitungan token

Anda dapat melihat penggunaan yang tepat untuk permintaan tertentu melalui properti respons `usage`:

```python nocheck
message = client.messages.create(...)
print(message.usage)
# Usage(input_tokens=25, output_tokens=13)
```

Anda juga dapat menghitung token sebelum membuat permintaan:

```python
count = client.messages.count_tokens(
    model="claude-opus-4-7", messages=[{"role": "user", "content": "Hello, world"}]
)
print(count.input_tokens)  # 10
```

## Penggunaan alat

SDK ini menyediakan dukungan untuk penggunaan alat, juga dikenal sebagai function calling. Detail lebih lanjut dapat ditemukan di [ikhtisar penggunaan alat](/docs/id/agents-and-tools/tool-use/overview).

### Pembantu alat

SDK menyediakan pembantu untuk mendefinisikan dan menjalankan alat sebagai fungsi Python murni. Anda dapat menggunakan dekorator `@beta_tool` untuk kontrol yang lebih besar:

```python
import json
from anthropic import Anthropic, beta_tool

client = Anthropic()


@beta_tool
def get_weather(location: str) -> str:
    """Get the weather for a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA
    Returns:
        A dictionary containing the location, temperature, and weather condition.
    """
    return json.dumps(
        {
            "location": location,
            "temperature": "68°F",
            "condition": "Sunny",
        }
    )


# Use the tool_runner to automatically handle tool calls
runner = client.beta.messages.tool_runner(
    max_tokens=1024,
    model="claude-opus-4-7",
    tools=[get_weather],
    messages=[
        {"role": "user", "content": "What is the weather in SF?"},
    ],
)
for message in runner:
    print(message)
```

Pada setiap iterasi, permintaan API dibuat. Jika Claude ingin memanggil salah satu alat yang diberikan, alat tersebut secara otomatis dipanggil, dan hasilnya dikembalikan langsung ke model dalam iterasi berikutnya.

## Batch pesan

SDK ini menyediakan dukungan untuk [Message Batches API](/docs/id/build-with-claude/batch-processing) di bawah `client.messages.batches`.

### Membuat batch

Message Batches mengambil array permintaan, di mana setiap objek memiliki pengidentifikasi `custom_id` dan `params` permintaan yang sama seperti Messages API standar:

```python
client.messages.batches.create(
    requests=[
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-opus-4-7",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello, world"}],
            },
        },
        {
            "custom_id": "my-second-request",
            "params": {
                "model": "claude-opus-4-7",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hi again, friend"}],
            },
        },
    ]
)
```

### Mendapatkan hasil dari batch

Setelah Message Batch diproses, ditunjukkan oleh `.processing_status == 'ended'`, Anda dapat mengakses hasil dengan `.batches.results()`:

```python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
batch_id = "batch_abc123"
result_stream = client.messages.batches.results(batch_id)
for entry in result_stream:
    if entry.result.type == "succeeded":
        print(entry.result.message.content)
```

## Unggahan file

Parameter permintaan yang sesuai dengan unggahan file dapat diteruskan dalam berbagai bentuk:

- Objek `PathLike` (misalnya, `pathlib.Path`)
- Tuple dari `(filename, content, content_type)`
- Objek file-like `BinaryIO`
- Nilai pengembalian dari pembantu `toFile`

```python nocheck
from pathlib import Path
from anthropic import Anthropic

client = Anthropic()

# Upload using a file path
client.beta.files.upload(
    file=Path("/path/to/file"),
    betas=["files-api-2025-04-14"],
)

# Upload using bytes
client.beta.files.upload(
    file=("file.txt", b"my bytes", "text/plain"),
    betas=["files-api-2025-04-14"],
)
```

Klien asinkron menggunakan antarmuka yang sama persis. Jika Anda melewatkan instans `PathLike`, konten file dibaca secara asinkron secara otomatis.

## Menangani kesalahan

Ketika perpustakaan tidak dapat terhubung ke API, atau jika API mengembalikan kode status non-sukses (yaitu, respons 4xx atau 5xx), subkelas `APIError` akan dimunculkan:

```python hidelines={2..5}
import anthropic
from anthropic import Anthropic

client = Anthropic()

try:
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-opus-4-7",
    )
except anthropic.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx
except anthropic.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except anthropic.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Kode kesalahan adalah sebagai berikut:

| Kode Status | Jenis Kesalahan |
|-------------|-----------|
| 400 | `BadRequestError` |
| 401 | `AuthenticationError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 422 | `UnprocessableEntityError` |
| 429 | `RateLimitError` |
| >=500 | `InternalServerError` |
| N/A | `APIConnectionError` |

## ID Permintaan

> Untuk informasi lebih lanjut tentang debugging permintaan, lihat [dokumentasi kesalahan](/docs/id/api/errors#request-id).

Semua respons objek dalam SDK menyediakan properti `_request_id` yang ditambahkan dari header respons `request-id` sehingga Anda dapat dengan cepat mencatat permintaan yang gagal dan melaporkannya kembali ke Anthropic.

```python
message = client.messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-4-7",
)
print(message._request_id)  # e.g., req_018EeWyXxfu5pfWkrYcMdjWG
```

<Note>
Tidak seperti properti lain yang menggunakan awalan `_`, properti `_request_id` bersifat publik. Kecuali didokumentasikan sebaliknya, semua properti, metode, dan modul awalan `_` lainnya bersifat pribadi.
</Note>

## Percobaan ulang

Kesalahan tertentu secara otomatis dicoba ulang 2 kali secara default, dengan backoff eksponensial pendek. Kesalahan koneksi (misalnya, karena masalah konektivitas jaringan), 408 Request Timeout, 409 Conflict, 429 Rate Limit, dan >=500 Internal errors semuanya dicoba ulang secara default.

Anda dapat menggunakan opsi `max_retries` untuk mengonfigurasi atau menonaktifkan ini:

```python hidelines={1..2}
from anthropic import Anthropic

# Configure the default for all requests:
client = Anthropic(
    max_retries=0,  # default is 2
)

# Or, configure per-request:
client.with_options(max_retries=5).messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-4-7",
)
```

## Batas waktu

Secara default permintaan habis waktu setelah 10 menit. Anda dapat mengonfigurasi ini dengan opsi `timeout`, yang menerima float atau objek `httpx.Timeout`:

```python
import httpx
from anthropic import Anthropic

# Configure the default for all requests:
client = Anthropic(
    timeout=20.0,  # 20 seconds (default is 10 minutes)
)

# More granular control:
client = Anthropic(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
client.with_options(timeout=5.0).messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-4-7",
)
```

Pada batas waktu, `APITimeoutError` akan dimunculkan.

Perhatikan bahwa permintaan yang habis waktu akan [dicoba ulang dua kali secara default](#retries).

## Permintaan panjang

<Warning>
Pertimbangkan menggunakan streaming [Messages API](#streaming-responses) untuk permintaan yang berjalan lebih lama.
</Warning>

Hindari menetapkan nilai `max_tokens` besar tanpa menggunakan streaming. Beberapa jaringan mungkin memutuskan koneksi idle setelah periode waktu tertentu, yang dapat menyebabkan permintaan gagal atau [habis waktu](#timeouts) tanpa menerima respons dari Anthropic.

SDK akan melempar `ValueError` jika permintaan non-streaming diharapkan memakan waktu lebih lama dari sekitar 10 menit. Melewatkan `stream=True` atau mengganti opsi `timeout` di tingkat klien atau permintaan menonaktifkan kesalahan ini.

Latensi permintaan yang diharapkan lebih lama dari [batas waktu](#timeouts) untuk permintaan non-streaming akan menghasilkan klien mengakhiri koneksi dan mencoba ulang tanpa menerima respons.

SDK menetapkan opsi [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/overview.html) untuk mengurangi dampak batas waktu koneksi idle pada beberapa jaringan. Ini dapat ditimpa dengan melewatkan opsi `http_client` kustom ke klien.

## Paginasi otomatis

Metode daftar dalam Claude API dipaginasi. Anda dapat menggunakan sintaks `for` untuk mengulangi item di semua halaman:

```python hidelines={1..2}
from anthropic import Anthropic

client = Anthropic()

all_batches = []
# Automatically fetches more pages as needed.
for batch in client.messages.batches.list(limit=20):
    all_batches.append(batch)
print(all_batches)
```

Untuk iterasi asinkron:

```python hidelines={1..6}
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()


async def main() -> None:
    all_batches = []
    async for batch in client.messages.batches.list(limit=20):
        all_batches.append(batch)
    print(all_batches)


asyncio.run(main())
```

Alternatifnya, Anda dapat menggunakan metode `.has_next_page()`, `.next_page_info()`, atau `.get_next_page()` untuk kontrol yang lebih granular saat bekerja dengan halaman:

```python nocheck
first_page = await client.messages.batches.list(limit=20)

if first_page.has_next_page():
    print(f"will fetch next page using these details: {first_page.next_page_info()}")
    next_page = await first_page.get_next_page()
    print(f"number of items we just fetched: {len(next_page.data)}")

# Remove `await` for non-async usage.
```

Atau bekerja langsung dengan data yang dikembalikan:

```python nocheck
first_page = await client.messages.batches.list(limit=20)

print(f"next page cursor: {first_page.last_id}")
for batch in first_page.data:
    print(batch.id)

# Remove `await` for non-async usage.
```

## Header default

SDK secara otomatis mengirimkan header `anthropic-version` yang diatur ke `2023-06-01`.

Jika perlu, Anda dapat menimpanya dengan menetapkan header default pada objek klien atau per-permintaan.

<Warning>
Menimpa header default dapat menghasilkan tipe yang tidak benar dan perilaku tidak terduga atau tidak terdefinisi lainnya dalam SDK.
</Warning>

```python nocheck hidelines={1..2}
from anthropic import Anthropic

# Set default headers for all requests on the client
client = Anthropic(
    default_headers={"anthropic-version": "My-Custom-Value"},
)

# Or override per-request
client.messages.with_raw_response.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-4-7",
    extra_headers={"anthropic-version": "My-Custom-Value"},
)
```

## Sistem tipe

### Parameter permintaan

Parameter permintaan bersarang adalah [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict). Respons adalah [model Pydantic](https://docs.pydantic.dev) yang juga memiliki metode pembantu untuk hal-hal seperti serialisasi kembali ke JSON ([`v1`](https://docs.pydantic.dev/1.10/usage/models/), [`v2`](https://docs.pydantic.dev/latest/concepts/serialization/)).

Permintaan dan respons yang diketik memberikan autocomplete dan dokumentasi dalam editor Anda. Jika Anda ingin melihat kesalahan tipe di VS Code untuk membantu menangkap bug lebih awal, atur `python.analysis.typeCheckingMode` ke `basic`.

### Model respons

Untuk mengonversi model Pydantic ke kamus, gunakan metode pembantu:

```python nocheck
message = client.messages.create(...)

# Convert to JSON string
json_str = message.to_json()

# Convert to dictionary
data = message.to_dict()
```

### Menangani null vs field yang hilang

Dalam respons, Anda dapat membedakan antara field yang secara eksplisit `null` versus field yang tidak dikembalikan (hilang):

```python nocheck
response = client.messages.create(
    model="claude-opus-4-7",
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

`Response` "mentah" yang dikembalikan oleh `httpx` dapat diakses melalui properti `.with_raw_response` pada klien. Ini berguna untuk mengakses header respons atau metadata lainnya:

```python hidelines={1..2}
from anthropic import Anthropic

client = Anthropic()

response = client.messages.with_raw_response.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-4-7",
)

print(response.headers.get("x-request-id"))
message = (
    response.parse()
)  # get the object that `messages.create()` would have returned
print(message.content)
```

Metode ini mengembalikan objek `APIResponse`.

### Streaming body respons

Pendekatan `.with_raw_response` di atas dengan antusias membaca body respons penuh saat Anda membuat permintaan. Untuk streaming body respons sebagai gantinya, gunakan `.with_streaming_response`, yang memerlukan context manager dan hanya membaca body respons setelah Anda memanggil `.read()`, `.text()`, `.json()`, `.iter_bytes()`, `.iter_text()`, `.iter_lines()`, atau `.parse()`. Dalam klien asinkron, ini adalah metode asinkron.

```python
with client.messages.with_streaming_response.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-4-7",
) as response:
    print(response.headers.get("x-request-id"))

    for line in response.iter_lines():
        print(line)
```

Context manager diperlukan sehingga respons akan ditutup dengan andal.

### Logging

SDK menggunakan modul `logging` perpustakaan standar.

Anda dapat mengaktifkan logging dengan menetapkan variabel lingkungan `ANTHROPIC_LOG` ke salah satu dari `debug`, `info`, `warn`, atau `off`:

```bash
export ANTHROPIC_LOG=debug
```

### Membuat permintaan kustom/tidak terdokumentasi

Perpustakaan ini diketik untuk akses yang nyaman ke API yang terdokumentasi. Jika Anda perlu mengakses endpoint, param, atau properti respons yang tidak terdokumentasi, perpustakaan masih dapat digunakan.

#### Endpoint yang tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi, Anda dapat menggunakan `client.get`, `client.post`, dan verba HTTP lainnya. Opsi pada klien, seperti percobaan ulang, akan dihormati saat membuat permintaan ini.

```python nocheck
import httpx

response = client.post(
    "/foo",
    cast_to=httpx.Response,
    body={"my_param": True},
)

print(response.json())
```

#### Param permintaan yang tidak terdokumentasi

Jika Anda ingin secara eksplisit mengirim param tambahan, Anda dapat melakukannya dengan opsi permintaan `extra_query`, `extra_body`, dan `extra_headers`.

<Warning>
Parameter `extra_` menimpa parameter terdokumentasi dengan nama yang sama. Untuk alasan keamanan, pastikan metode ini hanya digunakan dengan data input yang terpercaya.
</Warning>

#### Properti respons yang tidak terdokumentasi

Untuk mengakses properti respons yang tidak terdokumentasi, Anda dapat mengakses field tambahan seperti `response.unknown_prop`. Anda juga dapat mendapatkan semua field tambahan pada model Pydantic sebagai dict dengan `response.model_extra`.

### Mengonfigurasi klien HTTP

Anda dapat langsung menimpa [klien httpx](https://www.python-httpx.org/api/#client) untuk menyesuaikannya dengan kasus penggunaan Anda, termasuk dukungan untuk proxy dan transport:

```python
import httpx
from anthropic import Anthropic, DefaultHttpxClient

client = Anthropic(
    # Or use the `ANTHROPIC_BASE_URL` env var
    base_url="http://my.test.server.example.com:8083",
    http_client=DefaultHttpxClient(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

Anda juga dapat menyesuaikan klien berdasarkan per-permintaan dengan menggunakan `with_options()`:

```python
client.with_options(http_client=DefaultHttpxClient(...))
```

<Note>
Gunakan `DefaultHttpxClient` dan `DefaultAsyncHttpxClient` sebagai pengganti `httpx.Client` dan `httpx.AsyncClient` mentah untuk memastikan konfigurasi default SDK (batas waktu, batas koneksi, dll.) dipertahankan.
</Note>

### Mengelola sumber daya HTTP

Secara default perpustakaan menutup koneksi HTTP yang mendasar setiap kali klien [garbage collected](https://docs.python.org/3/reference/datamodel.html#object.__del__). Anda dapat secara manual menutup klien menggunakan metode `.close()` jika diinginkan, atau dengan context manager yang ditutup saat keluar.

```python nocheck hidelines={1..2}
from anthropic import Anthropic

with Anthropic() as client:
    message = client.messages.create(...)

# HTTP client is automatically closed
```

## Fitur beta

Fitur beta tersedia sebelum rilis umum untuk mendapatkan umpan balik awal dan menguji fungsionalitas baru. Anda dapat memeriksa ketersediaan semua kemampuan dan alat Claude di [ikhtisar build with Claude](/docs/id/build-with-claude/overview).

Anda dapat mengakses sebagian besar fitur API beta melalui properti `beta` klien. Untuk mengaktifkan fitur beta tertentu, Anda perlu menambahkan [header beta](/docs/id/api/beta-headers) yang sesuai ke field `betas` saat membuat pesan.

Misalnya, untuk menggunakan [Files API](/docs/id/build-with-claude/files):

```python nocheck hidelines={1..2}
from anthropic import Anthropic

client = Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please summarize this document for me."},
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": "file_abc123",
                    },
                },
            ],
        },
    ],
    betas=["files-api-2025-04-14"],
)
```

## Integrasi platform

<Note>
Untuk panduan penyiapan platform terperinci dengan contoh kode, lihat:
- [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock)
- [Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)
- [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry)
</Note>

Ketiga kelas klien disertakan dalam paket `anthropic` dasar:

| Penyedia | Klien | Dependensi tambahan |
|-----------|--------|-------------------|
| Bedrock | `from anthropic import AnthropicBedrock` | `pip install anthropic[bedrock]` |
| Vertex AI | `from anthropic import AnthropicVertex` | `pip install anthropic[vertex]` |
| Foundry | `from anthropic import AnthropicFoundry` | Tidak ada |

## Semantic versioning

Paket ini umumnya mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan yang tidak kompatibel ke belakang tertentu dapat dirilis sebagai versi minor:

1. Perubahan yang hanya mempengaruhi tipe statis, tanpa merusak perilaku runtime.
2. Perubahan pada internal perpustakaan yang secara teknis publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
3. Perubahan yang tidak diharapkan berdampak pada sebagian besar pengguna dalam praktik.

### Menentukan versi yang diinstal

Jika Anda telah meningkatkan ke versi terbaru tetapi tidak melihat fitur baru yang Anda harapkan, lingkungan Python Anda kemungkinan masih menggunakan versi yang lebih lama. Anda dapat menentukan versi yang digunakan saat runtime dengan:

```python hidelines={1..2}
import anthropic

print(anthropic.__version__)
```

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-python)
- [Referensi API](/docs/id/api/overview)
- [Panduan streaming](/docs/id/build-with-claude/streaming)
- [Panduan penggunaan alat](/docs/id/agents-and-tools/tool-use/overview)