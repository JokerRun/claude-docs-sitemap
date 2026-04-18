---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/increase-consistency
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: aa30314a0c6feb57984cb0f3c9ce5a322555293989ec6d4bc2ecd082ef538133
---

# Tingkatkan konsistensi output

Pelajari teknik untuk membuat respons Claude lebih konsisten, termasuk menentukan format output, prefill respons, memberikan contoh, dan mempertahankan karakter peran.

---

<Tip>
**Untuk kepatuhan skema JSON yang dijamin**

Jika Anda memerlukan Claude untuk selalu mengeluarkan JSON yang valid sesuai dengan skema tertentu, gunakan [Structured Outputs](/docs/id/build-with-claude/structured-outputs) sebagai gantinya dari teknik rekayasa prompt di bawah ini. Structured outputs memberikan kepatuhan skema yang dijamin dan dirancang khusus untuk kasus penggunaan ini.

Teknik di bawah ini berguna untuk konsistensi output umum atau ketika Anda memerlukan fleksibilitas di luar skema JSON yang ketat.
</Tip>

Berikut adalah cara membuat respons Claude lebih konsisten:

## Tentukan format output yang diinginkan
Tentukan dengan tepat format output yang Anda inginkan menggunakan JSON, XML, atau template khusus sehingga Claude memahami setiap elemen pemformatan output yang Anda perlukan.

<section title="Contoh: Standardisasi umpan balik pelanggan">

    | Peran | Konten |
    | ---- | ------- |
    | Pengguna | Anda adalah Customer Insights AI. Analisis umpan balik ini dan keluarkan dalam format JSON dengan kunci: "sentiment" (positif/negatif/netral), "key_issues" (daftar), dan "action_items" (daftar dict dengan "team" dan "task").<br/><br/>"Saya telah menjadi pengguna setia selama 3 tahun, tetapi pembaruan UI terbaru adalah bencana. Menemukan fitur dasar sekarang seperti berburu harta karun. Ditambah lagi, "premium" pricing baru sangat mahal. Saya sedang mempertimbangkan untuk beralih kecuali ini diperbaiki ASAP." |
    | Asisten | \{<br/>  "sentiment": "negative",<br/>  "key_issues": [<br/>    "Poor UI/UX in recent update",<br/>    "Difficulty finding basic features",<br/>    "Perceived high pricing (new 'premium' tier)"<br/>  ],<br/>  "action_items": [<br/>    \{<br/>      "team": "Product",<br/>      "task": "Conduct usability testing and iterate on UI based on findings"<br/>    \},<br/>    \{<br/>      "team": "UX",<br/>      "task": "Create a feature discovery guide or onboarding flow"<br/>    \},<br/>    \{<br/>      "team": "Marketing",<br/>      "task": "Review pricing strategy and communicate value proposition"<br/>    },<br/>    \{<br/>      "team": "Customer Success",<br/>      "task": "Reach out to user, offer concessions to prevent churn"<br/>    \}<br/>  ]<br/>\} |

</section>

## Prefill respons Claude

<Note>Prefilling tidak didukung pada [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs) atau instruksi system prompt sebagai gantinya.</Note>

Prefill giliran `Assistant` dengan format yang Anda inginkan. Trik ini melewati pembukaan ramah Claude dan memberlakukan struktur Anda.

