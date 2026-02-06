---
source: platform
url: https://platform.claude.com/docs/id/resources/prompt-library/website-wizard
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 1d88b7be6d68b1f57dd004f77c0a00a75a5d2c8fd0746c9e040536a7183c489f
---

# Wizard situs web

Buat situs web satu halaman berdasarkan spesifikasi pengguna.

---

> Salin prompt ini ke [Konsol](/docs/id/dashboard) pengembang kami untuk mencobanya sendiri!

|        | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sistem | Tugas Anda adalah membuat situs web satu halaman berdasarkan spesifikasi yang diberikan, dikirimkan sebagai file HTML dengan JavaScript dan CSS yang tertanam. Situs web harus menggabungkan berbagai fitur desain yang menarik dan interaktif, seperti menu dropdown, teks dan konten dinamis, tombol yang dapat diklik, dan lainnya. Pastikan desainnya menarik secara visual, responsif, dan ramah pengguna. Kode HTML, CSS, dan JavaScript harus terstruktur dengan baik, terorganisir secara efisien, dan berkomentar dengan tepat untuk keterbacaan dan pemeliharaan.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Pengguna | Buat situs web satu halaman untuk platform pembelajaran online bernama "EduQuest" dengan fitur dan bagian berikut:<br/><br/>1. Bilah navigasi tetap dengan tautan ke kategori kursus (Matematika, Sains, Bahasa, Seni) dan bilah pencarian.<br/>2. Bagian hero dengan latar belakang video yang menampilkan siswa belajar online, tagline dinamis yang berputar antara "Belajar dengan kecepatan Anda sendiri," "Temukan gairah baru," dan "Perluas wawasan Anda" setiap 3 detik, dan tombol "Mulai" yang mengarah ke katalog kursus.<br/>3. Bagian kursus unggulan yang menampilkan kartu kursus dengan placeholder untuk gambar kursus, judul, instruktur, dan deskripsi.<br/>4. Bagian "Jalur Pembelajaran" interaktif dengan kuis singkat untuk menentukan gaya belajar dan minat, serta tombol untuk memulai kuis.<br/>5. Bagian "Kisah Sukses" yang menampilkan testimonial dari siswa yang puas, dengan placeholder untuk teks testimonial dan nama siswa.<br/>6. Footer dengan tautan ke blog platform, FAQ, kebijakan privasi, dan tombol "Hubungi Kami" yang membuka jendela modal dengan formulir kontak dan informasi dukungan pelanggan.<br/><br/>Sertakan konten placeholder pengisi untuk latar belakang video, kartu kursus, dan testimonial. Sematkan gaya CSS dalam tag `<style>` di bagian `<head>` dan tempatkan kode JavaScript dalam tag `<script>` di akhir bagian `<body>`.<br/><br/>Kode JavaScript harus menangani tagline dinamis di bagian hero, berputar melalui tagline yang berbeda setiap 3 detik. |

