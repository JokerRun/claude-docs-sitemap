---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 95b74ee3d7323c1ca3a6ef35dbe09f1acf69bae9af3783276779d3f92136ab57
---

# Menangani alasan penghentian

Pelajari cara menangani berbagai nilai stop_reason dari Messages API Claude untuk membangun aplikasi yang lebih robust

---

Ketika Anda membuat permintaan ke Messages API, respons Claude mencakup bidang `stop_reason` yang menunjukkan mengapa model berhenti menghasilkan responsnya. Memahami nilai-nilai ini sangat penting untuk membangun aplikasi yang robust yang menangani berbagai jenis respons dengan tepat.

Untuk detail tentang `stop_reason` dalam respons API, lihat [referensi Messages API](/docs/id/api/messages).

## Apa itu stop_reason?

Bidang `stop_reason` adalah bagian dari setiap respons Messages API yang berhasil. Tidak seperti kesalahan, yang menunjukkan kegagalan dalam memproses permintaan Anda, `stop_reason` memberi tahu Anda mengapa Claude berhasil menyelesaikan pembuatan responsnya.

```json Example response
{
  "id": "msg_01234",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Here's the answer to your question..."
    }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  }
}
```

## Nilai-nilai stop reason

### end_turn
Alasan penghentian yang paling umum. Menunjukkan Claude menyelesaikan responsnya secara alami.

```python
if response.stop_reason == "end_turn":
    # Process the complete response
    print(response.content[0].text)
```

#### Respons kosong dengan end_turn

Kadang-kadang Claude mengembalikan respons kosong (tepat 2-3 token tanpa konten) dengan `stop_reason: "end_turn"`. Ini biasanya terjadi ketika Claude menginterpretasikan bahwa giliran asisten sudah selesai, terutama setelah hasil alat.

**Penyebab umum:**
- Menambahkan blok teks segera setelah hasil alat (Claude belajar untuk mengharapkan pengguna selalu menyisipkan teks setelah hasil alat, jadi ia mengakhiri gilirannya untuk mengikuti pola)
- Mengirim respons Claude yang sudah selesai kembali tanpa menambahkan apa pun (Claude sudah memutuskan bahwa itu selesai, jadi itu akan tetap selesai)

**Cara mencegah respons kosong:**

```python
# INCORRECT: Adding text immediately after tool_result
messages = [
    {"role": "user", "content": "Calculate the sum of 1234 and 5678"},
    {"role": "assistant", "content": [
        {
            "type": "tool_use",
            "id": "toolu_123",
            "name": "calculator",
            "input": {"operation": "add", "a": 1234, "b": 5678}
        }
    ]},
    {"role": "user", "content": [
        {
            "type": "tool_result",
            "tool_use_id": "toolu_123",
            "content": "6912"
        },
        {
            "type": "text",
            "text": "Here's the result"  # Don't add text after tool_result
        }
    ]}
]

# CORRECT: Send tool results directly without additional text
messages = [
    {"role": "user", "content": "Calculate the sum of 1234 and 5678"},
    {"role": "assistant", "content": [
        {
            "type": "tool_use",
            "id": "toolu_123",
            "name": "calculator",
            "input": {"operation": "add", "a": 1234, "b": 5678}
        }
    ]},
    {"role": "user", "content": [
        {
            "type": "tool_result",
            "tool_use_id": "toolu_123",
            "content": "6912"
        }
    ]}  # Just the tool_result, no additional text
]

# If you still get empty responses after fixing the above:
def handle_empty_response(client, messages):
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=messages
    )

    # Check if response is empty
    if (response.stop_reason == "end_turn" and
        not response.content):

        # INCORRECT: Don't just retry with the empty response
        # This won't work because Claude already decided it's done

        # CORRECT: Add a continuation prompt in a NEW user message
        messages.append({"role": "user", "content": "Please continue"})

        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=messages
        )

    return response
```

**Praktik terbaik:**
1. **Jangan pernah menambahkan blok teks segera setelah hasil alat** - Ini mengajarkan Claude untuk mengharapkan input pengguna setelah setiap penggunaan alat
2. **Jangan coba lagi respons kosong tanpa modifikasi** - Hanya mengirim respons kosong kembali tidak akan membantu
3. **Gunakan prompt kelanjutan sebagai pilihan terakhir** - Hanya jika perbaikan di atas tidak menyelesaikan masalah

### max_tokens
Claude berhenti karena mencapai batas `max_tokens` yang ditentukan dalam permintaan Anda.

