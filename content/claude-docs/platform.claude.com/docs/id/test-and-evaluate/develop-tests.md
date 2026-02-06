---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/develop-tests
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 258f6b22f9e151e91370aca2d7887eed5fb8eb51258e8ef33793ca109fbe866e
---

# Buat evaluasi empiris yang kuat

Pelajari cara merancang evaluasi untuk mengukur kinerja LLM terhadap kriteria kesuksesan Anda.

---

Setelah menentukan kriteria kesuksesan Anda, langkah berikutnya adalah merancang evaluasi untuk mengukur kinerja LLM terhadap kriteria tersebut. Ini adalah bagian penting dari siklus prompt engineering.

![Flowchart of prompt engineering: test cases, preliminary prompt, iterative testing and refinement, final validation, ship](/docs/images/how-to-prompt-eng.png)

Panduan ini berfokus pada cara mengembangkan test case Anda.

## Membangun evals dan test case

### Prinsip desain eval

1. **Spesifik untuk tugas**: Rancang evals yang mencerminkan distribusi tugas dunia nyata Anda. Jangan lupa untuk mempertimbangkan edge case!
    <section title="Contoh edge case">

       - Data input yang tidak relevan atau tidak ada
       - Data input yang terlalu panjang atau input pengguna
       - [Kasus penggunaan chat] Input pengguna yang buruk, berbahaya, atau tidak relevan
       - Test case yang ambigu di mana bahkan manusia akan kesulitan mencapai konsensus penilaian
    
</section>
2. **Otomatisasi jika memungkinkan**: Struktur pertanyaan untuk memungkinkan penilaian otomatis (misalnya, pilihan ganda, string match, code-graded, LLM-graded).
3. **Prioritaskan volume daripada kualitas**: Lebih banyak pertanyaan dengan penilaian otomatis sinyal yang sedikit lebih rendah lebih baik daripada lebih sedikit pertanyaan dengan evals hand-graded berkualitas tinggi oleh manusia.

### Contoh evals

  <section title="Kesetiaan tugas (analisis sentimen) - evaluasi exact match">

    **Apa yang diukur**: Evals exact match mengukur apakah output model persis cocok dengan jawaban yang benar yang telah ditentukan sebelumnya. Ini adalah metrik sederhana dan tidak ambigu yang sempurna untuk tugas dengan jawaban kategoris yang jelas seperti analisis sentimen (positif, negatif, netral).

    **Contoh test case eval**: 1000 tweet dengan sentimen berlabel manusia.
    ```python
    import anthropic
    
    tweets = [
        {"text": "This movie was a total waste of time. 👎", "sentiment": "negative"},
        {"text": "The new album is 🔥! Been on repeat all day.", "sentiment": "positive"},
        {"text": "I just love it when my flight gets delayed for 5 hours. #bestdayever", "sentiment": "negative"},  # Edge case: Sarcasm
        {"text": "The movie's plot was terrible, but the acting was phenomenal.", "sentiment": "mixed"},  # Edge case: Mixed sentiment
        # ... 996 more tweets
    ]

    client = anthropic.Anthropic()

    def get_completion(prompt: str):
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=50,
            messages=[
            {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    
    def evaluate_exact_match(model_output, correct_answer):
        return model_output.strip().lower() == correct_answer.lower()

    outputs = [get_completion(f"Classify this as 'positive', 'negative', 'neutral', or 'mixed': {tweet['text']}") for tweet in tweets]
    accuracy = sum(evaluate_exact_match(output, tweet['sentiment']) for output, tweet in zip(outputs, tweets)) / len(tweets)
    print(f"Sentiment Analysis Accuracy: {accuracy * 100}%")
    ```
  
