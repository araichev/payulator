import datetime as dt

import numpy as np
import pandas as pd
import pytest

from .context import payulator as pl


def test_freq_to_num():
    d = {
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
    for allow_cts in [True, False]:
        # Test on valid freq names
        for key, val in d.items():
            if key == "continuously" and not allow_cts:
                with pytest.raises(ValueError):
                    pl.freq_to_num(key, allow_cts=allow_cts)
            else:
                assert pl.freq_to_num(key, allow_cts=allow_cts) == val

        # Test on invalid freq name
        with pytest.raises(ValueError):
            pl.freq_to_num("bingo", allow_cts=allow_cts)


def test_to_date_offset():
    for k in [1, 2, 3, 4, 6, 12, 26, 52, 365]:
        assert isinstance(pl.to_date_offset(k), pd.DateOffset)

    assert pl.to_date_offset(10) is None


def test_amortize():
    # Compare a few outputs to those of
    # https://www.calculator.net/business-loan-calculator.html
    A = pl.amortize(1000, 0.05, "quarterly", "monthly", 3 * 12)
    assert round(A, 2) == 29.96

    A = pl.amortize(1000, 0.02, "continuously", "semiannually", 2 * 2)
    assert round(A, 2) == 256.31


def test_compute_period_interest_rate():
    I = pl.compute_period_interest_rate(0.12, "monthly", "monthly")
    assert round(I, 2) == 0.01


def test_build_principal_fn():
    balances = [
        100.00,
        91.93,
        83.81,
        75.65,
        67.44,
        59.18,
        50.87,
        42.52,
        34.11,
        25.66,
        17.16,
        8.60,
        0,
    ]
    p = pl.build_principal_fn(100, 0.07, "monthly", "monthly", 12)
    for i in range(13):
        assert round(p(i), 2) == balances[i]


def test_aggregate_payment_schedules():
    # Compare a few outputs to those of
    # https://www.calculator.net/business-loan-calculator.html
    first_payment_date = dt.date(2018, 1, 1)
    A = pl.Loan(
        code="A",
        principal=1000,
        interest_rate=0.05,
        compounding_freq="quarterly",
        payment_freq="monthly",
        num_payments=3 * 12,
        num_payments_interest_only=0,
        fee=10,
        first_payment_date=first_payment_date,
    ).payments()
    B = pl.Loan(
        code="B",
        principal=1000,
        interest_rate=0.05,
        compounding_freq="quarterly",
        payment_freq="monthly",
        num_payments=3 * 12,
        num_payments_interest_only=0,
        fee=10,
        first_payment_date=first_payment_date,
    ).payments()
    f = pl.aggregate_payment_schedules(
        [A["payment_schedule"], B["payment_schedule"]], freq="YE"
    )
    assert set(f.columns) == {
        "payment_date",
        "interest_payment",
        "principal_payment",
        "fee_payment",
        "total_payment",
        "interest_payment_cumsum",
        "principal_payment_cumsum",
        "fee_payment_cumsum",
        "total_payment_cumsum",
    }
    assert f.shape[0] == 3
