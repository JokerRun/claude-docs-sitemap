---
source: platform
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/content-moderation
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: ad04cf53b436daa2463ba6d9b8dba09a8b4ad5440e41355cf3a748ef581ff9e5
---

# Moderasi konten

Moderasi konten adalah aspek penting dalam menjaga lingkungan yang aman, saling menghormati, dan produktif dalam aplikasi digital. Panduan ini membahas bagaimana Claude dapat digunakan untuk memoderasi konten dalam aplikasi digital Anda.

---

> Kunjungi [cookbook moderasi konten](https://platform.claude.com/cookbook/misc-building-moderation-filter) untuk melihat contoh implementasi moderasi konten menggunakan Claude.

<Tip>
  Panduan ini berfokus pada moderasi konten yang dibuat pengguna dalam aplikasi Anda. Jika Anda mencari panduan tentang memoderasi interaksi dengan Claude, lihat 

  [panduan guardrails](/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

  .
</Tip>

## Sebelum membangun dengan Claude

### Tentukan apakah akan menggunakan Claude untuk moderasi konten

Berikut adalah beberapa indikator utama bahwa Anda sebaiknya menggunakan LLM seperti Claude alih-alih pendekatan ML tradisional atau berbasis aturan untuk moderasi konten:

<AccordionGroup>
  <Accordion title="Anda menginginkan implementasi yang hemat biaya dan cepat">
    Metode ML tradisional memerlukan sumber daya rekayasa yang signifikan, keahlian ML, dan biaya infrastruktur. Sistem moderasi manusia menimbulkan biaya yang lebih tinggi lagi. Dengan Claude, Anda dapat memiliki sistem moderasi yang canggih dan berjalan dalam waktu yang jauh lebih singkat dengan biaya yang jauh lebih rendah.
  </Accordion>

  <Accordion title="Anda menginginkan pemahaman semantik sekaligus keputusan yang cepat">
    Pendekatan ML tradisional, seperti model bag-of-words atau pencocokan pola sederhana, sering kali kesulitan memahami nada, maksud, dan konteks dari konten. Meskipun sistem moderasi manusia unggul dalam memahami makna semantik, mereka memerlukan waktu untuk meninjau konten. Claude menjembatani kesenjangan ini dengan menggabungkan pemahaman semantik dengan kemampuan untuk memberikan keputusan moderasi dengan cepat.
  </Accordion>

  <Accordion title="Anda membutuhkan keputusan kebijakan yang konsisten">
    Dengan memanfaatkan kemampuan penalaran tingkat lanjutnya, Claude dapat menafsirkan dan menerapkan pedoman moderasi yang kompleks secara seragam. Konsistensi ini membantu memastikan perlakuan yang adil terhadap semua konten, mengurangi risiko keputusan moderasi yang tidak konsisten atau bias yang dapat merusak kepercayaan pengguna.
  </Accordion>

  <Accordion title="Kebijakan moderasi Anda kemungkinan akan berubah atau berkembang seiring waktu">
    Setelah pendekatan ML tradisional ditetapkan, mengubahnya adalah upaya yang melelahkan dan membutuhkan banyak data. Di sisi lain, seiring produk atau kebutuhan pelanggan Anda berkembang, Claude dapat dengan mudah beradaptasi dengan perubahan atau penambahan pada kebijakan moderasi tanpa pelabelan ulang data pelatihan yang ekstensif.
  </Accordion>

  <Accordion title="Anda memerlukan penalaran yang dapat diinterpretasikan untuk keputusan moderasi Anda">
    Jika Anda ingin memberikan penjelasan yang jelas kepada pengguna atau regulator di balik keputusan moderasi, Claude dapat menghasilkan justifikasi yang terperinci dan koheren. Transparansi ini penting untuk membangun kepercayaan dan memastikan akuntabilitas dalam praktik moderasi konten.
  </Accordion>

  <Accordion title="Anda membutuhkan dukungan multibahasa tanpa memelihara model terpisah">
    Pendekatan ML tradisional biasanya memerlukan model terpisah atau proses penerjemahan yang ekstensif untuk setiap bahasa yang didukung. Moderasi manusia memerlukan perekrutan tenaga kerja yang fasih dalam setiap bahasa yang didukung. Kemampuan multibahasa Claude memungkinkannya mengklasifikasikan tiket dalam berbagai bahasa tanpa memerlukan model terpisah atau proses penerjemahan yang ekstensif, menyederhanakan moderasi untuk basis pelanggan global.
  </Accordion>

  <Accordion title="Anda memerlukan dukungan multimodal">
    Kemampuan multimodal Claude memungkinkannya menganalisis dan menafsirkan konten baik dalam bentuk teks maupun gambar. Ini menjadikannya alat serbaguna untuk moderasi konten yang komprehensif di lingkungan di mana berbagai jenis media perlu dievaluasi bersama.
  </Accordion>
</AccordionGroup>

<Note>
  Anthropic telah melatih semua model Claude untuk jujur, membantu, dan tidak berbahaya. Hal ini dapat menyebabkan Claude memoderasi konten yang dianggap sangat berbahaya (sesuai dengan 

  [Kebijakan Penggunaan yang Dapat Diterima](https://www.anthropic.com/legal/aup)

  ), terlepas dari prompt yang digunakan. Misalnya, situs web dewasa yang ingin mengizinkan pengguna memposting konten seksual eksplisit mungkin mendapati bahwa Claude tetap menandai konten eksplisit sebagai memerlukan moderasi, meskipun mereka menentukan dalam prompt mereka untuk tidak memoderasi konten seksual eksplisit. Pertimbangkan untuk meninjau AUP sebelum membangun solusi moderasi.
</Note>

### Buat contoh konten untuk dimoderasi

Sebelum mengembangkan solusi moderasi konten, pertama-tama buat contoh konten yang harus ditandai dan konten yang tidak boleh ditandai. Pastikan Anda menyertakan kasus tepi (edge case) dan skenario menantang yang mungkin sulit ditangani secara efektif oleh sistem moderasi konten. Setelah itu, tinjau contoh-contoh Anda untuk membuat daftar kategori moderasi yang terdefinisi dengan baik. Misalnya, contoh yang dihasilkan oleh platform media sosial mungkin mencakup hal berikut:

```python
allowed_user_comments = [
    "This movie was great, I really enjoyed it. The main actor really killed it!",
    "I hate Mondays.",
    "It is a great time to invest in gold!",
]

disallowed_user_comments = [
    "Delete this post now or you better hide. I am coming after you and your family.",
    "Stay away from the 5G cellphones!! They are using 5G to control you.",
    "Congratulations! You have won a $1,000 gift card. Click here to claim your prize!",
]

# Contoh komentar pengguna untuk menguji moderasi konten
user_comments = allowed_user_comments + disallowed_user_comments

# Daftar kategori yang dianggap tidak aman untuk moderasi konten
unsafe_categories = [
    "Child Exploitation",
    "Conspiracy Theories",
    "Hate",
    "Indiscriminate Weapons",
    "Intellectual Property",
    "Non-Violent Crimes",
    "Privacy",
    "Self-Harm",
    "Sex Crimes",
    "Sexual Content",
    "Specialized Advice",
    "Violent Crimes",
]
```

Memoderasi contoh-contoh ini secara efektif memerlukan pemahaman bahasa yang bernuansa. Dalam komentar, `This movie was great, I really enjoyed it. The main actor really killed it!`, sistem moderasi konten perlu mengenali bahwa "killed it" adalah metafora, bukan indikasi kekerasan yang sebenarnya. Sebaliknya, meskipun tidak ada penyebutan kekerasan secara eksplisit, komentar `Delete this post now or you better hide. I am coming after you and your family.` harus ditandai oleh sistem moderasi konten.

Daftar `unsafe_categories` dapat disesuaikan agar sesuai dengan kebutuhan spesifik Anda. Misalnya, jika Anda ingin mencegah anak di bawah umur membuat konten di situs web Anda, Anda dapat menambahkan "Underage Posting" ke daftar tersebut.

***

## Cara memoderasi konten menggunakan Claude

### Pilih model Claude yang tepat

Saat memilih model, penting untuk mempertimbangkan ukuran data Anda. Jika biaya menjadi perhatian, model yang lebih kecil seperti Claude Haiku 4.5 adalah pilihan yang sangat baik karena efektivitas biayanya. Di bawah ini adalah perkiraan biaya untuk memoderasi teks untuk platform media sosial yang menerima satu miliar postingan per bulan:

* **Ukuran konten**

  * Postingan per bulan: 1 miliar
  * Karakter per postingan: 100
  * Total karakter: 100 miliar

* **Perkiraan token**

  * Token input: 28,6 miliar (dengan asumsi 1 token per 3,5 karakter)
  * Persentase pesan yang ditandai: 3%
  * Token output per pesan yang ditandai: 50
  * Total token output: 1,5 miliar

* **Perkiraan biaya Claude Haiku 4.5**

  * Biaya token input: 28.600 MTok \* $1,00/MTok = $28.600 USD
  * Biaya token output: 1.500 MTok \* $5,00/MTok = $7.500 USD
  * Biaya bulanan: $28.600 + $7.500 = $36.100 USD

* **Perkiraan biaya Claude Opus 4.8**

  * Biaya token input: 28.600 MTok \* $5,00/MTok = $143.000 USD
  * Biaya token output: 1.500 MTok \* $25,00/MTok = $37.500 USD
  * Biaya bulanan: $143.000 + $37.500 = $180.500 USD

<Tip>
  Biaya aktual mungkin berbeda dari perkiraan ini. Perkiraan ini didasarkan pada prompt yang disorot di bagian tentang 

  [pemrosesan batch](#consider-batch-processing)

  . Token output dapat dikurangi lebih lanjut dengan menghapus field 

  `explanation`

   dari respons.
</Tip>

### Bangun prompt yang kuat

Untuk menggunakan Claude untuk moderasi konten, Claude harus memahami persyaratan moderasi aplikasi Anda. Mari kita mulai dengan menulis prompt yang memungkinkan Anda mendefinisikan kebutuhan moderasi Anda:

```python Python
import json

# Inisialisasi klien Anthropic
client = anthropic.Anthropic()


def moderate_message(message, unsafe_categories):
    # Konversi daftar kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
    unsafe_category_str = "\n".join(unsafe_categories)

    # Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
    assessment_prompt = f"""
    Determine whether the following message warrants moderation,
    based on the unsafe categories outlined below.

    Message:
    <message>{message}</message>

    Unsafe Categories:
    <categories>
    {unsafe_category_str}
    </categories>

    Respond with ONLY a JSON object, using the format below:
    {{
    "violation": <Boolean field denoting whether the message should be moderated>,
    "categories": [Comma-separated list of violated categories],
    "explanation": [Optional. Only include if there is a violation.]
    }}"""

    # Kirim permintaan ke Claude untuk moderasi konten
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
        max_tokens=200,
        temperature=0,  # Use 0 temperature for increased consistency
        messages=[{"role": "user", "content": assessment_prompt}],
    )

    # Parse respons JSON dari Claude
    assessment = json.loads(response.content[0].text)

    # Ekstrak status pelanggaran dari penilaian
    contains_violation = assessment["violation"]

    # Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
    violated_categories = assessment.get("categories", []) if contains_violation else []
    explanation = assessment.get("explanation") if contains_violation else None

    return contains_violation, violated_categories, explanation


# Proses setiap komentar dan cetak hasilnya
for comment in user_comments:
    print(f"\nComment: {comment}")
    violation, violated_categories, explanation = moderate_message(
        comment, unsafe_categories
    )

    if violation:
        print(f"Violated Categories: {', '.join(violated_categories)}")
        print(f"Explanation: {explanation}")
    else:
        print("No issues detected.")
```

Dalam contoh ini, fungsi `moderate_message` berisi prompt penilaian yang mencakup kategori konten tidak aman dan pesan yang akan dievaluasi. Prompt tersebut meminta Claude untuk menilai apakah pesan harus dimoderasi, berdasarkan kategori tidak aman yang didefinisikan di atas.

Penilaian model kemudian diurai untuk menentukan apakah ada pelanggaran. Jika ada pelanggaran, Claude juga mengembalikan daftar kategori yang dilanggar, serta penjelasan mengapa pesan tersebut tidak aman.

### Evaluasi prompt Anda

Moderasi konten adalah masalah klasifikasi. Dengan demikian, Anda dapat menggunakan teknik yang sama yang diuraikan dalam [cookbook klasifikasi](https://platform.claude.com/cookbook/capabilities-classification-guide) untuk menentukan akurasi sistem moderasi konten Anda.

Satu pertimbangan tambahan adalah bahwa alih-alih memperlakukan moderasi konten sebagai masalah klasifikasi biner, Anda dapat membuat beberapa kategori untuk mewakili berbagai tingkat risiko. Membuat beberapa tingkat risiko memungkinkan Anda menyesuaikan agresivitas moderasi Anda. Misalnya, Anda mungkin ingin secara otomatis memblokir kueri pengguna yang dianggap berisiko tinggi, sementara pengguna dengan banyak kueri berisiko sedang ditandai untuk tinjauan manusia.

```python Python
import json

# Inisialisasi klien Anthropic
client = anthropic.Anthropic()


def assess_risk_level(message, unsafe_categories):
    # Konversi daftar kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
    unsafe_category_str = "\n".join(unsafe_categories)

    # Susun prompt untuk Claude, termasuk pesan, kategori tidak aman, dan definisi tingkat risiko
    assessment_prompt = f"""
    Assess the risk level of the following message,
    based on the unsafe categories listed below.

Message:
<message>{message}</message>

Unsafe Categories:
<categories>
{unsafe_category_str}
</categories>

Assign a risk level based on your confidence that the user's message should be moderated
based on the defined unsafe categories:

0 - No risk
1 - Low risk
2 - Medium risk
3 - High risk

Respond with ONLY a JSON object, using the format below:
{{
  "risk_level": <Numerical field denoting the risk level>,
  "categories": [Comma-separated list of violated categories],
  "explanation": <Optional. Only include if risk level is greater than 0>
}}"""

    # Kirim permintaan ke Claude untuk penilaian risiko
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
        max_tokens=200,
        temperature=0,  # Use 0 temperature for increased consistency
        messages=[{"role": "user", "content": assessment_prompt}],
    )

    # Parse respons JSON dari Claude
    assessment = json.loads(response.content[0].text)

    # Ekstrak tingkat risiko, kategori yang dilanggar, dan penjelasan dari penilaian
    risk_level = assessment["risk_level"]
    violated_categories = assessment["categories"]
    explanation = assessment.get("explanation")

    return risk_level, violated_categories, explanation


# Proses setiap komentar dan cetak hasilnya
for comment in user_comments:
    print(f"\nComment: {comment}")
    risk_level, violated_categories, explanation = assess_risk_level(
        comment, unsafe_categories
    )

    print(f"Risk Level: {risk_level}")
    if violated_categories:
        print(f"Violated Categories: {', '.join(violated_categories)}")
    if explanation:
        print(f"Explanation: {explanation}")
```

Kode ini mengimplementasikan fungsi `assess_risk_level` yang menggunakan Claude untuk mengevaluasi tingkat risiko sebuah pesan. Fungsi ini menerima pesan dan daftar kategori tidak aman sebagai input.

Di dalam fungsi, sebuah prompt dibuat untuk Claude, yang mencakup pesan yang akan dinilai, kategori tidak aman, dan instruksi spesifik untuk mengevaluasi tingkat risiko. Prompt tersebut menginstruksikan Claude untuk merespons dengan objek JSON yang mencakup tingkat risiko, kategori yang dilanggar, dan penjelasan opsional.

Pendekatan ini memungkinkan moderasi konten yang fleksibel dengan menetapkan tingkat risiko. Pendekatan ini dapat diintegrasikan dengan mulus ke dalam sistem yang lebih besar untuk mengotomatiskan pemfilteran konten atau menandai komentar untuk tinjauan manusia berdasarkan tingkat risiko yang dinilai. Misalnya, saat menjalankan kode ini, komentar `Delete this post now or you better hide. I am coming after you and your family.` diidentifikasi sebagai risiko tinggi karena ancaman berbahayanya. Sebaliknya, komentar `Stay away from the 5G cellphones!! They are using 5G to control you.` dikategorikan sebagai risiko sedang.

### Terapkan prompt Anda

Setelah Anda yakin dengan kualitas solusi Anda, saatnya untuk menerapkannya ke produksi. Berikut adalah beberapa praktik terbaik yang harus diikuti saat menggunakan moderasi konten dalam produksi:

1. **Berikan umpan balik yang jelas kepada pengguna:** Ketika input pengguna diblokir atau respons ditandai karena moderasi konten, berikan umpan balik yang informatif dan konstruktif untuk membantu pengguna memahami mengapa pesan mereka ditandai dan bagaimana mereka dapat menyusun ulang dengan tepat. Dalam contoh kode sebelumnya, ini dilakukan melalui field `explanation` dalam respons Claude.

2. **Analisis konten yang dimoderasi:** Lacak jenis konten yang ditandai oleh sistem moderasi Anda untuk mengidentifikasi tren dan area potensial untuk perbaikan.

3. **Evaluasi dan tingkatkan secara berkelanjutan:** Secara teratur nilai kinerja sistem moderasi konten Anda menggunakan metrik seperti pelacakan presisi dan recall. Gunakan data ini untuk secara iteratif menyempurnakan prompt moderasi, kata kunci, dan kriteria penilaian Anda.

***

## Tingkatkan kinerja

Dalam skenario yang kompleks, mungkin berguna untuk mempertimbangkan strategi tambahan untuk meningkatkan kinerja di luar [teknik rekayasa prompt](/docs/id/build-with-claude/prompt-engineering/overview) standar. Berikut adalah beberapa strategi lanjutan:

### Definisikan topik dan berikan contoh

Selain mencantumkan kategori tidak aman dalam prompt, peningkatan lebih lanjut dapat dilakukan dengan memberikan definisi dan frasa yang terkait dengan setiap kategori.

```python Python
import json

# Inisialisasi klien Anthropic
client = anthropic.Anthropic()

# Kamus kategori yang dianggap tidak aman untuk moderasi konten, beserta definisinya
unsafe_category_definitions = {
    "Child Exploitation": "Content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.",
    "Conspiracy Theories": """Content that promotes or endorses unfounded, false, or misleading theories about events, situations, or individuals,
        which can incite harm or undermine public trust in institutions or facts.""",
    "Hate": """Content that is hateful toward people on the basis of their protected characteristics
        (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease),
        or content that perpetuates negative stereotypes.""",
    "Indiscriminate Weapons": "Content that enables the creation of weapons of mass destruction.",
    "Intellectual Property": "Content that violates the intellectual property rights of third parties.",
    "Non-Violent Crimes": "Content that enables, encourages, or excuses the commission of non-violent crimes.",
    "Privacy": "Content that contains sensitive, personal information about private individuals.",
    "Self-Harm": "Content that enables, encourages, or excuses acts of intentional self-harm.",
    "Sex Crimes": "Content that enables, encourages, or excuses the commission of sex crimes.",
    "Sexual Content": "Content that contains erotic descriptions or explicit depictions of sex acts.",
    "Specialized Advice": """Content that contains financial, medical, or legal advice.
        Financial advice includes guidance on investments, stocks, bonds, or any financial planning.""",
    "Violent Crimes": "Content that enables, encourages, or excuses the commission of violent crimes.",
}


def moderate_message_with_definitions(message, unsafe_category_definitions):
    # Format string kategori tidak aman, dengan setiap kategori dan definisinya pada baris baru
    unsafe_category_str = "\n".join(
        f"{category}: {definition}"
        for category, definition in unsafe_category_definitions.items()
    )

    # Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
    assessment_prompt = f"""Determine whether the following message warrants moderation, based on the unsafe categories outlined below.

Message:
<message>{message}</message>

Unsafe Categories and Their Definitions:
<categories>
{unsafe_category_str}
</categories>

It's important that you remember all unsafe categories and their definitions.

Respond with ONLY a JSON object, using the format below:
{{
  "violation": <Boolean field denoting whether the message should be moderated>,
  "categories": [Comma-separated list of violated categories],
  "explanation": [Optional. Only include if there is a violation.]
}}"""

    # Kirim permintaan ke Claude untuk moderasi konten
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
        max_tokens=200,
        temperature=0,  # Use 0 temperature for increased consistency
        messages=[{"role": "user", "content": assessment_prompt}],
    )

    # Parse respons JSON dari Claude
    assessment = json.loads(response.content[0].text)

    # Ekstrak status pelanggaran dari penilaian
    contains_violation = assessment["violation"]

    # Jika ada pelanggaran, ambil kategori dan penjelasannya; jika tidak, gunakan nilai default kosong
    violated_categories = assessment.get("categories", []) if contains_violation else []
    explanation = assessment.get("explanation") if contains_violation else None

    return contains_violation, violated_categories, explanation


# Proses setiap komentar dan cetak hasilnya
for comment in user_comments:
    print(f"\nComment: {comment}")
    violation, violated_categories, explanation = moderate_message_with_definitions(
        comment, unsafe_category_definitions
    )

    if violation:
        print(f"Violated Categories: {', '.join(violated_categories)}")
        print(f"Explanation: {explanation}")
    else:
        print("No issues detected.")
```

Fungsi `moderate_message_with_definitions` memperluas fungsi `moderate_message` sebelumnya dengan memungkinkan setiap kategori tidak aman dipasangkan dengan definisi terperinci. Ini terjadi dalam kode dengan mengganti daftar `unsafe_categories` dari fungsi asli dengan dictionary `unsafe_category_definitions`. Dictionary ini memetakan setiap kategori tidak aman ke definisi yang sesuai. Baik nama kategori maupun definisinya disertakan dalam prompt.

Perlu dicatat, definisi untuk kategori `Specialized Advice` sekarang menentukan jenis saran keuangan yang harus dilarang. Akibatnya, komentar `It is a great time to invest in gold!`, yang sebelumnya lolos penilaian `moderate_message`, sekarang memicu pelanggaran.

### Pertimbangkan pemrosesan batch

Untuk mengurangi biaya dalam situasi di mana moderasi real-time tidak diperlukan, pertimbangkan untuk memoderasi pesan dalam batch. Sertakan beberapa pesan dalam konteks prompt, dan minta Claude untuk menilai pesan mana yang harus dimoderasi.

```python Python
import json

# Inisialisasi klien Anthropic
client = anthropic.Anthropic()


def batch_moderate_messages(messages, unsafe_categories):
    # Konversi daftar kategori tidak aman menjadi string, dengan setiap kategori pada baris baru
    unsafe_category_str = "\n".join(unsafe_categories)

    # Format string pesan, dengan setiap pesan dibungkus dalam tag mirip XML dan diberi ID
    messages_str = "\n".join(
        [f"<message id={idx}>{msg}</message>" for idx, msg in enumerate(messages)]
    )

    # Susun prompt untuk Claude, termasuk pesan dan kategori tidak aman
    assessment_prompt = f"""Determine the messages to moderate, based on the unsafe categories outlined below.

Messages:
<messages>
{messages_str}
</messages>

Unsafe Categories:
<categories>
{unsafe_category_str}
</categories>

Respond with ONLY a JSON object, using the format below:
{{
  "violations": [
    {{
      "id": <message id>,
      "categories": [list of violated categories],
      "explanation": <Explanation of why there's a violation>
    }},
    ...
  ]
}}

Important Notes:
- Remember to analyze every message for a violation.
- Select any number of violations that reasonably apply."""

    # Kirim permintaan ke Claude untuk moderasi konten
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Using the Haiku model for lower costs
        max_tokens=2048,  # Increased max token count to handle batches
        temperature=0,  # Use 0 temperature for increased consistency
        messages=[{"role": "user", "content": assessment_prompt}],
    )

    # Parse respons JSON dari Claude
    assessment = json.loads(response.content[0].text)
    return assessment


# Proses batch komentar dan dapatkan responsnya
response_obj = batch_moderate_messages(user_comments, unsafe_categories)

# Cetak hasil untuk setiap pelanggaran yang terdeteksi
for violation in response_obj["violations"]:
    print(f"""Comment: {user_comments[violation["id"]]}
Violated Categories: {", ".join(violation["categories"])}
Explanation: {violation["explanation"]}
""")
```

Dalam contoh ini, fungsi `batch_moderate_messages` menangani moderasi seluruh batch pesan dengan satu panggilan API Claude. Di dalam fungsi, sebuah prompt dibuat yang mencakup daftar pesan untuk dievaluasi dan kategori konten tidak aman. Prompt tersebut mengarahkan Claude untuk mengembalikan objek JSON yang mencantumkan semua pesan yang mengandung pelanggaran. Setiap pesan dalam respons diidentifikasi oleh id-nya, yang sesuai dengan posisi pesan dalam daftar input. Perlu diingat bahwa menemukan ukuran batch optimal untuk kebutuhan spesifik Anda mungkin memerlukan beberapa eksperimen. Meskipun ukuran batch yang lebih besar dapat menurunkan biaya, hal itu juga dapat menyebabkan sedikit penurunan kualitas. Selain itu, Anda mungkin perlu meningkatkan parameter `max_tokens` dalam panggilan API Claude untuk mengakomodasi respons yang lebih panjang. Untuk detail tentang jumlah maksimum token yang dapat dihasilkan oleh model pilihan Anda, lihat [tabel perbandingan model](/docs/id/about-claude/models/overview#latest-models-comparison).

<CardGroup cols={2}>
  <Card title="Cookbook moderasi konten" icon="link" href="https://platform.claude.com/cookbook/misc-building-moderation-filter">
    Lihat contoh berbasis kode yang diimplementasikan sepenuhnya tentang cara menggunakan Claude untuk moderasi konten.
  </Card>

  <Card title="Panduan guardrails" icon="link" href="/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations">
    Jelajahi panduan guardrails untuk teknik memoderasi interaksi dengan Claude.
  </Card>
</CardGroup>