</section>

  <section title="Konsistensi (bot FAQ) - evaluasi cosine similarity">

    **Apa yang diukur**: Cosine similarity mengukur kesamaan antara dua vektor (dalam hal ini, sentence embeddings dari output model menggunakan SBERT) dengan menghitung kosinus sudut di antara mereka. Nilai yang lebih dekat ke 1 menunjukkan kesamaan yang lebih tinggi. Ini ideal untuk mengevaluasi konsistensi karena pertanyaan serupa harus menghasilkan jawaban yang secara semantik serupa, bahkan jika kata-katanya berbeda.

    **Contoh test case eval**: 50 grup dengan beberapa versi parafrase masing-masing.
    ```python
    from sentence_transformers import SentenceTransformer
    import numpy as np
    import anthropic
    
    faq_variations = [
        {"questions": ["What's your return policy?", "How can I return an item?", "Wut's yur retrn polcy?"], "answer": "Our return policy allows..."},  # Edge case: Typos
        {"questions": ["I bought something last week, and it's not really what I expected, so I was wondering if maybe I could possibly return it?", "I read online that your policy is 30 days but that seems like it might be out of date because the website was updated six months ago, so I'm wondering what exactly is your current policy?"], "answer": "Our return policy allows..."},  # Edge case: Long, rambling question
        {"questions": ["I'm Jane's cousin, and she said you guys have great customer service. Can I return this?", "Reddit told me that contacting customer service this way was the fastest way to get an answer. I hope they're right! What is the return window for a jacket?"], "answer": "Our return policy allows..."},  # Edge case: Irrelevant info
        # ... 47 more FAQs
    ]

    client = anthropic.Anthropic()

    def get_completion(prompt: str):
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            messages=[
            {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def evaluate_cosine_similarity(outputs):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = [model.encode(output) for output in outputs]
    
        cosine_similarities = np.dot(embeddings, embeddings.T) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(embeddings, axis=1).T)
        return np.mean(cosine_similarities)

    for faq in faq_variations:
        outputs = [get_completion(question) for question in faq["questions"]]
        similarity_score = evaluate_cosine_similarity(outputs)
        print(f"FAQ Consistency Score: {similarity_score * 100}%")
    ```
  
</section>

  <section title="Relevansi dan koherensi (peringkasan) - evaluasi ROUGE-L">

    **Apa yang diukur**: ROUGE-L (Recall-Oriented Understudy for Gisting Evaluation - Longest Common Subsequence) mengevaluasi kualitas ringkasan yang dihasilkan. Ini mengukur panjang subsequence umum terpanjang antara ringkasan kandidat dan referensi. Skor ROUGE-L yang tinggi menunjukkan bahwa ringkasan yang dihasilkan menangkap informasi kunci dalam urutan yang koheren.

    **Contoh test case eval**: 200 artikel dengan ringkasan referensi.
    ```python
    from rouge import Rouge
    import anthropic
    
    articles = [
        {"text": "In a groundbreaking study, researchers at MIT...", "summary": "MIT scientists discover a new antibiotic..."},
        {"text": "Jane Doe, a local hero, made headlines last week for saving... In city hall news, the budget... Meteorologists predict...", "summary": "Community celebrates local hero Jane Doe while city grapples with budget issues."},  # Edge case: Multi-topic
        {"text": "You won't believe what this celebrity did! ... extensive charity work ...", "summary": "Celebrity's extensive charity work surprises fans"},  # Edge case: Misleading title
        # ... 197 more articles
    ]

    client = anthropic.Anthropic()

    def get_completion(prompt: str):
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
            {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def evaluate_rouge_l(model_output, true_summary):
        rouge = Rouge()
        scores = rouge.get_scores(model_output, true_summary)
        return scores[0]['rouge-l']['f']  # ROUGE-L F1 score

    outputs = [get_completion(f"Summarize this article in 1-2 sentences:\n\n{article['text']}") for article in articles]
    relevance_scores = [evaluate_rouge_l(output, article['summary']) for output, article in zip(outputs, articles)]
    print(f"Average ROUGE-L F1 Score: {sum(relevance_scores) / len(relevance_scores)}")
    ```
  
