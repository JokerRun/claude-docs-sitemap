---
source: platform
url: https://platform.claude.com/docs/id/api/service-tiers
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 4b2d146b762b09c18efb0be1b312344678c6bf1d066bca2b434456c516334225
---

# Tingkatan layanan

Tingkatan layanan yang berbeda memungkinkan Anda menyeimbangkan ketersediaan, performa, dan biaya yang dapat diprediksi berdasarkan kebutuhan aplikasi Anda.

---

<Warning>
  Komitmen kapasitas Priority Tier tidak lagi tersedia untuk dibeli. Organisasi dengan komitmen yang sudah ada dapat terus menggunakan Priority Tier hingga tanggal berakhirnya kontrak mereka, dan halaman ini tetap tersedia sebagai referensi bagi mereka. Jika Anda membutuhkan kapasitas yang terjamin, [hubungi tim penjualan](https://claude.com/contact-sales).
</Warning>

Anthropic menawarkan tiga tingkatan layanan:

* **Priority Tier:** Hanya tersedia untuk organisasi dengan komitmen kapasitas yang sudah ada
* **Standard:** Tingkatan default untuk uji coba maupun penskalaan kasus penggunaan sehari-hari
* **Batch:** Paling cocok untuk alur kerja asinkron yang dapat menunggu atau mendapat manfaat karena berada di luar kapasitas normal Anda

## Standard Tier

Standard tier adalah tingkatan layanan default untuk semua permintaan API. API memprioritaskan permintaan ini bersama dengan semua permintaan lainnya dengan ketersediaan upaya terbaik (best-effort).

## Priority Tier

API memprioritaskan permintaan dalam tingkatan ini di atas semua permintaan lainnya. Prioritas ini membantu meminimalkan [error "server overloaded"](/docs/id/api/errors#http-errors), bahkan pada waktu puncak.

Untuk informasi lebih lanjut, lihat [Komitmen Priority Tier yang sudah ada](#existing-priority-tier-commitments).

## Bagaimana permintaan ditetapkan ke tingkatan

Saat menangani permintaan, Anthropic memutuskan untuk menetapkan permintaan ke Priority Tier dalam skenario berikut:

* Organisasi Anda memiliki kapasitas priority tier yang cukup untuk token **input** per menit
* Organisasi Anda memiliki kapasitas priority tier yang cukup untuk token **output** per menit

Anthropic menghitung penggunaan terhadap kapasitas Priority Tier sebagai berikut:

**Token Input**

* Pembacaan cache dihitung sebagai 0,1 token per token yang dibaca dari cache
* Penulisan cache dihitung sebagai 1,25 token per token yang ditulis ke cache dengan TTL 5 menit
* Penulisan cache dihitung sebagai 2,00 token per token yang ditulis ke cache dengan TTL 1 jam
* Untuk permintaan [inferensi khusus AS](/docs/id/manage-claude/data-residency) (`inference_geo: "us"`) pada Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih baru, token input dihitung sebagai 1,1 token per token
* Semua token input lainnya dihitung sebagai 1 token per token

**Token Output**

* Untuk permintaan [inferensi khusus AS](/docs/id/manage-claude/data-residency) (`inference_geo: "us"`) pada Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih baru, token output dihitung sebagai 1,1 token per token
* Semua token output lainnya dihitung sebagai 1 token per token

Jika tidak, permintaan akan diproses pada standard tier.

<Note>
  Tarif pengurangan (burndown rate) ini mencerminkan harga relatif dari setiap jenis token. Misalnya, inferensi khusus AS dihargai 1,1x pada Opus 4.6, Sonnet 4.6, dan model yang lebih baru, sehingga setiap token yang dikonsumsi dengan `inference_geo: "us"` mengurangi 1,1 token dari kapasitas Priority Tier Anda.
</Note>

<Note>
  Permintaan yang ditetapkan ke Priority Tier mengambil dari kapasitas Priority Tier sekaligus dari batas laju reguler. Jika melayani permintaan tersebut akan melebihi batas laju, permintaan akan ditolak.
</Note>

## Menggunakan tingkatan layanan

Anda dapat mengontrol tingkatan layanan mana yang dapat digunakan untuk sebuah permintaan dengan mengatur parameter `service_tier`:

```python Python
message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}],
    service_tier="auto",  # Automatically use Priority Tier when available, fallback to standard
)
print(message.usage.service_tier)
```

Parameter `service_tier` menerima nilai-nilai berikut:

* `"auto"` (default) - Menggunakan kapasitas Priority Tier jika tersedia, beralih ke kapasitas Anda yang lain jika tidak
* `"standard_only"` - Hanya menggunakan kapasitas standard tier, berguna jika Anda tidak ingin menggunakan kapasitas Priority Tier Anda

Objek `usage` dalam respons juga menyertakan tingkatan layanan yang ditetapkan untuk permintaan tersebut:

```json
{
  "usage": {
    "input_tokens": 410,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 585,
    "service_tier": "priority"
  }
}
```

Ini memungkinkan Anda menentukan tingkatan layanan mana yang ditetapkan untuk permintaan tersebut.

Saat meminta `service_tier="auto"` dengan model yang memiliki komitmen Priority Tier, header respons berikut memberikan informasi:

```text wrap
anthropic-priority-input-tokens-limit: 10000
anthropic-priority-input-tokens-remaining: 9618
anthropic-priority-input-tokens-reset: 2025-01-12T23:11:59Z
anthropic-priority-output-tokens-limit: 10000
anthropic-priority-output-tokens-remaining: 6000
anthropic-priority-output-tokens-reset: 2025-01-12T23:12:21Z
```

Anda dapat menggunakan keberadaan header ini untuk mendeteksi apakah permintaan Anda memenuhi syarat untuk Priority Tier, bahkan jika permintaan tersebut melebihi batas.

## Komitmen Priority Tier yang sudah ada

Komitmen Priority Tier terdiri dari:

* Sejumlah token input per menit
* Sejumlah token output per menit
* Durasi komitmen (1, 3, 6, atau 12 bulan)
* Versi model tertentu

Priority Tier menargetkan uptime 99,5% dengan sumber daya komputasi yang diprioritaskan. Permintaan yang melebihi kapasitas komitmen Anda secara otomatis beralih ke standard tier.

### Model yang didukung

Priority Tier didukung pada semua model Claude yang tersedia (termasuk Claude Fable 5 dan Claude Opus 4.8) kecuali Claude Sonnet 5, [Claude Mythos Preview](https://anthropic.com/glasswing), dan Claude Mythos 5.

Lihat [Ikhtisar model](/docs/id/about-claude/models/overview) untuk detail lebih lanjut tentang model yang tersedia.
