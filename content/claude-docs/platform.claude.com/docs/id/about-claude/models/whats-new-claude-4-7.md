---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-claude-4-7
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 2d1a52f49aac559cc404bebb9b0bd5c9aab3b0a2601decb8d8f930b02a880310
---

# Apa yang baru di Claude Opus 4.7

Ikhtisar fitur baru, perubahan yang merusak, dan perubahan perilaku di Claude Opus 4.7.

---

Claude Opus 4.7 adalah model yang tersedia secara umum paling mampu hingga saat ini. Model ini sangat otonom dan berkinerja luar biasa pada pekerjaan agentic jangka panjang, pekerjaan pengetahuan, tugas visi, dan tugas memori. Halaman ini merangkum semua yang baru saat peluncuran.

## Model baru

| Model | ID model API | Deskripsi |
|:------|:-------------|:------------|
| Claude Opus 4.7 | `claude-opus-4-7` | Model yang tersedia secara umum paling mampu kami untuk penalaran kompleks dan pengkodean agentic |

Claude Opus 4.7 mendukung [jendela konteks token 1M](/docs/id/build-with-claude/context-windows), token output maksimal 128k, [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), dan set alat serta fitur platform yang sama dengan Claude Opus 4.6.

Untuk harga lengkap dan spesifikasi, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

## Fitur baru

### Dukungan gambar resolusi tinggi

Claude Opus 4.7 adalah model Claude pertama kami dengan dukungan gambar resolusi tinggi. Resolusi gambar maksimal telah meningkat menjadi **2576px / 3.75MP** (meningkat dari batas sebelumnya 1568px / 1.15MP). Perubahan ini harus membuka keuntungan kinerja pada beban kerja yang berat visi, dan sangat penting untuk penggunaan komputer dan alur kerja pemahaman tangkapan layar/artefak/dokumen.

Selain itu, operasi seperti pemetaan koordinat ke gambar sekarang lebih sederhana — koordinat model adalah 1:1 dengan piksel aktual, jadi tidak ada matematika faktor skala yang diperlukan.

Gambar resolusi tinggi menggunakan lebih banyak token. Jika kejelasan gambar tambahan tidak perlu, kurangi sampel gambar sebelum mengirim ke Claude untuk menghindari peningkatan penggunaan token.

Selain resolusi, Claude Opus 4.7 juga meningkat pada:

- **Persepsi tingkat rendah** — menunjuk, mengukur, menghitung, dan tugas serupa.
- **Lokalisasi gambar** — lokalisasi dan deteksi kotak pembatas gambar alami ditingkatkan.

Lihat [Gambar dan visi](/docs/id/build-with-claude/vision) untuk detail.

### Tingkat upaya `xhigh` baru

[Parameter upaya](/docs/id/build-with-claude/effort) memungkinkan Anda menyesuaikan kecerdasan Claude vs. pengeluaran token, menukar kemampuan untuk kecepatan lebih cepat dan biaya lebih rendah. Mulai dengan tingkat upaya `xhigh` baru untuk kasus penggunaan pengkodean dan agentic, dan gunakan upaya minimum `high` untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan. Lihat [Tingkat upaya yang direkomendasikan untuk Claude Opus 4.7](/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-4-7) untuk panduan per tingkat. (Hanya Messages API; Claude Managed Agents menangani upaya secara otomatis.)

### Anggaran tugas (beta)

