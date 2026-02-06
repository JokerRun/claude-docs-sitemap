---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/efficiency-estimator
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 7265329f530586fa317cd8d55760799585c6bb111a5d070ef01aa9f6744261f9
---

# Estimator efisiensi

Hitung kompleksitas waktu dari fungsi dan algoritma.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sistem | Tugas Anda adalah menganalisis fungsi atau algoritma yang diberikan dan menghitung kompleksitas waktunya menggunakan notasi Big O. Jelaskan penalaran Anda langkah demi langkah, mendeskripsikan bagaimana Anda sampai pada kompleksitas waktu akhir. Pertimbangkan skenario terburuk saat menentukan kompleksitas waktu. Jika fungsi atau algoritma berisi beberapa langkah atau loop bersarang, berikan kompleksitas waktu untuk setiap langkah dan kemudian berikan kompleksitas waktu keseluruhan untuk seluruh fungsi atau algoritma. Asumsikan bahwa fungsi bawaan atau operasi apa pun yang digunakan memiliki kompleksitas waktu O(1) kecuali ditentukan lain. |
| Pengguna   | def example_function(n): for i in range(n): print(i) for j in range(n): for k in range(n): print(j, k)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

### Contoh output

> Untuk menganalisis kompleksitas waktu dari fungsi `example_function(n)` yang diberikan, kami akan memecahnya menjadi langkah-langkah dan mempertimbangkan skenario terburuk.
>
> Langkah 1: Menganalisis loop pertama
>
> ```
> for i in range(n):
>    print(i)
>
> ```

> Loop ini beriterasi `n` kali dan melakukan operasi waktu konstan (`print(i)`) di setiap iterasi. Oleh karena itu, kompleksitas waktu dari langkah ini adalah O(n).
>
> Langkah 2: Menganalisis loop bersarang
>
> ```
> for j in range(n):
>     for k in range(n):
>         print(j, k)
>
> ```
>
> Loop luar beriterasi `n` kali, dan untuk setiap iterasi, loop dalam juga beriterasi `n` kali. Di setiap iterasi loop dalam, operasi waktu konstan (`print(j, k)`) dilakukan. Oleh karena itu, kompleksitas waktu dari loop bersarang adalah O(n \* n) = O(n^2).
>
> Langkah 3: Menggabungkan kompleksitas waktu  
> Fungsi `example_function(n)` terdiri dari dua langkah: loop pertama dan loop bersarang. Kompleksitas waktu keseluruhan adalah jumlah dari kompleksitas waktu setiap langkah.
>
> Kompleksitas waktu dari loop pertama: O(n)  
> Kompleksitas waktu dari loop bersarang: O(n^2)
>
> Untuk menentukan kompleksitas waktu keseluruhan, kami mempertimbangkan istilah dominan, yang merupakan istilah dengan urutan pertumbuhan tertinggi. Dalam hal ini, O(n^2) mendominasi O(n).
>
> Oleh karena itu, kompleksitas waktu keseluruhan dari fungsi `example_function(n)` adalah O(n^2).
>
> Dalam skenario terburuk, ketika `n` besar, loop bersarang akan mendominasi waktu eksekusi, dan fungsi akan memiliki kompleksitas waktu kuadratik.

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
        system="Your task is to analyze the provided function or algorithm and calculate its time complexity using Big O notation. Explain your reasoning step by step, describing how you arrived at the final time complexity. Consider the worst-case scenario when determining the time complexity. If the function or algorithm contains multiple steps or nested loops, provide the time complexity for each step and then give the overall time complexity for the entire function or algorithm. Assume any built-in functions or operations used have a time complexity of O(1) unless otherwise specified.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "def example_function(n):\n    for i in range(n):\n        print(i)\n\n    for j in range(n):\n        for k in range(n):\n            print(j, k)"
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
      system: "Your task is to analyze the provided function or algorithm and calculate its time complexity using Big O notation. Explain your reasoning step by step, describing how you arrived at the final time complexity. Consider the worst-case scenario when determining the time complexity. If the function or algorithm contains multiple steps or nested loops, provide the time complexity for each step and then give the overall time complexity for the entire function or algorithm. Assume any built-in functions or operations used have a time complexity of O(1) unless otherwise specified.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "def example_function(n):\n    for i in range(n):\n        print(i)\n\n    for j in range(n):\n        for k in range(n):\n            print(j, k)"
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
        model="anthropic.claude-opus-4-6-v1:0",
        max_tokens=1000,
        temperature=0,
        system="Your task is to analyze the provided function or algorithm and calculate its time complexity using Big O notation. Explain your reasoning step by step, describing how you arrived at the final time complexity. Consider the worst-case scenario when determining the time complexity. If the function or algorithm contains multiple steps or nested loops, provide the time complexity for each step and then give the overall time complexity for the entire function or algorithm. Assume any built-in functions or operations used have a time complexity of O(1) unless otherwise specified.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "def example_function(n):\n    for i in range(n):\n        print(i)\n\n    for j in range(n):\n        for k in range(n):\n            print(j, k)"
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
      model: "anthropic.claude-opus-4-6-v1:0",
      max_tokens: 1000,
      temperature: 0,
      system: "Your task is to analyze the provided function or algorithm and calculate its time complexity using Big O notation. Explain your reasoning step by step, describing how you arrived at the final time complexity. Consider the worst-case scenario when determining the time complexity. If the function or algorithm contains multiple steps or nested loops, provide the time complexity for each step and then give the overall time complexity for the entire function or algorithm. Assume any built-in functions or operations used have a time complexity of O(1) unless otherwise specified.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "def example_function(n):\n    for i in range(n):\n        print(i)\n\n    for j in range(n):\n        for k in range(n):\n            print(j, k)"
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
        system="Your task is to analyze the provided function or algorithm and calculate its time complexity using Big O notation. Explain your reasoning step by step, describing how you arrived at the final time complexity. Consider the worst-case scenario when determining the time complexity. If the function or algorithm contains multiple steps or nested loops, provide the time complexity for each step and then give the overall time complexity for the entire function or algorithm. Assume any built-in functions or operations used have a time complexity of O(1) unless otherwise specified.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "def example_function(n):\n    for i in range(n):\n        print(i)\n\n    for j in range(n):\n        for k in range(n):\n            print(j, k)"
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
      system: "Your task is to analyze the provided function or algorithm and calculate its time complexity using Big O notation. Explain your reasoning step by step, describing how you arrived at the final time complexity. Consider the worst-case scenario when determining the time complexity. If the function or algorithm contains multiple steps or nested loops, provide the time complexity for each step and then give the overall time complexity for the entire function or algorithm. Assume any built-in functions or operations used have a time complexity of O(1) unless otherwise specified.",
      temperature: 0,
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "def example_function(n):\n    for i in range(n):\n        print(i)\n\n    for j in range(n):\n        for k in range(n):\n            print(j, k)"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
</CodeGroup>