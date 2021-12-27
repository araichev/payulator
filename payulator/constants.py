import os
import pathlib as pl
import numpy as np


#: Frequency string -> number of occurrences per year
NUM_BY_FREQ = {
    "annually": 1,
    "semiannually": 2,
    "triannually": 3,
    "quarterly": 4,
    "bimonthly": 6,
    "monthly": 12,
    "fortnightly": 26,
    "weekly": 52,
    "daily": 365,
    "continuously": np.inf,
}

ROOT = pl.Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
THEME_DIR = ROOT / "payulator" / "theme"
