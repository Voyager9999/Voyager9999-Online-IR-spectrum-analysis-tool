
import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
from core.rules import load_rules

st.set_page_config(layout="wide")
st.title("📄 Literature IR Peak Extractor")

uploaded_pdf = st.file_uploader("Upload PDF (with IR peaks)", type="pdf")

if uploaded_pdf:
    rules = load_rules()
    extracted = []
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    
    for page in doc:
        text = page.get_text()
        matches = re.findall(r"\b(\d{3,4})\b", text)
        for m in matches:
            w = int(m)
            if 800 <= w <= 3800:
                match = [name for name, (lo, hi) in rules.items() if lo <= w <= hi]
                extracted.append({
                    "Wavenumber (cm⁻¹)": w,
                    "Match": "; ".join(match) if match else "Unassigned"
                })

    df_peaks = pd.DataFrame(sorted(extracted, key=lambda x: -x["Wavenumber (cm⁻¹)"]))
    st.success(f"✅ Extracted {len(df_peaks)} peaks from text.")
    st.dataframe(df_peaks)
    st.download_button("⬇️ Download CSV", df_peaks.to_csv(index=False), "literature_peaks.csv")
else:
    st.info("Please upload a PDF with visible text (tables or peak values).")
