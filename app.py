
import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

st.set_page_config(page_title='IR Spectrum Annotator', layout='wide')
st.title('🔬 IR Spectrum Annotator (Improved Version)')
st.markdown('Upload your spectrum CSV file (with columns `x` and `y`) to analyze and annotate peaks with better accuracy.')

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
uploaded_rules = st.file_uploader("Upload Custom IR Rules (optional)", type=["json"])

default_rules = {
    "O–H (alcohol stretch)": [3200, 3600],
    "O–H (carboxylic acid stretch)": [2500, 3000],
    "N–H (amine/amide stretch)": [3300, 3500],
    "C–H (alkane stretch)": [2850, 2960],
    "C–H (aromatic stretch)": [3000, 3100],
    "C≡C (alkyne stretch)": [2100, 2260],
    "C≡N (nitrile stretch)": [2210, 2260],
    "C=O (carbonyl stretch)": [1680, 1750],
    "C=C (alkene stretch)": [1620, 1680],
    "C–O (ether/ester/alcohol stretch)": [1000, 1300],
    "C–N (amine stretch)": [1020, 1250],
    "NO₂ (nitro stretch)": [1500, 1600],
    "SO₂ (sulfonyl stretch)": [1120, 1350],
    "P=O (phosphoryl stretch)": [1200, 1280]
}

def annotate_peaks(x, y, rules, height_ratio=0.05, distance=10):
    peaks, props = find_peaks(y, height=height_ratio * max(y), distance=distance, prominence=0.01, width=2)
    peak_x = x[peaks]
    peak_y = y[peaks]
    annotations = []
    for px, py in zip(peak_x, peak_y):
        matches = [name for name, (low, high) in rules.items() if low <= px <= high]
        if matches:
            annotations.append({
                "peak_cm-1": px,
                "intensity": py,
                "annotations": "; ".join(matches)
            })
    return pd.DataFrame(annotations)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'x' in df.columns and 'y' in df.columns:
        x = df['x'].values
        y = df['y'].values
        st.success("Spectrum file loaded successfully.")
        rules = default_rules
        if uploaded_rules:
            try:
                rules = json.load(uploaded_rules)
                st.success("Custom rules loaded.")
            except:
                st.warning("Failed to load custom rules. Using default.")

        result_df = annotate_peaks(x, y, rules)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, color='black')
        for _, row in result_df.iterrows():
            ax.axvline(x=row['peak_cm-1'], color='red', linestyle='--', alpha=0.6)
            ax.text(row['peak_cm-1'], row['intensity'] + 0.01, row['annotations'],
                    rotation=90, fontsize=7, color='blue', ha='center')
        ax.invert_xaxis()
        ax.set_xlabel('Wavenumber (cm⁻¹)')
        ax.set_ylabel('Intensity')
        ax.set_title('IR Spectrum with Annotated Peaks')
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)

        st.markdown("### 📄 Annotated Peaks Table")
        st.dataframe(result_df)

        csv = result_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Download Annotations", csv, "spectrum_annotations.csv", "text/csv")
    else:
        st.error("CSV must contain columns named 'x' and 'y'.")
