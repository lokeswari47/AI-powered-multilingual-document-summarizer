##%%writefile app.py
from flask import Flask, render_template, request
from transformers import pipeline
import functools
from newspaper import Article
from googletrans import Translator
import PyPDF2

app = Flask(__name__)

# Load summarizer only once
@functools.lru_cache(maxsize=2)
def load_summarizer():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        tokenizer="facebook/bart-large-cnn"
    )

# Load translator only once
@functools.lru_cache(maxsize=1)
def load_translator():
    return Translator()

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@app.route("/", methods=["GET", "POST"])
def home():
    final_summary = ""

    if request.method == "POST":
        text_input = request.form.get("text", "")
        url_input = request.form.get("url", "")
        pdf_file = request.files.get("pdf")
        language = request.form.get("language", "en")

        summarizer = load_summarizer()
        translator = load_translator()

        try:
            content = ""

            if pdf_file and pdf_file.filename.endswith(".pdf"):
                content = extract_text_from_pdf(pdf_file)

            elif url_input:
                article = Article(url_input)
                article.download()
                article.parse()
                content = article.text

            elif text_input:
                content = text_input

            else:
                final_summary = " Please provide text, URL, or PDF."
                return render_template("index.html", summary=final_summary)

            if not content.strip():
                final_summary = " No readable text found."
                return render_template("index.html", summary=final_summary)

            # Handle long text (chunking)
            chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
            summaries = []

            for chunk in chunks[:3]:
                result = summarizer(
                    chunk,
                    max_length=250,
                    min_length=200,
                    do_sample=False
                )
                summaries.append(result[0]["summary_text"])

            summary_text = " ".join(summaries)

            if language != "en":
                final_summary = translator.translate(
                    summary_text, dest=language
                ).text
            else:
                final_summary = summary_text

        except Exception as e:
            final_summary = f" Error: {e}"

    return render_template("index.html", summary=final_summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

