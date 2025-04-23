
import streamlit as st
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

st.title("📈 Spectrum Viewer")

uploaded = st.file_uploader("Upload IR Spectrum CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    if "x" in df.columns and "y" in df.columns:
        x = df["x"]
        y = df["y"]
        fig, ax = plt.subplots()
        ax.plot(x, y, label="IR Spectrum")
        peaks, _ = find_peaks(-y, distance=10)
        ax.plot(x[peaks], y[peaks], "ro")
        for p in peaks:
            ax.text(x[p], y[p]-0.05, f"{int(x[p])}", color="blue", fontsize=8)
        ax.invert_yaxis()
        st.pyplot(fig)
    else:
        st.warning("CSV must contain 'x' and 'y' columns.")
