---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/rate-limits-api
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 3e0a61f0de9bb823d395ca6a5ba72bf9402c18d7c48ce91cda019882d3ea7c13
---

# Rate Limits API

Kueri batas laju API organisasi Anda secara terprogram dengan Rate Limits API.

---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, atur organisasi Anda di **Console → Settings → Organization**.
</Tip>

Rate Limits API menyediakan akses terprogram ke "rate limits" (batas laju) yang dikonfigurasi untuk organisasi Anda dan workspace-nya. Ini adalah informasi yang sama dengan yang ditampilkan di halaman [Limits](/settings/limits) di Claude Console.

Gunakan API ini untuk:

* **Menjaga gateway dan proxy tetap sinkron:** Baca batas Anda saat ini pada saat startup dan secara terjadwal, alih-alih melakukan hardcode nilai yang akan menyimpang ketika Anthropic menyesuaikannya.
* **Mendukung peringatan internal:** Bandingkan data penggunaan dari [Usage and Cost API](/docs/id/manage-claude/usage-cost-api) dengan batas yang telah Anda konfigurasi.
* **Mengaudit konfigurasi workspace:** Verifikasi bahwa override workspace sesuai dengan yang diharapkan oleh otomatisasi provisioning Anda.

<Check>
  **Kunci Admin API diperlukan.** Endpoint ini memerlukan kunci Admin API, yang berbeda dari kunci API Claude standar. Lihat [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys) untuk mengetahui tempat membuatnya sesuai jenis organisasi Anda dan cakupan mana yang harus dipilih.
</Check>

## Mulai cepat

Tampilkan daftar batas laju yang dikonfigurasi untuk organisasi Anda:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rate_limits" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Batas laju organisasi

Endpoint `/v1/organizations/rate_limits` mengembalikan batas laju yang diterapkan di tingkat organisasi untuk Messages API dan sumber daya pendukungnya. Batas untuk produk lain, seperti [Claude Managed Agents](/docs/id/managed-agents/overview), tidak disertakan.

### Konsep utama

