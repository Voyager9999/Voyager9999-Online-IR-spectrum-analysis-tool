import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.signal import savgol_filter

st.set_page_config(layout="wide")
st.title("🧠 Structure Identifier (with manual peak selection)")

uploaded_file = st.file_uploader("Upload IR CSV file (x, y)", type=["csv"])

# 官能团规则库（可扩展）
rules = {
    "O–H stretch (alcohol)": (3200, 3600),
    "O–H stretch (acid)": (2500, 3000),
    "N–H stretch (amine)": (3300, 3500),
    "C–H stretch (alkane)": (2850, 2960),
    "C–H stretch (aromatic)": (3000, 3100),
    "C≡C stretch": (2100, 2260),
    "C≡N stretch": (2210, 2260),
    "C=O stretch": (1680, 1750),
    "C=C stretch": (1600, 1680),
    "C–O stretch": (1000, 1300),
    "C–N stretch": (1020, 1250),
    "NO₂ (nitro)": (1500, 1600),
    "S=O (sulfonyl)": (1120, 1350)
}

picked_peaks = []

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'x' in df.columns and 'y' in df.columns:
        x = df['x'].values
        y = df['y'].values
        y_smooth = savgol_filter(y, 11, 3)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Original'))
        fig.add_trace(go.Scatter(x=x, y=y_smooth, mode='lines', name='Smoothed'))

        st.markdown("🎯 **Use the slider to manually pick a peak**, then click confirm:")
        selected_peak = st.slider("Pick a wavenumber (cm⁻¹)", min_value=int(min(x)), max_value=int(max(x)), value=int(x[np.argmin(y)]))
        
        if st.button("➕ Confirm this peak"):
            matched = [name for name, (lo, hi) in rules.items() if lo <= selected_peak <= hi]
            picked_peaks.append({
                "Peak (cm⁻¹)": selected_peak,
                "Possible Functional Groups": "; ".join(matched) if matched else "Unassigned"
            })

        # 显示历史选择
        if picked_peaks:
            df_result = pd.DataFrame(picked_peaks)
            st.dataframe(df_result)

        # 绘制 marker
        fig.add_vline(x=selected_peak, line_dash="dash", line_color="red")
        fig.update_layout(xaxis_title="Wavenumber (cm⁻¹)", yaxis_title="Absorbance", xaxis_autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("CSV must contain 'x' and 'y' columns.")
