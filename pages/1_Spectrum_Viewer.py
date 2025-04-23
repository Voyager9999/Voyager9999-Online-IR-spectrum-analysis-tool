
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

st.set_page_config(layout="wide")
st.title("📈 Spectrum Viewer")

uploaded_file = st.file_uploader("Upload IR CSV (x, y)", type=["csv"])
show_peaks = st.checkbox("Show Peak Annotations", value=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'x' in df.columns and 'y' in df.columns:
        x = df['x'].values
        y = df['y'].values
        y_smooth = savgol_filter(y, 11, 3)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(x, y, label="Original", color="black", alpha=0.6)
        ax.plot(x, y_smooth, label="Smoothed", linestyle="--", color="gray")

        if show_peaks:
            for i in range(2, len(y_smooth) - 2):
                if y_smooth[i] < y_smooth[i - 1] and y_smooth[i] < y_smooth[i + 1]:
                    if 2000 <= x[i] <= 2400:
                        continue
                    ax.axvline(x[i], color="red", linestyle="--", alpha=0.6)
                    ax.text(x[i], y[i] - 0.05, f"{int(x[i])}", color="blue", fontsize=8,
                            rotation=90, ha="center", va="top", backgroundcolor="white")

        ax.set_xlabel("Wavenumber (cm⁻¹)")
        ax.set_ylabel("Absorbance")
        ax.invert_xaxis()
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("CSV must contain columns 'x' and 'y'.")
