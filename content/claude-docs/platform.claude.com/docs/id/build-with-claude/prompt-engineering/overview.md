---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: f4af126a30e96ab8c6aee742f0b34590a0f97b5c91022b710f305b0ebcc76597
---

# Gambaran umum prompt engineering

Panduan komprehensif tentang teknik prompt engineering untuk meningkatkan kinerja model Claude

---

<Note>
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips).
</Note>

## Sebelum prompt engineering

Panduan ini mengasumsikan bahwa Anda memiliki:
1. Definisi yang jelas tentang kriteria kesuksesan untuk kasus penggunaan Anda
2. Beberapa cara untuk menguji secara empiris terhadap kriteria tersebut
3. Draf prompt pertama yang ingin Anda tingkatkan

Jika tidak, kami sangat menyarankan Anda meluangkan waktu untuk membangun itu terlebih dahulu. Lihat [Tentukan kriteria kesuksesan Anda](/docs/id/test-and-evaluate/define-success) dan [Buat evaluasi empiris yang kuat](/docs/id/test-and-evaluate/develop-tests) untuk tips dan panduan.

<Card title="Pembuat prompt" icon="link" href="/dashboard">
  Tidak memiliki draf prompt pertama? Coba pembuat prompt di Claude Console!
</Card>

***

## Kapan melakukan prompt engineering

  Panduan ini berfokus pada kriteria kesuksesan yang dapat dikendalikan melalui prompt engineering.
  Tidak setiap kriteria kesuksesan atau evaluasi yang gagal paling baik diselesaikan dengan prompt engineering. Misalnya, latensi dan biaya terkadang dapat ditingkatkan lebih mudah dengan memilih model yang berbeda.

<section title="Prompting vs. finetuning">

  Prompt engineering jauh lebih cepat daripada metode kontrol perilaku model lainnya, seperti finetuning, dan sering kali dapat menghasilkan lompatan kinerja dalam waktu yang jauh lebih singkat. Berikut adalah beberapa alasan untuk mempertimbangkan prompt engineering daripada finetuning:<br/>
  - **Efisiensi sumber daya**: Fine-tuning memerlukan GPU kelas atas dan memori besar, sementara prompt engineering hanya memerlukan input teks, menjadikannya jauh lebih ramah sumber daya.
  - **Efektivitas biaya**: Untuk layanan AI berbasis cloud, fine-tuning menimbulkan biaya signifikan. Prompt engineering menggunakan model dasar, yang biasanya lebih murah.
  - **Mempertahankan pembaruan model**: Ketika penyedia memperbarui model, versi yang di-fine-tune mungkin perlu dilatih ulang. Prompt biasanya bekerja di seluruh versi tanpa perubahan.
  - **Penghematan waktu**: Fine-tuning dapat memakan waktu berjam-jam atau bahkan berhari-hari. Sebaliknya, prompt engineering memberikan hasil yang hampir instan, memungkinkan pemecahan masalah yang cepat.
  - **Kebutuhan data minimal**: Fine-tuning memerlukan data berlabel khusus tugas yang substansial, yang dapat langka atau mahal. Prompt engineering bekerja dengan pembelajaran few-shot atau bahkan zero-shot.
  - **Fleksibilitas & iterasi cepat**: Coba berbagai pendekatan dengan cepat, sesuaikan prompt, dan lihat hasil segera. Eksperimen cepat ini sulit dilakukan dengan fine-tuning.
  - **Adaptasi domain**: Dengan mudah sesuaikan model ke domain baru dengan memberikan konteks khusus domain dalam prompt, tanpa pelatihan ulang.
  - **Peningkatan pemahaman**: Prompt engineering jauh lebih efektif daripada finetuning dalam membantu model lebih baik memahami dan memanfaatkan konten eksternal seperti dokumen yang diambil
  - **Mempertahankan pengetahuan umum**: Fine-tuning berisiko lupa bencana, di mana model kehilangan pengetahuan umum. Prompt engineering mempertahankan kemampuan luas model.
  - **Transparansi**: Prompt dapat dibaca manusia, menunjukkan dengan tepat informasi apa yang diterima model. Transparansi ini membantu dalam pemahaman dan debugging.

</section>

***

## Cara melakukan prompt engineering

Halaman prompt engineering di bagian ini telah diatur dari teknik yang paling luas efektif hingga teknik yang lebih khusus. Saat memecahkan masalah kinerja, kami menyarankan Anda mencoba teknik ini secara berurutan, meskipun dampak sebenarnya dari setiap teknik akan bergantung pada kasus penggunaan Anda.
1. [Pembuat prompt](/docs/id/build-with-claude/prompt-engineering/prompt-generator)
2. [Jadilah jelas dan langsung](/docs/id/build-with-claude/prompt-engineering/be-clear-and-direct)
3. [Gunakan contoh (multishot)](/docs/id/build-with-claude/prompt-engineering/multishot-prompting)
4. [Biarkan Claude berpikir (chain of thought)](/docs/id/build-with-claude/prompt-engineering/chain-of-thought)
5. [Gunakan tag XML](/docs/id/build-with-claude/prompt-engineering/use-xml-tags)
6. [Berikan Claude peran (system prompts)](/docs/id/build-with-claude/prompt-engineering/system-prompts)
7. [Rantai prompt kompleks](/docs/id/build-with-claude/prompt-engineering/chain-prompts)
8. [Tips konteks panjang](/docs/id/build-with-claude/prompt-engineering/long-context-tips)

***

## Tutorial prompt engineering

Jika Anda adalah pelajar interaktif, Anda dapat menyelami tutorial interaktif kami sebagai gantinya!

<CardGroup cols={2}>
  <Card title="Tutorial prompting GitHub" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    Tutorial yang penuh dengan contoh yang mencakup konsep prompt engineering yang ditemukan di dokumen kami.
  </Card>
  <Card title="Tutorial prompting Google Sheets" icon="link" href="https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8">
    Versi yang lebih ringan dari tutorial prompt engineering kami melalui spreadsheet interaktif.
  </Card>
</CardGroup>