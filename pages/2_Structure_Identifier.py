
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.signal import savgol_filter
from core.rules import load_rules, save_rules
from core.memory import load_memory, save_memory
from core.plot_utils import create_ir_plot

st.set_page_config(layout="wide")
st.title("🧠 Structure Identifier")

rules = load_rules()
memory = load_memory()

uploaded_file = st.file_uploader("Upload IR CSV (x, y)", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'x' in df.columns and 'y' in df.columns:
        x = df['x'].values
        y = df['y'].values
        y_smooth = savgol_filter(y, 11, 3)

        selected_peak = st.slider("🎯 Adjust Red Marker to Peak", 4100, 400, int(x[np.argmin(y_smooth)]), step=1)

        if st.button("➕ Confirm this peak"):
            matched = [name for name, (lo, hi) in rules.items() if lo <= selected_peak <= hi]
            memory.append({
                "Peak (cm⁻¹)": selected_peak,
                "Match": "; ".join(matched) if matched else "Unassigned"
            })
            save_memory(memory)

        if memory:
            df_peaks = pd.DataFrame(memory)
            st.dataframe(df_peaks)
            del_idx = st.number_input("Delete peak index", 0, len(df_peaks)-1, step=1)
            if st.button("🗑 Delete selected peak"):
                memory.pop(del_idx)
                save_memory(memory)
                st.experimental_rerun()

            if st.button("🧹 Clear all peaks"):
                memory.clear()
                save_memory(memory)
                st.experimental_rerun()

        fig = create_ir_plot(x, y, memory, selected_peak)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("CSV must contain columns 'x' and 'y'.")

# 添加自定义规则
st.markdown("### ➕ Add Custom Rule")
col1, col2, col3 = st.columns(3)
with col1:
    new_name = st.text_input("Group Name")
with col2:
    lo = st.number_input("From", step=1)
with col3:
    hi = st.number_input("To", step=1)

if st.button("Add Rule"):
    if new_name and hi > lo:
        rules[new_name] = (lo, hi)
        save_rules(rules)
        st.success(f"Added: {new_name} → {lo}–{hi} cm⁻¹")
    else:
        st.error("Please check the name and range (hi must be > lo)")

# 展示所有规则
st.markdown("### 📚 Current Rules")
st.dataframe(pd.DataFrame([{"Group": k, "From": v[0], "To": v[1]} for k, v in rules.items()]))
