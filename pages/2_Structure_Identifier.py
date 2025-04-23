import streamlit as st
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

st.set_page_config(page_title="Structure Identifier", layout="wide")
st.title("🧠 Functional Group Identifier from IR Peaks")

uploaded_file = st.file_uploader("Upload IR CSV File (x: wavenumber, y: absorbance)", type="csv")

# 默认结构规则库（可扩展）
rules = {
    "O–H (alcohol)": (3200, 3600),
    "O–H (acid)": (2500, 3000),
    "N–H (amine/amide)": (3300, 3500),
    "C–H (alkane)": (2850, 2960),
    "C–H (aromatic)": (3000, 3100),
    "C≡C (alkyne)": (2100, 2260),
    "C≡N (nitrile)": (2210, 2260),
    "C=O (carbonyl)": (1680, 1750),
    "C=C (alkene)": (1620, 1680),
    "C–O (ether/ester/alcohol)": (1000, 1300),
    "C–N (amine)": (1020, 1250),
    "NO₂ (nitro)": (1500, 1600),
    "SO₂ (sulfonyl)": (1120, 1350)
}

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'x' in df.columns and 'y' in df.columns:
        x = df['x'].values
        y = df['y'].values
        y_smooth = savgol_filter(y, 11, 3)

        # 基于局部极小值识别吸收谷
        peaks = []
        for i in range(2, len(y_smooth) - 2):
            if y_smooth[i] < y_smooth[i - 1] and y_smooth[i] < y_smooth[i + 1]:
                if 1900 <= x[i] <= 2500:
                    continue
                peaks.append((x[i], y[i]))

        # 匹配结构
        annotations = []
        for px, py in peaks:
            matched = [name for name, (lo, hi) in rules.items() if lo <= px <= hi]
            annotations.append({
                "Peak (cm⁻¹)": round(px, 1),
                "Absorbance": round(py, 4),
                "Possible Groups": "; ".join(matched) if matched else "Unassigned"
            })

        df_result = pd.DataFrame(annotations)
        st.success(f"{len(df_result)} peaks identified.")
        st.dataframe(df_result)
    else:
        st.error("CSV must contain 'x' and 'y' columns.")
