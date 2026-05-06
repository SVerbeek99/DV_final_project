# Tourism and Structural Transformation Dashboard

Interactive Dash application for exploring how tourism dependence relates to structural transformation in employment and selected development outcomes.

## Course Context
- Course: JM0250 Data Visualization
- Project theme: Tourism and structural transformation
- Approach: Exploratory visual analysis (not causal inference)

## What This Dashboard Explores
- Tourism receipts as a share of exports
- Employment composition across services, industry, and agriculture
- Associations with GDP per capita, urbanization, poverty, and inequality
- Country pathways over time and cross-country comparisons

## Repository Contents
- `tourism_structural_dashboard_designed.py`: main Dash app
- `tourism_structural_requirements.txt`: original dependency list
- `requirements.txt`: standard dependency file for quick setup
- `employmentdata.csv`: employment and value-added indicators
- `tourism15indicators.csv`: tourism and development indicators
- `tourism_structural_presentation_script.md`: presentation script
- `AI_USAGE_LOG.md`: AI usage disclosure notes
- `agents.md`: project guidance notes

## Quick Start
### 1. Create and activate a virtual environment
Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
python tourism_structural_dashboard_designed.py
```

Then open:
- `http://127.0.0.1:8050`

## Notes
- Keep `employmentdata.csv` and `tourism15indicators.csv` in the same folder as the Python dashboard script.
- If you see `ModuleNotFoundError`, confirm your active interpreter is the one inside `.venv`.

## Data Source
- World Bank World Development Indicators (WDI)

