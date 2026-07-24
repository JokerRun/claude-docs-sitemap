---
source: platform
url: https://platform.claude.com/docs/id/api/claude-code/routines-fire
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 7fb3b1af73dbbed1a09fb87b7522d988e36c305c58ccc21486f32493b1aae00a
---

# Memicu routine melalui API

Mulai sesi routine Claude Code sesuai permintaan dengan mengirimkan permintaan POST yang terautentikasi.

---

<Warning>
  Ini adalah API eksperimental. Bentuk permintaan dan respons, batas laju, dan semantik token dapat berubah. Perubahan yang merusak kompatibilitas dirilis di balik versi header beta bertanggal yang baru, dan dua versi header sebelumnya tetap berfungsi sehingga pemanggil memiliki waktu untuk bermigrasi.
</Warning>

[Claude Code](https://code.claude.com/docs) adalah alat pemrograman agentik dari Anthropic. [Claude Code di web](https://code.claude.com/docs/en/claude-code-on-the-web) menjalankan sesi Claude Code pada infrastruktur cloud yang dikelola Anthropic di claude.ai/code, dan [routine](https://code.claude.com/docs/en/routines) adalah konfigurasi tersimpan di sana: sebuah prompt, satu atau lebih repositori, dan konektor, yang dikemas sehingga dapat berjalan tanpa pengawasan sesuai jadwal, sebagai respons terhadap peristiwa GitHub, atau saat dipanggil melalui HTTP.

Endpoint ini adalah titik masuk HTTP. Mengirim POST ke endpoint ini memulai eksekusi baru dari routine yang sudah ada dan mengembalikan ID sesi serta URL yang dihasilkan. Pemanggil yang umum adalah sistem peringatan, pipeline CI, dan alat internal yang perlu memulai sesi Claude Code secara terprogram.

Memanggil endpoint ini memerlukan akun claude.ai pada paket Pro, Max, Team, atau Enterprise dengan [Claude Code di web](https://code.claude.com/docs/en/claude-code-on-the-web) diaktifkan. Autentikasi dengan bearer token per-routine yang dibuat di UI web Claude Code, bukan dengan kunci API Claude.

## Perbedaan dari Claude Platform

Endpoint pemicu routine termasuk dalam permukaan produk Claude Code, yang berbeda dari API dan SDK Claude Platform dalam beberapa hal:

| Aspek          | Endpoint ini                                                                                                                                    | API Claude Platform                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Autentikasi    | `Authorization: Bearer` dengan token per-routine (`sk-ant-oat01-...`) yang dibuat di [claude.ai/code/routines](https://claude.ai/code/routines) | `x-api-key` dengan kunci API Claude dari Claude Console             |
| Cakupan token  | Hanya satu routine; tanpa akses baca                                                                                                            | Tingkat workspace                                                   |
| Dukungan SDK   | Tidak ada                                                                                                                                       | Tersedia di semua [SDK klien](/docs/id/cli-sdks-libraries/overview) |
| Penagihan      | Penggunaan langganan Claude Code di claude.ai                                                                                                   | Penggunaan Claude Platform                                          |
| Namespace path | `/v1/claude_code/...`                                                                                                                           | `/v1/...`                                                           |
| Stabilitas     | Eksperimental; memerlukan `anthropic-beta: experimental-cc-routine-2026-04-01`                                                                  | Stabil atau beta standar                                            |

## Sebelum Anda mulai

Untuk memanggil endpoint ini, Anda memerlukan:

1. Routine yang dibuat di [claude.ai/code/routines](https://claude.ai/code/routines).
2. Bearer token yang dihasilkan untuk routine tersebut: buka routine untuk diedit, klik **Add another trigger** di bawah **Select a trigger**, pilih **API**, lalu klik **Generate token** di jendela modal. Token hanya ditampilkan sekali dan tidak dapat diambil kembali nanti.

Lihat [Add an API trigger](https://code.claude.com/docs/en/routines#add-an-api-trigger) di dokumentasi Claude Code untuk panduan penyiapan lengkap.

## Memicu routine

```http
POST https://api.anthropic.com/v1/claude_code/routines/{routine_id}/fire
```

Setiap permintaan harus menyertakan header `anthropic-beta: experimental-cc-routine-2026-04-01`. Permintaan tanpa header ini mengembalikan `400 invalid_request_error`.

UI web Claude Code menyediakan URL lengkap bersama dengan token saat Anda menambahkan pemicu API, sehingga sebagian besar integrasi menyimpan keduanya sebagai secret dan memanggil endpoint secara langsung. Contoh berikut menunjukkan panggilan shell dan langkah GitHub Actions yang memicu routine saat CI gagal.

```bash cURL
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

Permintaan mengembalikan respons setelah sesi dibuat. Permintaan ini tidak melakukan streaming output sesi atau menunggu sesi selesai.

### Header

| Nama                | Wajib         | Deskripsi                                                                                             |
| ------------------- | ------------- | ----------------------------------------------------------------------------------------------------- |
| `Authorization`     | Ya            | `Bearer <token>`. Token per-routine yang dibuat di UI web Claude Code, dengan awalan `sk-ant-oat01-`. |
| `anthropic-beta`    | Ya            | Harus menyertakan `experimental-cc-routine-2026-04-01`.                                               |
| `anthropic-version` | Ya            | [Versi API](/docs/id/api/versioning), misalnya `2023-06-01`.                                          |
| `Content-Type`      | Saat body ada | `application/json`.                                                                                   |

### Parameter path

| Nama         | Tipe   | Deskripsi                                                                                                                                                                                         |
| ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `routine_id` | string | Pengidentifikasi routine. Meskipun nama parameternya demikian, nilainya berawalan `trig_` bukan `routine_`. Disertakan dalam URL yang ditampilkan jendela modal saat Anda menambahkan pemicu API. |

### Body permintaan

| Field  | Tipe   | Wajib | Deskripsi                                                                                                                                                                                                                                                                                                                            |
| ------ | ------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `text` | string | Tidak | Konteks awal untuk eksekusi ini, seperti isi peringatan, baris log yang gagal, atau git diff. Nilainya adalah teks bebas dan tidak diurai; jika Anda mengirim JSON atau payload terstruktur lainnya, routine menerimanya sebagai string literal. Diteruskan ke routine bersama dengan prompt tersimpannya. Maksimum 65.536 karakter. |

Body bersifat opsional. Field yang tidak dikenal dalam body akan diabaikan.

### Respons

Permintaan yang berhasil mengembalikan `200 OK` dengan detail sesi baru:

```json
{
  "type": "routine_fire",
  "claude_code_session_id": "session_01HJKLMNOPQRSTUVWXYZ",
  "claude_code_session_url": "https://claude.ai/code/session_01HJKLMNOPQRSTUVWXYZ"
}
```

| Field                     | Tipe   | Deskripsi                                                                                                              |
| ------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------- |
| `type`                    | string | Selalu `routine_fire`.                                                                                                 |
| `claude_code_session_id`  | string | ID sesi Claude Code yang dibuat untuk eksekusi ini.                                                                    |
| `claude_code_session_url` | string | Tautan ke sesi di claude.ai. Buka di browser untuk memantau eksekusi, meninjau perubahan, atau melanjutkan percakapan. |

### Error

Error menggunakan [amplop error](/docs/id/api/errors) standar Anthropic:

```json
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "<string>"
  }
}
```

| Status HTTP | Tipe error              | Penyebab                                                                                                                                                                                                       |
| ----------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 400         | `invalid_request_error` | Header `anthropic-beta` hilang atau tidak valid, `text` melebihi 65.536 karakter, atau routine dijeda (lihat [Edit and control routines](https://code.claude.com/docs/en/routines#edit-and-control-routines)). |
| 401         | `authentication_error`  | Tidak ada bearer token di header `Authorization`, atau token tidak cocok dengan routine ini.                                                                                                                   |
| 403         | `permission_error`      | Akun atau organisasi tidak memiliki akses ke endpoint ini.                                                                                                                                                     |
| 404         | `not_found_error`       | Routine tidak ada.                                                                                                                                                                                             |
| 429         | `rate_limit_error`      | Batas eksekusi routine atau batas penggunaan akun telah tercapai. Respons menyertakan header `Retry-After` yang menunjukkan kapan jendela waktu direset.                                                       |
| 500         | `api_error`             | Error server yang tidak terduga. Coba lagi dengan exponential backoff; jika error berlanjut, hubungi dukungan dengan menyertakan ID permintaan.                                                                |
| 503         | `overloaded_error`      | Layanan sedang kelebihan beban sementara. Coba lagi setelah jeda singkat. Claude Platform mengembalikan 529 untuk tipe error ini; endpoint ini mengembalikan 503.                                              |

## Autentikasi

Bearer token dibatasi cakupannya pada satu routine. Token yang bocor hanya dapat memicu routine tersebut; token tidak memberikan akses baca, tidak memberikan akses ke routine lain, dan tidak memberikan akses ke data akun.

Hasilkan dan cabut token dari pengaturan pemicu API routine di [claude.ai/code/routines](https://claude.ai/code/routines). Tidak ada API publik untuk manajemen token. Menghasilkan token baru akan mencabut token sebelumnya.

## Idempotensi

Setiap permintaan yang berhasil membuat sesi baru. Tidak ada kunci idempotensi. Jika pemanggil webhook mencoba ulang, endpoint akan membuat beberapa sesi.

## Batas laju

Eksekusi routine dihitung terhadap jatah harian per-akun yang bervariasi menurut paket, dan sesi yang dihasilkan menggunakan kuota penggunaan langganan Claude Code yang sama dengan sesi interaktif. Ketika salah satu batas tercapai, endpoint mengembalikan `429 rate_limit_error` dengan header `Retry-After`. Organisasi dengan penggunaan ekstra yang diaktifkan dapat melanjutkan melewati jatah yang disertakan dengan kelebihan penggunaan berbasis meteran.

Lihat sisa eksekusi harian Anda di [claude.ai/code/routines](https://claude.ai/code/routines). Untuk bagaimana penggunaan routine berinteraksi dengan batas langganan dan penagihan penggunaan ekstra, lihat [Usage and limits](https://code.claude.com/docs/en/routines#usage-and-limits) di dokumentasi Claude Code.

## Dukungan SDK

Endpoint ini tidak tersedia di SDK Anthropic. Model tokennya berbeda dari autentikasi kunci API, dan pemanggil yang umum seperti job CI dan webhook peringatan mengirim permintaan secara langsung.

## Lihat juga

* [Otomatiskan pekerjaan dengan routine](https://code.claude.com/docs/en/routines) di dokumentasi Claude Code
* [Header beta](/docs/id/api/beta-headers)
* [Error](/docs/id/api/errors)
