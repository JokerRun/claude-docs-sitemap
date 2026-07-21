---
source: platform
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/customer-support-chat
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 9b96988d47820f16cff77b71a995a8837c9fbbd9c28d145cface3fad9c74cbee
---

# Agen dukungan pelanggan

Bangun chatbot dukungan pelanggan dengan Claude yang menjawab pertanyaan produk, tetap pada topik, dan menghasilkan penawaran harga melalui penggunaan alat.

---

## Prasyarat

Untuk mengikuti panduan ini, Anda memerlukan:

* Kunci API Claude (diatur sebagai variabel lingkungan `ANTHROPIC_API_KEY`)
* Python 3.9 atau yang lebih baru

Instal paket yang diperlukan:

```bash
pip install anthropic streamlit python-dotenv
```

## Sebelum membangun dengan Claude

### Tentukan apakah akan menggunakan Claude untuk obrolan dukungan

Berikut adalah beberapa indikator utama bahwa Anda sebaiknya menggunakan LLM seperti Claude untuk mengotomatiskan sebagian proses dukungan pelanggan Anda:

<AccordionGroup>
  <Accordion title="Volume pertanyaan berulang yang tinggi">
    Claude unggul dalam menangani sejumlah besar pertanyaan serupa secara efisien, membebaskan agen manusia untuk menangani masalah yang lebih kompleks.
  </Accordion>

  <Accordion title="Kebutuhan sintesis informasi yang cepat">
    Claude dapat dengan cepat mengambil, memproses, dan menggabungkan informasi dari basis pengetahuan yang luas, sementara agen manusia mungkin memerlukan waktu untuk meneliti atau berkonsultasi dengan berbagai sumber.
  </Accordion>

  <Accordion title="Kebutuhan ketersediaan 24/7">
    Claude dapat memberikan dukungan sepanjang waktu tanpa kelelahan, sedangkan menempatkan agen manusia untuk cakupan berkelanjutan bisa mahal dan menantang.
  </Accordion>

  <Accordion title="Penskalaan cepat selama periode puncak">
    Claude dapat menangani peningkatan volume pertanyaan secara tiba-tiba tanpa perlu merekrut dan melatih staf tambahan.
  </Accordion>

  <Accordion title="Suara merek yang konsisten">
    Anda dapat menginstruksikan Claude untuk secara konsisten merepresentasikan nada dan nilai merek Anda, sedangkan agen manusia mungkin bervariasi dalam gaya komunikasi mereka.
  </Accordion>
</AccordionGroup>

Beberapa pertimbangan untuk memilih Claude dibandingkan LLM lainnya:

* Anda memprioritaskan percakapan yang alami dan bernuansa: Pemahaman bahasa Claude yang canggih memungkinkan percakapan yang lebih alami dan sadar konteks yang terasa lebih seperti manusia dibandingkan obrolan dengan LLM lainnya.
* Anda sering menerima pertanyaan yang kompleks dan terbuka: Claude dapat menangani berbagai topik dan pertanyaan tanpa menghasilkan respons kaku atau memerlukan pemrograman ekstensif untuk berbagai permutasi ucapan pengguna.
* Anda memerlukan dukungan multibahasa yang dapat diskalakan: Kemampuan multibahasa Claude memungkinkannya terlibat dalam percakapan dalam lebih dari 200 bahasa tanpa memerlukan chatbot terpisah atau proses terjemahan ekstensif untuk setiap bahasa yang didukung.

### Definisikan interaksi obrolan ideal Anda

Buat garis besar interaksi pelanggan yang ideal untuk mendefinisikan bagaimana dan kapan Anda mengharapkan pelanggan berinteraksi dengan Claude. Garis besar ini akan membantu menentukan persyaratan teknis solusi Anda.

Berikut adalah contoh interaksi obrolan untuk dukungan pelanggan asuransi mobil:

* **Pelanggan:** Memulai pengalaman obrolan dukungan
  * **Claude:** Menyapa pelanggan dengan hangat dan memulai percakapan

* **Pelanggan:** Bertanya tentang asuransi untuk mobil listrik baru mereka
  * **Claude:** Memberikan informasi relevan tentang cakupan kendaraan listrik

* **Pelanggan:** Mengajukan pertanyaan terkait kebutuhan unik untuk asuransi kendaraan listrik
  * **Claude:** Merespons dengan jawaban yang akurat dan informatif serta memberikan tautan ke sumbernya

* **Pelanggan:** Mengajukan pertanyaan di luar topik yang tidak terkait dengan asuransi atau mobil
  * **Claude:** Mengklarifikasi bahwa ia tidak membahas topik yang tidak terkait dan mengarahkan pengguna kembali ke asuransi mobil