```python
# Request with limited tokens
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=10,
    messages=[{"role": "user", "content": "Explain quantum physics"}]
)

if response.stop_reason == "max_tokens":
    # Response was truncated
    print("Response was cut off at token limit")
    # Consider making another request to continue
```

### stop_sequence
Claude menemukan salah satu urutan penghentian khusus Anda.

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    stop_sequences=["END", "STOP"],
    messages=[{"role": "user", "content": "Generate text until you say END"}]
)

if response.stop_reason == "stop_sequence":
    print(f"Stopped at sequence: {response.stop_sequence}")
```

### tool_use
Claude memanggil alat dan mengharapkan Anda untuk menjalankannya.

<Note>
Untuk sebagian besar implementasi penggunaan alat, kami merekomendasikan menggunakan [tool runner](/docs/id/agents-and-tools/tool-use/implement-tool-use#tool-runner-beta) yang secara otomatis menangani eksekusi alat, pemformatan hasil, dan manajemen percakapan.
</Note>

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "What's the weather?"}]
)

if response.stop_reason == "tool_use":
    # Extract and execute the tool
    for content in response.content:
        if content.type == "tool_use":
            result = execute_tool(content.name, content.input)
            # Return result to Claude for final response
```

### pause_turn
Digunakan dengan alat server seperti pencarian web ketika Claude perlu menjeda operasi yang berjalan lama.

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{"role": "user", "content": "Search for latest AI news"}]
)

if response.stop_reason == "pause_turn":
    # Continue the conversation
    messages = [
        {"role": "user", "content": original_query},
        {"role": "assistant", "content": response.content}
    ]
    continuation = client.messages.create(
        model="claude-opus-4-6",
        messages=messages,
        tools=[{"type": "web_search_20250305", "name": "web_search"}]
    )
```

### refusal
Claude menolak untuk menghasilkan respons karena masalah keamanan.

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "[Unsafe request]"}]
)

if response.stop_reason == "refusal":
    # Claude declined to respond
    print("Claude was unable to process this request")
    # Consider rephrasing or modifying the request
```

