import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from roller_core import compute, rho_s, E_steel





# ==== Password check (Streamlit Cloud only) ====
try:
    _pw = st.secrets.get('viewers', {}).get('password', '')
except Exception:
    _pw = ''
if _pw:
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        pwd_input = st.text_input('Password', type='password')
        if pwd_input == _pw:
            st.session_state.authenticated = True
            st.rerun()
        elif pwd_input:
            st.error('Wrong password')
        st.stop()

st.set_page_config(page_title="Roller Compaction", layout="wide")
st.title("Roller Compaction Parametric Study")

with st.sidebar:
    st.header("Parameters")
    D_mm   = st.slider("D: Roller diameter (mm)", 4, 100, 8)
    L_mm   = st.slider("L: Roller length (mm)", 10, 300, 50)
    h_um   = st.slider("h: Target gap (um)", 30, 300, 150)
    h0_um  = st.slider("h0: Feed thickness (um)", 150, 800, 356)
    sy_MPa = st.slider("sigma_y: Yield (MPa)", 5, 200, 50)
    sig_A  = st.slider("Areal density (g/m^2)", 100, 500, 200) / 1000

D, L, h, h0, sy = D_mm*1e-3, L_mm*1e-3, h_um*1e-6, h0_um*1e-6, sy_MPa*1e6

S, F, db, dc, pm, x_arc, p_arc, y_beam, gap_beam = compute(D, L, h, h0, sy, sig_A)
R_target = sig_A / (rho_s * h)
R0 = sig_A / (rho_s * h0)
dev = db / h * 100 if h > 0 else 0
mid_gap = (h + db) * 1e6
if dev < 1: grade = "A"; gtxt = "Negligible"
elif dev < 5: grade = "B"; gtxt = "Marginal"
elif dev < 10: grade = "C"; gtxt = "Significant"
else: grade = "D"; gtxt = "Unacceptable"
gc = "green" if grade=="A" else "orange" if grade in ("B","C") else "red"

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Contact arc S", f"{S*1e3:.2f} mm")
c2.metric("Peak pressure", f"{pm/1e6:.1f} MPa")
c3.metric("Total force F", f"{F:.1f} N")
c4.metric("Bend deflection", f"{db*1e6:.1f} um", delta=f"{dev:.1f}%")
c5.metric("Contact squeeze", f"{dc*1e6:.2f} um")
st.markdown(f"**Grade: <span style='color:{gc}'>{grade}</span>** — {gtxt} | Feed R0={R0:.2f}, Target R={R_target:.2f} | Actual mid-gap = {mid_gap:.1f} um", unsafe_allow_html=True)

sweep = st.radio("Sweep parameter", ["L", "D", "h", "h0", "sigma_y"], horizontal=True, key="sweep")

# --- Run sweep ---
if sweep == "L":
    vals = np.linspace(10, 300, 30); lab = "Roller length L (mm)"; unit = "mm"
    data = [compute(D, v*1e-3, h, h0, sy, sig_A) for v in vals]
elif sweep == "D":
    vals = np.array([4,6,8,10,12,14,16,18,20,25,30,35,40,50,60,80,100])
    lab = "Roller diameter D (mm)"; unit = "mm"
    data = [compute(v*1e-3, L, h, h0, sy, sig_A) for v in vals]
elif sweep == "h":
    vals = np.linspace(30, 300, 20); lab = "Target gap h (um)"; unit = "um"
    data = [compute(D, L, v*1e-6, h0, sy, sig_A) for v in vals]
elif sweep == "h0":
    vals = np.linspace(150, 800, 20); lab = "Feed thickness h0 (um)"; unit = "um"
    data = [compute(D, L, h, v*1e-6, sy, sig_A) for v in vals]
else:
    vals = np.linspace(5, 200, 30); lab = "sigma_y (MPa)"; unit = "MPa"
    data = [compute(D, L, h, h0, v*1e6, sig_A) for v in vals]

d_ums  = [d[2]*1e6 for d in data]   # bend deflection (um)
dc_ums = [d[3]*1e6 for d in data]   # contact squeeze (um)
fs     = [d[1] for d in data]        # force (N)
ss     = [d[0]*1e3 for d in data]    # arc length (mm)
pms    = [d[4]/1e6 for d in data]    # peak pressure (MPa)

# --- Plots ---
fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

ax0 = axes[0]
ax0.plot(vals, d_ums, 'b-o', markersize=5, zorder=3, label='Bend deflection')
step = max(1, len(vals)//8)
for i in range(0, len(vals), step):
    ax0.annotate(f'{d_ums[i]:.1f}', (vals[i], d_ums[i]),
                 textcoords="offset points", xytext=(0,10), fontsize=7, ha='center', color='blue')
ax0.axhline(y=0.01*h*1e6, color='green', linestyle='--', linewidth=0.8, alpha=0.5, label='1% grade')
ax0.axhline(y=0.05*h*1e6, color='orange', linestyle='--', linewidth=0.8, alpha=0.5, label='5% grade')
ax0.axhline(y=0.10*h*1e6, color='red', linestyle='--', linewidth=0.8, alpha=0.5, label='10% grade')
ax0.set_xlabel(lab); ax0.set_ylabel("Bend deflection (um)")
ax0.set_title(f"Bend deflection vs {lab}")
ax0.legend(loc='upper left', fontsize=7); ax0.grid(True, alpha=0.3)

if len(y_beam) > 0:
    axes[1].fill_between(y_beam, gap_beam, h*1e6, alpha=0.2, color='orange')
    axes[1].axhline(y=h*1e6, color='green', linestyle='--', linewidth=1.2, label=f"Target gap = {h*1e6:.0f} um")
    axes[1].set_xlabel("Position along roller (mm)"); axes[1].set_ylabel("Actual gap (um)")
    axes[1].set_title("Actual gap distribution along roller")
    axes[1].legend(loc='lower right'); axes[1].grid(True, alpha=0.3)

if len(x_arc) > 0:
    axes[2].fill_between(x_arc, p_arc, alpha=0.2)
    axes[2].set_xlabel("Position along arc (mm)"); axes[2].set_ylabel("Pressure (MPa)")
    axes[2].set_title("Pressure p(x) along contact arc")
    axes[2].grid(True, alpha=0.3)

fig.tight_layout()
st.pyplot(fig)

# --- Data table ---
with st.expander("Raw data"):
    df = pd.DataFrame({
        f'{sweep} ({unit})': vals,
        'Arc S (mm)': [f"{v:.2f}" for v in ss],
        'Peak p (MPa)': [f"{v:.2f}" for v in pms],
        'Force (N)': [f"{v:.1f}" for v in fs],
        'Bend defl (um)': [f"{v:.2f}" for v in d_ums],
        'Contact squeeze (um)': [f"{v:.2f}" for v in dc_ums],
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

st.caption(
    "Left: bending deflection vs sweep parameter (drops with D, rises with L). "
    "Middle: actual gap along roller accounting for bending. "
    "Right: pressure distribution along contact arc."
)