* **Pelanggan:** Menyatakan minat pada penawaran harga asuransi

  * **Claude:** Mengajukan serangkaian pertanyaan untuk menentukan penawaran yang sesuai, menyesuaikan dengan respons mereka
  * **Claude:** Mengirim permintaan untuk menggunakan alat API pembuatan penawaran bersama dengan informasi yang diperlukan yang dikumpulkan dari pengguna
  * **Claude:** Menerima informasi respons dari penggunaan alat API, mensintesis informasi menjadi respons yang alami, dan menyajikan penawaran yang diberikan kepada pengguna

* **Pelanggan:** Mengajukan pertanyaan lanjutan

  * **Claude:** Menjawab pertanyaan lanjutan sesuai kebutuhan
  * **Claude:** Memandu pelanggan ke langkah berikutnya dalam proses asuransi dan menutup percakapan

<Tip>
  Dalam contoh nyata yang Anda tulis untuk kasus penggunaan Anda sendiri, Anda mungkin merasa berguna untuk menuliskan kata-kata sebenarnya dalam interaksi ini sehingga Anda juga dapat memahami nada ideal, panjang respons, dan tingkat detail yang Anda inginkan dari Claude.
</Tip>

### Pecah interaksi menjadi tugas-tugas unik

Obrolan dukungan pelanggan adalah kumpulan dari berbagai tugas yang berbeda, mulai dari menjawab pertanyaan hingga pengambilan informasi hingga mengambil tindakan atas permintaan, yang dikemas dalam satu interaksi pelanggan. Sebelum Anda mulai membangun, pecah interaksi pelanggan ideal Anda menjadi setiap tugas yang Anda ingin Claude dapat lakukan. Ini memastikan Anda dapat membuat prompt dan mengevaluasi Claude untuk setiap tugas, dan memberi Anda gambaran yang baik tentang rentang interaksi yang perlu Anda perhitungkan saat menulis kasus uji.

<Tip>
  Pelanggan terkadang merasa terbantu untuk memvisualisasikan ini sebagai diagram alur interaksi dari titik-titik perubahan percakapan yang mungkin terjadi tergantung pada permintaan pengguna.
</Tip>

Berikut adalah tugas-tugas utama yang terkait dengan contoh interaksi asuransi:

1. Sapaan dan panduan umum

   * Menyapa pelanggan dengan hangat dan memulai percakapan
   * Memberikan informasi umum tentang perusahaan dan interaksi

2. Informasi produk

   * Memberikan informasi tentang cakupan kendaraan listrik
     <Note>
       Ini akan mengharuskan Claude memiliki informasi yang diperlukan dalam konteksnya, dan mungkin menyiratkan bahwa 

       [integrasi RAG](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide)

        diperlukan.
     </Note>
   * Menjawab pertanyaan terkait kebutuhan asuransi kendaraan listrik yang unik
   * Menjawab pertanyaan lanjutan tentang penawaran atau detail asuransi
   * Menawarkan tautan ke sumber jika sesuai

3. Manajemen percakapan

   * Tetap pada topik (asuransi mobil)
   * Mengarahkan kembali pertanyaan di luar topik ke subjek yang relevan

4. Pembuatan penawaran

   * Mengajukan pertanyaan yang sesuai untuk menentukan kelayakan penawaran
   * Menyesuaikan pertanyaan berdasarkan respons pelanggan
   * Mengirimkan informasi yang dikumpulkan ke API pembuatan penawaran
   * Menyajikan penawaran yang diberikan kepada pelanggan

### Tetapkan kriteria keberhasilan

Bekerja sama dengan tim dukungan Anda untuk [mendefinisikan kriteria keberhasilan dan menulis evaluasi terperinci](/docs/id/test-and-evaluate/develop-tests) dengan tolok ukur dan tujuan yang terukur.

Berikut adalah kriteria dan tolok ukur yang dapat digunakan untuk mengevaluasi seberapa berhasil Claude melakukan tugas-tugas yang telah didefinisikan:

