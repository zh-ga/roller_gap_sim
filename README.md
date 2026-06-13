# Roller Compaction Parametric Study

Graphite powder roller compaction deformation analysis tool.

## Quick Start (Local)

```powershell
pip install -r requirements.txt
streamlit run roller_app.py
```

Or double-click `run_roller.bat` on Windows.

## Deploy to Streamlit Cloud

1. Push this repo to GitHub (private or public)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → select this repo → set Main file path to `roller_app.py`
4. Edit `.streamlit/secrets.toml` to set your password
5. Share the generated URL + password

## CLI Usage

```powershell
python roller_study.py           # single-point calculation
python roller_study.py --sweep   # full parametric sweeps
```

Edit variables at top of `roller_study.py` to customize.

## Theory

See `docs/roller_analysis.md` for the full derivation.

## Parameters

| Param | Symbol | Unit | Default |
|---|---|---|---|
| Roller diameter | D | mm | 8 |
| Roller length | L | mm | 50 |
| Target gap | h | um | 150 |
| Feed thickness | h0 | um | 356 |
| Effective yield | sigma_y | MPa | 50 |
| Areal density | sigma_A | g/m2 | 200 |
