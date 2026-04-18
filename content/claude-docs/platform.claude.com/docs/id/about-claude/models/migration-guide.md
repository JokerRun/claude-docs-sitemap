---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/migration-guide
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: ab2c5af993f9e507a1b56a5a2a8c6d195a838f7e5a9ec69978e1630954156da2
---

# Panduan migrasi

Panduan untuk bermigrasi ke model Claude Opus 4.7 dan Claude 4.6 dari versi Claude sebelumnya

---

<Note>
Panduan ini mencakup migrasi kode [Messages API](/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](/docs/id/managed-agents/overview), tidak ada perubahan selain memperbarui nama model yang diperlukan.
</Note>

## Bermigrasi ke Claude Opus 4.7

Claude Opus 4.7 adalah model yang tersedia secara umum paling mampu hingga saat ini. Model ini sangat otonom dan berkinerja luar biasa pada pekerjaan agentic jangka panjang, pekerjaan pengetahuan, tugas visi, dan tugas memori. Claude Opus 4.7 harus memiliki kinerja out-of-the-box yang kuat pada prompt dan eval Claude Opus 4.6 yang ada dengan harga `$5 / $25` per MTok yang sama, tetapi ada beberapa perubahan perilaku dan API yang perlu diketahui saat Anda bermigrasi. Model ini mendukung set fitur yang sama dengan Claude Opus 4.6, termasuk [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) dengan harga API standar tanpa premium konteks panjang, 128k token output maksimal, [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), prompt caching, batch processing, Files API, dukungan PDF, visi, dan set lengkap alat sisi server dan sisi klien (bash, eksekusi kode, penggunaan komputer, editor teks, pencarian web, pengambilan web, konektor MCP, memori).