<AccordionGroup>
  <Accordion title="Akurasi pemahaman pertanyaan">
    Metrik ini mengevaluasi seberapa akurat Claude memahami pertanyaan pelanggan di berbagai topik. Ukur ini dengan meninjau sampel percakapan dan menilai apakah Claude memiliki interpretasi yang benar tentang maksud pelanggan, langkah penting berikutnya, seperti apa penyelesaian yang berhasil, dan lainnya. Targetkan akurasi pemahaman 95% atau lebih tinggi.
  </Accordion>

  <Accordion title="Relevansi respons">
    Ini menilai seberapa baik respons Claude menjawab pertanyaan atau masalah spesifik pelanggan. Evaluasi serangkaian percakapan dan beri nilai relevansi setiap respons (menggunakan penilaian berbasis LLM untuk skala). Targetkan skor relevansi 90% atau lebih.
  </Accordion>

  <Accordion title="Akurasi respons">
    Nilai kebenaran informasi umum perusahaan dan produk yang diberikan kepada pengguna, berdasarkan informasi yang diberikan kepada Claude dalam konteks. Targetkan akurasi 100% dalam informasi pengantar ini.
  </Accordion>

  <Accordion title="Relevansi penyediaan sitasi">
    Lacak frekuensi dan relevansi tautan atau sumber yang ditawarkan. Targetkan penyediaan sumber yang relevan dalam 80% interaksi di mana informasi tambahan dapat bermanfaat.
  </Accordion>

  <Accordion title="Kepatuhan topik">
    Ukur seberapa baik Claude tetap pada topik, seperti topik asuransi mobil dalam contoh implementasi. Targetkan 95% respons terkait langsung dengan asuransi mobil atau pertanyaan spesifik pelanggan.
  </Accordion>

  <Accordion title="Efektivitas pembuatan konten">
    Ukur seberapa berhasil Claude dalam menentukan kapan harus menghasilkan konten informasional dan seberapa relevan konten tersebut. Misalnya, dalam implementasi ini, Anda akan menentukan seberapa baik Claude memahami kapan harus menghasilkan penawaran dan seberapa akurat penawaran tersebut. Targetkan akurasi 100%, karena ini adalah informasi vital untuk interaksi pelanggan yang berhasil.
  </Accordion>

  <Accordion title="Efisiensi eskalasi">
    Ini mengukur kemampuan Claude untuk mengenali kapan suatu pertanyaan memerlukan intervensi manusia dan mengeskalasi dengan tepat. Lacak persentase percakapan yang dieskalasi dengan benar versus yang seharusnya dieskalasi tetapi tidak. Targetkan akurasi eskalasi 95% atau lebih tinggi.
  </Accordion>
</AccordionGroup>

Berikut adalah kriteria dan tolok ukur yang dapat digunakan untuk mengevaluasi dampak bisnis dari penggunaan Claude untuk dukungan:

<AccordionGroup>
  <Accordion title="Pemeliharaan sentimen">
    Ini menilai kemampuan Claude untuk mempertahankan atau meningkatkan sentimen pelanggan sepanjang percakapan. Gunakan alat analisis sentimen untuk mengukur sentimen di awal dan akhir setiap percakapan. Targetkan sentimen yang dipertahankan atau ditingkatkan dalam 90% interaksi.
  </Accordion>

  <Accordion title="Tingkat defleksi">
    Persentase pertanyaan pelanggan yang berhasil ditangani oleh chatbot tanpa intervensi manusia. Biasanya targetkan tingkat defleksi 70-80%, tergantung pada kompleksitas pertanyaan.
  </Accordion>

  <Accordion title="Skor kepuasan pelanggan">
    Ukuran seberapa puas pelanggan dengan interaksi chatbot mereka. Biasanya dilakukan melalui survei pasca-interaksi. Targetkan skor CSAT 4 dari 5 atau lebih tinggi.
  </Accordion>

  <Accordion title="Waktu penanganan rata-rata">
    Waktu rata-rata yang dibutuhkan chatbot untuk menyelesaikan suatu pertanyaan. Ini sangat bervariasi berdasarkan kompleksitas masalah, tetapi secara umum, targetkan AHT yang lebih rendah dibandingkan dengan agen manusia.
  </Accordion>
</AccordionGroup>

## Cara mengimplementasikan Claude sebagai agen layanan pelanggan

### Pilih model Claude yang tepat

Pilihan model bergantung pada pertukaran antara biaya, akurasi, dan waktu respons.

Untuk obrolan dukungan pelanggan, Claude Opus 4.8 sangat cocok untuk menyeimbangkan kecerdasan, latensi, dan biaya. Namun, untuk kasus di mana Anda memiliki alur percakapan dengan beberapa prompt termasuk RAG, penggunaan alat, atau prompt konteks panjang, Claude Haiku 4.5 mungkin lebih cocok untuk mengoptimalkan latensi.

### Bangun prompt yang kuat

Menggunakan Claude untuk dukungan pelanggan mengharuskan Claude memiliki arahan dan konteks yang cukup untuk merespons dengan tepat, sambil memiliki fleksibilitas yang cukup untuk menangani berbagai pertanyaan pelanggan.

Mulailah dengan menulis elemen-elemen prompt yang kuat, dimulai dengan prompt sistem. Buat file bernama `config.py` dan tambahkan setiap blok berikut ke dalamnya:

```python
IDENTITY = """You are Eva, a friendly and knowledgeable AI assistant for Acme Insurance
Company. Your role is to warmly welcome customers and provide information on
Acme's insurance offerings, which include car insurance and electric car
insurance. You can also help customers get quotes for their insurance needs."""
```