</section>

  <section title="Nada dan gaya (layanan pelanggan) - skala Likert berbasis LLM">

    **Apa yang diukur**: Skala Likert berbasis LLM adalah skala psikometrik yang menggunakan LLM untuk menilai sikap atau persepsi subjektif. Di sini, ini digunakan untuk menilai nada respons pada skala 1 hingga 5. Ini ideal untuk mengevaluasi aspek bernuansa seperti empati, profesionalisme, atau kesabaran yang sulit dikuantifikasi dengan metrik tradisional.

    **Contoh test case eval**: 100 pertanyaan pelanggan dengan nada target (empatik, profesional, ringkas).
    ```python
    import anthropic

    inquiries = [
        {"text": "This is the third time you've messed up my order. I want a refund NOW!", "tone": "empathetic"},  # Edge case: Angry customer
        {"text": "I tried resetting my password but then my account got locked...", "tone": "patient"},  # Edge case: Complex issue
        {"text": "I can't believe how good your product is. It's ruined all others for me!", "tone": "professional"},  # Edge case: Compliment as complaint
        # ... 97 more inquiries
    ]

    client = anthropic.Anthropic()

    def get_completion(prompt: str):
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            messages=[
            {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def evaluate_likert(model_output, target_tone):
        tone_prompt = f"""Rate this customer service response on a scale of 1-5 for being {target_tone}:
        <response>{model_output}</response>
        1: Not at all {target_tone}
        5: Perfectly {target_tone}
        Output only the number."""

        # Generally best practice to use a different model to evaluate than the model used to generate the evaluated output 
        response = client.messages.create(model="claude-opus-4-6", max_tokens=50, messages=[{"role": "user", "content": tone_prompt}])
        return int(response.content[0].text.strip())

    outputs = [get_completion(f"Respond to this customer inquiry: {inquiry['text']}") for inquiry in inquiries]
    tone_scores = [evaluate_likert(output, inquiry['tone']) for output, inquiry in zip(outputs, inquiries)]
    print(f"Average Tone Score: {sum(tone_scores) / len(tone_scores)}")
    ```
  
</section>

  <section title="Preservasi privasi (chatbot medis) - klasifikasi biner berbasis LLM">

    **Apa yang diukur**: Klasifikasi biner menentukan apakah input termasuk dalam salah satu dari dua kelas. Di sini, ini digunakan untuk mengklasifikasikan apakah respons berisi PHI atau tidak. Metode ini dapat memahami konteks dan mengidentifikasi bentuk PHI yang halus atau implisit yang mungkin terlewatkan oleh sistem berbasis aturan.

    **Contoh test case eval**: 500 pertanyaan pasien simulasi, beberapa dengan PHI.
    ```python
    import anthropic
    
    patient_queries = [
        {"query": "What are the side effects of Lisinopril?", "contains_phi": False},
        {"query": "Can you tell me why John Doe, DOB 5/12/1980, was prescribed Metformin?", "contains_phi": True},  # Edge case: Explicit PHI
        {"query": "If my friend Alice, who was born on July 4, 1985, had diabetes, what...", "contains_phi": True},  # Edge case: Hypothetical PHI
        {"query": "I'm worried about my son. He's been prescribed the same medication as his father last year.", "contains_phi": True},  # Edge case: Implicit PHI
        # ... 496 more queries
    ]

    client = anthropic.Anthropic()

    def get_completion(prompt: str):
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
            {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def evaluate_binary(model_output, query_contains_phi):
        if not query_contains_phi:
            return True

        binary_prompt = """Does this response contain or reference any Personal Health Information (PHI)?
        PHI refers to any individually identifiable health data that is created, used, or disclosed in the course of providing healthcare services. This includes information related to an individual's physical or mental health condition, the provision of healthcare to that individual, or payment for such care.
        Key aspects of PHI include:
        - Identifiers: Names, addresses, birthdates, Social Security numbers, medical record numbers, etc.
        - Health data: Diagnoses, treatment plans, test results, medication records, etc.
        - Financial information: Insurance details, payment records, etc.
        - Communication: Notes from healthcare providers, emails or messages about health.

        <response>{model_output}</response>
        Output only 'yes' or 'no'."""

        # Generally best practice to use a different model to evaluate than the model used to generate the evaluated output
        response = client.messages.create(model="claude-opus-4-6", max_tokens=50, messages=[{"role": "user", "content": binary_prompt}])
        return response.content[0].text.strip().lower() == "no"

    outputs = [get_completion(f"You are a medical assistant. Never reveal any PHI in your responses. PHI refers to any individually identifiable health data that is created, used, or disclosed in the course of providing healthcare services. This includes information related to an individual's physical or mental health condition, the provision of healthcare to that individual, or payment for such care. Here is the question: {query['query']}") for query in patient_queries]
    privacy_scores = [evaluate_binary(output, query['contains_phi']) for output, query in zip(outputs, patient_queries)]
    print(f"Privacy Preservation Score: {sum(privacy_scores) / len(privacy_scores) * 100}%")
    ```
  
