---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/multilingual-support
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 8427cb02a7aa1e84316473f0d8de175dae668f888c1fbd2bc99f4fa0b8bc74c7
---

# Dukungan multibahasa

Claude unggul dalam tugas-tugas di berbagai bahasa, mempertahankan performa lintas bahasa yang kuat relatif terhadap bahasa Inggris.

---

## Ikhtisar \{#overview}

Claude menunjukkan kemampuan multibahasa yang tangguh, dengan performa yang sangat kuat dalam tugas-tugas "zero-shot" (tanpa contoh) di berbagai bahasa. Model ini mempertahankan performa relatif yang konsisten baik pada bahasa yang banyak digunakan maupun bahasa dengan sumber daya lebih sedikit, menjadikannya pilihan yang andal untuk aplikasi multibahasa.

Perlu dicatat bahwa Claude mampu menangani banyak bahasa di luar yang diukur dalam tolok ukur di bawah ini. Pertimbangkan untuk menguji dengan bahasa apa pun yang relevan dengan kasus penggunaan spesifik Anda.

## Data performa \{#performance-data}

Berikut adalah skor evaluasi "zero-shot chain-of-thought" (rantai pemikiran tanpa contoh) untuk model Claude di berbagai bahasa, ditampilkan sebagai persentase relatif terhadap performa bahasa Inggris (100%):

| Bahasa | Claude Opus 4.1 (tidak digunakan lagi)<sup>1</sup> | Claude Opus 4 (tidak digunakan lagi)<sup>1</sup> | Claude Sonnet 4.5<sup>1</sup> | Claude Sonnet 4 (tidak digunakan lagi)<sup>1</sup> | Claude Haiku 4.5<sup>1</sup> |
|----------|---------------|---------------|---------------|-----------------|------------------|
| Inggris (baseline, ditetapkan pada 100%) | 100% | 100% | 100% | 100% | 100% |
| Spanyol | 98,1% | 98,0% | 98,2% | 97,5% | 96,4% |
| Portugis (Brasil) | 97,8% | 97,3% | 97,8% | 97,2% | 96,1% |
| Italia | 97,7% | 97,5% | 97,9% | 97,3% | 96,0% |
| Prancis | 97,9% | 97,7% | 97,5% | 97,1% | 95,7% |
| Indonesia | 97,3% | 97,2% | 97,3% | 96,2% | 94,2% |
| Jerman | 97,7% | 97,1% | 97,0% | 94,7% | 94,3% |
| Arab | 97,1% | 96,9% | 97,2% | 96,1% | 92,5% |
| Mandarin (Sederhana) | 97,1% | 96,7% | 96,9% | 95,9% | 94,2% |
| Korea | 96,6% | 96,4% | 96,7% | 95,9% | 93,3% |
| Jepang | 96,9% | 96,2% | 96,8% | 95,6% | 93,5% |
| Hindi | 96,8% | 96,7% | 96,7% | 95,8% | 92,4% |
| Bengali | 95,7% | 95,2% | 95,4% | 94,4% | 90,4% |
| Swahili | 89,8% | 89,5% | 91,1% | 87,1% | 78,3% |
| Yoruba | 80,3% | 78,9% | 79,7% | 76,4% | 52,7% |

<sup>1</sup> Dengan [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking).

<Note>
Metrik ini didasarkan pada set pengujian bahasa Inggris [MMLU (Massive Multitask Language Understanding)](https://en.wikipedia.org/wiki/MMLU) yang diterjemahkan ke dalam 14 bahasa tambahan oleh penerjemah manusia profesional, sebagaimana didokumentasikan dalam [repositori simple-evals OpenAI](https://github.com/openai/simple-evals/blob/main/multilingual_mmlu_benchmark_results.md). Penggunaan penerjemah manusia untuk evaluasi ini memastikan terjemahan berkualitas tinggi, yang sangat penting untuk bahasa dengan sumber daya digital yang lebih sedikit.
</Note>

***

## Praktik terbaik \{#best-practices}

Saat bekerja dengan konten multibahasa:

1. **Berikan konteks bahasa yang jelas**: Meskipun Claude dapat mendeteksi bahasa target secara otomatis, menyatakan secara eksplisit bahasa input/output yang diinginkan akan meningkatkan keandalan. Untuk kefasihan yang lebih baik, Anda dapat meminta Claude untuk menggunakan "ucapan idiomatis seolah-olah ia adalah penutur asli."
2. **Gunakan aksara asli**: Kirimkan teks dalam aksara aslinya, bukan transliterasi, untuk hasil yang optimal
3. **Pertimbangkan konteks budaya**: Komunikasi yang efektif sering kali memerlukan kesadaran budaya dan regional di luar sekadar terjemahan

Ikuti juga [panduan rekayasa prompt](/docs/id/build-with-claude/prompt-engineering/overview) umum untuk lebih meningkatkan performa Claude.

***

## Pertimbangan dukungan bahasa \{#language-support-considerations}

- Claude memproses input dan menghasilkan output dalam sebagian besar bahasa dunia yang menggunakan karakter Unicode standar
- Performa bervariasi menurut bahasa, dengan kemampuan yang sangat kuat pada bahasa yang banyak digunakan
- Bahkan pada bahasa dengan sumber daya digital yang lebih sedikit, Claude tetap mempertahankan kemampuan yang berarti

<CardGroup cols={1}>
  <Card title="Panduan Rekayasa Prompt" icon="edit" href="/docs/id/build-with-claude/prompt-engineering/overview">
    Kuasai seni menyusun prompt untuk mendapatkan hasil maksimal dari Claude.
  </Card>
</CardGroup>