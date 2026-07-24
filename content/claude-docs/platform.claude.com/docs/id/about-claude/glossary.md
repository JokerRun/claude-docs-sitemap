---
source: platform
url: https://platform.claude.com/docs/id/about-claude/glossary
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 2159a74f20c2eccf772241a7ee657faca49dc987e47f5d9ce4719ac48297891c
---

# Glosarium

Konsep-konsep ini tidak unik untuk model bahasa Anthropic, tetapi halaman ini menyajikan ringkasan singkat dari istilah-istilah kunci.

---

## Context window

"Context window" (jendela konteks) mengacu pada jumlah teks yang dapat dilihat kembali oleh model bahasa dan direferensikan saat menghasilkan teks baru. Ini berbeda dari corpus data besar tempat model bahasa dilatih, dan sebaliknya mewakili "memori kerja" untuk model. Jendela konteks yang lebih besar memungkinkan model untuk memproses dan merespons prompt yang lebih kompleks dan panjang, sementara jendela konteks yang lebih kecil dapat membatasi kemampuan model untuk menangani prompt yang lebih panjang atau mempertahankan koherensi selama percakapan yang diperpanjang.

Lihat [panduan untuk memahami jendela konteks](/docs/id/build-with-claude/context-windows) untuk mempelajari lebih lanjut.

## Fine-tuning

"Fine-tuning" (penyetelan halus) adalah proses pelatihan lebih lanjut dari model bahasa yang telah dilatih sebelumnya menggunakan data tambahan. Ini menyebabkan model mulai merepresentasikan dan meniru pola dan karakteristik dari dataset fine-tuning. Claude bukan model bahasa murni; model ini telah dilatih dengan fine-tuning untuk menjadi asisten yang membantu. Claude API saat ini tidak menawarkan fine-tuning, tetapi silakan tanyakan kepada kontak Anthropic Anda jika Anda tertarik untuk menjelajahi opsi ini. Fine-tuning dapat berguna untuk menyesuaikan model bahasa dengan domain, tugas, atau gaya penulisan tertentu, tetapi memerlukan pertimbangan cermat terhadap data fine-tuning dan dampak potensial pada kinerja dan bias model.

## HHH

Ketiga H ini mewakili tujuan Anthropic dalam memastikan bahwa Claude bermanfaat bagi masyarakat:

* AI yang **helpful** akan mencoba melakukan tugas atau menjawab pertanyaan yang diajukan sebaik-baiknya, memberikan informasi yang relevan dan berguna.
* AI yang **honest** akan memberikan informasi yang akurat, dan tidak akan hallucinate atau confabulate. Ini akan mengakui keterbatasan dan ketidakpastiannya ketika sesuai.
* AI yang **harmless** tidak akan bersifat ofensif atau diskriminatif, dan ketika diminta untuk membantu dalam tindakan yang berbahaya atau tidak etis, AI harus dengan sopan menolak dan menjelaskan mengapa tidak dapat mematuhi.

## Latency

"Latency" (latensi), dalam konteks AI generatif dan model bahasa besar, mengacu pada waktu yang diperlukan model untuk merespons prompt tertentu. Ini adalah penundaan antara pengiriman prompt dan penerimaan output yang dihasilkan. Latency yang lebih rendah menunjukkan waktu respons yang lebih cepat, yang sangat penting untuk aplikasi real-time, chatbot, dan pengalaman interaktif. Faktor yang dapat mempengaruhi latency termasuk ukuran model, kemampuan hardware, kondisi jaringan, dan kompleksitas prompt dan respons yang dihasilkan.

## LLM

"Large language models" (model bahasa besar), atau LLM, adalah model bahasa AI dengan banyak parameter yang mampu melakukan berbagai tugas yang mengejutkan berguna. Model-model ini dilatih pada jumlah data teks yang sangat besar dan dapat menghasilkan teks yang mirip manusia, menjawab pertanyaan, merangkum informasi, dan banyak lagi. Claude adalah asisten percakapan berdasarkan model bahasa besar yang telah dilatih dengan fine-tuning dan dilatih menggunakan RLHF untuk menjadi lebih membantu, jujur, dan tidak berbahaya.

