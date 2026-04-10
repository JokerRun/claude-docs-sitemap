---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/data-residency
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: f3efeb5c9907865003ee426d632c3cae583bde2191dba182bfcdc33a75fbf3cd
---

# Residensi data

Kelola di mana inferensi model berjalan dan di mana data disimpan dengan kontrol geografis.

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Kontrol residensi data memungkinkan Anda mengelola di mana data Anda diproses dan disimpan. Dua pengaturan independen mengatur hal ini:

- **Geo inferensi:** Mengontrol di mana inferensi model berjalan, berdasarkan per-permintaan. Diatur melalui parameter API `inference_geo` atau sebagai default workspace.
- **Geo workspace:** Mengontrol di mana data disimpan saat tidak aktif dan di mana pemrosesan endpoint (transcoding gambar, eksekusi kode, dll.) terjadi. Dikonfigurasi di tingkat workspace di [Console](https://platform.claude.com).

## Geo inferensi

Parameter `inference_geo` mengontrol di mana inferensi model berjalan untuk permintaan API tertentu. Tambahkan ke panggilan `POST /v1/messages` mana pun.

| Nilai | Deskripsi |
|:------|:------------|
| `"global"` | Default. Inferensi dapat berjalan di geografi mana pun yang tersedia untuk performa dan ketersediaan optimal. |
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

```bash CLI
ant messages create \
  --model claude-opus-4-6 \
  --max-tokens 1024 \
  --inference-geo us \
  --message '{role: user, content: "Summarize the key points of this document."}' \
  --transform '{content.0.text,usage.inference_geo}' --format yaml
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    inference_geo="us",
    messages=[
        {"role": "user", "content": "Summarize the key points of this document."}
    ],
)

print(response.content[0].text)
# Check where inference actually ran
print(f"Inference geo: {response.usage.inference_geo}")
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  inference_geo: "us",
  messages: [
    {
      role: "user",
      content: "Summarize the key points of this document."
    }
  ]
});

const textBlock = response.content.find(
  (block): block is Anthropic.TextBlock => block.type === "text"
);
console.log(textBlock?.text);
// Check where inference actually ran
console.log(`Inference geo: ${response.usage.inference_geo}`);
```
</CodeGroup>

### Respons

Objek `usage` dalam respons menyertakan field `inference_geo` yang menunjukkan di mana inferensi berjalan:

```json Output
{
  "usage": {
    "input_tokens": 25,
    "output_tokens": 150,
    "inference_geo": "us"
  }
}
```

### Ketersediaan model

Parameter `inference_geo` didukung pada Claude Opus 4.6 dan semua model berikutnya. Model lama yang dirilis sebelum Opus 4.6 tidak mendukung parameter ini. Permintaan dengan `inference_geo` pada model lama akan mengembalikan error 400.

<Note>
Parameter `inference_geo` hanya tersedia di Claude API (1P). Pada platform pihak ketiga (AWS Bedrock, Google Vertex AI), wilayah inferensi ditentukan oleh URL endpoint atau profil inferensi, sehingga `inference_geo` tidak berlaku. Parameter `inference_geo` juga tidak tersedia melalui [endpoint kompatibilitas OpenAI SDK](/docs/id/api/openai-sdk).
</Note>

### Pembatasan tingkat workspace

Pengaturan workspace juga mendukung pembatasan geo inferensi mana yang tersedia:

- **`allowed_inference_geos`:** Membatasi geo mana yang dapat digunakan oleh workspace. Jika permintaan menentukan `inference_geo` yang tidak ada dalam daftar ini, API akan mengembalikan error.
- **`default_inference_geo`:** Menetapkan geo fallback ketika `inference_geo` dihilangkan dari permintaan. Permintaan individual dapat mengganti ini dengan menetapkan `inference_geo` secara eksplisit.

Pengaturan ini dapat dikonfigurasi melalui Console atau [Admin API](/docs/id/build-with-claude/administration-api) di bawah field `data_residency`.

## Geo workspace

Geo workspace ditetapkan saat Anda membuat workspace dan tidak dapat diubah setelahnya. Saat ini, `"us"` adalah satu-satunya geo workspace yang tersedia.

Untuk menetapkan geo workspace, buat workspace baru di [Console](https://platform.claude.com):

1. Buka **Settings** > **Workspaces**.
2. Buat workspace baru.
3. Pilih geo workspace.

## Harga

Harga residensi data bervariasi berdasarkan generasi model:

- **Claude Opus 4.6 dan yang lebih baru:** Inferensi khusus AS (`inference_geo: "us"`) dihargai 1,1x tarif standar di semua kategori harga token (token input, token output, penulisan cache, dan pembacaan cache).
- **Perutean global** (`inference_geo: "global"` atau dihilangkan): Harga standar berlaku.
- **Model lama:** Harga yang ada tidak berubah terlepas dari pengaturan `inference_geo`.

Harga ini hanya berlaku untuk Claude API (1P). Platform pihak ketiga (AWS Bedrock, Google Vertex AI) memiliki harga regional mereka sendiri. Lihat [halaman harga](/docs/id/about-claude/pricing#data-residency-pricing) untuk detailnya.

<Note>
Jika Anda menggunakan [Priority Tier](/docs/id/api/service-tiers), pengali 1,1x untuk inferensi khusus AS juga memengaruhi cara token dihitung terhadap kapasitas Priority Tier Anda. Setiap token yang dikonsumsi dengan `inference_geo: "us"` akan mengurangi 1,1 token dari TPM yang Anda komitkan, konsisten dengan cara pengali harga lainnya (seperti prompt caching) memengaruhi tingkat burndown.
</Note>

## Dukungan Batch API

Parameter `inference_geo` didukung pada [Batch API](/docs/id/build-with-claude/batch-processing). Setiap permintaan dalam batch dapat menentukan nilai `inference_geo`-nya sendiri.

## Migrasi dari opt-out lama

Jika organisasi Anda sebelumnya memilih keluar dari perutean global untuk menjaga inferensi di AS, workspace Anda telah dikonfigurasi secara otomatis dengan `allowed_inference_geos: ["us"]` dan `default_inference_geo: "us"`. Tidak diperlukan perubahan kode. Persyaratan residensi data Anda yang ada terus diterapkan melalui kontrol geo baru.

### Apa yang berubah

Opt-out lama adalah pengaturan tingkat organisasi yang membatasi semua permintaan ke infrastruktur berbasis AS. Kontrol residensi data baru menggantikan ini dengan dua mekanisme:

- **Kontrol per-permintaan:** Parameter `inference_geo` memungkinkan Anda menentukan `"us"` atau `"global"` pada setiap panggilan API, memberikan fleksibilitas tingkat permintaan.
- **Kontrol workspace:** Pengaturan `default_inference_geo` dan `allowed_inference_geos` di Console memungkinkan Anda menerapkan kebijakan geo di semua kunci dalam workspace.

### Apa yang terjadi pada workspace Anda

Workspace Anda dimigrasikan secara otomatis:

| Pengaturan lama | Ekuivalen baru |
|:---------------|:---------------|
| Opt-out perutean global (khusus AS) | `allowed_inference_geos: ["us"]`, `default_inference_geo: "us"` |

Semua permintaan API yang menggunakan kunci dari workspace Anda terus berjalan di infrastruktur berbasis AS. Tidak diperlukan tindakan untuk mempertahankan perilaku Anda saat ini.

### Jika Anda ingin menggunakan perutean global

Jika persyaratan residensi data Anda telah berubah dan Anda ingin memanfaatkan perutean global untuk performa dan ketersediaan yang lebih baik, perbarui pengaturan geo inferensi workspace Anda untuk menyertakan `"global"` dalam geo yang diizinkan dan tetapkan `default_inference_geo` ke `"global"`. Lihat [Pembatasan tingkat workspace](#workspace-level-restrictions) untuk detailnya.

### Dampak harga

Model lama tidak terpengaruh oleh migrasi ini. Untuk harga terkini pada model yang lebih baru, lihat [Harga](#pricing).

## Keterbatasan saat ini

- **Batas rate bersama:** Batas rate dibagikan di semua geo.
- **Geo inferensi:** Hanya `"us"` dan `"global"` yang tersedia saat peluncuran. Wilayah tambahan akan ditambahkan seiring waktu.
- **Geo workspace:** Hanya `"us"` yang saat ini tersedia. Geo workspace tidak dapat diubah setelah pembuatan workspace.

## Langkah selanjutnya

<CardGroup>
  <Card title="Harga" icon="dollar-sign" href="/docs/id/about-claude/pricing#data-residency-pricing">
    Lihat detail harga residensi data.
  </Card>
  <Card title="Workspace" icon="building" href="/docs/id/build-with-claude/workspaces">
    Pelajari tentang konfigurasi workspace.
  </Card>
  <Card title="API Penggunaan dan Biaya" icon="chart" href="/docs/id/build-with-claude/usage-cost-api">
    Lacak penggunaan dan biaya berdasarkan residensi data.
  </Card>
</CardGroup>