<Tip>
  **Otomatiskan migrasi ini dengan Claude API skill.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [Claude API skill](/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) yang disertakan:

  ```text
  /claude-api migrate this project to claude-opus-4-7
  ```

  Skill menerapkan penukaran ID model, perubahan parameter yang merusak, penggantian prefill, dan kalibrasi upaya yang dijelaskan di bawah di seluruh basis kode Anda, kemudian menghasilkan daftar periksa item untuk diverifikasi secara manual. Skill meminta Anda untuk mengonfirmasi cakupan migrasi (seluruh direktori kerja, subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun.
</Tip>

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-6"  # Sebelum
model = "claude-opus-4-7"  # Sesudah
```

### Perubahan yang merusak

1. **Extended thinking dihapus:** `thinking: {type: "enabled", budget_tokens: N}` tidak lagi didukung pada Claude Opus 4.7 atau model yang lebih baru dan mengembalikan kesalahan 400. Beralih ke [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Adaptive thinking **dimatikan secara default** pada Claude Opus 4.7: permintaan tanpa bidang `thinking` berjalan tanpa pemikiran, cocok dengan perilaku Opus 4.6. Atur `thinking: {type: "adaptive"}` secara eksplisit untuk mengaktifkannya.

    Sebelum (Claude Opus 4.6):

    ```python
    client.messages.create(
        model="claude-opus-4-6",
        max_tokens=64000,
        thinking={"type": "enabled", "budget_tokens": 32000},
        messages=[{"role": "user", "content": "..."}],
    )
    ```

    Sesudah (Claude Opus 4.7):

    ```python
    client.messages.create(
        model="claude-opus-4-7",
        max_tokens=64000,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},  # atau "max", "xhigh", "medium", "low"
        messages=[{"role": "user", "content": "..."}],
    )
    ```

    Adaptive thinking dapat diarahkan melalui prompting. Untuk panduan tentang penyesuaian ketika model berpikir terlalu banyak atau terlalu sedikit, lihat [Kalibrasi upaya dan kedalaman pemikiran](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#calibrating-effort-and-thinking-depth).

2. **Parameter sampling dihapus:** Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun pada Claude Opus 4.7 mengembalikan kesalahan 400. Jalur migrasi paling aman adalah menghilangkan parameter ini sepenuhnya dari muatan permintaan. Prompting adalah cara yang direkomendasikan untuk memandu perilaku model pada Claude Opus 4.7. Jika Anda menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa itu tidak pernah menjamin output yang identik pada model sebelumnya.

3. **Konten pemikiran dihilangkan secara default:** Blok pemikiran masih muncul dalam aliran respons pada Claude Opus 4.7, tetapi bidang `thinking` mereka kosong kecuali Anda secara eksplisit memilih untuk masuk. Ini adalah perubahan senyap dari Claude Opus 4.6, di mana default adalah mengembalikan teks pemikiran yang dirangkum. Untuk mengembalikan konten pemikiran yang dirangkum pada Claude Opus 4.7, atur `thinking.display` ke `"summarized"`:

    ```python
    thinking = {
        "type": "adaptive",
        "display": "summarized",
    }
    ```

    Default adalah `"omitted"` pada Claude Opus 4.7. Jika produk Anda melakukan streaming penalaran kepada pengguna, default baru muncul sebagai jeda panjang sebelum output dimulai; atur `display: "summarized"` untuk mengembalikan kemajuan yang terlihat selama pemikiran. Lihat [Extended thinking](/docs/id/build-with-claude/extended-thinking#controlling-thinking-display) untuk detail.

4. **Penghitungan token yang diperbarui:** Claude Opus 4.7 menggunakan tokenizer baru, berkontribusi pada peningkatan kinerjanya pada berbagai tugas. Tokenizer baru ini mungkin menggunakan kira-kira 1x hingga 1,35x lebih banyak token saat memproses teks dibandingkan dengan model sebelumnya (hingga ~35% lebih banyak, bervariasi menurut konten), dan [`/v1/messages/count_tokens`](/docs/id/build-with-claude/token-counting) akan mengembalikan jumlah token yang berbeda untuk Claude Opus 4.7 daripada untuk Claude Opus 4.6. Efisiensi token Claude Opus 4.7 dapat bervariasi menurut bentuk beban kerja. Intervensi prompting, `task_budget`, dan `effort` dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai. Ingat bahwa kontrol ini dapat menukar kecerdasan model. Kami menyarankan memperbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu pemadatan. Claude Opus 4.7 menyediakan jendela konteks 1M dengan harga API standar tanpa premium konteks panjang.

5. **Penghapusan prefill (dibawa dari Opus 4.6):** Prefilling pesan asisten mengembalikan kesalahan 400 pada Claude Opus 4.7. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

### Memilih tingkat upaya

[Parameter effort](/docs/id/build-with-claude/effort) memungkinkan Anda untuk menyesuaikan kecerdasan Claude vs. pengeluaran token, menukar kemampuan untuk kecepatan lebih cepat dan biaya lebih rendah. Mulai dengan tingkat upaya `xhigh` baru untuk kasus penggunaan coding dan agentic, dan gunakan minimum upaya `high` untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan. Bereksperimen dengan tingkat upaya lain untuk lebih menyesuaikan penggunaan token dan kecerdasan:

- **`max`:** Upaya maksimal dapat memberikan peningkatan kinerja dalam beberapa kasus penggunaan, tetapi mungkin menunjukkan hasil yang berkurang dari peningkatan penggunaan token. Pengaturan ini juga kadang-kadang dapat rentan terhadap overthinking. Kami merekomendasikan pengujian upaya maksimal untuk tugas yang menuntut kecerdasan.
- **`xhigh` (baru):** Upaya ekstra tinggi adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentic.
- **`high`:** Pengaturan ini menyeimbangkan penggunaan token dan kecerdasan. Untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan, kami merekomendasikan minimum upaya `high`.
- **`medium`:** Baik untuk kasus penggunaan yang sensitif terhadap biaya yang perlu mengurangi penggunaan token sambil menukar kecerdasan.
- **`low`:** Cadangkan untuk tugas pendek dan terbatas serta beban kerja yang sensitif terhadap latensi yang tidak sensitif terhadap kecerdasan.

Kami mengharapkan upaya menjadi lebih penting untuk model ini daripada untuk Opus sebelumnya, dan merekomendasikan bereksperimen dengannya secara aktif saat Anda meningkatkan.

### Perubahan perilaku

Claude Opus 4.7 memiliki beberapa perbedaan perilaku dari Claude Opus 4.6 yang bukan perubahan API yang merusak tetapi mungkin memerlukan pembaruan prompt atau penghapusan scaffolding.

1. **Panjang respons bervariasi menurut kasus penggunaan:** Claude Opus 4.7 mengkalibrasi panjang respons ke seberapa kompleks yang dianggapnya tugas tersebut, daripada default ke verbositas tetap. Ini biasanya berarti jawaban lebih pendek pada pencarian sederhana dan jawaban jauh lebih panjang pada analisis terbuka. Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyesuaikan prompt Anda. Sebagai contoh, untuk mengurangi verbositas, Anda mungkin menambahkan: "Berikan respons yang ringkas dan terfokus. Lewati konteks yang tidak penting, dan jaga contoh tetap minimal." Jika Anda melihat contoh spesifik tentang jenis verbositas (yaitu penjelasan berlebihan), Anda dapat menambahkan instruksi tambahan dalam prompt Anda untuk mencegahnya. Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang sesuai cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan.

2. **Penurutan instruksi yang lebih literal:** Claude Opus 4.7 menafsirkan prompt lebih literal dan eksplisit daripada Claude Opus 4.6, terutama pada tingkat upaya yang lebih rendah. Model ini tidak akan diam-diam menggeneralisasi instruksi dari satu item ke item lain, dan tidak akan menyimpulkan permintaan yang tidak Anda buat. Sisi positif dari literalisme ini adalah presisi dan lebih sedikit thrash. Model ini umumnya berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang dikalibrasi dengan hati-hati, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Tinjauan prompt dan harness mungkin sangat membantu untuk migrasi ke Claude Opus 4.7.

3. **Nada yang lebih langsung:** Seperti halnya model baru apa pun, gaya prosa pada penulisan bentuk panjang mungkin bergeser. Claude Opus 4.7 lebih langsung dan berpendapat, dengan frasa yang lebih sedikit yang berpusat pada validasi dan emoji lebih sedikit daripada gaya yang lebih hangat dari Claude Opus 4.6. Jika produk Anda mengandalkan suara tertentu, evaluasi kembali prompt gaya terhadap baseline baru.

4. **Pembaruan kemajuan bawaan dalam jejak agentic:** Claude Opus 4.7 menyediakan pembaruan yang lebih teratur dan berkualitas lebih tinggi kepada pengguna di seluruh jejak agentic yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status interim ("Setelah setiap 3 panggilan alat, rangkum kemajuan"), coba hapus. Jika Anda menemukan bahwa panjang atau konten pembaruan yang menghadap pengguna dari Claude Opus 4.7 tidak dikalibrasi dengan baik untuk kasus penggunaan Anda, secara eksplisit jelaskan seperti apa pembaruan ini dalam prompt dan berikan contoh.

5. **Lebih sedikit subagen yang dihasilkan secara default:** Claude Opus 4.7 cenderung menghasilkan lebih sedikit subagen secara default. Namun, perilaku ini dapat diarahkan melalui prompting; berikan Claude Opus 4.7 panduan eksplisit tentang kapan subagen diinginkan.

6. **Kalibrasi upaya yang lebih ketat:** Bermakna berubah dari Claude Opus 4.6, Claude Opus 4.7 menghormati [tingkat upaya](/docs/id/build-with-claude/effort) secara ketat, terutama di ujung bawah. Pada `low` dan `medium`, model membatasi pekerjaan ke apa yang diminta daripada melampaui dan di atas. Ini baik untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada upaya `low` ada beberapa risiko under-thinking. Jika Anda mengamati penalaran dangkal pada masalah kompleks, naikkan upaya ke `high` atau `xhigh` daripada prompting di sekitarnya. Jika Anda perlu menjaga upaya pada `low` untuk latensi, tambahkan panduan yang ditargetkan: "Tugas ini melibatkan penalaran multi-langkah. Pikirkan dengan hati-hati melalui masalah sebelum merespons." Lihat [Tingkat upaya yang direkomendasikan untuk Claude Opus 4.7](/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-4-7).

7. **Lebih sedikit panggilan alat secara default:** Claude Opus 4.7 memiliki kecenderungan untuk menggunakan alat lebih jarang daripada Claude Opus 4.6 dan menggunakan penalaran lebih banyak. Ini menghasilkan hasil yang lebih baik dalam sebagian besar kasus. Namun, meningkatkan pengaturan upaya adalah tuas yang berguna untuk meningkatkan tingkat penggunaan alat, terutama dalam pekerjaan pengetahuan. Pengaturan upaya `high` atau `xhigh` menunjukkan penggunaan alat yang jauh lebih banyak dalam pencarian agentic dan coding. Untuk skenario di mana Anda menginginkan lebih banyak penggunaan alat, Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan alat dengan benar.

8. **Perlindungan keamanan siber real-time:** Baru ditambahkan di Claude Opus 4.7, permintaan yang melibatkan topik yang dilarang atau berisiko tinggi dapat menyebabkan penolakan. Untuk pekerjaan keamanan yang sah seperti penetration testing, penelitian kerentanan, atau red-teaming, ajukan permohonan ke [Program Verifikasi Siber](https://claude.com/form/cyber-use-case) untuk meminta pembatasan yang lebih rendah. Lihat [Perlindungan, peringatan, dan banding](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) untuk latar belakang.

9. **Dukungan gambar resolusi tinggi:** Claude Opus 4.7 adalah model Claude pertama dengan dukungan gambar resolusi tinggi, dengan resolusi gambar maksimal 2576 piksel di tepi panjang (naik dari 1568 piksel pada model sebelumnya). Ini membuka keuntungan pada beban kerja yang berat visi dan sangat berharga untuk penggunaan komputer, pemahaman tangkapan layar, dan analisis dokumen. Dukungan resolusi tinggi bersifat otomatis dan tidak memerlukan header beta atau opt-in sisi klien. Gambar resolusi penuh dapat menggunakan hingga sekitar 3x lebih banyak token gambar daripada pada model sebelumnya (hingga 4.784 token per gambar, dibandingkan dengan batas sebelumnya sekitar 1.600 token per gambar), jadi anggaran ulang `max_tokens` dan ekspektasi biaya untuk beban kerja yang berat gambar, atau downsample sebelum mengirim jika Anda tidak memerlukan kesetiaan tambahan. Koordinat penunjukan dan kotak pembatas yang dikembalikan oleh model adalah 1:1 dengan piksel gambar aktual pada Claude Opus 4.7, jadi tidak ada konversi faktor skala yang diperlukan. Lihat [Dukungan gambar resolusi tinggi pada Claude Opus 4.7](/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) untuk detail.

### Perubahan yang direkomendasikan

Ini bukan persyaratan tetapi akan meningkatkan pengalaman Anda:

1. **Evaluasi kembali `max_tokens`:** Karena teks yang sama menghasilkan jumlah token yang lebih tinggi pada Claude Opus 4.7, kami menyarankan memperbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu pemadatan. Intervensi prompting, [`task_budget`](/docs/id/build-with-claude/task-budgets), dan [`effort`](/docs/id/build-with-claude/effort) dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai.

2. **Audit ekspektasi penghitungan token:** Jalur kode apa pun yang memperkirakan token sisi klien atau mengasumsikan rasio token-ke-karakter tetap harus diuji ulang terhadap Claude Opus 4.7. Gunakan [endpoint Token counting](/docs/id/build-with-claude/token-counting) untuk memverifikasi.

3. **Adopsi [task budgets](/docs/id/build-with-claude/task-budgets) (beta):** Claude Opus 4.7 memperkenalkan task budgets. Anggaran ini memungkinkan Anda untuk menginformasikan Claude berapa banyak token yang dimilikinya untuk loop agentic penuh, termasuk pemikiran, panggilan alat, hasil alat, dan output akhir. Model melihat hitungan mundur yang berjalan dan menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan tugas dengan anggun saat anggaran dikonsumsi. Untuk menggunakan, atur header beta `task-budgets-2026-03-13` dan tambahkan yang berikut ke konfigurasi output Anda:

    ```python
    output_config = {
        "effort": "high",
        "task_budget": {"type": "tokens", "total": 128000},
    }
    ```

    Anda mungkin perlu bereksperimen dengan anggaran tugas yang berbeda untuk kasus penggunaan Anda. Jika model diberi anggaran tugas yang terlalu ketat untuk tugas tertentu, model mungkin menyelesaikan tugas dengan kurang menyeluruh, mereferensikan anggaran sebagai kendala. Untuk tugas agentic terbuka di mana kualitas lebih penting daripada kecepatan, jangan atur anggaran tugas; cadangkan anggaran tugas untuk beban kerja di mana Anda perlu model untuk membatasi pekerjaan ke tunjangan token. Nilai minimum untuk anggaran tugas adalah 20k token.

    Ini bukan batas keras; ini adalah saran yang disadari model. Ini berbeda dari `max_tokens`, yang merupakan batas keras per permintaan pada token yang dihasilkan (`max_tokens` tidak diteruskan ke model, dan model tidak menyadarinya), sementara `task_budget` adalah batas penasihat di seluruh loop agentic penuh. Gunakan `task_budget` ketika Anda ingin model untuk self-moderate, dan `max_tokens` sebagai batas per permintaan keras untuk membatasi penggunaan.

4. **Atur `max_tokens` besar pada upaya `max` atau `xhigh`:** Jika Anda menjalankan Claude Opus 4.7 pada upaya `max` atau `xhigh`, atur anggaran token output maksimal yang besar sehingga model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan panggilan alat. Kami merekomendasikan memulai dengan 64k token dan menyesuaikan dari sana.

5. **Downsample gambar jika resolusi tinggi tidak perlu:** Claude Opus 4.7 mendukung gambar hingga 2576px / 3.75MP. Gambar resolusi tinggi menggunakan lebih banyak token. Jika kesetiaan gambar tambahan tidak perlu, downsample gambar sebelum mengirim ke Claude untuk menghindari peningkatan penggunaan token. Lihat [Gambar dan visi](/docs/id/build-with-claude/vision).

### Daftar periksa migrasi

- [ ] Perbarui nama model dari `claude-opus-4-6` ke `claude-opus-4-7` (atau perbarui alias).
- [ ] Hapus `temperature`, `top_p`, dan `top_k` dari muatan permintaan.
- [ ] Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](/docs/id/build-with-claude/effort).
- [ ] Hapus prefill pesan asisten apa pun.
- [ ] Jika UI Anda menampilkan konten pemikiran, secara eksplisit pilih untuk merangkum pemikiran.
- [ ] Benchmark ulang biaya dan latensi end-to-end di bawah tokenisasi yang diperbarui.
- [ ] Sesuaikan ulang `max_tokens` untuk memperhitungkan tokenisasi yang diperbarui.
- [ ] Uji ulang estimasi penghitungan token sisi klien apa pun.
- [ ] Jika aplikasi Anda mengirim gambar, anggaran ulang untuk [dukungan gambar resolusi tinggi](/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (hingga sekitar 3x lebih banyak token gambar per gambar resolusi penuh). Downsample sebelum mengirim jika Anda tidak memerlukan kesetiaan tambahan. Jika Anda mengonsumsi koordinat penunjukan atau kotak pembatas dari model, hapus konversi faktor skala apa pun; koordinat adalah 1:1 dengan piksel gambar aktual pada Claude Opus 4.7.
- [ ] Tinjau prompt untuk perubahan perilaku di atas (panjang respons, literalisme, nada, pembaruan kemajuan, subagen, kalibrasi upaya, pemicu alat, perlindungan siber, penanganan gambar resolusi tinggi).
- [ ] Baseline ulang panjang respons dengan prompt kontrol panjang yang ada dihapus, kemudian sesuaikan secara eksplisit.
- [ ] Jika menggunakan upaya `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
- [ ] Pertimbangkan untuk mengadopsi task budgets (beta) untuk alur kerja agentic.
- [ ] Jika produk Anda melakukan pekerjaan keamanan yang sah, ajukan permohonan ke [Program Verifikasi Siber](https://claude.com/form/cyber-use-case) untuk akses ke pembatasan yang lebih rendah pada konten siber.

## Bermigrasi ke Claude Opus 4.7 dari Opus 4.5 atau lebih awal

Jika Anda bermigrasi dari Claude Opus 4.5, Opus 4.1, atau model yang lebih awal langsung ke Claude Opus 4.7, terapkan **semua [perubahan Opus 4.7 di atas](#migrating-to-claude-opus-4-7)** ditambah perubahan kumulatif di bagian ini yang berlaku antara Opus 4.5 dan Opus 4.7. Jika Anda bermigrasi dari Opus 4.6, Anda hanya memerlukan [bagian Opus 4.7 di atas](#migrating-to-claude-opus-4-7).

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-5"  # Sebelum
model = "claude-opus-4-7"  # Sesudah
```

### Perubahan yang merusak

1. **Penghapusan prefill** tercakup dalam [perubahan yang merusak Opus 4.7](#breaking-changes) di atas.

2. **Penawaran parameter alat:** Model Claude Opus 4.6 dan yang lebih baru mungkin menghasilkan penghindaran string JSON yang sedikit berbeda dalam argumen panggilan alat (misalnya, penanganan penghindaran Unicode atau penghindaran garis miring yang berbeda). Jika Anda mengurai `input` panggilan alat sebagai string mentah daripada menggunakan parser JSON, verifikasi logika parsing Anda. Parser JSON standar (seperti `json.loads()` atau `JSON.parse()`) menangani perbedaan ini secara otomatis.

### Perubahan yang direkomendasikan

Perubahan ini meningkatkan pengalaman Anda pada Opus 4.7. Item yang ditandai **(diperlukan pada Opus 4.7)** adalah rekomendasi opsional saat Opus 4.6 diluncurkan tetapi sekarang wajib; sisanya tetap direkomendasikan.

1. **Migrasi ke adaptive thinking (diperlukan pada Opus 4.7):** `thinking: {type: "enabled", budget_tokens: N}` mengembalikan kesalahan 400 pada Claude Opus 4.7. Beralih ke `thinking: {type: "adaptive"}` dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Lihat [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).

   <CodeGroup>
   
   ```python Before nocheck
   response = client.beta.messages.create(
       model="claude-opus-4-5",
       max_tokens=16000,
       thinking={"type": "enabled", "budget_tokens": 32000},
       betas=["interleaved-thinking-2025-05-14"],
       messages=[...],
   )
   ```

   ```python After
   response = client.messages.create(
       model="claude-opus-4-7",
       max_tokens=16000,
       thinking={"type": "adaptive"},
       output_config={"effort": "high"},
       messages=[{"role": "user", "content": "Your prompt here"}],
   )
   ```

   ```bash CLI
   ant messages create <<'YAML'
   model: claude-opus-4-7
   max_tokens: 16000
   thinking:
     type: adaptive
   output_config:
     effort: high
   messages:
     - role: user
       content: Your prompt here
   YAML
   ```

   ```typescript TypeScript hidelines={1..2}
   import Anthropic from "@anthropic-ai/sdk";

   const client = new Anthropic();

   const response = await client.messages.create({
     model: "claude-opus-4-7",
     max_tokens: 16000,
     thinking: { type: "adaptive" },
     output_config: { effort: "high" },
     messages: [{ role: "user", content: "Your prompt here" }]
   } as unknown as Anthropic.MessageCreateParamsNonStreaming);
   ```

   ```csharp C#
   using Anthropic;
   using Anthropic.Models.Messages;

   public class Program
   {
       public static async Task Main(string[] args)
       {
           AnthropicClient client = new();

           var parameters = new MessageCreateParams
           {
               Model = Model.ClaudeOpus4_7,
               MaxTokens = 16000,
               Thinking = new ThinkingConfigAdaptive(),
               OutputConfig = new OutputConfig { Effort = Effort.High },
               Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
           };

           var response = await client.Messages.Create(parameters);
           Console.WriteLine(response);
       }
   }
   ```

   ```go Go hidelines={1..11,-1}
   package main

   import (
   	"context"
   	"fmt"
   	"log"

   	"github.com/anthropics/anthropic-sdk-go"
   )

   func main() {
   	client := anthropic.NewClient()

   	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
   		Model:     anthropic.ModelClaudeOpus4_7,
   		MaxTokens: 16000,
   		Thinking: anthropic.ThinkingConfigParamUnion{
   			OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
   		},
   		OutputConfig: anthropic.OutputConfigParam{
   			Effort: anthropic.OutputConfigEffortHigh,
   		},
   		Messages: []anthropic.MessageParam{
   			anthropic.NewUserMessage(anthropic.NewTextBlock("Your prompt here")),
   		},
   	})
   	if err != nil {
   		log.Fatal(err)
   	}
   	fmt.Println(response)
   }
   ```

   ```java Java hidelines={1..5,8..10,-2..}
   import com.anthropic.client.AnthropicClient;
   import com.anthropic.client.okhttp.AnthropicOkHttpClient;
   import com.anthropic.models.messages.MessageCreateParams;
   import com.anthropic.models.messages.Message;
   import com.anthropic.models.messages.Model;
   import com.anthropic.models.messages.OutputConfig;
   import com.anthropic.models.messages.ThinkingConfigAdaptive;

   public class AdaptiveThinkingExample {
       public static void main(String[] args) {
           AnthropicClient client = AnthropicOkHttpClient.fromEnv();

           MessageCreateParams params = MessageCreateParams.builder()
               .model(Model.CLAUDE_OPUS_4_7)
               .maxTokens(16000L)
               .thinking(ThinkingConfigAdaptive.builder().build())
               .outputConfig(OutputConfig.builder()
                   .effort(OutputConfig.Effort.HIGH)
                   .build())
               .addUserMessage("Your prompt here")
               .build();

           Message response = client.messages().create(params);
           System.out.println(response);
       }
   }
   ```

   ```php PHP hidelines={1..4}
   <?php

   use Anthropic\Client;

   $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

   $response = $client->messages->create(
       maxTokens: 16000,
       messages: [['role' => 'user', 'content' => 'Your prompt here']],
       model: 'claude-opus-4-7',
       thinking: ['type' => 'adaptive'],
       outputConfig: ['effort' => 'high'],
   );
   ```

   ```ruby Ruby hidelines={1..2}
   require "anthropic"

   client = Anthropic::Client.new

   response = client.messages.create(
     model: "claude-opus-4-7",
     max_tokens: 16000,
     thinking: { type: "adaptive" },
     output_config: { effort: "high" },
     messages: [{ role: "user", content: "Your prompt here" }]
   )
   ```
   </CodeGroup>

   Perhatikan bahwa migrasi juga bergerak dari `client.beta.messages.create` ke `client.messages.create`. Adaptive thinking dan effort adalah fitur GA dan tidak memerlukan namespace SDK beta atau header beta apa pun.

2. **Hapus header beta effort:** Parameter effort sekarang GA. Hapus `betas=["effort-2025-11-24"]` dari permintaan Anda.

3. **Hapus header beta streaming alat yang halus:** Streaming alat yang halus sekarang GA. Hapus `betas=["fine-grained-tool-streaming-2025-05-14"]` dari permintaan Anda.

4. **Hapus header beta pemikiran yang saling terkait:** Adaptive thinking secara otomatis mengaktifkan pemikiran yang saling terkait pada Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6. Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Anda. Header masih berfungsi pada Sonnet 4.6 dengan pemikiran extended manual, tetapi mode manual sudah usang.

5. **Migrasi ke output_config.format:** Jika menggunakan structured outputs, perbarui `output_format={...}` ke `output_config={"format": {...}}`. Parameter lama tetap berfungsi tetapi sudah usang dan akan dihapus dalam rilis model di masa depan.

### Bermigrasi dari Claude 4.1 atau lebih awal

Jika Anda bermigrasi dari Opus 4.1, Sonnet 4 (sudah usang), atau model yang lebih awal langsung ke Claude Opus 4.7, terapkan perubahan Claude Opus 4.7 di bagian atas panduan ini dan perubahan kumulatif di atas ditambah perubahan tambahan di bagian ini.

```python
# Dari Opus 4.1
model = "claude-opus-4-1-20250805"  # Sebelum
model = "claude-opus-4-7"  # Sesudah

