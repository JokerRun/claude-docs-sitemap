---
source: platform
url: https://platform.claude.com/docs/id/about-claude/glossary
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 2c47f2cd077a437ea0b28e284232b11c6768bb5ba52d7db1cf4e348890ac6a75
---

# Glosarium

Konsep-konsep ini tidak unik untuk model bahasa Anthropic, tetapi kami menyajikan ringkasan singkat istilah-istilah kunci di bawah ini.

---

## Context window

"Context window" mengacu pada jumlah teks yang dapat dilihat kembali oleh model bahasa dan direferensikan saat menghasilkan teks baru. Ini berbeda dari corpus data besar tempat model bahasa dilatih, dan sebaliknya mewakili "memori kerja" untuk model. Context window yang lebih besar memungkinkan model untuk memahami dan merespons prompt yang lebih kompleks dan panjang, sementara context window yang lebih kecil dapat membatasi kemampuan model untuk menangani prompt yang lebih panjang atau mempertahankan koherensi selama percakapan yang diperpanjang.

Lihat [panduan kami tentang memahami context windows](/docs/id/build-with-claude/context-windows) untuk mempelajari lebih lanjut.

## Fine-tuning

Fine-tuning adalah proses pelatihan lebih lanjut dari model bahasa yang telah dilatih sebelumnya menggunakan data tambahan. Ini menyebabkan model mulai merepresentasikan dan meniru pola dan karakteristik dari dataset fine-tuning. Claude bukan model bahasa murni; model ini telah dilatih dengan fine-tuning untuk menjadi asisten yang membantu. API kami saat ini tidak menawarkan fine-tuning, tetapi silakan tanyakan kepada kontak Anthropic Anda jika Anda tertarik untuk menjelajahi opsi ini. Fine-tuning dapat berguna untuk menyesuaikan model bahasa dengan domain, tugas, atau gaya penulisan tertentu, tetapi memerlukan pertimbangan cermat terhadap data fine-tuning dan dampak potensial pada kinerja dan bias model.

## HHH

Ketiga H ini mewakili tujuan Anthropic dalam memastikan bahwa Claude bermanfaat bagi masyarakat:

- AI yang **helpful** akan mencoba melakukan tugas atau menjawab pertanyaan yang diajukan sebaik-baiknya, memberikan informasi yang relevan dan berguna.
- AI yang **honest** akan memberikan informasi yang akurat, dan tidak akan hallucinate atau confabulate. Ini akan mengakui keterbatasan dan ketidakpastiannya ketika sesuai.
- AI yang **harmless** tidak akan bersifat ofensif atau diskriminatif, dan ketika diminta untuk membantu dalam tindakan yang berbahaya atau tidak etis, AI harus dengan sopan menolak dan menjelaskan mengapa tidak dapat mematuhi.

## Latency

Latency, dalam konteks generative AI dan large language models, mengacu pada waktu yang diperlukan model untuk merespons prompt tertentu. Ini adalah penundaan antara pengiriman prompt dan penerimaan output yang dihasilkan. Latency yang lebih rendah menunjukkan waktu respons yang lebih cepat, yang sangat penting untuk aplikasi real-time, chatbot, dan pengalaman interaktif. Faktor yang dapat mempengaruhi latency termasuk ukuran model, kemampuan hardware, kondisi jaringan, dan kompleksitas prompt dan respons yang dihasilkan.

## LLM

Large language models (LLMs) adalah model bahasa AI dengan banyak parameter yang mampu melakukan berbagai tugas yang mengejutkan berguna. Model-model ini dilatih pada jumlah data teks yang sangat besar dan dapat menghasilkan teks yang mirip manusia, menjawab pertanyaan, merangkum informasi, dan banyak lagi. Claude adalah asisten percakapan berdasarkan large language model yang telah dilatih dengan fine-tuning dan dilatih menggunakan RLHF untuk menjadi lebih membantu, jujur, dan tidak berbahaya.

## MCP (Model Context Protocol)

Model Context Protocol (MCP) adalah protokol terbuka yang menstandarkan bagaimana aplikasi memberikan konteks kepada LLMs. Seperti port USB-C untuk aplikasi AI, MCP menyediakan cara terpadu untuk menghubungkan model AI ke berbagai sumber data dan alat. MCP memungkinkan sistem AI untuk mempertahankan konteks yang konsisten di seluruh interaksi dan mengakses sumber daya eksternal dengan cara yang terstandar. Lihat [dokumentasi MCP kami](/docs/id/mcp) untuk mempelajari lebih lanjut.

## MCP connector

MCP connector adalah fitur yang memungkinkan pengguna API untuk terhubung ke server MCP secara langsung dari Messages API tanpa membangun klien MCP. Ini memungkinkan integrasi seamless dengan alat dan layanan yang kompatibel dengan MCP melalui Claude API. MCP connector mendukung fitur seperti tool calling dan tersedia dalam beta. Lihat [dokumentasi MCP connector](/docs/id/agents-and-tools/mcp-connector) untuk mempelajari lebih lanjut.

## Pretraining

Pretraining adalah proses awal pelatihan model bahasa pada corpus teks besar yang tidak berlabel. Dalam kasus Claude, model bahasa autoregressive (seperti model dasar Claude) dilatih sebelumnya untuk memprediksi kata berikutnya, mengingat konteks teks sebelumnya dalam dokumen. Model-model yang dilatih sebelumnya ini tidak secara inheren baik dalam menjawab pertanyaan atau mengikuti instruksi, dan sering kali memerlukan keterampilan mendalam dalam prompt engineering untuk membangkitkan perilaku yang diinginkan. Fine-tuning dan RLHF digunakan untuk menyempurnakan model-model yang dilatih sebelumnya ini, menjadikannya lebih berguna untuk berbagai tugas.

