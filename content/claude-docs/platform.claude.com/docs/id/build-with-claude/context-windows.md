---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/context-windows
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 4567c46eba5a09bd83183c444ff077375a3c1c7169b9936392e3f3078b1f0e00
---

# Jendela konteks

Pelajari cara mengelola jendela konteks saat percakapan berkembang, termasuk strategi kompaksi dan pengeditan konteks.

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Seiring percakapan berkembang, Anda pada akhirnya akan mendekati batas jendela konteks. Panduan ini menjelaskan cara kerja jendela konteks dan memperkenalkan strategi untuk mengelolanya secara efektif.

Untuk percakapan jangka panjang dan alur kerja agentic, [kompaksi sisi server](/docs/id/build-with-claude/compaction) adalah strategi utama untuk manajemen konteks. Untuk kebutuhan yang lebih khusus, [pengeditan konteks](/docs/id/build-with-claude/context-editing) menawarkan strategi tambahan seperti pembersihan hasil alat dan pembersihan blok pemikiran.

## Memahami jendela konteks

"Jendela konteks" mengacu pada semua teks yang dapat direferensikan model bahasa saat menghasilkan respons, termasuk respons itu sendiri. Ini berbeda dari corpus data besar tempat model bahasa dilatih, dan sebaliknya mewakili "memori kerja" untuk model. Jendela konteks yang lebih besar memungkinkan model menangani prompt yang lebih kompleks dan panjang, tetapi lebih banyak konteks tidak secara otomatis lebih baik. Seiring jumlah token bertambah, akurasi dan recall menurun, fenomena yang dikenal sebagai *context rot*. Ini membuat kurasi apa yang ada dalam konteks sama pentingnya dengan berapa banyak ruang yang tersedia.