# Dari Sonnet 4
model = "claude-sonnet-4-20250514"  # Sebelum
model = "claude-opus-4-7"  # Sesudah

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Sebelum
model = "claude-opus-4-7"  # Sesudah
```

#### Perubahan yang merusak tambahan

1. **Hapus parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Mulai dengan Claude Opus 4.7, mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun akan mengembalikan kesalahan 400. Jalur migrasi paling aman adalah menghilangkan parameter ini sepenuhnya dari permintaan, dan menggunakan prompting untuk memandu perilaku model. Jika Anda menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa itu tidak pernah menjamin output yang identik.

   
   ```python Python nocheck
   # Sebelum - Ini akan error di model Claude 4+
   response = client.messages.create(
       model="claude-3-7-sonnet-20250219",
       temperature=0.7,
       top_p=0.9,  # Parameter sampling non-default mengembalikan 400 pada Opus 4.7
       # ...
   )

   # Sesudah
   response = client.messages.create(
       model="claude-opus-4-7",
       # ...
   )
   ```

2. **Perbarui versi alat**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru. Hapus kode apa pun yang menggunakan perintah `undo_edit`.

   ```python
   # Sebelum
   tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]

   # Sesudah
   tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
   ```

   - **Editor teks:** Gunakan `text_editor_20250728` dan `str_replace_based_edit_tool`. Lihat [dokumentasi alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) untuk detail.
   - **Eksekusi kode:** Tingkatkan ke `code_execution_20250825`. Lihat [dokumentasi alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk instruksi migrasi.

3. **Tangani alasan penghentian `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan penghentian `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):

   
   ```python Python nocheck
   response = client.messages.create(...)

   if response.stop_reason == "refusal":
       # Tangani penolakan dengan tepat
       pass
   ```

4. **Tangani alasan penghentian `model_context_window_exceeded`**

   Model Claude 4.5+ mengembalikan alasan penghentian `model_context_window_exceeded` ketika generasi berhenti karena mencapai batas jendela konteks, daripada batas `max_tokens` yang diminta. Perbarui aplikasi Anda untuk menangani alasan penghentian baru ini:

   
   ```python Python nocheck
   response = client.messages.create(...)

   if response.stop_reason == "model_context_window_exceeded":
       # Tangani batas jendela konteks dengan tepat
       pass
   ```

5. **Verifikasi penanganan parameter alat (trailing newlines)**

   Model Claude 4.5+ mempertahankan trailing newlines dalam parameter string panggilan alat yang sebelumnya dihapus. Jika alat Anda mengandalkan pencocokan string yang tepat terhadap parameter panggilan alat, verifikasi logika Anda menangani trailing newlines dengan benar.

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4+ memiliki gaya komunikasi yang lebih ringkas dan langsung dan memerlukan arahan eksplisit. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimisasi.

#### Perubahan yang direkomendasikan tambahan

- **Hapus header beta legacy:** Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`. Semua model Claude 4+ memiliki penggunaan alat yang efisien token bawaan dan header ini tidak berpengaruh.

