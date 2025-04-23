
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

st.set_page_config(page_title="IR Spectrum Viewer", layout="wide")
st.title("🔬 IR Spectrum Viewer & Annotator")

uploaded_file = st.file_uploader("Upload IR CSV File (x: wavenumber, y: absorbance)", type="csv")
show_peaks = st.checkbox("Show Peak Annotations", value=True)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'x' in df.columns and 'y' in df.columns:
        x = df['x'].values
        y = df['y'].values
        y_smooth = savgol_filter(y, 11, 3)

        peaks = []
        for i in range(2, len(y_smooth) - 2):
            if y_smooth[i] < y_smooth[i-1] and y_smooth[i] < y_smooth[i+1]:
                if 1900 <= x[i] <= 2500:
                    continue
                peaks.append((x[i], y[i]))

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(x, y, color='black', label='Original Spectrum')
        ax.plot(x, y_smooth, color='gray', linestyle='--', label='Smoothed')

        if show_peaks:
            for px, py in peaks:
                ax.axvline(x=px, color='red', linestyle='--', alpha=0.6)
                ax.text(px, py - 0.02, f"{int(px)} cm⁻¹", rotation=90,
                        fontsize=8, color='blue', ha='center', va='top',
                        bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))

        ax.set_xlabel("Wavenumber (cm⁻¹)")
        ax.set_ylabel("Absorbance")
        ax.invert_xaxis()
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.legend()
        st.pyplot(fig)
