
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.signal import savgol_filter

st.set_page_config(layout="wide")
st.title("🧠 Structure Identifier (Full Version)")

# 初始化状态
if "picked_peaks" not in st.session_state:
    st.session_state.picked_peaks = []
if "rules" not in st.session_state:
    st.session_state.rules = {
        "O–H stretch (alcohol)": (3200, 3600),
        "C=O stretch": (1680, 1750),
        "C=C stretch": (1600, 1680),
        "C–H stretch": (2850, 3100),
        "C≡C": (2100, 2260),
        "C≡N": (2210, 2260),
        "C–O stretch": (1000, 1300)
    }

# 上传光谱
uploaded_file = st.file_uploader("Upload CSV (with x and y)", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'x' in df.columns and 'y' in df.columns:
        x = df['x'].values
        y = df['y'].values
        y_smooth = savgol_filter(y, 11, 3)

        default_x = int(x[np.argmin(y_smooth)])
        selected_peak = st.slider("🎯 Move the red marker to your peak", int(x.min()), int(x.max()), default_x, step=1)

        if st.button("➕ Confirm this peak"):
            matched = [name for name, (lo, hi) in st.session_state.rules.items() if lo <= selected_peak <= hi]
            st.session_state.picked_peaks.append({
                "Peak (cm⁻¹)": selected_peak,
                "Functional Groups": "; ".join(matched) if matched else "Unassigned"
            })

        # 可编辑表格（带删除功能）
        if st.session_state.picked_peaks:
            df_peaks = pd.DataFrame(st.session_state.picked_peaks)
            st.dataframe(df_peaks)

            delete_index = st.number_input("Delete peak index (starting from 0)", min_value=0,
                                           max_value=len(df_peaks) - 1, step=1)
            if st.button("🗑 Delete selected peak"):
                st.session_state.picked_peaks.pop(delete_index)
                st.experimental_rerun()

        # 绘图
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, name="Original", line=dict(color="black")))
        fig.add_trace(go.Scatter(x=x, y=y_smooth, name="Smoothed", line=dict(color="gray", dash="dot")))
        fig.add_vline(x=selected_peak, line_color="red", line_dash="dash")
        fig.update_layout(xaxis_title="Wavenumber (cm⁻¹)", yaxis_title="Absorbance", xaxis_autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

# 自定义匹配规则
st.markdown("### ➕ Add Custom Functional Group Rule")
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Functional Group Name")
with col2:
    lo = st.number_input("Start (cm⁻¹)", step=1)
with col3:
    hi = st.number_input("End (cm⁻¹)", step=1)

if st.button("Add Rule"):
    if name and hi > lo:
        st.session_state.rules[name] = (lo, hi)
        st.success(f"Added rule: {name} → {lo}-{hi} cm⁻¹")
    else:
        st.error("Please enter valid name and range (hi > lo).")

# 显示当前规则
st.markdown("### 📚 Current Matching Rules")
df_rules = pd.DataFrame([
    {"Functional Group": k, "From": v[0], "To": v[1]}
    for k, v in st.session_state.rules.items()
])
st.dataframe(df_rules)