### Daftar periksa migrasi (dari Opus 4.5 atau lebih awal)

- [ ] Perbarui ID model ke `claude-opus-4-7`
- [ ] Terapkan semua [perubahan yang merusak Opus 4.7](#migrating-to-claude-opus-4-7) (extended thinking dihapus, parameter sampling dihapus, tampilan pemikiran dihilangkan secara default, tokenisasi yang diperbarui)
- [ ] **BREAKING:** Hapus prefill pesan asisten (mengembalikan kesalahan 400); gunakan structured outputs atau `output_config.format` sebagai gantinya
- [ ] **BREAKING pada Opus 4.7:** Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](/docs/id/build-with-claude/effort) (mengembalikan 400 pada Opus 4.7)
- [ ] Verifikasi parsing JSON panggilan alat menggunakan parser JSON standar
- [ ] Hapus header beta `effort-2025-11-24` (effort sekarang GA)
- [ ] Hapus header beta `fine-grained-tool-streaming-2025-05-14`
- [ ] Hapus header beta `interleaved-thinking-2025-05-14` (adaptive thinking mengaktifkan pemikiran yang saling terkait secara otomatis)
- [ ] Migrasi `output_format` ke `output_config.format` (jika berlaku)
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: hapus `temperature`, `top_p`, dan `top_k` (nilai non-default mengembalikan 400 pada Opus 4.7)
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: perbarui versi alat (`text_editor_20250728`, `code_execution_20250825`)
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: tangani alasan penghentian `refusal`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: tangani alasan penghentian `model_context_window_exceeded`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: verifikasi penanganan parameter string alat untuk trailing newlines
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: hapus header beta legacy (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`)
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Uji di lingkungan pengembangan sebelum penerapan produksi

---

## Bermigrasi ke Claude Sonnet 4.6

Claude Sonnet 4.6 menggabungkan kecerdasan yang kuat dengan kinerja cepat, menampilkan kemampuan pencarian agentic yang ditingkatkan dan eksekusi kode gratis saat digunakan dengan pencarian web atau pengambilan web. Model ini ideal untuk tugas coding, analisis, dan konten sehari-hari.

Untuk gambaran lengkap tentang kemampuan, lihat [gambaran umum model](/docs/id/about-claude/models/overview).

<Note>
Harga Sonnet 4.6 adalah $3 per juta token input, $15 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Sonnet 4.5
model = "claude-sonnet-4-5"  # Sebelum
model = "claude-sonnet-4-6"  # Sesudah

# Dari Sonnet 4
model = "claude-sonnet-4-20250514"  # Sebelum
model = "claude-sonnet-4-6"  # Sesudah
```

### Perubahan yang merusak

#### Saat bermigrasi dari Sonnet 4.5

1. **Prefilling pesan asisten tidak lagi didukung**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari Sonnet 4.5 atau lebih awal.
   </Warning>

   Prefilling pesan asisten mengembalikan kesalahan `400` pada Sonnet 4.6. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi system prompt, atau `output_config.format` sebagai gantinya.

   **Kasus penggunaan prefill umum dan migrasi:**

   - **Mengontrol format output** (memaksa output JSON/YAML): Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs) atau tools dengan enum fields untuk tugas klasifikasi.

   - **Menghilangkan preamble** (menghapus frasa "Here is..."): Tambahkan instruksi langsung dalam system prompt: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc."

   - **Menghindari penolakan yang buruk:** Claude sekarang jauh lebih baik dalam penolakan yang tepat. Prompting yang jelas dalam pesan pengguna tanpa prefill harus cukup.

   - **Continuations** (melanjutkan respons yang terputus): Pindahkan continuation ke pesan pengguna: "Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off."

   - **Context hydration / role consistency** (menyegarkan konteks dalam percakapan panjang): Injeksikan apa yang sebelumnya adalah pengingat prefilled-assistant ke dalam user turn sebagai gantinya.

