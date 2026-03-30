import sys
from pathlib import Path

# Allow `pytest` to import the src-layout package without requiring installation.
SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))
