from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
API = ROOT / "apps" / "api"
RECOMMENDER = ROOT / "packages" / "recommender"

for path in (ROOT, API, RECOMMENDER):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)
