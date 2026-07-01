---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/data-residency
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: 9ad590dc72c3ba64d7e8200a400c57a81dc7593c9c0297c8765410ae99b91c5b
---

# Residensi data

Kelola di mana inferensi model dijalankan dan di mana data disimpan dengan kontrol geografis.

---

<Note>
  Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Kontrol residensi data memungkinkan Anda mengelola di mana data Anda diproses dan disimpan. Dua pengaturan independen mengatur hal ini:

* **Inference geo:** Mengontrol di mana inferensi model dijalankan, berdasarkan per permintaan. Diatur melalui parameter API `inference_geo` atau sebagai default workspace.
* **Workspace geo:** Mengontrol di mana data disimpan saat tidak aktif (at rest) dan di mana pemrosesan endpoint (seperti transcoding gambar dan eksekusi kode) terjadi. Dikonfigurasi pada tingkat workspace di [Claude Console](https://platform.claude.com).

<Note>
  [Claude Managed Agents](/docs/id/managed-agents/overview) tidak mendukung parameter `inference_geo`, tetapi mengikuti Workspace geo yang dikonfigurasi di Console. Dengan [self-hosted sandboxes](/docs/id/managed-agents/self-hosted-sandboxes), eksekusi alat dan filesystem sandbox tetap berada di infrastruktur yang Anda kontrol.
</Note>

## Inference geo

Parameter `inference_geo` mengontrol di mana inferensi model dijalankan untuk permintaan API tertentu. Tambahkan parameter ini ke panggilan `POST /v1/messages` mana pun.

| Nilai      | Deskripsi                                                                                                                |
| ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| `"global"` | Default. Inferensi dapat dijalankan di wilayah geografis mana pun yang tersedia untuk performa dan ketersediaan optimal. |
| `"us"`     | Inferensi hanya dijalankan di infrastruktur yang berbasis di AS.                                                         |

### Penggunaan API

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
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
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --inference-geo us \
    --message '{role: user, content: "Summarize the key points of this document."}' \
    --transform '{content.0.text,usage.inference_geo}' --format yaml
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      inference_geo="us",
      messages=[
          {"role": "user", "content": "Summarize the key points of this document."}
      ],
  )

  print(response.content[0].text)
  # Periksa di mana inferensi sebenarnya dijalankan
  print(f"Inference geo: {response.usage.inference_geo}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
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
  // Periksa di mana inferensi sebenarnya dijalankan
  console.log(`Inference geo: ${response.usage.inference_geo}`);
  ```
</CodeGroup>

### Respons

Objek `usage` dalam respons menyertakan field `inference_geo` yang menunjukkan di mana inferensi dijalankan:

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

Parameter `inference_geo` didukung pada Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih baru. Permintaan dengan `inference_geo` pada Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, atau model yang lebih lama akan mengembalikan error 400.

<Note>
  Parameter `inference_geo` tersedia di Claude API (first-party) dan [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws). Di Amazon Bedrock dan Google Cloud, wilayah inferensi ditentukan oleh URL endpoint atau profil inferensi, sehingga `inference_geo` tidak berlaku. Di [Claude in Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry), `inference_geo` juga tidak berlaku: deployment yang di-host di Azure dapat menggunakan tipe deployment US Data Zone Standard, yang menjaga inferensi tetap berada di Amerika Serikat. Parameter `inference_geo` juga tidak tersedia melalui [endpoint kompatibilitas OpenAI SDK](/docs/id/cli-sdks-libraries/libraries/openai-sdk).
</Note>

### Pembatasan tingkat workspace

Pengaturan workspace juga mendukung pembatasan inference geo mana yang tersedia:

* **`allowed_inference_geos`:** Membatasi geo mana yang dapat digunakan oleh workspace. Jika permintaan menentukan `inference_geo` yang tidak ada dalam daftar ini, API akan mengembalikan error.
* **`default_inference_geo`:** Menetapkan geo fallback ketika `inference_geo` dihilangkan dari permintaan. Permintaan individual dapat menimpa ini dengan menetapkan `inference_geo` secara eksplisit.

Pengaturan ini dapat dikonfigurasi melalui Console atau [Admin API](/docs/id/manage-claude/admin-api) di bawah field `data_residency`.

## Workspace geo

Workspace geo ditetapkan saat Anda membuat workspace dan tidak dapat diubah setelahnya. Saat ini, `"us"` adalah satu-satunya workspace geo yang tersedia.

Untuk menetapkan workspace geo, buat workspace baru di [Console](https://platform.claude.com):

1. Buka **Settings** > **Workspaces**.
2. Buat workspace baru.
3. Pilih workspace geo.

<Note>
  **Claude Platform on AWS:** Workspace geo tidak dapat dikonfigurasi. Workspace disediakan melalui AWS Console, dan halaman Workspaces di Claude Console bersifat read-only. Sesi Claude Managed Agents pada platform ini berjalan dengan Workspace geo efektif `"us"`, yang saat ini merupakan satu-satunya workspace geo yang tersedia. Lihat [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws) untuk pertimbangan residensi data yang spesifik untuk platform tersebut.
</Note>

## Harga

Harga residensi data bervariasi berdasarkan generasi model:

* **Claude Opus 4.6, Claude Sonnet 4.6, dan yang lebih baru:** Inferensi khusus AS (`inference_geo: "us"`) dikenakan harga 1,1x dari tarif standar di semua kategori harga token (token input, token output, penulisan cache, dan pembacaan cache).
* **Routing global** (`inference_geo: "global"`): Harga standar berlaku.
* **Model lama:** Tidak mendukung `inference_geo` (lihat [Ketersediaan model](#model-availability)); harga standar berlaku. Permintaan yang menyertakan parameter ini akan mengembalikan error 400.

Harga ini berlaku untuk Claude API (first-party) dan Claude Platform on AWS. Di Claude in Microsoft Foundry, pengali 1,1x yang sama berlaku untuk deployment yang di-host di Azure yang menggunakan tipe deployment US Data Zone Standard. Platform yang dioperasikan mitra (Bedrock dan Google Cloud) memiliki harga regional mereka sendiri. Lihat [Harga residensi data](/docs/id/about-claude/pricing#data-residency-pricing) untuk detailnya.

<Note>
  Jika Anda memiliki komitmen [Priority Tier](/docs/id/api/service-tiers), pengali 1,1x untuk inferensi khusus AS juga memengaruhi cara token dihitung terhadap kapasitas Priority Tier Anda. Setiap token yang dikonsumsi dengan `inference_geo: "us"` mengurangi 1,1 token dari TPM yang telah Anda komitmenkan, konsisten dengan cara pengali harga lainnya (seperti caching prompt) memengaruhi tingkat burndown.
</Note>

## Dukungan Batch API

Parameter `inference_geo` didukung pada [Batch API](/docs/id/build-with-claude/batch-processing). Setiap permintaan dalam batch dapat menentukan nilai `inference_geo`-nya sendiri.

## Migrasi dari opt-out lama

Jika organisasi Anda sebelumnya memilih keluar (opt-out) dari routing global untuk menjaga inferensi tetap di AS, workspace Anda telah dikonfigurasi secara otomatis dengan `allowed_inference_geos: ["us"]` dan `default_inference_geo: "us"`. Tidak diperlukan perubahan kode. Persyaratan residensi data Anda yang ada terus diberlakukan melalui kontrol geo yang baru.

### Apa yang berubah

Opt-out lama adalah pengaturan tingkat organisasi yang membatasi semua permintaan ke infrastruktur berbasis AS. Kontrol residensi data yang baru menggantikan ini dengan dua mekanisme:

* **Kontrol per permintaan:** Parameter `inference_geo` memungkinkan Anda menentukan `"us"` atau `"global"` pada setiap panggilan API, memberikan Anda fleksibilitas tingkat permintaan.
* **Kontrol workspace:** Pengaturan `default_inference_geo` dan `allowed_inference_geos` di Console memungkinkan Anda menerapkan kebijakan geo di semua kunci dalam workspace.

### Apa yang terjadi pada workspace Anda

Workspace Anda dimigrasikan secara otomatis:

| Pengaturan lama                   | Padanan baru                                                    |
| --------------------------------- | --------------------------------------------------------------- |
| Opt-out routing global (hanya AS) | `allowed_inference_geos: ["us"]`, `default_inference_geo: "us"` |

Semua permintaan API yang menggunakan kunci dari workspace Anda terus berjalan di infrastruktur berbasis AS. Tidak ada tindakan yang diperlukan untuk mempertahankan perilaku Anda saat ini.

### Jika Anda ingin menggunakan routing global

Jika persyaratan residensi data Anda telah berubah dan Anda ingin memanfaatkan routing global untuk performa dan ketersediaan yang lebih baik, perbarui pengaturan inference geo workspace Anda untuk menyertakan `"global"` dalam geo yang diizinkan dan tetapkan `default_inference_geo` ke `"global"`. Lihat [Pembatasan tingkat workspace](#workspace-level-restrictions) untuk detailnya.

### Dampak harga

Model lama tidak terpengaruh oleh migrasi ini. Untuk harga terkini pada model yang lebih baru, lihat [Harga](#pricing).

## Keterbatasan saat ini

* **Batas laju bersama:** Batas laju dibagi di semua geo.
* **Inference geo:** Hanya `"us"` dan `"global"` yang tersedia.
* **Workspace geo:** Hanya `"us"` yang saat ini tersedia. Workspace geo tidak dapat diubah setelah workspace dibuat.

## Langkah selanjutnya

<CardGroup>
  <Card title="Harga" icon="dollar-sign" href="/docs/id/about-claude/pricing#data-residency-pricing">
    Lihat detail harga residensi data.
  </Card>

  <Card title="Workspace" icon="building" href="/docs/id/manage-claude/workspaces">
    Pelajari tentang konfigurasi workspace.
  </Card>

  <Card title="Usage and Cost API" icon="chart" href="/docs/id/manage-claude/usage-cost-api">
    Lacak penggunaan dan biaya berdasarkan residensi data.
  </Card>
</CardGroup>
