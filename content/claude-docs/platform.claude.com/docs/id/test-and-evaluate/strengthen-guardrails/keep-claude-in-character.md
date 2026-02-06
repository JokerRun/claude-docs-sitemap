---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/keep-claude-in-character
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 30f29102f8e86fa60cc56ded5af636ea38d5c89480de13df141a17b8161fdd16
---

# Pertahankan Claude tetap sesuai karakter dengan role prompting dan prefilling

Panduan praktis untuk menjaga Claude tetap sesuai karakter, bahkan selama interaksi yang panjang dan kompleks.

---

Panduan ini menyediakan tips yang dapat ditindaklanjuti untuk menjaga Claude tetap sesuai karakter, bahkan selama interaksi yang panjang dan kompleks.

<Note>Prefilling sudah usang dan tidak didukung pada Claude Opus 4.6 dan Claude Sonnet 4.5. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs) atau instruksi system prompt sebagai gantinya.</Note>

- **Gunakan system prompts untuk menetapkan peran:** Gunakan [system prompts](/docs/id/build-with-claude/prompt-engineering/system-prompts) untuk mendefinisikan peran dan kepribadian Claude. Ini menetapkan fondasi yang kuat untuk respons yang konsisten.
    <Tip>Saat menyiapkan karakter, berikan informasi terperinci tentang kepribadian, latar belakang, dan sifat atau keunikan khusus apa pun. Ini akan membantu model lebih baik meniru dan menggeneralisasi sifat-sifat karakter.</Tip>
- **Perkuat dengan respons yang sudah diisi sebelumnya:** Isi respons Claude sebelumnya dengan tag karakter untuk memperkuat perannya, terutama dalam percakapan yang panjang.
- **Siapkan Claude untuk kemungkinan skenario:** Berikan daftar skenario umum dan respons yang diharapkan dalam prompt Anda. Ini "melatih" Claude untuk menangani situasi yang beragam tanpa keluar dari karakter.

<section title="Contoh: Chatbot perusahaan untuk role prompting">

    | Peran | Konten |
    | ---- | ------- |
    | System | Anda adalah AcmeBot, asisten AI tingkat perusahaan untuk AcmeTechCo. Peran Anda:<br/>    - Analisis dokumen teknis (TDD, PRD, RFC)<br/>    - Berikan wawasan yang dapat ditindaklanjuti untuk tim teknik, produk, dan operasi<br/>    - Pertahankan nada profesional dan ringkas |
    | User | Berikut adalah pertanyaan pengguna untuk Anda jawab:<br/>\<user_query><br/>\{\{USER_QUERY}}<br/>\</user_query><br/><br/>Aturan interaksi Anda adalah:<br/>    - Selalu referensikan standar AcmeTechCo atau praktik terbaik industri<br/>    - Jika tidak yakin, minta klarifikasi sebelum melanjutkan<br/>    - Jangan pernah mengungkapkan informasi rahasia AcmeTechCo.<br/><br/>Sebagai AcmeBot, Anda harus menangani situasi sesuai dengan panduan berikut:<br/>    - Jika ditanya tentang IP AcmeTechCo: "Saya tidak dapat mengungkapkan informasi proprietary TechCo."<br/>    - Jika ditanyakan tentang praktik terbaik: "Per ISO/IEC 25010, kami memprioritaskan..."<br/>    - Jika tidak jelas tentang dokumen: "Untuk memastikan akurasi, silakan klarifikasi bagian 3.2..." |
    | Assistant (prefill) | [AcmeBot] |

</section>