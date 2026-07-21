---
source: platform
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/ticket-routing
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 0a9339737b3fb57255e909538fe51dd3d4563cc07a14a065d1033b5cb2395fc5
---

# Perutean tiket

Panduan ini menjelaskan cara memanfaatkan kemampuan pemahaman bahasa alami tingkat lanjut dari Claude untuk mengklasifikasikan tiket dukungan pelanggan dalam skala besar berdasarkan maksud pelanggan, urgensi, prioritas, profil pelanggan, dan lainnya.

---

## Tentukan apakah akan menggunakan Claude untuk perutean tiket

Berikut adalah beberapa indikator utama bahwa Anda sebaiknya menggunakan LLM seperti Claude alih-alih pendekatan ML tradisional untuk tugas klasifikasi Anda:

<AccordionGroup>
  <Accordion title="Anda memiliki data pelatihan berlabel yang terbatas">
    Proses ML tradisional memerlukan dataset berlabel yang sangat besar. Model Claude yang telah dilatih sebelumnya dapat secara efektif mengklasifikasikan tiket hanya dengan beberapa lusin contoh berlabel, sehingga secara signifikan mengurangi waktu dan biaya persiapan data.
  </Accordion>

  <Accordion title="Kategori klasifikasi Anda kemungkinan akan berubah atau berkembang seiring waktu">
    Setelah pendekatan ML tradisional ditetapkan, mengubahnya adalah upaya yang melelahkan dan membutuhkan banyak data. Di sisi lain, seiring produk atau kebutuhan pelanggan Anda berkembang, Claude dapat dengan mudah beradaptasi dengan perubahan definisi kelas atau kelas baru tanpa pelabelan ulang data pelatihan yang ekstensif.
  </Accordion>

  <Accordion title="Anda perlu menangani input teks yang kompleks dan tidak terstruktur">
    Model ML tradisional sering kali kesulitan dengan data tidak terstruktur dan memerlukan rekayasa fitur yang ekstensif. Pemahaman bahasa tingkat lanjut dari Claude memungkinkan klasifikasi yang akurat berdasarkan konten dan konteks, alih-alih mengandalkan struktur ontologis yang ketat.
  </Accordion>

  <Accordion title="Aturan klasifikasi Anda didasarkan pada pemahaman semantik">
    Pendekatan ML tradisional sering kali mengandalkan model bag-of-words atau pencocokan pola sederhana. Claude unggul dalam memahami dan menerapkan aturan yang mendasarinya ketika kelas didefinisikan oleh kondisi, bukan oleh contoh.
  </Accordion>

  <Accordion title="Anda memerlukan penalaran yang dapat diinterpretasikan untuk keputusan klasifikasi">
    Banyak model ML tradisional memberikan sedikit wawasan tentang proses pengambilan keputusannya. Claude dapat memberikan penjelasan yang dapat dibaca manusia untuk keputusan klasifikasinya, membangun kepercayaan pada sistem otomatisasi dan memfasilitasi adaptasi yang mudah jika diperlukan.
  </Accordion>

  <Accordion title="Anda ingin menangani kasus tepi dan tiket ambigu dengan lebih efektif">
    Sistem ML tradisional sering kali kesulitan dengan outlier dan input ambigu, sering salah mengklasifikasikannya atau mengarahkannya ke kategori umum. Kemampuan pemrosesan bahasa alami Claude memungkinkannya untuk lebih baik menginterpretasikan konteks dan nuansa dalam tiket dukungan, yang berpotensi mengurangi jumlah tiket yang salah dirutekan atau tidak terklasifikasi yang memerlukan intervensi manual.
  </Accordion>

  <Accordion title="Anda memerlukan dukungan multibahasa tanpa memelihara model terpisah">
    Pendekatan ML tradisional biasanya memerlukan model terpisah atau proses terjemahan yang ekstensif untuk setiap bahasa yang didukung. Kemampuan multibahasa Claude memungkinkannya untuk mengklasifikasikan tiket dalam berbagai bahasa tanpa perlu model terpisah atau proses terjemahan yang ekstensif, menyederhanakan dukungan untuk basis pelanggan global.
  </Accordion>
</AccordionGroup>

***

## Bangun dan terapkan alur kerja dukungan LLM Anda

### Pahami pendekatan dukungan Anda saat ini

