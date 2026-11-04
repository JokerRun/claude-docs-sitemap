---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/text-watermark
fetched_at: 2026-11-04T02:12:37.489821Z
sha256: 2d782d0e78e5a0a3a2abc87a33ad8ba8953595007400dae4bc18914619c8f482
---

---
title: Watermark teks
url: https://platform.claude.com/docs/id/build-with-claude/text-watermark
description: Apa yang tidak diubah oleh watermark teks Anthropic, di mana menemukan model dan platform yang dicakupnya, dan parameter sampling mana yang harus dihilangkan jika Anda mengandalkannya.
---

Teks yang dihasilkan oleh model Claude yang didukung membawa watermark teks Anthropic. [How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content) mencantumkan model dan platform yang dicakupnya, dan [How Claude’s text watermark works](https://www.anthropic.com/news/claude-text-watermark) memberikan latar belakangnya.

Watermark tidak mengubah makna, kualitas, atau keterbacaan output. Watermark tidak menambahkan token atau karakter tersembunyi dan tidak membawa informasi apa pun tentang Anda atau organisasi Anda. Anda tidak perlu mengubah permintaan atau penanganan respons Anda karenanya. Jika Anda mengandalkan watermark dan menetapkan `temperature`, `top_p`, atau `top_k`, lihat [Pengaturan sampling](https://platform.claude.com/docs/id/build-with-claude/text-watermark#sampling-settings).

## Pengaturan sampling

Pada Claude Sonnet 4.6, teks yang dihasilkan untuk permintaan yang menetapkan `temperature`, `top_p`, atau `top_k` ke nilai non-default mungkin tidak membawa watermark. Jika Anda mengandalkan watermark, hilangkan ketiga parameter tersebut dari permintaan Anda, termasuk parameter yang ditetapkan untuk Anda oleh framework atau pustaka klien.