<section title="Contoh: Laporan penjualan harian">

    | Peran | Konten |
    | ---- | ------- |
    | Pengguna | Anda adalah Sales Intelligence AI yang berwawasan. Hasilkan laporan penjualan hari ini.<br/><br/>Struktur laporan seperti ini:<br/><br/>\<report><br/>    \<summary><br/>        \<metric name="total_revenue">\$0.00\</metric><br/>        \<metric name="units_sold">0\</metric><br/>        \<metric name="avg_order_value">\$0.00\</metric><br/>    \</summary><br/>    \<top_products><br/>        \<br/>            \<name>Product Name\</name><br/>            \<revenue>\$0.00\</revenue><br/>            \<units>0\</units><br/>        \</product><br/>        ...<br/>    \</top_products><br/>    \<regional_performance><br/>        \<region><br/>            \<name>Region Name\</name><br/>            \<revenue>\$0.00\</revenue><br/>            \<growth>0.0%\</growth><br/>        \</region><br/>        ...<br/>    \</regional_performance><br/>    \<action_items><br/>        \<item>Action item.\</item><br/>        ...<br/>    \</action_items><br/>\</report> |
    | Asisten (prefill) | \<report><br/>    \<summary><br/>        \<metric name= |
    | Asisten | "total_revenue">\$842,567.00\</metric><br/>        \<metric name="units_sold">15,238\</metric><br/>        \<metric name="avg_order_value">\$55.29\</metric><br/>    \</summary><br/>    \<top_products><br/>        \<br/>            \<name>AcmeGuard Pro\</name><br/>            \<revenue>\$325,890.00\</revenue><br/>            \<units>3,621\</units><br/>        \</product><br/>        \<br/>            \<name>AcmeVault Enterprise\</name><br/>            \<revenue>\$254,400.00\</revenue><br/>            \<units>1,272\</units><br/>        \</product><br/>        \<br/>            \<name>AcmeBoost XL\</name><br/>            \<revenue>\$147,690.00\</revenue><br/>            \<units>4,923\</units><br/>        \</product><br/>    \</top_products><br/>    \<regional_performance><br/>        \<region><br/>            \<name>APAC\</name><br/>            \<revenue>\$258,960.00\</revenue><br/>            \<growth>12.8%\</growth><br/>        \</region><br/>        \<region><br/>            \<name>EMEA\</name><br/>            \<revenue>\$325,478.00\</revenue><br/>            \<growth>3.2%\</growth><br/>        \</region><br/>        \<region><br/>            \<name>Americas\</name><br/>            \<revenue>\$258,129.00\</revenue><br/>            \<growth>-2.1%\</growth><br/>        \</region><br/>    \</regional_performance><br/>    \<action_items><br/>        \<item>Investigate Americas revenue drop; schedule regional sales team meeting.\</item><br/>        \<item>Accelerate CloudGuard Pro rollout in APAC to capitalize on growth.\</item><br/>        \<item>Review NetBoost XL pricing; high volume but lower revenue.\</item><br/>    \</action_items><br/>\</report> |

</section>

## Batasi dengan contoh
Berikan contoh output yang Anda inginkan. Ini melatih pemahaman Claude lebih baik daripada instruksi abstrak.

<section title="Contoh: Menghasilkan intelijen pasar yang konsisten">

    | Peran | Konten |
    | ---- | ------- |
    | Pengguna | Sebagai Market Intelligence AI, tugas Anda adalah menganalisis data tentang pesaing kami. Berikut adalah data pesaing kami:<br/>\<data><br/>\{\{DATA}}<br/>\</data><br/><br/>Keluarkan mengikuti format contoh ini:<br/><br/>\<competitor><br/>  \<name>Rival Inc\</name><br/>  \<overview>Ringkasan 50 kata.\</overview><br/>  \<swot><br/>    \<strengths>- Poin-poin bullet\</strengths><br/>    \<weaknesses>- Poin-poin bullet\</weaknesses><br/>    \<opportunities>- Poin-poin bullet\</opportunities><br/>    \<threats>- Poin-poin bullet\</threats><br/>  \</swot><br/>  \<strategy>Respons strategis 30 kata.\</strategy><br/>\</competitor><br/><br/>Sekarang, analisis AcmeGiant dan AcmeDataCo menggunakan format ini. |
    | Asisten | \<competitor><br/>  \<name>AcmeGiant\</name><br/>  \<overview>Pemimpin teknologi global dengan ekosistem produk konsumen dan enterprise yang luas. Dikenal karena inovasi, merek yang kuat, dan penguncian pelanggan yang mendalam melalui hardware, software, dan layanan terintegrasi.\</overview><br/>  \<swot><br/>    \<strengths><br/>      - Anggaran R&D besar mendorong inovasi berkelanjutan<br/>      - Basis pelanggan setia dan pengakuan merek yang kuat<br/>      - Ekosistem produk sinergis meningkatkan biaya switching<br/>    \</strengths><br/>    \<weaknesses><br/>      - Harga tinggi dapat mengalihkan pelanggan yang sensitif terhadap biaya<br/>      - Lambat mengatasi kebutuhan kustomisasi khusus enterprise<br/>      - Kekhawatiran privasi dan pengawasan regulasi di berbagai pasar<br/>    \</weaknesses><br/>    \<opportunities><br/>      - Permintaan yang berkembang untuk kemampuan AI dan ML<br/>      - Ekspansi ke pasar yang sedang berkembang<br/>      - Akuisisi untuk mengisi celah produk atau bakat<br/>    \</opportunities><br/>    \<threats><br/>      - Kebangkitan cepat pesaing cloud-native<br/>      - Gugatan antitrust dan tindakan regulasi<br/>      - Perebutan bakat oleh startup dan pesaing<br/>    \</threats><br/>  \</swot><br/>  \<strategy>Fokus pada kelincahan dan kustomisasi kami. Targetkan respons enterprise yang lambat dari TechGiant dan masalah privasi dalam pemasaran kami.\</strategy><br/>\</competitor><br/><br/>\<competitor><br/>  \<name>AcmeDataCo\</name><br/>  \<overview>Bintang yang sedang naik dalam analitik data dan visualisasi. Menawarkan alat BI self-service yang intuitif dengan model freemium, menarik bagi startup dan tim enterprise.\</overview><br/>  \<swot><br/>    \<strengths><br/>      - Antarmuka yang ramah pengguna mengurangi kebutuhan pelatihan khusus<br/>      - Model freemium menurunkan hambatan masuk, mendorong pertumbuhan viral<br/>      - Kecocokan produk-pasar yang kuat dengan kebangkitan keputusan berbasis data<br/>    \</strengths><br/>    \<weaknesses><br/>      - Analitik lanjutan terbatas dibandingkan dengan alat BI yang sudah mapan<br/>      - Masalah penskalaan dilaporkan dengan dataset yang sangat besar<br/>      - Bergantung pada infrastruktur cloud pihak ketiga (AWS)<br/>    \</weaknesses><br/>    \<opportunities><br/>      - Ekspansi ke analitik prediktif dan wawasan berbasis AI<br/>      - Membentuk aliansi strategis dengan vendor teknologi komplementer<br/>      - Dashboard yang dapat disesuaikan untuk solusi khusus industri<br/>    \</opportunities><br/>    \<threats><br/>      - Saturasi pasar; banyak pendatang baru di BI self-service<br/>      - Raksasa BI enterprise mengembangkan alat yang lebih ramah pengguna<br/>      - Regulasi privasi data meningkatkan kompleksitas kepatuhan<br/>    \</threats><br/>  \</swot><br/>  \<strategy>Sorot fitur enterprise yang kuat dan tata kelola data kami. Targetkan akun yang berjuang dengan keterbatasan skala DataCo.\</strategy><br/>\</competitor> |