## Contoh output

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduQuest - Online Learning Platform</title>
    <style>
        /* CSS Styles */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: #333;
            color: #fff;
            padding: 20px;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 999;
        }

        nav ul {
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: space-between;
        }

        nav ul li a {
            color: #fff;
            text-decoration: none;
            padding: 10px;
        }

        .hero {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }

        .hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
        }

        .hero p {
            font-size: 24px;
            margin-bottom: 40px;
        }

        .hero button {
            padding: 10px 20px;
            font-size: 18px;
            background-color: #333;
            color: #fff;
            border: none;
            cursor: pointer;
        }

        .featured-courses, .success-stories {
            padding: 40px;
        }

        .course-card {
            background-color: #f5f5f5;
            padding: 20px;
            margin-bottom: 20px;
        }

        .testimonial {
            background-color: #f5f5f5;
            padding: 20px;
            margin-bottom: 20px;
        }

        footer {
            background-color: #333;
            color: #fff;
            padding: 20px;
            text-align: center;
        }

        footer a {
            color: #fff;
            text-decoration: none;
            margin: 0 10px;
        }

        footer button {
            padding: 10px 20px;
            font-size: 18px;
            background-color: #fff;
            color: #333;
            border: none;
            cursor: pointer;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="#">Math</a></li>
                <li><a href="#">Science</a></li>
                <li><a href="#">Languages</a></li>
                <li><a href="#">Arts</a></li>
                <li><input type="text" placeholder="Search"></li>
            </ul>
        </nav>
    </header>

    <section class="hero">
        <video src="placeholder-video.mp4" autoplay loop muted></video>
        <h1>Welcome to EduQuest</h1>
        <p id="tagline">Learn at your own pace</p>
        <button>Get Started</button>
    </section>

    <section class="featured-courses">
        <h2>Featured Courses</h2>
        <div class="course-card">
            <img src="placeholder-course-image.jpg" alt="Course Image">
            <h3>Course Title</h3>
            <p>Instructor: John Doe</p>
            <p>Course description goes here.</p>
        </div>
        <div class="course-card">
            <img src="placeholder-course-image.jpg" alt="Course Image">
            <h3>Course Title</h3>
            <p>Instructor: Jane Smith</p>
            <p>Course description goes here.</p>
        </div>
    </section>

    <section class="success-stories">
        <h2>Success Stories</h2>
        <div class="testimonial">
            <p>"EduQuest helped me learn a new skill and advance my career. Highly recommended!"</p>
            <p>- John Doe</p>
        </div>
        <div class="testimonial">
            <p>"I never thought I could learn a new language online, but EduQuest made it possible. Thank you!"</p>
            <p>- Jane Smith</p>
        </div>
    </section>

    <footer>
        <a href="#">Blog</a>
        <a href="#">FAQ</a>
        <a href="#">Privacy Policy</a>
        <button>Contact Us</button>
    </footer>

    <script>
        // JavaScript Code
        const taglines = [
            "Learn at your own pace",
            "Discover new passions",
            "Expand your horizons"
        ];

        let index = 0;
        const taglineElement = document.getElementById("tagline");

        function rotateTagline() {
            taglineElement.textContent = taglines[index];
            index = (index + 1) % taglines.length;
        }

        setInterval(rotateTagline, 3000);
    </script>
</body>
</html>
```

> Kode ini membuat situs web satu halaman untuk "EduQuest" dengan fitur dan bagian berikut:
> 
> Bilah navigasi tetap dengan tautan ke kategori kursus (Matematika, Sains, Bahasa, Seni) dan bilah pencarian.
> 
> Bagian hero dengan latar belakang video placeholder, tagline dinamis yang berputar antara "Belajar dengan kecepatan Anda sendiri," "Temukan gairah baru," dan "Perluas wawasan Anda" setiap 3 detik, dan tombol "Mulai".
> 
> Bagian kursus unggulan yang menampilkan kartu kursus dengan placeholder untuk gambar kursus, judul, instruktur, dan deskripsi.
> 
> Bagian "Kisah Sukses" yang menampilkan testimonial dari siswa yang puas, dengan placeholder untuk teks testimonial dan nama siswa.
> 
> Footer dengan tautan ke blog platform, FAQ, kebijakan privasi, dan tombol "Hubungi Kami".
> 
> Gaya CSS disematkan dalam tag `<style>` di bagian `<head>`, dan kode JavaScript ditempatkan dalam tag `<script>` di akhir bagian `<body>`.
> 
> Kode JavaScript menangani tagline dinamis di bagian hero, berputar melalui tagline yang berbeda setiap 3 detik menggunakan fungsi setInterval.
> 
> Harap perhatikan bahwa latar belakang video, gambar kursus, dan testimonial adalah placeholder dan harus diganti dengan konten aktual.

## Permintaan API

<Tabs>
<Tab title="Python">

```python
import anthropic

client = anthropic.Anthropic( # defaults to os.environ.get("ANTHROPIC_API_KEY")
api_key="my_api_key",
)
message = client.messages.create(
  model="claude-opus-4-6",
  max_tokens=4000,
  temperature=0,
  system="Tugas Anda adalah membuat situs web satu halaman berdasarkan spesifikasi yang diberikan, dikirimkan sebagai file HTML dengan JavaScript dan CSS yang tertanam. Situs web harus menggabungkan berbagai fitur desain yang menarik dan interaktif, seperti menu dropdown, teks dan konten dinamis, tombol yang dapat diklik, dan lainnya. Pastikan desainnya menarik secara visual, responsif, dan ramah pengguna. Kode HTML, CSS, dan JavaScript harus terstruktur dengan baik, terorganisir secara efisien, dan berkomentar dengan tepat untuk keterbacaan dan pemeliharaan.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Buat situs web satu halaman untuk platform pembelajaran online bernama \"EduQuest\" dengan fitur dan bagian berikut: \n \n1. Bilah navigasi tetap dengan tautan ke kategori kursus (Matematika, Sains, Bahasa, Seni) dan bilah pencarian. \n \n2. Bagian hero dengan latar belakang video yang menampilkan siswa belajar online, tagline dinamis yang berputar antara \"Belajar dengan kecepatan Anda sendiri,\" \"Temukan gairah baru,\" dan \"Perluas wawasan Anda\" setiap 3 detik, dan tombol \"Mulai\" yang mengarah ke katalog kursus. \n \n3. Bagian kursus unggulan yang menampilkan kartu kursus dengan placeholder untuk gambar kursus, judul, instruktur, dan deskripsi. \n \n4. Bagian \"Jalur Pembelajaran\" interaktif dengan kuis singkat untuk menentukan gaya belajar dan minat, serta tombol untuk memulai kuis. \n \n5. Bagian \"Kisah Sukses\" yang menampilkan testimonial dari siswa yang puas, dengan placeholder untuk teks testimonial dan nama siswa. \n \n6. Footer dengan tautan ke blog platform, FAQ, kebijakan privasi, dan tombol \"Hubungi Kami\" yang membuka jendela modal dengan formulir kontak dan informasi dukungan pelanggan. \n \nSertakan konten placeholder pengisi untuk latar belakang video, kartu kursus, dan testimonial. Sematkan gaya CSS dalam tag `<style>` di bagian `<head>` dan tempatkan kode JavaScript dalam tag `<script>` di akhir bagian `<body>`. \n \nKode JavaScript harus menangani tagline dinamis di bagian hero, berputar melalui tagline yang berbeda setiap 3 detik."
        }
      ]
    }
  ]
)
print(message.content)