* **Grup batas laju:** Setiap entri dalam respons mewakili satu grup batas laju. Batas laju model dikelompokkan sehingga beberapa versi model berbagi satu set batas yang sama, dan grup lainnya mencakup sumber daya seperti Message Batches API, Files API, Token Counting API, agent skills, dan alat pencarian web.
* **`group_type`:** Mengidentifikasi kategori batas mana yang dicakup oleh entri tersebut. Lihat [Memfilter berdasarkan tipe grup](#filtering-by-group-type) untuk daftar nilainya.
* **Daftar `models`:** Untuk entri `model_group`, field `models` mencantumkan setiap ID model dan alias yang dihitung terhadap batas grup tersebut. Gunakan daftar ini untuk mencari grup mana yang mencakup string model apa pun. Untuk tipe grup lainnya, `models` bernilai `null`.
* **Daftar `limits`:** Setiap grup membawa daftar pasangan `{type, value}`. Field `type` mengidentifikasi pembatas (seperti `requests_per_minute`, `input_tokens_per_minute`, atau `output_tokens_per_minute`) dan `value` adalah batas yang dikonfigurasi. Lihat [Batas laju](/docs/id/api/rate-limits) untuk mengetahui bagaimana setiap pembatas diukur dan diterapkan.

Untuk detail parameter lengkap dan skema respons, lihat [referensi Organization Rate Limits API](/docs/id/api/admin/rate_limits/list).

### Menampilkan semua batas laju organisasi

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rate_limits" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "rate_limit",
      "group_type": "model_group",
      "models": [
        "claude-opus-4-5",
        "claude-opus-4-5-20251101",
        "claude-opus-4-6",
        "claude-opus-4-7",
        "claude-opus-4-8"
      ],
      "limits": [
        { "type": "requests_per_minute", "value": 4000 },
        { "type": "input_tokens_per_minute", "value": 10000000 },
        { "type": "output_tokens_per_minute", "value": 800000 }
      ]
    },
    {
      "type": "rate_limit",
      "group_type": "batch",
      "models": null,
      "limits": [{ "type": "enqueued_batch_requests", "value": 500000 }]
    }
  ],
  "next_page": null
}
```

### Mencari batas untuk model tertentu

Berikan ID model atau alias apa pun sebagai parameter kueri `model` untuk mengembalikan hanya entri yang memuatnya:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rate_limits?model=claude-opus-4-8" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Jika string model tidak cocok dengan grup mana pun, endpoint mengembalikan error 404. Parameter `model` hanya didukung pada endpoint organisasi; endpoint workspace tidak menerimanya.

## Batas laju workspace

Endpoint `/v1/organizations/workspaces/{workspace_id}/rate_limits` mengembalikan override batas laju yang dikonfigurasi untuk satu workspace.

Respons hanya menyertakan override, sehingga apa pun yang tidak ada di dalamnya diwarisi dari organisasi:

* Grup yang tidak ada dalam `data` tidak memiliki override workspace sama sekali. Workspace mewarisi batas tingkat organisasi untuk grup tersebut (bukan berarti tidak terbatas).
* Dalam grup yang ada, tipe pembatas yang tidak ada dalam `limits[]` tidak memiliki override workspace untuk pembatas tersebut. Workspace mewarisi nilai organisasi untuknya.
* Untuk setiap pembatas yang ada, `org_limit` adalah nilai tingkat organisasi untuk pembatas yang sama, atau `null` jika organisasi tidak memiliki batas yang dikonfigurasi untuk tipe pembatas tersebut.

Untuk detail parameter lengkap dan skema respons, lihat [referensi Workspace Rate Limits API](/docs/id/api/admin/workspaces/rate_limits/list).

<Tip>
  Untuk mengambil ID workspace organisasi Anda, gunakan endpoint [List Workspaces](/docs/id/api/admin/workspaces/list), atau temukan di [Claude Console](/settings/workspaces). Workspace default tidak dapat memiliki override batas laju, sehingga tidak memiliki entri pada endpoint ini; gunakan endpoint organisasi untuk membaca batasnya.
</Tip>

```bash cURL
curl "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/rate_limits" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "workspace_rate_limit",
      "group_type": "model_group",
      "models": [
        "claude-opus-4-5",
        "claude-opus-4-5-20251101",
        "claude-opus-4-6",
        "claude-opus-4-7",
        "claude-opus-4-8"
      ],
      "limits": [
        { "type": "requests_per_minute", "value": 1000, "org_limit": 4000 },
        { "type": "input_tokens_per_minute", "value": 500000, "org_limit": 10000000 }
      ]
    }
  ],
  "next_page": null
}
```

## Memfilter berdasarkan tipe grup

Kedua endpoint menerima parameter kueri opsional `group_type` yang membatasi respons ke satu kategori:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rate_limits?group_type=batch" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Nilai yang valid adalah `model_group`, `batch`, `token_count`, `files`, `skills`, dan `web_search`.

## Paginasi

Kedua endpoint menerima parameter kueri `page` dan mengembalikan field `next_page`. Respons saat ini selalu berupa satu halaman, sehingga `next_page` bernilai `null`. Lakukan perulangan pada `next_page` agar klien Anda melakukan paginasi dengan benar tanpa perubahan ketika respons bertambah besar.

## Pertanyaan yang sering diajukan

### String model apa yang muncul dalam daftar `models`?

Setiap ID model dan alias yang dihitung terhadap grup tersebut, termasuk ID bertanggal (seperti `claude-sonnet-4-5-20250929`) dan alias tanpa tanggal (seperti `claude-sonnet-4-5`). Cari string model apa pun yang Anda berikan ke Messages API dan Anda akan menemukannya di tepat satu entri `model_group`.

### Apa artinya jika sebuah grup tidak ada dalam respons workspace?

Workspace tidak memiliki override untuk grup tersebut dan mewarisi batas tingkat organisasi. Kueri endpoint organisasi untuk melihat nilai yang diwarisi.

### Bisakah saya memperbarui batas laju dengan API ini?

Tidak. Untuk mengatur batas laju workspace, buka workspace di [Claude Console](/settings/workspaces) dan gunakan tab **Limits**.

## Lihat juga

* [Batas laju](/docs/id/api/rate-limits)
* [Admin API](/docs/id/manage-claude/admin-api)
* [Referensi Admin API](/docs/id/api/admin)
* [Workspace](/docs/id/manage-claude/workspaces)
* [Usage and Cost API](/docs/id/manage-claude/usage-cost-api)
