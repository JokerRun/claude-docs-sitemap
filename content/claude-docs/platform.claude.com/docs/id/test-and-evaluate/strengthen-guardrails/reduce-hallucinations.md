---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: 29fb30cf0959af8b913fc23b5d2c5a6d5c3a59fe12d28a6d3ee6d938ab0d6bfb
---

---
title: Mengurangi halusinasi
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
description: Minimalkan halusinasi dalam output Claude dengan mengizinkan ketidakpastian, mendasarkan respons pada kutipan langsung, dan memverifikasi klaim dengan sitasi.
---

Bahkan model bahasa paling canggih, seperti Claude, terkadang dapat menghasilkan teks yang secara faktual salah atau tidak konsisten dengan konteks yang diberikan. Fenomena ini, yang dikenal sebagai “hallucination” (halusinasi), dapat merusak keandalan solusi berbasis AI Anda. Panduan ini membahas teknik-teknik untuk meminimalkan halusinasi dan memastikan output Claude akurat dan dapat dipercaya.

## Strategi dasar untuk meminimalkan halusinasi

* **Izinkan Claude untuk mengatakan “Saya tidak tahu”:** Secara eksplisit berikan Claude izin untuk mengakui ketidakpastian. Teknik ini dapat secara drastis mengurangi informasi yang salah.

<Accordion title="Contoh: Menganalisis laporan merger dan akuisisi">
  ```text User wrap
  As our M&A advisor, analyze this report on the potential acquisition of AcmeCo by ExampleCorp.

  <report>
  {{REPORT}}
  </report>

  Focus on financial projections, integration risks, and regulatory hurdles. If you're unsure about any aspect or if the report lacks necessary information, say "I don't have enough information to confidently assess this."
  ```
</Accordion>

* **Gunakan kutipan langsung sebagai landasan faktual:** Untuk tugas yang melibatkan dokumen panjang (>20 ribu token), minta Claude untuk mengekstrak kutipan kata per kata terlebih dahulu sebelum melakukan tugasnya. Ini mendasarkan responsnya pada teks yang sebenarnya, sehingga mengurangi halusinasi.

<Accordion title="Contoh: Mengaudit kebijakan privasi data">
  ```text User wrap
  As our Data Protection Officer, review this updated privacy policy for GDPR and CCPA compliance.
  <policy>
  {{POLICY}}
  </policy>

  1. Extract exact quotes from the policy that are most relevant to GDPR and CCPA compliance. If you can't find relevant quotes, state "No relevant quotes found."

  2. Use the quotes to analyze the compliance of these policy sections, referencing the quotes by number. Only base your analysis on the extracted quotes.
  ```
</Accordion>

* **Verifikasi dengan sitasi:** Jadikan respons Claude dapat diaudit dengan memintanya mengutip kutipan dan sumber untuk setiap klaimnya. Anda juga dapat meminta Claude memverifikasi setiap klaim dengan menemukan kutipan pendukung setelah menghasilkan respons. Jika tidak dapat menemukan kutipan, Claude harus menarik kembali klaim tersebut.

<Accordion title="Contoh: Menyusun siaran pers tentang peluncuran produk">
  ```text User wrap
  Draft a press release for our new cybersecurity product, AcmeSecurity Pro, using only information from these product briefs and market reports.
  <documents>
  {{DOCUMENTS}}
  </documents>

  After drafting, review each claim in your press release. For each claim, find a direct quote from the documents that supports it. If you can't find a supporting quote for a claim, remove that claim from the press release and mark where it was removed with empty [] brackets.
  ```
</Accordion>

***

## Teknik lanjutan

* **Verifikasi chain-of-thought:** Gunakan [thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) dengan `display: "summarized"`, dan tinjau penalaran yang dirangkum dalam blok `thinking` ketika sebuah jawaban tampak salah. Ini dapat mengungkap logika atau asumsi yang keliru.

* **Verifikasi best-of-N:** Jalankan Claude dengan prompt yang sama beberapa kali dan bandingkan outputnya. Inkonsistensi di antara output dapat mengindikasikan halusinasi.

* **Penyempurnaan iteratif:** Gunakan output Claude sebagai input untuk prompt lanjutan, dengan memintanya memverifikasi atau memperluas pernyataan sebelumnya. Ini dapat menangkap dan memperbaiki inkonsistensi.

* **Pembatasan pengetahuan eksternal:** Secara eksplisit instruksikan Claude untuk hanya menggunakan informasi dari dokumen yang diberikan dan bukan pengetahuan umumnya.

<Note>
  Ingat, meskipun teknik-teknik ini secara signifikan mengurangi halusinasi, teknik tersebut tidak menghilangkannya sepenuhnya. Selalu validasi informasi penting, terutama untuk keputusan berisiko tinggi.
</Note>
