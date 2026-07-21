---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: bbcfbcf34e781d66177c5743e336c445a0bd58b0e6cdb7829e00b18aebcd1b6a
---

# ID Model dan penentuan versi

Bagaimana ID model Claude disusun dan diberi versi, termasuk format tanpa tanggal yang diperkenalkan pada generasi Claude 4.6 dan apa artinya bagi stabilitas.

---

Setiap ID model Claude mengidentifikasi versi model yang telah dipatok (pinned). Ketika Anda menggunakan ID model dalam permintaan API, model yang mendasarinya tetap konstan selama masa pakai ID tersebut. Jaminan ini mencakup ID model, bukan alias kemudahan yang diterima oleh Claude API untuk beberapa model sebelumnya (lihat [Sebelum generasi 4.6](#before-the-4-6-generation)).

## Format ID model

ID model Claude mengikuti skema penamaan berversi.

### Generasi 4.6 dan setelahnya

Mulai dari generasi Claude 4.6, ID model menggunakan format tanpa tanggal:

```text wrap
claude-{name}-{major}[-{minor}]
```

Rilis versi mayor seperti Claude Sonnet 5 menghilangkan segmen minor.

Contohnya: `claude-sonnet-4-6`, `claude-sonnet-5`, `claude-opus-4-6`, `claude-opus-4-7`, dan `claude-opus-4-8`

Di Amazon Bedrock, format yang sesuai adalah:

```text wrap
anthropic.claude-{name}-{major}[-{minor}]
```

Contohnya: `anthropic.claude-sonnet-4-6`, `anthropic.claude-sonnet-5`, `anthropic.claude-opus-4-7`, `anthropic.claude-opus-4-8`

Claude Opus 4.6 adalah ID model Bedrock terakhir yang menyertakan akhiran `-v1` (`anthropic.claude-opus-4-6-v1`). Anthropic menghapus akhiran tersebut mulai dari Claude Sonnet 4.6.

Di Google Cloud, formatnya sama dengan Claude API.

### Sebelum generasi 4.6

Model sebelum generasi 4.6 menyertakan tanggal snapshot dalam ID:

```text wrap
claude-{name}-{major}-{minor}-{YYYYMMDD}
```

Contohnya: `claude-sonnet-4-5-20250929`, `claude-haiku-4-5-20251001`

Di Amazon Bedrock, model-model ini menggunakan format:

```text wrap
anthropic.claude-{name}-{major}-{minor}-{YYYYMMDD}-v1:0
```

Contohnya: `anthropic.claude-sonnet-4-5-20250929-v1:0`

Di Google Cloud, tanggal dipisahkan dengan `@`:

```text wrap
claude-{name}-{major}-{minor}@{YYYYMMDD}
```

Contohnya: `claude-haiku-4-5@20251001`

Di Claude API, model-model ini juga memiliki alias yang lebih pendek (misalnya, `claude-sonnet-4-5`) yang mengarah ke snapshot bertanggal terbaru untuk versi minor tersebut.

## ID tanpa tanggal adalah snapshot yang dipatok

Kesalahpahaman yang umum adalah bahwa ID model tanpa tanggal seperti `claude-sonnet-4-6` berperilaku sebagai penunjuk "evergreen" yang mengarahkan ke versi terbaru atau versi dengan performa terbaik. Hal itu tidak benar.

Untuk generasi 4.6 dan setelahnya, ID tanpa tanggal adalah ID model kanonis untuk rilis tersebut. ID ini dipetakan ke satu snapshot model yang tetap. Anthropic tidak memperbarui bobot atau konfigurasi dari ID model yang sudah ada. Ketika versi yang diperbarui tersedia, versi tersebut dirilis dengan ID model baru.

Hal ini berbeda dari alias tanpa tanggal yang ada di Claude API untuk model-model sebelumnya. Alias seperti `claude-sonnet-4-5` adalah penunjuk kemudahan yang mengarah ke snapshot bertanggal terbaru untuk versi minor tersebut. ID generasi 4.6 seperti `claude-sonnet-4-6` bukanlah alias. ID tersebut adalah snapshot itu sendiri.

Setiap ID model, baik bertanggal maupun tanpa tanggal, memiliki jadwal deprekasi dan penghentian tersendiri yang berbeda.

## Bobot model versus infrastruktur penyajian

Bobot model bersifat tetap untuk ID tertentu, tetapi infrastruktur penyajian di sekitar model dapat berubah seiring waktu. Infrastruktur ini mencakup komponen seperti router permintaan, pengklasifikasi keamanan, dan logika sampling.

Sesekali, pembaruan infrastruktur menghasilkan perbedaan kecil dalam perilaku yang dapat diamati meskipun ID model dan bobotnya tidak berubah. Jika Anda melihat perbedaan perilaku yang tidak terduga pada ID model yang sebelumnya stabil, pembaruan infrastruktur adalah penyebab yang paling mungkin.

## ID model saat ini

Untuk daftar lengkap ID model saat ini beserta padanannya di Amazon Bedrock dan Google Cloud, lihat [Ikhtisar model](/docs/id/about-claude/models/overview).
