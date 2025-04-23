
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os

st.title("🔬 Structure Identifier")

with open("data/rules.json") as f:
    rules = json.load(f)

try:
    df = pd.read_csv("data/uploaded.csv")
    st.success("Using spectrum uploaded in Page 1.")
    x = df["x"]
    y = df["y"]
except:
    st.warning("Please upload a spectrum in Page 1 first.")
    st.stop()

# 自动寻找峰（简单处理）
from scipy.signal import find_peaks
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
    dfm = pd.DataFrame(memory)
    st.dataframe(dfm)
    peaks = [m["peak"] for m in memory]
    fig = px.scatter(x=peaks, y=[1]*len(peaks), labels={"x": "Wavenumber", "y": "Intensity"})
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
