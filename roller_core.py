# ============================================================
#  roller_core.py — shared compute engine
#  Used by roller_app.py (Streamlit) and roller_study.py (CLI)
# ============================================================
import numpy as np

rho_s     = 2250        # graphite true density (kg/m^3)
E_steel   = 200e9       # steel Young modulus (Pa)


def trapz(y, x):
    """Trapezoidal integration, compatible with numpy 2.x."""
    return float(np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2)


def helle_p(R, R0, sy):
    """Helle-Fleck Stage I compaction pressure.
    R   = current relative density
    R0  = initial relative density
    sy  = effective yield strength (Pa)
    """
    if R <= R0:
        return 0.0
    return 1.5 * sy * (R - R0)**2 / (R * (1 - R0))


def compute(diam, length, gap, h_init, sigma_y, sigma_A=0.2):
    """
    Compute roller compaction: geometry, pressure, force, deflection.

    Parameters (all SI units):
        diam    : roller diameter (m)
        length  : roller length (m)
        gap     : target gap at narrowest point (m)
        h_init  : feed powder thickness (m)
        sigma_y : effective yield strength (Pa)
        sigma_A : areal density (kg/m^2), default 0.2 = 200 g/m^2

    Returns:
        S       : contact arc length (m)
        F       : total compaction force (N)
        db      : bending deflection at roller center (m)
        dc      : local contact squeeze (m)
        pm      : peak pressure at narrowest gap (Pa)
        x_arc   : positions along contact arc (mm)
        p_arc   : pressure along contact arc (MPa)
        y_beam  : positions along roller length (mm)
        gap_beam: actual gap along roller length including bending (um)
    """
    if gap >= h_init:
        return 0.0, 0.0, 0.0, 0.0, 0.0,
        np.array([]), np.array([]),
        np.array([]), np.array([])

    # --- Geometry ---
    dh = h_init - gap
    S = np.sqrt(diam * dh)

    # --- Density along contact arc ---
    x = np.linspace(-S / 2, S / 2, 200)
    hx = gap + x**2 / diam
    rx = sigma_A / (rho_s * hx)
    r0 = sigma_A / (rho_s * h_init)

    # --- Pressure along contact arc ---
    px = np.array([helle_p(r, r0, sigma_y) for r in rx])
    px[x**2 / diam > dh * 0.99] = 0.0   # zero pressure at entry/exit
    pm = float(px[len(px) // 2])          # peak pressure at narrowest

    # --- Total force ---
    F = trapz(px, x) * length

    # --- Bending deflection (simply-supported beam, uniform load) ---
    w = F / length
    I_sec = np.pi * diam**4 / 64
    db = 5.0 * w * length**4 / (384.0 * E_steel * I_sec)

    # --- Local contact squeeze (Hertz) ---
    dc = pm * diam / E_steel

    # --- Gap distribution along roller ---
    y = np.linspace(0, length, 200)
    dy = w * y * (length**3 - 2 * length * y**2 + y**3) / (24 * E_steel * I_sec)
    gap_y = gap + dy

    return S, F, db, dc, pm, x * 1e3, px / 1e6, y * 1e3, gap_y * 1e6
