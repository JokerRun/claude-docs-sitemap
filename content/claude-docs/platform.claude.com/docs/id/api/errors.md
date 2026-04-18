---
source: platform
url: https://platform.claude.com/docs/id/api/errors
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: cf6b21d30a870a8c0d0c894c19b13e6e7a370de72e23a662a8abb62f445b5e22
---

# Kesalahan

Panduan lengkap tentang kode kesalahan HTTP, batasan ukuran permintaan, bentuk kesalahan, ID permintaan, dan kesalahan validasi umum dalam API Anthropic.

---

## Kesalahan HTTP

API mengikuti format kode kesalahan HTTP yang dapat diprediksi:

* 400 - `invalid_request_error`: Ada masalah dengan format atau konten permintaan Anda. Jenis kesalahan ini juga dapat digunakan untuk kode status 4XX lainnya yang tidak tercantum di bawah.
* 401 - `authentication_error`: Ada masalah dengan kunci API Anda.
* 402 - `billing_error`: Ada masalah dengan informasi penagihan atau pembayaran Anda. Periksa detail pembayaran Anda di [Console](https://platform.claude.com).
* 403 - `permission_error`: Kunci API Anda tidak memiliki izin untuk menggunakan sumber daya yang ditentukan.
* 404 - `not_found_error`: Sumber daya yang diminta tidak ditemukan.
* 413 - `request_too_large`: Permintaan melebihi jumlah byte maksimal yang diizinkan. Ukuran permintaan maksimal adalah 32 MB untuk titik akhir API standar.
* 429 - `rate_limit_error`: Akun Anda telah mencapai batas laju.
* 500 - `api_error`: Kesalahan yang tidak terduga telah terjadi di dalam sistem Anthropic.
* 504 - `timeout_error`: Permintaan habis waktu saat diproses. Pertimbangkan untuk menggunakan [streaming](/docs/id/build-with-claude/streaming) untuk permintaan yang berjalan lama.
* 529 - `overloaded_error`: API sedang kelebihan beban sementara.

  <Warning>
  Kesalahan 529 dapat terjadi ketika API mengalami lalu lintas tinggi di semua pengguna.

  Dalam kasus yang jarang terjadi, jika organisasi Anda mengalami peningkatan penggunaan yang tajam, Anda mungkin melihat kesalahan 429 karena batas akselerasi pada API. Untuk menghindari mencapai batas akselerasi, tingkatkan lalu lintas Anda secara bertahap dan pertahankan pola penggunaan yang konsisten.
  </Warning>

Saat menerima respons [streaming](/docs/id/build-with-claude/streaming) melalui SSE, ada kemungkinan kesalahan dapat terjadi setelah mengembalikan respons 200, dalam hal ini penanganan kesalahan tidak akan mengikuti mekanisme standar ini.

## Batasan ukuran permintaan

API memberlakukan batasan ukuran permintaan untuk memastikan kinerja optimal:

| Jenis Titik Akhir | Ukuran Permintaan Maksimal |
|:---|:---|
| Messages API | 32 MB |
| Token Counting API | 32 MB |
| [Batch API](/docs/id/build-with-claude/batch-processing) | 256 MB |
| [Files API](/docs/id/build-with-claude/files) | 500 MB |

Jika Anda melampaui batas ini, Anda akan menerima kesalahan 413 `request_too_large`. Kesalahan dikembalikan dari Cloudflare sebelum permintaan mencapai server API.

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

Sesuai dengan kebijakan [versioning](/docs/id/api/versioning), nilai-nilai dalam objek ini dapat berkembang, dan ada kemungkinan nilai `type` akan bertambah seiring waktu.

## ID permintaan

Setiap respons API menyertakan header `request-id` unik. Header ini berisi nilai seperti `req_018EeWyXxfu5pfWkrYcMdjWG`. Saat menghubungi dukungan tentang permintaan tertentu, sertakan ID ini untuk membantu menyelesaikan masalah Anda dengan cepat.

SDK resmi menyediakan nilai ini sebagai properti pada objek respons tingkat atas, berisi nilai header `request-id`:

<CodeGroup>
  ```bash CLI
  # Header request-id dicetak ke stderr dengan --debug:
  ant --debug messages create \
    --model claude-opus-4-7 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python hidelines={1..2}
  import anthropic

  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-4-7",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(f"Request ID: {message._request_id}")
  ```

  ```typescript TypeScript hidelines={1..2}
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  console.log("Request ID:", message._request_id);
  ```
</CodeGroup>

## Permintaan panjang

<Warning>
 Pertimbangkan untuk menggunakan [streaming Messages API](/docs/id/build-with-claude/streaming) atau [Message Batches API](/docs/id/api/creating-message-batches) untuk permintaan yang berjalan lama, terutama yang lebih dari 10 menit.
</Warning>

Hindari menetapkan nilai `max_tokens` yang besar tanpa menggunakan [streaming Messages API](/docs/id/build-with-claude/streaming)
atau [Message Batches API](/docs/id/api/creating-message-batches):

- Beberapa jaringan dapat memutuskan koneksi idle setelah periode waktu yang bervariasi, yang
dapat menyebabkan permintaan gagal atau habis waktu tanpa menerima respons dari Anthropic.
- Jaringan berbeda dalam keandalan; [Message Batches API](/docs/id/api/creating-message-batches) dapat membantu Anda
mengelola risiko masalah jaringan dengan memungkinkan Anda melakukan polling untuk hasil daripada memerlukan koneksi jaringan yang tidak terputus.

Jika Anda membangun integrasi API langsung, Anda harus menyadari bahwa menetapkan [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/programming.html) dapat mengurangi dampak timeout koneksi idle di beberapa jaringan.

[SDK](/docs/id/api/client-sdks) memvalidasi bahwa permintaan Messages API non-streaming Anda tidak diharapkan melebihi timeout 10 menit dan
juga akan menetapkan opsi soket untuk TCP keep-alive.

Jika Anda tidak perlu memproses acara secara bertahap, gunakan `.stream()` dengan `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) untuk mendapatkan objek `Message` lengkap tanpa menulis kode penanganan acara:

<CodeGroup>
    ```python Python
    with client.messages.stream(
        max_tokens=128000,
        messages=[{"role": "user", "content": "Write a detailed analysis..."}],
        model="claude-opus-4-7",
    ) as stream:
        message = stream.get_final_message()
    ```

    ```typescript TypeScript
    const stream = client.messages.stream({
      max_tokens: 128000,
      messages: [{ role: "user", content: "Write a detailed analysis..." }],
      model: "claude-opus-4-7"
    });
    const message = await stream.finalMessage();
    ```
</CodeGroup>

Lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detail lebih lanjut.

## Kesalahan validasi umum

### Prefill tidak didukung

[Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6 tidak mendukung prefilling pesan asisten. Mengirim permintaan dengan pesan asisten terakhir yang sudah diisi sebelumnya ke salah satu model ini mengembalikan kesalahan 400 `invalid_request_error`:

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