</section>

  <section title="Pemanfaatan konteks (asisten percakapan) - skala ordinal berbasis LLM">

    **Apa yang diukur**: Mirip dengan skala Likert, skala ordinal mengukur pada skala tetap yang terurut (1-5). Ini sempurna untuk mengevaluasi pemanfaatan konteks karena dapat menangkap tingkat di mana model mereferensikan dan membangun riwayat percakapan, yang merupakan kunci untuk interaksi yang koheren dan dipersonalisasi.

    **Contoh test case eval**: 100 percakapan multi-turn dengan pertanyaan yang bergantung pada konteks.
    ```python
    import anthropic

    conversations = [
        [
            {"role": "user", "content": "I just got a new pomeranian!"},
            {"role": "assistant", "content": "Congratulations on your new furry friend! Is this your first dog?"},
            {"role": "user", "content": "Yes, it is. I named her Luna."},
            {"role": "assistant", "content": "Luna is a lovely name! As a first-time dog owner, you might have some questions. What would you like to know about caring for Luna?"},
            ...
            {"role": "user", "content": "What should I know about caring for a dog of this specific breed?"}  # Edge case: Relies on context from much earlier
        ],
        [
            {"role": "user", "content": "I'm reading 'To Kill a Mockingbird' for my book club."},
            {"role": "assistant", "content": "Great choice! 'To Kill a Mockingbird' by Harper Lee is a classic that explores themes of racial injustice and moral growth. How are you finding it so far?"},
            {"role": "user", "content": "It's powerful. Hey, when was Scout's birthday again?"},  # Edge case: Abrupt topic shift
            {"role": "assistant", "content": "I apologize, but I don't recall the exact date of Scout's birthday being mentioned in 'To Kill a Mockingbird'. The novel doesn't focus on such specific details. Instead, it centers on Scout's growth and experiences over several years. Is there a particular part of the book or Scout's development that you're interested in discussing?"},
            {"role": "user", "content": "Oh, right. Well, can you suggest a recipe for a classic Southern cake?"}  # Edge case: Another topic shift
        ],
        # ... 98 more conversations
    ]

    client = anthropic.Anthropic()

    def get_completion(prompt: str):
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
            {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def evaluate_ordinal(model_output, conversation):
        ordinal_prompt = f"""Rate how well this response utilizes the conversation context on a scale of 1-5:
        <conversation>
        {"".join(f"{turn['role']}: {turn['content']}\\n" for turn in conversation[:-1])}
        </conversation>
        <response>{model_output}</response>
        1: Completely ignores context
        5: Perfectly utilizes context
        Output only the number and nothing else."""

        # Generally best practice to use a different model to evaluate than the model used to generate the evaluated output
        response = client.messages.create(model="claude-opus-4-6", max_tokens=50, messages=[{"role": "user", "content": ordinal_prompt}])
        return int(response.content[0].text.strip())

    outputs = [get_completion(conversation) for conversation in conversations]
    context_scores = [evaluate_ordinal(output, conversation) for output, conversation in zip(outputs, conversations)]
    print(f"Average Context Utilization Score: {sum(context_scores) / len(context_scores)}")
    ```
  
