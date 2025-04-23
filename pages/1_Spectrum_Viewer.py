
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

st.title("📈 Spectrum Viewer")

uploaded_file = st.file_uploader("Upload IR Spectrum CSV", type="csv")
show_peaks = st.checkbox("Show peak annotations", value=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "x" in df.columns and "y" in df.columns:
        df.to_csv("data/uploaded.csv", index=False)
        x, y = df["x"], df["y"]
        peaks, _ = find_peaks(-y, distance=10)
        fig, ax = plt.subplots()
        ax.plot(x, y, label="IR Spectrum")
        if show_peaks:
            ax.plot(x[peaks], y[peaks], "ro")
            for p in peaks:
                ax.text(x[p], y[p], f"{int(x[p])}", color="blue", fontsize=8)
        ax.invert_yaxis()
        ax.set_xlabel("Wavenumber (cm⁻¹)")
        ax.set_ylabel("Absorbance")
        st.pyplot(fig)
    else:
        st.error("CSV must contain 'x' and 'y' columns.")
