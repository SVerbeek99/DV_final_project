"""Run the Tourism Structural Explorer from the repository-standard app path."""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / "tourism_structural_dashboard_designed.py"), run_name="__main__")