2. **Escaping JSON parameter tool mungkin berbeda**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari Sonnet 4.5 atau lebih awal.
   </Warning>

   Escaping string JSON dalam parameter tool mungkin berbeda dari model sebelumnya. Parser JSON standar menangani ini secara otomatis, tetapi parsing berbasis string kustom mungkin memerlukan pembaruan.

#### Saat bermigrasi dari Claude 3.x

3. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

4. **Perbarui versi tool**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi tool terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

5. **Tangani alasan stop `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan stop `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [prompting best practices](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Perubahan yang direkomendasikan

1. **Hapus header beta `fine-grained-tool-streaming-2025-05-14`:** Fine-grained tool streaming sekarang GA pada Sonnet 4.6 dan tidak lagi memerlukan header beta.
2. **Migrasikan `output_format` ke `output_config.format`:** Parameter `output_format` sudah usang. Gunakan `output_config.format` sebagai gantinya.

### Bermigrasi dari Sonnet 4.5

Pertimbangkan untuk bermigrasi dari Sonnet 4.5 ke Sonnet 4.6, yang memberikan lebih banyak kecerdasan dengan harga yang sama.

<Warning>
Sonnet 4.6 default ke effort level `high`, berbeda dengan Sonnet 4.5 yang tidak memiliki parameter effort. Pertimbangkan untuk menyesuaikan parameter effort saat Anda bermigrasi dari Sonnet 4.5 ke Sonnet 4.6. Jika tidak secara eksplisit diatur, Anda mungkin mengalami latency yang lebih tinggi dengan effort level default.
</Warning>

#### Jika Anda tidak menggunakan extended thinking

Jika Anda tidak menggunakan extended thinking pada Sonnet 4.5, Anda dapat melanjutkan tanpanya pada Sonnet 4.6. Anda harus secara eksplisit mengatur effort ke level yang sesuai untuk kasus penggunaan Anda. Pada effort `low` dengan thinking dinonaktifkan, Anda dapat mengharapkan performa yang sama atau lebih baik relatif terhadap Sonnet 4.5 tanpa extended thinking.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 8192,
    "output_config": {
        "effort": "low"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

```bash CLI
ant messages create <<'YAML'
model: claude-sonnet-4-6
max_tokens: 8192
output_config:
  effort: low
messages:
  - role: user
    content: Your prompt here
YAML
```

```python Python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  output_config: { effort: "low" },
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```csharp C#
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 8192,
            OutputConfig = new OutputConfig
            {
                Effort = Effort.Low
            },
            Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
        };
        var message = await client.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 8192,
		OutputConfig: anthropic.OutputConfigParam{
			Effort: anthropic.OutputConfigEffortLow,
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Your prompt here")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Content[0].Text)
}
```

```java Java hidelines={1..4,6..8,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.OutputConfig;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-sonnet-4-6")
            .maxTokens(8192L)
            .outputConfig(OutputConfig.builder()
                .effort(OutputConfig.Effort.LOW)
                .build())
            .addUserMessage("Your prompt here")
            .build();

        Message response = client.messages().create(params);
        response.content().stream()
            .flatMap(block -> block.text().stream())
            .forEach(textBlock -> System.out.println(textBlock.text()));
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 8192,
    messages: [['role' => 'user', 'content' => 'Your prompt here']],
    model: 'claude-sonnet-4-6',
    outputConfig: ['effort' => 'low'],
);
echo $message->content[0]->text;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  output_config: {
    effort: "low"
  },
  messages: [
    { role: "user", content: "Your prompt here" }
  ]
)
puts message.content.first.text
```
</CodeGroup>

#### Jika Anda menggunakan extended thinking

Jika Anda menggunakan extended thinking dengan `budget_tokens` pada Sonnet 4.5, masih berfungsi pada Sonnet 4.6 tetapi sudah usang. Migrasikan ke [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter effort](/docs/id/build-with-claude/effort).

##### Bermigrasi ke adaptive thinking

[Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) adalah pengganti yang direkomendasikan untuk `budget_tokens` pada Sonnet 4.6. Ini sangat cocok untuk pola beban kerja berikut:

- **Autonomous multi-step agents:** agen coding yang mengubah persyaratan menjadi software yang berfungsi, pipeline analisis data, dan bug finding di mana model berjalan secara independen di banyak langkah. Adaptive thinking memungkinkan model untuk mengkalibrasi penalarannya per langkah, tetap di jalur selama lintasan yang lebih panjang. Untuk beban kerja ini, mulai dengan effort `high`. Jika latency atau penggunaan token menjadi perhatian, turunkan ke `medium`.
- **Computer use agents:** Sonnet 4.6 mencapai akurasi terbaik di kelasnya pada evaluasi computer use menggunakan adaptive mode.
- **Bimodal workloads:** campuran tugas mudah dan sulit di mana adaptive melewati thinking pada query sederhana dan bernalar mendalam pada yang kompleks.

Saat menggunakan adaptive thinking, evaluasi effort `medium` dan `high` pada tugas Anda. Level yang tepat tergantung pada trade-off beban kerja Anda antara kualitas, latency, dan penggunaan token.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 64000,
    "thinking": {
        "type": "adaptive"
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

```bash CLI nocheck
ant messages create <<'YAML'
model: claude-sonnet-4-6
max_tokens: 64000
thinking:
  type: adaptive