Claude mencapai hasil canggih pada benchmark pengambilan konteks panjang seperti [MRCR](https://arxiv.org/abs/2501.03276) dan [GraphWalks](https://arxiv.org/abs/2412.04360), tetapi keuntungan ini bergantung pada apa yang ada dalam konteks, bukan hanya berapa banyak yang muat.

<Tip>
Untuk pendalaman tentang mengapa konteks panjang menurun dan cara merekayasa di sekitarnya, lihat [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Diagram di bawah mengilustrasikan perilaku jendela konteks standar untuk permintaan API<sup>1</sup>:

![Diagram jendela konteks](/docs/images/context-window.svg)

_<sup>1</sup>Untuk antarmuka obrolan, seperti untuk [claude.ai](https://claude.ai/), jendela konteks juga dapat diatur pada sistem "first in, first out" yang bergulir._

* **Akumulasi token progresif:** Seiring percakapan maju melalui giliran, setiap pesan pengguna dan respons asisten terakumulasi dalam jendela konteks. Giliran sebelumnya dipertahankan sepenuhnya.
* **Pola pertumbuhan linier:** Penggunaan konteks tumbuh secara linier dengan setiap giliran, dengan giliran sebelumnya dipertahankan sepenuhnya.
* **Kapasitas jendela konteks:** Total jendela konteks yang tersedia (hingga 1M token) mewakili kapasitas maksimum untuk menyimpan riwayat percakapan dan menghasilkan output baru dari Claude.
* **Aliran input-output:** Setiap giliran terdiri dari:
  - **Fase input:** Berisi semua riwayat percakapan sebelumnya ditambah pesan pengguna saat ini
  - **Fase output:** Menghasilkan respons teks yang menjadi bagian dari input masa depan

## Jendela konteks dengan pemikiran yang diperluas

Saat menggunakan [pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking), semua token input dan output, termasuk token yang digunakan untuk pemikiran, dihitung terhadap batas jendela konteks, dengan beberapa nuansa dalam situasi multi-giliran.

Token anggaran pemikiran adalah subset dari parameter `max_tokens` Anda, ditagih sebagai token output, dan dihitung terhadap batas laju. Dengan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking), Claude secara dinamis memutuskan alokasi pemikirannya, jadi penggunaan token pemikiran aktual mungkin berbeda per permintaan.

Namun, blok pemikiran sebelumnya secara otomatis dilepas dari perhitungan jendela konteks oleh Claude API dan bukan bagian dari riwayat percakapan yang "dilihat" model untuk giliran berikutnya, melestarikan kapasitas token untuk konten percakapan aktual.

Diagram di bawah mendemonstrasikan manajemen token khusus saat pemikiran yang diperluas diaktifkan:

![Diagram jendela konteks dengan pemikiran yang diperluas](/docs/images/context-window-thinking.svg)

* **Melepas pemikiran yang diperluas:** Blok pemikiran yang diperluas (ditampilkan dalam abu-abu gelap) dihasilkan selama fase output setiap giliran, **tetapi tidak dibawa maju sebagai token input untuk giliran berikutnya**. Anda tidak perlu melepas blok pemikiran sendiri. Claude API secara otomatis melakukan ini untuk Anda jika Anda meneruskannya kembali.
* **Detail implementasi teknis:**
  - API secara otomatis mengecualikan blok pemikiran dari giliran sebelumnya saat Anda meneruskannya kembali sebagai bagian dari riwayat percakapan.
  - Token pemikiran yang diperluas ditagih sebagai token output hanya sekali, selama generasinya.
  - Perhitungan jendela konteks yang efektif menjadi: `context_window = (input_tokens - previous_thinking_tokens) + current_turn_tokens`.
  - Token pemikiran mencakup blok `thinking`.

Arsitektur ini efisien token dan memungkinkan penalaran ekstensif tanpa pemborosan token, karena blok pemikiran dapat memiliki panjang yang substansial.

<Note>
Anda dapat membaca lebih lanjut tentang jendela konteks dan pemikiran yang diperluas dalam [panduan pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking).
</Note>

## Jendela konteks dengan pemikiran yang diperluas dan penggunaan alat

Diagram di bawah mengilustrasikan manajemen token jendela konteks saat menggabungkan pemikiran yang diperluas dengan penggunaan alat:

![Diagram jendela konteks dengan pemikiran yang diperluas dan penggunaan alat](/docs/images/context-window-thinking-tools.svg)

<Steps>
  <Step title="Arsitektur giliran pertama">
    - **Komponen input:** Konfigurasi alat dan pesan pengguna
    - **Komponen output:** Pemikiran yang diperluas + respons teks + permintaan penggunaan alat
    - **Perhitungan token:** Semua komponen input dan output dihitung terhadap jendela konteks, dan semua komponen output ditagih sebagai token output.
  </Step>
  <Step title="Penanganan hasil alat (giliran 2)">
    - **Komponen input:** Setiap blok dalam giliran pertama serta `tool_result`. Blok pemikiran yang diperluas **harus** dikembalikan dengan hasil alat yang sesuai. Ini adalah satu-satunya kasus di mana Anda **harus** mengembalikan blok pemikiran.
    - **Komponen output:** Setelah hasil alat telah diteruskan kembali ke Claude, Claude akan merespons dengan hanya teks (tidak ada pemikiran yang diperluas tambahan sampai pesan `user` berikutnya).
    - **Perhitungan token:** Semua komponen input dan output dihitung terhadap jendela konteks, dan semua komponen output ditagih sebagai token output.
  </Step>
  <Step title="Langkah Ketiga">
    - **Komponen input:** Semua input dan output dari giliran sebelumnya dibawa maju dengan pengecualian blok pemikiran, yang dapat dijatuhkan sekarang bahwa Claude telah menyelesaikan seluruh siklus penggunaan alat. API akan secara otomatis melepas blok pemikiran untuk Anda jika Anda meneruskannya kembali, atau Anda dapat melepasnya sendiri pada tahap ini. Ini juga di mana Anda akan menambahkan giliran `User` berikutnya.
    - **Komponen output:** Karena ada giliran `User` baru di luar siklus penggunaan alat, Claude menghasilkan blok pemikiran yang diperluas baru dan melanjutkan dari sana.
    - **Perhitungan token:** Token pemikiran sebelumnya secara otomatis dilepas dari perhitungan jendela konteks. Semua blok sebelumnya lainnya masih dihitung sebagai bagian dari jendela token, dan blok pemikiran dalam giliran `Assistant` saat ini dihitung sebagai bagian dari jendela konteks.
  </Step>
</Steps>

* **Pertimbangan untuk penggunaan alat dengan pemikiran yang diperluas:**
  - Saat memposting hasil alat, seluruh blok pemikiran yang tidak dimodifikasi yang menyertai permintaan alat spesifik itu (termasuk bagian tanda tangan) harus disertakan.
  - Perhitungan jendela konteks yang efektif untuk pemikiran yang diperluas dengan penggunaan alat menjadi: `context_window = input_tokens + current_turn_tokens`.
  - Sistem menggunakan tanda tangan kriptografi untuk memverifikasi keaslian blok pemikiran. Gagal melestarikan blok pemikiran selama penggunaan alat dapat memecahkan kontinuitas penalaran Claude. Dengan demikian, jika Anda memodifikasi blok pemikiran, API mengembalikan kesalahan.

<Note>
Model Claude 4 mendukung [pemikiran yang disisipi](/docs/id/build-with-claude/extended-thinking#interleaved-thinking), yang memungkinkan Claude untuk berpikir di antara panggilan alat dan melakukan penalaran yang lebih canggih setelah menerima hasil alat.

Claude Sonnet 3.7 tidak mendukung pemikiran yang disisipi, jadi tidak ada penyisipan pemikiran yang diperluas dan panggilan alat tanpa giliran pengguna non-`tool_result` di antaranya.

Untuk informasi lebih lanjut tentang menggunakan alat dengan pemikiran yang diperluas, lihat [panduan pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use).
</Note>

[Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6 memiliki jendela konteks 1M-token. Model Claude lainnya, termasuk Claude Sonnet 4.5 dan Sonnet 4 (deprecated), memiliki jendela konteks 200k-token.

Satu permintaan dapat mencakup hingga 600 gambar atau halaman PDF (100 untuk model dengan jendela konteks 200k-token). Saat mengirim banyak gambar atau dokumen besar, Anda mungkin mendekati [batas ukuran permintaan](/docs/id/api/overview#request-size-limits) sebelum batas token.

## Kesadaran konteks dalam Claude Sonnet 4.6, Sonnet 4.5, dan Haiku 4.5

Claude Sonnet 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5 menampilkan **kesadaran konteks**. Kemampuan ini memungkinkan model ini melacak jendela konteks yang tersisa mereka (yaitu "anggaran token") sepanjang percakapan. Ini memungkinkan Claude untuk menjalankan tugas dan mengelola konteks lebih efektif dengan memahami berapa banyak ruang yang dimilikinya untuk bekerja. Claude dilatih untuk menggunakan konteks ini dengan tepat, bertahan dalam tugas sampai akhir daripada menebak berapa banyak token yang tersisa. Bagi model, kurangnya kesadaran konteks seperti berkompetisi dalam acara memasak tanpa jam. Model Claude 4.5+ mengubah ini dengan secara eksplisit menginformasikan model tentang konteks yang tersisa, sehingga dapat memanfaatkan token yang tersedia secara maksimal.

**Cara kerjanya:**

Di awal percakapan, Claude menerima informasi tentang total jendela konteksnya:

```xml
<budget:token_budget>1000000</budget:token_budget>
```

Anggaran diatur ke 1M token (200k untuk model dengan jendela konteks yang lebih kecil).

Setelah setiap panggilan alat, Claude menerima pembaruan tentang kapasitas yang tersisa:

```xml
<system_warning>Token usage: 35000/1000000; 965000 remaining</system_warning>
```

Kesadaran ini membantu Claude menentukan berapa banyak kapasitas yang tersisa untuk pekerjaan dan memungkinkan eksekusi yang lebih efektif pada tugas jangka panjang. Token gambar disertakan dalam anggaran ini.

**Manfaat:**

Kesadaran konteks sangat berharga untuk:
- Sesi agen jangka panjang yang memerlukan fokus berkelanjutan
- Alur kerja multi-jendela-konteks di mana transisi status penting
- Tugas kompleks yang memerlukan manajemen token yang hati-hati

<Tip>
Untuk agen yang mencakup beberapa sesi, rancang artefak status Anda sehingga pemulihan konteks cepat saat sesi baru dimulai. [Pola multi-sesi alat memori](/docs/id/agents-and-tools/tool-use/memory-tool#multi-session-software-development-pattern) menjelaskan pendekatan konkret. Lihat juga [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
</Tip>

Untuk panduan prompting tentang memanfaatkan kesadaran konteks, lihat [panduan praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#context-awareness-and-multi-window-workflows).

## Mengelola konteks dengan kompaksi

Jika percakapan Anda secara teratur mendekati batas jendela konteks, [kompaksi sisi server](/docs/id/build-with-claude/compaction) adalah pendekatan yang direkomendasikan. Kompaksi menyediakan peringkasan sisi server yang secara otomatis mengondensasi bagian awal percakapan, memungkinkan percakapan jangka panjang melampaui batas konteks dengan pekerjaan integrasi minimal. Saat ini tersedia dalam beta untuk Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6.

Untuk kebutuhan yang lebih khusus, [pengeditan konteks](/docs/id/build-with-claude/context-editing) menawarkan strategi tambahan:
- **Pembersihan hasil alat** - Hapus hasil alat lama dalam alur kerja agentic
- **Pembersihan blok pemikiran** - Kelola blok pemikiran dengan pemikiran yang diperluas

## Manajemen jendela konteks dengan model Claude yang lebih baru

Model Claude yang lebih baru (dimulai dengan Claude Sonnet 3.7) mengembalikan kesalahan validasi saat token prompt dan output melebihi jendela konteks, daripada secara diam-diam memotong. Perubahan ini memberikan perilaku yang lebih dapat diprediksi tetapi memerlukan manajemen token yang lebih hati-hati.

Gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting) untuk memperkirakan penggunaan token sebelum mengirim pesan ke Claude. Ini membantu Anda merencanakan dan tetap dalam batas jendela konteks.

Lihat tabel [perbandingan model](/docs/id/about-claude/models/overview#latest-models-comparison) untuk daftar ukuran jendela konteks menurut model.

## Langkah berikutnya
<CardGroup cols={2}>
  <Card title="Kompaksi" icon="compress" href="/docs/id/build-with-claude/compaction">
    Strategi yang direkomendasikan untuk mengelola konteks dalam percakapan jangka panjang.
  </Card>
  <Card title="Pengeditan konteks" icon="pen" href="/docs/id/build-with-claude/context-editing">
    Strategi butir halus seperti pembersihan hasil alat dan pembersihan blok pemikiran.
  </Card>
  <Card title="Tabel perbandingan model" icon="scales" href="/docs/id/about-claude/models/overview#latest-models-comparison">
    Lihat tabel perbandingan model untuk daftar ukuran jendela konteks dan harga token input / output menurut model.
  </Card>
  <Card title="Ikhtisar pemikiran yang diperluas" icon="settings" href="/docs/id/build-with-claude/extended-thinking">
    Pelajari lebih lanjut tentang cara kerja pemikiran yang diperluas dan cara mengimplementasikannya bersama fitur lain seperti penggunaan alat dan caching prompt.
  </Card>
</CardGroup>