Claude Opus 4.7 memperkenalkan [anggaran tugas](/docs/id/build-with-claude/task-budgets). Anggaran tugas memberikan Claude perkiraan kasar tentang berapa banyak token yang ditargetkan untuk loop agentic penuh, termasuk pemikiran, panggilan alat, hasil alat, dan output akhir. Model melihat hitungan mundur yang berjalan dan menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan tugas dengan anggun saat anggaran dikonsumsi. Untuk menggunakan, atur header beta `task-budgets-2026-03-13` dan tambahkan yang berikut ke konfigurasi output Anda:

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=128000,
    output_config={
        "effort": "high",
        "task_budget": {"type": "tokens", "total": 128000},
    },
    messages=[
        {"role": "user", "content": "Review the codebase and propose a refactor plan."}
    ],
    betas=["task-budgets-2026-03-13"],
)
```

Anda mungkin perlu bereksperimen dengan anggaran tugas yang berbeda untuk kasus penggunaan Anda. Jika model diberi anggaran tugas yang terlalu ketat untuk tugas tertentu, model mungkin menyelesaikan tugas dengan kurang menyeluruh atau menolak untuk melakukan tugas sama sekali.

Untuk tugas agentic terbuka di mana kualitas lebih penting daripada kecepatan, jangan atur anggaran tugas; cadangkan anggaran tugas untuk beban kerja di mana Anda memerlukan model untuk membatasi pekerjaan ke tunjangan token. Nilai minimum untuk anggaran tugas adalah 20k token.

Ini bukan batas keras; ini adalah saran yang disadari model. Ini berbeda dari `max_tokens`, yang merupakan batas keras per permintaan pada token yang dihasilkan (`max_tokens` tidak diteruskan ke model, dan model tidak menyadarinya), sementara `task_budget` adalah batas penasihat di seluruh loop agentic penuh. Gunakan `task_budget` ketika Anda ingin model untuk memoderasi diri sendiri, dan `max_tokens` sebagai batas per permintaan keras untuk membatasi penggunaan.

## Perubahan yang merusak

<Note>
Perubahan yang merusak ini hanya berlaku untuk Messages API. Jika Anda menggunakan Claude Managed Agents, tidak ada perubahan API yang merusak untuk Claude Opus 4.7.
</Note>

### Anggaran pemikiran yang diperpanjang dihapus

Anggaran pemikiran yang diperpanjang dihapus di Claude Opus 4.7. Menetapkan `thinking: {"type": "enabled", "budget_tokens": N}` akan mengembalikan kesalahan 400. [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) adalah satu-satunya mode pemikiran-on, dan dalam evaluasi internal kami secara andal mengungguli pemikiran yang diperpanjang.

```python Python
# Sebelumnya (Opus 4.6)
thinking = {"type": "enabled", "budget_tokens": 32000}

# Sesudahnya (Opus 4.7)
thinking = {"type": "adaptive"}
output_config = {"effort": "high"}
```

Adaptive thinking **dimatikan secara default** di Claude Opus 4.7. Permintaan tanpa bidang `thinking` berjalan tanpa pemikiran. Atur `thinking: {type: "adaptive"}` secara eksplisit untuk mengaktifkannya.

### Parameter sampling dihapus

Mulai dengan Claude Opus 4.7, menetapkan `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun akan mengembalikan kesalahan 400. Jalur migrasi teraman adalah menghilangkan parameter ini sepenuhnya dari permintaan, dan menggunakan prompting untuk memandu perilaku model. Jika Anda menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa itu tidak pernah menjamin output yang identik.

### Konten pemikiran dihilangkan secara default

Mulai dengan Claude Opus 4.7, konten pemikiran dihilangkan dari respons secara default. Blok pemikiran masih muncul dalam aliran respons, tetapi bidang `thinking` mereka akan kosong kecuali pemanggil secara eksplisit memilih masuk. Ini adalah perubahan senyap — tidak ada kesalahan yang dimunculkan — dan latensi respons akan sedikit ditingkatkan. Jika output penalaran diperlukan, Anda dapat mengatur `display` ke `"summarized"` dan memilih kembali masuk dengan perubahan satu baris:

```python Python
thinking = {
    "type": "adaptive",
    "display": "summarized",  # atau "omitted" (default)
}
```

<Note>
Jika produk Anda mengalirkan penalaran kepada pengguna, default baru akan muncul sebagai jeda panjang sebelum output dimulai. Atur `"display": "summarized"` untuk mengembalikan kemajuan yang terlihat selama pemikiran.
</Note>

### Penghitungan token yang diperbarui

Claude Opus 4.7 menggunakan tokenizer baru, berkontribusi pada kinerja yang ditingkatkan pada berbagai tugas. Tokenizer baru ini mungkin menggunakan kira-kira 1x hingga 1.35x lebih banyak token saat memproses teks dibandingkan dengan model sebelumnya (hingga ~35% lebih, bervariasi menurut konten), dan [`/v1/messages/count_tokens`](/docs/id/build-with-claude/token-counting) akan mengembalikan jumlah token yang berbeda untuk Claude Opus 4.7 daripada untuk Claude Opus 4.6. Efisiensi token Claude Opus 4.7 dapat bervariasi menurut bentuk beban kerja. Intervensi prompting, `task_budget`, dan `effort` dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai. Ingat bahwa kontrol ini mungkin menukar kecerdasan model.

Kami menyarankan memperbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu pemadatan. Claude Opus 4.7 menyediakan jendela konteks 1M pada harga API standar tanpa premium konteks panjang.

## Peningkatan kemampuan

### Pekerjaan pengetahuan

Claude Opus 4.7 menunjukkan keuntungan yang berarti pada tugas pekerja pengetahuan, khususnya di mana model perlu memverifikasi output-nya sendiri secara visual:

- **Redlining .docx dan pengeditan .pptx** — ditingkatkan dalam menghasilkan dan memeriksa sendiri perubahan terlacak dan tata letak slide.
- **Analisis bagan dan gambar** — ditingkatkan pada panggilan alat pemrograman dengan perpustakaan pemrosesan gambar (misalnya PIL) untuk menganalisis bagan dan gambar, termasuk transkripsi data tingkat piksel.

Jika prompt yang ada memiliki mitigasi di area ini (misalnya "periksa kembali tata letak slide sebelum mengembalikan"), coba hapus perancah itu dan baseline ulang.

### Memori

Claude Opus 4.7 lebih baik dalam menulis dan menggunakan memori berbasis sistem file. Jika agen mempertahankan scratchpad, file catatan, atau penyimpanan memori terstruktur di seluruh putaran, agen itu harus meningkat dalam membuat catatan untuk dirinya sendiri dan memanfaatkan catatannya dalam tugas-tugas masa depan. Untuk memberikan Claude scratchpad yang dikelola tanpa membangun milik Anda sendiri, gunakan [alat memori](/docs/id/agents-and-tools/tool-use/memory-tool) sisi klien.

### Visi

Lihat [Dukungan gambar resolusi tinggi](#high-resolution-image-support) di atas.

## Perubahan perilaku

Ini bukan perubahan API yang merusak tetapi mungkin memerlukan pembaruan prompt. Lihat [Migrasi ke Claude Opus 4.7](/docs/id/about-claude/models/migration-guide#migrating-to-claude-opus-4-7) untuk panduan lengkap.

- **Mengikuti instruksi lebih literal**, khususnya pada tingkat upaya yang lebih rendah. Model tidak akan secara diam-diam menggeneralisasi instruksi dari satu item ke item lain, dan tidak akan menyimpulkan permintaan yang tidak Anda buat.
- **Panjang respons dikalibrasi ke kompleksitas tugas yang dirasakan** daripada default ke verbositas tetap.
- **Lebih sedikit panggilan alat secara default,** menggunakan penalaran lebih banyak. Meningkatkan upaya meningkatkan penggunaan alat.
- **Nada lebih langsung, berpendapat** dengan frasa yang lebih sedikit yang berpusat pada validasi dan lebih sedikit emoji daripada gaya yang lebih hangat dari Claude Opus 4.6.
- **Pembaruan kemajuan yang lebih teratur** kepada pengguna di seluruh jejak agentic yang panjang. Jika Anda telah menambahkan perancah untuk memaksa pesan status interim, coba hapus.
- **Lebih sedikit subagen yang dihasilkan secara default.** Dapat diarahkan melalui prompting.
- **Perlindungan keamanan siber real-time:** permintaan yang melibatkan topik terlarang atau berisiko tinggi dapat menyebabkan penolakan. Untuk pekerjaan keamanan yang sah, ajukan permohonan ke [Program Verifikasi Siber](https://claude.com/form/cyber-use-case).

## Panduan migrasi

Untuk instruksi migrasi langkah demi langkah dan daftar periksa migrasi lengkap, lihat [Migrasi ke Claude Opus 4.7](/docs/id/about-claude/models/migration-guide#migrating-to-claude-opus-4-7). Jika Anda menggunakan Claude Code atau Agent SDK, [Claude API skill](/docs/id/agents-and-tools/agent-skills/claude-api-skill) dapat menerapkan langkah-langkah migrasi ini ke basis kode Anda secara otomatis.

## Langkah berikutnya

<CardGroup>
  <Card title="Anggaran tugas" icon="gauge" href="/docs/id/build-with-claude/task-budgets">
    Berikan Claude anggaran token penasihat di seluruh loop agentic penuh.
  </Card>
  <Card title="Adaptive thinking" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Satu-satunya mode pemikiran-on yang didukung di Claude Opus 4.7.
  </Card>
  <Card title="Upaya" icon="sliders" href="/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-4-7">
    Panduan upaya per tingkat untuk Claude Opus 4.7.
  </Card>
  <Card title="Gambar dan visi" icon="image" href="/docs/id/build-with-claude/vision">
    Dukungan gambar resolusi tinggi dan pemetaan koordinat 1:1.
  </Card>
  <Card title="Panduan migrasi" icon="arrow-right" href="/docs/id/about-claude/models/migration-guide#migrating-to-claude-opus-4-7">
    Instruksi upgrade langkah demi langkah.
  </Card>
</CardGroup>