output_config:
  effort: medium
messages:
  - role: user
    content: Your prompt here
YAML
```

```python Python nocheck
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript nocheck
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 64000,
  thinking: { type: "adaptive" },
  output_config: { effort: "medium" },
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Messages;
using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 64000,
            Thinking = new ThinkingConfigAdaptive(),
            OutputConfig = new OutputConfig { Effort = Effort.Medium },
            Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
        };

        var message = await client.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     "claude-sonnet-4-6",
		MaxTokens: 64000,
		Thinking: anthropic.ThinkingConfigParamUnion{
			OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
		},
		OutputConfig: anthropic.OutputConfigParam{
			Effort: anthropic.OutputConfigEffortMedium,
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Your prompt here")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..4,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.OutputConfig;
import com.anthropic.models.messages.ThinkingConfigAdaptive;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-sonnet-4-6")
            .maxTokens(64000L)
            .thinking(ThinkingConfigAdaptive.builder().build())
            .outputConfig(OutputConfig.builder()
                .effort(OutputConfig.Effort.MEDIUM)
                .build())
            .addUserMessage("Your prompt here")
            .build();

        Message response = client.messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 64000,
    messages: [['role' => 'user', 'content' => 'Your prompt here']],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'adaptive'],
    outputConfig: ['effort' => 'medium'],
);