Sebelum terjun ke otomatisasi, sangat penting untuk memahami sistem tiket Anda yang sudah ada. Mulailah dengan menyelidiki bagaimana tim dukungan Anda saat ini menangani perutean tiket.

Pertimbangkan pertanyaan seperti:

* Kriteria apa yang digunakan untuk menentukan SLA/penawaran layanan mana yang diterapkan?
* Apakah perutean tiket digunakan untuk menentukan tingkat dukungan atau spesialis produk mana yang akan menerima tiket?
* Apakah sudah ada aturan atau alur kerja otomatis yang diterapkan? Dalam kasus apa aturan tersebut gagal?
* Bagaimana kasus tepi atau tiket ambigu ditangani?
* Bagaimana tim memprioritaskan tiket?

Semakin banyak Anda tahu tentang bagaimana manusia menangani kasus tertentu, semakin baik Anda dapat bekerja dengan Claude untuk melakukan tugas tersebut.

### Definisikan kategori maksud pengguna

Daftar kategori maksud pengguna yang terdefinisi dengan baik sangat penting untuk klasifikasi tiket dukungan yang akurat dengan Claude. Kemampuan Claude untuk merutekan tiket secara efektif dalam sistem Anda berbanding lurus dengan seberapa baik kategori sistem Anda didefinisikan.

Berikut adalah beberapa contoh kategori dan subkategori maksud pengguna.

<AccordionGroup>
  <Accordion title="Masalah teknis">
    * Masalah perangkat keras
    * Bug perangkat lunak
    * Masalah kompatibilitas
    * Masalah kinerja
  </Accordion>

  <Accordion title="Manajemen akun">
    * Reset kata sandi
    * Masalah akses akun
    * Pertanyaan penagihan
    * Perubahan langganan
  </Accordion>

  <Accordion title="Informasi produk">
    * Pertanyaan fitur
    * Pertanyaan kompatibilitas produk
    * Informasi harga
    * Pertanyaan ketersediaan
  </Accordion>

  <Accordion title="Panduan pengguna">
    * Pertanyaan cara penggunaan
    * Bantuan penggunaan fitur
    * Saran praktik terbaik
    * Panduan pemecahan masalah
  </Accordion>

  <Accordion title="Umpan balik">
    * Laporan bug
    * Permintaan fitur
    * Umpan balik atau saran umum
    * Keluhan
  </Accordion>

  <Accordion title="Terkait pesanan">
    * Pertanyaan status pesanan
    * Informasi pengiriman
    * Pengembalian dan penukaran
    * Modifikasi pesanan
  </Accordion>

  <Accordion title="Permintaan layanan">
    * Bantuan instalasi
    * Permintaan upgrade
    * Penjadwalan pemeliharaan
    * Pembatalan layanan
  </Accordion>

  <Accordion title="Kekhawatiran keamanan">
    * Pertanyaan privasi data
    * Laporan aktivitas mencurigakan
    * Bantuan fitur keamanan
  </Accordion>

  <Accordion title="Kepatuhan dan hukum">
    * Pertanyaan kepatuhan regulasi
    * Pertanyaan ketentuan layanan
    * Permintaan dokumentasi hukum
  </Accordion>

  <Accordion title="Dukungan darurat">
    * Kegagalan sistem kritis
    * Masalah keamanan mendesak
    * Masalah yang sensitif terhadap waktu
  </Accordion>

  <Accordion title="Pelatihan dan edukasi">
    * Permintaan pelatihan produk
    * Pertanyaan dokumentasi
    * Informasi webinar atau workshop
  </Accordion>

  <Accordion title="Integrasi dan API">
    * Bantuan integrasi
    * Pertanyaan penggunaan API
    * Pertanyaan kompatibilitas pihak ketiga
  </Accordion>
</AccordionGroup>

Selain maksud, perutean dan prioritas tiket juga dapat dipengaruhi oleh faktor lain seperti urgensi, jenis pelanggan, SLA, atau bahasa. Pastikan untuk mempertimbangkan kriteria perutean lainnya saat membangun sistem perutean otomatis Anda.

### Tetapkan kriteria keberhasilan

Bekerja samalah dengan tim dukungan Anda untuk [mendefinisikan kriteria keberhasilan yang jelas](/docs/id/test-and-evaluate/develop-tests) dengan tolok ukur, ambang batas, dan tujuan yang terukur.

