---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: b0c58ed9bbd9e298f0aadd4118984551b2281487737f3dbc47377b6f111c8ed8
---

# Ikhtisar rekayasa prompt

---

## Sebelum melakukan rekayasa prompt

Panduan ini mengasumsikan bahwa Anda telah memiliki:

1. Definisi yang jelas tentang kriteria keberhasilan untuk kasus penggunaan Anda
2. Beberapa cara untuk menguji secara empiris terhadap kriteria tersebut
3. Draf pertama prompt yang ingin Anda tingkatkan

Jika belum, kami sangat menyarankan Anda meluangkan waktu untuk menetapkannya terlebih dahulu. Lihat [Menentukan kriteria keberhasilan dan membangun evaluasi](/docs/id/test-and-evaluate/develop-tests) untuk tips dan panduan.

<CardGroup cols={2}>
  <Card title="Generator prompt" icon="link" href="/dashboard">
    Belum memiliki draf pertama prompt? Coba generator prompt di Claude Console!
  </Card>

  <Card title="Praktik terbaik prompting" icon="link" href="/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Untuk panduan penyetelan spesifik model pada model terbaru Claude, mulailah dari sini.
  </Card>
</CardGroup>

***

## Kapan melakukan rekayasa prompt

Panduan ini berfokus pada kriteria keberhasilan yang dapat dikendalikan melalui rekayasa prompt. Tidak semua kriteria keberhasilan atau evaluasi yang gagal paling baik diselesaikan dengan rekayasa prompt. Misalnya, "latency" (latensi) dan biaya terkadang dapat lebih mudah ditingkatkan dengan memilih model yang berbeda.

***

## Cara melakukan rekayasa prompt

Semua teknik prompting — mulai dari kejelasan dan contoh hingga penataan XML, role prompting, pemikiran, dan perantaian prompt — dibahas dalam [Praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices). Itu adalah referensi yang terus diperbarui; mulailah dari sana.

[Claude Console](/dashboard) juga menawarkan [alat prompting](/docs/id/build-with-claude/prompt-engineering/prompting-tools)—generator prompt, template dan variabel, serta penyempurna prompt—untuk membantu Anda membangun dan menyempurnakan prompt dengan cepat.

***

## Tutorial rekayasa prompt

Jika Anda adalah pembelajar interaktif, Anda dapat langsung menyelami tutorial interaktif kami!

<CardGroup cols={2}>
  <Card title="Tutorial prompting GitHub" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    Tutorial yang penuh dengan contoh yang mencakup konsep rekayasa prompt yang terdapat dalam dokumentasi kami.
  </Card>

  <Card title="Tutorial prompting Google Sheets" icon="link" href="https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8">
    Versi yang lebih ringan dari tutorial rekayasa prompt kami melalui spreadsheet interaktif.
  </Card>
</CardGroup>
