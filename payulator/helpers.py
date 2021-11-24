import math
from copy import copy
import datetime as dt
from typing import Union, Optional

import numpy as np
import pandas as pd
from pandas import DataFrame

from . import constants as cs


def freq_to_num(freq: str, *, allow_cts: bool = False) -> Union[int, float]:
    """
    Map frequency name to number of occurrences per year via
    :const:`NUM_BY_FREQ`.
    If not ``allow_cts``, then remove the ``"continuouly"`` option.
    Raise a ``ValueError`` in case of no frequency match.
    """
    d = copy(cs.NUM_BY_FREQ)
    if not allow_cts:
        del d["continuously"]

    try:
        return d[freq]
    except KeyError:
        raise ValueError(
            f"Invalid frequency {freq}. " f"Frequency must be one of {d.keys()}"
        )


def to_date_offset(num_per_year: int) -> Union[pd.DateOffset, None]:
    """
    Convert the given number of occurrences per year to its
    corresponding period (Pandas DateOffset object),
    e.g. map 4 to ``pd.DateOffset(months=3)``.
    Return ``None`` if num_per_year is not one of
    ``[1, 2, 3, 4, 6, 12, 26, 52, 365]``.
    """
    k = num_per_year
    if k in [1, 2, 3, 4, 6, 12]:
        d = pd.DateOffset(months=12 // k)
    elif k == 26:
        d = pd.DateOffset(weeks=2)
    elif k == 52:
        d = pd.DateOffset(weeks=1)
    elif k == 365:
        d = pd.DateOffset(days=1)
    else:
        d = None
    return d


def compute_period_interest_rate(
    interest_rate: float, compounding_freq: str, payment_freq: str
) -> float:
    """
    Compute the interest rate per payment period given
    an annual interest rate, a compounding frequency, and a payment
    freq.
    See the function :func:`freq_to_num` for acceptable frequencies.
    """
    i = interest_rate
    j = freq_to_num(compounding_freq, allow_cts=True)
    k = freq_to_num(payment_freq)

    if np.isinf(j):
        return math.exp(i / k) - 1
    else:
        return (1 + i / j) ** (j / k) - 1


def build_principal_fn(
    principal: float,
    interest_rate: float,
    compounding_freq: str,
    payment_freq: str,
    num_payments: int,
):
    """
    Compute the remaining loan principal, the loan balance,
    as a function of the number of payments made.
    Return the resulting function.
    """
    P = principal
    I = compute_period_interest_rate(interest_rate, compounding_freq, payment_freq)
    n = num_payments

    def p(t):
        if I == 0:
            return P - t * P / n
        else:
            return P * (1 - ((1 + I) ** t - 1) / ((1 + I) ** n - 1))

    return p


def amortize(
    principal: float,
    interest_rate: float,
    compounding_freq: str,
    payment_freq: str,
    num_payments: str,
) -> float:
    """
    Given the loan parameters

    - ``principal``: (float) amount of loan, that is, the principal
    - ``interest_rate``: (float) nominal annual interest rate
      (not as a percentage), e.g. 0.1 for 10%
    - ``compounding_freq``: (string) compounding frequency;
      one of the keys of :const:`NUM_BY_FREQ`, e.g. "monthly"
    - ``payment_freq``: (string) payments frequency;
      one of the keys of :const:`NUM_BY_FREQ`, e.g. "monthly"
    - ``num_payments``: (integer) number of payments in the loan
      term

    return the periodic payment amount due to
    amortize the loan into equal payments occurring at the frequency
    ``payment_freq``.
    See the function :func:`freq_to_num` for valid frequncies.

    Notes:

    - https://en.wikipedia.org/wiki/Amortization_calculator
    - https://www.vertex42.com/ExcelArticles/amortization-calculation.html
    """
    P = principal
    I = compute_period_interest_rate(interest_rate, compounding_freq, payment_freq)
    n = num_payments
    if I == 0:
        A = P / n
    else:
        A = P * I / (1 - (1 + I) ** (-n))

    return A


def aggregate_payment_schedules(
    payment_schedules: list[DataFrame],
    start_date: Optional[dt.date] = None,
    end_date: Optional[dt.date] = None,
    freq: Optional[str] = None,
) -> DataFrame:
    """
    Given a list of payment schedules in the form output by any of the
    `summarize` methods in the :mod:`loan` module, do the following.

    1. Concatenate the payment schedules.
    2. Slice to the given start date and end date (inclusive)
    3. Group by payment date, and resample at the given Pandas frequency
       (and not a frequency in :const:`NUM_BY_FREQ`) by summing.

    Return resulting DataFrame with the columns

    - ``"payment_date"``
    - ``"principal_payment"``
    - ``"interest_payment"``
    - ``"fee_payment"``
    - ``"total_payment"``: sum of principal_payment, interest payment, and fee_payment
    - ``"principal_payment_cumsum"``: cumulative sum of principal_payment
    - ``"interest_payment_cumsum"``: cumulative sum of interest payment
    - ``"fee_payment_cumsum"``: cumulative sum of fee_payment

    """
    if not payment_schedules:
        raise ValueError("No payment schedules given to aggregate")

    g = (
        pd.concat(payment_schedules)
        .filter(
            ["payment_date", "principal_payment", "interest_payment", "fee_payment"]
        )
        # Slice
        .set_index("payment_date")
        .loc[start_date:end_date]
        .reset_index()
        .groupby(pd.Grouper(key="payment_date", freq=freq))
        .sum()
        .sort_index()
        .reset_index()
    )

    # Append total payment column
    return (
        g.assign(
            total_payment=lambda x: (
                x.principal_payment + x.interest_payment + x.fee_payment
            )
        )
        .assign(principal_payment_cumsum=lambda x: x.principal_payment.cumsum())
        .assign(interest_payment_cumsum=lambda x: x.interest_payment.cumsum())
        .assign(fee_payment_cumsum=lambda x: x.fee_payment.cumsum())
        .assign(total_payment_cumsum=lambda x: x.total_payment.cumsum())
    )