<Tip>
Jika Anda sering mengalami alasan penghentian `refusal` saat menggunakan Claude Sonnet 4.5 atau Opus 4.1, Anda dapat mencoba memperbarui panggilan API Anda untuk menggunakan Sonnet 4 (`claude-sonnet-4-20250514`), yang memiliki batasan penggunaan yang berbeda. Pelajari lebih lanjut tentang [memahami filter keamanan API Sonnet 4.5](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Tip>

<Note>
Untuk mempelajari lebih lanjut tentang penolakan yang dipicu oleh filter keamanan API untuk Claude Sonnet 4.5, lihat [Memahami Filter Keamanan API Sonnet 4.5](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Note>

### model_context_window_exceeded
Claude berhenti karena mencapai batas jendela konteks model. Ini memungkinkan Anda untuk meminta token maksimal yang mungkin tanpa mengetahui ukuran input yang tepat.

```python
# Request with maximum tokens to get as much as possible
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=64000,  # Model's maximum output tokens
    messages=[{"role": "user", "content": "Large input that uses most of context window..."}]
)

if response.stop_reason == "model_context_window_exceeded":
    # Response hit context window limit before max_tokens
    print("Response reached model's context window limit")
    # The response is still valid but was limited by context window
```

<Note>
Alasan penghentian ini tersedia secara default di Sonnet 4.5 dan model yang lebih baru. Untuk model sebelumnya, gunakan header beta `model-context-window-exceeded-2025-08-26` untuk mengaktifkan perilaku ini.
</Note>

## Praktik terbaik untuk menangani alasan penghentian

### 1. Selalu periksa stop_reason

Jadikan kebiasaan untuk memeriksa `stop_reason` dalam logika penanganan respons Anda:

```python
def handle_response(response):
    if response.stop_reason == "tool_use":
        return handle_tool_use(response)
    elif response.stop_reason == "max_tokens":
        return handle_truncation(response)
    elif response.stop_reason == "model_context_window_exceeded":
        return handle_context_limit(response)
    elif response.stop_reason == "pause_turn":
        return handle_pause(response)
    elif response.stop_reason == "refusal":
        return handle_refusal(response)
    else:
        # Handle end_turn and other cases
        return response.content[0].text
```

### 2. Tangani respons yang terpotong dengan anggun

Ketika respons terpotong karena batas token atau jendela konteks:

```python
def handle_truncated_response(response):
    if response.stop_reason in ["max_tokens", "model_context_window_exceeded"]:
        # Option 1: Warn the user about the specific limit
        if response.stop_reason == "max_tokens":
            message = "[Response truncated due to max_tokens limit]"
        else:
            message = "[Response truncated due to context window limit]"
        return f"{response.content[0].text}\n\n{message}"

        # Option 2: Continue generation
        messages = [
            {"role": "user", "content": original_prompt},
            {"role": "assistant", "content": response.content[0].text}
        ]
        continuation = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=messages + [{"role": "user", "content": "Please continue"}]
        )
        return response.content[0].text + continuation.content[0].text
```

### 3. Implementasikan logika percobaan ulang untuk pause_turn

Untuk alat server yang mungkin berhenti:

```python
def handle_paused_conversation(initial_response, max_retries=3):
    response = initial_response
    messages = [{"role": "user", "content": original_query}]
    
    for attempt in range(max_retries):
        if response.stop_reason != "pause_turn":
            break
            
        messages.append({"role": "assistant", "content": response.content})
        response = client.messages.create(
            model="claude-opus-4-6",
            messages=messages,
            tools=original_tools
        )
    
    return response
```

## Alasan penghentian vs. kesalahan

Penting untuk membedakan antara nilai `stop_reason` dan kesalahan aktual:

### Alasan penghentian (respons berhasil)
- Bagian dari badan respons
- Menunjukkan mengapa pembuatan berhenti secara normal
- Respons berisi konten yang valid

### Kesalahan (permintaan gagal)
- Kode status HTTP 4xx atau 5xx
- Menunjukkan kegagalan pemrosesan permintaan
- Respons berisi detail kesalahan

```python
try:
    response = client.messages.create(...)
    
    # Handle successful response with stop_reason
    if response.stop_reason == "max_tokens":
        print("Response was truncated")
    
except anthropic.APIError as e:
    # Handle actual errors
    if e.status_code == 429:
        print("Rate limit exceeded")
    elif e.status_code == 500:
        print("Server error")
```

## Pertimbangan streaming

Saat menggunakan streaming, `stop_reason` adalah:
- `null` dalam acara `message_start` awal
- Disediakan dalam acara `message_delta`
- Tidak disediakan dalam acara lain apa pun

```python
with client.messages.stream(...) as stream:
    for event in stream:
        if event.type == "message_delta":
            stop_reason = event.delta.stop_reason
            if stop_reason:
                print(f"Stream ended with: {stop_reason}")
```

## Pola umum

### Menangani alur kerja penggunaan alat

<Tip>
**Lebih sederhana dengan tool runner**: Contoh di bawah menunjukkan penanganan alat manual. Untuk sebagian besar kasus penggunaan, [tool runner](/docs/id/agents-and-tools/tool-use/implement-tool-use#tool-runner-beta) secara otomatis menangani eksekusi alat dengan jauh lebih sedikit kode.
</Tip>

```python
def complete_tool_workflow(client, user_query, tools):
    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            messages=messages,
            tools=tools
        )

        if response.stop_reason == "tool_use":
            # Execute tools and continue
            tool_results = execute_tools(response.content)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            # Final response
            return response
```

### Memastikan respons lengkap

```python
def get_complete_response(client, prompt, max_attempts=3):
    messages = [{"role": "user", "content": prompt}]
    full_response = ""

    for _ in range(max_attempts):
        response = client.messages.create(
            model="claude-opus-4-6",
            messages=messages,
            max_tokens=4096
        )

        full_response += response.content[0].text

        if response.stop_reason != "max_tokens":
            break

        # Continue from where it left off
        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_response},
            {"role": "user", "content": "Please continue from where you left off."}
        ]

    return full_response
```

### Mendapatkan token maksimal tanpa mengetahui ukuran input

Dengan alasan penghentian `model_context_window_exceeded`, Anda dapat meminta token maksimal yang mungkin tanpa menghitung jumlah token input:

```python
def get_max_possible_tokens(client, prompt):
    """
    Get as many tokens as possible within the model's context window
    without needing to calculate input token count
    """
    response = client.messages.create(
        model="claude-opus-4-6",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=64000  # Set to model's maximum output tokens
    )

    if response.stop_reason == "model_context_window_exceeded":
        # Got the maximum possible tokens given input size
        print(f"Generated {response.usage.output_tokens} tokens (context limit reached)")
    elif response.stop_reason == "max_tokens":
        # Got exactly the requested tokens
        print(f"Generated {response.usage.output_tokens} tokens (max_tokens reached)")
    else:
        # Natural completion
        print(f"Generated {response.usage.output_tokens} tokens (natural completion)")

    return response.content[0].text
```

Dengan menangani nilai `stop_reason` dengan benar, Anda dapat membangun aplikasi yang lebih robust yang menangani berbagai skenario respons dengan anggun dan memberikan pengalaman pengguna yang lebih baik.