Berikut adalah beberapa kriteria dan tolok ukur standar saat menggunakan LLM untuk perutean tiket dukungan:

<AccordionGroup>
  <Accordion title="Konsistensi klasifikasi">
    Metrik ini menilai seberapa konsisten Claude mengklasifikasikan tiket serupa dari waktu ke waktu. Ini sangat penting untuk menjaga keandalan perutean. Ukur ini dengan menguji model secara berkala menggunakan serangkaian input terstandar dan targetkan tingkat konsistensi 95% atau lebih tinggi.
  </Accordion>

  <Accordion title="Kecepatan adaptasi">
    Ini mengukur seberapa cepat Claude dapat beradaptasi dengan kategori baru atau pola tiket yang berubah. Uji ini dengan memperkenalkan jenis tiket baru dan mengukur waktu yang diperlukan model untuk mencapai akurasi yang memuaskan (misalnya, >90%) pada kategori baru ini. Targetkan adaptasi dalam 50-100 sampel tiket.
  </Accordion>

  <Accordion title="Penanganan multibahasa">
    Ini menilai kemampuan Claude untuk merutekan tiket secara akurat dalam berbagai bahasa. Ukur akurasi perutean di berbagai bahasa, dengan target penurunan akurasi tidak lebih dari 5-10% untuk bahasa non-utama.
  </Accordion>

  <Accordion title="Penanganan kasus tepi">
    Ini mengevaluasi kinerja Claude pada tiket yang tidak biasa atau kompleks. Buat set pengujian kasus tepi dan ukur akurasi perutean, dengan target setidaknya 80% akurasi pada input yang menantang ini.
  </Accordion>

  <Accordion title="Mitigasi bias">
    Ini mengukur keadilan Claude dalam perutean di berbagai demografi pelanggan. Audit keputusan perutean secara berkala untuk potensi bias, dengan target akurasi perutean yang konsisten (dalam rentang 2-3%) di semua kelompok pelanggan.
  </Accordion>

  <Accordion title="Efisiensi prompt">
    Dalam situasi di mana meminimalkan jumlah token sangat penting, kriteria ini menilai seberapa baik Claude bekerja dengan konteks minimal. Ukur akurasi perutean dengan jumlah konteks yang bervariasi, dengan target akurasi 90%+ hanya dengan judul tiket dan deskripsi singkat.
  </Accordion>

  <Accordion title="Skor keterjelasan">
    Ini mengevaluasi kualitas dan relevansi penjelasan Claude untuk keputusan peruteannya. Penilai manusia dapat memberi skor penjelasan pada skala (misalnya, 1-5), dengan tujuan mencapai skor rata-rata 4 atau lebih tinggi.
  </Accordion>
</AccordionGroup>

Berikut adalah beberapa kriteria keberhasilan umum yang mungkin berguna terlepas dari apakah LLM digunakan atau tidak:

