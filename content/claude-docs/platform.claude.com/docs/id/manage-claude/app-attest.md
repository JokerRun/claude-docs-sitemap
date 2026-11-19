---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/app-attest
fetched_at: 2026-11-19T02:13:30.221159Z
sha256: 0a8402f8865067bfe7ccfabcbf2ec92c86683cbaa67aed80f024955d1cbe8fbf
---

---
title: App Attest untuk aplikasi iOS dan macOS
url: https://platform.claude.com/docs/id/manage-claude/app-attest
description: Izinkan instalasi asli aplikasi iOS atau macOS Anda memanggil Claude API tanpa menyertakan kunci API atau menjalankan proxy, menggunakan layanan App Attest dari Apple.
---

App Attest mengautentikasi aplikasi iOS dan macOS yang memanggil Claude API langsung dari perangkat, dengan penggunaan yang ditagihkan ke workspace Anda. Halaman ini menjelaskan cara kerja App Attest, cara mendaftarkan aplikasi Anda di Claude Console, dan cara mencabut integrasi aplikasi.

Aplikasi menggunakan App Attest melalui paket Swift [Claude for Foundation Models](https://github.com/anthropics/ClaudeForFoundationModels), yang masih dalam versi beta: paket ini memerlukan OS 27 beta, dan API mungkin berubah selama masa beta. Untuk konfigurasi Swift, lihat [Apple Foundation Models](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models#app-attest-production).

## Cara kerja App Attest

Setiap instalasi aplikasi Anda menggunakan layanan [App Attest](https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity) dari Apple untuk membuktikan bahwa aplikasi tersebut adalah build asli yang tidak dimodifikasi dari aplikasi yang Anda daftarkan. Anthropic kemudian menerbitkan “access token” (token akses) berumur pendek untuk perangkat tersebut yang menagihkan penggunaan ke workspace Anda. Aplikasi tidak menyertakan kunci API, dan tidak ada proxy yang perlu Anda operasikan.

Autentikasi App Attest hanya tersedia ketika aplikasi Anda memanggil Claude API secara langsung. Autentikasi ini tidak tersedia melalui Amazon Bedrock, Google Cloud, atau Microsoft Foundry.

Saat pertama kali aplikasi Anda menggunakan Claude di sebuah perangkat, aplikasi meminta challenge dari Anthropic, melakukan atestasi perangkat dengan `DCAppAttestService` milik Apple, dan menukarkan atestasi yang telah diverifikasi dengan “access token” (token akses). Paket Claude for Foundation Models menjalankan alur ini secara otomatis dan meminta token baru saat token lama kedaluwarsa; tidak ada kode atestasi yang perlu Anda tulis.

Token dibatasi cakupannya pada workspace Anda, kedaluwarsa setelah 1 jam, dan hanya mengotorisasi panggilan [Messages API](https://platform.claude.com/docs/id/api/messages/create). Token tidak membawa identitas pengguna akhir: App Attest mengidentifikasi aplikasi Anda, bukan orang yang menggunakannya, jadi tangani logika per pengguna apa pun di dalam aplikasi Anda.

## Menyiapkan App Attest

<Note>
  App Attest memerlukan perangkat fisik. Simulator, dan perangkat keras tanpa Secure Enclave, tidak dapat melakukan App Attest. Saat mengembangkan di Simulator, lakukan autentikasi dengan “API key” ([kunci API](https://platform.claude.com/docs/id/manage-claude/authentication#api-keys)) sebagai gantinya.
</Note>

Untuk menyiapkan App Attest, Anda memerlukan Apple Developer Team ID Anda dan peran admin di organisasi Claude Console Anda. Konfigurasikan proyek Xcode Anda dan daftarkan aplikasi Anda di [Claude Console](https://platform.claude.com/):

1. Di Xcode, tambahkan kapabilitas **App Attest** ke target aplikasi Anda di bawah **Signing & Capabilities**.
2. Di Claude Console, buka halaman [App integrations](https://platform.claude.com/settings/app-integrations) (`platform.claude.com/settings/app-integrations`) dan klik **Create app integration**.
3. Masukkan nama. Dari menu dropdown **Ruang kerja**, pilih workspace yang akan ditagih untuk penggunaan aplikasi tersebut. Setiap integrasi aplikasi dimiliki oleh satu workspace, yang tidak dapat Anda ubah nanti.
4. Masukkan Apple Developer Team ID Anda dan satu atau lebih bundle ID (hingga 32), lalu klik **Create app integration**.
5. Salin client ID (`clid_...`) dari tab **Ringkasan** integrasi tersebut.
6. Di aplikasi Anda, teruskan client ID ke [`.appAttest(clientID:)`](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models#app-attest-production).

## Mencabut integrasi aplikasi

Untuk menghentikan aplikasi yang telah disusupi atau sudah tidak digunakan lagi, cabut integrasinya. Pencabutan bersifat permanen dan mencakup setiap bundle ID dalam integrasi tersebut. Pencabutan akan mencabut token-token integrasi yang masih berlaku, dan perangkat tidak dapat lagi meminta token baru.

1. Di Claude Console, buka halaman [App integrations](https://platform.claude.com/settings/app-integrations) (`platform.claude.com/settings/app-integrations`).
2. Temukan integrasi tersebut. Daftar ini mencakup setiap workspace di organisasi Anda, dan kolom **Ruang kerja** menunjukkan workspace tempat setiap integrasi berada. Untuk mempersempit daftar ke satu workspace, pilih workspace tersebut di filter **Ruang kerja**.
3. Di ujung baris integrasi, buka menu **Tindakan lainnya** (tiga titik) dan pilih **Cabut**, lalu konfirmasi.

Untuk memulihkan akses, buat integrasi aplikasi baru dan perbarui aplikasi Anda agar menggunakan client ID-nya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Apple Foundation Models" icon="code" href="https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models#app-attest-production">
    Konfigurasikan App Attest dalam paket Swift Claude for Foundation Models
  </Card>

  <Card title="Autentikasi" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/authentication">
    Bandingkan kunci API, Workload Identity Federation, dan App Attest
  </Card>
</CardGroup>
