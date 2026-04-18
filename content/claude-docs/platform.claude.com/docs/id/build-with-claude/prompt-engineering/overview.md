---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 0c5f4ed6b86df558f7949d8bae671966fb6a9476a01ad8a8eae29c8519262802
---

# Ikhtisar rekayasa prompt

Panduan untuk meningkatkan prompt Anda melalui pengujian sistematis dan iterasi.

---

## Sebelum rekayasa prompt

Panduan ini mengasumsikan bahwa Anda memiliki:
1. Definisi yang jelas tentang kriteria kesuksesan untuk kasus penggunaan Anda
2. Beberapa cara untuk menguji secara empiris terhadap kriteria tersebut
3. Draf prompt pertama yang ingin Anda tingkatkan

Jika tidak, kami sangat menyarankan Anda meluangkan waktu untuk membangun itu terlebih dahulu. Lihat [Tentukan kriteria kesuksesan dan bangun evaluasi](/docs/id/test-and-evaluate/develop-tests) untuk tips dan panduan.

<CardGroup cols={2}>
  <Card title="Pembuat prompt" icon="link" href="/dashboard">
    Tidak memiliki draf prompt pertama? Coba pembuat prompt di Claude Console!
  </Card>
  <Card title="Praktik terbaik prompting" icon="link" href="/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Untuk panduan penyetelan khusus model untuk model Claude terbaru, mulai dari sini.
  </Card>
</CardGroup>

***

## Kapan melakukan rekayasa prompt

  Panduan ini berfokus pada kriteria kesuksesan yang dapat dikontrol melalui rekayasa prompt.
  Tidak setiap kriteria kesuksesan atau evaluasi yang gagal paling baik diselesaikan dengan rekayasa prompt. Misalnya, latensi dan biaya terkadang dapat ditingkatkan lebih mudah dengan memilih model yang berbeda.

***

## Cara melakukan rekayasa prompt

Semua teknik prompting — dari kejelasan dan contoh hingga strukturisasi XML, prompting peran, pemikiran, dan rantai prompt — tercakup dalam [Praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices). Itu adalah referensi yang hidup; mulai dari sana.

Claude Console juga menawarkan [alat prompting](/docs/id/build-with-claude/prompt-engineering/prompting-tools)—pembuat prompt, template dan variabel, dan penyempurna prompt—untuk membantu Anda membangun dan menyempurnakan prompt dengan cepat.

***

## Tutorial rekayasa prompt

Jika Anda adalah pelajar interaktif, Anda dapat menyelami tutorial interaktif kami sebagai gantinya!

<CardGroup cols={2}>
  <Card title="Tutorial prompting GitHub" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    Tutorial yang penuh dengan contoh yang mencakup konsep rekayasa prompt yang ditemukan di dokumentasi kami.
  </Card>
  <Card title="Tutorial prompting Google Sheets" icon="link" href="https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8">
    Versi yang lebih ringan dari tutorial rekayasa prompt kami melalui spreadsheet interaktif.
  </Card>
</CardGroup>