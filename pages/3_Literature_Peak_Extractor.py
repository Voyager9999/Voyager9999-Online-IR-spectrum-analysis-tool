import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd

st.set_page_config(layout="wide")
st.title("📄 IR Peak Extractor from Literature PDFs")

uploaded_pdf = st.file_uploader("Upload PDF File (IR tables or spectra text)", type="pdf")

if uploaded_pdf is not None:
    text_peaks = []
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    
    for page in doc:
        text = page.get_text()
        matches = re.findall(r"\b(\d{3,4})\b", text)
        for m in matches:
            w = int(m)
            if 800 <= w <= 3800:  # typical IR region
                text_peaks.append(w)

    text_peaks = sorted(set(text_peaks), reverse=True)
    st.success(f"✅ Extracted {len(text_peaks)} IR-like peaks from PDF text.")
    
    df_peaks = pd.DataFrame({"Wavenumber (cm⁻¹)": text_peaks})
    st.dataframe(df_peaks)
    st.download_button("⬇️ Download Peaks as CSV", df_peaks.to_csv(index=False), "extracted_peaks.csv")
else:
    st.info("Please upload a PDF file containing IR peak data (tables or descriptions).")
