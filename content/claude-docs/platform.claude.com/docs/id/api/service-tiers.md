---
source: platform
url: https://platform.claude.com/docs/id/api/service-tiers
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 76730349bf01e9518d7247ea38f1003c282f89b2d6de2d99fda76bddfcef691d
---

# Tingkatan layanan

Berbagai tingkatan layanan memungkinkan Anda menyeimbangkan ketersediaan, performa, dan biaya yang dapat diprediksi berdasarkan kebutuhan aplikasi Anda.

---

Anthropic menawarkan tiga tingkatan layanan:
- **Priority Tier:** Terbaik untuk alur kerja yang diterapkan dalam produksi di mana waktu, ketersediaan, dan harga yang dapat diprediksi sangat penting
- **Standard:** Tingkatan default untuk percontohan maupun penskalaan kasus penggunaan sehari-hari
- **Batch:** Terbaik untuk alur kerja asinkron yang dapat menunggu atau mendapat manfaat dari berada di luar kapasitas normal Anda

## Tingkatan Standard

Tingkatan standard adalah tingkatan layanan default untuk semua permintaan API. API memprioritaskan permintaan ini bersama semua permintaan lainnya dengan ketersediaan terbaik yang memungkinkan.

## Priority Tier

API memprioritaskan permintaan dalam tingkatan ini di atas semua permintaan lainnya. Prioritisasi ini membantu meminimalkan [kesalahan "server overloaded"](/docs/id/api/errors#http-errors), bahkan selama waktu puncak.

Untuk informasi lebih lanjut, lihat [Mulai menggunakan Priority Tier](#get-started-with-priority-tier)

## Cara permintaan mendapatkan tingkatan

Saat menangani permintaan, Anthropic memutuskan untuk menetapkan permintaan ke Priority Tier dalam skenario berikut:
- Organisasi Anda memiliki kapasitas priority tier yang cukup untuk token **input** per menit
- Organisasi Anda memiliki kapasitas priority tier yang cukup untuk token **output** per menit

Anthropic menghitung penggunaan terhadap kapasitas Priority Tier sebagai berikut:

**Token Input**
- Pembacaan cache dihitung sebagai 0,1 token per token yang dibaca dari cache
- Penulisan cache dihitung sebagai 1,25 token per token yang ditulis ke cache dengan TTL 5 menit
- Penulisan cache dihitung sebagai 2,00 token per token yang ditulis ke cache dengan TTL 1 jam
- Untuk permintaan [inferensi khusus AS](/docs/id/build-with-claude/data-residency) (`inference_geo: "us"`) pada Claude Opus 4.6 dan model yang lebih baru, token input dihitung sebagai 1,1 token per token
- Semua token input lainnya dihitung sebagai 1 token per token

**Token Output**
- Untuk permintaan [inferensi khusus AS](/docs/id/build-with-claude/data-residency) (`inference_geo: "us"`) pada Claude Opus 4.6 dan model yang lebih baru, token output dihitung sebagai 1,1 token per token
- Semua token output lainnya dihitung sebagai 1 token per token

Jika tidak, permintaan akan diproses pada tingkatan standard.

<Note>
Tingkat burndown ini mencerminkan harga relatif dari setiap jenis token. Misalnya, inferensi khusus AS dihargai 1,1x pada Opus 4.6 dan model yang lebih baru, sehingga setiap token yang dikonsumsi dengan `inference_geo: "us"` akan mengurangi 1,1 token dari kapasitas Priority Tier Anda.
</Note>

<Note>
Permintaan yang ditetapkan ke Priority Tier akan menarik dari kapasitas Priority Tier maupun batas tarif reguler.
Jika melayani permintaan tersebut akan melebihi batas tarif, permintaan akan ditolak.
</Note>

## Menggunakan tingkatan layanan

Anda dapat mengontrol tingkatan layanan mana yang dapat digunakan untuk suatu permintaan dengan mengatur parameter `service_tier`:

```python Python
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}],
    service_tier="auto",  # Secara otomatis menggunakan Priority Tier jika tersedia, fallback ke standard
)
```

Parameter `service_tier` menerima nilai-nilai berikut:

- `"auto"` (default) - Menggunakan kapasitas Priority Tier jika tersedia, beralih ke kapasitas lainnya jika tidak tersedia
- `"standard_only"` - Hanya menggunakan kapasitas tingkatan standard, berguna jika Anda tidak ingin menggunakan kapasitas Priority Tier Anda

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

Saat meminta `service_tier="auto"` dengan model yang memiliki komitmen Priority Tier, header respons berikut memberikan wawasan:
```text
anthropic-priority-input-tokens-limit: 10000
anthropic-priority-input-tokens-remaining: 9618
anthropic-priority-input-tokens-reset: 2025-01-12T23:11:59Z
anthropic-priority-output-tokens-limit: 10000
anthropic-priority-output-tokens-remaining: 6000
anthropic-priority-output-tokens-reset: 2025-01-12T23:12:21Z
```
Anda dapat menggunakan keberadaan header ini untuk mendeteksi apakah permintaan Anda memenuhi syarat untuk Priority Tier, meskipun melebihi batas.

## Mulai menggunakan Priority Tier

Anda mungkin ingin berkomitmen pada kapasitas Priority Tier jika Anda tertarik dengan:
- **Ketersediaan lebih tinggi**: Target uptime 99,5% dengan sumber daya komputasi yang diprioritaskan
- **Kontrol Biaya**: Pengeluaran yang dapat diprediksi dan diskon untuk komitmen jangka panjang
- **Overflow fleksibel**: Secara otomatis beralih ke tingkatan standard ketika Anda melebihi kapasitas yang dikomitmenkan

Berkomitmen pada Priority Tier akan melibatkan keputusan:
- Jumlah token input per menit
- Jumlah token output per menit
- Durasi komitmen (1, 3, 6, atau 12 bulan)
- Versi model tertentu

<Note>
Rasio token input terhadap output yang Anda beli sangat penting. Menyesuaikan kapasitas Priority Tier Anda dengan pola lalu lintas aktual membantu Anda memaksimalkan penggunaan token yang telah dibeli.
</Note>

### Model yang didukung

Priority Tier didukung pada semua model Claude yang tersedia kecuali [Claude Mythos Preview](https://anthropic.com/glasswing).

Periksa [halaman ikhtisar model](/docs/id/about-claude/models/overview) untuk detail lebih lanjut tentang model yang tersedia.

### Cara mengakses Priority Tier

Untuk mulai menggunakan Priority Tier:

1. [Hubungi tim penjualan](https://claude.com/contact-sales/priority-tier) untuk menyelesaikan penyediaan
2. (Opsional) Perbarui permintaan API Anda untuk secara opsional mengatur parameter `service_tier` ke `auto`
3. Pantau penggunaan Anda melalui header respons dan Claude Console