<AccordionGroup>
  <Accordion title="Akurasi perutean">
    Akurasi perutean mengukur seberapa sering tiket ditugaskan dengan benar ke tim atau individu yang tepat pada percobaan pertama. Ini biasanya diukur sebagai persentase tiket yang dirutekan dengan benar dari total tiket. Tolok ukur industri sering menargetkan akurasi 90-95%, meskipun ini dapat bervariasi berdasarkan kompleksitas struktur dukungan.
  </Accordion>

  <Accordion title="Waktu hingga penugasan">
    Metrik ini melacak seberapa cepat tiket ditugaskan setelah dikirimkan. Waktu penugasan yang lebih cepat umumnya menghasilkan resolusi yang lebih cepat dan kepuasan pelanggan yang lebih baik. Sistem terbaik di kelasnya sering mencapai waktu penugasan rata-rata di bawah 5 menit, dengan banyak yang menargetkan perutean hampir instan (yang dimungkinkan dengan implementasi LLM).
  </Accordion>

  <Accordion title="Tingkat perutean ulang">
    Tingkat perutean ulang menunjukkan seberapa sering tiket perlu ditugaskan ulang setelah perutean awal. Tingkat yang lebih rendah menunjukkan perutean awal yang lebih akurat. Targetkan tingkat perutean ulang di bawah 10%, dengan sistem berkinerja terbaik mencapai tingkat serendah 5% atau kurang.
  </Accordion>

  <Accordion title="Tingkat resolusi kontak pertama">
    Ini mengukur persentase tiket yang diselesaikan selama interaksi pertama dengan pelanggan. Tingkat yang lebih tinggi menunjukkan perutean yang efisien dan tim dukungan yang siap. Tolok ukur industri biasanya berkisar antara 70-75%, dengan performa terbaik mencapai tingkat 80% atau lebih tinggi.
  </Accordion>

  <Accordion title="Waktu penanganan rata-rata">
    Waktu penanganan rata-rata mengukur berapa lama waktu yang dibutuhkan untuk menyelesaikan tiket dari awal hingga akhir. Perutean yang efisien dapat secara signifikan mengurangi waktu ini. Tolok ukur sangat bervariasi berdasarkan industri dan kompleksitas, tetapi banyak organisasi menargetkan untuk menjaga waktu penanganan rata-rata di bawah 24 jam untuk masalah non-kritis.
  </Accordion>

  <Accordion title="Skor kepuasan pelanggan">
    Sering diukur melalui survei pasca-interaksi, skor ini mencerminkan kepuasan pelanggan secara keseluruhan dengan proses dukungan. Perutean yang efektif berkontribusi pada kepuasan yang lebih tinggi. Targetkan skor CSAT 90% atau lebih tinggi, dengan performa terbaik sering mencapai tingkat kepuasan 95%+.
  </Accordion>

  <Accordion title="Tingkat eskalasi">
    Ini mengukur seberapa sering tiket perlu dieskalasi ke tingkat dukungan yang lebih tinggi. Tingkat eskalasi yang lebih rendah sering menunjukkan perutean awal yang lebih akurat. Upayakan tingkat eskalasi di bawah 20%, dengan sistem terbaik di kelasnya mencapai tingkat 10% atau kurang.
  </Accordion>

  <Accordion title="Produktivitas agen">
    Metrik ini melihat berapa banyak tiket yang dapat ditangani agen secara efektif setelah menerapkan solusi perutean. Perutean yang lebih baik seharusnya meningkatkan produktivitas. Ukur ini dengan melacak tiket yang diselesaikan per agen per hari atau jam, dengan target peningkatan 10-20% setelah menerapkan sistem perutean baru.
  </Accordion>

  <Accordion title="Tingkat pengalihan layanan mandiri">
    Ini mengukur persentase tiket potensial yang diselesaikan melalui opsi layanan mandiri sebelum masuk ke sistem perutean. Tingkat yang lebih tinggi menunjukkan triase pra-perutean yang efektif. Targetkan tingkat pengalihan 20-30%, dengan performa terbaik mencapai tingkat 40% atau lebih tinggi.
  </Accordion>

  <Accordion title="Biaya per tiket">
    Metrik ini menghitung biaya rata-rata untuk menyelesaikan setiap tiket dukungan. Perutean yang efisien seharusnya membantu mengurangi biaya ini dari waktu ke waktu. Meskipun tolok ukur sangat bervariasi, banyak organisasi menargetkan pengurangan biaya per tiket sebesar 10-15% setelah menerapkan sistem perutean yang lebih baik.
  </Accordion>
</AccordionGroup>

### Pilih model Claude yang tepat

Pilihan model bergantung pada pertimbangan antara biaya, akurasi, dan waktu respons.

Banyak pelanggan menemukan bahwa `claude-haiku-4-5-20251001` adalah model yang ideal untuk perutean tiket, karena merupakan model tercepat dan paling hemat biaya dalam keluarga Claude 4 sambil tetap memberikan hasil yang sangat baik. Jika masalah klasifikasi Anda memerlukan keahlian subjek yang mendalam atau volume kategori maksud yang besar dengan penalaran kompleks, Anda dapat memilih [model Sonnet yang lebih besar](/docs/id/about-claude/models).

### Bangun prompt yang kuat

Perutean tiket adalah jenis tugas klasifikasi. Claude menganalisis konten tiket dukungan dan mengklasifikasikannya ke dalam kategori yang telah ditentukan berdasarkan jenis masalah, urgensi, keahlian yang diperlukan, atau faktor relevan lainnya.

Mari kita tulis prompt klasifikasi tiket. Prompt awal kita harus berisi konten permintaan pengguna dan mengembalikan penalaran serta maksud.

