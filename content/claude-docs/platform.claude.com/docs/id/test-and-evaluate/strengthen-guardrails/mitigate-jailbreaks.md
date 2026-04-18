---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 1d097c6ff47dc1930db4d3919d5998d667dd8d7e46ab2573f313fff3eac08ada
---

# Mitigasi jailbreak dan injeksi prompt

Pelajari strategi untuk melindungi aplikasi Claude dari jailbreak dan injeksi prompt melalui validasi input, rekayasa prompt, dan pemantauan berkelanjutan.

---

Jailbreaking dan injeksi prompt terjadi ketika pengguna membuat prompt untuk mengeksploitasi kerentanan model, dengan tujuan menghasilkan konten yang tidak pantas. Meskipun Claude secara inheren tahan terhadap serangan semacam itu, berikut adalah langkah-langkah tambahan untuk memperkuat penjaga Anda, khususnya terhadap penggunaan yang melanggar [Syarat Layanan](https://www.anthropic.com/legal/commercial-terms) atau [Kebijakan Penggunaan](https://www.anthropic.com/legal/aup) kami.

- **Layar keamanan**: Gunakan model ringan seperti Claude Haiku 4.5 untuk pra-pemeriksaan input pengguna. Gunakan [keluaran terstruktur](/docs/id/build-with-claude/structured-outputs) untuk membatasi respons menjadi klasifikasi sederhana.

    <section title="Contoh: Layar keamanan untuk moderasi konten">

        | Peran | Konten |
        | ---- | ------- |
        | Pengguna | Seorang pengguna mengirimkan konten ini:<br/>\<content><br/>\{\{CONTENT}\}<br/>\</content><br/><br/>Klasifikasikan apakah konten ini mengacu pada aktivitas berbahaya, ilegal, atau eksplisit. |

        Gunakan `output_config` dengan skema JSON untuk membatasi respons:

        ```json
        {
          "output_config": {
            "format": {
              "type": "json_schema",
              "schema": {
                "type": "object",
                "properties": {
                  "is_harmful": { "type": "boolean" }
                },
                "required": ["is_harmful"],
                "additionalProperties": false
              }
            }
          }
        }
        ```
    
</section>

- **Validasi input**: Filter prompt untuk pola jailbreaking. Anda bahkan dapat menggunakan LLM untuk membuat layar validasi yang digeneralisasi dengan memberikan bahasa jailbreaking yang diketahui sebagai contoh.

- **Rekayasa prompt**: Buat prompt yang menekankan batas-batas etika dan hukum.

    <section title="Contoh: Prompt sistem etika untuk chatbot perusahaan">

        | Peran | Konten |
        | ---- | ------- |
        | Sistem | Anda adalah asisten AI etika AcmeCorp. Respons Anda harus selaras dengan nilai-nilai kami:<br/>\<values><br/>- Integritas: Jangan pernah menipu atau membantu dalam penipuan.<br/>- Kepatuhan: Tolak permintaan apa pun yang melanggar hukum atau kebijakan kami.<br/>- Privasi: Lindungi semua data pribadi dan perusahaan.<br/>Penghormatan terhadap kekayaan intelektual: Output Anda tidak boleh melanggar hak kekayaan intelektual orang lain.<br/>\</values><br/><br/>Jika permintaan bertentangan dengan nilai-nilai ini, respons: "Saya tidak dapat melakukan tindakan itu karena bertentangan dengan nilai-nilai AcmeCorp." |
    
</section>

Sesuaikan respons dan pertimbangkan pembatasan kecepatan atau pelarangan pengguna yang berulang kali terlibat dalam perilaku kasar yang mencoba melewati penjaga Claude. Misalnya, jika pengguna tertentu memicu jenis penolakan yang sama berkali-kali (misalnya, "output diblokir oleh kebijakan penyaringan konten"), beri tahu pengguna bahwa tindakan mereka melanggar kebijakan penggunaan yang relevan dan ambil tindakan yang sesuai.

- **Pemantauan berkelanjutan**: Secara teratur analisis output untuk tanda-tanda jailbreaking.
Gunakan pemantauan ini untuk secara iteratif menyempurnakan prompt dan strategi validasi Anda.

## Lanjutan: Rantai penjaga
Gabungkan strategi untuk perlindungan yang kuat. Berikut adalah contoh tingkat perusahaan dengan penggunaan alat:

<section title="Contoh: Perlindungan berlapis untuk chatbot penasihat keuangan">

  ### Prompt sistem bot
  | Peran | Konten |
  | ---- | ------- |
  | Sistem | Anda adalah AcmeFinBot, penasihat keuangan untuk AcmeTrade Inc. Direktif utama Anda adalah melindungi kepentingan klien dan mempertahankan kepatuhan regulasi.<br/><br/>\<directives><br/>1. Validasi semua permintaan terhadap pedoman SEC dan FINRA.<br/>2. Tolak tindakan apa pun yang dapat dianggap sebagai perdagangan orang dalam atau manipulasi pasar.<br/>3. Lindungi privasi klien; jangan pernah mengungkapkan data pribadi atau keuangan.<br/>\</directives><br/><br/>Instruksi langkah demi langkah:<br/>\<instructions><br/>1. Layar kueri pengguna untuk kepatuhan (gunakan alat 'harmlessness_screen').<br/>2. Jika sesuai, proses kueri.<br/>3. Jika tidak sesuai, respons: "Saya tidak dapat memproses permintaan ini karena melanggar peraturan keuangan atau privasi klien."<br/>\</instructions> |

  ### Prompt dalam alat `harmlessness_screen`
  | Peran | Konten |
  | -------- | ------- |
  | Pengguna | \<user_query><br/>\{\{USER_QUERY}}<br/>\</user_query><br/><br/>Evaluasi apakah kueri ini melanggar aturan SEC, pedoman FINRA, atau privasi klien. |

  Gunakan [keluaran terstruktur](/docs/id/build-with-claude/structured-outputs) untuk membatasi respons menjadi klasifikasi boolean.

</section>

Dengan melapisi strategi-strategi ini, Anda menciptakan pertahanan yang kuat terhadap jailbreaking dan injeksi prompt, memastikan aplikasi bertenaga Claude Anda mempertahankan standar keamanan dan kepatuhan tertinggi.