---
source: platform
url: https://platform.claude.com/docs/id/about-claude/glossary
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 8bd6725a5343f92954b70deff5b2c85e7fb295ee5426664e853f656a5d2c2848
---

# Glosarium

Konsep-konsep ini tidak unik untuk model bahasa Anthropic, tetapi kami menyajikan ringkasan singkat istilah-istilah kunci di bawah ini.

---

## Context window

"Context window" (jendela konteks) mengacu pada jumlah teks yang dapat dilihat kembali dan direferensikan oleh model bahasa saat menghasilkan teks baru. Ini berbeda dari korpus data besar yang digunakan untuk melatih model bahasa, dan sebaliknya mewakili "memori kerja" untuk model tersebut. Jendela konteks yang lebih besar memungkinkan model untuk memahami dan merespons prompt yang lebih kompleks dan panjang, sementara jendela konteks yang lebih kecil dapat membatasi kemampuan model untuk menangani prompt yang lebih panjang atau mempertahankan koherensi selama percakapan yang diperpanjang.

Lihat [panduan kami untuk memahami jendela konteks](/docs/id/build-with-claude/context-windows) untuk mempelajari lebih lanjut.

## Fine-tuning

"Fine-tuning" (penyetelan halus) adalah proses pelatihan lebih lanjut dari model bahasa yang telah dilatih sebelumnya menggunakan data tambahan. Ini menyebabkan model mulai merepresentasikan dan meniru pola serta karakteristik dari dataset fine-tuning. Claude bukan model bahasa murni; model ini telah melalui fine-tuning untuk menjadi asisten yang membantu. API kami saat ini tidak menawarkan fine-tuning, tetapi silakan tanyakan kepada kontak Anthropic Anda jika Anda tertarik untuk menjelajahi opsi ini. Fine-tuning dapat berguna untuk menyesuaikan model bahasa dengan domain, tugas, atau gaya penulisan tertentu, tetapi memerlukan pertimbangan cermat terhadap data fine-tuning dan dampak potensial pada kinerja serta bias model.

## HHH

Ketiga H ini mewakili tujuan Anthropic dalam memastikan bahwa Claude bermanfaat bagi masyarakat:

* AI yang **helpful** (membantu) akan mencoba melakukan tugas atau menjawab pertanyaan yang diajukan dengan kemampuan terbaiknya, memberikan informasi yang relevan dan berguna.
* AI yang **honest** (jujur) akan memberikan informasi yang akurat, dan tidak akan berhalusinasi atau mengarang. AI ini akan mengakui keterbatasan dan ketidakpastiannya ketika sesuai.
* AI yang **harmless** (tidak berbahaya) tidak akan bersifat ofensif atau diskriminatif, dan ketika diminta untuk membantu dalam tindakan yang berbahaya atau tidak etis, AI harus dengan sopan menolak dan menjelaskan mengapa tidak dapat mematuhi.

## Latency

"Latency" (latensi), dalam konteks AI generatif dan model bahasa besar, mengacu pada waktu yang diperlukan model untuk merespons prompt tertentu. Ini adalah jeda antara pengiriman prompt dan penerimaan output yang dihasilkan. Latensi yang lebih rendah menunjukkan waktu respons yang lebih cepat, yang sangat penting untuk aplikasi real-time, chatbot, dan pengalaman interaktif. Faktor yang dapat memengaruhi latensi termasuk ukuran model, kemampuan hardware, kondisi jaringan, serta kompleksitas prompt dan respons yang dihasilkan.

## LLM

"Large language models" (model bahasa besar), atau LLM, adalah model bahasa AI dengan banyak parameter yang mampu melakukan berbagai tugas yang sangat berguna. Model-model ini dilatih pada jumlah data teks yang sangat besar dan dapat menghasilkan teks yang mirip manusia, menjawab pertanyaan, merangkum informasi, dan banyak lagi. Claude adalah asisten percakapan berdasarkan model bahasa besar yang telah melalui fine-tuning dan dilatih menggunakan RLHF untuk menjadi lebih membantu, jujur, dan tidak berbahaya.

## MCP (Model Context Protocol)

"Model Context Protocol", atau MCP, adalah protokol terbuka yang menstandarkan bagaimana aplikasi memberikan konteks kepada LLM. Seperti port USB-C untuk aplikasi AI, MCP menyediakan cara terpadu untuk menghubungkan model AI ke berbagai sumber data dan alat. MCP memungkinkan sistem AI untuk mempertahankan konteks yang konsisten di seluruh interaksi dan mengakses sumber daya eksternal dengan cara yang terstandar. Lihat [dokumentasi MCP kami](/docs/id/mcp) untuk mempelajari lebih lanjut.

## MCP connector

MCP connector adalah fitur yang memungkinkan pengguna API untuk terhubung ke server MCP langsung dari Messages API tanpa membangun klien MCP. Ini memungkinkan integrasi yang mulus dengan alat dan layanan yang kompatibel dengan MCP melalui Claude API. MCP connector mendukung fitur seperti pemanggilan alat dan tersedia dalam versi beta. Lihat [dokumentasi MCP connector](/docs/id/agents-and-tools/mcp-connector) untuk mempelajari lebih lanjut.

## Pretraining

"Pretraining" (prapelatihan) adalah proses awal pelatihan model bahasa pada korpus teks besar yang tidak berlabel. Dalam kasus Claude, model bahasa autoregresif (seperti model yang mendasari Claude) dilatih sebelumnya untuk memprediksi kata berikutnya, berdasarkan konteks teks sebelumnya dalam dokumen. Model yang telah dilatih sebelumnya ini secara inheren tidak pandai menjawab pertanyaan atau mengikuti instruksi, dan sering kali memerlukan keterampilan mendalam dalam rekayasa prompt untuk memunculkan perilaku yang diinginkan. Fine-tuning dan RLHF digunakan untuk menyempurnakan model yang telah dilatih sebelumnya ini, menjadikannya lebih berguna untuk berbagai tugas.