## MCP (Model Context Protocol)

"Model Context Protocol", atau MCP, adalah protokol terbuka yang menstandarkan bagaimana aplikasi memberikan konteks kepada LLM. Seperti port USB-C untuk aplikasi AI, MCP menyediakan cara terpadu untuk menghubungkan model AI ke berbagai sumber data dan alat. MCP memungkinkan sistem AI untuk mempertahankan konteks yang konsisten di seluruh interaksi dan mengakses sumber daya eksternal dengan cara yang terstandar. Lihat [dokumentasi MCP](/docs/id/mcp) untuk mempelajari lebih lanjut.

## MCP connector

"MCP connector" (konektor MCP) adalah fitur yang memungkinkan pengguna API untuk terhubung ke server MCP langsung dari Messages API tanpa membangun klien MCP. Ini memungkinkan integrasi yang mulus dengan alat dan layanan yang kompatibel dengan MCP melalui Claude API. MCP connector mendukung fitur seperti pemanggilan alat dan tersedia dalam versi beta. Lihat dokumentasi [MCP connector](/docs/id/agents-and-tools/mcp-connector) untuk mempelajari lebih lanjut.

## Pretraining

"Pretraining" (pralatihan) adalah proses awal pelatihan model bahasa pada corpus teks besar yang tidak berlabel. Dalam kasus Claude, model bahasa autoregresif (seperti model yang mendasari Claude) dilatih sebelumnya untuk memprediksi kata berikutnya, berdasarkan konteks teks sebelumnya dalam dokumen. Model yang telah dilatih sebelumnya ini pada dasarnya tidak pandai menjawab pertanyaan atau mengikuti instruksi, dan sering kali memerlukan keterampilan mendalam dalam rekayasa prompt untuk memunculkan perilaku yang diinginkan. Fine-tuning dan RLHF digunakan untuk menyempurnakan model yang telah dilatih sebelumnya ini, membuatnya lebih berguna untuk berbagai macam tugas.

## RAG (Retrieval augmented generation)

"Retrieval augmented generation" (generasi yang ditingkatkan dengan pengambilan), atau RAG, adalah teknik yang menggabungkan pengambilan informasi dengan generasi model bahasa untuk meningkatkan akurasi dan relevansi teks yang dihasilkan, dan untuk lebih mendasarkan respons model pada bukti. Dalam RAG, model bahasa ditingkatkan dengan basis pengetahuan eksternal atau sekumpulan dokumen yang dimasukkan ke dalam jendela konteks. Data diambil pada saat runtime ketika kueri dikirim ke model, meskipun model itu sendiri tidak selalu mengambil data (tetapi dapat melakukannya dengan [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview) dan fungsi pengambilan). Saat menghasilkan teks, informasi yang relevan pertama-tama harus diambil dari basis pengetahuan berdasarkan prompt input, dan kemudian diteruskan ke model bersama dengan kueri asli. Model menggunakan informasi ini untuk memandu output yang dihasilkannya. Ini memungkinkan model untuk mengakses dan menggunakan informasi di luar data pelatihannya, mengurangi ketergantungan pada hafalan dan meningkatkan akurasi faktual dari teks yang dihasilkan. RAG dapat sangat berguna untuk tugas-tugas yang memerlukan informasi terkini, pengetahuan spesifik domain, atau kutipan sumber yang eksplisit. Namun, efektivitas RAG bergantung pada kualitas dan relevansi basis pengetahuan eksternal dan pengetahuan yang diambil pada saat runtime.

## RLHF

