---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/embeddings
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: a9e9b3b9b52593ffb90b9c7945cbc5a1c7d71e6d803c0d72a5f3930a846ce2a2
---

# Embeddings

Embeddings teks adalah representasi numerik dari teks yang memungkinkan pengukuran kesamaan semantik. Panduan ini memperkenalkan embeddings, aplikasinya, dan cara menggunakan model embedding untuk tugas-tugas seperti pencarian, rekomendasi, dan deteksi anomali.

---

## Sebelum mengimplementasikan embeddings

Saat memilih penyedia embeddings, ada beberapa faktor yang dapat Anda pertimbangkan tergantung pada kebutuhan dan preferensi Anda:

- Ukuran dataset & spesifisitas domain: ukuran dataset pelatihan model dan relevansinya dengan domain yang ingin Anda embed. Data yang lebih besar atau lebih spesifik domain umumnya menghasilkan embeddings dalam domain yang lebih baik
- Kinerja inferensi: kecepatan pencarian embedding dan latensi end-to-end. Ini adalah pertimbangan yang sangat penting untuk penyebaran produksi skala besar
- Kustomisasi: opsi untuk pelatihan lanjutan pada data pribadi, atau spesialisasi model untuk domain yang sangat spesifik. Ini dapat meningkatkan kinerja pada kosakata unik

## Cara mendapatkan embeddings dengan Anthropic

Anthropic tidak menawarkan model embedding miliknya sendiri. Salah satu penyedia embeddings yang memiliki berbagai pilihan dan kemampuan yang mencakup semua pertimbangan di atas adalah Voyage AI.

Voyage AI membuat model embedding canggih dan menawarkan model yang disesuaikan untuk domain industri tertentu seperti keuangan dan kesehatan, atau model yang disesuaikan dengan baik untuk pelanggan individual.

Sisa panduan ini adalah untuk Voyage AI, tetapi kami mendorong Anda untuk mengevaluasi berbagai vendor embeddings untuk menemukan yang paling sesuai dengan kasus penggunaan spesifik Anda.

## Model yang Tersedia

Voyage merekomendasikan penggunaan model embedding teks berikut:

