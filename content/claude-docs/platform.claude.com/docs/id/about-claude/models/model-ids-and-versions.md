---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: b8a0445c805bed8f1dad898d13af263f9bd2039d20067c8664e4d382ad2c31e1
---

---
title: ID model dan pembuatan versi
url: https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions
description: Bagaimana ID model Claude disusun dan diberi versi, termasuk format tanpa tanggal yang diperkenalkan pada generasi Claude 4.6 dan apa artinya bagi stabilitas.
---

Setiap ID model Claude mengidentifikasi versi model yang disematkan (pinned). Saat Anda menggunakan ID model dalam permintaan API, model yang mendasarinya tetap konstan selama masa berlaku ID tersebut. Jaminan ini mencakup ID model, bukan alias praktis yang diterima Claude API untuk beberapa model terdahulu (lihat [Sebelum generasi 4.6](https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions#before-the-4-6-generation)).

## Format ID model

ID model Claude mengikuti skema penamaan berversi.

### Generasi 4.6 dan setelahnya

Mulai dari generasi Claude 4.6, ID model menggunakan format tanpa tanggal:

```text wrap
claude-{name}-{major}[-{minor}]
```

Rilis versi mayor seperti Claude Sonnet 5 dan Claude Opus 5 menghilangkan segmen minor.

Contohnya: `claude-sonnet-4-6`, `claude-sonnet-5`, `claude-opus-4-6`, `claude-opus-4-7`, `claude-opus-4-8`, dan `claude-opus-5`

Di Amazon Bedrock, format yang sesuai adalah:

```text wrap
anthropic.claude-{name}-{major}[-{minor}]
```

Contohnya: `anthropic.claude-sonnet-4-6`, `anthropic.claude-sonnet-5`, `anthropic.claude-opus-4-7`, `anthropic.claude-opus-4-8`, `anthropic.claude-opus-5`

Claude Opus 4.6 adalah ID model Bedrock terakhir yang menyertakan sufiks `-v1` (`anthropic.claude-opus-4-6-v1`). Anthropic menghapus sufiks tersebut mulai dari Claude Sonnet 4.6.

Di endpoint `bedrock-runtime`, model yang disajikan AWS melalui inferensi lintas wilayah, termasuk Claude Fable 5.2 dan Claude Mythos 5.2, menggunakan ID profil inferensi: ID model dasar dengan prefiks seperti `global.` atau `us.`, misalnya `global.anthropic.claude-fable-5-2`. Lihat [ID model API](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#api-model-ids).

Di [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) dan [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), formatnya sama dengan Claude API.

### Sebelum generasi 4.6

Model sebelum generasi 4.6 menyertakan tanggal snapshot dalam ID:

```text wrap
claude-{name}-{major}-{minor}-{YYYYMMDD}
```

Contohnya: `claude-haiku-4-5-20251001`

Di Claude API, model Claude 4.5 juga memiliki alias yang lebih pendek, seperti `claude-haiku-4-5`. Setiap alias menunjuk ke snapshot bertanggal terbaru untuk versi minornya.

Di Amazon Bedrock (`bedrock-runtime`), ID bertanggal menggunakan format:

```text wrap
anthropic.claude-{name}-{major}-{minor}-{YYYYMMDD}-v1:0
```

Contohnya: `anthropic.claude-haiku-4-5-20251001-v1:0`

Untuk memanggil model-model ini, tambahkan prefiks profil inferensi, seperti `global.` atau `us.`, ke ID tersebut. Untuk detailnya, lihat [ID model API](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#api-model-ids) di halaman Amazon Bedrock (`bedrock-runtime`).

Di [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#api-model-ids), formatnya sama dengan Claude API.

Di Claude Models on Google Cloud (Google managed), tanggal dipisahkan dengan `@`:

```text wrap
claude-{name}-{major}-{minor}@{YYYYMMDD}
```

Contohnya: `claude-haiku-4-5@20251001`

[Amazon Bedrock (`bedrock-mantle`)](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock#supported-models), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#available-models), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry#api-model-ids-and-deployments) mencantumkan model-model ini dengan ID tanpa tanggal. Setiap tautan membuka tabel model platform tersebut, yang berisi ID yang perlu digunakan.

## ID tanpa tanggal adalah snapshot yang disematkan

Kesalahpahaman yang umum adalah bahwa ID model tanpa tanggal seperti `claude-sonnet-4-6` berperilaku sebagai penunjuk evergreen (selalu terbaru) yang mengarahkan ke versi terbaru atau berkinerja terbaik. Hal itu tidak benar.

Untuk generasi 4.6 dan setelahnya, ID tanpa tanggal adalah ID model kanonis untuk rilis tersebut. ID ini memetakan ke satu snapshot model yang tetap. Anthropic tidak memperbarui bobot atau konfigurasi dari ID model yang sudah ada. Ketika versi yang diperbarui tersedia, versi tersebut dirilis dengan ID model baru.

ID dari generasi 4.6 atau setelahnya, seperti `claude-sonnet-4-6`, terlihat seperti alias di [Sebelum generasi 4.6](https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions#before-the-4-6-generation). Namun, ID tersebut bukanlah alias. ID tersebut adalah snapshot itu sendiri.

Setiap ID model, baik bertanggal maupun tanpa tanggal, memiliki jadwal deprecation (penghentian dukungan) dan retirement (pemberhentian) tersendiri.

## Bobot model versus infrastruktur penyajian

“Model weights” (bobot model) bersifat tetap untuk ID tertentu, tetapi “serving infrastructure” (infrastruktur penyajian) di sekitar model dapat berubah seiring waktu. Infrastruktur ini mencakup komponen seperti router permintaan, pengklasifikasi keamanan, dan logika sampling.

Sesekali, pembaruan infrastruktur menghasilkan perbedaan kecil dalam perilaku yang dapat diamati meskipun ID model dan bobotnya tidak berubah. Jika Anda melihat perbedaan perilaku yang tidak terduga pada ID model yang sebelumnya stabil, pembaruan infrastruktur adalah penyebab yang paling mungkin.

## ID model saat ini

Untuk ID model saat ini di setiap platform, lihat [Ikhtisar model](https://platform.claude.com/docs/id/models/overview).