<Tip>
  Coba [prompt generator](/docs/id/prompt-generator) di [Claude Console](/login) agar Claude menulis draf pertama untuk Anda.
</Tip>

Berikut adalah contoh prompt klasifikasi perutean tiket:

```python
def classify_support_request(ticket_contents):
    # Definisikan prompt untuk tugas klasifikasi
    classification_prompt = f"""You will be acting as a customer support ticket classification system. Your task is to analyze customer support requests and output the appropriate classification intent for each request, along with your reasoning.

        Here is the customer support request you need to classify:

        <request>{ticket_contents}</request>

        Please carefully analyze the above request to determine the customer's core intent and needs. Consider what the customer is asking for has concerns about.

        First, write out your reasoning and analysis of how to classify this request inside <reasoning> tags.

        Then, output the appropriate classification label for the request inside a <intent> tag. The valid intents are:
        <intents>
        <intent>Support, Feedback, Complaint</intent>
        <intent>Order Tracking</intent>
        <intent>Refund/Exchange</intent>
        </intents>

        A request may have ONLY ONE applicable intent. Only include the intent that is most applicable to the request.

        As an example, consider the following request:
        <request>Hello! I had high-speed fiber internet installed on Saturday and my installer, Kevin, was absolutely fantastic! Where can I send my positive review? Thanks for your help!</request>

        Here is an example of how your output should be formatted (for the above example request):
        <reasoning>The user seeks information in order to leave positive feedback.</reasoning>
        <intent>Support, Feedback, Complaint</intent>

        Here are a few more examples:
        <examples>
        <example 2>
        Example 2 Input:
        <request>I wanted to write and personally thank you for the compassion you showed towards my family during my father's funeral this past weekend. Your staff was so considerate and helpful throughout this whole process; it really took a load off our shoulders. The visitation brochures were beautiful. We'll never forget the kindness you showed us and we are so appreciative of how smoothly the proceedings went. Thank you, again, Amarantha Hill on behalf of the Hill Family.</request>

        Example 2 Output:
        <reasoning>User leaves a positive review of their experience.</reasoning>
        <intent>Support, Feedback, Complaint</intent>
        </example 2>
        <example 3>

        ...

        </example 8>
        <example 9>
        Example 9 Input:
        <request>Your website keeps sending ad-popups that block the entire screen. It took me twenty minutes just to finally find the phone number to call and complain. How can I possibly access my account information with all of these popups? Can you access my account for me, since your website is broken? I need to know what the address is on file.</request>

        Example 9 Output:
        <reasoning>The user requests help accessing their web account information.</reasoning>
        <intent>Support, Feedback, Complaint</intent>
        </example 9>

        Remember to always include your classification reasoning before your actual intent output. The reasoning should be enclosed in <reasoning> tags and the intent in <intent> tags. Return only the reasoning and the intent.
        """
```

Mari kita uraikan komponen utama dari prompt ini:

* Kita menggunakan f-string Python untuk membuat template prompt, memungkinkan `ticket_contents` disisipkan ke dalam tag `<request>`.
* Kita memberi Claude peran yang didefinisikan dengan jelas sebagai sistem klasifikasi yang dengan cermat menganalisis konten tiket untuk menentukan maksud dan kebutuhan inti pelanggan.
* Kita menginstruksikan Claude tentang format output yang tepat, dalam hal ini untuk memberikan penalaran dan analisisnya di dalam tag `<reasoning>`, diikuti oleh label klasifikasi yang sesuai di dalam tag `<intent>`.
* Kita menentukan kategori maksud yang valid: "Support, Feedback, Complaint", "Order Tracking", dan "Refund/Exchange".
* Kita menyertakan beberapa contoh (dikenal juga sebagai few-shot prompting) untuk mengilustrasikan bagaimana output harus diformat, yang meningkatkan akurasi dan konsistensi.

Alasan kita ingin Claude membagi responsnya ke dalam berbagai bagian tag XML adalah agar kita dapat menggunakan ekspresi reguler untuk mengekstrak penalaran dan maksud secara terpisah dari output. Ini memungkinkan kita untuk membuat langkah selanjutnya yang ditargetkan dalam alur kerja perutean tiket, seperti hanya menggunakan maksud untuk memutuskan kepada siapa tiket akan dirutekan.

### Terapkan prompt Anda

