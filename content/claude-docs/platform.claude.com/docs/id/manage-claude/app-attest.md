---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/app-attest
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 0f248db27c3e36a76f7037a138ad101e0c8dc518ad6eda0ef52fc36ec7f924b7
---

---
title: App Attest untuk aplikasi iOS dan macOS
url: https://platform.claude.com/docs/id/manage-claude/app-attest
description: Izinkan instalasi asli aplikasi iOS atau macOS Anda memanggil Claude API tanpa menyertakan kunci API atau menjalankan proxy, menggunakan layanan App Attest dari Apple.
---

App Attest mengautentikasi aplikasi iOS dan macOS yang memanggil Claude API langsung dari perangkat, dengan penggunaan yang ditagihkan ke workspace Anda. Halaman ini menjelaskan cara kerja App Attest, cara mendaftarkan aplikasi Anda di Claude Console, dan cara mencabut integrasi aplikasi.

Aplikasi menggunakan App Attest melalui paket Swift [Claude for Foundation Models](https://github.com/anthropics/ClaudeForFoundationModels), yang masih dalam versi beta: paket ini memerlukan OS 27 beta, dan API mungkin berubah selama masa beta. Untuk konfigurasi Swift, lihat [Apple Foundation Models](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models#app-attest-production).

## Cara kerja App Attest

Setiap instalasi aplikasi Anda menggunakan layanan [App Attest](https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity) dari Apple untuk membuktikan bahwa aplikasi tersebut adalah build asli yang tidak dimodifikasi dari aplikasi yang Anda daftarkan. Anthropic kemudian menerbitkan "access token" (token akses) berumur pendek untuk perangkat tersebut yang menagihkan penggunaan ke workspace Anda. Aplikasi tidak menyertakan kunci API, dan tidak ada proxy yang perlu Anda operasikan.

Autentikasi App Attest hanya tersedia ketika aplikasi Anda memanggil Claude API secara langsung. Autentikasi ini tidak tersedia melalui Amazon Bedrock, Google Cloud, atau Microsoft Foundry.

Saat pertama kali aplikasi Anda menggunakan Claude di sebuah perangkat, aplikasi meminta challenge dari Anthropic, melakukan atestasi perangkat dengan `DCAppAttestService` milik Apple, dan menukarkan atestasi yang telah diverifikasi dengan "access token" (token akses). Paket Claude for Foundation Models menjalankan alur ini secara otomatis dan meminta token baru saat token lama kedaluwarsa; tidak ada kode atestasi yang perlu Anda tulis.

Token dibatasi cakupannya pada workspace Anda, kedaluwarsa setelah satu jam, dan hanya mengotorisasi panggilan [Messages API](https://platform.claude.com/docs/id/api/messages/create). Token tidak membawa identitas pengguna akhir: App Attest mengidentifikasi aplikasi Anda, bukan orang yang menggunakannya, jadi tangani logika per pengguna apa pun di dalam aplikasi Anda.

## Menyiapkan App Attest

<Note>
  App Attest memerlukan perangkat fisik. Simulator, dan perangkat keras tanpa Secure Enclave, tidak dapat melakukan App Attest. Saat mengembangkan di Simulator, lakukan autentikasi dengan "API key" ([kunci API](https://platform.claude.com/docs/id/manage-claude/authentication#api-keys)) sebagai gantinya.
</Note>

Untuk menyiapkan App Attest, Anda memerlukan Apple Developer Team ID Anda dan peran admin, owner, atau primary owner di organisasi Anda. Konfigurasikan proyek Xcode Anda dan daftarkan aplikasi Anda di [Claude Console](https://platform.claude.com/):

1. Di Xcode, tambahkan kapabilitas **App Attest** ke target aplikasi Anda di bawah **Signing & Capabilities**.
2. Di pengaturan workspace Anda di Claude Console, buka **App integrations**.
3. Klik **Create app integration** dan masukkan nama, Apple Developer Team ID Anda, dan satu atau lebih bundle ID (hingga 32).
4. Salin client ID (`clid_...`) dari tab **Overview** integrasi tersebut dan teruskan ke konfigurasi Claude aplikasi Anda.

## Mencabut integrasi aplikasi

Untuk menghentikan aplikasi yang telah disusupi atau dipensiunkan, cabut integrasinya: di pengaturan workspace Anda di Claude Console, buka **App integrations**, pilih integrasi tersebut, dan klik **Revoke**, lalu konfirmasi. Mencabut integrasi akan mencabut token-tokennya yang masih berlaku, dan perangkat terdaftarnya tidak dapat lagi meminta token baru. Pencabutan bersifat permanen, jadi buat integrasi aplikasi baru untuk memulihkan akses.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Apple Foundation Models" icon="code" href="https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models#app-attest-production">
    Konfigurasikan App Attest dalam paket Swift Claude for Foundation Models
  </Card>

  <Card title="Autentikasi" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/authentication">
    Bandingkan kunci API, Workload Identity Federation, dan App Attest
  </Card>
</CardGroup>
