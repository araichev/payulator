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
