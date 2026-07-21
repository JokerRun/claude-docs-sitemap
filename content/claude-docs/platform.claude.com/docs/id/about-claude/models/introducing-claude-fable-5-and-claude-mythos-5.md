---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 4b6ecf519a0b6a582187110a63eb396f80ecc34615c4ed1b6a4e3bb8f9dd392a
---

# Memperkenalkan Claude Fable 5 dan Claude Mythos 5

Kemampuan, perubahan API, dan ketersediaan Claude Fable 5 dan Claude Mythos 5.

---

<Tip>
  Akses ke Claude Fable 5 dan Claude Mythos 5 telah dipulihkan. Lihat [pernyataan kami](https://www.anthropic.com/news/redeploying-fable-5) untuk informasi lebih lanjut.
</Tip>

Claude Fable 5 adalah model Anthropic paling mumpuni yang dirilis secara luas, dibangun untuk pekerjaan penalaran paling menuntut dan tugas agentik jangka panjang. Claude Mythos 5 memiliki kemampuan yang sama dan hanya tersedia dalam rilis terbatas melalui [Project Glasswing](https://anthropic.com/glasswing).

Perubahan utama untuk integrasi: Claude Fable 5 menyertakan pengklasifikasi keamanan yang dapat menolak permintaan. Claude Mythos 5 tidak menyertakan pengklasifikasi ini. Jika integrasi Anda memanggil Claude Fable 5, rencanakan tiga perubahan: penanganan respons baru untuk penolakan, opsi "fallback" (cadangan) untuk mencoba ulang pada model Claude lain, dan aturan penagihan baru. [Penolakan, fallback, dan penagihan pada Claude Fable 5](#refusals-fallback-and-billing-on-claude-fable-5) merangkum ketiganya.

## Model

| Model           | ID model API      | Deskripsi                                                                                                                                             |
| --------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Fable 5  | `claude-fable-5`  | Model Anthropic paling mumpuni yang dirilis secara luas, untuk pekerjaan penalaran paling menuntut dan tugas agentik jangka panjang                   |
| Claude Mythos 5 | `claude-mythos-5` | Memiliki kemampuan yang sama dengan Claude Fable 5 tanpa pengklasifikasi keamanan. Tersedia melalui Project Glasswing. Penerus Claude Mythos Preview. |

Claude Fable 5 dan Claude Mythos 5 memiliki spesifikasi dan harga yang sama:

* **Jendela konteks dan output:** [jendela konteks 1 juta token](/docs/id/build-with-claude/context-windows) secara default, dan hingga 128 ribu token output per permintaan.
* **Harga:** $10 per juta token input dan $50 per juta token output.

Untuk spesifikasi di seluruh model saat ini, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

## Penolakan, fallback, dan penagihan pada Claude Fable 5

Claude Fable 5 menyertakan pengklasifikasi keamanan yang dapat menolak permintaan tertentu. Claude Mythos 5 tidak menyertakan pengklasifikasi ini, sehingga bagian ini hanya berlaku untuk Claude Fable 5. Bagian-bagian berikut merangkum apa arti penolakan bagi integrasi Anda; masing-masing menautkan ke panduan lengkap.

### Penolakan

Ketika Claude Fable 5 menolak permintaan, Messages API mengembalikan `stop_reason: "refusal"` sebagai respons HTTP 200 yang berhasil, bukan sebagai error. Respons tersebut juga melaporkan pengklasifikasi mana yang menolak permintaan. Lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback) untuk bentuk respons dan panduan penanganan.

### Fallback

Permintaan yang ditolak oleh Claude Fable 5 biasanya dapat dilayani oleh model Claude lain. Ada tiga cara untuk mencoba ulang:

* **Sisi server:** Kirimkan parameter `fallbacks` agar API mencoba ulang untuk Anda (dalam versi beta pada Claude API dan Claude Platform on AWS). Lihat [Fallback sisi server](/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback).
* **Sisi klien:** Gunakan [middleware SDK](/docs/id/cli-sdks-libraries/middleware) (TypeScript, Python, Go, Java, dan C#) untuk mencoba ulang dari klien pada platform apa pun. Lihat [Fallback sisi klien](/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback).
* **Manual:** Bangun sendiri mekanisme percobaan ulang, pada platform apa pun dan dalam bahasa apa pun. Lihat [Kredit fallback](/docs/id/build-with-claude/fallback-credit).

### Penagihan

Anda tidak ditagih untuk permintaan yang ditolak sebelum output apa pun dihasilkan. Ketika Anda mencoba ulang pada model lain, [kredit fallback](/docs/id/build-with-claude/fallback-credit) mengembalikan biaya cache prompt akibat peralihan, sehingga Anda terhindar dari membayar biaya tersebut dua kali.

## Ketersediaan

Claude Fable 5 dan Claude Mythos 5 keduanya tersedia mulai 9 Juni 2026:

* **Claude Fable 5** tersedia secara umum pada Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).
* **Claude Mythos 5** tidak tersedia secara umum: model ini ditawarkan dalam ketersediaan terbatas kepada pelanggan yang disetujui dalam [Project Glasswing](https://anthropic.com/glasswing). Untuk mendapatkan akses, hubungi tim akun Anthropic, AWS, atau Google Cloud Anda. Pelanggan yang tidak memiliki akses ke Claude Mythos 5 dapat menggunakan Claude Fable 5, yang tersedia secara umum dan menawarkan kemampuan yang sama.

Claude Fable 5 dan Claude Mythos 5 memiliki retensi data 30 hari dan tidak tersedia dengan retensi data nol: keduanya ditetapkan sebagai [Covered Models](https://support.claude.com/en/articles/15425695). Lihat [Persyaratan retensi data khusus model](/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

## Bekerja dengan Claude Fable 5 dan Claude Mythos 5

### Prompting

Claude Fable 5 merespons teknik prompting yang sama seperti model Claude lainnya, dengan beberapa perbedaan dalam cara menyusun prompt konteks panjang dan instruksi penalaran. Lihat [Prompting Claude Fable 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5).

## Messages API pada Claude Fable 5 dan Claude Mythos 5

<Note>
  Perilaku dalam bagian ini khusus untuk Claude Fable 5 dan Claude Mythos 5. Messages API tidak berubah untuk model Opus, Sonnet, dan Haiku.
</Note>

### Adaptive thinking selalu aktif

[Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (pemikiran adaptif) adalah satu-satunya mode pemikiran pada Claude Fable 5 dan Claude Mythos 5. Mode ini berlaku setiap kali parameter `thinking` tidak disetel. `thinking: {"type": "disabled"}` tidak didukung. Gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran.

### Konten pemikiran mentah tidak pernah dikembalikan

Rantai pemikiran mentah tidak pernah dikembalikan pada Claude Fable 5 dan Claude Mythos 5. Pengaturan `thinking.display` mengontrol apa yang dimuat dalam blok pemikiran sebagai gantinya:

* `"summarized"` mengembalikan blok pemikiran dengan ringkasan penalaran yang mudah dibaca.
* `"omitted"` (default) mengembalikan blok pemikiran dengan field `thinking` kosong.

Kirimkan kembali blok pemikiran tanpa perubahan dalam percakapan multi-giliran pada model yang sama. Lihat [output pemikiran pada Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) untuk penanganan lintas model.

## Fitur yang didukung

Saat peluncuran, Claude Fable 5 dan Claude Mythos 5 mendukung:

* [Effort](/docs/id/build-with-claude/effort)
* [Task budgets](/docs/id/build-with-claude/task-budgets) (beta: setel header `task-budgets-2026-03-13`)
* [Memory tool](/docs/id/agents-and-tools/tool-use/memory-tool)
* [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool)
* [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling)
* Pembersihan hasil alat melalui [pengeditan konteks](/docs/id/build-with-claude/context-editing) (beta: setel header `context-management-2025-06-27`)
* [Compaction](/docs/id/build-with-claude/compaction)
* [Vision](/docs/id/build-with-claude/vision)

## Migrasi dari model sebelumnya

Instruksi langkah demi langkah tersedia dalam panduan migrasi:

* Dari Claude Mythos Preview: lihat [Migrasi dari Claude Mythos Preview ke Claude Mythos 5](/docs/id/about-claude/models/migration-guide#migrating-from-claude-mythos-preview).
* Dari Claude Opus 4.8: lihat [Migrasi dari Claude Opus 4.8 ke Claude Fable 5](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-48).

## Langkah selanjutnya

<CardGroup>
  <Card title="Panduan migrasi" icon="arrow-right" href="/docs/id/about-claude/models/migration-guide">
    Instruksi upgrade langkah demi langkah dari Claude Opus 4.8 dan Claude Mythos Preview.
  </Card>

  <Card title="Ikhtisar model" icon="settings" href="/docs/id/about-claude/models/overview">
    Spesifikasi dan perbandingan untuk semua model Claude saat ini.
  </Card>

  <Card title="Adaptive thinking" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Satu-satunya mode pemikiran pada Claude Fable 5 dan Claude Mythos 5.
  </Card>

  <Card title="Penolakan dan fallback" icon="shield" href="/docs/id/build-with-claude/refusals-and-fallback">
    Bagaimana Claude Fable 5 menolak permintaan, dan cara mencoba ulang pada model lain.
  </Card>

  <Card title="Kredit fallback" icon="coins" href="/docs/id/build-with-claude/fallback-credit">
    Hindari membayar biaya cache prompt dua kali saat mencoba ulang.
  </Card>

  <Card title="Cookbook fallback dan penagihan" icon="book-open" href="https://platform.claude.com/cookbook/fable-5-fallback-billing-guide">
    Contoh lengkap end-to-end untuk penanganan penolakan, fallback, dan penagihan.
  </Card>

  <Card title="Effort" icon="sliders" href="/docs/id/build-with-claude/effort">
    Kontrol kedalaman pemikiran dan biaya pada Claude Fable 5 dan Claude Mythos 5.
  </Card>

  <Card title="Prompting Claude Fable 5" icon="terminal" href="/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5">
    Teknik prompting khusus Fable.
  </Card>
</CardGroup>