</section>

<Tip>Menulis ratusan test case bisa sulit dilakukan dengan tangan! Minta Claude untuk membantu Anda menghasilkan lebih banyak dari satu set test case contoh baseline.</Tip>
<Tip>Jika Anda tidak tahu metode eval apa yang mungkin berguna untuk menilai kriteria kesuksesan Anda, Anda juga dapat brainstorm dengan Claude!</Tip>

***

## Penilaian evals

Saat memutuskan metode mana yang digunakan untuk menilai evals, pilih metode yang tercepat, paling andal, dan paling dapat diskalakan:

1. **Penilaian berbasis kode**: Tercepat dan paling andal, sangat dapat diskalakan, tetapi juga kurang bernuansa untuk penilaian yang lebih kompleks yang memerlukan kekakuan berbasis aturan yang lebih sedikit.
   - Exact match: `output == golden_answer`
   - String match: `key_phrase in output`

2. **Penilaian manusia**: Paling fleksibel dan berkualitas tinggi, tetapi lambat dan mahal. Hindari jika memungkinkan.

3. **Penilaian berbasis LLM**: Cepat dan fleksibel, dapat diskalakan dan cocok untuk penilaian kompleks. Uji untuk memastikan keandalan terlebih dahulu kemudian skalakan.

### Tips untuk penilaian berbasis LLM
- **Miliki rubrik yang terperinci dan jelas**: "Jawaban harus selalu menyebutkan 'Acme Inc.' di kalimat pertama. Jika tidak, jawaban secara otomatis dinilai sebagai 'tidak benar.'"
    <Note>Kasus penggunaan tertentu, atau bahkan kriteria kesuksesan spesifik untuk kasus penggunaan itu, mungkin memerlukan beberapa rubrik untuk evaluasi holistik.</Note>
- **Empiris atau spesifik**: Misalnya, instruksikan LLM untuk hanya mengeluarkan 'benar' atau 'tidak benar', atau untuk menilai dari skala 1-5. Evaluasi yang murni kualitatif sulit dinilai dengan cepat dan dalam skala besar.
- **Dorong penalaran**: Minta LLM untuk berpikir terlebih dahulu sebelum memutuskan skor evaluasi, kemudian buang penalarannya. Ini meningkatkan kinerja evaluasi, terutama untuk tugas yang memerlukan penilaian kompleks.

<section title="Contoh: Penilaian berbasis LLM">

```python
import anthropic

def build_grader_prompt(answer, rubric):
    return f"""Grade this answer based on the rubric:
    <rubric>{rubric}</rubric>
    <answer>{answer}</answer>
    Think through your reasoning in <thinking> tags, then output 'correct' or 'incorrect' in <result> tags.""

def grade_completion(output, golden_answer):
    grader_response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": build_grader_prompt(output, golden_answer)}]
    ).content[0].text

    return "correct" if "correct" in grader_response.lower() else "incorrect"

# Example usage
eval_data = [
    {"question": "Is 42 the answer to life, the universe, and everything?", "golden_answer": "Yes, according to 'The Hitchhiker's Guide to the Galaxy'."},
    {"question": "What is the capital of France?", "golden_answer": "The capital of France is Paris."}
]

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
        {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

outputs = [get_completion(q["question"]) for q in eval_data]
grades = [grade_completion(output, a["golden_answer"]) for output, a in zip(outputs, eval_data)]
print(f"Score: {grades.count('correct') / len(grades) * 100}%")
```

</section>

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="Brainstorm evaluasi" icon="link" href="/docs/id/build-with-claude/prompt-engineering/overview">
    Pelajari cara membuat prompt yang memaksimalkan skor eval Anda.
  </Card>
  <Card title="Buku resep evals" icon="link" href="https://platform.claude.com/cookbook/misc-building-evals">
    Lebih banyak contoh kode evals yang dinilai oleh manusia, kode, dan LLM.
  </Card>
</CardGroup>