---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/embeddings
fetched_at: 2026-06-11T03:14:59.596724Z
sha256: 9acfad8d45cc084e4ea4461e2f5acf737d42f264321a34934796708e83fd0a89
---

# Embeddings

Text embeddings adalah representasi numerik dari teks yang memungkinkan pengukuran kemiripan semantik. Panduan ini memperkenalkan embeddings, aplikasinya, dan cara menggunakan model embedding untuk tugas seperti pencarian, rekomendasi, dan deteksi anomali.

---

## Sebelum mengimplementasikan embeddings \{#before-implementing-embeddings}

Saat memilih penyedia embeddings, ada beberapa faktor yang dapat Anda pertimbangkan tergantung pada kebutuhan dan preferensi Anda:

- Ukuran dataset & spesifisitas domain: ukuran dataset pelatihan model dan relevansinya dengan domain yang ingin Anda embed. Data yang lebih besar atau lebih spesifik domain umumnya menghasilkan embeddings dalam-domain yang lebih baik
- Performa inferensi: kecepatan pencarian embedding dan "latency" (latensi) end-to-end. Ini adalah pertimbangan yang sangat penting untuk deployment produksi skala besar
- Kustomisasi: opsi untuk pelatihan lanjutan pada data privat, atau spesialisasi model untuk domain yang sangat spesifik. Ini dapat meningkatkan performa pada kosakata yang unik

## Cara mendapatkan embeddings dengan Anthropic \{#how-to-get-embeddings-with-anthropic}

Anthropic tidak menawarkan model embedding sendiri. Salah satu penyedia embeddings yang memiliki beragam opsi dan kemampuan yang mencakup semua pertimbangan di atas adalah Voyage AI.

Voyage AI membuat model embedding mutakhir dan menawarkan model yang dikustomisasi untuk domain industri tertentu seperti keuangan dan kesehatan, atau model yang di-fine-tune secara khusus untuk pelanggan individu.

Sisa panduan ini ditujukan untuk Voyage AI, tetapi Anda sebaiknya mengevaluasi berbagai vendor embeddings untuk menemukan yang paling sesuai dengan kasus penggunaan spesifik Anda.

## Model yang tersedia \{#available-models}

Voyage merekomendasikan penggunaan model text embedding berikut:

**Voyage 4 (generasi terbaru)**

