
import streamlit as st
import fitz
import pandas as pd
import re
import json

st.title("📄 Literature Peak Extractor")

with open("data/rules.json") as f:
    rules = json.load(f)

uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")
if uploaded_pdf:
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    matches = re.findall(r"\b(\d{3,4})\b", text)
    peaks = []
    for m in matches:
        w = int(m)
        match = [name for name, (lo, hi) in rules.items() if lo <= w <= hi]
        peaks.append({"peak": w, "match": match or ["Unassigned"]})

    st.dataframe(pd.DataFrame(peaks))

st.markdown("### ➕ Edit Rules")
name = st.text_input("Name")
lo = st.number_input("From", step=1)
hi = st.number_input("To", step=1)

if st.button("Add Rule"):
    if name and hi > lo:
        rules[name] = [lo, hi]
        with open("data/rules.json", "w") as f:
            json.dump(rules, f)
        st.experimental_rerun()

if st.button("Clear Rules"):
    with open("data/rules.json", "w") as f:
        json.dump({}, f)
    st.experimental_rerun()
