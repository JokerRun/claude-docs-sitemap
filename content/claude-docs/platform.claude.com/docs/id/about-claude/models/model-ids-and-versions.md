---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 27f6a77bc0b3354d2b5e02168cb87a650699f02bf393de21f7d7c1ee84717b72
---

---
title: ID model dan pembuatan versi
url: https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions
description: Bagaimana ID model Claude disusun dan diberi versi, termasuk format tanpa tanggal yang diperkenalkan dengan generasi Claude 4.6 dan apa artinya bagi stabilitas.
---

Setiap ID model Claude mengidentifikasi versi model yang telah dipatok (pinned). Ketika Anda menggunakan ID model dalam permintaan API, model yang mendasarinya tetap konstan selama masa pakai ID tersebut. Jaminan ini mencakup ID model, bukan alias kemudahan yang diterima Claude API untuk beberapa model sebelumnya (lihat [Sebelum generasi 4.6](https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions#before-the-4-6-generation)).

## Format ID model

ID model Claude mengikuti skema penamaan berversi.

### Generasi 4.6 dan setelahnya

Mulai dari generasi Claude 4.6, ID model menggunakan format tanpa tanggal:

```text wrap
claude-{name}-{major}[-{minor}]
```

Rilis versi mayor seperti Claude Sonnet 5 dan Claude Opus 5 menghilangkan segmen minor.

Sebagai contoh: `claude-sonnet-4-6`, `claude-sonnet-5`, `claude-opus-4-6`, `claude-opus-4-7`, `claude-opus-4-8`, dan `claude-opus-5`

Di Amazon Bedrock, format yang sesuai adalah:

```text wrap
anthropic.claude-{name}-{major}[-{minor}]
```

Sebagai contoh: `anthropic.claude-sonnet-4-6`, `anthropic.claude-sonnet-5`, `anthropic.claude-opus-4-7`, `anthropic.claude-opus-4-8`, `anthropic.claude-opus-5`

Claude Opus 4.6 adalah ID model Bedrock terakhir yang menyertakan sufiks `-v1` (`anthropic.claude-opus-4-6-v1`). Anthropic menghapus sufiks tersebut mulai dari Claude Sonnet 4.6.

Di Google Cloud, formatnya sama dengan Claude API.

### Sebelum generasi 4.6

Model sebelum generasi 4.6 menyertakan tanggal snapshot dalam ID:

```text wrap
claude-{name}-{major}-{minor}-{YYYYMMDD}
```

Sebagai contoh: `claude-sonnet-4-5-20250929`, `claude-haiku-4-5-20251001`

Di Amazon Bedrock, model-model ini menggunakan format:

```text wrap
anthropic.claude-{name}-{major}-{minor}-{YYYYMMDD}-v1:0
```

Sebagai contoh: `anthropic.claude-sonnet-4-5-20250929-v1:0`

Di Google Cloud, tanggal dipisahkan dengan `@`:

```text wrap
claude-{name}-{major}-{minor}@{YYYYMMDD}
```

Sebagai contoh: `claude-haiku-4-5@20251001`

Di Claude API, model-model ini juga memiliki alias yang lebih pendek (misalnya, `claude-sonnet-4-5`) yang menunjuk ke snapshot bertanggal terbaru untuk versi minor tersebut.

## ID tanpa tanggal adalah snapshot yang dipatok

Kesalahpahaman yang umum adalah bahwa ID model tanpa tanggal seperti `claude-sonnet-4-6` berperilaku sebagai penunjuk evergreen yang mengarahkan ke versi terbaru atau yang berkinerja terbaik. Hal itu tidak benar.

Untuk generasi 4.6 dan setelahnya, ID tanpa tanggal adalah ID model kanonis untuk rilis tersebut. ID ini memetakan ke satu snapshot model yang tetap. Anthropic tidak memperbarui bobot atau konfigurasi dari ID model yang sudah ada. Ketika versi yang diperbarui tersedia, versi tersebut dirilis dengan ID model baru.

Ini berbeda dari alias tanpa tanggal yang ada di Claude API untuk model-model sebelumnya. Alias seperti `claude-sonnet-4-5` adalah penunjuk kemudahan yang diselesaikan ke snapshot bertanggal terbaru untuk versi minor tersebut. ID generasi 4.6 seperti `claude-sonnet-4-6` bukanlah alias. ID tersebut adalah snapshot itu sendiri.

Setiap ID model, baik bertanggal maupun tanpa tanggal, memiliki jadwal deprekasi dan penghentian (retirement) yang berbeda.

## Bobot model versus infrastruktur penyajian

Bobot model bersifat tetap untuk ID tertentu, tetapi infrastruktur penyajian di sekitar model dapat berubah seiring waktu. Infrastruktur ini mencakup komponen seperti router permintaan, pengklasifikasi keamanan, dan logika sampling.

Terkadang, pembaruan infrastruktur menghasilkan perbedaan kecil dalam perilaku yang dapat diamati meskipun ID model dan bobotnya tidak berubah. Jika Anda melihat perbedaan perilaku yang tidak terduga pada ID model yang sebelumnya stabil, pembaruan infrastruktur adalah penyebab yang paling mungkin.

## ID model saat ini

Untuk daftar lengkap ID model saat ini beserta padanannya di Amazon Bedrock dan Google Cloud, lihat [Ikhtisar model](https://platform.claude.com/docs/id/about-claude/models/overview).