| Model | Panjang Konteks | Dimensi Embedding | Deskripsi |
| --- | --- | --- | --- |
| `voyage-4-large` | 32.000 | 1024 (default), 256, 512, 2048 | Kualitas retrieval serbaguna dan multibahasa terbaik. Lihat [postingan blog](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya. |
| `voyage-4` | 32.000 | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk kualitas retrieval serbaguna dan multibahasa. Menyeimbangkan kualitas dan efisiensi. Lihat [postingan blog](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya. |
| `voyage-4-lite` | 32.000 | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk latensi dan biaya. Lihat [postingan blog](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya. |
| `voyage-4-nano` | 32.000 | 1024 (default), 256, 512, 2048 | Model open-weight (lisensi Apache 2.0) tersedia di Hugging Face. Lihat [postingan blog](https://blog.voyageai.com/2026/01/15/voyage-4/) untuk detailnya. |

**Generasi sebelumnya**

| Model | Panjang Konteks | Dimensi Embedding | Deskripsi |
| --- | --- | --- | --- |
| `voyage-3-large` | 32.000 | 1024 (default), 256, 512, 2048 | Kualitas retrieval serbaguna dan multibahasa terbaik. Lihat [postingan blog](https://blog.voyageai.com/2025/01/07/voyage-3-large/) untuk detailnya. |
| `voyage-3.5` | 32.000 | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk kualitas retrieval serbaguna dan multibahasa. Lihat [postingan blog](https://blog.voyageai.com/2025/05/20/voyage-3-5/) untuk detailnya. |
| `voyage-3.5-lite` | 32.000 | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk latensi dan biaya. Lihat [postingan blog](https://blog.voyageai.com/2025/05/20/voyage-3-5/) untuk detailnya. |
| `voyage-code-3` | 32.000 | 1024 (default), 256, 512, 2048 | Dioptimalkan untuk retrieval **kode**. Lihat [postingan blog](https://blog.voyageai.com/2024/12/04/voyage-code-3/) untuk detailnya. |
| `voyage-finance-2` | 32.000 | 1024 | Dioptimalkan untuk retrieval dan RAG **keuangan**. Lihat [postingan blog](https://blog.voyageai.com/2024/06/03/domain-specific-embeddings-finance-edition-voyage-finance-2/) untuk detailnya. |
| `voyage-law-2` | 16.000 | 1024 | Dioptimalkan untuk retrieval dan RAG **hukum** dan **konteks panjang**. Juga meningkatkan performa di semua domain. Lihat [postingan blog](https://blog.voyageai.com/2024/04/15/domain-specific-embeddings-and-retrieval-legal-edition-voyage-law-2/) untuk detailnya. |

Selain itu, model embedding multimodal berikut direkomendasikan:

| Model | Panjang Konteks | Dimensi Embedding | Deskripsi |
| --- | --- | --- | --- |
| `voyage-multimodal-3.5` | 32.000 | 1024 (default), 256, 512, 2048 | Model embedding multimodal yang kaya yang dapat memvektorisasi teks, gambar, dan video yang disisipkan. Mencakup dukungan video sebagai model embedding video tingkat produksi pertama. Lihat [postingan blog](https://blog.voyageai.com/2026/01/15/voyage-multimodal-3-5/) untuk detailnya. |
| `voyage-multimodal-3` | 32.000 | 1024 | Model embedding multimodal yang kaya yang dapat memvektorisasi teks dan gambar kaya konten yang disisipkan, seperti tangkapan layar PDF, slide, tabel, gambar, dan lainnya. Lihat [postingan blog](https://blog.voyageai.com/2024/11/12/voyage-multimodal-3/) untuk detailnya. |

Butuh bantuan memutuskan model text embedding mana yang akan digunakan? Lihat [FAQ](https://docs.voyageai.com/docs/faq#what-embedding-models-are-available-and-which-one-should-i-use&ref=anthropic).

## Memulai dengan Voyage AI \{#getting-started-with-voyage-ai}

Untuk mengakses embeddings Voyage:

1. Daftar di situs web Voyage AI
2. Dapatkan kunci API
3. Atur kunci API sebagai variabel lingkungan untuk kemudahan:

```bash
export VOYAGE_API_KEY="<your secret key>"
```

Anda dapat memperoleh embeddings dengan menggunakan [package Python `voyageai`](https://github.com/voyage-ai/voyageai-python) resmi atau permintaan HTTP, seperti yang dijelaskan di bawah ini.

### Library Python Voyage \{#voyage-python-library}

Package `voyageai` dapat diinstal menggunakan perintah berikut:

```bash
pip install -U voyageai
```

Kemudian, Anda dapat membuat objek client dan mulai menggunakannya untuk meng-embed teks Anda:

```python nocheck
import voyageai

vo = voyageai.Client()
# Ini akan secara otomatis menggunakan variabel lingkungan VOYAGE_API_KEY.
# Alternatifnya, Anda dapat menggunakan vo = voyageai.Client(api_key="<your secret key>")

texts = ["Sample text 1", "Sample text 2"]

result = vo.embed(texts, model="voyage-4", input_type="document")
print(result.embeddings[0])
print(result.embeddings[1])
```

`result.embeddings` akan berupa daftar dua vektor embedding, masing-masing berisi 1024 angka floating-point. Setelah menjalankan kode di atas, kedua embeddings akan dicetak di layar:

```text nowrap
[-0.013131560757756233, 0.019828535616397858, ...]   # embedding for "Sample text 1"
[-0.0069352793507277966, 0.020878976210951805, ...]  # embedding for "Sample text 2"
```

Saat membuat embeddings, Anda dapat menentukan beberapa argumen lain ke fungsi `embed()`.

Untuk informasi lebih lanjut tentang package Python Voyage, lihat [dokumentasi Voyage](https://docs.voyageai.com/docs/embeddings#python-api).

### HTTP API Voyage \{#voyage-http-api}

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

Untuk informasi lebih lanjut tentang HTTP API Voyage, lihat [dokumentasi Voyage](https://docs.voyageai.com/reference/embeddings-api).

### AWS Marketplace \{#aws-marketplace}

Embeddings Voyage tersedia di [AWS Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=seller-snt4gb6fd7ljg). Instruksi untuk mengakses Voyage di AWS tersedia di [dokumentasi Voyage AWS Marketplace](https://docs.voyageai.com/docs/aws-marketplace-model-package?ref=anthropic).

## Contoh quickstart \{#quickstart-example}

Contoh singkat berikut menunjukkan cara menggunakan embeddings.

Misalkan Anda memiliki korpus kecil berisi enam dokumen untuk diambil

```python nocheck
documents = [
    "The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
    "Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
    "20th-century innovations, from radios to smartphones, centered on electronic advancements.",
    "Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
    "Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
    "Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature.",
]
```

Pertama, gunakan Voyage untuk mengonversi setiap dokumen menjadi vektor embedding

```python nocheck
import voyageai

vo = voyageai.Client()

# Lakukan embedding pada dokumen
doc_embds = vo.embed(documents, model="voyage-4", input_type="document").embeddings
```

Embeddings memungkinkan Anda melakukan pencarian / retrieval semantik di ruang vektor. Diberikan contoh query,

```python
query = "When is Apple's conference call scheduled?"
```

Selanjutnya, konversikan menjadi embedding dan lakukan pencarian nearest neighbor untuk menemukan dokumen yang paling relevan berdasarkan jarak di ruang embedding.

```python nocheck
import numpy as np

# Lakukan embedding pada kueri
query_embd = vo.embed([query], model="voyage-4", input_type="query").embeddings[0]

# Hitung kemiripannya
# Embedding Voyage dinormalisasi ke panjang 1, sehingga dot-product
# dan cosine similarity bernilai sama.
similarities = np.dot(doc_embds, query_embd)

retrieved_id = np.argmax(similarities)
print(documents[retrieved_id])
```

Perhatikan bahwa `input_type="document"` dan `input_type="query"` digunakan untuk meng-embed dokumen dan query, secara berurutan. Spesifikasi lebih lanjut dapat ditemukan di [Library Python Voyage](/docs/id/build-with-claude/embeddings#voyage-python-library).

Output-nya akan berupa dokumen ke-5, yang memang paling relevan dengan query:

```text
Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.
```

Jika Anda mencari kumpulan cookbook terperinci tentang cara melakukan RAG dengan embeddings, termasuk database vektor, lihat [cookbook RAG](https://platform.claude.com/cookbook/third-party-pinecone-rag-using-pinecone).

## FAQ \{#faq}

  <section title="Mengapa embeddings Voyage memiliki kualitas yang unggul?">

    Model embedding mengandalkan jaringan neural yang kuat untuk menangkap dan mengompresi konteks semantik, mirip dengan model generatif. Tim peneliti AI berpengalaman dari Voyage mengoptimalkan setiap komponen proses embedding, termasuk:
    - Arsitektur model
    - Pengumpulan data
    - Fungsi loss
    - Pemilihan optimizer

    Pelajari lebih lanjut tentang pendekatan teknis Voyage di [blog](https://blog.voyageai.com/) mereka.
  
</section>

  <section title="Model embedding apa yang tersedia dan mana yang harus saya gunakan?">

    Untuk embedding serbaguna, model yang direkomendasikan adalah:
    - `voyage-4-large`: Kualitas terbaik
    - `voyage-4-lite`: Latensi dan biaya terendah
    - `voyage-4`: Performa seimbang

    Untuk retrieval, gunakan parameter `input_type` untuk menentukan apakah teks adalah tipe query atau dokumen.

    Model spesifik domain:

    - Tugas hukum: `voyage-law-2`
    - Kode dan dokumentasi pemrograman: `voyage-code-3`
    - Tugas terkait keuangan: `voyage-finance-2`
  
</section>

  <section title="Fungsi kemiripan mana yang harus saya gunakan?">

    Anda dapat menggunakan embeddings Voyage dengan dot-product similarity, cosine similarity, atau Euclidean distance. Penjelasan tentang kemiripan embedding dapat ditemukan di [panduan kemiripan vektor](https://www.pinecone.io/learn/vector-similarity/) ini.

    Embeddings Voyage AI dinormalisasi ke panjang 1, yang berarti bahwa:

    - Cosine similarity setara dengan dot-product similarity, sementara yang terakhir dapat dihitung lebih cepat.
    - Cosine similarity dan Euclidean distance akan menghasilkan peringkat yang identik.
  
</section>

  <section title="Apa hubungan antara karakter, kata, dan token?">

    Lihat [halaman](https://docs.voyageai.com/docs/tokenization?ref=anthropic) ini.
  
</section>

  <section title="Kapan dan bagaimana saya harus menggunakan parameter input_type?">

    Untuk semua tugas dan kasus penggunaan retrieval (misalnya, RAG), gunakan parameter `input_type` untuk menentukan apakah teks input adalah query atau dokumen. Jangan menghilangkan `input_type` atau mengatur `input_type=None`. Menentukan apakah teks input adalah query atau dokumen dapat menciptakan representasi vektor padat yang lebih baik untuk retrieval, yang dapat menghasilkan kualitas retrieval yang lebih baik.

    Saat menggunakan parameter `input_type`, prompt khusus ditambahkan di awal teks input sebelum di-embed. Secara spesifik:

    > 📘 **Prompt yang terkait dengan `input_type`**
    >
    > - Untuk query, prompt-nya adalah “Represent the query for retrieving supporting documents: “.
    > - Untuk dokumen, prompt-nya adalah “Represent the document for retrieval: “.
    > - Contoh
    >     - Ketika `input_type="query"`, query seperti "When is Apple's conference call scheduled?" akan menjadi "**Represent the query for retrieving supporting documents:** When is Apple's conference call scheduled?"
    >     - Ketika `input_type="document"`, query seperti "Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET." akan menjadi "**Represent the document for retrieval:** Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET."

    `voyage-large-2-instruct`, seperti namanya, dilatih untuk responsif terhadap instruksi tambahan yang ditambahkan di awal teks input. Untuk klasifikasi, clustering, atau subtugas [MTEB](https://huggingface.co/mteb) lainnya, silakan gunakan [instruksi voyage-large-2-instruct](https://github.com/voyage-ai/voyage-large-2-instruct).
  
</section>

  <section title="Opsi kuantisasi apa yang tersedia?">

    Kuantisasi dalam embeddings mengonversi nilai presisi tinggi, seperti angka floating-point presisi tunggal 32-bit, ke format presisi lebih rendah seperti integer 8-bit atau nilai biner 1-bit, mengurangi penyimpanan, memori, dan biaya masing-masing sebesar 4x dan 32x. Model Voyage yang didukung memungkinkan kuantisasi dengan menentukan tipe data output menggunakan parameter `output_dtype`:

    - `float`: Setiap embedding yang dikembalikan adalah daftar angka floating-point presisi tunggal 32-bit (4-byte). Ini adalah default dan memberikan presisi / akurasi retrieval tertinggi.
    - `int8` dan `uint8`: Setiap embedding yang dikembalikan adalah daftar integer 8-bit (1-byte) dengan rentang masing-masing dari -128 hingga 127 dan 0 hingga 255.
    - `binary` dan `ubinary`: Setiap embedding yang dikembalikan adalah daftar integer 8-bit yang merepresentasikan nilai embedding single-bit terkuantisasi yang di-bit-pack: `int8` untuk `binary` dan `uint8` untuk `ubinary`. Panjang daftar integer yang dikembalikan adalah 1/8 dari dimensi sebenarnya dari embedding. Tipe binary menggunakan metode offset binary, yang dapat Anda pelajari lebih lanjut di FAQ di bawah ini.

    > **Contoh kuantisasi biner**
    >
    > Pertimbangkan delapan nilai embedding berikut: -0.03955078, 0.006214142, -0.07446289, -0.039001465, 0.0046463013, 0.00030612946, -0.08496094, dan 0.03994751. Dengan kuantisasi biner, nilai yang kurang dari atau sama dengan nol akan dikuantisasi menjadi biner nol, dan nilai positif menjadi biner satu, menghasilkan urutan biner berikut: 0, 1, 0, 0, 1, 1, 0, 1. Delapan bit ini kemudian dikemas menjadi satu integer 8-bit, 01001101 (dengan bit paling kiri sebagai bit paling signifikan).
    >   - `ubinary`: Urutan biner langsung dikonversi dan direpresentasikan sebagai unsigned integer (`uint8`) 77.
    >   - `binary`: Urutan biner direpresentasikan sebagai signed integer (`int8`) -51, dihitung menggunakan metode offset binary (77 - 128 = -51).
  
</section>

  <section title="Bagaimana cara memotong embeddings Matryoshka?">

    Matryoshka learning menciptakan embeddings dengan representasi kasar-ke-halus dalam satu vektor. Model Voyage, seperti `voyage-code-3`, yang mendukung beberapa dimensi output menghasilkan embeddings Matryoshka tersebut. Anda dapat memotong vektor-vektor ini dengan mempertahankan subset dimensi terdepan. Misalnya, kode Python berikut mendemonstrasikan cara memotong vektor 1024 dimensi menjadi 256 dimensi:

    
    ```python nocheck
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

    # Hasilkan vektor voyage-code-3, yang secara default berupa angka floating-point 1024 dimensi
    embd = vo.embed(["Sample text 1", "Sample text 2"], model="voyage-code-3").embeddings

    # Tetapkan dimensi yang lebih pendek
    short_dim = 256

    # Ubah ukuran dan normalisasi vektor ke dimensi yang lebih pendek
    resized_embd = embd_normalize(np.array(embd)[:, :short_dim]).tolist()
    ```
  
</section>

## Harga \{#pricing}

Kunjungi [halaman harga](https://docs.voyageai.com/docs/pricing?ref=anthropic) Voyage untuk detail harga terbaru.