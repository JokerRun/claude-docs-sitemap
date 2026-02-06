---
source: platform
url: https://platform.claude.com/docs/id/api/service-tiers
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: cd83fc98fd00ede4bad9a7ce8616597241825d575a9cb91434ffa5212b392917
---

# Tingkat layanan

Tingkat layanan yang berbeda memungkinkan Anda menyeimbangkan ketersediaan, kinerja, dan biaya yang dapat diprediksi berdasarkan kebutuhan aplikasi Anda.

---

Kami menawarkan tiga tingkat layanan:
- **Tingkat Prioritas:** Terbaik untuk alur kerja yang diterapkan dalam produksi di mana waktu, ketersediaan, dan penetapan harga yang dapat diprediksi penting
- **Standar:** Tingkat default untuk pemilihan dan penskalaan kasus penggunaan sehari-hari
- **Batch:** Terbaik untuk alur kerja asinkron yang dapat menunggu atau mendapat manfaat dari berada di luar kapasitas normal Anda

## Tingkat Standar

Tingkat standar adalah tingkat layanan default untuk semua permintaan API. Permintaan dalam tingkat ini diprioritaskan bersama semua permintaan lainnya dan mengamati ketersediaan upaya terbaik.

## Tingkat Prioritas

Permintaan dalam tingkat ini diprioritaskan di atas semua permintaan lainnya ke Anthropic. Prioritisasi ini membantu meminimalkan ["server overloaded" errors](/docs/id/api/errors#http-errors), bahkan selama waktu puncak.

Untuk informasi lebih lanjut, lihat [Mulai dengan Tingkat Prioritas](#get-started-with-priority-tier)

## Bagaimana permintaan mendapatkan tingkat yang ditugaskan

Saat menangani permintaan, Anthropic memutuskan untuk menugaskan permintaan ke Tingkat Prioritas dalam skenario berikut:
- Organisasi Anda memiliki kapasitas tingkat prioritas **input** token per menit yang cukup
- Organisasi Anda memiliki kapasitas tingkat prioritas **output** token per menit yang cukup

Anthropic menghitung penggunaan terhadap kapasitas Tingkat Prioritas sebagai berikut:

**Token Input**
- Cache reads sebagai 0,1 token per token yang dibaca dari cache
- Cache writes sebagai 1,25 token per token yang ditulis ke cache dengan TTL 5 menit
- Cache writes sebagai 2,00 token per token yang ditulis ke cache dengan TTL 1 jam
- Untuk permintaan [long-context](/docs/id/build-with-claude/context-windows) (>200k token input), token input adalah 2 token per token
- Untuk permintaan [US-only inference](/docs/id/build-with-claude/data-residency) (`inference_geo: "us"`), token input adalah 1,1 token per token
- Semua token input lainnya adalah 1 token per token

**Token Output**
- Untuk permintaan [long-context](/docs/id/build-with-claude/context-windows) (>200k token input), token output adalah 1,5 token per token
- Untuk permintaan [US-only inference](/docs/id/build-with-claude/data-residency) (`inference_geo: "us"`), token output adalah 1,1 token per token
- Semua token output lainnya adalah 1 token per token

Jika tidak, permintaan dilanjutkan pada tingkat standar.

<Note>
Tingkat pembakaran ini mencerminkan penetapan harga relatif dari setiap jenis token. Misalnya, inferensi hanya AS dihargai pada 1,1x, jadi setiap token yang dikonsumsi dengan `inference_geo: "us"` mengurangi 1,1 token dari kapasitas Tingkat Prioritas Anda. Pengganda bertumpuk — permintaan long-context dengan inferensi hanya AS mengurangi token input pada 2,2 token per token (2 × 1,1).
</Note>

<Note>
Permintaan yang ditugaskan Tingkat Prioritas ditarik dari kapasitas Tingkat Prioritas dan batas laju reguler.
Jika melayani permintaan akan melampaui batas laju, permintaan ditolak.
</Note>

## Menggunakan tingkat layanan

Anda dapat mengontrol tingkat layanan mana yang dapat digunakan untuk permintaan dengan menetapkan parameter `service_tier`:

```python
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}],
    service_tier="auto"  # Automatically use Priority Tier when available, fallback to standard
)
```

Parameter `service_tier` menerima nilai berikut:

- `"auto"` (default) - Menggunakan kapasitas Tingkat Prioritas jika tersedia, kembali ke kapasitas lain Anda jika tidak
- `"standard_only"` - Hanya gunakan kapasitas tingkat standar, berguna jika Anda tidak ingin menggunakan kapasitas Tingkat Prioritas Anda

Objek `usage` respons juga mencakup tingkat layanan yang ditugaskan untuk permintaan:

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
Ini memungkinkan Anda menentukan tingkat layanan mana yang ditugaskan untuk permintaan.

Saat meminta `service_tier="auto"` dengan model dengan komitmen Tingkat Prioritas, header respons ini memberikan wawasan:
```
anthropic-priority-input-tokens-limit: 10000
anthropic-priority-input-tokens-remaining: 9618
anthropic-priority-input-tokens-reset: 2025-01-12T23:11:59Z
anthropic-priority-output-tokens-limit: 10000
anthropic-priority-output-tokens-remaining: 6000
anthropic-priority-output-tokens-reset: 2025-01-12T23:12:21Z
```
Anda dapat menggunakan kehadiran header ini untuk mendeteksi apakah permintaan Anda memenuhi syarat untuk Tingkat Prioritas, bahkan jika melebihi batas.

## Mulai dengan Tingkat Prioritas

Anda mungkin ingin berkomitmen pada kapasitas Tingkat Prioritas jika Anda tertarik pada:
- **Ketersediaan lebih tinggi**: Target uptime 99,5% dengan sumber daya komputasi yang diprioritaskan
- **Kontrol Biaya**: Pengeluaran yang dapat diprediksi dan diskon untuk komitmen yang lebih lama
- **Overflow fleksibel**: Secara otomatis kembali ke tingkat standar ketika Anda melampaui kapasitas yang berkomitmen

Berkomitmen pada Tingkat Prioritas akan melibatkan pengambilan keputusan:
- Sejumlah token input per menit
- Sejumlah token output per menit
- Durasi komitmen (1, 3, 6, atau 12 bulan)
- Versi model tertentu

<Note>
Rasio token input ke output yang Anda beli penting. Mengukur kapasitas Tingkat Prioritas Anda agar sesuai dengan pola lalu lintas aktual Anda membantu Anda memaksimalkan pemanfaatan token yang dibeli.
</Note>

### Model yang didukung

Tingkat Prioritas didukung oleh:

- Claude Opus 4.6
- Claude Opus 4.5
- Claude Opus 4.1
- Claude Opus 4
- Claude Sonnet 4.5
- Claude Sonnet 4
- Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations))
- Claude Haiku 4.5
- Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations))

Periksa [halaman gambaran umum model](/docs/id/about-claude/models/overview) untuk detail lebih lanjut tentang model kami.

### Cara mengakses Tingkat Prioritas

Untuk mulai menggunakan Tingkat Prioritas:

1. [Hubungi penjualan](https://claude.com/contact-sales/priority-tier) untuk menyelesaikan penyediaan
2. (Opsional) Perbarui permintaan API Anda untuk secara opsional menetapkan parameter `service_tier` ke `auto`
3. Pantau penggunaan Anda melalui header respons dan Konsol Claude