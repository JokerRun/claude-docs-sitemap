---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/code-clarifier
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 94db955afad8a115207c59ec7d5a7178afb8a3eee5a1f7d8243052ba91bc1a7e
---

# Penjelasan kode

Sederhanakan dan jelaskan kode kompleks dalam bahasa biasa.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah mengambil cuplikan kode yang disediakan dan menjelaskannya dalam bahasa yang sederhana dan mudah dipahami. Uraikan fungsionalitas kode, tujuan, dan komponen utamanya. Gunakan analogi, contoh, dan istilah biasa untuk membuat penjelasan dapat diakses oleh seseorang dengan pengetahuan coding minimal. Hindari menggunakan jargon teknis kecuali benar-benar diperlukan, dan berikan penjelasan yang jelas untuk jargon apa pun yang digunakan. Tujuannya adalah membantu pembaca memahami apa yang dilakukan kode dan cara kerjanya pada tingkat tinggi. |
| Pengguna   | import random def bubble*sort(arr): n = len(arr) for i in range(n-1): for j in range(n-i-1): if arr[j] > arr[j+1]: arr[j], arr[j+1] = arr[j+1], arr[j] return arr numbers = [random.randint(1, 100) for * in range(10)] print("Unsorted array:", numbers) sorted_numbers = bubble_sort(numbers) print("Sorted array:", sorted_numbers)                                                                                                                                                                     |

### Contoh Output

> Kode ini mendemonstrasikan implementasi algoritma bubble sort, yang digunakan untuk mengurutkan daftar angka dalam urutan ascending. Mari kita uraikan langkah demi langkah:
>
> 1.  Kode dimulai dengan mengimpor modul 'random', yang akan digunakan untuk menghasilkan angka acak untuk contohnya.
> 2.  Fungsi 'bubble_sort' didefinisikan, yang mengambil array (daftar) angka sebagai input. Fungsi ini akan melakukan operasi pengurutan.
> 3.  Di dalam fungsi 'bubble_sort', variabel 'n' ditetapkan ke panjang array input. Ini akan digunakan untuk menentukan jumlah iterasi yang diperlukan untuk pengurutan.
> 4.  Loop pertama, dikendalikan oleh variabel 'i', melakukan iterasi sebanyak 'n-1' kali. Ini karena setelah 'n-1' pass, angka terbesar akan berada di akhir array, jadi kita tidak perlu membandingkannya lagi.
> 5.  Loop kedua, dikendalikan oleh variabel 'j', melakukan iterasi sebanyak 'n-i-1' kali. Ini karena setelah setiap pass, angka terbesar di antara elemen yang belum diurutkan akan ditempatkan di akhir, jadi kita tidak perlu membandingkannya di pass berikutnya.
> 6.  Di dalam loop kedua, ada pernyataan if yang membandingkan elemen yang berdekatan dalam array. Jika elemen pada indeks 'j' lebih besar dari elemen pada indeks 'j+1', keduanya ditukar. Ini memastikan bahwa elemen yang lebih besar bergerak menuju akhir array.
> 7.  Pertukaran dilakukan menggunakan sintaks Python 'arr\[j\], arr\[j+1\] = arr\[j+1\], arr\[j\]', yang secara bersamaan menetapkan nilai 'arr\[j+1\]' ke 'arr\[j\]' dan 'arr\[j\]' ke 'arr\[j+1\]'.
> 8.  Setelah semua iterasi selesai, array yang diurutkan dikembalikan oleh fungsi 'bubble_sort'.
> 9.  Dalam kode contoh, daftar 10 angka acak antara 1 dan 100 dihasilkan menggunakan list comprehension: '\[random.randint(1, 100) for \_ in range(10)\]'. Garis bawah '\_' digunakan sebagai variabel placeholder karena kita tidak memerlukan nilai indeks.
> 10. Array yang belum diurutkan dicetak untuk menunjukkan urutan awal angka-angka tersebut.
>
> 11. Fungsi 'bubble_sort' dipanggil dengan array 'numbers' sebagai input, dan array yang diurutkan disimpan dalam variabel 'sorted_numbers'.
>
> 12. Terakhir, array yang diurutkan dicetak untuk menampilkan angka-angka dalam urutan ascending.
>
> Dalam istilah yang lebih sederhana, bayangkan Anda memiliki daftar angka yang tidak teratur. Algoritma bubble sort bekerja dengan membandingkan setiap angka dengan angka di sebelahnya, dan jika mereka dalam urutan yang salah, mereka ditukar. Proses ini diulang berkali-kali sampai seluruh daftar diurutkan. Ini seperti gelembung yang naik ke permukaan, dengan angka-angka yang lebih besar secara bertahap bergerak menuju akhir daftar di setiap pass.

---

### Permintaan API

