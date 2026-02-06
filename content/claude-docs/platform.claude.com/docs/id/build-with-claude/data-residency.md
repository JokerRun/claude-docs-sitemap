---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/data-residency
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 9ca6faf121413fa00432c84ab7839a05e7ac209952725855545e5c28f9beb5a7
---

# Residensi data

Kelola di mana inferensi model berjalan dan di mana data disimpan dengan kontrol geografis.

---

Kontrol residensi data memungkinkan Anda mengelola di mana data Anda diproses dan disimpan. Dua pengaturan independen mengatur hal ini:

- **Inference geo**: Mengontrol di mana inferensi model berjalan, berdasarkan per-permintaan. Atur melalui parameter API `inference_geo` atau sebagai default workspace.
- **Workspace geo**: Mengontrol di mana data disimpan saat istirahat dan di mana pemrosesan endpoint (transcoding gambar, eksekusi kode, dll.) terjadi. Dikonfigurasi di tingkat workspace di [Console](https://platform.claude.com).

## Inference geo

Parameter `inference_geo` mengontrol di mana inferensi model berjalan untuk permintaan API tertentu. Tambahkan ke panggilan `POST /v1/messages` apa pun.

| Nilai | Deskripsi |
|:------|:------------|
| `"global"` | Default. Inferensi dapat berjalan di geografi mana pun yang tersedia untuk kinerja dan ketersediaan optimal. |
| `"us"` | Inferensi hanya berjalan di infrastruktur berbasis AS. |

### Penggunaan API

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 1024,
        "inference_geo": "us",
        "messages": [{
            "role": "user",
            "content": "Summarize the key points of this document."
        }]
    }'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    inference_geo="us",
    messages=[{
        "role": "user",
        "content": "Summarize the key points of this document."
    }]
)

print(response.content[0].text)
# Check where inference actually ran
print(f"Inference geo: {response.usage.inference_geo}")
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  inference_geo: "us",
  messages: [{
    role: "user",
    content: "Summarize the key points of this document."
  }]
});

