---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/text-watermark
fetched_at: 2026-11-14T02:12:32.675862Z
sha256: 0cf386fab4d9a2379ce4d2a99df552f26c76a19696b2f3c395d658eca922c970
---

---
title: Watermark teks
url: https://platform.claude.com/docs/id/build-with-claude/text-watermark
description: Apa yang tidak diubah oleh watermark teks Anthropic, di mana menemukan model dan platform yang dicakupnya, dan parameter sampling mana yang harus dihilangkan jika Anda mengandalkannya.
---

Teks yang dihasilkan oleh model Claude yang didukung membawa watermark teks Anthropic. [Bagaimana Claude menandai konten yang dihasilkan AI](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content) mencantumkan model dan platform yang dicakupnya, dan [How Claude’s text watermark works](https://www.anthropic.com/news/claude-text-watermark) memberikan latar belakangnya.

Watermark tidak mengubah makna, kualitas, atau keterbacaan output. Watermark tidak menambahkan token atau karakter tersembunyi dan tidak membawa informasi apa pun tentang Anda atau organisasi Anda. Anda tidak perlu mengubah permintaan atau penanganan respons Anda karenanya. Jika Anda mengandalkan watermark dan menetapkan `temperature`, `top_p`, atau `top_k`, lihat [Pengaturan sampling](https://platform.claude.com/docs/id/build-with-claude/text-watermark#sampling-settings).

## Pengaturan sampling

**Bagian ini berlaku untuk:** Claude Sonnet 4.6

Jika output Anda perlu membawa watermark, hilangkan `temperature`, `top_p`, dan `top_k` dari permintaan Anda. Jika sebuah permintaan menetapkan salah satu dari parameter tersebut ke nilai non-default, output mungkin tidak membawa watermark.

Framework atau pustaka klien Anda mungkin menetapkan parameter ini untuk Anda. Jika Anda memerlukan watermark, periksa pengaturannya dan body permintaan yang dikirimkannya, lalu hapus parameter mana pun dari ketiganya yang ditetapkannya.
