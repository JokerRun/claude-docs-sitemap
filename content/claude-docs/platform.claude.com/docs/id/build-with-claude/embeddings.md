---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/embeddings
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 43517619910e68d7986235bbe124d45a5c21eeabeb736748a893dd268ae91024
---

---
title: Embeddings
url: https://platform.claude.com/docs/id/build-with-claude/embeddings
description: Text embeddings adalah representasi numerik dari teks yang memungkinkan pengukuran kemiripan semantik. Panduan ini memperkenalkan embeddings, penerapannya, dan cara menggunakan model embedding untuk tugas-tugas seperti pencarian, rekomendasi, dan deteksi anomali.
---

## Sebelum mengimplementasikan embeddings

Saat memilih penyedia embeddings, ada beberapa faktor yang dapat Anda pertimbangkan tergantung pada kebutuhan dan preferensi Anda:

* Ukuran dataset & kekhususan domain: ukuran dataset pelatihan model dan relevansinya terhadap domain yang ingin Anda embed. Data yang lebih besar atau lebih spesifik terhadap domain umumnya menghasilkan embeddings dalam-domain yang lebih baik
* Performa inferensi: kecepatan pencarian embedding dan "latency" (latensi) end-to-end. Ini merupakan pertimbangan yang sangat penting untuk deployment produksi berskala besar
* Kustomisasi: opsi untuk pelatihan lanjutan pada data privat, atau spesialisasi model untuk domain yang sangat spesifik. Ini dapat meningkatkan performa pada kosakata yang unik

## Cara mendapatkan embeddings dengan Anthropic

Anthropic tidak menawarkan model embedding sendiri. Salah satu penyedia embeddings dengan beragam model dan kemampuan adalah Voyage AI oleh MongoDB.

Voyage AI membuat model embedding dan reranker. Model embedding-nya mencakup model serbaguna, multimodal, terkontekstualisasi, dan spesifik domain.

Sisa panduan ini ditujukan untuk Voyage AI, tetapi Anda sebaiknya menilai berbagai vendor embeddings untuk menemukan yang paling sesuai dengan kasus penggunaan spesifik Anda.

## Model yang tersedia

Voyage AI menawarkan model text embedding berikut:

**Generasi terbaru**

