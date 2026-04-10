---
source: platform
url: https://platform.claude.com/docs/id/api/errors
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 728340eeb47213650579ad6fbf650e9b147e1490b5f2eb8a36161fd19d0be804
---

# Error

---

## Error HTTP

API mengikuti format kode error HTTP yang dapat diprediksi:

* 400 - `invalid_request_error`: Ada masalah dengan format atau konten permintaan Anda. Jenis error ini juga dapat digunakan untuk kode status 4XX lainnya yang tidak tercantum di bawah.
* 401 - `authentication_error`: Ada masalah dengan API key Anda.
* 402 - `billing_error`: Ada masalah dengan informasi penagihan atau pembayaran Anda. Periksa detail pembayaran Anda di [Console](https://platform.claude.com).
* 403 - `permission_error`: API key Anda tidak memiliki izin untuk menggunakan sumber daya yang ditentukan.
* 404 - `not_found_error`: Sumber daya yang diminta tidak ditemukan.
* 413 - `request_too_large`: Permintaan melebihi jumlah byte maksimum yang diizinkan. Ukuran permintaan maksimum adalah 32 MB untuk endpoint API standar.
* 429 - `rate_limit_error`: Akun Anda telah mencapai batas rate limit.
* 500 - `api_error`: Terjadi error tak terduga di dalam sistem internal Anthropic.
* 504 - `timeout_error`: Permintaan habis waktu saat diproses. Pertimbangkan untuk menggunakan [streaming](/docs/id/build-with-claude/streaming) untuk permintaan yang berjalan lama.
* 529 - `overloaded_error`: API sedang kelebihan beban sementara.

  <Warning>
  Error 529 dapat terjadi ketika API mengalami lalu lintas tinggi dari semua pengguna.

  Dalam kasus yang jarang terjadi, jika organisasi Anda mengalami peningkatan penggunaan yang tajam, Anda mungkin melihat error 429 karena batas akselerasi pada API. Untuk menghindari mencapai batas akselerasi, tingkatkan lalu lintas Anda secara bertahap dan pertahankan pola penggunaan yang konsisten.
  </Warning>

Saat menerima respons [streaming](/docs/id/build-with-claude/streaming) melalui SSE, ada kemungkinan error dapat terjadi setelah mengembalikan respons 200, di mana penanganan error tidak akan mengikuti mekanisme standar ini.

## Batas ukuran permintaan

API memberlakukan batas ukuran permintaan untuk memastikan performa optimal:

| Jenis Endpoint | Ukuran Permintaan Maksimum |
|:---|:---|
| Messages API | 32 MB |
| Token Counting API | 32 MB |
| [Batch API](/docs/id/build-with-claude/batch-processing) | 256 MB |
| [Files API](/docs/id/build-with-claude/files) | 500 MB |

Jika Anda melebihi batas ini, Anda akan menerima error 413 `request_too_large`. Error dikembalikan dari Cloudflare sebelum permintaan mencapai server API.

## Bentuk error

Error selalu dikembalikan sebagai JSON, dengan objek `error` tingkat atas yang selalu menyertakan nilai `type` dan `message`. Respons juga menyertakan field `request_id` untuk pelacakan dan debugging yang lebih mudah. Misalnya:

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

Sesuai dengan kebijakan [versioning](/docs/id/api/versioning), nilai-nilai dalam objek ini dapat berkembang, dan nilai `type` mungkin bertambah seiring waktu.

## Request id

Setiap respons API menyertakan header `request-id` yang unik. Header ini berisi nilai seperti `req_018EeWyXxfu5pfWkrYcMdjWG`. Saat menghubungi dukungan tentang permintaan tertentu, sertakan ID ini untuk membantu menyelesaikan masalah Anda dengan cepat.

SDK resmi menyediakan nilai ini sebagai properti pada objek respons tingkat atas, yang berisi nilai header `request-id`:

<CodeGroup>
  ```bash CLI
  # Header request-id dicetak ke stderr dengan --debug:
  ant --debug messages create \
    --model claude-opus-4-6 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python hidelines={1..2}
  import anthropic

  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-4-6",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(f"Request ID: {message._request_id}")
  ```

  ```typescript TypeScript hidelines={1..2}
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  console.log("Request ID:", message._request_id);
  ```
</CodeGroup>

## Permintaan yang berjalan lama

<Warning>
 Pertimbangkan untuk menggunakan [streaming Messages API](/docs/id/build-with-claude/streaming) atau [Message Batches API](/docs/id/api/creating-message-batches) untuk permintaan yang berjalan lama, terutama yang melebihi 10 menit.
</Warning>

Hindari menetapkan nilai `max_tokens` yang besar tanpa menggunakan [streaming Messages API](/docs/id/build-with-claude/streaming)
atau [Message Batches API](/docs/id/api/creating-message-batches):

- Beberapa jaringan mungkin memutus koneksi yang tidak aktif setelah periode waktu tertentu, yang
dapat menyebabkan permintaan gagal atau habis waktu tanpa menerima respons dari Anthropic.
- Jaringan berbeda dalam keandalan; [Message Batches API](/docs/id/api/creating-message-batches) dapat membantu Anda
mengelola risiko masalah jaringan dengan memungkinkan Anda melakukan polling untuk hasil daripada memerlukan koneksi jaringan yang tidak terputus.

Jika Anda membangun integrasi API langsung, Anda harus mengetahui bahwa menetapkan [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/programming.html) dapat mengurangi dampak timeout koneksi yang tidak aktif pada beberapa jaringan.

[SDK](/docs/id/api/client-sdks) memvalidasi bahwa permintaan Messages API non-streaming Anda tidak diperkirakan melebihi timeout 10 menit dan
juga akan menetapkan opsi socket untuk TCP keep-alive.

Jika Anda tidak perlu memproses event secara bertahap, gunakan `.stream()` dengan `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) untuk mendapatkan objek `Message` yang lengkap tanpa menulis kode penanganan event:

<CodeGroup>
    ```python Python
    with client.messages.stream(
        max_tokens=128000,
        messages=[{"role": "user", "content": "Write a detailed analysis..."}],
        model="claude-opus-4-6",
    ) as stream:
        message = stream.get_final_message()
    ```

    ```typescript TypeScript
    const stream = client.messages.stream({
      max_tokens: 128000,
      messages: [{ role: "user", content: "Write a detailed analysis..." }],
      model: "claude-opus-4-6"
    });
    const message = await stream.finalMessage();
    ```
</CodeGroup>

Lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detail lebih lanjut.

## Error validasi umum

### Prefill tidak didukung

[Claude Mythos Preview](https://anthropic.com/glasswing) dan Claude Opus 4.6 tidak mendukung pengisian awal (prefilling) pesan asisten. Mengirim permintaan dengan pesan asisten terakhir yang telah diisi awal ke salah satu model mengembalikan error 400 `invalid_request_error`:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Prefilling assistant messages is not supported for this model."
  }
}
```

Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi system prompt, atau [`output_config.format`](/docs/id/build-with-claude/structured-outputs#json-outputs) sebagai gantinya.