Sulit untuk mengetahui seberapa baik prompt Anda bekerja tanpa menerapkannya dalam pengaturan produksi uji dan [menjalankan evaluasi](/docs/id/test-and-evaluate/develop-tests).

Mari kita bangun struktur penerapan. Mulailah dengan mendefinisikan signature metode untuk membungkus panggilan kita ke Claude. Kita akan mengambil metode yang sudah mulai kita tulis, yang memiliki `ticket_contents` sebagai input, dan sekarang mengembalikan tuple `reasoning` dan `intent` sebagai output. Jika Anda memiliki otomatisasi yang sudah ada menggunakan ML tradisional, Anda sebaiknya mengikuti signature metode tersebut.

```python Python
import re

# Buat instance dari klien API Claude
client = anthropic.Anthropic()

# Tetapkan model default
DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def classify_support_request(ticket_contents):
    # Definisikan prompt untuk tugas klasifikasi
    classification_prompt = f"""You will be acting as a customer support ticket classification system.
        ...
        ... The reasoning should be enclosed in <reasoning> tags and the intent in <intent> tags. Return only the reasoning and the intent.
        """
    # Kirim prompt ke API untuk mengklasifikasikan permintaan dukungan.
    message = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": classification_prompt}],
        stream=False,
    )
    reasoning_and_intent = message.content[0].text

    # Gunakan pustaka regular expression Python untuk mengekstrak `reasoning`.
    reasoning_match = re.search(
        r"<reasoning>(.*?)</reasoning>", reasoning_and_intent, re.DOTALL
    )
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""

    # Dengan cara serupa, ekstrak juga `intent`.
    intent_match = re.search(r"<intent>(.*?)</intent>", reasoning_and_intent, re.DOTALL)
    intent = intent_match.group(1).strip() if intent_match else ""

    return reasoning, intent
```

Kode ini:

* Membuat instance client menggunakan kunci API Anda.
* Mendefinisikan fungsi `classify_support_request` yang menerima string `ticket_contents`.
* Mengirim `ticket_contents` ke Claude untuk klasifikasi menggunakan `classification_prompt`
* Mengembalikan `reasoning` dan `intent` model yang diekstrak dari respons.

Karena kita perlu menunggu seluruh teks penalaran dan maksud dihasilkan sebelum mem-parsing, kita mengatur `stream=False` (default).

***

## Evaluasi prompt Anda

Prompting sering kali memerlukan pengujian dan optimasi agar siap untuk produksi. Untuk menentukan kesiapan solusi Anda, evaluasi kinerja berdasarkan kriteria keberhasilan dan ambang batas yang telah Anda tetapkan sebelumnya.

Untuk menjalankan evaluasi Anda, Anda memerlukan kasus uji untuk dijalankan. Sisa panduan ini mengasumsikan Anda telah [mengembangkan kasus uji Anda](/docs/id/test-and-evaluate/develop-tests).

### Bangun fungsi evaluasi

Contoh evaluasi kami untuk panduan ini mengukur kinerja Claude berdasarkan tiga metrik utama:

* Akurasi
* Biaya per klasifikasi

Anda mungkin perlu menilai Claude pada sumbu lain tergantung pada faktor apa yang penting bagi Anda.

Untuk menilai ini, pertama-tama kita harus memodifikasi skrip yang kita tulis dan menambahkan fungsi untuk membandingkan maksud yang diprediksi dengan maksud sebenarnya dan menghitung persentase prediksi yang benar. Kita juga harus menambahkan fungsionalitas perhitungan biaya dan pengukuran waktu.

```python Python
import re

# Buat instance dari klien API Claude
client = anthropic.Anthropic()

# Tetapkan model default
DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def classify_support_request(request, actual_intent):
    # Definisikan prompt untuk tugas klasifikasi
    classification_prompt = f"""You will be acting as a customer support ticket classification system.
        ...
        ...The reasoning should be enclosed in <reasoning> tags and the intent in <intent> tags. Return only the reasoning and the intent.
        """

    message = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": classification_prompt}],
    )
    usage = message.usage  # Get the usage statistics for the API call for how many input and output tokens were used.
    reasoning_and_intent = message.content[0].text

    # Gunakan pustaka regular expression Python untuk mengekstrak `reasoning`.
    reasoning_match = re.search(
        r"<reasoning>(.*?)</reasoning>", reasoning_and_intent, re.DOTALL
    )
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""

    # Dengan cara serupa, ekstrak juga `intent`.
    intent_match = re.search(r"<intent>(.*?)</intent>", reasoning_and_intent, re.DOTALL)
    intent = intent_match.group(1).strip() if intent_match else ""

    # Periksa apakah prediksi model sudah benar.
    correct = actual_intent.strip() == intent.strip()

    # Kembalikan reasoning, intent, correct, dan usage.
    return reasoning, intent, correct, usage
```