```

</Tab>

<Tab title="TypeScript">
```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
});

const msg = await anthropic.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4000,
  temperature: 0,
  system: "Tugas Anda adalah membuat situs web satu halaman berdasarkan spesifikasi yang diberikan, dikirimkan sebagai file HTML dengan JavaScript dan CSS yang tertanam. Situs web harus menggabungkan berbagai fitur desain yang menarik dan interaktif, seperti menu dropdown, teks dan konten dinamis, tombol yang dapat diklik, dan lainnya. Pastikan desainnya menarik secara visual, responsif, dan ramah pengguna. Kode HTML, CSS, dan JavaScript harus terstruktur dengan baik, terorganisir secara efisien, dan berkomentar dengan tepat untuk keterbacaan dan pemeliharaan.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Buat situs web satu halaman untuk platform pembelajaran online bernama \"EduQuest\" dengan fitur dan bagian berikut:  \n  \n1. Bilah navigasi tetap dengan tautan ke kategori kursus (Matematika, Sains, Bahasa, Seni) dan bilah pencarian.  \n  \n2. Bagian hero dengan latar belakang video yang menampilkan siswa belajar online, tagline dinamis yang berputar antara \"Belajar dengan kecepatan Anda sendiri,\" \"Temukan gairah baru,\" dan \"Perluas wawasan Anda\" setiap 3 detik, dan tombol \"Mulai\" yang mengarah ke katalog kursus.  \n  \n3. Bagian kursus unggulan yang menampilkan kartu kursus dengan placeholder untuk gambar kursus, judul, instruktur, dan deskripsi.  \n  \n4. Bagian \"Jalur Pembelajaran\" interaktif dengan kuis singkat untuk menentukan gaya belajar dan minat, serta tombol untuk memulai kuis.  \n  \n5. Bagian \"Kisah Sukses\" yang menampilkan testimonial dari siswa yang puas, dengan placeholder untuk teks testimonial dan nama siswa.  \n  \n6. Footer dengan tautan ke blog platform, FAQ, kebijakan privasi, dan tombol \"Hubungi Kami\" yang membuka jendela modal dengan formulir kontak dan informasi dukungan pelanggan.  \n  \nSertakan konten placeholder pengisi untuk latar belakang video, kartu kursus, dan testimonial. Sematkan gaya CSS dalam tag `<style>` di bagian `<head>` dan tempatkan kode JavaScript dalam tag `<script>` di akhir bagian `<body>`.  \n  \nKode JavaScript harus menangani tagline dinamis di bagian hero, berputar melalui tagline yang berbeda setiap 3 detik."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
