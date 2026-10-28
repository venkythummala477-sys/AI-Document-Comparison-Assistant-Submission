
# AI Document Comparison Assistant

## Project Category
Generative AI / LLM Application

## Technologies
- Python
- Streamlit
- Gemini API
- pypdf
- python-dotenv
- python-docx

## Features
- Upload two PDF documents
- Extract PDF text
- Generate separate document summaries
- Find similarities and differences
- Compare dates, amounts and requirements
- Display an overall conclusion
- Download a DOCX comparison report
- Validate unreadable and oversized PDFs

## Setup

Create a virtual environment:

    py -m venv venv

Activate it on Windows:

    .\venv\Scripts\Activate.ps1

Install libraries:

    pip install -r requirements.txt

Copy `.env.example` to `.env` and add your Gemini API key.

Run:

    streamlit run app.py

## Limitations
Scanned PDFs need OCR. AI-generated comparisons should be
verified against the original documents. This application
does not provide legal decisions.