"Reinforcement Learning from Human Feedback" (pembelajaran penguatan dari umpan balik manusia), atau RLHF, adalah teknik yang digunakan untuk melatih model bahasa yang telah dilatih sebelumnya agar berperilaku dengan cara yang konsisten dengan preferensi manusia. Ini dapat mencakup membantu model mengikuti instruksi dengan lebih efektif atau bertindak lebih seperti chatbot. Umpan balik manusia terdiri dari pemeringkatan sekumpulan dua atau lebih contoh teks, dan proses pembelajaran penguatan mendorong model untuk lebih memilih output yang mirip dengan yang berperingkat lebih tinggi. Claude telah dilatih menggunakan RLHF untuk menjadi asisten yang lebih membantu. Untuk detail lebih lanjut, Anda dapat membaca [makalah Anthropic tentang subjek ini](https://arxiv.org/abs/2204.05862).

## Temperature

"Temperature" (temperatur) adalah parameter yang mengontrol keacakan prediksi model selama pembuatan teks. Temperature yang lebih tinggi menghasilkan output yang lebih kreatif dan beragam, memungkinkan beberapa variasi dalam penyusunan kata dan, dalam kasus fiksi, variasi dalam jawaban juga. Temperature yang lebih rendah menghasilkan output yang lebih konservatif dan deterministik yang berpegang pada penyusunan kata dan jawaban yang paling mungkin. Menyesuaikan temperature memungkinkan pengguna untuk mendorong model bahasa mengeksplorasi pilihan kata dan urutan yang langka, tidak umum, atau mengejutkan, daripada hanya memilih prediksi yang paling mungkin.

Pengguna mungkin menemui non-determinisme dalam API. Bahkan dengan temperature diatur ke 0, hasilnya tidak akan sepenuhnya deterministik dan input yang identik dapat menghasilkan output yang berbeda di seluruh panggilan API. Ini berlaku baik untuk layanan inferensi pihak pertama Anthropic maupun untuk inferensi melalui penyedia cloud pihak ketiga.

## TTFT (Time to first token)

"Time to First Token" (waktu hingga token pertama), atau TTFT, adalah metrik kinerja yang mengukur waktu yang diperlukan model bahasa untuk menghasilkan token pertama dari outputnya setelah menerima prompt. Ini adalah indikator penting dari responsivitas model dan sangat relevan untuk aplikasi interaktif, chatbot, dan sistem real-time di mana pengguna mengharapkan umpan balik awal yang cepat. TTFT yang lebih rendah menunjukkan bahwa model dapat mulai menghasilkan respons lebih cepat, memberikan pengalaman pengguna yang lebih mulus dan menarik. Faktor yang dapat mempengaruhi TTFT termasuk ukuran model, kemampuan hardware, kondisi jaringan, dan kompleksitas prompt.

## Token

Token adalah unit individual terkecil dari model bahasa, dan dapat berkorespondensi dengan kata, subkata, karakter, atau bahkan byte (dalam kasus Unicode). Untuk Claude, satu token kira-kira mewakili 3,5 karakter bahasa Inggris, meskipun jumlah pastinya dapat bervariasi tergantung pada bahasa yang digunakan. Token biasanya tersembunyi saat berinteraksi dengan model bahasa pada tingkat "teks" tetapi menjadi relevan saat memeriksa input dan output yang tepat dari model bahasa. Ketika Claude diberikan teks untuk dievaluasi, teks (yang terdiri dari serangkaian karakter) dikodekan menjadi serangkaian token untuk diproses oleh model. Token yang lebih besar memungkinkan efisiensi data selama inferensi dan pretraining (dan digunakan jika memungkinkan), sementara token yang lebih kecil memungkinkan model untuk menangani kata-kata yang tidak umum atau belum pernah dilihat sebelumnya. Pilihan metode tokenisasi dapat mempengaruhi kinerja model, ukuran kosakata, dan kemampuan untuk menangani kata-kata di luar kosakata.