<Tab title="AWS Bedrock Python">

```python
from anthropic import AnthropicBedrock

# See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock

# for authentication options

client = AnthropicBedrock()

message = client.messages.create(
  model="anthropic.claude-opus-4-6-v1",
  max_tokens=4000,
  temperature=0,
  system="Tugas Anda adalah membuat situs web satu halaman berdasarkan spesifikasi yang diberikan, dikirimkan sebagai file HTML dengan JavaScript dan CSS yang tertanam. Situs web harus menggabungkan berbagai fitur desain yang menarik dan interaktif, seperti menu dropdown, teks dan konten dinamis, tombol yang dapat diklik, dan lainnya. Pastikan desainnya menarik secara visual, responsif, dan ramah pengguna. Kode HTML, CSS, dan JavaScript harus terstruktur dengan baik, terorganisir secara efisien, dan berkomentar dengan tepat untuk keterbacaan dan pemeliharaan.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Buat situs web satu halaman untuk platform pembelajaran online bernama \"EduQuest\" dengan fitur dan bagian berikut: \n \n1. Bilah navigasi tetap dengan tautan ke kategori kursus (Matematika, Sains, Bahasa, Seni) dan bilah pencarian. \n \n2. Bagian hero dengan latar belakang video yang menampilkan siswa belajar online, tagline dinamis yang berputar antara \"Belajar dengan kecepatan Anda sendiri,\" \"Temukan gairah baru,\" dan \"Perluas wawasan Anda\" setiap 3 detik, dan tombol \"Mulai\" yang mengarah ke katalog kursus. \n \n3. Bagian kursus unggulan yang menampilkan kartu kursus dengan placeholder untuk gambar kursus, judul, instruktur, dan deskripsi. \n \n4. Bagian \"Jalur Pembelajaran\" interaktif dengan kuis singkat untuk menentukan gaya belajar dan minat, serta tombol untuk memulai kuis. \n \n5. Bagian \"Kisah Sukses\" yang menampilkan testimonial dari siswa yang puas, dengan placeholder untuk teks testimonial dan nama siswa. \n \n6. Footer dengan tautan ke blog platform, FAQ, kebijakan privasi, dan tombol \"Hubungi Kami\" yang membuka jendela modal dengan formulir kontak dan informasi dukungan pelanggan. \n \nSertakan konten placeholder pengisi untuk latar belakang video, kartu kursus, dan testimonial. Sematkan gaya CSS dalam tag `<style>` di bagian `<head>` dan tempatkan kode JavaScript dalam tag `<script>` di akhir bagian `<body>`. \n \nKode JavaScript harus menangani tagline dinamis di bagian hero, berputar melalui tagline yang berbeda setiap 3 detik."
        }
      ]
    }
  ]
)
print(message.content)

```

</Tab>
<Tab title="AWS Bedrock TypeScript">