<Tip>
  Meskipun Anda mungkin tergoda untuk menempatkan semua informasi Anda di dalam prompt sistem sebagai cara untuk memisahkan instruksi dari percakapan pengguna, Claude sebenarnya bekerja paling baik dengan sebagian besar konten prompt-nya ditulis di dalam giliran 

  `User`

   pertama (dengan satu-satunya pengecualian adalah prompting peran). Baca lebih lanjut di 

  [Memberikan Claude peran dengan prompt sistem](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role)

  .
</Tip>

Sebaiknya pecah prompt yang kompleks menjadi subbagian dan tulis satu bagian pada satu waktu. Untuk setiap tugas, Anda mungkin menemukan keberhasilan yang lebih besar dengan mengikuti proses langkah demi langkah untuk mendefinisikan bagian-bagian prompt yang dibutuhkan Claude untuk melakukan tugas dengan baik. Untuk contoh dukungan pelanggan asuransi mobil ini, Anda akan menulis secara bertahap semua bagian untuk prompt yang dimulai dengan tugas "Sapaan dan panduan umum". Ini juga membuat debugging prompt Anda lebih mudah karena Anda dapat lebih cepat menyesuaikan bagian-bagian individual dari keseluruhan prompt.

```python
STATIC_GREETINGS_AND_GENERAL = """
<static_context>
Acme Auto Insurance: Your Trusted Companion on the Road

About:
At Acme Insurance, we understand that your vehicle is more than just a mode of transportation—it's your ticket to life's adventures.
Since 1985, we've been crafting auto insurance policies that give drivers the confidence to explore, commute, and travel with peace of mind.
Whether you're navigating city streets or embarking on cross-country road trips, Acme is there to protect you and your vehicle.
Our innovative auto insurance policies are designed to adapt to your unique needs, covering everything from fender benders to major collisions.
With Acme's award-winning customer service and swift claim resolution, you can focus on the joy of driving while we handle the rest.
We're not just an insurance provider—we're your co-pilot in life's journeys.
Choose Acme Auto Insurance and experience the assurance that comes with superior coverage and genuine care. Because at Acme, we don't just
insure your car—we fuel your adventures on the open road.

Note: We also offer specialized coverage for electric vehicles, ensuring that drivers of all car types can benefit from our protection.

Acme Insurance offers the following products:
- Car insurance
- Electric car insurance
- Two-wheeler insurance

Business hours: Monday-Friday, 9 AM - 5 PM EST
Customer service number: 1-800-123-4567
</static_context>
"""
```

Kemudian lakukan hal yang sama untuk informasi asuransi mobil dan asuransi mobil listrik Anda.

```python
STATIC_CAR_INSURANCE = """
<static_context>
Car Insurance Coverage:
Acme's car insurance policies typically cover:
1. Liability coverage: Pays for bodily injury and property damage you cause to others.
2. Collision coverage: Pays for damage to your car in an accident.
3. Comprehensive coverage: Pays for damage to your car from non-collision incidents.
4. Medical payments coverage: Pays for medical expenses after an accident.
5. Uninsured/underinsured motorist coverage: Protects you if you're hit by a driver with insufficient insurance.

Optional coverages include:
- Rental car reimbursement
- Roadside assistance
- New car replacement
</static_context>
"""

STATIC_ELECTRIC_CAR_INSURANCE = """
<static_context>
Electric Car Insurance:
Our specialized electric car insurance goes beyond traditional auto coverage,
offering tailored protection for your high-tech investment. In addition to standard coverages, we offer:
- Safeguarding expensive battery systems
- Covering home charging equipment
- Adapting to the rapidly evolving world of electric vehicles

Whether you're driving a Rivian, Nissan Leaf, Chevrolet Bolt,
or any other electric vehicle, our knowledgeable agents are ready to craft a policy
that gives you the confidence to enjoy every electron-powered mile.
</static_context>
"""
```

Sekarang setelah Anda memiliki konten statis, tambahkan setidaknya 4-5 contoh interaksi "baik" untuk memandu respons Claude. Contoh-contoh ini harus mewakili interaksi pelanggan ideal Anda dan dapat mencakup pagar pembatas, pemanggilan alat, dll.

