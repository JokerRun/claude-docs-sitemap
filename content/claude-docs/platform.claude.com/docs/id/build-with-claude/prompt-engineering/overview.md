---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 31a01b299b61efd21cfefa4a224a677f608f2f96e6f7d4e02fbfb26d7d4242da
---

---
title: Ikhtisar rekayasa prompt
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview
description: Pelajari kapan rekayasa prompt merupakan solusi yang tepat, dan temukan teknik prompting Claude serta tutorial interaktif.
---

## Sebelum rekayasa prompt

Panduan ini mengasumsikan bahwa Anda telah memiliki:

1. Definisi yang jelas tentang kriteria keberhasilan untuk kasus penggunaan Anda
2. Beberapa cara untuk menguji secara empiris terhadap kriteria tersebut
3. Draf pertama prompt yang ingin Anda tingkatkan

Jika belum, luangkan waktu untuk menetapkannya terlebih dahulu. Lihat [Tentukan kriteria keberhasilan dan bangun evaluasi](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests) untuk tips dan panduan.

<CardGroup cols={2}>
  <Card title="Notebook generator prompt" icon="link" href="https://colab.research.google.com/github/anthropics/claude-cookbooks/blob/main/misc/metaprompt.ipynb">
    Belum punya draf pertama prompt? Buat satu dengan resep metaprompt dari Claude Cookbook.
  </Card>

  <Card title="Praktik terbaik prompting" icon="link" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Untuk panduan penyetelan khusus model bagi model-model terbaru Claude, mulailah di sini.
  </Card>
</CardGroup>

***

## Kapan melakukan rekayasa prompt

Panduan ini berfokus pada kriteria keberhasilan yang dapat dikendalikan melalui "prompt engineering" (rekayasa prompt). Tidak setiap kriteria keberhasilan atau evaluasi yang gagal paling baik diselesaikan dengan rekayasa prompt. Misalnya, terkadang Anda dapat meningkatkan "latency" (latensi) dan biaya dengan lebih mudah dengan memilih model yang berbeda.

***

## Cara melakukan rekayasa prompt

Semua teknik prompting (mulai dari kejelasan dan contoh hingga penstrukturan XML, role prompting, thinking, dan prompt chaining) dibahas dalam [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices). Itu adalah referensi yang terus diperbarui; mulailah dari sana.

Untuk keahlian rekayasa prompt secara umum di luar teknik khusus Claude, lihat postingan blog tentang [praktik terbaik untuk rekayasa prompt](https://claude.com/blog/best-practices-for-prompt-engineering).

***

## Tutorial rekayasa prompt

Jika Anda adalah pembelajar interaktif, Anda dapat memulai dengan tutorial interaktif sebagai gantinya!

<CardGroup cols={2}>
  <Card title="Tutorial prompting GitHub" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    Tutorial penuh contoh yang mencakup konsep-konsep rekayasa prompt yang terdapat dalam dokumentasi.
  </Card>

  <Card title="Tutorial prompting Google Sheets" icon="link" href="https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8">
    Versi yang lebih ringan dari tutorial rekayasa prompt, dalam bentuk spreadsheet interaktif.
  </Card>
</CardGroup>
