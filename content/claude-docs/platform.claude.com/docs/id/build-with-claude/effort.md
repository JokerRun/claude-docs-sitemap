---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/effort
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: c642ba5c99141217666f3b4eac583df790bf130f205881cf81855d050539042a
---

# Effort

Kontrol berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menukar antara kelengkapan respons dan efisiensi token.

---

Parameter effort memungkinkan Anda mengontrol seberapa bersemangat Claude dalam menghabiskan token saat merespons permintaan. Ini memberi Anda kemampuan untuk menukar antara kelengkapan respons dan efisiensi token, semuanya dengan satu model. Parameter effort secara umum tersedia di semua model yang didukung tanpa memerlukan header beta.

<Note>
  Parameter effort didukung oleh Claude Opus 4.6 dan Claude Opus 4.5.
</Note>

<Tip>
Untuk Claude Opus 4.6, effort menggantikan `budget_tokens` sebagai cara yang direkomendasikan untuk mengontrol kedalaman pemikiran. Gabungkan effort dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) untuk pengalaman terbaik. Meskipun `budget_tokens` masih diterima di Opus 4.6, ini sudah usang dan akan dihapus dalam rilis model di masa depan. Pada effort `high` (default) dan `max`, Claude hampir selalu akan berpikir. Pada tingkat effort yang lebih rendah, mungkin akan melewati pemikiran untuk masalah yang lebih sederhana.
</Tip>

## Cara kerja effort

Secara default, Claude menggunakan high effort—menghabiskan sebanyak token yang diperlukan untuk hasil yang sangat baik. Anda dapat menaikkan tingkat effort ke `max` untuk kemampuan tertinggi absolut, atau menurunkannya untuk lebih konservatif dengan penggunaan token, mengoptimalkan kecepatan dan biaya sambil menerima beberapa pengurangan dalam kemampuan.

<Tip>
Mengatur `effort` ke `"high"` menghasilkan perilaku yang persis sama dengan menghilangkan parameter `effort` sepenuhnya.
</Tip>

Parameter effort mempengaruhi **semua token** dalam respons, termasuk:

- Respons teks dan penjelasan
- Panggilan alat dan argumen fungsi
- Pemikiran yang diperluas (ketika diaktifkan)

Pendekatan ini memiliki dua keuntungan utama:

1. Tidak memerlukan pemikiran untuk diaktifkan agar dapat menggunakannya.
2. Dapat mempengaruhi semua pengeluaran token termasuk panggilan alat. Misalnya, effort yang lebih rendah berarti Claude membuat lebih sedikit panggilan alat. Ini memberikan tingkat kontrol yang jauh lebih besar atas efisiensi.

### Tingkat effort

| Level    | Deskripsi                                                                                                                      | Kasus penggunaan umum                                                                      |
| -------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `max`    | Kemampuan maksimum absolut tanpa batasan pada pengeluaran token. Hanya Opus 4.6 — permintaan menggunakan `max` pada model lain akan mengembalikan kesalahan. | Tugas yang memerlukan penalaran paling mendalam dan analisis paling menyeluruh |
| `high`   | Kemampuan tinggi. Setara dengan tidak mengatur parameter. | Penalaran kompleks, masalah coding yang sulit, tugas agentic                           |
| `medium` | Pendekatan seimbang dengan penghematan token moderat. | Tugas agentic yang memerlukan keseimbangan kecepatan, biaya, dan kinerja                                                         |
| `low`    | Paling efisien. Penghematan token signifikan dengan beberapa pengurangan kemampuan. | Tugas yang lebih sederhana yang membutuhkan kecepatan terbaik dan biaya terendah, seperti subagents                     |

<Note>
Effort adalah sinyal perilaku, bukan anggaran token yang ketat. Pada tingkat effort yang lebih rendah, Claude masih akan berpikir pada masalah yang cukup sulit — hanya akan berpikir lebih sedikit daripada yang akan dilakukan pada tingkat effort yang lebih tinggi untuk masalah yang sama.
</Note>

## Penggunaan dasar

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": "Analyze the trade-offs between microservices and monolithic architectures"
    }],
    output_config={
        "effort": "medium"
    }
)

