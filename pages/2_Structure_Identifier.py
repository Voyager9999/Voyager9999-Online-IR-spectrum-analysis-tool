
import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.title("🔬 Structure Identifier")

with open("data/rules.json") as f:
    rules = json.load(f)
with open("data/memory.json") as f:
    memory = json.load(f)

picked = st.slider("Select Peak (cm⁻¹)", 400, 4100, 1700)

if st.button("➕ Confirm Peak"):
    if not any(abs(m["peak"] - picked) < 1 for m in memory):
        match = []
        for group, info in rules.items():
            for lo, hi in info["ranges"]:
                if lo <= picked <= hi:
                    match.append(f"{group} ({info['description']})")
        memory.append({"peak": picked, "match": match or ["Unassigned"]})
        memory = sorted(memory, key=lambda x: x["peak"])
        with open("data/memory.json", "w") as f:
            json.dump(memory, f)
        st.experimental_rerun()

if memory:
    df = pd.DataFrame(memory)
    st.dataframe(df)

    peaks = [m["peak"] for m in memory]
    fig = px.scatter(x=peaks, y=[1]*len(peaks), labels={"x": "Wavenumber (cm⁻¹)", "y": "Intensity"})
    st.plotly_chart(fig, use_container_width=True)

    idx = st.number_input("Delete peak at index", 0, len(memory)-1, 0)
    if st.button("❌ Delete"):
        memory.pop(idx)
        with open("data/memory.json", "w") as f:
            json.dump(memory, f)
        st.experimental_rerun()

if st.button("🧹 Clear All Peaks"):
    with open("data/memory.json", "w") as f:
        json.dump([], f)
    st.experimental_rerun()

st.download_button("📤 Export Memory", json.dumps(memory), "peaks.json")
upload = st.file_uploader("📥 Import Memory JSON", type="json")
if upload:
    memory = json.load(upload)
    with open("data/memory.json", "w") as f:
        json.dump(memory, f)
    st.experimental_rerun()