echo $message->content[0]->text;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 64000,
  thinking: {
    type: "adaptive"
  },
  output_config: {
    effort: "medium"
  },
  messages: [
    { role: "user", content: "Your prompt here" }
  ]
)
puts message
```
</CodeGroup>

<Note>
Jika Anda melihat perilaku yang tidak konsisten atau regresi kualitas dengan adaptive thinking, coba turunkan pengaturan [effort](/docs/id/build-with-claude/effort) atau gunakan `max_tokens` sebagai batas keras terlebih dahulu. Extended thinking dengan `budget_tokens` masih berfungsi pada Sonnet 4.6 tetapi sudah usang dan tidak lagi direkomendasikan.
</Note>

##### Menjaga budget_tokens selama migrasi

Jika Anda perlu menjaga `budget_tokens` sementara saat bermigrasi, budget sekitar 16k token memberikan ruang untuk masalah yang lebih sulit tanpa risiko penggunaan token yang liar. Konfigurasi ini sudah usang dan akan dihapus dalam rilis model di masa depan.

###### Kasus penggunaan coding dan agentic

Untuk coding agentic, desain frontend, workflow tool-heavy, dan workflow enterprise yang kompleks, mulai dengan effort `medium`. Jika Anda menemukan latency terlalu tinggi, pertimbangkan mengurangi effort ke `low`. Jika Anda memerlukan kecerdasan yang lebih tinggi, pertimbangkan meningkatkan effort ke `high` atau bermigrasi ke Opus 4.7.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: interleaved-thinking-2025-05-14" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 16384,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16384
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

```bash CLI
ant beta:messages create --beta interleaved-thinking-2025-05-14 <<'YAML'
model: claude-sonnet-4-6
max_tokens: 16384
thinking:
  type: enabled
  budget_tokens: 16384
output_config:
  effort: medium
messages:
  - role: user
    content: Your prompt here
YAML
```

```python Python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16384,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "medium"},
    betas=["interleaved-thinking-2025-05-14"],
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 16384,
  thinking: { type: "enabled", budget_tokens: 16384 },
  output_config: { effort: "medium" },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```csharp C#
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta;
using Anthropic.Models.Beta.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = "claude-sonnet-4-6",
            MaxTokens = 16384,
            Thinking = new BetaThinkingConfigEnabled { BudgetTokens = 16384 },
            OutputConfig = new BetaOutputConfig
            {
                Effort = Effort.Medium
            },
            Betas = [AnthropicBeta.InterleavedThinking2025_05_14],
            Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
        };

        var message = await client.Beta.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-sonnet-4-6",
		MaxTokens: 16384,
		Thinking:  anthropic.BetaThinkingConfigParamOfEnabled(16384),
		OutputConfig: anthropic.BetaOutputConfigParam{
			Effort: anthropic.BetaOutputConfigEffortMedium,
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Your prompt here")),
		},
		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaInterleavedThinking2025_05_14},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..4,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaThinkingConfigEnabled;
import com.anthropic.models.beta.messages.BetaOutputConfig;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-sonnet-4-6")
            .maxTokens(16384L)
            .thinking(BetaThinkingConfigEnabled.builder()
                .budgetTokens(16384L)
                .build())
            .outputConfig(BetaOutputConfig.builder()
                .effort(BetaOutputConfig.Effort.MEDIUM)
                .build())
            .addBeta("interleaved-thinking-2025-05-14")
            .addUserMessage("Your prompt here")
            .build();

        BetaMessage response = client.beta().messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->beta->messages->create(
    maxTokens: 16384,
    messages: [['role' => 'user', 'content' => 'Your prompt here']],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 16384],
    outputConfig: ['effort' => 'medium'],
    betas: ['interleaved-thinking-2025-05-14'],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.beta.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 16384,
  thinking: {
    type: "enabled",
    budget_tokens: 16384
  },
  output_config: {
    effort: "medium"
  },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [
    { role: "user", content: "Your prompt here" }
  ]
)
puts message
```
</CodeGroup>

###### Kasus penggunaan chat dan non-coding

Untuk chat, pembuatan konten, pencarian, klasifikasi, dan tugas non-coding lainnya, mulai dengan effort `low` dengan extended thinking. Jika Anda memerlukan kedalaman lebih, tingkatkan effort ke `medium`.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: interleaved-thinking-2025-05-14" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 8192,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16384
    },
    "output_config": {
        "effort": "low"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

```bash CLI
ant beta:messages create --beta interleaved-thinking-2025-05-14 <<'YAML'
model: claude-sonnet-4-6
max_tokens: 8192
thinking:
  type: enabled
  budget_tokens: 16384
output_config:
  effort: low
messages:
  - role: user
    content: Your prompt here
YAML
```

```python Python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "low"},
    betas=["interleaved-thinking-2025-05-14"],
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  thinking: { type: "enabled", budget_tokens: 16384 },
  output_config: { effort: "low" },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```csharp C#
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta;
using Anthropic.Models.Beta.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = "claude-sonnet-4-6",
            MaxTokens = 8192,
            Thinking = new BetaThinkingConfigEnabled { BudgetTokens = 16384 },
            OutputConfig = new BetaOutputConfig
            {
                Effort = Effort.Low
            },
            Betas = [AnthropicBeta.InterleavedThinking2025_05_14],
            Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
        };

        var message = await client.Beta.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-sonnet-4-6",
		MaxTokens: 8192,
		Thinking:  anthropic.BetaThinkingConfigParamOfEnabled(16384),
		OutputConfig: anthropic.BetaOutputConfigParam{
			Effort: anthropic.BetaOutputConfigEffortLow,
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Your prompt here")),
		},
		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaInterleavedThinking2025_05_14},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..4,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaThinkingConfigEnabled;