Mari kita uraikan perubahan yang telah kita buat:

* Kita menambahkan `actual_intent` dari kasus uji kita ke dalam metode `classify_support_request` dan menyiapkan perbandingan untuk menilai apakah klasifikasi maksud Claude cocok dengan klasifikasi maksud acuan kita.
* Kita mengekstrak statistik penggunaan untuk panggilan API guna menghitung biaya berdasarkan token input dan output yang digunakan

### Jalankan evaluasi Anda

Evaluasi yang tepat memerlukan ambang batas dan tolok ukur yang jelas untuk menentukan apa yang merupakan hasil yang baik. Skrip di atas memberi kita nilai runtime untuk akurasi, waktu respons, dan biaya per klasifikasi, tetapi kita masih memerlukan ambang batas yang ditetapkan dengan jelas. Misalnya:

* **Akurasi:** 95% (dari 100 pengujian)
* **Biaya per klasifikasi:** pengurangan rata-rata 50% (di 100 pengujian) dari metode perutean saat ini

Memiliki ambang batas ini memungkinkan Anda untuk dengan cepat dan mudah mengetahui dalam skala besar, dan dengan empirisme yang tidak memihak, metode mana yang terbaik untuk Anda dan perubahan apa yang mungkin perlu dilakukan agar lebih sesuai dengan kebutuhan Anda.

***

## Tingkatkan kinerja

Dalam skenario yang kompleks, mungkin berguna untuk mempertimbangkan strategi tambahan untuk meningkatkan kinerja di luar [teknik rekayasa prompt](/docs/id/build-with-claude/prompt-engineering/overview) standar & [strategi implementasi guardrail](/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations). Berikut adalah beberapa skenario umum:

### Gunakan hierarki taksonomi untuk kasus dengan 20+ kategori maksud

Seiring bertambahnya jumlah kelas, jumlah contoh yang diperlukan juga bertambah, yang berpotensi membuat prompt menjadi tidak praktis. Sebagai alternatif, Anda dapat mempertimbangkan untuk menerapkan sistem klasifikasi hierarkis menggunakan campuran pengklasifikasi.

1. Atur maksud Anda dalam struktur pohon taksonomi.
2. Buat serangkaian pengklasifikasi di setiap tingkat pohon, memungkinkan pendekatan perutean bertingkat.

Misalnya, Anda mungkin memiliki pengklasifikasi tingkat atas yang secara luas mengkategorikan tiket ke dalam "Technical Issues," "Billing Questions," dan "General Inquiries." Masing-masing kategori ini kemudian dapat memiliki sub-pengklasifikasi sendiri untuk lebih menyempurnakan klasifikasi.

![](/docs/images/ticket-hierarchy.png)

* **Kelebihan - nuansa dan akurasi yang lebih besar:** Anda dapat membuat prompt yang berbeda untuk setiap jalur induk, memungkinkan klasifikasi yang lebih terarah dan spesifik konteks. Ini dapat menghasilkan akurasi yang lebih baik dan penanganan permintaan pelanggan yang lebih bernuansa.

* **Kekurangan - latensi yang meningkat:** Perlu diketahui bahwa beberapa pengklasifikasi dapat menyebabkan peningkatan "latency" (latensi), dan kami merekomendasikan untuk menerapkan pendekatan ini dengan model tercepat kami, Haiku.

### Gunakan database vektor dan pengambilan pencarian kemiripan untuk menangani tiket yang sangat bervariasi

Meskipun memberikan contoh adalah cara paling efektif untuk meningkatkan kinerja, jika permintaan dukungan sangat bervariasi, mungkin sulit untuk menyertakan cukup contoh dalam satu prompt.

Dalam skenario ini, Anda dapat menggunakan database vektor untuk melakukan pencarian kemiripan dari dataset contoh dan mengambil contoh yang paling relevan untuk kueri tertentu.