```typescript

import AnthropicBedrock from '@anthropic-ai/bedrock-sdk';

// See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
// for authentication options
const client = new AnthropicBedrock();

const msg = await client.messages.create({
  model: "anthropic.claude-opus-4-6-v1",
  max_tokens: 4000,
  temperature: 0,
  system: "Tugas Anda adalah membuat situs web satu halaman berdasarkan spesifikasi yang diberikan, dikirimkan sebagai file HTML dengan JavaScript dan CSS yang tertanam. Situs web harus menggabungkan berbagai fitur desain yang menarik dan interaktif, seperti menu dropdown, teks dan konten dinamis, tombol yang dapat diklik, dan lainnya. Pastikan desainnya menarik secara visual, responsif, dan ramah pengguna. Kode HTML, CSS, dan JavaScript harus terstruktur dengan baik, terorganisir secara efisien, dan berkomentar dengan tepat untuk keterbacaan dan pemeliharaan.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Buat situs web satu halaman untuk platform pembelajaran online bernama \"EduQuest\" dengan fitur dan bagian berikut: \n \n1. Bilah navigasi tetap dengan tautan ke kategori kursus (Matematika, Sains, Bahasa, Seni) dan bilah pencarian. \n \n2. Bagian hero dengan latar belakang video yang menampilkan siswa belajar online, tagline dinamis yang berputar antara \"Belajar dengan kecepatan Anda sendiri,\" \"Temukan gairah baru,\" dan \"Perluas wawasan Anda\" setiap 3 detik, dan tombol \"Mulai\" yang mengarah ke katalog kursus. \n \n3. Bagian kursus unggulan yang menampilkan kartu kursus dengan placeholder untuk gambar kursus, judul, instruktur, dan deskripsi. \n \n4. Bagian \"Jalur Pembelajaran\" interaktif dengan kuis singkat untuk menentukan gaya belajar dan minat, serta tombol untuk memulai kuis. \n \n5. Bagian \"Kisah Sukses\" yang menampilkan testimonial dari siswa yang puas, dengan placeholder untuk teks testimonial dan nama siswa. \n \n6. Footer dengan tautan ke blog platform, FAQ, kebijakan privasi, dan tombol \"Hubungi Kami\" yang membuka jendela modal dengan formulir kontak dan informasi dukungan pelanggan. \n \nSertakan konten placeholder pengisi untuk latar belakang video, kartu kursus, dan testimonial. Sematkan gaya CSS dalam tag `<style>` di bagian `<head>` dan tempatkan kode JavaScript dalam tag `<script>` di akhir bagian `<body>`. \n \nKode JavaScript harus menangani tagline dinamis di bagian hero, berputar melalui tagline yang berbeda setiap 3 detik."
        }
      ]
    }
  ]
});
console.log(msg);

```
</Tab>

<Tab title="Vertex AI Python">

```python
from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
  model="claude-sonnet-4@20250514",
  max_tokens=4000,
  temperature=0,
  system="Tugas Anda adalah membuat situs web satu halaman berdasarkan spesifikasi yang diberikan, dikirimkan sebagai file HTML dengan JavaScript dan CSS yang tertanam. Situs web harus menggabungkan berbagai fitur desain yang menarik dan interaktif, seperti menu dropdown, teks dan konten dinamis, tombol yang dapat diklik, dan lainnya. Pastikan desainnya menarik secara visual, responsif, dan ramah pengguna. Kode HTML, CSS, dan JavaScript harus terstruktur dengan baik, terorganisir secara efisien, dan berkomentar dengan tepat untuk keterbacaan dan pemeliharaan.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Buat situs web satu halaman untuk platform pembelajaran online bernama \"EduQuest\" dengan fitur dan bagian berikut: \n \n1. Bilah navigasi tetap dengan tautan ke kategori kursus (Matematika, Sains, Bahasa, Seni) dan bilah pencarian. \n \n2. Bagian hero dengan latar belakang video yang menampilkan siswa belajar online, tagline dinamis yang berputar antara \"Belajar dengan kecepatan Anda sendiri,\" \"Temukan gairah baru,\" dan \"Perluas wawasan Anda\" setiap 3 detik, dan tombol \"Mulai\" yang mengarah ke katalog kursus. \n \n3. Bagian kursus unggulan yang menampilkan kartu kursus dengan placeholder untuk gambar kursus, judul, instruktur, dan deskripsi. \n \n4. Bagian \"Jalur Pembelajaran\" interaktif dengan kuis singkat untuk menentukan gaya belajar dan minat, serta tombol untuk memulai kuis. \n \n5. Bagian \"Kisah Sukses\" yang menampilkan testimonial dari siswa yang puas, dengan placeholder untuk teks testimonial dan nama siswa. \n \n6. Footer dengan tautan ke blog platform, FAQ, kebijakan privasi, dan tombol \"Hubungi Kami\" yang membuka jendela modal dengan formulir kontak dan informasi dukungan pelanggan. \n \nSertakan konten placeholder pengisi untuk latar belakang video, kartu kursus, dan testimonial. Sematkan gaya CSS dalam tag `<style>` di bagian `<head>` dan tempatkan kode JavaScript dalam tag `<script>` di akhir bagian `<body>`. \n \nKode JavaScript harus menangani tagline dinamis di bagian hero, berputar melalui tagline yang berbeda setiap 3 detik."
        }
      ]
    }
  ]
)
print(message.content)

```
</Tab>
<Tab title="Vertex AI TypeScript">

