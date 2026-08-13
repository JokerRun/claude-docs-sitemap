---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 755dc5c34aa209131a358745e539037bf27f4b3a136af2ed23e23e77a49b792f
---

---
title: Ikhtisar prompt engineering
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview
description: Pelajari kapan prompt engineering adalah solusi yang tepat, dan temukan teknik prompting Claude serta tutorial interaktif.
---

## Sebelum prompt engineering

Panduan ini mengasumsikan bahwa Anda memiliki:

1. Definisi yang jelas tentang kriteria keberhasilan untuk kasus penggunaan Anda
2. Beberapa cara untuk menguji secara empiris terhadap kriteria tersebut
3. Draf pertama prompt yang ingin Anda tingkatkan

Jika belum, luangkan waktu untuk menetapkan hal tersebut terlebih dahulu. Lihat [Menentukan kriteria keberhasilan dan membangun evaluasi](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests) untuk tips dan panduan.

<CardGroup cols={2}>
  <Card title="Notebook generator prompt" icon="link" href="https://colab.research.google.com/github/anthropics/claude-cookbooks/blob/main/misc/metaprompt.ipynb">
    Belum memiliki draf pertama prompt? Buat satu dengan resep metaprompt dari Claude Cookbook.
  </Card>

  <Card title="Praktik terbaik prompting" icon="link" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Untuk panduan penyetelan khusus model untuk model-model terbaru Claude, mulai dari sini.
  </Card>
</CardGroup>

***

## Kapan melakukan prompt engineering

Panduan ini berfokus pada kriteria keberhasilan yang dapat dikendalikan melalui prompt engineering. Tidak semua kriteria keberhasilan atau eval yang gagal paling baik diselesaikan dengan prompt engineering. Misalnya, Anda terkadang dapat meningkatkan "latency" (latensi) dan biaya dengan lebih mudah dengan memilih model yang berbeda.

***

## Cara melakukan prompt engineering

Semua teknik prompting (dari kejelasan dan contoh hingga penstrukturan XML, role prompting, thinking, dan prompt chaining) dibahas dalam [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices). Itu adalah referensi yang terus diperbarui; mulailah dari sana.

Untuk keterampilan prompt engineering umum di luar teknik khusus Claude, lihat postingan blog tentang [praktik terbaik untuk prompt engineering](https://claude.com/blog/best-practices-for-prompt-engineering).

***

## Tutorial prompt engineering

Jika Anda adalah pembelajar interaktif, Anda dapat memulai dengan tutorial interaktif sebagai gantinya!

<CardGroup cols={2}>
  <Card title="Tutorial prompting GitHub" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    Tutorial yang penuh dengan contoh yang mencakup konsep prompt engineering yang ditemukan dalam dokumentasi.
  </Card>

  <Card title="Tutorial prompting Google Sheets" icon="link" href="https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8">
    Versi yang lebih ringan dari tutorial prompt engineering, dalam bentuk spreadsheet interaktif.
  </Card>
</CardGroup>