| Model            | Panjang konteks | Dimensi embedding              | Deskripsi                                                                                                                                                                                                                                                                                                  |
| ---------------- | --------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voyage-4-large` | 32.000          | 1024 (default), 256, 512, 2048 | Kualitas retrieval serbaguna dan multibahasa terbaik. Lihat [postingan blog Voyage 4](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya.                                                                                                                                                     |
| `voyage-4`       | 32.000          | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk kualitas retrieval serbaguna dan multibahasa. Menyeimbangkan kualitas dan efisiensi. Lihat [postingan blog Voyage 4](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya.                                                                                                   |
| `voyage-4-lite`  | 32.000          | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk latensi dan biaya. Lihat [postingan blog Voyage 4](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya.                                                                                                                                                                     |
| `voyage-code-4`  | 32.000          | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk retrieval **kode** dan aplikasi agentic coding. Lihat [postingan blog voyage-code-4](https://blog.voyageai.com/2026/08/13/voyage-code-4/) untuk detailnya.                                                                                                                              |
| `voyage-4-nano`  | 32.000          | 2048 (default), 256, 512, 1024 | Model open-weight (lisensi Apache 2.0) yang Anda unduh dari [Hugging Face](https://huggingface.co/voyageai/voyage-4-nano) dan jalankan sendiri. Tidak tersedia melalui Atlas Embedding and Reranking API. Lihat [postingan blog Voyage 4](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya. |

**Generasi sebelumnya**

Untuk status siklus hidup setiap model dan pengganti yang direkomendasikan, lihat [Model deprecations, lifecycle states, and support](https://www.mongodb.com/docs/voyageai/models/lifecycle/) dalam dokumentasi MongoDB.

| Model              | Panjang konteks | Dimensi embedding              | Deskripsi                                                                                                                                                                                                       |
| ------------------ | --------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voyage-3-large`   | 32.000          | 1024 (default), 256, 512, 2048 | Generasi sebelumnya dari `voyage-4-large`. Lihat [postingan blog voyage-3-large](https://blog.voyageai.com/2025/01/07/voyage-3-large/) untuk detailnya.                                                         |
| `voyage-3.5`       | 32.000          | 1024 (default), 256, 512, 2048 | Generasi sebelumnya dari `voyage-4`. Lihat [postingan blog voyage-3.5](https://blog.voyageai.com/2025/05/20/voyage-3-5/) untuk detailnya.                                                                       |
| `voyage-3.5-lite`  | 32.000          | 1024 (default), 256, 512, 2048 | Generasi sebelumnya dari `voyage-4-lite`. Lihat [postingan blog voyage-3.5](https://blog.voyageai.com/2025/05/20/voyage-3-5/) untuk detailnya.                                                                  |
| `voyage-code-3`    | 32.000          | 1024 (default), 256, 512, 2048 | Generasi sebelumnya dari `voyage-code-4`. Lihat [postingan blog voyage-code-3](https://blog.voyageai.com/2024/12/04/voyage-code-3/) untuk detailnya.                                                            |
| `voyage-finance-2` | 32.000          | 1024                           | Dioptimalkan untuk retrieval dan RAG **keuangan**. Lihat [postingan blog voyage-finance-2](https://blog.voyageai.com/2024/06/03/domain-specific-embeddings-finance-edition-voyage-finance-2/) untuk detailnya.  |
| `voyage-law-2`     | 16.000          | 1024                           | Dioptimalkan untuk retrieval dan RAG **hukum**. Lihat [postingan blog voyage-law-2](https://blog.voyageai.com/2024/04/15/domain-specific-embeddings-and-retrieval-legal-edition-voyage-law-2/) untuk detailnya. |

Selain itu, Voyage AI menawarkan model embedding multimodal berikut. Panggil model-model ini dengan `multimodal_embed()` alih-alih `embed()`:

| Model                   | Panjang konteks | Dimensi embedding              | Deskripsi                                                                                                                                                                                                                                                                                                                     |
| ----------------------- | --------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voyage-multimodal-3.5` | 32.000          | 1024 (default), 256, 512, 2048 | Model embedding multimodal yang kaya yang dapat memvektorisasi teks, gambar, dan video yang saling berselang-seling. Mencakup dukungan video sebagai model embedding video kelas produksi pertama. Lihat [postingan blog voyage-multimodal-3.5](https://blog.voyageai.com/2026/01/15/voyage-multimodal-3-5/) untuk detailnya. |
| `voyage-multimodal-3`   | 32.000          | 1024                           | Generasi sebelumnya dari `voyage-multimodal-3.5`. Memvektorisasi teks yang saling berselang-seling dan gambar yang kaya konten, seperti tangkapan layar PDF, slide, tabel, gambar, dan lainnya. Lihat [postingan blog voyage-multimodal-3](https://blog.voyageai.com/2024/11/12/voyage-multimodal-3/) untuk detailnya.        |

Model contextualized chunk embedding berikut menghasilkan vektor tingkat chunk yang menangkap konteks dokumen secara penuh tanpa augmentasi metadata manual. Panggil model-model ini dengan `contextualized_embed()` alih-alih `embed()`:

| Model              | Panjang konteks | Dimensi embedding              | Deskripsi                                                                                                                                                                                                              |
| ------------------ | --------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voyage-context-4` | 120.000         | 1024 (default), 256, 512, 2048 | Contextualized chunk embeddings yang dioptimalkan untuk kualitas retrieval serbaguna dan multibahasa. Lihat [postingan blog voyage-context-4](https://blog.voyageai.com/2026/06/29/voyage-context-4/) untuk detailnya. |
| `voyage-context-3` | 120.000         | 1024 (default), 256, 512, 2048 | Generasi sebelumnya dari `voyage-context-4`. Lihat [postingan blog voyage-context-3](https://blog.voyageai.com/2025/07/23/voyage-context-3/) untuk detailnya.                                                          |

Batas 120.000 token berlaku ketika Anda mengatur `enable_auto_chunking` ke `true`. Jika tidak, jumlah total token di semua input tidak boleh melebihi 32.000.

Voyage AI juga menawarkan reranker, yang menerima sebuah query dan daftar dokumen lalu mengembalikannya dalam urutan berdasarkan relevansi terhadap query tersebut. Panggil model-model ini dengan `rerank()`:

| Model             | Panjang konteks | Deskripsi                                                                                                                                                           |
| ----------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rerank-3`        | 32.000          | Akurasi tertinggi. Direkomendasikan untuk sebagian besar aplikasi. Lihat [postingan blog rerank-3](https://blog.voyageai.com/2026/09/30/rerank-3/) untuk detailnya. |
| `rerank-3-lite`   | 32.000          | Dioptimalkan untuk latensi dan biaya. Lihat [postingan blog rerank-3](https://blog.voyageai.com/2026/09/30/rerank-3/) untuk detailnya.                              |
| `rerank-2.5`      | 32.000          | Generasi sebelumnya dari `rerank-3`. Lihat [postingan blog rerank-2.5](https://blog.voyageai.com/2025/08/11/rerank-2-5/) untuk detailnya.                           |
| `rerank-2.5-lite` | 32.000          | Generasi sebelumnya dari `rerank-3-lite`. Lihat [postingan blog rerank-2.5](https://blog.voyageai.com/2025/08/11/rerank-2-5/) untuk detailnya.                      |

Butuh bantuan memutuskan model mana yang akan digunakan? Lihat [Voyage AI embedding and reranking models overview](https://www.mongodb.com/docs/voyageai/models/) dalam dokumentasi MongoDB.

## Memulai dengan Voyage AI

Untuk mengakses model Voyage AI, buat kunci API model di MongoDB Atlas:

1. Buat akun MongoDB Atlas, atau masuk.
2. Di proyek Atlas Anda, pilih **AI Model APIs** di bilah navigasi, klik **Create model API key**, beri nama kunci tersebut, lalu klik **Create**.
3. Atur kunci API sebagai variabel lingkungan untuk kemudahan:

```bash
export VOYAGE_API_KEY="<your model API key>"
```

Untuk detail lebih lanjut, lihat [Voyage AI quick start](https://www.mongodb.com/docs/voyageai/quickstart/) dalam dokumentasi MongoDB.

Anda dapat memperoleh embeddings dengan menggunakan [paket Python `voyageai`](https://github.com/voyage-ai/voyageai-python) resmi atau permintaan HTTP, seperti yang dijelaskan di bagian-bagian berikut. Voyage AI juga memiliki klien TypeScript resmi. Untuk menggunakannya dengan kunci API model dari Atlas, atur opsi `environment`-nya ke `https://ai.mongodb.com/v1`, seperti yang dijelaskan dalam [TypeScript client](https://www.mongodb.com/docs/voyageai/api-and-clients/#typescript-client) dalam dokumentasi MongoDB.

### Pustaka Python Voyage AI

Instal paket `voyageai` menggunakan perintah berikut. Untuk menggunakan kunci API model dari Atlas, Anda memerlukan versi 0.3.7 atau yang lebih baru.

```bash
pip install -U voyageai
```

Kemudian, Anda dapat membuat objek client dan mulai menggunakannya untuk meng-embed teks Anda:

```python
import voyageai

vo = voyageai.Client()
# Ini akan otomatis menggunakan variabel lingkungan VOYAGE_API_KEY.
# Sebagai alternatif, Anda dapat menggunakan vo = voyageai.Client(api_key="<kunci API model Anda>")

texts = ["Sample text 1", "Sample text 2"]

result = vo.embed(texts, model="voyage-4", input_type="document")
print(result.embeddings[0])
print(result.embeddings[1])
```

`result.embeddings` adalah daftar berisi dua vektor embedding, masing-masing berisi 1024 bilangan floating-point. Setelah menjalankan kode di atas, kedua embeddings tersebut dicetak di layar:

```text
[-0.013131560757756233, 0.019828535616397858, ...]   # embedding for "Sample text 1"
[-0.0069352793507277966, 0.020878976210951805, ...]  # embedding for "Sample text 2"
```

Saat membuat embeddings, Anda dapat menentukan beberapa argumen lain pada fungsi `embed()`.

Untuk informasi lebih lanjut tentang paket Python, lihat [Accessing Voyage AI models](https://www.mongodb.com/docs/voyageai/api-and-clients/) dalam dokumentasi MongoDB.

### HTTP API Voyage AI

Anda juga dapat memperoleh embeddings dengan mengirimkan permintaan HTTP ke Atlas Embedding and Reranking API. Misalnya, Anda dapat mengirim permintaan HTTP melalui perintah `curl` di terminal:

```bash cURL
curl https://ai.mongodb.com/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VOYAGE_API_KEY" \
  -d '{
    "input": ["Sample text 1", "Sample text 2"],
    "model": "voyage-4",
    "input_type": "document"
  }'
```

Respons yang akan Anda dapatkan adalah objek JSON yang berisi embeddings dan penggunaan token:

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [-0.013131560757756233, 0.019828535616397858 /* ... */],
      "index": 0
    },
    {
      "object": "embedding",
      "embedding": [-0.0069352793507277966, 0.020878976210951805 /* ... */],
      "index": 1
    }
  ],
  "model": "voyage-4",
  "usage": {
    "total_tokens": 10
  }
}
```

Kunci API model dari Atlas berfungsi dengan `ai.mongodb.com`, kecuali kunci yang dibatasi pada suatu geografi, yang menggunakan endpoint geografi tersebut. Jika Anda memiliki kunci API dari platform Voyage AI, lihat [Migrate your applications to use the Atlas Embedding and Reranking API](https://www.mongodb.com/docs/voyageai/tutorials/migrate-to-atlas/) dalam dokumentasi MongoDB.

Untuk referensi lengkap permintaan dan respons, lihat [Create text embeddings](https://www.mongodb.com/docs/api/doc/atlas-embedding-and-reranking-api/operation/operation-createembedding) dalam dokumentasi Atlas Embedding and Reranking API.

### AWS Marketplace

Model Voyage AI juga tersedia di AWS Marketplace melalui [profil penjual MongoDB](https://aws.amazon.com/marketplace/seller-profile?id=c9032c7b-70dd-459f-834f-c1e23cf3d092). Untuk petunjuknya, lihat [Deploy Voyage AI models using AWS Marketplace](https://www.mongodb.com/docs/voyageai/management/aws-marketplace/) dalam dokumentasi MongoDB.

## Contoh quickstart

Contoh singkat berikut menunjukkan cara menggunakan embeddings.

Misalkan Anda memiliki korpus kecil berisi enam dokumen untuk di-retrieve

```python
documents = [
    "The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
    "Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
    "20th-century innovations, from radios to smartphones, centered on electronic advancements.",
    "Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
    "Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
    "Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature.",
]
```

Pertama, gunakan Voyage AI untuk mengonversi setiap dokumen menjadi vektor embedding.

```python
import voyageai

vo = voyageai.Client()

# Buat embedding untuk dokumen
doc_embds = vo.embed(documents, model="voyage-4", input_type="document").embeddings
```

Embeddings memungkinkan Anda melakukan pencarian semantik / retrieval di ruang vektor. Diberikan sebuah contoh query,

```python
query = "When is Apple's conference call scheduled?"
```

Selanjutnya, konversikan query tersebut menjadi embedding dan lakukan pencarian nearest neighbor untuk menemukan dokumen yang paling relevan berdasarkan jarak di ruang embedding.

```python
import numpy as np

# Buat embedding untuk kueri
query_embd = vo.embed([query], model="voyage-4", input_type="query").embeddings[0]

# Hitung kemiripan
# Embedding Voyage AI dinormalisasi ke panjang 1, sehingga dot-product
# dan cosine similarity bernilai sama.
similarities = np.dot(doc_embds, query_embd)

retrieved_id = np.argmax(similarities)
print(documents[retrieved_id])
```

Perhatikan bahwa `input_type="document"` dan `input_type="query"` digunakan masing-masing untuk meng-embed dokumen dan query. Untuk informasi lebih lanjut tentang `input_type`, lihat [Kapan dan bagaimana saya sebaiknya menggunakan parameter input\_type?](https://platform.claude.com/docs/id/build-with-claude/embeddings#faq) di FAQ.

Outputnya adalah dokumen kelima, yang memang paling relevan dengan query tersebut:

```text wrap
Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.
```

Jika Anda mencari kumpulan resep terperinci tentang cara melakukan RAG dengan embeddings, termasuk database vektor, lihat [resep RAG](https://platform.claude.com/cookbook/third-party-pinecone-rag-using-pinecone).

## FAQ

<AccordionGroup>
  <Accordion title="Mengapa embeddings Voyage AI memiliki kualitas yang unggul?">
    Model embedding mengandalkan jaringan saraf yang kuat untuk menangkap dan mengompresi konteks semantik, mirip dengan model generatif. Tim peneliti AI berpengalaman Voyage AI mengoptimalkan setiap komponen dari proses embedding, termasuk:

    * Arsitektur model
    * Pengumpulan data
    * Fungsi loss
    * Pemilihan optimizer

    Pelajari lebih lanjut tentang pendekatan teknis Voyage AI di [blog Voyage AI](https://blog.voyageai.com/).
  </Accordion>

  <Accordion title="Model embedding apa saja yang tersedia dan mana yang sebaiknya saya gunakan?">
    Untuk embedding serbaguna, model yang direkomendasikan adalah:

    * `voyage-4-large`: Kualitas terbaik
    * `voyage-4-lite`: Latensi dan biaya terendah
    * `voyage-4`: Performa seimbang

    Untuk retrieval, gunakan parameter `input_type` untuk menentukan apakah teks tersebut bertipe query atau dokumen.

    Model spesifik domain:

    * Tugas hukum: `voyage-law-2`
    * Retrieval kode dan agentic coding: `voyage-code-4`
    * Tugas terkait keuangan: `voyage-finance-2`

    Untuk retrieval tingkat chunk dan tingkat dokumen: `voyage-context-4`

    Untuk teks, gambar, dan video: `voyage-multimodal-3.5`
  </Accordion>

  <Accordion title="Fungsi kemiripan mana yang sebaiknya saya gunakan?">
    Anda dapat menggunakan embeddings Voyage AI dengan kemiripan dot-product, kemiripan cosine, atau jarak Euclidean. Untuk penjelasan tentang kemiripan embedding, lihat [panduan kemiripan vektor](https://www.pinecone.io/learn/vector-similarity/) ini.

    Embeddings Voyage AI dinormalisasi ke panjang 1, yang berarti bahwa:

    * Kemiripan cosine setara dengan kemiripan dot-product, sementara yang terakhir dapat dihitung lebih cepat.
    * Kemiripan cosine dan jarak Euclidean menghasilkan peringkat yang identik.
  </Accordion>

  <Accordion title="Apa hubungan antara karakter, kata, dan token?">
    Lihat [Tokenization](https://www.mongodb.com/docs/voyageai/tutorials/tokenization/) dalam dokumentasi MongoDB.
  </Accordion>

  <Accordion title="Kapan dan bagaimana saya sebaiknya menggunakan parameter input_type?">
    Untuk semua tugas dan kasus penggunaan retrieval (misalnya, RAG), gunakan parameter `input_type` untuk menentukan apakah teks input adalah query atau dokumen. Jangan menghilangkan `input_type` atau mengatur `input_type=None`. Menentukan apakah teks input adalah query atau dokumen dapat menciptakan representasi vektor padat yang lebih baik untuk retrieval, yang dapat menghasilkan kualitas retrieval yang lebih baik.

    Saat menggunakan parameter `input_type`, prompt khusus ditambahkan di awal teks input sebelum proses embedding. Secara spesifik:

    > 📘 **Prompt yang terkait dengan `input_type`**
    >
    > * Untuk query, prompt-nya adalah `"Represent the query for retrieving supporting documents: "`.
    >
    > * Untuk dokumen, prompt-nya adalah `"Represent the document for retrieval: "`.
    >
    > * Contoh
    >
    >   * Ketika `input_type="query"`, query seperti "When is Apple's conference call scheduled?" akan menjadi "**Represent the query for retrieving supporting documents:** When is Apple's conference call scheduled?"
    >   * Ketika `input_type="document"`, dokumen seperti "Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET." akan menjadi "**Represent the document for retrieval:** Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET."
  </Accordion>

  <Accordion title="Opsi kuantisasi apa saja yang tersedia?">
    "Quantization" (kuantisasi) dalam embeddings mengonversi nilai presisi tinggi, seperti bilangan floating-point presisi tunggal 32-bit, ke format presisi lebih rendah seperti bilangan bulat 8-bit atau nilai biner 1-bit, sehingga mengurangi penyimpanan, memori, dan biaya masing-masing sebesar 4x dan 32x. Model Voyage AI yang didukung memungkinkan kuantisasi dengan menentukan tipe data output menggunakan parameter `output_dtype`:

    * `float`: Setiap embedding yang dikembalikan adalah daftar bilangan floating-point presisi tunggal 32-bit (4-byte). Ini adalah default dan memberikan presisi / akurasi retrieval tertinggi.
    * `int8` dan `uint8`: Setiap embedding yang dikembalikan adalah daftar bilangan bulat 8-bit (1-byte) yang masing-masing berkisar dari -128 hingga 127 dan 0 hingga 255.
    * `binary` dan `ubinary`: Setiap embedding yang dikembalikan adalah daftar bilangan bulat 8-bit yang merepresentasikan nilai embedding bit tunggal terkuantisasi yang dikemas dalam bit (bit-packed): `int8` untuk `binary` dan `uint8` untuk `ubinary`. Panjang daftar bilangan bulat yang dikembalikan adalah 1/8 dari dimensi sebenarnya dari embedding. Tipe binary menggunakan metode offset binary, seperti yang ditunjukkan contoh berikut.

    > **Contoh kuantisasi biner**
    >
    > Pertimbangkan delapan nilai embedding berikut: -0.03955078, 0.006214142, -0.07446289, -0.039001465, 0.0046463013, 0.00030612946, -0.08496094, dan 0.03994751. Dengan kuantisasi biner, nilai yang kurang dari atau sama dengan nol akan dikuantisasi menjadi nol biner, dan nilai positif menjadi satu biner, menghasilkan urutan biner berikut: 0, 1, 0, 0, 1, 1, 0, 1. Delapan bit ini kemudian dikemas menjadi satu bilangan bulat 8-bit, 01001101 (dengan bit paling kiri sebagai bit paling signifikan).
    >
    > * `ubinary`: Urutan biner dikonversi secara langsung dan direpresentasikan sebagai bilangan bulat tak bertanda (`uint8`) 77.
    > * `binary`: Urutan biner direpresentasikan sebagai bilangan bulat bertanda (`int8`) -51, dihitung menggunakan metode offset binary (77 - 128 = -51).

    Untuk model yang mendukung setiap tipe data, lihat [Create text embeddings](https://www.mongodb.com/docs/api/doc/atlas-embedding-and-reranking-api/operation/operation-createembedding) dalam dokumentasi Atlas Embedding and Reranking API.
  </Accordion>

  <Accordion title="Bagaimana cara memotong embeddings Matryoshka?">
    Pembelajaran Matryoshka menciptakan embeddings dengan representasi dari kasar ke halus dalam satu vektor. Model Voyage AI yang mendukung beberapa dimensi output, seperti `voyage-code-4`, menghasilkan embeddings Matryoshka tersebut. Untuk mendapatkan vektor yang lebih pendek dari API, berikan `output_dimension` (misalnya, `output_dimension=256`). Untuk memperpendek vektor yang sudah Anda simpan, potong vektor tersebut dengan mempertahankan subset dimensi terdepan, lalu normalisasikan kembali. Misalnya, kode Python berikut menunjukkan cara memotong vektor 1024 dimensi menjadi 256 dimensi:

    ```python
    import voyageai
    import numpy as np


    def embd_normalize(v: np.ndarray) -> np.ndarray:
        """
        Normalize the rows of a 2D numpy array to unit vectors by dividing each row by its Euclidean
        norm. Raises a ValueError if any row has a norm of zero to prevent division by zero.
        """
        row_norms = np.linalg.norm(v, axis=1, keepdims=True)
        if np.any(row_norms == 0):
            raise ValueError("Cannot normalize rows with a norm of zero.")
        return v / row_norms


    vo = voyageai.Client()

    # Hasilkan vektor voyage-code-4, yang secara default berupa bilangan floating-point 1024 dimensi
    embd = vo.embed(["Sample text 1", "Sample text 2"], model="voyage-code-4").embeddings

    # Tetapkan dimensi yang lebih pendek
    short_dim = 256

    # Ubah ukuran dan normalisasi vektor ke dimensi yang lebih pendek
    resized_embd = embd_normalize(np.array(embd)[:, :short_dim]).tolist()
    ```
  </Accordion>
</AccordionGroup>

## Harga

Untuk detail harga terbaru, lihat [Model pricing](https://www.mongodb.com/docs/voyageai/management/billing/#model-pricing) dalam dokumentasi MongoDB.
