
project/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css

%%writefile README.md
# AI-Powered Multilingual Document Summarization System

This project is a Flask-based AI web application that summarizes PDFs, web articles, and text using Transformer models and supports multilingual translation.

## Features
- PDF upload and text extraction
- Web article summarization
- Text summarization using BART
- Multilingual translation
- Flask-based UI

## Tech Stack
Python, Flask, Transformers (BART), PyPDF2, GoogleTrans, HTML, CSS

## How to Run
pip install -r requirements.txt
python app.py
