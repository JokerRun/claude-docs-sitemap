---
source: platform
url: https://platform.claude.com/docs/id/models/haiku-4-5/migration-guide
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: b0fb6e1090079cd55b027d85287f2df147554bfa7913b66e32f948ddefde895a
---

---
title: Migrasi ke Claude Haiku 4.5
url: https://platform.claude.com/docs/id/models/haiku-4-5/migration-guide
description: "Migrasi ke Claude Haiku 4.5 dari model Haiku sebelumnya: ID model, perubahan yang merusak kompatibilitas, dan daftar periksa migrasi."
---

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan skill Claude API.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) bawaan. Skill ini berfungsi untuk model Claude terkini mana pun sebagai target:

  ```text wrap
  /claude-api migrate this project to claude-haiku-4-5
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, serta kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa berisi item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, sebuah subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock dan Claude Platform on AWS serta menyesuaikan format ID model dan perubahan fitur untuk platform tersebut.
</Tip>

Claude Haiku 4.5 adalah model Haiku tercepat dan tercerdas dengan performa mendekati frontier, menghadirkan kualitas model premium untuk aplikasi interaktif dan pemrosesan bervolume tinggi.

Untuk gambaran lengkap tentang kemampuannya, lihat [ikhtisar model](https://platform.claude.com/docs/id/models/overview).

<Note>
  Untuk harga Claude Haiku 4.5, lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).
</Note>

<Tip>
  Untuk peningkatan performa yang signifikan pada tugas pengodean dan penalaran, pertimbangkan untuk mengaktifkan "extended thinking" (pemikiran diperpanjang) dengan `thinking: {type: "enabled", budget_tokens: N}`.
</Tip>

<Note>
  Pemikiran diperpanjang memengaruhi efisiensi ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#caching-with-thinking-blocks).

  Pemikiran diperpanjang tidak lagi direkomendasikan (deprecated) pada model Claude 4.6 dan dihapus pada Claude Opus 4.7. Jika menggunakan model yang lebih baru, gunakan [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) sebagai gantinya.
</Note>

## Migrasi ke Claude Haiku 4.5 dari Claude Haiku 3.5 dan model Haiku sebelumnya

**Perbarui nama model Anda:**

```python
# Dari Haiku 3.5
model = "claude-3-5-haiku-20241022"  # Before
model = "claude-haiku-4-5-20251001"  # After
```

**Tinjau batas laju baru:** Haiku 4.5 memiliki "rate limit" (batas laju) yang terpisah dari Haiku 3.5. Lihat dokumentasi [Batas laju](https://platform.claude.com/docs/id/api/rate-limits) untuk detailnya.

**Jelajahi kemampuan baru:** Lihat [ikhtisar model](https://platform.claude.com/docs/id/models/overview) untuk detail tentang kesadaran konteks, kapasitas output yang lebih besar (64k token), kecerdasan yang lebih tinggi, dan kecepatan yang lebih baik.

### Perubahan yang merusak kompatibilitas

Perubahan yang merusak kompatibilitas ini berlaku saat bermigrasi dari model Claude 3.x Haiku.

1. **Perbarui parameter sampling**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya. Mengatur keduanya akan mengembalikan error 400 pada Claude Haiku 4.5.

2. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus semua kode yang menggunakan perintah `undo_edit`.

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Haiku 4.5

* Perbarui ID model ke `claude-haiku-4-5-20251001`
* **MERUSAK KOMPATIBILITAS:** Perbarui versi alat ke yang terbaru (`text_editor_20250728`, `code_execution_20250825`); versi lama tidak didukung
* **MERUSAK KOMPATIBILITAS:** Hapus semua kode yang menggunakan perintah `undo_edit` (jika ada)
* **MERUSAK KOMPATIBILITAS:** Perbarui parameter sampling agar hanya menggunakan `temperature` ATAU `top_p`, bukan keduanya (mengatur keduanya akan mengembalikan error 400)
* Tangani stop reason `refusal` yang baru di aplikasi Anda
* Tinjau dan sesuaikan dengan batas laju baru (terpisah dari Haiku 3.5)
* Tinjau dan perbarui prompt dengan mengikuti [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* Pertimbangkan untuk mengaktifkan pemikiran diperpanjang untuk tugas penalaran yang kompleks
* Uji di lingkungan pengembangan sebelum deployment ke produksi
