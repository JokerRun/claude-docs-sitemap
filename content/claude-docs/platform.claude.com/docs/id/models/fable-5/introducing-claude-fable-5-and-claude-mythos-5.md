---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: f763564224aab87e26142cae78796e88638a163e8550f29fb10c4c5e68c7f186
---

---
title: Memperkenalkan Claude Fable 5 dan Claude Mythos 5
url: https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5
description: Kemampuan, perubahan API, dan ketersediaan Claude Fable 5 dan Claude Mythos 5.
---

<Note>
  Claude Fable 5.1 dan Claude Mythos 5.1 dibangun di atas model-model ini. Lihat [Yang baru di Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1).
</Note>

<Tip>
  Akses ke Claude Fable 5 dan Claude Mythos 5 telah dipulihkan. Lihat [pernyataan kami](https://www.anthropic.com/news/redeploying-fable-5) untuk informasi lebih lanjut.
</Tip>

Claude Fable 5 dibangun untuk penalaran yang menuntut dan pekerjaan agentik berjangka panjang. Claude Mythos 5 memiliki kemampuan yang sama dan hanya tersedia dalam rilis terbatas melalui [Project Glasswing](https://anthropic.com/glasswing).

Perubahan utama untuk integrasi: Claude Fable 5 menyertakan pengklasifikasi keamanan yang dapat menolak permintaan. Claude Mythos 5 tidak menyertakan pengklasifikasi ini. Jika integrasi Anda memanggil Claude Fable 5, rencanakan tiga perubahan: penanganan respons baru untuk penolakan, opsi fallback untuk mencoba ulang pada model Claude lain, dan aturan penagihan baru. [Penolakan, fallback, dan penagihan pada Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5#refusals-fallback-and-billing-on-claude-fable-5) merangkum ketiganya.

## Model

| Model           | ID model API      | Deskripsi                                                                                                                                             |
| --------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Fable 5  | `claude-fable-5`  | Dibangun untuk penalaran yang menuntut dan pekerjaan agentik berjangka panjang                                                                        |
| Claude Mythos 5 | `claude-mythos-5` | Memiliki kemampuan yang sama dengan Claude Fable 5 tanpa pengklasifikasi keamanan. Tersedia melalui Project Glasswing. Penerus Claude Mythos Preview. |

Claude Fable 5 dan Claude Mythos 5 memiliki spesifikasi dan harga yang sama:

* **Jendela konteks dan output:** "context window" (jendela konteks) [1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, dan hingga 128 ribu token output per permintaan.
* **Harga:** $10 USD per juta token input dan $50 USD per juta token output.

Untuk spesifikasi semua model saat ini, lihat [ikhtisar model](https://platform.claude.com/docs/id/models/overview).

## Penolakan, fallback, dan penagihan pada Claude Fable 5

Claude Fable 5 menyertakan pengklasifikasi keamanan yang dapat menolak permintaan tertentu. Claude Mythos 5 tidak menyertakan pengklasifikasi ini, sehingga bagian ini hanya berlaku untuk Claude Fable 5. Bagian-bagian berikut merangkum apa arti penolakan bagi integrasi Anda. Masing-masing menautkan ke panduan lengkapnya.

### Penolakan

Ketika Claude Fable 5 menolak permintaan, Messages API mengembalikan `stop_reason: "refusal"` sebagai respons HTTP 200 yang berhasil, bukan error. Respons tersebut juga melaporkan pengklasifikasi mana yang menolak permintaan. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) untuk bentuk respons dan panduan penanganan.

### Fallback

Permintaan yang ditolak Claude Fable 5 biasanya dapat dilayani oleh model Claude lain. Ada tiga cara untuk mencoba ulang:

* **Sisi server:** Berikan parameter `fallbacks` agar API mencoba ulang untuk Anda, menggunakan mode `"default"` untuk model yang direkomendasikan Anthropic atau menyebutkan model pilihan Anda sendiri (dalam beta di Claude API). Lihat [Fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback).
* **Sisi klien:** Gunakan [middleware SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/middleware) untuk mencoba ulang dari klien di platform apa pun. Lihat [Fallback sisi klien](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback).
* **Manual:** Bangun sendiri mekanisme coba ulang, di platform apa pun dan dalam bahasa apa pun. Lihat [Kredit fallback](https://platform.claude.com/docs/id/build-with-claude/fallback-credit).

### Penagihan

Anda tidak ditagih untuk permintaan yang ditolak sebelum output apa pun dihasilkan. Ketika Anda mencoba ulang pada model lain, [kredit fallback](https://platform.claude.com/docs/id/build-with-claude/fallback-credit) mengembalikan biaya prompt-cache akibat perpindahan, sehingga Anda tidak membayar biaya tersebut dua kali.

## Ketersediaan

* **Claude Fable 5** tersedia di Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry).
* **Claude Mythos 5** hanya ditawarkan kepada pelanggan yang disetujui dalam [Project Glasswing](https://anthropic.com/glasswing). Untuk akses, hubungi tim akun Anthropic, AWS, atau Google Cloud Anda. Pelanggan tanpa akses ke Claude Mythos 5 dapat menggunakan Claude Fable 5, yang tidak memerlukan persetujuan akses dan menawarkan kemampuan yang sama.

Claude Fable 5 dan Claude Mythos 5 memiliki retensi data 30 hari dan tidak tersedia dengan retensi data nol kecuali diizinkan secara tegas oleh Anthropic. Keduanya ditetapkan sebagai [Covered Models](https://support.claude.com/en/articles/15425695). Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

## Prompting

Claude Fable 5 merespons teknik prompting yang sama seperti model Claude lainnya, dengan beberapa perbedaan dalam cara menyusun prompt konteks panjang dan instruksi penalaran. Lihat [Prompting Claude Fable 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5).

## Messages API pada Claude Fable 5 dan Claude Mythos 5

### Pemikiran adaptif selalu aktif

Claude Fable 5 dan Claude Mythos 5 selalu mengaktifkan pemikiran. Memberikan `thinking: {"type": "disabled"}` tidak didukung. Untuk mengurangi atau mengontrol kedalaman pemikiran, gunakan parameter [effort](https://platform.claude.com/docs/id/build-with-claude/effort).

### Konten pemikiran mentah tidak pernah dikembalikan

Rantai pemikiran mentah tidak pernah dikembalikan pada Claude Fable 5 dan Claude Mythos 5. Pengaturan `thinking.display` mengontrol apa yang dimuat blok pemikiran sebagai gantinya:

* `"summarized"` mengembalikan blok pemikiran dengan ringkasan penalaran yang dapat dibaca.
* `"omitted"` (default) mengembalikan blok pemikiran dengan field `thinking` kosong.

Kirimkan kembali blok pemikiran tanpa perubahan dalam percakapan multi-giliran pada model yang sama. Lihat [output pemikiran pada Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) untuk penanganan lintas model.

## Fitur yang didukung

Claude Fable 5 dan Claude Mythos 5 mendukung:

* [Effort](https://platform.claude.com/docs/id/build-with-claude/effort)
* [Anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (beta: atur header `task-budgets-2026-03-13`)
* [Alat memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool)
* [Eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool)
* [Pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling)
* Pembersihan hasil alat melalui [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) (beta: atur header `context-management-2025-06-27`)
* [Pemadatan](https://platform.claude.com/docs/id/build-with-claude/compaction)
* [Visi](https://platform.claude.com/docs/id/build-with-claude/vision)

## Migrasi dari model sebelumnya

Instruksi langkah demi langkah tersedia di panduan migrasi:

* Dari Claude Mythos Preview: lihat [Migrasi dari Claude Mythos Preview ke Claude Mythos 5](https://platform.claude.com/docs/id/models/fable-5/migration-guide#migrating-from-claude-mythos-preview).
* Dari Claude Opus 4.8: lihat [Migrasi dari Claude Opus 4.8 ke Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/migration-guide#migrating-from-claude-opus-48).

## Langkah selanjutnya

<CardGroup>
  <Card title="Ikhtisar model" icon="settings" href="https://platform.claude.com/docs/id/models/overview">
    Spesifikasi dan perbandingan untuk semua model Claude saat ini.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Satu-satunya mode pemikiran pada Claude Fable 5 dan Claude Mythos 5.
  </Card>

  <Card title="Penolakan dan fallback" icon="shield" href="https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback">
    Bagaimana Claude Fable 5 menolak permintaan, dan cara mencoba ulang pada model lain.
  </Card>

  <Card title="Kredit fallback" icon="coins" href="https://platform.claude.com/docs/id/build-with-claude/fallback-credit">
    Hindari membayar biaya prompt-cache dua kali saat mencoba ulang.
  </Card>

  <Card title="Cookbook fallback dan penagihan" icon="book-open" href="https://platform.claude.com/cookbook/fable-5-fallback-billing-guide">
    Contoh lengkap dari awal hingga akhir tentang penanganan penolakan, fallback, dan penagihan.
  </Card>

  <Card title="Effort" icon="sliders" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kontrol kedalaman pemikiran dan biaya pada Claude Fable 5 dan Claude Mythos 5.
  </Card>

  <Card title="Prompting Claude Fable 5" icon="terminal" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5">
    Teknik prompting khusus Fable.
  </Card>
</CardGroup>