</section>

## Gunakan retrieval untuk konsistensi kontekstual
Untuk tugas yang memerlukan konteks konsisten (misalnya, chatbot, basis pengetahuan), gunakan retrieval untuk mendasarkan respons Claude pada set informasi tetap.

<section title="Contoh: Meningkatkan konsistensi dukungan IT">

    | Peran | Konten |
    | ---- | ------- |
    | Pengguna | Anda adalah IT Support AI kami yang mengandalkan data basis pengetahuan. Berikut adalah entri dari basis pengetahuan Anda:<br/><br/>\<kb><br/>  \<entry><br/>    \<id>1\</id><br/>    \<title>Reset Active Directory password\</title><br/>    \<content>1. Buka password.ourcompany.com<br/>2. Masukkan nama pengguna Anda<br/>3. Klik "Forgot Password"<br/>4. Ikuti instruksi email\</content><br/>  \</entry><br/>  \<entry><br/>    \<id>2\</id><br/>    \<title>Connect to VPN\</title><br/>    \<content>1. Instal GlobalProtect dari software center<br/>2. Buka GlobalProtect, masukkan "vpn.ourcompany.com"<br/>3. Gunakan kredensial AD untuk login\</content><br/>  \</entry><br/>\</kb><br/><br/>Saat membantu pengguna, selalu periksa basis pengetahuan terlebih dahulu. Respons dalam format ini:<br/><br/>\<response><br/>  \<kb_entry>Entri basis pengetahuan yang digunakan\</kb_entry><br/>  \<answer>Respons Anda\</answer><br/>\</response> Tulis beberapa pertanyaan uji untuk diri sendiri dan jawab menggunakan basis pengetahuan, hanya untuk memastikan Anda memahami cara menggunakan basis pengetahuan dengan benar. |
    | Asisten | Dipahami. Saya akan menggunakan basis pengetahuan untuk respons yang konsisten. Mari kita uji dengan beberapa skenario.<br/><br/>Pengguna: Hei, saya tidak bisa login ke email saya. Saya pikir saya lupa password saya.<br/><br/>\<response><br/>  \<kb_entry>1: Reset Active Directory password\</entry><br/>  \<answer>Saya memahami Anda mengalami kesulitan login ke email Anda karena lupa password. Tidak masalah, ini adalah masalah umum. Untuk mereset password Active Directory Anda, yang digunakan untuk akses email, ikuti langkah-langkah berikut:<br/><br/>1. Buka password.ourcompany.com<br/>2. Masukkan nama pengguna Anda (sama dengan alamat email Anda)<br/>3. Klik tautan "Forgot Password"<br/>4. Anda akan menerima email dengan instruksi. Ikuti untuk mereset password Anda.<br/><br/>Setelah mereset, Anda harus dapat login ke email Anda. Beri tahu saya jika Anda memerlukan bantuan lebih lanjut.\</answer><br/>\</response><br/><br/>Pengguna: Saya bekerja dari rumah hari ini. Bagaimana cara saya mengakses sumber daya internal?<br/><br/>\<response><br/>  \<kb_entry>2: Connect to VPN\</entry><br/>  \<answer>Pertanyaan bagus! Untuk mengakses sumber daya internal saat bekerja dari rumah, Anda perlu terhubung ke VPN perusahaan kami (Virtual Private Network). Berikut adalah cara mengaturnya:<br/><br/>1. Pertama, instal klien VPN GlobalProtect. Anda dapat menemukan ini di software center kami.<br/>2. Setelah diinstal, buka aplikasi GlobalProtect.<br/>3. Di bidang server, masukkan "vpn.ourcompany.com".<br/>4. Gunakan kredensial Active Directory (AD) Anda untuk login - nama pengguna dan password yang sama yang Anda gunakan untuk email Anda.<br/><br/>Setelah terhubung, Anda akan memiliki akses aman ke semua sumber daya internal seolah-olah Anda berada di kantor. Beri tahu saya jika Anda mengalami masalah apa pun selama setup.\</answer><br/>\</response> |