Pendekatan ini, yang diuraikan secara rinci dalam [resep klasifikasi](https://platform.claude.com/cookbook/capabilities-classification-guide) kami, telah terbukti meningkatkan kinerja dari akurasi 71% menjadi akurasi 93%.

### Perhitungkan secara spesifik kasus tepi yang diharapkan

Berikut adalah beberapa skenario di mana Claude mungkin salah mengklasifikasikan tiket (mungkin ada skenario lain yang unik untuk situasi Anda). Dalam skenario ini, pertimbangkan untuk memberikan instruksi atau contoh eksplisit dalam prompt tentang bagaimana Claude harus menangani kasus tepi:

<AccordionGroup>
  <Accordion title="Pelanggan membuat permintaan implisit">
    Pelanggan sering mengungkapkan kebutuhan secara tidak langsung. Misalnya, "Saya sudah menunggu paket saya selama lebih dari dua minggu sekarang" mungkin merupakan permintaan tidak langsung untuk status pesanan.

    * **Solusi:** Berikan Claude beberapa contoh nyata dari pelanggan untuk jenis permintaan ini, beserta maksud yang mendasarinya. Anda bisa mendapatkan hasil yang lebih baik jika Anda menyertakan alasan klasifikasi untuk maksud tiket yang sangat bernuansa, sehingga Claude dapat lebih baik menggeneralisasi logika ke tiket lainnya.
  </Accordion>

  <Accordion title="Claude memprioritaskan emosi di atas maksud">
    Ketika pelanggan mengungkapkan ketidakpuasan, Claude mungkin memprioritaskan penanganan emosi daripada menyelesaikan masalah yang mendasarinya.

    * **Solusi:** Berikan Claude arahan tentang kapan harus memprioritaskan sentimen pelanggan atau tidak. Ini bisa sesederhana "Abaikan semua emosi pelanggan. Fokus hanya pada menganalisis maksud permintaan pelanggan dan informasi apa yang mungkin diminta pelanggan."
  </Accordion>

  <Accordion title="Beberapa masalah menyebabkan kebingungan prioritas masalah">
    Ketika pelanggan menyampaikan beberapa masalah dalam satu interaksi, Claude mungkin kesulitan mengidentifikasi kekhawatiran utama.

    * **Solusi:** Klarifikasi prioritas maksud sehingga Claude dapat lebih baik memeringkat maksud yang diekstrak dan mengidentifikasi kekhawatiran utama.
  </Accordion>
</AccordionGroup>

***

## Integrasikan Claude ke dalam alur kerja dukungan Anda yang lebih besar

Integrasi yang tepat mengharuskan Anda membuat beberapa keputusan mengenai bagaimana skrip perutean tiket berbasis Claude Anda cocok dengan arsitektur sistem perutean tiket Anda yang lebih besar. Ada dua cara yang dapat Anda lakukan:

* **Berbasis push:** Sistem tiket dukungan yang Anda gunakan (misalnya Zendesk) memicu kode Anda dengan mengirimkan event webhook ke layanan perutean Anda, yang kemudian mengklasifikasikan maksud dan merutekannya.
  * Pendekatan ini lebih skalabel untuk web, tetapi mengharuskan Anda mengekspos endpoint publik.
* **Berbasis pull:** Kode Anda menarik tiket terbaru berdasarkan jadwal tertentu dan merutekannya pada saat penarikan.
  * Pendekatan ini lebih mudah diimplementasikan tetapi mungkin membuat panggilan yang tidak perlu ke sistem tiket dukungan ketika frekuensi penarikan terlalu tinggi atau mungkin terlalu lambat ketika frekuensi penarikan terlalu rendah.

Untuk kedua pendekatan ini, Anda perlu membungkus skrip Anda dalam sebuah layanan. Pilihan pendekatan bergantung pada API apa yang disediakan oleh sistem tiket dukungan Anda.

***

<CardGroup cols={2}>
  <Card title="Cookbook klasifikasi" icon="link" href="https://platform.claude.com/cookbook/capabilities-classification-guide">
    Kunjungi cookbook klasifikasi kami untuk lebih banyak contoh kode dan panduan evaluasi yang terperinci.
  </Card>

  <Card title="Claude Console" icon="link" href="/dashboard">
    Mulai membangun dan mengevaluasi alur kerja Anda di Claude Console.
  </Card>
</CardGroup>