```python
EXAMPLES = """
Here are a few examples of how you can interact with customers:

<example 1>
H: Hi, do you offer commercial insurance for small businesses?

A: Ah! Unfortunately, we don't offer commercial insurance at this time.
However, we do provide a range of personal insurance products including car insurance and electric car insurance.
Would you like to know more about these offerings?
</example 1>

<example 2>
H: Hi, what are your business hours?

A: Our business hours are Monday to Friday, 9 AM to 5 PM EST.
If you have any questions or need assistance, feel free to reach out during those times.
How else can I assist you today?
</example 2>

<example 3>
H: I'm shopping for car insurance. What does Acme offer?

A: Great choice! Acme's car insurance policies typically include:
- Liability coverage: Protects you if you're at fault in an accident
- Collision coverage: Pays for damage to your car in an accident
- Comprehensive coverage: Covers non-collision incidents like theft or vandalism
- Medical payments coverage: Pays for medical expenses after an accident
- Uninsured/underinsured motorist coverage: Protects you from drivers with insufficient insurance

We also offer optional coverages like rental car reimbursement, roadside assistance, and new car replacement.
Would you like more details on any of these coverages, or do you have specific questions about insuring your vehicle?
</example 3>

<example 4>
H: I'd like to hear about your electric car insurance.

A: Certainly! Our electric car insurance is specially designed to meet the unique needs of electric vehicle owners.
In addition to all the standard coverages we offer for regular cars, our electric car policies include:

- Battery coverage: Protection against damage or degradation of your vehicle's expensive battery system
- Tech package: Covers repairs or replacement of advanced electronics and onboard computer systems
- Charging station coverage: Protects both home and portable charging equipment
- Cybersecurity protection: Coverage against hacking or digital threats
- Specialized roadside assistance: Includes flatbed towing to protect the vehicle's undercarriage

We cover a wide range of electric vehicles, including popular models from Tesla, Rivian, Nissan, Chevrolet, and more.
Is there a specific electric vehicle you're looking to insure, or would you like more details on any of these coverages?
</example 4>

<example 5>
H: I'd like to get a quote for my car insurance.

A: Certainly! I'd be happy to help you get a quote for your car insurance.
To provide you with an accurate quote, I'll need to collect some information about your vehicle and the primary driver.
Let's start with the basics:

1. What is the make and model of your vehicle?
2. What year was it manufactured?
3. Approximately how many miles have you driven?
4. What is the age of the primary driver?

Once you provide this information, I'll use our quoting tool to generate a personalized insurance quote for you.
</example 5>
"""
```

Anda juga perlu menyertakan instruksi penting apa pun yang menguraikan hal-hal yang boleh dan tidak boleh dilakukan tentang bagaimana Claude harus berinteraksi dengan pelanggan. Ini mungkin diambil dari pagar pembatas merek atau kebijakan dukungan.

```python
ADDITIONAL_GUARDRAILS = """Please adhere to the following guardrails:
1. Only provide information about insurance types listed in our offerings.
2. If asked about an insurance type we don't offer, politely state
that we don't provide that service.
3. Do not speculate about future product offerings or company plans.
4. Don't make promises or enter into agreements it's not authorized to make.
You only provide information and guidance.
5. Do not mention any competitor's products or services.
"""
```

Sekarang gabungkan semua bagian ini menjadi satu string untuk digunakan sebagai prompt Anda.

```python
TASK_SPECIFIC_INSTRUCTIONS = " ".join(
    [
        STATIC_GREETINGS_AND_GENERAL,
        STATIC_CAR_INSURANCE,
        STATIC_ELECTRIC_CAR_INSURANCE,
        EXAMPLES,
        ADDITIONAL_GUARDRAILS,
    ]
)
```

### Tambahkan kemampuan dinamis dan agentik dengan penggunaan alat

Claude mampu mengambil tindakan dan mengambil informasi secara dinamis menggunakan fungsionalitas penggunaan alat sisi klien. Mulailah dengan membuat daftar alat eksternal atau API apa pun yang harus digunakan prompt.

Untuk contoh ini, mulailah dengan satu alat untuk menghitung penawaran.

<Tip>
  Sebagai pengingat, alat ini tidak akan melakukan perhitungan sebenarnya, alat ini hanya akan memberi sinyal kepada aplikasi bahwa suatu alat harus digunakan dengan argumen apa pun yang ditentukan.
</Tip>

Tambahkan nama model, definisi alat, dan implementasi stub ke `config.py`:

```python
import time

MODEL = "claude-opus-4-8"

TOOLS = [
    {
        "name": "get_quote",
        "description": "Calculate the insurance quote based on user input. Returned value is per month premium.",
        "input_schema": {
            "type": "object",
            "properties": {
                "make": {"type": "string", "description": "The make of the vehicle."},
                "model": {"type": "string", "description": "The model of the vehicle."},
                "year": {
                    "type": "integer",
                    "description": "The year the vehicle was manufactured.",
                },
                "mileage": {
                    "type": "integer",
                    "description": "The mileage on the vehicle.",
                },
                "driver_age": {
                    "type": "integer",
                    "description": "The age of the primary driver.",
                },
            },
            "required": ["make", "model", "year", "mileage", "driver_age"],
        },
    }
]


def get_quote(make, model, year, mileage, driver_age):
    """Returns the premium per month in USD"""
    # Anda dapat memanggil endpoint http atau database untuk mendapatkan penawaran harga.
    # Di sini, kita mensimulasikan penundaan 1 detik dan mengembalikan penawaran tetap sebesar 100.
    time.sleep(1)
    return 100
```