</section>

## Rantai prompt untuk tugas kompleks
Pecah tugas kompleks menjadi subtask yang lebih kecil dan konsisten. Setiap subtask mendapatkan perhatian penuh Claude, mengurangi kesalahan inkonsistensi di seluruh alur kerja yang diskalakan.

## Pertahankan Claude tetap dalam karakter

Untuk aplikasi berbasis peran, mempertahankan karakter yang konsisten memerlukan prompting yang disengaja.

- **Gunakan system prompts untuk menetapkan peran:** Gunakan [system prompts](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role) untuk menentukan peran dan kepribadian Claude. Ini menetapkan fondasi yang kuat untuk respons yang konsisten.
    <Tip>Saat menyiapkan karakter, berikan informasi terperinci tentang kepribadian, latar belakang, dan sifat atau keunikan khusus apa pun. Ini akan membantu model lebih baik meniru dan menggeneralisasi sifat-sifat karakter.</Tip>
- **Siapkan Claude untuk skenario yang mungkin:** Berikan daftar skenario umum dan respons yang diharapkan dalam prompt Anda. Ini "melatih" Claude untuk menangani situasi yang beragam tanpa keluar dari karakter.

<section title="Contoh: Chatbot enterprise untuk prompting peran">

    | Peran | Konten |
    | ---- | ------- |
    | Sistem | Anda adalah AcmeBot, asisten AI tingkat enterprise untuk AcmeTechCo. Peran Anda:<br/>    - Analisis dokumen teknis (TDDs, PRDs, RFCs)<br/>    - Berikan wawasan yang dapat ditindaklanjuti untuk tim engineering, product, dan ops<br/>    - Pertahankan nada profesional dan ringkas |
    | Pengguna | Berikut adalah kueri pengguna untuk Anda respons:<br/>\<user_query><br/>\{\{USER_QUERY}}<br/>\</user_query><br/><br/>Aturan interaksi Anda adalah:<br/>    - Selalu referensikan standar AcmeTechCo atau praktik terbaik industri<br/>    - Jika tidak yakin, minta klarifikasi sebelum melanjutkan<br/>    - Jangan pernah ungkapkan informasi rahasia AcmeTechCo.<br/><br/>Sebagai AcmeBot, Anda harus menangani situasi sesuai dengan panduan ini:<br/>    - Jika ditanya tentang IP AcmeTechCo: "Saya tidak dapat mengungkapkan informasi proprietary TechCo."<br/>    - Jika dipertanyakan tentang praktik terbaik: "Per ISO/IEC 25010, kami memprioritaskan..."<br/>    - Jika tidak jelas pada dokumen: "Untuk memastikan akurasi, silakan klarifikasi bagian 3.2..." |

</section>