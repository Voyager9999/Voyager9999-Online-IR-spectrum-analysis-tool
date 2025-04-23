
import streamlit as st
import pandas as pd
import json

st.title("🔬 Structure Identifier")

with open("data/rules.json") as f:
    rules = json.load(f)

with open("data/memory.json") as f:
    memory = json.load(f)

st.write("Use the slider to confirm peak positions.")
picked = st.slider("Peak Position (cm⁻¹)", 400, 4100, 1700)

if st.button("➕ Confirm Peak"):
    match = [k for k, v in rules.items() if v[0] <= picked <= v[1]]
    memory.append({"peak": picked, "match": match or ["Unassigned"]})
    with open("data/memory.json", "w") as f:
        json.dump(memory, f)
    st.experimental_rerun()

st.write(pd.DataFrame(memory))

if st.button("🧹 Clear Peaks"):
    with open("data/memory.json", "w") as f:
        json.dump([], f)
    st.experimental_rerun()
