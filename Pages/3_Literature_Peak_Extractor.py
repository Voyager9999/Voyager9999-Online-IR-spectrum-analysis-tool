import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd

st.set_page_config(page_title="PDF Peak Extractor", layout="wide")
st.title("📄 IR Peak Extractor from Literature PDFs")

uploaded_pdf = st.file_uploader("Upload PDF File (IR spectra or tables)", type="pdf")
mode = st.radio("Select Extraction Mode", ["📑 Text Table (preferred)", "🖼 Image (OCR coming soon)"])

if uploaded_pdf is not None:
    if mode == "📑 Text Table (preferred)":
        text_peaks = []
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        for page in doc:
            text = page.get_text()
            matches = re.findall(r"\b(\d{3,4})\b", text)
            for m in matches:
                w = int(m)
                if 800 <= w <= 3800:
                    text_peaks.append(w)

        text_peaks = sorted(set(text_peaks), reverse=True)
        st.success(f"Extracted {len(text_peaks)} candidate peaks from text.")
        df_peaks = pd.DataFrame({"Wavenumber (cm⁻¹)": text_peaks})
        st.dataframe(df_peaks)
        st.download_button("Download Peaks as CSV", df_peaks.to_csv(index=False), "extracted_peaks.csv")

    elif mode == "🖼 Image (OCR coming soon)":
        st.info("Image-based peak extraction is under development (OCR + OpenCV coming soon)")