| Model | Panjang Konteks | Dimensi Embedding | Deskripsi |
| --- | --- | --- | --- |
| `voyage-3-large` | 32.000 | 1024 (default), 256, 512, 2048 | Kualitas pengambilan tujuan umum dan multibahasa terbaik. Lihat [blog post](https://blog.voyageai.com/2025/01/07/voyage-3-large/) untuk detail. |
| `voyage-3.5` | 32.000 | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk kualitas pengambilan tujuan umum dan multibahasa. Lihat [blog post](https://blog.voyageai.com/2025/05/20/voyage-3-5/) untuk detail. |
| `voyage-3.5-lite` | 32.000 | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk latensi dan biaya. Lihat [blog post](https://blog.voyageai.com/2025/05/20/voyage-3-5/) untuk detail. |
| `voyage-code-3` | 32.000 | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk pengambilan **kode**. Lihat [blog post](https://blog.voyageai.com/2024/12/04/voyage-code-3/) untuk detail. |
| `voyage-finance-2` | 32.000 | 1024 | Dioptimalkan untuk pengambilan dan RAG **keuangan**. Lihat [blog post](https://blog.voyageai.com/2024/06/03/domain-specific-embeddings-finance-edition-voyage-finance-2/) untuk detail. |
| `voyage-law-2` | 16.000 | 1024 | Dioptimalkan untuk pengambilan dan RAG **hukum** dan **konteks panjang**. Juga meningkatkan kinerja di semua domain. Lihat [blog post](https://blog.voyageai.com/2024/04/15/domain-specific-embeddings-and-retrieval-legal-edition-voyage-law-2/) untuk detail. |

Selain itu, model embedding multimodal berikut direkomendasikan:

| Model | Panjang Konteks | Dimensi Embedding | Deskripsi |
| --- | --- | --- | --- |
| `voyage-multimodal-3` | 32000 | 1024 | Model embedding multimodal kaya yang dapat memvektorisasi teks yang disisipi dan gambar yang kaya konten, seperti tangkapan layar PDF, slide, tabel, gambar, dan lainnya. Lihat [blog post](https://blog.voyageai.com/2024/11/12/voyage-multimodal-3/) untuk detail. |

Butuh bantuan memutuskan model embedding teks mana yang akan digunakan? Lihat [FAQ](https://docs.voyageai.com/docs/faq#what-embedding-models-are-available-and-which-one-should-i-use&ref=anthropic).

## Memulai dengan Voyage AI

Untuk mengakses embeddings Voyage:

1. Daftar di situs web Voyage AI
2. Dapatkan kunci API
3. Atur kunci API sebagai variabel lingkungan untuk kenyamanan:

```bash
export VOYAGE_API_KEY="<your secret key>"
```

Anda dapat memperoleh embeddings dengan menggunakan paket Python [`voyageai`](https://github.com/voyage-ai/voyageai-python) resmi atau permintaan HTTP, seperti yang dijelaskan di bawah.

### Perpustakaan Python Voyage

Paket `voyageai` dapat diinstal menggunakan perintah berikut:

```bash
pip install -U voyageai
```

Kemudian, Anda dapat membuat objek klien dan mulai menggunakannya untuk embed teks Anda:

```python
import voyageai

vo = voyageai.Client()
# This will automatically use the environment variable VOYAGE_API_KEY.
# Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")

texts = ["Sample text 1", "Sample text 2"]

result = vo.embed(texts, model="voyage-3.5", input_type="document")
print(result.embeddings[0])
print(result.embeddings[1])
```

`result.embeddings` akan menjadi daftar dua vektor embedding, masing-masing berisi 1024 angka floating-point. Setelah menjalankan kode di atas, dua embeddings akan dicetak di layar:

```
[-0.013131560757756233, 0.019828535616397858, ...]   # embedding for "Sample text 1"
[-0.0069352793507277966, 0.020878976210951805, ...]  # embedding for "Sample text 2"
```

Saat membuat embeddings, Anda dapat menentukan beberapa argumen lain ke fungsi `embed()`.

Untuk informasi lebih lanjut tentang paket python Voyage, lihat [dokumentasi Voyage](https://docs.voyageai.com/docs/embeddings#python-api).

### API HTTP Voyage

Anda juga dapat memperoleh embeddings dengan meminta API HTTP Voyage. Misalnya, Anda dapat mengirim permintaan HTTP melalui perintah `curl` di terminal:

```bash
curl https://api.voyageai.com/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VOYAGE_API_KEY" \
  -d '{
    "input": ["Sample text 1", "Sample text 2"],
    "model": "voyage-3.5"
  }'
```

Respons yang akan Anda dapatkan adalah objek JSON yang berisi embeddings dan penggunaan token:

```json
{
  "object": "list",
  "data": [
    {
      "embedding": [-0.013131560757756233, 0.019828535616397858, ...],
      "index": 0
    },
    {
      "embedding": [-0.0069352793507277966, 0.020878976210951805, ...],
      "index": 1
    }
  ],
  "model": "voyage-3.5",
  "usage": {
    "total_tokens": 10
  }
}

```

Untuk informasi lebih lanjut tentang API HTTP Voyage, lihat [dokumentasi Voyage](https://docs.voyageai.com/reference/embeddings-api).

### AWS Marketplace

Embeddings Voyage tersedia di [AWS Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=seller-snt4gb6fd7ljg). Instruksi untuk mengakses Voyage di AWS tersedia [di sini](https://docs.voyageai.com/docs/aws-marketplace-model-package?ref=anthropic).

## Contoh Quickstart

Sekarang kita tahu cara mendapatkan embeddings, mari kita lihat contoh singkat.

Misalkan kita memiliki corpus kecil enam dokumen untuk diambil dari

```python
documents = [
    "The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
    "Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
    "20th-century innovations, from radios to smartphones, centered on electronic advancements.",
    "Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
    "Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
    "Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature."
]

```

Kami akan terlebih dahulu menggunakan Voyage untuk mengonversi masing-masing menjadi vektor embedding

```python
import voyageai

vo = voyageai.Client()

# Embed the documents
doc_embds = vo.embed(
    documents, model="voyage-3.5", input_type="document"
).embeddings
```

Embeddings akan memungkinkan kami melakukan pencarian semantik / pengambilan dalam ruang vektor. Diberikan contoh kueri,

```python
query = "When is Apple's conference call scheduled?"
```

kami mengonversinya menjadi embedding, dan melakukan pencarian tetangga terdekat untuk menemukan dokumen paling relevan berdasarkan jarak dalam ruang embedding.

```python
import numpy as np

# Embed the query
query_embd = vo.embed(
    [query], model="voyage-3.5", input_type="query"
).embeddings[0]

# Compute the similarity
# Voyage embeddings are normalized to length 1, therefore dot-product
# and cosine similarity are the same.
similarities = np.dot(doc_embds, query_embd)

retrieved_id = np.argmax(similarities)
print(documents[retrieved_id])
```

Perhatikan bahwa kami menggunakan `input_type="document"` dan `input_type="query"` untuk embedding dokumen dan kueri, masing-masing. Spesifikasi lebih lanjut dapat ditemukan [di sini](/docs/id/build-with-claude/embeddings#voyage-python-package).

Hasilnya akan menjadi dokumen ke-5, yang memang paling relevan dengan kueri:

```
Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.
```

Jika Anda mencari serangkaian cookbook terperinci tentang cara melakukan RAG dengan embeddings, termasuk database vektor, lihat [cookbook RAG](https://platform.claude.com/cookbook/third-party-pinecone-rag-using-pinecone) kami.

## FAQ

  <section title="Mengapa embeddings Voyage memiliki kualitas superior?">

    Model embedding mengandalkan jaringan saraf yang kuat untuk menangkap dan mengompresi konteks semantik, mirip dengan model generatif. Tim peneliti AI berpengalaman Voyage mengoptimalkan setiap komponen proses embedding, termasuk:
    - Arsitektur model 
    - Pengumpulan data
    - Fungsi loss
    - Pemilihan optimizer

    Pelajari lebih lanjut tentang pendekatan teknis Voyage di [blog](https://blog.voyageai.com/) mereka.
  
</section>

  <section title="Model embedding apa yang tersedia dan mana yang harus saya gunakan?">

    Untuk embedding tujuan umum, kami merekomendasikan:
    - `voyage-3-large`: Kualitas terbaik
    - `voyage-3.5-lite`: Latensi dan biaya terendah
    - `voyage-3.5`: Kinerja seimbang dengan kualitas pengambilan superior dengan harga kompetitif 
    
    Untuk pengambilan, gunakan parameter `input_type` untuk menentukan apakah teks adalah tipe kueri atau dokumen.

    Model khusus domain:

    - Tugas hukum: `voyage-law-2`
    - Dokumentasi kode dan pemrograman: `voyage-code-3`
    - Tugas terkait keuangan: `voyage-finance-2`
  
</section>

  <section title="Fungsi kesamaan mana yang harus saya gunakan?">

    Anda dapat menggunakan embeddings Voyage dengan kesamaan dot-product, kesamaan cosine, atau jarak Euclidean. Penjelasan tentang kesamaan embedding dapat ditemukan [di sini](https://www.pinecone.io/learn/vector-similarity/).

    Embeddings Voyage AI dinormalisasi ke panjang 1, yang berarti:

    - Kesamaan cosine setara dengan kesamaan dot-product, sedangkan yang terakhir dapat dihitung lebih cepat.
    - Kesamaan cosine dan jarak Euclidean akan menghasilkan peringkat yang identik.
  
</section>

  <section title="Apa hubungan antara karakter, kata, dan token?">

    Silakan lihat [halaman](https://docs.voyageai.com/docs/tokenization?ref=anthropic) ini.
  
</section>

  <section title="Kapan dan bagaimana saya harus menggunakan parameter input_type?">

    Untuk semua tugas pengambilan dan kasus penggunaan (misalnya, RAG), kami merekomendasikan bahwa parameter `input_type` digunakan untuk menentukan apakah teks input adalah kueri atau dokumen. Jangan lewatkan `input_type` atau atur `input_type=None`. Menentukan apakah teks input adalah kueri atau dokumen dapat membuat representasi vektor padat yang lebih baik untuk pengambilan, yang dapat menyebabkan kualitas pengambilan yang lebih baik.

    Saat menggunakan parameter `input_type`, prompt khusus ditambahkan di depan teks input sebelum embedding. Secara khusus:

    > 📘 **Prompt yang terkait dengan `input_type`**
    > 
    > - Untuk kueri, prompt adalah "Represent the query for retrieving supporting documents: ".
    > - Untuk dokumen, prompt adalah "Represent the document for retrieval: ".
    > - Contoh
    >     - Ketika `input_type="query"`, kueri seperti "When is Apple's conference call scheduled?" akan menjadi "**Represent the query for retrieving supporting documents:** When is Apple's conference call scheduled?"
    >     - Ketika `input_type="document"`, kueri seperti "Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET." akan menjadi "**Represent the document for retrieval:** Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET."

    `voyage-large-2-instruct`, seperti namanya, dilatih untuk responsif terhadap instruksi tambahan yang ditambahkan di depan teks input. Untuk klasifikasi, clustering, atau subtask [MTEB](https://huggingface.co/mteb) lainnya, silakan gunakan instruksi [di sini](https://github.com/voyage-ai/voyage-large-2-instruct).
  
</section>

  <section title="Opsi kuantisasi apa yang tersedia?">

    Kuantisasi dalam embeddings mengonversi nilai presisi tinggi, seperti angka floating-point presisi tunggal 32-bit, ke format presisi lebih rendah seperti bilangan bulat 8-bit atau nilai biner 1-bit, mengurangi penyimpanan, memori, dan biaya sebesar 4x dan 32x, masing-masing. Model Voyage yang didukung memungkinkan kuantisasi dengan menentukan tipe data output dengan parameter `output_dtype`:

    - `float`: Setiap embedding yang dikembalikan adalah daftar angka floating-point presisi tunggal 32-bit (4-byte). Ini adalah default dan memberikan presisi tertinggi / akurasi pengambilan.
    - `int8` dan `uint8`: Setiap embedding yang dikembalikan adalah daftar bilangan bulat 8-bit (1-byte) berkisar dari -128 hingga 127 dan 0 hingga 255, masing-masing.
    - `binary` dan `ubinary`: Setiap embedding yang dikembalikan adalah daftar bilangan bulat 8-bit yang mewakili nilai embedding kuantisasi bit-packed, single-bit: `int8` untuk `binary` dan `uint8` untuk `ubinary`. Panjang daftar bilangan bulat yang dikembalikan adalah 1/8 dari dimensi sebenarnya dari embedding. Tipe biner menggunakan metode offset biner, yang dapat Anda pelajari lebih lanjut di FAQ di bawah.

    > **Contoh kuantisasi biner**
    > 
    > Pertimbangkan delapan nilai embedding berikut: -0.03955078, 0.006214142, -0.07446289, -0.039001465, 0.0046463013, 0.00030612946, -0.08496094, dan 0.03994751. Dengan kuantisasi biner, nilai kurang dari atau sama dengan nol akan dikuantisasi ke nol biner, dan nilai positif ke satu biner, menghasilkan urutan biner berikut: 0, 1, 0, 0, 1, 1, 0, 1. Delapan bit ini kemudian dikemas menjadi satu bilangan bulat 8-bit, 01001101 (dengan bit paling kiri sebagai bit paling signifikan).
    >   - `ubinary`: Urutan biner langsung dikonversi dan direpresentasikan sebagai bilangan bulat unsigned (`uint8`) 77.
    >   - `binary`: Urutan biner direpresentasikan sebagai bilangan bulat signed (`int8`) -51, dihitung menggunakan metode offset biner (77 - 128 = -51).
  
</section>

  <section title="Bagaimana cara memotong embeddings Matryoshka?">

    Pembelajaran Matryoshka membuat embeddings dengan representasi kasar-ke-halus dalam satu vektor. Model Voyage, seperti `voyage-code-3`, yang mendukung dimensi output ganda menghasilkan embeddings Matryoshka tersebut. Anda dapat memotong vektor ini dengan menyimpan subset dimensi terdepan. Misalnya, kode Python berikut menunjukkan cara memotong vektor 1024-dimensi menjadi 256 dimensi:

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

    # Generate voyage-code-3 vectors, which by default are 1024-dimensional floating-point numbers
    embd = vo.embed(['Sample text 1', 'Sample text 2'], model='voyage-code-3').embeddings

    # Set shorter dimension
    short_dim = 256

    # Resize and normalize vectors to shorter dimension
    resized_embd = embd_normalize(np.array(embd)[:, :short_dim]).tolist()
    ```
  
</section>

## Harga

Kunjungi [halaman harga](https://docs.voyageai.com/docs/pricing?ref=anthropic) Voyage untuk detail harga paling terkini.