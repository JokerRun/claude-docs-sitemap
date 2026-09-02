---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/embeddings
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: f9a0da0c832760a7252f02b348602d17efbe5613dbf2afdd640c00c46f583a81
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

Anthropic tidak menawarkan model embedding sendiri. Salah satu penyedia embeddings yang memiliki beragam opsi dan kemampuan yang mencakup semua pertimbangan di atas adalah Voyage AI.

Voyage AI membuat model embedding mutakhir dan menawarkan model yang dikustomisasi untuk domain industri tertentu seperti keuangan dan kesehatan, atau model "fine-tuned" (disetel halus) yang dibuat khusus untuk pelanggan individual.

Sisa panduan ini ditujukan untuk Voyage AI, tetapi Anda sebaiknya menilai berbagai vendor embeddings untuk menemukan yang paling sesuai dengan kasus penggunaan spesifik Anda.

## Model yang tersedia

Voyage merekomendasikan penggunaan model text embedding berikut:

**Voyage 4 (generasi terbaru)**

| Model            | Panjang konteks | Dimensi embedding              | Deskripsi                                                                                                                                                                                                |
| ---------------- | --------------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voyage-4-large` | 32.000          | 1024 (default), 256, 512, 2048 | Kualitas retrieval serbaguna dan multibahasa terbaik. Lihat [postingan blog Voyage 4](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya.                                                   |
| `voyage-4`       | 32.000          | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk kualitas retrieval serbaguna dan multibahasa. Menyeimbangkan kualitas dan efisiensi. Lihat [postingan blog Voyage 4](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya. |
| `voyage-4-lite`  | 32.000          | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk latensi dan biaya. Lihat [postingan blog Voyage 4](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya.                                                                   |
| `voyage-4-nano`  | 32.000          | 1024 (default), 256, 512, 2048 | Model open-weight (lisensi Apache 2.0) yang tersedia di Hugging Face. Lihat [postingan blog Voyage 4](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya.                                   |

**Generasi sebelumnya**

| Model              | Panjang konteks | Dimensi embedding              | Deskripsi                                                                                                                                                                                                                                                                           |
| ------------------ | --------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voyage-3-large`   | 32.000          | 1024 (default), 256, 512, 2048 | Kualitas retrieval serbaguna dan multibahasa terbaik. Lihat [postingan blog voyage-3-large](https://blog.voyageai.com/2025/01/07/voyage-3-large/) untuk detailnya.                                                                                                                  |
| `voyage-3.5`       | 32.000          | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk kualitas retrieval serbaguna dan multibahasa. Lihat [postingan blog voyage-3.5](https://blog.voyageai.com/2025/05/20/voyage-3-5/) untuk detailnya.                                                                                                               |
| `voyage-3.5-lite`  | 32.000          | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk latensi dan biaya. Lihat [postingan blog voyage-3.5](https://blog.voyageai.com/2025/05/20/voyage-3-5/) untuk detailnya.                                                                                                                                          |
| `voyage-code-3`    | 32.000          | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk retrieval **kode**. Lihat [postingan blog voyage-code-3](https://blog.voyageai.com/2024/12/04/voyage-code-3/) untuk detailnya.                                                                                                                                   |
| `voyage-finance-2` | 32.000          | 1024                           | Dioptimalkan untuk retrieval dan RAG **keuangan**. Lihat [postingan blog voyage-finance-2](https://blog.voyageai.com/2024/06/03/domain-specific-embeddings-finance-edition-voyage-finance-2/) untuk detailnya.                                                                      |
| `voyage-law-2`     | 16.000          | 1024                           | Dioptimalkan untuk retrieval dan RAG **hukum** dan **konteks panjang**. Juga meningkatkan performa di semua domain. Lihat [postingan blog voyage-law-2](https://blog.voyageai.com/2024/04/15/domain-specific-embeddings-and-retrieval-legal-edition-voyage-law-2/) untuk detailnya. |

Selain itu, Voyage merekomendasikan model embedding multimodal berikut:

| Model                   | Panjang konteks | Dimensi embedding              | Deskripsi                                                                                                                                                                                                                                                                                                                          |
| ----------------------- | --------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voyage-multimodal-3.5` | 32.000          | 1024 (default), 256, 512, 2048 | Model embedding multimodal yang kaya yang dapat memvektorisasi teks, gambar, dan video yang saling berselang-seling. Menyertakan dukungan video sebagai model embedding video tingkat produksi pertama. Lihat [postingan blog voyage-multimodal-3.5](https://blog.voyageai.com/2026/01/15/voyage-multimodal-3-5/) untuk detailnya. |
| `voyage-multimodal-3`   | 32.000          | 1024                           | Model embedding multimodal yang kaya yang dapat memvektorisasi teks yang berselang-seling dengan gambar yang kaya konten, seperti tangkapan layar PDF, slide, tabel, gambar, dan lainnya. Lihat [postingan blog voyage-multimodal-3](https://blog.voyageai.com/2024/11/12/voyage-multimodal-3/) untuk detailnya.                   |

Model contextualized chunk embedding berikut menghasilkan vektor tingkat chunk yang menangkap konteks dokumen secara penuh tanpa augmentasi metadata manual. Panggil model-model ini dengan `contextualized_embed()` alih-alih `embed()`:

| Model              | Panjang konteks | Dimensi embedding              | Deskripsi                                                                                                                                                                                                              |
| ------------------ | --------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voyage-context-4` | 120.000         | 1024 (default), 256, 512, 2048 | Contextualized chunk embeddings yang dioptimalkan untuk kualitas retrieval serbaguna dan multibahasa. Lihat [postingan blog voyage-context-4](https://blog.voyageai.com/2026/06/29/voyage-context-4/) untuk detailnya. |
| `voyage-context-3` | 120.000         | 1024 (default), 256, 512, 2048 | Contextualized chunk embeddings yang dioptimalkan untuk kualitas retrieval serbaguna dan multibahasa. Lihat [postingan blog voyage-context-3](https://blog.voyageai.com/2025/07/23/voyage-context-3/) untuk detailnya. |

Voyage AI juga menawarkan reranker, yang menerima sebuah query dan daftar dokumen lalu mengembalikannya dalam urutan berdasarkan relevansi terhadap query tersebut. Panggil model-model ini dengan `rerank()`:

| Model             | Panjang konteks | Deskripsi                                                                                                                                                               |
| ----------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rerank-2.5`      | 32.000          | Akurasi tertinggi. Direkomendasikan untuk sebagian besar aplikasi. Lihat [postingan blog rerank-2.5](https://blog.voyageai.com/2025/08/11/rerank-2-5/) untuk detailnya. |
| `rerank-2.5-lite` | 32.000          | Dioptimalkan untuk latensi dan biaya. Lihat [postingan blog rerank-2.5](https://blog.voyageai.com/2025/08/11/rerank-2-5/) untuk detailnya.                              |

Butuh bantuan untuk memutuskan model text embedding mana yang akan digunakan? Lihat [FAQ Voyage AI](https://docs.voyageai.com/docs/faq#what-embedding-models-are-available-and-which-one-should-i-use\&ref=anthropic).

## Memulai dengan Voyage AI

Untuk mengakses embeddings Voyage:

1. Daftar di situs web Voyage AI.
2. Dapatkan "API key" (kunci API).
3. Atur kunci API sebagai variabel lingkungan untuk kemudahan:

```bash
export VOYAGE_API_KEY="<your secret key>"
```

Anda dapat memperoleh embeddings dengan menggunakan [paket Python `voyageai`](https://github.com/voyage-ai/voyageai-python) resmi atau permintaan HTTP, seperti yang dijelaskan di bagian-bagian berikut.

### Library Python Voyage

Instal paket `voyageai` menggunakan perintah berikut:

```bash
pip install -U voyageai
```

Kemudian, Anda dapat membuat objek client dan mulai menggunakannya untuk meng-embed teks Anda:

```python
import voyageai

vo = voyageai.Client()
# Ini akan secara otomatis menggunakan variabel lingkungan VOYAGE_API_KEY.
# Sebagai alternatif, Anda dapat menggunakan vo = voyageai.Client(api_key="<kunci rahasia Anda>")

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

Untuk informasi lebih lanjut tentang paket Python Voyage, lihat [dokumentasi paket Python Voyage](https://docs.voyageai.com/docs/embeddings#python-api).

### HTTP API Voyage

Anda juga dapat memperoleh embeddings dengan mengirim permintaan ke HTTP API Voyage. Misalnya, Anda dapat mengirim permintaan HTTP melalui perintah `curl` di terminal:

```bash cURL
curl https://api.voyageai.com/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VOYAGE_API_KEY" \
  -d '{
    "input": ["Sample text 1", "Sample text 2"],
    "model": "voyage-4"
  }'
```

Respons yang akan Anda dapatkan adalah objek JSON yang berisi embeddings dan penggunaan token:

```json
{
  "object": "list",
  "data": [
    {
      "embedding": [-0.013131560757756233, 0.019828535616397858 /* ... */],
      "index": 0
    },
    {
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

Untuk informasi lebih lanjut tentang HTTP API Voyage, lihat [dokumentasi HTTP API Voyage](https://docs.voyageai.com/reference/embeddings-api).

### AWS Marketplace

Embeddings Voyage tersedia di [AWS Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=c9032c7b-70dd-459f-834f-c1e23cf3d092). Petunjuk untuk mengakses Voyage di AWS tersedia di [dokumentasi AWS Marketplace Voyage](https://docs.voyageai.com/docs/aws-marketplace-mongodb-voyage?ref=anthropic).

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

Pertama, gunakan Voyage untuk mengonversi setiap dokumen menjadi vektor embedding.

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

# Hitung kemiripannya
# Embedding Voyage dinormalisasi ke panjang 1, sehingga dot-product
# dan cosine similarity bernilai sama.
similarities = np.dot(doc_embds, query_embd)

retrieved_id = np.argmax(similarities)
print(documents[retrieved_id])
```

Perhatikan bahwa `input_type="document"` dan `input_type="query"` digunakan untuk meng-embed dokumen dan query, secara berurutan. Spesifikasi lebih lanjut dapat ditemukan di [library Python Voyage](https://platform.claude.com/docs/id/build-with-claude/embeddings#voyage-python-library).

Outputnya adalah dokumen kelima, yang memang paling relevan dengan query tersebut:

```text wrap
Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.
```

Jika Anda mencari kumpulan resep terperinci tentang cara melakukan RAG dengan embeddings, termasuk database vektor, lihat [resep RAG](https://platform.claude.com/cookbook/third-party-pinecone-rag-using-pinecone).

## FAQ

<AccordionGroup>
  <Accordion title="Mengapa embeddings Voyage memiliki kualitas yang unggul?">
    Model embedding mengandalkan jaringan neural yang kuat untuk menangkap dan mengompresi konteks semantik, mirip dengan model generatif. Tim peneliti AI berpengalaman Voyage mengoptimalkan setiap komponen proses embedding, termasuk:

    * Arsitektur model
    * Pengumpulan data
    * Fungsi loss
    * Pemilihan optimizer

    Pelajari lebih lanjut tentang pendekatan teknis Voyage di [blog Voyage AI](https://blog.voyageai.com/).
  </Accordion>

  <Accordion title="Model embedding apa saja yang tersedia dan mana yang sebaiknya saya gunakan?">
    Untuk embedding serbaguna, model yang direkomendasikan adalah:

    * `voyage-4-large`: Kualitas terbaik
    * `voyage-4-lite`: Latensi dan biaya terendah
    * `voyage-4`: Performa seimbang

    Untuk retrieval, gunakan parameter `input_type` untuk menentukan apakah teks tersebut bertipe query atau dokumen.

    Model spesifik domain:

    * Tugas hukum: `voyage-law-2`
    * Kode dan dokumentasi pemrograman: `voyage-code-3`
    * Tugas terkait keuangan: `voyage-finance-2`

    Untuk retrieval tingkat chunk dan tingkat dokumen: `voyage-context-4`
  </Accordion>

  <Accordion title="Fungsi kemiripan mana yang sebaiknya saya gunakan?">
    Anda dapat menggunakan embeddings Voyage dengan kemiripan dot-product, kemiripan cosine, atau jarak Euclidean. Untuk penjelasan tentang kemiripan embedding, lihat [panduan kemiripan vektor](https://www.pinecone.io/learn/vector-similarity/) ini.

    Embeddings Voyage AI dinormalisasi ke panjang 1, yang berarti bahwa:

    * Kemiripan cosine setara dengan kemiripan dot-product, sementara yang terakhir dapat dihitung lebih cepat.
    * Kemiripan cosine dan jarak Euclidean menghasilkan peringkat yang identik.
  </Accordion>

  <Accordion title="Apa hubungan antara karakter, kata, dan token?">
    Lihat [panduan tokenisasi Voyage](https://docs.voyageai.com/docs/tokenization?ref=anthropic).
  </Accordion>

  <Accordion title="Kapan dan bagaimana saya sebaiknya menggunakan parameter input_type?">
    Untuk semua tugas dan kasus penggunaan retrieval (misalnya, RAG), gunakan parameter `input_type` untuk menentukan apakah teks input adalah query atau dokumen. Jangan menghilangkan `input_type` atau mengatur `input_type=None`. Menentukan apakah teks input adalah query atau dokumen dapat menciptakan representasi vektor padat yang lebih baik untuk retrieval, yang dapat menghasilkan kualitas retrieval yang lebih baik.

    Saat menggunakan parameter `input_type`, prompt khusus ditambahkan di awal teks input sebelum proses embedding. Secara spesifik:

    > 📘 **Prompt yang terkait dengan `input_type`**
    >
    > * Untuk query, prompt-nya adalah “Represent the query for retrieving supporting documents: “.
    >
    > * Untuk dokumen, prompt-nya adalah “Represent the document for retrieval: “.
    >
    > * Contoh
    >
    >   * Ketika `input_type="query"`, query seperti "When is Apple's conference call scheduled?" akan menjadi "**Represent the query for retrieving supporting documents:** When is Apple's conference call scheduled?"
    >   * Ketika `input_type="document"`, query seperti "Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET." akan menjadi "**Represent the document for retrieval:** Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET."

    `voyage-large-2-instruct`, seperti namanya, dilatih agar responsif terhadap instruksi tambahan yang ditambahkan di awal teks input. Untuk klasifikasi, clustering, atau subtugas [MTEB](https://huggingface.co/mteb) lainnya, gunakan [instruksi voyage-large-2-instruct](https://github.com/voyage-ai/voyage-large-2-instruct).
  </Accordion>

  <Accordion title="Opsi kuantisasi apa saja yang tersedia?">
    Kuantisasi pada embeddings mengonversi nilai presisi tinggi, seperti bilangan floating-point presisi tunggal 32-bit, ke format presisi lebih rendah seperti integer 8-bit atau nilai biner 1-bit, sehingga mengurangi penyimpanan, memori, dan biaya sebesar 4x dan 32x, secara berurutan. Model Voyage yang didukung memungkinkan kuantisasi dengan menentukan tipe data output menggunakan parameter `output_dtype`:

    * `float`: Setiap embedding yang dikembalikan adalah daftar bilangan floating-point presisi tunggal 32-bit (4-byte). Ini adalah default dan memberikan presisi / akurasi retrieval tertinggi.
    * `int8` dan `uint8`: Setiap embedding yang dikembalikan adalah daftar integer 8-bit (1-byte) dengan rentang dari -128 hingga 127 dan 0 hingga 255, secara berurutan.
    * `binary` dan `ubinary`: Setiap embedding yang dikembalikan adalah daftar integer 8-bit yang merepresentasikan nilai embedding bit tunggal terkuantisasi yang dikemas dalam bit: `int8` untuk `binary` dan `uint8` untuk `ubinary`. Panjang daftar integer yang dikembalikan adalah 1/8 dari dimensi embedding yang sebenarnya. Tipe binary menggunakan metode offset binary, yang dapat Anda pelajari lebih lanjut di [FAQ embeddings](https://platform.claude.com/docs/id/build-with-claude/embeddings#faq).

    > **Contoh kuantisasi biner**
    >
    > Pertimbangkan delapan nilai embedding berikut: -0.03955078, 0.006214142, -0.07446289, -0.039001465, 0.0046463013, 0.00030612946, -0.08496094, dan 0.03994751. Dengan kuantisasi biner, nilai yang kurang dari atau sama dengan nol akan dikuantisasi menjadi nol biner, dan nilai positif menjadi satu biner, sehingga menghasilkan urutan biner berikut: 0, 1, 0, 0, 1, 1, 0, 1. Kedelapan bit ini kemudian dikemas menjadi satu integer 8-bit, 01001101 (dengan bit paling kiri sebagai bit paling signifikan).
    >
    > * `ubinary`: Urutan biner tersebut langsung dikonversi dan direpresentasikan sebagai unsigned integer (`uint8`) 77.
    > * `binary`: Urutan biner tersebut direpresentasikan sebagai signed integer (`int8`) -51, yang dihitung menggunakan metode offset binary (77 - 128 = -51).
  </Accordion>

  <Accordion title="Bagaimana cara memotong embeddings Matryoshka?">
    Matryoshka learning menciptakan embeddings dengan representasi kasar-ke-halus dalam satu vektor. Model Voyage, seperti `voyage-code-3`, yang mendukung beberapa dimensi output menghasilkan embeddings Matryoshka semacam ini. Anda dapat memotong vektor-vektor ini dengan mempertahankan subset dimensi terdepan. Misalnya, kode Python berikut menunjukkan cara memotong vektor 1024 dimensi menjadi 256 dimensi:

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

    # Hasilkan vektor voyage-code-3, yang secara default berupa bilangan floating-point berdimensi 1024
    embd = vo.embed(["Sample text 1", "Sample text 2"], model="voyage-code-3").embeddings

    # Tetapkan dimensi yang lebih pendek
    short_dim = 256

    # Ubah ukuran dan normalisasi vektor ke dimensi yang lebih pendek
    resized_embd = embd_normalize(np.array(embd)[:, :short_dim]).tolist()
    ```
  </Accordion>
</AccordionGroup>

## Harga

Kunjungi [halaman harga](https://docs.voyageai.com/docs/pricing?ref=anthropic) Voyage untuk detail harga terbaru.
