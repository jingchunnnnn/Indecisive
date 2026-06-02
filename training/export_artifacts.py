"""Copy exported Colab artifacts into the local models directory."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "training" / "exports"
DEST = ROOT / "models"
ARTIFACTS = ["ranker.pkl", "ranker_metadata.json"]


def main() -> None:
    DEST.mkdir(exist_ok=True)
    for name in ARTIFACTS:
        source = SOURCE / name
        if source.exists():
            shutil.copy2(source, DEST / name)
            print(f"Copied {source} to {DEST / name}")
        else:
            print(f"Skipped missing {source}")


if __name__ == "__main__":
    main()
