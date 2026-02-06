---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/cost-tracking
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: b2501b8913ceacf6a0a47713baad34afe83804ba71402236c62adc73e4032c8e
---

# Melacak Biaya dan Penggunaan

Pahami dan lacak penggunaan token untuk penagihan di Claude Agent SDK

---

# Pelacakan Biaya SDK

Claude Agent SDK menyediakan informasi penggunaan token yang terperinci untuk setiap interaksi dengan Claude. Panduan ini menjelaskan cara melacak biaya dengan benar dan memahami pelaporan penggunaan, terutama ketika menangani penggunaan alat paralel dan percakapan multi-langkah.

Untuk dokumentasi API lengkap, lihat [referensi SDK TypeScript](/docs/id/agent-sdk/typescript).

## Memahami Penggunaan Token

Ketika Claude memproses permintaan, ia melaporkan penggunaan token pada tingkat pesan. Data penggunaan ini sangat penting untuk melacak biaya dan menagih pengguna dengan tepat.

### Konsep Utama

1. **Langkah**: Langkah adalah pasangan permintaan/respons tunggal antara aplikasi Anda dan Claude
2. **Pesan**: Pesan individual dalam langkah (teks, penggunaan alat, hasil alat)
3. **Penggunaan**: Data konsumsi token yang terlampir pada pesan asisten

## Struktur Pelaporan Penggunaan

### Penggunaan Alat Tunggal vs Paralel

Ketika Claude menjalankan alat, pelaporan penggunaan berbeda berdasarkan apakah alat dijalankan secara berurutan atau paralel:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Contoh: Melacak penggunaan dalam percakapan
const result = await query({
  prompt: "Analisis basis kode ini dan jalankan tes",
  options: {
    onMessage: (message) => {
      if (message.type === 'assistant' && message.usage) {
        console.log(`Message ID: ${message.id}`);
        console.log(`Penggunaan:`, message.usage);
      }
    }
  }
});
```

```python Python
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage
import asyncio

# Contoh: Melacak penggunaan dalam percakapan
async def track_usage():
    # Proses pesan saat tiba
    async for message in query(
        prompt="Analisis basis kode ini dan jalankan tes"
    ):
        if isinstance(message, AssistantMessage) and hasattr(message, 'usage'):
            print(f"Message ID: {message.id}")
            print(f"Penggunaan: {message.usage}")

asyncio.run(track_usage())
```

</CodeGroup>

### Contoh Alur Pesan

Berikut adalah cara pesan dan penggunaan dilaporkan dalam percakapan multi-langkah yang khas:

```
<!-- Langkah 1: Permintaan awal dengan penggunaan alat paralel -->
assistant (text)      { id: "msg_1", usage: { output_tokens: 100, ... } }
assistant (tool_use)  { id: "msg_1", usage: { output_tokens: 100, ... } }
assistant (tool_use)  { id: "msg_1", usage: { output_tokens: 100, ... } }
assistant (tool_use)  { id: "msg_1", usage: { output_tokens: 100, ... } }
user (tool_result)
user (tool_result)
user (tool_result)

<!-- Langkah 2: Respons tindak lanjut -->
assistant (text)      { id: "msg_2", usage: { output_tokens: 98, ... } }
```

## Aturan Penggunaan Penting

### 1. ID Sama = Penggunaan Sama

**Semua pesan dengan bidang `id` yang sama melaporkan penggunaan yang identik**. Ketika Claude mengirim beberapa pesan dalam giliran yang sama (misalnya teks + penggunaan alat), mereka berbagi ID pesan dan data penggunaan yang sama.

```typescript
// Semua pesan ini memiliki ID dan penggunaan yang sama
const messages = [
  { type: 'assistant', id: 'msg_123', usage: { output_tokens: 100 } },
  { type: 'assistant', id: 'msg_123', usage: { output_tokens: 100 } },
  { type: 'assistant', id: 'msg_123', usage: { output_tokens: 100 } }
];

// Tagih hanya sekali per ID pesan unik
const uniqueUsage = messages[0].usage; // Sama untuk semua pesan dengan ID ini
```

### 2. Tagih Sekali Per Langkah

**Anda hanya harus menagih pengguna sekali per langkah**, bukan untuk setiap pesan individual. Ketika Anda melihat beberapa pesan asisten dengan ID yang sama, gunakan penggunaan dari salah satunya.

### 3. Pesan Hasil Berisi Penggunaan Kumulatif

Pesan `result` terakhir berisi total penggunaan kumulatif dari semua langkah dalam percakapan:

```typescript
// Hasil akhir mencakup penggunaan total
const result = await query({
  prompt: "Tugas multi-langkah",
  options: { /* ... */ }
});