```typescript 
import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';

// Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
// Additionally goes through the standard `google-auth-library` flow.
const client = new AnthropicVertex();

const msg = await client.messages.create({
model: "claude-sonnet-4@20250514",
max_tokens: 4000,
temperature: 0,
system: "Tugas Anda adalah membuat situs web satu halaman berdasarkan spesifikasi yang diberikan, dikirimkan sebagai file HTML dengan JavaScript dan CSS yang tertanam. Situs web harus menggabungkan berbagai fitur desain yang menarik dan interaktif, seperti menu dropdown, teks dan konten dinamis, tombol yang dapat diklik, dan lainnya. Pastikan desainnya menarik secara visual, responsif, dan ramah pengguna. Kode HTML, CSS, dan JavaScript harus terstruktur dengan baik, terorganisir secara efisien, dan berkomentar dengan tepat untuk keterbacaan dan pemeliharaan.",
messages: [
{
"role": "user",
"content": [
{
"type": "text",
"text": "Buat situs web satu halaman untuk platform pembelajaran online bernama \"EduQuest\" dengan fitur dan bagian berikut: \n \n1. Bilah navigasi tetap dengan tautan ke kategori kursus (Matematika, Sains, Bahasa, Seni) dan bilah pencarian. \n \n2. Bagian hero dengan latar belakang video yang menampilkan siswa belajar online, tagline dinamis yang berputar antara \"Belajar dengan kecepatan Anda sendiri,\" \"Temukan gairah baru,\" dan \"Perluas wawasan Anda\" setiap 3 detik, dan tombol \"Mulai\" yang mengarah ke katalog kursus. \n \n3. Bagian kursus unggulan yang menampilkan kartu kursus dengan placeholder untuk gambar kursus, judul, instruktur, dan deskripsi. \n \n4. Bagian \"Jalur Pembelajaran\" interaktif dengan kuis singkat untuk menentukan gaya belajar dan minat, serta tombol untuk memulai kuis. \n \n5. Bagian \"Kisah Sukses\" yang menampilkan testimonial dari siswa yang puas, dengan placeholder untuk teks testimonial dan nama siswa. \n \n6. Footer dengan tautan ke blog platform, FAQ, kebijakan privasi, dan tombol \"Hubungi Kami\" yang membuka jendela modal dengan formulir kontak dan informasi dukungan pelanggan. \n \nSertakan konten placeholder pengisi untuk latar belakang video, kartu kursus, dan testimonial. Sematkan gaya CSS dalam tag `<style>` di bagian `<head>` dan tempatkan kode JavaScript dalam tag `<script>` di akhir bagian `<body>`. \n \nKode JavaScript harus menangani tagline dinamis di bagian hero, berputar melalui tagline yang berbeda setiap 3 detik."
}
]
}
]
});
console.log(msg);

```

</Tab>
</Tabs>