
import streamlit as st
from dotenv import load_dotenv

from document_reader import extract_pdf_text
from comparison import compare_documents
from report_generator import create_docx_report

load_dotenv()

st.set_page_config(
    page_title="AI Document Comparison Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("AI Document Comparison Assistant")
st.write("Upload two PDF documents to compare their content.")

file_a = st.file_uploader("Upload Document A", type=["pdf"])
file_b = st.file_uploader("Upload Document B", type=["pdf"])

if st.button("Compare Documents", type="primary"):
    if not file_a or not file_b:
        st.error("Please upload both PDF documents.")
    else:
        try:
            with st.spinner("Reading PDF documents..."):
                doc_a = extract_pdf_text(file_a)
                doc_b = extract_pdf_text(file_b)

            with st.spinner("Comparing documents with AI..."):
                result = compare_documents(
                    doc_a["text"],
                    doc_b["text"],
                    file_a.name,
                    file_b.name
                )

            st.session_state["result"] = result
            st.session_state["names"] = (
                file_a.name,
                file_b.name
            )

        except Exception as error:
            st.error(f"Error: {error}")

if "result" in st.session_state:
    result = st.session_state["result"]

    tabs = st.tabs([
        "Summary A",
        "Summary B",
        "Similarities",
        "Differences",
        "Key Details",
        "Conclusion"
    ])

    sections = [
        ("Document A Summary", "summary_a"),
        ("Document B Summary", "summary_b"),
        ("Similarities", "similarities"),
        ("Differences", "differences"),
        ("Key Details Comparison", "key_details"),
        ("Overall Conclusion", "conclusion")
    ]

    for tab, (heading, key) in zip(tabs, sections):
        with tab:
            st.subheader(heading)
            st.markdown(
                result.get(key, "Not found in the provided text.")
            )

    st.subheader("Limitations")
    st.write(result.get("limitations", "Verify with original PDFs."))

    names = st.session_state["names"]

    report = create_docx_report(names[0], names[1], result)

    st.download_button(
        "Download Comparison Report",
        data=report,
        file_name="comparison_report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if st.button("Clear / Compare Again"):
    st.session_state.pop("result", None)
    st.session_state.pop("names", None)
    st.rerun()
