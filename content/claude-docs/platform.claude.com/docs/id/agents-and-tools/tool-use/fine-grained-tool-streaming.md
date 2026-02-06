---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: e0a8d286d3a5e022b0509952bb0d2c114816f92aec4d9eaabc6615553c3b7f55
---

# Streaming alat berbutir halus

Pelajari cara menggunakan streaming alat berbutir halus untuk mengurangi latensi saat menerima parameter besar

---

Streaming alat berbutir halus tersedia secara umum di semua model dan semua platform, tanpa memerlukan header beta. Ini memungkinkan [streaming](/docs/id/build-with-claude/streaming) nilai parameter penggunaan alat tanpa buffering atau validasi JSON, mengurangi latensi untuk mulai menerima parameter besar.

<Warning>
Saat menggunakan streaming alat berbutir halus, Anda mungkin menerima input JSON yang tidak valid atau sebagian. Pastikan untuk mempertimbangkan kasus-kasus tepi ini dalam kode Anda.
</Warning>

## Cara menggunakan streaming alat berbutir halus
Streaming alat berbutir halus tersedia di semua model dan semua platform (Claude API, Amazon Bedrock, Google Vertex AI, dan Microsoft Foundry). Untuk menggunakannya, atur `eager_input_streaming` ke `true` pada alat apa pun tempat Anda ingin streaming berbutir halus diaktifkan, dan aktifkan streaming pada permintaan Anda.

Berikut adalah contoh cara menggunakan streaming alat berbutir halus dengan API:

<CodeGroup>

  ```bash Shell
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-6",
      "max_tokens": 65536,
      "tools": [
        {
          "name": "make_file",
          "description": "Write text to a file",
          "eager_input_streaming": true,
          "input_schema": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "description": "The filename to write text to"
              },
              "lines_of_text": {
                "type": "array",
                "description": "An array of lines of text to write to the file"
              }
            },
            "required": ["filename", "lines_of_text"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Can you write a long poem and make a file called poem.txt?"
        }
      ],
      "stream": true
    }' | jq '.usage'
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  response = client.messages.stream(
      max_tokens=65536,
      model="claude-opus-4-6",
      tools=[{
        "name": "make_file",
        "description": "Write text to a file",
        "eager_input_streaming": True,
        "input_schema": {
          "type": "object",
          "properties": {
            "filename": {
              "type": "string",
              "description": "The filename to write text to"
            },
            "lines_of_text": {
              "type": "array",
              "description": "An array of lines of text to write to the file"
            }
          },
          "required": ["filename", "lines_of_text"]
        }
      }],
      messages=[{
        "role": "user",
        "content": "Can you write a long poem and make a file called poem.txt?"
      }]
  )

  print(response.usage)
  ```

  ```typescript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  const message = await anthropic.messages.stream({
    model: "claude-opus-4-6",
    max_tokens: 65536,
    tools: [{
      "name": "make_file",
      "description": "Write text to a file",
      "eager_input_streaming": true,
      "input_schema": {
        "type": "object",
        "properties": {
          "filename": {
            "type": "string",
            "description": "The filename to write text to"
          },
          "lines_of_text": {
            "type": "array",
            "description": "An array of lines of text to write to the file"
          }
        },
        "required": ["filename", "lines_of_text"]
      }
    }],
    messages: [{
      role: "user",
      content: "Can you write a long poem and make a file called poem.txt?"
    }]
  });

  console.log(message.usage);
  ```
</CodeGroup>

Dalam contoh ini, streaming alat berbutir halus memungkinkan Claude untuk melakukan streaming baris-baris puisi panjang ke dalam panggilan alat `make_file` tanpa buffering untuk memvalidasi apakah parameter `lines_of_text` adalah JSON yang valid. Ini berarti Anda dapat melihat parameter stream saat tiba, tanpa harus menunggu seluruh parameter untuk buffer dan validasi.

<Note>
Dengan streaming alat berbutir halus, chunk penggunaan alat mulai melakukan streaming lebih cepat, dan sering kali lebih panjang dan mengandung lebih sedikit jeda kata. Ini disebabkan oleh perbedaan dalam perilaku chunking.

Contoh: 

Tanpa streaming berbutir halus (penundaan 15 detik):
```
Chunk 1: '{"'
Chunk 2: 'query": "Ty'
Chunk 3: 'peScri'
Chunk 4: 'pt 5.0 5.1 '
Chunk 5: '5.2 5'
Chunk 6: '.3'
Chunk 8: ' new f'
Chunk 9: 'eatur'
...
```

Dengan streaming berbutir halus (penundaan 3 detik):
```
Chunk 1: '{"query": "TypeScript 5.0 5.1 5.2 5.3'
Chunk 2: ' new features comparison'
```
</Note>

<Warning>
Karena streaming berbutir halus mengirim parameter tanpa buffering atau validasi JSON, tidak ada jaminan bahwa stream yang dihasilkan akan selesai dalam string JSON yang valid.
Khususnya, jika [stop reason](/docs/id/build-with-claude/handling-stop-reasons) `max_tokens` tercapai, stream mungkin berakhir di tengah parameter dan mungkin tidak lengkap. Anda umumnya harus menulis dukungan khusus untuk menangani saat `max_tokens` tercapai.
</Warning>

## Menangani JSON tidak valid dalam respons alat

Saat menggunakan streaming alat berbutir halus, Anda mungkin menerima JSON yang tidak valid atau tidak lengkap dari model. Jika Anda perlu melewatkan JSON yang tidak valid ini kembali ke model dalam blok respons kesalahan, Anda dapat membungkusnya dalam objek JSON untuk memastikan penanganan yang tepat (dengan kunci yang masuk akal). Sebagai contoh:

```json
{
  "INVALID_JSON": "<your invalid json string>"
}
```

Pendekatan ini membantu model memahami bahwa konten adalah JSON yang tidak valid sambil mempertahankan data yang salah format asli untuk tujuan debugging.

<Note>
Saat membungkus JSON yang tidak valid, pastikan untuk dengan benar meloloskan tanda kutip atau karakter khusus apa pun dalam string JSON yang tidak valid untuk mempertahankan struktur JSON yang valid dalam objek wrapper.
</Note>