## RAG (Retrieval augmented generation)

Retrieval augmented generation (RAG) adalah teknik yang menggabungkan information retrieval dengan language model generation untuk meningkatkan akurasi dan relevansi teks yang dihasilkan, dan untuk lebih mendasarkan respons model pada bukti. Dalam RAG, model bahasa ditambah dengan knowledge base eksternal atau serangkaian dokumen yang dimasukkan ke dalam context window. Data diambil pada waktu runtime ketika query dikirim ke model, meskipun model itu sendiri tidak perlu mengambil data (tetapi dapat dengan [tool use](/docs/id/agents-and-tools/tool-use/overview) dan fungsi retrieval). Saat menghasilkan teks, informasi yang relevan terlebih dahulu harus diambil dari knowledge base berdasarkan prompt input, dan kemudian diteruskan ke model bersama dengan query asli. Model menggunakan informasi ini untuk memandu output yang dihasilkannya. Ini memungkinkan model untuk mengakses dan memanfaatkan informasi di luar data pelatihannya, mengurangi ketergantungan pada memorisasi dan meningkatkan akurasi faktual teks yang dihasilkan. RAG dapat sangat berguna untuk tugas-tugas yang memerlukan informasi terkini, pengetahuan khusus domain, atau kutipan eksplisit dari sumber. Namun, efektivitas RAG tergantung pada kualitas dan relevansi knowledge base eksternal dan pengetahuan yang diambil pada runtime.

## RLHF

Reinforcement Learning from Human Feedback (RLHF) adalah teknik yang digunakan untuk melatih model bahasa yang telah dilatih sebelumnya untuk berperilaku dengan cara yang konsisten dengan preferensi manusia. Ini dapat mencakup membantu model mengikuti instruksi lebih efektif atau bertindak lebih seperti chatbot. Umpan balik manusia terdiri dari peringkat serangkaian dua atau lebih contoh teks, dan proses reinforcement learning mendorong model untuk lebih memilih output yang mirip dengan yang berperingkat lebih tinggi. Claude telah dilatih menggunakan RLHF untuk menjadi asisten yang lebih membantu. Untuk detail lebih lanjut, Anda dapat membaca [makalah Anthropic tentang subjek ini](https://arxiv.org/abs/2204.05862).

## Temperature

Temperature adalah parameter yang mengontrol keacakan prediksi model selama text generation. Suhu yang lebih tinggi menghasilkan output yang lebih kreatif dan beragam, memungkinkan variasi ganda dalam frasing dan, dalam kasus fiksi, variasi dalam jawaban juga. Suhu yang lebih rendah menghasilkan output yang lebih konservatif dan deterministik yang mematuhi frasing dan jawaban yang paling mungkin. Menyesuaikan temperature memungkinkan pengguna untuk mendorong model bahasa mengeksplorasi pilihan kata dan urutan yang jarang, tidak biasa, atau mengejutkan, daripada hanya memilih prediksi yang paling mungkin.

Pengguna mungkin mengalami non-determinism dalam APIs. Bahkan dengan temperature diatur ke 0, hasilnya tidak akan sepenuhnya deterministik dan input yang identik dapat menghasilkan output yang berbeda di seluruh panggilan API. Ini berlaku baik untuk layanan inference first-party Anthropic maupun untuk inference melalui penyedia cloud pihak ketiga.

## TTFT (Time to first token)

Time to First Token (TTFT) adalah metrik kinerja yang mengukur waktu yang diperlukan model bahasa untuk menghasilkan token pertama dari outputnya setelah menerima prompt. Ini adalah indikator penting dari responsivitas model dan sangat relevan untuk aplikasi interaktif, chatbot, dan sistem real-time di mana pengguna mengharapkan umpan balik awal yang cepat. TTFT yang lebih rendah menunjukkan bahwa model dapat mulai menghasilkan respons lebih cepat, memberikan pengalaman pengguna yang lebih seamless dan engaging. Faktor yang dapat mempengaruhi TTFT termasuk ukuran model, kemampuan hardware, kondisi jaringan, dan kompleksitas prompt.

## Tokens

Tokens adalah unit individual terkecil dari model bahasa, dan dapat sesuai dengan kata, subword, karakter, atau bahkan byte (dalam kasus Unicode). Untuk Claude, token kira-kira mewakili 3,5 karakter Inggris, meskipun jumlah pastinya dapat bervariasi tergantung pada bahasa yang digunakan. Tokens biasanya tersembunyi saat berinteraksi dengan model bahasa pada tingkat "teks" tetapi menjadi relevan saat memeriksa input dan output yang tepat dari model bahasa. Ketika Claude disediakan dengan teks untuk dievaluasi, teks (terdiri dari serangkaian karakter) dikodekan menjadi serangkaian token untuk diproses oleh model. Token yang lebih besar memungkinkan efisiensi data selama inference dan pretraining (dan digunakan jika memungkinkan), sementara token yang lebih kecil memungkinkan model menangani kata-kata yang tidak biasa atau belum pernah dilihat sebelumnya. Pilihan metode tokenisasi dapat mempengaruhi kinerja model, ukuran kosakata, dan kemampuan menangani kata-kata out-of-vocabulary.