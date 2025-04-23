
import streamlit as st
import pandas as pd
import json
import plotly.express as px
from scipy.signal import find_peaks

st.title("🔬 Structure Identifier")

with open("data/rules.json") as f:
    rules = json.load(f)

try:
    df = pd.read_csv("data/uploaded.csv")
    x, y = df["x"], df["y"]
    st.success("Using uploaded spectrum from Page 1.")
except:
    st.error("Please upload a spectrum in Page 1 first.")
    st.stop()

peaks, _ = find_peaks(-y, distance=10)
picked = st.slider("Select Peak (cm⁻¹)", 400, 4100, int(x[peaks[0]]))

with open("data/memory.json") as f:
    memory = json.load(f)

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
    st.subheader("🧠 Confirmed Peaks")
    dfm = pd.DataFrame(memory)
    st.dataframe(dfm)

    peaks_plot = [m["peak"] for m in memory]
    fig = px.line(x=x, y=y, labels={"x": "Wavenumber", "y": "Absorbance"})
    fig.add_scatter(x=peaks_plot, y=[y[x.tolist().index(p)] if p in x.tolist() else 1 for p in peaks_plot],
                    mode="markers+text", marker=dict(color="red"), text=[f"{int(p)}" for p in peaks_plot])
    st.plotly_chart(fig)

    idx = st.number_input("Delete index", 0, len(memory)-1)
    if st.button("❌ Delete"):
        memory.pop(idx)
        with open("data/memory.json", "w") as f:
            json.dump(memory, f)
        st.experimental_rerun()

if st.button("🧹 Clear All"):
    with open("data/memory.json", "w") as f:
        json.dump([], f)
    st.experimental_rerun()
