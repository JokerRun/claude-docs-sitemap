---
source: platform
url: https://platform.claude.com/docs/id/api/errors
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 3fd1a6e3663f15ba43ec1085a0f91f450bf2a24ef591540b1906c1d51c3ffa2a
---

# Kesalahan

Panduan lengkap tentang penanganan kesalahan API Anthropic, termasuk kode HTTP, batasan ukuran permintaan, bentuk kesalahan, dan kesalahan validasi umum.

---

## Kesalahan HTTP

API kami mengikuti format kode kesalahan HTTP yang dapat diprediksi:

* 400 - `invalid_request_error`: Ada masalah dengan format atau konten permintaan Anda. Kami juga dapat menggunakan jenis kesalahan ini untuk kode status 4XX lainnya yang tidak tercantum di bawah.
* 401 - `authentication_error`: Ada masalah dengan kunci API Anda.
* 403 - `permission_error`: Kunci API Anda tidak memiliki izin untuk menggunakan sumber daya yang ditentukan.
* 404 - `not_found_error`: Sumber daya yang diminta tidak ditemukan.
* 413 - `request_too_large`: Permintaan melebihi jumlah byte maksimum yang diizinkan. Ukuran permintaan maksimum adalah 32 MB untuk titik akhir API standar.
* 429 - `rate_limit_error`: Akun Anda telah mencapai batas laju.
* 500 - `api_error`: Kesalahan yang tidak terduga telah terjadi di dalam sistem Anthropic.
* 529 - `overloaded_error`: API sedang kelebihan beban sementara.

  <Warning>
  Kesalahan 529 dapat terjadi ketika API mengalami lalu lintas tinggi di semua pengguna.  
  
  Dalam kasus yang jarang terjadi, jika organisasi Anda mengalami peningkatan penggunaan yang tajam, Anda mungkin melihat kesalahan 429 karena batas akselerasi pada API. Untuk menghindari mencapai batas akselerasi, tingkatkan lalu lintas Anda secara bertahap dan pertahankan pola penggunaan yang konsisten.
  </Warning>

Saat menerima respons [streaming](/docs/id/build-with-claude/streaming) melalui SSE, ada kemungkinan kesalahan dapat terjadi setelah mengembalikan respons 200, dalam hal ini penanganan kesalahan tidak akan mengikuti mekanisme standar ini.

## Batasan ukuran permintaan

API memberlakukan batasan ukuran permintaan untuk memastikan kinerja optimal:

| Jenis Titik Akhir | Ukuran Permintaan Maksimum |
|:---|:---|
| Messages API | 32 MB |
| Token Counting API | 32 MB |
| [Batch API](/docs/id/build-with-claude/batch-processing) | 256 MB |
| [Files API](/docs/id/build-with-claude/files) | 500 MB |

Jika Anda melampaui batas ini, Anda akan menerima kesalahan 413 `request_too_large`. Kesalahan dikembalikan dari Cloudflare sebelum permintaan mencapai server API kami.

## Bentuk kesalahan

Kesalahan selalu dikembalikan sebagai JSON, dengan objek `error` tingkat atas yang selalu menyertakan nilai `type` dan `message`. Respons juga menyertakan bidang `request_id` untuk pelacakan dan debugging yang lebih mudah. Sebagai contoh:

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

Sesuai dengan kebijakan [versioning](/docs/id/api/versioning) kami, kami dapat memperluas nilai dalam objek-objek ini, dan ada kemungkinan bahwa nilai `type` akan berkembang seiring waktu.

## ID permintaan

Setiap respons API menyertakan header `request-id` unik. Header ini berisi nilai seperti `req_018EeWyXxfu5pfWkrYcMdjWG`. Saat menghubungi dukungan tentang permintaan tertentu, harap sertakan ID ini untuk membantu kami menyelesaikan masalah Anda dengan cepat.

SDK resmi kami menyediakan nilai ini sebagai properti pada objek respons tingkat atas, berisi nilai header `request-id`:

<CodeGroup>
  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-4-6",
      max_tokens=1024,
      messages=[
          {"role": "user", "content": "Hello, Claude"}
      ]
  )
  print(f"Request ID: {message._request_id}")
  ```

  ```typescript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const client = new Anthropic();

  const message = await client.messages.create({
    model: 'claude-opus-4-6',
    max_tokens: 1024,
    messages: [
      {"role": "user", "content": "Hello, Claude"}
    ]
  });
  console.log('Request ID:', message._request_id);
  ```
</CodeGroup>

## Permintaan panjang

<Warning>
 Kami sangat mendorong penggunaan [streaming Messages API](/docs/id/build-with-claude/streaming) atau [Message Batches API](/docs/id/api/creating-message-batches) untuk permintaan yang berjalan lama, terutama yang lebih dari 10 menit.
</Warning>

Kami tidak merekomendasikan menetapkan nilai `max_tokens` yang besar tanpa menggunakan [streaming Messages API](/docs/id/build-with-claude/streaming) kami
atau [Message Batches API](/docs/id/api/creating-message-batches):

- Beberapa jaringan mungkin memutuskan koneksi idle setelah periode waktu yang bervariasi, yang
dapat menyebabkan permintaan gagal atau timeout tanpa menerima respons dari Anthropic.
- Jaringan berbeda dalam keandalan; [Message Batches API](/docs/id/api/creating-message-batches) kami dapat membantu Anda
mengelola risiko masalah jaringan dengan memungkinkan Anda menanyakan hasil daripada memerlukan koneksi jaringan yang tidak terputus.

Jika Anda membangun integrasi API langsung, Anda harus menyadari bahwa menetapkan [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/programming.html) dapat mengurangi dampak timeout koneksi idle di beberapa jaringan.

[SDK](/docs/id/api/client-sdks) kami akan memvalidasi bahwa permintaan Messages API non-streaming Anda tidak diharapkan melebihi timeout 10 menit dan
juga akan menetapkan opsi soket untuk TCP keep-alive.

Jika Anda tidak perlu memproses acara secara bertahap, gunakan `.stream()` dengan `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) untuk mendapatkan objek `Message` lengkap tanpa menulis kode penanganan acara:

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
        messages: [{role: 'user', content: 'Write a detailed analysis...'}],
        model: 'claude-opus-4-6',
    });
    const message = await stream.finalMessage();
    ```
</CodeGroup>

Lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detail lebih lanjut.

## Kesalahan validasi umum

### Prefill tidak didukung

Claude Opus 4.6 tidak mendukung prefilling pesan asisten. Mengirim permintaan dengan pesan asisten terakhir yang sudah diisi sebelumnya ke model ini mengembalikan kesalahan 400 `invalid_request_error`:

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