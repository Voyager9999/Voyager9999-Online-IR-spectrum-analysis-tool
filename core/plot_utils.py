import plotly.graph_objects as go
from scipy.signal import savgol_filter

def create_ir_plot(x, y, peaks=None, selected=None):
    y_smooth = savgol_filter(y, 11, 3)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name='Original', line=dict(color='black')))
    fig.add_trace(go.Scatter(x=x, y=y_smooth, name='Smoothed', line=dict(color='gray', dash='dot')))
    if selected:
        fig.add_vline(x=selected, line_color="red", line_dash="dash")
    if peaks:
        for p in peaks:
            fig.add_vline(x=p['Peak (cm⁻¹)'], line_color='red', line_dash='dot')
    fig.update_layout(xaxis_title="Wavenumber (cm⁻¹)", yaxis_title="Absorbance", xaxis_autorange="reversed")
    return fig