print(response.content[0].text)
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages: [{
    role: "user",
    content: "Analyze the trade-offs between microservices and monolithic architectures"
  }],
  output_config: {
    effort: "medium"
  }
});

console.log(response.content[0].text);
```

```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "messages": [{
            "role": "user",
            "content": "Analyze the trade-offs between microservices and monolithic architectures"
        }],
        "output_config": {
            "effort": "medium"
        }
    }'
```

</CodeGroup>

## Kapan saya harus menyesuaikan parameter effort?

- Gunakan **max effort** ketika Anda membutuhkan kemampuan tertinggi absolut tanpa batasan—penalaran paling menyeluruh dan analisis paling mendalam. Hanya tersedia di Opus 4.6; permintaan menggunakan `max` pada model lain akan mengembalikan kesalahan.
- Gunakan **high effort** (default) ketika Anda membutuhkan pekerjaan terbaik Claude—penalaran kompleks, analisis bernuansa, masalah coding yang sulit, atau tugas apa pun di mana kualitas adalah prioritas utama.
- Gunakan **medium effort** sebagai opsi seimbang ketika Anda menginginkan kinerja solid tanpa pengeluaran token penuh dari high effort.
- Gunakan **low effort** ketika Anda mengoptimalkan untuk kecepatan (karena Claude menjawab dengan lebih sedikit token) atau biaya—misalnya, tugas klasifikasi sederhana, pencarian cepat, atau kasus penggunaan volume tinggi di mana peningkatan kualitas marginal tidak membenarkan latensi atau pengeluaran tambahan.

## Effort dengan penggunaan alat

Saat menggunakan alat, parameter effort mempengaruhi penjelasan di sekitar panggilan alat dan panggilan alat itu sendiri. Tingkat effort yang lebih rendah cenderung:

- Menggabungkan beberapa operasi menjadi lebih sedikit panggilan alat
- Membuat lebih sedikit panggilan alat
- Melanjutkan langsung ke tindakan tanpa pembukaan
- Menggunakan pesan konfirmasi yang ringkas setelah penyelesaian

Tingkat effort yang lebih tinggi mungkin:

- Membuat lebih banyak panggilan alat
- Menjelaskan rencana sebelum mengambil tindakan
- Memberikan ringkasan perubahan yang terperinci
- Menyertakan komentar kode yang lebih komprehensif

## Effort dengan pemikiran yang diperluas

Parameter effort bekerja bersama pemikiran yang diperluas. Perilakunya tergantung pada model:

- **Claude Opus 4.6** menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Meskipun `budget_tokens` masih diterima di Opus 4.6, ini sudah usang dan akan dihapus dalam rilis di masa depan. Pada effort `high` dan `max`, Claude hampir selalu berpikir secara mendalam. Pada tingkat yang lebih rendah, mungkin akan melewati pemikiran untuk masalah yang lebih sederhana.
- **Claude Opus 4.5** menggunakan pemikiran manual (`thinking: {type: "enabled", budget_tokens: N}`), di mana effort bekerja bersama anggaran token pemikiran. Atur tingkat effort untuk tugas Anda, kemudian atur anggaran token pemikiran berdasarkan kompleksitas tugas.

Parameter effort dapat digunakan dengan atau tanpa pemikiran yang diperluas diaktifkan. Ketika digunakan tanpa pemikiran, itu masih mengontrol pengeluaran token keseluruhan untuk respons teks dan panggilan alat.

## Praktik terbaik

1. **Mulai dengan high**: Gunakan tingkat effort yang lebih rendah untuk menukar kinerja dengan efisiensi token.
2. **Gunakan low untuk tugas yang sensitif terhadap kecepatan atau sederhana**: Ketika latensi penting atau tugas sederhana, low effort dapat secara signifikan mengurangi waktu respons dan biaya.
3. **Uji kasus penggunaan Anda**: Dampak tingkat effort bervariasi menurut jenis tugas. Evaluasi kinerja pada kasus penggunaan spesifik Anda sebelum menerapkan.
4. **Pertimbangkan effort dinamis**: Sesuaikan effort berdasarkan kompleksitas tugas. Kueri sederhana mungkin memerlukan low effort sementara coding agentic dan penalaran kompleks mendapat manfaat dari high effort.