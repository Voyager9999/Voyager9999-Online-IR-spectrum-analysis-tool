
import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths

st.set_page_config(page_title='IR Peak Annotator', layout='wide')
st.title('🔬 IR Spectrum Annotator with Peak Shape')
st.markdown('Upload a spectrum CSV file with `x` and `y` columns to analyze and classify peaks (broad or sharp).')

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
    from numpy import min
    baseline = min(y)
    y_corrected = y - baseline

    peaks, props = find_peaks(
        y_corrected,
        height=height_ratio * max(y_corrected),
        distance=distance,
        prominence=0.03 * max(y_corrected),
        width=3
    )
    results_half = peak_widths(y_corrected, peaks, rel_height=0.5)
    widths = results_half[0]

    peak_x = x[peaks]
    peak_y = y[peaks]

    annotations = []
    for px, py, width in zip(peak_x, peak_y, widths):
        matches = [name for name, (low, high) in rules.items() if low <= px <= high]
        if matches:
            peak_type = 'broad' if width >= 25 else 'sharp'
            annotations.append({
                "peak_cm-1": round(px, 2),
                "intensity": round(py, 3),
                "width": round(width, 2),
                "type": peak_type,
                "annotations": '; '.join(matches)
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
            label = f"{row['annotations']}\n({row['type']})"
            ax.axvline(x=row['peak_cm-1'], color='red', linestyle='--', alpha=0.6)
            ax.text(row['peak_cm-1'], row['intensity'] + 0.01, label,
                    rotation=90, fontsize=7, color='blue', ha='center')
        ax.invert_xaxis()
        ax.set_xlabel('Wavenumber (cm⁻¹)')
        ax.set_ylabel('Intensity')
        ax.set_title('IR Spectrum with Annotated Peaks and Shape')
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)

        st.markdown("### 📄 Annotated Peaks Table")
        st.dataframe(result_df)

        csv = result_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Download Annotations", csv, "spectrum_annotations.csv", "text/csv")
    else:
        st.error("CSV must contain columns named 'x' and 'y'.")