### Deploy prompt Anda

Sulit untuk mengetahui seberapa baik prompt Anda bekerja tanpa men-deploy-nya dalam pengaturan produksi uji dan [menjalankan evaluasi](/docs/id/test-and-evaluate/develop-tests). Bangun aplikasi kecil menggunakan prompt, Anthropic SDK, dan Streamlit untuk antarmuka pengguna.

Dalam file bernama `chatbot.py`, mulailah dengan menyiapkan kelas ChatBot, yang akan mengenkapsulasi interaksi dengan Anthropic SDK.

Kelas ini harus memiliki dua metode utama: `generate_message` dan `process_user_input`.

```python
from anthropic import Anthropic
from config import IDENTITY, TOOLS, MODEL, get_quote
from dotenv import load_dotenv

load_dotenv()


class ChatBot:
    def __init__(self, session_state):
        self.anthropic = Anthropic()
        self.session_state = session_state

    def generate_message(
        self,
        messages,
        max_tokens,
    ):
        try:
            response = self.anthropic.messages.create(
                model=MODEL,
                system=IDENTITY,
                max_tokens=max_tokens,
                messages=messages,
                tools=TOOLS,
            )
            return response
        except Exception as e:
            return {"error": str(e)}

    def process_user_input(self, user_input):
        self.session_state.messages.append({"role": "user", "content": user_input})

        response_message = self.generate_message(
            messages=self.session_state.messages,
            max_tokens=2048,
        )

        if "error" in response_message:
            return f"An error occurred: {response_message['error']}"

        if response_message.content[-1].type == "tool_use":
            tool_use = response_message.content[-1]
            func_name = tool_use.name
            func_params = tool_use.input
            tool_use_id = tool_use.id

            result = self.handle_tool_use(func_name, func_params)
            self.session_state.messages.append(
                {"role": "assistant", "content": response_message.content}
            )
            self.session_state.messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": f"{result}",
                        }
                    ],
                }
            )

            follow_up_response = self.generate_message(
                messages=self.session_state.messages,
                max_tokens=2048,
            )

            if "error" in follow_up_response:
                return f"An error occurred: {follow_up_response['error']}"

            response_text = follow_up_response.content[0].text
            self.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )
            return response_text

        elif response_message.content[0].type == "text":
            response_text = response_message.content[0].text
            self.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )
            return response_text

        else:
            raise Exception("An error occurred: Unexpected response type")

    def handle_tool_use(self, func_name, func_params):
        if func_name == "get_quote":
            premium = get_quote(**func_params)
            return f"Quote generated: ${premium:.2f} per month"

        raise Exception("An unexpected tool was used")
```

### Bangun antarmuka pengguna Anda

Uji deployment kode ini dengan Streamlit menggunakan metode main. Fungsi `main()` ini menyiapkan antarmuka obrolan berbasis Streamlit.

Lakukan ini dalam file bernama `app.py`

```python
import streamlit as st
from chatbot import ChatBot
from config import TASK_SPECIFIC_INSTRUCTIONS


def main():
    st.title("Chat with Eva, Acme Insurance Company's Assistant🤖")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "user", "content": TASK_SPECIFIC_INSTRUCTIONS},
            {"role": "assistant", "content": "Understood"},
        ]

    chatbot = ChatBot(st.session_state)

    # Tampilkan pesan pengguna dan asisten dengan melewati dua yang pertama
    for message in st.session_state.messages[2:]:
        # abaikan blok tool use
        if isinstance(message["content"], str):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if user_msg := st.chat_input("Type your message here..."):
        st.chat_message("user").markdown(user_msg)

        with st.chat_message("assistant"):
            with st.spinner("Eva is thinking..."):
                response_placeholder = st.empty()
                full_response = chatbot.process_user_input(user_msg)
                response_placeholder.markdown(full_response)


if __name__ == "__main__":
    main()
```

Jalankan program dengan:

```bash
streamlit run app.py
```

### Evaluasi prompt Anda