import com.anthropic.models.beta.messages.BetaOutputConfig;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-sonnet-4-6")
            .maxTokens(8192L)
            .thinking(BetaThinkingConfigEnabled.builder()
                .budgetTokens(16384L)
                .build())
            .outputConfig(BetaOutputConfig.builder()
                .effort(BetaOutputConfig.Effort.LOW)
                .build())
            .addBeta("interleaved-thinking-2025-05-14")
            .addUserMessage("Your prompt here")
            .build();

        BetaMessage response = client.beta().messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->beta->messages->create(
    maxTokens: 8192,
    messages: [['role' => 'user', 'content' => 'Your prompt here']],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 16384],
    outputConfig: ['effort' => 'low'],
    betas: ['interleaved-thinking-2025-05-14'],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.beta.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  thinking: {
    type: "enabled",
    budget_tokens: 16384
  },
  output_config: {
    effort: "low"
  },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [
    { role: "user", content: "Your prompt here" }
  ]
)
puts message
```
</CodeGroup>

### Daftar periksa migrasi Sonnet 4.6

- [ ] Perbarui ID model ke `claude-sonnet-4-6`
- [ ] **BREAKING:** Hapus prefilling pesan asisten; gunakan structured outputs atau `output_config.format` sebagai gantinya
- [ ] **BREAKING:** Verifikasi parsing JSON parameter tool menangani perbedaan escaping
- [ ] **BREAKING:** Perbarui versi tool ke versi terbaru (`text_editor_20250728`, `code_execution_20250825`); versi legacy tidak didukung (jika bermigrasi dari 3.x)
- [ ] **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **BREAKING:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya (jika bermigrasi dari 3.x)
- [ ] Tangani alasan stop `refusal` baru dalam aplikasi Anda
- [ ] Hapus header beta `fine-grained-tool-streaming-2025-05-14` (sekarang GA)
- [ ] Migrasikan `output_format` ke `output_config.format`
- [ ] Tinjau dan perbarui prompt mengikuti [prompting best practices](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] **Direkomendasikan:** Migrasikan dari `thinking: {type: "enabled", budget_tokens: N}` ke `thinking: {type: "adaptive"}` dengan [parameter effort](/docs/id/build-with-claude/effort) (`budget_tokens` sudah usang dan akan dihapus dalam rilis di masa depan)
- [ ] Uji di lingkungan pengembangan sebelum deployment produksi

---

## Bermigrasi ke Claude Sonnet 4.5

Claude Sonnet 4.5 menggabungkan kecerdasan yang kuat dengan performa cepat, menjadikannya ideal untuk tugas coding, analisis, dan konten sehari-hari.

Untuk gambaran lengkap kemampuan, lihat [models overview](/docs/id/about-claude/models/overview).

<Note>
Harga Sonnet 4.5 adalah $3 per juta token input, $15 per juta token output. Lihat [Claude pricing](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Sonnet 4
model = "claude-sonnet-4-20250514"  # Sebelum
model = "claude-sonnet-4-5-20250929"  # Sesudah

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Sebelum
model = "claude-sonnet-4-5-20250929"  # Sesudah
```

### Perubahan yang merusak

Perubahan yang merusak ini berlaku saat bermigrasi dari model Claude 3.x Sonnet.

1. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Perbarui versi tool**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi tool terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani alasan stop `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan stop `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [prompting best practices](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Sonnet 4.5

- [ ] Perbarui ID model ke `claude-sonnet-4-5-20250929`
- [ ] **BREAKING:** Perbarui versi tool ke versi terbaru (`text_editor_20250728`, `code_execution_20250825`); versi legacy tidak didukung (jika bermigrasi dari 3.x)
- [ ] **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **BREAKING:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya (jika bermigrasi dari 3.x)
- [ ] Tangani alasan stop `refusal` baru dalam aplikasi Anda
- [ ] Tinjau dan perbarui prompt mengikuti [prompting best practices](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Pertimbangkan mengaktifkan extended thinking untuk tugas penalaran kompleks
- [ ] Uji di lingkungan pengembangan sebelum deployment produksi

---

## Bermigrasi ke Claude Haiku 4.5

Claude Haiku 4.5 adalah model Haiku tercepat dan paling cerdas dengan performa mendekati frontier, memberikan kualitas model premium untuk aplikasi interaktif dan pemrosesan volume tinggi.

Untuk gambaran lengkap kemampuan, lihat [models overview](/docs/id/about-claude/models/overview).

<Note>
Harga Haiku 4.5 adalah $1 per juta token input, $5 per juta token output. Lihat [Claude pricing](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Haiku 3.5
model = "claude-3-5-haiku-20241022"  # Sebelum
model = "claude-haiku-4-5-20251001"  # Sesudah

# Dari Haiku 3
model = "claude-3-haiku-20240307"  # Sebelum
model = "claude-haiku-4-5-20251001"  # Sesudah
```

**Tinjau batas laju baru:** Haiku 4.5 memiliki batas laju terpisah dari Haiku 3.5 dan Haiku 3. Lihat [dokumentasi Rate limits](/docs/id/api/rate-limits) untuk detail.

<Tip>
Untuk peningkatan performa signifikan pada tugas coding dan penalaran, pertimbangkan mengaktifkan extended thinking dengan `thinking: {type: "enabled", budget_tokens: N}`.
</Tip>

<Note>
Extended thinking berdampak pada efisiensi [prompt caching](/docs/id/build-with-claude/prompt-caching#caching-with-thinking-blocks).

Extended thinking sudah usang dalam model Claude 4.6 atau lebih baru. Jika menggunakan model lebih baru, gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) sebagai gantinya.
</Note>

**Jelajahi kemampuan baru:** Lihat [models overview](/docs/id/about-claude/models/overview) untuk detail tentang context awareness, peningkatan kapasitas output (64k token), kecerdasan lebih tinggi, dan kecepatan yang ditingkatkan.

### Perubahan yang merusak

Perubahan yang merusak ini berlaku saat bermigrasi dari model Claude 3.x Haiku.

1. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Perbarui versi tool**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi tool terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani alasan stop `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan stop `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [prompting best practices](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Haiku 4.5

- [ ] Perbarui ID model ke `claude-haiku-4-5-20251001`
- [ ] **BREAKING:** Perbarui versi tool ke versi terbaru (`text_editor_20250728`, `code_execution_20250825`); versi legacy tidak didukung
- [ ] **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **BREAKING:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya
- [ ] Tangani alasan stop `refusal` baru dalam aplikasi Anda
- [ ] Tinjau dan sesuaikan untuk batas laju baru (terpisah dari Haiku 3.5)
- [ ] Tinjau dan perbarui prompt mengikuti [prompting best practices](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Pertimbangkan mengaktifkan extended thinking untuk tugas penalaran kompleks
- [ ] Uji di lingkungan pengembangan sebelum deployment produksi

---

## Dapatkan bantuan

- Periksa [dokumentasi API](/docs/id/api/overview) untuk spesifikasi detail
- Tinjau [model capabilities](/docs/id/about-claude/models/overview) untuk perbandingan performa
- Tinjau [API release notes](/docs/id/release-notes/api) untuk pembaruan API
- Hubungi dukungan jika Anda mengalami masalah apa pun selama migrasi