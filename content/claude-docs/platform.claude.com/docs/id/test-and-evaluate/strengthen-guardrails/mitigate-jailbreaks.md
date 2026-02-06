---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 16929ac36ab4db22dc5444d52de9c895fb13b129827983660ef61b8d0ccd5cc2
---

# Mitigasi jailbreak dan injeksi prompt

Pelajari cara memperkuat perlindungan terhadap jailbreak dan injeksi prompt dengan strategi validasi input, rekayasa prompt, dan pemantauan berkelanjutan.

---

Jailbreaking dan injeksi prompt terjadi ketika pengguna membuat prompt untuk mengeksploitasi kerentanan model, dengan tujuan menghasilkan konten yang tidak pantas. Meskipun Claude secara inheren tahan terhadap serangan semacam itu, berikut adalah langkah-langkah tambahan untuk memperkuat perlindungan Anda, khususnya terhadap penggunaan yang melanggar [Syarat Layanan](https://www.anthropic.com/legal/commercial-terms) atau [Kebijakan Penggunaan](https://www.anthropic.com/legal/aup) kami.

<Tip>Claude jauh lebih tahan terhadap jailbreaking dibandingkan LLM utama lainnya, berkat metode pelatihan canggih seperti Constitutional AI.</Tip>

- **Layar keamanan**: Gunakan model ringan seperti Claude Haiku 3 untuk pra-pemeriksaan input pengguna. (Catatan: prefilling sudah usang dan tidak didukung di Claude Opus 4.6 dan Sonnet 4.5.)

    <section title="Contoh: Layar keamanan untuk moderasi konten">

        | Peran | Konten |
        | ---- | ------- |
        | Pengguna | Seorang pengguna mengirimkan konten ini:<br/>\<content><br/>\{\{CONTENT}\}<br/>\</content><br/><br/>Balas dengan (Y) jika mengacu pada aktivitas berbahaya, ilegal, atau eksplisit. Balas dengan (N) jika aman. |
        | Asisten (prefill) | \( |
        | Asisten | N) |
    
</section>

- **Validasi input**: Filter prompt untuk pola jailbreaking. Anda bahkan dapat menggunakan LLM untuk membuat layar validasi yang digeneralisasi dengan memberikan bahasa jailbreaking yang diketahui sebagai contoh.

- **Rekayasa prompt**: Buat prompt yang menekankan batas-batas etika dan hukum.

    <section title="Contoh: Prompt sistem etis untuk chatbot perusahaan">

        | Peran | Konten |
        | ---- | ------- |
        | Sistem | Anda adalah asisten AI etis AcmeCorp. Respons Anda harus selaras dengan nilai-nilai kami:<br/>\<values><br/>- Integritas: Jangan pernah menipu atau membantu penipuan.<br/>- Kepatuhan: Tolak permintaan apa pun yang melanggar hukum atau kebijakan kami.<br/>- Privasi: Lindungi semua data pribadi dan perusahaan.<br/>Penghormatan terhadap kekayaan intelektual: Output Anda tidak boleh melanggar hak kekayaan intelektual orang lain.<br/>\</values><br/><br/>Jika permintaan bertentangan dengan nilai-nilai ini, balas: "Saya tidak dapat melakukan tindakan itu karena bertentangan dengan nilai-nilai AcmeCorp." |
    
</section>

Sesuaikan respons dan pertimbangkan pembatasan laju atau pelarangan pengguna yang berulang kali terlibat dalam perilaku kasar yang mencoba melewati perlindungan Claude. Misalnya, jika pengguna tertentu memicu jenis penolakan yang sama berkali-kali (misalnya, "output diblokir oleh kebijakan penyaringan konten"), beri tahu pengguna bahwa tindakan mereka melanggar kebijakan penggunaan yang relevan dan ambil tindakan yang sesuai.

- **Pemantauan berkelanjutan**: Secara teratur analisis output untuk tanda-tanda jailbreaking.
Gunakan pemantauan ini untuk secara iteratif menyempurnakan prompt dan strategi validasi Anda.

## Lanjutan: Rantai perlindungan
Gabungkan strategi untuk perlindungan yang kuat. Berikut adalah contoh tingkat perusahaan dengan penggunaan alat:

<section title="Contoh: Perlindungan berlapis untuk chatbot penasihat keuangan">

  ### Prompt sistem bot
  | Peran | Konten |
  | ---- | ------- |
  | Sistem | Anda adalah AcmeFinBot, penasihat keuangan untuk AcmeTrade Inc. Direktif utama Anda adalah melindungi kepentingan klien dan mempertahankan kepatuhan peraturan.<br/><br/>\<directives><br/>1. Validasi semua permintaan terhadap pedoman SEC dan FINRA.<br/>2. Tolak tindakan apa pun yang dapat dianggap sebagai perdagangan orang dalam atau manipulasi pasar.<br/>3. Lindungi privasi klien; jangan pernah mengungkapkan data pribadi atau keuangan.<br/>\</directives><br/><br/>Instruksi langkah demi langkah:<br/>\<instructions><br/>1. Layar kueri pengguna untuk kepatuhan (gunakan alat 'harmlessness_screen').<br/>2. Jika sesuai, proses kueri.<br/>3. Jika tidak sesuai, balas: "Saya tidak dapat memproses permintaan ini karena melanggar peraturan keuangan atau privasi klien."<br/>\</instructions> |
  
  ### Prompt dalam alat `harmlessness_screen`
  | Peran | Konten |
  | -------- | ------- |
  | Pengguna | \<user_query><br/>\{\{USER_QUERY}}<br/>\</user_query><br/><br/>Evaluasi apakah kueri ini melanggar aturan SEC, pedoman FINRA, atau privasi klien. Balas (Y) jika melanggar, (N) jika tidak. |
  | Asisten (prefill) | \( |

</section>

Dengan melapisi strategi-strategi ini, Anda membuat pertahanan yang kuat terhadap jailbreaking dan injeksi prompt, memastikan aplikasi berbasis Claude Anda mempertahankan standar keamanan dan kepatuhan tertinggi.