console.log("Penggunaan total:", result.usage);
console.log("Biaya total:", result.usage.total_cost_usd);
```

### 4. Rincian Penggunaan Per-Model

Pesan hasil juga mencakup `modelUsage`, yang menyediakan data penggunaan per-model yang berwenang. Seperti `total_cost_usd`, bidang ini akurat dan cocok untuk tujuan penagihan. Ini sangat berguna ketika menggunakan beberapa model (misalnya Haiku untuk subagen, Opus untuk agen utama).

```typescript
// modelUsage menyediakan rincian per-model
type ModelUsage = {
  inputTokens: number
  outputTokens: number
  cacheReadInputTokens: number
  cacheCreationInputTokens: number
  webSearchRequests: number
  costUSD: number
  contextWindow: number
}

// Akses dari pesan hasil
const result = await query({ prompt: "..." });

// result.modelUsage adalah peta nama model ke ModelUsage
for (const [modelName, usage] of Object.entries(result.modelUsage)) {
  console.log(`${modelName}: $${usage.costUSD.toFixed(4)}`);
  console.log(`  Token input: ${usage.inputTokens}`);
  console.log(`  Token output: ${usage.outputTokens}`);
}
```

Untuk definisi tipe lengkap, lihat [referensi SDK TypeScript](/docs/id/agent-sdk/typescript).

## Implementasi: Sistem Pelacakan Biaya

Berikut adalah contoh lengkap implementasi sistem pelacakan biaya:

<CodeGroup>

```typescript TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

class CostTracker {
  private processedMessageIds = new Set<string>();
  private stepUsages: Array<any> = [];
  
  async trackConversation(prompt: string) {
    const result = await query({
      prompt,
      options: {
        onMessage: (message) => {
          this.processMessage(message);
        }
      }
    });
    
    return {
      result,
      stepUsages: this.stepUsages,
      totalCost: result.usage?.total_cost_usd || 0
    };
  }
  
  private processMessage(message: any) {
    // Hanya proses pesan asisten dengan penggunaan
    if (message.type !== 'assistant' || !message.usage) {
      return;
    }
    
    // Lewati jika kami sudah memproses ID pesan ini
    if (this.processedMessageIds.has(message.id)) {
      return;
    }
    
    // Tandai sebagai diproses dan catat penggunaan
    this.processedMessageIds.add(message.id);
    this.stepUsages.push({
      messageId: message.id,
      timestamp: new Date().toISOString(),
      usage: message.usage,
      costUSD: this.calculateCost(message.usage)
    });
  }
  
  private calculateCost(usage: any): number {
    // Implementasikan perhitungan harga Anda di sini
    // Ini adalah contoh yang disederhanakan
    const inputCost = usage.input_tokens * 0.00003;
    const outputCost = usage.output_tokens * 0.00015;
    const cacheReadCost = (usage.cache_read_input_tokens || 0) * 0.0000075;
    
    return inputCost + outputCost + cacheReadCost;
  }
}

// Penggunaan
const tracker = new CostTracker();
const { result, stepUsages, totalCost } = await tracker.trackConversation(
  "Analisis dan refaktor kode ini"
);

console.log(`Langkah diproses: ${stepUsages.length}`);
console.log(`Biaya total: $${totalCost.toFixed(4)}`);
```

```python Python
from claude_agent_sdk import query, AssistantMessage, ResultMessage
from datetime import datetime
import asyncio

class CostTracker:
    def __init__(self):
        self.processed_message_ids = set()
        self.step_usages = []

    async def track_conversation(self, prompt):
        result = None

        # Proses pesan saat tiba
        async for message in query(prompt=prompt):
            self.process_message(message)

            # Tangkap pesan hasil akhir
            if isinstance(message, ResultMessage):
                result = message

        return {
            "result": result,
            "step_usages": self.step_usages,
            "total_cost": result.total_cost_usd if result else 0
        }

    def process_message(self, message):
        # Hanya proses pesan asisten dengan penggunaan
        if not isinstance(message, AssistantMessage) or not hasattr(message, 'usage'):
            return

        # Lewati jika sudah memproses ID pesan ini
        message_id = getattr(message, 'id', None)
        if not message_id or message_id in self.processed_message_ids:
            return

        # Tandai sebagai diproses dan catat penggunaan
        self.processed_message_ids.add(message_id)
        self.step_usages.append({
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
            "usage": message.usage,
            "cost_usd": self.calculate_cost(message.usage)
        })

    def calculate_cost(self, usage):
        # Implementasikan perhitungan harga Anda
        input_cost = usage.get("input_tokens", 0) * 0.00003
        output_cost = usage.get("output_tokens", 0) * 0.00015
        cache_read_cost = usage.get("cache_read_input_tokens", 0) * 0.0000075

        return input_cost + output_cost + cache_read_cost