## RAG (Retrieval augmented generation)

"Retrieval augmented generation" (generasi yang diperkaya pengambilan), atau RAG, adalah teknik yang menggabungkan pengambilan informasi dengan generasi model bahasa untuk meningkatkan akurasi dan relevansi teks yang dihasilkan, serta untuk lebih mendasarkan respons model pada bukti. Dalam RAG, model bahasa diperkaya dengan basis pengetahuan eksternal atau sekumpulan dokumen yang diteruskan ke dalam jendela konteks. Data diambil pada saat runtime ketika kueri dikirim ke model, meskipun model itu sendiri tidak selalu mengambil data tersebut (tetapi dapat melakukannya dengan [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview) dan fungsi pengambilan). Saat menghasilkan teks, informasi yang relevan pertama-tama harus diambil dari basis pengetahuan berdasarkan prompt input, lalu diteruskan ke model bersama dengan kueri asli. Model menggunakan informasi ini untuk memandu output yang dihasilkannya. Ini memungkinkan model untuk mengakses dan memanfaatkan informasi di luar data pelatihannya, mengurangi ketergantungan pada hafalan dan meningkatkan akurasi faktual dari teks yang dihasilkan. RAG dapat sangat berguna untuk tugas yang memerlukan informasi terkini, pengetahuan khusus domain, atau kutipan sumber secara eksplisit. Namun, efektivitas RAG bergantung pada kualitas dan relevansi basis pengetahuan eksternal serta pengetahuan yang diambil pada saat runtime.

## RLHF

"Reinforcement Learning from Human Feedback" (pembelajaran penguatan dari umpan balik manusia), atau RLHF, adalah teknik yang digunakan untuk melatih model bahasa yang telah dilatih sebelumnya agar berperilaku dengan cara yang konsisten dengan preferensi manusia. Ini dapat mencakup membantu model mengikuti instruksi dengan lebih efektif atau bertindak lebih seperti chatbot. Umpan balik manusia terdiri dari pemeringkatan sekumpulan dua atau lebih contoh teks, dan proses pembelajaran penguatan mendorong model untuk lebih memilih output yang mirip dengan yang berperingkat lebih tinggi. Claude telah dilatih menggunakan RLHF untuk menjadi asisten yang lebih membantu. Untuk detail lebih lanjut, Anda dapat membaca [makalah Anthropic tentang subjek ini](https://arxiv.org/abs/2204.05862).

## Temperature

"Temperature" (temperatur) adalah parameter yang mengontrol keacakan prediksi model selama pembuatan teks. Temperatur yang lebih tinggi menghasilkan output yang lebih kreatif dan beragam, memungkinkan berbagai variasi dalam penyusunan kalimat dan, dalam kasus fiksi, variasi dalam jawaban juga. Temperatur yang lebih rendah menghasilkan output yang lebih konservatif dan deterministik yang berpegang pada penyusunan kalimat dan jawaban yang paling mungkin. Menyesuaikan temperatur memungkinkan pengguna untuk mendorong model bahasa mengeksplorasi pilihan dan urutan kata yang langka, tidak umum, atau mengejutkan, daripada hanya memilih prediksi yang paling mungkin.

Pengguna mungkin menemukan non-determinisme dalam API. Bahkan dengan temperatur yang diatur ke 0, hasilnya tidak akan sepenuhnya deterministik dan input yang identik dapat menghasilkan output yang berbeda di seluruh panggilan API. Ini berlaku baik untuk layanan inferensi pihak pertama Anthropic maupun untuk inferensi melalui penyedia cloud pihak ketiga.

## TTFT (Time to first token)

"Time to First Token" (waktu ke token pertama), atau TTFT, adalah metrik kinerja yang mengukur waktu yang diperlukan model bahasa untuk menghasilkan token pertama dari outputnya setelah menerima prompt. Ini adalah indikator penting dari responsivitas model dan sangat relevan untuk aplikasi interaktif, chatbot, dan sistem real-time di mana pengguna mengharapkan umpan balik awal yang cepat. TTFT yang lebih rendah menunjukkan bahwa model dapat mulai menghasilkan respons lebih cepat, memberikan pengalaman pengguna yang lebih mulus dan menarik. Faktor yang dapat memengaruhi TTFT termasuk ukuran model, kemampuan hardware, kondisi jaringan, dan kompleksitas prompt.

## Token

Token adalah unit individual terkecil dari model bahasa, dan dapat berkorespondensi dengan kata, subkata, karakter, atau bahkan byte (dalam kasus Unicode). Untuk Claude, satu token kira-kira mewakili 3,5 karakter bahasa Inggris, meskipun jumlah pastinya dapat bervariasi tergantung pada bahasa yang digunakan. Token biasanya tersembunyi saat berinteraksi dengan model bahasa pada level "teks" tetapi menjadi relevan saat memeriksa input dan output yang tepat dari model bahasa. Ketika Claude diberikan teks untuk dievaluasi, teks tersebut (yang terdiri dari serangkaian karakter) dikodekan menjadi serangkaian token untuk diproses oleh model. Token yang lebih besar memungkinkan efisiensi data selama inferensi dan prapelatihan (dan digunakan jika memungkinkan), sementara token yang lebih kecil memungkinkan model untuk menangani kata-kata yang tidak umum atau belum pernah dilihat sebelumnya. Pilihan metode tokenisasi dapat memengaruhi kinerja model, ukuran kosakata, dan kemampuan untuk menangani kata-kata di luar kosakata.
