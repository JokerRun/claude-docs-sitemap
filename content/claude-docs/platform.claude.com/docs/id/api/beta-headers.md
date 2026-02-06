---
source: platform
url: https://platform.claude.com/docs/id/api/beta-headers
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: a69f43de73fbddf0aa56a62d4fad8126d15033a605cd479f539930893843617f
---

# Header beta

Dokumentasi untuk menggunakan header beta dengan Claude API

---

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

Fitur-fitur ini dapat berubah dan mungkin dimodifikasi atau dihapus dalam rilis mendatang.

<Info>
Header beta sering digunakan bersama dengan [namespace beta di SDK klien](/docs/id/api/client-sdks#beta-namespace-in-client-sdks)
</Info>

## Cara menggunakan header beta

Untuk mengakses fitur beta, sertakan header `anthropic-beta` dalam permintaan API Anda:

```http
POST /v1/messages
Content-Type: application/json
X-API-Key: YOUR_API_KEY
anthropic-beta: BETA_FEATURE_NAME
```

Saat menggunakan SDK, Anda dapat menentukan header beta dalam opsi permintaan:

<CodeGroup>

```python Python
from anthropic import Anthropic

client = Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ],
    betas=["code-execution-2025-08-25"]
)
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

const msg = await anthropic.beta.messages.create({
  model: 'claude-opus-4-6',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude' }
  ],
  betas: ['code-execution-2025-08-25']
});
```

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello, Claude"}
    ]
  }'
```

</CodeGroup>

<Warning>
Fitur beta bersifat eksperimental dan mungkin:
- Memiliki perubahan yang merusak tanpa pemberitahuan
- Dihentikan atau dihapus
- Memiliki batas laju atau harga yang berbeda
- Tidak tersedia di semua wilayah
</Warning>

### Fitur beta berganda

Untuk menggunakan beberapa fitur beta dalam satu permintaan, sertakan semua nama fitur dalam header yang dipisahkan dengan koma:

```http
anthropic-beta: feature1,feature2,feature3
```

### Konvensi penamaan versi

Nama fitur beta biasanya mengikuti pola: `feature-name-YYYY-MM-DD`, di mana tanggal menunjukkan kapan versi beta dirilis. Selalu gunakan nama fitur beta yang tepat seperti yang didokumentasikan.

## Penanganan kesalahan

Jika Anda menggunakan header beta yang tidak valid atau tidak tersedia, Anda akan menerima respons kesalahan:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Unsupported beta header: invalid-beta-name"
  }
}
```

## Mendapatkan bantuan

Untuk pertanyaan tentang fitur beta:

1. Periksa dokumentasi untuk fitur spesifik
2. Tinjau [changelog API](/docs/id/api/versioning) untuk pembaruan
3. Hubungi dukungan untuk bantuan dengan penggunaan produksi

Ingat bahwa fitur beta disediakan "sebagaimana adanya" dan mungkin tidak memiliki jaminan SLA yang sama dengan fitur API stabil.