console.log(response.content[0].text);
// Check where inference actually ran
console.log(`Inference geo: ${response.usage.inference_geo}`);
```
</CodeGroup>

### Respons

Objek `usage` respons mencakup bidang `inference_geo` yang menunjukkan di mana inferensi berjalan:

```json
{
  "usage": {
    "input_tokens": 25,
    "output_tokens": 150,
    "inference_geo": "us"
  }
}
```

### Ketersediaan model

Parameter `inference_geo` didukung pada Claude Opus 4.6 dan semua model berikutnya. Model yang lebih lama yang dirilis sebelum Opus 4.6 tidak mendukung parameter ini. Permintaan dengan `inference_geo` pada model legacy mengembalikan kesalahan 400.

<Note>
Parameter `inference_geo` hanya tersedia di Claude API (1P). Di platform pihak ketiga (AWS Bedrock, Google Vertex AI), wilayah inferensi ditentukan oleh URL endpoint atau profil inferensi, jadi `inference_geo` tidak berlaku. Parameter `inference_geo` juga tidak tersedia melalui [endpoint kompatibilitas OpenAI SDK](/docs/id/api/openai-sdk).
</Note>

### Pembatasan tingkat workspace

Pengaturan workspace juga mendukung pembatasan inference geo mana yang tersedia:

- **`allowed_inference_geos`**: Membatasi geo mana yang dapat digunakan workspace. Jika permintaan menentukan `inference_geo` yang tidak ada dalam daftar ini, API mengembalikan kesalahan.
- **`default_inference_geo`**: Menetapkan geo fallback ketika `inference_geo` dihilangkan dari permintaan. Permintaan individual dapat mengganti ini dengan menetapkan `inference_geo` secara eksplisit.

Pengaturan ini dapat dikonfigurasi melalui Console atau [Admin API](/docs/id/build-with-claude/administration-api) di bawah bidang `data_residency`.

## Workspace geo

Workspace geo ditetapkan saat Anda membuat workspace dan tidak dapat diubah setelahnya. Saat ini, `"us"` adalah satu-satunya workspace geo yang tersedia.

Untuk menetapkan workspace geo, buat workspace baru di [Console](https://platform.claude.com):

1. Buka **Settings** > **Workspaces**.
2. Buat workspace baru.
3. Pilih workspace geo.

## Harga

Harga residensi data bervariasi menurut generasi model:

- **Claude Opus 4.6 dan lebih baru**: Inferensi hanya AS (`inference_geo: "us"`) dihargai pada tingkat 1,1x standar di semua kategori harga token (token input, token output, cache writes, dan cache reads).
- **Routing global** (`inference_geo: "global"` atau dihilangkan): Harga standar berlaku.
- **Model yang lebih lama**: Harga yang ada tidak berubah terlepas dari pengaturan `inference_geo`.

Harga ini berlaku untuk Claude API (1P) saja. Platform pihak ketiga (AWS Bedrock, Google Vertex AI, Microsoft Foundry) memiliki harga regional mereka sendiri. Lihat [halaman harga](/docs/id/about-claude/pricing#data-residency-pricing) untuk detail.

<Note>
Jika Anda menggunakan [Priority Tier](/docs/id/api/service-tiers), pengganda 1,1x untuk inferensi hanya AS juga mempengaruhi cara token dihitung terhadap kapasitas Priority Tier Anda. Setiap token yang dikonsumsi dengan `inference_geo: "us"` mengurangi 1,1 token dari TPM yang berkomitmen, konsisten dengan cara pengganda harga lainnya (prompt caching, long context) mempengaruhi tingkat burndown.
</Note>

## Dukungan Batch API

Parameter `inference_geo` didukung pada [Batch API](/docs/id/build-with-claude/batch-processing). Setiap permintaan dalam batch dapat menentukan nilai `inference_geo` miliknya sendiri.

## Migrasi dari opt-out legacy

Jika organisasi Anda sebelumnya memilih untuk tidak menggunakan routing global untuk menjaga inferensi di AS, workspace Anda telah dikonfigurasi secara otomatis dengan `allowed_inference_geos: ["us"]` dan `default_inference_geo: "us"`. Tidak ada perubahan kode yang diperlukan. Persyaratan residensi data yang ada terus ditegakkan melalui kontrol geo baru.

### Apa yang berubah

Opt-out legacy adalah pengaturan tingkat organisasi yang membatasi semua permintaan ke infrastruktur berbasis AS. Kontrol residensi data baru menggantikan ini dengan dua mekanisme:

- **Kontrol per-permintaan**: Parameter `inference_geo` memungkinkan Anda menentukan `"us"` atau `"global"` pada setiap panggilan API, memberikan Anda fleksibilitas tingkat permintaan.
- **Kontrol workspace**: Pengaturan `default_inference_geo` dan `allowed_inference_geos` di Console memungkinkan Anda menerapkan kebijakan geo di semua kunci dalam workspace.

### Apa yang terjadi pada workspace Anda

Workspace Anda dimigrasikan secara otomatis:

| Pengaturan legacy | Setara baru |
|:---------------|:---------------|
| Opt-out routing global (hanya AS) | `allowed_inference_geos: ["us"]`, `default_inference_geo: "us"` |

Semua permintaan API menggunakan kunci dari workspace Anda terus berjalan di infrastruktur berbasis AS. Tidak ada tindakan yang diperlukan untuk mempertahankan perilaku saat ini Anda.

### Jika Anda ingin menggunakan routing global

Jika persyaratan residensi data Anda telah berubah dan Anda ingin memanfaatkan routing global untuk kinerja dan ketersediaan yang lebih baik, perbarui pengaturan inference geo workspace Anda untuk menyertakan `"global"` dalam geo yang diizinkan dan atur `default_inference_geo` ke `"global"`. Lihat [Pembatasan tingkat workspace](#workspace-level-restrictions) untuk detail.

### Dampak harga

Model legacy tidak terpengaruh oleh migrasi ini. Untuk harga saat ini pada model yang lebih baru, lihat [Harga](#pricing).

## Batasan saat ini

- **Batas laju bersama**: Batas laju dibagikan di semua geo.
- **Inference geo**: Hanya `"us"` dan `"global"` yang tersedia saat peluncuran. Wilayah tambahan akan ditambahkan seiring waktu.
- **Workspace geo**: Hanya `"us"` yang saat ini tersedia. Workspace geo tidak dapat diubah setelah pembuatan workspace.

## Langkah berikutnya

<CardGroup>
  <Card title="Harga" icon="dollar-sign" href="/docs/id/about-claude/pricing#data-residency-pricing">
    Lihat detail harga residensi data.
  </Card>
  <Card title="Workspaces" icon="building" href="/docs/id/build-with-claude/workspaces">
    Pelajari tentang konfigurasi workspace.
  </Card>
  <Card title="Usage and Cost API" icon="chart" href="/docs/id/build-with-claude/usage-cost-api">
    Lacak penggunaan dan biaya berdasarkan residensi data.
  </Card>
</CardGroup>