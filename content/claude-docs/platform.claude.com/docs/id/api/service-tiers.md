---
source: platform
url: https://platform.claude.com/docs/id/api/service-tiers
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 77b982fb6f6ecc7d49d972f23d7874e8bd950922221247cc0cb8879ba8813342
---

# Tingkat layanan

Tingkat layanan yang berbeda memungkinkan Anda menyeimbangkan ketersediaan, kinerja, dan biaya yang dapat diprediksi berdasarkan kebutuhan aplikasi Anda.

---

Anthropic menawarkan tiga tingkat layanan:
- **Priority Tier:** Terbaik untuk alur kerja yang diterapkan dalam produksi di mana waktu, ketersediaan, dan harga yang dapat diprediksi penting
- **Standard:** Tingkat default untuk pemilihan dan penskalaan kasus penggunaan sehari-hari
- **Batch:** Terbaik untuk alur kerja asinkron yang dapat menunggu atau mendapat manfaat dari berada di luar kapasitas normal Anda

## Standard Tier

Tingkat standard adalah tingkat layanan default untuk semua permintaan API. API memprioritaskan permintaan ini bersama semua permintaan lain dengan ketersediaan upaya terbaik.

## Priority Tier

API memprioritaskan permintaan di tingkat ini di atas semua permintaan lain. Prioritisasi ini membantu meminimalkan [kesalahan "server overloaded"](/docs/id/api/errors#http-errors), bahkan selama waktu puncak.

Untuk informasi lebih lanjut, lihat [Mulai dengan Priority Tier](#get-started-with-priority-tier)

## Bagaimana permintaan mendapatkan tingkat yang ditugaskan

Saat menangani permintaan, Anthropic memutuskan untuk menugaskan permintaan ke Priority Tier dalam skenario berikut:
- Organisasi Anda memiliki kapasitas priority tier yang cukup **input** token per menit
- Organisasi Anda memiliki kapasitas priority tier yang cukup **output** token per menit

Anthropic menghitung penggunaan terhadap kapasitas Priority Tier sebagai berikut:

**Input Tokens**
- Cache reads sebagai 0,1 token per token yang dibaca dari cache
- Cache writes sebagai 1,25 token per token yang ditulis ke cache dengan TTL 5 menit
- Cache writes sebagai 2,00 token per token yang ditulis ke cache dengan TTL 1 jam
- Untuk permintaan [US-only inference](/docs/id/build-with-claude/data-residency) (`inference_geo: "us"`) pada Claude Opus 4.7, Claude Opus 4.6, dan model yang lebih baru, input token adalah 1,1 token per token
- Semua input token lainnya adalah 1 token per token

**Output Tokens**
- Untuk permintaan [US-only inference](/docs/id/build-with-claude/data-residency) (`inference_geo: "us"`) pada Claude Opus 4.7, Claude Opus 4.6, dan model yang lebih baru, output token adalah 1,1 token per token
- Semua output token lainnya adalah 1 token per token

Jika tidak, permintaan dilanjutkan di tingkat standard.

<Note>
Tingkat burndown ini mencerminkan harga relatif dari setiap jenis token. Misalnya, US-only inference dihargai pada 1,1x pada Opus 4.7, Opus 4.6, dan model yang lebih baru, jadi setiap token yang dikonsumsi dengan `inference_geo: "us"` mengurangi 1,1 token dari kapasitas Priority Tier Anda.
</Note>

<Note>
Permintaan yang ditugaskan Priority Tier ditarik dari kapasitas Priority Tier dan batas laju reguler.
Jika melayani permintaan akan melampaui batas laju, permintaan ditolak.
</Note>

## Menggunakan tingkat layanan

Anda dapat mengontrol tingkat layanan mana yang dapat digunakan untuk permintaan dengan menetapkan parameter `service_tier`:

```python Python
message = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}],
    service_tier="auto",  # Automatically use Priority Tier when available, fallback to standard
)
```

Parameter `service_tier` menerima nilai berikut:

- `"auto"` (default) - Menggunakan kapasitas Priority Tier jika tersedia, kembali ke kapasitas lain Anda jika tidak
- `"standard_only"` - Hanya gunakan kapasitas tingkat standard, berguna jika Anda tidak ingin menggunakan kapasitas Priority Tier Anda

Objek `usage` respons juga mencakup tingkat layanan yang ditugaskan ke permintaan:

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
Ini memungkinkan Anda menentukan tingkat layanan mana yang ditugaskan ke permintaan.

Saat meminta `service_tier="auto"` dengan model yang memiliki komitmen Priority Tier, header respons ini memberikan wawasan:
```text
anthropic-priority-input-tokens-limit: 10000
anthropic-priority-input-tokens-remaining: 9618
anthropic-priority-input-tokens-reset: 2025-01-12T23:11:59Z
anthropic-priority-output-tokens-limit: 10000
anthropic-priority-output-tokens-remaining: 6000
anthropic-priority-output-tokens-reset: 2025-01-12T23:12:21Z
```
Anda dapat menggunakan kehadiran header ini untuk mendeteksi apakah permintaan Anda memenuhi syarat untuk Priority Tier, bahkan jika melampaui batas.

## Mulai dengan Priority Tier

Anda mungkin ingin berkomitmen pada kapasitas Priority Tier jika Anda tertarik pada:
- **Ketersediaan lebih tinggi**: Target uptime 99,5% dengan sumber daya komputasi yang diprioritaskan
- **Kontrol Biaya**: Pengeluaran yang dapat diprediksi dan diskon untuk komitmen yang lebih lama
- **Overflow Fleksibel**: Secara otomatis kembali ke tingkat standard ketika Anda melampaui kapasitas komitmen Anda

Berkomitmen pada Priority Tier akan melibatkan pengambilan keputusan:
- Sejumlah input token per menit
- Sejumlah output token per menit
- Durasi komitmen (1, 3, 6, atau 12 bulan)
- Versi model tertentu

<Note>
Rasio input ke output token yang Anda beli penting. Mengukur kapasitas Priority Tier Anda agar selaras dengan pola lalu lintas aktual Anda membantu Anda memaksimalkan pemanfaatan token yang dibeli.
</Note>

### Model yang didukung

Priority Tier didukung pada semua model Claude yang tersedia (termasuk Claude Opus 4.7) kecuali [Claude Mythos Preview](https://anthropic.com/glasswing).

Periksa [halaman ringkasan model](/docs/id/about-claude/models/overview) untuk detail lebih lanjut tentang model yang tersedia.

### Cara mengakses Priority Tier

Untuk mulai menggunakan Priority Tier:

1. [Hubungi penjualan](https://claude.com/contact-sales/priority-tier) untuk menyelesaikan penyediaan
2. (Opsional) Perbarui permintaan API Anda untuk secara opsional menetapkan parameter `service_tier` ke `auto`
3. Pantau penggunaan Anda melalui header respons dan Claude Console