<CodeGroup>
    ```python Python
    import anthropic
    
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="my_api_key",
    )
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1000,
        temperature=0,
        system="Your task is to take the code snippet provided and explain it in simple, easy-to-understand language. Break down the code's functionality, purpose, and key components. Use analogies, examples, and plain terms to make the explanation accessible to someone with minimal coding knowledge. Avoid using technical jargon unless absolutely necessary, and provide clear explanations for any jargon used. The goal is to help the reader understand what the code does and how it works at a high level.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "import random\n\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n-1):\n        for j in range(n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\nnumbers = [random.randint(1, 100) for _ in range(10)]\nprint(\"Unsorted array:\", numbers)\nsorted_numbers = bubble_sort(numbers)\nprint(\"Sorted array:\", sorted_numbers)"
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript TypeScript
    import Anthropic from "@anthropic-ai/sdk";
    
    const anthropic = new Anthropic({
      apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
    });
    
    const msg = await anthropic.messages.create({
      model: "claude-opus-4-6",
      max_tokens: 1000,
      temperature: 0,
      system: "Your task is to take the code snippet provided and explain it in simple, easy-to-understand language. Break down the code's functionality, purpose, and key components. Use analogies, examples, and plain terms to make the explanation accessible to someone with minimal coding knowledge. Avoid using technical jargon unless absolutely necessary, and provide clear explanations for any jargon used. The goal is to help the reader understand what the code does and how it works at a high level.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "import random\n\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n-1):\n        for j in range(n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\nnumbers = [random.randint(1, 100) for _ in range(10)]\nprint(\"Unsorted array:\", numbers)\nsorted_numbers = bubble_sort(numbers)\nprint(\"Sorted array:\", sorted_numbers)"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python AWS Bedrock Python
    from anthropic import AnthropicBedrock
    
    # See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    # for authentication options
    client = AnthropicBedrock()
    
    message = client.messages.create(
        model="anthropic.claude-opus-4-6-v1",
        max_tokens=1000,
        temperature=0,
        system="Your task is to take the code snippet provided and explain it in simple, easy-to-understand language. Break down the code's functionality, purpose, and key components. Use analogies, examples, and plain terms to make the explanation accessible to someone with minimal coding knowledge. Avoid using technical jargon unless absolutely necessary, and provide clear explanations for any jargon used. The goal is to help the reader understand what the code does and how it works at a high level.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "import random\n\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n-1):\n        for j in range(n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\nnumbers = [random.randint(1, 100) for _ in range(10)]\nprint(\"Unsorted array:\", numbers)\nsorted_numbers = bubble_sort(numbers)\nprint(\"Sorted array:\", sorted_numbers)"
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript AWS Bedrock TypeScript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";
    
    // See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    // for authentication options
    const client = new AnthropicBedrock();
    
    const msg = await client.messages.create({
      model: "anthropic.claude-opus-4-6-v1",
      max_tokens: 1000,
      temperature: 0,
      system: "Your task is to take the code snippet provided and explain it in simple, easy-to-understand language. Break down the code's functionality, purpose, and key components. Use analogies, examples, and plain terms to make the explanation accessible to someone with minimal coding knowledge. Avoid using technical jargon unless absolutely necessary, and provide clear explanations for any jargon used. The goal is to help the reader understand what the code does and how it works at a high level.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "import random\n\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n-1):\n        for j in range(n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\nnumbers = [random.randint(1, 100) for _ in range(10)]\nprint(\"Unsorted array:\", numbers)\nsorted_numbers = bubble_sort(numbers)\nprint(\"Sorted array:\", sorted_numbers)"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python Vertex AI Python
    from anthropic import AnthropicVertex
    
    client = AnthropicVertex()
    
    message = client.messages.create(
        model="claude-sonnet-4@20250514",
        max_tokens=1000,
        temperature=0,
        system="Your task is to take the code snippet provided and explain it in simple, easy-to-understand language. Break down the code's functionality, purpose, and key components. Use analogies, examples, and plain terms to make the explanation accessible to someone with minimal coding knowledge. Avoid using technical jargon unless absolutely necessary, and provide clear explanations for any jargon used. The goal is to help the reader understand what the code does and how it works at a high level.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "import random\n\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n-1):\n        for j in range(n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\nnumbers = [random.randint(1, 100) for _ in range(10)]\nprint(\"Unsorted array:\", numbers)\nsorted_numbers = bubble_sort(numbers)\nprint(\"Sorted array:\", sorted_numbers)"
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript Vertex AI TypeScript
    import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';
    
    // Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
    // Additionally goes through the standard `google-auth-library` flow.
    const client = new AnthropicVertex();
    
    const msg = await client.messages.create({
      model: "claude-sonnet-4@20250514",
      max_tokens: 1000,
      temperature: 0,
      system: "Your task is to take the code snippet provided and explain it in simple, easy-to-understand language. Break down the code's functionality, purpose, and key components. Use analogies, examples, and plain terms to make the explanation accessible to someone with minimal coding knowledge. Avoid using technical jargon unless absolutely necessary, and provide clear explanations for any jargon used. The goal is to help the reader understand what the code does and how it works at a high level.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "import random\n\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n-1):\n        for j in range(n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\nnumbers = [random.randint(1, 100) for _ in range(10)]\nprint(\"Unsorted array:\", numbers)\nsorted_numbers = bubble_sort(numbers)\nprint(\"Sorted array:\", sorted_numbers)"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
</CodeGroup>