# Penggunaan
async def main():
    tracker = CostTracker()
    result = await tracker.track_conversation("Analisis dan refaktor kode ini")

    print(f"Langkah diproses: {len(result['step_usages'])}")
    print(f"Biaya total: ${result['total_cost']:.4f}")

asyncio.run(main())
```

</CodeGroup>

## Menangani Kasus Tepi

### Perbedaan Token Output

Dalam kasus yang jarang terjadi, Anda mungkin mengamati nilai `output_tokens` yang berbeda untuk pesan dengan ID yang sama. Ketika ini terjadi:

1. **Gunakan nilai tertinggi** - Pesan terakhir dalam grup biasanya berisi total yang akurat
2. **Verifikasi terhadap biaya total** - `total_cost_usd` dalam pesan hasil bersifat otoritatif
3. **Laporkan ketidakkonsistenan** - Ajukan masalah di [repositori GitHub Claude Code](https://github.com/anthropics/claude-code/issues)

### Pelacakan Token Cache

Ketika menggunakan prompt caching, lacak jenis token ini secara terpisah:

```typescript
interface CacheUsage {
  cache_creation_input_tokens: number;
  cache_read_input_tokens: number;
  cache_creation: {
    ephemeral_5m_input_tokens: number;
    ephemeral_1h_input_tokens: number;
  };
}
```

## Praktik Terbaik

1. **Gunakan ID Pesan untuk Deduplikasi**: Selalu lacak ID pesan yang diproses untuk menghindari penagihan ganda
2. **Pantau Pesan Hasil**: Hasil akhir berisi penggunaan kumulatif yang otoritatif
3. **Implementasikan Logging**: Catat semua data penggunaan untuk audit dan debugging
4. **Tangani Kegagalan dengan Baik**: Lacak penggunaan parsial bahkan jika percakapan gagal
5. **Pertimbangkan Streaming**: Untuk respons streaming, akumulasikan penggunaan saat pesan tiba

## Referensi Bidang Penggunaan

Setiap objek penggunaan berisi:

- `input_tokens`: Token input dasar yang diproses
- `output_tokens`: Token yang dihasilkan dalam respons
- `cache_creation_input_tokens`: Token yang digunakan untuk membuat entri cache
- `cache_read_input_tokens`: Token yang dibaca dari cache
- `service_tier`: Tingkat layanan yang digunakan (misalnya "standard")
- `total_cost_usd`: Biaya total dalam USD (hanya dalam pesan hasil)

## Contoh: Membangun Dashboard Penagihan

Berikut adalah cara mengagregasi data penggunaan untuk dashboard penagihan:

```typescript
class BillingAggregator {
  private userUsage = new Map<string, {
    totalTokens: number;
    totalCost: number;
    conversations: number;
  }>();
  
  async processUserRequest(userId: string, prompt: string) {
    const tracker = new CostTracker();
    const { result, stepUsages, totalCost } = await tracker.trackConversation(prompt);
    
    // Perbarui total pengguna
    const current = this.userUsage.get(userId) || {
      totalTokens: 0,
      totalCost: 0,
      conversations: 0
    };
    
    const totalTokens = stepUsages.reduce((sum, step) => 
      sum + step.usage.input_tokens + step.usage.output_tokens, 0
    );
    
    this.userUsage.set(userId, {
      totalTokens: current.totalTokens + totalTokens,
      totalCost: current.totalCost + totalCost,
      conversations: current.conversations + 1
    });
    
    return result;
  }
  
  getUserBilling(userId: string) {
    return this.userUsage.get(userId) || {
      totalTokens: 0,
      totalCost: 0,
      conversations: 0
    };
  }
}
```

## Dokumentasi Terkait

- [Referensi SDK TypeScript](/docs/id/agent-sdk/typescript) - Dokumentasi API lengkap
- [Ringkasan SDK](/docs/id/agent-sdk/overview) - Memulai dengan SDK
- [Izin SDK](/docs/id/agent-sdk/permissions) - Mengelola izin alat