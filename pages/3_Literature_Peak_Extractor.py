
import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
from core.rules import load_rules, save_rules

st.set_page_config(layout="wide")
st.title("📄 Literature IR Peak Extractor")

rules = load_rules()

uploaded_pdf = st.file_uploader("Upload PDF (with IR peaks)", type="pdf")

if uploaded_pdf:
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

st.markdown("### ➕ Add Custom Rule (Shared with Structure Identifier)")
col1, col2, col3 = st.columns(3)
with col1:
    new_name = st.text_input("Group Name")
with col2:
    lo = st.number_input("From", step=1, key="pdf_lo")
with col3:
    hi = st.number_input("To", step=1, key="pdf_hi")

if st.button("Add Rule", key="pdf_add_rule"):
    if new_name and hi > lo:
        rules[new_name] = (lo, hi)
        save_rules(rules)
        st.success(f"Added: {new_name} → {lo}–{hi} cm⁻¹")
    else:
        st.error("Please check the name and range (hi must be > lo)")

st.markdown("### 📚 Current Rules")
st.dataframe(pd.DataFrame([{"Group": k, "From": v[0], "To": v[1]} for k, v in rules.items()]))
