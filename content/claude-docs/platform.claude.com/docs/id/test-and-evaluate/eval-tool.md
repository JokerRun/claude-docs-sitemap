---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/eval-tool
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 41b55ba432a1296fe361b9891fc583a46f60a7110ad918a65c34f234d129d336
---

# Menggunakan Alat Evaluasi

[Claude Console](/dashboard) menyediakan **alat Evaluasi** yang memungkinkan Anda menguji prompt Anda dalam berbagai skenario.

---

## Mengakses Fitur Evaluasi

Untuk memulai dengan alat Evaluasi:

1. Buka Claude Console dan navigasikan ke editor prompt.
2. Setelah menyusun prompt Anda, cari tab 'Evaluate' di bagian atas layar.

![Mengakses Fitur Evaluasi](/docs/images/access_evaluate.png)

<Tip>
  Pastikan prompt Anda menyertakan setidaknya 1-2 variabel dinamis menggunakan sintaks kurung kurawal ganda: \{\{variable}}. Ini diperlukan untuk membuat set pengujian evaluasi.
</Tip>

## Menghasilkan Prompt

Console menawarkan [prompt generator](/docs/id/build-with-claude/prompt-engineering/prompting-tools) bawaan yang didukung oleh Claude Sonnet 4.5:

<Steps>
  <Step title="Klik 'Generate Prompt'">
    Mengklik alat bantu 'Generate Prompt' akan membuka modal yang memungkinkan Anda memasukkan informasi tugas Anda.
  </Step>

  <Step title="Deskripsikan tugas Anda">
    Deskripsikan tugas yang Anda inginkan (misalnya, "Triase permintaan dukungan pelanggan yang masuk") dengan detail sebanyak atau sesedikit yang Anda inginkan. Semakin banyak konteks yang Anda sertakan, semakin Claude dapat menyesuaikan prompt yang dihasilkan dengan kebutuhan spesifik Anda.
  </Step>

  <Step title="Hasilkan prompt Anda">
    Mengklik tombol oranye 'Generate Prompt' di bagian bawah akan membuat Claude menghasilkan prompt berkualitas tinggi untuk Anda. Anda kemudian dapat menyempurnakan prompt tersebut lebih lanjut menggunakan layar Evaluasi di Console.
  </Step>
</Steps>

Fitur ini memudahkan pembuatan prompt dengan sintaks variabel yang sesuai untuk evaluasi.

![Prompt Generator](/docs/images/promptgenerator.png)

## Membuat Kasus Uji

Saat Anda mengakses layar Evaluasi, Anda memiliki beberapa opsi untuk membuat kasus uji:

1. Klik tombol '+ Add Row' di kiri bawah untuk menambahkan kasus secara manual.
2. Gunakan fitur 'Generate Test Case' agar Claude secara otomatis menghasilkan kasus uji untuk Anda.
3. Impor kasus uji dari file CSV.

Untuk menggunakan fitur 'Generate Test Case':

<Steps>
  <Step title="Klik 'Generate Test Case'">
    Claude akan menghasilkan kasus uji untuk Anda, satu baris setiap kali Anda mengklik tombol tersebut.
  </Step>

  <Step title="Edit logika pembuatan (opsional)">
    Anda juga dapat mengedit logika pembuatan kasus uji dengan mengklik dropdown panah di sebelah kanan tombol 'Generate Test Case', lalu klik 'Show generation logic' di bagian atas jendela Variables yang muncul. Anda mungkin perlu mengklik \`Generate' di kanan atas jendela ini untuk mengisi logika pembuatan awal.

    Mengedit ini memungkinkan Anda menyesuaikan dan menyempurnakan kasus uji yang dihasilkan Claude dengan presisi dan spesifisitas yang lebih tinggi.
  </Step>
</Steps>

Berikut adalah contoh layar Evaluasi yang telah terisi dengan beberapa kasus uji:

![Layar Evaluasi yang Terisi](/docs/images/eval_populated.png)

<Note>
  Jika Anda memperbarui teks prompt asli Anda, Anda dapat menjalankan kembali seluruh rangkaian evaluasi terhadap prompt baru untuk melihat bagaimana perubahan memengaruhi kinerja di semua kasus uji.
</Note>

## Tips untuk Evaluasi yang Efektif

<Accordion title="Struktur Prompt untuk Evaluasi">
  Untuk memaksimalkan alat Evaluasi, susun prompt Anda dengan format input dan output yang jelas. Sebagai contoh:

  ```text wrap
  In this task, you will generate a cute one sentence story that incorporates two elements: a color and a sound.
  The color to include in the story is:
  <color>
  {{COLOR}}
  </color>
  The sound to include in the story is:
  <sound>
  {{SOUND}}
  </sound>
  Here are the steps to generate the story:
  1. Think of an object, animal, or scene that is commonly associated with the color provided. For example, if the color is "blue", you might think of the sky, the ocean, or a bluebird.
  2. Imagine a simple action, event or scene involving the colored object/animal/scene you identified and the sound provided. For instance, if the color is "blue" and the sound is "whistle", you might imagine a bluebird whistling a tune.
  3. Describe the action, event or scene you imagined in a single, concise sentence. Focus on making the sentence cute, evocative and imaginative. For example: "A cheerful bluebird whistled a merry melody as it soared through the azure sky."
  Please keep your story to one sentence only. Aim to make that sentence as charming and engaging as possible while naturally incorporating the given color and sound.
  Write your completed one sentence story inside <story> tags.

  ```

  Struktur ini memudahkan untuk memvariasikan input (\{\{COLOR}} dan \{\{SOUND}}) dan mengevaluasi output secara konsisten.
</Accordion>

<Tip>
  Gunakan alat bantu 'Generate a prompt' di Console untuk membuat prompt dengan cepat menggunakan sintaks variabel yang sesuai untuk evaluasi.
</Tip>

## Memahami dan membandingkan hasil

Alat Evaluasi menawarkan beberapa fitur untuk membantu Anda menyempurnakan prompt Anda:

1. **Perbandingan berdampingan**: Bandingkan output dari dua atau lebih prompt untuk melihat dampak perubahan Anda dengan cepat.
2. **Penilaian kualitas**: Nilai kualitas respons pada skala 5 poin untuk melacak peningkatan kualitas respons per prompt.
3. **Versi prompt**: Buat versi baru dari prompt Anda dan jalankan kembali rangkaian pengujian untuk beriterasi dengan cepat dan meningkatkan hasil.

Dengan meninjau hasil di seluruh kasus uji dan membandingkan berbagai versi prompt, Anda dapat mengidentifikasi pola dan membuat penyesuaian yang tepat pada prompt Anda dengan lebih efisien.

Mulailah mengevaluasi prompt Anda hari ini untuk membangun aplikasi AI yang lebih tangguh dengan Claude!
