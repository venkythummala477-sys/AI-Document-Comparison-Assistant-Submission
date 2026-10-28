
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def compare_documents(text_a, text_b, name_a, name_b):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY missing. Check your .env file."
        )

    model = os.getenv(
        "GROQ_MODEL", "openai/gpt-oss-20b"
    ).strip()

    # Keep the request reasonably small.
    max_chars = 12000
    text_a = text_a[:max_chars]
    text_b = text_b[:max_chars]

    prompt = f"""
Compare these two documents using only the supplied text.
Do not invent facts. Keep each document separate.

Return these exact headings:
DOCUMENT A SUMMARY
DOCUMENT B SUMMARY
SIMILARITIES
DIFFERENCES
KEY DETAILS COMPARISON
OVERALL CONCLUSION
LIMITATIONS

Include important dates, names, amounts, deadlines,
and requirements. If information is missing, write:
Not found in the provided text.

Document A filename: {name_a}
Document A text:
{text_a}

Document B filename: {name_b}
Document B text:
{text_b}
"""

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful document comparison "
                        "assistant. Use only supplied evidence."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_completion_tokens=3000,
        )

        answer = (
            response.choices[0].message.content or ""
        ).strip()

        if not answer:
            raise ValueError("Groq returned an empty response.")

    except Exception as error:
        raise RuntimeError(
            f"Groq comparison failed: {error}"
        ) from error

    headings = {
        "summary_a": "DOCUMENT A SUMMARY",
        "summary_b": "DOCUMENT B SUMMARY",
        "similarities": "SIMILARITIES",
        "differences": "DIFFERENCES",
        "key_details": "KEY DETAILS COMPARISON",
        "conclusion": "OVERALL CONCLUSION",
        "limitations": "LIMITATIONS",
    }

    result = {key: "" for key in headings}
    found = []

    for key, heading in headings.items():
        pos = answer.upper().find(heading)
        if pos >= 0:
            found.append((pos, key, pos + len(heading)))

    found.sort()

    for i, (start, key, body_start) in enumerate(found):
        end = (
            found[i + 1][0]
            if i + 1 < len(found)
            else len(answer)
        )
        result[key] = answer[body_start:end].strip(" \n:-")

    if not found:
        result["conclusion"] = answer

    for key in result:
        if not result[key]:
            result[key] = "Not found in the provided text."

    return result
