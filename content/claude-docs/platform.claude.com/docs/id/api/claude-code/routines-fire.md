---
source: platform
url: https://platform.claude.com/docs/id/api/claude-code/routines-fire
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 4547216ea16dfec1461c62026dabcfc2fbd080a78b45fdb6b98d2b2c17776491
---

# Memicu rutinitas melalui API

Mulai sesi rutinitas Claude Code sesuai permintaan dengan mengirimkan permintaan POST yang terautentikasi.

---

<Warning>
Ini adalah API eksperimental. Bentuk permintaan dan respons, batas laju, dan semantik token mungkin berubah. Perubahan yang merusak dikirimkan di balik versi header beta bertanggal baru, dan dua versi header sebelumnya terus berfungsi sehingga pemanggil memiliki waktu untuk bermigrasi.
</Warning>

[Claude Code](https://code.claude.com/docs) adalah alat pengkodean agentic Anthropic. [Claude Code di web](https://code.claude.com/docs/en/claude-code-on-the-web) menjalankan sesi Claude Code pada infrastruktur cloud yang dikelola Anthropic di claude.ai/code, dan [rutinitas](https://code.claude.com/docs/en/routines) adalah konfigurasi yang disimpan di sana: prompt, satu atau lebih repositori, dan konektor, dikemas sehingga dapat berjalan tanpa pengawasan sesuai jadwal, sebagai respons terhadap peristiwa GitHub, atau ketika dipanggil melalui HTTP.

Titik akhir ini adalah titik masuk HTTP. POSTing ke dalamnya memulai proses baru dari rutinitas yang ada dan mengembalikan ID sesi dan URL yang dihasilkan. Pemanggil khas adalah sistem peringatan, saluran CI, dan alat internal yang perlu memulai sesi Claude Code secara terprogram.

Memanggil titik akhir ini memerlukan akun claude.ai pada paket Pro, Max, Team, atau Enterprise dengan [Claude Code di web](https://code.claude.com/docs/en/claude-code-on-the-web) diaktifkan. Autentikasi dengan token pembawa per-rutinitas yang dibuat di UI web Claude Code daripada kunci API Anthropic.

## Perbedaan dari Claude Platform

Titik akhir rutinitas fire termasuk dalam permukaan produk Claude Code, yang berbeda dari API dan SDK Claude Platform dalam beberapa cara:

| Aspek | Titik akhir ini | API Anthropic lainnya |
| :--- | :--- | :--- |
| Autentikasi | `Authorization: Bearer` dengan token per-rutinitas (`sk-ant-oat01-...`) yang dibuat di [claude.ai/code/routines](https://claude.ai/code/routines) | `x-api-key` dengan kunci API Anthropic dari Claude Console |
| Cakupan token | Satu rutinitas saja; tidak ada akses baca | Tingkat ruang kerja |
| Dukungan SDK | Tidak ada | Tersedia di semua [SDK klien](/docs/id/api/client-sdks) |
| Penagihan | Penggunaan langganan Claude Code di claude.ai | Penggunaan Claude Platform |
| Namespace jalur | `/v1/claude_code/...` | `/v1/...` |
| Stabilitas | Eksperimental; memerlukan `anthropic-beta: experimental-cc-routine-2026-04-01` | Stabil atau beta standar |

## Sebelum Anda mulai

Untuk memanggil titik akhir ini, Anda memerlukan:

1. Rutinitas yang dibuat di [claude.ai/code/routines](https://claude.ai/code/routines)
2. Token pembawa yang dihasilkan untuk rutinitas tersebut: buka rutinitas untuk pengeditan, klik **Add another trigger** di bawah **Select a trigger**, pilih **API**, lalu klik **Generate token** di modal. Token ditampilkan sekali dan tidak dapat diambil kembali nanti.

Lihat [Add an API trigger](https://code.claude.com/docs/en/routines#add-an-api-trigger) dalam dokumentasi Claude Code untuk panduan pengaturan lengkap.

## Memicu rutinitas

```http
POST https://api.anthropic.com/v1/claude_code/routines/{routine_id}/fire
```

Setiap permintaan harus menyertakan header `anthropic-beta: experimental-cc-routine-2026-04-01`. Permintaan tanpa header ini mengembalikan `400 invalid_request_error`.

UI web Claude Code menyediakan URL lengkap bersama token ketika Anda menambahkan pemicu API, jadi sebagian besar integrasi menyimpan keduanya sebagai rahasia dan memanggil titik akhir secara langsung. Contoh di bawah menunjukkan panggilan shell dan langkah GitHub Actions yang memicu rutinitas pada kegagalan CI.

```bash Shell
curl -X POST https://api.anthropic.com/v1/claude_code/routines/$ROUTINE_ID/fire \
  -H "Authorization: Bearer $ROUTINE_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Sentry alert SEN-4521 fired in prod. Stack trace attached."}'
```

```yaml GitHub Actions
- if: failure()
  env:
    ROUTINE_FIRE_URL: ${{ secrets.ROUTINE_FIRE_URL }}
    ROUTINE_FIRE_TOKEN: ${{ secrets.ROUTINE_FIRE_TOKEN }}
  run: |
    curl -X POST "$ROUTINE_FIRE_URL" \
      -H "Authorization: Bearer $ROUTINE_FIRE_TOKEN" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
      -H "Content-Type: application/json" \
      -d "{\"text\": \"CI failed: $GITHUB_WORKFLOW run $GITHUB_RUN_ID on $GITHUB_REF\"}"
```

Permintaan kembali setelah sesi dibuat. Ini tidak melakukan streaming output sesi atau menunggu sesi selesai.

### Header

| Nama | Diperlukan | Deskripsi |
| :--- | :--- | :--- |
| `Authorization` | Ya | `Bearer <token>`. Token per-rutinitas yang dibuat di UI web Claude Code, dengan awalan `sk-ant-oat01-`. |
| `anthropic-beta` | Ya | Harus menyertakan `experimental-cc-routine-2026-04-01`. |
| `anthropic-version` | Ya | [Versi API](/docs/id/api/versioning), misalnya `2023-06-01`. |
| `Content-Type` | Ketika badan ada | `application/json`. |

### Parameter jalur

| Nama | Tipe | Deskripsi |
| :--- | :--- | :--- |
| `routine_id` | string | Pengenal rutinitas. Meskipun nama parameter, nilainya diawali `trig_` daripada `routine_`. Disertakan dalam URL yang ditampilkan modal ketika Anda menambahkan pemicu API. |

### Badan permintaan

| Bidang | Tipe | Diperlukan | Deskripsi |
| :--- | :--- | :--- | :--- |
| `text` | string | Tidak | Konteks awal untuk proses ini, seperti badan peringatan, baris log yang gagal, atau git diff. Nilainya adalah teks bentuk bebas dan tidak diuraikan; jika Anda mengirim JSON atau muatan terstruktur lainnya, rutinitas menerimanya sebagai string literal. Dilewatkan ke rutinitas bersama prompt yang disimpannya. Maksimal 65.536 karakter. |

Badan bersifat opsional. Bidang yang tidak dikenal dalam badan diabaikan.

### Respons

Permintaan yang berhasil mengembalikan `200 OK` dengan detail sesi baru:

```json
{
  "type": "routine_fire",
  "claude_code_session_id": "session_01HJKLMNOPQRSTUVWXYZ",
  "claude_code_session_url": "https://claude.ai/code/session_01HJKLMNOPQRSTUVWXYZ"
}
```

| Bidang | Tipe | Deskripsi |
| :--- | :--- | :--- |
| `type` | string | Selalu `routine_fire`. |
| `claude_code_session_id` | string | ID sesi Claude Code yang dibuat untuk proses ini. |
| `claude_code_session_url` | string | Tautan ke sesi di claude.ai. Buka di browser untuk menonton proses, meninjau perubahan, atau melanjutkan percakapan. |

### Kesalahan

Kesalahan menggunakan [amplop kesalahan](/docs/id/api/errors) Anthropic standar:

```json
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "<string>"
  }
}
```

| Status HTTP | Tipe kesalahan | Penyebab |
| :--- | :--- | :--- |
| 400 | `invalid_request_error` | Header `anthropic-beta` yang hilang atau tidak valid, `text` melebihi 65.536 karakter, atau rutinitas [dijeda](https://code.claude.com/docs/en/routines#edit-and-control-routines). |
| 401 | `authentication_error` | Tidak ada token pembawa di header `Authorization`, atau token tidak cocok dengan rutinitas ini. |
| 403 | `permission_error` | Akun atau organisasi tidak memiliki akses ke titik akhir ini. |
| 404 | `not_found_error` | Rutinitas tidak ada. |
| 429 | `rate_limit_error` | Batas jalankan rutinitas akun atau batas penggunaan telah tercapai. Respons menyertakan header `Retry-After` yang menunjukkan kapan jendela direset. |
| 500 | `api_error` | Kesalahan server yang tidak terduga. |
| 503 | `overloaded_error` | Layanan sementara kelebihan beban. Coba lagi setelah penundaan singkat. Claude Platform mengembalikan 529 untuk tipe kesalahan ini; titik akhir ini mengembalikan 503. |

## Autentikasi

Token pembawa dibatasi pada satu rutinitas. Token yang dikompromikan hanya dapat memicu rutinitas itu; token tidak memberikan akses baca, tidak ada akses ke rutinitas lain, dan tidak ada akses ke data akun.

Hasilkan dan cabut token dari pengaturan pemicu API rutinitas di [claude.ai/code/routines](https://claude.ai/code/routines). Tidak ada API publik untuk manajemen token. Menghasilkan token baru mencabut token sebelumnya.

## Idempotency

Setiap permintaan yang berhasil membuat sesi baru. Tidak ada kunci idempotency. Jika pemanggil webhook mencoba lagi, titik akhir membuat beberapa sesi.

## Batas laju

Proses rutinitas dihitung terhadap tunjangan harian per-akun yang bervariasi menurut paket, dan sesi yang dihasilkan mengurangi penggunaan langganan Claude Code yang sama dengan sesi interaktif. Ketika salah satu batas tercapai, titik akhir mengembalikan `429 rate_limit_error` dengan header `Retry-After`. Organisasi dengan penggunaan ekstra yang diaktifkan terus melampaui tunjangan yang disertakan pada overage terukur.

Proses harian yang tersisa ditampilkan di [claude.ai/code/routines](https://claude.ai/code/routines). Untuk cara penggunaan rutinitas berinteraksi dengan batas langganan dan penagihan overage ekstra, lihat [Usage and limits](https://code.claude.com/docs/en/routines#usage-and-limits) dalam dokumentasi Claude Code.

## Dukungan SDK

Titik akhir ini tidak ada di SDK Anthropic. Model tokennya berbeda dari autentikasi kunci API, dan pemanggil khas seperti pekerjaan CI dan webhook peringatan mengirim permintaan secara langsung.

## Lihat juga

- [Automate work with routines](https://code.claude.com/docs/en/routines) dalam dokumentasi Claude Code
- [Beta headers](/docs/id/api/beta-headers)
- [Errors](/docs/id/api/errors)