Prompting sering kali memerlukan pengujian dan optimasi agar siap untuk produksi. Untuk menentukan kesiapan solusi Anda, evaluasi kinerja chatbot menggunakan proses sistematis yang menggabungkan metode kuantitatif dan kualitatif. Membuat [evaluasi empiris yang kuat](/docs/id/test-and-evaluate/develop-tests#building-evals-and-test-cases) berdasarkan kriteria keberhasilan yang telah Anda definisikan akan memungkinkan Anda mengoptimalkan prompt Anda.

<Tip>
  [Claude Console](/dashboard)

   sekarang memiliki fitur alat Evaluation yang memungkinkan Anda menguji prompt Anda dalam berbagai skenario.
</Tip>

### Tingkatkan kinerja

Dalam skenario yang kompleks, mungkin berguna untuk mempertimbangkan strategi tambahan untuk meningkatkan kinerja di luar [teknik rekayasa prompt](/docs/id/build-with-claude/prompt-engineering/overview) standar & [strategi implementasi pagar pembatas](/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations). Berikut adalah beberapa skenario umum:

#### Kurangi latensi konteks panjang dengan RAG

Saat menangani sejumlah besar konteks statis dan dinamis, menyertakan semua informasi dalam prompt dapat menyebabkan biaya tinggi, waktu respons yang lebih lambat, dan mencapai batas jendela konteks. Dalam skenario ini, mengimplementasikan teknik "Retrieval Augmented Generation" (RAG) dapat meningkatkan kinerja dan efisiensi.

Dengan menggunakan [model embedding seperti Voyage](/docs/id/build-with-claude/embeddings) untuk mengonversi informasi menjadi representasi vektor, Anda dapat membuat sistem yang lebih dapat diskalakan dan responsif. Pendekatan ini memungkinkan pengambilan informasi relevan secara dinamis berdasarkan pertanyaan saat ini, daripada menyertakan semua konteks yang mungkin dalam setiap prompt.

Mengimplementasikan RAG untuk kasus penggunaan dukungan telah terbukti meningkatkan akurasi, mengurangi waktu respons, dan mengurangi biaya API dalam sistem dengan persyaratan konteks yang luas. Lihat [resep RAG](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide) untuk contoh yang telah dikerjakan.

#### Integrasikan data real-time dengan penggunaan alat

Saat menangani pertanyaan yang memerlukan informasi real-time, seperti saldo akun atau detail polis, pendekatan RAG berbasis embedding tidak cukup. Sebagai gantinya, penggunaan alat dapat meningkatkan kemampuan chatbot Anda untuk memberikan respons yang akurat dan real-time. Misalnya, Anda dapat menggunakan penggunaan alat untuk mencari informasi pelanggan, mengambil detail pesanan, dan membatalkan pesanan atas nama pelanggan.

Pendekatan ini, [diuraikan dalam resep penggunaan alat: agen layanan pelanggan](https://platform.claude.com/cookbook/tool-use-customer-service-agent), memungkinkan Anda mengintegrasikan data langsung ke dalam respons Claude dan memberikan pengalaman pelanggan yang lebih personal dan efisien.

#### Perkuat pagar pembatas input dan output

Saat men-deploy chatbot, terutama dalam skenario layanan pelanggan, penting untuk mencegah risiko yang terkait dengan penyalahgunaan, pertanyaan di luar cakupan, dan respons yang tidak pantas. Meskipun Claude secara inheren tangguh terhadap skenario semacam itu, berikut adalah langkah-langkah tambahan untuk memperkuat pagar pembatas chatbot Anda:

* [Kurangi halusinasi](/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations): Implementasikan mekanisme pemeriksaan fakta dan [sitasi](https://platform.claude.com/cookbook/misc-using-citations) untuk mendasarkan respons pada informasi yang disediakan.
* Periksa silang informasi: Verifikasi bahwa respons agen selaras dengan kebijakan perusahaan Anda dan fakta yang diketahui.
* Hindari komitmen kontraktual: Pastikan agen tidak membuat janji atau masuk ke dalam perjanjian yang tidak diizinkan untuk dibuatnya.
* [Mitigasi jailbreak](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks): Gunakan metode seperti penyaringan ketidakberbahayaan dan validasi input untuk mencegah pengguna mengeksploitasi kerentanan model, yang bertujuan menghasilkan konten yang tidak pantas.
* Hindari menyebutkan pesaing: Implementasikan filter penyebutan pesaing untuk mempertahankan fokus merek dan tidak menyebutkan produk atau layanan pesaing mana pun.
* [Tingkatkan konsistensi output](/docs/id/test-and-evaluate/strengthen-guardrails/increase-consistency): Cegah Claude mengubah gaya atau keluar dari karakter, bahkan selama interaksi yang panjang dan kompleks.
* Hapus Informasi Identitas Pribadi (PII): Kecuali secara eksplisit diperlukan dan diizinkan, hapus PII apa pun dari respons.

#### Kurangi waktu respons yang dirasakan dengan streaming

Saat menangani respons yang berpotensi panjang, mengimplementasikan streaming dapat meningkatkan keterlibatan dan kepuasan pengguna. Dalam skenario ini, pengguna menerima jawaban secara progresif alih-alih menunggu seluruh respons dihasilkan.

Berikut cara mengimplementasikan streaming:

1. Gunakan [Anthropic Streaming API](/docs/id/build-with-claude/streaming) untuk mendukung respons streaming.
2. Siapkan frontend Anda untuk menangani potongan teks yang masuk.
3. Tampilkan setiap potongan saat tiba, mensimulasikan pengetikan real-time.
4. Implementasikan mekanisme untuk menyimpan respons lengkap, memungkinkan pengguna melihatnya jika mereka menavigasi keluar dan kembali.

Dalam beberapa kasus, streaming memungkinkan penggunaan model yang lebih canggih dengan latensi dasar yang lebih tinggi, karena tampilan progresif mengurangi dampak waktu pemrosesan yang lebih lama.

#### Skalakan chatbot Anda

Seiring bertambahnya kompleksitas chatbot Anda, arsitektur aplikasi Anda dapat berkembang untuk menyesuaikan. Sebelum Anda menambahkan lapisan lebih lanjut ke arsitektur Anda, pertimbangkan opsi-opsi yang kurang menyeluruh berikut:

* Pastikan Anda memaksimalkan prompt Anda dan mengoptimalkan melalui rekayasa prompt. Gunakan [panduan rekayasa prompt](/docs/id/build-with-claude/prompt-engineering/overview) untuk menulis prompt yang paling efektif.
* Tambahkan [alat](/docs/id/agents-and-tools/tool-use/overview) tambahan ke prompt (yang dapat mencakup [rantai prompt](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#chain-complex-prompts)) dan lihat apakah Anda dapat mencapai fungsionalitas yang diperlukan.

Jika chatbot Anda menangani tugas yang sangat bervariasi, Anda mungkin ingin mempertimbangkan untuk menambahkan [pengklasifikasi maksud terpisah](https://platform.claude.com/cookbook/capabilities-classification-guide) untuk merutekan pertanyaan pelanggan awal. Untuk aplikasi yang ada, ini akan melibatkan pembuatan pohon keputusan yang akan merutekan pertanyaan pelanggan melalui pengklasifikasi dan kemudian ke percakapan khusus (dengan set alat dan prompt sistem mereka sendiri). Perhatikan, metode ini memerlukan panggilan tambahan ke Claude yang dapat meningkatkan latensi.

### Integrasikan Claude ke dalam alur kerja dukungan Anda

Meskipun contoh-contoh ini berfokus pada fungsi Python yang dapat dipanggil dalam lingkungan Streamlit, men-deploy Claude untuk chatbot dukungan real-time memerlukan layanan API.

Berikut cara Anda dapat melakukan pendekatan ini:

1. Buat pembungkus API: Kembangkan pembungkus API sederhana di sekitar fungsi klasifikasi Anda. Misalnya, Anda dapat menggunakan Flask API atau Fast API untuk membungkus kode Anda menjadi Layanan HTTP. Layanan HTTP Anda dapat menerima input pengguna dan mengembalikan respons Assistant secara keseluruhan. Dengan demikian, layanan Anda dapat memiliki karakteristik berikut:

   * Server-Sent Events (SSE): SSE memungkinkan streaming respons secara real-time dari server ke klien. Ini memberikan pengalaman yang mulus dan interaktif saat bekerja dengan LLM.
   * Caching: Mengimplementasikan caching dapat meningkatkan waktu respons dan mengurangi panggilan API yang tidak perlu.
   * Retensi konteks: Mempertahankan konteks saat pengguna menavigasi keluar dan kembali penting untuk kontinuitas dalam percakapan.

2. Bangun antarmuka web: Implementasikan UI web yang ramah pengguna untuk berinteraksi dengan agen yang didukung Claude.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Penggunaan alat" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Berikan Claude akses ke API Anda sehingga dapat mengambil tindakan atas nama pelanggan.
  </Card>

  <Card title="Kembangkan pengujian" icon="check" href="/docs/id/test-and-evaluate/develop-tests">
    Bangun evaluasi untuk mengukur agen dukungan Anda terhadap kriteria keberhasilan yang telah Anda definisikan.
  </Card>

  <Card title="Streaming" icon="bolt" href="/docs/id/build-with-claude/streaming">
    Stream respons sehingga pelanggan melihat jawaban saat dihasilkan.
  </Card>

  <Card title="Rekayasa prompt" icon="lightbulb" href="/docs/id/build-with-claude/prompt-engineering/overview">
    Sempurnakan prompt sistem dan contoh Anda untuk kinerja tugas yang lebih baik.
  </Card>
</CardGroup>
